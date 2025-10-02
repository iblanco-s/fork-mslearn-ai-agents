---
lab:
    title: 'Conectar Agentes de IA a un servidor MCP remoto'
    description: 'Aprende a integrar herramientas del Protocolo de Contexto de Modelo con agentes de IA'
---

# Conectar agentes de IA a herramientas usando el Protocolo de Contexto de Modelo (MCP)

En este ejercicio, construirás un agente que se conecta a un servidor MCP alojado en la nube. El agente utilizará búsqueda potenciada por IA para ayudar a los desarrolladores a encontrar respuestas precisas y en tiempo real de la documentación oficial de Microsoft. Esto es útil para construir asistentes que apoyen a desarrolladores con orientación actualizada sobre herramientas como Azure, .NET y Microsoft 365. El agente utilizará la herramienta `microsoft_docs_search` proporcionada para consultar la documentación y devolver resultados relevantes.

> **Consejo**: El código utilizado en este ejercicio está basado en el repositorio de ejemplo de soporte MCP del servicio de Agentes de IA de Azure. Consulta [demos de Azure OpenAI](https://github.com/retkowsky/Azure-OpenAI-demos/blob/main/Azure%20Agent%20Service/9%20Azure%20AI%20Agent%20service%20-%20MCP%20support.ipynb) o visita [Conectar a servidores del Protocolo de Contexto de Modelo](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/model-context-protocol) para más detalles.

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
    - **Región**: *Selecciona cualquiera de las siguientes ubicaciones soportadas:* \*
      * West US 2
      * West US
      * Norway East
      * Switzerland North
      * UAE North
      * South India

    > \* Algunos recursos de Azure AI están limitados por cuotas de modelo regionales. En el caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Crear** y espera a que se cree tu proyecto.
1. Si se te solicita, despliega un modelo **gpt-4o** utilizando la opción de implementación *Estándar Global* o *Estándar* (dependiendo de la disponibilidad de tu cuota).

    >**Nota**: Si la cuota está disponible, un modelo base GPT-4o puede desplegarse automáticamente al crear tu Agente y proyecto.

1. Cuando se cree tu proyecto, el playground de Agentes se abrirá.

1. En el panel de navegación a la izquierda, selecciona **Información general** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de la página de información general de un proyecto de Azure AI Foundry.](./Media/ai-foundry-project.png)

1. Copia el valor del **endpoint del proyecto de Azure AI Foundry**. Lo usarás para conectarte a tu proyecto en una aplicación cliente.

## Desarrollar un agente que usa herramientas de función MCP

Ahora que has creado tu proyecto en AI Foundry, desarrollemos una aplicación que integre un agente de IA con un servidor MCP.

### Clonar el repositorio que contiene el código de la aplicación

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

    > **Consejo**: A medida que ingresas comandos en el cloudshell, la salida puede ocupar una gran cantidad del búfer de pantalla y el cursor en la línea actual puede quedar oculto. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```
   cd ai-agents/Labfiles/03c-use-agent-tools-with-mcp/Python
   ls -a -l
    ```

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt --pre azure-ai-projects mcp
    ```

    >**Nota:** Puedes ignorar cualquier mensaje de advertencia o error mostrado durante la instalación de la biblioteca.

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación del modelo (que debería ser *gpt-4o*).

1. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Conectar un Agente de IA de Azure a un servidor MCP remoto

En esta tarea, te conectarás a un servidor MCP remoto, prepararás el agente de IA y ejecutarás un prompt del usuario.

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```
   code client.py
    ```

    El archivo se abre en el editor de código.

1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import McpTool, ToolSet, ListSortOrder
    ```

1. Encuentra el comentario **Connect to the agents client** y agrega el siguiente código para conectarte al proyecto de Azure AI usando las credenciales actuales de Azure.

    ```python
   # Connect to the agents client
   agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
   )
    ```

1. Bajo el comentario **Initialize agent MCP tool**, agrega el siguiente código:

    ```python
   # Initialize agent MCP tool
   mcp_tool = McpTool(
        server_label=mcp_server_label,
        server_url=mcp_server_url,
   )
    
   mcp_tool.set_approval_mode("never")
    
   toolset = ToolSet()
   toolset.add(mcp_tool)
    ```

    Este código se conectará al servidor MCP remoto de Microsft Learn Docs. Este es un servicio alojado en la nube que permite a los clientes acceder a información confiable y actualizada directamente de la documentación oficial de Microsoft.

