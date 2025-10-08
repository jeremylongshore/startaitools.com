<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-26T19:08:23+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "lt"
}
-->
# MCP Saugumo Kontrolės - 2025 m. rugpjūčio atnaujinimas

> **Dabartinis standartas**: Šis dokumentas atspindi [MCP specifikacijos 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) saugumo reikalavimus ir oficialias [MCP saugumo geriausias praktikas](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) reikšmingai patobulėjo, įtraukiant sustiprintas saugumo kontrolės priemones, kurios apima tiek tradicinį programinės įrangos saugumą, tiek AI specifines grėsmes. Šis dokumentas pateikia išsamias saugumo kontrolės priemones, skirtas saugiam MCP įgyvendinimui nuo 2025 m. rugpjūčio.

## **PRIVALOMI saugumo reikalavimai**

### **Kritiniai MCP specifikacijos draudimai:**

> **DRAUDŽIAMA**: MCP serveriai **NETURI** priimti jokių žetonų, kurie nebuvo aiškiai išduoti MCP serveriui  
>
> **DRAUDŽIAMA**: MCP serveriai **NETURI** naudoti sesijų autentifikacijai  
>
> **PRIVALOMA**: MCP serveriai, įgyvendinantys autorizaciją, **TURI** patikrinti VISUS gaunamus užklausimus  
>
> **PRIVALOMA**: MCP proxy serveriai, naudojantys statinius klientų ID, **TURI** gauti vartotojo sutikimą kiekvienam dinamiškai registruotam klientui  

---

## 1. **Autentifikacijos ir autorizacijos kontrolės**

### **Išorinių tapatybės teikėjų integracija**

**Dabartinis MCP standartas (2025-06-18)** leidžia MCP serveriams deleguoti autentifikaciją išoriniams tapatybės teikėjams, kas žymiai pagerina saugumą:

**Saugumo privalumai:**
1. **Pašalina individualios autentifikacijos rizikas**: Sumažina pažeidžiamumo paviršių, išvengiant individualių autentifikacijos įgyvendinimų  
2. **Įmonės lygio saugumas**: Naudoja patikimus tapatybės teikėjus, tokius kaip Microsoft Entra ID, su pažangiomis saugumo funkcijomis  
3. **Centralizuotas tapatybės valdymas**: Supaprastina vartotojų gyvavimo ciklo valdymą, prieigos kontrolę ir atitikties auditą  
4. **Daugiafaktorė autentifikacija**: Paveldi MFA galimybes iš įmonės tapatybės teikėjų  
5. **Sąlyginių prieigos politikų taikymas**: Naudoja rizika pagrįstą prieigos kontrolę ir adaptyvią autentifikaciją  

**Įgyvendinimo reikalavimai:**
- **Žetono auditorijos patikrinimas**: Patikrinkite, ar visi žetonai buvo aiškiai išduoti MCP serveriui  
- **Išdavėjo patikrinimas**: Patikrinkite, ar žetono išdavėjas atitinka tikėtiną tapatybės teikėją  
- **Parašo patikrinimas**: Kriptografinis žetono vientisumo patikrinimas  
- **Galiojimo laiko užtikrinimas**: Griežtas žetono galiojimo laiko ribų laikymasis  
- **Apimties patikrinimas**: Užtikrinkite, kad žetonai turėtų tinkamus leidimus prašomoms operacijoms  

### **Autorizacijos logikos saugumas**

**Kritinės kontrolės priemonės:**
- **Išsamūs autorizacijos auditai**: Reguliarūs saugumo peržiūros visuose autorizacijos sprendimų taškuose  
- **Saugios numatytosios reikšmės**: Atmesti prieigą, kai autorizacijos logika negali priimti aiškaus sprendimo  
- **Leidimų ribos**: Aiškus skirtingų privilegijų lygių ir išteklių prieigos atskyrimas  
- **Audito žurnalai**: Visiškas visų autorizacijos sprendimų registravimas saugumo stebėjimui  
- **Reguliarūs prieigos peržiūros**: Periodinis vartotojų leidimų ir privilegijų priskyrimų patikrinimas  

## 2. **Žetonų saugumas ir apsauga nuo perdavimo**

### **Žetonų perdavimo prevencija**

**Žetonų perdavimas yra griežtai draudžiamas** MCP autorizacijos specifikacijoje dėl kritinių saugumo rizikų:

**Sprendžiamos saugumo rizikos:**
- **Kontrolės apeinimas**: Apeina esmines saugumo kontrolės priemones, tokias kaip užklausų ribojimas, užklausų patikrinimas ir srauto stebėjimas  
- **Atsakomybės praradimas**: Neįmanoma identifikuoti kliento, sugadinant audito pėdsakus ir incidentų tyrimus  
- **Ištraukimas per proxy**: Leidžia piktavaliams naudoti serverius kaip proxy neleistinai duomenų prieigai  
- **Pasitikėjimo ribų pažeidimai**: Sugadina pasitikėjimo prielaidas apie žetonų kilmę paslaugų grandinėje  
- **Šoninis judėjimas**: Kompromituoti žetonai tarp kelių paslaugų leidžia platesnį atakų plitimą  

