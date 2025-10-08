<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T11:37:59+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "es"
}
-->
# Mejores Prácticas de Seguridad para MCP - Actualización de Agosto 2025

> **Importante**: Este documento refleja los últimos requisitos de seguridad de la [Especificación MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) y las [Mejores Prácticas de Seguridad de MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Siempre consulta la especificación actual para obtener la guía más actualizada.

## Prácticas Esenciales de Seguridad para Implementaciones de MCP

El Protocolo de Contexto de Modelo (MCP) introduce desafíos de seguridad únicos que van más allá de la seguridad tradicional del software. Estas prácticas abordan tanto los requisitos de seguridad fundamentales como las amenazas específicas de MCP, incluyendo inyección de prompts, envenenamiento de herramientas, secuestro de sesiones, problemas de delegación confusa y vulnerabilidades de paso de tokens.

### **Requisitos de Seguridad OBLIGATORIOS**

**Requisitos Críticos de la Especificación MCP:**

> **MUST NOT**: Los servidores MCP **NO DEBEN** aceptar tokens que no hayan sido emitidos explícitamente para el servidor MCP.  
> 
> **MUST**: Los servidores MCP que implementen autorización **DEBEN** verificar TODAS las solicitudes entrantes.  
>  
> **MUST NOT**: Los servidores MCP **NO DEBEN** usar sesiones para autenticación.  
>
> **MUST**: Los servidores proxy MCP que utilicen IDs de cliente estáticos **DEBEN** obtener el consentimiento del usuario para cada cliente registrado dinámicamente.

---

## 1. **Seguridad de Tokens y Autenticación**

**Controles de Autenticación y Autorización:**
   - **Revisión Rigurosa de Autorización**: Realiza auditorías exhaustivas de la lógica de autorización del servidor MCP para garantizar que solo los usuarios y clientes previstos puedan acceder a los recursos.  
   - **Integración con Proveedores de Identidad Externos**: Utiliza proveedores de identidad establecidos como Microsoft Entra ID en lugar de implementar autenticación personalizada.  
   - **Validación de Audiencia de Tokens**: Siempre valida que los tokens hayan sido emitidos explícitamente para tu servidor MCP; nunca aceptes tokens de upstream.  
   - **Ciclo de Vida Adecuado de Tokens**: Implementa rotación segura de tokens, políticas de expiración y prevén ataques de repetición de tokens.  

**Almacenamiento Protegido de Tokens:**
   - Usa Azure Key Vault o almacenes de credenciales seguros similares para todos los secretos.  
   - Implementa cifrado para tokens tanto en reposo como en tránsito.  
   - Realiza rotación regular de credenciales y monitorea accesos no autorizados.  

## 2. **Gestión de Sesiones y Seguridad en el Transporte**

**Prácticas Seguras de Sesión:**
   - **IDs de Sesión Criptográficamente Seguros**: Usa IDs de sesión seguros y no deterministas generados con generadores de números aleatorios seguros.  
   - **Vinculación Específica del Usuario**: Vincula los IDs de sesión a las identidades de usuario utilizando formatos como `<user_id>:<session_id>` para prevenir abusos entre usuarios.  
   - **Gestión del Ciclo de Vida de Sesiones**: Implementa expiración, rotación e invalidación adecuadas para limitar las ventanas de vulnerabilidad.  
   - **Aplicación de HTTPS/TLS**: HTTPS obligatorio para todas las comunicaciones para prevenir la intercepción de IDs de sesión.  

**Seguridad de la Capa de Transporte:**
   - Configura TLS 1.3 siempre que sea posible con una gestión adecuada de certificados.  
   - Implementa fijación de certificados para conexiones críticas.  
   - Realiza rotación regular de certificados y verifica su validez.  

## 3. **Protección contra Amenazas Específicas de IA** 🤖

**Defensa contra Inyección de Prompts:**
   - **Microsoft Prompt Shields**: Despliega AI Prompt Shields para la detección avanzada y el filtrado de instrucciones maliciosas.  
   - **Saneamiento de Entradas**: Valida y sanea todas las entradas para prevenir ataques de inyección y problemas de delegación confusa.  
   - **Delimitación de Contenidos**: Usa sistemas de delimitación y marcado de datos para distinguir entre instrucciones confiables y contenido externo.  

**Prevención de Envenenamiento de Herramientas:**
   - **Validación de Metadatos de Herramientas**: Implementa verificaciones de integridad para las definiciones de herramientas y monitorea cambios inesperados.  
   - **Monitoreo Dinámico de Herramientas**: Supervisa el comportamiento en tiempo de ejecución y configura alertas para patrones de ejecución inesperados.  
   - **Flujos de Trabajo de Aprobación**: Requiere aprobación explícita del usuario para modificaciones de herramientas y cambios de capacidades.  

## 4. **Control de Acceso y Permisos**

**Principio de Menor Privilegio:**
   - Otorga a los servidores MCP solo los permisos mínimos necesarios para la funcionalidad prevista.  
   - Implementa control de acceso basado en roles (RBAC) con permisos granulares.  
   - Realiza revisiones regulares de permisos y monitoreo continuo para detectar escaladas de privilegios.  

**Controles de Permisos en Tiempo de Ejecución:**
   - Aplica límites de recursos para prevenir ataques de agotamiento de recursos.  
   - Usa aislamiento de contenedores para entornos de ejecución de herramientas.  
   - Implementa acceso just-in-time para funciones administrativas.  

## 5. **Seguridad de Contenidos y Monitoreo**

**Implementación de Seguridad de Contenidos:**
   - **Integración con Azure Content Safety**: Usa Azure Content Safety para detectar contenido dañino, intentos de jailbreak y violaciones de políticas.  
   - **Análisis de Comportamiento**: Implementa monitoreo de comportamiento en tiempo de ejecución para detectar anomalías en la ejecución del servidor MCP y herramientas.  
   - **Registro Integral**: Registra todos los intentos de autenticación, invocaciones de herramientas y eventos de seguridad con almacenamiento seguro y a prueba de manipulaciones.  

**Monitoreo Continuo:**
   - Alertas en tiempo real para patrones sospechosos e intentos de acceso no autorizados.  
   - Integración con sistemas SIEM para la gestión centralizada de eventos de seguridad.  
   - Auditorías de seguridad regulares y pruebas de penetración de las implementaciones de MCP.  

## 6. **Seguridad de la Cadena de Suministro**

**Verificación de Componentes:**
   - **Escaneo de Dependencias**: Usa escaneo automatizado de vulnerabilidades para todas las dependencias de software y componentes de IA.  
   - **Validación de Procedencia**: Verifica el origen, las licencias y la integridad de modelos, fuentes de datos y servicios externos.  
   - **Paquetes Firmados**: Usa paquetes firmados criptográficamente y verifica las firmas antes del despliegue.  

**Pipeline de Desarrollo Seguro:**
   - **GitHub Advanced Security**: Implementa escaneo de secretos, análisis de dependencias y análisis estático con CodeQL.  
   - **Seguridad en CI/CD**: Integra validaciones de seguridad en los pipelines de despliegue automatizado.  
   - **Integridad de Artefactos**: Implementa verificaciones criptográficas para artefactos y configuraciones desplegados.  

## 7. **Seguridad OAuth y Prevención de Delegación Confusa**

**Implementación de OAuth 2.1:**
   - **Implementación de PKCE**: Usa Proof Key for Code Exchange (PKCE) para todas las solicitudes de autorización.  
   - **Consentimiento Explícito**: Obtén el consentimiento del usuario para cada cliente registrado dinámicamente para prevenir ataques de delegación confusa.  
   - **Validación de URI de Redirección**: Implementa validación estricta de URIs de redirección e identificadores de cliente.  

**Seguridad de Proxies:**
   - Prevén el bypass de autorización mediante la explotación de IDs de cliente estáticos.  
   - Implementa flujos de trabajo de consentimiento adecuados para el acceso a APIs de terceros.  
   - Monitorea el robo de códigos de autorización y el acceso no autorizado a APIs.  

## 8. **Respuesta a Incidentes y Recuperación**

**Capacidades de Respuesta Rápida:**
   - **Respuesta Automatizada**: Implementa sistemas automatizados para la rotación de credenciales y la contención de amenazas.  
   - **Procedimientos de Reversión**: Capacidad para revertir rápidamente a configuraciones y componentes conocidos como seguros.  
   - **Capacidades Forenses**: Registros detallados y trazas de auditoría para la investigación de incidentes.  

**Comunicación y Coordinación:**
   - Procedimientos claros de escalación para incidentes de seguridad.  
   - Integración con equipos organizacionales de respuesta a incidentes.  
   - Simulaciones regulares de incidentes de seguridad y ejercicios de mesa.  

## 9. **Cumplimiento y Gobernanza**

**Cumplimiento Normativo:**
   - Asegura que las implementaciones de MCP cumplan con los requisitos específicos de la industria (GDPR, HIPAA, SOC 2).  
   - Implementa controles de clasificación de datos y privacidad para el procesamiento de datos de IA.  
   - Mantén documentación completa para auditorías de cumplimiento.  

**Gestión de Cambios:**
   - Procesos formales de revisión de seguridad para todas las modificaciones del sistema MCP.  
   - Control de versiones y flujos de trabajo de aprobación para cambios de configuración.  
   - Evaluaciones regulares de cumplimiento y análisis de brechas.  

## 10. **Controles de Seguridad Avanzados**

**Arquitectura de Confianza Cero:**
   - **Nunca Confíes, Siempre Verifica**: Verificación continua de usuarios, dispositivos y conexiones.  
   - **Microsegmentación**: Controles de red granulares que aíslan componentes individuales de MCP.  
   - **Acceso Condicional**: Controles de acceso basados en riesgos que se adaptan al contexto y comportamiento actuales.  

**Protección de Aplicaciones en Tiempo de Ejecución:**
   - **Protección de Aplicaciones en Tiempo de Ejecución (RASP)**: Despliega técnicas RASP para la detección de amenazas en tiempo real.  
   - **Monitoreo del Rendimiento de Aplicaciones**: Supervisa anomalías de rendimiento que puedan indicar ataques.  
   - **Políticas de Seguridad Dinámicas**: Implementa políticas de seguridad que se adapten según el panorama de amenazas actual.  

## 11. **Integración con el Ecosistema de Seguridad de Microsoft**

**Seguridad Integral de Microsoft:**
   - **Microsoft Defender for Cloud**: Gestión de postura de seguridad en la nube para cargas de trabajo MCP.  
   - **Azure Sentinel**: Capacidades nativas de SIEM y SOAR para detección avanzada de amenazas.  
   - **Microsoft Purview**: Gobernanza de datos y cumplimiento para flujos de trabajo de IA y fuentes de datos.  

**Gestión de Identidad y Acceso:**
   - **Microsoft Entra ID**: Gestión de identidad empresarial con políticas de acceso condicional.  
   - **Privileged Identity Management (PIM)**: Acceso just-in-time y flujos de trabajo de aprobación para funciones administrativas.  
   - **Protección de Identidad**: Acceso condicional basado en riesgos y respuesta automatizada a amenazas.  

## 12. **Evolución Continua de la Seguridad**

**Manteniéndose al Día:**
   - **Monitoreo de Especificaciones**: Revisión regular de actualizaciones de la especificación MCP y cambios en la guía de seguridad.  
   - **Inteligencia de Amenazas**: Integración de fuentes de amenazas específicas de IA e indicadores de compromiso.  
   - **Participación en la Comunidad de Seguridad**: Participación activa en la comunidad de seguridad de MCP y programas de divulgación de vulnerabilidades.  

**Seguridad Adaptativa:**
   - **Seguridad Basada en Aprendizaje Automático**: Usa detección de anomalías basada en ML para identificar patrones de ataque novedosos.  
   - **Análisis Predictivo de Seguridad**: Implementa modelos predictivos para la identificación proactiva de amenazas.  
   - **Automatización de Seguridad**: Actualizaciones automatizadas de políticas de seguridad basadas en inteligencia de amenazas y cambios en la especificación.  

---

## **Recursos Críticos de Seguridad**

### **Documentación Oficial de MCP**
- [Especificación MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Mejores Prácticas de Seguridad de MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Especificación de Autorización de MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Soluciones de Seguridad de Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Seguridad de Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Estándares de Seguridad**
- [Mejores Prácticas de Seguridad OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 para Modelos de Lenguaje Extenso](https://genai.owasp.org/)  
- [Marco de Gestión de Riesgos de IA de NIST](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Guías de Implementación**
- [Gateway de Autenticación MCP con Azure API Management](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID con Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Aviso de Seguridad**: Las prácticas de seguridad de MCP evolucionan rápidamente. Siempre verifica contra la [especificación actual de MCP](https://spec.modelcontextprotocol.io/) y la [documentación oficial de seguridad](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) antes de la implementación.  

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Si bien nos esforzamos por lograr precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.