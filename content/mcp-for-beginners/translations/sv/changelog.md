<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:14:10+00:00",
  "source_file": "changelog.md",
  "language_code": "sv"
}
-->
# Ändringslogg: MCP för Nybörjare Curriculum

Detta dokument fungerar som en redogörelse för alla betydande ändringar som gjorts i Model Context Protocol (MCP) för nybörjare. Ändringarna dokumenteras i omvänd kronologisk ordning (nyaste ändringar först).

## 6 oktober 2025

### Utökning av avsnittet Komma igång – Avancerad serveranvändning & Enkel autentisering

#### Avancerad serveranvändning (03-GettingStarted/10-advanced)
- **Nytt kapitel tillagt**: Introducerade en omfattande guide till avancerad användning av MCP-servrar, som täcker både vanliga och låg-nivå serverarkitekturer.
  - **Vanlig vs. Låg-nivå server**: Detaljerad jämförelse och kodexempel i Python och TypeScript för båda tillvägagångssätten.
  - **Handler-baserad design**: Förklaring av handler-baserad hantering av verktyg/resurser/prompter för skalbara och flexibla serverimplementationer.
  - **Praktiska mönster**: Verkliga scenarier där låg-nivå servermönster är fördelaktiga för avancerade funktioner och arkitekturer.

#### Enkel autentisering (03-GettingStarted/11-simple-auth)
- **Nytt kapitel tillagt**: Steg-för-steg-guide för att implementera enkel autentisering i MCP-servrar.
  - **Autentiseringskoncept**: Klar förklaring av skillnaden mellan autentisering och auktorisering, samt hantering av autentiseringsuppgifter.
  - **Grundläggande autentisering**: Middleware-baserade autentiseringsmönster i Python (Starlette) och TypeScript (Express), med kodexempel.
  - **Framsteg mot avancerad säkerhet**: Vägledning om att börja med enkel autentisering och avancera till OAuth 2.1 och RBAC, med hänvisningar till avancerade säkerhetsmoduler.

Dessa tillägg ger praktisk, handgriplig vägledning för att bygga mer robusta, säkra och flexibla MCP-serverimplementationer, och skapar en bro mellan grundläggande koncept och avancerade produktionsmönster.

## 29 september 2025

### MCP Server Database Integration Labs - Omfattande praktisk inlärningsväg

#### 11-MCPServerHandsOnLabs - Ny komplett databasintegrationscurriculum
- **Komplett 13-labs inlärningsväg**: Lagt till en omfattande praktisk curriculum för att bygga produktionsklara MCP-servrar med PostgreSQL-databasintegration.
  - **Verklig implementering**: Zava Retail-analysfall som demonstrerar mönster i företagsklass.
  - **Strukturerad inlärningsprogression**:
    - **Labs 00-03: Grunder** - Introduktion, kärnarkitektur, säkerhet & multi-tenancy, miljöinställning.
    - **Labs 04-06: Bygga MCP-servern** - Databasedesign & schema, MCP-serverimplementation, verktygsutveckling.
    - **Labs 07-09: Avancerade funktioner** - Semantisk sökintegration, testning & felsökning, VS Code-integration.
    - **Labs 10-12: Produktion & bästa praxis** - Implementeringsstrategier, övervakning & observabilitet, bästa praxis & optimering.
  - **Företagsteknologier**: FastMCP-ramverk, PostgreSQL med pgvector, Azure OpenAI-embeddingar, Azure Container Apps, Application Insights.
  - **Avancerade funktioner**: Row Level Security (RLS), semantisk sökning, multi-tenant dataåtkomst, vektor-embeddingar, realtidsövervakning.

#### Terminologistandardisering - Omvandling från modul till labb
- **Omfattande dokumentationsuppdatering**: Systematiskt uppdaterat alla README-filer i 11-MCPServerHandsOnLabs för att använda "Lab"-terminologi istället för "Modul".
  - **Avsnittsrubriker**: Uppdaterat "Vad denna modul täcker" till "Vad detta labb täcker" i alla 13 labb.
  - **Innehållsbeskrivning**: Ändrat "Denna modul tillhandahåller..." till "Detta labb tillhandahåller..." i hela dokumentationen.
  - **Inlärningsmål**: Uppdaterat "I slutet av denna modul..." till "I slutet av detta labb..."
  - **Navigeringslänkar**: Konverterat alla "Modul XX:"-referenser till "Lab XX:" i korsreferenser och navigering.
  - **Slutförandespårning**: Uppdaterat "Efter att ha slutfört denna modul..." till "Efter att ha slutfört detta labb..."
  - **Bevarade tekniska referenser**: Bibehållit Python-modulreferenser i konfigurationsfiler (t.ex. `"module": "mcp_server.main"`).

