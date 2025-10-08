<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T16:10:45+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "fi"
}
-->
# MCP:n turvallisuuden parhaat käytännöt 2025

Tämä kattava opas esittelee olennaiset turvallisuuden parhaat käytännöt Model Context Protocol (MCP) -järjestelmien toteuttamiseen perustuen uusimpaan **MCP Specification 2025-06-18** -määrittelyyn ja nykyisiin alan standardeihin. Käytännöt käsittelevät sekä perinteisiä turvallisuushuolia että MCP-toteutuksille ainutlaatuisia tekoälyyn liittyviä uhkia.

## Keskeiset turvallisuusvaatimukset

### Pakolliset turvallisuuskontrollit (MUST-vaatimukset)

1. **Tokenien validointi**: MCP-palvelimet **EIVÄT SAA** hyväksyä tokeneita, joita ei ole nimenomaisesti luotu kyseiselle MCP-palvelimelle.
2. **Valtuutuksen tarkistaminen**: MCP-palvelimien, jotka toteuttavat valtuutuksen, **TÄYTYY** tarkistaa KAIKKI saapuvat pyynnöt, eikä niiden **TULE** käyttää istuntoja autentikointiin.  
3. **Käyttäjän suostumus**: MCP-välityspalvelimien, jotka käyttävät staattisia asiakastunnuksia, **TÄYTYY** hankkia käyttäjän nimenomainen suostumus jokaiselle dynaamisesti rekisteröidylle asiakkaalle.
4. **Turvalliset istuntotunnukset**: MCP-palvelimien **TÄYTYY** käyttää kryptografisesti turvallisia, ei-deterministisiä istuntotunnuksia, jotka on luotu turvallisilla satunnaislukugeneraattoreilla.

## Ydinturvallisuuskäytännöt

### 1. Syötteiden validointi ja puhdistus
- **Kattava syötteiden validointi**: Validoi ja puhdista kaikki syötteet injektiohyökkäysten, "confused deputy" -ongelmien ja kehotepohjaisten injektioiden estämiseksi.
- **Parametrien skeeman valvonta**: Toteuta tiukka JSON-skeeman validointi kaikille työkalujen parametreille ja API-syötteille.
- **Sisällön suodatus**: Käytä Microsoft Prompt Shields -ratkaisua ja Azure Content Safety -palvelua haitallisen sisällön suodattamiseen kehotteista ja vastauksista.
- **Tulosteiden puhdistus**: Validoi ja puhdista kaikki mallin tuottamat tulosteet ennen niiden esittämistä käyttäjille tai jatkokäsittelyyn.

### 2. Autentikoinnin ja valtuutuksen huippuosaaminen  
- **Ulkoiset identiteettipalvelut**: Delegoi autentikointi vakiintuneille identiteettipalveluille (Microsoft Entra ID, OAuth 2.1 -palveluntarjoajat) sen sijaan, että toteuttaisit oman autentikoinnin.
- **Hienojakoiset käyttöoikeudet**: Toteuta työkalukohtaiset käyttöoikeudet vähimmän oikeuden periaatteen mukaisesti.
- **Tokenien elinkaaren hallinta**: Käytä lyhytikäisiä käyttöoikeustokeneita, joissa on turvallinen kierto ja asianmukainen kohdevalidointi.
- **Monivaiheinen tunnistautuminen**: Edellytä MFA:ta kaikessa hallinnollisessa käytössä ja arkaluontoisissa toiminnoissa.

### 3. Turvalliset viestintäprotokollat
- **Kuljetuskerroksen turvallisuus**: Käytä HTTPS/TLS 1.3 -protokollaa kaikessa MCP-viestinnässä ja varmista sertifikaattien oikeellisuus.
- **Päästä päähän -salaus**: Toteuta lisäsalauskerroksia erittäin arkaluontoisille tiedoille siirron ja säilytyksen aikana.
- **Sertifikaattien hallinta**: Ylläpidä sertifikaattien elinkaaren hallintaa automatisoiduilla uusintaprosesseilla.
- **Protokollaversion valvonta**: Käytä nykyistä MCP-protokollaversiota (2025-06-18) ja varmista oikea version neuvottelu.

### 4. Kehittynyt kuormanhallinta ja resurssien suojaus
- **Monitasoinen kuormanhallinta**: Toteuta kuormanhallinta käyttäjä-, istunto-, työkalu- ja resurssitasoilla väärinkäytön estämiseksi.
- **Mukautuva kuormanhallinta**: Käytä koneoppimiseen perustuvaa kuormanhallintaa, joka mukautuu käyttökuvioihin ja uhkaindikaattoreihin.
- **Resurssikiintiöiden hallinta**: Aseta sopivat rajat laskentateholle, muistin käytölle ja suoritusaikaan.
- **DDoS-suojaus**: Ota käyttöön kattavat DDoS-suojaus- ja liikenteen analysointijärjestelmät.

