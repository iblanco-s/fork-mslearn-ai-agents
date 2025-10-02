---
lab:
    title: 'Usar herramientas de servidor MCP local con agentes de IA'
    description: 'Aprende a configurar un servidor MCP local y conectarlo con agentes de IA de Azure'
---

# Conectar agentes de IA a herramientas usando el Protocolo de Contexto de Modelo (MCP)

En este ejercicio, crearás un agente que puede conectarse a un servidor MCP y descubrir automáticamente funciones invocables.

Construirás un agente simple de evaluación de inventario para un minorista de cosméticos. Usando el servidor MCP, el agente podrá recuperar información sobre el inventario y hacer sugerencias de reabastecimiento o liquidación.

> **Consejo**: El código utilizado en este ejercicio está basado en los SDKs de Azure AI Foundry y MCP para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET. Consulta [Bibliotecas de cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) y [SDK de MCP para C#](https://modelcontextprotocol.github.io/csharp-sdk/api/ModelContextProtocol.html) para más detalles.

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

1. Copia el valor del **endpoint del proyecto de Azure AI Foundry** a un bloc de notas, ya que lo usarás para conectarte a tu proyecto en una aplicación cliente.

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
   cd ai-agents/Labfiles/03d-use-local-mcp-server-tools/Python
   ls -a -l
    ```

    Los archivos proporcionados incluyen el código de la aplicación cliente y del servidor. El Protocolo de Contexto de Modelo proporciona una forma estandarizada de conectar modelos de IA con diferentes fuentes de datos y herramientas. Separamos `client.py` y `server.py` para mantener la lógica del agente y las definiciones de herramientas modulares y simular una arquitectura del mundo real.
    
    `server.py` define las herramientas que el agente puede usar, simulando servicios backend o lógica de negocio. 
    `client.py` maneja la configuración del agente de IA, los prompts del usuario y la llamada a las herramientas cuando sea necesario.

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects mcp
    ```

    >**Nota:** Puedes ignorar cualquier mensaje de advertencia o error mostrado durante la instalación de la biblioteca.

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación del modelo (que debería ser *gpt-4o*).

1. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Implementar un servidor MCP

Un servidor MCP (Model Context Protocol) es un componente que aloja herramientas invocables. Estas herramientas son funciones de Python que pueden ser expuestas a agentes de IA. Cuando las herramientas están anotadas con `@mcp.tool()`, se vuelven descubribles para el cliente, permitiendo que un agente de IA las llame dinámicamente durante una conversación o tarea. En esta tarea, agregarás algunas herramientas que permitirán al agente realizar verificaciones de inventario.

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado para tu código de función:

    ```
   code server.py
    ```

    En este archivo de código, definirás las herramientas que el agente puede usar para simular un servicio backend para la tienda minorista. Observa el código de configuración del servidor en la parte superior del archivo. Usa `FastMCP` para crear rápidamente una instancia de servidor MCP llamada "Inventory". Este servidor alojará las herramientas que definas y las hará accesibles al agente durante el laboratorio.

1. Encuentra el comentario **Add an inventory check tool** y agrega el siguiente código:

    ```python
   # Add an inventory check tool
   @mcp.tool()
   def get_inventory_levels() -> dict:
        """Returns current inventory for all products."""
        return {
            "Moisturizer": 6,
            "Shampoo": 8,
            "Body Spray": 28,
            "Hair Gel": 5, 
            "Lip Balm": 12,
            "Skin Serum": 9,
            "Cleanser": 30,
            "Conditioner": 3,
            "Setting Powder": 17,
            "Dry Shampoo": 45
        }
    ```

    Este diccionario representa un inventario de muestra. La anotación `@mcp.tool()` permitirá al LLM descubrir tu función. 

1. Encuentra el comentario **Add a weekly sales tool** y agrega el siguiente código:

    ```python
   # Add a weekly sales tool
   @mcp.tool()
   def get_weekly_sales() -> dict:
        """Returns number of units sold last week."""
        return {
            "Moisturizer": 22,
            "Shampoo": 18,
            "Body Spray": 3,
            "Hair Gel": 2,
            "Lip Balm": 14,
            "Skin Serum": 19,
            "Cleanser": 4,
            "Conditioner": 1,
            "Setting Powder": 13,
            "Dry Shampoo": 17
        }
    ```

1. Guarda el archivo (*CTRL+S*).

### Implementar un cliente MCP

Un cliente MCP es el componente que se conecta al servidor MCP para descubrir y llamar herramientas. Puedes pensar en él como el puente entre el agente y las funciones alojadas en el servidor, habilitando el uso dinámico de herramientas en respuesta a los prompts del usuario.

1. Ingresa el siguiente comando para comenzar a editar el código del cliente.

    ```
   code client.py
    ```

    > **Consejo**: A medida que agregues código al archivo de código, asegúrate de mantener la indentación correcta.

1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases:

    ```python
   # Add references
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import FunctionTool, MessageRole, ListSortOrder
   from azure.identity import DefaultAzureCredential
    ```

1. Encuentra el comentario **Start the MCP server** y agrega el siguiente código:

    ```python
   # Start the MCP server
   stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
   stdio, write = stdio_transport
    ```

    En una configuración de producción estándar, el servidor se ejecutaría por separado del cliente. Pero para efectos de este laboratorio, el cliente es responsable de iniciar el servidor usando transporte de entrada/salida estándar. Esto crea un canal de comunicación ligero entre los dos componentes y simplifica la configuración de desarrollo local.

1. Encuentra el comentario **Create an MCP client session** y agrega el siguiente código:

    ```python
   # Create an MCP client session
   session = await exit_stack.enter_async_context(ClientSession(stdio, write))
   await session.initialize()
    ```

    Esto crea una nueva sesión de cliente usando los flujos de entrada y salida del paso anterior. Llamar a `session.initialize` prepara la sesión para descubrir y llamar herramientas que están registradas en el servidor MCP.

1. Bajo el comentario **List available tools**, agrega el siguiente código para verificar que el cliente se haya conectado al servidor:

    ```python
   # List available tools
   response = await session.list_tools()
   tools = response.tools
   print("\nConnected to server with tools:", [tool.name for tool in tools]) 
    ```

    Ahora tu sesión de cliente está lista para ser usada con tu Agente de IA de Azure.

### Conectar las herramientas MCP a tu agente

En esta tarea, prepararás el agente de IA, aceptarás prompts del usuario e invocarás las herramientas de función.

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

1. Bajo el comentario **List tools available on the server**, agrega el siguiente código:

    ```python
   # List tools available on the server
   response = await session.list_tools()
   tools = response.tools
    ```

1. Bajo el comentario **Build a function for each tool** y agrega el siguiente código:

    ```python
   # Build a function for each tool
   def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            result = await session.call_tool(tool_name, kwargs)
            return result
        
        tool_func.__name__ = tool_name
        return tool_func

   functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}
   mcp_function_tool = FunctionTool(functions=list(functions_dict.values()))
    ```

    Este código envuelve dinámicamente las herramientas disponibles en el servidor MCP para que puedan ser llamadas por el agente de IA. Cada herramienta se convierte en una función asíncrona y luego se agrupa en un `FunctionTool` para que el agente lo use.

1. Encuentra el comentario **Create the agent** y agrega el siguiente código:

    ```python
   # Create the agent
   agent = agents_client.create_agent(
        model=model_deployment,
        name="inventory-agent",
        instructions="""
        You are an inventory assistant. Here are some general guidelines:
        - Recommend restock if item inventory < 10  and weekly sales > 15
        - Recommend clearance if item inventory > 20 and weekly sales < 5
        """,
        tools=mcp_function_tool.definitions
   )
    ```

1. Encuentra el comentario **Enable auto function calling** y agrega el siguiente código:

    ```python
   # Enable auto function calling
   agents_client.enable_auto_function_calls(tools=mcp_function_tool)
    ```

1. Bajo el comentario **Create a thread for the chat session**, agrega el siguiente código:

    ```python
   # Create a thread for the chat session
   thread = agents_client.threads.create()
    ```

1. Ubica el comentario **Invoke the prompt** y agrega el siguiente código:

    ```python
   # Invoke the prompt
   message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=user_input,
   )
   run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
    ```

1. Ubica el comentario **Retrieve the matching function tool** y agrega el siguiente código:

    ```python
   # Retrieve the matching function tool
   function_name = tool_call.function.name
   args_json = tool_call.function.arguments
   kwargs = json.loads(args_json)
   required_function = functions_dict.get(function_name)

   # Invoke the function
   output = await required_function(**kwargs)
    ```

    Este código usa la información de la llamada de herramienta del hilo del agente. El nombre de la función y los argumentos se recuperan y se usan para invocar la función correspondiente.

1. Bajo el comentario **Append the output text**, agrega el siguiente código:

    ```python
   # Append the output text
   tool_outputs.append({
        "tool_call_id": tool_call.id,
        "output": output.content[0].text,
   })
    ```

1. Bajo el comentario **Submit the tool call output**, agrega este código:

    ```python
   # Submit the tool call output
   agents_client.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)
    ```

    Este código señalará al hilo del agente que la acción requerida está completa y actualizará las salidas de la llamada de herramienta.

1. Encuentra el comentario **Display the response** y agrega el siguiente código:

    ```python
   # Display the response
   messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}:\n{last_msg.text.value}\n")
    ```

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

1. Cuando se te solicite, ingresa una consulta como:

    ```
   ¿Cuáles son los niveles de inventario actuales?
    ```

    > **Consejo**: Si la aplicación falla porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder.

    Deberías ver una salida similar a la siguiente:

    ```
    MessageRole.AGENT:
    Aquí están los niveles de inventario actuales:

    - Moisturizer: 6
    - Shampoo: 8
    - Body Spray: 28
    - Hair Gel: 5
    - Lip Balm: 12
    - Skin Serum: 9
    - Cleanser: 30
    - Conditioner: 3
    - Setting Powder: 17
    - Dry Shampoo: 45
    ```

1. Puedes continuar la conversación si lo deseas. El hilo tiene *estado*, por lo que retiene el historial de conversación - lo que significa que el agente tiene el contexto completo para cada respuesta. 

    Intenta ingresar prompts como:

    ```
   ¿Hay productos que deban ser reabastecidos?
    ```

    ```
   ¿Qué productos recomendarías para liquidación?
    ```

    ```
   ¿Cuáles son los productos más vendidos esta semana?
    ```

    Ingresa `quit` cuando hayas terminado.

## Limpiar

Ahora que has terminado el ejercicio, deberías eliminar los recursos en la nube que has creado para evitar el uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del grupo de recursos donde desplegaste los recursos del hub utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

