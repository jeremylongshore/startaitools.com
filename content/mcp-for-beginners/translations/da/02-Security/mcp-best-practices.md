<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T15:16:54+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "da"
}
-->
# MCP Sikkerhedsbedste Praksis 2025

Denne omfattende guide beskriver essentielle sikkerhedsbedste praksis for implementering af Model Context Protocol (MCP)-systemer baseret på den nyeste **MCP Specification 2025-06-18** og gældende industristandarder. Disse praksisser adresserer både traditionelle sikkerhedsudfordringer og AI-specifikke trusler, der er unikke for MCP-implementeringer.

## Kritiske Sikkerhedskrav

### Obligatoriske Sikkerhedskontroller (MUST-krav)

1. **Tokenvalidering**: MCP-servere **MÅ IKKE** acceptere tokens, der ikke eksplicit er udstedt til den specifikke MCP-server  
2. **Autorisationsverifikation**: MCP-servere, der implementerer autorisation, **SKAL** verificere ALLE indgående forespørgsler og **MÅ IKKE** bruge sessioner til autentifikation  
3. **Brugersamtykke**: MCP-proxyservere, der bruger statiske klient-ID'er, **SKAL** indhente eksplicit brugersamtykke for hver dynamisk registreret klient  
4. **Sikre Sessions-ID'er**: MCP-servere **SKAL** bruge kryptografisk sikre, ikke-deterministiske sessions-ID'er genereret med sikre tilfældige talgeneratorer  

## Centrale Sikkerhedspraksisser

### 1. Validering og Sanitering af Input
- **Omfattende Inputvalidering**: Valider og saniter alle input for at forhindre injektionsangreb, "confused deputy"-problemer og promptinjektionssårbarheder  
- **Parameter Schema Enforcement**: Implementer streng JSON-schema-validering for alle værktøjsparametre og API-input  
- **Indholdsfiltrering**: Brug Microsoft Prompt Shields og Azure Content Safety til at filtrere skadeligt indhold i prompts og svar  
- **Outputsanitering**: Valider og saniter alle modeloutput, før de præsenteres for brugere eller downstream-systemer  

### 2. Ekspertise i Autentifikation og Autorisation  
- **Eksterne Identitetsudbydere**: Delegér autentifikation til etablerede identitetsudbydere (Microsoft Entra ID, OAuth 2.1-udbydere) frem for at implementere brugerdefineret autentifikation  
- **Fingranulerede Rettigheder**: Implementer detaljerede, værktøjsspecifikke rettigheder baseret på princippet om mindst privilegium  
- **Tokenlivscyklusstyring**: Brug kortlivede adgangstokens med sikker rotation og korrekt validering af målgruppe  
- **Multifaktorautentifikation**: Kræv MFA for al administrativ adgang og følsomme operationer  

### 3. Sikker Kommunikationsprotokoller
- **Transport Layer Security**: Brug HTTPS/TLS 1.3 til al MCP-kommunikation med korrekt certifikatvalidering  
- **End-to-End Kryptering**: Implementer yderligere krypteringslag for meget følsomme data under overførsel og i hvile  
- **Certifikathåndtering**: Vedligehold korrekt certifikatlifecycle-håndtering med automatiserede fornyelsesprocesser  
- **Protokolversionshåndhævelse**: Brug den aktuelle MCP-protokolversion (2025-06-18) med korrekt versionsforhandling  

### 4. Avanceret Ratebegrænsning og Ressourcebeskyttelse
- **Flerlags Ratebegrænsning**: Implementer ratebegrænsning på bruger-, session-, værktøjs- og ressourceniveau for at forhindre misbrug  
- **Adaptiv Ratebegrænsning**: Brug maskinlæringsbaseret ratebegrænsning, der tilpasser sig brugsmønstre og trusselindikatorer  
- **Ressourcekvotestyring**: Sæt passende grænser for beregningsressourcer, hukommelsesforbrug og eksekveringstid  
- **DDoS-beskyttelse**: Implementer omfattende DDoS-beskyttelse og trafikanalysesystemer  

### 5. Omfattende Logning og Overvågning
- **Struktureret Auditlogning**: Implementer detaljerede, søgbare logs for alle MCP-operationer, værktøjseksekveringer og sikkerhedshændelser  
- **Realtids Sikkerhedsovervågning**: Brug SIEM-systemer med AI-drevet anomali-detektion til MCP-arbejdsbelastninger  
- **Privatlivskompatibel Logning**: Log sikkerhedshændelser under hensyntagen til databeskyttelseskrav og -regler  
- **Integration af Hændelsesrespons**: Forbind logningssystemer med automatiserede hændelsesresponsarbejdsgange  

