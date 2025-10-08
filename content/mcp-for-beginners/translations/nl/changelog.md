<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:25:56+00:00",
  "source_file": "changelog.md",
  "language_code": "nl"
}
-->
# Changelog: MCP voor Beginners Curriculum

Dit document dient als een overzicht van alle belangrijke wijzigingen die zijn aangebracht in het Model Context Protocol (MCP) voor Beginners curriculum. Wijzigingen worden gedocumenteerd in omgekeerde chronologische volgorde (nieuwste wijzigingen eerst).

## 6 oktober 2025

### Uitbreiding van de sectie Aan de slag – Geavanceerd servergebruik & eenvoudige authenticatie

#### Geavanceerd servergebruik (03-GettingStarted/10-advanced)
- **Nieuw hoofdstuk toegevoegd**: Een uitgebreide gids geïntroduceerd voor geavanceerd MCP-servergebruik, met zowel reguliere als low-level serverarchitecturen.
  - **Regulier vs. Low-Level Server**: Gedetailleerde vergelijking en codevoorbeelden in Python en TypeScript voor beide benaderingen.
  - **Handler-gebaseerd ontwerp**: Uitleg over handler-gebaseerd beheer van tools/resources/prompts voor schaalbare, flexibele serverimplementaties.
  - **Praktische patronen**: Realistische scenario's waarin low-level serverpatronen voordelig zijn voor geavanceerde functies en architectuur.

#### Eenvoudige authenticatie (03-GettingStarted/11-simple-auth)
- **Nieuw hoofdstuk toegevoegd**: Stapsgewijze gids voor het implementeren van eenvoudige authenticatie in MCP-servers.
  - **Authenticatieconcepten**: Duidelijke uitleg over authenticatie versus autorisatie en het omgaan met inloggegevens.
  - **Implementatie van Basic Auth**: Middleware-gebaseerde authenticatiepatronen in Python (Starlette) en TypeScript (Express), met codevoorbeelden.
  - **Overgang naar geavanceerde beveiliging**: Richtlijnen om te beginnen met eenvoudige authenticatie en door te groeien naar OAuth 2.1 en RBAC, met verwijzingen naar geavanceerde beveiligingsmodules.

Deze toevoegingen bieden praktische, hands-on begeleiding voor het bouwen van robuustere, veiligere en flexibelere MCP-serverimplementaties, waarbij fundamentele concepten worden verbonden met geavanceerde productiepatronen.

## 29 september 2025

### MCP Server Database Integratie Labs - Uitgebreid hands-on leerpad

#### 11-MCPServerHandsOnLabs - Nieuw compleet database-integratiecurriculum
- **Compleet 13-labs leerpad**: Toegevoegd uitgebreid hands-on curriculum voor het bouwen van productieklare MCP-servers met PostgreSQL-database-integratie.
  - **Implementatie in de praktijk**: Zava Retail analytics use case die enterprise-grade patronen demonstreert.
  - **Gestructureerde leerprogressie**:
    - **Labs 00-03: Basisprincipes** - Introductie, kernarchitectuur, beveiliging & multi-tenancy, omgevingsinstelling.
    - **Labs 04-06: Het bouwen van de MCP-server** - Databaseontwerp & schema, MCP-serverimplementatie, toolontwikkeling.
    - **Labs 07-09: Geavanceerde functies** - Integratie van semantisch zoeken, testen & debuggen, VS Code-integratie.
    - **Labs 10-12: Productie & best practices** - Implementatiestrategieën, monitoring & observatie, best practices & optimalisatie.
  - **Enterprise-technologieën**: FastMCP-framework, PostgreSQL met pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Geavanceerde functies**: Row Level Security (RLS), semantisch zoeken, multi-tenant data toegang, vector embeddings, realtime monitoring.

