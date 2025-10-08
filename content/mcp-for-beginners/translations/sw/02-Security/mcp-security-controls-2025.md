<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T14:38:31+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "sw"
}
-->
# Udhibiti wa Usalama wa MCP - Sasisho la Agosti 2025

> **Kiwango cha Sasa**: Hati hii inaonyesha mahitaji ya usalama ya [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) na [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) rasmi.

Model Context Protocol (MCP) imeimarika sana kwa udhibiti wa usalama ulioboreshwa unaoshughulikia vitisho vya jadi vya programu na vitisho maalum vya AI. Hati hii inatoa udhibiti wa kina wa usalama kwa utekelezaji salama wa MCP kuanzia Agosti 2025.

## **MAHITAJI YA LAZIMA YA Usalama**

### **Mambo Muhimu Yanayokatazwa kutoka kwa MCP Specification:**

> **IMEKATAZWA**: Seva za MCP **HAZIRUHUSIWI** kukubali tokeni zozote ambazo hazijatolewa wazi kwa seva ya MCP  
>
> **IMEKATAZWA**: Seva za MCP **HAZIRUHUSIWI** kutumia vikao kwa uthibitishaji  
>
> **INAHITAJIKA**: Seva za MCP zinazotekeleza idhini **LAZIMA** kuthibitisha maombi yote yanayoingia  
>
> **LAZIMA**: Seva za wakala wa MCP zinazotumia vitambulisho vya wateja vya static **LAZIMA** kupata idhini ya mtumiaji kwa kila mteja aliyesajiliwa kwa njia ya nguvu  

---

## 1. **Udhibiti wa Uthibitishaji na Idhini**

### **Ujumuishaji wa Mtoa Utambulisho wa Nje**

**Kiwango cha Sasa cha MCP (2025-06-18)** kinaruhusu seva za MCP kuhamisha uthibitishaji kwa watoa utambulisho wa nje, hatua kubwa ya kuboresha usalama:

**Faida za Usalama:**
1. **Kuondoa Hatari za Uthibitishaji wa Kawaida**: Kupunguza hatari kwa kuepuka utekelezaji wa uthibitishaji wa kawaida  
2. **Usalama wa Daraja la Biashara**: Kutumia watoa utambulisho waliothibitishwa kama Microsoft Entra ID na vipengele vya usalama vya hali ya juu  
3. **Usimamizi wa Utambulisho wa Kati**: Kurahisisha usimamizi wa mzunguko wa mtumiaji, udhibiti wa ufikiaji, na ukaguzi wa kufuata  
4. **Uthibitishaji wa Vipengele Vingi**: Kurithi uwezo wa MFA kutoka kwa watoa utambulisho wa biashara  
5. **Sera za Ufikiaji wa Masharti**: Kufaidika na udhibiti wa ufikiaji unaotegemea hatari na uthibitishaji unaobadilika  

**Mahitaji ya Utekelezaji:**
- **Uthibitishaji wa Hadhira ya Tokeni**: Hakikisha tokeni zote zimetolewa wazi kwa seva ya MCP  
- **Uthibitishaji wa Mtoaji**: Thibitisha mtoaji wa tokeni unalingana na mtoa utambulisho anayetarajiwa  
- **Uthibitishaji wa Saini**: Uthibitishaji wa kimaandishi wa uadilifu wa tokeni  
- **Utekelezaji wa Muda wa Kuisha**: Utekelezaji mkali wa mipaka ya muda wa tokeni  
- **Uthibitishaji wa Upeo**: Hakikisha tokeni zina ruhusa zinazofaa kwa shughuli zinazohitajika  

### **Usalama wa Mantiki ya Idhini**

**Udhibiti Muhimu:**
- **Ukaguzi wa Idhini wa Kina**: Mapitio ya mara kwa mara ya usalama wa sehemu zote za maamuzi ya idhini  
- **Chaguo za Kawaida Salama**: Kataa ufikiaji wakati mantiki ya idhini haiwezi kufanya uamuzi wa uhakika  
- **Mipaka ya Ruhusa**: Mgawanyo wazi kati ya viwango tofauti vya upendeleo na ufikiaji wa rasilimali  
- **Kumbukumbu za Ukaguzi**: Kumbukumbu kamili za maamuzi yote ya idhini kwa ufuatiliaji wa usalama  
- **Mapitio ya Mara kwa Mara ya Ufikiaji**: Uthibitishaji wa mara kwa mara wa ruhusa za watumiaji na mgawanyo wa upendeleo  

