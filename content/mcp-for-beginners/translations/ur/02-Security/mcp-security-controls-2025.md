<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T14:13:00+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ur"
}
-->
# ایم سی پی سیکیورٹی کنٹرولز - اگست 2025 اپ ڈیٹ

> **موجودہ معیار**: یہ دستاویز [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) کے سیکیورٹی تقاضوں اور [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) کی عکاسی کرتی ہے۔

ماڈل کانٹیکسٹ پروٹوکول (MCP) نے روایتی سافٹ ویئر سیکیورٹی اور AI سے متعلق خطرات کو مدنظر رکھتے ہوئے سیکیورٹی کنٹرولز میں نمایاں بہتری حاصل کی ہے۔ یہ دستاویز اگست 2025 تک محفوظ MCP عمل درآمد کے لیے جامع سیکیورٹی کنٹرولز فراہم کرتی ہے۔

## **لازمی سیکیورٹی تقاضے**

### **MCP وضاحت نامے سے اہم ممانعتیں:**

> **ممنوع**: MCP سرورز کو **کسی بھی ایسے ٹوکن کو قبول نہیں کرنا چاہیے** جو خاص طور پر MCP سرور کے لیے جاری نہ کیا گیا ہو  
>
> **ممنوع**: MCP سرورز کو **سیشنز کو تصدیق کے لیے استعمال نہیں کرنا چاہیے**  
>
> **ضروری**: MCP سرورز جو اجازت نامہ نافذ کرتے ہیں انہیں **تمام آنے والی درخواستوں کی تصدیق کرنی چاہیے**  
>
> **لازمی**: MCP پراکسی سرورز جو جامد کلائنٹ IDs استعمال کرتے ہیں انہیں **ہر متحرک طور پر رجسٹرڈ کلائنٹ کے لیے صارف کی رضامندی حاصل کرنی چاہیے**

---

## 1. **تصدیق اور اجازت کنٹرولز**

### **بیرونی شناخت فراہم کنندہ کے انضمام**

**موجودہ MCP معیار (2025-06-18)** MCP سرورز کو بیرونی شناخت فراہم کنندگان کے ذریعے تصدیق تفویض کرنے کی اجازت دیتا ہے، جو ایک اہم سیکیورٹی بہتری کی نمائندگی کرتا ہے:

**سیکیورٹی فوائد:**
1. **حسب ضرورت تصدیق کے خطرات ختم کرنا**: حسب ضرورت تصدیق کے نفاذ سے بچ کر خطرات کو کم کرنا  
2. **انٹرپرائز گریڈ سیکیورٹی**: مائیکروسافٹ انٹرا ID جیسے قائم شدہ شناخت فراہم کنندگان کے جدید سیکیورٹی فیچرز کا فائدہ اٹھانا  
3. **مرکزی شناخت کا انتظام**: صارف کے لائف سائیکل مینجمنٹ، رسائی کنٹرول، اور تعمیل آڈٹ کو آسان بنانا  
4. **کثیر عوامل کی تصدیق**: انٹرپرائز شناخت فراہم کنندگان سے MFA صلاحیتوں کا وراثت میں ملنا  
5. **مشروط رسائی کی پالیسیاں**: خطرے پر مبنی رسائی کنٹرولز اور موافقتی تصدیق سے فائدہ اٹھانا  

**عمل درآمد کے تقاضے:**
- **ٹوکن آڈینس کی تصدیق**: تمام ٹوکنز کی تصدیق کریں کہ وہ خاص طور پر MCP سرور کے لیے جاری کیے گئے ہیں  
- **جاری کنندہ کی تصدیق**: ٹوکن جاری کنندہ کی تصدیق کریں کہ وہ متوقع شناخت فراہم کنندہ سے میل کھاتا ہے  
- **دستخط کی تصدیق**: ٹوکن کی سالمیت کی کرپٹوگرافک تصدیق  
- **میعاد کی پابندی**: ٹوکن کی زندگی کی حدوں کی سختی سے پابندی  
- **دائرہ کار کی تصدیق**: اس بات کو یقینی بنائیں کہ ٹوکنز میں درخواست کردہ آپریشنز کے لیے مناسب اجازتیں موجود ہیں  

### **اجازت نامہ منطق کی سیکیورٹی**

**اہم کنٹرولز:**
- **جامع اجازت نامہ آڈٹس**: تمام اجازت نامہ فیصلہ پوائنٹس کے باقاعدہ سیکیورٹی جائزے  
- **محفوظ ڈیفالٹس**: جب اجازت نامہ منطق کوئی حتمی فیصلہ نہ کر سکے تو رسائی کو مسترد کریں  
- **اجازت کی حدود**: مختلف مراعات کی سطحوں اور وسائل تک رسائی کے درمیان واضح علیحدگی  
- **آڈٹ لاگنگ**: سیکیورٹی مانیٹرنگ کے لیے تمام اجازت نامہ فیصلوں کی مکمل لاگنگ  
- **باقاعدہ رسائی کے جائزے**: صارف کی اجازتوں اور مراعات کی تفویض کی وقتاً فوقتاً تصدیق  

