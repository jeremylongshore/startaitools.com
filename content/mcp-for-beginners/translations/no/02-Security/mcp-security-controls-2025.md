<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T15:43:47+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "no"
}
-->
# MCP Sikkerhetskontroller - Oppdatering August 2025

> **Gjeldende Standard**: Dette dokumentet reflekterer [MCP Spesifikasjon 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) sikkerhetskrav og offisielle [MCP Sikkerhetsbestepraksis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) har utviklet seg betydelig med forbedrede sikkerhetskontroller som adresserer både tradisjonell programvaresikkerhet og AI-spesifikke trusler. Dette dokumentet gir omfattende sikkerhetskontroller for sikre MCP-implementeringer per august 2025.

## **OBLIGATORISKE Sikkerhetskrav**

### **Kritiske Forbud fra MCP Spesifikasjon:**

> **FORBUDT**: MCP-servere **MÅ IKKE** akseptere noen tokens som ikke eksplisitt er utstedt for MCP-serveren  
>
> **FORBUDT**: MCP-servere **MÅ IKKE** bruke sesjoner for autentisering  
>
> **PÅKREVD**: MCP-servere som implementerer autorisasjon **MÅ** verifisere ALLE innkommende forespørsler  
>
> **OBLIGATORISK**: MCP proxy-servere som bruker statiske klient-IDer **MÅ** innhente brukerens samtykke for hver dynamisk registrerte klient  

---

## 1. **Autentisering & Autorisasjonskontroller**

### **Integrasjon med Ekstern Identitetsleverandør**

**Gjeldende MCP Standard (2025-06-18)** tillater MCP-servere å delegere autentisering til eksterne identitetsleverandører, noe som representerer en betydelig sikkerhetsforbedring:

**Sikkerhetsfordeler:**
1. **Eliminerer Risiko ved Egendefinert Autentisering**: Reduserer sårbarhet ved å unngå egendefinerte autentiseringsimplementasjoner  
2. **Sikkerhet på Enterprise-Nivå**: Utnytter etablerte identitetsleverandører som Microsoft Entra ID med avanserte sikkerhetsfunksjoner  
3. **Sentralisert Identitetsadministrasjon**: Forenkler administrasjon av brukerens livssyklus, tilgangskontroll og samsvarsrevisjoner  
4. **Flerfaktorautentisering**: Arver MFA-funksjonalitet fra enterprise identitetsleverandører  
5. **Betingede Tilgangspolicyer**: Drar nytte av risikobasert tilgangskontroll og adaptiv autentisering  

**Implementeringskrav:**
- **Validering av Token Audience**: Verifiser at alle tokens eksplisitt er utstedt for MCP-serveren  
- **Issuer-verifisering**: Bekreft at token-utsteder samsvarer med forventet identitetsleverandør  
- **Signaturverifisering**: Kryptografisk validering av token-integritet  
- **Håndheving av Utløp**: Streng håndheving av token-livstidsgrenser  
- **Validering av Scope**: Sørg for at tokens inneholder passende tillatelser for forespurte operasjoner  

### **Sikkerhet i Autorisasjonslogikk**

**Kritiske Kontroller:**
- **Omfattende Autorisasjonsrevisjoner**: Regelmessige sikkerhetsgjennomganger av alle autorisasjonsbeslutningspunkter  
- **Fail-Safe Defaults**: Avslå tilgang når autorisasjonslogikken ikke kan ta en definitiv beslutning  
- **Tillatelsesgrenser**: Klar separasjon mellom ulike privilegienivåer og ressursadgang  
- **Revisjonslogging**: Fullstendig logging av alle autorisasjonsbeslutninger for sikkerhetsovervåking  
- **Regelmessige Tilgangsrevisjoner**: Periodisk validering av brukerrettigheter og privilegietildelinger  

## 2. **Token Sikkerhet & Anti-Passthrough Kontroller**

### **Forebygging av Token Passthrough**

**Token passthrough er eksplisitt forbudt** i MCP Autorisasjonsspesifikasjonen på grunn av kritiske sikkerhetsrisikoer:

**Sikkerhetsrisikoer adressert:**
- **Omgåelse av Kontroller**: Omgår essensielle sikkerhetskontroller som hastighetsbegrensning, forespørselsvalidering og trafikkovervåking  
- **Ansvarsbrudd**: Gjør klientidentifikasjon umulig, korrumperer revisjonsspor og hendelsesundersøkelser  
- **Proxy-basert Eksfiltrering**: Lar ondsinnede aktører bruke servere som proxyer for uautorisert dataadgang  
- **Brudd på Tillitsgrenser**: Ødelegger antagelser om token-opprinnelse i nedstrøms tjenester  
- **Lateral Bevegelse**: Kompromitterte tokens på tvers av flere tjenester muliggjør bredere angrepsutvidelse  

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

