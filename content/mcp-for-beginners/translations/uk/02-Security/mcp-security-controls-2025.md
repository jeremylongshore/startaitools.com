<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T19:21:16+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "uk"
}
-->
# Контроль безпеки MCP - Оновлення серпень 2025

> **Поточний стандарт**: Цей документ відображає вимоги безпеки [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) та офіційні [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Протокол Model Context Protocol (MCP) значно вдосконалився завдяки посиленим заходам безпеки, які охоплюють як традиційні загрози для програмного забезпечення, так і специфічні для штучного інтелекту. Цей документ надає комплексний набір заходів безпеки для безпечної реалізації MCP станом на серпень 2025 року.

## **ОБОВ’ЯЗКОВІ вимоги до безпеки**

### **Критичні заборони з MCP Specification:**

> **ЗАБОРОНЕНО**: MCP-сервери **НЕ ПОВИННІ** приймати жодні токени, які не були явно видані для MCP-сервера  
>
> **ЗАБОРОНЕНО**: MCP-сервери **НЕ ПОВИННІ** використовувати сесії для автентифікації  
>
> **ОБОВ’ЯЗКОВО**: MCP-сервери, які реалізують авторизацію, **ПОВИННІ** перевіряти ВСІ вхідні запити  
>
> **ОБОВ’ЯЗКОВО**: MCP-проксі-сервери, які використовують статичні ідентифікатори клієнтів, **ПОВИННІ** отримувати згоду користувача для кожного динамічно зареєстрованого клієнта  

---

## 1. **Контроль автентифікації та авторизації**

### **Інтеграція з зовнішніми постачальниками ідентифікації**

**Поточний стандарт MCP (2025-06-18)** дозволяє MCP-серверам делегувати автентифікацію зовнішнім постачальникам ідентифікації, що є значним покращенням безпеки:

**Переваги безпеки:**
1. **Усунення ризиків власної автентифікації**: Зменшує поверхню вразливостей, уникаючи власних реалізацій автентифікації  
2. **Безпека корпоративного рівня**: Використання перевірених постачальників ідентифікації, таких як Microsoft Entra ID, з розширеними функціями безпеки  
3. **Централізоване управління ідентифікацією**: Спрощує управління життєвим циклом користувачів, контроль доступу та аудит відповідності  
4. **Багатофакторна автентифікація**: Успадковує можливості MFA від корпоративних постачальників ідентифікації  
5. **Політики умовного доступу**: Використання адаптивної автентифікації та контролю доступу на основі ризиків  

**Вимоги до реалізації:**
- **Перевірка аудиторії токенів**: Переконайтеся, що всі токени явно видані для MCP-сервера  
- **Перевірка видавця**: Перевірте, чи відповідає видавець токена очікуваному постачальнику ідентифікації  
- **Перевірка підпису**: Криптографічна перевірка цілісності токена  
- **Дотримання терміну дії**: Строге дотримання обмежень терміну дії токенів  
- **Перевірка обсягу**: Переконайтеся, що токени містять відповідні дозволи для запитуваних операцій  

### **Безпека логіки авторизації**

**Критичні заходи:**
- **Комплексний аудит авторизації**: Регулярні перевірки безпеки всіх точок прийняття рішень щодо авторизації  
- **Безпечні значення за замовчуванням**: Відмова у доступі, якщо логіка авторизації не може прийняти остаточне рішення  
- **Межі дозволів**: Чітке розмежування між різними рівнями привілеїв і доступу до ресурсів  
- **Журналювання аудиту**: Повне ведення журналу всіх рішень щодо авторизації для моніторингу безпеки  
- **Регулярний перегляд доступу**: Періодична перевірка дозволів користувачів і призначення привілеїв  

## 2. **Безпека токенів та контроль проти передачі**

### **Запобігання передачі токенів**

**Передача токенів категорично заборонена** в MCP Authorization Specification через критичні ризики безпеки:

**Ризики безпеки, які усуваються:**
- **Обхід контролю**: Уникає важливих заходів безпеки, таких як обмеження швидкості, перевірка запитів і моніторинг трафіку  
- **Порушення підзвітності**: Унеможливлює ідентифікацію клієнта, що ускладнює аудит і розслідування інцидентів  
- **Експлуатація через проксі**: Дозволяє зловмисникам використовувати сервери як проксі для несанкціонованого доступу до даних  
- **Порушення довіри**: Руйнує припущення про походження токенів у сервісах нижчого рівня  
- **Горизонтальне переміщення**: Компрометація токенів у кількох сервісах дозволяє розширити атаку  

**Контроль реалізації:**
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

### **Безпечні шаблони управління токенами**

**Найкращі практики:**
- **Короткострокові токени**: Мінімізуйте вікно експозиції за допомогою частого оновлення токенів  
- **Видача за потребою**: Видавайте токени лише тоді, коли це необхідно для конкретних операцій  
- **Безпечне зберігання**: Використовуйте апаратні модулі безпеки (HSM) або захищені сховища ключів  
- **Прив’язка токенів**: Прив’язуйте токени до конкретних клієнтів, сесій або операцій, якщо це можливо  
- **Моніторинг і сповіщення**: Виявлення в реальному часі зловживань токенами або несанкціонованих шаблонів доступу  

## 3. **Контроль безпеки сесій**

### **Запобігання викраденню сесій**

**Вразливості, які усуваються:**
- **Викрадення сесій через ін’єкцію**: Зловмисні події, впроваджені у спільний стан сесії  
- **Імперсонація сесії**: Несанкціоноване використання викрадених ідентифікаторів сесій для обходу автентифікації  
- **Атаки на відновлення потоків**: Експлуатація відновлення подій сервера для впровадження зловмисного контенту  

**Обов’язкові заходи безпеки сесій:**
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

**Безпека транспорту:**
- **Примусове використання HTTPS**: Уся комунікація сесій через TLS 1.3  
- **Атрибути безпечних cookie**: HttpOnly, Secure, SameSite=Strict  
- **Фіксація сертифікатів**: Для критичних з’єднань, щоб запобігти атакам MITM  

### **Розгляд стану сесій: Stateful vs Stateless**

**Для stateful реалізацій:**
- Спільний стан сесій вимагає додаткового захисту від ін’єкцій  
- Управління сесіями на основі черг потребує перевірки цілісності  
- Кілька серверних інстанцій вимагають безпечної синхронізації стану сесій  

**Для stateless реалізацій:**
- Управління сесіями на основі JWT або подібних токенів  
- Криптографічна перевірка цілісності стану сесій  
- Зменшена поверхня атаки, але потрібна надійна перевірка токенів  

## 4. **Контроль безпеки, специфічний для ШІ**

### **Захист від ін’єкцій у підказки**

**Інтеграція Microsoft Prompt Shields:**
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

**Контроль реалізації:**
- **Санітаризація вводу**: Комплексна перевірка та фільтрація всіх користувацьких вводів  
- **Визначення меж контенту**: Чітке розмежування між системними інструкціями та користувацьким контентом  
- **Ієрархія інструкцій**: Правильний пріоритет для конфліктуючих інструкцій  
- **Моніторинг виводу**: Виявлення потенційно шкідливих або маніпульованих результатів  

### **Запобігання отруєнню інструментів**

**Рамка безпеки інструментів:**
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

**Динамічне управління інструментами:**
- **Процеси затвердження**: Явна згода користувача на модифікації інструментів  
- **Можливості відкату**: Здатність повернутися до попередніх версій інструментів  
- **Аудит змін**: Повна історія змін визначень інструментів  
- **Оцінка ризиків**: Автоматизована оцінка безпеки інструментів  

## 5. **Запобігання атакам "заплутаного заступника"**

### **Безпека OAuth-проксі**

**Контроль запобігання атакам:**
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

**Вимоги до реалізації:**
- **Перевірка згоди користувача**: Ніколи не пропускайте екрани згоди для динамічної реєстрації клієнтів  
- **Перевірка URI перенаправлення**: Строга перевірка на основі білого списку для місць перенаправлення  
- **Захист коду авторизації**: Короткострокові коди з примусовим одноразовим використанням  
- **Перевірка ідентичності клієнта**: Надійна перевірка облікових даних і метаданих клієнта  

## 6. **Безпека виконання інструментів**

### **Пісочниця та ізоляція**

**Ізоляція на основі контейнерів:**
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

**Ізоляція процесів:**
- **Окремі контексти процесів**: Кожне виконання інструменту в ізольованому просторі процесів  
- **Міжпроцесна комунікація**: Безпечні механізми IPC із перевіркою  
- **Моніторинг процесів**: Аналіз поведінки в реальному часі та виявлення аномалій  
- **Обмеження ресурсів**: Жорсткі ліміти на використання CPU, пам’яті та операцій вводу/виводу  

### **Реалізація принципу найменших привілеїв**

**Управління дозволами:**
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

## 7. **Контроль безпеки ланцюга постачання**

### **Перевірка залежностей**

**Комплексна безпека компонентів:**
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

### **Безперервний моніторинг**

**Виявлення загроз у ланцюзі постачання:**
- **Моніторинг стану залежностей**: Постійна оцінка всіх залежностей на предмет проблем безпеки  
- **Інтеграція розвідки загроз**: Оновлення в реальному часі про нові загрози в ланцюзі постачання  
- **Аналіз поведінки**: Виявлення незвичайної поведінки зовнішніх компонентів  
- **Автоматизована реакція**: Негайна ізоляція скомпрометованих компонентів  

## 8. **Контроль моніторингу та виявлення**

### **Системи управління інформацією та подіями безпеки (SIEM)**

**Комплексна стратегія журналювання:**
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

### **Виявлення загроз у реальному часі**

**Аналіз поведінки:**
- **Аналіз поведінки користувачів (UBA)**: Виявлення незвичайних шаблонів доступу користувачів  
- **Аналіз поведінки сутностей (EBA)**: Моніторинг поведінки MCP-серверів та інструментів  
- **Виявлення аномалій за допомогою ШІ**: Ідентифікація загроз безпеці за допомогою штучного інтелекту  
- **Кореляція розвідки загроз**: Зіставлення спостережуваних дій із відомими шаблонами атак  

## 9. **Реагування на інциденти та відновлення**

### **Автоматизовані можливості реагування**

**Негайні дії у відповідь:**
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

### **Можливості судової експертизи**

**Підтримка розслідувань:**
- **Збереження журналів аудиту**: Незмінне ведення журналів із криптографічною цілісністю  
- **Збір доказів**: Автоматизоване збирання відповідних артефактів безпеки  
- **Реконструкція хронології**: Детальна послідовність подій, що призвели до інцидентів безпеки  
- **Оцінка впливу**: Оцінка масштабу компрометації та витоку даних  

## **Ключові принципи архітектури безпеки**

### **Захист у глибину**
- **Кілька шарів безпеки**: Відсутність єдиної точки відмови в архітектурі безпеки  
- **Резервні заходи**: Перекриваючі заходи безпеки для критичних функцій  
- **Механізми безпечного відмови**: Безпечні значення за замовчуванням у разі помилок або атак  

### **Реалізація принципу Zero Trust**
- **Ніколи не довіряй, завжди перевіряй**: Постійна перевірка всіх сутностей і запитів  
- **Принцип найменших привілеїв**: Мінімальні права доступу для всіх компонентів  
- **Мікросегментація**: Гранульовані мережеві та контрольні доступи  

### **Безперервна еволюція безпеки**
- **Адаптація до загроз**: Регулярні оновлення для усунення нових загроз  
- **Ефективність контролю безпеки**: Постійна оцінка та вдосконалення заходів  
- **Відповідність специфікаціям**: Вирівнювання з еволюційними стандартами безпеки MCP  

---

## **Ресурси для реалізації**

### **Офіційна документація MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Рішення Microsoft для безпеки**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Стандарти безпеки**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Важливо**: Ці заходи безпеки відображають поточну специфікацію MCP (2025-06-18). Завжди перевіряйте останню [офіційну документацію](https://spec.modelcontextprotocol.io/), оскільки стандарти швидко розвиваються.

**Відмова від відповідальності**:  
Цей документ був перекладений за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ на його рідній мові слід вважати авторитетним джерелом. Для критичної інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникають внаслідок використання цього перекладу.