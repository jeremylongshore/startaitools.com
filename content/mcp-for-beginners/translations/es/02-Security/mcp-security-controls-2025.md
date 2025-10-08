<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T11:42:33+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "es"
}
-->
# Controles de Seguridad MCP - Actualización de Agosto 2025

> **Estándar Actual**: Este documento refleja los requisitos de seguridad de la [Especificación MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) y las [Mejores Prácticas de Seguridad MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) oficiales.

El Protocolo de Contexto de Modelo (MCP) ha evolucionado significativamente con controles de seguridad mejorados que abordan tanto las amenazas tradicionales de software como las específicas de IA. Este documento proporciona controles de seguridad integrales para implementaciones seguras de MCP a partir de agosto de 2025.

## **Requisitos de Seguridad OBLIGATORIOS**

### **Prohibiciones Críticas de la Especificación MCP:**

> **PROHIBIDO**: Los servidores MCP **NO DEBEN** aceptar tokens que no hayan sido emitidos explícitamente para el servidor MCP  
>
> **PROHIBIDO**: Los servidores MCP **NO DEBEN** usar sesiones para autenticación  
>
> **REQUERIDO**: Los servidores MCP que implementen autorización **DEBEN** verificar TODAS las solicitudes entrantes  
>
> **OBLIGATORIO**: Los servidores proxy MCP que utilicen IDs de cliente estáticos **DEBEN** obtener el consentimiento del usuario para cada cliente registrado dinámicamente  

---

## 1. **Controles de Autenticación y Autorización**

### **Integración con Proveedores de Identidad Externos**

El **Estándar Actual MCP (2025-06-18)** permite que los servidores MCP deleguen la autenticación a proveedores de identidad externos, representando una mejora significativa en seguridad:

**Beneficios de Seguridad:**
1. **Elimina Riesgos de Autenticación Personalizada**: Reduce la superficie de vulnerabilidad al evitar implementaciones personalizadas de autenticación  
2. **Seguridad de Nivel Empresarial**: Aprovecha proveedores de identidad establecidos como Microsoft Entra ID con características avanzadas de seguridad  
3. **Gestión Centralizada de Identidad**: Simplifica la gestión del ciclo de vida del usuario, el control de acceso y las auditorías de cumplimiento  
4. **Autenticación Multifactor**: Hereda capacidades de MFA de los proveedores de identidad empresariales  
5. **Políticas de Acceso Condicional**: Se beneficia de controles de acceso basados en riesgos y autenticación adaptativa  

**Requisitos de Implementación:**
- **Validación de Audiencia de Tokens**: Verificar que todos los tokens hayan sido emitidos explícitamente para el servidor MCP  
- **Verificación del Emisor**: Validar que el emisor del token coincida con el proveedor de identidad esperado  
- **Verificación de Firma**: Validación criptográfica de la integridad del token  
- **Cumplimiento de Expiración**: Aplicación estricta de los límites de tiempo de vida del token  
- **Validación de Alcance**: Asegurarse de que los tokens contengan los permisos adecuados para las operaciones solicitadas  

### **Seguridad en la Lógica de Autorización**

**Controles Críticos:**
- **Auditorías Completas de Autorización**: Revisiones regulares de seguridad en todos los puntos de decisión de autorización  
- **Valores Predeterminados Seguros**: Denegar el acceso cuando la lógica de autorización no pueda tomar una decisión definitiva  
- **Límites de Permisos**: Separación clara entre diferentes niveles de privilegios y acceso a recursos  
- **Registro de Auditoría**: Registro completo de todas las decisiones de autorización para monitoreo de seguridad  
- **Revisiones Periódicas de Acceso**: Validación periódica de permisos de usuario y asignaciones de privilegios  

## 2. **Seguridad de Tokens y Controles Anti-Passthrough**

### **Prevención de Passthrough de Tokens**

**El passthrough de tokens está explícitamente prohibido** en la Especificación de Autorización MCP debido a riesgos críticos de seguridad:

**Riesgos de Seguridad Abordados:**
- **Elusión de Controles**: Evita controles de seguridad esenciales como limitación de tasa, validación de solicitudes y monitoreo de tráfico  
- **Falta de Responsabilidad**: Hace imposible identificar clientes, corrompiendo las pistas de auditoría y la investigación de incidentes  
- **Exfiltración Basada en Proxy**: Permite a actores maliciosos usar servidores como proxies para acceso no autorizado a datos  
- **Violaciones de Límites de Confianza**: Rompe las suposiciones de confianza de los servicios downstream sobre los orígenes de los tokens  
- **Movimiento Lateral**: Los tokens comprometidos en múltiples servicios permiten una expansión más amplia del ataque  

