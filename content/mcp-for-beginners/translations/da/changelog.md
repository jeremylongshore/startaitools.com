<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:16:54+00:00",
  "source_file": "changelog.md",
  "language_code": "da"
}
-->
# Ændringslog: MCP for Begyndere Curriculum

Dette dokument fungerer som en oversigt over alle væsentlige ændringer, der er foretaget i Model Context Protocol (MCP) for Begyndere curriculum. Ændringer er dokumenteret i omvendt kronologisk rækkefølge (nyeste ændringer først).

## 6. oktober 2025

### Udvidelse af Introduktionssektionen – Avanceret Serverbrug & Enkel Autentifikation

#### Avanceret Serverbrug (03-GettingStarted/10-advanced)
- **Nyt Kapitel Tilføjet**: Introduceret en omfattende guide til avanceret MCP-serverbrug, der dækker både almindelige og lav-niveau serverarkitekturer.
  - **Almindelig vs. Lav-Niveau Server**: Detaljeret sammenligning og kodeeksempler i Python og TypeScript for begge tilgange.
  - **Handler-Baseret Design**: Forklaring af handler-baseret værktøjs-/ressource-/promptstyring for skalerbare og fleksible serverimplementeringer.
  - **Praktiske Mønstre**: Virkelige scenarier, hvor lav-niveau servermønstre er fordelagtige for avancerede funktioner og arkitektur.

#### Enkel Autentifikation (03-GettingStarted/11-simple-auth)
- **Nyt Kapitel Tilføjet**: Trin-for-trin guide til implementering af enkel autentifikation i MCP-servere.
  - **Autentifikationskoncepter**: Klar forklaring af forskellen mellem autentifikation og autorisation samt håndtering af legitimationsoplysninger.
  - **Grundlæggende Autentifikationsimplementering**: Middleware-baserede autentifikationsmønstre i Python (Starlette) og TypeScript (Express) med kodeeksempler.
  - **Udvikling til Avanceret Sikkerhed**: Vejledning i at starte med enkel autentifikation og udvikle sig til OAuth 2.1 og RBAC med henvisninger til avancerede sikkerhedsmoduler.

Disse tilføjelser giver praktisk, hands-on vejledning til at bygge mere robuste, sikre og fleksible MCP-serverimplementeringer, der forbinder grundlæggende koncepter med avancerede produktionsmønstre.

## 29. september 2025

### MCP Server Database Integration Labs - Omfattende Hands-On Læringssti

#### 11-MCPServerHandsOnLabs - Ny Komplet Databaseintegrationscurriculum
- **Komplet 13-Labs Læringssti**: Tilføjet omfattende hands-on curriculum til opbygning af produktionsklare MCP-servere med PostgreSQL databaseintegration.
  - **Virkelighedsnær Implementering**: Zava Retail analytics use case, der demonstrerer mønstre i enterprise-klassen.
  - **Struktureret Læringsprogression**:
    - **Labs 00-03: Grundlag** - Introduktion, Kernearkitektur, Sikkerhed & Multi-Tenancy, Miljøopsætning.
    - **Labs 04-06: Opbygning af MCP Server** - Database Design & Schema, MCP Server Implementering, Værktøjsudvikling.
    - **Labs 07-09: Avancerede Funktioner** - Semantisk Søgeintegration, Test & Debugging, VS Code Integration.
    - **Labs 10-12: Produktion & Best Practices** - Implementeringsstrategier, Overvågning & Observabilitet, Best Practices & Optimering.
  - **Enterprise Teknologier**: FastMCP framework, PostgreSQL med pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Avancerede Funktioner**: Row Level Security (RLS), semantisk søgning, multi-tenant dataadgang, vektorembeddings, realtidsmonitorering.

