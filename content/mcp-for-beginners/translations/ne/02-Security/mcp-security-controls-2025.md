<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T16:10:44+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ne"
}
-->
# MCP सुरक्षा नियन्त्रणहरू - अगस्ट २०२५ अद्यावधिक

> **हालको मापदण्ड**: यो दस्तावेजले [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) सुरक्षा आवश्यकताहरू र आधिकारिक [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) लाई प्रतिबिम्बित गर्दछ।

मोडेल कन्टेक्स्ट प्रोटोकल (MCP) ले परम्परागत सफ्टवेयर सुरक्षा र AI-विशेष खतराहरूलाई सम्बोधन गर्दै महत्वपूर्ण रूपमा सुधारिएको सुरक्षा नियन्त्रणहरू विकास गरेको छ। यो दस्तावेजले अगस्ट २०२५ सम्मको सुरक्षित MCP कार्यान्वयनका लागि व्यापक सुरक्षा नियन्त्रणहरू प्रदान गर्दछ।

## **अनिवार्य सुरक्षा आवश्यकताहरू**

### **MCP Specification बाट महत्त्वपूर्ण निषेधहरू:**

> **निषेधित**: MCP सर्भरहरूले **कुनै पनि टोकन स्वीकार गर्न हुँदैन** जुन MCP सर्भरका लागि स्पष्ट रूपमा जारी गरिएको छैन  
>
> **प्रतिबन्धित**: MCP सर्भरहरूले **सत्रहरू प्रमाणीकरणका लागि प्रयोग गर्न हुँदैन**  
>
> **आवश्यक**: MCP सर्भरहरूले प्राधिकरण कार्यान्वयन गर्दा **सबै इनबाउन्ड अनुरोधहरू प्रमाणित गर्नै पर्छ**  
>
> **अनिवार्य**: स्थिर क्लाइन्ट ID प्रयोग गर्ने MCP प्रोक्सी सर्भरहरूले **प्रत्येक गतिशील रूपमा दर्ता गरिएको क्लाइन्टका लागि प्रयोगकर्ताको सहमति प्राप्त गर्नै पर्छ**  

---

## १. **प्रमाणीकरण र प्राधिकरण नियन्त्रणहरू**

### **बाह्य पहिचान प्रदायक एकीकरण**

**हालको MCP मापदण्ड (2025-06-18)** ले MCP सर्भरहरूलाई प्रमाणीकरण बाह्य पहिचान प्रदायकहरूमा प्रतिनिधि गर्न अनुमति दिन्छ, जसले सुरक्षा सुधारमा महत्त्वपूर्ण योगदान पुर्‍याउँछ:

**सुरक्षा फाइदाहरू:**
1. **अनुकूलित प्रमाणीकरण जोखिमहरू हटाउँछ**: अनुकूलित प्रमाणीकरण कार्यान्वयनबाट बचेर जोखिम कम गर्दछ  
2. **उद्यम-स्तरको सुरक्षा**: Microsoft Entra ID जस्ता स्थापित पहिचान प्रदायकहरूको उन्नत सुरक्षा सुविधाहरू प्रयोग गर्दछ  
3. **केन्द्रित पहिचान व्यवस्थापन**: प्रयोगकर्ता जीवनचक्र व्यवस्थापन, पहुँच नियन्त्रण, र अनुपालन अडिटलाई सरल बनाउँछ  
4. **बहु-कारक प्रमाणीकरण (MFA)**: उद्यम पहिचान प्रदायकहरूको MFA क्षमताहरू अपनाउँछ  
5. **सशर्त पहुँच नीतिहरू**: जोखिम-आधारित पहुँच नियन्त्रण र अनुकूलन प्रमाणीकरणको फाइदा उठाउँछ  