**Controles de Implementación:**
```yaml
Token Validation Requirements:
  audience_validation: MANDATORY
  issuer_verification: MANDATORY  
  signature_check: MANDATORY
  expiration_enforcement: MANDATORY
  scope_validation: MANDATORY
  
Token Lifecycle Management:
  rotation_frequency: "Short-lived tokens preferred"
  secure_storage: "Azure Key Vault or equivalent"
  transmission_security: "TLS 1.3 minimum"
  replay_protection: "Implemented via nonce/timestamp"
```

### **Patrones Seguros de Gestión de Tokens**

**Mejores Prácticas:**
- **Tokens de Vida Corta**: Minimizar la ventana de exposición con rotación frecuente de tokens  
- **Emisión Justo a Tiempo**: Emitir tokens solo cuando sean necesarios para operaciones específicas  
- **Almacenamiento Seguro**: Usar módulos de seguridad de hardware (HSM) o bóvedas de claves seguras  
- **Vinculación de Tokens**: Vincular tokens a clientes, sesiones u operaciones específicas cuando sea posible  
- **Monitoreo y Alertas**: Detección en tiempo real de uso indebido de tokens o patrones de acceso no autorizados  

## 3. **Controles de Seguridad de Sesiones**

### **Prevención de Secuestro de Sesiones**

**Vectores de Ataque Abordados:**
- **Inyección de Indicaciones en Secuestro de Sesión**: Eventos maliciosos inyectados en el estado compartido de la sesión  
- **Suplantación de Sesión**: Uso no autorizado de IDs de sesión robados para eludir la autenticación  
- **Ataques de Reanudación de Flujos**: Explotación de la reanudación de eventos enviados por el servidor para inyección de contenido malicioso  

**Controles Obligatorios de Sesión:**
```yaml
Session ID Generation:
  randomness_source: "Cryptographically secure RNG"
  entropy_bits: 128 # Minimum recommended
  format: "Base64url encoded"
  predictability: "MUST be non-deterministic"

Session Binding:
  user_binding: "REQUIRED - <user_id>:<session_id>"
  additional_identifiers: "Device fingerprint, IP validation"
  context_binding: "Request origin, user agent validation"
  
Session Lifecycle:
  expiration: "Configurable timeout policies"
  rotation: "After privilege escalation events"
  invalidation: "Immediate on security events"
  cleanup: "Automated expired session removal"
```

**Seguridad de Transporte:**
- **Aplicación de HTTPS**: Toda comunicación de sesión sobre TLS 1.3  
- **Atributos Seguros de Cookies**: HttpOnly, Secure, SameSite=Strict  
- **Fijación de Certificados**: Para conexiones críticas y prevenir ataques MITM  

### **Consideraciones sobre Implementaciones con Estado vs Sin Estado**

**Para Implementaciones con Estado:**
- El estado compartido de la sesión requiere protección adicional contra ataques de inyección  
- La gestión de sesiones basada en colas necesita verificación de integridad  
- Múltiples instancias de servidor requieren sincronización segura del estado de la sesión  

**Para Implementaciones sin Estado:**
- Gestión de sesiones basada en JWT o tokens similares  
- Verificación criptográfica de la integridad del estado de la sesión  
- Superficie de ataque reducida, pero requiere validación robusta de tokens  

## 4. **Controles de Seguridad Específicos de IA**

### **Defensa contra Inyección de Indicaciones**

**Integración con Microsoft Prompt Shields:**
```yaml
Detection Mechanisms:
  - "Advanced ML-based instruction detection"
  - "Contextual analysis of external content"
  - "Real-time threat pattern recognition"
  
Protection Techniques:
  - "Spotlighting trusted vs untrusted content"
  - "Delimiter systems for content boundaries"  
  - "Data marking for content source identification"
  
Integration Points:
  - "Azure Content Safety service"
  - "Real-time content filtering"
  - "Threat intelligence updates"
```

**Controles de Implementación:**
- **Saneamiento de Entradas**: Validación y filtrado exhaustivo de todas las entradas del usuario  
- **Definición de Límites de Contenido**: Separación clara entre instrucciones del sistema y contenido del usuario  
- **Jerarquía de Instrucciones**: Reglas de precedencia adecuadas para instrucciones conflictivas  
- **Monitoreo de Salidas**: Detección de salidas potencialmente dañinas o manipuladas  

### **Prevención de Envenenamiento de Herramientas**

