---
lab:
    title: 'Conectar a agentes remotos con el protocolo A2A'
    description: 'Usa el protocolo A2A para colaborar con agentes remotos.'
---

# Conectar a agentes remotos con el protocolo A2A

En este ejercicio, utilizarás el Servicio de Agentes de IA de Azure con el protocolo A2A para crear agentes remotos simples que interactúan entre sí. Estos agentes asistirán a escritores técnicos con la preparación de sus publicaciones de blog para desarrolladores. Un agente de título generará un titular, y un agente de esquema usará el título para desarrollar un esquema conciso para el artículo. ¡Comencemos!

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

## Crear una aplicación A2A

Ahora estás listo para crear una aplicación cliente que usa un agente. Se te ha proporcionado algo de código en un repositorio de GitHub.

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
   cd ai-agents/Labfiles/06-build-remote-agents-with-a2a/python
   ls -a -l
    ```

    Los archivos proporcionados incluyen:
    ```output
    python
    ├── outline_agent/
    │   ├── agent.py
    │   ├── agent_executor.py
    │   └── server.py
    ├── routing_agent/
    │   ├── agent.py
    │   └── server.py
    ├── title_agent/
    │   ├── agent.py
    |   ├── agent_executor.py
    │   └── server.py
    ├── client.py
    └── run_all.py
    ```

    Cada carpeta de agente contiene el código del agente de IA de Azure y un servidor para alojar el agente. El **agente de enrutamiento** es responsable de descubrir y comunicarse con los agentes de **título** y **esquema**. El **cliente** permite a los usuarios enviar prompts al agente de enrutamiento. `run_all.py` lanza todos los servidores y ejecuta el cliente.

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects a2a-sdk
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación del modelo (que debería ser *gpt-4o*).
1. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Crear un agente descubrible

En esta tarea, crearás el agente de título que ayuda a los escritores a crear titulares de moda para sus artículos. También definirás las habilidades del agente y la tarjeta requerida por el protocolo A2A para hacer que el agente sea descubrible.

1. Navega al directorio `title_agent`:

    ```
   cd title_agent
    ```

> **Consejo**: A medida que agregues código, asegúrate de mantener la indentación correcta. Usa los niveles de indentación de los comentarios como guía.

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```
   code agent.py
    ```

1. Encuentra el comentario **Create the agents client** y agrega el siguiente código para conectarte al proyecto de Azure AI:

    > **Consejo**: Ten cuidado de mantener el nivel de indentación correcto.

    ```python
   # Create the agents client
   self.client = AgentsClient(
       endpoint=os.environ['PROJECT_ENDPOINT'],
       credential=DefaultAzureCredential(
           exclude_environment_credential=True,
           exclude_managed_identity_credential=True
       )
   )
    ```

1. Encuentra el comentario **Create the title agent** y agrega el siguiente código para crear el agente:

    ```python
   # Create the title agent
   self.agent = self.client.create_agent(
       model=os.environ['MODEL_DEPLOYMENT_NAME'],
       name='title-agent',
       instructions="""
       You are a helpful writing assistant.
       Given a topic the user wants to write about, suggest a single clear and catchy blog post title.
       """,
   )
    ```

1. Encuentra el comentario **Create a thread for the chat session** y agrega el siguiente código para crear el hilo de chat:

    ```python
   # Create a thread for the chat session
   thread = self.client.threads.create()
    ```

1. Ubica el comentario **Send user message** y agrega este código para enviar el prompt del usuario:

    ```python
   # Send user message
   self.client.messages.create(thread_id=thread.id, role=MessageRole.USER, content=user_message)
    ```

1. Bajo el comentario **Create and run the agent**, agrega el siguiente código para iniciar la generación de respuesta del agente:

    ```python
   # Create and run the agent
   run = self.client.runs.create_and_process(thread_id=thread.id, agent_id=self.agent.id)
    ```

    El código proporcionado en el resto del archivo procesará y devolverá la respuesta del agente. 

1. Guarda el archivo de código (*CTRL+S*). Ahora estás listo para compartir las habilidades del agente y la tarjeta con el protocolo A2A. 

1. Ingresa el siguiente comando para editar el archivo `server.py` del agente de título  

    ```
   code server.py
    ```

1. Encuentra el comentario **Define agent skills** y agrega el siguiente código para especificar la funcionalidad del agente:

    ```python
   # Define agent skills
   skills = [
       AgentSkill(
           id='generate_blog_title',
           name='Generate Blog Title',
           description='Generates a blog title based on a topic',
           tags=['title'],
           examples=[
               'Can you give me a title for this article?',
           ],
       ),
   ]
    ```

1. Encuentra el comentario **Create agent card** y agrega este código para definir los metadatos que hacen que el agente sea descubrible:

    ```python
   # Create agent card
   agent_card = AgentCard(
       name='AI Foundry Title Agent',
       description='An intelligent title generator agent powered by Azure AI Foundry. '
       'I can help you generate catchy titles for your articles.',
       url=f'http://{host}:{port}/',
       version='1.0.0',
       default_input_modes=['text'],
       default_output_modes=['text'],
       capabilities=AgentCapabilities(),
       skills=skills,
   )
    ```

1. Ubica el comentario **Create agent executor** y agrega el siguiente código para inicializar el ejecutor del agente usando la tarjeta del agente:

    ```python
   # Create agent executor
   agent_executor = create_foundry_agent_executor(agent_card)
    ```

    El ejecutor del agente actuará como un wrapper para el agente de título que creaste.

1. Encuentra el comentario **Create request handler** y agrega lo siguiente para manejar las solicitudes entrantes usando el ejecutor:

    ```python
   # Create request handler
   request_handler = DefaultRequestHandler(
       agent_executor=agent_executor, task_store=InMemoryTaskStore()
   )
    ```

1. Bajo el comentario **Create A2A application**, agrega este código para crear la instancia de aplicación compatible con A2A:

    ```python
   # Create A2A application
   a2a_app = A2AStarletteApplication(
       agent_card=agent_card, http_handler=request_handler
   )
    ```
    
    Este código crea un servidor A2A que compartirá la información del agente de título y manejará las solicitudes entrantes para este agente usando el ejecutor del agente de título.

1. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado.

### Habilitar mensajes entre los agentes

En esta tarea, usarás el protocolo A2A para permitir que el agente de enrutamiento envíe mensajes a los otros agentes. También permitirás que el agente de título reciba mensajes implementando la clase ejecutora del agente.

1. Navega al directorio `routing_agent`:

    ```
   cd ../routing_agent
    ```

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```
   code agent.py
    ```

    El agente de enrutamiento actúa como un orquestador que maneja mensajes del usuario y determina qué agente remoto debe procesar la solicitud.

    Cuando se recibe un mensaje del usuario, el agente de enrutamiento:
    - Inicia un hilo de conversación.
    - Usa el método `create_and_process` para evaluar el agente que mejor coincide con el mensaje del usuario.
    - El mensaje se enruta al agente apropiado a través de HTTP usando la función `send_message`.
    - El agente remoto procesa el mensaje y devuelve una respuesta.

    El agente de enrutamiento finalmente captura la respuesta y la devuelve al usuario a través del hilo.

    Observa que el método `send_message` es asíncrono y debe esperarse para que la ejecución del agente se complete exitosamente.

1. Agrega el siguiente código bajo el comentario **Retrieve the remote agent's A2A client using the agent name**:

    ```python
   # Retrieve the remote agent's A2A client using the agent name 
   client = self.remote_agent_connections[agent_name]
    ```

1. Ubica el comentario **Construct the payload to send to the remote agent** y agrega el siguiente código:

    ```python
   # Construct the payload to send to the remote agent
   payload: dict[str, Any] = {
       'message': {
           'role': 'user',
           'parts': [{'kind': 'text', 'text': task}],
           'messageId': message_id,
       },
   }
    ```

1. Encuentra el comentario **Wrap the payload in a SendMessageRequest object** y agrega el siguiente código:

    ```python
   # Wrap the payload in a SendMessageRequest object
   message_request = SendMessageRequest(id=message_id, params=MessageSendParams.model_validate(payload))
    ```

1. Agrega el siguiente código bajo el comentario **Send the message to the remote agent client and await the response**:

    ```python
   # Send the message to the remote agent client and await the response
   send_response: SendMessageResponse = await client.send_message(message_request=message_request)
    ```


1. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado. Ahora el agente de enrutamiento puede descubrir y enviar mensajes al agente de título. Creemos el código ejecutor del agente para manejar esos mensajes entrantes del agente de enrutamiento.

1. Navega al directorio `title_agent`:

    ```
   cd ../title_agent
    ```

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```
   code agent_executor.py
    ```

    La implementación de la clase `AgentExecutor` debe contener los métodos `execute` y `cancel`. El método cancel ha sido proporcionado para ti. El método `execute` incluye un objeto `TaskUpdater` que gestiona eventos y señales al llamador cuando la tarea está completa. Agreguemos la lógica para la ejecución de tareas.

1. En el método `execute`, agrega el siguiente código bajo el comentario **Process the request**:

    ```python
   # Process the request
   await self._process_request(context.message.parts, context.context_id, updater)
    ```

1. En el método `_process_request`, agrega el siguiente código bajo el comentario **Get the title agent**:

    ```python
   # Get the title agent
   agent = await self._get_or_create_agent()
    ```

1. Agrega el siguiente código bajo el comentario **Update the task status**:

    ```python
   # Update the task status
   await task_updater.update_status(
       TaskState.working,
       message=new_agent_text_message('Title Agent is processing your request...', context_id=context_id),
   )
    ```

1. Encuentra el comentario **Run the agent conversation** y agrega el siguiente código:

    ```python
   # Run the agent conversation
   responses = await agent.run_conversation(user_message)
    ```

1. Encuentra el comentario **Update the task with the responses** y agrega el siguiente código:

    ```python
   # Update the task with the responses
   for response in responses:
       await task_updater.update_status(
           TaskState.working,
           message=new_agent_text_message(response, context_id=context_id),
       )
    ```

1. Encuentra el comentario **Mark the task as complete** y agrega el siguiente código:

    ```python
   # Mark the task as complete
   final_message = responses[-1] if responses else 'Task completed.'
   await task_updater.complete(
       message=new_agent_text_message(final_message, context_id=context_id)
   )
    ```

    ¡Ahora tu agente de título ha sido envuelto con un ejecutor de agente que el protocolo A2A usará para manejar mensajes. ¡Excelente trabajo!

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
    cd ..
    python run_all.py
    ```
    
    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente. Deberías ver alguna salida de cada servidor a medida que se inicia.

1. Espera hasta que aparezca el prompt de entrada, luego ingresa un prompt como:

    ```
   Crea un título y esquema para un artículo sobre programación en React.
    ```

    Después de unos momentos, deberías ver una respuesta del agente con los resultados.

1. Ingresa `quit` para salir del programa y detener los servidores.
    
## Resumen

En este ejercicio, utilizaste el SDK del Servicio de Agentes de IA de Azure y el SDK de Python A2A para crear una solución multi-agente remota. Creaste un agente compatible con A2A descubrible y configuraste un agente de enrutamiento para acceder a las habilidades del agente. También implementaste un ejecutor de agente para procesar mensajes A2A entrantes y gestionar tareas. ¡Excelente trabajo!

## Limpiar

Si has terminado de explorar el Servicio de Agentes de IA de Azure, deberías eliminar los recursos que has creado en este ejercicio para evitar costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o vuelve a abrir el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde desplegaste los recursos utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

