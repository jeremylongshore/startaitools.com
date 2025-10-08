<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T17:32:04+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "it"
}
-->
# Controlli di Sicurezza MCP - Aggiornamento Agosto 2025

> **Standard Attuale**: Questo documento riflette i requisiti di sicurezza della [Specifica MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) e le [Migliori Pratiche di Sicurezza MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) ufficiali.

Il Model Context Protocol (MCP) ha raggiunto un livello di maturità significativo con controlli di sicurezza avanzati che affrontano sia le minacce tradizionali alla sicurezza del software sia quelle specifiche per l'IA. Questo documento fornisce controlli di sicurezza completi per implementazioni MCP sicure aggiornate ad agosto 2025.

## **Requisiti di Sicurezza OBBLIGATORI**

### **Divieti Critici dalla Specifica MCP:**

> **VIETATO**: I server MCP **NON DEVONO** accettare token che non siano stati esplicitamente emessi per il server MCP  
>
> **PROIBITO**: I server MCP **NON DEVONO** utilizzare sessioni per l'autenticazione  
>
> **OBBLIGATORIO**: I server MCP che implementano l'autorizzazione **DEVONO** verificare TUTTE le richieste in entrata  
>
> **MANDATORIO**: I server proxy MCP che utilizzano ID client statici **DEVONO** ottenere il consenso dell'utente per ogni client registrato dinamicamente  

---

## 1. **Controlli di Autenticazione e Autorizzazione**

### **Integrazione con Provider di Identità Esterni**

Lo **Standard MCP Attuale (2025-06-18)** consente ai server MCP di delegare l'autenticazione a provider di identità esterni, rappresentando un significativo miglioramento della sicurezza:

**Vantaggi di Sicurezza:**
1. **Eliminazione dei Rischi di Autenticazione Personalizzata**: Riduce la superficie di vulnerabilità evitando implementazioni di autenticazione personalizzate  
2. **Sicurezza di Livello Aziendale**: Sfrutta provider di identità consolidati come Microsoft Entra ID con funzionalità di sicurezza avanzate  
3. **Gestione Centralizzata delle Identità**: Semplifica la gestione del ciclo di vita degli utenti, il controllo degli accessi e la verifica della conformità  
4. **Autenticazione Multi-Fattore**: Eredita le capacità MFA dai provider di identità aziendali  
5. **Politiche di Accesso Condizionale**: Beneficia di controlli di accesso basati sul rischio e autenticazione adattiva  

**Requisiti di Implementazione:**
- **Validazione del Pubblico del Token**: Verificare che tutti i token siano esplicitamente emessi per il server MCP  
- **Verifica dell'Emittente**: Validare che l'emittente del token corrisponda al provider di identità previsto  
- **Verifica della Firma**: Validazione crittografica dell'integrità del token  
- **Applicazione della Scadenza**: Applicazione rigorosa dei limiti di durata del token  
- **Validazione degli Ambiti**: Assicurarsi che i token contengano i permessi appropriati per le operazioni richieste  

### **Sicurezza della Logica di Autorizzazione**

**Controlli Critici:**
- **Audit Completi dell'Autorizzazione**: Revisioni regolari di sicurezza di tutti i punti decisionali di autorizzazione  
- **Default Sicuri**: Negare l'accesso quando la logica di autorizzazione non può prendere una decisione definitiva  
- **Confini di Permessi**: Separazione chiara tra diversi livelli di privilegi e accesso alle risorse  
- **Registrazione degli Audit**: Registrazione completa di tutte le decisioni di autorizzazione per il monitoraggio della sicurezza  
- **Revisioni Regolari degli Accessi**: Validazione periodica dei permessi degli utenti e delle assegnazioni di privilegi  

## 2. **Sicurezza dei Token e Controlli Anti-Passthrough**

### **Prevenzione del Passthrough dei Token**

**Il passthrough dei token è esplicitamente vietato** nella Specifica di Autorizzazione MCP a causa di rischi critici per la sicurezza:

**Rischi di Sicurezza Affrontati:**
- **Elusione dei Controlli**: Bypass dei controlli di sicurezza essenziali come il rate limiting, la validazione delle richieste e il monitoraggio del traffico  
- **Perdita di Responsabilità**: Rende impossibile identificare i client, corrompendo le tracce di audit e le indagini sugli incidenti  
- **Esfiltrazione Basata su Proxy**: Consente agli attori malevoli di utilizzare i server come proxy per l'accesso non autorizzato ai dati  
- **Violazioni dei Confini di Fiducia**: Compromette le assunzioni di fiducia dei servizi downstream sull'origine dei token  
- **Movimento Laterale**: Token compromessi tra più servizi consentono un'espansione più ampia degli attacchi  