## 2. **Usalama wa Tokeni na Udhibiti wa Kupitisha**

### **Kuzuia Kupitisha Tokeni**

**Kupitisha tokeni kunakatazwa wazi** katika MCP Authorization Specification kutokana na hatari kubwa za usalama:

**Hatari za Usalama Zinazoshughulikiwa:**
- **Kuzunguka Udhibiti**: Kuepuka udhibiti muhimu wa usalama kama kupunguza kiwango, uthibitishaji wa maombi, na ufuatiliaji wa trafiki  
- **Kuvunjika kwa Uwajibikaji**: Kufanya utambulisho wa mteja kuwa haiwezekani, kuharibu njia za ukaguzi na uchunguzi wa matukio  
- **Uchimbaji wa Kivuli**: Kuruhusu wahusika wa uovu kutumia seva kama wakala wa ufikiaji wa data bila ruhusa  
- **Uvunjaji wa Mipaka ya Uaminifu**: Kuvunja dhana za uaminifu wa huduma za chini kuhusu asili ya tokeni  
- **Harakati za Kando**: Tokeni zilizovunjwa katika huduma nyingi huruhusu upanuzi mpana wa mashambulizi  

**Udhibiti wa Utekelezaji:**
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

### **Mifumo Salama ya Usimamizi wa Tokeni**

**Mbinu Bora:**
- **Tokeni za Muda Mfupi**: Punguza dirisha la hatari kwa mzunguko wa mara kwa mara wa tokeni  
- **Utoaji wa Wakati Muafaka**: Toa tokeni tu wakati zinahitajika kwa shughuli maalum  
- **Uhifadhi Salama**: Tumia moduli za usalama wa vifaa (HSMs) au hifadhi salama za funguo  
- **Ufungaji wa Tokeni**: Funga tokeni kwa wateja, vikao, au shughuli maalum inapowezekana  
- **Ufuatiliaji na Tahadhari**: Kugundua kwa wakati halisi matumizi mabaya ya tokeni au mifumo ya ufikiaji bila ruhusa  

## 3. **Udhibiti wa Usalama wa Vikao**

### **Kuzuia Utekaji wa Vikao**

**Njia za Mashambulizi Zinazoshughulikiwa:**
- **Utekeaji wa Vikao kwa Kuingiza Maelekezo**: Matukio ya uovu yaliyoingizwa katika hali ya vikao vilivyoshirikiwa  
- **Kujifanya Vikao**: Matumizi yasiyoidhinishwa ya vitambulisho vya vikao vilivyoibiwa ili kuepuka uthibitishaji  
- **Mashambulizi ya Mkusanyiko wa Mifumo**: Unyonyaji wa urejeshaji wa matukio yaliyotumwa na seva kwa kuingiza maudhui ya uovu  

**Udhibiti wa Lazima wa Vikao:**
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

**Usalama wa Usafirishaji:**
- **Utekelezaji wa HTTPS**: Mawasiliano yote ya vikao kupitia TLS 1.3  
- **Sifa Salama za Vidakuzi**: HttpOnly, Secure, SameSite=Strict  
- **Uwekaji wa Cheti**: Kwa miunganisho muhimu ili kuzuia mashambulizi ya MITM  

### **Mazingatio ya Hali ya Kihifadhi vs Isiyohifadhi**

**Kwa Utekelezaji wa Kihifadhi:**
- Hali ya vikao vilivyoshirikiwa inahitaji ulinzi wa ziada dhidi ya mashambulizi ya kuingiza  
- Usimamizi wa vikao kwa msingi wa foleni unahitaji uthibitishaji wa uadilifu  
- Seva nyingi zinahitaji usawazishaji salama wa hali ya vikao  

