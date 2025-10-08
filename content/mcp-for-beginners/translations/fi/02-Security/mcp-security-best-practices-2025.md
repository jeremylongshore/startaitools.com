<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T16:06:50+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "fi"
}
-->
# MCP:n turvallisuuskäytännöt - Päivitys elokuu 2025

> **Tärkeää**: Tämä asiakirja heijastaa uusimpia [MCP-määrityksen 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) turvallisuusvaatimuksia ja virallisia [MCP:n turvallisuuskäytäntöjä](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Tarkista aina ajantasaiset ohjeet nykyisestä määrityksestä.

## Keskeiset turvallisuuskäytännöt MCP-toteutuksille

Model Context Protocol tuo mukanaan ainutlaatuisia turvallisuushaasteita, jotka ylittävät perinteisen ohjelmistoturvallisuuden. Nämä käytännöt käsittelevät sekä perusturvallisuusvaatimuksia että MCP-spesifisiä uhkia, kuten kehotteen injektiota, työkalujen manipulointia, istunnon kaappaamista, "hämmentynyt apulainen" -ongelmia ja tunnusten välityshaavoittuvuuksia.

### **PAKOLLISET turvallisuusvaatimukset**

**Keskeiset vaatimukset MCP-määrityksestä:**

> **EI SAA**: MCP-palvelimet **EIVÄT SAA** hyväksyä tunnuksia, joita ei ole nimenomaisesti myönnetty MCP-palvelimelle  
> 
> **ON PAKKO**: MCP-palvelimien, jotka toteuttavat valtuutuksen, **ON PAKKO** tarkistaa KAIKKI saapuvat pyynnöt  
>  
> **EI SAA**: MCP-palvelimet **EIVÄT SAA** käyttää istuntoja todennukseen  
>
> **ON PAKKO**: MCP-välityspalvelimien, jotka käyttävät staattisia asiakastunnuksia, **ON PAKKO** hankkia käyttäjän suostumus jokaiselle dynaamisesti rekisteröidylle asiakkaalle  

---

## 1. **Tunnusten turvallisuus ja todennus**

**Todennus- ja valtuutuskontrollit:**
   - **Perusteellinen valtuutuksen tarkistus**: Suorita kattavat auditoinnit MCP-palvelimen valtuutuslogiikasta varmistaaksesi, että vain tarkoitetut käyttäjät ja asiakkaat pääsevät resursseihin  
   - **Ulkoinen identiteettipalveluntarjoaja**: Käytä vakiintuneita identiteettipalveluntarjoajia, kuten Microsoft Entra ID:tä, sen sijaan että toteuttaisit oman todennuksen  
   - **Tunnusten kohdevalidointi**: Varmista aina, että tunnukset on nimenomaisesti myönnetty MCP-palvelimellesi - älä koskaan hyväksy ylävirran tunnuksia  
   - **Tunnusten elinkaaren hallinta**: Toteuta turvallinen tunnusten kierto, vanhenemiskäytännöt ja estä tunnusten toistohyökkäykset  

**Tunnusten suojattu säilytys:**
   - Käytä Azure Key Vaultia tai vastaavia turvallisia salasanavarastoja kaikille salaisuuksille  
   - Toteuta salaus tunnuksille sekä levossa että siirron aikana  
   - Säännöllinen salasanan kierto ja luvattoman käytön valvonta  

## 2. **Istunnon hallinta ja siirtoturvallisuus**

**Turvalliset istuntokäytännöt:**
   - **Kryptografisesti turvalliset istuntotunnukset**: Käytä turvallisia, ei-deterministisiä istuntotunnuksia, jotka on luotu turvallisilla satunnaislukugeneraattoreilla  
   - **Käyttäjäkohtainen sitominen**: Sido istuntotunnukset käyttäjätunnuksiin käyttämällä muotoja, kuten `<user_id>:<session_id>`, estääksesi istuntojen väärinkäytön käyttäjien välillä  
   - **Istunnon elinkaaren hallinta**: Toteuta asianmukainen vanheneminen, kierto ja mitätöinti haavoittuvuusikkunoiden rajoittamiseksi  
   - **HTTPS/TLS:n pakottaminen**: HTTPS on pakollinen kaikessa viestinnässä istuntotunnusten sieppaamisen estämiseksi  

**Siirtokerroksen turvallisuus:**
   - Konfiguroi TLS 1.3 aina kun mahdollista ja varmista asianmukainen sertifikaattien hallinta  
   - Toteuta sertifikaattien kiinnitys kriittisille yhteyksille  
   - Säännöllinen sertifikaattien kierto ja voimassaolon tarkistus  

## 3. **AI-spesifisten uhkien torjunta** 🤖

**Kehotteen injektion puolustus:**
   - **Microsoft Prompt Shields**: Käytä AI Prompt Shield -ratkaisuja haitallisten ohjeiden havaitsemiseen ja suodattamiseen  
   - **Syötteiden validointi**: Varmista ja puhdista kaikki syötteet injektiohyökkäysten ja "hämmentynyt apulainen" -ongelmien estämiseksi  
   - **Sisältörajoitukset**: Käytä erottimia ja datamerkintäjärjestelmiä luotettujen ohjeiden ja ulkoisen sisällön erottamiseen  

**Työkalujen manipuloinnin estäminen:**
   - **Työkalujen metadatan validointi**: Toteuta eheystarkistukset työkalumäärittelyille ja valvo odottamattomia muutoksia  
   - **Dynaaminen työkalujen valvonta**: Valvo ajonaikaista käyttäytymistä ja aseta hälytyksiä odottamattomille suorituskuvioille  
   - **Hyväksyntäprosessit**: Edellytä käyttäjän nimenomaista hyväksyntää työkalumuutoksille ja ominaisuuksien päivityksille  

## 4. **Pääsynhallinta ja käyttöoikeudet**

**Vähimmän oikeuden periaate:**
   - Myönnä MCP-palvelimille vain vähimmäisoikeudet, jotka ovat tarpeen aiottua toimintaa varten  
   - Toteuta roolipohjainen pääsynhallinta (RBAC) hienojakoisilla käyttöoikeuksilla  
   - Säännölliset käyttöoikeuksien tarkistukset ja jatkuva valvonta oikeuksien laajentumisen varalta  

**Ajonaikaiset käyttöoikeuskontrollit:**
   - Aseta resurssirajoituksia resurssien ehtymishyökkäysten estämiseksi  
   - Käytä konttien eristämistä työkalujen suoritusympäristöissä  
   - Toteuta juuri ajoissa -pääsy hallinnollisiin toimintoihin  

## 5. **Sisällön turvallisuus ja valvonta**

**Sisällön turvallisuuden toteutus:**
   - **Azure Content Safety -integraatio**: Käytä Azure Content Safety -ratkaisuja haitallisen sisällön, jailbreak-yritysten ja käytäntörikkomusten havaitsemiseen  
   - **Käyttäytymisanalyysi**: Toteuta ajonaikainen käyttäytymisen valvonta MCP-palvelimen ja työkalujen suorituspoikkeamien havaitsemiseksi  
   - **Kattava lokitus**: Kirjaa kaikki todennusyritykset, työkalujen kutsut ja turvallisuustapahtumat turvalliseen, peukaloinnin kestävään tallennustilaan  

**Jatkuva valvonta:**
   - Reaaliaikaiset hälytykset epäilyttävistä kuvioista ja luvattomista käyttöyrityksistä  
   - Integraatio SIEM-järjestelmiin keskitettyä turvallisuustapahtumien hallintaa varten  
   - Säännölliset turvallisuusauditoinnit ja MCP-toteutusten tunkeutumistestaukset  

## 6. **Toimitusketjun turvallisuus**

**Komponenttien tarkistus:**
   - **Riippuvuuksien skannaus**: Käytä automatisoituja haavoittuvuusskannauksia kaikille ohjelmistoriippuvuuksille ja AI-komponenteille  
   - **Alkuperän validointi**: Varmista mallien, tietolähteiden ja ulkoisten palveluiden alkuperä, lisensointi ja eheys  
   - **Allekirjoitetut paketit**: Käytä kryptografisesti allekirjoitettuja paketteja ja tarkista allekirjoitukset ennen käyttöönottoa  

**Turvallinen kehitysputki:**
   - **GitHub Advanced Security**: Toteuta salaisuuksien skannaus, riippuvuusanalyysi ja CodeQL-staattinen analyysi  
   - **CI/CD-turvallisuus**: Integroi turvallisuuden validointi automatisoituihin käyttöönottoihin  
   - **Artefaktien eheys**: Toteuta kryptografinen validointi käyttöönotettaville artefakteille ja konfiguraatioille  

## 7. **OAuth-turvallisuus ja "hämmentynyt apulainen" -ongelman ehkäisy**

**OAuth 2.1 -toteutus:**
   - **PKCE-toteutus**: Käytä Proof Key for Code Exchange (PKCE) -menetelmää kaikissa valtuutuspyynnöissä  
   - **Nimenomainen suostumus**: Hanki käyttäjän suostumus jokaiselle dynaamisesti rekisteröidylle asiakkaalle "hämmentynyt apulainen" -hyökkäysten estämiseksi  
   - **Uudelleenohjaus-URI:n validointi**: Toteuta tiukka uudelleenohjaus-URI:iden ja asiakastunnisteiden validointi  

**Välityspalvelimen turvallisuus:**
   - Estä valtuutuksen ohittaminen staattisten asiakastunnisteiden hyväksikäytön kautta  
   - Toteuta asianmukaiset suostumusprosessit kolmansien osapuolten API-käyttöön  
   - Valvo valtuutuskoodien varkauksia ja luvattomia API-käyttöjä  

## 8. **Tapahtumien hallinta ja palautuminen**

**Nopeat reagointikyvyt:**
   - **Automatisoitu reagointi**: Toteuta automatisoituja järjestelmiä salaisuuksien kiertoon ja uhkien rajoittamiseen  
   - **Palautusmenettelyt**: Kyky nopeasti palauttaa tunnetusti toimiviin konfiguraatioihin ja komponentteihin  
   - **Oikeuslääketieteelliset kyvyt**: Yksityiskohtaiset auditointijäljet ja lokit tapahtumien tutkimista varten  

**Viestintä ja koordinointi:**
   - Selkeät eskalointimenettelyt turvallisuustapahtumille  
   - Integraatio organisaation tapahtumien hallintatiimien kanssa  
   - Säännölliset turvallisuustapahtumien simulaatiot ja harjoitukset  

## 9. **Säädösten noudattaminen ja hallinto**

**Sääntelyvaatimusten noudattaminen:**
   - Varmista, että MCP-toteutukset täyttävät toimialakohtaiset vaatimukset (GDPR, HIPAA, SOC 2)  
   - Toteuta tietojen luokittelu- ja yksityisyydensuojakontrollit AI-tietojen käsittelyyn  
   - Pidä kattava dokumentaatio vaatimustenmukaisuuden auditointeja varten  

**Muutosten hallinta:**
   - Viralliset turvallisuusarviointiprosessit kaikille MCP-järjestelmän muutoksille  
   - Versiohallinta ja hyväksyntäprosessit konfiguraatiomuutoksille  
   - Säännölliset vaatimustenmukaisuuden arvioinnit ja aukkoanalyysit  

## 10. **Edistyneet turvallisuuskontrollit**

**Zero Trust -arkkitehtuuri:**
   - **Älä koskaan luota, varmista aina**: Käyttäjien, laitteiden ja yhteyksien jatkuva varmistaminen  
   - **Mikrosegmentointi**: Hienojakoiset verkkokontrollit, jotka eristävät yksittäiset MCP-komponentit  
   - **Ehdollinen pääsy**: Riskipohjaiset pääsynhallinnat, jotka mukautuvat nykyiseen kontekstiin ja käyttäytymiseen  

**Ajonaikainen sovellussuojaus:**
   - **Ajonaikainen sovelluksen itsepuolustus (RASP)**: Käytä RASP-tekniikoita reaaliaikaiseen uhkien havaitsemiseen  
   - **Sovelluksen suorituskyvyn valvonta**: Valvo suorituskyvyn poikkeamia, jotka voivat viitata hyökkäyksiin  
   - **Dynaamiset turvallisuuskäytännöt**: Toteuta turvallisuuskäytännöt, jotka mukautuvat nykyiseen uhkakuvaan  

## 11. **Microsoftin turvallisuusekosysteemin integrointi**

**Kattava Microsoft-turvallisuus:**
   - **Microsoft Defender for Cloud**: Pilviturvallisuuden hallinta MCP-työkuormille  
   - **Azure Sentinel**: Pilvinatiivi SIEM- ja SOAR-ominaisuudet edistyneeseen uhkien havaitsemiseen  
   - **Microsoft Purview**: Tietojen hallinta ja vaatimustenmukaisuus AI-työnkuluille ja tietolähteille  

**Identiteetin ja pääsyn hallinta:**
   - **Microsoft Entra ID**: Yrityksen identiteetinhallinta ehdollisilla pääsynhallintakäytännöillä  
   - **Privileged Identity Management (PIM)**: Juuri ajoissa -pääsy ja hyväksyntäprosessit hallinnollisille toiminnoille  
   - **Identiteettisuojaus**: Riskipohjainen ehdollinen pääsy ja automatisoitu uhkien torjunta  

## 12. **Jatkuva turvallisuuden kehittäminen**

**Ajantasaisena pysyminen:**
   - **Määritysten seuranta**: MCP-määritysten päivitysten ja turvallisuusohjeiden säännöllinen tarkistus  
   - **Uhkatiedustelu**: AI-spesifisten uhkatietojen ja kompromissien indikaattorien integrointi  
   - **Turvallisuusyhteisön osallistuminen**: Aktiivinen osallistuminen MCP-turvallisuusyhteisöön ja haavoittuvuuksien ilmoitusohjelmiin  

**Mukautuva turvallisuus:**
   - **Koneoppimisen turvallisuus**: Käytä koneoppimiseen perustuvaa poikkeamien havaitsemista uusien hyökkäysmallien tunnistamiseen  
   - **Ennakoiva turvallisuusanalytiikka**: Toteuta ennakoivia malleja uhkien tunnistamiseen etukäteen  
   - **Turvallisuusautomaatio**: Automatisoidut turvallisuuskäytäntöjen päivitykset uhkatiedustelun ja määritysmuutosten perusteella  

---

## **Keskeiset turvallisuusresurssit**

### **Virallinen MCP-dokumentaatio**
- [MCP-määritys (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP:n turvallisuuskäytännöt](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP:n valtuutusmääritys](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoftin turvallisuusratkaisut**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID -turvallisuus](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Turvallisuusstandardit**
- [OAuth 2.0 -turvallisuuskäytännöt (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 suurille kielimalleille](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Toteutusoppaat**
- [Azure API Management MCP -todennusportti](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID MCP-palvelimien kanssa](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Turvallisuusilmoitus**: MCP:n turvallisuuskäytännöt kehittyvät nopeasti. Varmista aina nykyisen [MCP-määrityksen](https://spec.modelcontextprotocol.io/) ja [virallisen turvallisuusdokumentaation](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) mukaisuus ennen toteutusta.

**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, huomioithan, että automaattiset käännökset voivat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäisellä kielellä tulisi pitää ensisijaisena lähteenä. Kriittisen tiedon osalta suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa väärinkäsityksistä tai virhetulkinnoista, jotka johtuvat tämän käännöksen käytöstä.