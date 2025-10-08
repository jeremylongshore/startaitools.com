<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-07T00:27:07+00:00",
  "source_file": "changelog.md",
  "language_code": "lt"
}
-->
# Keitimų žurnalas: MCP pradedančiųjų mokymo programa

Šis dokumentas yra visų reikšmingų pakeitimų, atliktų Model Context Protocol (MCP) pradedančiųjų mokymo programoje, įrašas. Pakeitimai dokumentuojami atvirkštine chronologine tvarka (naujausi pakeitimai pirmiausia).

## 2025 m. spalio 6 d.

### Pradžios skyriaus plėtra – pažangus serverio naudojimas ir paprasta autentifikacija

#### Pažangus serverio naudojimas (03-GettingStarted/10-advanced)
- **Pridėtas naujas skyrius**: Įtraukta išsami MCP serverio pažangaus naudojimo instrukcija, apimanti tiek įprastą, tiek žemo lygio serverio architektūrą.
  - **Įprastas vs. žemo lygio serveris**: Išsamus palyginimas ir Python bei TypeScript kodų pavyzdžiai abiem metodams.
  - **Handler pagrįstas dizainas**: Paaiškinimas apie handler pagrįstą įrankių/resursų/promptų valdymą, siekiant sukurti mastelio keičiamus ir lankstus serverio sprendimus.
  - **Praktiniai modeliai**: Realių situacijų pavyzdžiai, kur žemo lygio serverio modeliai yra naudingi pažangioms funkcijoms ir architektūrai.

#### Paprasta autentifikacija (03-GettingStarted/11-simple-auth)
- **Pridėtas naujas skyrius**: Žingsnis po žingsnio vadovas, kaip įgyvendinti paprastą autentifikaciją MCP serveriuose.
  - **Autentifikacijos sąvokos**: Aiškus autentifikacijos ir autorizacijos bei kredencialų tvarkymo paaiškinimas.
  - **Pagrindinė autentifikacija**: Middleware pagrįsti autentifikacijos modeliai Python (Starlette) ir TypeScript (Express) su kodų pavyzdžiais.
  - **Perėjimas prie pažangios saugos**: Patarimai, kaip pradėti nuo paprastos autentifikacijos ir pereiti prie OAuth 2.1 ir RBAC, su nuorodomis į pažangius saugos modulius.

Šie papildymai suteikia praktinių, praktinių instrukcijų, kaip kurti tvirtesnius, saugesnius ir lankstesnius MCP serverio sprendimus, sujungiant pagrindines sąvokas su pažangiais gamybos modeliais.

## 2025 m. rugsėjo 29 d.

### MCP serverio duomenų bazės integracijos laboratorijos – išsamus praktinio mokymosi kelias

#### 11-MCPServerHandsOnLabs - Nauja pilna duomenų bazės integracijos mokymo programa
- **Pilnas 13 laboratorijų mokymosi kelias**: Pridėta išsami praktinė mokymo programa, skirta kurti gamybai paruoštus MCP serverius su PostgreSQL duomenų bazės integracija.
  - **Realių situacijų įgyvendinimas**: Zava Retail analitikos naudojimo atvejis, demonstruojantis įmonės lygio modelius.
  - **Struktūrizuotas mokymosi progresas**:
    - **Laboratorijos 00-03: Pagrindai** - Įvadas, pagrindinė architektūra, saugumas ir daugiaklientė aplinka, aplinkos nustatymas.
    - **Laboratorijos 04-06: MCP serverio kūrimas** - Duomenų bazės dizainas ir schema, MCP serverio įgyvendinimas, įrankių kūrimas.
    - **Laboratorijos 07-09: Pažangios funkcijos** - Semantinės paieškos integracija, testavimas ir derinimas, VS Code integracija.
    - **Laboratorijos 10-12: Gamyba ir geriausios praktikos** - Diegimo strategijos, stebėjimas ir stebimumas, geriausios praktikos ir optimizavimas.
  - **Įmonės technologijos**: FastMCP framework, PostgreSQL su pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Pažangios funkcijos**: Row Level Security (RLS), semantinė paieška, daugiaklientė duomenų prieiga, vektoriniai embeddingai, realaus laiko stebėjimas.

