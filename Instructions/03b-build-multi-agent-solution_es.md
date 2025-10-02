---
lab:
    title: 'Desarrollar una solución multi-agente con Azure AI Foundry'
    description: 'Aprende a configurar múltiples agentes para colaborar usando el Servicio de Agentes de Azure AI Foundry'
---

# Desarrollar una solución multi-agente

En este ejercicio, crearás un proyecto que orquesta múltiples agentes de IA usando el Servicio de Agentes de Azure AI Foundry. Diseñarás una solución de IA que asiste con el triaje de tickets. Los agentes conectados evaluarán la prioridad del ticket, sugerirán una asignación de equipo y determinarán el nivel de esfuerzo requerido para completar el ticket. ¡Comencemos!

> **Consejo**: El código utilizado en este ejercicio está basado en el SDK de Azure AI Foundry para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas de cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos para completar.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Ayuda** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./Media/ai-foundry-home.png)

1. En la página de inicio, selecciona **Crear un agente**.
1. Cuando se te solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Opciones avanzadas**.
1. Confirma las siguientes configuraciones para tu proyecto:
    - **Recurso de Azure AI Foundry**: *Un nombre válido para tu recurso de Azure AI Foundry*
    - **Suscripción**: *Tu suscripción de Azure*
    - **Grupo de recursos**: *Crea o selecciona un grupo de recursos*
    - **Región**: *Selecciona cualquiera **recomendada por AI Foundry***\*

    > \* Algunos recursos de Azure AI están limitados por cuotas de modelo regionales. En el caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Crear** y espera a que se cree tu proyecto.
1. Si se te solicita, despliega un modelo **gpt-4o** utilizando la opción de implementación *Estándar Global* o *Estándar* (dependiendo de la disponibilidad de tu cuota).

    >**Nota**: Si la cuota está disponible, un modelo base GPT-4o puede desplegarse automáticamente al crear tu Agente y proyecto.

1. Cuando se cree tu proyecto, el playground de Agentes se abrirá.

1. En el panel de navegación a la izquierda, selecciona **Información general** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de la página de información general de un proyecto de Azure AI Foundry.](./Media/ai-foundry-project.png)

1. Copia los valores del **endpoint del proyecto de Azure AI Foundry** a un bloc de notas, ya que los usarás para conectarte a tu proyecto en una aplicación cliente.

## Crear una aplicación cliente de Agente de IA

Ahora estás listo para crear una aplicación cliente que define los agentes e instrucciones. Se te ha proporcionado algo de código en un repositorio de GitHub.

### Preparar el entorno

1. Abre una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego en la nueva pestaña, navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con tus credenciales de Azure si se te solicita.

    Cierra cualquier notificación de bienvenida para ver la página de inicio del portal de Azure.

1. Usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno ***PowerShell*** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puedes redimensionar o maximizar este panel para facilitar el trabajo.

    > **Nota**: Si has creado previamente un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Configuración**, selecciona **Ir a la versión Clásica** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pega como texto sin formato):

    ```
   rm -r ai-agents -f
   git clone https://github.com/MicrosoftLearning/mslearn-ai-agents ai-agents
    ```

    > **Consejo**: A medida que ingresas comandos en el cloud shell, la salida puede ocupar una gran cantidad del búfer de pantalla y el cursor en la línea actual puede quedar oculto. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Cuando el repositorio haya sido clonado, ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```
   cd ai-agents/Labfiles/03b-build-multi-agent-solution/Python
   ls -a -l
    ```

    Los archivos proporcionados incluyen código de aplicación y un archivo para configuraciones.

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry), y el marcador de posición **your_model_deployment** con el nombre que asignaste a tu implementación del modelo gpt-4o (que por defecto es `gpt-4o`).

1. Después de haber reemplazado los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Crear agentes de IA

Ahora estás listo para crear los agentes para tu solución multi-agente! ¡Comencemos!

1. Ingresa el siguiente comando para editar el archivo **agent_triage.py**:

    ```
   code agent_triage.py
    ```

1. Revisa el código en el archivo, observando que contiene cadenas de texto para cada nombre de agente e instrucciones.

