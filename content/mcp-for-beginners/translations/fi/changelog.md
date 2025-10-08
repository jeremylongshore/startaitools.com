<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:23:26+00:00",
  "source_file": "changelog.md",
  "language_code": "fi"
}
-->
# Muutosloki: MCP for Beginners -opetussuunnitelma

Tämä dokumentti toimii merkittävien muutosten kirjana Model Context Protocol (MCP) for Beginners -opetussuunnitelmassa. Muutokset on dokumentoitu käänteisessä aikajärjestyksessä (uusimmat muutokset ensin).

## 6. lokakuuta 2025

### Getting Started -osion laajennus – Edistynyt palvelimen käyttö & Yksinkertainen autentikointi

#### Edistynyt palvelimen käyttö (03-GettingStarted/10-advanced)
- **Uusi luku lisätty**: Kattava opas MCP-palvelimen edistyneeseen käyttöön, sisältäen sekä tavalliset että matalan tason palvelinarkkitehtuurit.
  - **Tavallinen vs. matalan tason palvelin**: Yksityiskohtainen vertailu ja Python- sekä TypeScript-koodiesimerkit molemmista lähestymistavoista.
  - **Handler-pohjainen suunnittelu**: Selitys handler-pohjaisesta työkalujen/resurssien/promptien hallinnasta skaalautuvien ja joustavien palvelinratkaisujen toteuttamiseksi.
  - **Käytännön mallit**: Todellisia esimerkkejä tilanteista, joissa matalan tason palvelinmallit ovat hyödyllisiä edistyneissä ominaisuuksissa ja arkkitehtuurissa.

#### Yksinkertainen autentikointi (03-GettingStarted/11-simple-auth)
- **Uusi luku lisätty**: Vaiheittainen opas yksinkertaisen autentikoinnin toteuttamiseen MCP-palvelimissa.
  - **Autentikoinnin käsitteet**: Selkeä selitys autentikoinnin ja autorisoinnin eroista sekä tunnistetietojen käsittelystä.
  - **Perusautentikoinnin toteutus**: Middleware-pohjaiset autentikointimallit Pythonilla (Starlette) ja TypeScriptillä (Express), sisältäen koodiesimerkit.
  - **Edistyneeseen turvallisuuteen siirtyminen**: Ohjeet yksinkertaisesta autentikoinnista siirtymiseen OAuth 2.1:een ja RBAC:iin, sisältäen viittaukset edistyneisiin turvallisuusmoduuleihin.

Nämä lisäykset tarjoavat käytännönläheistä opastusta vahvempien, turvallisempien ja joustavampien MCP-palvelinratkaisujen rakentamiseen, yhdistäen perustavanlaatuiset käsitteet edistyneisiin tuotantomalleihin.

## 29. syyskuuta 2025

### MCP-palvelimen tietokantaintegraatiolaboratoriot – Kattava käytännön oppimispolku

#### 11-MCPServerHandsOnLabs - Uusi täydellinen tietokantaintegraatio-opetussuunnitelma
- **Täydellinen 13-laboratorion oppimispolku**: Lisätty kattava käytännön opetussuunnitelma tuotantovalmiiden MCP-palvelimien rakentamiseen PostgreSQL-tietokantaintegraatiolla.
  - **Todellinen toteutus**: Zava Retail -analytiikkatapaus, joka esittelee yritystason malleja.
  - **Rakenteellinen oppimispolku**:
    - **Laboratoriot 00-03: Perusteet** - Johdanto, ydinarkkitehtuuri, turvallisuus ja monikäyttäjyys, ympäristön asennus.
    - **Laboratoriot 04-06: MCP-palvelimen rakentaminen** - Tietokannan suunnittelu ja skeema, MCP-palvelimen toteutus, työkalujen kehitys.
    - **Laboratoriot 07-09: Edistyneet ominaisuudet** - Semanttinen hakuintegraatio, testaus ja virheenkorjaus, VS Code -integraatio.
    - **Laboratoriot 10-12: Tuotanto ja parhaat käytännöt** - Julkaisustrategiat, valvonta ja havainnointi, parhaat käytännöt ja optimointi.
  - **Yritysteknologiat**: FastMCP-kehys, PostgreSQL pgvectorilla, Azure OpenAI -upotukset, Azure Container Apps, Application Insights.
  - **Edistyneet ominaisuudet**: Rivitasoinen turvallisuus (RLS), semanttinen haku, monikäyttäjäinen datan käyttö, vektoriupotukset, reaaliaikainen valvonta.