#### Terminologijos standartizavimas - Modulių keitimas į laboratorijas
- **Išsamus dokumentacijos atnaujinimas**: Sistemingai atnaujinti visi README failai 11-MCPServerHandsOnLabs, kad būtų naudojama "Laboratorijos" terminologija vietoj "Moduliai".
  - **Skyriaus antraštės**: Atnaujinta "Ką apima šis modulis" į "Ką apima ši laboratorija" visose 13 laboratorijose.
  - **Turinio aprašymas**: Pakeista "Šis modulis suteikia..." į "Ši laboratorija suteikia..." visoje dokumentacijoje.
  - **Mokymosi tikslai**: Atnaujinta "Iki šio modulio pabaigos..." į "Iki šios laboratorijos pabaigos..."
  - **Navigacijos nuorodos**: Visos "Modulis XX:" nuorodos pakeistos į "Laboratorija XX:" kryžminėse nuorodose ir navigacijoje.
  - **Užbaigimo stebėjimas**: Atnaujinta "Baigus šį modulį..." į "Baigus šią laboratoriją..."
  - **Išsaugotos techninės nuorodos**: Išlaikytos Python modulio nuorodos konfigūracijos failuose (pvz., `"module": "mcp_server.main"`).

#### Mokymosi vadovo patobulinimas (study_guide.md)
- **Vizualus mokymo programos žemėlapis**: Pridėta nauja "11. Duomenų bazės integracijos laboratorijos" sekcija su išsamia laboratorijų struktūros vizualizacija.
- **Repozitorijos struktūra**: Atnaujinta nuo dešimties iki vienuolikos pagrindinių sekcijų su detaliu 11-MCPServerHandsOnLabs aprašymu.
- **Mokymosi kelio gairės**: Patobulintos navigacijos instrukcijos, apimančios sekcijas 00-11.
- **Technologijų aprėptis**: Pridėta FastMCP, PostgreSQL, Azure paslaugų integracijos detalės.
- **Mokymosi rezultatai**: Pabrėžtas gamybai paruoštų serverių kūrimas, duomenų bazės integracijos modeliai ir įmonės saugumas.

#### Pagrindinio README struktūros patobulinimas
- **Laboratorijų terminologija**: Atnaujintas pagrindinis README.md 11-MCPServerHandsOnLabs, kad būtų nuosekliai naudojama "Laboratorijų" struktūra.
- **Mokymosi kelio organizavimas**: Aiškus progresas nuo pagrindinių sąvokų iki pažangaus įgyvendinimo ir gamybos diegimo.
- **Realių situacijų dėmesys**: Pabrėžtas praktinis, praktinis mokymasis su įmonės lygio modeliais ir technologijomis.

### Dokumentacijos kokybės ir nuoseklumo patobulinimai
- **Praktinio mokymosi akcentas**: Sustiprintas praktinis, laboratorijomis pagrįstas požiūris visoje dokumentacijoje.
- **Įmonės modelių dėmesys**: Pabrėžtas gamybai paruoštų įgyvendinimų ir įmonės saugumo aspektų svarba.
- **Technologijų integracija**: Išsamiai aprašytos modernios Azure paslaugos ir AI integracijos modeliai.
- **Mokymosi progresas**: Aiškus, struktūrizuotas kelias nuo pagrindinių sąvokų iki gamybos diegimo.

## 2025 m. rugsėjo 26 d.

### Atvejų studijų patobulinimas – GitHub MCP registracijos integracija