#### Terminologie standaardisatie - Conversie van module naar lab
- **Uitgebreide documentatie-update**: Systematisch alle README-bestanden in 11-MCPServerHandsOnLabs bijgewerkt om "Lab"-terminologie te gebruiken in plaats van "Module".
  - **Sectiekoppen**: "Wat deze module behandelt" gewijzigd naar "Wat dit lab behandelt" in alle 13 labs.
  - **Inhoudsbeschrijving**: "Deze module biedt..." veranderd naar "Dit lab biedt..." in de documentatie.
  - **Leerdoelen**: "Aan het einde van deze module..." gewijzigd naar "Aan het einde van dit lab...".
  - **Navigatielinks**: Alle verwijzingen naar "Module XX:" geconverteerd naar "Lab XX:" in kruisverwijzingen en navigatie.
  - **Volgstatus**: "Na het voltooien van deze module..." gewijzigd naar "Na het voltooien van dit lab...".
  - **Technische referenties behouden**: Python module-referenties in configuratiebestanden behouden (bijv. `"module": "mcp_server.main"`).

#### Verbetering van studiegids (study_guide.md)
- **Visuele curriculumkaart**: Nieuwe sectie "11. Database Integratie Labs" toegevoegd met uitgebreide labstructuurvisualisatie.
- **Repositorystructuur**: Bijgewerkt van tien naar elf hoofdsecties met gedetailleerde beschrijving van 11-MCPServerHandsOnLabs.
- **Leerpadrichtlijnen**: Verbeterde navigatie-instructies om secties 00-11 te dekken.
- **Technologieoverzicht**: Toegevoegd details over FastMCP, PostgreSQL, Azure-services integratie.
- **Leerresultaten**: Nadruk gelegd op productieklare serverontwikkeling, database-integratiepatronen en enterprise-beveiliging.

#### Hoofd README-structuur verbetering
- **Lab-gebaseerde terminologie**: Hoofd README.md in 11-MCPServerHandsOnLabs bijgewerkt om consequent "Lab"-structuur te gebruiken.
- **Leerpadorganisatie**: Duidelijke progressie van fundamentele concepten naar geavanceerde implementatie tot productie-implementatie.
- **Praktijkgericht**: Nadruk op praktische, hands-on leren met enterprise-grade patronen en technologieën.

### Verbeteringen in documentatiekwaliteit & consistentie
- **Hands-on leren benadrukt**: Praktische, lab-gebaseerde aanpak versterkt in de documentatie.
- **Focus op enterprise-patronen**: Productieklare implementaties en enterprise-beveiliging benadrukt.
- **Technologie-integratie**: Uitgebreide dekking van moderne Azure-services en AI-integratiepatronen.
- **Leerprogressie**: Duidelijk, gestructureerd pad van basisconcepten naar productie-implementatie.

## 26 september 2025

### Verbetering van casestudies - GitHub MCP Registry-integratie

#### Casestudies (09-CaseStudy/) - Focus op ecosysteemontwikkeling
- **README.md**: Grote uitbreiding met uitgebreide GitHub MCP Registry casestudy.
  - **GitHub MCP Registry casestudy**: Nieuwe uitgebreide casestudy over de lancering van GitHub's MCP Registry in september 2025.
    - **Probleemanalyse**: Gedetailleerd onderzoek naar gefragmenteerde MCP-serverontdekking en implementatie-uitdagingen.
    - **Oplossingsarchitectuur**: GitHub's gecentraliseerde registry-benadering met één-klik VS Code-installatie.
    - **Zakelijke impact**: Meetbare verbeteringen in ontwikkelaar onboarding en productiviteit.
    - **Strategische waarde**: Focus op modulaire agentimplementatie en cross-tool interoperabiliteit.
    - **Ecosysteemontwikkeling**: Positionering als fundamenteel platform voor agentische integratie.
  - **Verbeterde structuur van casestudies**: Alle zeven casestudies bijgewerkt met consistente opmaak en uitgebreide beschrijvingen.
    - Azure AI Travel Agents: Nadruk op multi-agent orkestratie.
    - Azure DevOps-integratie: Focus op workflowautomatisering.
    - Realtime documentatie-ophaling: Python console client-implementatie.
    - Interactieve studieplangenerator: Chainlit conversatie-webapp.
    - In-editor documentatie: VS Code en GitHub Copilot-integratie.
    - Azure API Management: Enterprise API-integratiepatronen.
    - GitHub MCP Registry: Ecosysteemontwikkeling en communityplatform.
  - **Uitgebreide conclusie**: Conclusiesectie herschreven met nadruk op zeven casestudies die meerdere MCP-implementatiedimensies bestrijken.
    - Categorisatie: Enterprise-integratie, multi-agent orkestratie, ontwikkelaarsproductiviteit.
    - Inzichten: Architecturale patronen, implementatiestrategieën en best practices.
    - Nadruk op MCP als volwassen, productieklare protocol.