1. Bajo el comentario **Create a new agent** y agrega el siguiente código:

    ```python
   # Create a new agent
   agent = agents_client.create_agent(
        model=model_deployment,
        name="my-mcp-agent",
        instructions="""
        You have access to an MCP server called `microsoft.docs.mcp` - this tool allows you to 
        search through Microsoft's latest official documentation. Use the available MCP tools 
        to answer questions and perform tasks."""
   )
    ```

    En este código, proporcionas instrucciones para el agente y le proporcionas las definiciones de herramientas MCO.

1. Encuentra el comentario **Create thread for communication** y agrega el siguiente código:

    ```python
   # Create thread for communication
   thread = agents_client.threads.create()
   print(f"Created thread, ID: {thread.id}")
    ```

1. Encuentra el comentario **Create a message on the thread** y agrega el siguiente código:

    ```python
   # Create a message on the thread
   prompt = input("\n¿Cómo puedo ayudar?: ")
   message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
   )
   print(f"Created message, ID: {message.id}")
    ```

1. Encuentra el comentario **Create and process agent run in thread with MCP tools** y agrega el siguiente código:

    ```python
   # Create and process agent run in thread with MCP tools
   run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id, toolset=toolset)
   print(f"Created run, ID: {run.id}")
    ```
    
    El Agente de IA invoca automáticamente las herramientas MCP conectadas para procesar la solicitud de prompt. Para ilustrar este proceso, el código proporcionado bajo el comentario **Display run steps and tool calls** mostrará cualquier herramienta invocada del servidor MCP.

1. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado. También puedes cerrar el editor de código (*CTRL+Q*); aunque es posible que desees mantenerlo abierto en caso de que necesites hacer alguna edición al código que agregaste. En cualquier caso, mantén abierto el panel de línea de comandos del cloud shell.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```
   az login
    ```

    **<font color="red">Debes iniciar sesión en Azure - aunque la sesión del cloud shell ya esté autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, simplemente usar *az login* será suficiente. Sin embargo, si tienes suscripciones en varios tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para más detalles.
    
1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresar el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```
   python client.py
    ```

1. Cuando se te solicite, ingresa una solicitud de información técnica como:

    ```
    Dame los comandos de Azure CLI para crear una Azure Container App con una identidad administrada.
    ```

1. Espera a que el agente procese tu prompt, usando el servidor MCP para encontrar una herramienta adecuada para recuperar la información solicitada. Deberías ver una salida similar a la siguiente:

    ```
    Created agent, ID: <<agent-id>>
    MCP Server: mslearn at https://learn.microsoft.com/api/mcp
    Created thread, ID: <<thread-id>>
    Created message, ID: <<message-id>>
    Created run, ID: <<run-id>>
    Run completed with status: RunStatus.COMPLETED
    Step <<step1-id>> status: completed

    Step <<step2-id>> status: completed
    MCP Tool calls:
        Tool Call ID: <<tool-call-id>>
        Type: mcp
        Type: microsoft_docs_search


    Conversation:
    --------------------------------------------------
    ASSISTANT: Puedes usar Azure CLI para crear una Azure Container App con una identidad administrada (ya sea asignada por el sistema o asignada por el usuario). A continuación se muestran los comandos relevantes y el flujo de trabajo:

    ---

    ### **1. Crear un Grupo de Recursos**
    '''azurecli
    az group create --name myResourceGroup --location eastus
    '''
    

    {{continuado...}}

    Al seguir estos pasos, puedes implementar una Azure Container App con identidades administradas asignadas por el sistema o por el usuario para integrarse sin problemas con otros servicios de Azure.
    --------------------------------------------------
    USER: Dame los comandos de Azure CLI para crear una Azure Container App con una identidad administrada.
    --------------------------------------------------
    Deleted agent
    ```

    Observa que el agente pudo invocar la herramienta MCP `microsoft_docs_search` automáticamente para cumplir con la solicitud.

1. Puedes ejecutar la aplicación nuevamente (usando el comando `python client.py`) para solicitar información diferente. En cada caso, el agente intentará encontrar documentación técnica usando la herramienta MCP.

## Limpiar

Ahora que has terminado el ejercicio, deberías eliminar los recursos en la nube que has creado para evitar el uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del grupo de recursos donde desplegaste los recursos del hub utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