#### Atvejų studijos (09-CaseStudy/) - Dėmesys ekosistemos plėtrai
- **README.md**: Didelis išplėtimas su išsamia GitHub MCP registracijos atvejo studija.
  - **GitHub MCP registracijos atvejo studija**: Nauja išsami atvejo studija, nagrinėjanti GitHub MCP registracijos paleidimą 2025 m. rugsėjį.
    - **Problemos analizė**: Išsamus suskaidytos MCP serverio paieškos ir diegimo iššūkių nagrinėjimas.
    - **Sprendimo architektūra**: GitHub centralizuotos registracijos metodas su vieno paspaudimo VS Code diegimu.
    - **Verslo poveikis**: Matomi patobulinimai kūrėjų įsitraukime ir produktyvume.
    - **Strateginė vertė**: Dėmesys modulinio agento diegimui ir kryžminiam įrankių suderinamumui.
    - **Ekosistemos plėtra**: Pozicionavimas kaip pagrindinė platforma agentų integracijai.
  - **Patobulinta atvejo studijų struktūra**: Atnaujintos visos septynios atvejų studijos su nuosekliu formatavimu ir išsamiais aprašymais.
    - Azure AI kelionių agentai: Dėmesys daugiagentinei orkestracijai.
    - Azure DevOps integracija: Dėmesys darbo eigos automatizavimui.
    - Realaus laiko dokumentacijos paieška: Python konsolės kliento įgyvendinimas.
    - Interaktyvus mokymosi plano generatorius: Chainlit pokalbių internetinė programa.
    - Dokumentacija redaktoriuje: VS Code ir GitHub Copilot integracija.
    - Azure API valdymas: Įmonės API integracijos modeliai.
    - GitHub MCP registracija: Ekosistemos plėtra ir bendruomenės platforma.
  - **Išsamios išvados**: Perrašyta išvadų sekcija, pabrėžianti septynias atvejų studijas, apimančias įvairius MCP įgyvendinimo aspektus.
    - Įmonės integracija, daugiagentinė orkestracija, kūrėjų produktyvumas.
    - Ekosistemos plėtra, edukacinės aplikacijos kategorijos.
    - Patobulintos įžvalgos apie architektūros modelius, įgyvendinimo strategijas ir geriausias praktikas.
    - Dėmesys MCP kaip brandžiam, gamybai paruoštam protokolui.

#### Mokymosi vadovo atnaujinimai (study_guide.md)
- **Vizualus mokymo programos žemėlapis**: Atnaujintas minčių žemėlapis, įtraukiant GitHub MCP registraciją į atvejų studijų sekciją.
- **Atvejų studijų aprašymas**: Patobulintas nuo bendrų aprašymų iki detalių septynių išsamių atvejų studijų aprašymų.
- **Repozitorijos struktūra**: Atnaujinta 10 sekcija, kad atspindėtų išsamų atvejų studijų aprėptį su konkrečiomis įgyvendinimo detalėmis.
- **Keitimų žurnalo integracija**: Pridėta 2025 m. rugsėjo 26 d. įrašas, dokumentuojantis GitHub MCP registracijos papildymą ir atvejų studijų patobulinimus.
- **Datos atnaujinimai**: Atnaujintas poraštės laiko žymeklis, kad atspindėtų naujausią peržiūrą (2025 m. rugsėjo 26 d.).

### Dokumentacijos kokybės patobulinimai
- **Nuoseklumo patobulinimas**: Standartizuotas atvejų studijų formatavimas ir struktūra visose septyniose pavyzdžiuose.
- **Išsamus aprėptis**: Atvejų studijos dabar apima įmonės, kūrėjų produktyvumo ir ekosistemos plėtros scenarijus.
- **Strateginis pozicionavimas**: Sustiprintas dėmesys MCP kaip pagrindinei platformai agentų sistemų diegimui.
- **Resursų integracija**: Atnaujinti papildomi resursai, įtraukiant GitHub MCP registracijos nuorodą.

## 2025 m. rugsėjo 15 d.

### Pažangių temų plėtra – individualūs transportai ir konteksto inžinerija