#### Updates in studiegids (study_guide.md)
- **Visuele curriculumkaart**: Mindmap bijgewerkt om GitHub MCP Registry op te nemen in de sectie Casestudies.
- **Beschrijving van casestudies**: Verbeterd van generieke beschrijvingen naar gedetailleerde uiteenzetting van zeven uitgebreide casestudies.
- **Repositorystructuur**: Sectie 10 bijgewerkt om uitgebreide dekking van casestudies te weerspiegelen met specifieke implementatiedetails.
- **Changelog-integratie**: Toegevoegd 26 september 2025 vermelding die GitHub MCP Registry toevoeging en verbeteringen in casestudies documenteert.
- **Datumupdates**: Voettekst bijgewerkt om de laatste revisie (26 september 2025) weer te geven.

### Verbeteringen in documentatiekwaliteit
- **Consistentieverbetering**: Casestudy-opmaak en structuur gestandaardiseerd over alle zeven voorbeelden.
- **Uitgebreide dekking**: Casestudies bestrijken nu enterprise-, ontwikkelaarsproductiviteit- en ecosysteemontwikkelingsscenario's.
- **Strategische positionering**: Versterkte focus op MCP als fundamenteel platform voor agentische systeemimplementatie.
- **Resource-integratie**: Extra bronnen bijgewerkt om GitHub MCP Registry-link op te nemen.

## 15 september 2025

### Uitbreiding van geavanceerde onderwerpen - Aangepaste transports & context engineering

#### MCP Custom Transports (05-AdvancedTopics/mcp-transport/) - Nieuwe geavanceerde implementatiegids
- **README.md**: Complete implementatiegids voor aangepaste MCP-transportmechanismen.
  - **Azure Event Grid Transport**: Uitgebreide serverloze event-driven transportimplementatie.
    - Voorbeelden in C#, TypeScript en Python met Azure Functions-integratie.
    - Event-driven architectuurpatronen voor schaalbare MCP-oplossingen.
    - Webhook-ontvangers en push-gebaseerde berichtafhandeling.
  - **Azure Event Hubs Transport**: High-throughput streaming transportimplementatie.
    - Realtime streamingmogelijkheden voor low-latency scenario's.
    - Partitioneringsstrategieën en checkpointbeheer.
    - Berichtbatching en prestatieoptimalisatie.
  - **Enterprise-integratiepatronen**: Productieklare architecturale voorbeelden.
    - Gedistribueerde MCP-verwerking over meerdere Azure Functions.
    - Hybride transportarchitecturen die meerdere transporttypen combineren.
    - Berichtduurzaamheid, betrouwbaarheid en foutafhandelingsstrategieën.
  - **Beveiliging & monitoring**: Azure Key Vault-integratie en observatiepatronen.
    - Managed identity authenticatie en toegang met minimaal privilege.
    - Application Insights telemetrie en prestatiemonitoring.
    - Circuit breakers en fouttolerantiepatronen.
  - **Testframeworks**: Uitgebreide teststrategieën voor aangepaste transports.
    - Unit testing met test doubles en mocking frameworks.
    - Integratietesten met Azure Test Containers.
    - Prestatie- en belastingtestoverwegingen.

