import asyncio
import json
import os
import time
import uuid
import httpx

from typing import Any, Callable
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FunctionTool, MessageRole
from collections.abc import Callable
from dotenv import load_dotenv
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
    SendMessageSuccessResponse,
    Task,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
)

load_dotenv()

TaskCallbackArg = Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
TaskUpdateCallback = Callable[[TaskCallbackArg, AgentCard], Task]


class RemoteAgentConnections:
    """Una clase para mantener las conexiones a los agentes remotos."""

    def __init__(self, agent_card: AgentCard, agent_url: str):
        self._httpx_client = httpx.AsyncClient(timeout=30)
        self.agent_client = A2AClient(self._httpx_client, agent_card, url=agent_url)
        self.card = agent_card

    def get_agent(self) -> AgentCard:
        return self.card

    async def send_message(self, message_request: SendMessageRequest) -> SendMessageResponse:
        return await self.agent_client.send_message(message_request)

class RoutingAgent:

    def __init__(self,task_callback: TaskUpdateCallback | None = None):

        self.task_callback = task_callback
        self.remote_agent_connections: dict[str, RemoteAgentConnections] = {}
        self.cards: dict[str, AgentCard] = {}
        self.agents: str = ''
        
        # Inicializar el cliente de Agentes de IA de Azure
        self.agents_client = AgentsClient(
            endpoint=os.environ["PROJECT_ENDPOINT"],
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            )
        )

        self.azure_agent = None
        self.current_thread = None


    @classmethod
    async def create(cls, remote_agent_addresses: list[str], task_callback: TaskUpdateCallback | None = None) -> 'RoutingAgent':
        """Crear e inicializar asincrónicamente una instancia del RoutingAgent."""
        instance = cls(task_callback)
        await instance._async_init_components(remote_agent_addresses)
        return instance
    

    def list_remote_agents(self) -> str:
        if not self.remote_agent_connections:
            return "[]"

        lines = []
        for card in self.cards.values():
            lines.append(f"{card.name}: {card.description}")

        return "[\n  " + ",\n  ".join(lines) + "\n]"
    

    async def _async_init_components(self, remote_agent_addresses: list[str]) -> None:
        """Parte asíncrona de la inicialización."""

        # Usar un solo httpx.AsyncClient para todas las resoluciones de tarjetas para eficiencia
        async with httpx.AsyncClient(timeout=30) as client:
            for address in remote_agent_addresses:
                card_resolver = A2ACardResolver(client, address)
                try:
                    card = await card_resolver.get_agent_card()

                    remote_connection = RemoteAgentConnections(agent_card=card, agent_url=address)
                    self.remote_agent_connections[card.name] = remote_connection
                    self.cards[card.name] = card

                except httpx.ConnectError as e:
                    print( f'ERROR: Falló al obtener tarjeta de agente de {address}: {e}')
                except Exception as e:  # Capturar otros errores potenciales
                    print(f'ERROR: Falló al inicializar conexión para {address}: {e}')
            print(f"Agentes remotos encontrados: {self.list_remote_agents()}")

    
    async def send_message(self, agent_name: str, task: str):
        # Envía una tarea al agente remoto.

        if agent_name not in self.remote_agent_connections:
            raise ValueError(f'Agente {agent_name} no encontrado')
        
        # Recuperar el cliente A2A del agente remoto usando el nombre del agente
        

        if not client:
            raise ValueError(f'Cliente no disponible para {agent_name}')
        
        message_id = str(uuid.uuid4())

        # Construir la carga útil para enviar al agente remoto
        
        
        # Envolver la carga útil en un objeto SendMessageRequest
        

        # Enviar el mensaje al cliente del agente remoto y esperar la respuesta
        
        
        if not isinstance(send_response.root, SendMessageSuccessResponse):
            print('respuesta no exitosa recibida. Abortando obtener tarea ')
            return

        if not isinstance(send_response.root.result, Task):
            print('respuesta no es tarea recibida. Abortando obtener tarea ')
            return

        return send_response.root.result


    def create_agent(self):
        # Crear una instancia de Agente de IA de Azure
        
        try:
            # Crear Agente de IA de Azure con la función send_message
            functions = FunctionTool({self.send_message})
            self.azure_agent = self.agents_client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="routing-agent",
                instructions=f"""
                Eres un Delegador de Enrutamiento experto que ayuda a los usuarios con solicitudes.

                Tu rol:
                - Delegar consultas de usuarios a agentes remotos especializados apropiados
                - Proporcionar respuestas claras y útiles a los usuarios

                Agentes Disponibles: {self.list_remote_agents()}

                Siempre sé útil y enruta las solicitudes al agente más apropiado.""",
                tools=functions.definitions
            )

            # Crear un hilo para conversación
            self.current_thread = self.agents_client.threads.create()

            return self.azure_agent
            
        except Exception as e:
            print(f"Error creando agente de IA de Azure: {e}")
            raise

    async def process_user_message(self, user_message: str) -> str:

        if not hasattr(self, 'azure_agent') or not self.azure_agent:
            return "Agente de IA de Azure no inicializado. Por favor asegúrate de que el agente esté creado correctamente."
        
        if not hasattr(self, 'current_thread') or not self.current_thread:
            return "Hilo de IA de Azure no inicializado. Por favor asegúrate de que el agente esté creado correctamente."
        
        try:
            # Crear mensaje en el hilo
            self.agents_client.messages.create(
                thread_id=self.current_thread.id, 
                role=MessageRole.User, 
                content=user_message
            )

            # Crear y ejecutar el agente
            run = self.agents_client.runs.create(
                thread_id=self.current_thread.id, 
                agent_id=self.azure_agent.id
            )
            
            # Necesita esperar la función send_message
            while run.status in ["queued", "in_progress", "requires_action"]:
                time.sleep(1)
                run = self.agents_client.runs.get(thread_id=self.current_thread.id, run_id=run.id)

                if run.status == "requires_action":
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = []
                    
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        if function_name == "send_message":
                            try:
                                result = await self.send_message(agent_name=function_args["agent_name"], task=function_args["task"])
                                output = json.dumps(result.model_dump() if hasattr(result, 'model_dump') else str(result))

                            except Exception as e:
                                output = json.dumps({"error": str(e)})
                        else:
                            output = json.dumps({"error": f"Función desconocida: {function_name}"})
                        
                        tool_outputs.append({"tool_call_id": tool_call.id,  "output": output})
                
                    # Enviar las salidas de herramientas
                    self.agents_client.runs.submit_tool_outputs(
                        thread_id=self.current_thread.id, run_id=run.id, tool_outputs=tool_outputs
                    )

            if run.status == "failed":
                error_info = f"Error de ejecución: {run.last_error}"
                print(error_info)
                return f"Error procesando solicitud: {error_info}"

            # Devolver la respuesta
            messages = self.agents_client.messages.list(thread_id=self.current_thread.id, order=ListSortOrder.DESCENDING)
            for msg in messages:
                if msg.role == MessageRole.AGENT and msg.text_messages:
                    last_text = msg.text_messages[-1]
                    return last_text.text.value
            
            return "No se recibió respuesta del agente."
            
        except Exception as e:
            error_msg = f"Error en process_user_message: {e}"
            print(error_msg)
            return f"Ocurrió un error al procesar tu mensaje."


async def _get_initialized_routing_agent_sync() -> RoutingAgent:

    async def _async_main() -> RoutingAgent:
        routing_agent_instance = await RoutingAgent.create(
            remote_agent_addresses=[
                f"http://{os.environ["SERVER_URL"]}:{os.environ["TITLE_AGENT_PORT"]}",
                f"http://{os.environ["SERVER_URL"]}:{os.environ["OUTLINE_AGENT_PORT"]}",
            ]
        )
        # Crear el agente de IA de Azure
        routing_agent_instance.create_agent()
        return routing_agent_instance

    try:
        return asyncio.run(_async_main())
    except RuntimeError as e:
        raise

# Inicializar el agente de enrutamiento
routing_agent = _get_initialized_routing_agent_sync()

