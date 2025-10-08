<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T12:06:59+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "fa"
}
-->
# کنترل‌های امنیتی MCP - به‌روزرسانی آگوست ۲۰۲۵

> **استاندارد فعلی**: این سند الزامات امنیتی [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) و [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) رسمی را منعکس می‌کند.

پروتکل مدل کانتکست (MCP) به طور قابل توجهی پیشرفت کرده است و کنترل‌های امنیتی بهبودیافته‌ای را برای مقابله با تهدیدات سنتی نرم‌افزاری و تهدیدات خاص هوش مصنوعی ارائه می‌دهد. این سند کنترل‌های امنیتی جامع برای پیاده‌سازی‌های امن MCP تا آگوست ۲۰۲۵ را ارائه می‌دهد.

## **الزامات امنیتی اجباری**

### **ممنوعیت‌های حیاتی از MCP Specification:**

> **ممنوع**: سرورهای MCP **نباید** هیچ توکنی را که به طور صریح برای سرور MCP صادر نشده است، بپذیرند.
>
> **ممنوع**: سرورهای MCP **نباید** از جلسات برای احراز هویت استفاده کنند.  
>
> **الزامی**: سرورهای MCP که مجوزدهی را پیاده‌سازی می‌کنند، **باید** تمام درخواست‌های ورودی را تأیید کنند.
>
> **اجباری**: سرورهای پروکسی MCP که از شناسه‌های ثابت مشتری استفاده می‌کنند، **باید** برای هر مشتری ثبت‌شده پویا رضایت کاربر را دریافت کنند.

---

## ۱. **کنترل‌های احراز هویت و مجوزدهی**

### **ادغام با ارائه‌دهندگان هویت خارجی**

**استاندارد فعلی MCP (2025-06-18)** به سرورهای MCP اجازه می‌دهد تا احراز هویت را به ارائه‌دهندگان هویت خارجی واگذار کنند، که این یک پیشرفت امنیتی قابل توجه است:

### **ادغام با ارائه‌دهندگان هویت خارجی**

**استاندارد فعلی MCP (2025-06-18)** به سرورهای MCP اجازه می‌دهد تا احراز هویت را به ارائه‌دهندگان هویت خارجی واگذار کنند، که این یک پیشرفت امنیتی قابل توجه است:

**مزایای امنیتی:**
۱. **حذف خطرات احراز هویت سفارشی**: کاهش سطح آسیب‌پذیری با اجتناب از پیاده‌سازی‌های احراز هویت سفارشی  
۲. **امنیت در سطح سازمانی**: استفاده از ارائه‌دهندگان هویت معتبر مانند Microsoft Entra ID با ویژگی‌های امنیتی پیشرفته  
۳. **مدیریت متمرکز هویت**: ساده‌سازی مدیریت چرخه عمر کاربران، کنترل دسترسی و ممیزی انطباق  
۴. **احراز هویت چندعاملی**: بهره‌گیری از قابلیت‌های MFA ارائه‌دهندگان هویت سازمانی  
۵. **سیاست‌های دسترسی شرطی**: بهره‌مندی از کنترل‌های دسترسی مبتنی بر ریسک و احراز هویت تطبیقی  

**الزامات پیاده‌سازی:**
- **اعتبارسنجی مخاطب توکن**: تأیید کنید که تمام توکن‌ها به طور صریح برای سرور MCP صادر شده‌اند.  
- **تأیید صادرکننده**: مطمئن شوید که صادرکننده توکن با ارائه‌دهنده هویت مورد انتظار مطابقت دارد.  
- **تأیید امضا**: اعتبارسنجی رمزنگاری یکپارچگی توکن  
- **اجرای انقضا**: اجرای دقیق محدودیت‌های زمانی عمر توکن  
- **اعتبارسنجی محدوده**: اطمینان حاصل کنید که توکن‌ها دارای مجوزهای مناسب برای عملیات درخواست‌شده هستند.  

