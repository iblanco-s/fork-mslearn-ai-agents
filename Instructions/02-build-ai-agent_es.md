---
lab:
    title: 'Desarrollar un agente de IA'
    description: 'Usa el Servicio de Agentes de IA de Azure para desarrollar un agente que utiliza herramientas integradas.'
---

# Desarrollar un agente de IA

En este ejercicio, utilizarás el Servicio de Agentes de IA de Azure para crear un agente simple que analiza datos y crea gráficos. El agente puede usar la herramienta integrada *Code Interpreter* para generar dinámicamente cualquier código necesario para analizar datos.

> **Consejo**: El código utilizado en este ejercicio está basado en el SDK de Azure AI Foundry para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas de cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para más detalles.

Este ejercicio debería requerir aproximadamente de **30** minutos para completarlo.

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

## Crear una aplicación cliente del agente

Ahora estás listo para crear una aplicación cliente que use un agente. Se te ha proporcionado algo de código en un repositorio de GitHub.

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
   cd ai-agents/Labfiles/02-build-ai-agent/Python
   ls -a -l
    ```

    Los archivos proporcionados incluyen código de aplicación, configuraciones y datos.

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación del modelo (que debería ser *gpt-4o*).
1. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Escribir código para una aplicación de agente

> **Consejo**: A medida que agregues código, asegúrate de mantener la indentación correcta. Usa los niveles de indentación de los comentarios como guía.

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```
   code agent.py
    ```

1. Revisa el código existente, que recupera las configuraciones de la aplicación y carga datos desde *data.txt* para ser analizados. El resto del archivo incluye comentarios donde agregarás el código necesario para implementar tu agente de análisis de datos.
1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás para construir un agente de IA de Azure que usa la herramienta integrada de intérprete de código:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import FilePurpose, CodeInterpreterTool, ListSortOrder, MessageRole
    ```

1. Encuentra el comentario **Connect to the Agent client** y agrega el siguiente código para conectarte al proyecto de Azure AI.

    > **Consejo**: Ten cuidado de mantener el nivel de indentación correcto.

    ```python
   # Connect to the Agent client
   agent_client = AgentsClient(
       endpoint=project_endpoint,
       credential=DefaultAzureCredential
           (exclude_environment_credential=True,
            exclude_managed_identity_credential=True)
   )
   with agent_client:
    ```

    El código se conecta al proyecto de Azure AI Foundry usando las credenciales actuales de Azure. La instrucción final *with agent_client* inicia un bloque de código que define el alcance del cliente, asegurando que se limpie cuando el código dentro del bloque haya terminado.

1. Encuentra el comentario **Upload the data file and create a CodeInterpreterTool**, dentro del bloque *with agent_client*, y agrega el siguiente código para subir el archivo de datos al proyecto y crear un CodeInterpreterTool que pueda acceder a los datos en él:

    ```python
   # Upload the data file and create a CodeInterpreterTool
   file = agent_client.files.upload_and_poll(
        file_path=file_path, purpose=FilePurpose.AGENTS
   )
   print(f"Uploaded {file.filename}")

   code_interpreter = CodeInterpreterTool(file_ids=[file.id])
    ```
    
1. Encuentra el comentario **Define an agent that uses the CodeInterpreterTool** y agrega el siguiente código para definir un agente de IA que analiza datos y puede usar la herramienta de intérprete de código que definiste anteriormente:

    ```python
   # Define an agent that uses the CodeInterpreterTool
   agent = agent_client.create_agent(
        model=model_deployment,
        name="data-agent",
        instructions="You are an AI agent that analyzes the data in the file that has been uploaded. Use Python to calculate statistical metrics as necessary.",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
   )
   print(f"Using agent: {agent.name}")
    ```

1. Encuentra el comentario **Create a thread for the conversation** y agrega el siguiente código para iniciar un hilo en el que se ejecutará la sesión de chat con el agente:

    ```python
   # Create a thread for the conversation
   thread = agent_client.threads.create()
    ```
    