#### MCP individualūs transportai (05-AdvancedTopics/mcp-transport/) - Naujas pažangus įgyvendinimo vadovas
- **README.md**: Pilnas įgyvendinimo vadovas individualiems MCP transporto mechanizmams.
  - **Azure Event Grid transportas**: Išsamus serverless įvykių pagrįsto transporto įgyvendinimas.
    - C#, TypeScript ir Python pavyzdžiai su Azure Functions integracija.
    - Įvykių pagrįstos architektūros modeliai, skirti mastelio keičiamoms MCP sprendimams.
    - Webhook gavėjai ir push pagrįstas pranešimų tvarkymas.
  - **Azure Event Hubs transportas**: Didelio pralaidumo srautinio transporto įgyvendinimas.
    - Realaus laiko srautinės galimybės mažo vėlavimo scenarijams.
    - Particionavimo strategijos ir kontrolės taškų valdymas.
    - Pranešimų grupavimas ir našumo optimizavimas.
  - **Įmonės integracijos modeliai**: Gamybai paruošti architektūros pavyzdžiai.
    - Paskirstytas MCP apdorojimas per kelias Azure Functions.
    - Hibridinės transporto architektūros, derinančios kelis transporto tipus.
    - Pranešimų patvarumas, patikimumas ir klaidų tvarkymo strategijos.
  - **Saugumas ir stebėjimas**: Azure Key Vault integracija ir stebėjimo modeliai.
    - Valdomos tapatybės autentifikacija ir minimalios privilegijos prieiga.
    - Application Insights telemetrija ir našumo stebėjimas.
    - Circuit breakers ir gedimų tolerancijos modeliai.
  - **Testavimo sistemos**: Išsamios testavimo strategijos individualiems transportams.
    - Vienetinis testavimas su test doubles ir mocking framework'ais.
    - Integracinis testavimas su Azure Test Containers.
    - Našumo ir apkrovos testavimo aspektai.

#### Konteksto inžinerija (05-AdvancedTopics/mcp-contextengineering/) - Nauja AI disciplina
- **README.md**: Išsamus konteksto inžinerijos kaip naujos srities tyrimas.
  - **Pagrindiniai principai**: Pilnas konteksto dalijimasis, veiksmų sprendimų supratimas ir konteksto lango valdymas.
  - **MCP protokolo suderinamumas**: Kaip MCP dizainas sprendžia konteksto inžinerijos iššūkius.
    - Konteksto lango apribojimai ir progresyvaus įkėlimo strategijos.
    - Reikšmingumo nustatymas ir dinaminis konteksto paieška.
    - Daugiarūšio konteksto tvarkymas ir saugumo aspektai.
  - **Įgyvendinimo metodai**: Vieno gijos vs. daugiagentės architektūros.
    - Konteksto skaidymas ir prioritizavimo technikos.
    - Progresyvus konteksto įkėlimas ir suspaudimo strategijos.
    - Sluoksniuotos konteksto metodikos ir paieškos optimizavimas.
  - **Matavimo sistema**: Nauji metrikos konteksto efektyvumo vertinimui.
    - Įvesties efektyvumas, našumas, kokybė ir vartotojo patirties aspektai.
    - Eksperimentiniai konteksto optimizavimo metodai.
    - Klaidų analizė ir tobulinimo metodologijos.

#### Mokymo programos navigacijos atnaujinimai (README.md)
- **Patobulinta modulių struktūra**: Atnaujinta mokymo programos lentelė, įtraukiant naujas pažangias temas.
  - Pridėta Konteksto inžinerija (5.14) ir Individualus transportas (5.15).
  - Nuoseklus formatavimas ir navigacijos nuorodos visiems moduliams.
  - Atnaujinti aprašymai, atspindintys dabartinį turinio apimtį.

### Katalogo struktūros patobulinimai
- **Pavadinimų standartizavimas**: Pervadintas "mcp transport" į "mcp-transport", kad būtų nuoseklumas su kitais pažangių temų katalogais.
- **Turinio organizavimas**: Visi 05-AdvancedTopics katalogai dabar laikosi nuoseklaus pavadinimų modelio (mcp-[tema]).