### **امنیت منطق مجوزدهی**

**کنترل‌های حیاتی:**
- **ممیزی‌های جامع مجوزدهی**: بررسی‌های امنیتی منظم از تمام نقاط تصمیم‌گیری مجوزدهی  
- **پیش‌فرض‌های ایمن**: دسترسی را زمانی که منطق مجوزدهی نمی‌تواند تصمیم قطعی بگیرد، رد کنید.  
- **مرزهای مجوز**: جداسازی واضح بین سطوح مختلف امتیازات و دسترسی به منابع  
- **ثبت ممیزی**: ثبت کامل تمام تصمیمات مجوزدهی برای نظارت امنیتی  
- **بررسی‌های منظم دسترسی**: اعتبارسنجی دوره‌ای مجوزهای کاربران و تخصیص امتیازات  

## ۲. **امنیت توکن و کنترل‌های ضد عبور**

### **پیشگیری از عبور توکن**

**عبور توکن به طور صریح در MCP Authorization Specification ممنوع است** به دلیل خطرات امنیتی حیاتی:

**خطرات امنیتی که برطرف شده‌اند:**
- **دور زدن کنترل‌ها**: دور زدن کنترل‌های امنیتی ضروری مانند محدودیت نرخ، اعتبارسنجی درخواست و نظارت بر ترافیک  
- **شکست حسابرسی**: شناسایی مشتری را غیرممکن می‌کند و مسیرهای ممیزی و تحقیقات حادثه را خراب می‌کند.  
- **نفوذ مبتنی بر پروکسی**: به بازیگران مخرب اجازه می‌دهد از سرورها به عنوان پروکسی برای دسترسی غیرمجاز به داده‌ها استفاده کنند.  
- **نقض مرزهای اعتماد**: فرضیات اعتماد سرویس‌های پایین‌دستی درباره منشأ توکن‌ها را خراب می‌کند.  
- **حرکت جانبی**: توکن‌های به خطر افتاده در چندین سرویس امکان گسترش حملات گسترده‌تر را فراهم می‌کنند.  

**کنترل‌های پیاده‌سازی:**
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

### **الگوهای مدیریت امن توکن**

**بهترین شیوه‌ها:**
- **توکن‌های کوتاه‌مدت**: کاهش پنجره آسیب‌پذیری با چرخش مکرر توکن  
- **صدور به‌موقع**: صدور توکن‌ها فقط زمانی که برای عملیات خاص مورد نیاز هستند  
- **ذخیره‌سازی امن**: استفاده از ماژول‌های امنیتی سخت‌افزاری (HSM) یا مخازن کلید امن  
- **اتصال توکن**: اتصال توکن‌ها به مشتریان، جلسات یا عملیات خاص در صورت امکان  
- **نظارت و هشدار**: تشخیص بلادرنگ سوءاستفاده از توکن یا الگوهای دسترسی غیرمجاز  

## ۳. **کنترل‌های امنیتی جلسه**

### **پیشگیری از ربودن جلسه**

**بردارهای حمله که برطرف شده‌اند:**
- **تزریق درخواست ربودن جلسه**: رویدادهای مخرب تزریق‌شده به حالت جلسه مشترک  
- **جعل جلسه**: استفاده غیرمجاز از شناسه‌های جلسه دزدیده‌شده برای دور زدن احراز هویت  
- **حملات جریان قابل ازسرگیری**: سوءاستفاده از ازسرگیری رویدادهای ارسال‌شده توسط سرور برای تزریق محتوای مخرب  

**کنترل‌های اجباری جلسه:**
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

**امنیت انتقال:**
- **اجرای HTTPS**: تمام ارتباطات جلسه از طریق TLS 1.3  
- **ویژگی‌های امن کوکی**: HttpOnly، Secure، SameSite=Strict  
- **پین کردن گواهی**: برای اتصالات حیاتی جهت جلوگیری از حملات MITM  

