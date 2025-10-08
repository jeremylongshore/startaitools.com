<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T15:42:48+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "no"
}
-->
# MCP Sikkerhetspraksis 2025

Denne omfattende veiledningen beskriver viktige sikkerhetspraksiser for implementering av Model Context Protocol (MCP)-systemer basert på den nyeste **MCP-spesifikasjonen 2025-06-18** og gjeldende industristandarder. Disse praksisene tar for seg både tradisjonelle sikkerhetsutfordringer og AI-spesifikke trusler som er unike for MCP-distribusjoner.

## Kritiske sikkerhetskrav

### Obligatoriske sikkerhetskontroller (MÅ-krav)

1. **Tokenvalidering**: MCP-servere **MÅ IKKE** akseptere noen tokens som ikke eksplisitt er utstedt for MCP-serveren selv  
2. **Autorisasjonsverifisering**: MCP-servere som implementerer autorisasjon **MÅ** verifisere ALLE innkommende forespørsler og **MÅ IKKE** bruke sesjoner for autentisering  
3. **Brukersamtykke**: MCP-proxyservere som bruker statiske klient-ID-er **MÅ** innhente eksplisitt brukersamtykke for hver dynamisk registrerte klient  
4. **Sikre sesjons-ID-er**: MCP-servere **MÅ** bruke kryptografisk sikre, ikke-deterministiske sesjons-ID-er generert med sikre tilfeldige tallgeneratorer  

## Kjerneprinsipper for sikkerhet

### 1. Validering og sanitering av inndata
- **Omfattende validering av inndata**: Valider og saniter alle inndata for å forhindre injeksjonsangrep, "confused deputy"-problemer og prompt-injeksjons-sårbarheter  
- **Parameter-skjema-håndhevelse**: Implementer streng JSON-skjema-validering for alle verktøyparametere og API-inndata  
- **Innholdsfiltrering**: Bruk Microsoft Prompt Shields og Azure Content Safety for å filtrere skadelig innhold i forespørsler og svar  
- **Sanitering av utdata**: Valider og saniter alle modellutdata før de presenteres for brukere eller nedstrøms systemer  

### 2. Ekspertise innen autentisering og autorisasjon  
- **Eksterne identitetsleverandører**: Deleger autentisering til etablerte identitetsleverandører (Microsoft Entra ID, OAuth 2.1-leverandører) i stedet for å implementere egendefinert autentisering  
- **Fingranulære tillatelser**: Implementer detaljerte, verktøyspesifikke tillatelser i tråd med prinsippet om minste privilegium  
- **Token-livssyklusadministrasjon**: Bruk kortlivede tilgangstokens med sikker rotasjon og korrekt validering av målgruppen  
- **Flerfaktorautentisering**: Krev MFA for all administrativ tilgang og sensitive operasjoner  

### 3. Sikker kommunikasjon
- **Transportlagssikkerhet**: Bruk HTTPS/TLS 1.3 for all MCP-kommunikasjon med korrekt sertifikatvalidering  
- **Ende-til-ende-kryptering**: Implementer ekstra krypteringslag for svært sensitiv data i transitt og i hvile  
- **Sertifikathåndtering**: Oppretthold korrekt sertifikatlivssyklusadministrasjon med automatiserte fornyelsesprosesser  
- **Protokollversjonshåndhevelse**: Bruk gjeldende MCP-protokollversjon (2025-06-18) med korrekt versjonsforhandling  

### 4. Avansert ratebegrensning og ressursbeskyttelse
- **Flerlags ratebegrensning**: Implementer ratebegrensning på bruker-, sesjons-, verktøy- og ressursnivå for å forhindre misbruk  
- **Adaptiv ratebegrensning**: Bruk maskinlæringsbasert ratebegrensning som tilpasser seg bruksmønstre og trusselindikatorer  
- **Ressurskvoteadministrasjon**: Sett passende grenser for beregningsressurser, minnebruk og kjøretid  
- **DDoS-beskyttelse**: Distribuer omfattende DDoS-beskyttelse og trafikkanalysesystemer  

### 5. Omfattende logging og overvåking
- **Strukturert revisjonslogging**: Implementer detaljerte, søkbare logger for alle MCP-operasjoner, verktøyutførelser og sikkerhetshendelser  
- **Sanntidsovervåking av sikkerhet**: Distribuer SIEM-systemer med AI-drevet anomalioppdagelse for MCP-arbeidsbelastninger  
- **Personvernkompatibel logging**: Loggfør sikkerhetshendelser samtidig som du respekterer krav og forskrifter om databeskyttelse  
- **Integrasjon av hendelsesrespons**: Koble loggsystemer til automatiserte arbeidsflyter for hendelsesrespons  