1. Observa que la siguiente sección de código configura un bucle para que el usuario ingrese un prompt, terminando cuando el usuario ingresa "quit".

1. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código para agregar un mensaje del usuario al prompt (junto con los datos del archivo que se cargaron anteriormente), y luego ejecutar el hilo con el agente.

    ```python
   # Send a prompt to the agent
   message = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt,
    )

   run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    ```

1. Encuentra el comentario **Check the run status for failures** y agrega el siguiente código para verificar si hay errores.

    ```python
   # Check the run status for failures
   if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    ```

1. Encuentra el comentario **Show the latest response from the agent** y agrega el siguiente código para recuperar los mensajes del hilo completado y mostrar el último que fue enviado por el agente.

    ```python
   # Show the latest response from the agent
   last_msg = agent_client.messages.get_last_message_text_by_role(
       thread_id=thread.id,
       role=MessageRole.AGENT,
   )
   if last_msg:
       print(f"Last Message: {last_msg.text.value}")
    ```

1. Encuentra el comentario **Get the conversation history**, que está después de que termina el bucle, y agrega el siguiente código para imprimir los mensajes del hilo de conversación; invirtiendo el orden para mostrarlos en secuencia cronológica

    ```python
   # Get the conversation history
   print("\nConversation Log:\n")
   messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
       if message.text_messages:
           last_msg = message.text_messages[-1]
           print(f"{message.role}: {last_msg.text.value}\n")
    ```

1. Encuentra el comentario **Clean up** y agrega el siguiente código para eliminar el agente y el hilo cuando ya no sean necesarios.

    ```python
   # Clean up
   agent_client.delete_agent(agent.id)
    ```

1. Revisa el código, usando los comentarios para entender cómo:
    - Se conecta al proyecto de AI Foundry.
    - Sube el archivo de datos y crea una herramienta de intérprete de código que puede acceder a él.
    - Crea un nuevo agente que usa la herramienta de intérprete de código y tiene instrucciones explícitas para usar Python según sea necesario para análisis estadístico.
    - Ejecuta un hilo con un mensaje de prompt del usuario junto con los datos a analizar.
    - Verifica el estado de la ejecución en caso de que haya un fallo
    - Recupera los mensajes del hilo completado y muestra el último enviado por el agente.
    - Muestra el historial de conversación
    - Elimina el agente y el hilo cuando ya no se requieren.

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
    python agent.py
    ```
    
    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

1. Cuando se te solicite, visualiza los datos que la aplicación ha cargado desde el archivo de texto *data.txt*. Luego ingresa un prompt como:

    ```
   ¿Cuál es la categoría con el costo más alto?
    ```

    > **Consejo**: Si la aplicación falla porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder.

1. Visualiza la respuesta. Luego ingresa otro prompt, esta vez solicitando una visualización:

    ```
   Crea un gráfico de barras basado en texto mostrando el costo por categoría
    ```

1. Visualiza la respuesta. Luego ingresa otro prompt, esta vez solicitando una métrica estadística:

    ```
   ¿Cuál es la desviación estándar del costo?
    ```

    Visualiza la respuesta.

1. Puedes continuar la conversación si lo deseas. El hilo tiene *estado*, por lo que retiene el historial de conversación - lo que significa que el agente tiene el contexto completo para cada respuesta. Ingresa `quit` cuando hayas terminado.
1. Revisa los mensajes de conversación que fueron recuperados del hilo - que pueden incluir mensajes que el agente generó para explicar sus pasos al usar la herramienta de intérprete de código.

## Resumen

En este ejercicio, utilizaste el SDK del Servicio de Agentes de IA de Azure para crear una aplicación cliente que usa un agente de IA. El agente puede usar la herramienta integrada de Intérprete de Código para ejecutar código Python dinámico para realizar análisis estadísticos.

## Limpiar

Si has terminado de explorar el Servicio de Agentes de IA de Azure, deberías eliminar los recursos que has creado en este ejercicio para evitar costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o vuelve a abrir el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde desplegaste los recursos utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