#### Context Engineering (05-AdvancedTopics/mcp-contextengineering/) - Opkomende AI-discipline
- **README.md**: Uitgebreide verkenning van context engineering als opkomend vakgebied.
  - **Kernprincipes**: Volledige contextdeling, bewustzijn van actiebeslissingen en contextvensterbeheer.
  - **MCP Protocol Alignment**: Hoe MCP-ontwerp context engineering-uitdagingen aanpakt.
    - Beperkingen van contextvensters en progressieve laadstrategieën.
    - Relevantiebepaling en dynamische contextophaling.
    - Multi-modale contextverwerking en beveiligingsoverwegingen.
  - **Implementatiebenaderingen**: Single-threaded vs. multi-agent architecturen.
    - Context chunking en prioriteringstechnieken.
    - Progressieve contextladen en compressiestrategieën.
    - Gelaagde contextbenaderingen en optimalisatie van ophaling.
  - **Meetkader**: Opkomende metrics voor evaluatie van contexteffectiviteit.
    - Inputefficiëntie, prestaties, kwaliteit en gebruikerservaringsoverwegingen.
    - Experimentele benaderingen voor contextoptimalisatie.
    - Foutanalyse en verbeteringsmethodologieën.

#### Updates in curriculum navigatie (README.md)
- **Verbeterde modulestructuur**: Curriculumtabel bijgewerkt om nieuwe geavanceerde onderwerpen op te nemen.
  - Toegevoegd Context Engineering (5.14) en Custom Transport (5.15) vermeldingen.
  - Consistente opmaak en navigatielinks in alle modules.
  - Beschrijvingen bijgewerkt om huidige inhoudsscope te weerspiegelen.

### Verbeteringen in directorystructuur
- **Naamgeving standaardisatie**: "mcp transport" hernoemd naar "mcp-transport" voor consistentie met andere geavanceerde onderwerpfolders.
- **Inhoudsorganisatie**: Alle 05-AdvancedTopics folders volgen nu een consistent naamgevingspatroon (mcp-[onderwerp]).

### Verbeteringen in documentatiekwaliteit
- **MCP-specificatie afstemming**: Alle nieuwe inhoud verwijst naar huidige MCP-specificatie 2025-06-18.
- **Meertalige voorbeelden**: Uitgebreide codevoorbeelden in C#, TypeScript en Python.
- **Enterprise-focus**: Productieklare patronen en Azure-cloudintegratie door de hele documentatie.
- **Visuele documentatie**: Mermaid-diagrammen voor architectuur en stroomvisualisatie.

## 18 augustus 2025

### Uitgebreide documentatie-update - MCP 2025-06-18 standaarden

#### MCP Beveiligingsbest Practices (02-Security/) - Volledige modernisering
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Volledige herschrijving afgestemd op MCP-specificatie 2025-06-18.
  - **Verplichte vereisten**: Toegevoegd expliciete MOET/MAG NIET vereisten uit officiële specificatie met duidelijke visuele indicatoren.
  - **12 kernbeveiligingspraktijken**: Herstructureerd van 15-item lijst naar uitgebreide beveiligingsdomeinen.
    - Tokenbeveiliging & authenticatie met externe identiteitsproviderintegratie.
    - Sessiebeheer & transportbeveiliging met cryptografische vereisten.
    - AI-specifieke dreigingsbescherming met Microsoft Prompt Shields-integratie.
    - Toegangscontrole & machtigingen met principe van minimaal privilege.
    - Inhoudsveiligheid & monitoring met Azure Content Safety-integratie.
    - Beveiliging van de toeleveringsketen met uitgebreide componentverificatie.
    - OAuth-beveiliging & verwarring van deputy-preventie met PKCE-implementatie.
    - Incidentrespons & herstel met geautomatiseerde mogelijkheden.
    - Naleving & governance met regelgevingsafstemming.
    - Geavanceerde beveiligingscontroles met zero trust architectuur.
    - Microsoft beveiligingsecosysteemintegratie met uitgebreide oplossingen.
    - Continue beveiligingsevolutie met adaptieve praktijken.
  - **Microsoft beveiligingsoplossingen**: Verbeterde integratierichtlijnen voor Prompt Shields, Azure Content Safety, Entra ID en GitHub Advanced Security.
  - **Implementatiebronnen**: Gecategoriseerde uitgebreide resource-links per officiële MCP-documentatie, Microsoft beveiligingsoplossingen, beveiligingsstandaarden en implementatiegidsen.