#### Förbättring av studieguide (study_guide.md)
- **Visuell curriculumkarta**: Lagt till nytt avsnitt "11. Database Integration Labs" med omfattande labbstrukturvisualisering.
- **Repository-struktur**: Uppdaterat från tio till elva huvudavsnitt med detaljerad beskrivning av 11-MCPServerHandsOnLabs.
- **Inlärningsvägledning**: Förbättrade navigeringsinstruktioner för att täcka avsnitt 00-11.
- **Teknologitäckning**: Lagt till detaljer om FastMCP, PostgreSQL och Azure-tjänsters integration.
- **Inlärningsresultat**: Betonade produktionsklar serverutveckling, databasintegrationsmönster och företagsklassad säkerhet.

#### Förbättring av huvud-README-struktur
- **Lab-baserad terminologi**: Uppdaterat huvud-README.md i 11-MCPServerHandsOnLabs för att konsekvent använda "Lab"-struktur.
- **Inlärningsvägsorganisation**: Klar progression från grundläggande koncept till avancerad implementering och produktionsdistribution.
- **Fokus på verkliga tillämpningar**: Betoning på praktisk, handgriplig inlärning med mönster och teknologier i företagsklass.

### Förbättringar av dokumentationskvalitet och konsistens
- **Betoning på praktisk inlärning**: Förstärkt praktisk, labb-baserad metodik i hela dokumentationen.
- **Fokus på företagsmönster**: Lyfte fram produktionsklara implementationer och överväganden kring företagsklassad säkerhet.
- **Teknologiintegration**: Omfattande täckning av moderna Azure-tjänster och AI-integrationsmönster.
- **Inlärningsprogression**: Klar, strukturerad väg från grundläggande koncept till produktionsdistribution.

## 26 september 2025

### Förbättring av fallstudier – GitHub MCP Registry Integration

#### Fallstudier (09-CaseStudy/) - Fokus på ekosystemutveckling
- **README.md**: Större expansion med omfattande fallstudie om GitHubs MCP Registry.
  - **GitHub MCP Registry-fallstudie**: Ny omfattande fallstudie som undersöker GitHubs lansering av MCP Registry i september 2025.
    - **Problemanalys**: Detaljerad undersökning av fragmenterade MCP-serverupptäckts- och distributionsutmaningar.
    - **Lösningsarkitektur**: GitHubs centraliserade registeransats med installation i VS Code med ett klick.
    - **Affärspåverkan**: Mätbara förbättringar i utvecklarintroduktion och produktivitet.
    - **Strategiskt värde**: Fokus på modulär agentdistribution och interoperabilitet mellan verktyg.
    - **Ekosystemutveckling**: Positionering som grundläggande plattform för agentisk integration.
  - **Förbättrad fallstudiestruktur**: Uppdaterat alla sju fallstudier med konsekvent formatering och omfattande beskrivningar.
    - Azure AI Travel Agents: Fokus på multi-agent orkestrering.
    - Azure DevOps Integration: Fokus på arbetsflödesautomation.
    - Realtidsdokumentationshämtning: Implementering av Python-konsolklient.
    - Interaktiv studieplangenerator: Chainlit-konverserande webbapp.
    - Dokumentation i editor: VS Code och GitHub Copilot-integration.
    - Azure API Management: Mönster för företagsklassad API-integration.
    - GitHub MCP Registry: Ekosystemutveckling och communityplattform.
  - **Omfattande slutsats**: Omskriven slutsatssektion som lyfter fram sju fallstudier som täcker flera MCP-implementationsdimensioner.
    - Företagsintegration, multi-agent orkestrering, utvecklarproduktivitet.
    - Ekosystemutveckling, utbildningsapplikationer kategorisering.
    - Förbättrade insikter i arkitekturmönster, implementeringsstrategier och bästa praxis.
    - Betoning på MCP som ett moget, produktionsklart protokoll.

