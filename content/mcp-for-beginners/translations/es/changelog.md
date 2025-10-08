<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T21:54:41+00:00",
  "source_file": "changelog.md",
  "language_code": "es"
}
-->
# Registro de cambios: Currículo MCP para principiantes

Este documento sirve como registro de todos los cambios significativos realizados en el currículo del Protocolo de Contexto de Modelo (MCP) para principiantes. Los cambios están documentados en orden cronológico inverso (los cambios más recientes primero).

## 6 de octubre de 2025

### Expansión de la sección Introducción – Uso avanzado de servidores y autenticación simple

#### Uso avanzado de servidores (03-GettingStarted/10-advanced)
- **Nuevo capítulo añadido**: Se ha introducido una guía completa sobre el uso avanzado de servidores MCP, que abarca arquitecturas de servidores regulares y de bajo nivel.
  - **Servidor regular vs. de bajo nivel**: Comparación detallada y ejemplos de código en Python y TypeScript para ambos enfoques.
  - **Diseño basado en manejadores**: Explicación sobre la gestión de herramientas/recursos/prompts basada en manejadores para implementaciones de servidores escalables y flexibles.
  - **Patrones prácticos**: Escenarios reales donde los patrones de servidores de bajo nivel son beneficiosos para características avanzadas y arquitecturas.

#### Autenticación simple (03-GettingStarted/11-simple-auth)
- **Nuevo capítulo añadido**: Guía paso a paso para implementar autenticación simple en servidores MCP.
  - **Conceptos de autenticación**: Explicación clara de la diferencia entre autenticación y autorización, y manejo de credenciales.
  - **Implementación básica de autenticación**: Patrones de autenticación basados en middleware en Python (Starlette) y TypeScript (Express), con ejemplos de código.
  - **Progresión hacia seguridad avanzada**: Orientación para comenzar con autenticación simple y avanzar hacia OAuth 2.1 y RBAC, con referencias a módulos de seguridad avanzados.

Estas adiciones proporcionan orientación práctica y aplicada para construir implementaciones de servidores MCP más robustas, seguras y flexibles, conectando conceptos fundamentales con patrones avanzados de producción.

## 29 de septiembre de 2025

### Laboratorios de integración de bases de datos en servidores MCP - Ruta de aprendizaje práctica y completa

#### 11-MCPServerHandsOnLabs - Nuevo currículo completo de integración de bases de datos
- **Ruta de aprendizaje completa de 13 laboratorios**: Se ha añadido un currículo práctico completo para construir servidores MCP listos para producción con integración de bases de datos PostgreSQL.
  - **Implementación en el mundo real**: Caso de uso de análisis de retail de Zava que demuestra patrones de nivel empresarial.
  - **Progresión estructurada de aprendizaje**:
    - **Laboratorios 00-03: Fundamentos** - Introducción, arquitectura principal, seguridad y multi-tenencia, configuración del entorno.
    - **Laboratorios 04-06: Construcción del servidor MCP** - Diseño y esquema de base de datos, implementación del servidor MCP, desarrollo de herramientas.
    - **Laboratorios 07-09: Características avanzadas** - Integración de búsqueda semántica, pruebas y depuración, integración con VS Code.
    - **Laboratorios 10-12: Producción y mejores prácticas** - Estrategias de despliegue, monitoreo y observabilidad, mejores prácticas y optimización.
  - **Tecnologías empresariales**: Framework FastMCP, PostgreSQL con pgvector, embeddings de Azure OpenAI, Azure Container Apps, Application Insights.
  - **Características avanzadas**: Seguridad a nivel de fila (RLS), búsqueda semántica, acceso a datos multi-tenant, embeddings vectoriales, monitoreo en tiempo real.

