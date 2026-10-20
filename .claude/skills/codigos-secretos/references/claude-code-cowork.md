# Cowork y comandos de Claude Code (CLI)

Fuente: guía "584 Códigos Secretos para ChatGPT, Claude, Claude Code y Cowork" (Xabi Inteligencia Artificial, 2026). 67 entradas.

Estos son **comandos y funciones nativos** de Cowork y Claude Code: ya vienen incluidos, no hace falta instalarlos. La disponibilidad depende de la versión y del entorno (CLI, app de escritorio, web/nube).

> ⚠ "Funciones Rumoreadas (Leak 2026)": según la guía, no están confirmadas por Anthropic. Se dejan solo como curiosidad; no cuentes con ellas.

### 🚀 Funciones Clave de Cowork

| Código | Qué hace |
|---|---|
| `Carpeta de Trabajo` | Das a Claude acceso a una carpeta de tu ordenador para leer, crear y editar archivos de forma autónoma. Es la base de todo Cowork. |
| `/schedule` | Programa tareas recurrentes ("cada mañana a las 9", "cada lunes") que se ejecutan solas con tus archivos y conectores. |
| `Tareas Programadas` | Cada ejecución abre una sesión nueva en tu equipo con acceso total a archivos, MCP, skills y conectores. Como un analista junior 24/7. |
| `Live Artifacts` | Paneles, trackers y dashboards que viven en la barra lateral entre sesiones y se actualizan con datos frescos de tus conectores. |
| `Skills` | Instrucciones reutilizables (carpeta con SKILL.md) que Claude activa automáticamente cuando detecta la tarea adecuada. |
| `Sub-agentes` | Lanza varios agentes en paralelo para trabajo divisible (investigar, verificar, redactar) y reúne los resultados. |
| `Conectores (MCP)` | Conecta Gmail, Calendar, Notion, Slack, Drive, etc. para que Claude actúe directamente sobre tus apps reales. |
| `Dispatch (móvil)` | Lanza una tarea desde el teléfono; se ejecuta en tu escritorio con tus conectores y recibes el resultado en el móvil. |

### 💻 Comandos Esenciales

| Código | Qué hace |
|---|---|
| `/help` | Muestra la ayuda contextual y la lista de comandos disponibles. |
| `/compact` | Resume la conversación actual para liberar tokens de contexto cuando el uso supera el 70%. |
| `/clear` | Reinicia la conversación y limpia el contexto por completo. |
| `/status` | Muestra el estado de la sesión y el uso detallado del contexto. |
| `/cost` | Muestra las estadísticas de uso de tokens y el costo de la sesión actual. |
| `/insights` | Genera un informe HTML analizando tus patrones de uso y hábitos de codificación. |
| `/rewind` | Retrocede en el tiempo, deshaciendo cambios de código o revirtiendo la conversación (atajo: Esc+Esc). |
| `/doctor` | Ejecuta diagnósticos del entorno para detectar problemas de dependencias o configuración. |
| `/init` | Inicializa un nuevo proyecto creando el archivo de memoria CLAUDE.md. |

### ⚙ Modelo y Rendimiento

| Código | Qué hace |
|---|---|
| `/model` | Cambia el modelo activo (sonnet / opus / opusplan) durante la sesión. |
| `/fast` | Activa el modo rápido (2.5x velocidad, 6x costo). |
| `/context` | Muestra un desglose detallado del consumo de tokens. |
| `/usage` | Muestra el uso del plan y el estado del límite de velocidad. |
| `/export` | Exporta la conversación actual a un archivo o al portapapeles. |
| `/review` | Solicita una revisión de código del trabajo realizado. |
| `/debug` | Inicia un proceso sistemático de resolución de problemas en el código. |
| `/pr_comments` | Muestra los comentarios de Pull Requests (requiere integración con GitHub). |
| `/install-github-app` | Instala la GitHub App para automatizar revisiones de PR. |

### 🚀 Avanzados y Flujo de Trabajo

