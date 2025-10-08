<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T16:11:50+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "fi"
}
-->
# MCP:n tietoturvakontrollit - Elokuu 2025 Päivitys

> **Nykyinen standardi**: Tämä asiakirja heijastaa [MCP-määrityksen 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) tietoturvavaatimuksia ja virallisia [MCP:n tietoturvan parhaat käytännöt](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) on kehittynyt merkittävästi, ja siinä on parannettu tietoturvakontrolleja, jotka käsittelevät sekä perinteisiä ohjelmistoturvallisuusuhkia että tekoälyyn liittyviä uhkia. Tämä asiakirja tarjoaa kattavat tietoturvakontrollit turvallisten MCP-toteutusten varmistamiseksi elokuussa 2025.

## **PAKOLLISET tietoturvavaatimukset**

### **MCP-määrityksen kriittiset kiellot:**

> **KIELLETTY**: MCP-palvelimet **EIVÄT SAA** hyväksyä mitään tunnuksia, joita ei ole nimenomaisesti myönnetty MCP-palvelimelle  
>
> **KIELLETTY**: MCP-palvelimet **EIVÄT SAA** käyttää istuntoja todennukseen  
>
> **VAADITTU**: MCP-palvelimien, jotka toteuttavat valtuutuksen, **TÄYTYY** tarkistaa KAIKKI saapuvat pyynnöt  
>
> **PAKOLLINEN**: MCP-välityspalvelimien, jotka käyttävät staattisia asiakastunnuksia, **TÄYTYY** hankkia käyttäjän suostumus jokaiselle dynaamisesti rekisteröidylle asiakkaalle  

---

## 1. **Todennus- ja valtuutuskontrollit**

### **Ulkopuolisen identiteettipalveluntarjoajan integrointi**

**Nykyinen MCP-standardi (2025-06-18)** sallii MCP-palvelimien delegoida todennuksen ulkopuolisille identiteettipalveluntarjoajille, mikä edustaa merkittävää tietoturvaparannusta:

**Tietoturvaedut:**
1. **Poistaa mukautetun todennuksen riskit**: Vähentää haavoittuvuuksia välttämällä mukautettuja todennustoteutuksia  
2. **Yritystason turvallisuus**: Hyödyntää vakiintuneita identiteettipalveluntarjoajia, kuten Microsoft Entra ID:tä, edistyneillä tietoturvaominaisuuksilla  
3. **Keskitetty identiteetinhallinta**: Yksinkertaistaa käyttäjän elinkaaren hallintaa, käyttöoikeuksien hallintaa ja vaatimustenmukaisuuden auditointia  
4. **Monivaiheinen todennus**: Perii MFA-ominaisuudet yrityksen identiteettipalveluntarjoajilta  
5. **Ehdolliset käyttöpolitiikat**: Hyötyy riskipohjaisista käyttöoikeuskontrolleista ja mukautuvasta todennuksesta  

**Toteutusvaatimukset:**
- **Tunnuksen kohdevalidointi**: Varmista, että kaikki tunnukset on nimenomaisesti myönnetty MCP-palvelimelle  
- **Myöntäjän validointi**: Varmista, että tunnuksen myöntäjä vastaa odotettua identiteettipalveluntarjoajaa  
- **Allekirjoituksen validointi**: Kryptografinen tarkistus tunnuksen eheyden varmistamiseksi  
- **Vanhenemisen valvonta**: Tiukka tunnuksen elinkaaren rajoitusten noudattaminen  
- **Laajuuden validointi**: Varmista, että tunnuksilla on asianmukaiset käyttöoikeudet pyydettyihin toimintoihin  

### **Valtuutuslogiikan turvallisuus**

