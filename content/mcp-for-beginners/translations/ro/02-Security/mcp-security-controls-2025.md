<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T16:31:31+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ro"
}
-->
# MCP Controale de Securitate - Actualizare August 2025

> **Standard Curent**: Acest document reflectă cerințele de securitate din [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) și [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Protocolul Model Context (MCP) a evoluat semnificativ, cu controale de securitate îmbunătățite care abordează atât securitatea software tradițională, cât și amenințările specifice AI. Acest document oferă controale de securitate cuprinzătoare pentru implementările MCP sigure, valabile din august 2025.

## **Cerințe de Securitate OBLIGATORII**

### **Interdicții Critice din Specificația MCP:**

> **INTERZIS**: Serverele MCP **NU TREBUIE** să accepte token-uri care nu au fost emise explicit pentru serverul MCP  
>
> **PROHIBIT**: Serverele MCP **NU TREBUIE** să utilizeze sesiuni pentru autentificare  
>
> **OBLIGATORIU**: Serverele MCP care implementează autorizarea **TREBUIE** să verifice TOATE cererile primite  
>
> **MANDATORIU**: Serverele proxy MCP care folosesc ID-uri statice de client **TREBUIE** să obțină consimțământul utilizatorului pentru fiecare client înregistrat dinamic  

---

## 1. **Controale de Autentificare și Autorizare**

### **Integrarea cu Furnizori Externi de Identitate**

**Standardul MCP Curent (2025-06-18)** permite serverelor MCP să delege autentificarea către furnizori externi de identitate, reprezentând o îmbunătățire semnificativă a securității:

**Beneficii de Securitate:**
1. **Eliminarea Riscurilor de Autentificare Personalizată**: Reduce suprafața vulnerabilităților prin evitarea implementărilor personalizate de autentificare  
2. **Securitate la Nivel de Întreprindere**: Utilizează furnizori de identitate consacrați, precum Microsoft Entra ID, cu funcții avansate de securitate  
3. **Management Centralizat al Identității**: Simplifică gestionarea ciclului de viață al utilizatorilor, controlul accesului și auditarea conformității  
4. **Autentificare Multi-Factor**: Moștenește capacitățile MFA de la furnizorii de identitate pentru întreprinderi  
5. **Politici de Acces Condiționat**: Beneficiază de controale de acces bazate pe riscuri și autentificare adaptivă  

**Cerințe de Implementare:**
- **Validarea Publicului Token-ului**: Verificați ca toate token-urile să fie emise explicit pentru serverul MCP  
- **Verificarea Emitentului**: Asigurați-vă că emitentul token-ului corespunde furnizorului de identitate așteptat  
- **Verificarea Semnăturii**: Validare criptografică a integrității token-ului  
- **Respectarea Expirării**: Aplicarea strictă a limitelor de durată a token-ului  
- **Validarea Domeniului de Aplicare**: Asigurați-vă că token-urile conțin permisiuni adecvate pentru operațiunile solicitate  

### **Securitatea Logicii de Autorizare**

**Controale Critice:**
- **Audituri Complete de Autorizare**: Revizuiri regulate ale tuturor punctelor de decizie privind autorizarea  
- **Setări de Siguranță Implicite**: Refuzarea accesului atunci când logica de autorizare nu poate lua o decizie clară  
- **Limite de Permisiuni**: Separare clară între nivelurile de privilegii și accesul la resurse  
- **Logare Auditabilă**: Înregistrarea completă a tuturor deciziilor de autorizare pentru monitorizarea securității  
- **Revizuiri Periodice ale Accesului**: Validarea periodică a permisiunilor utilizatorilor și a atribuțiilor de privilegii  

## 2. **Securitatea Token-urilor și Controale Anti-Passthrough**

### **Prevenirea Passthrough-ului Token-urilor**

**Passthrough-ul token-urilor este explicit interzis** în Specificația de Autorizare MCP din cauza riscurilor critice de securitate:

**Riscuri de Securitate Abordate:**
- **Ocolirea Controalelor**: Evită controale esențiale precum limitarea ratei, validarea cererilor și monitorizarea traficului  
- **Degradarea Responsabilității**: Face imposibilă identificarea clientului, corupând traseele de audit și investigațiile incidentelor  
- **Exfiltrare prin Proxy**: Permite actorilor rău intenționați să utilizeze serverele ca proxy pentru acces neautorizat la date  
- **Încălcarea Limitelor de Încredere**: Distruge presupunerile de încredere ale serviciilor downstream despre originea token-urilor  
- **Mișcare Laterală**: Token-urile compromise între mai multe servicii permit extinderea atacurilor  

**Controale de Implementare:**
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

### **Modele Sigure de Gestionare a Token-urilor**

**Cele mai bune practici:**
- **Token-uri de Durată Scurtă**: Minimizarea ferestrei de expunere prin rotația frecventă a token-urilor  
- **Emitere Just-in-Time**: Emiterea token-urilor doar atunci când sunt necesare pentru operațiuni specifice  
- **Stocare Securizată**: Utilizarea modulelor de securitate hardware (HSM) sau a seifurilor de chei securizate  
- **Legarea Token-urilor**: Asocierea token-urilor cu clienți, sesiuni sau operațiuni specifice, acolo unde este posibil  
- **Monitorizare și Alertare**: Detectarea în timp real a utilizării greșite a token-urilor sau a modelelor de acces neautorizat  

## 3. **Controale de Securitate ale Sesiunilor**

### **Prevenirea Deturnării Sesiunilor**

**Vectori de Atac Abordați:**
- **Injectarea Prompturilor de Deturnare a Sesiunilor**: Evenimente rău intenționate injectate în starea sesiunii partajate  
- **Impersonarea Sesiunilor**: Utilizarea neautorizată a ID-urilor de sesiune furate pentru a ocoli autentificarea  
- **Atacuri pe Fluxuri Reluabile**: Exploatarea reluării evenimentelor trimise de server pentru injectarea de conținut rău intenționat  

**Controale Obligatorii ale Sesiunilor:**
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

**Securitatea Transportului:**
- **Aplicarea HTTPS**: Toată comunicarea sesiunii prin TLS 1.3  
- **Atribute Securizate ale Cookie-urilor**: HttpOnly, Secure, SameSite=Strict  
- **Fixarea Certificatelor**: Pentru conexiuni critice, pentru a preveni atacurile MITM  

### **Considerații Stateful vs Stateless**

**Pentru Implementări Stateful:**
- Starea sesiunii partajate necesită protecție suplimentară împotriva atacurilor de injectare  
- Gestionarea sesiunilor bazată pe cozi necesită verificarea integrității  
- Instanțele multiple de server necesită sincronizare securizată a stării sesiunii  

**Pentru Implementări Stateless:**
- Gestionarea sesiunilor bazată pe token-uri JWT sau similare  
- Verificare criptografică a integrității stării sesiunii  
- Suprafață de atac redusă, dar necesită validare robustă a token-urilor  

## 4. **Controale de Securitate Specifice AI**

### **Apărarea împotriva Injectării Prompturilor**

**Integrarea Microsoft Prompt Shields:**
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

**Controale de Implementare:**
- **Sanitizarea Inputurilor**: Validare și filtrare cuprinzătoare a tuturor inputurilor utilizatorilor  
- **Definirea Limitelor de Conținut**: Separare clară între instrucțiunile sistemului și conținutul utilizatorului  
- **Ierarhia Instrucțiunilor**: Reguli adecvate de prioritate pentru instrucțiuni conflictuale  
- **Monitorizarea Outputurilor**: Detectarea outputurilor potențial dăunătoare sau manipulate  

### **Prevenirea Otrăvirii Instrumentelor**

**Cadru de Securitate pentru Instrumente:**
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

**Gestionarea Dinamică a Instrumentelor:**
- **Fluxuri de Aprobare**: Consimțământ explicit al utilizatorului pentru modificările instrumentelor  
- **Capacități de Revertare**: Posibilitatea de a reveni la versiunile anterioare ale instrumentelor  
- **Auditarea Modificărilor**: Istoric complet al modificărilor definiției instrumentelor  
- **Evaluarea Riscurilor**: Evaluare automată a posturii de securitate a instrumentelor  

## 5. **Prevenirea Atacurilor de Tip Confused Deputy**

### **Securitatea Proxy-ului OAuth**

**Controale de Prevenire a Atacurilor:**
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

**Cerințe de Implementare:**
- **Verificarea Consimțământului Utilizatorului**: Nu săriți peste ecranele de consimțământ pentru înregistrarea dinamică a clienților  
- **Validarea URI-urilor de Redirecționare**: Validare strictă bazată pe liste albe a destinațiilor de redirecționare  
- **Protecția Codului de Autorizare**: Coduri de scurtă durată cu aplicarea utilizării unice  
- **Verificarea Identității Clientului**: Validare robustă a acreditivelor și metadatelor clientului  

## 6. **Securitatea Execuției Instrumentelor**

### **Sandboxing și Izolare**

**Izolare Bazată pe Containere:**
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

**Izolare Procesuală:**
- **Context Proces Separat**: Fiecare execuție a instrumentului într-un spațiu de proces izolat  
- **Comunicare Inter-Proces**: Mecanisme IPC securizate cu validare  
- **Monitorizarea Proceselor**: Analiza comportamentului în timpul execuției și detectarea anomaliilor  
- **Aplicarea Resurselor**: Limite stricte pentru CPU, memorie și operațiuni I/O  

### **Implementarea Privilegiului Minim**

**Gestionarea Permisiunilor:**
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

## 7. **Controale de Securitate ale Lanțului de Aprovizionare**

### **Verificarea Dependențelor**

**Securitatea Componentei Cuprinzătoare:**
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

### **Monitorizare Continuă**

**Detectarea Amenințărilor în Lanțul de Aprovizionare:**
- **Monitorizarea Sănătății Dependențelor**: Evaluarea continuă a tuturor dependențelor pentru probleme de securitate  
- **Integrarea Inteligenței de Amenințări**: Actualizări în timp real despre amenințările emergente din lanțul de aprovizionare  
- **Analiza Comportamentală**: Detectarea comportamentului neobișnuit în componentele externe  
- **Răspuns Automatizat**: Contenirea imediată a componentelor compromise  

## 8. **Controale de Monitorizare și Detectare**

### **Managementul Informațiilor și Evenimentelor de Securitate (SIEM)**

**Strategie Cuprinzătoare de Logare:**
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

### **Detectarea Amenințărilor în Timp Real**

**Analiza Comportamentală:**
- **Analiza Comportamentului Utilizatorilor (UBA)**: Detectarea modelelor neobișnuite de acces ale utilizatorilor  
- **Analiza Comportamentului Entităților (EBA)**: Monitorizarea comportamentului serverului MCP și al instrumentelor  
- **Detectarea Anomaliilor cu Ajutorul Machine Learning**: Identificarea amenințărilor de securitate cu ajutorul AI  
- **Corelarea Inteligenței de Amenințări**: Potrivirea activităților observate cu modele de atac cunoscute  

## 9. **Răspuns și Recuperare în Caz de Incident**

### **Capacități de Răspuns Automatizat**

**Acțiuni Imediate de Răspuns:**
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

### **Capacități Forensice**

**Suport pentru Investigații:**
- **Păstrarea Traseului de Audit**: Logare imuabilă cu integritate criptografică  
- **Colectarea Dovezilor**: Adunarea automată a artefactelor relevante de securitate  
- **Reconstrucția Cronologiei**: Secvență detaliată a evenimentelor care au dus la incidente de securitate  
- **Evaluarea Impactului**: Analiza extinderii compromisului și expunerii datelor  

## **Principii Cheie ale Arhitecturii de Securitate**

### **Apărare în Profunzime**
- **Straturi Multiple de Securitate**: Fără punct unic de eșec în arhitectura de securitate  
- **Controale Redundante**: Măsuri de securitate suprapuse pentru funcții critice  
- **Mecanisme de Siguranță**: Setări implicite sigure atunci când sistemele întâmpină erori sau atacuri  

### **Implementarea Zero Trust**
- **Nu Aveți Încredere, Verificați Întotdeauna**: Validare continuă a tuturor entităților și cererilor  
- **Principiul Privilegiului Minim**: Drepturi de acces minime pentru toate componentele  
- **Micro-Segmentare**: Controale granulare de rețea și acces  

### **Evoluția Continuă a Securității**
- **Adaptarea la Peisajul Amenințărilor**: Actualizări regulate pentru a aborda amenințările emergente  
- **Eficiența Controalelor de Securitate**: Evaluarea și îmbunătățirea continuă a controalelor  
- **Conformitatea cu Specificațiile**: Alinierea la standardele de securitate MCP în evoluție  

---

## **Resurse de Implementare**

### **Documentația Oficială MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Soluții de Securitate Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Standarde de Securitate**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Important**: Aceste controale de securitate reflectă specificația MCP curentă (2025-06-18). Verificați întotdeauna documentația [oficială](https://spec.modelcontextprotocol.io/) deoarece standardele continuă să evolueze rapid.

**Declinare de responsabilitate**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim să asigurăm acuratețea, vă rugăm să fiți conștienți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa natală ar trebui considerat sursa autoritară. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care pot apărea din utilizarea acestei traduceri.