### 5. Kattava lokitus ja valvonta
- **Rakenteellinen auditointilokitus**: Toteuta yksityiskohtaiset, haettavat lokit kaikille MCP-toiminnoille, työkalujen suorituksille ja turvallisuustapahtumille.
- **Reaaliaikainen turvallisuusvalvonta**: Käytä SIEM-järjestelmiä, joissa on tekoälypohjainen poikkeamien havaitseminen MCP-työkuormille.
- **Tietosuojayhteensopiva lokitus**: Kirjaa turvallisuustapahtumat noudattaen tietosuojavaatimuksia ja -säädöksiä.
- **Tapahtumavasteen integrointi**: Liitä lokitusjärjestelmät automatisoituihin tapahtumavasteen työnkulkuihin.

### 6. Parannetut turvalliset tallennuskäytännöt
- **Laitteistopohjaiset turvallisuusmoduulit**: Käytä HSM-pohjaista avainten tallennusta (Azure Key Vault, AWS CloudHSM) kriittisiin kryptografisiin toimintoihin.
- **Salausavainten hallinta**: Toteuta asianmukainen avainten kierto, erottelu ja käyttöoikeuksien hallinta.
- **Salaisuuksien hallinta**: Säilytä kaikki API-avaimet, tokenit ja tunnistetiedot omistetuissa salaisuuksien hallintajärjestelmissä.
- **Tietojen luokittelu**: Luokittele tiedot herkkyystason mukaan ja sovella asianmukaisia suojaustoimenpiteitä.

### 7. Kehittynyt tokenien hallinta
- **Tokenien läpiviennin estäminen**: Kiellä nimenomaisesti tokenien läpivientimallit, jotka ohittavat turvallisuuskontrollit.
- **Kohdevalidointi**: Varmista aina, että tokenin kohdeväitteet vastaavat MCP-palvelimen identiteettiä.
- **Väitteisiin perustuva valtuutus**: Toteuta hienojakoinen valtuutus tokenin väitteiden ja käyttäjäominaisuuksien perusteella.
- **Tokenien sitominen**: Sido tokenit tiettyihin istuntoihin, käyttäjiin tai laitteisiin tarpeen mukaan.

### 8. Turvallinen istuntohallinta
- **Kryptografiset istuntotunnukset**: Luo istuntotunnukset kryptografisesti turvallisilla satunnaislukugeneraattoreilla (ei ennustettavia sekvenssejä).
- **Käyttäjäkohtainen sitominen**: Sido istuntotunnukset käyttäjäkohtaisiin tietoihin turvallisilla formaateilla, kuten `<user_id>:<session_id>`.
- **Istuntojen elinkaaren hallinta**: Toteuta asianmukainen istuntojen vanhentuminen, kierto ja mitätöinti.
- **Istuntojen turvallisuusotsikot**: Käytä sopivia HTTP-turvallisuusotsikoita istuntojen suojaamiseen.

### 9. Tekoälyyn liittyvät turvallisuuskontrollit
- **Kehotepohjaisten injektioiden torjunta**: Käytä Microsoft Prompt Shields -ratkaisua, jossa on korostus-, rajaus- ja datamerkintätekniikoita.
- **Työkalujen myrkyttämisen estäminen**: Validoi työkalujen metatiedot, seuraa dynaamisia muutoksia ja varmista työkalujen eheys.
- **Mallin tulosteiden validointi**: Tarkista mallin tulosteet mahdollisen tietovuodon, haitallisen sisällön tai turvallisuuspolitiikan rikkomusten varalta.
- **Kontekstin suojaus**: Toteuta kontrollit, jotka estävät kontekstin manipuloinnin ja myrkyttämisen.

### 10. Työkalujen suorittamisen turvallisuus
- **Suoritusympäristön eristäminen**: Suorita työkalut kontitetuissa, eristetyissä ympäristöissä, joissa on resurssirajoitukset.
- **Oikeuksien erottelu**: Suorita työkalut vähimmäisoikeuksilla ja erillisillä palvelutileillä.
- **Verkkoeristys**: Toteuta verkon segmentointi työkalujen suoritusympäristöille.
- **Suorituksen valvonta**: Valvo työkalujen suorittamista poikkeavan käyttäytymisen, resurssien käytön ja turvallisuusrikkomusten varalta.

### 11. Jatkuva turvallisuuden validointi
- **Automaattinen turvallisuustestaus**: Integroi turvallisuustestaus CI/CD-putkiin työkaluilla, kuten GitHub Advanced Security.
- **Haavoittuvuuksien hallinta**: Skannaa säännöllisesti kaikki riippuvuudet, mukaan lukien tekoälymallit ja ulkoiset palvelut.
- **Tunkeutumistestaus**: Suorita säännöllisiä turvallisuusarviointeja, jotka kohdistuvat erityisesti MCP-toteutuksiin.
- **Turvallisuuskoodin tarkistukset**: Toteuta pakolliset turvallisuustarkistukset kaikille MCP:hen liittyville koodimuutoksille.

