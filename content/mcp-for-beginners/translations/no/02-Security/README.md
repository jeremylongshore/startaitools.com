<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T15:41:12+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "no"
}
-->
# MCP-sikkerhet: Omfattende beskyttelse for AI-systemer

[![MCP Security Best Practices](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.no.png)](https://youtu.be/88No8pw706o)

_(Klikk på bildet over for å se videoen til denne leksjonen)_

Sikkerhet er grunnleggende i designet av AI-systemer, og derfor prioriterer vi det som vår andre seksjon. Dette er i tråd med Microsofts **Secure by Design**-prinsipp fra [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) gir kraftige nye muligheter for AI-drevne applikasjoner, men introduserer også unike sikkerhetsutfordringer som går utover tradisjonelle programvarerisikoer. MCP-systemer står overfor både etablerte sikkerhetsproblemer (sikker koding, minst privilegium, forsyningskjedesikkerhet) og nye AI-spesifikke trusler som prompt-injeksjon, verktøyforgiftning, sesjonskapring, "confused deputy"-angrep, token-sårbarheter og dynamisk kapabilitetsmodifikasjon.

Denne leksjonen utforsker de mest kritiske sikkerhetsrisikoene i MCP-implementeringer—inkludert autentisering, autorisasjon, overdrevne tillatelser, indirekte prompt-injeksjon, sesjonssikkerhet, "confused deputy"-problemer, tokenhåndtering og forsyningskjedesårbarheter. Du vil lære praktiske kontroller og beste praksis for å redusere disse risikoene, samtidig som du utnytter Microsoft-løsninger som Prompt Shields, Azure Content Safety og GitHub Advanced Security for å styrke MCP-distribusjonen din.

## Læringsmål

Ved slutten av denne leksjonen vil du kunne:

- **Identifisere MCP-spesifikke trusler**: Gjenkjenne unike sikkerhetsrisikoer i MCP-systemer, inkludert prompt-injeksjon, verktøyforgiftning, overdrevne tillatelser, sesjonskapring, "confused deputy"-problemer, token-sårbarheter og forsyningskjedesikkerhet
- **Implementere sikkerhetskontroller**: Gjennomføre effektive tiltak som robust autentisering, minst privilegium-tilgang, sikker tokenhåndtering, sesjonssikkerhetskontroller og forsyningskjedeverifisering
- **Utnytte Microsofts sikkerhetsløsninger**: Forstå og distribuere Microsoft Prompt Shields, Azure Content Safety og GitHub Advanced Security for MCP-arbeidsbelastningsbeskyttelse
- **Validere verktøysikkerhet**: Gjenkjenne viktigheten av validering av verktøymetadata, overvåking av dynamiske endringer og forsvar mot indirekte prompt-injeksjonsangrep
- **Integrere beste praksis**: Kombinere etablerte sikkerhetsprinsipper (sikker koding, serverherding, nulltillit) med MCP-spesifikke kontroller for omfattende beskyttelse

# MCP-sikkerhetsarkitektur og kontroller

Moderne MCP-implementeringer krever lagdelte sikkerhetstilnærminger som adresserer både tradisjonell programvaresikkerhet og AI-spesifikke trusler. Den raskt utviklende MCP-spesifikasjonen fortsetter å modne sine sikkerhetskontroller, noe som muliggjør bedre integrasjon med virksomheters sikkerhetsarkitekturer og etablerte beste praksiser.

Forskning fra [Microsoft Digital Defense Report](https://aka.ms/mddr) viser at **98 % av rapporterte brudd kunne vært forhindret med robust sikkerhetshygiene**. Den mest effektive beskyttelsesstrategien kombinerer grunnleggende sikkerhetspraksis med MCP-spesifikke kontroller—beviste grunnleggende sikkerhetstiltak forblir de mest effektive for å redusere den totale sikkerhetsrisikoen.

## Nåværende sikkerhetslandskap

> **Note:** Denne informasjonen reflekterer MCP-sikkerhetsstandarder per **18. august 2025**. MCP-protokollen utvikler seg raskt, og fremtidige implementeringer kan introdusere nye autentiseringsmønstre og forbedrede kontroller. Se alltid den gjeldende [MCP-spesifikasjonen](https://spec.modelcontextprotocol.io/), [MCP GitHub-repositoriet](https://github.com/modelcontextprotocol) og [dokumentasjon for sikkerhetspraksis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) for den nyeste veiledningen.

### Utvikling av MCP-autentisering

MCP-spesifikasjonen har utviklet seg betydelig i sin tilnærming til autentisering og autorisasjon:

- **Opprinnelig tilnærming**: Tidlige spesifikasjoner krevde at utviklere implementerte tilpassede autentiseringsservere, der MCP-servere fungerte som OAuth 2.0-autoriseringstjenere som håndterte brukerautentisering direkte
- **Nåværende standard (2025-06-18)**: Oppdatert spesifikasjon tillater MCP-servere å delegere autentisering til eksterne identitetsleverandører (som Microsoft Entra ID), noe som forbedrer sikkerhetsnivået og reduserer implementeringskompleksiteten
- **Transportlagssikkerhet**: Forbedret støtte for sikre transportmekanismer med riktige autentiseringsmønstre for både lokale (STDIO) og eksterne (Streamable HTTP) tilkoblinger

## Autentisering og autorisasjonssikkerhet

### Nåværende sikkerhetsutfordringer

Moderne MCP-implementeringer står overfor flere autentiserings- og autorisasjonsutfordringer:

### Risikoer og trusselvektorer

- **Feilkonfigurert autorisasjonslogikk**: Feil i autorisasjonsimplementeringen i MCP-servere kan eksponere sensitiv data og feilaktig anvende tilgangskontroller
- **OAuth-tokenkompromittering**: Tyveri av lokale MCP-servertokens gjør det mulig for angripere å utgi seg for servere og få tilgang til nedstrøms tjenester
- **Token-sårbarheter**: Feilaktig tokenhåndtering skaper omgåelser av sikkerhetskontroller og hull i ansvarlighet
- **Overdrevne tillatelser**: MCP-servere med for mange privilegier bryter prinsippet om minst privilegium og utvider angrepsflaten

#### Token-sårbarheter: Et kritisk anti-mønster

**Token-sårbarheter er eksplisitt forbudt** i den nåværende MCP-autorisasjonsspesifikasjonen på grunn av alvorlige sikkerhetsimplikasjoner:

##### Omgåelse av sikkerhetskontroller
- MCP-servere og nedstrøms API-er implementerer kritiske sikkerhetskontroller (ratebegrensning, forespørselsvalidering, trafikkovervåking) som avhenger av riktig tokenvalidering
- Direkte bruk av klient-til-API-tokens omgår disse essensielle beskyttelsene, noe som undergraver sikkerhetsarkitekturen

##### Ansvarlighet og revisjonsutfordringer  
- MCP-servere kan ikke skille mellom klienter som bruker oppstrøms utstedte tokens, noe som bryter revisjonsspor
- Logger på nedstrøms ressursservere viser misvisende forespørselsopprinnelse i stedet for faktiske MCP-servermellomledd
- Hendelsesundersøkelser og samsvarsrevisjoner blir betydelig vanskeligere

##### Risiko for dataeksfiltrering
- Uvaliderte tokenkrav gjør det mulig for ondsinnede aktører med stjålne tokens å bruke MCP-servere som proxyer for dataeksfiltrering
- Brudd på tillitsgrenser tillater uautoriserte tilgangsmønstre som omgår tiltenkte sikkerhetskontroller

##### Angrepsvektorer på tvers av tjenester
- Kompromitterte tokens akseptert av flere tjenester muliggjør lateral bevegelse på tvers av tilkoblede systemer
- Tillitsforutsetninger mellom tjenester kan brytes når tokenopprinnelse ikke kan verifiseres

### Sikkerhetskontroller og tiltak

**Kritiske sikkerhetskrav:**

> **OBLIGATORISK**: MCP-servere **MÅ IKKE** akseptere noen tokens som ikke eksplisitt ble utstedt for MCP-serveren

#### Autentiserings- og autorisasjonskontroller

- **Grundig autorisasjonsgjennomgang**: Gjennomfør omfattende revisjoner av MCP-serverens autorisasjonslogikk for å sikre at kun tiltenkte brukere og klienter kan få tilgang til sensitive ressurser
  - **Implementeringsveiledning**: [Azure API Management som autentiseringsgateway for MCP-servere](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Identitetsintegrasjon**: [Bruke Microsoft Entra ID for MCP-serverautentisering](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Sikker tokenhåndtering**: Implementer [Microsofts beste praksis for tokenvalidering og livssyklus](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Valider at tokenets målgruppekrav samsvarer med MCP-serverens identitet
  - Implementer riktig tokenrotasjon og utløpspolicyer
  - Forhindre token-replay-angrep og uautorisert bruk

- **Beskyttet tokenlagring**: Sikre tokenlagring med kryptering både i hvile og under overføring
  - **Beste praksis**: [Veiledning for sikker tokenlagring og kryptering](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementering av tilgangskontroll

- **Prinsippet om minst privilegium**: Gi MCP-servere kun minimumstillatelser som kreves for tiltenkt funksjonalitet
  - Regelmessige tillatelsesgjennomganger og oppdateringer for å forhindre privilegieøkning
  - **Microsoft-dokumentasjon**: [Sikker tilgang med minst privilegium](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Rollebasert tilgangskontroll (RBAC)**: Implementer finjusterte rolleoppgaver
  - Begrens roller strengt til spesifikke ressurser og handlinger
  - Unngå brede eller unødvendige tillatelser som utvider angrepsflaten

- **Kontinuerlig tillatelsesovervåking**: Implementer pågående tilgangsrevisjoner og overvåking
  - Overvåk tillatelsesbruksmønstre for avvik
  - Raskt utbedre overdrevne eller ubrukte privilegier

## AI-spesifikke sikkerhetstrusler

### Prompt-injeksjon og verktøysmanipulasjonsangrep

Moderne MCP-implementeringer står overfor sofistikerte AI-spesifikke angrepsvektorer som tradisjonelle sikkerhetstiltak ikke fullt ut kan adressere:

#### **Indirekte prompt-injeksjon (tverrdomeneprompt-injeksjon)**

**Indirekte prompt-injeksjon** representerer en av de mest kritiske sårbarhetene i MCP-aktiverte AI-systemer. Angripere skjuler ondsinnede instruksjoner i eksternt innhold—dokumenter, nettsider, e-poster eller datakilder—som AI-systemer deretter behandler som legitime kommandoer.

**Angrepsscenarier:**
- **Dokumentbasert injeksjon**: Ondsinnede instruksjoner skjult i behandlede dokumenter som utløser utilsiktede AI-handlinger
- **Utnyttelse av nettinnhold**: Kompromitterte nettsider med innebygde prompt som manipulerer AI-adferd når de skrapes
- **E-postbaserte angrep**: Ondsinnede prompt i e-poster som får AI-assistenter til å lekke informasjon eller utføre uautoriserte handlinger
- **Datakildekontaminering**: Kompromitterte databaser eller API-er som leverer forurenset innhold til AI-systemer

**Reell påvirkning**: Disse angrepene kan føre til dataeksfiltrering, personvernbrudd, generering av skadelig innhold og manipulering av brukerinteraksjoner. For detaljert analyse, se [Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Prompt Injection Attack Diagram](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.no.png)

#### **Verktøyforgiftning**

**Verktøyforgiftning** retter seg mot metadataene som definerer MCP-verktøy, og utnytter hvordan LLM-er tolker verktøybeskrivelser og parametere for å ta beslutninger om utførelse.

**Angrepsmekanismer:**
- **Manipulasjon av metadata**: Angripere injiserer ondsinnede instruksjoner i verktøybeskrivelser, parameterdefinisjoner eller brukseksempler
- **Usynlige instruksjoner**: Skjulte prompt i verktøymetadata som behandles av AI-modeller, men som er usynlige for menneskelige brukere
- **Dynamisk verktøymodifikasjon ("Rug Pulls")**: Verktøy godkjent av brukere endres senere for å utføre ondsinnede handlinger uten brukerens bevissthet
- **Parameterinjeksjon**: Ondsinnet innhold innebygd i verktøyparameter-skjemaer som påvirker modelladferd

**Risiko ved eksterne servere**: Eksterne MCP-servere utgjør økte risikoer ettersom verktøydefinisjoner kan oppdateres etter første brukeraksept, noe som skaper scenarier der tidligere trygge verktøy blir ondsinnede. For omfattende analyse, se [Tool Poisoning Attacks (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Tool Injection Attack Diagram](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.no.png)

#### **Ytterligere AI-angrepsvektorer**

- **Tverrdomeneprompt-injeksjon (XPIA)**: Sofistikerte angrep som utnytter innhold fra flere domener for å omgå sikkerhetskontroller
- **Dynamisk kapabilitetsmodifikasjon**: Endringer i verktøyfunksjoner i sanntid som unngår opprinnelige sikkerhetsvurderinger
- **Kontaminering av kontekstvindu**: Angrep som manipulerer store kontekstvinduer for å skjule ondsinnede instruksjoner
- **Modellforvirringsangrep**: Utnyttelse av modellbegrensninger for å skape uforutsigbar eller usikker adferd

### AI-sikkerhetsrisiko og konsekvenser

**Høye konsekvenser:**
- **Dataeksfiltrering**: Uautorisert tilgang og tyveri av sensitiv bedrifts- eller persondata
- **Personvernbrudd**: Eksponering av personlig identifiserbar informasjon (PII) og konfidensielle forretningsdata  
- **Systemmanipulasjon**: Utilsiktede modifikasjoner av kritiske systemer og arbeidsflyter
- **Tyveri av legitimasjon**: Kompromittering av autentiseringstokens og tjenestekredentialer
- **Lateral bevegelse**: Bruk av kompromitterte AI-systemer som springbrett for bredere nettverksangrep

### Microsoft AI-sikkerhetsløsninger

#### **AI Prompt Shields: Avansert beskyttelse mot injeksjonsangrep**

Microsoft **AI Prompt Shields** gir omfattende forsvar mot både direkte og indirekte prompt-injeksjonsangrep gjennom flere sikkerhetslag:

##### **Kjernebeskyttelsesmekanismer:**

1. **Avansert deteksjon og filtrering**
   - Maskinlæringsalgoritmer og NLP-teknikker oppdager ondsinnede instruksjoner i eksternt innhold
   - Sanntidsanalyse av dokumenter, nettsider, e-poster og datakilder for innebygde trusler
   - Kontekstuell forståelse av legitime vs. ondsinnede prompt-mønstre

2. **Spotlight-teknikker**  
   - Skiller mellom betrodde systeminstruksjoner og potensielt kompromitterte eksterne input
   - Teksttransformasjonsmetoder som forbedrer modellrelevans samtidig som ondsinnet innhold isoleres
   - Hjelper AI-systemer med å opprettholde riktig instruksjonshierarki og ignorere injiserte kommandoer

3. **Avgrensnings- og datamerkesystemer**
   - Eksplisitt grensedefinisjon mellom betrodde systemmeldinger og eksternt input-tekst
   - Spesielle markører fremhever grenser mellom betrodde og ikke-betrodde datakilder
   - Klar separasjon forhindrer instruksjonsforvirring og uautorisert kommandoeksekvering

4. **Kontinuerlig trusselintelligens**
   - Microsoft overvåker kontinuerlig fremvoksende angrepsmønstre og oppdaterer forsvar
   - Proaktiv trusseljakt etter nye injeksjonsteknikker og angrepsvektorer
   - Regelmessige sikkerhetsmodelloppdateringer for å opprettholde effektivitet mot utviklende trusler

5. **Azure Content Safety-integrasjon**
   - En del av den omfattende Azure AI Content Safety-pakken
   - Ekstra deteksjon for jailbreak-forsøk, skadelig innhold og
- **Sikker generering av økter**: Bruk kryptografisk sikre, ikke-deterministiske økt-ID-er generert med sikre tilfeldige tallgeneratorer  
- **Brukerspesifikk binding**: Bind økt-ID-er til brukerspesifikk informasjon ved hjelp av formater som `<user_id>:<session_id>` for å forhindre misbruk av økter på tvers av brukere  
- **Håndtering av øktlivssyklus**: Implementer riktig utløp, rotasjon og ugyldiggjøring for å begrense sårbarhetsvinduer  
- **Transport-sikkerhet**: Obligatorisk HTTPS for all kommunikasjon for å forhindre avlytting av økt-ID-er  

### Problemet med forvirlet stedfortreder

**Problemet med forvirlet stedfortreder** oppstår når MCP-servere fungerer som autentiseringsproxyer mellom klienter og tredjepartstjenester, noe som skaper muligheter for autorisasjonsomgåelse gjennom utnyttelse av statiske klient-ID-er.

#### **Angrepsmekanismer og risikoer**

- **Samtykkebypass via informasjonskapsler**: Tidligere brukerautentisering oppretter samtykkekapsler som angripere utnytter gjennom ondsinnede autorisasjonsforespørsler med manipulerte omdirigerings-URI-er  
- **Tyveri av autorisasjonskode**: Eksisterende samtykkekapsler kan føre til at autorisasjonsservere hopper over samtykkeskjermer, og omdirigerer koder til angriperstyrte endepunkter  
- **Uautorisert API-tilgang**: Stjålne autorisasjonskoder muliggjør tokenutveksling og brukerimitasjon uten eksplisitt godkjenning  

#### **Tiltaksstrategier**

**Obligatoriske kontroller:**
- **Eksplisitte samtykkekrav**: MCP-proxyservere som bruker statiske klient-ID-er **MÅ** innhente brukersamtykke for hver dynamisk registrerte klient  
- **Implementering av OAuth 2.1-sikkerhet**: Følg gjeldende OAuth-sikkerhetspraksis, inkludert PKCE (Proof Key for Code Exchange) for alle autorisasjonsforespørsler  
- **Streng klientvalidering**: Implementer grundig validering av omdirigerings-URI-er og klientidentifikatorer for å forhindre utnyttelse  

### Sårbarheter ved token-gjennomstrømming  

**Token-gjennomstrømming** representerer et eksplisitt antipattern der MCP-servere aksepterer klienttokens uten riktig validering og videresender dem til nedstrøms-API-er, noe som bryter MCP-autorisasjonsspesifikasjoner.

#### **Sikkerhetsimplikasjoner**

- **Omgåelse av kontroller**: Direkte bruk av klient-til-API-tokens omgår kritiske kontroller som hastighetsbegrensning, validering og overvåking  
- **Korrupsjon av revisjonsspor**: Tokens utstedt oppstrøms gjør klientidentifikasjon umulig, noe som ødelegger muligheten for hendelsesundersøkelser  
- **Proxy-basert dataeksfiltrering**: Uvaliderte tokens gjør det mulig for ondsinnede aktører å bruke servere som proxyer for uautorisert datatilgang  
- **Brudd på tillitsgrenser**: Tillitsforutsetningene til nedstrømstjenester kan brytes når tokenopprinnelse ikke kan verifiseres  
- **Utvidelse av angrep på flere tjenester**: Kompromitterte tokens akseptert på tvers av flere tjenester muliggjør lateral bevegelse  

#### **Påkrevde sikkerhetskontroller**

**Ikke-forhandlingsbare krav:**
- **Tokenvalidering**: MCP-servere **MÅ IKKE** akseptere tokens som ikke eksplisitt er utstedt for MCP-serveren  
- **Publikumsverifisering**: Valider alltid at tokenets publikumsfelt samsvarer med MCP-serverens identitet  
- **Riktig tokenlivssyklus**: Implementer kortlivede tilgangstokens med sikre rotasjonspraksiser  

## Forsyningskjedesikkerhet for AI-systemer

Forsyningskjedesikkerhet har utviklet seg utover tradisjonelle programvareavhengigheter til å omfatte hele AI-økosystemet. Moderne MCP-implementeringer må nøye verifisere og overvåke alle AI-relaterte komponenter, da hver av dem introduserer potensielle sårbarheter som kan kompromittere systemets integritet.

### Utvidede AI-forsyningskjedekomponenter

**Tradisjonelle programvareavhengigheter:**
- Åpen kildekode-biblioteker og rammeverk  
- Containerbilder og basissystemer  
- Utviklingsverktøy og byggelinjer  
- Infrastrukturkomponenter og tjenester  

**AI-spesifikke forsyningskjedeelementer:**
- **Grunnmodeller**: Forhåndstrente modeller fra ulike leverandører som krever verifisering av opprinnelse  
- **Embedding-tjenester**: Eksterne vektorisering- og semantiske søketjenester  
- **Kontekstleverandører**: Datakilder, kunnskapsbaser og dokumentlagre  
- **Tredjeparts-API-er**: Eksterne AI-tjenester, ML-pipelines og dataprosesseringsendepunkter  
- **Modellartefakter**: Vekter, konfigurasjoner og finjusterte modellvarianter  
- **Treningsdatasett**: Datasett brukt til modelltrening og finjustering  

### Omfattende strategi for forsyningskjedesikkerhet

#### **Komponentverifisering og tillit**
- **Validering av opprinnelse**: Verifiser opprinnelse, lisensiering og integritet for alle AI-komponenter før integrasjon  
- **Sikkerhetsvurdering**: Utfør sårbarhetsskanninger og sikkerhetsgjennomganger for modeller, datakilder og AI-tjenester  
- **Rykteanalyse**: Evaluer sikkerhetspraksis og historikk for AI-tjenesteleverandører  
- **Samsvarsverifisering**: Sørg for at alle komponenter oppfyller organisasjonens sikkerhets- og regulatoriske krav  

#### **Sikre distribusjonslinjer**  
- **Automatisert CI/CD-sikkerhet**: Integrer sikkerhetsskanning gjennom hele automatiserte distribusjonslinjer  
- **Artefaktintegritet**: Implementer kryptografisk verifisering for alle distribuerte artefakter (kode, modeller, konfigurasjoner)  
- **Trinnvis distribusjon**: Bruk gradvise distribusjonsstrategier med sikkerhetsvalidering på hvert trinn  
- **Pålitelige artefaktlagre**: Distribuer kun fra verifiserte, sikre artefaktregistre og lagre  

#### **Kontinuerlig overvåking og respons**
- **Avhengighetsskanning**: Løpende sårbarhetsovervåking for alle programvare- og AI-komponentavhengigheter  
- **Modellovervåking**: Kontinuerlig vurdering av modellatferd, ytelsesdrift og sikkerhetsavvik  
- **Tjenestehelseovervåking**: Overvåk eksterne AI-tjenester for tilgjengelighet, sikkerhetshendelser og policyendringer  
- **Trusselintelligensintegrasjon**: Inkluder trusselstrømmer spesifikke for AI- og ML-sikkerhetsrisikoer  

#### **Tilgangskontroll og minst privilegium**
- **Komponentnivå-tillatelser**: Begrens tilgang til modeller, data og tjenester basert på forretningsbehov  
- **Håndtering av tjenestekontoer**: Implementer dedikerte tjenestekontoer med minimale nødvendige tillatelser  
- **Nettverkssegmentering**: Isoler AI-komponenter og begrens nettverkstilgang mellom tjenester  
- **API-gateway-kontroller**: Bruk sentraliserte API-gatewayer for å kontrollere og overvåke tilgang til eksterne AI-tjenester  

#### **Hendelsesrespons og gjenoppretting**
- **Raske responsprosedyrer**: Etablerte prosesser for å oppdatere eller erstatte kompromitterte AI-komponenter  
- **Rotasjon av legitimasjon**: Automatiserte systemer for å rotere hemmeligheter, API-nøkler og tjenestekredentialer  
- **Tilbakerullingskapabiliteter**: Evne til raskt å gå tilbake til tidligere kjente gode versjoner av AI-komponenter  
- **Gjenoppretting etter forsyningskjedeangrep**: Spesifikke prosedyrer for å håndtere kompromitteringer i oppstrøms AI-tjenester  

### Microsofts sikkerhetsverktøy og integrasjon

**GitHub Advanced Security** tilbyr omfattende beskyttelse for forsyningskjeden, inkludert:
- **Hemmelighetsskanning**: Automatisk deteksjon av legitimasjon, API-nøkler og tokens i repositorier  
- **Avhengighetsskanning**: Sårbarhetsvurdering for åpen kildekode-avhengigheter og biblioteker  
- **CodeQL-analyse**: Statisk kodeanalyse for sikkerhetssårbarheter og kodeproblemer  
- **Innsikt i forsyningskjeden**: Synlighet i helsen og sikkerhetsstatusen til avhengigheter  

**Azure DevOps og Azure Repos-integrasjon:**
- Sømløs integrasjon av sikkerhetsskanning på tvers av Microsofts utviklingsplattformer  
- Automatiserte sikkerhetssjekker i Azure Pipelines for AI-arbeidsbelastninger  
- Policyhåndhevelse for sikker distribusjon av AI-komponenter  

**Microsofts interne praksis:**
Microsoft implementerer omfattende sikkerhetspraksis for forsyningskjeden på tvers av alle produkter. Lær om velprøvde tilnærminger i [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Microsoft Sikkerhetsløsninger**
- [Microsoft Prompt Shields Dokumentasjon](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety Service](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID Sikkerhet](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Azure Token Management Beste Praksis](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Avansert Sikkerhet](https://github.com/security/advanced-security)

### **Implementeringsguider og Opplæringer**
- [Azure API Management som MCP Autentiseringsgateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID Autentisering med MCP Servere](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Sikker Tokenlagring og Kryptering (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps og Forsyningskjede Sikkerhet**
- [Azure DevOps Sikkerhet](https://azure.microsoft.com/products/devops)
- [Azure Repos Sikkerhet](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft Forsyningskjede Sikkerhetsreise](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Tilleggsdokumentasjon om Sikkerhet**

For omfattende sikkerhetsveiledning, se disse spesialiserte dokumentene i denne seksjonen:

- **[MCP Sikkerhets Beste Praksis 2025](./mcp-security-best-practices-2025.md)** - Fullstendige beste praksiser for MCP-implementeringer
- **[Azure Content Safety Implementering](./azure-content-safety-implementation.md)** - Praktiske eksempler på implementering av Azure Content Safety-integrasjon  
- **[MCP Sikkerhetskontroller 2025](./mcp-security-controls-2025.md)** - Nyeste sikkerhetskontroller og teknikker for MCP-distribusjoner
- **[MCP Beste Praksis Hurtigreferanse](./mcp-best-practices.md)** - Hurtigreferanse for essensielle MCP-sikkerhetspraksiser

---

## Hva er Neste

Neste: [Kapittel 3: Kom i Gang](../03-GettingStarted/README.md)

**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi tilstreber nøyaktighet, vær oppmerksom på at automatiserte oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på sitt opprinnelige språk bør anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.