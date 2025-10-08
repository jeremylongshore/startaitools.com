<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T16:32:04+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "nl"
}
-->
# MCP Beveiligingsrichtlijnen 2025

Deze uitgebreide gids beschrijft essentiële beveiligingsrichtlijnen voor het implementeren van Model Context Protocol (MCP)-systemen op basis van de nieuwste **MCP Specificatie 2025-06-18** en huidige industriestandaarden. De richtlijnen behandelen zowel traditionele beveiligingskwesties als AI-specifieke bedreigingen die uniek zijn voor MCP-implementaties.

## Kritieke Beveiligingseisen

### Verplichte Beveiligingsmaatregelen (MUST-eisen)

1. **Tokenvalidatie**: MCP-servers **MOGEN GEEN** tokens accepteren die niet expliciet zijn uitgegeven voor de MCP-server zelf.
2. **Autorisatieverificatie**: MCP-servers die autorisatie implementeren **MOETEN** ALLE inkomende verzoeken verifiëren en **MOGEN GEEN** sessies gebruiken voor authenticatie.  
3. **Gebruikersinstemming**: MCP-proxyservers die statische client-ID's gebruiken **MOETEN** expliciete gebruikersinstemming verkrijgen voor elke dynamisch geregistreerde client.
4. **Veilige sessie-ID's**: MCP-servers **MOETEN** cryptografisch veilige, niet-deterministische sessie-ID's gebruiken die zijn gegenereerd met veilige willekeurige getalgeneratoren.

## Kernbeveiligingspraktijken

### 1. Validatie en Sanering van Invoer
- **Uitgebreide Invoervalidatie**: Valideer en saneer alle invoer om injectieaanvallen, confused deputy-problemen en promptinjectie-kwetsbaarheden te voorkomen.
- **Parameter Schema Handhaving**: Implementeer strikte JSON-schema-validatie voor alle toolparameters en API-invoer.
- **Inhoudsfiltering**: Gebruik Microsoft Prompt Shields en Azure Content Safety om schadelijke inhoud in prompts en reacties te filteren.
- **Uitvoersanering**: Valideer en saneer alle modeluitvoer voordat deze aan gebruikers of downstreamsystemen wordt gepresenteerd.

### 2. Uitmuntendheid in Authenticatie en Autorisatie  
- **Externe Identiteitsproviders**: Besteed authenticatie uit aan gevestigde identiteitsproviders (Microsoft Entra ID, OAuth 2.1-providers) in plaats van zelf authenticatie te implementeren.
- **Fijnmazige Machtigingen**: Implementeer gedetailleerde, tool-specifieke machtigingen volgens het principe van minimale rechten.
- **Tokenlevenscyclusbeheer**: Gebruik kortdurende toegangstokens met veilige rotatie en juiste validatie van de doelgroep.
- **Multi-factor Authenticatie**: Vereis MFA voor alle administratieve toegang en gevoelige operaties.

### 3. Veilige Communicatieprotocollen
- **Transportlaagbeveiliging**: Gebruik HTTPS/TLS 1.3 voor alle MCP-communicatie met juiste certificaatvalidatie.
- **End-to-End Encryptie**: Implementeer extra encryptielagen voor zeer gevoelige gegevens tijdens transport en opslag.
- **Certificaatbeheer**: Onderhoud een correct certificaatlevenscyclusbeheer met geautomatiseerde verlengingsprocessen.
- **Protocolversie Handhaving**: Gebruik de huidige MCP-protocolversie (2025-06-18) met correcte versieonderhandeling.

### 4. Geavanceerde Rate Limiting & Resourcebescherming
- **Meerdere lagen Rate Limiting**: Implementeer rate limiting op gebruikers-, sessie-, tool- en resource-niveau om misbruik te voorkomen.
- **Adaptieve Rate Limiting**: Gebruik machine learning-gebaseerde rate limiting die zich aanpast aan gebruikspatronen en dreigingsindicatoren.
- **Resourcequotabeheer**: Stel passende limieten in voor computermiddelen, geheugengebruik en uitvoeringstijd.
- **DDoS-bescherming**: Zet uitgebreide DDoS-bescherming en verkeersanalysesystemen in.

