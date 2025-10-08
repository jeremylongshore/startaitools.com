<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T18:21:10+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "tl"
}
-->
# Mga Pinakamahusay na Praktika sa Seguridad ng MCP 2025

Ang komprehensibong gabay na ito ay naglalahad ng mahahalagang pinakamahusay na praktika sa seguridad para sa pagpapatupad ng mga sistema ng Model Context Protocol (MCP) batay sa pinakabagong **MCP Specification 2025-06-18** at kasalukuyang mga pamantayan ng industriya. Ang mga praktika na ito ay tumutugon sa parehong tradisyunal na mga alalahanin sa seguridad at mga banta na partikular sa AI na natatangi sa mga deployment ng MCP.

## Mahahalagang Kinakailangan sa Seguridad

### Mga Mandatoryong Kontrol sa Seguridad (MUST Requirements)

1. **Token Validation**: Ang mga MCP server **HINDI DAPAT** tumanggap ng anumang token na hindi partikular na inisyu para sa MCP server mismo.
2. **Authorization Verification**: Ang mga MCP server na nagpapatupad ng awtorisasyon **DAPAT** i-verify ang LAHAT ng papasok na kahilingan at **HINDI DAPAT** gumamit ng mga session para sa authentication.  
3. **User Consent**: Ang mga MCP proxy server na gumagamit ng static client IDs **DAPAT** kumuha ng malinaw na pahintulot ng user para sa bawat dinamikong nakarehistrong kliyente.
4. **Secure Session IDs**: Ang mga MCP server **DAPAT** gumamit ng cryptographically secure, non-deterministic session IDs na nabuo gamit ang secure random number generators.

## Mga Pangunahing Praktika sa Seguridad

### 1. Pag-validate at Pag-sanitize ng Input
- **Komprehensibong Pag-validate ng Input**: I-validate at i-sanitize ang lahat ng input upang maiwasan ang injection attacks, confused deputy problems, at prompt injection vulnerabilities.
- **Parameter Schema Enforcement**: Magpatupad ng mahigpit na JSON schema validation para sa lahat ng tool parameters at API inputs.
- **Content Filtering**: Gumamit ng Microsoft Prompt Shields at Azure Content Safety upang salain ang malisyosong nilalaman sa mga prompt at tugon.
- **Output Sanitization**: I-validate at i-sanitize ang lahat ng output ng modelo bago ipakita sa mga user o downstream systems.

### 2. Kahusayan sa Authentication at Authorization  
- **External Identity Providers**: I-delegate ang authentication sa mga kilalang identity provider (Microsoft Entra ID, OAuth 2.1 providers) sa halip na magpatupad ng custom authentication.
- **Fine-grained Permissions**: Magpatupad ng granular, tool-specific permissions na sumusunod sa prinsipyo ng least privilege.
- **Token Lifecycle Management**: Gumamit ng short-lived access tokens na may secure rotation at tamang audience validation.
- **Multi-Factor Authentication**: I-require ang MFA para sa lahat ng administrative access at sensitibong operasyon.

### 3. Mga Secure na Protocol sa Komunikasyon
- **Transport Layer Security**: Gumamit ng HTTPS/TLS 1.3 para sa lahat ng komunikasyon ng MCP na may tamang certificate validation.
- **End-to-End Encryption**: Magpatupad ng karagdagang encryption layers para sa lubos na sensitibong data habang nasa transit at nakaimbak.
- **Certificate Management**: Panatilihin ang tamang certificate lifecycle management na may automated renewal processes.
- **Protocol Version Enforcement**: Gumamit ng kasalukuyang bersyon ng MCP protocol (2025-06-18) na may tamang version negotiation.

### 4. Advanced Rate Limiting at Proteksyon ng Resource
- **Multi-layer Rate Limiting**: Magpatupad ng rate limiting sa antas ng user, session, tool, at resource upang maiwasan ang pang-aabuso.
- **Adaptive Rate Limiting**: Gumamit ng machine learning-based rate limiting na umaangkop sa mga pattern ng paggamit at mga indikasyon ng banta.
- **Resource Quota Management**: Magtakda ng angkop na limitasyon para sa computational resources, memory usage, at execution time.
- **DDoS Protection**: Mag-deploy ng komprehensibong DDoS protection at traffic analysis systems.

### 5. Komprehensibong Logging at Monitoring
- **Structured Audit Logging**: Magpatupad ng detalyado, searchable logs para sa lahat ng operasyon ng MCP, tool executions, at mga kaganapan sa seguridad.
- **Real-time Security Monitoring**: Mag-deploy ng SIEM systems na may AI-powered anomaly detection para sa mga workload ng MCP.
- **Privacy-compliant Logging**: Mag-log ng mga kaganapan sa seguridad habang iginagalang ang mga kinakailangan sa privacy ng data at regulasyon.
- **Incident Response Integration**: Ikonekta ang mga logging system sa mga automated incident response workflows.

