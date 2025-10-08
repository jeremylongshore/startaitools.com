<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T15:39:26+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "cs"
}
-->
# Bezpečnostní opatření MCP - Aktualizace srpen 2025

> **Aktuální standard**: Tento dokument odráží bezpečnostní požadavky [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) a oficiální [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) se výrazně vyvinul díky vylepšeným bezpečnostním opatřením, která řeší jak tradiční softwarovou bezpečnost, tak hrozby specifické pro umělou inteligenci. Tento dokument poskytuje komplexní bezpečnostní opatření pro bezpečné implementace MCP k srpnu 2025.

## **POVINNÉ bezpečnostní požadavky**

### **Kritické zákazy z MCP specifikace:**

> **ZAKÁZÁNO**: MCP servery **NESMÍ** přijímat žádné tokeny, které nebyly výslovně vydány pro MCP server  
>
> **ZAKÁZÁNO**: MCP servery **NESMÍ** používat relace pro autentizaci  
>
> **POVINNÉ**: MCP servery implementující autorizaci **MUSÍ** ověřovat VŠECHNY příchozí požadavky  
>
> **POVINNÉ**: MCP proxy servery používající statické ID klientů **MUSÍ** získat souhlas uživatele pro každého dynamicky registrovaného klienta  

---

## 1. **Ovládání autentizace a autorizace**

### **Integrace externího poskytovatele identity**

**Aktuální MCP standard (2025-06-18)** umožňuje MCP serverům delegovat autentizaci na externí poskytovatele identity, což představuje významné zlepšení bezpečnosti:

**Bezpečnostní přínosy:**
1. **Eliminace rizik vlastních autentizací**: Snižuje povrch zranitelnosti tím, že se vyhýbá vlastním implementacím autentizace  
2. **Podniková úroveň bezpečnosti**: Využívá zavedené poskytovatele identity, jako je Microsoft Entra ID, s pokročilými bezpečnostními funkcemi  
3. **Centralizovaná správa identity**: Zjednodušuje správu životního cyklu uživatelů, kontrolu přístupu a auditování souladu  
4. **Vícefaktorová autentizace**: Přebírá schopnosti MFA od podnikových poskytovatelů identity  
5. **Podmíněné přístupové politiky**: Využívá přístupy založené na rizicích a adaptivní autentizaci  

**Požadavky na implementaci:**
- **Ověření publika tokenu**: Ověřte, že všechny tokeny byly výslovně vydány pro MCP server  
- **Ověření vydavatele**: Ověřte, že vydavatel tokenu odpovídá očekávanému poskytovateli identity  
- **Ověření podpisu**: Kryptografické ověření integrity tokenu  
- **Vynucení expirace**: Přísné vynucení časových limitů platnosti tokenu  
- **Ověření rozsahu**: Zajistěte, že tokeny obsahují odpovídající oprávnění pro požadované operace  

### **Bezpečnost logiky autorizace**

**Kritická opatření:**
- **Komplexní audity autorizace**: Pravidelné bezpečnostní kontroly všech rozhodovacích bodů autorizace  
- **Výchozí bezpečné nastavení**: Odepření přístupu, pokud logika autorizace nemůže učinit jednoznačné rozhodnutí  
- **Hranice oprávnění**: Jasné oddělení mezi různými úrovněmi oprávnění a přístupem k prostředkům  
- **Auditní logování**: Kompletní záznam všech rozhodnutí o autorizaci pro bezpečnostní monitorování  
- **Pravidelné přezkumy přístupu**: Periodické ověřování uživatelských oprávnění a přiřazení privilegií  

## 2. **Bezpečnost tokenů a opatření proti předávání**

### **Prevence předávání tokenů**

**Předávání tokenů je výslovně zakázáno** ve specifikaci MCP autorizace kvůli kritickým bezpečnostním rizikům:

**Řešená bezpečnostní rizika:**
- **Obcházení kontrol**: Obchází základní bezpečnostní opatření, jako je omezení rychlosti, validace požadavků a monitorování provozu  
- **Narušení odpovědnosti**: Ztěžuje identifikaci klienta, což narušuje auditní stopy a vyšetřování incidentů  
- **Exfiltrace přes proxy**: Umožňuje škodlivým aktérům používat servery jako proxy pro neoprávněný přístup k datům  
- **Porušení důvěryhodných hranic**: Narušuje předpoklady o původu tokenů u downstream služeb  
- **Boční pohyb**: Kompromitované tokeny napříč více službami umožňují širší expanzi útoků  