**कार्यान्वयन आवश्यकताहरू:**
- **टोकन दर्शक प्रमाणीकरण**: सबै टोकनहरू MCP सर्भरका लागि स्पष्ट रूपमा जारी गरिएको सुनिश्चित गर्नुहोस्  
- **जारीकर्ता प्रमाणीकरण**: टोकन जारीकर्ता अपेक्षित पहिचान प्रदायकसँग मेल खाने सुनिश्चित गर्नुहोस्  
- **हस्ताक्षर प्रमाणीकरण**: टोकनको अखण्डताको क्रिप्टोग्राफिक प्रमाणीकरण  
- **समाप्ति प्रवर्तन**: टोकनको जीवनकाल सीमा कडाइका साथ लागू गर्नुहोस्  
- **स्कोप प्रमाणीकरण**: टोकनहरूले अनुरोध गरिएका कार्यहरूको लागि उपयुक्त अनुमति समावेश गरेको सुनिश्चित गर्नुहोस्  

### **प्राधिकरण तर्क सुरक्षा**

**महत्त्वपूर्ण नियन्त्रणहरू:**
- **व्यापक प्राधिकरण अडिटहरू**: सबै प्राधिकरण निर्णय बिन्दुहरूको नियमित सुरक्षा समीक्षा  
- **असफल-सुरक्षित पूर्वनिर्धारणहरू**: प्राधिकरण तर्कले स्पष्ट निर्णय गर्न नसक्दा पहुँच अस्वीकार गर्नुहोस्  
- **अनुमति सीमाहरू**: विभिन्न विशेषाधिकार स्तर र स्रोत पहुँच बीच स्पष्ट विभाजन  
- **अडिट लगिङ**: सुरक्षा निगरानीका लागि सबै प्राधिकरण निर्णयहरूको पूर्ण लगिङ  
- **नियमित पहुँच समीक्षा**: प्रयोगकर्ता अनुमतिहरू र विशेषाधिकार असाइनमेन्टहरूको आवधिक प्रमाणीकरण  

## २. **टोकन सुरक्षा र पासथ्रु नियन्त्रणहरू**

### **टोकन पासथ्रु रोकथाम**

**MCP प्राधिकरण मापदण्डमा टोकन पासथ्रु स्पष्ट रूपमा निषेधित छ** किनभने यसले गम्भीर सुरक्षा जोखिमहरू निम्त्याउँछ:

**सम्बोधन गरिएका सुरक्षा जोखिमहरू:**
- **नियन्त्रणको परिक्रमा**: दर सीमितता, अनुरोध प्रमाणीकरण, र ट्राफिक निगरानी जस्ता महत्त्वपूर्ण सुरक्षा नियन्त्रणहरूलाई बाइपास गर्दछ  
- **जवाफदेहिता विघटन**: क्लाइन्ट पहिचान असम्भव बनाउँछ, अडिट ट्रेलहरू र घटनाको अनुसन्धानलाई बिगार्छ  
- **प्रोक्सी-आधारित डाटा चोरी**: अनधिकृत डाटा पहुँचका लागि सर्भरहरूलाई प्रोक्सीको रूपमा प्रयोग गर्न सक्षम बनाउँछ  
- **विश्वास सीमा उल्लङ्घन**: टोकन उत्पत्तिबारे डाउनस्ट्रीम सेवाहरूको विश्वास मान्यताहरू तोड्छ  
- **पार्श्व आन्दोलन**: धेरै सेवाहरूमा सम्झौता गरिएका टोकनहरूले व्यापक आक्रमण विस्तार सक्षम बनाउँछ  

**कार्यान्वयन नियन्त्रणहरू:**
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

### **सुरक्षित टोकन व्यवस्थापन ढाँचाहरू**