### **ملاحظات حالت‌دار در مقابل بدون حالت**

**برای پیاده‌سازی‌های حالت‌دار:**
- حالت جلسه مشترک نیاز به حفاظت اضافی در برابر حملات تزریقی دارد.  
- مدیریت جلسه مبتنی بر صف نیاز به اعتبارسنجی یکپارچگی دارد.  
- نمونه‌های متعدد سرور نیاز به همگام‌سازی امن حالت جلسه دارند.  

**برای پیاده‌سازی‌های بدون حالت:**
- مدیریت جلسه مبتنی بر توکن JWT یا مشابه  
- اعتبارسنجی رمزنگاری یکپارچگی حالت جلسه  
- کاهش سطح حمله اما نیاز به اعتبارسنجی قوی توکن  

## ۴. **کنترل‌های امنیتی خاص هوش مصنوعی**

### **دفاع در برابر تزریق درخواست**

**ادغام Microsoft Prompt Shields:**
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

**کنترل‌های پیاده‌سازی:**
- **پاک‌سازی ورودی**: اعتبارسنجی و فیلتر جامع تمام ورودی‌های کاربران  
- **تعریف مرز محتوا**: جداسازی واضح بین دستورالعمل‌های سیستم و محتوای کاربران  
- **سلسله‌مراتب دستورالعمل‌ها**: قوانین اولویت مناسب برای دستورالعمل‌های متناقض  
- **نظارت بر خروجی**: تشخیص خروجی‌های بالقوه مضر یا دستکاری‌شده  

### **پیشگیری از مسمومیت ابزار**

**چارچوب امنیت ابزار:**
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

**مدیریت پویا ابزار:**
- **گردش‌کارهای تأیید**: رضایت صریح کاربران برای تغییرات ابزار  
- **قابلیت‌های بازگشت**: توانایی بازگشت به نسخه‌های قبلی ابزار  
- **ممیزی تغییرات**: تاریخچه کامل تغییرات تعریف ابزار  
- **ارزیابی ریسک**: ارزیابی خودکار وضعیت امنیتی ابزار  

## ۵. **پیشگیری از حملات نماینده سردرگم**

### **امنیت پروکسی OAuth**

**کنترل‌های پیشگیری از حمله:**
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

**الزامات پیاده‌سازی:**
- **تأیید رضایت کاربر**: هرگز صفحه‌های رضایت را برای ثبت مشتری پویا رد نکنید.  
- **اعتبارسنجی URI بازگشت**: اعتبارسنجی دقیق مبتنی بر لیست سفید مقصدهای بازگشت  
- **حفاظت از کد مجوز**: کدهای کوتاه‌مدت با اجرای استفاده یک‌بار  
- **تأیید هویت مشتری**: اعتبارسنجی قوی اعتبارنامه‌ها و متاداده‌های مشتری  

## ۶. **امنیت اجرای ابزار**

### **محصورسازی و جداسازی**

**جداسازی مبتنی بر کانتینر:**
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

**جداسازی فرآیند:**
- **زمینه‌های فرآیند جداگانه**: هر اجرای ابزار در فضای فرآیند جداگانه  
- **ارتباط بین فرآیندها**: مکانیزم‌های IPC امن با اعتبارسنجی  
- **نظارت بر فرآیند**: تحلیل رفتار زمان اجرا و تشخیص ناهنجاری  
- **اجرای منابع**: محدودیت‌های سخت بر CPU، حافظه و عملیات I/O  

### **پیاده‌سازی حداقل امتیاز**

**مدیریت مجوزها:**
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

## ۷. **کنترل‌های امنیتی زنجیره تأمین**

### **اعتبارسنجی وابستگی‌ها**

**امنیت جامع اجزا:**
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

### **نظارت مداوم**

