<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T15:40:06+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "mr"
}
-->
# MCP सुरक्षा नियंत्रण - ऑगस्ट 2025 अद्यतन

> **सध्याचा मानक**: हा दस्तऐवज [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) सुरक्षा आवश्यकता आणि अधिकृत [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) प्रतिबिंबित करतो.

मॉडेल कॉन्टेक्स्ट प्रोटोकॉल (MCP) ने पारंपरिक सॉफ्टवेअर सुरक्षा आणि AI-विशिष्ट धोके यांना संबोधित करणाऱ्या सुधारित सुरक्षा नियंत्रणांसह लक्षणीय प्रगती केली आहे. ऑगस्ट 2025 पर्यंत सुरक्षित MCP अंमलबजावणीसाठी व्यापक सुरक्षा नियंत्रण प्रदान करणारा हा दस्तऐवज आहे.

## **अनिवार्य सुरक्षा आवश्यकता**

### **MCP स्पेसिफिकेशनमधील महत्त्वाचे प्रतिबंध:**

> **मनाई**: MCP सर्व्हर **कधीही स्वीकारू नये** असे टोकन जे MCP सर्व्हरसाठी स्पष्टपणे जारी केलेले नाहीत  
>
> **प्रतिबंधित**: MCP सर्व्हरने **सत्रे प्रमाणीकरणासाठी वापरू नयेत**  
>
> **आवश्यक**: अधिकृतता अंमलात आणणारे MCP सर्व्हर **सर्व** येणाऱ्या विनंत्यांची पडताळणी करणे आवश्यक आहे  
>
> **अनिवार्य**: स्थिर क्लायंट IDs वापरणारे MCP प्रॉक्सी सर्व्हर **प्रत्येक डायनॅमिक नोंदणीकृत क्लायंटसाठी** वापरकर्त्याची संमती मिळवणे आवश्यक आहे  

---

## 1. **प्रमाणीकरण आणि अधिकृतता नियंत्रण**

### **बाह्य ओळख प्रदाता एकत्रीकरण**

**सध्याचा MCP मानक (2025-06-18)** MCP सर्व्हरना प्रमाणीकरण बाह्य ओळख प्रदात्यांकडे सोपवण्याची परवानगी देतो, ज्यामुळे सुरक्षा लक्षणीय सुधारते:

**सुरक्षा फायदे:**
1. **कस्टम प्रमाणीकरण जोखमींचा नाश**: कस्टम प्रमाणीकरण अंमलबजावणी टाळून असुरक्षितता पृष्ठभाग कमी करतो  
2. **एंटरप्राइझ-ग्रेड सुरक्षा**: Microsoft Entra ID सारख्या प्रगत सुरक्षा वैशिष्ट्यांसह स्थापित ओळख प्रदात्यांचा लाभ  
3. **केंद्रीकृत ओळख व्यवस्थापन**: वापरकर्ता जीवनचक्र व्यवस्थापन, प्रवेश नियंत्रण आणि अनुपालन ऑडिटिंग सुलभ करते  
4. **मल्टी-फॅक्टर प्रमाणीकरण**: एंटरप्राइझ ओळख प्रदात्यांकडून MFA क्षमता वारशाने मिळते  
5. **शर्ती आधारित प्रवेश धोरणे**: जोखीम-आधारित प्रवेश नियंत्रण आणि अडॅप्टिव्ह प्रमाणीकरणाचा लाभ  

**अंमलबजावणी आवश्यकता:**
- **टोकन प्रेक्षक पडताळणी**: सर्व टोकन MCP सर्व्हरसाठी स्पष्टपणे जारी केले असल्याची पडताळणी करा  
- **जारीकर्ता पडताळणी**: टोकन जारीकर्ता अपेक्षित ओळख प्रदात्याशी जुळतो याची पडताळणी करा  
- **स्वाक्षरी पडताळणी**: टोकन अखंडतेची क्रिप्टोग्राफिक पडताळणी  
- **कालबाह्यता अंमलबजावणी**: टोकन आयुष्य मर्यादेचे कठोर अंमलबजावणी  
- **व्याप्ती पडताळणी**: विनंती केलेल्या ऑपरेशन्ससाठी टोकनमध्ये योग्य परवानग्या आहेत याची खात्री करा  

### **अधिकृतता लॉजिक सुरक्षा**