**Kwa Utekelezaji Usiohifadhi:**
- Usimamizi wa vikao kwa msingi wa JWT au tokeni zinazofanana  
- Uthibitishaji wa kimaandishi wa uadilifu wa hali ya vikao  
- Kupunguza uso wa mashambulizi lakini inahitaji uthibitishaji thabiti wa tokeni  

## 4. **Udhibiti wa Usalama Maalum wa AI**

### **Ulinzi Dhidi ya Kuingiza Maelekezo**

**Ujumuishaji wa Microsoft Prompt Shields:**
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

**Udhibiti wa Utekelezaji:**
- **Usafi wa Ingizo**: Uthibitishaji wa kina na uchujaji wa maingizo yote ya watumiaji  
- **Ufafanuzi wa Mipaka ya Maudhui**: Mgawanyo wazi kati ya maelekezo ya mfumo na maudhui ya mtumiaji  
- **Hierakia ya Maelekezo**: Sheria sahihi za kipaumbele kwa maelekezo yanayokinzana  
- **Ufuatiliaji wa Matokeo**: Kugundua matokeo yanayoweza kuwa hatari au yaliyobadilishwa  

### **Kuzuia Uchafuzi wa Zana**

**Mfumo wa Usalama wa Zana:**
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

**Usimamizi wa Zana wa Kiadinamik:**
- **Mifumo ya Idhini**: Idhini ya wazi ya mtumiaji kwa mabadiliko ya zana  
- **Uwezo wa Kurejesha**: Uwezo wa kurudi kwenye matoleo ya awali ya zana  
- **Ukaguzi wa Mabadiliko**: Historia kamili ya mabadiliko ya ufafanuzi wa zana  
- **Tathmini ya Hatari**: Uthibitishaji wa kiotomatiki wa hali ya usalama wa zana  

## 5. **Kuzuia Mashambulizi ya Naibu Aliyechanganyikiwa**

### **Usalama wa Wakala wa OAuth**

**Udhibiti wa Kuzuia Mashambulizi:**
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

**Mahitaji ya Utekelezaji:**
- **Uthibitishaji wa Idhini ya Mtumiaji**: Kamwe usiruke skrini za idhini kwa usajili wa wateja wa kiadinamik  
- **Uthibitishaji wa URI ya Uelekezaji**: Uthibitishaji mkali wa msingi wa orodha nyeupe wa maeneo ya uelekezaji  
- **Ulinzi wa Nambari ya Idhini**: Nambari za muda mfupi na utekelezaji wa matumizi moja  
- **Uthibitishaji wa Utambulisho wa Mteja**: Uthibitishaji thabiti wa hati za mteja na metadata  

## 6. **Usalama wa Utekelezaji wa Zana**

### **Uwekaji wa Sanduku na Kutengwa**

**Kutengwa kwa Msingi wa Kontena:**
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

**Kutengwa kwa Mchakato:**
- **Muktadha Tofauti wa Mchakato**: Kila utekelezaji wa zana katika nafasi ya mchakato iliyotengwa  
- **Mawasiliano ya Kati ya Michakato**: Mbinu salama za IPC na uthibitishaji  
- **Ufuatiliaji wa Mchakato**: Uchambuzi wa tabia wakati wa utekelezaji na kugundua hali zisizo za kawaida  
- **Utekelezaji wa Rasilimali**: Mipaka madhubuti ya CPU, kumbukumbu, na operesheni za I/O  

### **Utekelezaji wa Upendeleo Mdogo**

**Usimamizi wa Ruhusa:**
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

## 7. **Udhibiti wa Usalama wa Ugavi**

### **Uthibitishaji wa Utegemezi**

**Usalama wa Sehemu za Kina:**
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

### **Ufuatiliaji Endelevu**

**Kugundua Vitisho vya Ugavi:**
- **Ufuatiliaji wa Afya ya Utegemezi**: Tathmini endelevu ya utegemezi wote kwa masuala ya usalama  
- **Ujumuishaji wa Ujasusi wa Vitisho**: Sasisho za wakati halisi kuhusu vitisho vya ugavi vinavyoibuka  
- **Uchambuzi wa Tabia**: Kugundua tabia isiyo ya kawaida katika sehemu za nje  
- **Jibu la Kiotomatiki**: Kuzuia mara moja sehemu zilizoharibiwa  

