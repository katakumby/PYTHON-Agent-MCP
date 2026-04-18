import asyncio
import logging
import os
import sys
from collections.abc import Awaitable, Callable
from typing import Any

import click
import grpc
import uvicorn
from fastapi import FastAPI, Header, Query, Request
from fastapi.responses import JSONResponse, Response
from dotenv import load_dotenv

try:
    from . import patch_a2a_sdk  # noqa: F401
except ImportError:
    import patch_a2a_sdk  # type: ignore  # noqa: F401

from a2a.compat.v0_3 import a2a_v0_3_pb2_grpc
from a2a.compat.v0_3.grpc_handler import CompatGrpcHandler
from a2a.server.request_handlers import DefaultRequestHandler, GrpcHandler
from a2a.server.request_handlers.response_helpers import agent_card_to_dict
from a2a.server.routes import create_jsonrpc_routes, create_rest_routes
from a2a.server.routes.rest_dispatcher import RestDispatcher
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentProvider,
    AgentSkill,
    a2a_pb2_grpc,
)
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from starlette.routing import Route

try:
    from .rest_openapi_models import (
        AgentCardDoc,
        ListTasksResponseDoc,
        SendMessageRequestDoc,
        SendMessageResponseDoc,
        TaskDoc,
        TaskPushNotificationConfigDoc,
        TaskPushNotificationConfigListResponseDoc,
        TaskStateName,
    )
except ImportError:
    from rest_openapi_models import (  # type: ignore
        AgentCardDoc,
        ListTasksResponseDoc,
        SendMessageRequestDoc,
        SendMessageResponseDoc,
        TaskDoc,
        TaskPushNotificationConfigDoc,
        TaskPushNotificationConfigListResponseDoc,
        TaskStateName,
    )

try:
    from .agent import AnalysisAgent
    from .agent_executor import AnalysisAgentExecutor
except ImportError:
    from agent import AnalysisAgent  # type: ignore
    from agent_executor import AnalysisAgentExecutor  # type: ignore


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DEFAULT_A2A_VERSION = '1.0'
A2A_VERSION_HEADER = 'A2A-Version'


class MissingConfigurationError(Exception):
    """Exception for missing required runtime configuration."""


def _resolve_public_host(bind_host: str) -> str:
    configured_host = os.getenv('A2A_AGENT_HOST')
    if configured_host:
        return configured_host

    if bind_host in {'0.0.0.0', '::'}:
        return '127.0.0.1'

    return bind_host


def _validate_ports(
    http_port: int,
    grpc_port: int,
    compat_grpc_port: int,
) -> None:
    ports = [port for port in (http_port, grpc_port, compat_grpc_port) if port]
    if any(port < 0 for port in ports):
        raise ValueError('Ports must be zero or positive integers.')
    if len(ports) != len(set(ports)):
        raise ValueError(
            'HTTP, gRPC, and compatibility gRPC ports must be distinct.'
        )


def _build_supported_interfaces(
    public_host: str,
    http_port: int,
    grpc_port: int,
    compat_grpc_port: int,
) -> list[AgentInterface]:
    http_base_url = f'http://{public_host}:{http_port}'
    supported_interfaces = [
        AgentInterface(
            protocol_binding='JSONRPC',
            protocol_version='1.0',
            url=f'{http_base_url}/a2a/jsonrpc',
        ),
        AgentInterface(
            protocol_binding='HTTP+JSON',
            protocol_version='1.0',
            url=f'{http_base_url}/a2a/rest',
        ),
    ]

    if grpc_port:
        supported_interfaces.append(
            AgentInterface(
                protocol_binding='GRPC',
                protocol_version='1.0',
                url=f'{public_host}:{grpc_port}',
            )
        )

    supported_interfaces.extend(
        [
            AgentInterface(
                protocol_binding='JSONRPC',
                protocol_version='0.3',
                url=f'{http_base_url}/a2a/jsonrpc',
            ),
            AgentInterface(
                protocol_binding='HTTP+JSON',
                protocol_version='0.3',
                url=f'{http_base_url}/a2a/rest',
            ),
        ]
    )

    if compat_grpc_port:
        supported_interfaces.append(
            AgentInterface(
                protocol_binding='GRPC',
                protocol_version='0.3',
                url=f'{public_host}:{compat_grpc_port}',
            )
        )

    return supported_interfaces