#### Estandarización de terminología - Conversión de módulo a laboratorio
- **Actualización completa de documentación**: Se han actualizado sistemáticamente todos los archivos README en 11-MCPServerHandsOnLabs para usar la terminología "Laboratorio" en lugar de "Módulo".
  - **Encabezados de sección**: Se actualizó "Qué cubre este módulo" a "Qué cubre este laboratorio" en los 13 laboratorios.
  - **Descripción del contenido**: Se cambió "Este módulo proporciona..." a "Este laboratorio proporciona..." en toda la documentación.
  - **Objetivos de aprendizaje**: Se actualizó "Al final de este módulo..." a "Al final de este laboratorio...".
  - **Enlaces de navegación**: Se convirtieron todas las referencias "Módulo XX:" a "Laboratorio XX:" en referencias cruzadas y navegación.
  - **Seguimiento de finalización**: Se actualizó "Después de completar este módulo..." a "Después de completar este laboratorio...".
  - **Referencias técnicas preservadas**: Se mantuvieron las referencias a módulos de Python en los archivos de configuración (por ejemplo, `"module": "mcp_server.main"`).

#### Mejora de la guía de estudio (study_guide.md)
- **Mapa visual del currículo**: Se añadió una nueva sección "11. Laboratorios de integración de bases de datos" con una visualización completa de la estructura de los laboratorios.
- **Estructura del repositorio**: Actualización de diez a once secciones principales con una descripción detallada de 11-MCPServerHandsOnLabs.
- **Guía de ruta de aprendizaje**: Instrucciones de navegación mejoradas para cubrir las secciones 00-11.
- **Cobertura tecnológica**: Se añadieron detalles sobre la integración de FastMCP, PostgreSQL y servicios de Azure.
- **Resultados de aprendizaje**: Énfasis en el desarrollo de servidores listos para producción, patrones de integración de bases de datos y seguridad empresarial.

#### Mejora de la estructura del README principal
- **Terminología basada en laboratorios**: Actualización del archivo README.md principal en 11-MCPServerHandsOnLabs para usar consistentemente la estructura de "Laboratorio".
- **Organización de la ruta de aprendizaje**: Progresión clara desde conceptos fundamentales hasta implementación avanzada y despliegue en producción.
- **Enfoque en el mundo real**: Énfasis en el aprendizaje práctico con patrones y tecnologías de nivel empresarial.

### Mejoras en la calidad y consistencia de la documentación
- **Énfasis en el aprendizaje práctico**: Reforzamiento del enfoque práctico basado en laboratorios en toda la documentación.
- **Enfoque en patrones empresariales**: Destacados implementaciones listas para producción y consideraciones de seguridad empresarial.
- **Integración tecnológica**: Cobertura completa de servicios modernos de Azure e integración de IA.
- **Progresión de aprendizaje**: Ruta estructurada y clara desde conceptos básicos hasta despliegue en producción.

## 26 de septiembre de 2025

### Mejora de estudios de caso - Integración del registro MCP de GitHub

#### Estudios de caso (09-CaseStudy/) - Enfoque en el desarrollo del ecosistema
- **README.md**: Expansión importante con un estudio de caso completo sobre el registro MCP de GitHub.
  - **Estudio de caso del registro MCP de GitHub**: Nuevo estudio de caso completo que examina el lanzamiento del registro MCP de GitHub en septiembre de 2025.
    - **Análisis del problema**: Examen detallado de los desafíos de descubrimiento y despliegue fragmentado de servidores MCP.
    - **Arquitectura de la solución**: Enfoque centralizado del registro de GitHub con instalación de VS Code con un solo clic.
    - **Impacto empresarial**: Mejoras medibles en la incorporación y productividad de desarrolladores.
    - **Valor estratégico**: Enfoque en el despliegue modular de agentes y la interoperabilidad entre herramientas.
    - **Desarrollo del ecosistema**: Posicionamiento como plataforma fundamental para la integración de agentes.
  - **Estructura mejorada de estudios de caso**: Actualización de los siete estudios de caso con formato consistente y descripciones completas.
    - Agentes de viaje de Azure AI: Énfasis en la orquestación multi-agente.
    - Integración con Azure DevOps: Enfoque en la automatización de flujos de trabajo.
    - Recuperación de documentación en tiempo real: Implementación de cliente de consola en Python.
    - Generador interactivo de planes de estudio: Aplicación web conversacional con Chainlit.
    - Documentación en el editor: Integración con VS Code y GitHub Copilot.
    - Gestión de API de Azure: Patrones de integración de API empresariales.
    - Registro MCP de GitHub: Desarrollo del ecosistema y plataforma comunitaria.
  - **Conclusión completa**: Reescritura de la sección de conclusión destacando siete estudios de caso que abarcan múltiples dimensiones de implementación MCP.
    - Integración empresarial, orquestación multi-agente, productividad del desarrollador.
    - Desarrollo del ecosistema, aplicaciones educativas categorizadas.
    - Perspectivas mejoradas sobre patrones arquitectónicos, estrategias de implementación y mejores prácticas.
    - Énfasis en MCP como protocolo maduro y listo para producción.

