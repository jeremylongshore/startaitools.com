<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T16:59:20+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "bg"
}
-->
# MCP Контроли за сигурност - Актуализация август 2025

> **Текущ стандарт**: Този документ отразява [MCP Спецификация 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) изисквания за сигурност и официалните [MCP Най-добри практики за сигурност](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Протоколът за контекст на модела (MCP) значително се е развил с подобрени контроли за сигурност, които адресират както традиционните заплахи за софтуерната сигурност, така и специфични за AI рискове. Този документ предоставя изчерпателни контроли за сигурност за сигурни MCP реализации към август 2025.

## **ЗАДЪЛЖИТЕЛНИ изисквания за сигурност**

### **Критични забрани от MCP Спецификацията:**

> **ЗАБРАНЕНО**: MCP сървърите **НЕ ТРЯБВА** да приемат токени, които не са изрично издадени за MCP сървъра  
>
> **ЗАБРАНЕНО**: MCP сървърите **НЕ ТРЯБВА** да използват сесии за удостоверяване  
>
> **ЗАДЪЛЖИТЕЛНО**: MCP сървърите, които прилагат авторизация, **ТРЯБВА** да проверяват ВСИЧКИ входящи заявки  
>
> **ЗАДЪЛЖИТЕЛНО**: MCP прокси сървърите, използващи статични клиентски идентификатори, **ТРЯБВА** да получат съгласие от потребителя за всеки динамично регистриран клиент  

---

## 1. **Контроли за удостоверяване и авторизация**

### **Интеграция с външни доставчици на идентичност**

**Текущият MCP стандарт (2025-06-18)** позволява на MCP сървърите да делегират удостоверяването на външни доставчици на идентичност, което представлява значително подобрение в сигурността:

**Ползи за сигурността:**
1. **Елиминиране на рисковете от персонализирано удостоверяване**: Намалява повърхността на уязвимост чрез избягване на персонализирани реализации за удостоверяване  
2. **Сигурност на корпоративно ниво**: Използва утвърдени доставчици на идентичност като Microsoft Entra ID с усъвършенствани функции за сигурност  
3. **Централизирано управление на идентичността**: Оптимизира управлението на жизнения цикъл на потребителите, контрола на достъпа и одитите за съответствие  
4. **Многофакторно удостоверяване**: Наследява MFA възможности от корпоративните доставчици на идентичност  
5. **Политики за условен достъп**: Възползва се от контроли за достъп, базирани на риска, и адаптивно удостоверяване  

**Изисквания за реализация:**
- **Валидиране на аудиторията на токените**: Проверка, че всички токени са изрично издадени за MCP сървъра  
- **Проверка на издателя**: Удостоверяване, че издателят на токена съответства на очаквания доставчик на идентичност  
- **Проверка на подписа**: Криптографска проверка на целостта на токена  
- **Принудително спазване на срока на валидност**: Строго спазване на ограниченията за продължителност на токените  
- **Валидиране на обхвата**: Уверяване, че токените съдържат подходящи разрешения за заявените операции  

### **Сигурност на логиката за авторизация**

**Критични контроли:**
- **Изчерпателни одити на авторизацията**: Редовни прегледи на сигурността на всички точки за вземане на решения за авторизация  
- **Безопасни настройки по подразбиране**: Отказ на достъп, когато логиката за авторизация не може да вземе категорично решение  
- **Граници на разрешенията**: Ясно разделение между различни нива на привилегии и достъп до ресурси  
- **Одитни записи**: Пълно регистриране на всички решения за авторизация за мониторинг на сигурността  
- **Редовни прегледи на достъпа**: Периодична проверка на разрешенията и назначенията на привилегии на потребителите  

## 2. **Сигурност на токените и контроли срещу предаване**

### **Предотвратяване на предаването на токени**

**Предаването на токени е изрично забранено** в MCP Спецификацията за авторизация поради критични рискове за сигурността:

**Адресирани рискове за сигурността:**
- **Заобикаляне на контроли**: Пропускане на основни контроли за сигурност като ограничаване на скоростта, валидиране на заявки и мониторинг на трафика  
- **Разпадане на отчетността**: Невъзможност за идентифициране на клиента, което компрометира одитните записи и разследването на инциденти  
- **Експлоатация чрез прокси**: Позволява на злонамерени актьори да използват сървъри като прокси за неоторизиран достъп до данни  
- **Нарушения на границите на доверие**: Компрометира предположенията за доверие на услугите надолу по веригата относно произхода на токените  
- **Латерално движение**: Компрометирани токени между множество услуги позволяват разширяване на атаката  

**Контроли за реализация:**
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

### **Сигурни модели за управление на токени**

**Най-добри практики:**
- **Краткотрайни токени**: Минимизиране на прозореца на експозиция чрез честа ротация на токените  
- **Издаване при нужда**: Издаване на токени само когато са необходими за конкретни операции  
- **Сигурно съхранение**: Използване на хардуерни модули за сигурност (HSM) или сигурни хранилища за ключове  
- **Обвързване на токени**: Обвързване на токени със специфични клиенти, сесии или операции, когато е възможно  
- **Мониторинг и предупреждения**: Засичане в реално време на злоупотреба с токени или неоторизирани модели на достъп  

## 3. **Контроли за сигурност на сесиите**

### **Предотвратяване на отвличане на сесии**

**Адресирани вектори на атака:**
- **Инжектиране на злонамерени събития в сесия**: Злонамерени събития, инжектирани в споделено състояние на сесията  
- **Имперсонация на сесия**: Неоторизирано използване на откраднати идентификатори на сесии за заобикаляне на удостоверяването  
- **Атаки чрез възобновяване на потоци**: Експлоатация на възобновяване на събития, изпратени от сървъра, за инжектиране на злонамерено съдържание  

**Задължителни контроли за сесии:**
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

**Транспортна сигурност:**
- **Принудително използване на HTTPS**: Цялата комуникация на сесията през TLS 1.3  
- **Сигурни атрибути на бисквитки**: HttpOnly, Secure, SameSite=Strict  
- **Закрепване на сертификати**: За критични връзки за предотвратяване на атаки тип "човек в средата"  

### **Съображения за състояние и безсъстояние**

**За реализации със състояние:**
- Споделеното състояние на сесията изисква допълнителна защита срещу атаки чрез инжектиране  
- Управлението на сесии, базирано на опашки, се нуждае от проверка на целостта  
- Множество сървърни инстанции изискват сигурна синхронизация на състоянието на сесията  

**За реализации без състояние:**
- Управление на сесии, базирано на JWT или подобни токени  
- Криптографска проверка на целостта на състоянието на сесията  
- Намалена повърхност на атака, но изисква надеждна проверка на токените  

## 4. **Контроли за сигурност, специфични за AI**

### **Защита срещу инжектиране на инструкции**

**Интеграция с Microsoft Prompt Shields:**
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

**Контроли за реализация:**
- **Санитизация на входа**: Изчерпателна проверка и филтриране на всички потребителски входове  
- **Определяне на граници на съдържанието**: Ясно разделение между системни инструкции и потребителско съдържание  
- **Йерархия на инструкциите**: Правилно приоритизиране на конфликтни инструкции  
- **Мониторинг на изхода**: Засичане на потенциално вредни или манипулирани изходи  

### **Предотвратяване на отравяне на инструменти**

**Рамка за сигурност на инструментите:**
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

**Динамично управление на инструменти:**
- **Работни потоци за одобрение**: Изрично съгласие от потребителя за модификации на инструменти  
- **Възможности за връщане назад**: Възможност за връщане към предишни версии на инструменти  
- **Одит на промените**: Пълна история на модификациите на дефинициите на инструменти  
- **Оценка на риска**: Автоматизирана оценка на сигурността на инструментите  

## 5. **Предотвратяване на атаки тип "объркан заместник"**

### **Сигурност на OAuth прокси**

**Контроли за предотвратяване на атаки:**
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

**Изисквания за реализация:**
- **Проверка на съгласието на потребителя**: Никога не пропускайте екрани за съгласие при динамична регистрация на клиенти  
- **Валидиране на URI за пренасочване**: Строга проверка на дестинациите за пренасочване, базирана на бели списъци  
- **Защита на кодовете за авторизация**: Краткотрайни кодове с принудително еднократно използване  
- **Проверка на идентичността на клиента**: Надеждна проверка на идентификационните данни и метаданните на клиента  

## 6. **Сигурност при изпълнение на инструменти**

### **Изолиране и пясъчник**

**Изолиране, базирано на контейнери:**
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

**Изолиране на процеси:**
- **Отделни контексти на процеси**: Всяко изпълнение на инструмент в изолирано пространство на процеса  
- **Междупроцесна комуникация**: Сигурни механизми за IPC с проверка  
- **Мониторинг на процесите**: Анализ на поведението по време на изпълнение и засичане на аномалии  
- **Принудително спазване на ресурсите**: Твърди ограничения за CPU, памет и I/O операции  

### **Реализация на принципа за минимални привилегии**

**Управление на разрешенията:**
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

## 7. **Контроли за сигурност на веригата за доставки**

### **Проверка на зависимостите**

**Изчерпателна сигурност на компонентите:**
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

### **Непрекъснат мониторинг**

**Засичане на заплахи във веригата за доставки:**
- **Мониторинг на здравето на зависимостите**: Непрекъсната оценка на всички зависимости за проблеми със сигурността  
- **Интеграция на разузнаване за заплахи**: Актуализации в реално време за нововъзникващи заплахи във веригата за доставки  
- **Анализ на поведението**: Засичане на необичайно поведение в външни компоненти  
- **Автоматизиран отговор**: Незабавно ограничаване на компрометирани компоненти  

## 8. **Контроли за мониторинг и засичане**

### **Управление на информацията и събитията за сигурност (SIEM)**

**Изчерпателна стратегия за регистриране:**
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

### **Засичане на заплахи в реално време**

**Анализ на поведението:**
- **Анализ на поведението на потребителите (UBA)**: Засичане на необичайни модели на достъп на потребителите  
- **Анализ на поведението на обектите (EBA)**: Мониторинг на поведението на MCP сървъра и инструментите  
- **Засичане на аномалии чрез машинно обучение**: Идентифициране на заплахи за сигурността, захранвано от AI  
- **Корелация на разузнаване за заплахи**: Съпоставяне на наблюдаваните дейности с известни модели на атаки  

## 9. **Реакция при инциденти и възстановяване**

### **Автоматизирани възможности за реакция**

**Незабавни действия за реакция:**
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

### **Възможности за криминалистика**

**Подкрепа за разследване:**
- **Запазване на одитните записи**: Непроменими регистри с криптографска цялост  
- **Събиране на доказателства**: Автоматизирано събиране на релевантни артефакти за сигурност  
- **Реконструкция на времевата линия**: Подробна последователност на събитията, водещи до инциденти със сигурността  
- **Оценка на въздействието**: Оценка на обхвата на компрометиране и експозиция на данни  

## **Основни принципи на архитектурата за сигурност**

### **Защита в дълбочина**
- **Множество слоеве за сигурност**: Без единична точка на отказ в архитектурата за сигурност  
- **Резервни контроли**: Прекриващи се мерки за сигурност за критични функции  
- **Безопасни механизми при отказ**: Сигурни настройки по подразбиране, когато системите срещнат грешки или атаки  

### **Реализация на Zero Trust**
- **Никога не се доверявай, винаги проверявай**: Непрекъсната проверка на всички обекти и заявки  
- **Принцип на минимални привилегии**: Минимални права за достъп за всички компоненти  
- **Микросегментация**: Гранулирани мрежови и контролни механизми за достъп  

### **Непрекъсната еволюция на сигурността**
- **Адаптация към заплахи**: Редовни актуализации за адресиране на нововъзникващи заплахи  
- **Ефективност на контрола за сигурност**: Постоянна оценка и подобрение на контролите  
- **Съответствие със спецификацията**: Съгласуване с развиващите се стандарти за сигурност на MCP  

---

## **Ресурси за реализация**

### **Официална документация на MCP**
- [MCP Спецификация (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Най-добри практики за сигурност](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Спецификация за авторизация](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Решения за сигурност на Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI услуга за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматичните преводи може да съдържат грешки или неточности. Оригиналният документ на неговия изходен език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да било недоразумения или погрешни интерпретации, произтичащи от използването на този превод.