**Marco de Seguridad de Herramientas:**
```yaml
Tool Definition Protection:
  validation:
    - "Schema validation against expected formats"
    - "Content analysis for malicious instructions" 
    - "Parameter injection detection"
    - "Hidden instruction identification"
  
  integrity_verification:
    - "Cryptographic hashing of tool definitions"
    - "Digital signatures for tool packages"
    - "Version control with change auditing"
    - "Tamper detection mechanisms"
  
  monitoring:
    - "Real-time change detection"
    - "Behavioral analysis of tool usage"
    - "Anomaly detection for execution patterns"
    - "Automated alerting for suspicious modifications"
```

**Gestión Dinámica de Herramientas:**
- **Flujos de Trabajo de Aprobación**: Consentimiento explícito del usuario para modificaciones de herramientas  
- **Capacidades de Reversión**: Posibilidad de volver a versiones anteriores de herramientas  
- **Auditoría de Cambios**: Historial completo de modificaciones en definiciones de herramientas  
- **Evaluación de Riesgos**: Evaluación automatizada de la postura de seguridad de herramientas  

## 5. **Prevención de Ataques de Confused Deputy**

### **Seguridad de Proxies OAuth**

**Controles de Prevención de Ataques:**
```yaml
Client Registration:
  static_client_protection:
    - "Explicit user consent for dynamic registration"
    - "Consent bypass prevention mechanisms"  
    - "Cookie-based consent validation"
    - "Redirect URI strict validation"
    
  authorization_flow:
    - "PKCE implementation (OAuth 2.1)"
    - "State parameter validation"
    - "Authorization code binding"
    - "Nonce verification for ID tokens"
```

**Requisitos de Implementación:**
- **Verificación de Consentimiento del Usuario**: Nunca omitir pantallas de consentimiento para el registro dinámico de clientes  
- **Validación de URI de Redirección**: Validación estricta basada en listas blancas de destinos de redirección  
- **Protección de Códigos de Autorización**: Códigos de corta duración con aplicación de uso único  
- **Verificación de Identidad del Cliente**: Validación robusta de credenciales y metadatos del cliente  

## 6. **Seguridad en la Ejecución de Herramientas**

### **Aislamiento y Sandboxing**

**Aislamiento Basado en Contenedores:**
```yaml
Execution Environment:
  containerization: "Docker/Podman with security profiles"
  resource_limits:
    cpu: "Configurable CPU quotas"
    memory: "Memory usage restrictions"
    disk: "Storage access limitations"
    network: "Network policy enforcement"
  
  privilege_restrictions:
    user_context: "Non-root execution mandatory"
    capability_dropping: "Remove unnecessary Linux capabilities"
    syscall_filtering: "Seccomp profiles for syscall restriction"
    filesystem: "Read-only root with minimal writable areas"
```

**Aislamiento de Procesos:**
- **Contextos de Procesos Separados**: Cada ejecución de herramienta en un espacio de proceso aislado  
- **Comunicación entre Procesos**: Mecanismos de IPC seguros con validación  
- **Monitoreo de Procesos**: Análisis de comportamiento en tiempo de ejecución y detección de anomalías  
- **Aplicación de Recursos**: Límites estrictos en CPU, memoria y operaciones de E/S  

### **Implementación de Mínimos Privilegios**

**Gestión de Permisos:**
```yaml
Access Control:
  file_system:
    - "Minimal required directory access"
    - "Read-only access where possible"
    - "Temporary file cleanup automation"
    
  network_access:
    - "Explicit allowlist for external connections"
    - "DNS resolution restrictions" 
    - "Port access limitations"
    - "SSL/TLS certificate validation"
  
  system_resources:
    - "No administrative privilege elevation"
    - "Limited system call access"
    - "No hardware device access"
    - "Restricted environment variable access"
```

## 7. **Controles de Seguridad en la Cadena de Suministro**

### **Verificación de Dependencias**

**Seguridad Integral de Componentes:**
```yaml
Software Dependencies:
  scanning: 
    - "Automated vulnerability scanning (GitHub Advanced Security)"
    - "License compliance verification"
    - "Known vulnerability database checks"
    - "Malware detection and analysis"
  
  verification:
    - "Package signature verification"
    - "Checksum validation"
    - "Provenance attestation"
    - "Software Bill of Materials (SBOM)"

AI Components:
  model_verification:
    - "Model provenance validation"
    - "Training data source verification" 
    - "Model behavior testing"
    - "Adversarial robustness assessment"
  
  service_validation:
    - "Third-party API security assessment"
    - "Service level agreement review"
    - "Data handling compliance verification"
    - "Incident response capability evaluation"
```

### **Monitoreo Continuo**