### 5. Uitgebreide Logging & Monitoring
- **Gestructureerde Audit Logging**: Implementeer gedetailleerde, doorzoekbare logs voor alle MCP-operaties, toolexecuties en beveiligingsevenementen.
- **Realtime Beveiligingsmonitoring**: Zet SIEM-systemen in met AI-gestuurde anomaliedetectie voor MCP-werkbelastingen.
- **Privacy-compliant Logging**: Log beveiligingsevenementen met respect voor gegevensprivacyvereisten en regelgeving.
- **Incidentrespons Integratie**: Verbind logsystemen met geautomatiseerde incidentrespons-workflows.

### 6. Verbeterde Veilige Opslagpraktijken
- **Hardware Security Modules**: Gebruik HSM-ondersteunde sleutelopslag (Azure Key Vault, AWS CloudHSM) voor kritieke cryptografische operaties.
- **Encryptiesleutelbeheer**: Implementeer correcte sleutelrotatie, scheiding en toegangscontrole voor encryptiesleutels.
- **Geheimenbeheer**: Sla alle API-sleutels, tokens en referenties op in speciale geheimenbeheersystemen.
- **Gegevensclassificatie**: Classificeer gegevens op basis van gevoeligheidsniveaus en pas passende beschermingsmaatregelen toe.

### 7. Geavanceerd Tokenbeheer
- **Token Passthrough Preventie**: Verbied expliciet token passthrough-patronen die beveiligingsmaatregelen omzeilen.
- **Doelgroepvalidatie**: Controleer altijd of token-doelgroepclaims overeenkomen met de beoogde MCP-serveridentiteit.
- **Claims-gebaseerde Autorisatie**: Implementeer gedetailleerde autorisatie op basis van tokenclaims en gebruikerskenmerken.
- **Tokenbinding**: Bind tokens aan specifieke sessies, gebruikers of apparaten waar nodig.

### 8. Veilige Sessiebeheer
- **Cryptografische Sessie-ID's**: Genereer sessie-ID's met cryptografisch veilige willekeurige getalgeneratoren (geen voorspelbare reeksen).
- **Gebruikersspecifieke Binding**: Bind sessie-ID's aan gebruikersspecifieke informatie met veilige formaten zoals `<user_id>:<session_id>`.
- **Sessielevencyclusbeheer**: Implementeer correcte sessieverloop, rotatie en ongeldigverklaring.
- **Sessiebeveiligingsheaders**: Gebruik geschikte HTTP-beveiligingsheaders voor sessiebescherming.

### 9. AI-specifieke Beveiligingsmaatregelen
- **Promptinjectie Verdediging**: Zet Microsoft Prompt Shields in met spotlighting, delimiters en datamarking-technieken.
- **Toolvergiftiging Preventie**: Valideer toolmetadata, monitor dynamische wijzigingen en verifieer toolintegriteit.
- **Modeluitvoer Validatie**: Scan modeluitvoer op mogelijke gegevenslekken, schadelijke inhoud of schendingen van beveiligingsbeleid.
- **Contextvenster Bescherming**: Implementeer controles om contextvenstervergiftiging en manipulatieaanvallen te voorkomen.

### 10. Tooluitvoeringsbeveiliging
- **Uitvoeringssandboxing**: Voer tooluitvoeringen uit in gecontaineriseerde, geïsoleerde omgevingen met resourcebeperkingen.
- **Scheiding van Privileges**: Voer tools uit met minimale vereiste privileges en gescheiden serviceaccounts.
- **Netwerkisolatie**: Implementeer netwerksegmentatie voor tooluitvoeringsomgevingen.
- **Uitvoeringsmonitoring**: Monitor tooluitvoeringen op afwijkend gedrag, resourcegebruik en beveiligingsschendingen.

