<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T16:54:12+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "he"
}
-->
# בקרות אבטחה MCP - עדכון אוגוסט 2025

> **תקן נוכחי**: מסמך זה משקף את דרישות האבטחה של [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) ואת [הנחיות האבטחה הטובות ביותר של MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

פרוטוקול Model Context Protocol (MCP) התפתח משמעותית עם בקרות אבטחה משופרות המתמודדות עם איומים מסורתיים בתוכנה ואיומים ספציפיים ל-AI. מסמך זה מספק בקרות אבטחה מקיפות ליישומי MCP מאובטחים נכון לאוגוסט 2025.

## **דרישות אבטחה חובה**

### **איסורים קריטיים מתוך מפרט MCP:**

> **אסור**: שרתי MCP **לא יקבלו** אסימונים שלא הונפקו במפורש עבור שרת MCP  
>
> **אסור**: שרתי MCP **לא ישתמשו** במפגשים לצורך אימות  
>
> **חובה**: שרתי MCP המיישמים הרשאות **חייבים** לאמת את כל הבקשות הנכנסות  
>
> **חובה**: שרתי פרוקסי MCP המשתמשים במזהי לקוח סטטיים **חייבים** לקבל את הסכמת המשתמש עבור כל לקוח שנרשם באופן דינמי  

---

## 1. **בקרות אימות והרשאה**

### **שילוב ספקי זהות חיצוניים**

**תקן MCP נוכחי (2025-06-18)** מאפשר לשרתי MCP להאציל את תהליך האימות לספקי זהות חיצוניים, מה שמייצג שיפור משמעותי באבטחה:

**יתרונות אבטחה:**
1. **מניעת סיכוני אימות מותאם אישית**: מצמצם את שטח הפגיעות על ידי הימנעות מיישומי אימות מותאמים אישית  
2. **אבטחה ברמה ארגונית**: מנצל ספקי זהות מבוססים כמו Microsoft Entra ID עם תכונות אבטחה מתקדמות  
3. **ניהול זהות מרכזי**: מפשט את ניהול מחזור חיי המשתמש, בקרת גישה וביקורת תאימות  
4. **אימות רב-שלבי**: יורש יכולות MFA מספקי זהות ארגוניים  
5. **מדיניות גישה מותנית**: נהנה מבקרות גישה מבוססות סיכון ואימות אדפטיבי  

**דרישות יישום:**
- **אימות קהל האסימונים**: יש לוודא שכל האסימונים הונפקו במפורש עבור שרת MCP  
- **אימות מנפיק**: יש לוודא שמנפיק האסימונים תואם לספק הזהות הצפוי  
- **אימות חתימה**: אימות קריפטוגרפי של שלמות האסימונים  
- **אכיפת תוקף**: אכיפה קפדנית של מגבלות זמן חיים של אסימונים  
- **אימות תחום**: יש לוודא שהאסימונים מכילים הרשאות מתאימות לפעולות המבוקשות  

### **אבטחת לוגיקת הרשאה**

**בקרות קריטיות:**
- **ביקורות הרשאה מקיפות**: סקירות אבטחה קבועות של כל נקודות קבלת ההחלטות בהרשאה  
- **ברירות מחדל בטוחות**: מניעת גישה כאשר לוגיקת ההרשאה אינה יכולה לקבל החלטה חד משמעית  
- **גבולות הרשאה**: הפרדה ברורה בין רמות הרשאה שונות וגישה למשאבים  
- **רישום ביקורת**: רישום מלא של כל החלטות ההרשאה לצורך ניטור אבטחה  
- **סקירות גישה קבועות**: אימות תקופתי של הרשאות משתמש והקצאות הרשאה  

## 2. **אבטחת אסימונים ובקרות נגד העברת אסימונים**

### **מניעת העברת אסימונים**

**העברת אסימונים אסורה במפורש** במפרט ההרשאה של MCP בשל סיכוני אבטחה קריטיים:

**סיכוני אבטחה מטופלים:**
- **עקיפת בקרות**: עוקף בקרות אבטחה חיוניות כמו הגבלת קצב, אימות בקשות וניטור תעבורה  
- **שיבוש אחריות**: הופך זיהוי לקוח לבלתי אפשרי, פוגע בנתיבי ביקורת ובחקירת אירועים  
- **הוצאת נתונים דרך פרוקסי**: מאפשר לשחקנים זדוניים להשתמש בשרתים כפרוקסי לגישה לא מורשית לנתונים  
- **הפרת גבולות אמון**: מפר את הנחות האמון של שירותים במורד הזרם לגבי מקורות האסימונים  
- **תנועה רוחבית**: אסימונים שנפגעו בין שירותים מרובים מאפשרים הרחבת התקפה רחבה יותר  

**בקרות יישום:**
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

### **דפוסי ניהול אסימונים מאובטחים**

**הנחיות מומלצות:**
- **אסימונים קצרי טווח**: צמצום חלון החשיפה עם סיבוב אסימונים תכוף  
- **הנפקה לפי צורך**: הנפקת אסימונים רק כאשר יש צורך בפעולות ספציפיות  
- **אחסון מאובטח**: שימוש במודולי אבטחת חומרה (HSMs) או כספות מפתחות מאובטחות  
- **קישור אסימונים**: קישור אסימונים ללקוחות, מפגשים או פעולות ספציפיות ככל האפשר  
- **ניטור והתראה**: זיהוי בזמן אמת של שימוש לרעה באסימונים או דפוסי גישה לא מורשים  

## 3. **בקרות אבטחת מפגשים**

### **מניעת חטיפת מפגשים**

**וקטורי התקפה מטופלים:**
- **הזרקת אירועים לחטיפת מפגשים**: אירועים זדוניים המוזרקים למצב מפגש משותף  
- **התחזות מפגשים**: שימוש לא מורשה במזהי מפגש גנובים לעקיפת אימות  
- **התקפות זרם ניתנות לחידוש**: ניצול חידוש אירועים שנשלחו על ידי השרת להזרקת תוכן זדוני  

**בקרות מפגש חובה:**
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

**אבטחת תעבורה:**
- **אכיפת HTTPS**: כל תקשורת המפגשים מעל TLS 1.3  
- **תכונות עוגיות מאובטחות**: HttpOnly, Secure, SameSite=Strict  
- **הצמדת תעודות**: עבור חיבורים קריטיים למניעת התקפות MITM  

### **שיקולים למצב סטטי מול מצב חסר מצב**

**עבור יישומים סטטיים:**
- מצב מפגש משותף דורש הגנה נוספת מפני התקפות הזרקה  
- ניהול מפגשים מבוסס תורים דורש אימות שלמות  
- מספר מופעי שרת דורשים סנכרון מצב מפגש מאובטח  

**עבור יישומים חסרי מצב:**
- ניהול מפגשים מבוסס אסימונים כמו JWT  
- אימות קריפטוגרפי של שלמות מצב המפגש  
- שטח התקפה מצומצם אך דורש אימות אסימונים חזק  

## 4. **בקרות אבטחה ספציפיות ל-AI**

### **הגנה מפני הזרקת הנחיות**

**שילוב Microsoft Prompt Shields:**
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

**בקרות יישום:**
- **טיהור קלט**: אימות וסינון מקיף של כל קלטי המשתמש  
- **הגדרת גבולות תוכן**: הפרדה ברורה בין הוראות מערכת לתוכן משתמש  
- **היררכיית הוראות**: כללי קדימות נכונים להוראות סותרות  
- **ניטור פלט**: זיהוי פלטים שעלולים להיות מזיקים או מניפולטיביים  

### **מניעת הרעלת כלים**

**מסגרת אבטחת כלים:**
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

**ניהול כלים דינמי:**
- **תהליכי אישור**: הסכמה מפורשת של משתמש לשינויים בכלים  
- **יכולות שחזור**: אפשרות לחזור לגרסאות קודמות של כלים  
- **ביקורת שינויים**: היסטוריה מלאה של שינויים בהגדרות כלים  
- **הערכת סיכונים**: הערכה אוטומטית של מצב האבטחה של כלים  

## 5. **מניעת התקפות סגן מבולבל**

### **אבטחת פרוקסי OAuth**

**בקרות מניעת התקפה:**
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

**דרישות יישום:**
- **אימות הסכמת משתמש**: לעולם לא לדלג על מסכי הסכמה לרישום לקוח דינמי  
- **אימות URI להפניה**: אימות קפדני מבוסס רשימת לבנה של יעדי הפניה  
- **הגנת קוד הרשאה**: קודים קצרי טווח עם אכיפת שימוש חד-פעמי  
- **אימות זהות לקוח**: אימות חזק של אישורי לקוח ומטא-נתונים  

## 6. **אבטחת ביצוע כלים**

### **ארגז חול ובידוד**

**בידוד מבוסס מכולות:**
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

**בידוד תהליכים:**
- **הקשרי תהליך נפרדים**: כל ביצוע כלי במרחב תהליך מבודד  
- **תקשורת בין-תהליכית**: מנגנוני IPC מאובטחים עם אימות  
- **ניטור תהליכים**: ניתוח התנהגות בזמן ריצה וזיהוי חריגות  
- **אכיפת משאבים**: מגבלות קשיחות על CPU, זיכרון ופעולות I/O  

### **יישום הרשאות מינימליות**

**ניהול הרשאות:**
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

## 7. **בקרות אבטחת שרשרת אספקה**

### **אימות תלות**

**אבטחת רכיבים מקיפה:**
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

### **ניטור מתמשך**

**זיהוי איומים בשרשרת אספקה:**
- **ניטור בריאות תלות**: הערכה מתמשכת של כל התלויות לבעיות אבטחה  
- **שילוב מודיעין איומים**: עדכונים בזמן אמת על איומים מתפתחים בשרשרת אספקה  
- **ניתוח התנהגותי**: זיהוי התנהגות חריגה ברכיבים חיצוניים  
- **תגובה אוטומטית**: הכלה מיידית של רכיבים שנפגעו  

## 8. **בקרות ניטור וזיהוי**

### **ניהול מידע ואירועי אבטחה (SIEM)**

**אסטרטגיית רישום מקיפה:**
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

### **זיהוי איומים בזמן אמת**

**ניתוח התנהגותי:**
- **ניתוח התנהגות משתמשים (UBA)**: זיהוי דפוסי גישה חריגים של משתמשים  
- **ניתוח התנהגות ישויות (EBA)**: ניטור התנהגות שרת MCP וכלים  
- **זיהוי חריגות מבוסס AI**: זיהוי איומי אבטחה באמצעות AI  
- **התאמת מודיעין איומים**: התאמת פעילויות נצפות לדפוסי התקפה ידועים  

## 9. **תגובה והתאוששות מאירועים**

### **יכולות תגובה אוטומטית**

**פעולות תגובה מיידיות:**
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

### **יכולות פורנזיות**

**תמיכה בחקירה:**
- **שימור נתיבי ביקורת**: רישום בלתי ניתן לשינוי עם שלמות קריפטוגרפית  
- **איסוף ראיות**: איסוף אוטומטי של פריטי אבטחה רלוונטיים  
- **שחזור ציר זמן**: רצף מפורט של אירועים שהובילו לאירועי אבטחה  
- **הערכת השפעה**: הערכת היקף הפגיעה וחשיפת נתונים  

## **עקרונות מפתח בארכיטקטורת אבטחה**

### **הגנה בשכבות**
- **שכבות אבטחה מרובות**: ללא נקודת כשל יחידה בארכיטקטורת האבטחה  
- **בקרות חופפות**: אמצעי אבטחה חופפים לפונקציות קריטיות  
- **מנגנוני ברירת מחדל בטוחים**: ברירות מחדל מאובטחות כאשר מערכות נתקלות בשגיאות או התקפות  

### **יישום אפס אמון**
- **לעולם לא לסמוך, תמיד לאמת**: אימות מתמשך של כל ישויות ובקשות  
- **עקרון ההרשאה המינימלית**: זכויות גישה מינימליות לכל הרכיבים  
- **מיקרו-סגמנטציה**: בקרות רשת וגישה גרנולריות  

### **התפתחות אבטחה מתמשכת**
- **התאמה לנוף איומים**: עדכונים קבועים להתמודדות עם איומים מתפתחים  
- **יעילות בקרות אבטחה**: הערכה ושיפור מתמשכים של בקרות  
- **עמידה במפרט**: התאמה לסטנדרטים אבטחה מתפתחים של MCP  

---

## **משאבי יישום**

### **תיעוד רשמי של MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **פתרונות אבטחה של Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **סטנדרטים אבטחה**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **חשוב**: בקרות אבטחה אלו משקפות את מפרט MCP הנוכחי (2025-06-18). תמיד יש לוודא מול [התיעוד הרשמי](https://spec.modelcontextprotocol.io/) מכיוון שהסטנדרטים ממשיכים להתפתח במהירות.  

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש להיות מודעים לכך שתרגומים אוטומטיים עשויים להכיל שגיאות או אי דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור סמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. איננו נושאים באחריות לאי הבנות או לפרשנויות שגויות הנובעות משימוש בתרגום זה.