#### Terminologian standardointi - Moduulista laboratorioon
- **Kattava dokumentaatiopäivitys**: Päivitetty systemaattisesti kaikki README-tiedostot 11-MCPServerHandsOnLabs-osiossa käyttämään "Laboratorio"-terminologiaa "Moduuli"-termin sijaan.
  - **Otsikot**: Päivitetty "Mitä tämä moduuli kattaa" muotoon "Mitä tämä laboratorio kattaa" kaikissa 13 laboratoriossa.
  - **Sisällön kuvaus**: Muutettu "Tämä moduuli tarjoaa..." muotoon "Tämä laboratorio tarjoaa..." dokumentaation läpi.
  - **Oppimistavoitteet**: Päivitetty "Tämän moduulin lopussa..." muotoon "Tämän laboratorion lopussa..."
  - **Navigointilinkit**: Muutettu kaikki "Moduuli XX:" viittaukset muotoon "Laboratorio XX:" ristiinviittauksissa ja navigoinnissa.
  - **Suorituksen seuranta**: Päivitetty "Kun olet suorittanut tämän moduulin..." muotoon "Kun olet suorittanut tämän laboratorion..."
  - **Teknisten viittausten säilyttäminen**: Säilytetty Python-moduuliviittaukset konfiguraatiotiedostoissa (esim. `"module": "mcp_server.main"`).

#### Opintosuunnitelman parannus (study_guide.md)
- **Visuaalinen opetussuunnitelmakartta**: Lisätty uusi "11. Tietokantaintegraatiolaboratoriot" -osio kattavalla laboratoriostruktuurin visualisoinnilla.
- **Repositorion rakenne**: Päivitetty kymmenestä yhdentoista pääosioon, sisältäen yksityiskohtaisen 11-MCPServerHandsOnLabs-kuvauksen.
- **Oppimispolun ohjeistus**: Parannettu navigointiohjeita kattamaan osiot 00-11.
- **Teknologian kattavuus**: Lisätty FastMCP-, PostgreSQL- ja Azure-palveluiden integraatiotiedot.
- **Oppimistulokset**: Korostettu tuotantovalmiiden palvelimien kehittämistä, tietokantaintegraatiomalleja ja yritystason turvallisuutta.

#### Pää-README-rakenteen parannus
- **Laboratoriopohjainen terminologia**: Päivitetty pää-README.md tiedostossa 11-MCPServerHandsOnLabs käyttämään johdonmukaisesti "Laboratorio"-rakennetta.
- **Oppimispolun organisointi**: Selkeä eteneminen perustavanlaatuisista käsitteistä edistyneeseen toteutukseen ja tuotantoon.
- **Todellinen fokus**: Painotus käytännönläheiseen oppimiseen yritystason malleilla ja teknologioilla.