### 6. Pinahusay na Praktika sa Secure Storage
- **Hardware Security Modules**: Gumamit ng HSM-backed key storage (Azure Key Vault, AWS CloudHSM) para sa mga kritikal na cryptographic operations.
- **Encryption Key Management**: Magpatupad ng tamang key rotation, segregation, at access controls para sa encryption keys.
- **Secrets Management**: I-imbak ang lahat ng API keys, tokens, at credentials sa mga dedikadong secret management systems.
- **Data Classification**: I-classify ang data batay sa antas ng sensitivity at magpatupad ng angkop na mga hakbang sa proteksyon.

### 7. Advanced Token Management
- **Token Passthrough Prevention**: Tahasang ipagbawal ang mga token passthrough patterns na bypass sa mga kontrol sa seguridad.
- **Audience Validation**: Palaging i-verify ang mga token audience claims na tumutugma sa intended MCP server identity.
- **Claims-based Authorization**: Magpatupad ng fine-grained authorization batay sa token claims at user attributes.
- **Token Binding**: I-bind ang mga token sa partikular na session, user, o device kung naaangkop.

### 8. Secure Session Management
- **Cryptographic Session IDs**: Bumuo ng session IDs gamit ang cryptographically secure random number generators (hindi predictable sequences).
- **User-specific Binding**: I-bind ang session IDs sa user-specific information gamit ang secure formats tulad ng `<user_id>:<session_id>`.
- **Session Lifecycle Controls**: Magpatupad ng tamang session expiration, rotation, at invalidation mechanisms.
- **Session Security Headers**: Gumamit ng angkop na HTTP security headers para sa proteksyon ng session.

### 9. Mga Kontrol sa Seguridad na Partikular sa AI
- **Prompt Injection Defense**: Mag-deploy ng Microsoft Prompt Shields na may spotlighting, delimiters, at datamarking techniques.
- **Tool Poisoning Prevention**: I-validate ang metadata ng tool, i-monitor ang mga dinamikong pagbabago, at i-verify ang integridad ng tool.
- **Model Output Validation**: I-scan ang mga output ng modelo para sa potensyal na data leakage, mapanganib na nilalaman, o paglabag sa mga patakaran sa seguridad.
- **Context Window Protection**: Magpatupad ng mga kontrol upang maiwasan ang context window poisoning at manipulation attacks.

### 10. Seguridad sa Pagpapatupad ng Tool
- **Execution Sandboxing**: Patakbuhin ang mga tool executions sa containerized, isolated environments na may resource limits.
- **Privilege Separation**: Patakbuhin ang mga tool na may minimal na kinakailangang pribilehiyo at hiwalay na service accounts.
- **Network Isolation**: Magpatupad ng network segmentation para sa mga tool execution environments.
- **Execution Monitoring**: I-monitor ang tool execution para sa anomalous behavior, resource usage, at mga paglabag sa seguridad.

### 11. Patuloy na Pag-validate ng Seguridad
- **Automated Security Testing**: Isama ang security testing sa CI/CD pipelines gamit ang mga tool tulad ng GitHub Advanced Security.
- **Vulnerability Management**: Regular na i-scan ang lahat ng dependencies, kabilang ang mga AI models at external services.
- **Penetration Testing**: Magsagawa ng regular na security assessments na partikular na tumutok sa mga implementasyon ng MCP.
- **Security Code Reviews**: Magpatupad ng mandatory security reviews para sa lahat ng pagbabago sa code na may kaugnayan sa MCP.

### 12. Seguridad ng Supply Chain para sa AI
- **Component Verification**: I-verify ang provenance, integridad, at seguridad ng lahat ng AI components (models, embeddings, APIs).
- **Dependency Management**: Panatilihin ang kasalukuyang imbentaryo ng lahat ng software at AI dependencies na may vulnerability tracking.
- **Trusted Repositories**: Gumamit ng verified, trusted sources para sa lahat ng AI models, libraries, at tools.
- **Supply Chain Monitoring**: Patuloy na i-monitor ang mga kompromiso sa AI service providers at model repositories.

## Mga Advanced na Pattern sa Seguridad

### Zero Trust Architecture para sa MCP
- **Never Trust, Always Verify**: Magpatupad ng tuloy-tuloy na pag-verify para sa lahat ng MCP participants.
- **Micro-segmentation**: I-isolate ang mga MCP components na may granular network at identity controls.
- **Conditional Access**: Magpatupad ng risk-based access controls na umaangkop sa konteksto at pag-uugali.
- **Continuous Risk Assessment**: Dinamikong suriin ang security posture batay sa kasalukuyang mga indikasyon ng banta.

### Privacy-Preserving AI Implementation
- **Data Minimization**: I-expose lamang ang minimum na kinakailangang data para sa bawat operasyon ng MCP.
- **Differential Privacy**: Magpatupad ng privacy-preserving techniques para sa sensitibong data processing.
- **Homomorphic Encryption**: Gumamit ng advanced encryption techniques para sa secure computation sa encrypted data.
- **Federated Learning**: Magpatupad ng distributed learning approaches na pinapanatili ang data locality at privacy.