**Controlli di Implementazione:**
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

### **Modelli di Gestione Sicura dei Token**

**Migliori Pratiche:**
- **Token a Breve Durata**: Ridurre la finestra di esposizione con una rotazione frequente dei token  
- **Emissione Just-in-Time**: Emettere token solo quando necessario per operazioni specifiche  
- **Archiviazione Sicura**: Utilizzare moduli di sicurezza hardware (HSM) o vault di chiavi sicuri  
- **Binding dei Token**: Associare i token a client, sessioni o operazioni specifiche ove possibile  
- **Monitoraggio e Allerta**: Rilevamento in tempo reale dell'uso improprio dei token o di schemi di accesso non autorizzati  

## 3. **Controlli di Sicurezza delle Sessioni**

### **Prevenzione del Furto di Sessione**

**Vettori di Attacco Affrontati:**
- **Injection di Prompt nelle Sessioni**: Eventi malevoli iniettati nello stato condiviso della sessione  
- **Impersonificazione della Sessione**: Uso non autorizzato di ID di sessione rubati per bypassare l'autenticazione  
- **Attacchi a Flussi Ripristinabili**: Sfruttamento della ripresa di eventi inviati dal server per l'iniezione di contenuti malevoli  

**Controlli Obbligatori per le Sessioni:**
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

**Sicurezza del Trasporto:**
- **Applicazione di HTTPS**: Tutte le comunicazioni di sessione su TLS 1.3  
- **Attributi Sicuri dei Cookie**: HttpOnly, Secure, SameSite=Strict  
- **Pinning dei Certificati**: Per connessioni critiche per prevenire attacchi MITM  

### **Considerazioni su Implementazioni Stateful vs Stateless**

**Per Implementazioni Stateful:**
- Lo stato condiviso della sessione richiede protezioni aggiuntive contro gli attacchi di injection  
- La gestione delle sessioni basata su code necessita di verifiche di integrità  
- Più istanze del server richiedono una sincronizzazione sicura dello stato della sessione  

**Per Implementazioni Stateless:**
- Gestione delle sessioni basata su JWT o token simili  
- Verifica crittografica dell'integrità dello stato della sessione  
- Superficie di attacco ridotta ma richiede una robusta validazione dei token  

## 4. **Controlli di Sicurezza Specifici per l'IA**

### **Difesa contro l'Injection di Prompt**

**Integrazione con Microsoft Prompt Shields:**
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

**Controlli di Implementazione:**
- **Sanitizzazione degli Input**: Validazione e filtraggio completi di tutti gli input degli utenti  
- **Definizione dei Confini dei Contenuti**: Separazione chiara tra istruzioni di sistema e contenuti degli utenti  
- **Gerarchia delle Istruzioni**: Regole di precedenza adeguate per istruzioni in conflitto  
- **Monitoraggio degli Output**: Rilevamento di output potenzialmente dannosi o manipolati  

### **Prevenzione dell'Avvelenamento degli Strumenti**

**Framework di Sicurezza degli Strumenti:**
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

**Gestione Dinamica degli Strumenti:**
- **Workflow di Approvazione**: Consenso esplicito dell'utente per modifiche agli strumenti  
- **Capacità di Rollback**: Possibilità di ripristinare versioni precedenti degli strumenti  
- **Audit delle Modifiche**: Storia completa delle modifiche alla definizione degli strumenti  
- **Valutazione del Rischio**: Valutazione automatizzata della postura di sicurezza degli strumenti  

## 5. **Prevenzione degli Attacchi Confused Deputy**

### **Sicurezza dei Proxy OAuth**

**Controlli di Prevenzione degli Attacchi:**
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

**Requisiti di Implementazione:**
- **Verifica del Consenso dell'Utente**: Non saltare mai le schermate di consenso per la registrazione dinamica dei client  
- **Validazione degli URI di Reindirizzamento**: Validazione rigorosa basata su whitelist delle destinazioni di reindirizzamento  
- **Protezione dei Codici di Autorizzazione**: Codici a breve durata con applicazione di utilizzo singolo  
- **Verifica dell'Identità del Client**: Validazione robusta delle credenziali e dei metadati del client  

## 6. **Sicurezza nell'Esecuzione degli Strumenti**

### **Sandboxing e Isolamento**

**Isolamento Basato su Contenitori:**
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

