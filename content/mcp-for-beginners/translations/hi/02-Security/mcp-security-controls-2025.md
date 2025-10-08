<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T12:35:05+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "hi"
}
-->
# एमसीपी सुरक्षा नियंत्रण - अगस्त 2025 अपडेट

> **वर्तमान मानक**: यह दस्तावेज़ [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) की सुरक्षा आवश्यकताओं और आधिकारिक [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) को दर्शाता है।

मॉडल कॉन्टेक्स्ट प्रोटोकॉल (MCP) ने पारंपरिक सॉफ़्टवेयर सुरक्षा और एआई-विशिष्ट खतरों को संबोधित करते हुए उन्नत सुरक्षा नियंत्रणों के साथ महत्वपूर्ण प्रगति की है। यह दस्तावेज़ अगस्त 2025 तक सुरक्षित MCP कार्यान्वयन के लिए व्यापक सुरक्षा नियंत्रण प्रदान करता है।

## **अनिवार्य सुरक्षा आवश्यकताएँ**

### **MCP विनिर्देश से महत्वपूर्ण निषेध:**

> **निषिद्ध**: MCP सर्वर **किसी भी टोकन को स्वीकार नहीं कर सकते** जो MCP सर्वर के लिए स्पष्ट रूप से जारी नहीं किया गया हो  
>
> **प्रतिबंधित**: MCP सर्वर **सत्रों का उपयोग प्रमाणीकरण के लिए नहीं कर सकते**  
>
> **आवश्यक**: प्राधिकरण लागू करने वाले MCP सर्वर **सभी इनबाउंड अनुरोधों को सत्यापित करना चाहिए**  
>
> **अनिवार्य**: स्थिर क्लाइंट आईडी का उपयोग करने वाले MCP प्रॉक्सी सर्वर को प्रत्येक गतिशील रूप से पंजीकृत क्लाइंट के लिए उपयोगकर्ता की सहमति प्राप्त करनी चाहिए  

---

## 1. **प्रमाणीकरण और प्राधिकरण नियंत्रण**

### **बाहरी पहचान प्रदाता एकीकरण**

**वर्तमान MCP मानक (2025-06-18)** MCP सर्वरों को प्रमाणीकरण को बाहरी पहचान प्रदाताओं को सौंपने की अनुमति देता है, जो एक महत्वपूर्ण सुरक्षा सुधार का प्रतिनिधित्व करता है:

**सुरक्षा लाभ:**
1. **कस्टम प्रमाणीकरण जोखिम समाप्त करता है**: कस्टम प्रमाणीकरण कार्यान्वयन से बचकर भेद्यता को कम करता है  
2. **एंटरप्राइज़-ग्रेड सुरक्षा**: Microsoft Entra ID जैसे स्थापित पहचान प्रदाताओं की उन्नत सुरक्षा सुविधाओं का लाभ उठाता है  
3. **केंद्रीकृत पहचान प्रबंधन**: उपयोगकर्ता जीवनचक्र प्रबंधन, एक्सेस नियंत्रण और अनुपालन ऑडिटिंग को सरल बनाता है  
4. **मल्टी-फैक्टर प्रमाणीकरण**: एंटरप्राइज़ पहचान प्रदाताओं से एमएफए क्षमताओं को अपनाता है  
5. **शर्त आधारित एक्सेस नीतियाँ**: जोखिम-आधारित एक्सेस नियंत्रण और अनुकूली प्रमाणीकरण का लाभ उठाता है  

**कार्यान्वयन आवश्यकताएँ:**
- **टोकन ऑडियंस सत्यापन**: सुनिश्चित करें कि सभी टोकन MCP सर्वर के लिए स्पष्ट रूप से जारी किए गए हैं  
- **जारीकर्ता सत्यापन**: सत्यापित करें कि टोकन जारीकर्ता अपेक्षित पहचान प्रदाता से मेल खाता है  
- **हस्ताक्षर सत्यापन**: टोकन की अखंडता का क्रिप्टोग्राफिक सत्यापन  
- **समाप्ति प्रवर्तन**: टोकन की समय सीमा सख्ती से लागू करें  
- **स्कोप सत्यापन**: सुनिश्चित करें कि टोकन में अनुरोधित संचालन के लिए उपयुक्त अनुमतियाँ हैं  

### **प्राधिकरण लॉजिक सुरक्षा**

