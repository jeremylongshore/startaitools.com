<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T14:53:28+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "sv"
}
-->
# MCP Säkerhetsbästa Praxis 2025

Denna omfattande guide beskriver viktiga säkerhetsbästa praxis för implementering av Model Context Protocol (MCP)-system baserat på den senaste **MCP-specifikationen 2025-06-18** och aktuella branschstandarder. Dessa praxis adresserar både traditionella säkerhetsfrågor och AI-specifika hot som är unika för MCP-distributioner.

## Kritiska Säkerhetskrav

### Obligatoriska Säkerhetskontroller (MÅSTE-krav)

1. **Tokenvalidering**: MCP-servrar **FÅR INTE** acceptera några tokens som inte uttryckligen har utfärdats för just den MCP-servern.
2. **Behörighetsverifiering**: MCP-servrar som implementerar behörighet **MÅSTE** verifiera ALLA inkommande förfrågningar och **FÅR INTE** använda sessioner för autentisering.  
3. **Användarsamtycke**: MCP-proxyservrar som använder statiska klient-ID:n **MÅSTE** inhämta uttryckligt användarsamtycke för varje dynamiskt registrerad klient.
4. **Säkra sessions-ID:n**: MCP-servrar **MÅSTE** använda kryptografiskt säkra, icke-deterministiska sessions-ID:n som genereras med säkra slumptalsgeneratorer.

## Kärnsäkerhetspraxis

### 1. Validering och Sanering av Inmatning
- **Omfattande Inmatningsvalidering**: Validera och sanera all inmatning för att förhindra injektionsattacker, förvirrade mellanhandproblem och promptinjektionssårbarheter.
- **Parameterschemavalidering**: Implementera strikt JSON-schemavalidering för alla verktygsparametrar och API-inmatningar.
- **Innehållsfiltrering**: Använd Microsoft Prompt Shields och Azure Content Safety för att filtrera skadligt innehåll i prompts och svar.
- **Utmatningssanering**: Validera och sanera alla modellutmatningar innan de presenteras för användare eller nedströms system.

### 2. Autentisering och Behörighetsexcellens  
- **Externa Identitetsleverantörer**: Delegera autentisering till etablerade identitetsleverantörer (Microsoft Entra ID, OAuth 2.1-leverantörer) istället för att implementera egen autentisering.
- **Fingraderade Behörigheter**: Implementera detaljerade, verktygsspecifika behörigheter enligt principen om minsta privilegium.
- **Tokenlivscykelhantering**: Använd kortlivade åtkomsttokens med säker rotation och korrekt validering av målgrupp.
- **Multifaktorautentisering**: Kräv MFA för all administrativ åtkomst och känsliga operationer.

### 3. Säkra Kommunikationsprotokoll
- **Transportlagersäkerhet**: Använd HTTPS/TLS 1.3 för all MCP-kommunikation med korrekt certifikatvalidering.
- **End-to-End-kryptering**: Implementera ytterligare krypteringslager för mycket känslig data i transit och i vila.
- **Certifikathantering**: Upprätthåll korrekt certifikatlifecyclehantering med automatiserade förnyelseprocesser.
- **Protokollversionshantering**: Använd aktuell MCP-protokollversion (2025-06-18) med korrekt versionsförhandling.

### 4. Avancerad Hastighetsbegränsning och Resursskydd
- **Flerlagers Hastighetsbegränsning**: Implementera hastighetsbegränsning på användar-, sessions-, verktygs- och resursnivåer för att förhindra missbruk.
- **Adaptiv Hastighetsbegränsning**: Använd maskininlärningsbaserad hastighetsbegränsning som anpassar sig efter användningsmönster och hotindikatorer.
- **Resurskvothantering**: Sätt lämpliga gränser för beräkningsresurser, minnesanvändning och exekveringstid.
- **DDoS-skydd**: Distribuera omfattande DDoS-skydd och trafikanalysystem.

### 5. Omfattande Loggning och Övervakning
- **Strukturerad Revisionsloggning**: Implementera detaljerade, sökbara loggar för alla MCP-operationer, verktygskörningar och säkerhetshändelser.
- **Realtidsövervakning av Säkerhet**: Distribuera SIEM-system med AI-driven anomalidetektion för MCP-arbetsbelastningar.
- **Integritetskompatibel Loggning**: Logga säkerhetshändelser samtidigt som dataskyddskrav och regleringar respekteras.
- **Incidentresponsintegration**: Koppla loggningssystem till automatiserade incidentresponsarbetsflöden.

### 6. Förbättrade Säkra Lagringspraxis
- **Hårdvarusäkerhetsmoduler**: Använd HSM-stödd nyckellagring (Azure Key Vault, AWS CloudHSM) för kritiska kryptografiska operationer.
- **Krypteringsnyckelhantering**: Implementera korrekt nyckelrotation, segmentering och åtkomstkontroller för krypteringsnycklar.
- **Hemlighetshantering**: Lagra alla API-nycklar, tokens och autentiseringsuppgifter i dedikerade system för hemlighetshantering.
- **Dataklassificering**: Klassificera data baserat på känslighetsnivåer och tillämpa lämpliga skyddsåtgärder.

