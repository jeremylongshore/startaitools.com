<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T18:18:23+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "sl"
}
-->
# Varnostni ukrepi MCP - Posodobitev avgust 2025

> **Trenutni standard**: Ta dokument odraža varnostne zahteve [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) in uradne [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) se je znatno razvil z izboljšanimi varnostnimi ukrepi, ki obravnavajo tako tradicionalne varnostne grožnje programske opreme kot grožnje, specifične za umetno inteligenco. Ta dokument ponuja celovite varnostne ukrepe za varne implementacije MCP od avgusta 2025.

## **OBVEZNE varnostne zahteve**

### **Ključne prepovedi iz MCP specifikacije:**

> **PREPOVEDANO**: MCP strežniki **NE SMEJO** sprejemati nobenih žetonov, ki niso bili izrecno izdani za MCP strežnik  
>
> **PREPOVEDANO**: MCP strežniki **NE SMEJO** uporabljati sej za avtentikacijo  
>
> **ZAHTEVANO**: MCP strežniki, ki izvajajo avtorizacijo, **MORAJO** preveriti VSE dohodne zahteve  
>
> **OBVEZNO**: MCP proxy strežniki, ki uporabljajo statične ID-je odjemalcev, **MORAJO** pridobiti soglasje uporabnika za vsakega dinamično registriranega odjemalca  

---

## 1. **Kontrole avtentikacije in avtorizacije**

### **Integracija zunanjih ponudnikov identitete**

**Trenutni MCP standard (2025-06-18)** omogoča MCP strežnikom delegiranje avtentikacije zunanjim ponudnikom identitete, kar predstavlja pomembno izboljšanje varnosti:

**Varnostne prednosti:**
1. **Odprava tveganj lastne avtentikacije**: Zmanjšanje površine ranljivosti z izogibanjem lastnim implementacijam avtentikacije  
2. **Varnost na ravni podjetja**: Uporaba uveljavljenih ponudnikov identitete, kot je Microsoft Entra ID, z naprednimi varnostnimi funkcijami  
3. **Centralizirano upravljanje identitete**: Poenostavitev upravljanja življenjskega cikla uporabnikov, nadzora dostopa in revizij skladnosti  
4. **Večfaktorska avtentikacija**: Dedovanje MFA zmogljivosti od ponudnikov identitete na ravni podjetja  
5. **Politike pogojnega dostopa**: Koristi od nadzora dostopa na podlagi tveganja in prilagodljive avtentikacije  

**Zahteve za implementacijo:**
- **Preverjanje občinstva žetona**: Preverite, ali so vsi žetoni izrecno izdani za MCP strežnik  
- **Preverjanje izdajatelja**: Preverite, ali se izdajatelj žetona ujema s pričakovanim ponudnikom identitete  
- **Preverjanje podpisa**: Kriptografsko preverjanje celovitosti žetona  
- **Uveljavljanje poteka veljavnosti**: Strogo uveljavljanje časovnih omejitev veljavnosti žetona  
- **Preverjanje obsega**: Zagotovite, da žetoni vsebujejo ustrezna dovoljenja za zahtevane operacije  

### **Varnost logike avtorizacije**

**Ključni ukrepi:**
- **Celovite revizije avtorizacije**: Redni varnostni pregledi vseh točk odločanja o avtorizaciji  
- **Privzeti varni načini**: Zavrnitev dostopa, kadar logika avtorizacije ne more sprejeti dokončne odločitve  
- **Meje dovoljenj**: Jasna ločitev med različnimi ravnmi privilegijev in dostopom do virov  
- **Revizijski dnevnik**: Popolno beleženje vseh odločitev o avtorizaciji za varnostno spremljanje  
- **Redni pregledi dostopa**: Periodična validacija dovoljenj uporabnikov in dodelitev privilegijev  

## 2. **Varnost žetonov in preprečevanje prenosa**

### **Preprečevanje prenosa žetonov**

**Prenos žetonov je izrecno prepovedan** v MCP specifikaciji avtorizacije zaradi kritičnih varnostnih tveganj:

**Naslovljena varnostna tveganja:**
- **Obhod nadzora**: Obide bistvene varnostne ukrepe, kot so omejevanje hitrosti, validacija zahtev in spremljanje prometa  
- **Razpad odgovornosti**: Onemogoča identifikacijo odjemalca, kar pokvari revizijske sledi in preiskave incidentov  
- **Eksfiltracija prek proxyja**: Omogoča zlonamernim akterjem uporabo strežnikov kot proxyjev za nepooblaščen dostop do podatkov  
- **Kršitve meja zaupanja**: Poruši predpostavke zaupanja storitev o izvoru žetonov  
- **Lateralno gibanje**: Kompromitirani žetoni med več storitvami omogočajo širšo širitev napadov  