#### Actualizaciones de la guía de estudio (study_guide.md)
- **Mapa visual del currículo**: Actualización del mapa mental para incluir el registro MCP de GitHub en la sección de estudios de caso.
- **Descripción de estudios de caso**: Mejora de descripciones genéricas a un desglose detallado de siete estudios de caso completos.
- **Estructura del repositorio**: Actualización de la sección 10 para reflejar la cobertura completa de estudios de caso con detalles específicos de implementación.
- **Integración del registro de cambios**: Adición de la entrada del 26 de septiembre de 2025 documentando la incorporación del registro MCP de GitHub y las mejoras en los estudios de caso.
- **Actualización de fechas**: Actualización de la marca de tiempo del pie de página para reflejar la última revisión (26 de septiembre de 2025).

### Mejoras en la calidad de la documentación
- **Mejora de la consistencia**: Formato y estructura estandarizados de los estudios de caso en todos los ejemplos.
- **Cobertura completa**: Los estudios de caso ahora abarcan escenarios de integración empresarial, productividad del desarrollador y desarrollo del ecosistema.
- **Posicionamiento estratégico**: Enfoque mejorado en MCP como plataforma fundamental para el despliegue de sistemas de agentes.
- **Integración de recursos**: Actualización de recursos adicionales para incluir el enlace al registro MCP de GitHub.

## 15 de septiembre de 2025

### Expansión de temas avanzados - Transportes personalizados y ingeniería de contexto

#### Transportes personalizados de MCP (05-AdvancedTopics/mcp-transport/) - Nueva guía avanzada de implementación
- **README.md**: Guía completa de implementación para mecanismos de transporte personalizados de MCP.
  - **Transporte de Azure Event Grid**: Implementación integral de transporte sin servidor basado en eventos.
    - Ejemplos en C#, TypeScript y Python con integración de Azure Functions.
    - Patrones de arquitectura basada en eventos para soluciones MCP escalables.
    - Receptores de webhook y manejo de mensajes basado en push.
  - **Transporte de Azure Event Hubs**: Implementación de transporte de transmisión de alto rendimiento.
    - Capacidades de transmisión en tiempo real para escenarios de baja latencia.
    - Estrategias de partición y gestión de puntos de control.
    - Agrupación de mensajes y optimización de rendimiento.
  - **Patrones de integración empresarial**: Ejemplos arquitectónicos listos para producción.
    - Procesamiento MCP distribuido en múltiples Azure Functions.
    - Arquitecturas híbridas de transporte que combinan múltiples tipos de transporte.
    - Estrategias de durabilidad, confiabilidad y manejo de errores en mensajes.
  - **Seguridad y monitoreo**: Integración con Azure Key Vault y patrones de observabilidad.
    - Autenticación con identidad administrada y acceso de privilegio mínimo.
    - Telemetría de Application Insights y monitoreo de rendimiento.
    - Interruptores automáticos y patrones de tolerancia a fallos.
  - **Marcos de prueba**: Estrategias completas de prueba para transportes personalizados.
    - Pruebas unitarias con dobles de prueba y marcos de simulación.
    - Pruebas de integración con contenedores de prueba de Azure.
    - Consideraciones sobre pruebas de rendimiento y carga.