**تشخیص تهدید زنجیره تأمین:**
- **نظارت بر سلامت وابستگی‌ها**: ارزیابی مداوم تمام وابستگی‌ها برای مسائل امنیتی  
- **ادغام اطلاعات تهدید**: به‌روزرسانی بلادرنگ درباره تهدیدات نوظهور زنجیره تأمین  
- **تحلیل رفتاری**: تشخیص رفتار غیرعادی در اجزای خارجی  
- **پاسخ خودکار**: مهار فوری اجزای به خطر افتاده  

## ۸. **کنترل‌های نظارت و تشخیص**

### **مدیریت اطلاعات و رویدادهای امنیتی (SIEM)**

**استراتژی جامع ثبت:**
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

### **تشخیص تهدید بلادرنگ**

**تحلیل رفتاری:**
- **تحلیل رفتار کاربران (UBA)**: تشخیص الگوهای دسترسی غیرعادی کاربران  
- **تحلیل رفتار موجودیت‌ها (EBA)**: نظارت بر رفتار سرور MCP و ابزارها  
- **تشخیص ناهنجاری مبتنی بر یادگیری ماشین**: شناسایی تهدیدات امنیتی با قدرت هوش مصنوعی  
- **همبستگی اطلاعات تهدید**: تطبیق فعالیت‌های مشاهده‌شده با الگوهای حمله شناخته‌شده  

## ۹. **پاسخ به حادثه و بازیابی**

### **قابلیت‌های پاسخ خودکار**

**اقدامات پاسخ فوری:**
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

### **قابلیت‌های قانونی**

**پشتیبانی از تحقیقات:**
- **حفظ مسیرهای ممیزی**: ثبت غیرقابل تغییر با یکپارچگی رمزنگاری  
- **جمع‌آوری شواهد**: جمع‌آوری خودکار مصنوعات امنیتی مرتبط  
- **بازسازی جدول زمانی**: توالی دقیق رویدادهای منجر به حوادث امنیتی  
- **ارزیابی تأثیر**: ارزیابی دامنه نفوذ و افشای داده‌ها  

## **اصول کلیدی معماری امنیتی**

### **دفاع در عمق**
- **لایه‌های امنیتی متعدد**: عدم وجود نقطه شکست واحد در معماری امنیتی  
- **کنترل‌های افزونه**: اقدامات امنیتی همپوشان برای عملکردهای حیاتی  
- **مکانیزم‌های ایمن پیش‌فرض**: پیش‌فرض‌های امن زمانی که سیستم‌ها با خطاها یا حملات مواجه می‌شوند  

### **پیاده‌سازی اعتماد صفر**
- **هرگز اعتماد نکنید، همیشه تأیید کنید**: اعتبارسنجی مداوم تمام موجودیت‌ها و درخواست‌ها  
- **اصل حداقل امتیاز**: حقوق دسترسی حداقلی برای تمام اجزا  
- **تقسیم‌بندی خرد**: کنترل‌های شبکه و دسترسی دقیق  

### **تکامل مداوم امنیت**
- **انطباق با چشم‌انداز تهدیدات**: به‌روزرسانی‌های منظم برای مقابله با تهدیدات نوظهور  
- **اثربخشی کنترل‌های امنیتی**: ارزیابی و بهبود مداوم کنترل‌ها  
- **انطباق با مشخصات**: هماهنگی با استانداردهای امنیتی در حال تکامل MCP  

---

## **منابع پیاده‌سازی**

### **مستندات رسمی MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **راه‌حل‌های امنیتی مایکروسافت**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **استانداردهای امنیتی**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **مهم**: این کنترل‌های امنیتی مشخصات فعلی MCP (2025-06-18) را منعکس می‌کنند. همیشه با [مستندات رسمی](https://spec.modelcontextprotocol.io/) بررسی کنید زیرا استانداردها به سرعت در حال تکامل هستند.

**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما برای دقت تلاش می‌کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان اصلی آن باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حساس، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما هیچ مسئولیتی در قبال سوءتفاهم‌ها یا تفسیرهای نادرست ناشی از استفاده از این ترجمه نداریم.