def _build_agent_card(
    public_host: str,
    http_port: int,
    grpc_port: int,
    compat_grpc_port: int,
) -> AgentCard:
    http_base_url = f'http://{public_host}:{http_port}'
    input_modes = AnalysisAgent.SUPPORTED_CONTENT_TYPES
    output_modes = ['text', 'task-status']

    capabilities = AgentCapabilities(streaming=True, push_notifications=False)
    skill = AgentSkill(
        id='system_analysis',
        name='System Analysis Tool',
        description='Helps with system analysis and research tasks.',
        tags=['system-analysis', 'research'],
        examples=['What is system analysis?'],
        input_modes=input_modes,
        output_modes=output_modes,
    )

    return AgentCard(
        name='Deep Research Agent',
        description='Helps with deep research and system analysis.',
        provider=AgentProvider(
            organization='Business Agent',
            url=http_base_url,
        ),
        version='1.0.0',
        default_input_modes=input_modes,
        default_output_modes=output_modes,
        capabilities=capabilities,
        skills=[skill],
        supported_interfaces=_build_supported_interfaces(
            public_host=public_host,
            http_port=http_port,
            grpc_port=grpc_port,
            compat_grpc_port=compat_grpc_port,
        ),
    )


def _build_request_handler(agent_card: AgentCard) -> DefaultRequestHandler:
    return DefaultRequestHandler(
        agent_executor=AnalysisAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )


def _streaming_response_docs() -> dict[int | str, dict[str, object]]:
    return {
        200: {
            'description': 'Server-Sent Events stream of A2A updates.',
            'content': {
                'text/event-stream': {
                    'schema': {
                        'type': 'string',
                        'description': (
                            'SSE frames where each `data:` line contains a '
                            'JSON-encoded A2A stream response.'
                        ),
                        'example': (
                            'data: {"statusUpdate":{"taskId":"task-123",'
                            '"contextId":"ctx-123","status":{"state":"'
                            'TASK_STATE_WORKING"}}}\n\n'
                        ),
                    }
                }
            },
        }
    }


def _with_a2a_version(request: Request, a2a_version: str | None) -> Request:
    version = (a2a_version or DEFAULT_A2A_VERSION).strip() or DEFAULT_A2A_VERSION
    header_name = b'a2a-version'
    headers = []
    replaced = False

    for key, value in request.scope.get('headers', []):
        if key.lower() == header_name:
            headers.append((header_name, version.encode('latin-1')))
            replaced = True
        else:
            headers.append((key, value))

    if not replaced:
        headers.append((header_name, version.encode('latin-1')))

    request.scope['headers'] = headers
    if hasattr(request, '_headers'):
        delattr(request, '_headers')
    return request


async def _dispatch_rest_request(
    handler: Callable[[Request], Awaitable[Response | Any]],
    request: Request,
    a2a_version: str,
) -> Response | Any:
    return await handler(_with_a2a_version(request, a2a_version))