### Dokumentaation laatu- ja johdonmukaisuusparannukset
- **Käytännön oppimisen korostus**: Vahvistettu käytännönläheistä, laboratoriopohjaista lähestymistapaa dokumentaation läpi.
- **Yritysmallien fokus**: Korostettu tuotantovalmiita toteutuksia ja yritystason turvallisuuskysymyksiä.
- **Teknologian integraatio**: Kattava modernien Azure-palveluiden ja AI-integraatiomallien kattavuus.
- **Oppimisen eteneminen**: Selkeä, rakenteellinen polku peruskäsitteistä tuotantoon.
#### Edistyneet aiheet: Tietoturva (05-AdvancedTopics/mcp-security/) - Valmis tuotantototeutus
- **README.md**: Täydellinen uudistus yritystason tietoturvan toteutusta varten
  - **Nykyinen spesifikaatioiden mukaisuus**: Päivitetty MCP Spesifikaatioon 2025-06-18, sisältäen pakolliset tietoturvavaatimukset
  - **Parannettu tunnistautuminen**: Microsoft Entra ID -integraatio kattavilla .NET- ja Java Spring Security -esimerkeillä
  - **AI-tietoturvaintegraatio**: Microsoft Prompt Shields ja Azure Content Safety -toteutus yksityiskohtaisilla Python-esimerkeillä
  - **Edistynyt uhkien torjunta**: Kattavat toteutusesimerkit
    - Confused Deputy -hyökkäysten estäminen PKCE:llä ja käyttäjän suostumuksen validoinnilla
    - Token Passthrough -hyökkäysten estäminen yleisön validoinnilla ja turvallisella token-hallinnalla
    - Istunnon kaappauksen estäminen kryptografisella sidonnalla ja käyttäytymisanalyysillä
  - **Yritystason tietoturvaintegraatio**: Azure Application Insights -seuranta, uhkien tunnistusputket ja toimitusketjun tietoturva
  - **Toteutuksen tarkistuslista**: Selkeä erottelu pakollisten ja suositeltujen tietoturvakontrollien välillä, hyödyntäen Microsoftin tietoturvaekosysteemin etuja

### Dokumentaation laatu ja standardien mukaisuus
- **Spesifikaatioviittaukset**: Päivitetty kaikki viittaukset nykyiseen MCP Spesifikaatioon 2025-06-18
- **Microsoftin tietoturvaekosysteemi**: Parannettu integraatio-ohjeistus kaikessa tietoturvadokumentaatiossa
- **Käytännön toteutus**: Lisätty yksityiskohtaisia koodiesimerkkejä .NET-, Java- ja Python-kielillä yrityskäytännöillä
- **Resurssien organisointi**: Kattava virallisten dokumenttien, tietoturvastandardien ja toteutusoppaiden kategorisointi
- **Visuaaliset indikaattorit**: Selkeä merkintä pakollisten vaatimusten ja suositeltujen käytäntöjen välillä

#### Peruskäsitteet (01-CoreConcepts/) - Täydellinen modernisointi
- **Protokollaversion päivitys**: Päivitetty viittaamaan nykyiseen MCP Spesifikaatioon 2025-06-18, käyttäen päivämääräpohjaista versionumerointia (YYYY-MM-DD-muoto)
- **Arkkitehtuurin tarkennus**: Parannettu isäntien, asiakkaiden ja palvelimien kuvauksia nykyisten MCP-arkkitehtuurimallien mukaisesti
  - Isännät määritelty selkeästi AI-sovelluksiksi, jotka koordinoivat useita MCP-asiakasliitäntöjä
  - Asiakkaat kuvattu protokollaliitäntöinä, jotka ylläpitävät yksi-yhteen-suhdetta palvelimiin
  - Palvelimet parannettu paikallisten ja etäkäyttöön tarkoitettujen käyttöönottojen skenaarioilla
- **Primitivien uudelleenjärjestely**: Täydellinen palvelin- ja asiakasprimitivien uudistus
  - Palvelinprimitivit: Resurssit (datapisteet), Kehotteet (mallit), Työkalut (suoritettavat funktiot) yksityiskohtaisilla selityksillä ja esimerkeillä
  - Asiakasprimitivit: Näytteenotto (LLM-täydennykset), Tiedustelu (käyttäjän syöte), Lokitus (virheenkorjaus/seuranta)
  - Päivitetty nykyisiin löytämisen (`*/list`), hakemisen (`*/get`) ja suorittamisen (`*/call`) menetelmäkuvioihin
- **Protokolla-arkkitehtuuri**: Esitelty kaksikerroksinen arkkitehtuurimalli
  - Datalayer: JSON-RPC 2.0 -pohja elinkaaren hallinnalla ja primitiiveillä
  - Kuljetuskerros: STDIO (paikallinen) ja Streamable HTTP SSE:llä (etäkäyttö)
