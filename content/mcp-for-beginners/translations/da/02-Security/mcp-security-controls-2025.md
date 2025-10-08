<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T15:18:02+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "da"
}
-->
# MCP Sikkerhedskontroller - August 2025 Opdatering

> **Nuværende Standard**: Dette dokument afspejler [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) sikkerhedskrav og officielle [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) er blevet væsentligt forbedret med avancerede sikkerhedskontroller, der adresserer både traditionelle softwaretrusler og AI-specifikke risici. Dette dokument giver omfattende sikkerhedskontroller for sikre MCP-implementeringer pr. august 2025.

## **OBLIGATORISKE Sikkerhedskrav**

### **Kritiske Forbud fra MCP Specifikationen:**

> **FORBUDT**: MCP-servere **MÅ IKKE** acceptere tokens, der ikke specifikt er udstedt til MCP-serveren  
>
> **FORBUDT**: MCP-servere **MÅ IKKE** bruge sessioner til autentifikation  
>
> **KRÆVET**: MCP-servere, der implementerer autorisation, **SKAL** verificere ALLE indgående anmodninger  
>
> **OBLIGATORISK**: MCP proxy-servere, der bruger statiske klient-ID'er, **SKAL** indhente brugerens samtykke for hver dynamisk registreret klient  

---

## 1. **Autentifikation & Autorisationskontroller**

### **Integration med Eksterne Identitetsudbydere**

**Nuværende MCP Standard (2025-06-18)** tillader MCP-servere at delegere autentifikation til eksterne identitetsudbydere, hvilket repræsenterer en betydelig sikkerhedsforbedring:

**Sikkerhedsfordele:**
1. **Eliminerer Risici ved Egenudviklet Autentifikation**: Reducerer sårbarheder ved at undgå egenudviklede autentifikationsimplementeringer  
2. **Sikkerhed på Enterprise-Niveau**: Udnytter etablerede identitetsudbydere som Microsoft Entra ID med avancerede sikkerhedsfunktioner  
3. **Centraliseret Identitetsstyring**: Forenkler brugerhåndtering, adgangskontrol og compliance-auditering  
4. **Multi-Faktor Autentifikation**: Arver MFA-funktioner fra enterprise identitetsudbydere  
5. **Betingede Adgangspolitikker**: Drager fordel af risikobaseret adgangskontrol og adaptiv autentifikation  

**Implementeringskrav:**
- **Validering af Token Audience**: Verificer, at alle tokens specifikt er udstedt til MCP-serveren  
- **Issuer Validering**: Bekræft, at token-udstederen matcher den forventede identitetsudbyder  
- **Signaturvalidering**: Kryptografisk validering af token-integritet  
- **Håndhævelse af Udløbstid**: Streng håndhævelse af token-livstidsgrænser  
- **Scope Validering**: Sikr, at tokens indeholder passende tilladelser til de ønskede operationer  

### **Sikkerhed i Autorisationslogik**

**Kritiske Kontroller:**
- **Omfattende Autorisationsrevisioner**: Regelmæssige sikkerhedsgennemgange af alle autorisationsbeslutningspunkter  
- **Fail-Safe Defaults**: Nægt adgang, når autorisationslogikken ikke kan træffe en endelig beslutning  
- **Tilladelsesgrænser**: Klar adskillelse mellem forskellige privilegieniveauer og ressourceadgang  
- **Audit Logging**: Fuld logning af alle autorisationsbeslutninger til sikkerhedsovervågning  
- **Regelmæssige Adgangsrevisioner**: Periodisk validering af brugerrettigheder og privilegietildelinger  

## 2. **Token Sikkerhed & Anti-Passthrough Kontroller**

### **Forebyggelse af Token Passthrough**

**Token passthrough er eksplicit forbudt** i MCP Autorisationsspecifikationen på grund af kritiske sikkerhedsrisici:

**Sikkerhedsrisici adresseret:**
- **Omgåelse af Kontroller**: Omgår essentielle sikkerhedskontroller som ratebegrænsning, anmodningsvalidering og trafikovervågning  
- **Manglende Ansvarlighed**: Gør klientidentifikation umulig, hvilket korrumperer audit trails og hændelsesundersøgelser  
- **Proxy-baseret Eksfiltration**: Muliggør, at ondsindede aktører bruger servere som proxyer til uautoriseret dataadgang  
- **Brud på Tillidsgrænser**: Ødelægger downstream serviceforventninger om token-oprindelse  
- **Lateral Bevægelse**: Kompromitterede tokens på tværs af flere tjenester muliggør bredere angreb  

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