### 7. Avancerad Tokenhantering
- **Förhindrande av Tokenpassering**: Förbjud uttryckligen tokenpasseringsmönster som kringgår säkerhetskontroller.
- **Validering av Målgrupp**: Verifiera alltid att tokenmålgruppens påståenden matchar den avsedda MCP-serverns identitet.
- **Behörighet baserad på Påståenden**: Implementera detaljerad behörighet baserad på tokenpåståenden och användarattribut.
- **Tokenbindning**: Binda tokens till specifika sessioner, användare eller enheter där det är lämpligt.

### 8. Säker Sessionshantering
- **Kryptografiska Sessions-ID:n**: Generera sessions-ID:n med kryptografiskt säkra slumptalsgeneratorer (inte förutsägbara sekvenser).
- **Användarspecifik Bindning**: Binda sessions-ID:n till användarspecifik information med säkra format som `<user_id>:<session_id>`.
- **Kontroller för Sessionslivscykel**: Implementera korrekt sessionsutgång, rotation och ogiltigförklaringsmekanismer.
- **Säkerhetshuvuden för Sessioner**: Använd lämpliga HTTP-säkerhetshuvuden för sessionsskydd.

### 9. AI-specifika Säkerhetskontroller
- **Försvar mot Promptinjektion**: Distribuera Microsoft Prompt Shields med spotlighting, avgränsare och datamärkningstekniker.
- **Förebyggande av Verktygsförgiftning**: Validera verktygsmetadata, övervaka dynamiska ändringar och verifiera verktygsintegritet.
- **Validering av Modellutmatning**: Skanna modellutmatningar för potentiella dataläckor, skadligt innehåll eller säkerhetspolicyöverträdelser.
- **Skydd av Kontextfönster**: Implementera kontroller för att förhindra förgiftning och manipulation av kontextfönster.

### 10. Säker Verktygskörning
- **Isolering av Körning**: Kör verktyg i containeriserade, isolerade miljöer med resursbegränsningar.
- **Separering av Privilegier**: Kör verktyg med minimalt nödvändiga privilegier och separata tjänstekonton.
- **Nätverksisolering**: Implementera nätverkssegmentering för verktygskörningsmiljöer.
- **Övervakning av Körning**: Övervaka verktygskörning för avvikande beteende, resursanvändning och säkerhetsöverträdelser.

### 11. Kontinuerlig Säkerhetsvalidering
- **Automatiserad Säkerhetstestning**: Integrera säkerhetstestning i CI/CD-pipelines med verktyg som GitHub Advanced Security.
- **Sårbarhetshantering**: Skanna regelbundet alla beroenden, inklusive AI-modeller och externa tjänster.
- **Penetrationstestning**: Utför regelbundna säkerhetsbedömningar som specifikt riktar sig mot MCP-implementationer.
- **Säkerhetskodgranskningar**: Implementera obligatoriska säkerhetsgranskningar för alla MCP-relaterade kodändringar.

### 12. Leveranskedjesäkerhet för AI
- **Komponentverifiering**: Verifiera ursprung, integritet och säkerhet för alla AI-komponenter (modeller, inbäddningar, API:er).
- **Beroendehantering**: Upprätthåll aktuella inventarier av alla mjukvaru- och AI-beroenden med sårbarhetsspårning.
- **Betrodda Repositorier**: Använd verifierade, betrodda källor för alla AI-modeller, bibliotek och verktyg.
- **Övervakning av Leveranskedjan**: Övervaka kontinuerligt för kompromisser hos AI-tjänsteleverantörer och modellrepositorier.

## Avancerade Säkerhetsmönster

### Zero Trust-arkitektur för MCP
- **Lita Aldrig, Verifiera Alltid**: Implementera kontinuerlig verifiering för alla MCP-deltagare.
- **Mikrosegmentering**: Isolera MCP-komponenter med detaljerade nätverks- och identitetskontroller.
- **Villkorlig Åtkomst**: Implementera riskbaserade åtkomstkontroller som anpassar sig efter kontext och beteende.
- **Kontinuerlig Riskbedömning**: Utvärdera säkerhetsläget dynamiskt baserat på aktuella hotindikatorer.

### Integritetsskyddande AI-implementering
- **Dataminimering**: Exponera endast minimalt nödvändig data för varje MCP-operation.
- **Differentiell Integritet**: Implementera integritetsskyddande tekniker för känslig databehandling.
- **Homomorfisk Kryptering**: Använd avancerade krypteringstekniker för säker beräkning på krypterad data.
- **Federerad Inlärning**: Implementera distribuerade inlärningsmetoder som bevarar datalokalitet och integritet.

