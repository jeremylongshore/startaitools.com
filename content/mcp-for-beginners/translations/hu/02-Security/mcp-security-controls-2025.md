<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T15:07:49+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "hu"
}
-->
# MCP Biztonsági Ellenőrzések - 2025. augusztusi frissítés

> **Jelenlegi szabvány**: Ez a dokumentum a [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) biztonsági követelményeit és a hivatalos [MCP Biztonsági Legjobb Gyakorlatokat](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) tükrözi.

A Model Context Protocol (MCP) jelentős fejlődésen ment keresztül, és továbbfejlesztett biztonsági ellenőrzéseket vezetett be, amelyek mind a hagyományos szoftverbiztonságot, mind az AI-specifikus fenyegetéseket kezelik. Ez a dokumentum átfogó biztonsági ellenőrzéseket nyújt a biztonságos MCP implementációkhoz 2025 augusztusától.

## **KÖTELEZŐ biztonsági követelmények**

### **Kritikus tiltások az MCP specifikációból:**

> **TILOS**: Az MCP szerverek **NEM FOGADHATNAK EL** olyan tokeneket, amelyeket nem kifejezetten az MCP szerver számára bocsátottak ki  
>
> **TILTOTT**: Az MCP szerverek **NEM HASZNÁLHATNAK** munkameneteket hitelesítéshez  
>
> **KÖTELEZŐ**: Az engedélyezést megvalósító MCP szervereknek **MINDEN** bejövő kérést ellenőrizniük kell  
>
> **KÖTELEZŐ**: A statikus kliensazonosítókat használó MCP proxy szervereknek **MINDEN** dinamikusan regisztrált klienshez felhasználói hozzájárulást kell szerezniük  

---

## 1. **Hitelesítési és engedélyezési ellenőrzések**

### **Külső identitásszolgáltató integrációja**

A **jelenlegi MCP szabvány (2025-06-18)** lehetővé teszi az MCP szerverek számára, hogy a hitelesítést külső identitásszolgáltatókra bízzák, ami jelentős biztonsági javulást jelent:

**Biztonsági előnyök:**
1. **Egyedi hitelesítési kockázatok megszüntetése**: Csökkenti a sebezhetőségi felületet az egyedi hitelesítési megoldások elkerülésével  
2. **Vállalati szintű biztonság**: Olyan bevált identitásszolgáltatók használata, mint a Microsoft Entra ID, fejlett biztonsági funkciókkal  
3. **Központosított identitáskezelés**: Egyszerűsíti a felhasználói életciklus-kezelést, a hozzáférés-ellenőrzést és a megfelelőségi auditokat  
4. **Többtényezős hitelesítés**: Örökli a vállalati identitásszolgáltatók MFA képességeit  
5. **Feltételes hozzáférési szabályok**: Kihasználja a kockázatalapú hozzáférés-ellenőrzést és az adaptív hitelesítést  

**Implementációs követelmények:**
- **Token célközönség ellenőrzése**: Ellenőrizze, hogy minden token kifejezetten az MCP szerver számára lett-e kiadva  
- **Kibocsátó ellenőrzése**: Ellenőrizze, hogy a token kibocsátója megfelel-e a várt identitásszolgáltatónak  
- **Aláírás ellenőrzése**: A token integritásának kriptográfiai ellenőrzése  
- **Lejárati idő betartása**: A token élettartamának szigorú betartása  
- **Jogosultságok ellenőrzése**: Győződjön meg arról, hogy a tokenek tartalmazzák a kért műveletekhez szükséges engedélyeket  

### **Engedélyezési logika biztonsága**

**Kritikus ellenőrzések:**
- **Átfogó engedélyezési auditok**: Az összes engedélyezési döntési pont rendszeres biztonsági felülvizsgálata  
- **Biztonságos alapértelmezések**: Hozzáférés megtagadása, ha az engedélyezési logika nem tud egyértelmű döntést hozni  
- **Jogosultsági határok**: Egyértelmű elválasztás a különböző jogosultsági szintek és erőforrás-hozzáférések között  
- **Auditnaplózás**: Az összes engedélyezési döntés teljes körű naplózása a biztonsági monitorozás érdekében  
- **Rendszeres hozzáférési felülvizsgálatok**: A felhasználói jogosultságok és jogosultság-hozzárendelések időszakos ellenőrzése  

## 2. **Tokenbiztonság és átengedési védelem**

### **Token átengedésének megakadályozása**

**A token átengedése kifejezetten tiltott** az MCP engedélyezési specifikációban a kritikus biztonsági kockázatok miatt:

