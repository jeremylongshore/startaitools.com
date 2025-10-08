<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T13:44:01+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ar"
}
-->
# تحديث ضوابط الأمان لـ MCP - أغسطس 2025

> **المعيار الحالي**: يعكس هذا المستند متطلبات الأمان وفقًا لـ [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) وأفضل الممارسات الرسمية للأمان [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

لقد تطور بروتوكول Model Context Protocol (MCP) بشكل كبير مع تعزيز ضوابط الأمان التي تعالج تهديدات البرمجيات التقليدية والتهديدات الخاصة بالذكاء الاصطناعي. يقدم هذا المستند ضوابط أمان شاملة لتطبيقات MCP الآمنة اعتبارًا من أغسطس 2025.

## **متطلبات الأمان الإلزامية**

### **المحظورات الحرجة من مواصفات MCP:**

> **ممنوع**: يجب على خوادم MCP **عدم قبول** أي رموز (tokens) لم يتم إصدارها صراحةً لخادم MCP  
>
> **محظور**: يجب على خوادم MCP **عدم استخدام** الجلسات للمصادقة  
>
> **مطلوب**: يجب على خوادم MCP التي تنفذ التفويض **التحقق من جميع الطلبات الواردة**  
>
> **إلزامي**: يجب على خوادم الوكيل MCP التي تستخدم معرفات عملاء ثابتة **الحصول على موافقة المستخدم** لكل عميل يتم تسجيله ديناميكيًا  

---

## 1. **ضوابط المصادقة والتفويض**

### **تكامل مزود الهوية الخارجي**

يسمح معيار MCP الحالي (2025-06-18) لخوادم MCP بتفويض المصادقة إلى مزودي الهوية الخارجيين، مما يمثل تحسينًا كبيرًا في الأمان:

**فوائد الأمان:**
1. **القضاء على مخاطر المصادقة المخصصة**: يقلل من سطح الهجوم من خلال تجنب تنفيذ مصادقة مخصصة  
2. **أمان على مستوى المؤسسات**: يستفيد من مزودي الهوية المعروفين مثل Microsoft Entra ID بميزات أمان متقدمة  
3. **إدارة هوية مركزية**: تبسيط إدارة دورة حياة المستخدم، والتحكم في الوصول، وتدقيق الامتثال  
4. **المصادقة متعددة العوامل (MFA)**: الاستفادة من قدرات MFA من مزودي الهوية المؤسسيين  
5. **سياسات الوصول الشرطي**: الاستفادة من ضوابط الوصول القائمة على المخاطر والمصادقة التكيفية  

**متطلبات التنفيذ:**
- **التحقق من جمهور الرمز**: التحقق من أن جميع الرموز تم إصدارها صراحةً لخادم MCP  
- **التحقق من المصدر**: التحقق من أن مصدر الرمز يتطابق مع مزود الهوية المتوقع  
- **التحقق من التوقيع**: التحقق التشفيري من سلامة الرمز  
- **فرض انتهاء الصلاحية**: فرض صارم لحدود عمر الرمز  
- **التحقق من النطاق**: التأكد من أن الرموز تحتوي على الأذونات المناسبة للعمليات المطلوبة  

### **أمان منطق التفويض**

**الضوابط الحرجة:**
- **مراجعات تفويض شاملة**: مراجعات أمان منتظمة لجميع نقاط اتخاذ قرارات التفويض  
- **الإعدادات الافتراضية الآمنة**: رفض الوصول عندما لا يمكن لمنطق التفويض اتخاذ قرار حاسم  
- **حدود الأذونات**: فصل واضح بين مستويات الامتياز المختلفة والوصول إلى الموارد  
- **تسجيل التدقيق**: تسجيل كامل لجميع قرارات التفويض لمراقبة الأمان  
- **مراجعات الوصول المنتظمة**: التحقق الدوري من أذونات المستخدم وتعيينات الامتيازات  

## 2. **أمان الرموز وضوابط منع التمرير**

### **منع تمرير الرموز**

**تم حظر تمرير الرموز بشكل صريح** في مواصفات تفويض MCP بسبب المخاطر الأمنية الحرجة:

**المخاطر الأمنية التي يتم معالجتها:**
- **تجاوز الضوابط**: يتجاوز ضوابط الأمان الأساسية مثل تحديد المعدل، والتحقق من الطلبات، ومراقبة الحركة  
- **انهيار المسؤولية**: يجعل تحديد هوية العميل مستحيلاً، مما يفسد سجلات التدقيق والتحقيق في الحوادث  
- **الاستخراج عبر الوكيل**: يمكّن الجهات الخبيثة من استخدام الخوادم كوسطاء للوصول غير المصرح به إلى البيانات  
- **انتهاكات حدود الثقة**: يكسر افتراضات الثقة الخاصة بالخدمات اللاحقة حول أصول الرموز  
- **الحركة الجانبية**: تمكّن الرموز المخترقة عبر خدمات متعددة من توسيع الهجوم بشكل أوسع  

**ضوابط التنفيذ:**
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

### **أنماط إدارة الرموز الآمنة**

**أفضل الممارسات:**
- **الرموز قصيرة العمر**: تقليل نافذة التعرض من خلال التدوير المتكرر للرموز  
- **الإصدار عند الحاجة**: إصدار الرموز فقط عند الحاجة لعمليات محددة  
- **التخزين الآمن**: استخدام وحدات أمان الأجهزة (HSMs) أو خزائن المفاتيح الآمنة  
- **ربط الرموز**: ربط الرموز بعملاء أو جلسات أو عمليات محددة حيثما أمكن  
- **المراقبة والتنبيه**: الكشف في الوقت الفعلي عن إساءة استخدام الرموز أو أنماط الوصول غير المصرح بها  

## 3. **ضوابط أمان الجلسات**

### **منع اختطاف الجلسات**

**نواقل الهجوم التي يتم معالجتها:**
- **حقن اختطاف الجلسة**: أحداث خبيثة يتم حقنها في حالة الجلسة المشتركة  
- **انتحال الجلسة**: الاستخدام غير المصرح به لمعرفات الجلسة المسروقة لتجاوز المصادقة  
- **هجمات استئناف التدفق**: استغلال استئناف الأحداث المرسلة من الخادم لحقن محتوى خبيث  

**ضوابط الجلسة الإلزامية:**
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

**أمان النقل:**
- **فرض HTTPS**: جميع اتصالات الجلسة عبر TLS 1.3  
- **سمات ملفات تعريف الارتباط الآمنة**: HttpOnly، Secure، SameSite=Strict  
- **تثبيت الشهادات**: للاتصالات الحرجة لمنع هجمات MITM  

### **اعتبارات الحالة مقابل عدم الحالة**

**للتطبيقات ذات الحالة:**
- تتطلب حالة الجلسة المشتركة حماية إضافية ضد هجمات الحقن  
- تحتاج إدارة الجلسات القائمة على الطابور إلى التحقق من السلامة  
- تتطلب مثيلات الخادم المتعددة مزامنة آمنة لحالة الجلسة  

**للتطبيقات عديمة الحالة:**
- إدارة الجلسات باستخدام JWT أو رموز مشابهة  
- التحقق التشفيري من سلامة حالة الجلسة  
- تقليل سطح الهجوم ولكن يتطلب التحقق القوي من الرموز  

## 4. **ضوابط الأمان الخاصة بالذكاء الاصطناعي**

### **الدفاع ضد حقن التعليمات**

**تكامل Microsoft Prompt Shields:**
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

**ضوابط التنفيذ:**
- **تنقية المدخلات**: التحقق الشامل وتصفيتها لجميع مدخلات المستخدم  
- **تعريف حدود المحتوى**: فصل واضح بين تعليمات النظام ومحتوى المستخدم  
- **تسلسل التعليمات**: قواعد أولوية مناسبة للتعليمات المتضاربة  
- **مراقبة المخرجات**: الكشف عن المخرجات الضارة أو المتلاعب بها  

### **منع تسميم الأدوات**

**إطار أمان الأدوات:**
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

**إدارة الأدوات الديناميكية:**
- **عمليات الموافقة**: موافقة المستخدم الصريحة على تعديلات الأدوات  
- **إمكانيات التراجع**: القدرة على العودة إلى إصدارات الأدوات السابقة  
- **تدقيق التغييرات**: سجل كامل لتعديلات تعريف الأدوات  
- **تقييم المخاطر**: تقييم آلي لوضع أمان الأدوات  

## 5. **منع هجمات الوكيل المربك**

### **أمان وكيل OAuth**

**ضوابط منع الهجوم:**
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

**متطلبات التنفيذ:**
- **التحقق من موافقة المستخدم**: عدم تخطي شاشات الموافقة لتسجيل العملاء الديناميكي  
- **التحقق من URI لإعادة التوجيه**: التحقق الصارم القائم على القائمة البيضاء لوجهات إعادة التوجيه  
- **حماية رمز التفويض**: رموز قصيرة العمر مع فرض الاستخدام لمرة واحدة  
- **التحقق من هوية العميل**: التحقق القوي من بيانات اعتماد العميل والبيانات الوصفية  

## 6. **أمان تنفيذ الأدوات**

### **العزل والتشغيل في بيئة محمية**

**العزل القائم على الحاويات:**
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

**عزل العمليات:**
- **سياقات عمليات منفصلة**: تنفيذ كل أداة في مساحة عملية معزولة  
- **اتصالات العمليات البينية**: آليات IPC آمنة مع التحقق  
- **مراقبة العمليات**: تحليل السلوك أثناء التشغيل واكتشاف الشذوذ  
- **فرض الموارد**: حدود صارمة على وحدة المعالجة المركزية والذاكرة وعمليات الإدخال/الإخراج  

### **تنفيذ مبدأ أقل الامتيازات**

**إدارة الأذونات:**
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

## 7. **ضوابط أمان سلسلة التوريد**

### **التحقق من التبعيات**

**أمان المكونات الشامل:**
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

### **المراقبة المستمرة**

**كشف تهديدات سلسلة التوريد:**
- **مراقبة صحة التبعيات**: التقييم المستمر لجميع التبعيات بحثًا عن مشكلات الأمان  
- **تكامل معلومات التهديدات**: تحديثات في الوقت الفعلي حول تهديدات سلسلة التوريد الناشئة  
- **تحليل السلوك**: الكشف عن السلوك غير المعتاد في المكونات الخارجية  
- **الاستجابة الآلية**: احتواء فوري للمكونات المخترقة  

## 8. **ضوابط المراقبة والكشف**

### **إدارة معلومات الأمان والأحداث (SIEM)**

**استراتيجية تسجيل شاملة:**
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

### **الكشف عن التهديدات في الوقت الفعلي**

**تحليلات السلوك:**
- **تحليلات سلوك المستخدم (UBA)**: الكشف عن أنماط الوصول غير المعتادة للمستخدم  
- **تحليلات سلوك الكيانات (EBA)**: مراقبة سلوك خادم MCP والأدوات  
- **اكتشاف الشذوذ باستخدام الذكاء الاصطناعي**: تحديد التهديدات الأمنية باستخدام الذكاء الاصطناعي  
- **مقارنة معلومات التهديدات**: مطابقة الأنشطة المرصودة مع أنماط الهجوم المعروفة  

## 9. **الاستجابة للحوادث والتعافي**

### **قدرات الاستجابة الآلية**

**إجراءات الاستجابة الفورية:**
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

### **قدرات التحليل الجنائي**

**دعم التحقيق:**
- **حفظ سجلات التدقيق**: تسجيل غير قابل للتغيير مع سلامة تشفيرية  
- **جمع الأدلة**: جمع آلي للمواد الأمنية ذات الصلة  
- **إعادة بناء الجدول الزمني**: تسلسل مفصل للأحداث التي أدت إلى الحوادث الأمنية  
- **تقييم التأثير**: تقييم نطاق الاختراق والتعرض للبيانات  

## **المبادئ الرئيسية لهندسة الأمان**

### **الدفاع في العمق**
- **طبقات أمان متعددة**: عدم وجود نقطة فشل واحدة في بنية الأمان  
- **ضوابط متكررة**: تدابير أمان متداخلة للوظائف الحرجة  
- **آليات آمنة عند الفشل**: إعدادات افتراضية آمنة عند مواجهة الأنظمة للأخطاء أو الهجمات  

### **تنفيذ الثقة الصفرية**
- **عدم الثقة مطلقًا، التحقق دائمًا**: التحقق المستمر من جميع الكيانات والطلبات  
- **مبدأ أقل الامتيازات**: حقوق وصول دنيا لجميع المكونات  
- **التقسيم الدقيق**: ضوابط شبكة ووصول دقيقة  

### **التطور المستمر للأمان**
- **التكيف مع مشهد التهديدات**: تحديثات منتظمة لمعالجة التهديدات الناشئة  
- **فعالية ضوابط الأمان**: التقييم والتحسين المستمر للضوابط  
- **الامتثال للمواصفات**: التوافق مع معايير أمان MCP المتطورة  

---

## **موارد التنفيذ**

### **وثائق MCP الرسمية**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **حلول الأمان من Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **معايير الأمان**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **مهم**: تعكس ضوابط الأمان هذه مواصفات MCP الحالية (2025-06-18). تحقق دائمًا من [الوثائق الرسمية](https://spec.modelcontextprotocol.io/) حيث تستمر المعايير في التطور بسرعة.  

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو معلومات غير دقيقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق. للحصول على معلومات حاسمة، يُوصى بالاستعانة بترجمة بشرية احترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة تنشأ عن استخدام هذه الترجمة.