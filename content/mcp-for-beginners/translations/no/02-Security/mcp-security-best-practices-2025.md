<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T15:39:09+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "no"
}
-->
# MCP Sikkerhetspraksis - Oppdatering August 2025

> **Viktig**: Dette dokumentet reflekterer de nyeste [MCP Spesifikasjon 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) sikkerhetskravene og offisielle [MCP Sikkerhetspraksis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Sørg alltid for å referere til den gjeldende spesifikasjonen for den mest oppdaterte veiledningen.

## Essensielle sikkerhetspraksiser for MCP-implementeringer

Model Context Protocol introduserer unike sikkerhetsutfordringer som går utover tradisjonell programvaresikkerhet. Disse praksisene adresserer både grunnleggende sikkerhetskrav og MCP-spesifikke trusler, inkludert prompt-injeksjon, verktøyforgiftning, sesjonshijacking, forvirrede stedfortrederproblemer og token-passering sårbarheter.

### **OBLIGATORISKE sikkerhetskrav**

**Kritiske krav fra MCP Spesifikasjon:**

> **MÅ IKKE**: MCP-servere **MÅ IKKE** akseptere noen tokens som ikke eksplisitt ble utstedt for MCP-serveren  
> 
> **MÅ**: MCP-servere som implementerer autorisasjon **MÅ** verifisere ALLE innkommende forespørsler  
>  
> **MÅ IKKE**: MCP-servere **MÅ IKKE** bruke sesjoner for autentisering  
>
> **MÅ**: MCP proxy-servere som bruker statiske klient-IDer **MÅ** innhente brukerens samtykke for hver dynamisk registrerte klient  

---

## 1. **Token-sikkerhet og autentisering**

**Kontroller for autentisering og autorisasjon:**  
   - **Grundig autorisasjonsgjennomgang**: Utfør omfattende revisjoner av MCP-serverens autorisasjonslogikk for å sikre at kun tiltenkte brukere og klienter har tilgang til ressurser  
   - **Integrasjon med eksterne identitetsleverandører**: Bruk etablerte identitetsleverandører som Microsoft Entra ID i stedet for å implementere egen autentisering  
   - **Validering av token-målgruppe**: Valider alltid at tokens eksplisitt ble utstedt for din MCP-server - aksepter aldri oppstrøms tokens  
   - **Riktig token-livssyklus**: Implementer sikker token-rotasjon, utløpspolicyer og forhindre replay-angrep  

**Beskyttet token-lagring:**  
   - Bruk Azure Key Vault eller lignende sikre lagringsløsninger for alle hemmeligheter  
   - Implementer kryptering for tokens både i hvilemodus og under transport  
   - Regelmessig rotasjon av legitimasjon og overvåking for uautorisert tilgang  

## 2. **Sesjonshåndtering og transport-sikkerhet**

**Sikre sesjonspraksiser:**  
   - **Kryptografisk sikre sesjons-IDer**: Bruk sikre, ikke-deterministiske sesjons-IDer generert med sikre tilfeldige tallgeneratorer  
   - **Bruker-spesifikk binding**: Bind sesjons-IDer til brukeridentiteter ved å bruke formater som `<user_id>:<session_id>` for å forhindre misbruk av sesjoner på tvers av brukere  
   - **Håndtering av sesjonslivssyklus**: Implementer riktig utløp, rotasjon og ugyldiggjøring for å begrense sårbarhetsvinduer  
   - **HTTPS/TLS påbud**: Obligatorisk HTTPS for all kommunikasjon for å forhindre avlytting av sesjons-IDer  

**Transportlagssikkerhet:**  
   - Konfigurer TLS 1.3 der det er mulig med riktig sertifikathåndtering  
   - Implementer sertifikat-pinning for kritiske forbindelser  
   - Regelmessig rotasjon av sertifikater og verifisering av gyldighet  

## 3. **AI-spesifikk trusselbeskyttelse** 🤖

**Forsvar mot prompt-injeksjon:**  
   - **Microsoft Prompt Shields**: Bruk AI Prompt Shields for avansert deteksjon og filtrering av skadelige instruksjoner  
   - **Input-sanitisering**: Valider og rens alle innspill for å forhindre injeksjonsangrep og forvirrede stedfortrederproblemer  
   - **Innholdsgrenser**: Bruk avgrensnings- og datamerkesystemer for å skille mellom betrodde instruksjoner og eksternt innhold  

**Forebygging av verktøyforgiftning:**  
   - **Validering av verktøymetadata**: Implementer integritetskontroller for verktøydefinisjoner og overvåk for uventede endringer  
   - **Dynamisk verktøyovervåking**: Overvåk runtime-oppførsel og sett opp varsler for uventede utførelsesmønstre  
   - **Godkjenningsarbeidsflyter**: Krev eksplisitt brukerens godkjenning for verktøyendringer og kapabilitetsmodifikasjoner  

## 4. **Tilgangskontroll og tillatelser**

**Prinsippet om minst privilegium:**  
   - Gi MCP-servere kun minimumstillatelser som kreves for tiltenkt funksjonalitet  
   - Implementer rollebasert tilgangskontroll (RBAC) med detaljerte tillatelser  
   - Regelmessige tillatelsesgjennomganger og kontinuerlig overvåking for privilegieeskalering  

**Kontroller for runtime-tillatelser:**  
   - Påfør ressursgrenser for å forhindre angrep som utnytter ressursuttømming  
   - Bruk containerisolasjon for verktøyutførelsesmiljøer  
   - Implementer tilgang etter behov for administrative funksjoner  

## 5. **Innholdssikkerhet og overvåking**

**Implementering av innholdssikkerhet:**  
   - **Azure Content Safety-integrasjon**: Bruk Azure Content Safety for å oppdage skadelig innhold, forsøk på jailbreak og policybrudd  
   - **Atferdsanalyse**: Implementer runtime-atferdsovervåking for å oppdage anomalier i MCP-server og verktøyutførelse  
   - **Omfattende logging**: Logg alle autentiseringsforsøk, verktøyaktiveringer og sikkerhetshendelser med sikker, manipulasjonssikker lagring  

**Kontinuerlig overvåking:**  
   - Sanntidsvarsling for mistenkelige mønstre og uautoriserte tilgangsforsøk  
   - Integrasjon med SIEM-systemer for sentralisert sikkerhetshendelseshåndtering  
   - Regelmessige sikkerhetsrevisjoner og penetrasjonstesting av MCP-implementeringer  

## 6. **Forsyningskjede-sikkerhet**

**Komponentverifisering:**  
   - **Avhengighetsskanning**: Bruk automatisert sårbarhetsskanning for alle programvareavhengigheter og AI-komponenter  
   - **Provenansvalidering**: Verifiser opprinnelse, lisensiering og integritet av modeller, datakilder og eksterne tjenester  
   - **Signerte pakker**: Bruk kryptografisk signerte pakker og verifiser signaturer før distribusjon  

**Sikker utviklingspipeline:**  
   - **GitHub Advanced Security**: Implementer hemmelighetsskanning, avhengighetsanalyse og CodeQL statisk analyse  
   - **CI/CD-sikkerhet**: Integrer sikkerhetsvalidering gjennom automatiserte distribusjonspipelines  
   - **Artefaktintegritet**: Implementer kryptografisk verifisering for distribuerte artefakter og konfigurasjoner  

## 7. **OAuth-sikkerhet og forebygging av forvirrede stedfortrederproblemer**

**OAuth 2.1-implementering:**  
   - **PKCE-implementering**: Bruk Proof Key for Code Exchange (PKCE) for alle autorisasjonsforespørsler  
   - **Eksplisitt samtykke**: Innhent brukerens samtykke for hver dynamisk registrerte klient for å forhindre forvirrede stedfortrederangrep  
   - **Validering av omdirigerings-URI**: Implementer streng validering av omdirigerings-URIer og klientidentifikatorer  

**Proxy-sikkerhet:**  
   - Forhindre autorisasjonsomgåelse gjennom utnyttelse av statiske klient-IDer  
   - Implementer riktige samtykkearbeidsflyter for tredjeparts API-tilgang  
   - Overvåk for tyveri av autorisasjonskoder og uautorisert API-tilgang  

## 8. **Hendelseshåndtering og gjenoppretting**

**Rask responskapasitet:**  
   - **Automatisert respons**: Implementer automatiserte systemer for legitimasjonsrotasjon og trusselbegrensning  
   - **Tilbakerullingsprosedyrer**: Evne til raskt å gå tilbake til kjente gode konfigurasjoner og komponenter  
   - **Forensiske kapasiteter**: Detaljerte revisjonsspor og logging for hendelsesundersøkelser  

**Kommunikasjon og koordinering:**  
   - Klare eskaleringsprosedyrer for sikkerhetshendelser  
   - Integrasjon med organisasjonens hendelseshåndteringsteam  
   - Regelmessige simuleringer av sikkerhetshendelser og bordøvelser  

## 9. **Overholdelse og styring**

**Regulatorisk overholdelse:**  
   - Sørg for at MCP-implementeringer oppfyller bransjespesifikke krav (GDPR, HIPAA, SOC 2)  
   - Implementer dataklassifisering og personvernkontroller for AI-databehandling  
   - Oppretthold omfattende dokumentasjon for revisjon av overholdelse  

**Endringshåndtering:**  
   - Formelle sikkerhetsgjennomgangsprosesser for alle MCP-systemmodifikasjoner  
   - Versjonskontroll og godkjenningsarbeidsflyter for konfigurasjonsendringer  
   - Regelmessige vurderinger av overholdelse og gap-analyser  

## 10. **Avanserte sikkerhetskontroller**

**Zero Trust-arkitektur:**  
   - **Aldri stol, alltid verifiser**: Kontinuerlig verifisering av brukere, enheter og forbindelser  
   - **Mikrosegmentering**: Granulære nettverkskontroller som isolerer individuelle MCP-komponenter  
   - **Betinget tilgang**: Risiko-baserte tilgangskontroller som tilpasser seg nåværende kontekst og oppførsel  

**Runtime-applikasjonsbeskyttelse:**  
   - **Runtime Application Self-Protection (RASP)**: Bruk RASP-teknikker for sanntidsdeteksjon av trusler  
   - **Applikasjonsytelsesovervåking**: Overvåk ytelsesanomalier som kan indikere angrep  
   - **Dynamiske sikkerhetspolicyer**: Implementer sikkerhetspolicyer som tilpasser seg basert på nåværende trussellandskap  

## 11. **Microsoft sikkerhetsøkosystemintegrasjon**

**Omfattende Microsoft-sikkerhet:**  
   - **Microsoft Defender for Cloud**: Sikkerhetshåndtering for MCP-arbeidsbelastninger i skyen  
   - **Azure Sentinel**: Skybaserte SIEM- og SOAR-funksjoner for avansert trusseldeteksjon  
   - **Microsoft Purview**: Datastyring og overholdelse for AI-arbeidsflyter og datakilder  

**Identitets- og tilgangshåndtering:**  
   - **Microsoft Entra ID**: Identitetsadministrasjon for bedrifter med betingede tilgangspolicyer  
   - **Privileged Identity Management (PIM)**: Tilgang etter behov og godkjenningsarbeidsflyter for administrative funksjoner  
   - **Identity Protection**: Risiko-baserte betingede tilgangskontroller og automatisert trusselrespons  

## 12. **Kontinuerlig sikkerhetsevolusjon**

**Hold deg oppdatert:**  
   - **Spesifikasjonsmonitorering**: Regelmessig gjennomgang av MCP-spesifikasjonsoppdateringer og endringer i sikkerhetsveiledning  
   - **Trusselinformasjon**: Integrasjon av AI-spesifikke trusselstrømmer og kompromissindikatorer  
   - **Sikkerhetsfellesskap-engasjement**: Aktiv deltakelse i MCP-sikkerhetsfellesskapet og programmer for sårbarhetsrapportering  

**Adaptiv sikkerhet:**  
   - **Maskinlæringssikkerhet**: Bruk ML-basert anomalideteksjon for å identifisere nye angrepsmønstre  
   - **Prediktiv sikkerhetsanalyse**: Implementer prediktive modeller for proaktiv trusselidentifikasjon  
   - **Sikkerhetsautomatisering**: Automatiserte oppdateringer av sikkerhetspolicyer basert på trusselinformasjon og spesifikasjonsendringer  

---

## **Kritiske sikkerhetsressurser**

### **Offisiell MCP-dokumentasjon**  
- [MCP Spesifikasjon (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Sikkerhetspraksis](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Autorisasjonsspesifikasjon](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft sikkerhetsløsninger**  
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Sikkerhet](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Sikkerhetsstandarder**  
- [OAuth 2.0 Sikkerhetspraksis (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Topp 10 for Store Språkmodeller](https://genai.owasp.org/)  
- [NIST AI Risikostyringsrammeverk](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Implementeringsveiledninger**  
- [Azure API Management MCP Autentiseringsgateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID med MCP-servere](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Sikkerhetsvarsel**: MCP-sikkerhetspraksiser utvikler seg raskt. Verifiser alltid mot den gjeldende [MCP-spesifikasjonen](https://spec.modelcontextprotocol.io/) og [offisiell sikkerhetsdokumentasjon](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) før implementering.  

**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi tilstreber nøyaktighet, vennligst vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på sitt opprinnelige språk bør anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.