**Beste Praksis:**
- **Kortlevde Tokens**: Minimer eksponeringsvinduet med hyppig tokenrotasjon  
- **Just-in-Time Utstedelse**: Utsted tokens kun når det er nødvendig for spesifikke operasjoner  
- **Sikker Lagring**: Bruk maskinvare sikkerhetsmoduler (HSM) eller sikre nøkkelhvelv  
- **Token Binding**: Bind tokens til spesifikke klienter, sesjoner eller operasjoner der det er mulig  
- **Overvåking & Varsling**: Sanntidsdeteksjon av tokenmisbruk eller uautoriserte tilgangsmønstre  

## 3. **Sesjonssikkerhetskontroller**

### **Forebygging av Sesjonshijacking**

**Angrepsvektorer adressert:**
- **Sesjonshijacking via Prompt Injection**: Ondsinnede hendelser injisert i delt sesjonstilstand  
- **Sesjonsimitasjon**: Uautorisert bruk av stjålne sesjons-IDer for å omgå autentisering  
- **Angrep på Resumerbare Strømmer**: Utnyttelse av server-sendt hendelsesgjenopptakelse for ondsinnet innholdsinjeksjon  

**Obligatoriske Sesjonskontroller:**
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

**Transport Sikkerhet:**
- **HTTPS Håndheving**: All sesjonskommunikasjon over TLS 1.3  
- **Sikre Cookie Attributter**: HttpOnly, Secure, SameSite=Strict  
- **Sertifikatpinnering**: For kritiske forbindelser for å forhindre MITM-angrep  

### **Stateful vs Stateless Betraktninger**

**For Stateful Implementeringer:**
- Delt sesjonstilstand krever ekstra beskyttelse mot injeksjonsangrep  
- Købasert sesjonshåndtering trenger integritetsverifisering  
- Flere serverinstanser krever sikker synkronisering av sesjonstilstand  

**For Stateless Implementeringer:**
- JWT eller lignende token-basert sesjonshåndtering  
- Kryptografisk verifisering av sesjonstilstandens integritet  
- Redusert angrepsflate, men krever robust tokenvalidering  

## 4. **AI-Spesifikke Sikkerhetskontroller**

### **Forsvar mot Prompt Injection**

**Microsoft Prompt Shields Integrasjon:**
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
- **Input Sanitization**: Omfattende validering og filtrering av alle brukerinput  
- **Definisjon av Innholdsgrenser**: Klar separasjon mellom systeminstruksjoner og brukerinnhold  
- **Instruksjonshierarki**: Riktige prioriteringsregler for motstridende instruksjoner  
- **Output Overvåking**: Deteksjon av potensielt skadelige eller manipulerte utdata  

### **Forebygging av Verktøyforgiftning**

**Sikkerhetsrammeverk for Verktøy:**
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

**Dynamisk Verktøyhåndtering:**
- **Godkjenningsarbeidsflyter**: Eksplisitt brukersamtykke for verktøysmodifikasjoner  
- **Tilbakerullingsmuligheter**: Mulighet til å gjenopprette tidligere verktøyversjoner  
- **Endringsrevisjon**: Fullstendig historikk over verktøydefinisjonsendringer  
- **Risikovurdering**: Automatisk evaluering av verktøyets sikkerhetsstatus  

## 5. **Forebygging av Confused Deputy Angrep**

### **OAuth Proxy Sikkerhet**

**Angrepsforebyggende Kontroller:**
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
- **Verifisering av Brukersamtykke**: Aldri hopp over samtykkeskjermer for dynamisk klientregistrering  
- **Validering av Redirect URI**: Streng validering basert på hviteliste av omdirigeringsdestinasjoner  
- **Beskyttelse av Autorisasjonskode**: Kortlevde koder med håndheving av engangsbruk  
- **Validering av Klientidentitet**: Robust validering av klientlegitimasjon og metadata  

## 6. **Sikkerhet ved Verktøyutførelse**

### **Sandboxing & Isolasjon**

**Container-basert Isolasjon:**
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