#### Ingeniería de contexto (05-AdvancedTopics/mcp-contextengineering/) - Disciplina emergente de IA
- **README.md**: Exploración completa de la ingeniería de contexto como un campo emergente.
  - **Principios básicos**: Compartir contexto completo, conciencia de decisiones de acción y gestión de ventanas de contexto.
  - **Alineación con el protocolo MCP**: Cómo el diseño de MCP aborda los desafíos de la ingeniería de contexto.
    - Limitaciones de ventanas de contexto y estrategias de carga progresiva.
    - Determinación de relevancia y recuperación dinámica de contexto.
    - Manejo de contexto multimodal y consideraciones de seguridad.
  - **Enfoques de implementación**: Arquitecturas de un solo hilo vs. multi-agente.
    - Técnicas de fragmentación y priorización de contexto.
    - Estrategias de carga progresiva y compresión de contexto.
    - Enfoques de contexto en capas y optimización de recuperación.
  - **Marco de medición**: Métricas emergentes para la evaluación de la efectividad del contexto.
    - Eficiencia de entrada, rendimiento, calidad y consideraciones de experiencia del usuario.
    - Enfoques experimentales para la optimización del contexto.
    - Análisis de fallos y metodologías de mejora.

#### Actualizaciones de navegación del currículo (README.md)
- **Estructura mejorada de módulos**: Actualización de la tabla del currículo para incluir nuevos temas avanzados.
  - Se añadieron las entradas de Ingeniería de Contexto (5.14) y Transporte Personalizado (5.15).
  - Formato consistente y enlaces de navegación en todos los módulos.
  - Descripciones actualizadas para reflejar el alcance actual del contenido.

### Mejoras en la estructura del directorio
- **Estandarización de nombres**: Se renombró "mcp transport" a "mcp-transport" para mantener la consistencia con otras carpetas de temas avanzados.
- **Organización del contenido**: Todas las carpetas de 05-AdvancedTopics ahora siguen un patrón de nomenclatura consistente (mcp-[tema]).

### Mejoras en la calidad de la documentación
- **Alineación con la especificación MCP**: Todo el contenido nuevo hace referencia a la actual Especificación MCP 2025-06-18.
- **Ejemplos en múltiples lenguajes**: Ejemplos de código completos en C#, TypeScript y Python.
- **Enfoque empresarial**: Patrones listos para producción e integración con la nube de Azure en todo el contenido.
- **Documentación visual**: Diagramas de Mermaid para la visualización de arquitectura y flujo.

## 18 de agosto de 2025

### Actualización integral de la documentación - Estándares MCP 2025-06-18

#### Mejores prácticas de seguridad MCP (02-Security/) - Modernización completa
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Reescritura completa alineada con la Especificación MCP 2025-06-18.
  - **Requisitos obligatorios**: Se añadieron requisitos explícitos DEBE/NO DEBE de la especificación oficial con indicadores visuales claros.
  - **12 prácticas principales de seguridad**: Reestructuración de la lista de 15 elementos a dominios de seguridad completos.
    - Seguridad de tokens y autenticación con integración de proveedores de identidad externos.
    - Gestión de sesiones y seguridad de transporte con requisitos criptográficos.
    - Protección contra amenazas específicas de IA con integración de Microsoft Prompt Shields.
    - Control de acceso y permisos con el principio de privilegio mínimo.
    - Seguridad y monitoreo de contenido con integración de Azure Content Safety.
    - Seguridad de la cadena de suministro con verificación completa de componentes.
    - Seguridad OAuth y prevención de ataques de delegado confundido con implementación de PKCE.
    - Respuesta a incidentes y recuperación con capacidades automatizadas.
    - Cumplimiento y gobernanza con alineación regulatoria.
    - Controles de seguridad avanzados con arquitectura de confianza cero.
    - Integración del ecosistema de seguridad de Microsoft con soluciones completas.
    - Evolución continua de la seguridad con prácticas adaptativas.
  - **Soluciones de seguridad de Microsoft**: Guía de integración mejorada para Prompt Shields, Azure Content Safety, Entra ID y GitHub Advanced Security.
  - **Recursos de implementación**: Enlaces de recursos categorizados por Documentación oficial de MCP, Soluciones de seguridad de Microsoft, Estándares de seguridad y Guías de implementación.