### 6. Forbedrede Sikker Lagringspraksisser
- **Hardware Security Modules**: Brug HSM-understøttet nøglelagring (Azure Key Vault, AWS CloudHSM) til kritiske kryptografiske operationer  
- **Krypteringsnøglehåndtering**: Implementer korrekt nøglerotation, adskillelse og adgangskontrol for krypteringsnøgler  
- **Hemmelighedshåndtering**: Opbevar alle API-nøgler, tokens og legitimationsoplysninger i dedikerede hemmelighedshåndteringssystemer  
- **Dataklassificering**: Klassificér data baseret på følsomhedsniveauer og anvend passende beskyttelsesforanstaltninger  

### 7. Avanceret Tokenhåndtering
- **Forhindring af Tokenpassthrough**: Forbyd eksplicit tokenpassthrough-mønstre, der omgår sikkerhedskontroller  
- **Validering af Målgruppe**: Verificér altid, at tokenmålgruppekrav matcher den tilsigtede MCP-serveridentitet  
- **Claims-baseret Autorisation**: Implementer detaljeret autorisation baseret på tokenclaims og brugerattributter  
- **Tokenbinding**: Bind tokens til specifikke sessioner, brugere eller enheder, hvor det er relevant  

### 8. Sikker Sessionshåndtering
- **Kryptografiske Sessions-ID'er**: Generér sessions-ID'er ved hjælp af kryptografisk sikre tilfældige talgeneratorer (ikke forudsigelige sekvenser)  
- **Brugerspecifik Binding**: Bind sessions-ID'er til brugerspecifik information ved hjælp af sikre formater som `<user_id>:<session_id>`  
- **Kontrol af Sessionslivscyklus**: Implementer korrekt sessionseksponering, rotation og ugyldiggørelsesmekanismer  
- **Sikkerhedsoverskrifter for Sessioner**: Brug passende HTTP-sikkerhedsoverskrifter til sessionsbeskyttelse  

### 9. AI-specifikke Sikkerhedskontroller
- **Forsvar mod Promptinjektion**: Brug Microsoft Prompt Shields med spotlighting, afgrænsere og datamarkeringsmetoder  
- **Forebyggelse af Værktøjsforgiftning**: Valider værktøjsmetadata, overvåg for dynamiske ændringer og verificér værktøjets integritet  
- **Validering af Modeloutput**: Gennemgå modeloutput for potentielle datalækager, skadeligt indhold eller overtrædelser af sikkerhedspolitikker  
- **Beskyttelse af Kontekstvindue**: Implementer kontroller for at forhindre forgiftning og manipulation af kontekstvinduer  

### 10. Sikker Eksekvering af Værktøjer
- **Eksekveringssandboxing**: Kør værktøjseksekveringer i containeriserede, isolerede miljøer med ressourcebegrænsninger  
- **Adskillelse af Rettigheder**: Eksekvér værktøjer med minimale nødvendige rettigheder og separate servicekonti  
- **Netværksisolering**: Implementer netværkssegmentering for værktøjseksekveringsmiljøer  
- **Overvågning af Eksekvering**: Overvåg værktøjseksekvering for unormal adfærd, ressourceforbrug og sikkerhedsbrud  

### 11. Kontinuerlig Sikkerhedsvalidering
- **Automatiseret Sikkerhedstest**: Integrér sikkerhedstest i CI/CD-pipelines med værktøjer som GitHub Advanced Security  
- **Sårbarhedshåndtering**: Gennemgå regelmæssigt alle afhængigheder, inklusive AI-modeller og eksterne tjenester  
- **Penetrationstest**: Udfør regelmæssige sikkerhedsvurderinger, der specifikt retter sig mod MCP-implementeringer  
- **Sikkerhedskodegennemgang**: Implementer obligatoriske sikkerhedsgennemgange for alle MCP-relaterede kodeændringer  

