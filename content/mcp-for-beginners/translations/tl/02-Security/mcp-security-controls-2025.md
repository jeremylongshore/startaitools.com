<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T18:21:53+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "tl"
}
-->
# Mga Kontrol sa Seguridad ng MCP - Update noong Agosto 2025

> **Kasalukuyang Pamantayan**: Ang dokumentong ito ay sumasalamin sa mga kinakailangan sa seguridad ng [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) at opisyal na [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Ang Model Context Protocol (MCP) ay nagkaroon ng malaking pag-unlad sa pagpapahusay ng mga kontrol sa seguridad na tumutugon sa parehong tradisyunal na seguridad ng software at mga banta na partikular sa AI. Ang dokumentong ito ay nagbibigay ng komprehensibong mga kontrol sa seguridad para sa ligtas na implementasyon ng MCP simula Agosto 2025.

## **MGA KAILANGANG SEGURIDAD NA DAPAT SUNDIN**

### **Mga Kritikal na Pagbabawal mula sa MCP Specification:**

> **IPINAGBABAWAL**: Ang mga MCP server **HINDI DAPAT** tumanggap ng anumang token na hindi tahasang inisyu para sa MCP server  
>
> **IPINAGBABAWAL**: Ang mga MCP server **HINDI DAPAT** gumamit ng mga session para sa authentication  
>
> **KINAKAILANGAN**: Ang mga MCP server na nagpapatupad ng authorization **DAPAT** i-verify ang LAHAT ng papasok na kahilingan  
>
> **MANDATORYO**: Ang mga MCP proxy server na gumagamit ng static client IDs **DAPAT** kumuha ng pahintulot ng user para sa bawat dinamikong nakarehistrong kliyente  

---

## 1. **Mga Kontrol sa Authentication at Authorization**

### **Integrasyon ng Panlabas na Tagapagbigay ng Pagkakakilanlan**

Ang **Kasalukuyang Pamantayan ng MCP (2025-06-18)** ay nagpapahintulot sa mga MCP server na i-delegate ang authentication sa mga panlabas na tagapagbigay ng pagkakakilanlan, na nagdadala ng malaking pagpapabuti sa seguridad:

**Mga Benepisyo sa Seguridad:**
1. **Pag-aalis ng Panganib sa Custom Authentication**: Binabawasan ang posibilidad ng kahinaan sa pamamagitan ng pag-iwas sa custom na implementasyon ng authentication  
2. **Seguridad na Pang-Enterprise**: Ginagamit ang mga kilalang tagapagbigay ng pagkakakilanlan tulad ng Microsoft Entra ID na may mga advanced na tampok sa seguridad  
3. **Sentralisadong Pamamahala ng Pagkakakilanlan**: Pinapasimple ang pamamahala sa lifecycle ng user, kontrol sa access, at pag-audit ng pagsunod  
4. **Multi-Factor Authentication**: Namamana ang mga kakayahan ng MFA mula sa mga tagapagbigay ng pagkakakilanlan ng enterprise  
5. **Mga Patakaran sa Kondisyunal na Access**: Nakikinabang mula sa mga kontrol sa access na batay sa panganib at adaptive na authentication  

**Mga Kinakailangan sa Implementasyon:**
- **Pag-validate ng Token Audience**: Siguraduhing ang lahat ng token ay tahasang inisyu para sa MCP server  
- **Pag-verify ng Issuer**: Siguraduhing ang issuer ng token ay tumutugma sa inaasahang tagapagbigay ng pagkakakilanlan  
- **Pag-verify ng Lagda**: Cryptographic na pag-validate ng integridad ng token  
- **Pagpapatupad ng Expiration**: Mahigpit na pagpapatupad ng mga limitasyon sa tagal ng token  
- **Pag-validate ng Saklaw**: Siguraduhing ang mga token ay naglalaman ng naaangkop na mga pahintulot para sa mga hinihiling na operasyon  

### **Seguridad ng Authorization Logic**

**Kritikal na Mga Kontrol:**
- **Komprehensibong Mga Audit ng Authorization**: Regular na pagsusuri sa seguridad ng lahat ng mga punto ng desisyon sa authorization  
- **Fail-Safe Defaults**: Tanggihan ang access kapag hindi makagawa ng tiyak na desisyon ang authorization logic  
- **Mga Hangganan ng Pahintulot**: Malinaw na paghihiwalay sa pagitan ng iba't ibang antas ng pribilehiyo at access sa mga mapagkukunan  
- **Audit Logging**: Kumpletong pag-log ng lahat ng desisyon sa authorization para sa pagsubaybay sa seguridad  
- **Regular na Pagsusuri ng Access**: Pana-panahong pag-validate ng mga pahintulot ng user at mga itinalagang pribilehiyo  

## 2. **Seguridad ng Token at Mga Kontrol sa Anti-Passthrough**

### **Pag-iwas sa Token Passthrough**

**Ang token passthrough ay tahasang ipinagbabawal** sa MCP Authorization Specification dahil sa mga kritikal na panganib sa seguridad:

**Mga Panganib sa Seguridad na Natugunan:**
- **Pag-iwas sa Kontrol**: Iniiwasan ang mahahalagang kontrol sa seguridad tulad ng rate limiting, pag-validate ng kahilingan, at pagsubaybay sa trapiko  
- **Pagkasira ng Pananagutan**: Ginagawang imposibleng matukoy ang kliyente, na sinisira ang mga audit trail at pagsisiyasat ng insidente  
- **Proxy-Based Exfiltration**: Pinapahintulutan ang mga malisyosong aktor na gamitin ang mga server bilang proxy para sa hindi awtorisadong pag-access ng data  
- **Paglabag sa Trust Boundary**: Sinisira ang mga inaasahan ng downstream service tungkol sa pinagmulan ng token  
- **Lateral Movement**: Ang mga nakompromisong token sa maraming serbisyo ay nagpapalawak ng saklaw ng pag-atake  

**Mga Kontrol sa Implementasyon:**
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

### **Mga Ligtas na Pattern sa Pamamahala ng Token**

**Mga Pinakamahusay na Kasanayan:**
- **Mga Token na Maikli ang Buhay**: Bawasan ang exposure window sa pamamagitan ng madalas na pag-rotate ng token  
- **Just-in-Time Issuance**: Mag-isyu ng mga token lamang kapag kinakailangan para sa mga partikular na operasyon  
- **Ligtas na Imbakan**: Gumamit ng hardware security modules (HSMs) o secure key vaults  
- **Token Binding**: Itali ang mga token sa mga partikular na kliyente, session, o operasyon kung maaari  
- **Pagsubaybay at Pag-alerto**: Real-time na pagtuklas ng maling paggamit ng token o mga pattern ng hindi awtorisadong pag-access  

## 3. **Mga Kontrol sa Seguridad ng Session**

### **Pag-iwas sa Session Hijacking**

**Mga Vector ng Pag-atake na Natugunan:**
- **Session Hijack Prompt Injection**: Mga malisyosong kaganapan na na-inject sa shared session state  
- **Session Impersonation**: Hindi awtorisadong paggamit ng mga ninakaw na session ID upang iwasan ang authentication  
- **Resumable Stream Attacks**: Pagsasamantala sa resumption ng server-sent event para sa malisyosong pag-inject ng nilalaman  

**Mga Mandatoryong Kontrol sa Session:**
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

**Seguridad sa Transportasyon:**
- **Pagpapatupad ng HTTPS**: Lahat ng komunikasyon sa session ay dapat dumaan sa TLS 1.3  
- **Mga Atributo ng Secure Cookie**: HttpOnly, Secure, SameSite=Strict  
- **Certificate Pinning**: Para sa mga kritikal na koneksyon upang maiwasan ang MITM attacks  

### **Mga Pagsasaalang-alang sa Stateful vs Stateless**

**Para sa Stateful na Implementasyon:**
- Ang shared session state ay nangangailangan ng karagdagang proteksyon laban sa mga pag-atake ng injection  
- Ang pamamahala ng session na nakabatay sa queue ay nangangailangan ng pag-verify ng integridad  
- Ang maraming instance ng server ay nangangailangan ng ligtas na pag-synchronize ng session state  

**Para sa Stateless na Implementasyon:**
- JWT o katulad na token-based na pamamahala ng session  
- Cryptographic na pag-verify ng integridad ng session state  
- Nabawasang attack surface ngunit nangangailangan ng matibay na pag-validate ng token  

## 4. **Mga Kontrol sa Seguridad na Partikular sa AI**

### **Depensa laban sa Prompt Injection**

**Integrasyon ng Microsoft Prompt Shields:**
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

**Mga Kontrol sa Implementasyon:**
- **Sanitasyon ng Input**: Komprehensibong pag-validate at pag-filter ng lahat ng input ng user  
- **Pagpapakahulugan ng Content Boundary**: Malinaw na paghihiwalay sa pagitan ng mga tagubilin ng sistema at nilalaman ng user  
- **Hierarchy ng Instruksyon**: Tamang mga panuntunan sa precedence para sa mga nagkakasalungatang tagubilin  
- **Pagsubaybay sa Output**: Pagtuklas ng potensyal na mapanganib o manipuladong output  

### **Pag-iwas sa Tool Poisoning**

**Framework ng Seguridad ng Tool:**
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

**Dynamic na Pamamahala ng Tool:**
- **Mga Workflow ng Pag-apruba**: Tahasang pahintulot ng user para sa mga pagbabago sa tool  
- **Mga Kakayahan sa Rollback**: Kakayahang ibalik sa mga nakaraang bersyon ng tool  
- **Pag-audit ng Pagbabago**: Kumpletong kasaysayan ng mga pagbabago sa depinisyon ng tool  
- **Pagtatasa ng Panganib**: Awtomatikong pagsusuri ng security posture ng tool  

## 5. **Pag-iwas sa Confused Deputy Attack**

### **Seguridad ng OAuth Proxy**

**Mga Kontrol sa Pag-iwas sa Pag-atake:**
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

**Mga Kinakailangan sa Implementasyon:**
- **Pag-verify ng Pahintulot ng User**: Huwag kailanman laktawan ang mga screen ng pahintulot para sa dinamikong pagpaparehistro ng kliyente  
- **Pag-validate ng Redirect URI**: Mahigpit na pag-validate batay sa whitelist ng mga destinasyon ng redirect  
- **Proteksyon ng Authorization Code**: Mga code na maikli ang buhay na may pagpapatupad ng single-use  
- **Pag-verify ng Identidad ng Kliyente**: Matibay na pag-validate ng mga kredensyal at metadata ng kliyente  

## 6. **Seguridad sa Pagpapatupad ng Tool**

### **Sandboxing at Isolation**

**Isolation na Batay sa Container:**
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

**Isolation ng Proseso:**
- **Hiwalay na Mga Konteksto ng Proseso**: Ang bawat pagpapatupad ng tool ay nasa hiwalay na espasyo ng proseso  
- **Inter-Process Communication**: Mga secure na mekanismo ng IPC na may pag-validate  
- **Pagsubaybay sa Proseso**: Pagsusuri ng runtime behavior at pagtuklas ng anomalya  
- **Pagpapatupad ng Resource**: Mahigpit na limitasyon sa CPU, memory, at mga operasyon ng I/O  

### **Pagpapatupad ng Least Privilege**

**Pamamahala ng Pahintulot:**
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

## 7. **Mga Kontrol sa Seguridad ng Supply Chain**

### **Pag-verify ng Dependency**

**Komprehensibong Seguridad ng Komponent:**
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

### **Patuloy na Pagsubaybay**

**Pagtuklas ng Banta sa Supply Chain:**
- **Pagsubaybay sa Kalusugan ng Dependency**: Patuloy na pagtatasa ng lahat ng dependency para sa mga isyu sa seguridad  
- **Integrasyon ng Threat Intelligence**: Real-time na mga update sa mga umuusbong na banta sa supply chain  
- **Pagsusuri ng Pag-uugali**: Pagtuklas ng hindi pangkaraniwang pag-uugali sa mga panlabas na bahagi  
- **Awtomatikong Tugon**: Agarang containment ng mga nakompromisong bahagi  

## 8. **Mga Kontrol sa Pagsubaybay at Pagtuklas**

### **Security Information and Event Management (SIEM)**

**Komprehensibong Estratehiya sa Pag-log:**
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

### **Real-Time na Pagtuklas ng Banta**

**Behavioral Analytics:**
- **User Behavior Analytics (UBA)**: Pagtuklas ng hindi pangkaraniwang mga pattern ng pag-access ng user  
- **Entity Behavior Analytics (EBA)**: Pagsubaybay sa pag-uugali ng MCP server at tool  
- **Machine Learning Anomaly Detection**: AI-powered na pagtukoy ng mga banta sa seguridad  
- **Threat Intelligence Correlation**: Pagtutugma ng mga naobserbahang aktibidad laban sa mga kilalang pattern ng pag-atake  

## 9. **Pagtugon at Pagbangon sa Insidente**

### **Mga Kakayahan sa Awtomatikong Tugon**

**Agarang Mga Aksyon sa Tugon:**
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

### **Mga Kakayahan sa Forensic**

**Suporta sa Pagsisiyasat:**
- **Pagpapanatili ng Audit Trail**: Immutable na pag-log na may cryptographic integrity  
- **Koleksyon ng Ebidensya**: Awtomatikong pagkuha ng mga kaugnay na artifact sa seguridad  
- **Rekonstruksyon ng Timeline**: Detalyadong pagkakasunod-sunod ng mga kaganapan na humantong sa mga insidente sa seguridad  
- **Pagtatasa ng Epekto**: Pagsusuri ng saklaw ng kompromiso at pagkakalantad ng data  

## **Pangunahing Prinsipyo ng Arkitektura ng Seguridad**

### **Defense in Depth**
- **Maramihang Layer ng Seguridad**: Walang iisang punto ng kabiguan sa arkitektura ng seguridad  
- **Redundant na Mga Kontrol**: Mga magkakapatong na hakbang sa seguridad para sa mga kritikal na function  
- **Fail-Safe na Mekanismo**: Mga ligtas na default kapag ang mga sistema ay nakakaranas ng mga error o pag-atake  

### **Pagpapatupad ng Zero Trust**
- **Huwag Magtiwala, Laging Mag-verify**: Patuloy na pag-validate ng lahat ng entity at kahilingan  
- **Prinsipyo ng Least Privilege**: Minimal na karapatan sa pag-access para sa lahat ng bahagi  
- **Micro-Segmentation**: Granular na kontrol sa network at access  

### **Patuloy na Ebolusyon ng Seguridad**
- **Pag-aangkop sa Landscape ng Banta**: Regular na mga update upang matugunan ang mga umuusbong na banta  
- **Epektibidad ng Kontrol sa Seguridad**: Patuloy na pagsusuri at pagpapabuti ng mga kontrol  
- **Pagsunod sa Espesipikasyon**: Pagsunod sa mga umuusbong na pamantayan sa seguridad ng MCP  

---

## **Mga Mapagkukunan sa Implementasyon**

### **Opisyal na Dokumentasyon ng MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Mga Solusyon sa Seguridad ng Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Mga Pamantayan sa Seguridad**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Mahalaga**: Ang mga kontrol sa seguridad na ito ay sumasalamin sa kasalukuyang MCP specification (2025-06-18). Palaging i-verify laban sa pinakabagong [opisyal na dokumentasyon](https://spec.modelcontextprotocol.io/) dahil ang mga pamantayan ay patuloy na mabilis na nagbabago.  

**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't sinisikap naming maging tumpak, pakitandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na opisyal na sanggunian. Para sa mahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na maaaring magmula sa paggamit ng pagsasaling ito.