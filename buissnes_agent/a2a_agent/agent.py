import os
import logging

from collections.abc import AsyncIterable
from typing import Any, Literal

import httpx

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
import litellm
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, create_model, Field
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_tool import McpTool
from langchain_core.tools import BaseTool
import patch_pydantic  # TODO REMOVE THIS LATER
from langfuse import get_client
from langfuse.langchain import CallbackHandler
import json

from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
logger = logging.getLogger(__name__)
memory = MemorySaver()

AGENT_SETTINGS = os.getenv("AGENT_SETTINGS", "Analyst agent")
SSL_VERIFY = bool(os.getenv('SSL_VERIFY', False))
INTERNAL_MCP_URL = os.getenv("INTERNAL_MCP_URL", "http://localhost:8011/mcp")
ATLASSIAN_MCP_URL = os.getenv("ATLASSIAN_MCP_URL", "http://localhost:9002/mcp/")

langfuse = get_client()
langfuse_enabled = False
langfuse_handler = CallbackHandler()
try:
# Verify connection
    if langfuse.auth_check():
        print("Langfuse testscripts is authenticated and ready!")
        langfuse_enabled = True
    else:
        print("Authentication failed. Please check your credentials and host.")
except Exception as e:
    print(f"Failed to connect to Langfuse: {e}")


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""
    
    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str