**Kriittiset kontrollit:**
- **Kattavat valtuutusauditoinnit**: Säännölliset tietoturvatarkastukset kaikissa valtuutuspäätöspisteissä  
- **Vikasietoiset oletukset**: Käyttöoikeuden epääminen, kun valtuutuslogiikka ei pysty tekemään yksiselitteistä päätöstä  
- **Käyttöoikeusrajat**: Selkeä erottelu eri käyttöoikeustasojen ja resurssien välillä  
- **Auditointilokitus**: Kaikkien valtuutuspäätösten täydellinen lokitus tietoturvavalvontaa varten  
- **Säännölliset käyttöoikeustarkistukset**: Käyttäjän käyttöoikeuksien ja käyttöoikeuksien säännöllinen tarkistaminen  

## 2. **Tunnusturvallisuus ja läpivientikontrollit**

### **Tunnuksen läpiviennin estäminen**

**Tunnuksen läpivienti on nimenomaisesti kielletty** MCP:n valtuutusmäärityksessä kriittisten tietoturvariskien vuoksi:

**Ratkaistut tietoturvariskit:**
- **Kontrollien kiertäminen**: Ohittaa olennaiset tietoturvakontrollit, kuten nopeusrajoitukset, pyyntöjen validoinnin ja liikenteen valvonnan  
- **Vastuullisuuden heikkeneminen**: Estää asiakkaiden tunnistamisen, mikä heikentää auditointijälkiä ja tapaustutkintaa  
- **Välityspohjainen tietojen vuotaminen**: Mahdollistaa haitallisten toimijoiden käyttää palvelimia välityspalvelimina luvattomaan tiedonhakuun  
- **Luottamusrajojen rikkominen**: Rikkoo alaspäin suuntautuvien palveluiden luottamusoletukset tunnuksen alkuperästä  
- **Sivuttaisliike**: Kompromissitunnukset useissa palveluissa mahdollistavat laajemman hyökkäyksen laajentamisen  

**Toteutuskontrollit:**
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

### **Turvalliset tunnusten hallintamallit**

**Parhaat käytännöt:**
- **Lyhytikäiset tunnukset**: Minimoi altistusaika usein tapahtuvalla tunnusten kierrätyksellä  
- **Tarpeen mukainen myöntäminen**: Myönnä tunnuksia vain tarvittaessa tiettyihin toimintoihin  
- **Turvallinen säilytys**: Käytä laitteistopohjaisia turvallisuusmoduuleja (HSM) tai turvallisia avainsäilöjä  
- **Tunnuksen sitominen**: Sido tunnukset tiettyihin asiakkaisiin, istuntoihin tai toimintoihin mahdollisuuksien mukaan  
- **Valvonta ja hälytys**: Reaaliaikainen tunnusten väärinkäytön tai luvattoman käytön havaitseminen  

## 3. **Istuntoturvallisuuskontrollit**

### **Istunnon kaappauksen estäminen**

**Käsitellyt hyökkäysvektorit:**
- **Istunnon kaappauksen syöteinjektio**: Haitallisten tapahtumien syöttäminen jaetun istuntotilan kautta  
- **Istunnon väärentäminen**: Varastettujen istuntotunnusten luvaton käyttö todennuksen ohittamiseksi  
- **Jatkuvien virtojen hyökkäykset**: Palvelimen lähettämien tapahtumien jatkamisen hyväksikäyttö haitallisen sisällön syöttämiseksi  

**Pakolliset istuntokontrollit:**
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

**Kuljetusturvallisuus:**
- **HTTPS:n pakottaminen**: Kaikki istuntoviestintä TLS 1.3:n kautta  
- **Turvalliset evästeominaisuudet**: HttpOnly, Secure, SameSite=Strict  
- **Sertifikaattien kiinnitys**: Kriittisille yhteyksille MITM-hyökkäysten estämiseksi  

### **Tilalliset vs tilattomat näkökohdat**

**Tilallisille toteutuksille:**
- Jaettu istuntotila vaatii lisäsuojauksia injektiohyökkäyksiä vastaan  
- Jonopohjainen istuntohallinta tarvitsee eheystarkistuksen  
- Useat palvelininstanssit vaativat turvallisen istuntotilan synkronoinnin  

