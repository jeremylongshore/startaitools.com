<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T11:41:48+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "es"
}
-->
# Prácticas de Seguridad MCP 2025

Esta guía completa detalla las prácticas esenciales de seguridad para implementar sistemas del Protocolo de Contexto de Modelo (MCP) basados en la última **Especificación MCP 2025-06-18** y los estándares actuales de la industria. Estas prácticas abordan tanto preocupaciones tradicionales de seguridad como amenazas específicas de IA únicas en los despliegues de MCP.

## Requisitos Críticos de Seguridad

### Controles de Seguridad Obligatorios (Requisitos MUST)

1. **Validación de Tokens**: Los servidores MCP **NO DEBEN** aceptar tokens que no hayan sido emitidos explícitamente para el propio servidor MCP.
2. **Verificación de Autorización**: Los servidores MCP que implementen autorización **DEBEN** verificar TODAS las solicitudes entrantes y **NO DEBEN** usar sesiones para autenticación.  
3. **Consentimiento del Usuario**: Los servidores proxy MCP que utilicen IDs de cliente estáticos **DEBEN** obtener el consentimiento explícito del usuario para cada cliente registrado dinámicamente.
4. **IDs de Sesión Seguros**: Los servidores MCP **DEBEN** usar IDs de sesión criptográficamente seguros y no determinísticos generados con generadores de números aleatorios seguros.

## Prácticas Fundamentales de Seguridad

### 1. Validación y Saneamiento de Entradas
- **Validación Exhaustiva de Entradas**: Validar y sanear todas las entradas para prevenir ataques de inyección, problemas de delegación confusa y vulnerabilidades de inyección de prompts.
- **Aplicación de Esquemas de Parámetros**: Implementar validación estricta de esquemas JSON para todos los parámetros de herramientas y entradas de API.
- **Filtrado de Contenido**: Utilizar Microsoft Prompt Shields y Azure Content Safety para filtrar contenido malicioso en prompts y respuestas.
- **Saneamiento de Salidas**: Validar y sanear todas las salidas del modelo antes de presentarlas a los usuarios o sistemas posteriores.

### 2. Excelencia en Autenticación y Autorización  
- **Proveedores de Identidad Externos**: Delegar la autenticación a proveedores de identidad establecidos (Microsoft Entra ID, proveedores OAuth 2.1) en lugar de implementar autenticación personalizada.
- **Permisos Granulares**: Implementar permisos específicos para herramientas siguiendo el principio de menor privilegio.
- **Gestión del Ciclo de Vida de Tokens**: Usar tokens de acceso de corta duración con rotación segura y validación adecuada de audiencia.
- **Autenticación Multifactor**: Requerir MFA para todo acceso administrativo y operaciones sensibles.

### 3. Protocolos de Comunicación Seguros
- **Seguridad de Capa de Transporte**: Usar HTTPS/TLS 1.3 para todas las comunicaciones MCP con validación adecuada de certificados.
- **Cifrado de Extremo a Extremo**: Implementar capas adicionales de cifrado para datos altamente sensibles en tránsito y en reposo.
- **Gestión de Certificados**: Mantener una gestión adecuada del ciclo de vida de certificados con procesos automatizados de renovación.
- **Aplicación de Versión de Protocolo**: Usar la versión actual del protocolo MCP (2025-06-18) con negociación adecuada de versiones.

### 4. Limitación Avanzada de Tasa y Protección de Recursos
- **Limitación de Tasa Multicapa**: Implementar limitación de tasa a nivel de usuario, sesión, herramienta y recurso para prevenir abusos.
- **Limitación de Tasa Adaptativa**: Usar limitación de tasa basada en aprendizaje automático que se adapte a patrones de uso e indicadores de amenazas.
- **Gestión de Cuotas de Recursos**: Establecer límites apropiados para recursos computacionales, uso de memoria y tiempo de ejecución.
- **Protección contra DDoS**: Desplegar sistemas completos de protección contra DDoS y análisis de tráfico.