#### Uppdateringar av studieguide (study_guide.md)
- **Visuell curriculumkarta**: Uppdaterad mindmap för att inkludera GitHub MCP Registry i avsnittet Fallstudier.
- **Beskrivning av fallstudier**: Förbättrad från generiska beskrivningar till detaljerad uppdelning av sju omfattande fallstudier.
- **Repository-struktur**: Uppdaterat avsnitt 10 för att återspegla omfattande täckning av fallstudier med specifika implementeringsdetaljer.
- **Integration av ändringslogg**: Lagt till posten 26 september 2025 som dokumenterar tillägget av GitHub MCP Registry och förbättringar av fallstudier.
- **Datumuppdateringar**: Uppdaterat fotnotens tidsstämpel för att återspegla senaste revisionen (26 september 2025).

### Förbättringar av dokumentationskvalitet
- **Förbättrad konsistens**: Standardiserad formatering och struktur för fallstudier över alla sju exempel.
- **Omfattande täckning**: Fallstudier täcker nu företagsintegration, utvecklarproduktivitet och ekosystemutvecklingsscenarier.
- **Strategisk positionering**: Förbättrat fokus på MCP som grundläggande plattform för agentiska system.
- **Resursintegration**: Uppdaterat ytterligare resurser för att inkludera länk till GitHub MCP Registry.

## 15 september 2025

### Utökning av avancerade ämnen – Anpassade transportsystem & kontextteknik

#### MCP Anpassade transportsystem (05-AdvancedTopics/mcp-transport/) - Ny avancerad implementeringsguide
- **README.md**: Komplett implementeringsguide för anpassade MCP-transportmekanismer.
  - **Azure Event Grid Transport**: Omfattande serverlös händelsedriven transportimplementering.
    - Exempel i C#, TypeScript och Python med Azure Functions-integration.
    - Händelsedrivna arkitekturmönster för skalbara MCP-lösningar.
    - Webhook-mottagare och push-baserad meddelandehantering.
  - **Azure Event Hubs Transport**: Implementering av högkapacitets streamingtransport.
    - Realtidsstreaming för scenarier med låg latens.
    - Partitionsstrategier och kontrollpunkthantering.
    - Meddelandebatchning och prestandaoptimering.
  - **Företagsintegrationsmönster**: Produktionsklara arkitekturexempel.
    - Distribuerad MCP-bearbetning över flera Azure Functions.
    - Hybridtransportarkitekturer som kombinerar flera transporttyper.
    - Meddelandedurabilitet, tillförlitlighet och felhanteringsstrategier.
  - **Säkerhet & övervakning**: Integration med Azure Key Vault och observabilitetsmönster.
    - Autentisering med hanterade identiteter och åtkomst med minsta privilegier.
    - Telemetri med Application Insights och prestandaövervakning.
    - Circuit breakers och felhantering.
  - **Testningsramverk**: Omfattande teststrategier för anpassade transportsystem.
    - Enhetstestning med testdubletter och mockningsramverk.
    - Integrationstestning med Azure Test Containers.
    - Prestanda- och belastningstestningsöverväganden.

#### Kontextteknik (05-AdvancedTopics/mcp-contextengineering/) - Framväxande AI-disciplin
- **README.md**: Omfattande utforskning av kontextteknik som ett framväxande område.
  - **Kärnprinciper**: Komplett kontextdelning, medvetenhet om beslutsfattande och hantering av kontextfönster.
  - **MCP-protokollanpassning**: Hur MCP-designen adresserar utmaningar inom kontextteknik.
    - Begränsningar i kontextfönster och strategier för progressiv laddning.
    - Relevansbestämning och dynamisk kontexthämtning.
    - Multimodal kontexthantering och säkerhetsöverväganden.
  - **Implementeringsmetoder**: Enkelttrådade vs. multi-agent arkitekturer.
    - Kontextchunkning och prioriteringstekniker.
    - Progressiv kontextladdning och komprimeringsstrategier.
    - Lagerbaserade kontextmetoder och optimering av hämtning.
  - **Mätningsramverk**: Framväxande metrik för utvärdering av kontexteffektivitet.
    - Effektivitet, prestanda, kvalitet och användarupplevelse.
    - Experimentella metoder för kontextoptimering.
    - Felanalys och förbättringsmetodologier.

#### Uppdateringar av curriculum-navigering (README.md)
- **Förbättrad modulstruktur**: Uppdaterat curriculumtabellen för att inkludera nya avancerade ämnen.
  - Lagt till Kontextteknik (5.14) och Anpassade transportsystem (5.15).
  - Konsekvent formatering och navigeringslänkar över alla moduler.
  - Uppdaterade beskrivningar för att återspegla aktuellt innehåll.