**Tilattomille toteutuksille:**
- JWT- tai vastaava tunnuspohjainen istuntohallinta  
- Kryptografinen tarkistus istuntotilan eheyden varmistamiseksi  
- Pienempi hyökkäyspinta, mutta vaatii vahvaa tunnusten validointia  

## 4. **Tekoälyyn liittyvät tietoturvakontrollit**

### **Syöteinjektioiden torjunta**

**Microsoft Prompt Shields -integraatio:**
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

**Toteutuskontrollit:**
- **Syötteiden puhdistus**: Kaikkien käyttäjän syötteiden kattava validointi ja suodatus  
- **Sisältörajojen määrittely**: Selkeä erottelu järjestelmän ohjeiden ja käyttäjän sisällön välillä  
- **Ohjehierarkia**: Asianmukaiset etusijajärjestykset ristiriitaisille ohjeille  
- **Tuotosten valvonta**: Mahdollisesti haitallisten tai manipuloitujen tuotosten havaitseminen  

### **Työkalujen myrkyttämisen estäminen**

**Työkalujen tietoturvakehys:**
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

**Dynaaminen työkalujen hallinta:**
- **Hyväksyntätyönkulut**: Käyttäjän nimenomainen suostumus työkalumuutoksille  
- **Palautusominaisuudet**: Mahdollisuus palauttaa aiempiin työkalujen versioihin  
- **Muutosten auditointi**: Työkalumääritelmien muutosten täydellinen historia  
- **Riskiarviointi**: Työkalujen tietoturvatilanteen automaattinen arviointi  

## 5. **Confused Deputy -hyökkäysten estäminen**

### **OAuth-välityspalvelimen turvallisuus**

**Hyökkäysten estokontrollit:**
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

**Toteutusvaatimukset:**
- **Käyttäjän suostumuksen tarkistus**: Älä koskaan ohita suostumusnäyttöjä dynaamisessa asiakasrekisteröinnissä  
- **Uudelleenohjaus-URI:n validointi**: Tiukka sallittuihin kohteisiin perustuva validointi  
- **Valtuutuskoodin suojaus**: Lyhytikäiset koodit, joiden käyttö on kertaluonteista  
- **Asiakastunnistuksen validointi**: Asiakastunnusten ja metatietojen vahva tarkistus  

## 6. **Työkalujen suorittamisen turvallisuus**

### **Hiekkalaatikointi ja eristäminen**

**Konttipohjainen eristäminen:**
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

**Prosessien eristäminen:**
- **Eri prosessikontekstit**: Jokainen työkalun suoritus eristetyssä prosessitilassa  
- **Prosessien välinen viestintä**: Turvalliset IPC-mekanismit validoinnilla  
- **Prosessien valvonta**: Suoritusajan käyttäytymisen analyysi ja poikkeamien havaitseminen  
- **Resurssien valvonta**: Tiukat rajoitukset suorittimen, muistin ja I/O-toimintojen käytölle  

### **Vähimpien oikeuksien periaate**

**Käyttöoikeuksien hallinta:**
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

## 7. **Toimitusketjun tietoturvakontrollit**

### **Riippuvuuksien validointi**

**Kattava komponenttien turvallisuus:**
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

### **Jatkuva valvonta**

**Toimitusketjun uhkien havaitseminen:**
- **Riippuvuuksien terveysvalvonta**: Kaikkien riippuvuuksien jatkuva arviointi tietoturvaongelmien varalta  
- **Uhkatiedustelun integrointi**: Reaaliaikaiset päivitykset toimitusketjun uusista uhista  
- **Käyttäytymisanalyysi**: Ulkoisten komponenttien epätavallisen käyttäytymisen havaitseminen  
- **Automaattinen reagointi**: Kompromissien sisältämien komponenttien välitön eristäminen  

