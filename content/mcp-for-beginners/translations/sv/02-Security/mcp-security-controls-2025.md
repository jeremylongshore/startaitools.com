<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T14:54:28+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "sv"
}
-->
# MCP Säkerhetskontroller - Uppdatering augusti 2025

> **Nuvarande standard**: Detta dokument återspeglar säkerhetskraven i [MCP-specifikationen 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) och de officiella [MCP-säkerhetsbästa praxis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) har utvecklats avsevärt med förbättrade säkerhetskontroller som adresserar både traditionella mjukvarusäkerhetsrisker och AI-specifika hot. Detta dokument tillhandahåller omfattande säkerhetskontroller för säkra MCP-implementationer från och med augusti 2025.

## **OBLIGATORISKA säkerhetskrav**

### **Kritiska förbud enligt MCP-specifikationen:**

> **FÖRBJUDET**: MCP-servrar **FÅR INTE** acceptera några tokens som inte uttryckligen har utfärdats för MCP-servern  
>
> **FÖRBJUDET**: MCP-servrar **FÅR INTE** använda sessioner för autentisering  
>
> **KRÄVS**: MCP-servrar som implementerar auktorisering **MÅSTE** verifiera ALLA inkommande förfrågningar  
>
> **OBLIGATORISKT**: MCP-proxyservrar som använder statiska klient-ID:n **MÅSTE** inhämta användarens samtycke för varje dynamiskt registrerad klient  

---

## 1. **Autentiserings- och auktoriseringskontroller**

### **Integration med externa identitetsleverantörer**

**Nuvarande MCP-standard (2025-06-18)** tillåter MCP-servrar att delegera autentisering till externa identitetsleverantörer, vilket innebär en betydande säkerhetsförbättring:

**Säkerhetsfördelar:**
1. **Eliminerar risker med egenutvecklad autentisering**: Minskar sårbarhetsytan genom att undvika egenutvecklade autentiseringslösningar  
2. **Säkerhet på företagsnivå**: Utnyttjar etablerade identitetsleverantörer som Microsoft Entra ID med avancerade säkerhetsfunktioner  
3. **Centraliserad identitetshantering**: Förenklar hantering av användarlivscykler, åtkomstkontroll och efterlevnad  
4. **Multifaktorautentisering**: Ärver MFA-funktioner från företagsidentitetsleverantörer  
5. **Villkorliga åtkomstpolicyer**: Drar nytta av riskbaserade åtkomstkontroller och adaptiv autentisering  

**Implementeringskrav:**
- **Validering av token-målgrupp**: Verifiera att alla tokens uttryckligen är utfärdade för MCP-servern  
- **Verifiering av utfärdare**: Kontrollera att token-utfärdaren matchar den förväntade identitetsleverantören  
- **Signaturverifiering**: Kryptografisk validering av token-integritet  
- **Efterlevnad av utgångsdatum**: Strikt efterlevnad av token-livslängdsgränser  
- **Validering av omfattning**: Säkerställ att tokens innehåller lämpliga behörigheter för begärda operationer  

### **Säkerhet i auktoriseringslogik**

**Kritiska kontroller:**
- **Omfattande auktoriseringsgranskningar**: Regelbundna säkerhetsgranskningar av alla beslutspunkter för auktorisering  
- **Failsafe-standarder**: Nekad åtkomst när auktoriseringslogiken inte kan fatta ett definitivt beslut  
- **Behörighetsgränser**: Tydlig separation mellan olika privilegienivåer och resursåtkomst  
- **Revisionsloggning**: Fullständig loggning av alla auktoriseringsbeslut för säkerhetsövervakning  
- **Regelbundna åtkomstgranskningar**: Periodisk validering av användarbehörigheter och privilegietilldelningar  

## 2. **Tokensäkerhet och skydd mot vidarebefordran**

### **Förhindrande av token-vidarebefordran**

**Token-vidarebefordran är uttryckligen förbjuden** i MCP:s auktoriseringsspecifikation på grund av kritiska säkerhetsrisker:

**Säkerhetsrisker som adresseras:**
- **Kontrollförbigående**: Förbikopplar viktiga säkerhetskontroller som hastighetsbegränsning, begäranvalidering och trafikövervakning  
- **Ansvarsbrist**: Omöjliggör klientidentifiering, vilket förstör granskningsspår och incidentutredningar  
- **Proxybaserad exfiltrering**: Gör det möjligt för skadliga aktörer att använda servrar som proxies för obehörig dataåtkomst  
- **Överträdelse av förtroendegränser**: Bryter nedströms tjänsters förtroende för token-ursprung  
- **Lateral rörelse**: Komprometterade tokens över flera tjänster möjliggör bredare attacker  

**Implementeringskontroller:**
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

### **Säkra tokenhanteringsmönster**

**Bästa praxis:**
- **Kortlivade tokens**: Minimera exponeringsfönstret med frekvent tokenrotation  
- **Just-in-Time-utgivning**: Utfärda tokens endast vid behov för specifika operationer  
- **Säker lagring**: Använd hårdvarusäkerhetsmoduler (HSM) eller säkra nyckelvalv  
- **Tokenbindning**: Binda tokens till specifika klienter, sessioner eller operationer där det är möjligt  
- **Övervakning och varningar**: Realtidsdetektering av tokenmissbruk eller obehöriga åtkomstmönster  

## 3. **Sessionssäkerhetskontroller**

### **Förhindrande av sessionskapning**

**Attackvektorer som adresseras:**
- **Sessionskapning genom promptinjektion**: Skadliga händelser injicerade i delat sessionsläge  
- **Sessionsimitation**: Obehörig användning av stulna sessions-ID:n för att kringgå autentisering  
- **Återupptagningsattacker på strömmar**: Utnyttjande av server-sända händelser för skadlig innehållsinjektion  

**Obligatoriska sessionskontroller:**
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

**Transportskydd:**
- **Tvingande HTTPS**: All sessionskommunikation över TLS 1.3  
- **Säkra cookie-attribut**: HttpOnly, Secure, SameSite=Strict  
- **Certifikatspärrning**: För kritiska anslutningar för att förhindra MITM-attacker  

### **Stateful vs Stateless överväganden**

**För stateful-implementationer:**
- Delat sessionsläge kräver ytterligare skydd mot injektionsattacker  
- Köbaserad sessionshantering behöver integritetsverifiering  
- Flera serverinstanser kräver säker synkronisering av sessionsläge  

**För stateless-implementationer:**
- JWT eller liknande tokenbaserad sessionshantering  
- Kryptografisk verifiering av sessionsintegritet  
- Minskad attackyta men kräver robust tokenvalidering  

## 4. **AI-specifika säkerhetskontroller**

### **Skydd mot promptinjektion**

**Integration med Microsoft Prompt Shields:**
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

**Implementeringskontroller:**
- **Inmatningssanering**: Omfattande validering och filtrering av alla användarinmatningar  
- **Definition av innehållsgränser**: Tydlig separation mellan systeminstruktioner och användarinnehåll  
- **Instruktionshierarki**: Korrekt prioritering av motstridiga instruktioner  
- **Utdataövervakning**: Detektering av potentiellt skadliga eller manipulerade utdata  

### **Skydd mot verktygsförgiftning**

**Säkerhetsramverk för verktyg:**
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

**Dynamisk verktygshantering:**
- **Godkännandeflöden**: Explicit användarsamtycke för verktygsändringar  
- **Återställningsmöjligheter**: Möjlighet att återgå till tidigare verktygsversioner  
- **Ändringsgranskning**: Fullständig historik över ändringar i verktygsdefinitioner  
- **Riskbedömning**: Automatisk utvärdering av verktygets säkerhetsstatus  

## 5. **Skydd mot förvirrade ställföreträdarattacker**

### **OAuth-proxy-säkerhet**

**Attackförebyggande kontroller:**
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

**Implementeringskrav:**
- **Verifiering av användarsamtycke**: Hoppa aldrig över samtyckesskärmar för dynamisk klientregistrering  
- **Validering av omdirigerings-URI**: Strikt vitlistbaserad validering av omdirigeringsdestinationer  
- **Skydd av auktoriseringskoder**: Kortlivade koder med engångsanvändning  
- **Verifiering av klientidentitet**: Robust validering av klientuppgifter och metadata  

## 6. **Säkerhet vid verktygskörning**