### Incident Response para sa AI Systems
- **AI-Specific Incident Procedures**: Bumuo ng mga incident response procedures na iniakma sa mga banta na partikular sa AI at MCP.
- **Automated Response**: Magpatupad ng automated containment at remediation para sa mga karaniwang insidente sa seguridad ng AI.  
- **Forensic Capabilities**: Panatilihin ang forensic readiness para sa mga kompromiso sa AI system at data breaches.
- **Recovery Procedures**: Magtatag ng mga pamamaraan para sa pag-recover mula sa AI model poisoning, prompt injection attacks, at service compromises.

## Mga Mapagkukunan sa Implementasyon at Pamantayan

### Opisyal na Dokumentasyon ng MCP
- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Kasalukuyang MCP protocol specification
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Opisyal na gabay sa seguridad
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Mga pattern sa authentication at authorization
- [MCP Transport Security](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Mga kinakailangan sa transport layer security

### Microsoft Security Solutions
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Advanced na proteksyon laban sa prompt injection
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Komprehensibong AI content filtering
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Pamamahala sa enterprise identity at access
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Secure secrets at credential management
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Supply chain at code security scanning

### Mga Pamantayan sa Seguridad at Frameworks
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Kasalukuyang gabay sa seguridad ng OAuth
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Mga panganib sa seguridad ng web application
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Mga panganib sa seguridad na partikular sa AI
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Komprehensibong pamamahala sa panganib ng AI
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Mga sistema sa pamamahala ng seguridad ng impormasyon

### Mga Gabay sa Implementasyon at Tutorials
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Mga pattern sa enterprise authentication
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Pagsasama ng identity provider
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Mga pinakamahusay na praktika sa pamamahala ng token
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Mga advanced na pattern sa encryption

### Mga Advanced na Mapagkukunan sa Seguridad
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Mga praktika sa secure development
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - Pagsubok sa seguridad na partikular sa AI
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodolohiya sa threat modeling ng AI
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Mga teknolohiya sa privacy-preserving AI

### Pagsunod at Pamamahala
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Pagsunod sa privacy sa mga sistema ng AI
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Responsable na implementasyon ng AI
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Mga kontrol sa seguridad para sa mga AI service provider
- [HIPAA Compliance for AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Mga kinakailangan sa pagsunod ng AI sa healthcare

### DevSecOps at Automation
- [DevSecOps Pipeline for AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Mga secure na pipeline sa pag-develop ng AI
- [Automated Security Testing](https://learn.microsoft.com/security/engineering/devsecops) - Patuloy na pag-validate ng seguridad
- [Infrastructure as Code Security](https://learn.microsoft.com/security/engineering/infrastructure-security) - Secure na deployment ng infrastructure
- [Container Security for AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Seguridad sa containerization ng workload ng AI

### Monitoring at Incident Response  
- [Azure Monitor for AI Workloads](https://learn.microsoft.com/azure/azure-monitor/overview) - Komprehensibong solusyon sa monitoring
- [AI Security Incident Response](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Mga pamamaraan sa insidente na partikular sa AI
- [SIEM for AI Systems](https://learn.microsoft.com/azure/sentinel/overview) - Security information at event management
- [Threat Intelligence for AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Mga mapagkukunan ng threat intelligence para sa AI

## 🔄 Patuloy na Pagpapabuti

### Manatiling Napapanahon sa Ebolusyon ng Pamantayan
- **MCP Specification Updates**: Subaybayan ang mga opisyal na pagbabago sa MCP specification at mga security advisories.
- **Threat Intelligence**: Mag-subscribe sa mga AI security threat feeds at vulnerability databases.  
- **Community Engagement**: Makilahok sa mga talakayan ng komunidad sa seguridad ng MCP at mga working groups.
- **Regular Assessment**: Magsagawa ng quarterly security posture assessments at i-update ang mga praktika nang naaayon.

### Pag-aambag sa Seguridad ng MCP
- **Security Research**: Mag-ambag sa pananaliksik sa seguridad ng MCP at mga programa sa pag-disclose ng vulnerability.
- **Best Practice Sharing**: Ibahagi ang mga implementasyon sa seguridad at mga natutunan sa komunidad.
- **Standard Development**: Makilahok sa pag-develop ng MCP specification at paglikha ng mga pamantayan sa seguridad.
- **Pagbuo ng Kasangkapan**: Bumuo at ibahagi ang mga kasangkapan at aklatan para sa seguridad ng MCP ecosystem

---

*Ang dokumentong ito ay sumasalamin sa mga pinakamahusay na kasanayan sa seguridad ng MCP noong Agosto 18, 2025, batay sa MCP Specification 2025-06-18. Ang mga kasanayan sa seguridad ay dapat regular na suriin at i-update habang ang protocol at tanawin ng banta ay patuloy na nagbabago.*

**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't sinisikap naming maging tumpak, pakitandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa kanyang orihinal na wika ang dapat ituring na opisyal na sanggunian. Para sa mahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na maaaring magmula sa paggamit ng pagsasaling ito.