**महत्त्वाचे नियंत्रण:**
- **संपूर्ण अधिकृतता ऑडिट्स**: सर्व अधिकृतता निर्णय बिंदूंच्या नियमित सुरक्षा पुनरावलोकने  
- **फेल-सेफ डीफॉल्ट्स**: अधिकृतता लॉजिक निश्चित निर्णय घेऊ शकत नसल्यास प्रवेश नाकारणे  
- **परवानगी सीमा**: वेगवेगळ्या विशेषाधिकार स्तर आणि संसाधन प्रवेशामध्ये स्पष्ट विभाजन  
- **ऑडिट लॉगिंग**: सुरक्षा निरीक्षणासाठी सर्व अधिकृतता निर्णयांचे संपूर्ण लॉगिंग  
- **नियमित प्रवेश पुनरावलोकने**: वापरकर्ता परवानग्या आणि विशेषाधिकार नियुक्त्यांची आवधिक पडताळणी  

## 2. **टोकन सुरक्षा आणि अँटी-पासथ्रू नियंत्रण**

### **टोकन पासथ्रू प्रतिबंध**

**MCP अधिकृतता स्पेसिफिकेशनमध्ये टोकन पासथ्रू स्पष्टपणे प्रतिबंधित आहे** कारण गंभीर सुरक्षा जोखमी:

**सुरक्षा जोखीम दूर केल्या:**
- **नियंत्रण टाळणे**: दर मर्यादित करणे, विनंती पडताळणी आणि ट्रॅफिक निरीक्षण यासारख्या आवश्यक सुरक्षा नियंत्रणांना बायपास करते  
- **जबाबदारीचा तुटवडा**: क्लायंट ओळख करणे अशक्य बनवते, ऑडिट ट्रेल्स आणि घटना तपास भ्रष्ट करते  
- **प्रॉक्सी-आधारित डेटा चोरी**: अनधिकृत डेटा प्रवेशासाठी सर्व्हरचा प्रॉक्सी म्हणून वापर करण्यास सक्षम करते  
- **विश्वास सीमा उल्लंघन**: टोकन मूळाबद्दल डाउनस्ट्रीम सेवांच्या विश्वास गृहीतकांना तोडते  
- **लॅटरल मूव्हमेंट**: एकाधिक सेवांमध्ये तडजोड केलेल्या टोकनमुळे व्यापक हल्ल्याचा विस्तार सक्षम होतो  

**अंमलबजावणी नियंत्रण:**
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

### **सुरक्षित टोकन व्यवस्थापन पद्धती**

**सर्वोत्तम पद्धती:**
- **अल्पकालीन टोकन**: वारंवार टोकन रोटेशनसह एक्सपोजर विंडो कमी करा  
- **जस्ट-इन-टाइम जारी**: विशिष्ट ऑपरेशन्ससाठी आवश्यक असताना टोकन जारी करा  
- **सुरक्षित संग्रहण**: हार्डवेअर सुरक्षा मॉड्यूल्स (HSMs) किंवा सुरक्षित की व्हॉल्ट्स वापरा  
- **टोकन बाइंडिंग**: शक्य असल्यास विशिष्ट क्लायंट, सत्र किंवा ऑपरेशन्ससाठी टोकन बाइंड करा  
- **निरीक्षण आणि सतर्कता**: टोकन गैरवापर किंवा अनधिकृत प्रवेश नमुन्यांचे रिअल-टाइम शोध  

## 3. **सत्र सुरक्षा नियंत्रण**

### **सत्र हायजॅकिंग प्रतिबंध**

**हल्ल्याचे मार्ग दूर केले:**
- **सत्र हायजॅक प्रॉम्प्ट इंजेक्शन**: सामायिक सत्र स्थितीत घातक घटना इंजेक्ट केल्या जातात  
- **सत्र व्यक्तिमत्व चोरी**: सत्र IDs चा अनधिकृत वापर करून प्रमाणीकरण बायपास करणे  
- **पुनरारंभ करण्यायोग्य प्रवाह हल्ले**: सर्व्हर-सेंड इव्हेंट पुनरारंभाचा गैरवापर करून घातक सामग्री इंजेक्शन  

**अनिवार्य सत्र नियंत्रण:**
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

**वाहतूक सुरक्षा:**
- **HTTPS अंमलबजावणी**: TLS 1.3 वर सर्व सत्र संप्रेषण  
- **सुरक्षित कुकी गुणधर्म**: HttpOnly, Secure, SameSite=Strict  
- **सर्टिफिकेट पिनिंग**: MITM हल्ले टाळण्यासाठी महत्त्वाच्या कनेक्शनसाठी  

### **स्टेटफुल विरुद्ध स्टेटलेस विचार**

