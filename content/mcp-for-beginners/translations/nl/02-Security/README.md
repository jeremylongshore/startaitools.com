<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T16:30:26+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "nl"
}
-->
# MCP Beveiliging: Uitgebreide Bescherming voor AI-Systemen

[![MCP Beveiligingsrichtlijnen](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.nl.png)](https://youtu.be/88No8pw706o)

_(Klik op de afbeelding hierboven om de video van deze les te bekijken)_

Beveiliging is essentieel bij het ontwerpen van AI-systemen, en daarom geven we hier prioriteit aan in onze tweede sectie. Dit sluit aan bij Microsoft's **Secure by Design**-principe uit het [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Het Model Context Protocol (MCP) biedt krachtige nieuwe mogelijkheden voor AI-gedreven applicaties, maar introduceert ook unieke beveiligingsuitdagingen die verder gaan dan traditionele software risico's. MCP-systemen worden geconfronteerd met zowel bekende beveiligingsproblemen (zoals veilig coderen, minimaal benodigde rechten, en beveiliging van de toeleveringsketen) als nieuwe AI-specifieke bedreigingen, waaronder promptinjectie, toolvergiftiging, sessiekaping, confused deputy-aanvallen, token-passthrough kwetsbaarheden, en dynamische capaciteitswijzigingen.

Deze les behandelt de meest kritieke beveiligingsrisico's bij MCP-implementaties, zoals authenticatie, autorisatie, overmatige rechten, indirecte promptinjectie, sessiebeveiliging, confused deputy-problemen, tokenbeheer en kwetsbaarheden in de toeleveringsketen. Je leert praktische controles en best practices om deze risico's te beperken, terwijl je gebruik maakt van Microsoft-oplossingen zoals Prompt Shields, Azure Content Safety en GitHub Advanced Security om je MCP-implementatie te versterken.

## Leerdoelen

Aan het einde van deze les kun je:

- **MCP-specifieke bedreigingen identificeren**: Herken unieke beveiligingsrisico's in MCP-systemen, zoals promptinjectie, toolvergiftiging, overmatige rechten, sessiekaping, confused deputy-problemen, token-passthrough kwetsbaarheden en risico's in de toeleveringsketen
- **Beveiligingscontroles toepassen**: Voer effectieve maatregelen uit, zoals robuuste authenticatie, toegang met minimaal benodigde rechten, veilig tokenbeheer, sessiebeveiligingscontroles en verificatie van de toeleveringsketen
- **Microsoft-beveiligingsoplossingen gebruiken**: Begrijp en implementeer Microsoft Prompt Shields, Azure Content Safety en GitHub Advanced Security voor MCP-werkbelastingbescherming
- **Toolbeveiliging valideren**: Erken het belang van validatie van toolmetadata, monitoring van dynamische wijzigingen en verdediging tegen indirecte promptinjectie-aanvallen
- **Best practices integreren**: Combineer gevestigde beveiligingsprincipes (zoals veilig coderen, serverhardening, zero trust) met MCP-specifieke controles voor uitgebreide bescherming

# MCP Beveiligingsarchitectuur & Controles

Moderne MCP-implementaties vereisen gelaagde beveiligingsbenaderingen die zowel traditionele softwarebeveiliging als AI-specifieke bedreigingen aanpakken. De snel evoluerende MCP-specificatie blijft zijn beveiligingscontroles verbeteren, waardoor een betere integratie met bedrijfsbeveiligingsarchitecturen en gevestigde best practices mogelijk wordt.

Onderzoek uit het [Microsoft Digital Defense Report](https://aka.ms/mddr) toont aan dat **98% van de gemelde inbreuken voorkomen had kunnen worden door robuuste beveiligingshygiëne**. De meest effectieve beschermingsstrategie combineert fundamentele beveiligingspraktijken met MCP-specifieke controles—bewezen basisbeveiligingsmaatregelen blijven het meest impactvol bij het verminderen van het totale beveiligingsrisico.

## Huidige Beveiligingslandschap

> **Note:** Deze informatie weerspiegelt MCP-beveiligingsstandaarden vanaf **18 augustus 2025**. Het MCP-protocol evolueert snel, en toekomstige implementaties kunnen nieuwe authenticatiepatronen en verbeterde controles introduceren. Raadpleeg altijd de actuele [MCP Specificatie](https://spec.modelcontextprotocol.io/), [MCP GitHub-repository](https://github.com/modelcontextprotocol), en [documentatie over beveiligingsbest practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) voor de meest recente richtlijnen.

### Evolutie van MCP Authenticatie

De MCP-specificatie heeft aanzienlijke vooruitgang geboekt in zijn aanpak van authenticatie en autorisatie:

- **Oorspronkelijke aanpak**: Vroege specificaties vereisten dat ontwikkelaars aangepaste authenticatieservers implementeerden, waarbij MCP-servers fungeerden als OAuth 2.0 Authorization Servers die gebruikersauthenticatie rechtstreeks beheerden
- **Huidige standaard (2025-06-18)**: Bijgewerkte specificatie stelt MCP-servers in staat authenticatie te delegeren aan externe identiteitsproviders (zoals Microsoft Entra ID), wat de beveiligingspositie verbetert en de implementatiecomplexiteit vermindert
- **Transportlaagbeveiliging**: Verbeterde ondersteuning voor veilige transportmechanismen met correcte authenticatiepatronen voor zowel lokale (STDIO) als externe (Streamable HTTP) verbindingen

## Authenticatie & Autorisatie Beveiliging

### Huidige Beveiligingsuitdagingen

Moderne MCP-implementaties worden geconfronteerd met verschillende authenticatie- en autorisatie-uitdagingen:

### Risico's & Bedreigingsvectoren

- **Misgeconfigureerde autorisatielogica**: Foutieve implementatie van autorisatie in MCP-servers kan gevoelige gegevens blootstellen en toegang controles onjuist toepassen
- **OAuth-tokencompromis**: Diefstal van lokale MCP-servertokens stelt aanvallers in staat servers te imiteren en toegang te krijgen tot downstream-services
- **Token-passthrough kwetsbaarheden**: Onjuiste tokenverwerking creëert omzeiling van beveiligingscontroles en hiaten in verantwoordelijkheid
- **Overmatige rechten**: Over-geprivilegieerde MCP-servers schenden principes van minimaal benodigde rechten en vergroten het aanvalsoppervlak

#### Token-passthrough: Een Kritiek Anti-Patroon

**Token-passthrough is expliciet verboden** in de huidige MCP-autorisatiespecificatie vanwege ernstige beveiligingsimplicaties:

##### Omzeiling van Beveiligingscontroles
- MCP-servers en downstream-API's implementeren kritieke beveiligingscontroles (zoals rate limiting, verzoekvalidatie, verkeersmonitoring) die afhankelijk zijn van correcte tokenvalidatie
- Direct gebruik van client-naar-API-tokens omzeilt deze essentiële beschermingen, wat de beveiligingsarchitectuur ondermijnt

##### Verantwoordelijkheid & Audituitdagingen  
- MCP-servers kunnen geen onderscheid maken tussen clients die upstream-uitgegeven tokens gebruiken, wat audit trails verbreekt
- Logs van downstream-resource servers tonen misleidende verzoekbronnen in plaats van daadwerkelijke MCP-serverintermediairs
- Incidentonderzoek en compliance-audits worden aanzienlijk moeilijker

##### Gegevensuitvoeringsrisico's
- Ongevalideerde tokenclaims stellen kwaadwillenden met gestolen tokens in staat MCP-servers te gebruiken als proxy's voor gegevensuitvoer
- Schendingen van vertrouwensgrenzen maken ongeautoriseerde toegangspatronen mogelijk die bedoelde beveiligingscontroles omzeilen

##### Multi-Service Aanvalsvectoren
- Gecompromitteerde tokens die door meerdere services worden geaccepteerd, maken laterale bewegingen mogelijk tussen verbonden systemen
- Vertrouwensveronderstellingen tussen services kunnen worden geschonden wanneer tokenbronnen niet kunnen worden geverifieerd

### Beveiligingscontroles & Maatregelen

**Kritieke Beveiligingsvereisten:**

> **VERPLICHT**: MCP-servers **MOETEN GEEN** tokens accepteren die niet expliciet zijn uitgegeven voor de MCP-server

#### Authenticatie & Autorisatie Controles

- **Grondige Autorisatiecontrole**: Voer uitgebreide audits uit van MCP-serverautorisatielogica om ervoor te zorgen dat alleen bedoelde gebruikers en clients toegang hebben tot gevoelige bronnen
  - **Implementatiegids**: [Azure API Management als Authenticatie Gateway voor MCP-servers](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Identiteitsintegratie**: [Microsoft Entra ID gebruiken voor MCP-serverauthenticatie](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Veilig Tokenbeheer**: Implementeer [Microsoft's best practices voor tokenvalidatie en levenscyclus](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Valideer token audience claims die overeenkomen met MCP-serveridentiteit
  - Implementeer correcte tokenrotatie- en vervalbeleid
  - Voorkom token-replay-aanvallen en ongeautoriseerd gebruik

- **Beveiligde Tokenopslag**: Beveilig tokenopslag met encryptie zowel in rust als tijdens transport
  - **Best Practices**: [Richtlijnen voor veilige tokenopslag en encryptie](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementatie van Toegangscontrole

- **Principe van Minimaal Benodigde Rechten**: Geef MCP-servers alleen de minimale rechten die nodig zijn voor de beoogde functionaliteit
  - Regelmatige rechtenreviews en updates om privilege-uitbreiding te voorkomen
  - **Microsoft Documentatie**: [Beveiligde toegang met minimaal benodigde rechten](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Rolgebaseerde Toegangscontrole (RBAC)**: Implementeer fijnmazige roltoewijzingen
  - Beperk rollen strikt tot specifieke bronnen en acties
  - Vermijd brede of onnodige rechten die het aanvalsoppervlak vergroten

- **Continue Rechtenmonitoring**: Implementeer doorlopende audits en monitoring van toegang
  - Monitor gebruikspatronen van rechten op anomalieën
  - Los overmatige of ongebruikte rechten snel op

## AI-Specifieke Beveiligingsbedreigingen

### Promptinjectie & Toolmanipulatie-aanvallen

Moderne MCP-implementaties worden geconfronteerd met geavanceerde AI-specifieke aanvalsvectoren die traditionele beveiligingsmaatregelen niet volledig kunnen aanpakken:

#### **Indirecte Promptinjectie (Cross-Domain Promptinjectie)**

**Indirecte Promptinjectie** is een van de meest kritieke kwetsbaarheden in MCP-gestuurde AI-systemen. Aanvallers verbergen kwaadaardige instructies in externe inhoud—documenten, webpagina's, e-mails of gegevensbronnen—die AI-systemen vervolgens verwerken als legitieme opdrachten.

**Aanvalsscenario's:**
- **Documentgebaseerde Injectie**: Kwaadaardige instructies verborgen in verwerkte documenten die onbedoelde AI-acties veroorzaken
- **Webinhoud Exploitatie**: Gecompromitteerde webpagina's met ingebedde prompts die AI-gedrag manipuleren bij het scrapen
- **E-mailgebaseerde Aanvallen**: Kwaadaardige prompts in e-mails die AI-assistenten informatie laten lekken of ongeautoriseerde acties laten uitvoeren
- **Gegevensbronvervuiling**: Gecompromitteerde databases of API's die besmette inhoud leveren aan AI-systemen

**Impact in de praktijk**: Deze aanvallen kunnen leiden tot gegevensuitvoer, privacyschendingen, het genereren van schadelijke inhoud en manipulatie van gebruikersinteracties. Voor gedetailleerde analyse, zie [Promptinjectie in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Promptinjectie Aanval Diagram](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.nl.png)

#### **Toolvergiftiging-aanvallen**

**Toolvergiftiging** richt zich op de metadata die MCP-tools definiëren, waarbij wordt misbruik gemaakt van hoe LLM's toolbeschrijvingen en parameters interpreteren om uitvoeringsbeslissingen te nemen.

**Aanvalsmechanismen:**
- **Manipulatie van Metadata**: Aanvallers injecteren kwaadaardige instructies in toolbeschrijvingen, parameterdefinities of gebruiksvoorbeelden
- **Onzichtbare Instructies**: Verborgen prompts in toolmetadata die door AI-modellen worden verwerkt maar onzichtbaar zijn voor menselijke gebruikers
- **Dynamische Toolwijziging ("Rug Pulls")**: Tools die door gebruikers zijn goedgekeurd, worden later gewijzigd om kwaadaardige acties uit te voeren zonder dat gebruikers dit merken
- **Parameterinjectie**: Kwaadaardige inhoud ingebed in toolparameterschema's die modelgedrag beïnvloeden

**Risico's bij Gehoste Servers**: Remote MCP-servers brengen verhoogde risico's met zich mee, omdat tooldefinities kunnen worden bijgewerkt na de initiële goedkeuring door gebruikers, waardoor scenario's ontstaan waarin eerder veilige tools kwaadaardig worden. Voor uitgebreide analyse, zie [Toolvergiftiging-aanvallen (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Toolinjectie Aanval Diagram](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.nl.png)

#### **Aanvullende AI-aanvalsvectoren**

- **Cross-Domain Promptinjectie (XPIA)**: Geavanceerde aanvallen die inhoud uit meerdere domeinen gebruiken om beveiligingscontroles te omzeilen
- **Dynamische Capaciteitswijziging**: Real-time wijzigingen in toolcapaciteiten die ontsnappen aan initiële beveiligingsbeoordelingen
- **Context Window Poisoning**: Aanvallen die grote contextvensters manipuleren om kwaadaardige instructies te verbergen
- **Modelverwarringsaanvallen**: Misbruik van modellimieten om onvoorspelbaar of onveilig gedrag te creëren

### Impact van AI-beveiligingsrisico's

**Gevolgen met hoge impact:**
- **Gegevensuitvoer**: Ongeautoriseerde toegang en diefstal van gevoelige bedrijfs- of persoonlijke gegevens
- **Privacyschendingen**: Blootstelling van persoonlijk identificeerbare informatie (PII) en vertrouwelijke bedrijfsgegevens  
- **Systeemmanipulatie**: Onbedoelde wijzigingen in kritieke systemen en workflows
- **Diefstal van Inloggegevens**: Compromittering van authenticatietokens en service-inloggegevens
- **Laterale Beweging**: Gebruik van gecompromitteerde AI-systemen als draaipunt voor bredere netwerkaanvallen

### Microsoft AI Beveiligingsoplossingen

#### **AI Prompt Shields: Geavanceerde Bescherming tegen Injectie-aanvallen**

Microsoft **AI Prompt Shields** bieden uitgebreide verdediging tegen zowel directe als indirecte promptinjectie-aanvallen via meerdere beveiligingslagen:

##### **Kernbeschermingsmechanismen:**

1. **Geavanceerde Detectie & Filtering**
   - Machine learning-algoritmen en NLP-technieken detecteren kwaadaardige instructies in externe inhoud
   - Real-time analyse van documenten, webpagina's, e-mails en gegevensbronnen op ingebedde bedreigingen
   - Contextueel begrip van legitieme versus kwaadaardige promptpatronen

2. **Spotlighting Technieken**  
   - Onderscheidt tussen vertrouwde systeeminstructies en mogelijk gecompromitteerde externe inputs
   - Teksttransformatiemethoden die de relevantie voor modellen verbeteren terwijl kwaadaardige inhoud wordt geïsoleerd
   - Helpt AI-systemen de juiste instructiehiërarchie te behouden en geïnjecteerde opdrachten te negeren

3. **Delimiter & Datamarking Systemen**
   - Expliciete grensdefinitie tussen vertrouwde systeemberichten en externe invoertekst
   - Speciale markeringen benadrukken grenzen tussen vertrouwde en niet-vertrouwde gegevensbronnen
   - Duidelijke scheiding voorkomt instructieverwarring en ongeautoriseerde opdrachtuitvoering

4. **Continue Dreigingsinformatie**
   - Microsoft monitort voortdurend opkomende aanvalspatronen en werkt verdedigingen bij
   - Proactieve dreigingsjacht op nieuwe injectietechnieken en aanvalsvectoren
   - Regelmatige updates van beveiligingsmodellen om effectief te blijven tegen evoluerende bedreigingen

5. **Azure Content Safety Integratie**
   - Onderdeel van de uitgebreide Azure AI Content Safety-suite
   - Aanvullende detectie voor jailbreakpogingen, schadelijke inhoud en schendingen van beveiligingsbeleid
   - Geïntegreerde beveiligingscontroles over AI-applicatiecomponenten

**Implementatiebronnen**: [Microsoft Prompt Shields Documentatie](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)

![Microsoft Prompt Shields Bescherming](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.nl.png)


## Geavanceerde MCP Beveiligingsbedreigingen

### Sessiekaping Kwetsbaarheden

**Sessiekaping** vormt een kritieke aanvalsvector in stateful MCP-implementaties waarbij onbevoegde partijen legitieme sessie-ID's verkrijgen en misbruiken om clients te imiteren en ongeautoriseerde acties uit te voeren.

#### **Aanvalsscenario's & Risico's**

- **Sessiekaping Promptinjectie**: Aanvallers met gestolen sessie-ID's injecteren kwaadaardige gebeurtenissen in servers die sessiestatus delen, wat mogelijk schadelijke acties of toegang tot gevoelige gegevens veroorzaakt
- **Directe Imitatie**: Gestolen sessie-ID's stellen aanvallers in staat directe MCP-serveroproepen te doen die authenticatie omzeilen, waardoor ze als legitieme gebruikers worden behandeld
- **Gecompromitteerde Hervatbare Streams**: Aanvallers kunnen verzoeken voortijdig beëindigen, waardoor legitieme clients hervatten met mogelijk kwaadaardige inhoud

#### **Beveiligingscontroles voor Sessiebeheer**

**Kritieke Vereisten:**
- **Autorisatieverificatie**: MCP-servers die autorisatie implementeren **MOETEN** ALLE inkomende verzoeken verifiëren en **MOETEN GEEN** sessies gebruiken voor authenticatie
- **Veilige sessiegeneratie**: Gebruik cryptografisch veilige, niet-deterministische sessie-ID's die worden gegenereerd met veilige willekeurige nummergeneratoren  
- **Gebruikersspecifieke koppeling**: Koppel sessie-ID's aan gebruikersspecifieke informatie met formaten zoals `<user_id>:<session_id>` om misbruik van sessies tussen gebruikers te voorkomen  
- **Beheer van sessielevenscyclus**: Implementeer correcte vervaldatum, rotatie en ongeldigverklaring om kwetsbaarheidsvensters te beperken  
- **Transportbeveiliging**: Verplicht HTTPS voor alle communicatie om onderschepping van sessie-ID's te voorkomen  

### Probleem van de verwarde tussenpersoon

Het **probleem van de verwarde tussenpersoon** doet zich voor wanneer MCP-servers optreden als authenticatieproxies tussen clients en externe diensten, waardoor mogelijkheden ontstaan voor autorisatieomzeiling via statische client-ID-exploitatie.

#### **Aanvalsmechanismen & risico's**

- **Omzeiling van cookie-gebaseerde toestemming**: Eerdere gebruikersauthenticatie creëert toestemmingscookies die aanvallers misbruiken via kwaadaardige autorisatieverzoeken met aangepaste redirect-URI's  
- **Diefstal van autorisatiecodes**: Bestaande toestemmingscookies kunnen ervoor zorgen dat autorisatieservers toestemmingsschermen overslaan, waardoor codes worden doorgestuurd naar door aanvallers gecontroleerde eindpunten  
- **Ongeautoriseerde API-toegang**: Gestolen autorisatiecodes maken tokenuitwisseling en gebruikersimitatie mogelijk zonder expliciete goedkeuring  

#### **Mitigatiestrategieën**

**Verplichte controles:**
- **Expliciete toestemmingsvereisten**: MCP-proxyservers die statische client-ID's gebruiken **MOETEN** gebruikers toestemming vragen voor elke dynamisch geregistreerde client  
- **OAuth 2.1 beveiligingsimplementatie**: Volg de huidige OAuth-beveiligingsrichtlijnen, inclusief PKCE (Proof Key for Code Exchange) voor alle autorisatieverzoeken  
- **Strikte clientvalidatie**: Implementeer rigoureuze validatie van redirect-URI's en client-ID's om exploitatie te voorkomen  

### Kwetsbaarheden bij token-doorvoer  

**Token-doorvoer** is een expliciet anti-patroon waarbij MCP-servers clienttokens accepteren zonder juiste validatie en deze doorsturen naar downstream-API's, wat in strijd is met MCP-autorisatiespecificaties.

#### **Beveiligingsimplicaties**

- **Omzeiling van controles**: Directe client-naar-API-tokengebruik omzeilt cruciale limieten, validatie en monitoring  
- **Corruptie van auditsporen**: Tokens die upstream zijn uitgegeven maken clientidentificatie onmogelijk, wat incidentonderzoek belemmert  
- **Proxy-gebaseerde data-exfiltratie**: Niet-gevalideerde tokens stellen kwaadwillenden in staat servers te gebruiken als proxy's voor ongeautoriseerde gegevens toegang  
- **Schending van vertrouwensgrenzen**: Vertrouwensassumpties van downstream-diensten kunnen worden geschonden wanneer de oorsprong van tokens niet kan worden geverifieerd  
- **Uitbreiding van aanvallen tussen diensten**: Gecompromitteerde tokens die worden geaccepteerd door meerdere diensten maken laterale beweging mogelijk  

#### **Vereiste beveiligingscontroles**

**Niet-onderhandelbare vereisten:**
- **Tokenvalidatie**: MCP-servers **MOETEN GEEN** tokens accepteren die niet expliciet zijn uitgegeven voor de MCP-server  
- **Audience-verificatie**: Controleer altijd of de audience-claims van tokens overeenkomen met de identiteit van de MCP-server  
- **Correcte tokenlevenscyclus**: Implementeer kortlevende toegangstokens met veilige rotatiepraktijken  

## Beveiliging van de toeleveringsketen voor AI-systemen

Beveiliging van de toeleveringsketen is geëvolueerd voorbij traditionele softwareafhankelijkheden en omvat nu het hele AI-ecosysteem. Moderne MCP-implementaties moeten alle AI-gerelateerde componenten rigoureus verifiëren en monitoren, aangezien elk potentiële kwetsbaarheden introduceert die de systeemintegriteit kunnen aantasten.

### Uitgebreide AI-toeleveringsketencomponenten

**Traditionele softwareafhankelijkheden:**
- Open-source bibliotheken en frameworks  
- Containerafbeeldingen en basissystemen  
- Ontwikkeltools en build-pijplijnen  
- Infrastructuurcomponenten en -diensten  

**AI-specifieke toeleveringsketenelementen:**
- **Foundation Models**: Voorgetrainde modellen van verschillende aanbieders die verificatie van herkomst vereisen  
- **Embedding Services**: Externe vectorisatie- en semantische zoekdiensten  
- **Context Providers**: Gegevensbronnen, kennisbanken en documentrepositories  
- **Externe API's**: Externe AI-diensten, ML-pijplijnen en gegevensverwerkingseindpunten  
- **Modelartefacten**: Gewichten, configuraties en fijn-afgestemde modelvarianten  
- **Trainingsgegevensbronnen**: Datasets gebruikt voor modeltraining en fijn-afstemming  

### Uitgebreide strategie voor beveiliging van de toeleveringsketen

#### **Componentverificatie & vertrouwen**
- **Herkomstvalidatie**: Verifieer de oorsprong, licenties en integriteit van alle AI-componenten vóór integratie  
- **Beveiligingsbeoordeling**: Voer kwetsbaarheidsscans en beveiligingsreviews uit voor modellen, gegevensbronnen en AI-diensten  
- **Reputatieanalyse**: Evalueer het beveiligingsrecord en de praktijken van AI-dienstverleners  
- **Compliance-verificatie**: Zorg ervoor dat alle componenten voldoen aan organisatorische beveiligings- en regelgevingsvereisten  

#### **Veilige implementatiepijplijnen**  
- **Geautomatiseerde CI/CD-beveiliging**: Integreer beveiligingsscans in geautomatiseerde implementatiepijplijnen  
- **Artefactintegriteit**: Implementeer cryptografische verificatie voor alle geïmplementeerde artefacten (code, modellen, configuraties)  
- **Gefaseerde implementatie**: Gebruik progressieve implementatiestrategieën met beveiligingsvalidatie in elke fase  
- **Vertrouwde artefactrepositories**: Implementeer alleen vanuit geverifieerde, veilige artefactregisters en repositories  

#### **Continue monitoring & respons**
- **Afhankelijkheidsscanning**: Voortdurende kwetsbaarheidsmonitoring voor alle software- en AI-componentafhankelijkheden  
- **Modelmonitoring**: Continue beoordeling van modelgedrag, prestatiedrift en beveiligingsanomalieën  
- **Servicegezondheidstracking**: Monitor externe AI-diensten op beschikbaarheid, beveiligingsincidenten en beleidswijzigingen  
- **Integratie van dreigingsinformatie**: Gebruik dreigingsfeeds specifiek voor AI- en ML-beveiligingsrisico's  

#### **Toegangscontrole & minimaal privilege**
- **Componentniveau-permissies**: Beperk toegang tot modellen, gegevens en diensten op basis van zakelijke noodzaak  
- **Beheer van serviceaccounts**: Implementeer toegewijde serviceaccounts met minimale vereiste permissies  
- **Netwerksegmentatie**: Isoleer AI-componenten en beperk netwerktoegang tussen diensten  
- **API-gatewaycontroles**: Gebruik gecentraliseerde API-gateways om toegang tot externe AI-diensten te controleren en te monitoren  

#### **Incidentrespons & herstel**
- **Snelle responsprocedures**: Vastgestelde processen voor het patchen of vervangen van gecompromitteerde AI-componenten  
- **Credentialrotatie**: Geautomatiseerde systemen voor het roteren van geheimen, API-sleutels en servicecredentials  
- **Rollbackmogelijkheden**: Mogelijkheid om snel terug te keren naar eerdere bekende goede versies van AI-componenten  
- **Herstel van toeleveringsketenbreuken**: Specifieke procedures voor het reageren op compromissen van upstream AI-diensten  

### Microsoft-beveiligingstools & integratie

**GitHub Advanced Security** biedt uitgebreide bescherming van de toeleveringsketen, waaronder:  
- **Geheimenscanning**: Geautomatiseerde detectie van credentials, API-sleutels en tokens in repositories  
- **Afhankelijkheidsscanning**: Kwetsbaarheidsbeoordeling voor open-source afhankelijkheden en bibliotheken  
- **CodeQL-analyse**: Statische codeanalyse voor beveiligingskwetsbaarheden en coderingsproblemen  
- **Inzichten in de toeleveringsketen**: Zichtbaarheid in de gezondheid en beveiligingsstatus van afhankelijkheden  

**Azure DevOps & Azure Repos-integratie:**  
- Naadloze integratie van beveiligingsscans in Microsoft-ontwikkelplatforms  
- Geautomatiseerde beveiligingscontroles in Azure Pipelines voor AI-werkbelastingen  
- Beleidsafdwinging voor veilige implementatie van AI-componenten  

**Microsoft interne praktijken:**  
Microsoft implementeert uitgebreide beveiligingspraktijken voor de toeleveringsketen in alle producten. Lees meer over bewezen benaderingen in [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  

## Fundamentele beveiligingspraktijken

MCP-implementaties bouwen voort op de bestaande beveiligingshouding van uw organisatie. Het versterken van fundamentele beveiligingspraktijken verbetert de algehele beveiliging van AI-systemen en MCP-implementaties aanzienlijk.

### Kernbeveiligingsprincipes

#### **Veilige ontwikkelpraktijken**
- **OWASP-naleving**: Bescherm tegen [OWASP Top 10](https://owasp.org/www-project-top-ten/) kwetsbaarheden in webapplicaties  
- **AI-specifieke bescherming**: Implementeer controles voor [OWASP Top 10 voor LLM's](https://genai.owasp.org/download/43299/?tmstv=1731900559)  
- **Veilig geheimenbeheer**: Gebruik toegewijde kluizen voor tokens, API-sleutels en gevoelige configuratiegegevens  
- **End-to-end encryptie**: Implementeer veilige communicatie tussen alle applicatiecomponenten en gegevensstromen  
- **Inputvalidatie**: Rigoureuze validatie van alle gebruikersinvoer, API-parameters en gegevensbronnen  

#### **Verharding van infrastructuur**
- **Multi-factor authenticatie**: Verplichte MFA voor alle administratieve en serviceaccounts  
- **Patchbeheer**: Geautomatiseerd, tijdig patchen van besturingssystemen, frameworks en afhankelijkheden  
- **Integratie van identiteitsproviders**: Gecentraliseerd identiteitsbeheer via enterprise identiteitsproviders (Microsoft Entra ID, Active Directory)  
- **Netwerksegmentatie**: Logische isolatie van MCP-componenten om laterale beweging te beperken  
- **Principe van minimaal privilege**: Minimale vereiste permissies voor alle systeemcomponenten en accounts  

#### **Beveiligingsmonitoring & detectie**
- **Uitgebreide logging**: Gedetailleerde logging van AI-applicatieactiviteiten, inclusief MCP-client-serverinteracties  
- **SIEM-integratie**: Gecentraliseerd beheer van beveiligingsinformatie en -gebeurtenissen voor anomaliedetectie  
- **Gedragsanalyse**: AI-gestuurde monitoring om ongebruikelijke patronen in systeem- en gebruikersgedrag te detecteren  
- **Dreigingsinformatie**: Integratie van externe dreigingsfeeds en indicatoren van compromissen (IOCs)  
- **Incidentrespons**: Goed gedefinieerde procedures voor detectie, respons en herstel van beveiligingsincidenten  

#### **Zero Trust-architectuur**
- **Nooit vertrouwen, altijd verifiëren**: Continue verificatie van gebruikers, apparaten en netwerkverbindingen  
- **Micro-segmentatie**: Granulaire netwerkcontroles die individuele werkbelastingen en diensten isoleren  
- **Identiteitsgerichte beveiliging**: Beveiligingsbeleid gebaseerd op geverifieerde identiteiten in plaats van netwerklocatie  
- **Continue risicobeoordeling**: Dynamische evaluatie van de beveiligingshouding op basis van huidige context en gedrag  
- **Voorwaardelijke toegang**: Toegangscontroles die zich aanpassen op basis van risicofactoren, locatie en apparaatvertrouwen  

### Integratiepatronen voor ondernemingen

#### **Integratie met Microsoft-beveiligingsecosysteem**
- **Microsoft Defender for Cloud**: Uitgebreid beheer van beveiligingshouding in de cloud  
- **Azure Sentinel**: Cloud-native SIEM- en SOAR-mogelijkheden voor bescherming van AI-werkbelastingen  
- **Microsoft Entra ID**: Enterprise identiteits- en toegangsbeheer met voorwaardelijke toegangsbeleid  
- **Azure Key Vault**: Gecentraliseerd geheimenbeheer met hardwarebeveiligingsmodule (HSM) ondersteuning  
- **Microsoft Purview**: Gegevensbeheer en compliance voor AI-gegevensbronnen en workflows  

#### **Compliance & governance**
- **Regelgevingsafstemming**: Zorg ervoor dat MCP-implementaties voldoen aan branchespecifieke compliancevereisten (GDPR, HIPAA, SOC 2)  
- **Gegevensclassificatie**: Correcte categorisatie en behandeling van gevoelige gegevens verwerkt door AI-systemen  
- **Auditsporen**: Uitgebreide logging voor naleving en forensisch onderzoek  
- **Privacycontroles**: Implementatie van privacy-by-design principes in AI-systeemarchitectuur  
- **Wijzigingsbeheer**: Formele processen voor beveiligingsreviews van wijzigingen in AI-systemen  

Deze fundamentele praktijken creëren een robuuste beveiligingsbasis die de effectiviteit van MCP-specifieke beveiligingscontroles verbetert en uitgebreide bescherming biedt voor AI-gestuurde applicaties.

## Belangrijke beveiligingsinzichten

- **Gelaagde beveiligingsaanpak**: Combineer fundamentele beveiligingspraktijken (veilig coderen, minimaal privilege, verificatie van toeleveringsketen, continue monitoring) met AI-specifieke controles voor uitgebreide bescherming  

- **AI-specifiek dreigingslandschap**: MCP-systemen worden geconfronteerd met unieke risico's zoals promptinjectie, toolvergiftiging, sessiekaping, problemen met verwarde tussenpersonen, kwetsbaarheden bij token-doorvoer en overmatige permissies die gespecialiseerde mitigaties vereisen  

- **Authenticatie & autorisatie-excellentie**: Implementeer robuuste authenticatie met externe identiteitsproviders (Microsoft Entra ID), handhaaf correcte tokenvalidatie en accepteer nooit tokens die niet expliciet zijn uitgegeven voor uw MCP-server  

- **Preventie van AI-aanvallen**: Gebruik Microsoft Prompt Shields en Azure Content Safety om indirecte promptinjectie en toolvergiftigingsaanvallen te voorkomen, terwijl u toolmetadata valideert en monitort op dynamische wijzigingen  

- **Sessies & transportbeveiliging**: Gebruik cryptografisch veilige, niet-deterministische sessie-ID's gekoppeld aan gebruikersidentiteiten, implementeer correct beheer van sessielevenscyclus en gebruik sessies nooit voor authenticatie  

- **OAuth-beveiligingsrichtlijnen**: Voorkom aanvallen van verwarde tussenpersonen door expliciete gebruikers toestemming voor dynamisch geregistreerde clients, correcte OAuth 2.1-implementatie met PKCE en strikte validatie van redirect-URI's  

- **Tokenbeveiligingsprincipes**: Vermijd anti-patronen bij token-doorvoer, valideer audience-claims van tokens, implementeer kortlevende tokens met veilige rotatie en behoud duidelijke vertrouwensgrenzen  

- **Uitgebreide beveiliging van de toeleveringsketen**: Behandel alle AI-ecosysteemcomponenten (modellen, embeddings, contextproviders, externe API's) met dezelfde beveiligingsrigor als traditionele softwareafhankelijkheden  

- **Continue evolutie**: Blijf op de hoogte van snel evoluerende MCP-specificaties, draag bij aan beveiligingsstandaarden in de gemeenschap en onderhoud adaptieve beveiligingshoudingen naarmate het protocol zich ontwikkelt  

- **Microsoft-beveiligingsintegratie**: Maak gebruik van het uitgebreide beveiligingsecosysteem van Microsoft (Prompt Shields, Azure Content Safety, GitHub Advanced Security, Entra ID) voor verbeterde bescherming van MCP-implementaties  

## Uitgebreide bronnen

### **Officiële MCP-beveiligingsdocumentatie**
- [MCP-specificatie (Huidig: 2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP-beveiligingsrichtlijnen](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP-autorisatiespecificatie](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  
- [MCP GitHub-repository](https://github.com/modelcontextprotocol)  

### **Beveiligingsstandaarden & richtlijnen**
- [OAuth 2.0 beveiligingsrichtlijnen (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 Web Application Security](https://owasp.org/www-project-top-ten/)  
- [OWASP Top 10 voor Large Language Models](https://genai.owasp.org/download/43299/?tmstv=1731900559)  
- [Microsoft Digital Defense Report](https://aka.ms/mddr)  

### **AI-beveiligingsonderzoek & analyse**
- [Promptinjectie in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)  
- [Toolvergiftigingsaanvallen (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)  
- [MCP-beveiligingsonderzoeksbriefing (Wiz Security)](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)  
### **Microsoft Security-oplossingen**
- [Microsoft Prompt Shields Documentatie](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety Service](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID Beveiliging](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Azure Token Management Best Practices](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Implementatiegidsen & Tutorials**
- [Azure API Management als MCP Authenticatie Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID Authenticatie met MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Veilige Tokenopslag en Encryptie (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps & Beveiliging van de Supply Chain**
- [Azure DevOps Beveiliging](https://azure.microsoft.com/products/devops)
- [Azure Repos Beveiliging](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft Supply Chain Security Journey](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Aanvullende Beveiligingsdocumentatie**

Voor uitgebreide beveiligingsrichtlijnen, raadpleeg de gespecialiseerde documenten in deze sectie:

- **[MCP Security Best Practices 2025](./mcp-security-best-practices-2025.md)** - Volledige beveiligingsrichtlijnen voor MCP-implementaties
- **[Azure Content Safety Implementatie](./azure-content-safety-implementation.md)** - Praktische implementatievoorbeelden voor integratie van Azure Content Safety  
- **[MCP Security Controls 2025](./mcp-security-controls-2025.md)** - Nieuwste beveiligingsmaatregelen en technieken voor MCP-implementaties
- **[MCP Best Practices Quick Reference](./mcp-best-practices.md)** - Snelgids voor essentiële MCP-beveiligingspraktijken

---

## Wat Nu

Volgende: [Hoofdstuk 3: Aan de Slag](../03-GettingStarted/README.md)

**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we ons best doen voor nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.