#### Geavanceerde beveiligingscontroles (02-Security/) - Enterprise-implementatie
- **MCP-SECURITY-CONTROLS-2025.md**: Volledige revisie met enterprise-grade beveiligingsframework.
  - **9 uitgebreide beveiligingsdomeinen**: Uitgebreid van basiscontroles naar gedetailleerd enterprise-framework.
    - Geavanceerde authenticatie & autorisatie met Microsoft Entra ID-integratie.
    - Tokenbeveiliging & anti-passthrough controles met uitgebreide validatie.
    - Sessiebeveiligingscontroles met kapingpreventie.
    - AI-specifieke beveiligingscontroles met promptinjectie en toolvergiftigingpreventie.
    - Preventie van verwarring van deputy-aanvallen met OAuth proxy beveiliging.
    - Tooluitvoeringsbeveiliging met sandboxing en isolatie.
    - Beveiligingscontroles van de toeleveringsketen met afhankelijkheidsverificatie.
    - Monitoring & detectiecontroles met SIEM-integratie.
    - Incidentrespons & herstel met geautomatiseerde mogelijkheden.
  - **Implementatievoorbeelden**: Gedetailleerde YAML-configuratieblokken en codevoorbeelden toegevoegd.
  - **Microsoft oplossingenintegratie**: Uitgebreide dekking van Azure beveiligingsdiensten, GitHub Advanced Security en enterprise-identiteitsbeheer.
#### Geavanceerde Onderwerpen Beveiliging (05-AdvancedTopics/mcp-security/) - Productieklaar Implementatie
- **README.md**: Volledige herschrijving voor implementatie van beveiliging op ondernemingsniveau
  - **Huidige Specificatie Afstemming**: Bijgewerkt naar MCP Specificatie 2025-06-18 met verplichte beveiligingseisen
  - **Verbeterde Authenticatie**: Integratie van Microsoft Entra ID met uitgebreide voorbeelden in .NET en Java Spring Security
  - **AI Beveiligingsintegratie**: Implementatie van Microsoft Prompt Shields en Azure Content Safety met gedetailleerde Python-voorbeelden
  - **Geavanceerde Dreigingsbeperking**: Uitgebreide implementatievoorbeelden voor:
    - Preventie van Confused Deputy-aanvallen met PKCE en validatie van gebruikersconsent
    - Preventie van Token Passthrough met validatie van publiek en veilig tokenbeheer
    - Preventie van sessiekaping met cryptografische binding en gedragsanalyse
  - **Beveiligingsintegratie op ondernemingsniveau**: Monitoring met Azure Application Insights, dreigingsdetectie-pipelines en beveiliging van de toeleveringsketen
  - **Implementatiechecklist**: Duidelijke verplichte versus aanbevolen beveiligingscontroles met voordelen van het Microsoft-beveiligingsecosysteem

### Documentatiekwaliteit & Standaardafstemming
- **Specificatiereferenties**: Alle referenties bijgewerkt naar de huidige MCP Specificatie 2025-06-18
- **Microsoft Beveiligingsecosysteem**: Verbeterde integratierichtlijnen door alle beveiligingsdocumentatie heen
- **Praktische Implementatie**: Gedetailleerde codevoorbeelden toegevoegd in .NET, Java en Python met ondernemingspatronen
- **Resourceorganisatie**: Uitgebreide categorisatie van officiële documentatie, beveiligingsstandaarden en implementatiegidsen
- **Visuele Indicatoren**: Duidelijke markering van verplichte eisen versus aanbevolen praktijken

#### Kernconcepten (01-CoreConcepts/) - Volledige Modernisering
- **Protocolversie-update**: Bijgewerkt naar de huidige MCP Specificatie 2025-06-18 met datumgebaseerde versie-indeling (YYYY-MM-DD formaat)
- **Architectuurverbetering**: Verbeterde beschrijvingen van Hosts, Clients en Servers om huidige MCP-architectuurpatronen te weerspiegelen
  - Hosts nu duidelijk gedefinieerd als AI-toepassingen die meerdere MCP-clientverbindingen coördineren
  - Clients beschreven als protocolconnectors die één-op-één serverrelaties onderhouden
  - Servers verbeterd met lokale versus externe implementatiescenario's