def _add_documented_rest_routes(
    app: FastAPI,
    rest_dispatcher: RestDispatcher,
    path_prefix: str,
) -> None:
    rest_tag = 'A2A REST'

    @app.post(
        f'{path_prefix}/message:send',
        tags=[rest_tag],
        summary='Send an A2A message',
        description='Submit a message over the HTTP+JSON binding and wait for the final response.',
        response_model=SendMessageResponseDoc,
    )
    async def rest_message_send(
        payload: SendMessageRequestDoc,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ) -> JSONResponse:
        _ = payload
        return await _dispatch_rest_request(
            rest_dispatcher.on_message_send,
            request,
            a2a_version,
        )

    @app.post(
        f'{path_prefix}/message:stream',
        tags=[rest_tag],
        summary='Send an A2A message with streaming updates',
        description='Submit a message over the HTTP+JSON binding and receive task updates as server-sent events.',
        responses=_streaming_response_docs(),
    )
    async def rest_message_stream(
        payload: SendMessageRequestDoc,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ):
        _ = payload
        return await _dispatch_rest_request(
            rest_dispatcher.on_message_send_stream,
            request,
            a2a_version,
        )

    @app.post(
        f'{path_prefix}/tasks/{{id}}:cancel',
        tags=[rest_tag],
        summary='Cancel an A2A task',
        description='Cancel a running task by id.',
        response_model=TaskDoc,
    )
    async def rest_cancel_task(
        id: str,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ) -> JSONResponse:
        _ = id
        return await _dispatch_rest_request(
            rest_dispatcher.on_cancel_task,
            request,
            a2a_version,
        )

    @app.get(
        f'{path_prefix}/tasks/{{id}}:subscribe',
        tags=[rest_tag],
        summary='Subscribe to an A2A task',
        description='Receive task updates as server-sent events.',
        responses=_streaming_response_docs(),
    )
    async def rest_subscribe_task_get(
        id: str,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ):
        _ = id
        return await _dispatch_rest_request(
            rest_dispatcher.on_subscribe_to_task,
            request,
            a2a_version,
        )

    @app.post(
        f'{path_prefix}/tasks/{{id}}:subscribe',
        tags=[rest_tag],
        summary='Subscribe to an A2A task',
        description='Receive task updates as server-sent events.',
        responses=_streaming_response_docs(),
    )
    async def rest_subscribe_task_post(
        id: str,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ):
        _ = id
        return await _dispatch_rest_request(
            rest_dispatcher.on_subscribe_to_task,
            request,
            a2a_version,
        )

    @app.get(
        f'{path_prefix}/tasks/{{id}}',
        tags=[rest_tag],
        summary='Get A2A task',
        description='REST GET endpoint for fetching a task by id.',
        response_model=TaskDoc,
    )
    async def rest_get_task(
        id: str,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
        historyLength: int | None = Query(
            default=None,
            alias='historyLength',
            ge=0,
        ),
    ) -> JSONResponse:
        _ = (id, historyLength)
        return await _dispatch_rest_request(
            rest_dispatcher.on_get_task,
            request,
            a2a_version,
        )

    @app.get(
        f'{path_prefix}/tasks',
        tags=[rest_tag],
        summary='List A2A tasks',
        description='List tasks for the agent with optional filtering and pagination.',
        response_model=ListTasksResponseDoc,
    )
    async def rest_list_tasks(
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
        contextId: str | None = Query(default=None, alias='contextId'),
        status: TaskStateName | None = Query(default=None),
        pageSize: int | None = Query(
            default=None,
            alias='pageSize',
            ge=1,
        ),
        pageToken: str | None = Query(default=None, alias='pageToken'),
        historyLength: int | None = Query(
            default=None,
            alias='historyLength',
            ge=0,
        ),
        statusTimestampAfter: str | None = Query(
            default=None,
            alias='statusTimestampAfter',
            description='RFC 3339 timestamp filter.',
        ),
        includeArtifacts: bool | None = Query(
            default=None,
            alias='includeArtifacts',
        ),
    ) -> JSONResponse:
        _ = (
            contextId,
            status,
            pageSize,
            pageToken,
            historyLength,
            statusTimestampAfter,
            includeArtifacts,
        )
        return await _dispatch_rest_request(
            rest_dispatcher.list_tasks,
            request,
            a2a_version,
        )

    @app.post(
        f'{path_prefix}/tasks/{{id}}/pushNotificationConfigs',
        tags=[rest_tag],
        summary='Create task push notification config',
        description='Create or replace a push notification config for a task.',
        response_model=TaskPushNotificationConfigDoc,
    )
    async def rest_set_push_notification(
        id: str,
        payload: TaskPushNotificationConfigDoc,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ) -> JSONResponse:
        _ = (id, payload)
        return await _dispatch_rest_request(
            rest_dispatcher.set_push_notification,
            request,
            a2a_version,
        )

    @app.get(
        f'{path_prefix}/tasks/{{id}}/pushNotificationConfigs',
        tags=[rest_tag],
        summary='List task push notification configs',
        description='List push notification configs for a task.',
        response_model=TaskPushNotificationConfigListResponseDoc,
    )
    async def rest_list_push_notifications(
        id: str,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ) -> JSONResponse:
        _ = id
        return await _dispatch_rest_request(
            rest_dispatcher.list_push_notifications,
            request,
            a2a_version,
        )

    @app.get(
        f'{path_prefix}/tasks/{{id}}/pushNotificationConfigs/{{push_id}}',
        tags=[rest_tag],
        summary='Get task push notification config',
        description='Get a push notification config for a task.',
        response_model=TaskPushNotificationConfigDoc,
    )
    async def rest_get_push_notification(
        id: str,
        push_id: str,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ) -> JSONResponse:
        _ = (id, push_id)
        return await _dispatch_rest_request(
            rest_dispatcher.get_push_notification,
            request,
            a2a_version,
        )

    @app.delete(
        f'{path_prefix}/tasks/{{id}}/pushNotificationConfigs/{{push_id}}',
        tags=[rest_tag],
        summary='Delete task push notification config',
        description='Delete a push notification config for a task.',
        response_model=dict[str, object],
    )
    async def rest_delete_push_notification(
        id: str,
        push_id: str,
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ) -> JSONResponse:
        _ = (id, push_id)
        return await _dispatch_rest_request(
            rest_dispatcher.delete_push_notification,
            request,
            a2a_version,
        )

    @app.get(
        f'{path_prefix}/extendedAgentCard',
        tags=[rest_tag],
        summary='Get extended agent card',
        description='Fetch the authenticated extended agent card when enabled.',
        response_model=AgentCardDoc,
    )
    async def rest_get_extended_agent_card(
        request: Request,
        a2a_version: str = Header(
            default=DEFAULT_A2A_VERSION,
            alias=A2A_VERSION_HEADER,
            description='A2A protocol version for this request.',
        ),
    ) -> JSONResponse:
        return await _dispatch_rest_request(
            rest_dispatcher.handle_authenticated_agent_card,
            request,
            a2a_version,
        )