**Įgyvendinimo kontrolės priemonės:**
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

### **Saugūs žetonų valdymo modeliai**

**Geriausios praktikos:**
- **Trumpalaikiai žetonai**: Sumažinkite pažeidžiamumo langą dažnai sukdami žetonus  
- **Išdavimas pagal poreikį**: Išduokite žetonus tik tada, kai jų reikia konkrečioms operacijoms  
- **Saugus saugojimas**: Naudokite aparatinės įrangos saugumo modulius (HSM) arba saugius raktų saugyklas  
- **Žetonų susiejimas**: Susiekite žetonus su konkrečiais klientais, sesijomis ar operacijomis, kai įmanoma  
- **Stebėjimas ir įspėjimai**: Realaus laiko žetonų netinkamo naudojimo ar neleistinos prieigos modelių aptikimas  

## 3. **Sesijų saugumo kontrolės**

### **Sesijų užgrobimo prevencija**

**Sprendžiami atakų vektoriai:**
- **Sesijos užgrobimo injekcija**: Kenkėjiški įvykiai, įterpti į bendrą sesijos būseną  
- **Sesijos apsimetimas**: Neleistinas pavogtų sesijos ID naudojimas autentifikacijai apeiti  
- **Atnaujinamų srautų atakos**: Serverio siunčiamų įvykių atnaujinimo išnaudojimas kenkėjiškam turiniui įterpti  

**Privalomos sesijų kontrolės priemonės:**
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

**Transporto saugumas:**
- **HTTPS užtikrinimas**: Visa sesijų komunikacija per TLS 1.3  
- **Saugūs slapukų atributai**: HttpOnly, Secure, SameSite=Strict  
- **Sertifikatų prisegimas**: Kritinėms jungtims, siekiant išvengti MITM atakų  

### **Valstybinės ir bevalstybinės sesijos**

**Valstybinėms įgyvendinimams:**
- Bendros sesijos būsenos apsauga nuo injekcijos atakų  
- Eilių pagrindu valdomų sesijų vientisumo patikrinimas  
- Kelių serverių egzempliorių sesijos būsenos sinchronizavimas  

**Bevalstybinėms įgyvendinimams:**
- JWT ar panašūs žetonų pagrindu valdomi sesijų modeliai  
- Kriptografinis sesijos būsenos vientisumo patikrinimas  
- Sumažintas atakų paviršius, tačiau reikalingas tvirtas žetonų patikrinimas  

## 4. **AI specifinės saugumo kontrolės**

### **Įvesties injekcijos gynyba**

**Microsoft Prompt Shields integracija:**
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

**Įgyvendinimo kontrolės priemonės:**
- **Įvesties valymas**: Išsamus visų vartotojo įvestų duomenų patikrinimas ir filtravimas  
- **Turinio ribų apibrėžimas**: Aiškus sistemos instrukcijų ir vartotojo turinio atskyrimas  
- **Instrukcijų hierarchija**: Tinkamos pirmenybės taisyklės konfliktuojančioms instrukcijoms  
- **Išvesties stebėjimas**: Potencialiai kenksmingų ar manipuliuotų išvesties aptikimas  

### **Įrankių užnuodijimo prevencija**

**Įrankių saugumo sistema:**
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

**Dinaminis įrankių valdymas:**
- **Patvirtinimo procesai**: Aiškus vartotojo sutikimas dėl įrankių pakeitimų  
- **Grąžinimo galimybės**: Galimybė grįžti prie ankstesnių įrankių versijų  
- **Pakeitimų auditas**: Išsamus įrankių apibrėžimų pakeitimų istorijos registravimas  
- **Rizikos vertinimas**: Automatinis įrankių saugumo būklės įvertinimas  

## 5. **Suklaidinto tarpininko atakų prevencija**

### **OAuth proxy saugumas**

**Atakų prevencijos kontrolės priemonės:**
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

**Įgyvendinimo reikalavimai:**
- **Vartotojo sutikimo patikrinimas**: Niekada nepraleiskite sutikimo ekranų dinamiškai registruojant klientus  
- **Peradresavimo URI patikrinimas**: Griežtas baltųjų sąrašų pagrindu atliekamas peradresavimo tikslų patikrinimas  
- **Autorizacijos kodo apsauga**: Trumpalaikiai kodai su vienkartinio naudojimo užtikrinimu  
- **Kliento tapatybės patikrinimas**: Tvirtas klientų kredencialų ir metaduomenų patikrinimas  

## 6. **Įrankių vykdymo saugumas**

### **Izoliacija ir smėlio dėžės**

**Konteinerių pagrindu vykdoma izoliacija:**
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