### Förbättringar av katalogstruktur
- **Standardisering av namn**: Bytt namn från "mcp transport" till "mcp-transport" för att matcha andra avancerade ämnesmappar.
- **Innehållsorganisation**: Alla mappar i 05-AdvancedTopics följer nu ett konsekvent namnmönster (mcp-[ämne]).

### Förbättringar av dokumentationskvalitet
- **Anpassning till MCP-specifikation**: Allt nytt innehåll hänvisar till aktuella MCP-specifikationer 2025-06-18.
- **Exempel i flera språk**: Omfattande kodexempel i C#, TypeScript och Python.
- **Fokus på företagsklass**: Produktionsklara mönster och Azure-molnintegration genomgående.
- **Visuell dokumentation**: Mermaid-diagram för arkitektur och flödesvisualisering.

## 18 augusti 2025

### Omfattande dokumentationsuppdatering - MCP 2025-06-18-standarder

#### MCP Säkerhetsbästa praxis (02-Security/) - Komplett modernisering
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Komplett omskrivning anpassad till MCP-specifikation 2025-06-18.
  - **Obligatoriska krav**: Lagt till explicita MÅSTE/MÅSTE INTE-krav från officiell specifikation med tydliga visuella indikatorer.
  - **12 kärnsäkerhetspraxis**: Omstrukturerad från 15-punktslista till omfattande säkerhetsdomäner.
    - Tokensäkerhet & autentisering med integration av externa identitetsleverantörer.
    - Sessionshantering & transportskydd med kryptografiska krav.
    - AI-specifik hotbekämpning med Microsoft Prompt Shields-integration.
    - Åtkomstkontroll & behörigheter med principen om minsta privilegier.
    - Innehållssäkerhet & övervakning med Azure Content Safety-integration.
    - Försörjningskedjesäkerhet med omfattande komponentverifiering.
    - OAuth-säkerhet & förvirrad ställföreträdarprevention med PKCE-implementering.
    - Incidenthantering & återhämtning med automatiserade kapabiliteter.
    - Efterlevnad & styrning med regulatorisk anpassning.
    - Avancerade säkerhetskontroller med zero trust-arkitektur.
    - Microsofts säkerhetsekosystemintegration med omfattande lösningar.
    - Kontinuerlig säkerhetsevolution med adaptiva praxis.
  - **Microsofts säkerhetslösningar**: Förbättrad integrationsvägledning för Prompt Shields, Azure Content Safety, Entra ID och GitHub Advanced Security.
  - **Implementeringsresurser**: Kategoriserade omfattande resurslänkar efter Officiell MCP-dokumentation, Microsofts säkerhetslösningar, säkerhetsstandarder och implementeringsguider.

#### Avancerade säkerhetskontroller (02-Security/) - Företagsimplementering
- **MCP-SECURITY-CONTROLS-2025.md**: Komplett översyn med företagsklassad säkerhetsramverk.
  - **9 omfattande säkerhetsdomäner**: Utökad från grundläggande kontroller till detaljerad företagsramverk.
    - Avancerad autentisering & auktorisering med Microsoft Entra ID-integration.
    - Tokensäkerhet & anti-passthrough-kontroller med omfattande validering.
    - Sessionssäkerhetskontroller med kapningsprevention.
    - AI-specifika säkerhetskontroller med skydd mot promptinjektion och verktygsförgiftning.
    - Förvirrad ställföreträdarattackprevention med OAuth-pro
#### Avancerade ämnen säkerhet (05-AdvancedTopics/mcp-security/) - Implementering redo för produktion
- **README.md**: Fullständig omskrivning för företagsimplementering av säkerhet
  - **Nuvarande specifikationsanpassning**: Uppdaterad till MCP-specifikation 2025-06-18 med obligatoriska säkerhetskrav
  - **Förbättrad autentisering**: Integration med Microsoft Entra ID med omfattande exempel i .NET och Java Spring Security
  - **AI-säkerhetsintegration**: Implementering av Microsoft Prompt Shields och Azure Content Safety med detaljerade Python-exempel
  - **Avancerad hotreducering**: Omfattande implementeringsexempel för
    - Förebyggande av förvirrade ställföreträdarattacker med PKCE och validering av användarsamtycke
    - Förebyggande av tokenöverföring med validering av målgrupp och säker tokenhantering
    - Förebyggande av sessionkapning med kryptografisk bindning och beteendeanalys
  - **Integration av företagsäkerhet**: Övervakning med Azure Application Insights, hotdetekteringspipelines och leverantörskedjesäkerhet
  - **Implementeringschecklista**: Tydliga obligatoriska kontra rekommenderade säkerhetskontroller med fördelar från Microsofts säkerhetsekosystem