**Implementační opatření:**
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

### **Vzory bezpečné správy tokenů**

**Nejlepší postupy:**
- **Krátkodobé tokeny**: Minimalizace expozičního okna častou rotací tokenů  
- **Vydávání na vyžádání**: Vydávání tokenů pouze tehdy, když jsou potřeba pro konkrétní operace  
- **Bezpečné úložiště**: Použití hardwarových bezpečnostních modulů (HSM) nebo bezpečných úložišť klíčů  
- **Vázání tokenů**: Vázání tokenů na konkrétní klienty, relace nebo operace, pokud je to možné  
- **Monitorování a upozorňování**: Detekce zneužití tokenů nebo neoprávněných přístupových vzorců v reálném čase  

## 3. **Ovládání bezpečnosti relací**

### **Prevence únosu relací**

**Řešené vektory útoků:**
- **Únos relace pomocí injekce**: Škodlivé události vložené do sdíleného stavu relace  
- **Impersonace relace**: Neoprávněné použití odcizených ID relací k obcházení autentizace  
- **Útoky na obnovitelné proudy**: Zneužití obnovení událostí odesílaných serverem pro vložení škodlivého obsahu  

**Povinná opatření pro relace:**
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

**Transportní bezpečnost:**
- **Vynucení HTTPS**: Veškerá komunikace relace přes TLS 1.3  
- **Atributy zabezpečených cookies**: HttpOnly, Secure, SameSite=Strict  
- **Pinning certifikátů**: Pro kritická spojení k prevenci MITM útoků  

### **Úvahy o stavových a bezstavových implementacích**

**Pro stavové implementace:**
- Sdílený stav relace vyžaduje dodatečnou ochranu proti injekčním útokům  
- Správa relací založená na frontách potřebuje ověření integrity  
- Více instancí serveru vyžaduje bezpečnou synchronizaci stavu relace  

**Pro bezstavové implementace:**
- Správa relací založená na JWT nebo podobných tokenových mechanismech  
- Kryptografické ověření integrity stavu relace  
- Snížený povrch útoku, ale vyžaduje robustní validaci tokenů  

## 4. **Bezpečnostní opatření specifická pro AI**

### **Obrana proti injekci promptů**

**Integrace Microsoft Prompt Shields:**
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

**Implementační opatření:**
- **Sanitace vstupů**: Komplexní validace a filtrování všech uživatelských vstupů  
- **Definice hranic obsahu**: Jasné oddělení systémových instrukcí a uživatelského obsahu  
- **Hierarchie instrukcí**: Správná precedence pravidel pro konfliktní instrukce  
- **Monitorování výstupů**: Detekce potenciálně škodlivých nebo manipulovaných výstupů  

### **Prevence otravy nástrojů**

**Rámec bezpečnosti nástrojů:**
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

**Dynamická správa nástrojů:**
- **Schvalovací workflowy**: Výslovný souhlas uživatele pro změny nástrojů  
- **Možnosti návratu zpět**: Schopnost vrátit se k předchozím verzím nástrojů  
- **Audit změn**: Kompletní historie změn definic nástrojů  
- **Hodnocení rizik**: Automatizované vyhodnocení bezpečnostního stavu nástrojů  

## 5. **Prevence útoků zmateného zástupce**

### **Bezpečnost OAuth proxy**

**Opatření pro prevenci útoků:**
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

**Požadavky na implementaci:**
- **Ověření souhlasu uživatele**: Nikdy nevynechávat obrazovky souhlasu pro dynamickou registraci klientů  
- **Validace přesměrovacích URI**: Přísná validace destinací přesměrování na základě whitelistu  
- **Ochrana autorizačních kódů**: Krátkodobé kódy s vynucením jednorázového použití  
- **Ověření identity klienta**: Robustní validace přihlašovacích údajů a metadat klienta  

## 6. **Bezpečnost při spouštění nástrojů**

### **Sandboxing a izolace**

**Izolace založená na kontejnerech:**
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