### Dokumentacijos kokybės patobulinimai
- **MCP specifikacijos suderinamumas**: Visas naujas turinys remiasi dabartine MCP specifikacija 2025-06-18.
- **Daugiakalbiai pavyzdžiai**: Išsamūs kodų pavy
#### Pažangios temos saugumas (05-AdvancedTopics/mcp-security/) - Paruošta gamybai
- **README.md**: Visiškai perrašyta įmonės saugumo įgyvendinimui
  - **Dabartinis specifikacijos suderinimas**: Atnaujinta pagal MCP specifikaciją 2025-06-18 su privalomais saugumo reikalavimais
  - **Patobulinta autentifikacija**: Microsoft Entra ID integracija su išsamiais .NET ir Java Spring Security pavyzdžiais
  - **AI saugumo integracija**: Microsoft Prompt Shields ir Azure Content Safety įgyvendinimas su detalizuotais Python pavyzdžiais
  - **Pažangi grėsmių mažinimo strategija**: Išsamūs įgyvendinimo pavyzdžiai:
    - „Confused Deputy“ atakų prevencija naudojant PKCE ir vartotojo sutikimo patvirtinimą
    - Tokenų perdavimo prevencija naudojant auditorijos patvirtinimą ir saugų tokenų valdymą
    - Sesijos užgrobimo prevencija naudojant kriptografinį susiejimą ir elgsenos analizę
  - **Įmonės saugumo integracija**: Azure Application Insights stebėjimas, grėsmių aptikimo kanalai ir tiekimo grandinės saugumas
  - **Įgyvendinimo kontrolinis sąrašas**: Aiškiai atskirti privalomi ir rekomenduojami saugumo kontrolės punktai su Microsoft saugumo ekosistemos privalumais

### Dokumentacijos kokybė ir standartų suderinimas
- **Specifikacijos nuorodos**: Atnaujintos visos nuorodos į dabartinę MCP specifikaciją 2025-06-18
- **Microsoft saugumo ekosistema**: Patobulintos integracijos gairės visoje saugumo dokumentacijoje
- **Praktinis įgyvendinimas**: Pridėti detalizuoti kodų pavyzdžiai .NET, Java ir Python su įmonės šablonais
- **Resursų organizavimas**: Išsamus oficialios dokumentacijos, saugumo standartų ir įgyvendinimo vadovų kategorizavimas
- **Vizualiniai indikatoriai**: Aiškiai pažymėti privalomi reikalavimai ir rekomenduojamos praktikos

#### Pagrindinės sąvokos (01-CoreConcepts/) - Visiška modernizacija
- **Protokolo versijos atnaujinimas**: Atnaujinta nuoroda į dabartinę MCP specifikaciją 2025-06-18 su datos pagrindu versijavimu (YYYY-MM-DD formatas)
- **Architektūros patobulinimas**: Patobulinti aprašymai apie Host'us, Klientus ir Serverius, atspindint dabartinius MCP architektūros šablonus
  - Host'ai dabar aiškiai apibrėžti kaip AI programos, koordinuojančios kelis MCP klientų ryšius
  - Klientai aprašyti kaip protokolo jungtys, palaikančios vienas su vienu serverio ryšius
  - Serveriai patobulinti su vietinio ir nuotolinio diegimo scenarijais
- **Primitivų restruktūrizavimas**: Visiškai peržiūrėti serverio ir kliento primityvai
  - Serverio primityvai: Resursai (duomenų šaltiniai), Šablonai (templates), Įrankiai (vykdomos funkcijos) su detalizuotais paaiškinimais ir pavyzdžiais
  - Kliento primityvai: Mėginių ėmimas (LLM užbaigimai), Elicitacija (vartotojo įvestis), Žurnalavimas (debugging/monitoring)
  - Atnaujinta su dabartiniais atradimo (`*/list`), gavimo (`*/get`) ir vykdymo (`*/call`) metodų šablonais
- **Protokolo architektūra**: Įvesta dviejų sluoksnių architektūros modelis
  - Duomenų sluoksnis: JSON-RPC 2.0 pagrindas su gyvavimo ciklo valdymu ir primityvais
  - Transporto sluoksnis: STDIO (vietinis) ir Streamable HTTP su SSE (nuotolinis) transporto mechanizmais