#### Terminologistandardisering - Modul til Lab Konvertering
- **Omfattende Dokumentationsopdatering**: Systematisk opdateret alle README-filer i 11-MCPServerHandsOnLabs til at bruge "Lab"-terminologi i stedet for "Modul".
  - **Sektionoverskrifter**: Opdateret "What This Module Covers" til "What This Lab Covers" på tværs af alle 13 labs.
  - **Indholdsbeskrivelse**: Ændret "This module provides..." til "This lab provides..." i hele dokumentationen.
  - **Læringsmål**: Opdateret "By the end of this module..." til "By the end of this lab...".
  - **Navigationslinks**: Konverteret alle "Module XX:" referencer til "Lab XX:" i krydsreferencer og navigation.
  - **Afslutningssporing**: Opdateret "After completing this module..." til "After completing this lab...".
  - **Bevarede Tekniske Referencer**: Bibeholdt Python modulreferencer i konfigurationsfiler (f.eks., `"module": "mcp_server.main"`).

#### Studieguideforbedring (study_guide.md)
- **Visuel Curriculum Kort**: Tilføjet ny "11. Database Integration Labs" sektion med omfattende lab-struktur visualisering.
- **Repository Struktur**: Opdateret fra ti til elleve hovedsektioner med detaljeret beskrivelse af 11-MCPServerHandsOnLabs.
- **Læringssti Vejledning**: Forbedrede navigationsinstruktioner til at dække sektioner 00-11.
- **Teknologidækning**: Tilføjet FastMCP, PostgreSQL, Azure services integrationsdetaljer.
- **Læringsresultater**: Fremhævet produktionsklar serverudvikling, databaseintegrationsmønstre og enterprise-sikkerhed.

#### Hoved README Strukturforbedring
- **Lab-Baseret Terminologi**: Opdateret hoved README.md i 11-MCPServerHandsOnLabs til konsekvent at bruge "Lab"-struktur.
- **Læringssti Organisation**: Klar progression fra grundlæggende koncepter til avanceret implementering og produktionsimplementering.
- **Virkelighedsnær Fokus**: Fokus på praktisk, hands-on læring med mønstre og teknologier i enterprise-klassen.

### Dokumentationskvalitet & Konsistensforbedringer
- **Hands-On Læringsfokus**: Styrket praktisk, lab-baseret tilgang i hele dokumentationen.
- **Enterprise Mønstre Fokus**: Fremhævet produktionsklare implementeringer og enterprise-sikkerhedsovervejelser.
- **Teknologiintegration**: Omfattende dækning af moderne Azure services og AI integrationsmønstre.
- **Læringsprogression**: Klar, struktureret sti fra grundlæggende koncepter til produktionsimplementering.

## 26. september 2025

### Case Studies Forbedring - GitHub MCP Registry Integration

#### Case Studies (09-CaseStudy/) - Fokus på Økosystemudvikling
- **README.md**: Større udvidelse med omfattende GitHub MCP Registry case study.
  - **GitHub MCP Registry Case Study**: Ny omfattende case study, der undersøger GitHubs MCP Registry lancering i september 2025.
    - **Problemanalyse**: Detaljeret undersøgelse af fragmenterede MCP serveropdagelses- og implementeringsudfordringer.
    - **Løsningsarkitektur**: GitHubs centraliserede registry tilgang med ét-klik VS Code installation.
    - **Forretningspåvirkning**: Målbare forbedringer i udvikler onboarding og produktivitet.
    - **Strategisk Værdi**: Fokus på modulær agentimplementering og kryds-værktøjs interoperabilitet.
    - **Økosystemudvikling**: Positionering som fundamentalt platform for agentisk integration.
  - **Forbedret Case Study Struktur**: Opdateret alle syv case studies med konsekvent format og omfattende beskrivelser.
    - Azure AI Travel Agents: Fokus på multi-agent orkestrering.
    - Azure DevOps Integration: Workflow automatiseringsfokus.
    - Realtidsdokumentationshentning: Python konsolklient implementering.
    - Interaktiv Studieplan Generator: Chainlit samtale-webapp.
    - In-Editor Dokumentation: VS Code og GitHub Copilot integration.
    - Azure API Management: Enterprise API integrationsmønstre.
    - GitHub MCP Registry: Økosystemudvikling og community platform.
  - **Omfattende Konklusion**: Omskrevet konklusionssektion, der fremhæver syv case studies, der spænder over flere MCP implementeringsdimensioner.
    - Enterprise Integration, Multi-Agent Orkestrering, Udviklerproduktivitet.
    - Økosystemudvikling, Uddannelsesapplikationer kategorisering.
    - Forbedrede indsigter i arkitekturmønstre, implementeringsstrategier og best practices.
    - Fokus på MCP som moden, produktionsklar protokol.