### 12. Tekoälyn toimitusketjun turvallisuus
- **Komponenttien tarkistus**: Varmista kaikkien tekoälykomponenttien (mallit, upotukset, API:t) alkuperä, eheys ja turvallisuus.
- **Riippuvuuksien hallinta**: Pidä ajan tasalla olevat inventaariot kaikista ohjelmisto- ja tekoälyriippuvuuksista haavoittuvuuksien seurannalla.
- **Luotetut arkistot**: Käytä varmennettuja, luotettuja lähteitä kaikille tekoälymalleille, kirjastoille ja työkaluille.
- **Toimitusketjun valvonta**: Seuraa jatkuvasti tekoälypalveluntarjoajien ja mallivarastojen kompromisseja.

## Kehittyneet turvallisuusmallit

### Zero Trust -arkkitehtuuri MCP:lle
- **Älä koskaan luota, varmista aina**: Toteuta jatkuva validointi kaikille MCP-osapuolille.
- **Mikrosegmentointi**: Eristä MCP-komponentit hienojakoisilla verkko- ja identiteettikontrolleilla.
- **Ehdollinen pääsy**: Toteuta riskiperusteiset pääsynvalvontakontrollit, jotka mukautuvat kontekstiin ja käyttäytymiseen.
- **Jatkuva riskinarviointi**: Arvioi turvallisuusasemaa dynaamisesti nykyisten uhkaindikaattorien perusteella.

### Tietosuojaa säilyttävä tekoälyn toteutus
- **Tietojen minimointi**: Paljasta vain vähimmäismäärä tietoja jokaisessa MCP-toiminnossa.
- **Differentiaalinen tietosuoja**: Käytä tietosuojaa säilyttäviä tekniikoita arkaluontoisten tietojen käsittelyssä.
- **Homomorfinen salaus**: Käytä kehittyneitä salausmenetelmiä turvalliseen laskentaan salatuilla tiedoilla.
- **Hajautettu oppiminen**: Toteuta hajautettuja oppimismenetelmiä, jotka säilyttävät tietojen paikallisuuden ja yksityisyyden.

### Tekoälyjärjestelmien tapahtumavaste
- **Tekoälyyn liittyvät tapahtumamenettelyt**: Kehitä tapahtumavasteen menettelytapoja, jotka on räätälöity tekoälyyn ja MCP:hen liittyviin uhkiin.
- **Automaattinen vaste**: Toteuta automaattinen eristäminen ja korjaus yleisille tekoälyyn liittyville turvallisuustapahtumille.  
- **Oikeuslääketieteelliset valmiudet**: Ylläpidä valmiutta tekoälyjärjestelmien kompromissien ja tietomurtojen tutkintaan.
- **Palautusmenettelyt**: Määritä menettelyt tekoälymallien myrkyttämisestä, kehotepohjaisista injektiohyökkäyksistä ja palvelukompromisseista toipumiseen.

## Toteutusresurssit ja standardit

### Virallinen MCP-dokumentaatio
- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Nykyinen MCP-protokollan määrittely
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Virallinen turvallisuusohjeistus
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Autentikointi- ja valtuutusmallit
- [MCP Transport Security](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Kuljetuskerroksen turvallisuusvaatimukset

### Microsoftin turvallisuusratkaisut
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Kehotepohjaisten injektioiden kehittynyt torjunta
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Kattava tekoälyn sisällön suodatus
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Yritysten identiteetin ja pääsyn hallinta
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Turvallinen salaisuuksien ja tunnistetietojen hallinta
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Toimitusketjun ja koodin turvallisuusskannaus

### Turvallisuusstandardit ja -kehykset
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Nykyiset OAuth-turvallisuusohjeet
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Verkkosovellusten turvallisuusriskit
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Tekoälyyn liittyvät turvallisuusriskit
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Kattava tekoälyn riskienhallinta
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Tietoturvan hallintajärjestelmät

### Toteutusoppaat ja -ohjeet
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Yritysten autentikointimallit
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Identiteettipalvelun integrointi
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Tokenien hallinnan parhaat käytännöt
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Kehittyneet salausmallit

### Kehittyneet turvallisuusresurssit
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Turvallisen kehityksen käytännöt
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - Tekoälyyn liittyvä turvallisuustestaus
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Tekoälyn uhkamallinnusmenetelmä
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Tietosuojaa säilyttävät tekoälytekniikat

### Sääntely ja hallinnointi
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Tietosuojayhteensopivuus tekoälyjärjestelmissä
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Vastuullisen tekoälyn toteutus
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Turvallisuuskontrollit tekoälypalveluntarjoajille
-
- **Työkalujen kehittäminen**: Kehitä ja jaa turvallisuustyökaluja ja -kirjastoja MCP-ekosysteemiä varten

---

*Tämä asiakirja heijastaa MCP:n turvallisuuden parhaita käytäntöjä 18. elokuuta 2025 tilanteen mukaan, perustuen MCP-määritykseen 2025-06-18. Turvallisuuskäytäntöjä tulisi tarkistaa ja päivittää säännöllisesti protokollan ja uhkakentän kehittyessä.*

**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, huomioithan, että automaattiset käännökset voivat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäisellä kielellä tulisi pitää ensisijaisena lähteenä. Kriittisen tiedon osalta suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa väärinkäsityksistä tai virhetulkinnoista, jotka johtuvat tämän käännöksen käytöstä.