### Incidentrespons för AI-system
- **AI-specifika Incidentprocedurer**: Utveckla incidentresponsprocedurer anpassade för AI- och MCP-specifika hot.
- **Automatiserad Respons**: Implementera automatiserad inneslutning och åtgärd för vanliga AI-säkerhetsincidenter.  
- **Forensiska Möjligheter**: Upprätthåll forensisk beredskap för kompromisser i AI-system och dataintrång.
- **Återställningsprocedurer**: Etablera procedurer för återställning från AI-modellförgiftning, promptinjektionsattacker och tjänstekompromisser.

## Implementeringsresurser och Standarder

### Officiell MCP-dokumentation
- [MCP-specifikation 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Aktuell MCP-protokollspecifikation
- [MCP Säkerhetsbästa Praxis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Officiell säkerhetsvägledning
- [MCP Behörighetsspecifikation](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Autentiserings- och behörighetsmönster
- [MCP Transportskydd](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Transportlagersäkerhetskrav

### Microsoft Säkerhetslösningar
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Avancerat skydd mot promptinjektion
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Omfattande AI-innehållsfiltrering
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Företagsidentitet och åtkomsthantering
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Säker hantering av hemligheter och autentiseringsuppgifter
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Leveranskedje- och kodsäkerhetsskanning

### Säkerhetsstandarder och Ramverk
- [OAuth 2.1 Säkerhetsbästa Praxis](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Aktuell OAuth-säkerhetsvägledning
- [OWASP Topp 10](https://owasp.org/www-project-top-ten/) - Webbsäkerhetsrisker
- [OWASP Topp 10 för LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI-specifika säkerhetsrisker
- [NIST AI Riskhanteringsramverk](https://www.nist.gov/itl/ai-risk-management-framework) - Omfattande AI-riskhantering
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Informationssäkerhetshanteringssystem

### Implementeringsguider och Tutorials
- [Azure API Management som MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Företagsautentiseringsmönster
- [Microsoft Entra ID med MCP-servrar](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integration av identitetsleverantör
- [Implementering av Säker Tokenlagring](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Bästa praxis för tokenhantering
- [End-to-End-kryptering för AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Avancerade krypteringsmönster

### Avancerade Säkerhetsresurser
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Säkra utvecklingspraxis
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - AI-specifik säkerhetstestning
- [Hotmodellering för AI-system](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodik för AI-hotmodellering
- [Integritetsteknik för AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Integritetsskyddande AI-tekniker

### Efterlevnad och Styrning
- [GDPR-efterlevnad för AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Integritetsefterlevnad i AI-system
- [AI Styrningsramverk](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Ansvarsfull AI-implementering
- [SOC 2 för AI-tjänster](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Säkerhetskontroller för AI-tjänsteleverantörer
- [HIPAA-efterlevnad för AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Hälso- och sjukvårds-AI-efterlevnadskrav

### DevSecOps och Automatisering
- [DevSecOps Pipeline för AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Säker AI-utvecklingspipeline
- [Automatiserad Säkerhetstestning](https://learn.microsoft.com/security/engineering/devsecops) - Kontinuerlig säkerhetsvalidering
- [Infrastruktur som Kod Säkerhet](https://learn.microsoft.com/security/engineering/infrastructure-security) - Säker distribution av infrastruktur
- [Containersäkerhet för AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Säkerhet för AI-arbetsbelastningar i containrar

### Övervakning och Incidentrespons  
- [Azure Monitor för AI-arbetsbelastningar](https://learn.microsoft.com/azure/azure-monitor/overview) - Omfattande övervakningslösningar
- [AI Säkerhetsincidentrespons](https://learn.microsoft.com/security/compass/incident-response-playbooks) - AI-specifika incidentprocedurer
- [SIEM för AI-system](https://learn.microsoft.com/azure/sentinel/overview) - Säkerhetsinformation och händelsehantering
- [Hotintelligens för AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Källor för AI-hotintelligens

## 🔄 Kontinuerlig Förbättring

### Håll Dig Uppdaterad med Utvecklande Standarder
- **Uppdateringar av MCP-specifikationen**: Övervaka officiella ändringar i MCP-specifikationen och säkerhetsrådgivningar.
- **Hotintelligens**: Prenumerera på AI-säkerhetshotflöden och sårbarhetsdatabaser.  
- **Gemenskapsengagemang**: Delta i MCP-säkerhetsdiskussioner och arbetsgrupper.
- **Regelbunden Bed
- **Verktygsutveckling**: Utveckla och dela säkerhetsverktyg och bibliotek för MCP-ekosystemet

---

*Detta dokument återspeglar MCP:s säkerhetsbästa praxis per den 18 augusti 2025, baserat på MCP-specifikationen 2025-06-18. Säkerhetspraxis bör regelbundet ses över och uppdateras i takt med att protokollet och hotlandskapet utvecklas.*

**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, bör det noteras att automatiserade översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess originalspråk bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för eventuella missförstånd eller feltolkningar som uppstår vid användning av denna översättning.