#### Studieguideopdateringer (study_guide.md)
- **Visuel Curriculum Kort**: Opdateret mindmap til at inkludere GitHub MCP Registry i Case Studies sektionen.
- **Case Studies Beskrivelse**: Forbedret fra generiske beskrivelser til detaljeret opdeling af syv omfattende case studies.
- **Repository Struktur**: Opdateret sektion 10 til at afspejle omfattende case study dækning med specifikke implementeringsdetaljer.
- **Ændringslog Integration**: Tilføjet 26. september 2025 indgang, der dokumenterer GitHub MCP Registry tilføjelse og case study forbedringer.
- **Datoopdateringer**: Opdateret fodnote tidsstempel til at afspejle seneste revision (26. september 2025).

### Dokumentationskvalitetsforbedringer
- **Konsistensforbedring**: Standardiseret case study format og struktur på tværs af alle syv eksempler.
- **Omfattende Dækning**: Case studies spænder nu over enterprise, udviklerproduktivitet og økosystemudviklingsscenarier.
- **Strategisk Positionering**: Forbedret fokus på MCP som fundamentalt platform for agentiske systemimplementeringer.
- **Ressourceintegration**: Opdateret yderligere ressourcer til at inkludere GitHub MCP Registry link.

## 15. september 2025

### Udvidelse af Avancerede Emner - Custom Transports & Context Engineering

#### MCP Custom Transports (05-AdvancedTopics/mcp-transport/) - Ny Avanceret Implementeringsguide
- **README.md**: Komplet implementeringsguide til custom MCP transportmekanismer.
  - **Azure Event Grid Transport**: Omfattende serverless event-drevet transportimplementering.
    - C#, TypeScript og Python eksempler med Azure Functions integration.
    - Event-drevet arkitekturmønstre for skalerbare MCP-løsninger.
    - Webhook modtagere og push-baseret meddelelseshåndtering.
  - **Azure Event Hubs Transport**: Høj-gennemstrømning streaming transportimplementering.
    - Realtidsstreaming kapaciteter for lav-latens scenarier.
    - Partitioneringsstrategier og checkpoint management.
    - Meddelelsesbatching og performanceoptimering.
  - **Enterprise Integrationsmønstre**: Produktionsklare arkitektureksempler.
    - Distribueret MCP behandling på tværs af flere Azure Functions.
    - Hybrid transportarkitekturer, der kombinerer flere transporttyper.
    - Meddelelsesholdbarhed, pålidelighed og fejlhåndteringsstrategier.
  - **Sikkerhed & Overvågning**: Azure Key Vault integration og observabilitetsmønstre.
    - Managed identity autentifikation og mindst privilegeret adgang.
    - Application Insights telemetri og performanceovervågning.
    - Circuit breakers og fejltolerance mønstre.
  - **Test Frameworks**: Omfattende teststrategier for custom transports.
    - Enhedstest med testdoubles og mocking frameworks.
    - Integrationstest med Azure Test Containers.
    - Performance- og belastningstestovervejelser.

