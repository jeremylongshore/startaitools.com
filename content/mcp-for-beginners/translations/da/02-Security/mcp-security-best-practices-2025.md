<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T15:12:51+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "da"
}
-->
# MCP Sikkerhedsbedste Praksis - Opdatering August 2025

> **Vigtigt**: Dette dokument afspejler de nyeste [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) sikkerhedskrav og officielle [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Henvis altid til den aktuelle specifikation for den mest opdaterede vejledning.

## Grundlæggende Sikkerhedspraksis for MCP Implementeringer

Model Context Protocol introducerer unikke sikkerhedsudfordringer, der går ud over traditionel software-sikkerhed. Disse praksisser adresserer både fundamentale sikkerhedskrav og MCP-specifikke trusler, herunder prompt injection, værktøjsforgiftning, session hijacking, confused deputy problemer og token passthrough sårbarheder.

### **OBLIGATORISKE Sikkerhedskrav**

**Kritiske Krav fra MCP Specifikationen:**

> **MÅ IKKE**: MCP-servere **MÅ IKKE** acceptere tokens, der ikke eksplicit er udstedt til MCP-serveren  
> 
> **SKAL**: MCP-servere, der implementerer autorisation, **SKAL** verificere ALLE indgående anmodninger  
>  
> **MÅ IKKE**: MCP-servere **MÅ IKKE** bruge sessioner til autentifikation  
>
> **SKAL**: MCP proxy-servere, der bruger statiske klient-ID'er, **SKAL** indhente brugerens samtykke for hver dynamisk registreret klient  

---

## 1. **Token Sikkerhed & Autentifikation**

**Kontroller for Autentifikation & Autorisation:**  
   - **Grundig Autorisationsgennemgang**: Udfør omfattende audits af MCP-serverens autorisationslogik for at sikre, at kun tilsigtede brugere og klienter kan få adgang til ressourcer  
   - **Integration med Eksterne Identitetsudbydere**: Brug etablerede identitetsudbydere som Microsoft Entra ID frem for at implementere egen autentifikation  
   - **Validering af Token Audience**: Valider altid, at tokens eksplicit er udstedt til din MCP-server - accepter aldrig upstream tokens  
   - **Korrekt Token Livscyklus**: Implementer sikker tokenrotation, udløbspolitikker og forebyg token replay-angreb  

**Beskyttet Token Opbevaring:**  
   - Brug Azure Key Vault eller lignende sikre credential stores til alle hemmeligheder  
   - Implementer kryptering af tokens både i hvile og under transport  
   - Regelmæssig credential rotation og overvågning for uautoriseret adgang  

## 2. **Sessionhåndtering & Transport Sikkerhed**

**Sikre Session Praksisser:**  
   - **Kryptografisk Sikker Session-ID'er**: Brug sikre, ikke-deterministiske session-ID'er genereret med sikre tilfældighedsgeneratorer  
   - **Bruger-Specifik Binding**: Bind session-ID'er til brugeridentiteter ved hjælp af formater som `<user_id>:<session_id>` for at forhindre misbrug på tværs af brugere  
   - **Session Livscyklus Håndtering**: Implementer korrekt udløb, rotation og ugyldiggørelse for at begrænse sårbarhedsvinduer  
   - **HTTPS/TLS Krav**: Obligatorisk HTTPS for al kommunikation for at forhindre session-ID-aflytning  

**Transportlagssikkerhed:**  
   - Konfigurer TLS 1.3, hvor det er muligt, med korrekt certifikathåndtering  
   - Implementer certifikatpinning for kritiske forbindelser  
   - Regelmæssig certifikatrotation og validering af gyldighed  

## 3. **AI-Specifik Trusselsbeskyttelse** 🤖

**Forsvar mod Prompt Injection:**  
   - **Microsoft Prompt Shields**: Implementer AI Prompt Shields for avanceret detektion og filtrering af skadelige instruktioner  
   - **Input Sanitering**: Valider og saniter alle inputs for at forhindre injektionsangreb og confused deputy problemer  
   - **Indholdsgrænser**: Brug delimiter- og datamarkeringssystemer til at skelne mellem betroede instruktioner og eksternt indhold  

**Forebyggelse af Værktøjsforgiftning:**  
   - **Validering af Værktøjsmetadata**: Implementer integritetskontroller for værktøjsdefinitioner og overvåg for uventede ændringer  
   - **Dynamisk Værktøjsovervågning**: Overvåg runtime-adfærd og opsæt alarmer for uventede eksekveringsmønstre  
   - **Godkendelsesarbejdsgange**: Kræv eksplicit brugeraccept for værktøjsmodifikationer og kapacitetsændringer  

## 4. **Adgangskontrol & Tilladelser**

**Princippet om Mindste Privilegium:**  
   - Giv MCP-servere kun de minimumstilladelser, der kræves for den tilsigtede funktionalitet  
   - Implementer rollebaseret adgangskontrol (RBAC) med fine-grained tilladelser  
   - Regelmæssige tilladelsesgennemgange og kontinuerlig overvågning for privilegieeskalering  

**Kontroller for Runtime Tilladelser:**  
   - Anvend ressourcebegrænsninger for at forhindre angreb med ressourceudtømning  
   - Brug containerisolering til værktøjseksekveringsmiljøer  
   - Implementer just-in-time adgang til administrative funktioner  

## 5. **Indholdssikkerhed & Overvågning**

**Implementering af Indholdssikkerhed:**  
   - **Azure Content Safety Integration**: Brug Azure Content Safety til at detektere skadeligt indhold, jailbreak-forsøg og politikovertrædelser  
   - **Adfærdsanalyse**: Implementer runtime-adfærdsmonitorering for at detektere anomalier i MCP-server og værktøjseksekvering  
   - **Omfattende Logning**: Log alle autentifikationsforsøg, værktøjsindkaldelser og sikkerhedshændelser med sikker, manipulationssikker opbevaring  

**Kontinuerlig Overvågning:**  
   - Realtidsalarmering for mistænkelige mønstre og uautoriserede adgangsforsøg  
   - Integration med SIEM-systemer for centraliseret sikkerhedshændelseshåndtering  
   - Regelmæssige sikkerhedsaudits og penetrationstest af MCP-implementeringer  

## 6. **Forsyningskædesikkerhed**

**Komponentverifikation:**  
   - **Afhængighedsscanning**: Brug automatiseret sårbarhedsscanning for alle softwareafhængigheder og AI-komponenter  
   - **Provenansvalidering**: Verificer oprindelse, licens og integritet af modeller, datakilder og eksterne tjenester  
   - **Signede Pakker**: Brug kryptografisk signede pakker og verificer signaturer før implementering  

**Sikker Udviklingspipeline:**  
   - **GitHub Advanced Security**: Implementer hemmelighedsscanning, afhængighedsanalyse og CodeQL statisk analyse  
   - **CI/CD Sikkerhed**: Integrer sikkerhedsvalidering i hele automatiserede implementeringspipelines  
   - **Artefaktintegritet**: Implementer kryptografisk verifikation for implementerede artefakter og konfigurationer  

## 7. **OAuth Sikkerhed & Forebyggelse af Confused Deputy**

**OAuth 2.1 Implementering:**  
   - **PKCE Implementering**: Brug Proof Key for Code Exchange (PKCE) for alle autorisationsanmodninger  
   - **Eksplicit Samtykke**: Indhent brugerens samtykke for hver dynamisk registreret klient for at forhindre confused deputy angreb  
   - **Validering af Redirect URI**: Implementer streng validering af redirect URI'er og klientidentifikatorer  

**Proxy Sikkerhed:**  
   - Forebyg autorisationsomgåelse gennem udnyttelse af statiske klient-ID'er  
   - Implementer korrekte samtykkearbejdsgange for tredjeparts API-adgang  
   - Overvåg for tyveri af autorisationskoder og uautoriseret API-adgang  

## 8. **Hændelseshåndtering & Genopretning**

**Hurtige Responskapaciteter:**  
   - **Automatiseret Respons**: Implementer automatiserede systemer til credential rotation og trusselsinddæmning  
   - **Rollback Procedurer**: Evne til hurtigt at vende tilbage til kendte gode konfigurationer og komponenter  
   - **Forensiske Kapaciteter**: Detaljerede audit trails og logning for hændelsesundersøgelse  

**Kommunikation & Koordinering:**  
   - Klare eskaleringsprocedurer for sikkerhedshændelser  
   - Integration med organisationens hændelseshåndteringsteam  
   - Regelmæssige sikkerhedshændelsessimuleringer og tabletop-øvelser  

## 9. **Overholdelse & Governance**

**Regulatorisk Overholdelse:**  
   - Sikr, at MCP-implementeringer opfylder branchespecifikke krav (GDPR, HIPAA, SOC 2)  
   - Implementer dataklassificering og privatlivskontroller for AI-databehandling  
   - Oprethold omfattende dokumentation for compliance-audits  

**Ændringshåndtering:**  
   - Formelle sikkerhedsgennemgangsprocesser for alle MCP-systemmodifikationer  
   - Versionskontrol og godkendelsesarbejdsgange for konfigurationsændringer  
   - Regelmæssige compliance-vurderinger og gap-analyser  

## 10. **Avancerede Sikkerhedskontroller**

**Zero Trust Arkitektur:**  
   - **Aldrig Stol, Altid Verificer**: Kontinuerlig verifikation af brugere, enheder og forbindelser  
   - **Mikro-segmentering**: Granulære netværkskontroller, der isolerer individuelle MCP-komponenter  
   - **Betinget Adgang**: Risiko-baserede adgangskontroller, der tilpasser sig den aktuelle kontekst og adfærd  

**Runtime Applikationsbeskyttelse:**  
   - **Runtime Application Self-Protection (RASP)**: Implementer RASP-teknikker for realtidsdetektion af trusler  
   - **Applikationsperformanceovervågning**: Overvåg for performance-anomalier, der kan indikere angreb  
   - **Dynamiske Sikkerhedspolitikker**: Implementer sikkerhedspolitikker, der tilpasser sig baseret på det aktuelle trusselslandskab  

## 11. **Microsoft Sikkerhedsøkosystem Integration**

**Omfattende Microsoft Sikkerhed:**  
   - **Microsoft Defender for Cloud**: Cloud-sikkerhedshåndtering for MCP-arbejdsbelastninger  
   - **Azure Sentinel**: Cloud-native SIEM og SOAR kapaciteter for avanceret trusselsdetektion  
   - **Microsoft Purview**: Datastyring og compliance for AI-arbejdsgange og datakilder  

**Identitets- & Adgangsstyring:**  
   - **Microsoft Entra ID**: Enterprise identitetsstyring med betingede adgangspolitikker  
   - **Privileged Identity Management (PIM)**: Just-in-time adgang og godkendelsesarbejdsgange for administrative funktioner  
   - **Identity Protection**: Risiko-baseret betinget adgang og automatiseret trusselsrespons  

## 12. **Kontinuerlig Sikkerhedsudvikling**

**Hold Dig Opdateret:**  
   - **Specifikationsovervågning**: Regelmæssig gennemgang af MCP-specifikationsopdateringer og ændringer i sikkerhedsvejledning  
   - **Trusselsintelligens**: Integration af AI-specifikke trusselsfeeds og kompromisindikatorer  
   - **Sikkerhedsfællesskab Engagement**: Aktiv deltagelse i MCP-sikkerhedsfællesskabet og programmer for sårbarhedsrapportering  

**Adaptiv Sikkerhed:**  
   - **Maskinlæringssikkerhed**: Brug ML-baseret anomalidetektion til at identificere nye angrebsmønstre  
   - **Forudsigende Sikkerhedsanalyse**: Implementer forudsigende modeller for proaktiv trusselsidentifikation  
   - **Sikkerhedsautomatisering**: Automatiserede opdateringer af sikkerhedspolitikker baseret på trusselsintelligens og specifikationsændringer  

---

## **Kritiske Sikkerhedsressourcer**

### **Officiel MCP Dokumentation**  
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Sikkerhedsløsninger**  
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Security](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Sikkerhedsstandarder**  
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Implementeringsvejledninger**  
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Sikkerhedsmeddelelse**: MCP-sikkerhedspraksisser udvikler sig hurtigt. Verificer altid mod den aktuelle [MCP specifikation](https://spec.modelcontextprotocol.io/) og [officiel sikkerhedsdokumentation](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) før implementering.  

**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på at opnå nøjagtighed, skal det bemærkes, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os ikke ansvar for eventuelle misforståelser eller fejltolkninger, der måtte opstå som følge af brugen af denne oversættelse.