**स्टेटफुल अंमलबजावणीसाठी:**
- सामायिक सत्र स्थिती इंजेक्शन हल्ल्यांपासून अतिरिक्त संरक्षण आवश्यक आहे  
- सत्र व्यवस्थापनासाठी रांगेवर आधारित अंमलबजावणीस अखंडता पडताळणी आवश्यक आहे  
- एकाधिक सर्व्हर उदाहरणांसाठी सुरक्षित सत्र स्थिती समक्रमण आवश्यक आहे  

**स्टेटलेस अंमलबजावणीसाठी:**
- JWT किंवा तत्सम टोकन-आधारित सत्र व्यवस्थापन  
- सत्र स्थिती अखंडतेची क्रिप्टोग्राफिक पडताळणी  
- कमी हल्ल्याचा पृष्ठभाग परंतु मजबूत टोकन पडताळणी आवश्यक आहे  

## 4. **AI-विशिष्ट सुरक्षा नियंत्रण**

### **प्रॉम्प्ट इंजेक्शन संरक्षण**

**Microsoft Prompt Shields एकत्रीकरण:**
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

**अंमलबजावणी नियंत्रण:**
- **इनपुट स्वच्छता**: सर्व वापरकर्ता इनपुटची व्यापक पडताळणी आणि फिल्टरिंग  
- **सामग्री सीमा परिभाषा**: प्रणाली सूचनांमध्ये आणि वापरकर्ता सामग्रीमध्ये स्पष्ट विभाजन  
- **सूचना श्रेणी**: विरोधी सूचनांसाठी योग्य प्राधान्य नियम  
- **आउटपुट निरीक्षण**: संभाव्य घातक किंवा फेरफार केलेल्या आउटपुट्सचा शोध  

### **टूल विषबाधा प्रतिबंध**

**टूल सुरक्षा फ्रेमवर्क:**
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

**डायनॅमिक टूल व्यवस्थापन:**
- **मंजुरी कार्यप्रवाह**: टूल बदलांसाठी स्पष्ट वापरकर्ता संमती  
- **रोलबॅक क्षमता**: मागील टूल आवृत्त्यांवर परत जाण्याची क्षमता  
- **बदल ऑडिटिंग**: टूल परिभाषा बदलांचा संपूर्ण इतिहास  
- **जोखीम मूल्यांकन**: टूल सुरक्षा स्थितीचे स्वयंचलित मूल्यांकन  

## 5. **गोंधळलेल्या डेप्युटी हल्ल्याचा प्रतिबंध**

### **OAuth प्रॉक्सी सुरक्षा**

**हल्ला प्रतिबंध नियंत्रण:**
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

**अंमलबजावणी आवश्यकता:**
- **वापरकर्ता संमती पडताळणी**: डायनॅमिक क्लायंट नोंदणीसाठी संमती स्क्रीन कधीही वगळू नका  
- **रीडायरेक्ट URI पडताळणी**: रीडायरेक्ट गंतव्यस्थानांची कठोर श्वेतसूची-आधारित पडताळणी  
- **अधिकृतता कोड संरक्षण**: एकल-वापर अंमलबजावणीसह अल्पकालीन कोड  
- **क्लायंट ओळख पडताळणी**: क्लायंट क्रेडेन्शियल्स आणि मेटाडेटाची मजबूत पडताळणी  

## 6. **टूल अंमलबजावणी सुरक्षा**

### **सँडबॉक्सिंग आणि वेगळेपणा**

**कंटेनर-आधारित वेगळेपणा:**
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

**प्रक्रिया वेगळेपणा:**
- **स्वतंत्र प्रक्रिया संदर्भ**: प्रत्येक टूल अंमलबजावणी स्वतंत्र प्रक्रिया जागेत  
- **इंटर-प्रोसेस कम्युनिकेशन**: पडताळणीसह सुरक्षित IPC यंत्रणा  
- **प्रक्रिया निरीक्षण**: रनटाइम वर्तन विश्लेषण आणि विसंगती शोध  
- **संसाधन अंमलबजावणी**: CPU, मेमरी आणि I/O ऑपरेशन्सवर कठोर मर्यादा  

### **किमान विशेषाधिकार अंमलबजावणी**

**परवानगी व्यवस्थापन:**
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

## 7. **पुरवठा साखळी सुरक्षा नियंत्रण**

### **अवलंबन पडताळणी**

**संपूर्ण घटक सुरक्षा:**
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

### **सतत निरीक्षण**