| Código | Qué hace |
|---|---|
| `/plan` | Entra en Modo Planificación (solo lectura). Claude analiza el código y propone una solución sin modificar archivos. |
| `/execute` | Sale del Modo Planificación y aplica los cambios propuestos. |
| `/batch` | Ejecuta refactorizaciones a gran escala usando entre 5 y 30 agentes paralelos en árboles de trabajo. |
| `/simplify` | Detecta sobre-ingeniería en el código modificado y propone correcciones automáticas para simplificarlo. |
| `/loop [intervalo]` | Ejecuta un prompt de forma repetitiva (ej. /loop 5m revisa el despliegue). |
| `/voice` | Activa la entrada de voz nativa (mantén la barra espaciadora para hablar). |
| `/btw` | Permite hacer una pregunta lateral rápida sin contaminar el historial de la conversación principal. |
| `/agents` | Gestiona sub-agentes para el procesamiento paralelo de tareas complejas. |
| `/ultraplan` | Envía la planificación a la nube de Claude para revisión en el navegador (v2.1.91+). |
| `/teleport` | Teleporta una sesión desde la interfaz web al terminal local. |
| `/remote-env` | Configura el entorno de ejecución en la nube. |
| `/remote-control` | Inicia una sesión de control remoto desde el teléfono o navegador (alias: /rc). |
| `/schedule` | Programa tareas para ejecución futura en la infraestructura de Anthropic. |
| `/tasks` | Monitoriza las tareas en segundo plano. |
| `/powerup` | Lecciones animadas interactivas que enseñan las funciones de Claude Code. |
| `/rename` | Nombra o renombra la sesión actual para fácil identificación. |
| `/copy` | Selector interactivo para copiar un bloque de código o una respuesta completa. |
| `/stats` | Muestra gráfico de uso, modelo favorito y racha de uso. |
| `/mobile` | Obtiene los enlaces de descarga de la app móvil de Claude. |
| `/exit` | Sale de Claude Code (equivalente a Ctrl+D). |

### ⌨ Atajos de Teclado

| Código | Qué hace |
|---|---|
| `Shift+Tab` | Cicla entre los modos de permiso (Normal, Auto-Accept, Plan). |
| `Esc x 2` | Abre el menú de retroceso (rewind). |
| `Ctrl+C` | Interrumpe la operación actual. |
| `Ctrl+R` | Busca en el historial de comandos. |
| `Ctrl+L` | Limpia la pantalla (mantiene el contexto). |
| `Tab` | Autocompletado de comandos y rutas. |
| `Shift+Enter` | Inserta una nueva línea sin enviar el mensaje. |
| `Ctrl+B` | Gestiona tareas en segundo plano. |
| `Ctrl+F x 2` | Mata todos los agentes en segundo plano. |
| `Alt+T` | Activa o desactiva el modo de pensamiento extendido. |
| `Space (mantener)` | Entrada de voz (requiere /voice activado). |
| `Ctrl+D` | Sale de Claude Code. |

### @ Prefijos Especiales

| Código | Qué hace |
|---|---|
| `@ruta/archivo.ts` | Referencia un archivo específico del proyecto para que Claude lo lea. |
| `@nombre-agente` | Invoca a un agente personalizado definido en .claude/agents/. |
| `!comando-shell` | Ejecuta un comando de shell directamente desde el prompt de Claude Code. |
| `ultrathink` | Palabra clave que fuerza el máximo esfuerzo de pensamiento en Opus (v2.1.68+). |

### 🔓 Funciones Rumoreadas (Leak 2026)

| Código | Qué hace |
|---|---|
| `KAIROS` | Asistente persistente que registra la actividad diaria y consolida recuerdos durante la noche. |
| `ULTRAPLAN` | Envía tareas de planificación muy complejas a la nube por hasta 30 minutos, con aprobación manual. |
| `Modo Coordinador` | Sistema donde múltiples agentes trabajan en paralelo y reportan su progreso vía estructuras XML. |
| `Stealth Mode` | Se activaría automáticamente cuando personal de Anthropic usa la herramienta en repos públicos. |
| `USER_TYPE=ant` | Variable de entorno mencionada en el leak, asociada a empleados de Anthropic. Rumoreada, no verificada. |