## 8. **Udhibiti wa Ufuatiliaji na Kugundua**

### **Usimamizi wa Taarifa za Usalama na Matukio (SIEM)**

**Mkakati wa Kumbukumbu wa Kina:**
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

### **Kugundua Vitisho kwa Wakati Halisi**

**Uchambuzi wa Tabia:**
- **Uchambuzi wa Tabia ya Mtumiaji (UBA)**: Kugundua mifumo isiyo ya kawaida ya ufikiaji wa mtumiaji  
- **Uchambuzi wa Tabia ya Kitu (EBA)**: Ufuatiliaji wa tabia ya seva ya MCP na zana  
- **Kugundua Hali Isiyo ya Kawaida kwa Kujifunza kwa Mashine**: Utambulisho unaotegemea AI wa vitisho vya usalama  
- **Ulinganishaji wa Ujasusi wa Vitisho**: Kulinganisha shughuli zilizogunduliwa dhidi ya mifumo ya mashambulizi inayojulikana  

## 9. **Jibu la Matukio na Urejeshaji**

### **Uwezo wa Jibu la Kiotomatiki**

**Hatua za Jibu la Mara Moja:**
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

### **Uwezo wa Uchunguzi**

**Msaada wa Uchunguzi:**
- **Uhifadhi wa Njia za Ukaguzi**: Kumbukumbu zisizoweza kubadilishwa na uadilifu wa kimaandishi  
- **Ukusanyaji wa Ushahidi**: Ukusanyaji wa kiotomatiki wa vifaa vya usalama vinavyohusika  
- **Ujenzi wa Muda**: Mlolongo wa kina wa matukio yanayopelekea matukio ya usalama  
- **Tathmini ya Athari**: Ukadiriaji wa upeo wa uvunjaji na kufichuliwa kwa data  

## **Kanuni Muhimu za Usanifu wa Usalama**

### **Ulinzi kwa Kina**
- **Tabaka Nyingi za Usalama**: Hakuna sehemu moja ya kushindwa katika usanifu wa usalama  
- **Udhibiti wa Ziada**: Hatua za usalama zinazofanana kwa kazi muhimu  
- **Mifumo Salama ya Kawaida**: Chaguo salama wakati mifumo inakutana na makosa au mashambulizi  

### **Utekelezaji wa Uaminifu Sifuri**
- **Kamwe Usiamini, Kagua Kila Wakati**: Uthibitishaji endelevu wa vyombo vyote na maombi  
- **Kanuni ya Upendeleo Mdogo**: Haki za ufikiaji za kiwango cha chini kwa sehemu zote  
- **Mgawanyo wa Ndani**: Udhibiti wa mtandao na ufikiaji wa granular  

### **Mageuzi Endelevu ya Usalama**
- **Urekebishaji wa Mandhari ya Vitisho**: Sasisho za mara kwa mara kushughulikia vitisho vinavyoibuka  
- **Ufanisi wa Udhibiti wa Usalama**: Tathmini endelevu na uboreshaji wa udhibiti  
- **Ufuataji wa Maelezo**: Ulinganifu na viwango vya usalama vya MCP vinavyoendelea kubadilika  

---

## **Rasilimali za Utekelezaji**

### **Hati Rasmi za MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Suluhisho za Usalama za Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Viwango vya Usalama**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Muhimu**: Udhibiti huu wa usalama unaonyesha maelezo ya sasa ya MCP (2025-06-18). Kagua kila wakati dhidi ya [hati rasmi](https://spec.modelcontextprotocol.io/) kwani viwango vinaendelea kubadilika haraka.

**Kanusho**:  
Hati hii imetafsiriwa kwa kutumia huduma ya kutafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kuhakikisha usahihi, tafadhali fahamu kuwa tafsiri za kiotomatiki zinaweza kuwa na makosa au kutokuwa sahihi. Hati ya asili katika lugha yake ya awali inapaswa kuzingatiwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu ya binadamu inapendekezwa. Hatutawajibika kwa kutoelewana au tafsiri zisizo sahihi zinazotokana na matumizi ya tafsiri hii.