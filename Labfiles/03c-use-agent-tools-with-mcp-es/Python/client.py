import os
from dotenv import load_dotenv

# Agregar referencias


# Cargar variables de entorno desde el archivo .env
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Conectar al cliente de agentes


# Configuración del servidor MCP
mcp_server_url = "https://learn.microsoft.com/api/mcp"
mcp_server_label = "mslearn"

# Inicializar herramienta MCP del agente


# Crear agente con herramienta MCP y procesar ejecución del agente
with agents_client:

    # Crear un nuevo agente
    

    # Registrar información
    print(f"Created agent, ID: {agent.id}")
    print(f"MCP Server: {mcp_tool.server_label} at {mcp_tool.server_url}")

    # Crear hilo para comunicación
    

    # Crear un mensaje en el hilo
    

    # Crear y procesar ejecución del agente en el hilo con herramientas MCP
    
    
    # Verificar el estado de ejecución
    print(f"Run completed with status: {run.status}")
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Mostrar pasos de ejecución y llamadas a herramientas
    run_steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)
    for step in run_steps:
        print(f"Step {step['id']} status: {step['status']}")

        # Verificar si hay llamadas a herramientas en los detalles del paso
        step_details = step.get("step_details", {})
        tool_calls = step_details.get("tool_calls", [])

        if tool_calls:
            # Mostrar los detalles de llamada a herramienta MCP
            print("  MCP Tool calls:")
            for call in tool_calls:
                print(f"    Tool Call ID: {call.get('id')}")
                print(f"    Type: {call.get('type')}")
                print(f"    Type: {call.get('name')}")

        print()  # agregar una línea extra entre pasos

    # Obtener y registrar todos los mensajes
    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    print("\nConversación:")
    print("-" * 50)
    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role.upper()}: {last_text.text.value}")
            print("-" * 50)

    # Limpiar y eliminar el agente una vez que la ejecución haya terminado.
    agents_client.delete_agent(agent.id)
    print("Agente eliminado")
