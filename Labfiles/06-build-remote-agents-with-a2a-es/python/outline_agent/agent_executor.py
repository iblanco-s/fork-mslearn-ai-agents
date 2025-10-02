""" Agente de Azure AI Foundry que genera un esquema """

from a2a.server.events.event_queue import EventQueue
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.tasks import TaskUpdater
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, Part, TaskState
from outline_agent.agent import OutlineAgent, create_foundry_outline_agent

class FoundryAgentExecutor(AgentExecutor):

    def __init__(self, card: AgentCard):
        self._card = card
        self._foundry_agent: OutlineAgent | None = None

    async def _get_or_create_agent(self) -> OutlineAgent:
        if not self._foundry_agent:
            self._foundry_agent = await create_foundry_outline_agent()
        return self._foundry_agent

    async def _process_request(self, message_parts: list[Part], context_id: str, task_updater: TaskUpdater) -> None:
        # Procesar una solicitud del usuario a través del agente de Foundry

        try:
            # Recuperar mensaje de las partes A2A
            user_message = message_parts[0].root.text

            # Obtener el agente de esquema
            agent = await self._get_or_create_agent()

            # Actualizar el estado de la tarea
            await task_updater.update_status(
                TaskState.working,
                message=new_agent_text_message('El Agente de Esquema está procesando tu solicitud...', context_id=context_id),
            )

            # Ejecutar la conversación del agente
            responses = await agent.run_conversation(user_message)

            # Actualizar la tarea con las respuestas
            for response in responses:
                await task_updater.update_status(
                    TaskState.working,
                    message=new_agent_text_message(response, context_id=context_id),
                )

            # Marcar la tarea como completa
            final_message = responses[-1] if responses else 'Tarea completada.'
            await task_updater.complete(
                message=new_agent_text_message(final_message, context_id=context_id)
            )

        except Exception as e:
            print(f'Agente de Esquema: Error procesando solicitud - {e}')
            await task_updater.failed(
                message=new_agent_text_message("El Agente de Esquema falló al procesar la solicitud.", 
                context_id=context_id)
            )

    async def execute(self, context: RequestContext, event_queue: EventQueue,):
       
        # Crear actualizador de tareas
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.submit()

        # Comenzar a trabajar
        await updater.start_work()

        # Procesar la solicitud
        await self._process_request(context.message.parts, context.context_id, updater)

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        print(f'Agente de Esquema: Cancelando ejecución para contexto {context.context_id}')

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.failed(
            message=new_agent_text_message('Tarea cancelada por el usuario', context_id=context.context_id)
        )

def create_foundry_agent_executor(card: AgentCard) -> FoundryAgentExecutor:
    return FoundryAgentExecutor(card)