## 8. **Valvonta- ja havaitsemiskontrollit**

### **Tietoturvatiedon ja tapahtumien hallinta (SIEM)**

**Kattava lokitusstrategia:**
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

### **Reaaliaikainen uhkien havaitseminen**

**Käyttäytymisanalytiikka:**
- **Käyttäjäkäyttäytymisen analytiikka (UBA)**: Epätavallisten käyttäjätoimintojen havaitseminen  
- **Entiteettikäyttäytymisen analytiikka (EBA)**: MCP-palvelimen ja työkalujen käyttäytymisen valvonta  
- **Koneoppimisen poikkeamien havaitseminen**: Tekoälypohjainen tietoturvauhkien tunnistaminen  
- **Uhkatiedustelun korrelaatio**: Havaittujen toimintojen yhdistäminen tunnettuihin hyökkäysmalleihin  

## 9. **Tapahtumien hallinta ja palautuminen**

### **Automaattiset reagointikyvyt**

**Välittömät toimenpiteet:**
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

### **Oikeuslääketieteelliset kyvyt**

**Tutkinnan tuki:**
- **Auditointijälkien säilyttäminen**: Muuttumaton lokitus kryptografisella eheydellä  
- **Todisteiden kerääminen**: Automaattinen asiaankuuluvien tietoturva-aineistojen kerääminen  
- **Aikajanan rekonstruointi**: Yksityiskohtainen tapahtumien kulku ennen tietoturvaloukkausta  
- **Vaikutusten arviointi**: Kompromissin laajuuden ja tietovuodon arviointi  

## **Keskeiset tietoturva-arkkitehtuurin periaatteet**

### **Syvyyspuolustus**
- **Useita tietoturvakerroksia**: Ei yksittäistä tietoturva-arkkitehtuurin epäonnistumispistettä  
- **Päällekkäiset kontrollit**: Päällekkäiset tietoturvatoimenpiteet kriittisille toiminnoille  
- **Vikasietomekanismit**: Turvalliset oletukset, kun järjestelmät kohtaavat virheitä tai hyökkäyksiä  

### **Zero Trust -toteutus**
- **Älä koskaan luota, varmista aina**: Jatkuva kaikkien toimijoiden ja pyyntöjen validointi  
- **Vähimpien oikeuksien periaate**: Minimioikeudet kaikille komponenteille  
- **Mikrosegmentointi**: Tarkat verkko- ja käyttöoikeuskontrollit  

### **Jatkuva tietoturvan kehitys**
- **Uhkakentän mukautuminen**: Säännölliset päivitykset uusien uhkien torjumiseksi  
- **Tietoturvakontrollien tehokkuus**: Kontrollien jatkuva arviointi ja parantaminen  
- **Määritysten noudattaminen**: Yhdenmukaisuus kehittyvien MCP-tietoturvastandardien kanssa  

---

## **Toteutusresurssit**

### **Virallinen MCP-dokumentaatio**
- [MCP-määritys (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP:n tietoturvan parhaat käytännöt](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP:n valtuutusmääritys](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoftin tietoturvaratkaisut**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Tietoturvastandardit**
- [OAuth 2.0:n tietoturvan parhaat käytännöt (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 suurille kielimalleille](https://genai.owasp.org/)  
- [NIST:n kyberturvallisuuskehys](https://www.nist.gov/cyberframework)  

---

> **Tärkeää**: Nämä tietoturvakontrollit heijastavat nykyistä MCP-määritystä (2025-06-18). Tarkista aina viimeisimmät [viralliset dokumentit](https://spec.modelcontextprotocol.io/), sillä standardit kehittyvät nopeasti.  

**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, huomioithan, että automaattiset käännökset voivat sisältää virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäisellä kielellä tulisi pitää ensisijaisena lähteenä. Kriittisen tiedon osalta suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa väärinkäsityksistä tai virhetulkinnoista, jotka johtuvat tämän käännöksen käytöstä.