### 6. Forbedrede sikre lagringspraksiser
- **Maskinvarebaserte sikkerhetsmoduler**: Bruk HSM-støttet nøkkellagring (Azure Key Vault, AWS CloudHSM) for kritiske kryptografiske operasjoner  
- **Administrasjon av krypteringsnøkler**: Implementer korrekt nøkkelrotasjon, segregering og tilgangskontroller for krypteringsnøkler  
- **Hemmelighetshåndtering**: Lagre alle API-nøkler, tokens og legitimasjon i dedikerte systemer for hemmelighetshåndtering  
- **Dataklassifisering**: Klassifiser data basert på sensitivitet og anvend passende beskyttelsestiltak  

### 7. Avansert tokenadministrasjon
- **Forhindring av token-passering**: Forby eksplisitt token-passering som omgår sikkerhetskontroller  
- **Validering av målgruppe**: Verifiser alltid at tokenets målgruppekrav samsvarer med den tiltenkte MCP-serveridentiteten  
- **Autorisasjon basert på krav**: Implementer detaljert autorisasjon basert på tokenkrav og brukerattributter  
- **Tokenbinding**: Bind tokens til spesifikke sesjoner, brukere eller enheter der det er hensiktsmessig  

### 8. Sikker sesjonsadministrasjon
- **Kryptografiske sesjons-ID-er**: Generer sesjons-ID-er ved hjelp av kryptografisk sikre tilfeldige tallgeneratorer (ikke forutsigbare sekvenser)  
- **Brukerspesifikk binding**: Bind sesjons-ID-er til brukerspesifikk informasjon ved hjelp av sikre formater som `<user_id>:<session_id>`  
- **Kontroller for sesjonslivssyklus**: Implementer korrekt sesjonsutløp, rotasjon og ugyldiggjøringsmekanismer  
- **Sikkerhetshoder for sesjoner**: Bruk passende HTTP-sikkerhetshoder for sesjonsbeskyttelse  

### 9. AI-spesifikke sikkerhetskontroller
- **Forsvar mot prompt-injeksjon**: Distribuer Microsoft Prompt Shields med spotlighting, avgrensere og datamerkingsteknikker  
- **Forebygging av verktøyforgiftning**: Valider verktøymetadata, overvåk for dynamiske endringer og verifiser verktøyets integritet  
- **Validering av modellutdata**: Skann modellutdata for potensielle datalekkasjer, skadelig innhold eller brudd på sikkerhetspolicyer  
- **Beskyttelse av kontekstvindu**: Implementer kontroller for å forhindre forgiftning og manipulasjon av kontekstvindu  

### 10. Sikkerhet ved verktøyutførelse
- **Sandkasse for utførelse**: Kjør verktøyutførelser i containeriserte, isolerte miljøer med ressursbegrensninger  
- **Separasjon av privilegier**: Utfør verktøy med minimale nødvendige privilegier og separate tjenestekontoer  
- **Nettverksisolasjon**: Implementer nettverkssegmentering for verktøyutførelsesmiljøer  
- **Overvåking av utførelse**: Overvåk verktøyutførelse for unormal oppførsel, ressursbruk og sikkerhetsbrudd  

### 11. Kontinuerlig sikkerhetsvalidering
- **Automatisert sikkerhetstesting**: Integrer sikkerhetstesting i CI/CD-pipelines med verktøy som GitHub Advanced Security  
- **Sårbarhetsadministrasjon**: Skann regelmessig alle avhengigheter, inkludert AI-modeller og eksterne tjenester  
- **Penetrasjonstesting**: Gjennomfør regelmessige sikkerhetsvurderinger som spesifikt retter seg mot MCP-implementeringer  
- **Sikkerhetskodegjennomganger**: Implementer obligatoriske sikkerhetsgjennomganger for alle MCP-relaterte kodeendringer  

### 12. Forsyningskjedesikkerhet for AI
- **Komponentverifisering**: Verifiser opprinnelse, integritet og sikkerhet for alle AI-komponenter (modeller, embeddings, API-er)  
- **Avhengighetsadministrasjon**: Oppretthold oppdaterte oversikter over alle programvare- og AI-avhengigheter med sårbarhetssporing  
- **Pålitelige repositorier**: Bruk verifiserte, pålitelige kilder for alle AI-modeller, biblioteker og verktøy  
- **Overvåking av forsyningskjeden**: Overvåk kontinuerlig for kompromisser hos AI-tjenesteleverandører og modellrepositorier  

## Avanserte sikkerhetsmønstre

### Nulltillitsarkitektur for MCP
- **Aldri stol, alltid verifiser**: Implementer kontinuerlig verifisering for alle MCP-deltakere  
- **Mikrosegmentering**: Isoler MCP-komponenter med detaljerte nettverks- og identitetskontroller  
- **Betinget tilgang**: Implementer risikobaserte tilgangskontroller som tilpasser seg kontekst og atferd  
- **Kontinuerlig risikovurdering**: Evaluer sikkerhetsstatus dynamisk basert på gjeldende trusselindikatorer  