**पुरवठा साखळी धोका शोध:**
- **अवलंबन आरोग्य निरीक्षण**: सर्व अवलंबनांमध्ये सुरक्षा समस्यांसाठी सतत मूल्यांकन  
- **धोका बुद्धिमत्ता एकत्रीकरण**: उदयोन्मुख पुरवठा साखळी धोके यावर रिअल-टाइम अद्यतने  
- **वर्तन विश्लेषण**: बाह्य घटकांमध्ये असामान्य वर्तनाचा शोध  
- **स्वयंचलित प्रतिसाद**: तडजोड केलेल्या घटकांचे त्वरित नियंत्रण  

## 8. **निरीक्षण आणि शोध नियंत्रण**

### **सुरक्षा माहिती आणि घटना व्यवस्थापन (SIEM)**

**संपूर्ण लॉगिंग धोरण:**
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

### **रिअल-टाइम धोका शोध**

**वर्तन विश्लेषण:**
- **वापरकर्ता वर्तन विश्लेषण (UBA)**: असामान्य वापरकर्ता प्रवेश नमुन्यांचा शोध  
- **घटक वर्तन विश्लेषण (EBA)**: MCP सर्व्हर आणि टूल वर्तनाचे निरीक्षण  
- **मशीन लर्निंग विसंगती शोध**: सुरक्षा धोके ओळखण्यासाठी AI-सक्षम तंत्रज्ञान  
- **धोका बुद्धिमत्ता संबंधीकरण**: ज्ञात हल्ल्याच्या नमुन्यांशी निरीक्षित क्रियाकलाप जुळवणे  

## 9. **घटना प्रतिसाद आणि पुनर्प्राप्ती**

### **स्वयंचलित प्रतिसाद क्षमता**

**तत्काळ प्रतिसाद क्रिया:**
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

### **फॉरेन्सिक क्षमता**

**तपास समर्थन:**
- **ऑडिट ट्रेल संरक्षण**: क्रिप्टोग्राफिक अखंडतेसह अपरिवर्तनीय लॉगिंग  
- **पुरावा संग्रह**: संबंधित सुरक्षा पुरावे स्वयंचलितपणे गोळा करणे  
- **कालक्रम पुनर्रचना**: सुरक्षा घटनांपर्यंत पोहोचणाऱ्या घटनांचा तपशीलवार क्रम  
- **प्रभाव मूल्यांकन**: तडजोडाची व्याप्ती आणि डेटा एक्सपोजरचे मूल्यांकन  

## **महत्त्वाचे सुरक्षा आर्किटेक्चर तत्त्व**

### **सुरक्षेची खोलीत रचना**
- **एकाधिक सुरक्षा स्तर**: सुरक्षा आर्किटेक्चरमध्ये एकही अपयशाचा बिंदू नाही  
- **अतिरिक्त नियंत्रण**: महत्त्वाच्या कार्यांसाठी ओव्हरलॅपिंग सुरक्षा उपाय  
- **फेल-सेफ यंत्रणा**: प्रणाली त्रुटी किंवा हल्ल्यांना सामोरे जाताना सुरक्षित डीफॉल्ट्स  

### **झिरो ट्रस्ट अंमलबजावणी**
- **कधीही विश्वास ठेवू नका, नेहमी पडताळणी करा**: सर्व घटक आणि विनंत्यांची सतत पडताळणी  
- **किमान विशेषाधिकार तत्त्व**: सर्व घटकांसाठी किमान प्रवेश अधिकार  
- **मायक्रो-सेगमेंटेशन**: सूक्ष्म नेटवर्क आणि प्रवेश नियंत्रण  

### **सतत सुरक्षा उत्क्रांती**
- **धोका लँडस्केप अनुकूलन**: उदयोन्मुख धोके दूर करण्यासाठी नियमित अद्यतने  
- **सुरक्षा नियंत्रण प्रभावीता**: नियंत्रणांचे सतत मूल्यांकन आणि सुधारणा  
- **स्पेसिफिकेशन अनुपालन**: विकसित MCP सुरक्षा मानकांशी संरेखन  

---

## **अंमलबजावणी संसाधने**

### **अधिकृत MCP दस्तऐवज**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft सुरक्षा उपाय**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **सुरक्षा मानक**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **महत्त्वाचे**: हे सुरक्षा नियंत्रण सध्याच्या MCP स्पेसिफिकेशन (2025-06-18) प्रतिबिंबित करतात. मानक जलद गतीने विकसित होत असल्याने नेहमी [अधिकृत दस्तऐवज](https://spec.modelcontextprotocol.io/) तपासा.

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी कृपया लक्षात ठेवा की स्वयंचलित भाषांतरे त्रुटी किंवा अचूकतेच्या अभावाने युक्त असू शकतात. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून उद्भवलेल्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.