**Kezelt biztonsági kockázatok:**
- **Ellenőrzések megkerülése**: Megkerüli az alapvető biztonsági ellenőrzéseket, például a sebességkorlátozást, a kérésellenőrzést és a forgalomfigyelést  
- **Elszámoltathatóság megszűnése**: Lehetetlenné teszi az ügyfélazonosítást, ami rontja az auditnaplókat és az incidensvizsgálatot  
- **Proxy-alapú adatlopás**: Lehetővé teszi rosszindulatú szereplők számára, hogy a szervereket proxyként használják jogosulatlan adat-hozzáféréshez  
- **Bizalmi határok megsértése**: Megszegi a downstream szolgáltatások token eredetére vonatkozó bizalmi feltételezéseit  
- **Oldalsó mozgás**: A több szolgáltatáson keresztül kompromittált tokenek szélesebb támadási lehetőséget biztosítanak  

**Implementációs ellenőrzések:**
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

### **Biztonságos tokenkezelési minták**

**Legjobb gyakorlatok:**
- **Rövid élettartamú tokenek**: Csökkentse a kitettségi ablakot a tokenek gyakori forgatásával  
- **Igény szerinti kiadás**: Tokenek kiadása csak a szükséges műveletekhez  
- **Biztonságos tárolás**: Hardverbiztonsági modulok (HSM-ek) vagy biztonságos kulcstárolók használata  
- **Token kötése**: Tokenek kötése meghatározott kliensekhez, munkamenetekhez vagy műveletekhez, ahol lehetséges  
- **Monitorozás és riasztás**: Tokenek visszaélésének vagy jogosulatlan hozzáférési mintáinak valós idejű észlelése  

## 3. **Munkamenet-biztonsági ellenőrzések**

### **Munkamenet-eltérítés megelőzése**

**Kezelt támadási vektorok:**
- **Munkamenet-eltérítés prompt injekcióval**: Rosszindulatú események befecskendezése a megosztott munkamenet-állapotba  
- **Munkamenet megszemélyesítése**: Ellopott munkamenet-azonosítók jogosulatlan használata a hitelesítés megkerülésére  
- **Újraindítható adatfolyam-támadások**: A szerver által küldött események újraindításának kihasználása rosszindulatú tartalom befecskendezésére  

**Kötelező munkamenet-ellenőrzések:**
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

**Szállítási biztonság:**
- **HTTPS kényszerítése**: Az összes munkamenet-kommunikáció TLS 1.3-on keresztül  
- **Biztonságos süti attribútumok**: HttpOnly, Secure, SameSite=Strict  
- **Tanúsítvány rögzítése**: Kritikus kapcsolatok esetén a közbeékelődéses támadások megelőzésére  

### **Állapotfüggő vs állapotfüggetlen megfontolások**

**Állapotfüggő implementációk esetén:**
- A megosztott munkamenet-állapot további védelmet igényel az injekciós támadások ellen  
- A soralapú munkamenet-kezelés integritásának ellenőrzése szükséges  
- Több szerverpéldány esetén biztonságos munkamenet-állapot szinkronizáció szükséges  

**Állapotfüggetlen implementációk esetén:**
- JWT vagy hasonló tokenalapú munkamenet-kezelés  
- A munkamenet-állapot integritásának kriptográfiai ellenőrzése  
- Csökkentett támadási felület, de robusztus tokenellenőrzést igényel  

## 4. **AI-specifikus biztonsági ellenőrzések**

### **Prompt injekció elleni védelem**

**Microsoft Prompt Shields integráció:**
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

**Implementációs ellenőrzések:**
- **Bemeneti tisztítás**: Az összes felhasználói bemenet átfogó ellenőrzése és szűrése  
- **Tartalmi határok meghatározása**: Egyértelmű elválasztás a rendszerutasítások és a felhasználói tartalom között  
- **Utasítási hierarchia**: Megfelelő prioritási szabályok az ellentmondó utasításokhoz  
- **Kimeneti monitorozás**: Potenciálisan káros vagy manipulált kimenetek észlelése  

### **Eszközmérgezés megelőzése**

**Eszközbiztonsági keretrendszer:**
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

**Dinamikus eszközkezelés:**
- **Jóváhagyási munkafolyamatok**: Felhasználói hozzájárulás az eszközmódosításokhoz  
- **Visszaállítási képességek**: Lehetőség az eszköz korábbi verzióira való visszatérésre  
- **Változási auditálás**: Az eszközdefiníció-módosítások teljes története  
- **Kockázatértékelés**: Az eszköz biztonsági helyzetének automatizált értékelése  

## 5. **Zavart helyettesítő támadások megelőzése**

### **OAuth proxy biztonság**

**Támadásmegelőzési ellenőrzések:**
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

**Implementációs követelmények:**
- **Felhasználói hozzájárulás ellenőrzése**: Soha ne hagyja ki a hozzájárulási képernyőket dinamikus kliensregisztráció esetén  
- **Átirányítási URI ellenőrzése**: Szigorú fehérlistás ellenőrzés az átirányítási célokhoz  
- **Engedélyezési kód védelem**: Rövid élettartamú kódok egyszeri használatának kényszerítése  
- **Kliensazonosság ellenőrzése**: A kliens hitelesítő adatok és metaadatok robusztus ellenőrzése  

