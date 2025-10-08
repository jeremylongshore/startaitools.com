<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T17:27:07+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "sr"
}
-->
# MCP Безбедносне Контроле - Ажурирање за август 2025.

> **Тренутни Стандард**: Овај документ одражава [MCP Спецификацију 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) безбедносне захтеве и званичне [MCP Најбоље Практике за Безбедност](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Протокол за Контекст Модела (MCP) значајно је напредовао са побољшаним безбедносним контролама које се баве како традиционалним софтверским безбедносним претњама, тако и претњама специфичним за вештачку интелигенцију. Овај документ пружа свеобухватне безбедносне контроле за сигурне MCP имплементације од августа 2025.

## **ОБАВЕЗНИ Безбедносни Захтеви**

### **Критичне Забране из MCP Спецификације:**

> **ЗАБРАЊЕНО**: MCP сервери **НЕ СМЕЈУ** прихватити било који токен који није изричито издат за MCP сервер  
>
> **ЗАБРАЊЕНО**: MCP сервери **НЕ СМЕЈУ** користити сесије за аутентификацију  
>
> **ОБАВЕЗНО**: MCP сервери који имплементирају ауторизацију **МОРАЈУ** проверити СВЕ долазне захтеве  
>
> **ОБАВЕЗНО**: MCP прокси сервери који користе статичне ID клијената **МОРАЈУ** добити сагласност корисника за сваког динамички регистрованог клијента  

---

## 1. **Контроле Аутентификације и Ауторизације**

### **Интеграција Спољашњих Провајдера Идентитета**

**Тренутни MCP Стандард (2025-06-18)** дозвољава MCP серверима да делегирају аутентификацију спољашњим провајдерима идентитета, што представља значајно побољшање безбедности:

**Безбедносне Предности:**
1. **Елиминисање Ризика Прилагођене Аутентификације**: Смањује површину рањивости избегавањем прилагођених имплементација аутентификације  
2. **Безбедност на Ентерпрајз Нивоу**: Користи утврђене провајдере идентитета као што је Microsoft Entra ID са напредним безбедносним функцијама  
3. **Централизовано Управљање Идентитетом**: Олакшава управљање животним циклусом корисника, контролу приступа и ревизију усклађености  
4. **Вишефакторска Аутентификација**: Наслеђује MFA могућности од ентерпрајз провајдера идентитета  
5. **Политике Условног Приступа**: Користи контроле приступа засноване на ризику и адаптивну аутентификацију  

**Захтеви за Имплементацију:**
- **Валидација Аудиторијума Токена**: Проверите да су сви токени изричито издати за MCP сервер  
- **Провера Издаваоца**: Потврдите да издаваоц токена одговара очекиваном провајдеру идентитета  
- **Провера Потписа**: Криптографска валидација интегритета токена  
- **Примена Истека**: Строга примена временских ограничења за токене  
- **Валидација Опсега**: Уверите се да токени садрже одговарајуће дозволе за тражене операције  

### **Безбедност Логике Ауторизације**

**Критичне Контроле:**
- **Свеобухватне Ревизије Ауторизације**: Редовне безбедносне провере свих тачака одлучивања о ауторизацији  
- **Безбедни Подразумевани Поставки**: Одбијте приступ када логика ауторизације не може донети дефинитивну одлуку  
- **Границе Дозвола**: Јасно раздвајање између различитих нивоа привилегија и приступа ресурсима  
- **Логовање Ревизије**: Комплетно бележење свих одлука о ауторизацији ради праћења безбедности  
- **Редовне Провере Приступа**: Периодична валидација дозвола корисника и додељених привилегија  

## 2. **Безбедност Токена и Контроле против Прослеђивања**

### **Превенција Прослеђивања Токена**

**Прослеђивање токена је изричито забрањено** у MCP Спецификацији Ауторизације због критичних безбедносних ризика:

**Ризици који се Адресирају:**
- **Заобилажење Контрола**: Заобилази основне безбедносне контроле као што су ограничење брзине, валидација захтева и праћење саобраћаја  
- **Прекид Одговорности**: Онемогућава идентификацију клијента, што корумпира ревизијске трагове и истрагу инцидената  
- **Експлоатација Проксија**: Омогућава злонамерним актерима да користе сервере као проксије за неовлашћени приступ подацима  
- **Кршење Границе Поверења**: Нарушава претпоставке о пореклу токена код услуга низводно  
- **Латерално Кретање**: Компромитовани токени широм више услуга омогућавају ширење напада  

**Контроле за Имплементацију:**
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

### **Шаблони за Безбедно Управљање Токенима**

**Најбоље Практике:**
- **Токени Кратког Рока Трајања**: Минимизирајте прозор изложености честом ротацијом токена  
- **Издавање по Потреби**: Издајте токене само када су потребни за одређене операције  
- **Сигурно Чување**: Користите хардверске безбедносне модуле (HSM) или сигурне трезоре за кључеве  
- **Везивање Токена**: Вежите токене за одређене клијенте, сесије или операције где је могуће  
- **Праћење и Упозорење**: Детекција у реалном времену злоупотребе токена или неовлашћених образаца приступа  

## 3. **Контроле Безбедности Сесија**

### **Превенција Отмице Сесије**

**Адресирани Вектори Напада:**
- **Убризгавање Злонамерних Догађаја у Сесију**: Злонамерни догађаји убризгани у заједничко стање сесије  
- **Имперсонација Сесије**: Неовлашћено коришћење украдених ID-ова сесије за заобилажење аутентификације  
- **Напади на Ресумпцију Стримова**: Експлоатација наставка догађаја које шаље сервер за убризгавање злонамерног садржаја  

**Обавезне Контроле Сесије:**
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

**Безбедност Транспорта:**
- **Примена HTTPS**: Сва комуникација сесије преко TLS 1.3  
- **Атрибути Сигурних Колачића**: HttpOnly, Secure, SameSite=Strict  
- **Пининг Сертификата**: За критичне везе ради спречавања MITM напада  

### **Разматрања о Стању Сесије**

**За Стање Сесије:**
- Заједничко стање сесије захтева додатну заштиту од напада убризгавања  
- Управљање сесијама засновано на редовима захтева верификацију интегритета  
- Више инстанци сервера захтевају сигурну синхронизацију стања сесије  

**За Бездржавне Имплементације:**
- JWT или слично управљање сесијама засновано на токенима  
- Криптографска верификација интегритета стања сесије  
- Смањена површина напада, али захтева робусну валидацију токена  

## 4. **Контроле Безбедности Специфичне за Вештачку Интелигенцију**

### **Одбрана од Убризгавања Упита**

**Интеграција Microsoft Prompt Shields:**
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

**Контроле за Имплементацију:**
- **Санитизација Уноса**: Свеобухватна валидација и филтрирање свих корисничких уноса  
- **Дефинисање Границе Садржаја**: Јасно раздвајање између системских инструкција и корисничког садржаја  
- **Хијерархија Инструкција**: Правилна правила првенства за конфликтне инструкције  
- **Праћење Излазног Садржаја**: Детекција потенцијално штетних или манипулисаних излаза  

### **Превенција Тровања Алатима**

**Оквир Безбедности Алатки:**
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

**Динамичко Управљање Алатима:**
- **Радни Токови Одобрења**: Изричита сагласност корисника за модификације алата  
- **Могућности Враћања**: Способност враћања на претходне верзије алата  
- **Ревизија Промена**: Комплетна историја модификација дефиниције алата  
- **Процена Ризика**: Аутоматизована евалуација безбедносног стања алата  

## 5. **Превенција Напада Збуњеног Заменика**

### **Безбедност OAuth Проксија**

**Контроле за Превенцију Напада:**
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

**Захтеви за Имплементацију:**
- **Провера Сагласности Корисника**: Никада не прескачите екране сагласности за динамичку регистрацију клијената  
- **Валидација URI Преусмеравања**: Строга валидација заснована на белој листи дестинација за преусмеравање  
- **Заштита Кодова Ауторизације**: Кодови кратког рока трајања са применом једнократне употребе  
- **Провера Идентитета Клијента**: Робусна валидација акредитива и метаподатака клијента  

## 6. **Безбедност Извршавања Алатки**

### **Сандбоксинг и Изолација**

**Изолација Заснована на Контејнерима:**
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

**Изолација Процеса:**
- **Одвојени Контексти Процеса**: Свако извршавање алата у изолованом простору процеса  
- **Међупроцесна Комуникација**: Сигурни механизми IPC са валидацијом  
- **Праћење Процеса**: Анализа понашања у реалном времену и детекција аномалија  
- **Примена Ресурса**: Тврда ограничења на CPU, меморију и I/O операције  

### **Имплементација Минималних Привилегија**

**Управљање Дозволама:**
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

## 7. **Контроле Безбедности Ланца Снабдевања**

### **Верификација Зависности**

**Свеобухватна Безбедност Компоненти:**
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

### **Континуирано Праћење**

**Детекција Претњи у Ланцу Снабдевања:**
- **Праћење Здравља Зависности**: Континуирана процена свих зависности за безбедносне проблеме  
- **Интеграција Обавештајних Података о Претњама**: Ажурирања у реалном времену о новим претњама у ланцу снабдевања  
- **Анализа Понашања**: Детекција необичног понашања у спољашњим компонентама  
- **Аутоматизовани Одговор**: Одмах ограничење компромитованих компоненти  

## 8. **Контроле Праћења и Детекције**

### **Управљање Безбедносним Информацијама и Догађајима (SIEM)**

**Свеобухватна Стратегија Логовања:**
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

### **Детекција Претњи у Реалном Времену**

**Аналитика Понашања:**
- **Аналитика Понашања Корисника (UBA)**: Детекција необичних образаца приступа корисника  
- **Аналитика Понашања Ентитета (EBA)**: Праћење понашања MCP сервера и алата  
- **Детекција Аномалија Заснована на Машинском Учењу**: Идентификација безбедносних претњи помоћу AI  
- **Корелација Обавештајних Података о Претњама**: Упоређивање посматраних активности са познатим обрасцима напада  

## 9. **Одговор на Инциденте и Опоравак**

### **Аутоматизоване Могућности Одговора**

**Акције Одговора у Реалном Времену:**
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

### **Форензичке Могућности**

**Подршка за Истраживање:**
- **Очување Ревизијског Трага**: Непроменљиво логовање са криптографским интегритетом  
- **Прикупљање Доказног Материјала**: Аутоматизовано прикупљање релевантних безбедносних артефаката  
- **Реконструкција Временске Линије**: Детаљан низ догађаја који су довели до безбедносних инцидената  
- **Процена Утицаја**: Евалуација обима компромиса и изложености података  

## **Кључни Принципи Архитектуре Безбедности**

### **Одбрана у Дубини**
- **Вишеструки Слојеви Безбедности**: Нема једне тачке отказа у архитектури безбедности  
- **Редундантне Контроле**: Преклапајуће безбедносне мере за критичне функције  
- **Механизми Безбедног Отказа**: Безбедни подразумевани поставки када системи наиђу на грешке или нападе  

### **Имплементација Zero Trust**
- **Никада Не Веруј, Увек Проверавај**: Континуирана валидација свих ентитета и захтева  
- **Принцип Минималних Привилегија**: Минимална права приступа за све компоненте  
- **Микро-Сегментација**: Грануларна контрола мреже и приступа  

### **Континуирана Еволуција Безбедности**
- **Адаптација Претњама**: Редовна ажурирања ради адресирања нових претњи  
- **Ефикасност Безбедносних Контрола**: Стално оцењивање и побољшање контрола  
- **Усклађеност са Спецификацијом**: Усклађеност са еволуирајућим MCP безбедносним стандардима  

---

## **Ресурси за Имплементацију**

### **Званична MCP Документација**
- [MCP Спецификација (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Најбоље Практике за Безбедност](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Сп

**Одрицање од одговорности**:  
Овај документ је преведен коришћењем услуге за превођење помоћу вештачке интелигенције [Co-op Translator](https://github.com/Azure/co-op-translator). Иако настојимо да обезбедимо тачност, молимо вас да имате у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати меродавним извором. За критичне информације препоручује се професионални превод од стране људи. Не преузимамо одговорност за било каква погрешна тумачења или неспоразуме који могу настати услед коришћења овог превода.