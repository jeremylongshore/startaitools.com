<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T14:51:57+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "sv"
}
-->
# MCP-säkerhet: Omfattande skydd för AI-system

[![MCP Security Best Practices](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.sv.png)](https://youtu.be/88No8pw706o)

_(Klicka på bilden ovan för att se videon för denna lektion)_

Säkerhet är grundläggande för design av AI-system, vilket är anledningen till att vi prioriterar det som vår andra sektion. Detta är i linje med Microsofts princip **Secure by Design** från [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) introducerar kraftfulla nya möjligheter för AI-drivna applikationer samtidigt som det medför unika säkerhetsutmaningar som går utöver traditionella mjukvarurisker. MCP-system står inför både etablerade säkerhetsproblem (säker kodning, minsta privilegium, leveranskedjesäkerhet) och nya AI-specifika hot som promptinjektion, verktygsförgiftning, sessionkapning, förvirrade ställföreträdarattacker, tokenöverföringssvagheter och dynamisk kapabilitetsmodifiering.

Denna lektion utforskar de mest kritiska säkerhetsriskerna i MCP-implementeringar—inklusive autentisering, auktorisering, överdrivna behörigheter, indirekt promptinjektion, sessionssäkerhet, förvirrade ställföreträdarproblem, tokenhantering och leveranskedjesårbarheter. Du kommer att lära dig praktiska kontroller och bästa praxis för att minska dessa risker samtidigt som du använder Microsoft-lösningar som Prompt Shields, Azure Content Safety och GitHub Advanced Security för att stärka din MCP-distribution.

## Lärandemål

I slutet av denna lektion kommer du att kunna:

- **Identifiera MCP-specifika hot**: Känna igen unika säkerhetsrisker i MCP-system, inklusive promptinjektion, verktygsförgiftning, överdrivna behörigheter, sessionkapning, förvirrade ställföreträdarproblem, tokenöverföringssvagheter och leveranskedjerisker
- **Tillämpa säkerhetskontroller**: Implementera effektiva åtgärder som robust autentisering, åtkomst med minsta privilegium, säker tokenhantering, sessionssäkerhetskontroller och leveranskedjeverifiering
- **Använda Microsofts säkerhetslösningar**: Förstå och distribuera Microsoft Prompt Shields, Azure Content Safety och GitHub Advanced Security för att skydda MCP-arbetsbelastningar
- **Validera verktygssäkerhet**: Erkänna vikten av validering av verktygsmetadata, övervakning av dynamiska förändringar och försvar mot indirekta promptinjektionsattacker
- **Integrera bästa praxis**: Kombinera etablerade säkerhetsgrunder (säker kodning, serverhärdning, zero trust) med MCP-specifika kontroller för omfattande skydd

# MCP-säkerhetsarkitektur och kontroller

Moderna MCP-implementeringar kräver lagerbaserade säkerhetsmetoder som adresserar både traditionell mjukvarusäkerhet och AI-specifika hot. Den snabbt utvecklande MCP-specifikationen fortsätter att förbättra sina säkerhetskontroller, vilket möjliggör bättre integration med företags säkerhetsarkitekturer och etablerade bästa praxis.

Forskning från [Microsoft Digital Defense Report](https://aka.ms/mddr) visar att **98 % av rapporterade intrång skulle kunna förhindras med robust säkerhetshygien**. Den mest effektiva skyddsstrategin kombinerar grundläggande säkerhetsmetoder med MCP-specifika kontroller—beprövade grundläggande säkerhetsåtgärder förblir de mest effektiva för att minska den totala säkerhetsrisken.

## Aktuellt säkerhetslandskap

> **Note:** Denna information återspeglar MCP-säkerhetsstandarder per **18 augusti 2025**. MCP-protokollet utvecklas snabbt, och framtida implementeringar kan introducera nya autentiseringsmönster och förbättrade kontroller. Hänvisa alltid till den aktuella [MCP-specifikationen](https://spec.modelcontextprotocol.io/), [MCP GitHub-repository](https://github.com/modelcontextprotocol) och [dokumentation om säkerhetsbästa praxis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) för den senaste vägledningen.

### Utveckling av MCP-autentisering

MCP-specifikationen har utvecklats avsevärt i sitt tillvägagångssätt för autentisering och auktorisering:

- **Ursprunglig metod**: Tidiga specifikationer krävde att utvecklare implementerade anpassade autentiseringsservrar, där MCP-servrar agerade som OAuth 2.0 Authorization Servers som hanterade användarautentisering direkt
- **Nuvarande standard (2025-06-18)**: Uppdaterad specifikation tillåter MCP-servrar att delegera autentisering till externa identitetsleverantörer (såsom Microsoft Entra ID), vilket förbättrar säkerhetsläget och minskar implementeringskomplexiteten
- **Transportlagersäkerhet**: Förbättrat stöd för säkra transportmekanismer med korrekta autentiseringsmönster för både lokala (STDIO) och fjärranslutningar (Streamable HTTP)

## Säkerhet för autentisering och auktorisering

### Aktuella säkerhetsutmaningar

Moderna MCP-implementeringar står inför flera autentiserings- och auktoriseringsutmaningar:

### Risker och hotvektorer

- **Felkonfigurerad auktoriseringslogik**: Bristfällig auktoriseringsimplementering i MCP-servrar kan exponera känslig data och tillämpa åtkomstkontroller felaktigt
- **OAuth-tokenkompromiss**: Stöld av lokala MCP-servertoken möjliggör för angripare att imitera servrar och få åtkomst till nedströms tjänster
- **Tokenöverföringssvagheter**: Felaktig tokenhantering skapar säkerhetskontrollförbikopplingar och ansvarsgap
- **Överdrivna behörigheter**: MCP-servrar med för stora privilegier bryter mot principen om minsta privilegium och utökar attackytor

#### Tokenöverföring: Ett kritiskt anti-mönster

**Tokenöverföring är uttryckligen förbjudet** i den aktuella MCP-auktoriseringsspecifikationen på grund av allvarliga säkerhetsimplikationer:

##### Förbikoppling av säkerhetskontroller
- MCP-servrar och nedströms-API:er implementerar kritiska säkerhetskontroller (hastighetsbegränsning, begäranvalidering, trafikövervakning) som är beroende av korrekt tokenvalidering
- Direkt användning av klient-till-API-token kringgår dessa viktiga skydd, vilket underminerar säkerhetsarkitekturen

##### Ansvars- och granskningsutmaningar  
- MCP-servrar kan inte skilja mellan klienter som använder uppströmsutfärdade token, vilket bryter granskningsspår
- Loggar från nedströms resursservrar visar vilseledande begäransursprung snarare än faktiska MCP-serverförmedlare
- Incidentutredning och efterlevnadsgranskning blir betydligt svårare

##### Risker för dataexfiltrering
- Ovalidierade tokenanspråk möjliggör för skadliga aktörer med stulna token att använda MCP-servrar som proxyer för dataexfiltrering
- Brott mot förtroendegränser tillåter obehöriga åtkomstmönster som kringgår avsedda säkerhetskontroller

##### Attackvektorer för flera tjänster
- Kompromissade token som accepteras av flera tjänster möjliggör lateral rörelse över anslutna system
- Förtroendeantaganden mellan tjänster kan brytas när tokenursprung inte kan verifieras

### Säkerhetskontroller och åtgärder

**Kritiska säkerhetskrav:**

> **OBLIGATORISKT**: MCP-servrar **FÅR INTE** acceptera några token som inte uttryckligen utfärdats för MCP-servern

#### Autentiserings- och auktoriseringskontroller

- **Noggrann auktoriseringsgranskning**: Utför omfattande granskningar av MCP-serverns auktoriseringslogik för att säkerställa att endast avsedda användare och klienter kan få åtkomst till känsliga resurser
  - **Implementeringsguide**: [Azure API Management som autentiseringsgateway för MCP-servrar](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Identitetsintegration**: [Använda Microsoft Entra ID för MCP-serverautentisering](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Säker tokenhantering**: Implementera [Microsofts bästa praxis för tokenvalidering och livscykel](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Validera att tokenanspråk för målgrupp matchar MCP-serverns identitet
  - Implementera korrekta tokenrotation- och utgångspolicyer
  - Förhindra tokenåterspelsattacker och obehörig användning

- **Skyddad tokenlagring**: Säker tokenlagring med kryptering både i vila och under överföring
  - **Bästa praxis**: [Riktlinjer för säker tokenlagring och kryptering](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementering av åtkomstkontroller

- **Principen om minsta privilegium**: Ge MCP-servrar endast de minimibehörigheter som krävs för avsedd funktionalitet
  - Regelbundna behörighetsgranskningar och uppdateringar för att förhindra privilegieökning
  - **Microsoft-dokumentation**: [Säker åtkomst med minsta privilegium](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Rollbaserad åtkomstkontroll (RBAC)**: Implementera finfördelade rolltilldelningar
  - Begränsa roller strikt till specifika resurser och åtgärder
  - Undvik breda eller onödiga behörigheter som utökar attackytor

- **Kontinuerlig behörighetsövervakning**: Implementera löpande åtkomstgranskning och övervakning
  - Övervaka användningsmönster för behörigheter för att identifiera avvikelser
  - Åtgärda snabbt överdrivna eller oanvända privilegier

## AI-specifika säkerhetshot

### Promptinjektion och verktygsmanipulationsattacker

Moderna MCP-implementeringar står inför sofistikerade AI-specifika attackvektorer som traditionella säkerhetsåtgärder inte fullt ut kan hantera:

#### **Indirekt promptinjektion (Cross-Domain Prompt Injection)**

**Indirekt promptinjektion** representerar en av de mest kritiska sårbarheterna i MCP-aktiverade AI-system. Angripare bäddar in skadliga instruktioner i extern innehåll—dokument, webbsidor, e-postmeddelanden eller datakällor—som AI-system sedan bearbetar som legitima kommandon.

**Attackscenarier:**
- **Dokumentbaserad injektion**: Skadliga instruktioner dolda i bearbetade dokument som utlöser oavsiktliga AI-åtgärder
- **Exploatering av webbinnehåll**: Kompromissade webbsidor med inbäddade prompts som manipulerar AI-beteende vid skrapning
- **E-postbaserade attacker**: Skadliga prompts i e-postmeddelanden som får AI-assistenter att läcka information eller utföra obehöriga åtgärder
- **Datakällförorening**: Kompromissade databaser eller API:er som serverar förorenat innehåll till AI-system

**Verklig påverkan**: Dessa attacker kan leda till dataexfiltrering, integritetsbrott, generering av skadligt innehåll och manipulation av användarinteraktioner. För detaljerad analys, se [Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Prompt Injection Attack Diagram](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.sv.png)

#### **Verktygsförgiftningsattacker**

**Verktygsförgiftning** riktar sig mot metadata som definierar MCP-verktyg och utnyttjar hur LLM:er tolkar verktygsbeskrivningar och parametrar för att fatta beslut om exekvering.

**Attackmekanismer:**
- **Manipulation av metadata**: Angripare injicerar skadliga instruktioner i verktygsbeskrivningar, parameterdefinitioner eller användningsexempel
- **Osynliga instruktioner**: Dolda prompts i verktygsmetadata som bearbetas av AI-modeller men är osynliga för mänskliga användare
- **Dynamisk verktygsmodifiering ("Rug Pulls")**: Verktyg som godkänts av användare modifieras senare för att utföra skadliga åtgärder utan användarens vetskap
- **Parameterinjektion**: Skadligt innehåll inbäddat i verktygsparameterstrukturer som påverkar modellbeteende

**Risker för värdservrar**: Fjärr-MCP-servrar medför förhöjda risker eftersom verktygsdefinitioner kan uppdateras efter initialt användargodkännande, vilket skapar scenarier där tidigare säkra verktyg blir skadliga. För omfattande analys, se [Tool Poisoning Attacks (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Tool Injection Attack Diagram](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.sv.png)

#### **Ytterligare AI-attackvektorer**

- **Cross-Domain Prompt Injection (XPIA)**: Sofistikerade attacker som utnyttjar innehåll från flera domäner för att kringgå säkerhetskontroller
- **Dynamisk kapabilitetsmodifiering**: Realtidsförändringar av verktygskapabiliteter som undgår initiala säkerhetsbedömningar
- **Förgiftning av kontextfönster**: Attacker som manipulerar stora kontextfönster för att dölja skadliga instruktioner
- **Modellförvirringsattacker**: Utnyttjande av modellbegränsningar för att skapa oförutsägbara eller osäkra beteenden

### Säkerhetsrisker för AI: Påverkan

**Högpåverkande konsekvenser:**
- **Dataexfiltrering**: Obefogad åtkomst och stöld av känslig företags- eller persondata
- **Integritetsbrott**: Exponering av personligt identifierbar information (PII) och konfidentiell affärsdata  
- **Systemmanipulation**: Oavsiktliga modifieringar av kritiska system och arbetsflöden
- **Stöld av autentiseringsuppgifter**: Kompromiss av autentiseringstoken och tjänstebehörigheter
- **Lateral rörelse**: Användning av kompromissade AI-system som pivoter för bredare nätverksattacker

### Microsofts säkerhetslösningar för AI

#### **AI Prompt Shields: Avancerat skydd mot injektionsattacker**

Microsoft **AI Prompt Shields** erbjuder omfattande försvar mot både direkta och indirekta promptinjektionsattacker genom flera säkerhetslager:

##### **Kärnmekanismer för skydd:**

1. **Avancerad upptäckt och filtrering**
   - Maskininlärningsalgoritmer och NLP-tekniker upptäcker skadliga instruktioner i externt innehåll
   - Realtidsanalys av dokument, webbsidor, e-postmeddelanden och datakällor för inbäddade hot
   - Kontextuell förståelse av legitima kontra skadliga promptmönster

2. **Spotlight-tekniker**  
   - Skiljer mellan betrodda systeminstruktioner och potentiellt kompromissade externa inmatningar
   - Texttransformationstekniker som förbättrar modellrelevans samtidigt som skadligt innehåll isoleras
   - Hjälper AI-system att upprätthålla korrekt instruktionshierarki och ignorera injicerade kommandon

3. **Avgränsnings- och datamarkeringssystem**
   - Tydlig gränsdefinition mellan betrodda systemmeddelanden och extern inmatningstext
   - Speciella markörer framhäver gränser mellan betrodda och opålitliga datakällor
   - Tydlig separation förhindrar instruktionsförvirring och obehörig kommandoutföring

4. **Kontinuerlig hotintelligens**
   - Microsoft övervakar kontinuerligt framväxande attackmönster och uppdaterar försvar
   - Proaktiv hotjakt för nya injektionstekniker och attackvektorer
   - Regelbundna säkerhetsmodelluppdateringar för att bibehålla effektivitet mot utvecklande hot

5. **Integration med Azure Content Safety**
   - Del av den omfattande Azure AI Content Safety-sviten
   - Ytterligare upptäckt av försök till jailbreak, skadligt innehåll och brott mot säkerhetspolicyer
   - Enhetliga säkerhetskontroller över AI-applikationskomponenter

**Implementeringsresurser**: [Microsoft Prompt Shields-dokumentation](https://learn.microsoft.com/azure/ai-services
- **Säker sessiongenerering**: Använd kryptografiskt säkra, icke-deterministiska sessions-ID:n som genereras med säkra slumpgeneratorer  
- **Användarspecifik bindning**: Koppla sessions-ID:n till användarspecifik information med format som `<user_id>:<session_id>` för att förhindra missbruk mellan användare  
- **Hantering av sessionslivscykel**: Implementera korrekt utgång, rotation och ogiltigförklaring för att begränsa sårbarhetsfönster  
- **Transportskydd**: Obligatorisk HTTPS för all kommunikation för att förhindra avlyssning av sessions-ID  

### Problemet med förvirrad mellanhand

**Problemet med förvirrad mellanhand** uppstår när MCP-servrar agerar som autentiseringsproxyer mellan klienter och tredjepartstjänster, vilket skapar möjligheter för att kringgå auktorisering genom att utnyttja statiska klient-ID:n.

#### **Attackmekanismer och risker**

- **Cookie-baserad samtyckesförbikoppling**: Tidigare användarautentisering skapar samtyckescookies som angripare utnyttjar genom skadliga auktoriseringsförfrågningar med manipulerade omdirigerings-URI:er  
- **Stöld av auktoriseringskod**: Befintliga samtyckescookies kan få auktoriseringsservrar att hoppa över samtyckesskärmar och omdirigera koder till angriparkontrollerade slutpunkter  
- **Obehörig API-åtkomst**: Stulna auktoriseringskoder möjliggör tokenutbyte och användarimpersonering utan uttryckligt godkännande  

#### **Strategier för att minska risker**

**Obligatoriska kontroller:**
- **Krav på uttryckligt samtycke**: MCP-proxyservrar som använder statiska klient-ID:n **MÅSTE** få användarens samtycke för varje dynamiskt registrerad klient  
- **Implementering av OAuth 2.1-säkerhet**: Följ aktuella säkerhetsrekommendationer för OAuth, inklusive PKCE (Proof Key for Code Exchange) för alla auktoriseringsförfrågningar  
- **Strikt klientvalidering**: Implementera rigorös validering av omdirigerings-URI:er och klientidentifierare för att förhindra exploatering  

### Sårbarheter vid tokenpassering  

**Tokenpassering** representerar ett explicit anti-mönster där MCP-servrar accepterar klienttoken utan korrekt validering och vidarebefordrar dem till nedströms-API:er, vilket bryter mot MCP-auktoriseringsspecifikationer.

#### **Säkerhetsimplikationer**

- **Kontrollförbikoppling**: Direkt användning av klient-till-API-token kringgår viktiga begränsningar, valideringar och övervakningskontroller  
- **Förvanskning av granskningsspår**: Token som utfärdats uppströms gör klientidentifiering omöjlig, vilket försvårar incidentutredningar  
- **Proxybaserad dataexfiltrering**: Ovaliderade token möjliggör för skadliga aktörer att använda servrar som proxyer för obehörig dataåtkomst  
- **Brott mot förtroendegränser**: Nedströms-tjänsters förtroendeantaganden kan brytas när tokenursprung inte kan verifieras  
- **Utökning av attacker mellan tjänster**: Komprometterade token som accepteras över flera tjänster möjliggör lateral rörelse  

#### **Nödvändiga säkerhetskontroller**

**Icke-förhandlingsbara krav:**
- **Tokenvalidering**: MCP-servrar **FÅR INTE** acceptera token som inte uttryckligen har utfärdats för MCP-servern  
- **Verifiering av målgrupp**: Validera alltid att tokenmålgruppens påståenden matchar MCP-serverns identitet  
- **Korrekt tokenlivscykel**: Implementera kortlivade åtkomsttoken med säkra rotationsrutiner  

## Säkerhet i leveranskedjan för AI-system

Säkerheten i leveranskedjan har utvecklats bortom traditionella mjukvaruberoenden för att omfatta hela AI-ekosystemet. Moderna MCP-implementationer måste noggrant verifiera och övervaka alla AI-relaterade komponenter, eftersom varje introducerar potentiella sårbarheter som kan äventyra systemets integritet.

### Utökade komponenter i AI-leveranskedjan

**Traditionella mjukvaruberoenden:**
- Öppen källkod-bibliotek och ramverk  
- Containerbilder och basystem  
- Utvecklingsverktyg och byggpipelines  
- Infrastrukturkomponenter och tjänster  

**AI-specifika element i leveranskedjan:**
- **Grundmodeller**: Förtränade modeller från olika leverantörer som kräver verifiering av ursprung  
- **Inbäddningstjänster**: Externa tjänster för vektorisering och semantisk sökning  
- **Kontextleverantörer**: Datakällor, kunskapsbaser och dokumentarkiv  
- **Tredjeparts-API:er**: Externa AI-tjänster, ML-pipelines och dataprestanda-slutpunkter  
- **Modellartefakter**: Vikter, konfigurationer och finjusterade modellvarianter  
- **Träningsdatakällor**: Dataset som används för modellträning och finjustering  

### Omfattande strategi för säkerhet i leveranskedjan

#### **Komponentverifiering och förtroende**
- **Validering av ursprung**: Verifiera ursprung, licensiering och integritet för alla AI-komponenter innan integration  
- **Säkerhetsbedömning**: Utför sårbarhetsskanningar och säkerhetsgranskningar för modeller, datakällor och AI-tjänster  
- **Rykteanalys**: Utvärdera säkerhetshistorik och praxis hos AI-tjänsteleverantörer  
- **Efterlevnadsverifiering**: Säkerställ att alla komponenter uppfyller organisationens säkerhets- och regulatoriska krav  

#### **Säkra distributionspipelines**  
- **Automatiserad CI/CD-säkerhet**: Integrera säkerhetsskanning i automatiserade distributionspipelines  
- **Artefaktintegritet**: Implementera kryptografisk verifiering för alla distribuerade artefakter (kod, modeller, konfigurationer)  
- **Stegvis distribution**: Använd progressiva distributionsstrategier med säkerhetsvalidering vid varje steg  
- **Betrodda artefaktregister**: Distribuera endast från verifierade, säkra artefaktregister och arkiv  

#### **Kontinuerlig övervakning och respons**
- **Beroendeskanning**: Löpande sårbarhetsövervakning för alla mjukvaru- och AI-komponentberoenden  
- **Modellövervakning**: Kontinuerlig bedömning av modellbeteende, prestandadrift och säkerhetsavvikelser  
- **Tjänstehälsospårning**: Övervaka externa AI-tjänster för tillgänglighet, säkerhetsincidenter och policyändringar  
- **Hotintelligensintegration**: Inkludera hotflöden specifika för AI- och ML-säkerhetsrisker  

#### **Åtkomstkontroll och minimal behörighet**
- **Behörigheter på komponentnivå**: Begränsa åtkomst till modeller, data och tjänster baserat på affärsbehov  
- **Hantering av tjänstekonton**: Implementera dedikerade tjänstekonton med minimalt nödvändiga behörigheter  
- **Nätverkssegmentering**: Isolera AI-komponenter och begränsa nätverksåtkomst mellan tjänster  
- **API-gatewaykontroller**: Använd centraliserade API-gateways för att kontrollera och övervaka åtkomst till externa AI-tjänster  

#### **Incidenthantering och återhämtning**
- **Snabba responsrutiner**: Etablerade processer för att patcha eller ersätta komprometterade AI-komponenter  
- **Rotering av autentiseringsuppgifter**: Automatiserade system för att rotera hemligheter, API-nycklar och tjänstautentiseringsuppgifter  
- **Återställningsmöjligheter**: Förmåga att snabbt återgå till tidigare kända godkända versioner av AI-komponenter  
- **Återhämtning vid brott i leveranskedjan**: Specifika procedurer för att hantera kompromisser i uppströms AI-tjänster  

### Microsofts säkerhetsverktyg och integration

**GitHub Advanced Security** erbjuder omfattande skydd för leveranskedjan, inklusive:  
- **Hemlighetsskanning**: Automatisk upptäckt av autentiseringsuppgifter, API-nycklar och token i arkiv  
- **Beroendeskanning**: Sårbarhetsbedömning för öppen källkod-bibliotek och ramverk  
- **CodeQL-analys**: Statisk kodanalys för säkerhetsbrister och kodningsproblem  
- **Insikter om leveranskedjan**: Synlighet i beroendens hälsa och säkerhetsstatus  

**Azure DevOps & Azure Repos Integration:**  
- Sömlös integration av säkerhetsskanning över Microsofts utvecklingsplattformar  
- Automatiserade säkerhetskontroller i Azure Pipelines för AI-arbetsbelastningar  
- Policytillämpning för säker distribution av AI-komponenter  

**Microsofts interna praxis:**  
Microsoft implementerar omfattande säkerhetsrutiner för leveranskedjan över alla produkter. Läs om beprövade metoder i [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Microsofts säkerhetslösningar**
- [Microsoft Prompt Shields-dokumentation](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety-tjänst](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID-säkerhet](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Bästa praxis för hantering av Azure-token](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Implementeringsguider och handledningar**
- [Azure API Management som MCP-autentiseringsgateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID-autentisering med MCP-servrar](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Säker tokenlagring och kryptering (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps och säkerhet i leveranskedjan**
- [Azure DevOps-säkerhet](https://azure.microsoft.com/products/devops)
- [Azure Repos-säkerhet](https://azure.microsoft.com/products/devops/repos/)
- [Microsofts resa mot säkerhet i leveranskedjan](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Ytterligare säkerhetsdokumentation**

För omfattande säkerhetsvägledning, se dessa specialiserade dokument i denna sektion:

- **[MCP säkerhetsbästa praxis 2025](./mcp-security-best-practices-2025.md)** - Kompletta bästa praxis för säkerhet vid MCP-implementeringar
- **[Implementering av Azure Content Safety](./azure-content-safety-implementation.md)** - Praktiska exempel på integration av Azure Content Safety  
- **[MCP säkerhetskontroller 2025](./mcp-security-controls-2025.md)** - De senaste säkerhetskontrollerna och teknikerna för MCP-distributioner
- **[Snabbreferens för MCP bästa praxis](./mcp-best-practices.md)** - Snabbreferensguide för grundläggande MCP-säkerhetspraxis

---

## Vad händer härnäst

Nästa: [Kapitel 3: Kom igång](../03-GettingStarted/README.md)

**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, bör du vara medveten om att automatiserade översättningar kan innehålla fel eller inexaktheter. Det ursprungliga dokumentet på dess originalspråk bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för eventuella missförstånd eller feltolkningar som uppstår vid användning av denna översättning.