**Izolace procesů:**
- **Oddělené kontexty procesů**: Každé spuštění nástroje v izolovaném procesním prostoru  
- **Meziprocesová komunikace**: Bezpečné mechanismy IPC s validací  
- **Monitorování procesů**: Analýza chování za běhu a detekce anomálií  
- **Vynucení zdrojů**: Pevné limity na CPU, paměť a I/O operace  

### **Implementace principu nejmenších privilegií**

**Správa oprávnění:**
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

## 7. **Bezpečnost dodavatelského řetězce**

### **Ověření závislostí**

**Komplexní bezpečnost komponent:**
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

### **Nepřetržité monitorování**

**Detekce hrozeb v dodavatelském řetězci:**
- **Monitorování zdraví závislostí**: Nepřetržité hodnocení všech závislostí na bezpečnostní problémy  
- **Integrace zpravodajství o hrozbách**: Aktualizace v reálném čase o vznikajících hrozbách v dodavatelském řetězci  
- **Analýza chování**: Detekce neobvyklého chování externích komponent  
- **Automatizovaná reakce**: Okamžité omezení kompromitovaných komponent  

## 8. **Monitorovací a detekční opatření**

### **Bezpečnostní informace a správa událostí (SIEM)**

**Komplexní strategie logování:**
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

### **Detekce hrozeb v reálném čase**

**Analýza chování:**
- **Analýza chování uživatelů (UBA)**: Detekce neobvyklých vzorců přístupu uživatelů  
- **Analýza chování entit (EBA)**: Monitorování chování MCP serveru a nástrojů  
- **Detekce anomálií pomocí strojového učení**: Identifikace bezpečnostních hrozeb pomocí AI  
- **Korelace zpravodajství o hrozbách**: Porovnání pozorovaných aktivit s známými vzory útoků  

## 9. **Reakce na incidenty a obnova**

### **Automatizované reakční schopnosti**

**Okamžité reakční akce:**
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

### **Forenzní schopnosti**

**Podpora vyšetřování:**
- **Zachování auditní stopy**: Neměnné logování s kryptografickou integritou  
- **Sběr důkazů**: Automatizované shromažďování relevantních bezpečnostních artefaktů  
- **Rekonstrukce časové osy**: Detailní sled událostí vedoucích k bezpečnostním incidentům  
- **Hodnocení dopadu**: Vyhodnocení rozsahu kompromitace a expozice dat  

## **Klíčové principy bezpečnostní architektury**

### **Obrana v hloubce**
- **Více bezpečnostních vrstev**: Žádný jediný bod selhání v bezpečnostní architektuře  
- **Redundantní opatření**: Překrývající se bezpečnostní opatření pro kritické funkce  
- **Mechanismy bezpečného selhání**: Bezpečné výchozí nastavení při chybách nebo útocích  

### **Implementace Zero Trust**
- **Nikdy nedůvěřuj, vždy ověřuj**: Nepřetržité ověřování všech entit a požadavků  
- **Princip nejmenších privilegií**: Minimální přístupová práva pro všechny komponenty  
- **Mikrosegmentace**: Granulární síťové a přístupové kontroly  

### **Nepřetržitý vývoj bezpečnosti**
- **Adaptace na hrozby**: Pravidelné aktualizace pro řešení vznikajících hrozeb  
- **Efektivita bezpečnostních opatření**: Průběžné hodnocení a zlepšování opatření  
- **Soulad se specifikacemi**: Sjednocení s vyvíjejícími se bezpečnostními standardy MCP  

---

## **Zdroje pro implementaci**

### **Oficiální dokumentace MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Bezpečnostní řešení Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Bezpečnostní standardy**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Důležité**: Tato bezpečnostní opatření odrážejí aktuální specifikaci MCP (2025-06-18). Vždy ověřujte podle nejnovější [oficiální dokumentace](https://spec.modelcontextprotocol.io/), protože standardy se rychle vyvíjejí.  

**Prohlášení**:  
Tento dokument byl přeložen pomocí služby pro automatický překlad [Co-op Translator](https://github.com/Azure/co-op-translator). I když se snažíme o přesnost, mějte prosím na paměti, že automatické překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho původním jazyce by měl být považován za závazný zdroj. Pro důležité informace doporučujeme profesionální lidský překlad. Neodpovídáme za žádná nedorozumění nebo nesprávné interpretace vyplývající z použití tohoto překladu.