1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás:

    ```python
   # Add references
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import ConnectedAgentTool, MessageRole, ListSortOrder, ToolSet, FunctionTool
   from azure.identity import DefaultAzureCredential
    ```

1. Observa que se ha proporcionado el código para cargar el endpoint del proyecto y el nombre del modelo desde tus variables de entorno.

1. Encuentra el comentario **Connect to the agents client**, y agrega el siguiente código para crear un AgentsClient conectado a tu proyecto:

    ```python
   # Connect to the agents client
   agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True, 
            exclude_managed_identity_credential=True
        ),
   )
    ```

    Ahora agregarás código que usa el AgentsClient para crear múltiples agentes, cada uno con un rol específico en el procesamiento de un ticket de soporte.

    > **Consejo**: Al agregar código subsecuente, asegúrate de mantener el nivel de indentación correcto bajo la declaración `using agents_client:`.

1. Encuentra el comentario **Create an agent to prioritize support tickets**, e ingresa el siguiente código (teniendo cuidado de mantener el nivel de indentación correcto):

    ```python
   # Create an agent to prioritize support tickets
   priority_agent_name = "priority_agent"
   priority_agent_instructions = """
   Assess how urgent a ticket is based on its description.

   Respond with one of the following levels:
   - High: User-facing or blocking issues
   - Medium: Time-sensitive but not breaking anything
   - Low: Cosmetic or non-urgent tasks

   Only output the urgency level and a very brief explanation.
   """

   priority_agent = agents_client.create_agent(
        model=model_deployment,
        name=priority_agent_name,
        instructions=priority_agent_instructions
   )
    ```

1. Encuentra el comentario **Create an agent to assign tickets to the appropriate team**, e ingresa el siguiente código:

    ```python
   # Create an agent to assign tickets to the appropriate team
   team_agent_name = "team_agent"
   team_agent_instructions = """
   Decide which team should own each ticket.

   Choose from the following teams:
   - Frontend
   - Backend
   - Infrastructure
   - Marketing

   Base your answer on the content of the ticket. Respond with the team name and a very brief explanation.
   """

   team_agent = agents_client.create_agent(
        model=model_deployment,
        name=team_agent_name,
        instructions=team_agent_instructions
   )
    ```

1. Encuentra el comentario **Create an agent to estimate effort for a support ticket**, e ingresa el siguiente código:

    ```python
   # Create an agent to estimate effort for a support ticket
   effort_agent_name = "effort_agent"
   effort_agent_instructions = """
   Estimate how much work each ticket will require.

   Use the following scale:
   - Small: Can be completed in a day
   - Medium: 2-3 days of work
   - Large: Multi-day or cross-team effort

   Base your estimate on the complexity implied by the ticket. Respond with the effort level and a brief justification.
   """

   effort_agent = agents_client.create_agent(
        model=model_deployment,
        name=effort_agent_name,
        instructions=effort_agent_instructions
   )
    ```

    Hasta ahora, has creado tres agentes; cada uno de los cuales tiene un rol específico en el triaje de un ticket de soporte. Ahora creemos objetos ConnectedAgentTool para cada uno de estos agentes para que puedan ser usados por otros agentes.

1. Encuentra el comentario **Create connected agent tools for the support agents**, e ingresa el siguiente código:

    ```python
   # Create connected agent tools for the support agents
   priority_agent_tool = ConnectedAgentTool(
        id=priority_agent.id, 
        name=priority_agent_name, 
        description="Assess the priority of a ticket"
   )
    
   team_agent_tool = ConnectedAgentTool(
        id=team_agent.id, 
        name=team_agent_name, 
        description="Determines which team should take the ticket"
   )
    
   effort_agent_tool = ConnectedAgentTool(
        id=effort_agent.id, 
        name=effort_agent_name, 
        description="Determines the effort required to complete the ticket"
   )
    ```

    Ahora estás listo para crear un agente principal que coordinará el proceso de triaje de tickets, usando los agentes conectados según sea necesario.