def _add_compat_rest_routes(
    app: FastAPI,
    request_handler: DefaultRequestHandler,
    path_prefix: str,
) -> None:
    compat_routes = create_rest_routes(
        request_handler=request_handler,
        path_prefix=path_prefix,
        enable_v0_3_compat=True,
    )
    for route in compat_routes:
        route_path = getattr(route, 'path', '')
        if '/v1/' in route_path:
            app.routes.append(route)


def _build_app(
    agent_card: AgentCard,
    request_handler: DefaultRequestHandler,
) -> FastAPI:
    rest_dispatcher = RestDispatcher(request_handler=request_handler)
    app = FastAPI(
        title='Deep Research Agent',
        description='A2A server exposing JSON-RPC, HTTP+JSON REST, and gRPC transports.',
        version='1.0.0',
    )

    @app.get(
        '/',
        include_in_schema=False,
    )
    async def root() -> dict[str, str]:
        return {
            'name': agent_card.name,
            'agent_card': AGENT_CARD_WELL_KNOWN_PATH,
            'jsonrpc': '/a2a/jsonrpc',
            'rest': '/a2a/rest',
            'docs': '/docs',
        }

    @app.get(
        AGENT_CARD_WELL_KNOWN_PATH,
        tags=['A2A Discovery'],
        summary='Get agent card',
        description='Returns the published agent card for discovery.',
        response_model=AgentCardDoc,
    )
    async def get_agent_card() -> JSONResponse:
        return JSONResponse(agent_card_to_dict(agent_card))

    _add_documented_rest_routes(
        app=app,
        rest_dispatcher=rest_dispatcher,
        path_prefix='/a2a/rest',
    )
    _add_compat_rest_routes(
        app=app,
        request_handler=request_handler,
        path_prefix='/a2a/rest',
    )

    app.routes.extend(
        create_jsonrpc_routes(
            request_handler=request_handler,
            rpc_url='/a2a/jsonrpc',
            enable_v0_3_compat=True,
        )
    )

    return app


def _build_grpc_server(
    request_handler: DefaultRequestHandler,
    bind_host: str,
    port: int,
    *,
    compat: bool = False,
) -> tuple[grpc.aio.Server, int]:
    server = grpc.aio.server()
    bound_port = server.add_insecure_port(f'{bind_host}:{port}')
    if bound_port == 0:
        raise RuntimeError(
            f'Unable to bind {"compatibility " if compat else ""}gRPC server to {bind_host}:{port}.'
        )

    if compat:
        compat_servicer = CompatGrpcHandler(request_handler)
        a2a_v0_3_pb2_grpc.add_A2AServiceServicer_to_server(
            compat_servicer,
            server,
        )
    else:
        servicer = GrpcHandler(request_handler)
        a2a_pb2_grpc.add_A2AServiceServicer_to_server(servicer, server)

    return server, bound_port