### Dokumentationskvalitet och standardanpassning
- **Specifikationsreferenser**: Uppdaterade alla referenser till nuvarande MCP-specifikation 2025-06-18
- **Microsofts säkerhetsekosystem**: Förbättrad integrationsvägledning genom hela säkerhetsdokumentationen
- **Praktisk implementering**: Lade till detaljerade kodexempel i .NET, Java och Python med företagsmönster
- **Resursorganisation**: Omfattande kategorisering av officiell dokumentation, säkerhetsstandarder och implementeringsguider
- **Visuella indikatorer**: Tydlig markering av obligatoriska krav kontra rekommenderade metoder

#### Grundläggande koncept (01-CoreConcepts/) - Komplett modernisering
- **Protokollversionsuppdatering**: Uppdaterad för att referera till nuvarande MCP-specifikation 2025-06-18 med datum-baserad versionering (format YYYY-MM-DD)
- **Arkitekturförfining**: Förbättrade beskrivningar av värdar, klienter och servrar för att återspegla aktuella MCP-arkitekturmodeller
  - Värdar definieras nu tydligt som AI-applikationer som koordinerar flera MCP-klientanslutningar
  - Klienter beskrivs som protokollanslutningar som upprätthåller en-till-en relationer med servrar
  - Servrar förbättrade med lokala kontra fjärrdistributionsscenarier
- **Omstrukturering av primitiva element**: Fullständig översyn av server- och klientprimitiver
  - Serverprimitiver: Resurser (datakällor), Prompter (mallar), Verktyg (exekverbara funktioner) med detaljerade förklaringar och exempel
  - Klientprimitiver: Sampling (LLM-slutföranden), Elicitation (användarinmatning), Loggning (felsökning/övervakning)
  - Uppdaterad med aktuella upptäckts- (`*/list`), hämtnings- (`*/get`) och exekverings- (`*/call`) metodmönster
- **Protokollarkitektur**: Introducerade tvålagers arkitekturmodell
  - Dataskikt: JSON-RPC 2.0-grund med livscykelhantering och primitiva element
  - Transportskikt: STDIO (lokalt) och Streamable HTTP med SSE (fjärr) transportmekanismer
- **Säkerhetsramverk**: Omfattande säkerhetsprinciper inklusive explicit användarsamtycke, dataskydd, verktygssäkerhet och transportskiktssäkerhet
- **Kommunikationsmönster**: Uppdaterade protokollmeddelanden för att visa initiering, upptäckt, exekvering och notifieringsflöden
- **Kodexempel**: Uppdaterade flerspråkiga exempel (.NET, Java, Python, JavaScript) för att återspegla aktuella MCP SDK-mönster

#### Säkerhet (02-Security/) - Omfattande säkerhetsöversyn  
- **Standardanpassning**: Fullständig anpassning till MCP-specifikation 2025-06-18 säkerhetskrav
- **Utveckling av autentisering**: Dokumenterad utveckling från anpassade OAuth-servrar till delegering av externa identitetsleverantörer (Microsoft Entra ID)
- **AI-specifik hotanalys**: Förbättrad täckning av moderna AI-attackvektorer
  - Detaljerade scenarier för promptinjektionsattacker med verkliga exempel
  - Mekanismer för verktygsförgiftning och "rug pull"-attackmönster
  - Förgiftning av kontextfönster och modellförvirringsattacker
- **Microsoft AI-säkerhetslösningar**: Omfattande täckning av Microsofts säkerhetsekosystem
  - AI Prompt Shields med avancerad detektering, spotlighting och avgränsningstekniker
  - Integrationsmönster för Azure Content Safety
  - GitHub Advanced Security för skydd av leverantörskedjan
- **Avancerad hotreducering**: Detaljerade säkerhetskontroller för
  - Sessionkapning med MCP-specifika attackscenarier och krav på kryptografiska sessions-ID
  - Förvirrade ställföreträdarproblem i MCP-proxy-scenarier med explicita samtyckeskrav
  - Tokenöverföringssvagheter med obligatoriska valideringskontroller
- **Leverantörskedjesäkerhet**: Utökad täckning av AI-leverantörskedjan inklusive grundmodeller, embeddings-tjänster, kontextleverantörer och tredjeparts-API:er
- **Grundläggande säkerhet**: Förbättrad integration med företagsäkerhetsmönster inklusive zero trust-arkitektur och Microsofts säkerhetsekosystem
- **Resursorganisation**: Kategoriserade omfattande resurslänkar efter typ (Officiella dokument, standarder, forskning, Microsoft-lösningar, implementeringsguider)