1. Encuentra el comentario **Create an agent to triage support ticket processing by using connected agents**, e ingresa el siguiente código:

    ```python
   # Create an agent to triage support ticket processing by using connected agents
   triage_agent_name = "triage-agent"
   triage_agent_instructions = """
   Triage the given ticket. Use the connected tools to determine the ticket's priority, 
   which team it should be assigned to, and how much effort it may take.
   """

   triage_agent = agents_client.create_agent(
        model=model_deployment,
        name=triage_agent_name,
        instructions=triage_agent_instructions,
        tools=[
            priority_agent_tool.definitions[0],
            team_agent_tool.definitions[0],
            effort_agent_tool.definitions[0]
        ]
   )
    ```

    Ahora que has definido un agente principal, puedes enviarle un prompt y hacer que use los otros agentes para hacer el triaje de un problema de soporte.

1. Encuentra el comentario **Use the agents to triage a support issue**, e ingresa el siguiente código:

    ```python
   # Use the agents to triage a support issue
   print("Creating agent thread.")
   thread = agents_client.threads.create()  

   # Create the ticket prompt
   prompt = input("\n¿Cuál es el problema de soporte que necesitas resolver?: ")
    
   # Send a prompt to the agent
   message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=prompt,
   )   
    
   # Run the thread usng the primary agent
   print("\nProcessing agent thread. Please wait.")
   run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=triage_agent.id)
        
   if run.status == "failed":
        print(f"Run failed: {run.last_error}")

   # Fetch and display messages
   messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}:\n{last_msg.text.value}\n")
   
    ```

1. Encuentra el comentario **Clean up**, e ingresa el siguiente código para eliminar los agentes cuando ya no sean necesarios:

    ```python
   # Clean up
   print("Cleaning up agents:")
   agents_client.delete_agent(triage_agent.id)
   print("Deleted triage agent.")
   agents_client.delete_agent(priority_agent.id)
   print("Deleted priority agent.")
   agents_client.delete_agent(team_agent.id)
   print("Deleted team agent.")
   agents_client.delete_agent(effort_agent.id)
   print("Deleted effort agent.")
    ```
    

1. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. Puedes mantenerlo abierto (en caso de que necesites editar el código para corregir errores) o usar el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Iniciar sesión en Azure y ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tus agentes de IA colaboran.

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```
   az login
    ```

    **<font color="red">Debes iniciar sesión en Azure - aunque la sesión del cloud shell ya esté autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, simplemente usar *az login* será suficiente. Sin embargo, si tienes suscripciones en varios tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para más detalles.

1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresar el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```
   python agent_triage.py
    ```

1. Ingresa un prompt, como `Los usuarios no pueden restablecer su contraseña desde la aplicación móvil.`

    Después de que los agentes procesen el prompt, deberías ver una salida similar a la siguiente:

    ```output
    Creating agent thread.
    Processing agent thread. Please wait.

    MessageRole.USER:
    Los usuarios no pueden restablecer su contraseña desde la aplicación móvil.

    MessageRole.AGENT:
    ### Evaluación del Ticket

    - **Prioridad:** Alta — Este problema bloquea a los usuarios de restablecer sus contraseñas, limitando el acceso a sus cuentas.
    - **Equipo Asignado:** Equipo Frontend — El problema reside en la interfaz de usuario o funcionalidad de la aplicación móvil.
    - **Esfuerzo Requerido:** Mediano — Resolver este problema implica identificar la causa raíz, potencialmente actualizar la funcionalidad de la aplicación móvil, revisar la integración API/backend, y realizar pruebas para asegurar compatibilidad entre plataformas Android/iOS.

    Cleaning up agents:
    Deleted triage agent.
    Deleted priority agent.
    Deleted team agent.
    Deleted effort agent.
    ```

    Puedes intentar modificar el prompt usando un escenario de ticket diferente para ver cómo colaboran los agentes. Por ejemplo, "Investigar errores 502 ocasionales del endpoint de búsqueda."

## Limpiar

Si has terminado de explorar el Servicio de Agentes de IA de Azure, deberías eliminar los recursos que has creado en este ejercicio para evitar costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o vuelve a abrir el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde desplegaste los recursos utilizados en este ejercicio.

1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.

1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