## 2. **ٹوکن سیکیورٹی اور اینٹی پاس تھرو کنٹرولز**

### **ٹوکن پاس تھرو کی روک تھام**

**ٹوکن پاس تھرو کو MCP اجازت نامہ وضاحت نامے میں واضح طور پر ممنوع قرار دیا گیا ہے** کیونکہ اس میں اہم سیکیورٹی خطرات شامل ہیں:

**حل شدہ سیکیورٹی خطرات:**
- **کنٹرول کی خلاف ورزی**: اہم سیکیورٹی کنٹرولز جیسے کہ ریٹ لمیٹنگ، درخواست کی تصدیق، اور ٹریفک مانیٹرنگ کو نظرانداز کرنا  
- **جوابدہی کا خاتمہ**: کلائنٹ کی شناخت ناممکن بنانا، آڈٹ ٹریلز اور واقعہ کی تحقیقات کو خراب کرنا  
- **پراکسی پر مبنی ڈیٹا چوری**: بدنیتی پر مبنی عناصر کو غیر مجاز ڈیٹا تک رسائی کے لیے سرورز کو پراکسی کے طور پر استعمال کرنے کے قابل بنانا  
- **اعتماد کی حد کی خلاف ورزی**: ٹوکن کے ماخذ کے بارے میں ڈاؤن اسٹریم سروس کے اعتماد کے مفروضوں کو توڑنا  
- **لچکدار حرکت**: متعدد خدمات میں سمجھوتہ شدہ ٹوکنز کے ذریعے حملے کو وسیع کرنا  

**عمل درآمد کنٹرولز:**
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

### **محفوظ ٹوکن مینجمنٹ کے نمونے**

**بہترین طریقے:**
- **مختصر مدت کے ٹوکنز**: بار بار ٹوکن کی گردش کے ساتھ نمائش کی کھڑکی کو کم کرنا  
- **صرف ضرورت کے وقت اجراء**: مخصوص آپریشنز کے لیے صرف ضرورت کے وقت ٹوکن جاری کرنا  
- **محفوظ اسٹوریج**: ہارڈویئر سیکیورٹی ماڈیولز (HSMs) یا محفوظ کلید والٹس کا استعمال  
- **ٹوکن بائنڈنگ**: جہاں ممکن ہو، ٹوکنز کو مخصوص کلائنٹس، سیشنز، یا آپریشنز سے منسلک کرنا  
- **مانیٹرنگ اور الرٹنگ**: ٹوکن کے غلط استعمال یا غیر مجاز رسائی کے نمونوں کا حقیقی وقت میں پتہ لگانا  

## 3. **سیشن سیکیورٹی کنٹرولز**

### **سیشن ہائی جیکنگ کی روک تھام**

**حل شدہ حملے کے ویکٹرز:**
- **سیشن ہائی جیک پرامپٹ انجیکشن**: مشترکہ سیشن اسٹیٹ میں بدنیتی پر مبنی واقعات کا انجیکشن  
- **سیشن کی نقالی**: چوری شدہ سیشن IDs کا غیر مجاز استعمال کرکے تصدیق کو نظرانداز کرنا  
- **دوبارہ شروع ہونے والے اسٹریم حملے**: سرور سے بھیجے گئے ایونٹ کے دوبارہ شروع ہونے کا استحصال کرکے بدنیتی پر مبنی مواد کا انجیکشن  

**لازمی سیشن کنٹرولز:**
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

**ٹرانسپورٹ سیکیورٹی:**
- **HTTPS کا نفاذ**: تمام سیشن مواصلات TLS 1.3 پر  
- **محفوظ کوکی خصوصیات**: HttpOnly، Secure، SameSite=Strict  
- **سرٹیفکیٹ پننگ**: MITM حملوں کو روکنے کے لیے اہم کنکشنز کے لیے  

### **اسٹیٹ فل بمقابلہ اسٹیٹ لیس تحفظات**

**اسٹیٹ فل عمل درآمد کے لیے:**
- مشترکہ سیشن اسٹیٹ کو انجیکشن حملوں سے اضافی تحفظ کی ضرورت ہے  
- قطار پر مبنی سیشن مینجمنٹ کو سالمیت کی تصدیق کی ضرورت ہے  
- متعدد سرور انسٹینسز کو محفوظ سیشن اسٹیٹ ہم آہنگی کی ضرورت ہے  