#### Controles de seguridad avanzados (02-Security/) - Implementación empresarial
- **MCP-SECURITY-CONTROLS-2025.md**: Revisión completa con un marco de seguridad de nivel empresarial.
  - **9 dominios de seguridad completos**: Expansión de controles básicos a un marco empresarial detallado.
    - Autenticación y autorización avanzadas con integración de Microsoft Entra ID.
    - Seguridad de tokens y controles contra passthrough con validación completa.
    - Controles de seguridad de sesiones con prevención de secuestro.
    - Controles de seguridad específicos de IA con prevención de inyección de prompts y envenenamiento de herramientas.
    - Prevención de ataques de delegado confundido con seguridad de proxy OAuth.
    - Seguridad en la ejecución de herramientas con sandboxing y aislamiento.
    - Controles de seguridad de la cadena de suministro con verificación de dependencias.
    - Controles de monitoreo y detección con integración de SIEM.
    - Respuesta a incidentes y recuperación con capacidades automatizadas.
  - **Ejemplos de implementación**: Se añadieron bloques de configuración YAML detallados y ejemplos de código.
  - **Integración de soluciones de Microsoft**: Cobertura completa de servicios de seguridad de Azure, GitHub Advanced Security y gestión de identidad empresarial.
#### Temas Avanzados de Seguridad (05-AdvancedTopics/mcp-security/) - Implementación Lista para Producción
- **README.md**: Reescritura completa para implementación de seguridad empresarial
  - **Alineación con Especificaciones Actuales**: Actualizado a la Especificación MCP 2025-06-18 con requisitos de seguridad obligatorios
  - **Autenticación Mejorada**: Integración con Microsoft Entra ID y ejemplos completos en .NET y Java Spring Security
  - **Integración de Seguridad con IA**: Implementación de Microsoft Prompt Shields y Azure Content Safety con ejemplos detallados en Python
  - **Mitigación Avanzada de Amenazas**: Ejemplos completos de implementación para:
    - Prevención de ataques de Confused Deputy con PKCE y validación de consentimiento del usuario
    - Prevención de Token Passthrough con validación de audiencia y gestión segura de tokens
    - Prevención de secuestro de sesiones con vinculación criptográfica y análisis de comportamiento
  - **Integración de Seguridad Empresarial**: Monitoreo con Azure Application Insights, pipelines de detección de amenazas y seguridad en la cadena de suministro
  - **Lista de Verificación de Implementación**: Controles de seguridad claros, obligatorios vs. recomendados, con beneficios del ecosistema de seguridad de Microsoft

### Calidad de Documentación y Alineación con Estándares
- **Referencias a Especificaciones**: Actualizadas todas las referencias a la Especificación MCP 2025-06-18
- **Ecosistema de Seguridad de Microsoft**: Guía mejorada de integración en toda la documentación de seguridad
- **Implementación Práctica**: Ejemplos de código detallados en .NET, Java y Python con patrones empresariales
- **Organización de Recursos**: Categorización completa de documentación oficial, estándares de seguridad y guías de implementación
- **Indicadores Visuales**: Marcado claro de requisitos obligatorios vs. prácticas recomendadas

