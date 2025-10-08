<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T11:40:21+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "es"
}
-->
# Seguridad MCP: Protección Integral para Sistemas de IA

[![Mejores Prácticas de Seguridad MCP](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.es.png)](https://youtu.be/88No8pw706o)

_(Haz clic en la imagen de arriba para ver el video de esta lección)_

La seguridad es fundamental en el diseño de sistemas de IA, por lo que la priorizamos como nuestra segunda sección. Esto está alineado con el principio de **Seguridad por Diseño** de Microsoft, parte de la [Iniciativa de Futuro Seguro](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

El Protocolo de Contexto de Modelos (MCP) aporta capacidades poderosas a las aplicaciones impulsadas por IA, pero también introduce desafíos únicos de seguridad que van más allá de los riesgos tradicionales del software. Los sistemas MCP enfrentan preocupaciones de seguridad establecidas (codificación segura, privilegios mínimos, seguridad en la cadena de suministro) y nuevas amenazas específicas de IA, como inyección de prompts, envenenamiento de herramientas, secuestro de sesiones, ataques de delegado confundido, vulnerabilidades de paso de tokens y modificación dinámica de capacidades.

Esta lección explora los riesgos de seguridad más críticos en las implementaciones de MCP, abarcando autenticación, autorización, permisos excesivos, inyección indirecta de prompts, seguridad de sesiones, problemas de delegado confundido, gestión de tokens y vulnerabilidades en la cadena de suministro. Aprenderás controles prácticos y mejores prácticas para mitigar estos riesgos mientras aprovechas soluciones de Microsoft como Prompt Shields, Azure Content Safety y GitHub Advanced Security para fortalecer tu implementación de MCP.

## Objetivos de Aprendizaje

Al final de esta lección, podrás:

- **Identificar Amenazas Específicas de MCP**: Reconocer riesgos únicos de seguridad en sistemas MCP, incluyendo inyección de prompts, envenenamiento de herramientas, permisos excesivos, secuestro de sesiones, problemas de delegado confundido, vulnerabilidades de paso de tokens y riesgos en la cadena de suministro.
- **Aplicar Controles de Seguridad**: Implementar mitigaciones efectivas como autenticación robusta, acceso con privilegios mínimos, gestión segura de tokens, controles de seguridad de sesiones y verificación de la cadena de suministro.
- **Aprovechar Soluciones de Seguridad de Microsoft**: Entender y desplegar Microsoft Prompt Shields, Azure Content Safety y GitHub Advanced Security para proteger cargas de trabajo MCP.
- **Validar la Seguridad de Herramientas**: Reconocer la importancia de validar metadatos de herramientas, monitorear cambios dinámicos y defenderse contra ataques de inyección indirecta de prompts.
- **Integrar Mejores Prácticas**: Combinar fundamentos de seguridad establecidos (codificación segura, endurecimiento de servidores, confianza cero) con controles específicos de MCP para una protección integral.

# Arquitectura y Controles de Seguridad MCP

Las implementaciones modernas de MCP requieren enfoques de seguridad en capas que aborden tanto las amenazas tradicionales de software como las específicas de IA. La especificación MCP, que evoluciona rápidamente, continúa madurando sus controles de seguridad, permitiendo una mejor integración con arquitecturas de seguridad empresariales y mejores prácticas establecidas.

Investigaciones del [Informe de Defensa Digital de Microsoft](https://aka.ms/mddr) demuestran que **el 98% de las brechas reportadas se evitarían con una higiene de seguridad robusta**. La estrategia de protección más efectiva combina prácticas de seguridad fundamentales con controles específicos de MCP: las medidas de seguridad básicas comprobadas siguen siendo las más impactantes para reducir el riesgo general.

## Panorama Actual de Seguridad

> **Nota:** Esta información refleja los estándares de seguridad MCP al **18 de agosto de 2025**. El protocolo MCP continúa evolucionando rápidamente, y las implementaciones futuras pueden introducir nuevos patrones de autenticación y controles mejorados. Consulta siempre la [Especificación MCP actual](https://spec.modelcontextprotocol.io/), el [repositorio GitHub de MCP](https://github.com/modelcontextprotocol) y la [documentación de mejores prácticas de seguridad](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) para obtener la orientación más reciente.

### Evolución de la Autenticación MCP

La especificación MCP ha evolucionado significativamente en su enfoque hacia la autenticación y autorización:

- **Enfoque Original**: Las especificaciones iniciales requerían que los desarrolladores implementaran servidores de autenticación personalizados, con servidores MCP actuando como Servidores de Autorización OAuth 2.0 gestionando la autenticación de usuarios directamente.
- **Estándar Actual (2025-06-18)**: La especificación actualizada permite que los servidores MCP deleguen la autenticación a proveedores de identidad externos (como Microsoft Entra ID), mejorando la postura de seguridad y reduciendo la complejidad de implementación.
- **Seguridad de la Capa de Transporte**: Soporte mejorado para mecanismos de transporte seguro con patrones de autenticación adecuados tanto para conexiones locales (STDIO) como remotas (HTTP Streamable).

## Seguridad de Autenticación y Autorización

### Desafíos Actuales de Seguridad

Las implementaciones modernas de MCP enfrentan varios desafíos de autenticación y autorización:

### Riesgos y Vectores de Amenaza

- **Lógica de Autorización Mal Configurada**: Implementaciones defectuosas de autorización en servidores MCP pueden exponer datos sensibles y aplicar controles de acceso incorrectamente.
- **Compromiso de Tokens OAuth**: El robo de tokens de servidores MCP locales permite a los atacantes suplantar servidores y acceder a servicios descendentes.
- **Vulnerabilidades de Paso de Tokens**: El manejo inadecuado de tokens crea bypasses de controles de seguridad y brechas de responsabilidad.
- **Permisos Excesivos**: Servidores MCP con privilegios excesivos violan principios de privilegios mínimos y amplían las superficies de ataque.

#### Paso de Tokens: Un Patrón Crítico Prohibido

**El paso de tokens está explícitamente prohibido** en la especificación actual de autorización MCP debido a graves implicaciones de seguridad:

##### Circunvención de Controles de Seguridad
- Los servidores MCP y las API descendentes implementan controles de seguridad críticos (limitación de tasas, validación de solicitudes, monitoreo de tráfico) que dependen de la validación adecuada de tokens.
- El uso directo de tokens cliente-API elude estas protecciones esenciales, socavando la arquitectura de seguridad.

##### Desafíos de Responsabilidad y Auditoría  
- Los servidores MCP no pueden distinguir entre clientes que usan tokens emitidos por upstream, rompiendo las trazas de auditoría.
- Los registros de servidores de recursos descendentes muestran orígenes de solicitud engañosos en lugar de intermediarios reales del servidor MCP.
- La investigación de incidentes y las auditorías de cumplimiento se vuelven significativamente más difíciles.

##### Riesgos de Exfiltración de Datos
- Las reclamaciones de tokens no validadas permiten que actores maliciosos con tokens robados usen servidores MCP como proxies para la exfiltración de datos.
- Las violaciones de límites de confianza permiten patrones de acceso no autorizados que eluden los controles de seguridad previstos.

##### Vectores de Ataque Multi-Servicio
- Los tokens comprometidos aceptados por múltiples servicios permiten movimientos laterales a través de sistemas conectados.
- Las suposiciones de confianza entre servicios pueden ser violadas cuando los orígenes de los tokens no pueden ser verificados.

### Controles de Seguridad y Mitigaciones

**Requisitos Críticos de Seguridad:**

> **OBLIGATORIO**: Los servidores MCP **NO DEBEN** aceptar tokens que no hayan sido emitidos explícitamente para el servidor MCP.

#### Controles de Autenticación y Autorización

- **Revisión Rigurosa de Autorización**: Realizar auditorías exhaustivas de la lógica de autorización del servidor MCP para garantizar que solo los usuarios y clientes previstos puedan acceder a recursos sensibles.
  - **Guía de Implementación**: [Azure API Management como Gateway de Autenticación para Servidores MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Integración de Identidad**: [Uso de Microsoft Entra ID para Autenticación de Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Gestión Segura de Tokens**: Implementar [prácticas recomendadas de validación y ciclo de vida de tokens de Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens).
  - Validar que las reclamaciones de audiencia de tokens coincidan con la identidad del servidor MCP.
  - Implementar políticas adecuadas de rotación y expiración de tokens.
  - Prevenir ataques de repetición de tokens y usos no autorizados.

- **Almacenamiento Protegido de Tokens**: Almacenamiento seguro de tokens con cifrado tanto en reposo como en tránsito.
  - **Mejores Prácticas**: [Guías de Almacenamiento Seguro y Cifrado de Tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2).

#### Implementación de Control de Acceso

- **Principio de Privilegio Mínimo**: Otorgar a los servidores MCP solo los permisos mínimos necesarios para la funcionalidad prevista.
  - Revisiones regulares de permisos y actualizaciones para prevenir acumulación de privilegios.
  - **Documentación de Microsoft**: [Acceso Seguro con Privilegios Mínimos](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access).

- **Control de Acceso Basado en Roles (RBAC)**: Implementar asignaciones de roles granulares.
  - Limitar roles estrictamente a recursos y acciones específicas.
  - Evitar permisos amplios o innecesarios que amplíen las superficies de ataque.

- **Monitoreo Continuo de Permisos**: Implementar auditorías y monitoreo continuo de acceso.
  - Monitorear patrones de uso de permisos para detectar anomalías.
  - Remediar rápidamente privilegios excesivos o no utilizados.

## Amenazas Específicas de IA

### Ataques de Inyección de Prompts y Manipulación de Herramientas

Las implementaciones modernas de MCP enfrentan vectores de ataque sofisticados específicos de IA que las medidas tradicionales de seguridad no pueden abordar completamente:

#### **Inyección Indirecta de Prompts (Inyección de Prompts entre Dominios)**

La **Inyección Indirecta de Prompts** representa una de las vulnerabilidades más críticas en sistemas de IA habilitados por MCP. Los atacantes incrustan instrucciones maliciosas dentro de contenido externo—documentos, páginas web, correos electrónicos o fuentes de datos—que los sistemas de IA procesan posteriormente como comandos legítimos.

**Escenarios de Ataque:**
- **Inyección basada en Documentos**: Instrucciones maliciosas ocultas en documentos procesados que desencadenan acciones no deseadas de IA.
- **Explotación de Contenido Web**: Páginas web comprometidas con prompts incrustados que manipulan el comportamiento de IA al ser analizadas.
- **Ataques basados en Correos Electrónicos**: Prompts maliciosos en correos electrónicos que hacen que asistentes de IA filtren información o realicen acciones no autorizadas.
- **Contaminación de Fuentes de Datos**: Bases de datos o APIs comprometidas que sirven contenido contaminado a sistemas de IA.

**Impacto en el Mundo Real**: Estos ataques pueden resultar en exfiltración de datos, violaciones de privacidad, generación de contenido dañino y manipulación de interacciones de usuarios. Para un análisis detallado, consulta [Inyección de Prompts en MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Diagrama de Ataque de Inyección de Prompts](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.es.png)

#### **Ataques de Envenenamiento de Herramientas**

El **Envenenamiento de Herramientas** apunta a los metadatos que definen las herramientas MCP, explotando cómo los LLMs interpretan descripciones de herramientas y parámetros para tomar decisiones de ejecución.

**Mecanismos de Ataque:**
- **Manipulación de Metadatos**: Los atacantes inyectan instrucciones maliciosas en descripciones de herramientas, definiciones de parámetros o ejemplos de uso.
- **Instrucciones Invisibles**: Prompts ocultos en metadatos de herramientas que son procesados por modelos de IA pero invisibles para usuarios humanos.
- **Modificación Dinámica de Herramientas ("Rug Pulls")**: Herramientas aprobadas por usuarios son modificadas posteriormente para realizar acciones maliciosas sin que los usuarios lo sepan.
- **Inyección de Parámetros**: Contenido malicioso incrustado en esquemas de parámetros de herramientas que influye en el comportamiento del modelo.

**Riesgos en Servidores Hospedados**: Los servidores MCP remotos presentan riesgos elevados ya que las definiciones de herramientas pueden ser actualizadas después de la aprobación inicial del usuario, creando escenarios donde herramientas previamente seguras se vuelven maliciosas. Para un análisis exhaustivo, consulta [Ataques de Envenenamiento de Herramientas (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Diagrama de Inyección de Herramientas](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.es.png)

#### **Vectores de Ataque Adicionales de IA**

- **Inyección de Prompts entre Dominios (XPIA)**: Ataques sofisticados que aprovechan contenido de múltiples dominios para eludir controles de seguridad.
- **Modificación Dinámica de Capacidades**: Cambios en tiempo real a capacidades de herramientas que escapan a evaluaciones iniciales de seguridad.
- **Envenenamiento de Ventanas de Contexto**: Ataques que manipulan grandes ventanas de contexto para ocultar instrucciones maliciosas.
- **Ataques de Confusión de Modelos**: Explotación de limitaciones del modelo para crear comportamientos impredecibles o inseguros.

### Impacto de Riesgos de Seguridad de IA

**Consecuencias de Alto Impacto:**
- **Exfiltración de Datos**: Acceso no autorizado y robo de datos sensibles empresariales o personales.
- **Violaciones de Privacidad**: Exposición de información personal identificable (PII) y datos confidenciales de negocios.
- **Manipulación de Sistemas**: Modificaciones no deseadas a sistemas y flujos de trabajo críticos.
- **Robo de Credenciales**: Compromiso de tokens de autenticación y credenciales de servicio.
- **Movimiento Lateral**: Uso de sistemas de IA comprometidos como pivotes para ataques más amplios en la red.

### Soluciones de Seguridad de IA de Microsoft

#### **AI Prompt Shields: Protección Avanzada Contra Ataques de Inyección**

Microsoft **AI Prompt Shields** proporciona defensa integral contra ataques de inyección de prompts directos e indirectos a través de múltiples capas de seguridad:

##### **Mecanismos de Protección Principales:**

1. **Detección y Filtrado Avanzados**
   - Algoritmos de aprendizaje automático y técnicas de NLP detectan instrucciones maliciosas en contenido externo.
   - Análisis en tiempo real de documentos, páginas web, correos electrónicos y fuentes de datos para identificar amenazas incrustadas.
   - Comprensión contextual de patrones legítimos frente a maliciosos.

2. **Técnicas de Spotlighting**  
   - Distingue entre instrucciones confiables del sistema y entradas externas potencialmente comprometidas.
   - Métodos de transformación de texto que mejoran la relevancia del modelo mientras aíslan contenido malicioso.
   - Ayuda a los sistemas de IA a mantener una jerarquía adecuada de instrucciones e ignorar comandos inyectados.

3. **Sistemas de Delimitación y Marcado de Datos**
   - Definición explícita de límites entre mensajes confiables del sistema y texto de entrada externo.
   - Marcadores especiales resaltan límites entre fuentes de datos confiables y no confiables.
   - Separación clara previene confusión de instrucciones y ejecución de comandos no autorizados.

4. **Inteligencia Continua de Amenazas**
   - Microsoft monitorea continuamente patrones de ataque emergentes y actualiza las defensas.
   - Búsqueda proactiva de nuevas técnicas de inyección y vectores de ataque.
   - Actualizaciones regulares de modelos de seguridad para mantener la efectividad contra amenazas en evolución.

5. **Integración con Azure Content Safety**
   - Parte de la suite integral de Azure AI Content Safety.
   - Detección adicional de intentos de jailbreak, contenido dañino y violaciones de políticas de seguridad.
   - Controles de seguridad unificados en componentes de aplicaciones de IA.

**Recursos de Implementación**: [Documentación de Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection).

![Protección de Microsoft Prompt Shields](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.es.png)

## Amenazas Avanzadas de Seguridad MCP

### Vulnerabilidades de Secuestro de Sesiones

El **secuestro de sesiones** representa un vector de ataque crítico en implementaciones MCP con estado, donde partes no autorizadas obtienen y abusan de identificadores de sesión legítimos para suplantar clientes y realizar acciones no autorizadas.

#### **Escenarios de Ataque y Riesgos**

- **Inyección de Prompts en Secuestro de Sesiones**: Los atacantes con IDs de sesión robados inyectan eventos maliciosos en servidores que comparten estado de sesión, potencialmente desencadenando acciones dañinas o accediendo a datos sensibles.
- **Suplantación Directa**: IDs de sesión robados permiten llamadas directas a servidores MCP que eluden la autenticación, tratando a los atacantes como usuarios legítimos.
- **Streams Reanudables Comprometidos**: Los atacantes pueden terminar solicitudes prematuramente, causando que los clientes legítimos reanuden con contenido potencialmente malicioso.

#### **Controles de Seguridad para Gestión de Sesiones**

**Requisitos Críticos:**
- **Verificación de Autorización**: Los servidores MCP que implementen autorización **DEBEN** verificar TODAS las solicitudes entrantes y **NO DEBEN** depender de sesiones para autenticación.
- **Generación Segura de Sesiones**: Usa identificadores de sesión criptográficamente seguros y no deterministas generados con generadores de números aleatorios seguros  
- **Vinculación Específica del Usuario**: Vincula los identificadores de sesión a información específica del usuario utilizando formatos como `<user_id>:<session_id>` para prevenir el abuso de sesiones entre usuarios  
- **Gestión del Ciclo de Vida de la Sesión**: Implementa expiración, rotación e invalidación adecuadas para limitar las ventanas de vulnerabilidad  
- **Seguridad en el Transporte**: HTTPS obligatorio para todas las comunicaciones para evitar la intercepción de identificadores de sesión  

### Problema del Delegado Confundido

El **problema del delegado confundido** ocurre cuando los servidores MCP actúan como proxies de autenticación entre clientes y servicios de terceros, creando oportunidades para eludir la autorización mediante la explotación de identificadores de cliente estáticos.

#### **Mecánica del Ataque y Riesgos**

- **Elusión de Consentimiento Basada en Cookies**: La autenticación previa del usuario genera cookies de consentimiento que los atacantes explotan mediante solicitudes de autorización maliciosas con URIs de redirección manipulados  
- **Robo de Códigos de Autorización**: Las cookies de consentimiento existentes pueden hacer que los servidores de autorización omitan las pantallas de consentimiento, redirigiendo los códigos a puntos finales controlados por atacantes  
- **Acceso No Autorizado a APIs**: Los códigos de autorización robados permiten el intercambio de tokens y la suplantación de usuarios sin aprobación explícita  

#### **Estrategias de Mitigación**

**Controles Obligatorios:**
- **Requisitos de Consentimiento Explícito**: Los servidores proxy MCP que usan identificadores de cliente estáticos **DEBEN** obtener el consentimiento del usuario para cada cliente registrado dinámicamente  
- **Implementación de Seguridad OAuth 2.1**: Sigue las mejores prácticas actuales de seguridad OAuth, incluyendo PKCE (Prueba de Clave para el Intercambio de Códigos) para todas las solicitudes de autorización  
- **Validación Estricta de Clientes**: Implementa una validación rigurosa de los URIs de redirección y los identificadores de cliente para prevenir la explotación  

### Vulnerabilidades de Passthrough de Tokens  

El **passthrough de tokens** representa un anti-patrón explícito donde los servidores MCP aceptan tokens de cliente sin validación adecuada y los reenvían a APIs downstream, violando las especificaciones de autorización de MCP.

#### **Implicaciones de Seguridad**

- **Elusión de Controles**: El uso directo de tokens cliente a API evita controles críticos como limitación de tasa, validación y monitoreo  
- **Corrupción de la Pista de Auditoría**: Los tokens emitidos upstream hacen imposible identificar al cliente, dificultando las investigaciones de incidentes  
- **Exfiltración de Datos Basada en Proxy**: Los tokens no validados permiten a actores maliciosos usar servidores como proxies para acceder a datos no autorizados  
- **Violaciones de Límites de Confianza**: Los supuestos de confianza de los servicios downstream pueden ser violados cuando no se puede verificar el origen de los tokens  
- **Expansión de Ataques Multi-servicio**: Los tokens comprometidos aceptados en múltiples servicios permiten movimientos laterales  

#### **Controles de Seguridad Requeridos**

**Requisitos No Negociables:**
- **Validación de Tokens**: Los servidores MCP **NO DEBEN** aceptar tokens que no hayan sido emitidos explícitamente para el servidor MCP  
- **Verificación de Audiencia**: Siempre valida que las afirmaciones de audiencia del token coincidan con la identidad del servidor MCP  
- **Ciclo de Vida Adecuado de Tokens**: Implementa tokens de acceso de corta duración con prácticas seguras de rotación  

## Seguridad de la Cadena de Suministro para Sistemas de IA

La seguridad de la cadena de suministro ha evolucionado más allá de las dependencias tradicionales de software para abarcar todo el ecosistema de IA. Las implementaciones modernas de MCP deben verificar y monitorear rigurosamente todos los componentes relacionados con IA, ya que cada uno introduce posibles vulnerabilidades que podrían comprometer la integridad del sistema.

### Componentes Ampliados de la Cadena de Suministro de IA

**Dependencias Tradicionales de Software:**
- Bibliotecas y frameworks de código abierto  
- Imágenes de contenedores y sistemas base  
- Herramientas de desarrollo y pipelines de construcción  
- Componentes y servicios de infraestructura  

**Elementos Específicos de la Cadena de Suministro de IA:**
- **Modelos Fundamentales**: Modelos preentrenados de diversos proveedores que requieren verificación de procedencia  
- **Servicios de Embedding**: Servicios externos de vectorización y búsqueda semántica  
- **Proveedores de Contexto**: Fuentes de datos, bases de conocimiento y repositorios de documentos  
- **APIs de Terceros**: Servicios externos de IA, pipelines de ML y puntos finales de procesamiento de datos  
- **Artefactos de Modelos**: Pesos, configuraciones y variantes de modelos ajustados  
- **Fuentes de Datos de Entrenamiento**: Conjuntos de datos utilizados para el entrenamiento y ajuste de modelos  

### Estrategia Integral de Seguridad de la Cadena de Suministro

#### **Verificación de Componentes y Confianza**
- **Validación de Procedencia**: Verifica el origen, la licencia y la integridad de todos los componentes de IA antes de la integración  
- **Evaluación de Seguridad**: Realiza análisis de vulnerabilidades y revisiones de seguridad para modelos, fuentes de datos y servicios de IA  
- **Análisis de Reputación**: Evalúa el historial de seguridad y las prácticas de los proveedores de servicios de IA  
- **Verificación de Cumplimiento**: Asegúrate de que todos los componentes cumplan con los requisitos de seguridad y normativos de la organización  

#### **Pipelines de Despliegue Seguro**  
- **Seguridad Automatizada en CI/CD**: Integra escaneos de seguridad en los pipelines de despliegue automatizados  
- **Integridad de Artefactos**: Implementa verificaciones criptográficas para todos los artefactos desplegados (código, modelos, configuraciones)  
- **Despliegue por Etapas**: Usa estrategias de despliegue progresivo con validación de seguridad en cada etapa  
- **Repositorios de Artefactos Confiables**: Despliega únicamente desde registros y repositorios de artefactos verificados y seguros  

#### **Monitoreo Continuo y Respuesta**
- **Escaneo de Dependencias**: Monitoreo continuo de vulnerabilidades en todas las dependencias de software y componentes de IA  
- **Monitoreo de Modelos**: Evaluación continua del comportamiento del modelo, el desvío de rendimiento y las anomalías de seguridad  
- **Seguimiento de Salud del Servicio**: Monitorea servicios externos de IA para disponibilidad, incidentes de seguridad y cambios en políticas  
- **Integración de Inteligencia de Amenazas**: Incorpora fuentes de amenazas específicas para riesgos de seguridad en IA y ML  

#### **Control de Acceso y Mínimos Privilegios**
- **Permisos a Nivel de Componente**: Restringe el acceso a modelos, datos y servicios según la necesidad empresarial  
- **Gestión de Cuentas de Servicio**: Implementa cuentas de servicio dedicadas con los permisos mínimos necesarios  
- **Segmentación de Red**: Aísla los componentes de IA y limita el acceso de red entre servicios  
- **Controles de Gateway de API**: Usa gateways de API centralizados para controlar y monitorear el acceso a servicios externos de IA  

#### **Respuesta a Incidentes y Recuperación**
- **Procedimientos de Respuesta Rápida**: Procesos establecidos para parchear o reemplazar componentes de IA comprometidos  
- **Rotación de Credenciales**: Sistemas automatizados para rotar secretos, claves de API y credenciales de servicio  
- **Capacidades de Reversión**: Habilidad para revertir rápidamente a versiones anteriores conocidas como seguras de componentes de IA  
- **Recuperación de Brechas en la Cadena de Suministro**: Procedimientos específicos para responder a compromisos de servicios de IA upstream  

### Herramientas de Seguridad de Microsoft e Integración

**GitHub Advanced Security** proporciona protección integral de la cadena de suministro, incluyendo:  
- **Escaneo de Secretos**: Detección automatizada de credenciales, claves de API y tokens en repositorios  
- **Escaneo de Dependencias**: Evaluación de vulnerabilidades para dependencias y bibliotecas de código abierto  
- **Análisis CodeQL**: Análisis estático de código para vulnerabilidades de seguridad y problemas de codificación  
- **Insights de la Cadena de Suministro**: Visibilidad sobre la salud y el estado de seguridad de las dependencias  

**Integración con Azure DevOps y Azure Repos:**
- Integración fluida de escaneos de seguridad en plataformas de desarrollo de Microsoft  
- Chequeos de seguridad automatizados en Azure Pipelines para cargas de trabajo de IA  
- Aplicación de políticas para el despliegue seguro de componentes de IA  

**Prácticas Internas de Microsoft:**
Microsoft implementa prácticas extensivas de seguridad en la cadena de suministro en todos sus productos. Aprende sobre enfoques probados en [El Viaje para Asegurar la Cadena de Suministro de Software en Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Soluciones de Seguridad de Microsoft**
- [Documentación de Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Servicio de Seguridad de Contenido de Azure](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Seguridad de Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Mejores Prácticas para la Gestión de Tokens en Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Seguridad Avanzada de GitHub](https://github.com/security/advanced-security)

### **Guías de Implementación y Tutoriales**
- [Azure API Management como Gateway de Autenticación MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Autenticación de Microsoft Entra ID con Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Almacenamiento Seguro de Tokens y Encriptación (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps y Seguridad de la Cadena de Suministro**
- [Seguridad en Azure DevOps](https://azure.microsoft.com/products/devops)
- [Seguridad en Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [El Viaje de Microsoft hacia la Seguridad en la Cadena de Suministro](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Documentación Adicional de Seguridad**

Para obtener orientación completa sobre seguridad, consulta estos documentos especializados en esta sección:

- **[Mejores Prácticas de Seguridad MCP 2025](./mcp-security-best-practices-2025.md)** - Mejores prácticas completas de seguridad para implementaciones MCP
- **[Implementación de Seguridad de Contenido en Azure](./azure-content-safety-implementation.md)** - Ejemplos prácticos de integración de Seguridad de Contenido en Azure  
- **[Controles de Seguridad MCP 2025](./mcp-security-controls-2025.md)** - Controles y técnicas de seguridad más recientes para despliegues MCP
- **[Guía Rápida de Mejores Prácticas MCP](./mcp-best-practices.md)** - Guía de referencia rápida para prácticas esenciales de seguridad MCP

---

## Próximos Pasos

Siguiente: [Capítulo 3: Primeros Pasos](../03-GettingStarted/README.md)

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por garantizar la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.