**اسٹیٹ لیس عمل درآمد کے لیے:**
- JWT یا اسی طرح کے ٹوکن پر مبنی سیشن مینجمنٹ  
- سیشن اسٹیٹ کی سالمیت کی کرپٹوگرافک تصدیق  
- حملے کی سطح کو کم کرنا لیکن مضبوط ٹوکن کی تصدیق کی ضرورت ہے  

## 4. **AI سے متعلق سیکیورٹی کنٹرولز**

### **پرامپٹ انجیکشن دفاع**

**مائیکروسافٹ پرامپٹ شیلڈز انضمام:**
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

**عمل درآمد کنٹرولز:**
- **ان پٹ کی صفائی**: تمام صارف ان پٹس کی جامع تصدیق اور فلٹرنگ  
- **مواد کی حد کی تعریف**: سسٹم کی ہدایات اور صارف کے مواد کے درمیان واضح علیحدگی  
- **ہدایات کی درجہ بندی**: متضاد ہدایات کے لیے مناسب ترجیحی اصول  
- **آؤٹ پٹ مانیٹرنگ**: ممکنہ طور پر نقصان دہ یا چھیڑے گئے آؤٹ پٹس کا پتہ لگانا  

### **ٹول پوائزننگ کی روک تھام**

**ٹول سیکیورٹی فریم ورک:**
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

**متحرک ٹول مینجمنٹ:**
- **منظوری کے ورک فلو**: ٹول میں ترمیم کے لیے صارف کی واضح رضامندی  
- **واپسی کی صلاحیتیں**: پچھلے ٹول ورژنز پر واپس جانے کی صلاحیت  
- **تبدیلی کا آڈٹ**: ٹول کی تعریف میں ترمیمات کی مکمل تاریخ  
- **خطرے کی تشخیص**: ٹول کی سیکیورٹی پوزیشن کا خودکار جائزہ  

## 5. **کنفیوزڈ ڈپٹی حملے کی روک تھام**

### **OAuth پراکسی سیکیورٹی**

**حملے کی روک تھام کے کنٹرولز:**
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

**عمل درآمد کے تقاضے:**
- **صارف کی رضامندی کی تصدیق**: متحرک کلائنٹ رجسٹریشن کے لیے رضامندی اسکرینز کو کبھی نہ چھوڑیں  
- **ری ڈائریکٹ URI کی تصدیق**: ری ڈائریکٹ مقامات کی سخت وائٹ لسٹ پر مبنی تصدیق  
- **اجازت کوڈ کا تحفظ**: مختصر مدت کے کوڈز کے ساتھ سنگل یوز کا نفاذ  
- **کلائنٹ کی شناخت کی تصدیق**: کلائنٹ کی اسناد اور میٹا ڈیٹا کی مضبوط تصدیق  

## 6. **ٹول عمل درآمد کی سیکیورٹی**

### **سینڈ باکسنگ اور آئسولیشن**

**کنٹینر پر مبنی آئسولیشن:**
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

**پروسیس آئسولیشن:**
- **الگ پروسیس سیاق و سباق**: ہر ٹول عمل درآمد کو الگ پروسیس اسپیس میں  
- **بین العمل مواصلات**: توثیق کے ساتھ محفوظ IPC میکانزم  
- **پروسیس مانیٹرنگ**: رن ٹائم رویے کا تجزیہ اور بے ضابطگیوں کا پتہ لگانا  
- **وسائل کا نفاذ**: CPU، میموری، اور I/O آپریشنز پر سخت حدود  

### **کم از کم مراعات کا نفاذ**

**اجازت مینجمنٹ:**
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

## 7. **سپلائی چین سیکیورٹی کنٹرولز**

### **انحصار کی تصدیق**

**جامع جزو سیکیورٹی:**
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

### **مسلسل مانیٹرنگ**

**سپلائی چین خطرے کا پتہ لگانا:**
- **انحصار کی صحت کی نگرانی**: تمام انحصارات کا مسلسل جائزہ لینا  
- **خطرے کی ذہانت کا انضمام**: ابھرتے ہوئے سپلائی چین خطرات پر حقیقی وقت کی اپ ڈیٹس  
- **رویے کا تجزیہ**: بیرونی اجزاء میں غیر معمولی رویے کا پتہ لگانا  
- **خودکار ردعمل**: سمجھوتہ شدہ اجزاء کی فوری روک تھام  

## 8. **مانیٹرنگ اور پتہ لگانے کے کنٹرولز**

### **سیکیورٹی انفارمیشن اور ایونٹ مینجمنٹ (SIEM)**

**جامع لاگنگ حکمت عملی:**
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

### **حقیقی وقت میں خطرے کا پتہ لگانا**