### **Sikre Tokenhåndteringsmønstre**

**Best Practices:**
- **Kortlivede Tokens**: Minimer eksponeringsvinduet med hyppig tokenrotation  
- **Just-in-Time Udstedelse**: Udsted tokens kun, når det er nødvendigt for specifikke operationer  
- **Sikker Opbevaring**: Brug hardware sikkerhedsmoduler (HSM'er) eller sikre nøglelagre  
- **Token Binding**: Bind tokens til specifikke klienter, sessioner eller operationer, hvor det er muligt  
- **Overvågning & Alarmering**: Realtidsdetektion af tokenmisbrug eller uautoriserede adgangsmønstre  

## 3. **Session Sikkerhedskontroller**

### **Forebyggelse af Session Hijacking**

**Angrebsvektorer adresseret:**
- **Session Hijack Prompt Injection**: Ondsindede hændelser injiceret i delt sessiontilstand  
- **Session Impersonation**: Uautoriseret brug af stjålne session-ID'er til at omgå autentifikation  
- **Resumable Stream Angreb**: Udnyttelse af server-sendt hændelsesgenoptagelse til ondsindet indholdsinjektion  

**Obligatoriske Sessionkontroller:**
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

**Transport Sikkerhed:**
- **HTTPS Håndhævelse**: Al sessionkommunikation over TLS 1.3  
- **Sikre Cookie Attributter**: HttpOnly, Secure, SameSite=Strict  
- **Certifikat Pinning**: For kritiske forbindelser for at forhindre MITM-angreb  

### **Stateful vs Stateless Overvejelser**

**For Stateful Implementeringer:**
- Delt sessiontilstand kræver ekstra beskyttelse mod injektionsangreb  
- Kø-baseret sessionstyring kræver integritetsverifikation  
- Flere serverinstanser kræver sikker synkronisering af sessiontilstand  

**For Stateless Implementeringer:**
- JWT eller lignende token-baseret sessionstyring  
- Kryptografisk verifikation af sessiontilstands integritet  
- Reduceret angrebsoverflade, men kræver robust tokenvalidering  

## 4. **AI-Specifikke Sikkerhedskontroller**

### **Forsvar mod Prompt Injection**

**Microsoft Prompt Shields Integration:**
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
- **Inputsanitering**: Omfattende validering og filtrering af alle brugerinput  
- **Indholdsgrænse Definition**: Klar adskillelse mellem systeminstruktioner og brugerindhold  
- **Instruktionshierarki**: Korrekte prioritetsregler for modstridende instruktioner  
- **Outputovervågning**: Detektion af potentielt skadelige eller manipulerede outputs  

### **Forebyggelse af Værktøjsforgiftning**

**Værktøjssikkerhedsramme:**
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

**Dynamisk Værktøjsstyring:**
- **Godkendelsesarbejdsgange**: Eksplicit brugeraccept for værktøjsændringer  
- **Rollback Funktioner**: Mulighed for at vende tilbage til tidligere værktøjsversioner  
- **Ændringsrevision**: Fuld historik over værktøjsdefinitionændringer  
- **Risikovurdering**: Automatisk evaluering af værktøjssikkerhed  

## 5. **Forebyggelse af Confused Deputy Angreb**

### **OAuth Proxy Sikkerhed**

**Angrebsforebyggelseskontroller:**
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
- **Brugersamtykke Verifikation**: Spring aldrig samtykkeskærme over for dynamisk klientregistrering  
- **Redirect URI Validering**: Streng validering baseret på whitelist af omdirigeringsdestinationer  
- **Beskyttelse af Autorisationskode**: Kortlivede koder med engangsbrug  
- **Klientidentitetsverifikation**: Robust validering af klientoplysninger og metadata  

## 6. **Sikkerhed for Værktøjsudførelse**

### **Sandboxing & Isolation**

**Containerbaseret Isolation:**
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

**Procesisolation:**
- **Separate Proceskontekster**: Hver værktøjsudførelse i isoleret procesrum  
- **Inter-Process Kommunikation**: Sikker IPC-mekanismer med validering  
- **Procesovervågning**: Analyse af runtime-adfærd og detektion af anomalier  
- **Ressourcehåndhævelse**: Hårde grænser for CPU, hukommelse og I/O-operationer  

### **Implementering af Mindst Mulige Privilegier**

**Tilladelsesstyring:**
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

## 7. **Forsyningskæde Sikkerhedskontroller**

### **Afhængighedsverifikation**

**Omfattende Komponent Sikkerhed:**
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

### **Kontinuerlig Overvågning**

**Trusselsdetektion i Forsyningskæden:**
- **Overvågning af Afhængigheders Sundhed**: Kontinuerlig vurdering af alle afhængigheder for sikkerhedsproblemer  
- **Integration af Trusselsintelligens**: Realtidsopdateringer om nye trusler i forsyningskæden  
- **Adfærdsanalyse**: Detektion af usædvanlig adfærd i eksterne komponenter  
- **Automatisk Respons**: Øjeblikkelig inddæmning af kompromitterede komponenter  

## 8. **Overvågnings- & Detektionskontroller**

### **Security Information and Event Management (SIEM)**

**Omfattende Logningsstrategi:**
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

### **Realtids Trusselsdetektion**

**Adfærdsanalyse:**
- **Brugeradfærdsanalyse (UBA)**: Detektion af usædvanlige brugeradgangsmønstre  
- **Enhedsadfærdsanalyse (EBA)**: Overvågning af MCP-server og værktøjsadfærd  
- **Maskinlæringsbaseret Anomalidetektion**: AI-drevet identifikation af sikkerhedstrusler  
- **Korrelationsanalyse af Trusselsintelligens**: Sammenligning af observerede aktiviteter med kendte angrebsmønstre  

## 9. **Hændelsesrespons & Genopretning**

### **Automatiske Responsfunktioner**

**Øjeblikkelige Responshandlinger:**
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

### **Forensiske Funktioner**

**Undersøgelsesstøtte:**
- **Bevaring af Audit Trails**: Uforanderlig logning med kryptografisk integritet  
- **Bevisindsamling**: Automatisk indsamling af relevante sikkerhedsartefakter  
- **Tidslinjerekonstruktion**: Detaljeret sekvens af begivenheder, der førte til sikkerhedshændelser  
- **Vurdering af Indvirkning**: Evaluering af kompromisets omfang og dataeksponering  

## **Vigtige Principper for Sikkerhedsarkitektur**

### **Forsvar i Dybdens**
- **Flere Sikkerhedslag**: Ingen enkelt fejlpunkt i sikkerhedsarkitekturen  
- **Redundante Kontroller**: Overlappende sikkerhedsforanstaltninger for kritiske funktioner  
- **Fail-Safe Mekanismer**: Sikker standardadfærd ved fejl eller angreb  

### **Zero Trust Implementering**
- **Aldrig Stol, Altid Verificer**: Kontinuerlig validering af alle enheder og anmodninger  
- **Princip om Mindst Mulige Privilegier**: Minimal adgangsret for alle komponenter  
- **Mikrosegmentering**: Granulære netværks- og adgangskontroller  

### **Kontinuerlig Sikkerhedsudvikling**
- **Tilpasning til Trusselslandskab**: Regelmæssige opdateringer for at adressere nye trusler  
- **Effektivitet af Sikkerhedskontroller**: Løbende evaluering og forbedring af kontroller  
- **Specifikationsoverholdelse**: Overensstemmelse med udviklende MCP-sikkerhedsstandarder  

---

## **Implementeringsressourcer**

### **Officiel MCP Dokumentation**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Sikkerhedsløsninger**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Sikkerhedsstandarder**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Vigtigt**: Disse sikkerhedskontroller afspejler den nuværende MCP-specifikation (2025-06-18). Verificer altid mod den seneste [officielle dokumentation](https://spec.modelcontextprotocol.io/), da standarder udvikler sig hurtigt.

**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi er ikke ansvarlige for eventuelle misforståelser eller fejltolkninger, der måtte opstå som følge af brugen af denne oversættelse.