- **Tietoturvakehys**: Kattavat tietoturvaperiaatteet, mukaan lukien käyttäjän suostumus, tietosuojan suojaus, työkalujen turvallinen suoritus ja kuljetuskerroksen tietoturva
- **Viestintäkuviot**: Päivitetty protokollaviestit näyttämään alustuksen, löytämisen, suorittamisen ja ilmoitusvirrat
- **Koodiesimerkit**: Uudistettu monikieliset esimerkit (.NET, Java, Python, JavaScript) nykyisten MCP SDK -mallien mukaisiksi

#### Tietoturva (02-Security/) - Kattava tietoturvan uudistus  
- **Standardien mukaisuus**: Täysi yhdenmukaisuus MCP Spesifikaation 2025-06-18 tietoturvavaatimusten kanssa
- **Tunnistautumisen kehitys**: Dokumentoitu siirtyminen mukautetuista OAuth-palvelimista ulkoisten identiteettipalveluntarjoajien delegointiin (Microsoft Entra ID)
- **AI-spesifinen uhka-analyysi**: Parannettu kattavuus nykyaikaisista AI-hyökkäysvektoreista
  - Yksityiskohtaiset kehotteen injektiohyökkäysten skenaariot todellisilla esimerkeillä
  - Työkalujen myrkytysmenetelmät ja "rug pull" -hyökkäysmallit
  - Kontekstin ikkunan myrkytys ja mallin sekaannushyökkäykset
- **Microsoftin AI-tietoturvaratkaisut**: Kattava Microsoftin tietoturvaekosysteemin käsittely
  - AI Prompt Shields edistyneillä tunnistus-, korostus- ja erottelutekniikoilla
  - Azure Content Safety -integraatiomallit
  - GitHub Advanced Security toimitusketjun suojaukseen
- **Edistynyt uhkien torjunta**: Yksityiskohtaiset tietoturvakontrollit
  - Istunnon kaappaus MCP-spesifisillä hyökkäysskenaarioilla ja kryptografisilla istuntotunnistevaatimuksilla
  - Confused Deputy -ongelmat MCP-välitysskenaarioissa eksplisiittisillä suostumusvaatimuksilla
  - Token Passthrough -haavoittuvuudet pakollisilla validointikontrolleilla
- **Toimitusketjun tietoturva**: Laajennettu AI-toimitusketjun kattavuus, mukaan lukien perustamallit, upotettujen palvelut, kontekstin tarjoajat ja kolmannen osapuolen API:t
- **Perustietoturva**: Parannettu integraatio yritystason tietoturvamalleihin, mukaan lukien nollaluottamusarkkitehtuuri ja Microsoftin tietoturvaekosysteemi
- **Resurssien organisointi**: Kategorisoitu kattavat resurssilinkit tyypin mukaan (Viralliset dokumentit, standardit, tutkimus, Microsoftin ratkaisut, toteutusoppaat)

### Dokumentaation laadun parannukset
- **Rakenteelliset oppimistavoitteet**: Parannettu oppimistavoitteet konkreettisilla ja toteutettavilla tuloksilla
- **Ristiviittaukset**: Lisätty linkkejä liittyvien tietoturva- ja peruskäsitteiden aiheiden välillä
- **Ajankohtainen tieto**: Päivitetty kaikki päivämääräviittaukset ja spesifikaatiolinkit nykyisiin standardeihin
- **Toteutusohjeet**: Lisätty erityisiä ja toteutettavia ohjeita molempiin osioihin

## 16. heinäkuuta 2025

### README ja navigoinnin parannukset
- Suunniteltu README.md:n navigointi kokonaan uudelleen
- Korvattu `<details>`-tagit saavutettavammalla taulukkomuotoisella rakenteella
- Luotu vaihtoehtoisia asetteluvaihtoehtoja uuteen "alternative_layouts" -kansioon
- Lisätty korttipohjaisia, välilehtityylisiä ja haitarimaisia navigointiesimerkkejä
- Päivitetty hakemistorakenteen osio sisältämään kaikki uusimmat tiedostot
- Parannettu "Kuinka käyttää tätä opetusohjelmaa" -osio selkeillä suosituksilla
- Päivitetty MCP-spesifikaatiolinkit osoittamaan oikeisiin URL-osoitteisiin
- Lisätty kontekstisuunnittelun osio (5.14) opetusohjelman rakenteeseen