**Kontrole implementacije:**
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

### **Vzorce varnega upravljanja žetonov**

**Najboljše prakse:**
- **Žetoni s kratko življenjsko dobo**: Zmanjšajte okno izpostavljenosti s pogostim vrtenjem žetonov  
- **Izdaja po potrebi**: Izdajte žetone le, kadar so potrebni za specifične operacije  
- **Varno shranjevanje**: Uporabite strojne varnostne module (HSM) ali varne ključne shrambe  
- **Povezovanje žetonov**: Povežite žetone s specifičnimi odjemalci, sejami ali operacijami, kjer je to mogoče  
- **Spremljanje in opozarjanje**: Zaznavanje zlorabe žetonov ali nepooblaščenih vzorcev dostopa v realnem času  

## 3. **Kontrole varnosti sej**

### **Preprečevanje ugrabitve sej**

**Naslovljeni vektorji napadov:**
- **Ugrabitve sej z vbrizgavanjem ukazov**: Zlonamerni dogodki, vbrizgani v skupno stanje seje  
- **Impersonacija seje**: Neavtorizirana uporaba ukradenih ID-jev sej za obhod avtentikacije  
- **Napadi na obnovljive tokove**: Izkoriščanje obnove dogodkov, poslanih s strežnika, za vbrizgavanje zlonamerne vsebine  

**Obvezni ukrepi za seje:**
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

**Transportna varnost:**
- **Uveljavljanje HTTPS**: Vsa komunikacija sej prek TLS 1.3  
- **Atributi varnih piškotkov**: HttpOnly, Secure, SameSite=Strict  
- **Pripenjanje certifikatov**: Za kritične povezave, da preprečite MITM napade  

### **Razmislek o stanju**

**Za implementacije s stanjem:**
- Skupno stanje seje zahteva dodatno zaščito pred napadi z vbrizgavanjem  
- Upravljanje sej na osnovi vrstic zahteva preverjanje celovitosti  
- Več primerkov strežnikov zahteva varno sinhronizacijo stanja sej  

**Za implementacije brez stanja:**
- Upravljanje sej na osnovi JWT ali podobnih žetonov  
- Kriptografsko preverjanje celovitosti stanja seje  
- Zmanjšana površina napada, vendar zahteva robustno validacijo žetonov  

## 4. **Varnostni ukrepi specifični za AI**

### **Obramba pred vbrizgavanjem ukazov**

**Integracija Microsoft Prompt Shields:**
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

**Kontrole implementacije:**
- **Sanitizacija vhodov**: Celovita validacija in filtriranje vseh uporabniških vhodov  
- **Definicija meja vsebine**: Jasna ločitev med sistemskimi navodili in uporabniško vsebino  
- **Hierarhija navodil**: Ustrezna pravila prednosti za nasprotujoča si navodila  
- **Spremljanje izhodov**: Zaznavanje potencialno škodljivih ali manipuliranih izhodov  

### **Preprečevanje zastrupitve orodij**

**Okvir varnosti orodij:**
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

**Dinamično upravljanje orodij:**
- **Delovni tokovi odobritve**: Izrecno soglasje uporabnika za spremembe orodij  
- **Zmožnosti povratka**: Možnost vrnitve na prejšnje različice orodij  
- **Revizija sprememb**: Popolna zgodovina sprememb definicij orodij  
- **Ocena tveganja**: Avtomatizirana ocena varnostnega stanja orodij  

## 5. **Preprečevanje napadov z zmedenim namestnikom**

### **Varnost OAuth proxyja**

**Kontrole za preprečevanje napadov:**
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

**Zahteve za implementacijo:**
- **Preverjanje soglasja uporabnika**: Nikoli ne preskočite zaslonov za soglasje pri dinamični registraciji odjemalcev  
- **Validacija URI-jev za preusmeritev**: Stroga validacija na podlagi belih seznamov ciljev preusmeritev  
- **Zaščita avtorizacijskih kod**: Kratkotrajne kode z uveljavljanjem enkratne uporabe  
- **Preverjanje identitete odjemalca**: Robustno preverjanje poverilnic in metapodatkov odjemalca  

## 6. **Varnost izvajanja orodij**

