<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T13:19:03+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ru"
}
-->
# Контроль безопасности MCP - обновление август 2025

> **Текущий стандарт**: Этот документ отражает требования безопасности [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) и официальные [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Протокол Model Context Protocol (MCP) значительно усовершенствован благодаря новым мерам безопасности, которые охватывают как традиционные угрозы для программного обеспечения, так и специфические угрозы для ИИ. Этот документ предоставляет полный набор мер безопасности для безопасной реализации MCP на август 2025 года.

## **ОБЯЗАТЕЛЬНЫЕ требования безопасности**

### **Критические запреты из спецификации MCP:**

> **ЗАПРЕЩЕНО**: Серверы MCP **НЕ ДОЛЖНЫ** принимать токены, которые не были явно выпущены для сервера MCP  
>
> **ЗАПРЕЩЕНО**: Серверы MCP **НЕ ДОЛЖНЫ** использовать сессии для аутентификации  
>
> **ОБЯЗАТЕЛЬНО**: Серверы MCP, реализующие авторизацию, **ДОЛЖНЫ** проверять ВСЕ входящие запросы  
>
> **ОБЯЗАТЕЛЬНО**: Прокси-серверы MCP, использующие статические идентификаторы клиентов, **ДОЛЖНЫ** получать согласие пользователя для каждого динамически зарегистрированного клиента  

---

## 1. **Контроль аутентификации и авторизации**

### **Интеграция с внешними поставщиками идентификации**

**Текущий стандарт MCP (2025-06-18)** позволяет серверам MCP делегировать аутентификацию внешним поставщикам идентификации, что представляет собой значительное улучшение безопасности:

**Преимущества безопасности:**
1. **Устранение рисков кастомной аутентификации**: Снижает уязвимость за счет отказа от собственных реализаций аутентификации  
2. **Корпоративная безопасность**: Использует проверенных поставщиков идентификации, таких как Microsoft Entra ID, с расширенными функциями безопасности  
3. **Централизованное управление идентификацией**: Упрощает управление жизненным циклом пользователей, контроль доступа и аудит соответствия  
4. **Многофакторная аутентификация**: Наследует возможности MFA от корпоративных поставщиков идентификации  
5. **Политики условного доступа**: Использует адаптивные механизмы контроля доступа, основанные на рисках  

**Требования к реализации:**
- **Проверка аудитории токена**: Убедитесь, что все токены явно выпущены для сервера MCP  
- **Проверка издателя**: Убедитесь, что издатель токена соответствует ожидаемому поставщику идентификации  
- **Проверка подписи**: Криптографическая проверка целостности токена  
- **Соблюдение срока действия**: Строгий контроль сроков действия токенов  
- **Проверка области действия**: Убедитесь, что токены содержат соответствующие разрешения для запрашиваемых операций  

### **Безопасность логики авторизации**

**Критические меры:**
- **Полные аудиты авторизации**: Регулярные проверки всех точек принятия решений по авторизации  
- **Безопасные настройки по умолчанию**: Отказ в доступе, если логика авторизации не может принять окончательное решение  
- **Границы разрешений**: Четкое разделение уровней привилегий и доступа к ресурсам  
- **Логирование аудита**: Полное ведение журнала всех решений по авторизации для мониторинга безопасности  
- **Регулярные проверки доступа**: Периодическая проверка разрешений пользователей и назначений привилегий  

## 2. **Безопасность токенов и контроль против передачи**

### **Предотвращение передачи токенов**

**Передача токенов строго запрещена** в спецификации авторизации MCP из-за критических рисков безопасности:

**Риски безопасности, которые устраняются:**
- **Обход контроля**: Игнорирование важных мер безопасности, таких как ограничение скорости, проверка запросов и мониторинг трафика  
- **Нарушение учета**: Невозможность идентификации клиента, что портит журналы аудита и расследование инцидентов  
- **Эксплуатация через прокси**: Злоумышленники могут использовать серверы как прокси для несанкционированного доступа к данным  
- **Нарушение границ доверия**: Подрывает предположения о происхождении токенов в downstream-сервисах  
- **Латеральное перемещение**: Скомпрометированные токены между несколькими сервисами позволяют расширить атаку  

**Контроль реализации:**
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

### **Безопасные шаблоны управления токенами**

**Лучшие практики:**
- **Краткосрочные токены**: Минимизируйте окно уязвимости с помощью частой ротации токенов  
- **Выдача по запросу**: Выпускайте токены только при необходимости для конкретных операций  
- **Безопасное хранение**: Используйте аппаратные модули безопасности (HSM) или защищенные хранилища ключей  
- **Привязка токенов**: Привязывайте токены к конкретным клиентам, сессиям или операциям, если возможно  
- **Мониторинг и оповещение**: Реальное время обнаружения злоупотребления токенами или несанкционированных шаблонов доступа  

## 3. **Контроль безопасности сессий**

### **Предотвращение захвата сессий**

**Устраненные векторы атак:**
- **Инъекция через захват сессии**: Внедрение вредоносных событий в общий статус сессии  
- **Имитация сессии**: Несанкционированное использование украденных идентификаторов сессий для обхода аутентификации  
- **Атаки на возобновляемые потоки**: Эксплуатация возобновления событий, отправленных сервером, для внедрения вредоносного контента  

**Обязательные меры контроля сессий:**
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

**Транспортная безопасность:**
- **Принудительное использование HTTPS**: Вся коммуникация сессий через TLS 1.3  
- **Атрибуты безопасных cookie**: HttpOnly, Secure, SameSite=Strict  
- **Закрепление сертификатов**: Для критических соединений, чтобы предотвратить атаки MITM  

### **Сравнение Stateful и Stateless**

**Для Stateful реализаций:**
- Общий статус сессии требует дополнительной защиты от атак инъекции  
- Управление сессиями на основе очередей требует проверки целостности  
- Несколько экземпляров серверов требуют безопасной синхронизации состояния сессий  

**Для Stateless реализаций:**
- Управление сессиями на основе JWT или аналогичных токенов  
- Криптографическая проверка целостности состояния сессии  
- Сниженная поверхность атаки, но требуется надежная проверка токенов  

## 4. **Контроль безопасности, специфичный для ИИ**

### **Защита от инъекций в подсказки**

**Интеграция Microsoft Prompt Shields:**
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

**Контроль реализации:**
- **Очистка ввода**: Полная проверка и фильтрация всех пользовательских вводов  
- **Определение границ контента**: Четкое разделение системных инструкций и пользовательского контента  
- **Иерархия инструкций**: Правильные правила приоритета для конфликтующих инструкций  
- **Мониторинг вывода**: Обнаружение потенциально вредоносных или манипулированных выводов  

### **Предотвращение отравления инструментов**

**Фреймворк безопасности инструментов:**
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

**Динамическое управление инструментами:**
- **Рабочие процессы утверждения**: Явное согласие пользователя на изменения инструментов  
- **Возможности отката**: Возможность возврата к предыдущим версиям инструментов  
- **Аудит изменений**: Полная история модификаций определения инструментов  
- **Оценка рисков**: Автоматическая оценка безопасности инструментов  

## 5. **Предотвращение атак "запутанный заместитель"**

### **Безопасность OAuth Proxy**

**Контроль предотвращения атак:**
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

**Требования к реализации:**
- **Проверка согласия пользователя**: Никогда не пропускайте экраны согласия для динамической регистрации клиентов  
- **Проверка URI перенаправления**: Строгая проверка на основе белого списка для мест назначения перенаправления  
- **Защита кода авторизации**: Краткосрочные коды с принудительным одноразовым использованием  
- **Проверка идентичности клиента**: Надежная проверка учетных данных и метаданных клиента  

## 6. **Безопасность выполнения инструментов**

### **Песочница и изоляция**

**Изоляция на основе контейнеров:**
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

**Изоляция процессов:**
- **Отдельные контексты процессов**: Каждое выполнение инструмента в изолированном пространстве процессов  
- **Межпроцессное взаимодействие**: Безопасные механизмы IPC с проверкой  
- **Мониторинг процессов**: Анализ поведения во время выполнения и обнаружение аномалий  
- **Контроль ресурсов**: Жесткие ограничения на использование CPU, памяти и операций ввода-вывода  

### **Реализация принципа минимальных привилегий**

**Управление разрешениями:**
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

## 7. **Контроль безопасности цепочки поставок**

### **Проверка зависимостей**

**Полная безопасность компонентов:**
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

### **Непрерывный мониторинг**

**Обнаружение угроз в цепочке поставок:**
- **Мониторинг здоровья зависимостей**: Непрерывная оценка всех зависимостей на наличие проблем безопасности  
- **Интеграция разведки угроз**: Обновления в реальном времени о новых угрозах в цепочке поставок  
- **Анализ поведения**: Обнаружение необычного поведения внешних компонентов  
- **Автоматический ответ**: Немедленное ограничение скомпрометированных компонентов  

## 8. **Контроль мониторинга и обнаружения**

### **Система управления информацией и событиями безопасности (SIEM)**

**Полная стратегия логирования:**
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

### **Обнаружение угроз в реальном времени**

**Аналитика поведения:**
- **Аналитика поведения пользователей (UBA)**: Обнаружение необычных шаблонов доступа пользователей  
- **Аналитика поведения сущностей (EBA)**: Мониторинг поведения серверов MCP и инструментов  
- **Обнаружение аномалий с помощью машинного обучения**: Идентификация угроз безопасности с помощью ИИ  
- **Корреляция разведки угроз**: Сопоставление наблюдаемых действий с известными шаблонами атак  

## 9. **Реакция на инциденты и восстановление**

### **Автоматизированные возможности реагирования**

**Немедленные действия:**
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

### **Форензика**

**Поддержка расследования:**
- **Сохранение журнала аудита**: Неподвижное логирование с криптографической целостностью  
- **Сбор доказательств**: Автоматический сбор соответствующих артефактов безопасности  
- **Реконструкция временной шкалы**: Детальная последовательность событий, ведущих к инцидентам безопасности  
- **Оценка воздействия**: Анализ масштаба компрометации и утечки данных  

## **Основные принципы архитектуры безопасности**

### **Защита в глубину**
- **Множественные уровни безопасности**: Отсутствие единой точки отказа в архитектуре безопасности  
- **Избыточные меры контроля**: Перекрывающиеся меры безопасности для критических функций  
- **Механизмы безопасного отказа**: Безопасные настройки по умолчанию при ошибках или атаках  

### **Реализация Zero Trust**
- **Никогда не доверяй, всегда проверяй**: Непрерывная проверка всех сущностей и запросов  
- **Принцип минимальных привилегий**: Минимальные права доступа для всех компонентов  
- **Микросегментация**: Гранулярный контроль сети и доступа  

### **Непрерывная эволюция безопасности**
- **Адаптация к угрозам**: Регулярные обновления для устранения новых угроз  
- **Эффективность мер безопасности**: Постоянная оценка и улучшение контроля  
- **Соответствие спецификации**: Согласование с развивающимися стандартами безопасности MCP  

---

## **Ресурсы для реализации**

### **Официальная документация MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Решения безопасности Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Стандарты безопасности**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Важно**: Эти меры безопасности отражают текущую спецификацию MCP (2025-06-18). Всегда проверяйте последнюю [официальную документацию](https://spec.modelcontextprotocol.io/), так как стандарты быстро развиваются.

**Отказ от ответственности**:  
Этот документ был переведен с использованием сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия обеспечить точность, автоматические переводы могут содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется профессиональный перевод человеком. Мы не несем ответственности за любые недоразумения или неправильные интерпретации, возникшие в результате использования данного перевода.