**सर्वोत्तम अभ्यासहरू:**
- **छोटो-समयावधि टोकनहरू**: बारम्बार टोकन घुमाएर जोखिमको झ्याललाई न्यूनतम बनाउनुहोस्  
- **ठीक समयमा जारी गर्नुहोस्**: विशिष्ट कार्यहरूको लागि आवश्यक पर्दा मात्र टोकनहरू जारी गर्नुहोस्  
- **सुरक्षित भण्डारण**: हार्डवेयर सुरक्षा मोड्युल (HSM) वा सुरक्षित कुञ्जी भण्डार प्रयोग गर्नुहोस्  
- **टोकन बाइन्डिङ**: टोकनहरू विशिष्ट क्लाइन्ट, सत्र, वा कार्यहरूमा बाँध्नुहोस् जहाँ सम्भव छ  
- **निगरानी र सतर्कता**: टोकन दुरुपयोग वा अनधिकृत पहुँच ढाँचाहरूको वास्तविक-समय पत्ता लगाउने  

## ३. **सत्र सुरक्षा नियन्त्रणहरू**

### **सत्र अपहरण रोकथाम**

**सम्बोधन गरिएका आक्रमण भेक्टरहरू:**
- **सत्र अपहरण प्रम्प्ट इन्जेक्सन**: साझा सत्र अवस्थामा दुर्भावनापूर्ण घटनाहरू इंजेक्ट गरिन्छ  
- **सत्र नक्कल**: चोरी भएका सत्र ID को अनधिकृत प्रयोगले प्रमाणीकरणलाई बाइपास गर्दछ  
- **पुनःसुरुयोग्य स्ट्रिम आक्रमणहरू**: दुर्भावनापूर्ण सामग्री इंजेक्सनका लागि सर्भर-प्रेषित घटनाको पुनःसुरुयोगको शोषण  

**अनिवार्य सत्र नियन्त्रणहरू:**
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
- **HTTPS प्रवर्तन**: TLS 1.3 मार्फत सबै सत्र सञ्चार  
- **सुरक्षित कुकी विशेषताहरू**: HttpOnly, Secure, SameSite=Strict  
- **प्रमाणपत्र पिनिङ**: MITM आक्रमण रोक्नका लागि महत्त्वपूर्ण जडानहरूको लागि  

### **राज्यपूर्ण बनाम राज्यरहित विचारहरू**

**राज्यपूर्ण कार्यान्वयनहरूको लागि:**
- साझा सत्र अवस्थाले इंजेक्सन आक्रमणहरू विरुद्ध थप सुरक्षा आवश्यक छ  
- पङ्क्ति-आधारित सत्र व्यवस्थापनले अखण्डता प्रमाणीकरण आवश्यक छ  
- धेरै सर्भर उदाहरणहरूले सुरक्षित सत्र अवस्था समक्रमण आवश्यक छ  

**राज्यरहित कार्यान्वयनहरूको लागि:**
- JWT वा यस्तै टोकन-आधारित सत्र व्यवस्थापन  
- सत्र अवस्थाको अखण्डताको क्रिप्टोग्राफिक प्रमाणीकरण  
- आक्रमण सतह घटाइन्छ तर बलियो टोकन प्रमाणीकरण आवश्यक छ  

## ४. **AI-विशेष सुरक्षा नियन्त्रणहरू**

### **प्रम्प्ट इन्जेक्सन रक्षा**

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

**कार्यान्वयन नियन्त्रणहरू:**
- **इनपुट स्वच्छता**: सबै प्रयोगकर्ता इनपुटहरूको व्यापक प्रमाणीकरण र फिल्टरिङ  
- **सामग्री सीमा परिभाषा**: प्रणाली निर्देशनहरू र प्रयोगकर्ता सामग्री बीच स्पष्ट विभाजन  
- **निर्देशन पदानुक्रम**: विरोधाभासी निर्देशनहरूको लागि उचित प्राथमिकता नियमहरू  
- **आउटपुट निगरानी**: सम्भावित हानिकारक वा हेरफेर गरिएका आउटपुटहरूको पत्ता लगाउने  

### **उपकरण विषाक्तता रोकथाम**

**उपकरण सुरक्षा रूपरेखा:**
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