### 5. Registro y Monitoreo Integral
- **Registro de Auditoría Estructurado**: Implementar registros detallados y buscables para todas las operaciones MCP, ejecuciones de herramientas y eventos de seguridad.
- **Monitoreo de Seguridad en Tiempo Real**: Desplegar sistemas SIEM con detección de anomalías impulsada por IA para cargas de trabajo MCP.
- **Registro Respetuoso con la Privacidad**: Registrar eventos de seguridad respetando los requisitos y regulaciones de privacidad de datos.
- **Integración de Respuesta a Incidentes**: Conectar sistemas de registro a flujos de trabajo automatizados de respuesta a incidentes.

### 6. Prácticas Mejoradas de Almacenamiento Seguro
- **Módulos de Seguridad de Hardware**: Usar almacenamiento de claves respaldado por HSM (Azure Key Vault, AWS CloudHSM) para operaciones criptográficas críticas.
- **Gestión de Claves de Cifrado**: Implementar rotación adecuada de claves, segregación y controles de acceso para claves de cifrado.
- **Gestión de Secretos**: Almacenar todas las claves de API, tokens y credenciales en sistemas dedicados de gestión de secretos.
- **Clasificación de Datos**: Clasificar los datos según niveles de sensibilidad y aplicar medidas de protección adecuadas.

### 7. Gestión Avanzada de Tokens
- **Prevención de Passthrough de Tokens**: Prohibir explícitamente patrones de passthrough de tokens que eviten controles de seguridad.
- **Validación de Audiencia**: Verificar siempre que las afirmaciones de audiencia de los tokens coincidan con la identidad del servidor MCP previsto.
- **Autorización Basada en Afirmaciones**: Implementar autorización granular basada en afirmaciones de tokens y atributos de usuario.
- **Vinculación de Tokens**: Vincular tokens a sesiones, usuarios o dispositivos específicos cuando sea apropiado.

### 8. Gestión Segura de Sesiones
- **IDs de Sesión Criptográficos**: Generar IDs de sesión utilizando generadores de números aleatorios criptográficamente seguros (no secuencias predecibles).
- **Vinculación Específica del Usuario**: Vincular IDs de sesión a información específica del usuario utilizando formatos seguros como `<user_id>:<session_id>`.
- **Controles del Ciclo de Vida de Sesiones**: Implementar mecanismos adecuados de expiración, rotación e invalidación de sesiones.
- **Encabezados de Seguridad de Sesión**: Usar encabezados HTTP apropiados para la protección de sesiones.

### 9. Controles de Seguridad Específicos de IA
- **Defensa contra Inyección de Prompts**: Desplegar Microsoft Prompt Shields con técnicas de delimitación, delimitadores y marcación de datos.
- **Prevención de Envenenamiento de Herramientas**: Validar metadatos de herramientas, monitorear cambios dinámicos y verificar la integridad de las herramientas.
- **Validación de Salidas del Modelo**: Escanear las salidas del modelo en busca de posibles fugas de datos, contenido dañino o violaciones de políticas de seguridad.
- **Protección de Ventanas de Contexto**: Implementar controles para prevenir el envenenamiento y manipulación de ventanas de contexto.

### 10. Seguridad en la Ejecución de Herramientas
- **Ejecución en Entornos Aislados**: Ejecutar herramientas en entornos contenedorizados y aislados con límites de recursos.
- **Separación de Privilegios**: Ejecutar herramientas con los privilegios mínimos requeridos y cuentas de servicio separadas.
- **Aislamiento de Red**: Implementar segmentación de red para entornos de ejecución de herramientas.
- **Monitoreo de Ejecución**: Monitorear la ejecución de herramientas en busca de comportamientos anómalos, uso de recursos y violaciones de seguridad.