#### Context Engineering (05-AdvancedTopics/mcp-contextengineering/) - Fremvoksende AI-disciplin
- **README.md**: Omfattende udforskning af context engineering som et fremvoksende felt.
  - **Kerneprincipper**: Komplet context sharing, action decision awareness og context window management.
  - **MCP Protokoltilpasning**: Hvordan MCP design adresserer context engineering udfordringer.
    - Begrænsninger i context window og progressive loading strategier.
    - Relevansbestemmelse og dynamisk context hentning.
    - Multi-modal context håndtering og sikkerhedsovervejelser.
  - **Implementeringsmetoder**: Single-threaded vs. multi-agent arkitekturer.
    - Context chunking og prioriteringsteknikker.
    - Progressive context loading og komprimeringsstrategier.
    - Lagdelte context tilgange og optimering af hentning.
  - **Målingsrammeværk**: Fremvoksende metrikker til evaluering af context effektivitet.
    - Inputeffektivitet, performance, kvalitet og brugeroplevelsesovervejelser.
    - Eksperimentelle tilgange til context optimering.
    - Fejlanalyse og forbedringsmetodologier.

#### Curriculum Navigationsopdateringer (README.md)
- **Forbedret Modulstruktur**: Opdateret curriculum tabel til at inkludere nye avancerede emner.
  - Tilføjet Context Engineering (5.14) og Custom Transport (5.15) poster.
  - Konsistent format og navigationslinks på tværs af alle moduler.
  - Opdaterede beskrivelser til at afspejle aktuelt indholdsomfang.

### Forbedringer af Mappestruktur
- **Navngivningsstandardisering**: Omdøbt "mcp transport" til "mcp-transport" for konsistens med andre avancerede emnemapper.
- **Indholdsorganisation**: Alle 05-AdvancedTopics mapper følger nu konsekvent navngivningsmønster (mcp-[topic]).

### Dokumentationskvalitetsforbedringer
- **MCP Specifikationsjustering**: Alt nyt indhold refererer til den aktuelle MCP Specifikation 2025-06-18.
- **Multi-Sprog Eksempler**: Omfattende kodeeksempler i C#, TypeScript og Python.
- **Enterprise Fokus**: Produktionsklare mønstre og Azure cloud integration gennem hele.
- **Visuel Dokumentation**: Mermaid diagrammer til arkitektur og flow visualisering.

## 18. august 2025

### Omfattende Dokumentationsopdatering - MCP 2025-06-18 Standarder

#### MCP Sikkerhedsbedste Praksis (02-Security/) - Komplet Modernisering
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Komplet omskrivning tilpasset MCP Specifikation 2025-06-18.
  - **Obligatoriske Krav**: Tilføjet eksplicitte MUST/MUST NOT krav fra den officielle specifikation med klare visuelle indikatorer.
  - **12 Kerne Sikkerhedspraksisser**: Omstruktureret fra 15-punkts liste til omfattende sikkerhedsområder.
    - Token Sikkerhed & Autentifikation med integration af eksterne identitetsudbydere.
    - Session Management & Transport Sikkerhed med kryptografiske krav.
    - AI-Specifik Trusselsbeskyttelse med Microsoft Prompt Shields integration.
    - Adgangskontrol & Tilladelser med princippet om mindst privilegium.
    - Indholdssikkerhed & Overvågning med Azure Content Safety integration.
    - Forsyningskædesikkerhed med omfattende komponentverifikation.
    - OAuth Sikkerhed & Forebyggelse af Confused Deputy med PKCE implementering.
    - Incident Response & Recovery med automatiserede kapaciteter.
    - Overholdelse & Governance med regulatorisk tilpasning.
    - Avancerede Sikkerhedskontroller med zero trust arkitektur.
    - Microsoft Sikkerhedsøkosystem Integration med omfattende løsninger.
    - Kontinuerlig Sikkerhedsudvikling med adaptive praksisser.
  - **Microsoft Sikkerhedsløsninger**: Forbedret integrationsvejledning for Prompt Shields, Azure Content Safety, Entra ID og GitHub Advanced Security.
  - **Implementeringsressourcer**: Kategoriserede omfattende ressourcelinks efter Officiel MCP Dokumentation, Microsoft Sikkerhedsløsninger, Sikkerhedsstandarder og Implementeringsguider.