#### Conceptos Básicos (01-CoreConcepts/) - Modernización Completa
- **Actualización de Versión de Protocolo**: Referencia actualizada a la Especificación MCP 2025-06-18 con versionado basado en fechas (formato YYYY-MM-DD)
- **Refinamiento de Arquitectura**: Descripciones mejoradas de Hosts, Clientes y Servidores para reflejar patrones actuales de arquitectura MCP
  - Hosts definidos claramente como aplicaciones de IA que coordinan múltiples conexiones de clientes MCP
  - Clientes descritos como conectores de protocolo que mantienen relaciones uno a uno con servidores
  - Servidores mejorados con escenarios de despliegue local vs. remoto
- **Reestructuración de Primitivas**: Revisión completa de primitivas de servidor y cliente
  - Primitivas de Servidor: Recursos (fuentes de datos), Prompts (plantillas), Herramientas (funciones ejecutables) con explicaciones y ejemplos detallados
  - Primitivas de Cliente: Muestreo (completaciones de LLM), Elicitación (entrada del usuario), Registro (depuración/monitoreo)
  - Actualizado con patrones actuales de descubrimiento (`*/list`), recuperación (`*/get`) y ejecución (`*/call`)
- **Arquitectura de Protocolo**: Introducción de un modelo de arquitectura de dos capas
  - Capa de Datos: Fundamento JSON-RPC 2.0 con gestión del ciclo de vida y primitivas
  - Capa de Transporte: STDIO (local) y HTTP transmisible con SSE (remoto)
- **Marco de Seguridad**: Principios de seguridad completos, incluyendo consentimiento explícito del usuario, protección de privacidad de datos, seguridad en la ejecución de herramientas y seguridad en la capa de transporte
- **Patrones de Comunicación**: Mensajes de protocolo actualizados para mostrar flujos de inicialización, descubrimiento, ejecución y notificación
- **Ejemplos de Código**: Ejemplos renovados en múltiples lenguajes (.NET, Java, Python, JavaScript) para reflejar patrones actuales del SDK MCP

#### Seguridad (02-Security/) - Revisión Integral de Seguridad  
- **Alineación con Estándares**: Total alineación con los requisitos de seguridad de la Especificación MCP 2025-06-18
- **Evolución de Autenticación**: Documentación de la evolución desde servidores OAuth personalizados a delegación de proveedores de identidad externos (Microsoft Entra ID)
- **Análisis de Amenazas Específicas de IA**: Cobertura mejorada de vectores de ataque modernos en IA
  - Escenarios detallados de ataques de inyección de prompts con ejemplos reales
  - Mecanismos de envenenamiento de herramientas y patrones de ataque "rug pull"
  - Envenenamiento de ventanas de contexto y ataques de confusión de modelos
- **Soluciones de Seguridad de IA de Microsoft**: Cobertura completa del ecosistema de seguridad de Microsoft
  - Prompt Shields de IA con técnicas avanzadas de detección, delimitación y resaltado
  - Patrones de integración de Azure Content Safety
  - Seguridad avanzada de GitHub para protección de la cadena de suministro
- **Mitigación Avanzada de Amenazas**: Controles de seguridad detallados para:
  - Secuestro de sesiones con escenarios de ataque específicos de MCP y requisitos criptográficos de ID de sesión
  - Problemas de Confused Deputy en escenarios de proxy MCP con requisitos explícitos de consentimiento
  - Vulnerabilidades de Token Passthrough con controles de validación obligatorios
- **Seguridad en la Cadena de Suministro**: Cobertura ampliada de la cadena de suministro de IA, incluyendo modelos base, servicios de embeddings, proveedores de contexto y APIs de terceros
- **Seguridad Fundamental**: Integración mejorada con patrones de seguridad empresarial, incluyendo arquitectura de confianza cero y ecosistema de seguridad de Microsoft
- **Organización de Recursos**: Enlaces de recursos categorizados por tipo (Documentos Oficiales, Estándares, Investigación, Soluciones de Microsoft, Guías de Implementación)