- **Herstructurering van Primitieven**: Volledige revisie van server- en clientprimitieven
  - Serverprimitieven: Resources (gegevensbronnen), Prompts (sjablonen), Tools (uitvoerbare functies) met gedetailleerde uitleg en voorbeelden
  - Clientprimitieven: Sampling (LLM-voltooiingen), Elicitation (gebruikersinput), Logging (debugging/monitoring)
  - Bijgewerkt met huidige ontdekking (`*/list`), ophalen (`*/get`) en uitvoeringsmethoden (`*/call`) patronen
- **Protocolarchitectuur**: Twee-laags architectuurmodel geïntroduceerd
  - Gegevenslaag: JSON-RPC 2.0 basis met levenscyclusbeheer en primitieven
  - Transportlaag: STDIO (lokaal) en Streamable HTTP met SSE (extern) transportmechanismen
- **Beveiligingskader**: Uitgebreide beveiligingsprincipes inclusief expliciete gebruikersconsent, gegevensprivacybescherming, veiligheid van tooluitvoering en transportlaagbeveiliging
- **Communicatiepatronen**: Protocolberichten bijgewerkt om initialisatie, ontdekking, uitvoering en notificatiestromen te tonen
- **Codevoorbeelden**: Meertalige voorbeelden (.NET, Java, Python, JavaScript) vernieuwd om huidige MCP SDK-patronen te weerspiegelen

#### Beveiliging (02-Security/) - Uitgebreide Beveiligingsrevisie  
- **Standaardafstemming**: Volledige afstemming met MCP Specificatie 2025-06-18 beveiligingseisen
- **Evolutie van Authenticatie**: Documentatie van evolutie van aangepaste OAuth-servers naar delegatie van externe identiteitsproviders (Microsoft Entra ID)
- **AI-specifieke dreigingsanalyse**: Verbeterde dekking van moderne AI-aanvalsvectoren
  - Gedetailleerde scenario's van promptinjectie-aanvallen met praktijkvoorbeelden
  - Mechanismen voor toolvergiftiging en "rug pull"-aanvalspatronen
  - Vergiftiging van contextvensters en verwarringsaanvallen op modellen
- **Microsoft AI Beveiligingsoplossingen**: Uitgebreide dekking van het Microsoft-beveiligingsecosysteem
  - AI Prompt Shields met geavanceerde detectie, spotlighting en scheidingstechnieken
  - Integratiepatronen voor Azure Content Safety
  - GitHub Advanced Security voor bescherming van de toeleveringsketen
- **Geavanceerde Dreigingsbeperking**: Gedetailleerde beveiligingscontroles voor:
  - Sessiekaping met MCP-specifieke aanvalsscenario's en cryptografische sessie-ID vereisten
  - Confused deputy-problemen in MCP-proxyscenario's met expliciete consentvereisten
  - Token passthrough kwetsbaarheden met verplichte validatiecontroles
- **Beveiliging van de Toeleveringsketen**: Uitgebreide dekking van AI-toeleveringsketen inclusief funderingsmodellen, embedding-services, contextproviders en externe API's
- **Fundamentele Beveiliging**: Verbeterde integratie met beveiligingspatronen op ondernemingsniveau, inclusief zero trust-architectuur en Microsoft-beveiligingsecosysteem
- **Resourceorganisatie**: Uitgebreide categorisatie van bronnenlinks per type (Officiële Documentatie, Standaarden, Onderzoek, Microsoft-oplossingen, Implementatiegidsen)

### Verbeteringen in Documentatiekwaliteit
- **Gestructureerde Leerdoelen**: Verbeterde leerdoelen met specifieke, uitvoerbare resultaten
- **Kruisverwijzingen**: Links toegevoegd tussen gerelateerde beveiligings- en kernconceptonderwerpen
- **Actuele Informatie**: Alle datums en specificatielinks bijgewerkt naar huidige standaarden
- **Implementatierichtlijnen**: Specifieke, uitvoerbare implementatierichtlijnen toegevoegd door beide secties heen

## 16 juli 2025