**गतिशील उपकरण व्यवस्थापन:**
- **स्वीकृति कार्यप्रवाहहरू**: उपकरण परिमार्जनहरूको लागि स्पष्ट प्रयोगकर्ता सहमति  
- **रोलब्याक क्षमताहरू**: अघिल्लो उपकरण संस्करणहरूमा फर्कने क्षमता  
- **परिवर्तन अडिटिङ**: उपकरण परिभाषा परिमार्जनहरूको पूर्ण इतिहास  
- **जोखिम मूल्याङ्कन**: उपकरण सुरक्षा अवस्थाको स्वचालित मूल्याङ्कन  

## ५. **Confused Deputy आक्रमण रोकथाम**

### **OAuth प्रोक्सी सुरक्षा**

**आक्रमण रोकथाम नियन्त्रणहरू:**
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

**कार्यान्वयन आवश्यकताहरू:**
- **प्रयोगकर्ता सहमति प्रमाणीकरण**: गतिशील क्लाइन्ट दर्ताका लागि सहमति स्क्रिनहरू कहिल्यै नछोड्नुहोस्  
- **पुनर्निर्देशन URI प्रमाणीकरण**: पुनर्निर्देशन गन्तव्यहरूको कडाइका साथ श्वेतसूची-आधारित प्रमाणीकरण  
- **प्राधिकरण कोड सुरक्षा**: छोटो-समयावधि कोडहरू एकल-प्रयोग प्रवर्तनका साथ  
- **क्लाइन्ट पहिचान प्रमाणीकरण**: क्लाइन्ट प्रमाणहरू र मेटाडाटाको बलियो प्रमाणीकरण  

## ६. **उपकरण कार्यान्वयन सुरक्षा**

### **स्यान्डबक्सिङ र अलगाव**

**कन्टेनर-आधारित अलगाव:**
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

**प्रक्रिया अलगाव:**
- **पृथक प्रक्रिया सन्दर्भहरू**: प्रत्येक उपकरण कार्यान्वयनलाई अलग प्रक्रिया स्थानमा  
- **प्रक्रिया अन्तर सञ्चार**: प्रमाणीकरणसहितको सुरक्षित IPC संयन्त्र  
- **प्रक्रिया निगरानी**: रनटाइम व्यवहार विश्लेषण र असामान्यता पत्ता लगाउने  
- **स्रोत प्रवर्तन**: CPU, मेमोरी, र I/O अपरेसनहरूमा कडा सीमा  

### **न्यूनतम विशेषाधिकार कार्यान्वयन**

**अनुमति व्यवस्थापन:**
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

## ७. **आपूर्ति श्रृंखला सुरक्षा नियन्त्रणहरू**

### **निर्भरता प्रमाणीकरण**

**व्यापक कम्पोनेन्ट सुरक्षा:**
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

### **निरन्तर निगरानी**

**आपूर्ति श्रृंखला खतरा पत्ता लगाउने:**
- **निर्भरता स्वास्थ्य निगरानी**: सबै निर्भरताहरूको सुरक्षा समस्याहरूको लागि निरन्तर मूल्याङ्कन  
- **खतरा खुफिया एकीकरण**: उदीयमान आपूर्ति श्रृंखला खतराहरूको वास्तविक-समय अद्यावधिक  
- **व्यवहार विश्लेषण**: बाह्य कम्पोनेन्टहरूको असामान्य व्यवहारको पत्ता लगाउने  
- **स्वचालित प्रतिक्रिया**: सम्झौता गरिएका कम्पोनेन्टहरूको तत्काल नियन्त्रण  

## ८. **निगरानी र पत्ता लगाउने नियन्त्रणहरू**

### **सुरक्षा जानकारी र घटना व्यवस्थापन (SIEM)**

**व्यापक लगिङ रणनीति:**
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

### **वास्तविक-समय खतरा पत्ता लगाउने**

**व्यवहार विश्लेषण:**
- **प्रयोगकर्ता व्यवहार विश्लेषण (UBA)**: असामान्य प्रयोगकर्ता पहुँच ढाँचाहरूको पत्ता लगाउने  
- **सत्ता व्यवहार विश्लेषण (EBA)**: MCP सर्भर र उपकरण व्यवहारको निगरानी  
- **मेसिन लर्निङ असामान्यता पत्ता लगाउने**: AI-शक्तियुक्त सुरक्षा खतराहरूको पहिचान  
- **खतरा खुफिया सम्बन्ध**: ज्ञात आक्रमण ढाँचाहरू विरुद्ध देखिएका गतिविधिहरूको मिलान  