#### Avancerede Sikkerhedskontroller (02-Security/) - Enterprise Implementering
- **MCP-SECURITY-CONTROLS-2025.md**: Komplet revision med enterprise-grade sikkerhedsrammeværk.
  - **9 Omfattende Sikkerhedsområder**: Udvidet fra grundlæggende kontroller til detaljeret enterprise rammeværk.
    - Avanceret Autentifikation & Autorisation med Microsoft Entra ID integration.
    - Token Sikkerhed & Anti-Passthrough Kontroller med omfattende validering.
    - Session Sikkerhedskontroller med kapring forebyggelse.
    - AI-Specifik Sikkerhedskontroller med prompt injection og værktøjsforgiftning forebyggelse.
    - Forebyggelse af Confused Deputy Angreb med OAuth proxy sikkerhed.
    - Værktøjsudførelse Sikkerhed med sandboxing og isolation.
    - Forsyningskædesikkerhedskontroller med afhængighedsverifikation.
    - Overvågnings- & Detektionskontroller med SIEM integration.
    - Incident Response & Recovery med automatiserede kapaciteter.
  - **Implementeringseksempler**: Tilføjet detaljerede YAML konfigurationsblokke og kodeeksempler.
  - **Microsoft Løsningsintegration**: Omfattende dækning af Azure sikkerhedstjenester, GitHub Advanced Security og enterprise identitetsstyring.
#### Avancerede Emner Sikkerhed (05-AdvancedTopics/mcp-security/) - Produktionsklar Implementering
- **README.md**: Fuldstændig omskrivning for implementering af virksomhedssikkerhed
  - **Nuværende Specifikationsjustering**: Opdateret til MCP Specifikation 2025-06-18 med obligatoriske sikkerhedskrav
  - **Forbedret Autentifikation**: Microsoft Entra ID-integration med omfattende .NET- og Java Spring Security-eksempler
  - **AI Sikkerhedsintegration**: Implementering af Microsoft Prompt Shields og Azure Content Safety med detaljerede Python-eksempler
  - **Avanceret Trusselsafværgelse**: Omfattende implementeringseksempler for
    - Forebyggelse af Confused Deputy-angreb med PKCE og validering af brugerens samtykke
    - Forebyggelse af Token Passthrough med validering af målgruppe og sikker tokenhåndtering
    - Forebyggelse af Session Hijacking med kryptografisk binding og adfærdsanalyse
  - **Integration af Virksomhedssikkerhed**: Overvågning med Azure Application Insights, trusselsdetektionspipelines og forsyningskædesikkerhed
  - **Implementeringscheckliste**: Klare obligatoriske vs. anbefalede sikkerhedskontroller med fordele ved Microsofts sikkerhedsøkosystem

### Dokumentationskvalitet & Standardjustering
- **Specifikationsreferencer**: Opdateret alle referencer til den aktuelle MCP Specifikation 2025-06-18
- **Microsofts Sikkerhedsøkosystem**: Forbedret integrationsvejledning i hele sikkerhedsdokumentationen
- **Praktisk Implementering**: Tilføjet detaljerede kodeeksempler i .NET, Java og Python med virksomhedsmønstre
- **Ressourceorganisering**: Omfattende kategorisering af officiel dokumentation, sikkerhedsstandarder og implementeringsvejledninger
- **Visuelle Indikatorer**: Klar markering af obligatoriske krav vs. anbefalede praksisser

#### Kernekoncepter (01-CoreConcepts/) - Fuldstændig Modernisering
- **Protokolversionsopdatering**: Opdateret til at referere til den aktuelle MCP Specifikation 2025-06-18 med dato-baseret versionering (YYYY-MM-DD format)
- **Arkitekturforfining**: Forbedrede beskrivelser af Hosts, Clients og Servers for at afspejle aktuelle MCP-arkitekturmønstre
  - Hosts nu klart defineret som AI-applikationer, der koordinerer flere MCP-klientforbindelser
  - Clients beskrevet som protokolforbindelser, der opretholder en-til-en serverrelationer
  - Servers forbedret med lokale vs. fjernimplementeringsscenarier