### README en Navigatieverbeteringen
- Curriculum-navigatie in README.md volledig opnieuw ontworpen
- `<details>`-tags vervangen door een toegankelijker tabelgebaseerd formaat
- Alternatieve lay-outopties gemaakt in de nieuwe map "alternative_layouts"
- Voorbeelden van kaartgebaseerde, tabbladstijl en accordeonstijl navigatie toegevoegd
- Sectie over repositorystructuur bijgewerkt om alle nieuwste bestanden op te nemen
- Sectie "Hoe gebruik je dit curriculum" verbeterd met duidelijke aanbevelingen
- MCP-specificatielinks bijgewerkt naar de juiste URL's
- Sectie Context Engineering (5.14) toegevoegd aan de curriculumstructuur

### Studiegidsupdates
- Studiegids volledig herzien om af te stemmen op de huidige repositorystructuur
- Nieuwe secties toegevoegd voor MCP Clients en Tools, en Populaire MCP Servers
- Visuele Curriculumkaart bijgewerkt om alle onderwerpen nauwkeurig weer te geven
- Beschrijvingen van Geavanceerde Onderwerpen verbeterd om alle gespecialiseerde gebieden te dekken
- Sectie Case Studies bijgewerkt om werkelijke voorbeelden te weerspiegelen
- Deze uitgebreide changelog toegevoegd

### Communitybijdragen (06-CommunityContributions/)
- Gedetailleerde informatie toegevoegd over MCP-servers voor beeldgeneratie
- Uitgebreide sectie toegevoegd over het gebruik van Claude in VSCode
- Instructies voor het instellen en gebruiken van de Cline terminalclient toegevoegd
- Sectie MCP-client bijgewerkt om alle populaire clientopties op te nemen
- Bijdragevoorbeelden verbeterd met nauwkeurigere codevoorbeelden

### Geavanceerde Onderwerpen (05-AdvancedTopics/)
- Alle gespecialiseerde onderwerpmappen georganiseerd met consistente naamgeving
- Materialen en voorbeelden voor context engineering toegevoegd
- Documentatie voor Foundry-agentintegratie toegevoegd
- Documentatie voor Entra ID-beveiligingsintegratie verbeterd

## 11 juni 2025

### Eerste Creatie
- Eerste versie van het MCP voor Beginners-curriculum uitgebracht
- Basisstructuur gecreëerd voor alle 10 hoofdsecties
- Visuele Curriculumkaart geïmplementeerd voor navigatie
- Eerste voorbeeldprojecten toegevoegd in meerdere programmeertalen

### Aan de Slag (03-GettingStarted/)
- Eerste serverimplementatievoorbeelden gecreëerd
- Richtlijnen voor clientontwikkeling toegevoegd
- Instructies voor LLM-clientintegratie opgenomen
- Documentatie voor VS Code-integratie toegevoegd
- Servervoorbeelden met Server-Sent Events (SSE) geïmplementeerd

### Kernconcepten (01-CoreConcepts/)
- Gedetailleerde uitleg toegevoegd over client-serverarchitectuur
- Documentatie gecreëerd over belangrijke protocolcomponenten
- Berichtenpatronen in MCP gedocumenteerd

## 23 mei 2025

### Repositorystructuur
- Repository geïnitialiseerd met basismapstructuur
- README-bestanden gecreëerd voor elke hoofdsectie
- Vertaalinfrastructuur opgezet
- Afbeeldingsassets en diagrammen toegevoegd

### Documentatie
- Eerste README.md gecreëerd met curriculumoverzicht
- CODE_OF_CONDUCT.md en SECURITY.md toegevoegd
- SUPPORT.md opgezet met richtlijnen voor hulp
- Voorlopige structuur van studiegids gecreëerd

## 15 april 2025

### Planning en Framework
- Eerste planning voor MCP voor Beginners-curriculum
- Leerdoelen en doelgroep gedefinieerd
- 10-sectie structuur van het curriculum geschetst
- Conceptueel framework ontwikkeld voor voorbeelden en casestudies
- Eerste prototypevoorbeelden gecreëerd voor kernconcepten

---

**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.