async def _shutdown_grpc_servers(
    *servers: grpc.aio.Server | None,
) -> None:
    for server in servers:
        if server is None:
            continue
        try:
            await asyncio.shield(server.stop(0))
            await asyncio.shield(server.wait_for_termination(timeout=5))
        except Exception:
            logger.exception('Error while shutting down gRPC server')


async def serve(
    host: str,
    http_port: int,
    grpc_port: int,
    compat_grpc_port: int,
) -> None:
    _validate_ports(http_port, grpc_port, compat_grpc_port)

    public_host = _resolve_public_host(host)
    agent_card = _build_agent_card(
        public_host=public_host,
        http_port=http_port,
        grpc_port=grpc_port,
        compat_grpc_port=compat_grpc_port,
    )
    request_handler = _build_request_handler(agent_card)
    app = _build_app(agent_card, request_handler)

    grpc_server = None
    compat_grpc_server = None

    if grpc_port:
        grpc_server, grpc_port = _build_grpc_server(
            request_handler=request_handler,
            bind_host=host,
            port=grpc_port,
            compat=False,
        )
        await grpc_server.start()

    if compat_grpc_port:
        compat_grpc_server, compat_grpc_port = _build_grpc_server(
            request_handler=request_handler,
            bind_host=host,
            port=compat_grpc_port,
            compat=True,
        )
        await compat_grpc_server.start()

    logger.info('Starting Deep Research Agent')
    logger.info(' - Agent card: http://%s:%s%s', public_host, http_port, AGENT_CARD_WELL_KNOWN_PATH)
    logger.info(' - JSON-RPC:   http://%s:%s/a2a/jsonrpc', public_host, http_port)
    logger.info(' - REST:       http://%s:%s/a2a/rest', public_host, http_port)
    logger.info(' - Swagger UI: http://%s:%s/docs', public_host, http_port)
    if grpc_port:
        logger.info(' - gRPC 1.0:   %s:%s', public_host, grpc_port)
    if compat_grpc_port:
        logger.info(' - gRPC 0.3:   %s:%s', public_host, compat_grpc_port)

    uvicorn_server = uvicorn.Server(
        uvicorn.Config(app, host=host, port=http_port)
    )

    try:
        await uvicorn_server.serve()
    finally:
        await _shutdown_grpc_servers(grpc_server, compat_grpc_server)
        grpc_server = None
        compat_grpc_server = None
        await asyncio.sleep(0)


@click.command()
@click.option('--host', 'host', default='localhost', show_default=True)
@click.option('--port', 'http_port', default=10000, show_default=True)
@click.option('--grpc-port', 'grpc_port', default=10001, show_default=True)
@click.option(
    '--compat-grpc-port',
    'compat_grpc_port',
    default=10002,
    show_default=True,
)
def main(
    host: str,
    http_port: int,
    grpc_port: int,
    compat_grpc_port: int,
) -> None:
    """Starts the Deep Research Agent server."""
    try:
        if not os.getenv('CHAT_BASE_URL'):
            raise MissingConfigurationError(
                'CHAT_BASE_URL environment variable not set.'
            )
        if not os.getenv('CHAT_MODEL'):
            raise MissingConfigurationError(
                'CHAT_MODEL environment variable not set.'
            )

        asyncio.run(
            serve(
                host=host,
                http_port=http_port,
                grpc_port=grpc_port,
                compat_grpc_port=compat_grpc_port,
            )
        )
    except MissingConfigurationError as exc:
        logger.error('Error: %s', exc)
        sys.exit(1)
    except Exception:
        logger.exception('An error occurred during server startup')
        sys.exit(1)


if __name__ == '__main__':
    try:
        main(standalone_mode=False)
    except (KeyboardInterrupt, click.Abort):
        logger.info('Shutdown requested.')
        sys.exit(0)