## ९. **घटना प्रतिक्रिया र पुनःप्राप्ति**

### **स्वचालित प्रतिक्रिया क्षमताहरू**

**तत्काल प्रतिक्रिया कार्यहरू:**
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

### **फरेन्सिक क्षमताहरू**

**अनुसन्धान समर्थन:**
- **अडिट ट्रेल संरक्षण**: क्रिप्टोग्राफिक अखण्डतासहितको अपरिवर्तनीय लगिङ  
- **प्रमाण सङ्कलन**: सम्बन्धित सुरक्षा कलाकृतिहरूको स्वचालित सङ्कलन  
- **समयरेखा पुनर्निर्माण**: सुरक्षा घटनाहरूको विस्तृत क्रम  
- **प्रभाव मूल्याङ्कन**: सम्झौताको दायरा र डाटा जोखिमको मूल्याङ्कन  

## **महत्त्वपूर्ण सुरक्षा वास्तुकला सिद्धान्तहरू**

### **गहिराइमा रक्षा**
- **धेरै सुरक्षा तहहरू**: सुरक्षा वास्तुकलामा कुनै पनि एकल असफलताको बिन्दु छैन  
- **अतिरिक्त नियन्त्रणहरू**: महत्त्वपूर्ण कार्यहरूको लागि ओभरल्यापिङ सुरक्षा उपायहरू  
- **असफल-सुरक्षित संयन्त्रहरू**: प्रणालीहरूले त्रुटि वा आक्रमणको सामना गर्दा सुरक्षित पूर्वनिर्धारणहरू  

### **शून्य विश्वास कार्यान्वयन**
- **कहिल्यै विश्वास नगर्नुहोस्, सधैं प्रमाणीकरण गर्नुहोस्**: सबै इकाईहरू र अनुरोधहरूको निरन्तर प्रमाणीकरण  
- **न्यूनतम विशेषाधिकारको सिद्धान्त**: सबै कम्पोनेन्टहरूको लागि न्यूनतम पहुँच अधिकार  
- **सूक्ष्म-खण्डीकरण**: सूक्ष्म नेटवर्क र पहुँच नियन्त्रण  

### **निरन्तर सुरक्षा विकास**
- **खतरा परिदृश्य अनुकूलन**: उदीयमान खतराहरूलाई सम्बोधन गर्न नियमित अद्यावधिक  
- **सुरक्षा नियन्त्रण प्रभावकारिता**: नियन्त्रणहरूको निरन्तर मूल्याङ्कन र सुधार  
- **मापदण्ड अनुपालन**: विकसित हुँदै गएका MCP सुरक्षा मापदण्डहरूसँगको संरेखण  

---

## **कार्यान्वयन स्रोतहरू**

### **आधिकारिक MCP दस्तावेजहरू**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft सुरक्षा समाधानहरू**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **सुरक्षा मापदण्डहरू**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **महत्त्वपूर्ण**: यी सुरक्षा नियन्त्रणहरूले हालको MCP मापदण्ड (2025-06-18) लाई प्रतिबिम्बित गर्दछ। मापदण्डहरू तीव्र रूपमा विकसित भइरहेकाले सधैं [आधिकारिक दस्तावेज](https://spec.modelcontextprotocol.io/) सँग प्रमाणीकरण गर्नुहोस्।  

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी यथासम्भव सटीकता सुनिश्चित गर्न प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादहरूमा त्रुटि वा अशुद्धता हुन सक्छ। यसको मूल भाषामा रहेको मूल दस्तावेज़लाई आधिकारिक स्रोत मानिनुपर्छ। महत्त्वपूर्ण जानकारीका लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुने छैनौं।