### 12. Forsyningskædesikkerhed for AI
- **Komponentverifikation**: Verificér oprindelse, integritet og sikkerhed for alle AI-komponenter (modeller, embeddings, API'er)  
- **Afhængighedsstyring**: Vedligehold opdaterede inventarer over alle software- og AI-afhængigheder med sårbarhedssporing  
- **Betroede Repositorier**: Brug verificerede, betroede kilder til alle AI-modeller, biblioteker og værktøjer  
- **Forsyningskædeovervågning**: Overvåg løbende for kompromitteringer i AI-tjenesteudbydere og modelrepositorier  

## Avancerede Sikkerhedsmønstre

### Zero Trust Arkitektur for MCP
- **Aldrig Stol På, Altid Verificér**: Implementér kontinuerlig verifikation for alle MCP-deltagere  
- **Mikrosegmentering**: Isolér MCP-komponenter med detaljerede netværks- og identitetskontroller  
- **Betinget Adgang**: Implementér risikobaserede adgangskontroller, der tilpasser sig kontekst og adfærd  
- **Kontinuerlig Risikovurdering**: Evaluer dynamisk sikkerhedstilstanden baseret på aktuelle trusselindikatorer  

### Privatlivsbevarende AI-Implementering
- **Dataminimering**: Eksponér kun de nødvendige data for hver MCP-operation  
- **Differential Privacy**: Implementér privatlivsbevarende teknikker til behandling af følsomme data  
- **Homomorfisk Kryptering**: Brug avancerede krypteringsteknikker til sikker beregning på krypterede data  
- **Federeret Læring**: Implementér distribuerede læringsmetoder, der bevarer datalokalitet og privatliv  

### Hændelsesrespons for AI-Systemer
- **AI-specifikke Hændelsesprocedurer**: Udvikl hændelsesresponsprocedurer, der er skræddersyet til AI- og MCP-specifikke trusler  
- **Automatiseret Respons**: Implementér automatiseret inddæmning og afhjælpning for almindelige AI-sikkerhedshændelser  
- **Forensiske Kapaciteter**: Oprethold beredskab til retsmedicinsk analyse af AI-systemkompromitteringer og databrud  
- **Gendannelsesprocedurer**: Etabler procedurer for gendannelse efter AI-modelforgiftning, promptinjektionsangreb og tjenestekompromitteringer  

## Implementeringsressourcer og Standarder

### Officiel MCP Dokumentation
- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Aktuel MCP-protokolspecifikation  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Officiel sikkerhedsvejledning  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Autentifikations- og autorisationsmønstre  
- [MCP Transport Security](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Krav til transportlagssikkerhed  

### Microsoft Sikkerhedsløsninger
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Avanceret beskyttelse mod promptinjektion  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Omfattende AI-indholdsfiltrering  
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Identitets- og adgangsstyring til virksomheder  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Sikker håndtering af hemmeligheder og legitimationsoplysninger  
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Forsyningskæde- og kodesikkerhedsscanning  

### Sikkerhedsstandarder og Rammeværk
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Aktuel OAuth-sikkerhedsvejledning  
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Webapplikationssikkerhedsrisici  
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI-specifikke sikkerhedsrisici  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Omfattende AI-risikostyring  
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Informationssikkerhedsstyringssystemer  

### Implementeringsguider og Tutorials
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Mønstre for virksomhedsauthentifikation  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integration af identitetsudbydere  
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Bedste praksis for tokenhåndtering  
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Avancerede krypteringsmønstre  

### Avancerede Sikkerhedsressourcer
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Sikker udviklingspraksis  
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - AI-specifik sikkerhedstestning  
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - AI-trusselsmodelleringsmetodik  
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Privatlivsbevarende AI-teknikker  

### Overholdelse og Styring
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Privatlivsoverholdelse i AI-systemer  
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Ansvarlig AI-implementering  
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Sikkerhedskontroller for AI-tjenesteudbydere  
- [HIPAA Compliance for AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Sundheds-AI-overholdelseskrav  

### DevSecOps og Automatisering
- [DevSecOps Pipeline for AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Sikker udviklingspipeline for AI  
- [Automated Security Testing](https://learn.microsoft.com/security/engineering/devsecops) - Kontinuerlig sikkerhedsvalidering  
- [Infrastructure as Code Security](https://learn.microsoft.com/security/engineering/infrastructure-security) - Sikker infrastrukturudrulning  
- [Container Security for AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Sikkerhed for AI-arbejdsbelastninger i containere  

### Overvågning og Hændelsesrespons  
- [Azure Monitor for AI Workloads](https://learn.microsoft.com/azure/azure-monitor/overview) - Omfattende overvågningsløsninger  
- [AI Security Incident Response](https://learn.microsoft.com/security/compass/incident-response-playbooks) - AI-specifikke hændelsesprocedurer  
- [SIEM for AI Systems](https://learn.microsoft.com/azure/sentinel/overview) - Sikkerhedsinformation og hændelsesstyring  
- [Threat Intelligence for AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Kilder til AI-trusselsinformation  

## 🔄 Kontinuerlig Forbedring

### Hold Dig Opdateret med Udviklende Standarder
- **Opdateringer til MCP-specifikation**: Følg officielle ændringer i MCP-specifikationen og sikkerhedsrådgivninger  
- **Trusselsinformation**: Abonnér på AI-sikkerhedstrusselsfeeds og sårbarhedsdatabaser  
- **Fællesskabsengagement**: Deltag i MCP-sikkerhedsdiskussioner og arbejdsgrupper  
- **Regelmæssig Vurdering**: Gennemfør kvartalsvise vurderinger af sikkerhedstilstanden og opdater praksisser derefter  

### Bidrag til MCP-sikkerhed
- **Sikkerhedsforskning**: Bidrag til MCP-sikkerhedsforskning og programmer for sårbarhedsrapportering  
- **Deling af Bedste Praksis**
- **Udvikling af værktøjer**: Udvikle og dele sikkerhedsværktøjer og biblioteker til MCP-økosystemet

---

*Dette dokument afspejler MCP-sikkerhedsbedste praksis pr. 18. august 2025, baseret på MCP-specifikationen 2025-06-18. Sikkerhedspraksis bør regelmæssigt gennemgås og opdateres, efterhånden som protokollen og trusselslandskabet udvikler sig.*

**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi er ikke ansvarlige for eventuelle misforståelser eller fejltolkninger, der måtte opstå som følge af brugen af denne oversættelse.