- **Saugumo sistema**: Išsamūs saugumo principai, įskaitant aiškų vartotojo sutikimą, duomenų privatumo apsaugą, įrankių vykdymo saugumą ir transporto sluoksnio saugumą
- **Komunikacijos šablonai**: Atnaujinti protokolo pranešimai, rodantys inicializaciją, atradimą, vykdymą ir pranešimų srautus
- **Kodų pavyzdžiai**: Atnaujinti daugiakalbiai pavyzdžiai (.NET, Java, Python, JavaScript), atspindintys dabartinius MCP SDK šablonus

#### Saugumas (02-Security/) - Išsamus saugumo peržiūrėjimas  
- **Standartų suderinimas**: Visiškas suderinimas su MCP specifikacijos 2025-06-18 saugumo reikalavimais
- **Autentifikacijos evoliucija**: Dokumentuota evoliucija nuo individualių OAuth serverių iki išorinių tapatybės tiekėjų delegavimo (Microsoft Entra ID)
- **AI specifinė grėsmių analizė**: Patobulinta šiuolaikinių AI atakų vektorių aprėptis
  - Detalizuoti „Prompt Injection“ atakų scenarijai su realaus pasaulio pavyzdžiais
  - Įrankių užnuodijimo mechanizmai ir „rug pull“ atakų šablonai
  - Konteksto lango užnuodijimas ir modelio painiavos atakos
- **Microsoft AI saugumo sprendimai**: Išsamus Microsoft saugumo ekosistemos aprėptis
  - AI Prompt Shields su pažangiu aptikimu, akcentavimu ir skyriklio technikomis
  - Azure Content Safety integracijos šablonai
  - GitHub Advanced Security tiekimo grandinės apsaugai
- **Pažangi grėsmių mažinimo strategija**: Detalizuoti saugumo kontrolės punktai:
  - Sesijos užgrobimas su MCP specifiniais atakų scenarijais ir kriptografiniais sesijos ID reikalavimais
  - „Confused Deputy“ problemos MCP proxy scenarijuose su aiškiais sutikimo reikalavimais
  - Tokenų perdavimo pažeidžiamumai su privalomais patvirtinimo kontrolės punktais
- **Tiekimo grandinės saugumas**: Išplėsta AI tiekimo grandinės aprėptis, įskaitant pagrindinius modelius, įterpimo paslaugas, konteksto tiekėjus ir trečiųjų šalių API
- **Pagrindinis saugumas**: Patobulinta integracija su įmonės saugumo šablonais, įskaitant „Zero Trust“ architektūrą ir Microsoft saugumo ekosistemą
- **Resursų organizavimas**: Kategorizuoti išsamūs resursų nuorodų sąrašai pagal tipą (Oficiali dokumentacija, Standartai, Tyrimai, Microsoft sprendimai, Įgyvendinimo vadovai)

### Dokumentacijos kokybės patobulinimai
- **Struktūruoti mokymosi tikslai**: Patobulinti mokymosi tikslai su konkrečiais, veiksmais pagrįstais rezultatais
- **Kryžminės nuorodos**: Pridėtos nuorodos tarp susijusių saugumo ir pagrindinių sąvokų temų
- **Dabartinė informacija**: Atnaujintos visos datos nuorodos ir specifikacijos nuorodos į dabartinius standartus
- **Įgyvendinimo gairės**: Pridėtos konkrečios, veiksmais pagrįstos įgyvendinimo gairės visose sekcijose

## 2025 m. liepos 16 d.

### README ir navigacijos patobulinimai
- Visiškai pertvarkyta mokymo programos navigacija README.md
- Pakeisti `<details>` žymos į labiau prieinamą lentelės formatą
- Sukurti alternatyvūs išdėstymo variantai naujame „alternative_layouts“ aplanke
- Pridėti kortelių, skirtukų stiliaus ir akordeono stiliaus navigacijos pavyzdžiai
- Atnaujinta saugyklos struktūros sekcija, įtraukiant visus naujausius failus
- Patobulinta „Kaip naudoti šią mokymo programą“ sekcija su aiškiomis rekomendacijomis
- Atnaujintos MCP specifikacijos nuorodos, kad nukreiptų į tinkamus URL
- Pridėta konteksto inžinerijos sekcija (5.14) į mokymo programos struktūrą