### 11. Continue Beveiligingsvalidatie
- **Geautomatiseerde Beveiligingstests**: Integreer beveiligingstests in CI/CD-pijplijnen met tools zoals GitHub Advanced Security.
- **Kwetsbaarheidsbeheer**: Scan regelmatig alle afhankelijkheden, inclusief AI-modellen en externe services.
- **Penetratietests**: Voer regelmatig beveiligingsbeoordelingen uit die specifiek gericht zijn op MCP-implementaties.
- **Beveiligingscode Reviews**: Implementeer verplichte beveiligingsreviews voor alle MCP-gerelateerde codewijzigingen.

### 12. Leveringsketenbeveiliging voor AI
- **Componentverificatie**: Verifieer herkomst, integriteit en beveiliging van alle AI-componenten (modellen, embeddings, API's).
- **Afhankelijkheidsbeheer**: Onderhoud actuele inventarissen van alle software- en AI-afhankelijkheden met kwetsbaarheidstracking.
- **Vertrouwde Repositories**: Gebruik geverifieerde, vertrouwde bronnen voor alle AI-modellen, bibliotheken en tools.
- **Leveringsketenmonitoring**: Monitor continu op compromissen bij AI-serviceproviders en modelrepositories.

## Geavanceerde Beveiligingspatronen

### Zero Trust Architectuur voor MCP
- **Nooit Vertrouwen, Altijd Verifiëren**: Implementeer continue verificatie voor alle MCP-deelnemers.
- **Micro-segmentatie**: Isoleer MCP-componenten met gedetailleerde netwerk- en identiteitscontroles.
- **Voorwaardelijke Toegang**: Implementeer risicogebaseerde toegangscontroles die zich aanpassen aan context en gedrag.
- **Continue Risicobeoordeling**: Evalueer dynamisch de beveiligingsstatus op basis van actuele dreigingsindicatoren.

### Privacybeschermende AI-implementatie
- **Gegevensminimalisatie**: Stel alleen de minimaal noodzakelijke gegevens bloot voor elke MCP-operatie.
- **Differentiële Privacy**: Implementeer privacybeschermende technieken voor gevoelige gegevensverwerking.
- **Homomorfe Encryptie**: Gebruik geavanceerde encryptietechnieken voor veilige berekeningen op versleutelde gegevens.
- **Federatief Leren**: Implementeer gedistribueerde leerbenaderingen die gegevenslokaliteit en privacy behouden.

### Incidentrespons voor AI-systemen
- **AI-specifieke Incidentprocedures**: Ontwikkel incidentresponsprocedures die zijn afgestemd op AI- en MCP-specifieke bedreigingen.
- **Geautomatiseerde Respons**: Implementeer geautomatiseerde containment en herstel voor veelvoorkomende AI-beveiligingsincidenten.  
- **Forensische Capaciteiten**: Zorg voor forensische gereedheid bij compromissen van AI-systemen en datalekken.
- **Herstelprocedures**: Stel procedures op voor herstel na AI-modelvergiftiging, promptinjectie-aanvallen en servicecompromissen.

## Implementatiebronnen & Standaarden

### Officiële MCP Documentatie
- [MCP Specificatie 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Huidige MCP-protocolspecificatie
- [MCP Beveiligingsrichtlijnen](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Officiële beveiligingsrichtlijnen
- [MCP Autorisatiespecificatie](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Authenticatie- en autorisatiepatronen
- [MCP Transportbeveiliging](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Transportlaagbeveiligingseisen

### Microsoft Beveiligingsoplossingen
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Geavanceerde bescherming tegen promptinjectie
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Uitgebreide AI-inhoudsfiltering
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Identiteits- en toegangsbeheer voor ondernemingen
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Veilige opslag van geheimen en referenties
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Leveringsketen- en codebeveiligingsscanning

### Beveiligingsstandaarden & Frameworks
- [OAuth 2.1 Beveiligingsrichtlijnen](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Huidige OAuth-beveiligingsrichtlijnen
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Webapplicatiebeveiligingsrisico's
- [OWASP Top 10 voor LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI-specifieke beveiligingsrisico's
- [NIST AI Risicobeheer Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Uitgebreid AI-risicobeheer
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Beheersystemen voor informatiebeveiliging

### Implementatiegidsen & Tutorials
- [Azure API Management als MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Authenticatiepatronen voor ondernemingen
- [Microsoft Entra ID met MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integratie van identiteitsproviders
- [Implementatie van Veilige Tokenopslag](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Beste praktijken voor tokenbeheer
- [End-to-End Encryptie voor AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Geavanceerde encryptiepatronen

### Geavanceerde Beveiligingsbronnen
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Praktijken voor veilige ontwikkeling
- [AI Red Team Richtlijnen](https://learn.microsoft.com/security/ai-red-team/) - AI-specifieke beveiligingstests
- [Dreigingsmodellering voor AI-systemen](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Methodologie voor dreigingsmodellering van AI
- [Privacy Engineering voor AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Privacybeschermende AI-technieken

### Naleving & Governance
- [GDPR Naleving voor AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Privacy-naleving in AI-systemen
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Verantwoordelijke AI-implementatie
- [SOC 2 voor AI-diensten](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Beveiligingscontroles voor AI-serviceproviders
- [HIPAA Naleving voor AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - AI-nalevingseisen voor de gezondheidszorg

### DevSecOps & Automatisering
- [DevSecOps Pijplijn voor AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Veilige AI-ontwikkelingspijplijnen
- [Geautomatiseerde Beveiligingstests](https://learn.microsoft.com/security/engineering/devsecops) - Continue beveiligingsvalidatie
- [Infrastructure as Code Beveiliging](https://learn.microsoft.com/security/engineering/infrastructure-security) - Veilige infrastructuurimplementatie
- [Containerbeveiliging voor AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Beveiliging van AI-werkbelastingen in containers

### Monitoring & Incidentrespons  
- [Azure Monitor voor AI-werkbelastingen](https://learn.microsoft.com/azure/azure-monitor/overview) - Uitgebreide monitoringsoplossingen
- [AI Beveiligingsincidentrespons](https://learn.microsoft.com/security/compass/incident-response-playbooks) - AI-specifieke incidentprocedures
- [SIEM voor AI-systemen](https://learn.microsoft.com/azure/sentinel/overview) - Security Information and Event Management
- [Dreigingsinformatie voor AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Bronnen voor AI-dreigingsinformatie

## 🔄 Continue Verbetering

### Blijf Op de Hoogte van Evoluerende Standaarden
- **MCP Specificatie Updates**: Houd officiële MCP-specificatiewijzigingen en beveiligingsadviezen in de gaten.
- **Dreigingsinformatie**: Abonneer op AI-beveiligingsdreigingsfeeds en kwetsbaarheidsdatabases.  
- **Communitybetrokkenheid**: Neem deel aan MCP-beveiligingscommunitydiscussies en werkgroepen.
- **Regelmatige Beoordeling**: Voer driemaandelijkse beoordelingen van de beveiligingsstatus uit en werk praktijken dienovereenkomstig bij.

### Bijdragen aan MCP Beveiliging
- **Beveiligingsonderzoek**: Draag bij aan MCP-beveiligingsonderzoek en programma's voor kwetsbaarheidsmeldingen.
- **Delen van Beste Praktijken**: Deel beveiligingsimplementaties en geleerde lessen met de community.
- **Standaardontwikkeling**: Neem deel aan de ontwikkeling van MCP-specificaties en het creëren van beveiligingsstandaarden.
- **Ontwikkeling van tools**: Ontwikkel en deel beveiligingstools en bibliotheken voor het MCP-ecosysteem

---

*Dit document weerspiegelt de beste beveiligingspraktijken voor MCP vanaf 18 augustus 2025, gebaseerd op MCP Specificatie 2025-06-18. Beveiligingspraktijken moeten regelmatig worden herzien en bijgewerkt naarmate het protocol en het dreigingslandschap zich ontwikkelen.*

**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we ons best doen voor nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.