- **Primitiv Omstrukturering**: Fuldstændig revision af server- og klientprimitiver
  - Serverprimitiver: Ressourcer (datakilder), Prompts (skabeloner), Tools (eksekverbare funktioner) med detaljerede forklaringer og eksempler
  - Klientprimitiver: Sampling (LLM-udfyldelser), Elicitation (brugerinput), Logging (fejlfinding/overvågning)
  - Opdateret med aktuelle opdagelses- (`*/list`), hentnings- (`*/get`) og eksekverings- (`*/call`) metode-mønstre
- **Protokolarkitektur**: Introduceret to-lags arkitekturmodel
  - Datalag: JSON-RPC 2.0 fundament med livscyklusstyring og primitiv
  - Transportlag: STDIO (lokal) og Streamable HTTP med SSE (fjern) transportmekanismer
- **Sikkerhedsramme**: Omfattende sikkerhedsprincipper, herunder eksplicit brugerens samtykke, databeskyttelse, værktøjssikkerhed og transportlagssikkerhed
- **Kommunikationsmønstre**: Opdaterede protokolmeddelelser til at vise initialisering, opdagelse, eksekvering og notifikationsflows
- **Kodeeksempler**: Opdaterede flersprogede eksempler (.NET, Java, Python, JavaScript) til at afspejle aktuelle MCP SDK-mønstre

#### Sikkerhed (02-Security/) - Omfattende Sikkerhedsoverhaling  
- **Standardjustering**: Fuld justering med MCP Specifikation 2025-06-18 sikkerhedskrav
- **Udvikling af Autentifikation**: Dokumenteret udvikling fra brugerdefinerede OAuth-servere til delegation af eksterne identitetsudbydere (Microsoft Entra ID)
- **AI-Specifik Trusselsanalyse**: Forbedret dækning af moderne AI-angrebsvektorer
  - Detaljerede scenarier for prompt injection-angreb med virkelige eksempler
  - Mekanismer for værktøjsforgiftning og "rug pull"-angrebsmønstre
  - Context window-forgiftning og model-forvirringsangreb
- **Microsoft AI Sikkerhedsløsninger**: Omfattende dækning af Microsofts sikkerhedsøkosystem
  - AI Prompt Shields med avanceret detektion, spotlighting og delimiter-teknikker
  - Azure Content Safety integrationsmønstre
  - GitHub Advanced Security til forsyningskædebeskyttelse
- **Avanceret Trusselsafværgelse**: Detaljerede sikkerhedskontroller for
  - Session hijacking med MCP-specifikke angrebsscenarier og kryptografiske session-ID-krav
  - Confused deputy-problemer i MCP proxy-scenarier med eksplicit samtykkekrav
  - Token passthrough-sårbarheder med obligatoriske valideringskontroller
- **Forsyningskædesikkerhed**: Udvidet dækning af AI-forsyningskæden, herunder grundlæggende modeller, embeddings-tjenester, kontekstudbydere og tredjeparts-API'er
- **Grundlæggende Sikkerhed**: Forbedret integration med virksomhedssikkerhedsmønstre, herunder zero trust-arkitektur og Microsofts sikkerhedsøkosystem
- **Ressourceorganisering**: Kategoriseret omfattende ressource-links efter type (Officielle Dokumenter, Standarder, Forskning, Microsoft-løsninger, Implementeringsvejledninger)

### Dokumentationskvalitetsforbedringer
- **Strukturerede Læringsmål**: Forbedrede læringsmål med specifikke, handlingsorienterede resultater
- **Krydsreferencer**: Tilføjet links mellem relaterede sikkerheds- og kernekonceptemner
- **Aktuel Information**: Opdateret alle datoreferencer og specifikationslinks til aktuelle standarder
- **Implementeringsvejledning**: Tilføjet specifikke, handlingsorienterede implementeringsretningslinjer i begge sektioner