**Isolamento dei Processi:**
- **Contesti di Processo Separati**: Ogni esecuzione dello strumento in uno spazio di processo isolato  
- **Comunicazione Inter-Processo**: Meccanismi IPC sicuri con validazione  
- **Monitoraggio dei Processi**: Analisi del comportamento in tempo reale e rilevamento di anomalie  
- **Applicazione delle Risorse**: Limiti rigidi su CPU, memoria e operazioni I/O  

### **Implementazione del Principio del Minimo Privilegio**

**Gestione dei Permessi:**
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

## 7. **Controlli di Sicurezza della Supply Chain**

### **Verifica delle Dipendenze**

**Sicurezza Completa dei Componenti:**
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

### **Monitoraggio Continuo**

**Rilevamento delle Minacce alla Supply Chain:**
- **Monitoraggio della Salute delle Dipendenze**: Valutazione continua di tutte le dipendenze per problemi di sicurezza  
- **Integrazione dell'Intelligence sulle Minacce**: Aggiornamenti in tempo reale sulle minacce emergenti alla supply chain  
- **Analisi Comportamentale**: Rilevamento di comportamenti insoliti nei componenti esterni  
- **Risposta Automatica**: Contenimento immediato dei componenti compromessi  

## 8. **Controlli di Monitoraggio e Rilevamento**

### **Gestione delle Informazioni e degli Eventi di Sicurezza (SIEM)**

**Strategia Completa di Logging:**
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

### **Rilevamento delle Minacce in Tempo Reale**

**Analisi Comportamentale:**
- **Analisi del Comportamento degli Utenti (UBA)**: Rilevamento di schemi di accesso insoliti degli utenti  
- **Analisi del Comportamento delle Entità (EBA)**: Monitoraggio del comportamento dei server MCP e degli strumenti  
- **Rilevamento delle Anomalie con Machine Learning**: Identificazione basata sull'IA di minacce alla sicurezza  
- **Correlazione dell'Intelligence sulle Minacce**: Confronto delle attività osservate con schemi di attacco noti  

## 9. **Risposta agli Incidenti e Recupero**

### **Capacità di Risposta Automatica**

**Azioni di Risposta Immediata:**
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

### **Capacità Forensi**

**Supporto alle Indagini:**
- **Preservazione delle Tracce di Audit**: Logging immutabile con integrità crittografica  
- **Raccolta delle Prove**: Raccolta automatizzata di artefatti di sicurezza rilevanti  
- **Ricostruzione della Timeline**: Sequenza dettagliata degli eventi che hanno portato agli incidenti di sicurezza  
- **Valutazione dell'Impatto**: Valutazione dell'entità della compromissione e dell'esposizione dei dati  

## **Principi Chiave dell'Architettura di Sicurezza**

### **Difesa in Profondità**
- **Molteplici Livelli di Sicurezza**: Nessun singolo punto di fallimento nell'architettura di sicurezza  
- **Controlli Ridondanti**: Misure di sicurezza sovrapposte per funzioni critiche  
- **Meccanismi Fail-Safe**: Default sicuri quando i sistemi incontrano errori o attacchi  

### **Implementazione Zero Trust**
- **Mai Fidarsi, Verificare Sempre**: Validazione continua di tutte le entità e richieste  
- **Principio del Minimo Privilegio**: Diritti di accesso minimi per tutti i componenti  
- **Micro-Segmentazione**: Controlli granulari di rete e accesso  

### **Evoluzione Continua della Sicurezza**
- **Adattamento al Panorama delle Minacce**: Aggiornamenti regolari per affrontare le minacce emergenti  
- **Efficacia dei Controlli di Sicurezza**: Valutazione e miglioramento continuo dei controlli  
- **Conformità alle Specifiche**: Allineamento con gli standard di sicurezza MCP in evoluzione  

---

## **Risorse per l'Implementazione**

### **Documentazione Ufficiale MCP**
- [Specifiche MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Migliori Pratiche di Sicurezza MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Specifiche di Autorizzazione MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Soluzioni di Sicurezza Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Standard di Sicurezza**
- [Migliori Pratiche di Sicurezza OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 per i Modelli di Linguaggio di Grandi Dimensioni](https://genai.owasp.org/)  
- [Framework di Cybersecurity NIST](https://www.nist.gov/cyberframework)  

---

> **Importante**: Questi controlli di sicurezza riflettono la specifica MCP attuale (2025-06-18). Verificare sempre la [documentazione ufficiale](https://spec.modelcontextprotocol.io/) più recente, poiché gli standard continuano a evolversi rapidamente.

**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si consiglia una traduzione professionale eseguita da un traduttore umano. Non siamo responsabili per eventuali fraintendimenti o interpretazioni errate derivanti dall'uso di questa traduzione.