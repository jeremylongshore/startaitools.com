<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T14:49:48+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "sv"
}
-->
# MCP Säkerhetsbästa praxis - Uppdatering augusti 2025

> **Viktigt**: Detta dokument återspeglar de senaste [MCP-specifikationen 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) säkerhetskraven och officiella [MCP Säkerhetsbästa praxis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Hänvisa alltid till den aktuella specifikationen för den mest uppdaterade vägledningen.

## Grundläggande säkerhetsrutiner för MCP-implementeringar

Model Context Protocol introducerar unika säkerhetsutmaningar som går utöver traditionell mjukvarusäkerhet. Dessa rutiner adresserar både grundläggande säkerhetskrav och MCP-specifika hot, inklusive promptinjektion, verktygsförgiftning, sessionkapning, förvirrade ställföreträdarproblem och sårbarheter relaterade till tokenpassering.

### **OBLIGATORISKA säkerhetskrav**

**Kritiska krav från MCP-specifikationen:**

> **MÅSTE INTE**: MCP-servrar **MÅSTE INTE** acceptera några tokens som inte uttryckligen har utfärdats för MCP-servern  
> 
> **MÅSTE**: MCP-servrar som implementerar auktorisering **MÅSTE** verifiera ALLA inkommande förfrågningar  
>  
> **MÅSTE INTE**: MCP-servrar **MÅSTE INTE** använda sessioner för autentisering  
>
> **MÅSTE**: MCP-proxyservrar som använder statiska klient-ID:n **MÅSTE** få användarens samtycke för varje dynamiskt registrerad klient  

---

## 1. **Tokensäkerhet & autentisering**

**Kontroller för autentisering och auktorisering:**  
   - **Noggrann granskning av auktorisering**: Utför omfattande granskningar av MCP-serverns auktoriseringslogik för att säkerställa att endast avsedda användare och klienter kan komma åt resurser  
   - **Integration med externa identitetsleverantörer**: Använd etablerade identitetsleverantörer som Microsoft Entra ID istället för att implementera egen autentisering  
   - **Validering av tokenmålgrupp**: Validera alltid att tokens uttryckligen har utfärdats för din MCP-server - acceptera aldrig tokens från uppströmskällor  
   - **Korrekt tokenlivscykel**: Implementera säker tokenrotation, utgångspolicyer och förhindra tokenåterspelningsattacker  

**Skyddad tokenlagring:**  
   - Använd Azure Key Vault eller liknande säkra lagringslösningar för alla hemligheter  
   - Implementera kryptering för tokens både i vila och under överföring  
   - Regelbunden rotation av autentiseringsuppgifter och övervakning för obehörig åtkomst  

## 2. **Sessionshantering & transportskydd**

**Säkra sessionsrutiner:**  
   - **Kryptografiskt säkra sessions-ID:n**: Använd säkra, icke-deterministiska sessions-ID:n genererade med säkra slumptalsgeneratorer  
   - **Användarspecifik bindning**: Bind sessions-ID:n till användaridentiteter med format som `<user_id>:<session_id>` för att förhindra missbruk mellan användare  
   - **Hantera sessionslivscykel**: Implementera korrekt utgång, rotation och ogiltigförklaring för att begränsa sårbarhetsfönster  
   - **Tvinga HTTPS/TLS**: Obligatorisk HTTPS för all kommunikation för att förhindra avlyssning av sessions-ID  

**Transportlagersäkerhet:**  
   - Konfigurera TLS 1.3 där det är möjligt med korrekt certifikathantering  
   - Implementera certifikatspärr för kritiska anslutningar  
   - Regelbunden rotation och verifiering av certifikatens giltighet  

## 3. **AI-specifik hotförsvar** 🤖

**Försvar mot promptinjektion:**  
   - **Microsoft Prompt Shields**: Använd AI Prompt Shields för avancerad upptäckt och filtrering av skadliga instruktioner  
   - **Sanering av indata**: Validera och sanera all indata för att förhindra injektionsattacker och förvirrade ställföreträdarproblem  
   - **Innehållsgränser**: Använd avgränsare och datamarkeringssystem för att skilja mellan betrodda instruktioner och externt innehåll  

**Förebyggande av verktygsförgiftning:**  
   - **Validering av verktygsmetadata**: Implementera integritetskontroller för verktygsdefinitioner och övervaka för oväntade ändringar  
   - **Dynamisk verktygsövervakning**: Övervaka beteende vid körning och sätt upp varningar för oväntade exekveringsmönster  
   - **Godkännandeflöden**: Kräva uttryckligt användargodkännande för verktygsändringar och kapacitetsförändringar  

## 4. **Åtkomstkontroll & behörigheter**

**Principen om minsta privilegium:**  
   - Ge MCP-servrar endast de minimibehörigheter som krävs för avsedd funktionalitet  
   - Implementera rollbaserad åtkomstkontroll (RBAC) med detaljerade behörigheter  
   - Regelbundna behörighetsgranskningar och kontinuerlig övervakning för privilegieeskalering  

**Kontroller för behörigheter vid körning:**  
   - Tillämpa resursbegränsningar för att förhindra attacker som utnyttjar resursuttömning  
   - Använd containerisolering för verktygs exekveringsmiljöer  
   - Implementera åtkomst vid behov för administrativa funktioner  

## 5. **Innehållssäkerhet & övervakning**

**Implementering av innehållssäkerhet:**  
   - **Azure Content Safety Integration**: Använd Azure Content Safety för att upptäcka skadligt innehåll, försök till jailbreak och policyöverträdelser  
   - **Beteendeanalys**: Implementera övervakning av beteende vid körning för att upptäcka avvikelser i MCP-servern och verktygs exekvering  
   - **Omfattande loggning**: Logga alla autentiseringsförsök, verktygsanrop och säkerhetshändelser med säker, manipuleringssäker lagring  

**Kontinuerlig övervakning:**  
   - Realtidsvarningar för misstänkta mönster och obehöriga åtkomstförsök  
   - Integration med SIEM-system för centraliserad hantering av säkerhetshändelser  
   - Regelbundna säkerhetsgranskningar och penetrationstester av MCP-implementeringar  

## 6. **Leverantörskedjans säkerhet**

**Komponentverifiering:**  
   - **Skanning av beroenden**: Använd automatiserad sårbarhetsskanning för alla mjukvaruberoenden och AI-komponenter  
   - **Validering av proveniens**: Verifiera ursprung, licensiering och integritet för modeller, datakällor och externa tjänster  
   - **Signerade paket**: Använd kryptografiskt signerade paket och verifiera signaturer före distribution  

**Säker utvecklingspipeline:**  
   - **GitHub Advanced Security**: Implementera hemlighetsskanning, beroendeanalys och CodeQL statisk analys  
   - **CI/CD-säkerhet**: Integrera säkerhetsvalidering i automatiserade distributionspipelines  
   - **Integritet för artefakter**: Implementera kryptografisk verifiering för distribuerade artefakter och konfigurationer  

## 7. **OAuth-säkerhet & förebyggande av förvirrade ställföreträdare**

**OAuth 2.1-implementering:**  
   - **PKCE-implementering**: Använd Proof Key for Code Exchange (PKCE) för alla auktoriseringsförfrågningar  
   - **Explicit samtycke**: Få användarens samtycke för varje dynamiskt registrerad klient för att förhindra förvirrade ställföreträdarattacker  
   - **Validering av omdirigerings-URI**: Implementera strikt validering av omdirigerings-URI:er och klientidentifierare  

**Proxy-säkerhet:**  
   - Förhindra auktoriseringsförbikoppling genom utnyttjande av statiska klient-ID:n  
   - Implementera korrekta samtyckesflöden för åtkomst till tredjeparts-API:er  
   - Övervaka för stöld av auktoriseringskoder och obehörig API-åtkomst  

## 8. **Incidenthantering & återhämtning**

**Snabba responsmöjligheter:**  
   - **Automatiserad respons**: Implementera automatiserade system för rotation av autentiseringsuppgifter och hotbegränsning  
   - **Återställningsprocedurer**: Förmåga att snabbt återgå till kända, fungerande konfigurationer och komponenter  
   - **Forensiska möjligheter**: Detaljerade granskningsspår och loggning för incidentutredning  

**Kommunikation & samordning:**  
   - Klara eskaleringsprocedurer för säkerhetsincidenter  
   - Integration med organisationens incidenthanteringsteam  
   - Regelbundna simuleringar av säkerhetsincidenter och övningar  

## 9. **Efterlevnad & styrning**

**Regulatorisk efterlevnad:**  
   - Säkerställ att MCP-implementeringar uppfyller branschspecifika krav (GDPR, HIPAA, SOC 2)  
   - Implementera dataklassificering och integritetskontroller för AI-databehandling  
   - Upprätthåll omfattande dokumentation för efterlevnadsgranskning  

**Ändringshantering:**  
   - Formella säkerhetsgranskningsprocesser för alla ändringar i MCP-systemet  
   - Versionskontroll och godkännandeflöden för konfigurationsändringar  
   - Regelbundna efterlevnadsbedömningar och gapanalys  

## 10. **Avancerade säkerhetskontroller**

**Zero Trust-arkitektur:**  
   - **Lita aldrig, verifiera alltid**: Kontinuerlig verifiering av användare, enheter och anslutningar  
   - **Mikrosegmentering**: Granulära nätverkskontroller som isolerar individuella MCP-komponenter  
   - **Villkorlig åtkomst**: Riskbaserade åtkomstkontroller som anpassar sig till aktuell kontext och beteende  

**Skydd av applikationer vid körning:**  
   - **Runtime Application Self-Protection (RASP)**: Implementera RASP-tekniker för realtidsupptäckt av hot  
   - **Övervakning av applikationsprestanda**: Övervaka för prestandaavvikelser som kan indikera attacker  
   - **Dynamiska säkerhetspolicyer**: Implementera säkerhetspolicyer som anpassar sig efter aktuellt hotlandskap  

## 11. **Integration med Microsofts säkerhetsekosystem**

**Omfattande Microsoft-säkerhet:**  
   - **Microsoft Defender for Cloud**: Hantering av säkerhetsställning för MCP-arbetsbelastningar i molnet  
   - **Azure Sentinel**: Molnbaserade SIEM- och SOAR-funktioner för avancerad hotupptäckt  
   - **Microsoft Purview**: Datastyrning och efterlevnad för AI-arbetsflöden och datakällor  

**Identitets- och åtkomsthantering:**  
   - **Microsoft Entra ID**: Företagsidentitetshantering med villkorliga åtkomstpolicyer  
   - **Privileged Identity Management (PIM)**: Åtkomst vid behov och godkännandeflöden för administrativa funktioner  
   - **Identity Protection**: Riskbaserad villkorlig åtkomst och automatiserad hotrespons  

## 12. **Kontinuerlig säkerhetsutveckling**

**Hålla sig uppdaterad:**  
   - **Specifikationsövervakning**: Regelbunden granskning av MCP-specifikationsuppdateringar och förändringar i säkerhetsvägledning  
   - **Hotintelligens**: Integration av AI-specifika hotflöden och indikatorer på kompromiss  
   - **Engagemang i säkerhetsgemenskapen**: Aktivt deltagande i MCP-säkerhetsgemenskapen och program för sårbarhetsrapportering  

**Adaptiv säkerhet:**  
   - **Maskininlärningssäkerhet**: Använd ML-baserad avvikelseupptäckt för att identifiera nya attackmönster  
   - **Prediktiv säkerhetsanalys**: Implementera prediktiva modeller för proaktiv hotidentifiering  
   - **Säkerhetsautomation**: Automatiserade uppdateringar av säkerhetspolicyer baserat på hotintelligens och specifikationsförändringar  

---

## **Kritiska säkerhetsresurser**

### **Officiell MCP-dokumentation**  
- [MCP-specifikationen (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Säkerhetsbästa praxis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Auktoriseringsspecifikation](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsofts säkerhetslösningar**  
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Säkerhet](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Säkerhetsstandarder**  
- [OAuth 2.0 Säkerhetsbästa praxis (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 för stora språkmodeller](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Implementeringsguider**  
- [Azure API Management MCP Autentiseringsgateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID med MCP-servrar](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Säkerhetsmeddelande**: MCP-säkerhetsrutiner utvecklas snabbt. Verifiera alltid mot den aktuella [MCP-specifikationen](https://spec.modelcontextprotocol.io/) och [officiell säkerhetsdokumentation](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) innan implementering.  

**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, bör du vara medveten om att automatiserade översättningar kan innehålla fel eller felaktigheter. Det ursprungliga dokumentet på dess originalspråk bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för eventuella missförstånd eller feltolkningar som uppstår vid användning av denna översättning.