## 16. juli 2025

### README og Navigationsforbedringer
- Fuldstændig redesignet curriculum-navigation i README.md
- Erstattet `<details>`-tags med mere tilgængeligt tabelbaseret format
- Oprettet alternative layoutmuligheder i ny "alternative_layouts"-mappe
- Tilføjet kortbaserede, fanebaserede og accordion-stil navigations-eksempler
- Opdateret afsnittet om repository-struktur til at inkludere alle nyeste filer
- Forbedret afsnittet "Sådan bruger du dette curriculum" med klare anbefalinger
- Opdateret MCP-specifikationslinks til at pege på korrekte URL'er
- Tilføjet afsnittet Context Engineering (5.14) til curriculum-strukturen

### Studieguideopdateringer
- Fuldstændig revideret studieguide for at tilpasse sig den aktuelle repository-struktur
- Tilføjet nye sektioner for MCP-klienter og værktøjer samt populære MCP-servere
- Opdateret det visuelle curriculum-kort for nøjagtigt at afspejle alle emner
- Forbedret beskrivelser af avancerede emner for at dække alle specialiserede områder
- Opdateret afsnittet om casestudier for at afspejle faktiske eksempler
- Tilføjet denne omfattende ændringslog

### Fællesskabsbidrag (06-CommunityContributions/)
- Tilføjet detaljeret information om MCP-servere til billedgenerering
- Tilføjet omfattende sektion om brug af Claude i VSCode
- Tilføjet opsætnings- og brugsinstruktioner for Cline terminalklient
- Opdateret MCP-klientsektion for at inkludere alle populære klientmuligheder
- Forbedret bidragseksempler med mere præcise kodeeksempler

### Avancerede Emner (05-AdvancedTopics/)
- Organiseret alle specialiserede emnemapper med ensartede navne
- Tilføjet materialer og eksempler på kontekstengineering
- Tilføjet dokumentation for Foundry-agentintegration
- Forbedret dokumentation for Entra ID-sikkerhedsintegration

## 11. juni 2025

### Oprettelse af første version
- Udgivet første version af MCP for Beginners-curriculum
- Oprettet grundlæggende struktur for alle 10 hovedsektioner
- Implementeret visuelt curriculum-kort til navigation
- Tilføjet indledende prøveprojekter i flere programmeringssprog

### Kom godt i gang (03-GettingStarted/)
- Oprettet første serverimplementeringseksempler
- Tilføjet vejledning til klientudvikling
- Inkluderet LLM-klientintegrationsinstruktioner
- Tilføjet dokumentation for VS Code-integration
- Implementeret Server-Sent Events (SSE) servereksempler

### Kernekoncepter (01-CoreConcepts/)
- Tilføjet detaljeret forklaring af klient-server-arkitektur
- Oprettet dokumentation om nøgleprotokolkomponenter
- Dokumenteret beskedmønstre i MCP

## 23. maj 2025

### Repository-struktur
- Initialiseret repository med grundlæggende mappestruktur
- Oprettet README-filer for hver hovedsektion
- Opsat oversættelsesinfrastruktur
- Tilføjet billedressourcer og diagrammer

### Dokumentation
- Oprettet indledende README.md med curriculum-oversigt
- Tilføjet CODE_OF_CONDUCT.md og SECURITY.md
- Opsat SUPPORT.md med vejledning til at få hjælp
- Oprettet foreløbig struktur for studieguide

## 15. april 2025

### Planlægning og Rammeværk
- Indledende planlægning for MCP for Beginners-curriculum
- Defineret læringsmål og målgruppe
- Skitseret 10-sektionsstruktur for curriculum
- Udviklet konceptuelt rammeværk for eksempler og casestudier
- Oprettet indledende prototypeeksempler for nøglekoncepter

---

**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal det bemærkes, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os ikke ansvar for misforståelser eller fejltolkninger, der måtte opstå som følge af brugen af denne oversættelse.