### Mejoras en la Calidad de Documentación
- **Objetivos de Aprendizaje Estructurados**: Objetivos de aprendizaje mejorados con resultados específicos y accionables
- **Referencias Cruzadas**: Enlaces añadidos entre temas relacionados de seguridad y conceptos básicos
- **Información Actualizada**: Todas las referencias de fechas y enlaces de especificaciones actualizados a estándares actuales
- **Guía de Implementación**: Directrices específicas y accionables añadidas en ambas secciones

## 16 de julio de 2025

### Mejoras en README y Navegación
- Rediseño completo de la navegación del currículo en README.md
- Sustitución de etiquetas `<details>` por un formato basado en tablas más accesible
- Creación de opciones de diseño alternativas en la nueva carpeta "alternative_layouts"
- Ejemplos de navegación con estilo de tarjetas, pestañas y acordeón añadidos
- Actualización de la sección de estructura del repositorio para incluir todos los archivos más recientes
- Mejora de la sección "Cómo usar este currículo" con recomendaciones claras
- Actualización de enlaces de especificación MCP para apuntar a las URLs correctas
- Adición de la sección de Ingeniería de Contexto (5.14) a la estructura del currículo

### Actualizaciones de la Guía de Estudio
- Revisión completa de la guía de estudio para alinearla con la estructura actual del repositorio
- Nuevas secciones añadidas para Clientes y Herramientas MCP, y Servidores MCP Populares
- Actualización del Mapa Visual del Currículo para reflejar con precisión todos los temas
- Descripciones mejoradas de Temas Avanzados para cubrir todas las áreas especializadas
- Actualización de la sección de Estudios de Caso para reflejar ejemplos reales
- Adición de este registro de cambios completo

### Contribuciones de la Comunidad (06-CommunityContributions/)
- Información detallada añadida sobre servidores MCP para generación de imágenes
- Sección completa añadida sobre el uso de Claude en VSCode
- Instrucciones de configuración y uso del cliente terminal Cline añadidas
- Actualización de la sección de clientes MCP para incluir todas las opciones populares
- Ejemplos de contribución mejorados con muestras de código más precisas

### Temas Avanzados (05-AdvancedTopics/)
- Organización de todas las carpetas de temas especializados con nombres consistentes
- Materiales y ejemplos de ingeniería de contexto añadidos
- Documentación de integración de agentes Foundry añadida
- Documentación mejorada de integración de seguridad con Entra ID

## 11 de junio de 2025

### Creación Inicial
- Lanzamiento de la primera versión del currículo MCP para Principiantes
- Creación de la estructura básica para las 10 secciones principales
- Implementación del Mapa Visual del Currículo para navegación
- Adición de proyectos de muestra iniciales en múltiples lenguajes de programación

### Primeros Pasos (03-GettingStarted/)
- Creación de los primeros ejemplos de implementación de servidores
- Adición de orientación para desarrollo de clientes
- Inclusión de instrucciones de integración de clientes LLM
- Documentación de integración con VS Code añadida
- Ejemplos de servidores con Server-Sent Events (SSE) implementados

### Conceptos Básicos (01-CoreConcepts/)
- Explicación detallada añadida sobre arquitectura cliente-servidor
- Creación de documentación sobre componentes clave del protocolo
- Documentación de patrones de mensajería en MCP

## 23 de mayo de 2025

### Estructura del Repositorio
- Inicialización del repositorio con estructura básica de carpetas
- Creación de archivos README para cada sección principal
- Configuración de infraestructura de traducción
- Adición de activos de imagen y diagramas

### Documentación
- Creación inicial de README.md con visión general del currículo
- Adición de CODE_OF_CONDUCT.md y SECURITY.md
- Configuración de SUPPORT.md con orientación para obtener ayuda
- Creación de estructura preliminar de guía de estudio

## 15 de abril de 2025

### Planificación y Marco
- Planificación inicial del currículo MCP para Principiantes
- Definición de objetivos de aprendizaje y público objetivo
- Esbozo de la estructura de 10 secciones del currículo
- Desarrollo del marco conceptual para ejemplos y estudios de caso
- Creación de prototipos iniciales de ejemplos para conceptos clave

---

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por garantizar la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.