**رویے کا تجزیہ:**
- **صارف رویے کا تجزیہ (UBA)**: غیر معمولی صارف رسائی کے نمونوں کا پتہ لگانا  
- **ادارے کے رویے کا تجزیہ (EBA)**: MCP سرور اور ٹول کے رویے کی نگرانی  
- **مشین لرننگ بے ضابطگی کا پتہ لگانا**: AI پر مبنی سیکیورٹی خطرات کی شناخت  
- **خطرے کی ذہانت کا ارتباط**: مشاہدہ شدہ سرگرمیوں کا معلوم حملے کے نمونوں سے موازنہ  

## 9. **واقعہ کا ردعمل اور بحالی**

### **خودکار ردعمل کی صلاحیتیں**

**فوری ردعمل کے اقدامات:**
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

### **فورینزک صلاحیتیں**

**تحقیقات کی معاونت:**
- **آڈٹ ٹریل کا تحفظ**: کرپٹوگرافک سالمیت کے ساتھ ناقابل تغیر لاگنگ  
- **شواہد کا مجموعہ**: متعلقہ سیکیورٹی نمونے خودکار طور پر جمع کرنا  
- **ٹائم لائن کی تعمیر نو**: سیکیورٹی واقعات کی طرف لے جانے والے واقعات کی تفصیلی ترتیب  
- **اثر کا جائزہ**: سمجھوتہ کی حد اور ڈیٹا کی نمائش کا جائزہ  

## **اہم سیکیورٹی آرکیٹیکچر کے اصول**

### **گہرائی میں دفاع**
- **متعدد سیکیورٹی پرتیں**: سیکیورٹی آرکیٹیکچر میں کسی ایک ناکامی کا امکان نہ ہو  
- **اضافی کنٹرولز**: اہم افعال کے لیے اوورلیپنگ سیکیورٹی اقدامات  
- **محفوظ میکانزم**: جب سسٹمز کو غلطیوں یا حملوں کا سامنا ہو تو محفوظ ڈیفالٹس  

### **زیرو ٹرسٹ کا نفاذ**
- **کبھی اعتماد نہ کریں، ہمیشہ تصدیق کریں**: تمام اداروں اور درخواستوں کی مسلسل تصدیق  
- **کم از کم مراعات کا اصول**: تمام اجزاء کے لیے کم سے کم رسائی کے حقوق  
- **مائیکرو سیگمنٹیشن**: باریک نیٹ ورک اور رسائی کنٹرولز  

### **مسلسل سیکیورٹی ارتقاء**
- **خطرے کے منظر نامے کی موافقت**: ابھرتے ہوئے خطرات کو حل کرنے کے لیے باقاعدہ اپ ڈیٹس  
- **سیکیورٹی کنٹرول کی تاثیر**: کنٹرولز کے جاری جائزے اور بہتری  
- **وضاحت نامے کی تعمیل**: بدلتے ہوئے MCP سیکیورٹی معیارات کے ساتھ ہم آہنگی  

---

## **عمل درآمد کے وسائل**

### **سرکاری MCP دستاویزات**
- [MCP وضاحت نامہ (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP سیکیورٹی بہترین طریقے](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP اجازت نامہ وضاحت نامہ](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **مائیکروسافٹ سیکیورٹی حل**
- [مائیکروسافٹ پرامپٹ شیلڈز](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure مواد کی حفاظت](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub ایڈوانسڈ سیکیورٹی](https://github.com/security/advanced-security)  
- [Azure کلید والٹ](https://learn.microsoft.com/azure/key-vault/)  

### **سیکیورٹی معیارات**
- [OAuth 2.0 سیکیورٹی بہترین طریقے (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP ٹاپ 10 برائے بڑے زبان ماڈلز](https://genai.owasp.org/)  
- [NIST سائبرسیکیورٹی فریم ورک](https://www.nist.gov/cyberframework)  

---

> **اہم**: یہ سیکیورٹی کنٹرولز موجودہ MCP وضاحت نامے (2025-06-18) کی عکاسی کرتے ہیں۔ ہمیشہ تازہ ترین [سرکاری دستاویزات](https://spec.modelcontextprotocol.io/) کے خلاف تصدیق کریں کیونکہ معیارات تیزی سے ترقی کرتے رہتے ہیں۔

**ڈس کلیمر**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کا استعمال کرتے ہوئے ترجمہ کی گئی ہے۔ ہم درستگی کے لیے پوری کوشش کرتے ہیں، لیکن براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستگی ہو سکتی ہیں۔ اصل دستاویز کو اس کی اصل زبان میں مستند ذریعہ سمجھا جانا چاہیے۔ اہم معلومات کے لیے، پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کے لیے ہم ذمہ دار نہیں ہیں۔