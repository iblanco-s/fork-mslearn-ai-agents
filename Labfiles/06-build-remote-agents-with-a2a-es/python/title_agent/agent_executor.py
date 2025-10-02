""" Agente de Azure AI Foundry que genera un título """

from a2a.server.events.event_queue import EventQueue
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.tasks import TaskUpdater
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, Part, TaskState
from title_agent.agent import TitleAgent, create_foundry_title_agent

class FoundryAgentExecutor(AgentExecutor):

    def __init__(self, card: AgentCard):
        self._card = card
        self._foundry_agent: TitleAgent | None = None

    async def _get_or_create_agent(self) -> TitleAgent:
        if not self._foundry_agent:
            self._foundry_agent = await create_foundry_title_agent()
        return self._foundry_agent

    async def _process_request(self, message_parts: list[Part], context_id: str, task_updater: TaskUpdater) -> None:
        # Procesar una solicitud del usuario a través del agente de Foundry

        try:
            # Recuperar mensaje de las partes A2A
            user_message = message_parts[0].root.text

            # Obtener el agente de título


            # Actualizar el estado de la tarea
            

            # Ejecutar la conversación del agente
            

            # Actualizar la tarea con las respuestas
            

            # Marcar la tarea como completa
            

        except Exception as e:
            print(f'Agente de Título: Error procesando solicitud - {e}')
            await task_updater.failed(
                message=new_agent_text_message("El Agente de Título falló al procesar la solicitud.", 
                context_id=context_id)
            )

    async def execute(self, context: RequestContext, event_queue: EventQueue,):
       
        # Crear actualizador de tareas
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.submit()

        # Comenzar a trabajar
        await updater.start_work()

        # Procesar la solicitud
        

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        print(f'Agente de Título: Cancelando ejecución para contexto {context.context_id}')

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.failed(
            message=new_agent_text_message('Tarea cancelada por el usuario', context_id=context.context_id)
        )

def create_foundry_agent_executor(card: AgentCard) -> FoundryAgentExecutor:
    return FoundryAgentExecutor(card)