### Förbättringar av dokumentationskvalitet
- **Strukturerade lärandemål**: Förbättrade lärandemål med specifika, handlingsbara resultat
- **Korsreferenser**: Lade till länkar mellan relaterade säkerhets- och grundläggande konceptämnen
- **Aktuell information**: Uppdaterade alla datumreferenser och specifikationslänkar till aktuella standarder
- **Implementeringsvägledning**: Lade till specifika, handlingsbara implementeringsriktlinjer genom båda sektionerna

## 16 juli 2025

### Förbättringar av README och navigering
- Fullständigt omdesignad navigering i README.md
- Ersatte `<details>`-taggar med mer tillgängligt tabellbaserat format
- Skapade alternativa layoutalternativ i den nya mappen "alternative_layouts"
- Lade till exempel på kortbaserad, flikbaserad och dragspelsbaserad navigering
- Uppdaterade avsnittet om mappstruktur för att inkludera alla senaste filer
- Förbättrade avsnittet "Hur man använder denna läroplan" med tydliga rekommendationer
- Uppdaterade MCP-specifikationslänkar för att peka på korrekta URL:er
- Lade till avsnittet Context Engineering (5.14) i läroplansstrukturen

### Uppdateringar av studieguiden
- Fullständigt reviderad studieguiden för att anpassas till aktuell mappstruktur
- Lade till nya sektioner för MCP-klienter och verktyg, samt populära MCP-servrar
- Uppdaterade den visuella läroplansöversikten för att korrekt återspegla alla ämnen
- Förbättrade beskrivningar av avancerade ämnen för att täcka alla specialiserade områden
- Uppdaterade avsnittet Fallstudier för att återspegla faktiska exempel
- Lade till denna omfattande ändringslogg

### Community Contributions (06-CommunityContributions/)
- Lade till detaljerad information om MCP-servrar för bildgenerering
- Lade till omfattande avsnitt om att använda Claude i VSCode
- Lade till instruktioner för att ställa in och använda Cline terminalklient
- Uppdaterade MCP-klientsektionen för att inkludera alla populära klientalternativ
- Förbättrade bidragsexempel med mer exakta kodexempel

### Avancerade ämnen (05-AdvancedTopics/)
- Organiserade alla specialiserade ämnesmappar med konsekvent namngivning
- Lade till material och exempel för kontextteknik
- Lade till dokumentation för Foundry-agentintegration
- Förbättrade dokumentationen för Entra ID-säkerhetsintegration

## 11 juni 2025

### Initial skapelse
- Släppte första versionen av MCP för nybörjare-läroplanen
- Skapade grundläggande struktur för alla 10 huvudsektioner
- Implementerade visuell läroplansöversikt för navigering
- Lade till initiala exempelprojekt i flera programmeringsspråk

### Komma igång (03-GettingStarted/)
- Skapade första serverimplementeringsexempel
- Lade till vägledning för klientutveckling
- Inkluderade instruktioner för LLM-klientintegration
- Lade till dokumentation för VS Code-integration
- Implementerade exempel på Server-Sent Events (SSE)-servrar

### Grundläggande koncept (01-CoreConcepts/)
- Lade till detaljerad förklaring av klient-server-arkitektur
- Skapade dokumentation om nyckelprotokollkomponenter
- Dokumenterade meddelandemönster i MCP

## 23 maj 2025

### Mappstruktur
- Initierade mappen med grundläggande struktur
- Skapade README-filer för varje större sektion
- Ställde in översättningsinfrastruktur
- Lade till bildresurser och diagram

### Dokumentation
- Skapade initial README.md med läroplansöversikt
- Lade till CODE_OF_CONDUCT.md och SECURITY.md
- Ställde in SUPPORT.md med vägledning för att få hjälp
- Skapade preliminär struktur för studieguiden

## 15 april 2025

### Planering och ramverk
- Initial planering för MCP för nybörjare-läroplanen
- Definierade lärandemål och målgrupp
- Skisserade 10-sektionsstruktur för läroplanen
- Utvecklade konceptuellt ramverk för exempel och fallstudier
- Skapade initiala prototypexempel för nyckelkoncept

---

**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, bör det noteras att automatiserade översättningar kan innehålla fel eller felaktigheter. Det ursprungliga dokumentet på dess originalspråk bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för eventuella missförstånd eller feltolkningar som uppstår vid användning av denna översättning.