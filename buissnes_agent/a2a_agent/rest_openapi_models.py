from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OpenAPIModel(BaseModel):
    model_config = ConfigDict(extra='allow')


class RoleName(str, Enum):
    ROLE_USER = 'ROLE_USER'
    ROLE_AGENT = 'ROLE_AGENT'


class TaskStateName(str, Enum):
    TASK_STATE_UNSPECIFIED = 'TASK_STATE_UNSPECIFIED'
    TASK_STATE_SUBMITTED = 'TASK_STATE_SUBMITTED'
    TASK_STATE_WORKING = 'TASK_STATE_WORKING'
    TASK_STATE_COMPLETED = 'TASK_STATE_COMPLETED'
    TASK_STATE_FAILED = 'TASK_STATE_FAILED'
    TASK_STATE_CANCELED = 'TASK_STATE_CANCELED'
    TASK_STATE_INPUT_REQUIRED = 'TASK_STATE_INPUT_REQUIRED'
    TASK_STATE_REJECTED = 'TASK_STATE_REJECTED'
    TASK_STATE_AUTH_REQUIRED = 'TASK_STATE_AUTH_REQUIRED'


class ProtocolBindingName(str, Enum):
    JSONRPC = 'JSONRPC'
    HTTP_JSON = 'HTTP+JSON'
    GRPC = 'GRPC'


class PartDoc(OpenAPIModel):
    text: str | None = None
    raw: str | None = Field(
        default=None,
        description='Base64-encoded binary payload.',
    )
    url: str | None = None
    data: Any | None = None
    metadata: dict[str, Any] | None = None
    filename: str | None = None
    mediaType: str | None = None


class MessageDoc(OpenAPIModel):
    messageId: str
    contextId: str | None = None
    taskId: str | None = None
    role: RoleName
    parts: list[PartDoc]
    metadata: dict[str, Any] | None = None
    extensions: list[str] | None = None
    referenceTaskIds: list[str] | None = None


class AuthenticationInfoDoc(OpenAPIModel):
    scheme: str | None = None
    credentials: str | None = None


class TaskPushNotificationConfigDoc(OpenAPIModel):
    tenant: str | None = None
    id: str | None = None
    taskId: str | None = None
    url: str | None = None
    token: str | None = None
    authentication: AuthenticationInfoDoc | None = None


class SendMessageConfigurationDoc(OpenAPIModel):
    acceptedOutputModes: list[str] | None = None
    taskPushNotificationConfig: TaskPushNotificationConfigDoc | None = None
    historyLength: int | None = None
    returnImmediately: bool | None = None


class ArtifactDoc(OpenAPIModel):
    artifactId: str
    name: str | None = None
    description: str | None = None
    parts: list[PartDoc]
    metadata: dict[str, Any] | None = None
    extensions: list[str] | None = None


class TaskStatusDoc(OpenAPIModel):
    state: TaskStateName
    message: MessageDoc | None = None
    timestamp: str | None = Field(
        default=None,
        description='RFC 3339 timestamp.',
    )


class TaskDoc(OpenAPIModel):
    id: str
    contextId: str
    status: TaskStatusDoc
    artifacts: list[ArtifactDoc] | None = None
    history: list[MessageDoc] | None = None
    metadata: dict[str, Any] | None = None


class TaskStatusUpdateEventDoc(OpenAPIModel):
    taskId: str
    contextId: str
    status: TaskStatusDoc
    metadata: dict[str, Any] | None = None


class TaskArtifactUpdateEventDoc(OpenAPIModel):
    taskId: str
    contextId: str
    artifact: ArtifactDoc
    append: bool | None = None
    lastChunk: bool | None = None
    metadata: dict[str, Any] | None = None


class StreamResponseDoc(OpenAPIModel):
    task: TaskDoc | None = None
    message: MessageDoc | None = None
    statusUpdate: TaskStatusUpdateEventDoc | None = None
    artifactUpdate: TaskArtifactUpdateEventDoc | None = None


class SendMessageRequestDoc(OpenAPIModel):
    tenant: str | None = None
    message: MessageDoc
    configuration: SendMessageConfigurationDoc | None = None
    metadata: dict[str, Any] | None = None


class SendMessageResponseDoc(OpenAPIModel):
    task: TaskDoc | None = None
    message: MessageDoc | None = None


class ListTasksResponseDoc(OpenAPIModel):
    tasks: list[TaskDoc]
    nextPageToken: str | None = None
    pageSize: int | None = None
    totalSize: int | None = None


class TaskPushNotificationConfigListResponseDoc(OpenAPIModel):
    configs: list[TaskPushNotificationConfigDoc]
    nextPageToken: str | None = None


class AgentProviderDoc(OpenAPIModel):
    organization: str | None = None
    url: str | None = None


class AgentCapabilitiesDoc(OpenAPIModel):
    streaming: bool | None = None
    pushNotifications: bool | None = None
    stateTransitionHistory: bool | None = None
    extensions: list[str] | None = None
    authenticatedExtendedCard: bool | None = None


class AgentSkillDoc(OpenAPIModel):
    id: str
    name: str
    description: str | None = None
    tags: list[str] | None = None
    examples: list[str] | None = None
    inputModes: list[str] | None = None
    outputModes: list[str] | None = None


class AgentInterfaceDoc(OpenAPIModel):
    url: str
    protocolBinding: ProtocolBindingName
    protocolVersion: str


class AdditionalInterfaceDoc(OpenAPIModel):
    transport: ProtocolBindingName
    url: str


class AgentCardDoc(OpenAPIModel):
    name: str
    description: str
    supportedInterfaces: list[AgentInterfaceDoc]
    provider: AgentProviderDoc | None = None
    version: str
    documentationUrl: str | None = None
    capabilities: AgentCapabilitiesDoc
    defaultInputModes: list[str]
    defaultOutputModes: list[str]
    skills: list[AgentSkillDoc]
    iconUrl: str | None = None

    # Legacy compatibility fields intentionally documented as optional because
    # the discovery endpoint serves a dual-shape card for older inspectors.
    url: str | None = None
    preferredTransport: ProtocolBindingName | None = None
    protocolVersion: str | None = None
    additionalInterfaces: list[AdditionalInterfaceDoc] | None = None