### Personvernbevarende AI-implementering
- **Dataminimering**: Eksponer kun minimum nødvendig data for hver MCP-operasjon  
- **Differensielt personvern**: Implementer personvernbevarende teknikker for behandling av sensitiv data  
- **Homomorfisk kryptering**: Bruk avanserte krypteringsteknikker for sikker beregning på kryptert data  
- **Føderert læring**: Implementer distribuert læring som bevarer datalokalitet og personvern  

### Hendelseshåndtering for AI-systemer
- **AI-spesifikke hendelsesprosedyrer**: Utvikle hendelseshåndteringsprosedyrer tilpasset AI- og MCP-spesifikke trusler  
- **Automatisert respons**: Implementer automatisert inneslutning og utbedring for vanlige AI-sikkerhetshendelser  
- **Forensiske kapabiliteter**: Oppretthold beredskap for rettsmedisinsk analyse ved kompromittering av AI-systemer og datainnbrudd  
- **Gjenopprettingsprosedyrer**: Etabler prosedyrer for gjenoppretting fra AI-modellforgiftning, prompt-injeksjonsangrep og tjenestekompromisser  

## Implementeringsressurser og standarder

### Offisiell MCP-dokumentasjon
- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Gjeldende MCP-protokollspesifikasjon  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Offisiell sikkerhetsveiledning  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Autentiserings- og autorisasjonsmønstre  
- [MCP Transport Security](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Krav til transportlagssikkerhet  

### Microsoft sikkerhetsløsninger
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Avansert beskyttelse mot prompt-injeksjon  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Omfattende AI-innholdsfiltrering  
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Identitets- og tilgangsstyring for bedrifter  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Sikker hemmelighets- og legitimasjonshåndtering  
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Forsyningskjede- og kodesikkerhetsskanning  

### Sikkerhetsstandarder og rammeverk
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Gjeldende OAuth-sikkerhetsveiledning  
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Sikkerhetsrisikoer for webapplikasjoner  
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI-spesifikke sikkerhetsrisikoer  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Omfattende AI-risikostyring  
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Systemer for informasjonssikkerhetsstyring  

### Implementeringsguider og opplæringer
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Autentiseringsmønstre for bedrifter  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integrasjon med identitetsleverandører  
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Beste praksis for tokenadministrasjon  
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Avanserte krypteringsmønstre  

### Avanserte sikkerhetsressurser
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Sikker utviklingspraksis  
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - AI-spesifikk sikkerhetstesting  
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodikk for AI-trusselmodellering  
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Personvernbevarende AI-teknikker  

### Samsvar og styring
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Personvernkrav i AI-systemer  
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Ansvarlig AI-implementering  
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Sikkerhetskontroller for AI-tjenesteleverandører  
- [HIPAA Compliance for AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Samsvarskrav for helse-AI  

### DevSecOps og automatisering
- [DevSecOps Pipeline for AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Sikker utviklingspipeline for AI  
- [Automated Security Testing](https://learn.microsoft.com/security/engineering/devsecops) - Kontinuerlig sikkerhetsvalidering  
- [Infrastructure as Code Security](https://learn.microsoft.com/security/engineering/infrastructure-security) - Sikker distribusjon av infrastruktur  
- [Container Security for AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Sikkerhet for containeriserte AI-arbeidsbelastninger  

### Overvåking og hendelseshåndtering  
- [Azure Monitor for AI Workloads](https://learn.microsoft.com/azure/azure-monitor/overview) - Omfattende overvåkingsløsninger  
- [AI Security Incident Response](https://learn.microsoft.com/security/compass/incident-response-playbooks) - AI-spesifikke hendelsesprosedyrer  
- [SIEM for AI Systems](https://learn.microsoft.com/azure/sentinel/overview) - Sikkerhetsinformasjon og hendelsesadministrasjon  
- [Threat Intelligence for AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Kilder til AI-trusselinformasjon  

## 🔄 Kontinuerlig forbedring

### Hold deg oppdatert med utviklende standarder
- **Oppdateringer i MCP-spesifikasjonen**: Følg med på offisielle endringer i MCP-spesifikasjonen og sikkerhetsråd  
- **Trusselinformasjon**: Abonner på AI-sikkerhetstrusselstrømmer og sårbarhetsdatabaser  
- **Fellesskapsengasjement**: Delta i MCP-sikkerhetsdiskusjoner og arbeidsgrupper  
- **Regelmessig vurdering**: Gjennomfør kvartalsvise vurderinger av sikkerhetsstatus og opp
- **Verktøyutvikling**: Utvikle og dele sikkerhetsverktøy og biblioteker for MCP-økosystemet

---

*Dette dokumentet gjenspeiler MCPs sikkerhetsbeste praksis per 18. august 2025, basert på MCP-spesifikasjonen 2025-06-18. Sikkerhetspraksis bør regelmessig gjennomgås og oppdateres ettersom protokollen og trussellandskapet utvikler seg.*

**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiserte oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på sitt opprinnelige språk bør anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.