**महत्वपूर्ण नियंत्रण:**
- **व्यापक प्राधिकरण ऑडिट**: सभी प्राधिकरण निर्णय बिंदुओं की नियमित सुरक्षा समीक्षा  
- **फेल-सेफ डिफॉल्ट्स**: जब प्राधिकरण लॉजिक कोई निश्चित निर्णय नहीं ले सकता, तो एक्सेस अस्वीकार करें  
- **अनुमति सीमाएँ**: विभिन्न विशेषाधिकार स्तरों और संसाधन एक्सेस के बीच स्पष्ट विभाजन  
- **ऑडिट लॉगिंग**: सुरक्षा निगरानी के लिए सभी प्राधिकरण निर्णयों का पूर्ण लॉगिंग  
- **नियमित एक्सेस समीक्षा**: उपयोगकर्ता अनुमतियों और विशेषाधिकार असाइनमेंट की आवधिक मान्यता  

## 2. **टोकन सुरक्षा और एंटी-पासथ्रू नियंत्रण**

### **टोकन पासथ्रू रोकथाम**

**MCP प्राधिकरण विनिर्देश में टोकन पासथ्रू स्पष्ट रूप से निषिद्ध है** क्योंकि यह गंभीर सुरक्षा जोखिम पैदा करता है:

**सुरक्षा जोखिमों का समाधान:**
- **नियंत्रण चूक**: दर सीमित करने, अनुरोध सत्यापन और ट्रैफ़िक निगरानी जैसे आवश्यक सुरक्षा नियंत्रणों को दरकिनार करता है  
- **जवाबदेही टूटना**: क्लाइंट पहचान को असंभव बनाता है, ऑडिट ट्रेल और घटना जांच को दूषित करता है  
- **प्रॉक्सी-आधारित डेटा चोरी**: अनधिकृत डेटा एक्सेस के लिए सर्वरों को प्रॉक्सी के रूप में उपयोग करने में दुर्भावनापूर्ण अभिनेताओं को सक्षम बनाता है  
- **विश्वास सीमा उल्लंघन**: टोकन मूल के बारे में डाउनस्ट्रीम सेवा विश्वास मान्यताओं को तोड़ता है  
- **लैटरल मूवमेंट**: कई सेवाओं में समझौता किए गए टोकन व्यापक हमले के विस्तार को सक्षम करते हैं  

**कार्यान्वयन नियंत्रण:**
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

### **सुरक्षित टोकन प्रबंधन पैटर्न**

**सर्वोत्तम प्रथाएँ:**
- **अल्पकालिक टोकन**: बार-बार टोकन रोटेशन के साथ एक्सपोज़र विंडो को कम करें  
- **जस्ट-इन-टाइम जारी करना**: केवल विशिष्ट संचालन के लिए आवश्यक होने पर टोकन जारी करें  
- **सुरक्षित भंडारण**: हार्डवेयर सुरक्षा मॉड्यूल (HSM) या सुरक्षित कुंजी वॉल्ट का उपयोग करें  
- **टोकन बाइंडिंग**: जहां संभव हो, टोकन को विशिष्ट क्लाइंट, सत्र या संचालन से जोड़ें  
- **निगरानी और अलर्टिंग**: टोकन के दुरुपयोग या अनधिकृत एक्सेस पैटर्न का वास्तविक समय में पता लगाना  

## 3. **सत्र सुरक्षा नियंत्रण**

### **सत्र अपहरण रोकथाम**

**हमले के वेक्टर का समाधान:**
- **सत्र अपहरण प्रॉम्प्ट इंजेक्शन**: साझा सत्र स्थिति में दुर्भावनापूर्ण घटनाओं को इंजेक्ट करना  
- **सत्र प्रतिरूपण**: प्रमाणीकरण को दरकिनार करने के लिए चोरी किए गए सत्र आईडी का अनधिकृत उपयोग  
- **पुन: प्रारंभ करने योग्य स्ट्रीम हमले**: दुर्भावनापूर्ण सामग्री इंजेक्शन के लिए सर्वर-भेजी गई घटना पुन: प्रारंभ का शोषण  

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

**परिवहन सुरक्षा:**
- **HTTPS प्रवर्तन**: TLS 1.3 पर सभी सत्र संचार  
- **सुरक्षित कुकी विशेषताएँ**: HttpOnly, Secure, SameSite=Strict  
- **सर्टिफिकेट पिनिंग**: MITM हमलों को रोकने के लिए महत्वपूर्ण कनेक्शनों के लिए  