### 11. Validación Continua de Seguridad
- **Pruebas Automatizadas de Seguridad**: Integrar pruebas de seguridad en los pipelines de CI/CD con herramientas como GitHub Advanced Security.
- **Gestión de Vulnerabilidades**: Escanear regularmente todas las dependencias, incluidos modelos de IA y servicios externos.
- **Pruebas de Penetración**: Realizar evaluaciones de seguridad periódicas dirigidas específicamente a implementaciones MCP.
- **Revisiones de Código de Seguridad**: Implementar revisiones obligatorias de seguridad para todos los cambios de código relacionados con MCP.

### 12. Seguridad de la Cadena de Suministro para IA
- **Verificación de Componentes**: Verificar la procedencia, integridad y seguridad de todos los componentes de IA (modelos, embeddings, APIs).
- **Gestión de Dependencias**: Mantener inventarios actualizados de todas las dependencias de software e IA con seguimiento de vulnerabilidades.
- **Repositorios Confiables**: Usar fuentes verificadas y confiables para todos los modelos, bibliotecas y herramientas de IA.
- **Monitoreo de la Cadena de Suministro**: Monitorear continuamente compromisos en proveedores de servicios de IA y repositorios de modelos.

## Patrones Avanzados de Seguridad

### Arquitectura de Confianza Cero para MCP
- **Nunca Confiar, Siempre Verificar**: Implementar verificación continua para todos los participantes de MCP.
- **Microsegmentación**: Aislar componentes MCP con controles granulares de red e identidad.
- **Acceso Condicional**: Implementar controles de acceso basados en riesgos que se adapten al contexto y comportamiento.
- **Evaluación Continua de Riesgos**: Evaluar dinámicamente la postura de seguridad basada en indicadores de amenazas actuales.

### Implementación de IA Respetuosa con la Privacidad
- **Minimización de Datos**: Exponer solo los datos mínimos necesarios para cada operación MCP.
- **Privacidad Diferencial**: Implementar técnicas de preservación de privacidad para el procesamiento de datos sensibles.
- **Cifrado Homomórfico**: Usar técnicas avanzadas de cifrado para cálculos seguros en datos cifrados.
- **Aprendizaje Federado**: Implementar enfoques de aprendizaje distribuido que preserven la localización y privacidad de los datos.

### Respuesta a Incidentes para Sistemas de IA
- **Procedimientos Específicos de Incidentes de IA**: Desarrollar procedimientos de respuesta a incidentes adaptados a amenazas específicas de IA y MCP.
- **Respuesta Automatizada**: Implementar contención y remediación automatizadas para incidentes comunes de seguridad en IA.  
- **Capacidades Forenses**: Mantener preparación forense para compromisos de sistemas de IA y brechas de datos.
- **Procedimientos de Recuperación**: Establecer procedimientos para la recuperación de envenenamiento de modelos de IA, ataques de inyección de prompts y compromisos de servicios.

## Recursos de Implementación y Estándares