class McpToolWrapper(BaseTool):
    """Wrapper for Google ADK MCP Tool to be compatible with LangChain."""
    
    mcp_tool: Any = Field(exclude=True)
    
    def __init__(self, mcp_tool: McpTool):
        """Initialize the wrapper."""
        super().__init__(
            name=mcp_tool.name,
            description=mcp_tool.description or "",
            mcp_tool=mcp_tool,
        )
        self.args_schema = self._create_args_schema(mcp_tool)

    def _create_args_schema(self, mcp_tool: McpTool) -> type[BaseModel]:
        """Create Pydantic model from JSON schema."""
        schema = mcp_tool.raw_mcp_tool.inputSchema
        if not schema or "properties" not in schema:
            return create_model(f"{mcp_tool.name}Model")
            
        fields = {}
        required = set(schema.get("required", []))
        
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        }

        for prop_name, prop_def in schema["properties"].items():
            prop_type = type_mapping.get(prop_def.get("type"), Any)
            # Handle simple description
            field_info = {}
            if "description" in prop_def:
                field_info["description"] = prop_def["description"]
            
            is_required = prop_name in required
            if is_required:
                fields[prop_name] = (prop_type, Field(**field_info))
            else:
                fields[prop_name] = (prop_type | None, Field(default=None, **field_info))
                
        return create_model(f"{mcp_tool.name}Model", **fields)

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Run tool synchronously - not implemented for async MCP."""
        raise NotImplementedError("MCP tools must be run asynchronously")

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        """Run tool asynchronously."""
        # Remove None values so we don't send explicit nulls for optional parameters
        # which can cause validation errors on the MCP server side
        clean_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return await self.mcp_tool.run_async(args=clean_kwargs, tool_context=None)


class AnalysisAgent:
    """Analysis Agent - a specialized assistant for currency conversions."""

    FORMAT_INSTRUCTION = (
        'Set response status to input_required if the user needs to provide more information to complete the request.'
        'Set response status to error if there is an error while processing the request.'
        'Set response status to completed if the request is complete.'
    )

    def __init__(self):
        self.model = None
        self.tools = []
        self.graph = None

    async def initialize(self):
        if self.graph: 
            return

        # Connect to Internal MCP
        logger.info(f"Connecting to Knowledge Base MCP at {INTERNAL_MCP_URL}")
        try:
             internal_mcp_params = StreamableHTTPServerParams(url=INTERNAL_MCP_URL)
             internal_tools = await MCPToolset(connection_params=internal_mcp_params).get_tools()
             # Wrap tools
             wrapped_internal_tools = [McpToolWrapper(t) for t in internal_tools]
             self.tools.extend(wrapped_internal_tools)
             logger.info(f"Loaded {len(internal_tools)} tools from Knowledge Base MCP")
        except Exception as e:
            logger.error(f"Failed to load tools from Knowledge Base MCP: {e}")

        # Connect to Atlassian MCP
        logger.info(f"Connecting to Atlassian MCP at {ATLASSIAN_MCP_URL}")
        try:
             atlassian_mcp_params = StreamableHTTPServerParams(url=ATLASSIAN_MCP_URL)
             atlassian_tools = await MCPToolset(connection_params=atlassian_mcp_params).get_tools()
             # Wrap tools
             wrapped_atlassian_tools = [McpToolWrapper(t) for t in atlassian_tools]
             self.tools.extend(wrapped_atlassian_tools)
             logger.info(f"Loaded {len(atlassian_tools)} tools from Atlassian MCP")
        except Exception as e:
            logger.error(f"Failed to load tools from Atlassian MCP: {e}")
        
        agent_config = {}
        if langfuse_enabled:
            prompt = langfuse.get_prompt(AGENT_SETTINGS, label="latest")
            agent_config = {
                "prompt": prompt.prompt,
                "config": {
                    "temperature": prompt.config.get("temperature", 0)
                }
            }
        else:
            with open(os.path.join(os.path.dirname(__file__), 'default_config.json')) as f:
                agent_config = json.load(f)

        self.model = ChatOpenAI(
            model=os.getenv('CHAT_MODEL'),
            openai_api_key=os.getenv('CHAT_API_KEY', 'EMPTY'),
            openai_api_base=os.getenv('CHAT_BASE_URL'),
            temperature=float(agent_config['config']['temperature']),
            tiktoken_model_name=None,
            default_headers=json.loads(os.getenv('DEFAULT_HEADERS')),
        )
        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=agent_config['prompt'],
            response_format=(self.FORMAT_INSTRUCTION, ResponseFormat),
        )

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        if self.graph is None:
            await self.initialize()

        inputs = {'messages': [('user', query)]}
        config = {
            'configurable': {
                'thread_id': context_id
            },
            "callbacks": [langfuse_handler] if langfuse_enabled else [],
            "metadata": {
                "langfuse_session_id": context_id
            }
        }
# 
        async for item in self.graph.astream(inputs, config, stream_mode='values'):
            message = item['messages'][-1]
            if (
                isinstance(message, AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': f"Using tool {message.tool_calls[0]['name']} with args {message.tool_calls[0]['args']}",
                }
            elif isinstance(message, ToolMessage):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Processing tool response..',
                }

        yield self.get_agent_response(config)

    def get_agent_response(self, config):
        current_state = self.graph.get_state(config)
        
        last_ai_message = ""
        messages = current_state.values.get('messages', [])
        for msg in reversed(messages):
            if getattr(msg, 'type', '') == 'human':
                break
            if isinstance(msg, AIMessage) and getattr(msg, 'content', None):
                content = msg.content
                if isinstance(content, str):
                    last_ai_message = content.strip()
                elif isinstance(content, list):
                    texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
                    if not texts:
                        texts = [b for b in content if isinstance(b, str)]
                    last_ai_message = " ".join(filter(None, texts)).strip()
                
                if last_ai_message:
                    break

        structured_response = current_state.values.get('structured_response')
        
        final_content = ""
        is_task_complete = False
        require_user_input = True

        if structured_response and isinstance(structured_response, ResponseFormat):
            final_content = structured_response.message
            
            # Combine if last_ai_message has additional meaningful content
            if last_ai_message and last_ai_message != structured_response.message:
                if structured_response.message in last_ai_message:
                    final_content = last_ai_message
                elif last_ai_message in structured_response.message:
                    final_content = structured_response.message
                else:
                    final_content = f"{last_ai_message}\n\n{structured_response.message}"
            
            if structured_response.status == 'input_required':
                is_task_complete = False
                require_user_input = True
            elif structured_response.status == 'error':
                is_task_complete = False
                require_user_input = True
            elif structured_response.status == 'completed':
                is_task_complete = True
                require_user_input = False
                
            return {
                'is_task_complete': is_task_complete,
                'require_user_input': require_user_input,
                'content': final_content,
            }
            
        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': last_ai_message or (
                'We are unable to process your request at the moment. '
                'Please try again.'
            ),
        }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
