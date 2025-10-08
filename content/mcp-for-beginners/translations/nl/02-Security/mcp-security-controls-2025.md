<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T16:32:50+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "nl"
}
-->
# MCP Beveiligingscontroles - Update augustus 2025

> **Huidige Standaard**: Dit document weerspiegelt de beveiligingseisen van [MCP Specificatie 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) en de officiële [MCP Beveiligingsrichtlijnen](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Het Model Context Protocol (MCP) heeft aanzienlijke vooruitgang geboekt met verbeterde beveiligingscontroles die zowel traditionele softwarebeveiliging als AI-specifieke bedreigingen aanpakken. Dit document biedt uitgebreide beveiligingscontroles voor veilige MCP-implementaties vanaf augustus 2025.

## **VERPLICHTE Beveiligingseisen**

### **Kritieke Verboden uit de MCP Specificatie:**

> **VERBODEN**: MCP-servers **MOGEN GEEN** tokens accepteren die niet expliciet voor de MCP-server zijn uitgegeven  
>
> **NIET TOEGESTAAN**: MCP-servers **MOGEN GEEN** sessies gebruiken voor authenticatie  
>
> **VEREIST**: MCP-servers die autorisatie implementeren **MOETEN** ALLE inkomende verzoeken verifiëren  
>
> **VERPLICHT**: MCP-proxyservers die statische client-ID's gebruiken **MOETEN** gebruikers toestemming vragen voor elke dynamisch geregistreerde client  

---

## 1. **Authenticatie- en Autorisatiecontroles**

### **Integratie met Externe Identiteitsproviders**

De **huidige MCP-standaard (2025-06-18)** staat MCP-servers toe authenticatie te delegeren aan externe identiteitsproviders, wat een aanzienlijke verbetering van de beveiliging betekent:

**Beveiligingsvoordelen:**
1. **Elimineert risico's van aangepaste authenticatie**: Vermindert kwetsbaarheden door het vermijden van eigen implementaties
2. **Enterprise-grade beveiliging**: Maakt gebruik van gevestigde identiteitsproviders zoals Microsoft Entra ID met geavanceerde beveiligingsfuncties
3. **Gecentraliseerd identiteitsbeheer**: Vereenvoudigt gebruikersbeheer, toegangscontrole en compliance-audits
4. **Multi-Factor Authenticatie**: Erft MFA-mogelijkheden van enterprise identiteitsproviders
5. **Voorwaardelijke Toegangsbeleid**: Profiteert van risicogebaseerde toegangscontroles en adaptieve authenticatie

**Implementatievereisten:**
- **Token Audience Validatie**: Controleer of alle tokens expliciet zijn uitgegeven voor de MCP-server
- **Issuer Verificatie**: Valideer of de token-uitgever overeenkomt met de verwachte identiteitsprovider
- **Handtekeningverificatie**: Cryptografische validatie van de tokenintegriteit
- **Strikte Verloophandhaving**: Zorg voor strikte handhaving van tokenlevensduur
- **Scope Validatie**: Controleer of tokens de juiste rechten bevatten voor de gevraagde operaties

### **Beveiliging van Autorisatielogica**

**Kritieke Controles:**
- **Uitgebreide Autorisatie-audits**: Regelmatige beveiligingscontroles van alle autorisatiebeslissingen
- **Fail-Safe Standaarden**: Toegang weigeren wanneer de autorisatielogica geen definitieve beslissing kan nemen
- **Rechtenafbakening**: Duidelijke scheiding tussen verschillende bevoegdheidsniveaus en toegangsrechten
- **Audit Logging**: Volledige logging van alle autorisatiebeslissingen voor beveiligingsmonitoring
- **Regelmatige Toegangscontroles**: Periodieke validatie van gebruikersrechten en bevoegdheidstoewijzingen

## 2. **Tokenbeveiliging & Anti-Passthrough Controles**

### **Voorkomen van Token Passthrough**

**Token passthrough is expliciet verboden** in de MCP Autorisatiespecificatie vanwege kritieke beveiligingsrisico's:

**Aangesproken Beveiligingsrisico's:**
- **Omzeiling van Controles**: Omzeilt essentiële beveiligingscontroles zoals rate limiting, verzoekvalidatie en verkeersmonitoring
- **Verlies van Verantwoordelijkheid**: Maakt clientidentificatie onmogelijk, wat audit trails en incidentonderzoek corrumpeert
- **Proxy-gebaseerde Exfiltratie**: Stelt kwaadwillenden in staat servers te gebruiken als proxy's voor ongeautoriseerde gegevens
- **Schending van Vertrouwensgrenzen**: Doorbreekt aannames over de oorsprong van tokens bij downstream services
- **Laterale Beweging**: Gecompromitteerde tokens over meerdere services maken bredere aanvallen mogelijk

**Implementatiecontroles:**
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

### **Veilige Tokenbeheerpatronen**

**Best Practices:**
- **Kortlevende Tokens**: Minimaliseer blootstellingsvensters met frequente tokenrotatie
- **Just-in-Time Uitgifte**: Geef tokens alleen uit wanneer nodig voor specifieke operaties
- **Veilige Opslag**: Gebruik hardwarebeveiligingsmodules (HSM's) of veilige sleutelkluizen
- **Tokenbinding**: Koppel tokens aan specifieke clients, sessies of operaties waar mogelijk
- **Monitoring & Waarschuwingen**: Realtime detectie van tokenmisbruik of ongeautoriseerde toegangspatronen

## 3. **Sessiebeveiligingscontroles**

### **Voorkomen van Sessiekaping**

**Aangevallen Vectoren:**
- **Sessiekaping via Promptinjectie**: Kwaadaardige gebeurtenissen geïnjecteerd in gedeelde sessiestatus
- **Sessievermoming**: Ongeautoriseerd gebruik van gestolen sessie-ID's om authenticatie te omzeilen
- **Aanvallen op Hervatbare Streams**: Misbruik van server-gestuurde gebeurtenisherneming voor kwaadaardige inhoudinjectie

**Verplichte Sessiecontroles:**
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

**Transportbeveiliging:**
- **HTTPS Verplichting**: Alle sessiecommunicatie via TLS 1.3
- **Veilige Cookie-attributen**: HttpOnly, Secure, SameSite=Strict
- **Certificaatpinnen**: Voor kritieke verbindingen om MITM-aanvallen te voorkomen

### **Overwegingen voor Stateful vs Stateless**

**Voor Stateful Implementaties:**
- Gedeelde sessiestatus vereist extra bescherming tegen injectieaanvallen
- Wachtrij-gebaseerd sessiebeheer vereist integriteitscontrole
- Meerdere serverinstanties vereisen veilige synchronisatie van sessiestatus

**Voor Stateless Implementaties:**
- JWT of vergelijkbaar token-gebaseerd sessiebeheer
- Cryptografische verificatie van sessiestatusintegriteit
- Verminderd aanvalsoppervlak, maar vereist robuuste tokenvalidatie

## 4. **AI-Specifieke Beveiligingscontroles**

### **Verdediging tegen Promptinjectie**

**Integratie met Microsoft Prompt Shields:**
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

**Implementatiecontroles:**
- **Inputvalidatie**: Uitgebreide controle en filtering van alle gebruikersinvoer
- **Definitie van Inhoudsgrenzen**: Duidelijke scheiding tussen systeeminstructies en gebruikersinhoud
- **Instructiehiërarchie**: Correcte prioriteitsregels voor conflicterende instructies
- **Outputmonitoring**: Detectie van mogelijk schadelijke of gemanipuleerde outputs

### **Voorkomen van Toolvergiftiging**

**Beveiligingskader voor Tools:**
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

**Dynamisch Toolbeheer:**
- **Goedkeuringsworkflows**: Expliciete gebruikersinstemming voor toolwijzigingen
- **Rollbackmogelijkheden**: Mogelijkheid om terug te keren naar eerdere toolversies
- **Wijzigingsaudits**: Volledige geschiedenis van tooldefinitiewijzigingen
- **Risicobeoordeling**: Geautomatiseerde evaluatie van de beveiligingsstatus van tools

## 5. **Voorkomen van Confused Deputy-aanvallen**

### **OAuth Proxy Beveiliging**

**Aanvalspreventiecontroles:**
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

**Implementatievereisten:**
- **Gebruikerstoestemming Verificatie**: Sla nooit toestemmingsschermen over bij dynamische clientregistratie
- **Redirect URI Validatie**: Strikte whitelist-gebaseerde validatie van redirect-bestemmingen
- **Bescherming van Autorisatiecodes**: Kortlevende codes met eenmalige handhaving
- **Validatie van Clientidentiteit**: Robuuste verificatie van clientreferenties en metadata

## 6. **Beveiliging van Tooluitvoering**

### **Sandboxing & Isolatie**

**Containergebaseerde Isolatie:**
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

**Procesisolatie:**
- **Gescheiden Procescontexten**: Elke tooluitvoering in een geïsoleerde procesruimte
- **Inter-Process Communicatie**: Veilige IPC-mechanismen met validatie
- **Procesmonitoring**: Analyse van runtimegedrag en detectie van afwijkingen
- **Resourcehandhaving**: Harde limieten op CPU, geheugen en I/O-operaties

### **Implementatie van Minimale Rechten**

**Rechtenbeheer:**
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

## 7. **Beveiliging van de Leveringsketen**

### **Verificatie van Afhankelijkheden**

**Uitgebreide Componentbeveiliging:**
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

### **Continue Monitoring**

**Detectie van Leveringsketenbedreigingen:**
- **Monitoring van Afhankelijkheidsgezondheid**: Continue beoordeling van alle afhankelijkheden op beveiligingsproblemen
- **Integratie van Dreigingsinformatie**: Realtime updates over opkomende bedreigingen in de leveringsketen
- **Gedragsanalyse**: Detectie van ongewoon gedrag in externe componenten
- **Geautomatiseerde Reactie**: Directe isolatie van gecompromitteerde componenten

## 8. **Monitoring- en Detectiecontroles**

### **Security Information and Event Management (SIEM)**

**Uitgebreide Loggingsstrategie:**
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

### **Realtime Dreigingsdetectie**

**Gedragsanalyse:**
- **Gebruikersgedragsanalyse (UBA)**: Detectie van ongebruikelijke gebruikerspatronen
- **Entiteitsgedragsanalyse (EBA)**: Monitoring van MCP-server- en toolgedrag
- **Machine Learning Anomaliedetectie**: AI-gestuurde identificatie van beveiligingsbedreigingen
- **Correlatie van Dreigingsinformatie**: Vergelijking van waargenomen activiteiten met bekende aanvalspatronen

## 9. **Incidentrespons & Herstel**

### **Geautomatiseerde Reactiemogelijkheden**

**Directe Reactieacties:**
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

### **Forensische Mogelijkheden**

**Ondersteuning bij Onderzoek:**
- **Bewaring van Audit Trails**: Onveranderlijke logging met cryptografische integriteit
- **Bewijsmateriaalverzameling**: Geautomatiseerde verzameling van relevante beveiligingsartefacten
- **Tijdlijnreconstructie**: Gedetailleerde volgorde van gebeurtenissen die tot beveiligingsincidenten hebben geleid
- **Impactanalyse**: Evaluatie van de omvang van de inbreuk en gegevensblootstelling

## **Belangrijke Beveiligingsarchitectuurprincipes**

### **Defense in Depth**
- **Meerdere Beveiligingslagen**: Geen enkel storingspunt in de beveiligingsarchitectuur
- **Redundante Controles**: Overlappende beveiligingsmaatregelen voor kritieke functies
- **Fail-Safe Mechanismen**: Veilige standaardinstellingen bij fouten of aanvallen

### **Zero Trust Implementatie**
- **Nooit Vertrouwen, Altijd Verifiëren**: Continue validatie van alle entiteiten en verzoeken
- **Principe van Minimale Rechten**: Minimale toegangsrechten voor alle componenten
- **Micro-Segmentatie**: Granulaire netwerk- en toegangscontroles

### **Continue Beveiligingsevolutie**
- **Aanpassing aan Dreigingslandschap**: Regelmatige updates om opkomende bedreigingen aan te pakken
- **Effectiviteit van Beveiligingscontroles**: Voortdurende evaluatie en verbetering van controles
- **Specificatiecompliance**: Afstemming op evoluerende MCP-beveiligingsstandaarden

---

## **Implementatiebronnen**

### **Officiële MCP Documentatie**
- [MCP Specificatie (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)
- [MCP Beveiligingsrichtlijnen](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [MCP Autorisatiespecificatie](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

### **Microsoft Beveiligingsoplossingen**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [GitHub Advanced Security](https://github.com/security/advanced-security)
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)

### **Beveiligingsstandaarden**
- [OAuth 2.0 Beveiligingsrichtlijnen (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [OWASP Top 10 voor Grote Taalmodellen](https://genai.owasp.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

> **Belangrijk**: Deze beveiligingscontroles weerspiegelen de huidige MCP-specificatie (2025-06-18). Controleer altijd de laatste [officiële documentatie](https://spec.modelcontextprotocol.io/) aangezien standaarden zich snel blijven ontwikkelen.

**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we ons best doen voor nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.