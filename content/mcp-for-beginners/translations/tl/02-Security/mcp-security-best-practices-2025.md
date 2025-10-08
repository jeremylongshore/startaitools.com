<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T18:17:25+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "tl"
}
-->
# MCP Mga Pinakamahusay na Kasanayan sa Seguridad - Update noong Agosto 2025

> **Mahalaga**: Ang dokumentong ito ay sumasalamin sa pinakabagong [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) na mga kinakailangan sa seguridad at opisyal na [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Palaging sumangguni sa kasalukuyang spesipikasyon para sa pinakabagong gabay.

## Mahahalagang Kasanayan sa Seguridad para sa MCP Implementations

Ang Model Context Protocol ay nagdadala ng mga natatanging hamon sa seguridad na lampas sa tradisyunal na seguridad ng software. Ang mga kasanayang ito ay tumutugon sa parehong mga pangunahing kinakailangan sa seguridad at mga banta na partikular sa MCP tulad ng prompt injection, tool poisoning, session hijacking, confused deputy problems, at token passthrough vulnerabilities.

### **KINAKAILANGANG Mga Kinakailangan sa Seguridad**

**Mga Kritikal na Kinakailangan mula sa MCP Specification:**

> **HINDI DAPAT**: Ang mga MCP server **HINDI DAPAT** tumanggap ng anumang mga token na hindi tahasang inisyu para sa MCP server  
> 
> **DAPAT**: Ang mga MCP server na nagpapatupad ng authorization **DAPAT** i-verify ang LAHAT ng papasok na mga kahilingan  
>  
> **HINDI DAPAT**: Ang mga MCP server **HINDI DAPAT** gumamit ng mga session para sa authentication  
>
> **DAPAT**: Ang mga MCP proxy server na gumagamit ng static client IDs **DAPAT** kumuha ng pahintulot ng user para sa bawat dinamikong nakarehistrong client  

---

## 1. **Seguridad ng Token at Authentication**

**Mga Kontrol sa Authentication at Authorization:**  
   - **Masusing Pagsusuri ng Authorization**: Magsagawa ng komprehensibong pagsusuri sa authorization logic ng MCP server upang matiyak na ang mga intended na user at client lamang ang may access sa mga resources  
   - **Pagsasama ng Panlabas na Identity Provider**: Gumamit ng mga kilalang identity provider tulad ng Microsoft Entra ID sa halip na magpatupad ng custom na authentication  
   - **Pagpapatunay ng Token Audience**: Palaging tiyakin na ang mga token ay tahasang inisyu para sa iyong MCP server - huwag kailanman tumanggap ng upstream tokens  
   - **Wastong Lifecycle ng Token**: Magpatupad ng secure na token rotation, expiration policies, at pigilan ang token replay attacks  

**Protektadong Imbakan ng Token:**  
   - Gumamit ng Azure Key Vault o katulad na secure credential stores para sa lahat ng mga lihim  
   - Magpatupad ng encryption para sa mga token parehong nakaimbak at nasa transit  
   - Regular na pag-ikot ng mga kredensyal at pagsubaybay para sa hindi awtorisadong access  

## 2. **Pamamahala ng Session at Seguridad ng Transportasyon**

**Mga Praktika sa Secure Session:**  
   - **Cryptographically Secure Session IDs**: Gumamit ng secure, non-deterministic session IDs na nabuo gamit ang secure random number generators  
   - **Pag-bind sa User-Specific**: I-bind ang session IDs sa mga user identities gamit ang mga format tulad ng `<user_id>:<session_id>` upang maiwasan ang cross-user session abuse  
   - **Pamamahala ng Lifecycle ng Session**: Magpatupad ng wastong expiration, rotation, at invalidation upang limitahan ang mga bintana ng kahinaan  
   - **Pagpapatupad ng HTTPS/TLS**: Mandatoryong HTTPS para sa lahat ng komunikasyon upang maiwasan ang interception ng session ID  

**Seguridad ng Transport Layer:**  
   - I-configure ang TLS 1.3 kung maaari gamit ang wastong pamamahala ng sertipiko  
   - Magpatupad ng certificate pinning para sa mga kritikal na koneksyon  
   - Regular na pag-ikot ng sertipiko at pagpapatunay ng bisa  

## 3. **Proteksyon Laban sa Mga Banta na Kaugnay sa AI** 🤖

**Depensa Laban sa Prompt Injection:**  
   - **Microsoft Prompt Shields**: Mag-deploy ng AI Prompt Shields para sa advanced na pagtuklas at pag-filter ng mga malisyosong utos  
   - **Input Sanitization**: I-validate at i-sanitize ang lahat ng inputs upang maiwasan ang injection attacks at confused deputy problems  
   - **Mga Hangganan ng Nilalaman**: Gumamit ng delimiter at datamarking systems upang makilala ang pagitan ng mga trusted instructions at external content  

**Pag-iwas sa Tool Poisoning:**  
   - **Pagpapatunay ng Metadata ng Tool**: Magpatupad ng integrity checks para sa mga tool definitions at subaybayan ang mga hindi inaasahang pagbabago  
   - **Dynamic Tool Monitoring**: Subaybayan ang runtime behavior at mag-set up ng alerting para sa mga hindi inaasahang pattern ng execution  
   - **Approval Workflows**: Mangailangan ng tahasang pag-apruba ng user para sa mga pagbabago sa tool at kakayahan  

## 4. **Kontrol sa Access at Mga Pahintulot**

**Prinsipyo ng Pinakamababang Pribilehiyo:**  
   - Bigyan ang mga MCP server ng minimum na mga pahintulot na kinakailangan para sa intended functionality  
   - Magpatupad ng role-based access control (RBAC) na may fine-grained permissions  
   - Regular na pagsusuri ng mga pahintulot at tuloy-tuloy na pagsubaybay para sa privilege escalation  

**Mga Kontrol sa Pahintulot sa Runtime:**  
   - Magpatupad ng mga limitasyon sa resources upang maiwasan ang resource exhaustion attacks  
   - Gumamit ng container isolation para sa mga tool execution environments  
   - Magpatupad ng just-in-time access para sa mga administrative functions  

## 5. **Seguridad ng Nilalaman at Pagsubaybay**

**Pagpapatupad ng Seguridad ng Nilalaman:**  
   - **Azure Content Safety Integration**: Gumamit ng Azure Content Safety upang matukoy ang mapanganib na nilalaman, jailbreak attempts, at mga paglabag sa patakaran  
   - **Behavioral Analysis**: Magpatupad ng runtime behavioral monitoring upang matukoy ang mga anomalya sa MCP server at tool execution  
   - **Komprehensibong Pag-log**: I-log ang lahat ng authentication attempts, tool invocations, at mga security events gamit ang secure, tamper-proof storage  

**Tuloy-tuloy na Pagsubaybay:**  
   - Real-time alerting para sa mga kahina-hinalang pattern at hindi awtorisadong access attempts  
   - Pagsasama sa mga SIEM systems para sa centralized security event management  
   - Regular na security audits at penetration testing ng MCP implementations  

## 6. **Seguridad ng Supply Chain**

**Pagpapatunay ng Component:**  
   - **Dependency Scanning**: Gumamit ng automated vulnerability scanning para sa lahat ng software dependencies at AI components  
   - **Provenance Validation**: I-verify ang pinagmulan, lisensya, at integridad ng mga modelo, data sources, at external services  
   - **Signed Packages**: Gumamit ng cryptographically signed packages at i-verify ang mga signature bago ang deployment  

**Secure Development Pipeline:**  
   - **GitHub Advanced Security**: Magpatupad ng secret scanning, dependency analysis, at CodeQL static analysis  
   - **CI/CD Security**: Isama ang security validation sa buong automated deployment pipelines  
   - **Artifact Integrity**: Magpatupad ng cryptographic verification para sa mga deployed artifacts at configurations  

## 7. **Seguridad ng OAuth at Pag-iwas sa Confused Deputy**

**Implementasyon ng OAuth 2.1:**  
   - **PKCE Implementation**: Gumamit ng Proof Key for Code Exchange (PKCE) para sa lahat ng authorization requests  
   - **Explicit Consent**: Kumuha ng pahintulot ng user para sa bawat dinamikong nakarehistrong client upang maiwasan ang confused deputy attacks  
   - **Redirect URI Validation**: Magpatupad ng mahigpit na validation ng redirect URIs at client identifiers  

**Seguridad ng Proxy:**  
   - Pigilan ang authorization bypass sa pamamagitan ng static client ID exploitation  
   - Magpatupad ng wastong consent workflows para sa third-party API access  
   - Subaybayan ang pagnanakaw ng authorization code at hindi awtorisadong API access  

## 8. **Pagtugon sa Insidente at Pagbawi**

**Kakayahan sa Mabilis na Pagtugon:**  
   - **Automated Response**: Magpatupad ng automated systems para sa credential rotation at threat containment  
   - **Rollback Procedures**: Kakayahang mabilis na bumalik sa mga kilalang mabuting configurations at components  
   - **Forensic Capabilities**: Detalyadong audit trails at pag-log para sa pagsisiyasat ng insidente  

**Komunikasyon at Koordinasyon:**  
   - Malinaw na mga pamamaraan ng escalation para sa mga insidente sa seguridad  
   - Pagsasama sa mga pang-organisasyong incident response teams  
   - Regular na simulations ng insidente sa seguridad at tabletop exercises  

## 9. **Pagsunod at Pamamahala**

**Pagsunod sa Regulasyon:**  
   - Tiyakin na ang mga MCP implementations ay nakakatugon sa mga kinakailangan ng industriya (GDPR, HIPAA, SOC 2)  
   - Magpatupad ng data classification at privacy controls para sa AI data processing  
   - Panatilihin ang komprehensibong dokumentasyon para sa compliance auditing  

**Pamamahala ng Pagbabago:**  
   - Pormal na mga proseso ng pagsusuri sa seguridad para sa lahat ng pagbabago sa MCP system  
   - Version control at approval workflows para sa mga pagbabago sa configuration  
   - Regular na compliance assessments at gap analysis  

## 10. **Mga Advanced na Kontrol sa Seguridad**

**Zero Trust Architecture:**  
   - **Never Trust, Always Verify**: Tuloy-tuloy na pagpapatunay ng mga user, devices, at koneksyon  
   - **Micro-segmentation**: Granular network controls na naghihiwalay sa mga indibidwal na MCP components  
   - **Conditional Access**: Risk-based access controls na umaangkop sa kasalukuyang konteksto at pag-uugali  

**Proteksyon sa Runtime Application:**  
   - **Runtime Application Self-Protection (RASP)**: Mag-deploy ng RASP techniques para sa real-time threat detection  
   - **Application Performance Monitoring**: Subaybayan ang mga performance anomalies na maaaring magpahiwatig ng mga pag-atake  
   - **Dynamic Security Policies**: Magpatupad ng mga security policies na umaangkop batay sa kasalukuyang threat landscape  

## 11. **Pagsasama ng Microsoft Security Ecosystem**

**Komprehensibong Microsoft Security:**  
   - **Microsoft Defender for Cloud**: Pamamahala ng cloud security posture para sa MCP workloads  
   - **Azure Sentinel**: Cloud-native SIEM at SOAR capabilities para sa advanced threat detection  
   - **Microsoft Purview**: Pamamahala ng data governance at pagsunod para sa AI workflows at data sources  

**Pamamahala ng Identity at Access:**  
   - **Microsoft Entra ID**: Pamamahala ng enterprise identity na may conditional access policies  
   - **Privileged Identity Management (PIM)**: Just-in-time access at approval workflows para sa mga administrative functions  
   - **Identity Protection**: Risk-based conditional access at automated threat response  

## 12. **Tuloy-tuloy na Ebolusyon ng Seguridad**

**Pananatiling Napapanahon:**  
   - **Specification Monitoring**: Regular na pagsusuri ng mga update sa MCP specification at mga pagbabago sa security guidance  
   - **Threat Intelligence**: Pagsasama ng AI-specific threat feeds at indicators of compromise  
   - **Security Community Engagement**: Aktibong pakikilahok sa MCP security community at vulnerability disclosure programs  

**Adaptive Security:**  
   - **Machine Learning Security**: Gumamit ng ML-based anomaly detection para matukoy ang mga bagong pattern ng pag-atake  
   - **Predictive Security Analytics**: Magpatupad ng predictive models para sa proactive threat identification  
   - **Security Automation**: Automated security policy updates batay sa threat intelligence at mga pagbabago sa spesipikasyon  

---

## **Mga Kritikal na Mapagkukunan sa Seguridad**

### **Opisyal na Dokumentasyon ng MCP**  
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Security Solutions**  
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Security](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Mga Pamantayan sa Seguridad**  
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Mga Gabay sa Implementasyon**  
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Paalala sa Seguridad**: Ang mga kasanayan sa seguridad ng MCP ay mabilis na nagbabago. Palaging i-verify laban sa kasalukuyang [MCP specification](https://spec.modelcontextprotocol.io/) at [opisyal na dokumentasyon sa seguridad](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) bago ang implementasyon.

**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't sinisikap naming maging tumpak, pakitandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na opisyal na sanggunian. Para sa mahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na maaaring magmula sa paggamit ng pagsasaling ito.