### **स्टेटफुल बनाम स्टेटलेस विचार**

**स्टेटफुल कार्यान्वयन के लिए:**
- साझा सत्र स्थिति को इंजेक्शन हमलों से अतिरिक्त सुरक्षा की आवश्यकता होती है  
- कतार-आधारित सत्र प्रबंधन को अखंडता सत्यापन की आवश्यकता होती है  
- कई सर्वर उदाहरणों को सुरक्षित सत्र स्थिति सिंक्रनाइज़ेशन की आवश्यकता होती है  

**स्टेटलेस कार्यान्वयन के लिए:**
- JWT या समान टोकन-आधारित सत्र प्रबंधन  
- सत्र स्थिति अखंडता का क्रिप्टोग्राफिक सत्यापन  
- कम हमला सतह लेकिन मजबूत टोकन सत्यापन की आवश्यकता होती है  

## 4. **एआई-विशिष्ट सुरक्षा नियंत्रण**

### **प्रॉम्प्ट इंजेक्शन रक्षा**

**Microsoft Prompt Shields एकीकरण:**
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

**कार्यान्वयन नियंत्रण:**
- **इनपुट स्वच्छता**: सभी उपयोगकर्ता इनपुट की व्यापक मान्यता और फ़िल्टरिंग  
- **सामग्री सीमा परिभाषा**: सिस्टम निर्देशों और उपयोगकर्ता सामग्री के बीच स्पष्ट विभाजन  
- **निर्देश पदानुक्रम**: परस्पर विरोधी निर्देशों के लिए उचित प्राथमिकता नियम  
- **आउटपुट निगरानी**: संभावित रूप से हानिकारक या हेरफेर किए गए आउटपुट का पता लगाना  

### **टूल पॉइज़निंग रोकथाम**

**टूल सुरक्षा ढांचा:**
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

**गतिशील टूल प्रबंधन:**
- **अनुमोदन वर्कफ़्लो**: टूल संशोधनों के लिए उपयोगकर्ता की स्पष्ट सहमति  
- **रोलबैक क्षमताएँ**: पिछले टूल संस्करणों पर वापस जाने की क्षमता  
- **परिवर्तन ऑडिटिंग**: टूल परिभाषा संशोधनों का पूरा इतिहास  
- **जोखिम मूल्यांकन**: टूल सुरक्षा स्थिति का स्वचालित मूल्यांकन  

## 5. **कन्फ्यूज्ड डिप्टी अटैक रोकथाम**

### **OAuth प्रॉक्सी सुरक्षा**

**हमले की रोकथाम नियंत्रण:**
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

**कार्यान्वयन आवश्यकताएँ:**
- **उपयोगकर्ता सहमति सत्यापन**: गतिशील क्लाइंट पंजीकरण के लिए सहमति स्क्रीन को कभी न छोड़ें  
- **रीडायरेक्ट URI सत्यापन**: रीडायरेक्ट गंतव्यों के सख्त श्वेतसूची-आधारित सत्यापन  
- **प्राधिकरण कोड सुरक्षा**: एकल-उपयोग प्रवर्तन के साथ अल्पकालिक कोड  
- **क्लाइंट पहचान सत्यापन**: क्लाइंट क्रेडेंशियल और मेटाडेटा का मजबूत सत्यापन  

## 6. **टूल निष्पादन सुरक्षा**

### **सैंडबॉक्सिंग और आइसोलेशन**

**कंटेनर-आधारित आइसोलेशन:**
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

**प्रक्रिया आइसोलेशन:**
- **अलग प्रक्रिया संदर्भ**: प्रत्येक टूल निष्पादन को अलग प्रक्रिया स्थान में  
- **इंटर-प्रोसेस कम्युनिकेशन**: सत्यापन के साथ सुरक्षित IPC तंत्र  
- **प्रक्रिया निगरानी**: रनटाइम व्यवहार विश्लेषण और विसंगति का पता लगाना  
- **संसाधन प्रवर्तन**: CPU, मेमोरी और I/O संचालन पर सख्त सीमाएँ  

### **न्यूनतम विशेषाधिकार कार्यान्वयन**

**अनुमति प्रबंधन:**
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

## 7. **सप्लाई चेन सुरक्षा नियंत्रण**

### **निर्भरता सत्यापन**

**व्यापक घटक सुरक्षा:**
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

### **निरंतर निगरानी**