### **Sandboxning och isolering**

**Isolering baserad på containrar:**
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

**Processisolering:**
- **Separata processkontexter**: Varje verktygskörning i isolerat processutrymme  
- **Interprocesskommunikation**: Säkra IPC-mekanismer med validering  
- **Processövervakning**: Analys av körningsbeteende och anomalidetektering  
- **Resursbegränsning**: Hårda gränser för CPU, minne och I/O-operationer  

### **Implementering av minst privilegium**

**Behörighetshantering:**
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

## 7. **Säkerhetskontroller för leveranskedjan**

### **Verifiering av beroenden**

**Omfattande komponentkontroll:**
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

### **Kontinuerlig övervakning**

**Hotdetektering i leveranskedjan:**
- **Hälsokontroll av beroenden**: Kontinuerlig bedömning av alla beroenden för säkerhetsproblem  
- **Integration av hotinformation**: Realtidsuppdateringar om framväxande hot i leveranskedjan  
- **Beteendeanalys**: Detektering av ovanligt beteende i externa komponenter  
- **Automatiserat svar**: Omedelbar isolering av komprometterade komponenter  

## 8. **Övervaknings- och detektionskontroller**

### **Säkerhetsinformation och händelsehantering (SIEM)**

**Omfattande loggningsstrategi:**
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

### **Realtidsdetektering av hot**

**Beteendeanalys:**
- **Användarbeteendeanalys (UBA)**: Detektering av ovanliga användaråtkomstmönster  
- **Entitetsbeteendeanalys (EBA)**: Övervakning av MCP-server och verktygsbeteende  
- **Maskininlärningsbaserad anomalidetektering**: AI-driven identifiering av säkerhetshot  
- **Korrelationsanalys av hotinformation**: Matchning av observerade aktiviteter mot kända attackmönster  

## 9. **Incidentrespons och återhämtning**

### **Automatiserade responsmöjligheter**

**Omedelbara åtgärder:**
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

### **Forensiska möjligheter**

**Stöd för utredning:**
- **Bevarande av granskningsspår**: Oföränderlig loggning med kryptografisk integritet  
- **Insamling av bevis**: Automatisk insamling av relevanta säkerhetsartefakter  
- **Rekonstruktion av tidslinje**: Detaljerad sekvens av händelser som ledde till säkerhetsincidenter  
- **Påverkansbedömning**: Utvärdering av omfattningen av kompromissen och dataexponeringen  

## **Viktiga säkerhetsarkitekturprinciper**

### **Djupförsvar**
- **Flera säkerhetslager**: Ingen enskild felpunkt i säkerhetsarkitekturen  
- **Redundanta kontroller**: Överlappande säkerhetsåtgärder för kritiska funktioner  
- **Failsafe-mekanismer**: Säkra standardinställningar vid fel eller attacker  

### **Implementering av Zero Trust**
- **Lita aldrig, verifiera alltid**: Kontinuerlig validering av alla enheter och förfrågningar  
- **Principen om minst privilegium**: Minimala åtkomsträttigheter för alla komponenter  
- **Mikrosegmentering**: Granulära nätverks- och åtkomstkontroller  

### **Kontinuerlig säkerhetsutveckling**
- **Anpassning till hotlandskapet**: Regelbundna uppdateringar för att hantera framväxande hot  
- **Effektivitet i säkerhetskontroller**: Löpande utvärdering och förbättring av kontroller  
- **Efterlevnad av specifikationer**: Anpassning till utvecklande MCP-säkerhetsstandarder  

---

## **Implementeringsresurser**

### **Officiell MCP-dokumentation**
- [MCP-specifikation (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP-säkerhetsbästa praxis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP-auktoriseringsspecifikation](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsofts säkerhetslösningar**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Säkerhetsstandarder**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 för stora språkmodeller](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Viktigt**: Dessa säkerhetskontroller återspeglar den nuvarande MCP-specifikationen (2025-06-18). Verifiera alltid mot den senaste [officiella dokumentationen](https://spec.modelcontextprotocol.io/) eftersom standarder fortsätter att utvecklas snabbt.  

**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, bör det noteras att automatiserade översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess originalspråk bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för eventuella missförstånd eller feltolkningar som uppstår vid användning av denna översättning.