### Documentación Oficial de MCP
- [Especificación MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Especificación actual del protocolo MCP
- [Prácticas de Seguridad MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Guía oficial de seguridad
- [Especificación de Autorización MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Patrones de autenticación y autorización
- [Seguridad de Transporte MCP](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Requisitos de seguridad de capa de transporte

### Soluciones de Seguridad de Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Protección avanzada contra inyección de prompts
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Filtrado integral de contenido de IA
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Gestión empresarial de identidad y acceso
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Gestión segura de secretos y credenciales
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Escaneo de seguridad de código y cadena de suministro

### Estándares y Marcos de Seguridad
- [Prácticas de Seguridad OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Guía actual de seguridad OAuth
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Riesgos de seguridad en aplicaciones web
- [OWASP Top 10 para LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Riesgos de seguridad específicos de IA
- [Marco de Gestión de Riesgos de IA de NIST](https://www.nist.gov/itl/ai-risk-management-framework) - Gestión integral de riesgos de IA
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sistemas de gestión de seguridad de la información

### Guías y Tutoriales de Implementación
- [Gestión de API de Azure como Gateway de Autenticación MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Patrones de autenticación empresarial
- [Microsoft Entra ID con Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integración de proveedores de identidad
- [Implementación de Almacenamiento Seguro de Tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Mejores prácticas de gestión de tokens
- [Cifrado de Extremo a Extremo para IA](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Patrones avanzados de cifrado

### Recursos Avanzados de Seguridad
- [Ciclo de Vida de Desarrollo Seguro de Microsoft](https://www.microsoft.com/sdl) - Prácticas de desarrollo seguro
- [Guía de Red Team para IA](https://learn.microsoft.com/security/ai-red-team/) - Pruebas de seguridad específicas de IA
- [Modelado de Amenazas para Sistemas de IA](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodología de modelado de amenazas de IA
- [Ingeniería de Privacidad para IA](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Técnicas de preservación de privacidad en IA

### Cumplimiento y Gobernanza
- [Cumplimiento GDPR para IA](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Cumplimiento de privacidad en sistemas de IA
- [Marco de Gobernanza de IA](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementación de IA responsable
- [SOC 2 para Servicios de IA](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Controles de seguridad para proveedores de servicios de IA
- [Cumplimiento HIPAA para IA](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Requisitos de cumplimiento de IA en el sector salud

### DevSecOps y Automatización
- [Pipeline DevSecOps para IA](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Pipelines seguros de desarrollo de IA
- [Pruebas Automatizadas de Seguridad](https://learn.microsoft.com/security/engineering/devsecops) - Validación continua de seguridad
- [Seguridad de Infraestructura como Código](https://learn.microsoft.com/security/engineering/infrastructure-security) - Despliegue seguro de infraestructura
- [Seguridad de Contenedores para IA](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Seguridad en la contenedorización de cargas de trabajo de IA

### Monitoreo y Respuesta a Incidentes  
- [Azure Monitor para Cargas de Trabajo de IA](https://learn.microsoft.com/azure/azure-monitor/overview) - Soluciones completas de monitoreo
- [Respuesta a Incidentes de Seguridad en IA](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Procedimientos específicos de incidentes de IA
- [SIEM para Sistemas de IA](https://learn.microsoft.com/azure/sentinel/overview) - Gestión de información y eventos de seguridad
- [Inteligencia de Amenazas para IA](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Fuentes de inteligencia de amenazas para IA

## 🔄 Mejora Continua

### Mantenerse Actualizado con los Estándares en Evolución
- **Actualizaciones de Especificación MCP**: Monitorear cambios oficiales en la especificación MCP y avisos de seguridad.
- **Inteligencia de Amenazas**: Suscribirse a feeds de amenazas de seguridad de IA y bases de datos de vulnerabilidades.  
- **Participación Comunitaria**: Participar en discusiones comunitarias de seguridad MCP y grupos de trabajo.
- **Evaluación Regular**: Realizar evaluaciones trimestrales de postura de seguridad y actualizar prácticas en consecuencia.

### Contribuir a la Seguridad MCP
- **Investigación de Seguridad**: Contribuir a la investigación de seguridad MCP y programas de divulgación de vulnerabilidades.
- **Compartir Mejores Prácticas**: Compartir implementaciones de seguridad y lecciones aprendidas con la comunidad.
- **Desarrollo de Estándares**: Participar en el desarrollo de especificaciones MCP y creación de estándares de seguridad.
- **Desarrollo de Herramientas**: Desarrollar y compartir herramientas y bibliotecas de seguridad para el ecosistema MCP

---

*Este documento refleja las mejores prácticas de seguridad de MCP al 18 de agosto de 2025, basadas en la Especificación MCP 2025-06-18. Las prácticas de seguridad deben revisarse y actualizarse regularmente a medida que evolucionen el protocolo y el panorama de amenazas.*

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Si bien nos esforzamos por lograr precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.