**Prosessisolasjon:**
- **Separate Prosesskontekster**: Hver verktøyutførelse i isolert prosessrom  
- **Inter-Prosess Kommunikasjon**: Sikre IPC-mekanismer med validering  
- **Prosessovervåking**: Analyse av runtime-adferd og deteksjon av avvik  
- **Ressurshåndheving**: Strenge grenser på CPU, minne og I/O-operasjoner  

### **Implementering av Minste Privilegium**

**Tillatelsesadministrasjon:**
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

## 7. **Forsyningskjede Sikkerhetskontroller**

### **Verifisering av Avhengigheter**

**Omfattende Komponent Sikkerhet:**
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

### **Kontinuerlig Overvåking**

**Trusseldeteksjon i Forsyningskjeden:**
- **Overvåking av Avhengighetshelse**: Kontinuerlig vurdering av alle avhengigheter for sikkerhetsproblemer  
- **Integrasjon av Trusselintelligens**: Sanntidsoppdateringer om fremvoksende trusler i forsyningskjeden  
- **Adferdsanalyse**: Deteksjon av uvanlig adferd i eksterne komponenter  
- **Automatisk Respons**: Umiddelbar inneslutning av kompromitterte komponenter  

## 8. **Overvåkings- & Deteksjonskontroller**

### **Sikkerhetsinformasjon og Hendelseshåndtering (SIEM)**

**Omfattende Loggstrategi:**
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

### **Sanntids Trusseldeteksjon**

**Adferdsanalyse:**
- **Brukeradferdsanalyse (UBA)**: Deteksjon av uvanlige brukeradgangsmønstre  
- **Enhetsadferdsanalyse (EBA)**: Overvåking av MCP-server og verktøysadferd  
- **Maskinlæringsbasert Anomalideteksjon**: AI-drevet identifikasjon av sikkerhetstrusler  
- **Korrelasjon av Trusselintelligens**: Matching av observerte aktiviteter mot kjente angrepsmønstre  

## 9. **Hendelseshåndtering & Gjenoppretting**

### **Automatiserte Responsmuligheter**

**Umiddelbare Responshandlinger:**
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

### **Forensiske Muligheter**

**Støtte for Undersøkelser:**
- **Bevaring av Revisjonsspor**: Uforanderlig logging med kryptografisk integritet  
- **Innsamling av Bevis**: Automatisk innhenting av relevante sikkerhetsartefakter  
- **Rekonstruksjon av Tidslinje**: Detaljert sekvens av hendelser som ledet til sikkerhetshendelser  
- **Vurdering av Påvirkning**: Evaluering av kompromissets omfang og dataeksponering  

## **Viktige Prinsipper for Sikkerhetsarkitektur**

### **Forsvar i Dybden**
- **Flere Sikkerhetslag**: Ingen enkelt feilpunkt i sikkerhetsarkitekturen  
- **Redundante Kontroller**: Overlappende sikkerhetstiltak for kritiske funksjoner  
- **Fail-Safe Mekanismer**: Sikre standarder når systemer møter feil eller angrep  

### **Implementering av Null Tillit**
- **Aldri Stol, Alltid Verifiser**: Kontinuerlig validering av alle enheter og forespørsler  
- **Prinsippet om Minste Privilegium**: Minimal tilgangsrettigheter for alle komponenter  
- **Mikrosegmentering**: Granulære nettverks- og tilgangskontroller  

### **Kontinuerlig Sikkerhetsutvikling**
- **Tilpasning til Trussellandskap**: Regelmessige oppdateringer for å adressere fremvoksende trusler  
- **Effektivitet av Sikkerhetskontroller**: Løpende evaluering og forbedring av kontroller  
- **Samsvar med Spesifikasjoner**: Justering med utviklende MCP-sikkerhetsstandarder  

---

## **Implementeringsressurser**

### **Offisiell MCP Dokumentasjon**
- [MCP Spesifikasjon (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Sikkerhetsbestepraksis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Autorisasjonsspesifikasjon](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Sikkerhetsløsninger**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Sikkerhetsstandarder**
- [OAuth 2.0 Sikkerhetsbestepraksis (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Topp 10 for Store Språkmodeller](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Viktig**: Disse sikkerhetskontrollene reflekterer gjeldende MCP spesifikasjon (2025-06-18). Verifiser alltid mot den nyeste [offisielle dokumentasjonen](https://spec.modelcontextprotocol.io/) ettersom standarder utvikler seg raskt.  

**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi tilstreber nøyaktighet, vær oppmerksom på at automatiserte oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på sitt opprinnelige språk bør anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.