### Opasmuutokset
- Uudistettu opas kokonaan vastaamaan nykyistä hakemistorakennetta
- Lisätty uusia osioita MCP-asiakkaille ja -työkaluille sekä suosituimmille MCP-palvelimille
- Päivitetty visuaalinen opetusohjelmakartta vastaamaan tarkasti kaikkia aiheita
- Parannettu edistyneiden aiheiden kuvauksia kattamaan kaikki erikoistuneet alueet
- Päivitetty tapaustutkimusten osio vastaamaan todellisia esimerkkejä
- Lisätty tämä kattava muutosloki

### Yhteisön panokset (06-CommunityContributions/)
- Lisätty yksityiskohtaista tietoa MCP-palvelimista kuvageneraatiota varten
- Lisätty kattava osio Clauden käytöstä VSCode:ssa
- Lisätty Cline-pääteliittymäasiakkaan asennus- ja käyttöohjeet
- Päivitetty MCP-asiakasosio sisältämään kaikki suosituimmat asiakasvaihtoehdot
- Parannettu esimerkkipanoksia tarkemmilla koodinäytteillä

### Edistyneet aiheet (05-AdvancedTopics/)
- Järjestetty kaikki erikoistuneiden aiheiden kansiot johdonmukaisilla nimillä
- Lisätty kontekstisuunnittelumateriaaleja ja esimerkkejä
- Lisätty Foundry-agentin integraatiodokumentaatio
- Parannettu Entra ID -tietoturvaintegraatiodokumentaatio

## 11. kesäkuuta 2025

### Alkuperäinen luominen
- Julkaistu ensimmäinen versio MCP for Beginners -opetusohjelmasta
- Luotu perusrakenne kaikille 10 pääosalle
- Toteutettu visuaalinen opetusohjelmakartta navigointia varten
- Lisätty alkuperäiset esimerkkiprojektit useilla ohjelmointikielillä

### Aloittaminen (03-GettingStarted/)
- Luotu ensimmäiset palvelintoteutusesimerkit
- Lisätty asiakaskehityksen ohjeistus
- Sisällytetty LLM-asiakasintegraatio-ohjeet
- Lisätty VS Code -integraatiodokumentaatio
- Toteutettu Server-Sent Events (SSE) -palvelinesimerkit

### Peruskäsitteet (01-CoreConcepts/)
- Lisätty yksityiskohtainen selitys asiakas-palvelin-arkkitehtuurista
- Luotu dokumentaatio keskeisistä protokollakomponenteista
- Dokumentoitu viestintäkuviot MCP:ssä

## 23. toukokuuta 2025

### Hakemistorakenne
- Alustettu hakemisto peruskansiorakenteella
- Luotu README-tiedostot jokaiselle pääosalle
- Asetettu käännösinfrastruktuuri
- Lisätty kuvatiedostot ja kaaviot

### Dokumentaatio
- Luotu alkuperäinen README.md opetusohjelman yleiskatsauksella
- Lisätty CODE_OF_CONDUCT.md ja SECURITY.md
- Asetettu SUPPORT.md ohjeilla avun saamiseen
- Luotu alustava opasrakenne

## 15. huhtikuuta 2025

### Suunnittelu ja kehys
- Alustava suunnittelu MCP for Beginners -opetusohjelmalle
- Määritelty oppimistavoitteet ja kohdeyleisö
- Luotu opetusohjelman 10-osainen rakenne
- Kehitetty käsitteellinen kehys esimerkeille ja tapaustutkimuksille
- Luotu alkuperäiset prototyyppiesimerkit keskeisistä käsitteistä

---

**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, huomioithan, että automaattiset käännökset voivat sisältää virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäisellä kielellä tulisi pitää ensisijaisena lähteenä. Kriittisen tiedon osalta suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa väärinkäsityksistä tai virhetulkinnoista, jotka johtuvat tämän käännöksen käytöstä.