## 6. **Eszközvégrehajtási biztonság**

### **Homokozás és izoláció**

**Konténeralapú izoláció:**
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

**Folyamatizoláció:**
- **Különálló folyamatkörnyezetek**: Minden eszközvégrehajtás izolált folyamatkörnyezetben  
- **Folyamatok közötti kommunikáció**: Biztonságos IPC mechanizmusok ellenőrzéssel  
- **Folyamatfigyelés**: Futásidejű viselkedéselemzés és anomáliaészlelés  
- **Erőforrás-korlátozás**: Szigorú CPU-, memória- és I/O-műveleti korlátok  

### **Minimális jogosultság elve**

**Jogosultságkezelés:**
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

## 7. **Ellátási lánc biztonsági ellenőrzések**

### **Függőségellenőrzés**

**Átfogó komponensbiztonság:**
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

### **Folyamatos monitorozás**

**Ellátási lánc fenyegetésészlelés:**
- **Függőségek egészségügyi monitorozása**: Az összes függőség folyamatos értékelése biztonsági problémák szempontjából  
- **Fenyegetési intelligencia integráció**: Valós idejű frissítések a felmerülő ellátási lánc fenyegetésekről  
- **Viselkedéselemzés**: Külső komponensek szokatlan viselkedésének észlelése  
- **Automatizált válasz**: Kompromittált komponensek azonnali elszigetelése  

## 8. **Monitorozási és észlelési ellenőrzések**

### **Biztonsági információ- és eseménykezelés (SIEM)**

**Átfogó naplózási stratégia:**
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

### **Valós idejű fenyegetésészlelés**

**Viselkedéselemzés:**
- **Felhasználói viselkedéselemzés (UBA)**: Szokatlan felhasználói hozzáférési minták észlelése  
- **Entitás viselkedéselemzés (EBA)**: MCP szerver és eszköz viselkedésének monitorozása  
- **Gépi tanulás alapú anomáliaészlelés**: AI-alapú biztonsági fenyegetések azonosítása  
- **Fenyegetési intelligencia korreláció**: Megfigyelt tevékenységek összevetése ismert támadási mintákkal  

## 9. **Incidensválasz és helyreállítás**

### **Automatizált válaszképességek**

**Azonnali válaszlépések:**
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

### **Igazságügyi képességek**

**Vizsgálati támogatás:**
- **Auditnaplók megőrzése**: Változtathatatlan naplózás kriptográfiai integritással  
- **Bizonyítékgyűjtés**: Releváns biztonsági artefaktumok automatizált gyűjtése  
- **Idővonal rekonstrukció**: Biztonsági incidensekhez vezető események részletes sorrendje  
- **Hatásértékelés**: A kompromittálás mértékének és az adatkitettségnek az értékelése  

## **Kulcsfontosságú biztonsági architektúra elvek**

### **Többrétegű védelem**
- **Többszintű biztonsági rétegek**: Nincs egyetlen hibapont a biztonsági architektúrában  
- **Redundáns ellenőrzések**: Átfedő biztonsági intézkedések kritikus funkciókhoz  
- **Biztonságos alapértelmezések**: Biztonságos alapbeállítások hibák vagy támadások esetén  

### **Zero Trust megközelítés**
- **Soha ne bízz, mindig ellenőrizz**: Az összes entitás és kérés folyamatos ellenőrzése  
- **Minimális jogosultság elve**: Minden komponens számára minimális hozzáférési jogok  
- **Mikroszegmentáció**: Finomhangolt hálózati és hozzáférés-ellenőrzések  

### **Folyamatos biztonsági fejlődés**
- **Fenyegetési környezethez való alkalmazkodás**: Rendszeres frissítések az új fenyegetések kezelésére  
- **Biztonsági ellenőrzések hatékonysága**: Az ellenőrzések folyamatos értékelése és javítása  
- **Specifikációs megfelelés**: Az MCP biztonsági szabványok fejlődéséhez való igazodás  

---

## **Implementációs források**

### **Hivatalos MCP dokumentáció**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Biztonsági Legjobb Gyakorlatok](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Engedélyezési Specifikáció](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft biztonsági megoldások**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/

**Felelősségkizárás**:  
Ez a dokumentum az [Co-op Translator](https://github.com/Azure/co-op-translator) AI fordítási szolgáltatás segítségével készült. Bár törekszünk a pontosságra, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az eredeti nyelvén tekintendő hiteles forrásnak. Kritikus információk esetén javasolt a professzionális, emberi fordítás igénybevétele. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy téves értelmezésekért.