### Mokymosi vadovo atnaujinimai
- Visiškai peržiūrėtas mokymosi vadovas, kad atitiktų dabartinę saugyklos struktūrą
- Pridėtos naujos sekcijos apie MCP klientus ir įrankius bei populiarius MCP serverius
- Atnaujintas vizualinis mokymo programos žemėlapis, kad tiksliai atspindėtų visas temas
- Patobulinti pažangių temų aprašymai, apimantys visas specializuotas sritis
- Atnaujinta atvejų analizės sekcija, kad atspindėtų realius pavyzdžius
- Pridėtas šis išsamus pakeitimų žurnalas

### Bendruomenės indėlis (06-CommunityContributions/)
- Pridėta išsami informacija apie MCP serverius vaizdų generavimui
- Pridėta išsami sekcija apie Claude naudojimą VSCode
- Pridėtos Cline terminalo kliento nustatymo ir naudojimo instrukcijos
- Atnaujinta MCP klientų sekcija, įtraukiant visus populiarius klientų variantus
- Patobulinti indėlių pavyzdžiai su tikslesniais kodų pavyzdžiais

### Pažangios temos (05-AdvancedTopics/)
- Organizuoti visi specializuotų temų aplankai su nuosekliais pavadinimais
- Pridėta konteksto inžinerijos medžiaga ir pavyzdžiai
- Pridėta Foundry agento integracijos dokumentacija
- Patobulinta Entra ID saugumo integracijos dokumentacija

## 2025 m. birželio 11 d.

### Pradinis sukūrimas
- Išleista pirmoji MCP pradedantiesiems mokymo programos versija
- Sukurta pagrindinė struktūra visoms 10 pagrindinių sekcijų
- Įgyvendintas vizualinis mokymo programos žemėlapis navigacijai
- Pridėti pradiniai pavyzdiniai projektai keliomis programavimo kalbomis

### Pradžia (03-GettingStarted/)
- Sukurti pirmieji serverio įgyvendinimo pavyzdžiai
- Pridėtos klientų kūrimo gairės
- Įtrauktos LLM kliento integracijos instrukcijos
- Pridėta VS Code integracijos dokumentacija
- Įgyvendinti Server-Sent Events (SSE) serverio pavyzdžiai

### Pagrindinės sąvokos (01-CoreConcepts/)
- Pridėtas išsamus klientų-serverių architektūros paaiškinimas
- Sukurta dokumentacija apie pagrindinius protokolo komponentus
- Dokumentuoti MCP pranešimų šablonai

## 2025 m. gegužės 23 d.

### Saugyklos struktūra
- Inicializuota saugykla su pagrindine aplankų struktūra
- Sukurti README failai kiekvienai pagrindinei sekcijai
- Nustatyta vertimo infrastruktūra
- Pridėti vaizdo ištekliai ir diagramos

### Dokumentacija
- Sukurtas pradinis README.md su mokymo programos apžvalga
- Pridėti CODE_OF_CONDUCT.md ir SECURITY.md
- Nustatytas SUPPORT.md su pagalbos gavimo gairėmis
- Sukurta preliminari mokymosi vadovo struktūra

## 2025 m. balandžio 15 d.

### Planavimas ir struktūra
- Pradinis MCP pradedantiesiems mokymo programos planavimas
- Apibrėžti mokymosi tikslai ir tikslinė auditorija
- Nubrėžta 10 sekcijų mokymo programos struktūra
- Sukurtas konceptualus pavyzdžių ir atvejų analizės pagrindas
- Sukurti pradiniai prototipiniai pavyzdžiai pagrindinėms sąvokoms

---

**Atsakomybės atsisakymas**:  
Šis dokumentas buvo išverstas naudojant AI vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojama naudoti profesionalų žmogaus vertimą. Mes neprisiimame atsakomybės už nesusipratimus ar neteisingus interpretavimus, atsiradusius dėl šio vertimo naudojimo.