**Procesų izoliacija:**
- **Atskiri procesų kontekstai**: Kiekvieno įrankio vykdymas atskirame procesų erdvėje  
- **Tarpusavio procesų komunikacija**: Saugūs IPC mechanizmai su patikrinimu  
- **Procesų stebėjimas**: Veikimo analizė ir anomalijų aptikimas vykdymo metu  
- **Išteklių ribojimas**: Griežtos CPU, atminties ir I/O operacijų ribos  

### **Minimalios privilegijos įgyvendinimas**

**Leidimų valdymas:**
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

## 7. **Tiekimo grandinės saugumo kontrolės**

### **Priklausomybių patikrinimas**

**Išsami komponentų sauga:**
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

### **Nuolatinis stebėjimas**

**Tiekimo grandinės grėsmių aptikimas:**
- **Priklausomybių sveikatos stebėjimas**: Nuolatinis visų priklausomybių saugumo problemų vertinimas  
- **Grėsmių žvalgybos integracija**: Realaus laiko atnaujinimai apie naujas tiekimo grandinės grėsmes  
- **Elgesio analizė**: Neįprasto išorinių komponentų elgesio aptikimas  
- **Automatinis atsakas**: Nedelsiant izoliuoti kompromituotus komponentus  

## 8. **Stebėjimo ir aptikimo kontrolės**

### **Saugumo informacijos ir įvykių valdymas (SIEM)**

**Išsami registravimo strategija:**
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

### **Realaus laiko grėsmių aptikimas**

**Elgesio analizė:**
- **Vartotojų elgesio analizė (UBA)**: Neįprastų vartotojų prieigos modelių aptikimas  
- **Subjektų elgesio analizė (EBA)**: MCP serverio ir įrankių elgesio stebėjimas  
- **Mašininio mokymosi anomalijų aptikimas**: AI pagrįstas saugumo grėsmių identifikavimas  
- **Grėsmių žvalgybos koreliacija**: Stebimų veiklų atitikimas žinomiems atakų modeliams  

## 9. **Incidentų valdymas ir atkūrimas**

### **Automatizuotos atsako galimybės**

**Nedelsiant vykdomi veiksmai:**
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

### **Teismo ekspertizės galimybės**

**Tyrimų palaikymas:**
- **Audito pėdsakų išsaugojimas**: Nekintamas registravimas su kriptografiniu vientisumu  
- **Įrodymų rinkimas**: Automatinis susijusių saugumo artefaktų surinkimas  
- **Laiko juostos atkūrimas**: Išsamus įvykių, vedusių į saugumo incidentus, sekos atkūrimas  
- **Poveikio vertinimas**: Kompromiso masto ir duomenų atskleidimo įvertinimas  

## **Pagrindiniai saugumo architektūros principai**

### **Gynyba gylio principu**
- **Keli saugumo sluoksniai**: Nėra vieno saugumo architektūros gedimo taško  
- **Redundantinės kontrolės**: Persidengiančios saugumo priemonės kritinėms funkcijoms  
- **Saugios numatytosios reikšmės**: Saugūs numatytieji nustatymai, kai sistemos susiduria su klaidomis ar atakomis  

### **Zero Trust įgyvendinimas**
- **Niekada nepasitikėk, visada tikrink**: Nuolatinis visų subjektų ir užklausų tikrinimas  
- **Minimalios privilegijos principas**: Minimalios prieigos teisės visiems komponentams  
- **Mikrosegmentacija**: Granuliuota tinklo ir prieigos kontrolė  

### **Nuolatinė saugumo evoliucija**
- **Grėsmių kraštovaizdžio adaptacija**: Reguliarūs atnaujinimai, siekiant spręsti naujas grėsmes  
- **Saugumo kontrolės efektyvumas**: Nuolatinis kontrolės priemonių vertinimas ir tobulinimas  
- **Specifikacijų laikymasis**: Atitikimas besikeičiantiems MCP saugumo standartams  

---

## **Įgyvendinimo ištekliai**

### **Oficiali MCP dokumentacija**
- [MCP specifikacija (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP saugumo geriausios praktikos](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP autorizacijos specifikacija](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft saugumo sprendimai**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Saugumo standartai**
- [OAuth 2.0 saugumo geriausios praktikos (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 dideliems kalbos modeliams](https://genai.owasp.org/)  
- [NIST kibernetinio saugumo sistema](https://www.nist.gov/cyberframework)  

---

> **Svarbu**: Šios saugumo kontrolės priemonės atspindi dabartinę MCP specifikaciją (2025-06-18). Visada patikrinkite pagal naujausią [oficialią dokumentaciją](https://spec.modelcontextprotocol.io/), nes standartai greitai keičiasi.

---

**Atsakomybės apribojimas**:  
Šis dokumentas buvo išverstas naudojant AI vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojama naudoti profesionalų žmogaus vertimą. Mes neprisiimame atsakomybės už nesusipratimus ar klaidingus interpretavimus, atsiradusius dėl šio vertimo naudojimo.