<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T15:15:18+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "da"
}
-->
# MCP Sikkerhed: Omfattende Beskyttelse af AI-Systemer

[![MCP Sikkerhedsbedste Praksis](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.da.png)](https://youtu.be/88No8pw706o)

_(Klik på billedet ovenfor for at se videoen til denne lektion)_

Sikkerhed er grundlæggende for designet af AI-systemer, og derfor prioriterer vi det som vores anden sektion. Dette er i tråd med Microsofts **Secure by Design**-princip fra [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) bringer kraftfulde nye muligheder til AI-drevne applikationer, men introducerer også unikke sikkerhedsudfordringer, der går ud over traditionelle softwaretrusler. MCP-systemer står over for både etablerede sikkerhedsproblemer (sikker kodning, mindst privilegium, forsyningskædesikkerhed) og nye AI-specifikke trusler som prompt injection, værktøjsforgiftning, session hijacking, confused deputy-angreb, token passthrough-sårbarheder og dynamisk kapabilitetsmodifikation.

Denne lektion udforsker de mest kritiske sikkerhedsrisici i MCP-implementeringer—herunder autentifikation, autorisation, overdrevne tilladelser, indirekte prompt injection, sessionssikkerhed, confused deputy-problemer, tokenhåndtering og forsyningskædesårbarheder. Du vil lære handlingsrettede kontroller og bedste praksis for at afbøde disse risici, samtidig med at du udnytter Microsoft-løsninger som Prompt Shields, Azure Content Safety og GitHub Advanced Security til at styrke din MCP-implementering.

## Læringsmål

Ved afslutningen af denne lektion vil du være i stand til at:

- **Identificere MCP-Specifikke Trusler**: Genkende unikke sikkerhedsrisici i MCP-systemer, herunder prompt injection, værktøjsforgiftning, overdrevne tilladelser, session hijacking, confused deputy-problemer, token passthrough-sårbarheder og forsyningskæderisici
- **Anvende Sikkerhedskontroller**: Implementere effektive afbødninger, herunder robust autentifikation, mindst privilegium adgang, sikker tokenhåndtering, sessionssikkerhedskontroller og forsyningskædeverifikation
- **Udnytte Microsoft Sikkerhedsløsninger**: Forstå og implementere Microsoft Prompt Shields, Azure Content Safety og GitHub Advanced Security til MCP-arbejdsbelastningsbeskyttelse
- **Validere Værktøjssikkerhed**: Indse vigtigheden af validering af værktøjsmetadata, overvågning af dynamiske ændringer og forsvar mod indirekte prompt injection-angreb
- **Integrere Bedste Praksis**: Kombinere etablerede sikkerhedsfundamenter (sikker kodning, serverhærdning, zero trust) med MCP-specifikke kontroller for omfattende beskyttelse

# MCP Sikkerhedsarkitektur & Kontroller

Moderne MCP-implementeringer kræver lagdelte sikkerhedstilgange, der adresserer både traditionelle softwaresikkerhedstrusler og AI-specifikke trusler. Den hurtigt udviklende MCP-specifikation fortsætter med at modne sine sikkerhedskontroller, hvilket muliggør bedre integration med virksomhedssikkerhedsarkitekturer og etablerede bedste praksis.

Forskning fra [Microsoft Digital Defense Report](https://aka.ms/mddr) viser, at **98 % af rapporterede brud kunne forhindres med robust sikkerhedshygiejne**. Den mest effektive beskyttelsesstrategi kombinerer grundlæggende sikkerhedspraksis med MCP-specifikke kontroller—beviste baseline sikkerhedsforanstaltninger forbliver de mest effektive til at reducere den samlede sikkerhedsrisiko.

## Aktuelt Sikkerhedslandskab

> **Note:** Disse oplysninger afspejler MCP-sikkerhedsstandarder pr. **18. august 2025**. MCP-protokollen udvikler sig hurtigt, og fremtidige implementeringer kan introducere nye autentifikationsmønstre og forbedrede kontroller. Henvis altid til den aktuelle [MCP-specifikation](https://spec.modelcontextprotocol.io/), [MCP GitHub-repository](https://github.com/modelcontextprotocol) og [sikkerhedsbedste praksis-dokumentation](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) for den nyeste vejledning.

### Udvikling af MCP Autentifikation

MCP-specifikationen har udviklet sig betydeligt i sin tilgang til autentifikation og autorisation:

- **Oprindelig Tilgang**: Tidlige specifikationer krævede, at udviklere implementerede brugerdefinerede autentifikationsservere, hvor MCP-servere fungerede som OAuth 2.0 Autorisationsservere, der håndterede brugerautentifikation direkte
- **Nuværende Standard (2025-06-18)**: Opdateret specifikation tillader MCP-servere at delegere autentifikation til eksterne identitetsudbydere (såsom Microsoft Entra ID), hvilket forbedrer sikkerhedsniveauet og reducerer implementeringskompleksiteten
- **Transportlagssikkerhed**: Forbedret understøttelse af sikre transportmekanismer med korrekte autentifikationsmønstre for både lokale (STDIO) og eksterne (Streamable HTTP) forbindelser

## Autentifikations- & Autorisationssikkerhed

### Aktuelle Sikkerhedsudfordringer

Moderne MCP-implementeringer står over for flere autentifikations- og autorisationsudfordringer:

### Risici & Trusselsvektorer

- **Fejlagtig Autorisationslogik**: Fejlbehæftet autorisationsimplementering i MCP-servere kan eksponere følsomme data og anvende adgangskontroller forkert
- **OAuth Token Kompromittering**: Tyveri af lokale MCP-servertokens gør det muligt for angribere at udgive sig for servere og få adgang til downstream-tjenester
- **Token Passthrough Sårbarheder**: Forkert tokenhåndtering skaber omgåelse af sikkerhedskontroller og ansvarlighedshuller
- **Overdrevne Tilladelser**: Overprivilegerede MCP-servere overtræder mindst privilegium-principper og udvider angrebsflader

#### Token Passthrough: Et Kritisk Anti-Mønster

**Token passthrough er eksplicit forbudt** i den nuværende MCP-autorisationsspecifikation på grund af alvorlige sikkerhedsmæssige konsekvenser:

##### Omgåelse af Sikkerhedskontroller
- MCP-servere og downstream-API'er implementerer kritiske sikkerhedskontroller (ratebegrænsning, anmodningsvalidering, trafikovervågning), der afhænger af korrekt tokenvalidering
- Direkte brug af klient-til-API-tokens omgår disse essentielle beskyttelser og underminerer sikkerhedsarkitekturen

##### Ansvarligheds- & Revisionsudfordringer  
- MCP-servere kan ikke skelne mellem klienter, der bruger upstream-udstedte tokens, hvilket bryder revisionsspor
- Downstream-ressourceserverlogfiler viser vildledende anmodningsoprindelser i stedet for de faktiske MCP-servermellemled
- Hændelsesundersøgelser og overholdelsesrevisioner bliver betydeligt vanskeligere

##### Risiko for Dataudtræk
- Uvaliderede tokenkrav gør det muligt for ondsindede aktører med stjålne tokens at bruge MCP-servere som proxyer til dataudtræk
- Overtrædelse af tillidsgrænser tillader uautoriserede adgangsmønstre, der omgår tilsigtede sikkerhedskontroller

##### Angrebsvektorer på Tværs af Tjenester
- Kompromitterede tokens, der accepteres af flere tjenester, muliggør lateral bevægelse på tværs af forbundne systemer
- Tillidsantagelser mellem tjenester kan blive overtrådt, når tokenoprindelser ikke kan verificeres

### Sikkerhedskontroller & Afbødninger

**Kritiske Sikkerhedskrav:**

> **OBLIGATORISK**: MCP-servere **MÅ IKKE** acceptere tokens, der ikke eksplicit er udstedt til MCP-serveren

#### Autentifikations- & Autorisationskontroller

- **Grundig Autorisationsgennemgang**: Udfør omfattende revisioner af MCP-serverens autorisationslogik for at sikre, at kun tilsigtede brugere og klienter kan få adgang til følsomme ressourcer
  - **Implementeringsvejledning**: [Azure API Management som Autentifikationsgateway for MCP-servere](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Identitetsintegration**: [Brug af Microsoft Entra ID til MCP-serverautentifikation](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Sikker Tokenhåndtering**: Implementer [Microsofts bedste praksis for tokenvalidering og livscyklus](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Valider, at token audience-krav matcher MCP-serverens identitet
  - Implementer korrekt tokenrotation og udløbspolitikker
  - Forebyg token replay-angreb og uautoriseret brug

- **Beskyttet Tokenlagring**: Sikre tokenlagring med kryptering både i hvile og under overførsel
  - **Bedste Praksis**: [Retningslinjer for Sikker Tokenlagring og Kryptering](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementering af Adgangskontrol

- **Princippet om Mindst Privilegium**: Giv MCP-servere kun de minimumstilladelser, der kræves for den tilsigtede funktionalitet
  - Regelmæssige tilladelsesgennemgange og opdateringer for at forhindre privilegieophobning
  - **Microsoft Dokumentation**: [Sikker Mindst-Privilegeret Adgang](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Rollebaseret Adgangskontrol (RBAC)**: Implementer fintmaskede rolleopgaver
  - Begræns roller stramt til specifikke ressourcer og handlinger
  - Undgå brede eller unødvendige tilladelser, der udvider angrebsflader

- **Kontinuerlig Tilladelsesovervågning**: Implementer løbende adgangsrevision og overvågning
  - Overvåg tilladelsesbrugsmønstre for unormale aktiviteter
  - Afhjælp straks overdrevne eller ubrugte privilegier

## AI-Specifikke Sikkerhedstrusler

### Prompt Injection & Manipulation af Værktøjer

Moderne MCP-implementeringer står over for sofistikerede AI-specifikke angrebsvektorer, som traditionelle sikkerhedsforanstaltninger ikke fuldt ud kan adressere:

#### **Indirekte Prompt Injection (Cross-Domain Prompt Injection)**

**Indirekte Prompt Injection** repræsenterer en af de mest kritiske sårbarheder i MCP-aktiverede AI-systemer. Angribere indlejrer ondsindede instruktioner i eksternt indhold—dokumenter, websider, e-mails eller datakilder—som AI-systemer efterfølgende behandler som legitime kommandoer.

**Angrebsscenarier:**
- **Dokumentbaseret Injection**: Ondsindede instruktioner skjult i behandlede dokumenter, der udløser utilsigtede AI-handlinger
- **Udnyttelse af Webindhold**: Kompromitterede websider med indlejrede prompts, der manipulerer AI-adfærd, når de skrabes
- **E-mailbaserede Angreb**: Ondsindede prompts i e-mails, der får AI-assistenter til at lække information eller udføre uautoriserede handlinger
- **Forurening af Datakilder**: Kompromitterede databaser eller API'er, der leverer forurenet indhold til AI-systemer

**Reel Indvirkning**: Disse angreb kan resultere i dataudtræk, brud på privatlivets fred, generering af skadeligt indhold og manipulation af brugerinteraktioner. For detaljeret analyse, se [Prompt Injection i MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Prompt Injection Angrebsdiagram](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.da.png)

#### **Værktøjsforgiftning**

**Værktøjsforgiftning** retter sig mod metadata, der definerer MCP-værktøjer, og udnytter, hvordan LLM'er fortolker værktøjsbeskrivelser og parametre til at træffe beslutninger om udførelse.

**Angrebsmekanismer:**
- **Manipulation af Metadata**: Angribere indsprøjter ondsindede instruktioner i værktøjsbeskrivelser, parameterdefinitioner eller brugseksempler
- **Usynlige Instruktioner**: Skjulte prompts i værktøjsmetadata, der behandles af AI-modeller, men er usynlige for menneskelige brugere
- **Dynamisk Værktøjsmodifikation ("Rug Pulls")**: Værktøjer, der er godkendt af brugere, ændres senere til at udføre ondsindede handlinger uden brugerens viden
- **Parameter Injection**: Ondsindet indhold indlejret i værktøjsparameter-skemaer, der påvirker modeladfærd

**Risici ved Hostede Servere**: Fjern-MCP-servere præsenterer forhøjede risici, da værktøjsdefinitioner kan opdateres efter den oprindelige brugeraccept, hvilket skaber scenarier, hvor tidligere sikre værktøjer bliver ondsindede. For omfattende analyse, se [Værktøjsforgiftningsangreb (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Værktøjs Injection Angrebsdiagram](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.da.png)

#### **Yderligere AI Angrebsvektorer**

- **Cross-Domain Prompt Injection (XPIA)**: Sofistikerede angreb, der udnytter indhold fra flere domæner til at omgå sikkerhedskontroller
- **Dynamisk Kapabilitetsmodifikation**: Ændringer i værktøjskapabiliteter i realtid, der undslipper den oprindelige sikkerhedsvurdering
- **Forurening af Kontekstvindue**: Angreb, der manipulerer store kontekstvinduer for at skjule ondsindede instruktioner
- **Model Forvirringsangreb**: Udnyttelse af modellens begrænsninger til at skabe uforudsigelig eller usikker adfærd

### AI Sikkerhedsrisiko Indvirkning

**Højindvirkningskonsekvenser:**
- **Dataudtræk**: Uautoriseret adgang og tyveri af følsomme virksomheds- eller persondata
- **Brud på Privatlivets Fred**: Eksponering af personligt identificerbare oplysninger (PII) og fortrolige forretningsdata  
- **Systemmanipulation**: Utilsigtede ændringer i kritiske systemer og arbejdsgange
- **Tyveri af Legitimation**: Kompromittering af autentifikationstokens og servicelegitimationer
- **Lateral Bevægelse**: Brug af kompromitterede AI-systemer som springbræt til bredere netværksangreb

### Microsoft AI Sikkerhedsløsninger

#### **AI Prompt Shields: Avanceret Beskyttelse mod Injection Angreb**

Microsoft **AI Prompt Shields** giver omfattende forsvar mod både direkte og indirekte prompt injection-angreb gennem flere sikkerhedslag:

##### **Kernebeskyttelsesmekanismer:**

1. **Avanceret Detektion & Filtrering**
   - Maskinlæringsalgoritmer og NLP-teknikker opdager ondsindede instruktioner i eksternt indhold
   - Realtidsanalyse af dokumenter, websider, e-mails og datakilder for indlejrede trusler
   - Kontekstuel forståelse af legitime vs. ondsindede promptmønstre

2. **Spotlighting Teknikker**  
   - Skelner mellem betroede systeminstruktioner og potentielt kompromitterede eksterne input
   - Teksttransformationsteknikker, der forbedrer modelrelevans, samtidig med at ondsindet indhold isoleres
   - Hjælper AI-systemer med at opretholde korrekt instruktionshierarki og ignorere injicerede kommandoer

3. **Afgrænsnings- & Datamarkeringssystemer**
   - Eksplicit grænsedefinition mellem betroede systemmeddelelser og eksterne inputtekster
   - Specielle markører fremhæver grænser mellem betroede og ikke-betroede datakilder
   - Klar adskillelse forhindrer instruktionsforvirring og uautoriseret kommandoeksekvering

4. **Kontinuerlig Trusselsintelligens**
   - Microsoft overvåger løbende fremvoksende angrebsmønstre og opdaterer forsvar
   - Proaktiv trusselsjagt efter nye injektionsteknikker og angrebsvektorer
   - Regelmæssige sikkerhedsmodelopdateringer for at opretholde effektivitet mod udviklende trusler

5. **Azure Content Safety Integration**
   - En del af den omfattende Azure AI Content Safety-suite
   - Yderligere detektion af jailbreak
- **Sikker generering af sessioner**: Brug kryptografisk sikre, ikke-deterministiske session-ID'er genereret med sikre tilfældige talgeneratorer  
- **Bruger-specifik binding**: Bind session-ID'er til bruger-specifik information ved hjælp af formater som `<user_id>:<session_id>` for at forhindre misbrug af sessioner på tværs af brugere  
- **Håndtering af sessionslivscyklus**: Implementer korrekt udløb, rotation og ugyldiggørelse for at begrænse sårbarhedsvinduer  
- **Transport-sikkerhed**: Obligatorisk HTTPS for al kommunikation for at forhindre aflytning af session-ID'er  

### Problemet med forvirrede mellemled

**Problemet med forvirrede mellemled** opstår, når MCP-servere fungerer som autentifikationsproxyer mellem klienter og tredjepartstjenester, hvilket skaber muligheder for at omgå autorisation gennem udnyttelse af statiske klient-ID'er.

#### **Angrebsmekanismer og risici**

- **Omgåelse af cookie-baseret samtykke**: Tidligere brugerautentifikation skaber samtykkecookies, som angribere udnytter gennem ondsindede autorisationsanmodninger med manipulerede redirect-URI'er  
- **Tyveri af autorisationskoder**: Eksisterende samtykkecookies kan få autorisationsservere til at springe samtykkeskærme over og omdirigere koder til angriberkontrollerede endepunkter  
- **Uautoriseret API-adgang**: Stjålne autorisationskoder muliggør tokenudveksling og brugerimitation uden eksplicit godkendelse  

#### **Afværgningsstrategier**

**Obligatoriske kontroller:**
- **Krav om eksplicit samtykke**: MCP-proxyservere, der bruger statiske klient-ID'er, **SKAL** indhente brugerens samtykke for hver dynamisk registreret klient  
- **Implementering af OAuth 2.1-sikkerhed**: Følg de nyeste OAuth-sikkerhedspraksisser, herunder PKCE (Proof Key for Code Exchange) for alle autorisationsanmodninger  
- **Streng klientvalidering**: Implementer grundig validering af redirect-URI'er og klientidentifikatorer for at forhindre udnyttelse  

### Sårbarheder ved token-videresendelse  

**Token-videresendelse** repræsenterer et eksplicit anti-mønster, hvor MCP-servere accepterer klienttokens uden korrekt validering og videresender dem til downstream-API'er, hvilket overtræder MCP-autorisationsspecifikationer.

#### **Sikkerhedsmæssige konsekvenser**

- **Omgåelse af kontroller**: Direkte brug af klient-til-API-tokens omgår kritiske kontroller som hastighedsbegrænsning, validering og overvågning  
- **Korruption af revisionsspor**: Tokens udstedt upstream gør det umuligt at identificere klienter, hvilket forhindrer undersøgelse af hændelser  
- **Proxy-baseret dataudtrækning**: Uvaliderede tokens gør det muligt for ondsindede aktører at bruge servere som proxyer til uautoriseret dataadgang  
- **Overtrædelse af tillidsgrænser**: Downstream-tjenesters tillidsantagelser kan blive brudt, når tokenoprindelse ikke kan verificeres  
- **Udvidelse af angreb på tværs af tjenester**: Kompromitterede tokens accepteret på tværs af flere tjenester muliggør lateral bevægelse  

#### **Påkrævede sikkerhedskontroller**

**Ufravigelige krav:**
- **Tokenvalidering**: MCP-servere **MÅ IKKE** acceptere tokens, der ikke eksplicit er udstedt til MCP-serveren  
- **Audience-verifikation**: Valider altid, at tokenets audience-krav matcher MCP-serverens identitet  
- **Korrekt tokenlivscyklus**: Implementer kortlivede adgangstokens med sikre rotationspraksisser  

## Forsyningskædesikkerhed for AI-systemer

Forsyningskædesikkerhed har udviklet sig ud over traditionelle softwareafhængigheder til at omfatte hele AI-økosystemet. Moderne MCP-implementeringer skal nøje verificere og overvåge alle AI-relaterede komponenter, da hver enkelt introducerer potentielle sårbarheder, der kan kompromittere systemets integritet.

### Udvidede AI-forsyningskædekomponenter

**Traditionelle softwareafhængigheder:**
- Open source-biblioteker og rammeværk  
- Containerbilleder og basissystemer  
- Udviklingsværktøjer og build-pipelines  
- Infrastrukturkomponenter og tjenester  

**AI-specifikke forsyningskædeelementer:**
- **Grundmodeller**: Fortrænede modeller fra forskellige udbydere, der kræver oprindelsesverifikation  
- **Indlejringsservices**: Eksterne vektoriseringer og semantiske søgetjenester  
- **Kontekstudbydere**: Datakilder, vidensbaser og dokumentarkiver  
- **Tredjeparts-API'er**: Eksterne AI-tjenester, ML-pipelines og databehandlingsendepunkter  
- **Modellartefakter**: Vægte, konfigurationer og finjusterede modelvarianter  
- **Træningsdatakilder**: Datasæt brugt til modellering og finjustering  

### Omfattende forsyningskædesikkerhedsstrategi

#### **Komponentverifikation og tillid**
- **Oprindelsesvalidering**: Verificer oprindelse, licens og integritet af alle AI-komponenter før integration  
- **Sikkerhedsvurdering**: Udfør sårbarhedsscanninger og sikkerhedsgennemgange for modeller, datakilder og AI-tjenester  
- **Rygteanalyse**: Evaluer sikkerhedshistorik og praksis hos AI-tjenesteudbydere  
- **Overholdelsesverifikation**: Sikr, at alle komponenter opfylder organisatoriske sikkerheds- og lovgivningsmæssige krav  

#### **Sikre implementeringspipelines**  
- **Automatiseret CI/CD-sikkerhed**: Integrer sikkerhedsscanning i automatiserede implementeringspipelines  
- **Artefaktintegritet**: Implementer kryptografisk verifikation for alle implementerede artefakter (kode, modeller, konfigurationer)  
- **Faset implementering**: Brug progressiv implementeringsstrategi med sikkerhedsvalidering på hvert trin  
- **Betroede artefaktlagre**: Implementer kun fra verificerede, sikre artefaktregistre og lagre  

#### **Kontinuerlig overvågning og respons**
- **Afhængighedsscanning**: Løbende sårbarhedsovervågning for alle software- og AI-komponentafhængigheder  
- **Modelovervågning**: Kontinuerlig vurdering af modeladfærd, præstationsdrift og sikkerhedsanomalier  
- **Serviceovervågning**: Overvåg eksterne AI-tjenester for tilgængelighed, sikkerhedshændelser og politikændringer  
- **Trusselsintelligensintegration**: Inkorporer trusselsfeeds specifikt for AI- og ML-sikkerhedsrisici  

#### **Adgangskontrol og mindst privilegium**
- **Komponentniveau-tilladelser**: Begræns adgang til modeller, data og tjenester baseret på forretningsbehov  
- **Servicekontoadministration**: Implementer dedikerede servicekonti med minimale nødvendige tilladelser  
- **Netværkssegmentering**: Isoler AI-komponenter og begræns netværksadgang mellem tjenester  
- **API-gatewaykontroller**: Brug centraliserede API-gateways til at kontrollere og overvåge adgang til eksterne AI-tjenester  

#### **Hændelsesrespons og genopretning**
- **Hurtige responsprocedurer**: Etablerede processer til at rette eller udskifte kompromitterede AI-komponenter  
- **Nøgle- og adgangsrotation**: Automatiserede systemer til at rotere hemmeligheder, API-nøgler og serviceoplysninger  
- **Tilbageføringsmuligheder**: Evne til hurtigt at vende tilbage til tidligere kendte gode versioner af AI-komponenter  
- **Genopretning efter forsyningskædebrud**: Specifikke procedurer til at reagere på kompromitterede upstream AI-tjenester  

### Microsofts sikkerhedsværktøjer og integration

**GitHub Advanced Security** tilbyder omfattende forsyningskædebeskyttelse, herunder:
- **Hemmelighedsscanning**: Automatisk detektion af legitimationsoplysninger, API-nøgler og tokens i repositories  
- **Afhængighedsscanning**: Sårbarhedsvurdering for open source-afhængigheder og biblioteker  
- **CodeQL-analyse**: Statisk kodeanalyse for sikkerhedssårbarheder og kodningsproblemer  
- **Forsyningskædeindsigt**: Synlighed i afhængigheders sundhed og sikkerhedsstatus  

**Azure DevOps og Azure Repos-integration:**
- Problemfri sikkerhedsscanningsintegration på tværs af Microsofts udviklingsplatforme  
- Automatiserede sikkerhedstjek i Azure Pipelines for AI-arbejdsbelastninger  
- Politikhåndhævelse for sikker implementering af AI-komponenter  

**Microsofts interne praksis:**
Microsoft implementerer omfattende forsyningskædesikkerhedspraksis på tværs af alle produkter. Læs om dokumenterede tilgange i [Rejsen mod at sikre softwareforsyningskæden hos Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Microsoft Sikkerhedsløsninger**
- [Microsoft Prompt Shields Dokumentation](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety Service](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID Sikkerhed](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Azure Token Management Bedste Praksis](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Implementeringsvejledninger & Tutorials**
- [Azure API Management som MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID Autentifikation med MCP Servere](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Sikker Token Opbevaring og Kryptering (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps & Forsyningskædesikkerhed**
- [Azure DevOps Sikkerhed](https://azure.microsoft.com/products/devops)
- [Azure Repos Sikkerhed](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft Forsyningskædesikkerhedsrejse](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Yderligere Sikkerhedsdokumentation**

For omfattende sikkerhedsvejledning, henvises til disse specialiserede dokumenter i denne sektion:

- **[MCP Sikkerhedsbedste Praksis 2025](./mcp-security-best-practices-2025.md)** - Komplette bedste praksis for MCP-implementeringer
- **[Azure Content Safety Implementering](./azure-content-safety-implementation.md)** - Praktiske implementeringseksempler for Azure Content Safety-integration  
- **[MCP Sikkerhedskontroller 2025](./mcp-security-controls-2025.md)** - Nyeste sikkerhedskontroller og teknikker til MCP-udrulninger
- **[MCP Bedste Praksis Hurtig Reference](./mcp-best-practices.md)** - Hurtig referenceguide til essentielle MCP-sikkerhedspraksisser

---

## Hvad er det næste

Næste: [Kapitel 3: Kom godt i gang](../03-GettingStarted/README.md)

**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal det bemærkes, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os ikke ansvar for eventuelle misforståelser eller fejltolkninger, der måtte opstå som følge af brugen af denne oversættelse.