**Detección de Amenazas en la Cadena de Suministro:**
- **Monitoreo de Salud de Dependencias**: Evaluación continua de todas las dependencias en busca de problemas de seguridad  
- **Integración de Inteligencia de Amenazas**: Actualizaciones en tiempo real sobre amenazas emergentes en la cadena de suministro  
- **Análisis de Comportamiento**: Detección de comportamientos inusuales en componentes externos  
- **Respuesta Automatizada**: Contención inmediata de componentes comprometidos  

## 8. **Controles de Monitoreo y Detección**

### **Gestión de Información y Eventos de Seguridad (SIEM)**

**Estrategia Integral de Registro:**
```yaml
Authentication Events:
  - "All authentication attempts (success/failure)"
  - "Token issuance and validation events"
  - "Session creation, modification, termination"
  - "Authorization decisions and policy evaluations"

Tool Execution:
  - "Tool invocation details and parameters"
  - "Execution duration and resource usage"
  - "Output generation and content analysis"
  - "Error conditions and exception handling"

Security Events:
  - "Potential prompt injection attempts"
  - "Tool poisoning detection events"
  - "Session hijacking indicators"
  - "Unusual access patterns and anomalies"
```

### **Detección de Amenazas en Tiempo Real**

**Análisis de Comportamiento:**
- **Análisis de Comportamiento de Usuarios (UBA)**: Detección de patrones de acceso inusuales de usuarios  
- **Análisis de Comportamiento de Entidades (EBA)**: Monitoreo del comportamiento de servidores MCP y herramientas  
- **Detección de Anomalías con Aprendizaje Automático**: Identificación impulsada por IA de amenazas de seguridad  
- **Correlación de Inteligencia de Amenazas**: Comparación de actividades observadas con patrones de ataque conocidos  

## 9. **Respuesta y Recuperación ante Incidentes**

### **Capacidades de Respuesta Automatizada**

**Acciones de Respuesta Inmediata:**
```yaml
Threat Containment:
  session_management:
    - "Immediate session termination"
    - "Account lockout procedures"
    - "Access privilege revocation"
  
  system_isolation:
    - "Network segmentation activation"
    - "Service isolation protocols"
    - "Communication channel restriction"

Recovery Procedures:
  credential_rotation:
    - "Automated token refresh"
    - "API key regeneration"
    - "Certificate renewal"
  
  system_restoration:
    - "Clean state restoration"
    - "Configuration rollback"
    - "Service restart procedures"
```

### **Capacidades Forenses**

**Soporte para Investigaciones:**
- **Preservación de Pistas de Auditoría**: Registro inmutable con integridad criptográfica  
- **Recolección de Evidencia**: Recolección automatizada de artefactos de seguridad relevantes  
- **Reconstrucción de Cronología**: Secuencia detallada de eventos que llevaron a incidentes de seguridad  
- **Evaluación de Impacto**: Evaluación del alcance del compromiso y exposición de datos  

## **Principios Clave de Arquitectura de Seguridad**

### **Defensa en Profundidad**
- **Múltiples Capas de Seguridad**: Sin puntos únicos de falla en la arquitectura de seguridad  
- **Controles Redundantes**: Medidas de seguridad superpuestas para funciones críticas  
- **Mecanismos de Falla Segura**: Valores predeterminados seguros cuando los sistemas enfrentan errores o ataques  

### **Implementación de Confianza Cero**
- **Nunca Confíes, Siempre Verifica**: Validación continua de todas las entidades y solicitudes  
- **Principio de Mínimos Privilegios**: Derechos de acceso mínimos para todos los componentes  
- **Microsegmentación**: Controles granulares de red y acceso  

### **Evolución Continua de la Seguridad**
- **Adaptación al Panorama de Amenazas**: Actualizaciones regulares para abordar amenazas emergentes  
- **Efectividad de los Controles de Seguridad**: Evaluación y mejora continua de los controles  
- **Cumplimiento de Especificaciones**: Alineación con los estándares de seguridad MCP en evolución  

---

## **Recursos de Implementación**

### **Documentación Oficial MCP**
- [Especificación MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Mejores Prácticas de Seguridad MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Especificación de Autorización MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Soluciones de Seguridad de Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Estándares de Seguridad**
- [Mejores Prácticas de Seguridad OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 para Modelos de Lenguaje Extenso](https://genai.owasp.org/)  
- [Marco de Ciberseguridad NIST](https://www.nist.gov/cyberframework)  

---

> **Importante**: Estos controles de seguridad reflejan la especificación MCP actual (2025-06-18). Siempre verifica contra la [documentación oficial](https://spec.modelcontextprotocol.io/) más reciente, ya que los estándares continúan evolucionando rápidamente.  

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Si bien nos esforzamos por garantizar la precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.