### **Peskovnik in izolacija**

**Izolacija na osnovi kontejnerjev:**
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

**Izolacija procesov:**
- **Ločeni konteksti procesov**: Vsako izvajanje orodja v izoliranem procesnem prostoru  
- **Medprocesna komunikacija**: Varni mehanizmi IPC s preverjanjem  
- **Spremljanje procesov**: Analiza vedenja med izvajanjem in zaznavanje anomalij  
- **Uveljavljanje virov**: Trde omejitve za CPU, pomnilnik in I/O operacije  

### **Implementacija najmanjših privilegijev**

**Upravljanje dovoljenj:**
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

## 7. **Varnostni ukrepi za dobavno verigo**

### **Preverjanje odvisnosti**

**Celovita varnost komponent:**
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

### **Nenehno spremljanje**

**Zaznavanje groženj v dobavni verigi:**
- **Spremljanje zdravja odvisnosti**: Nenehna ocena vseh odvisnosti glede varnostnih težav  
- **Integracija obveščanja o grožnjah**: Posodobitve v realnem času o nastajajočih grožnjah v dobavni verigi  
- **Analiza vedenja**: Zaznavanje nenavadnega vedenja zunanjih komponent  
- **Avtomatiziran odziv**: Takojšnja zajezitev kompromitiranih komponent  

## 8. **Kontrole spremljanja in zaznavanja**

### **Upravljanje varnostnih informacij in dogodkov (SIEM)**

**Celovita strategija beleženja:**
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

### **Zaznavanje groženj v realnem času**

**Analitika vedenja:**
- **Analitika vedenja uporabnikov (UBA)**: Zaznavanje nenavadnih vzorcev dostopa uporabnikov  
- **Analitika vedenja entitet (EBA)**: Spremljanje vedenja MCP strežnika in orodij  
- **Zaznavanje anomalij z umetno inteligenco**: Identifikacija varnostnih groženj z AI  
- **Korelacija obveščanja o grožnjah**: Ujemanje opaženih dejavnosti z znanimi vzorci napadov  

## 9. **Odziv na incidente in okrevanje**

### **Avtomatizirane zmožnosti odziva**

**Takojšnji odzivni ukrepi:**
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

### **Forenzične zmožnosti**

**Podpora preiskavam:**
- **Ohranjanje revizijskih sledi**: Nespremenljivo beleženje s kriptografsko celovitostjo  
- **Zbiranje dokazov**: Avtomatizirano zbiranje ustreznih varnostnih artefaktov  
- **Rekonstrukcija časovnice**: Podroben zaporedni pregled dogodkov, ki so privedli do varnostnih incidentov  
- **Ocena vpliva**: Ocena obsega kompromisa in izpostavljenosti podatkov  

## **Ključna načela varnostne arhitekture**

### **Obramba v globino**
- **Več varnostnih slojev**: Brez ene same točke odpovedi v varnostni arhitekturi  
- **Redundantni ukrepi**: Prekrivajoči se varnostni ukrepi za ključne funkcije  
- **Varni privzeti načini**: Varnostni privzeti načini, ko sistemi naletijo na napake ali napade  

### **Implementacija ničelnega zaupanja**
- **Nikoli ne zaupaj, vedno preverjaj**: Nenehno preverjanje vseh entitet in zahtev  
- **Načelo najmanjših privilegijev**: Minimalne pravice dostopa za vse komponente  
- **Mikrosegmentacija**: Granularni nadzor omrežja in dostopa  

### **Nenehen razvoj varnosti**
- **Prilagoditev grožnjam**: Redne posodobitve za obravnavo nastajajočih groženj  
- **Učinkovitost varnostnih ukrepov**: Nenehna ocena in izboljšanje ukrepov  
- **Skladnost s specifikacijami**: Usklajenost z razvijajočimi se MCP varnostnimi standardi  

---

## **Viri za implementacijo**

### **Uradna dokumentacija MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft varnostne rešitve**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Varnostni standardi**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Pomembno**: Ti varnostni ukrepi odražajo trenutno MCP specifikacijo (2025-06-18). Vedno preverite najnovejšo [uradno dokumentacijo](https://spec.modelcontextprotocol.io/), saj se standardi hitro razvijajo.

**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve AI za prevajanje [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da lahko avtomatizirani prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za ključne informacije priporočamo profesionalni človeški prevod. Ne prevzemamo odgovornosti za morebitna nesporazumevanja ali napačne razlage, ki bi nastale zaradi uporabe tega prevoda.