**सप्लाई चेन खतरे का पता लगाना:**
- **निर्भरता स्वास्थ्य निगरानी**: सुरक्षा मुद्दों के लिए सभी निर्भरताओं का निरंतर आकलन  
- **खतरे की खुफिया एकीकरण**: उभरते सप्लाई चेन खतरों पर वास्तविक समय अपडेट  
- **व्यवहार विश्लेषण**: बाहरी घटकों में असामान्य व्यवहार का पता लगाना  
- **स्वचालित प्रतिक्रिया**: समझौता किए गए घटकों की तत्काल रोकथाम  

## 8. **निगरानी और पता लगाने के नियंत्रण**

### **सुरक्षा सूचना और घटना प्रबंधन (SIEM)**

**व्यापक लॉगिंग रणनीति:**
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

### **वास्तविक समय खतरे का पता लगाना**

**व्यवहार विश्लेषिकी:**
- **उपयोगकर्ता व्यवहार विश्लेषिकी (UBA)**: असामान्य उपयोगकर्ता एक्सेस पैटर्न का पता लगाना  
- **इकाई व्यवहार विश्लेषिकी (EBA)**: MCP सर्वर और टूल व्यवहार की निगरानी  
- **मशीन लर्निंग विसंगति का पता लगाना**: एआई-संचालित सुरक्षा खतरों की पहचान  
- **खतरे की खुफिया सहसंबंध**: ज्ञात हमले पैटर्न के खिलाफ देखी गई गतिविधियों का मिलान  

## 9. **घटना प्रतिक्रिया और पुनर्प्राप्ति**

### **स्वचालित प्रतिक्रिया क्षमताएँ**

**तत्काल प्रतिक्रिया क्रियाएँ:**
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

### **फॉरेंसिक क्षमताएँ**

**जांच समर्थन:**
- **ऑडिट ट्रेल संरक्षण**: क्रिप्टोग्राफिक अखंडता के साथ अपरिवर्तनीय लॉगिंग  
- **साक्ष्य संग्रह**: प्रासंगिक सुरक्षा कलाकृतियों का स्वचालित संग्रह  
- **समयरेखा पुनर्निर्माण**: सुरक्षा घटनाओं की ओर ले जाने वाली घटनाओं का विस्तृत क्रम  
- **प्रभाव आकलन**: समझौता दायरे और डेटा एक्सपोज़र का मूल्यांकन  

## **मुख्य सुरक्षा वास्तुकला सिद्धांत**

### **गहराई में रक्षा**
- **कई सुरक्षा परतें**: सुरक्षा वास्तुकला में कोई एकल विफलता बिंदु नहीं  
- **अतिरिक्त नियंत्रण**: महत्वपूर्ण कार्यों के लिए ओवरलैपिंग सुरक्षा उपाय  
- **फेल-सेफ तंत्र**: जब सिस्टम त्रुटियों या हमलों का सामना करते हैं तो सुरक्षित डिफॉल्ट्स  

### **शून्य विश्वास कार्यान्वयन**
- **कभी भरोसा न करें, हमेशा सत्यापित करें**: सभी संस्थाओं और अनुरोधों का निरंतर सत्यापन  
- **न्यूनतम विशेषाधिकार का सिद्धांत**: सभी घटकों के लिए न्यूनतम एक्सेस अधिकार  
- **माइक्रो-सेगमेंटेशन**: सूक्ष्म नेटवर्क और एक्सेस नियंत्रण  

### **निरंतर सुरक्षा विकास**
- **खतरे के परिदृश्य का अनुकूलन**: उभरते खतरों को संबोधित करने के लिए नियमित अपडेट  
- **सुरक्षा नियंत्रण प्रभावशीलता**: नियंत्रणों के निरंतर मूल्यांकन और सुधार  
- **विनिर्देश अनुपालन**: विकसित हो रहे MCP सुरक्षा मानकों के साथ संरेखण  

---

## **कार्यान्वयन संसाधन**

### **आधिकारिक MCP दस्तावेज़ीकरण**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft सुरक्षा समाधान**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **सुरक्षा मानक**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **महत्वपूर्ण**: ये सुरक्षा नियंत्रण वर्तमान MCP विनिर्देश (2025-06-18) को दर्शाते हैं। मानक तेजी से विकसित हो रहे हैं, इसलिए हमेशा नवीनतम [आधिकारिक दस्तावेज़ीकरण](https://spec.modelcontextprotocol.io/) के खिलाफ सत्यापित करें।  

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को आधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।