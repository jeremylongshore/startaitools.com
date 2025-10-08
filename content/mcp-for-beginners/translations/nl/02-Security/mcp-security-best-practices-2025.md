<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T16:29:53+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "nl"
}
-->
# MCP Beveiligingsrichtlijnen - Update augustus 2025

> **Belangrijk**: Dit document weerspiegelt de nieuwste [MCP Specificatie 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) beveiligingseisen en officiële [MCP Beveiligingsrichtlijnen](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Raadpleeg altijd de huidige specificatie voor de meest actuele richtlijnen.

## Essentiële Beveiligingspraktijken voor MCP-implementaties

Het Model Context Protocol brengt unieke beveiligingsuitdagingen met zich mee die verder gaan dan traditionele softwarebeveiliging. Deze praktijken behandelen zowel fundamentele beveiligingseisen als MCP-specifieke bedreigingen, waaronder promptinjectie, toolvergiftiging, sessiekaping, confused deputy-problemen en kwetsbaarheden in token-passthrough.

### **VERPLICHTE Beveiligingseisen**

**Kritieke eisen uit de MCP Specificatie:**

> **MAG NIET**: MCP-servers **MAGEN NIET** tokens accepteren die niet expliciet zijn uitgegeven voor de MCP-server  
>  
> **MOET**: MCP-servers die autorisatie implementeren **MOETEN** ALLE inkomende verzoeken verifiëren  
>  
> **MAG NIET**: MCP-servers **MAGEN NIET** sessies gebruiken voor authenticatie  
>  
> **MOET**: MCP-proxyservers die statische client-ID's gebruiken **MOETEN** gebruikers toestemming verkrijgen voor elke dynamisch geregistreerde client  

---

## 1. **Tokenbeveiliging & Authenticatie**

**Authenticatie- en autorisatiecontroles:**
   - **Strikte autorisatiereview**: Voer uitgebreide audits uit van de autorisatielogica van MCP-servers om ervoor te zorgen dat alleen bedoelde gebruikers en clients toegang hebben tot resources  
   - **Integratie met externe identiteitsproviders**: Gebruik gevestigde identiteitsproviders zoals Microsoft Entra ID in plaats van aangepaste authenticatie te implementeren  
   - **Validatie van token-doelgroep**: Valideer altijd dat tokens expliciet zijn uitgegeven voor uw MCP-server - accepteer nooit upstream tokens  
   - **Correct tokenbeheer**: Implementeer veilige tokenrotatie, vervalbeleid en voorkom token-replay-aanvallen  

**Beveiligde tokenopslag:**
   - Gebruik Azure Key Vault of vergelijkbare veilige opslagplaatsen voor alle geheimen  
   - Implementeer encryptie voor tokens zowel in rust als tijdens transport  
   - Regelmatige rotatie van referenties en monitoring op ongeautoriseerde toegang  

## 2. **Sessiebeheer & Transportbeveiliging**

**Veilige sessiepraktijken:**
   - **Cryptografisch veilige sessie-ID's**: Gebruik veilige, niet-deterministische sessie-ID's gegenereerd met veilige willekeurige nummergeneratoren  
   - **Gebruikersspecifieke binding**: Bind sessie-ID's aan gebruikersidentiteiten met formaten zoals `<user_id>:<session_id>` om misbruik van sessies tussen gebruikers te voorkomen  
   - **Beheer van sessielevenscyclus**: Implementeer correct verval, rotatie en ongeldigverklaring om kwetsbaarheidsvensters te beperken  
   - **HTTPS/TLS-verplichting**: Verplicht HTTPS voor alle communicatie om onderschepping van sessie-ID's te voorkomen  

**Transportlaagbeveiliging:**
   - Configureer TLS 1.3 waar mogelijk met correct certificaatbeheer  
   - Implementeer certificaatpinnen voor kritieke verbindingen  
   - Regelmatige certificaatrotatie en verificatie van geldigheid  

## 3. **AI-specifieke bedreigingsbescherming** 🤖

**Verdediging tegen promptinjectie:**
   - **Microsoft Prompt Shields**: Gebruik AI Prompt Shields voor geavanceerde detectie en filtering van kwaadaardige instructies  
   - **Inputvalidatie**: Valideer en zuiver alle invoer om injectieaanvallen en confused deputy-problemen te voorkomen  
   - **Inhoudsgrenzen**: Gebruik scheidings- en datamarkering systemen om onderscheid te maken tussen vertrouwde instructies en externe inhoud  

**Preventie van toolvergiftiging:**
   - **Validatie van toolmetadata**: Implementeer integriteitscontroles voor tooldefinities en monitor op onverwachte wijzigingen  
   - **Dynamische toolmonitoring**: Monitor runtimegedrag en stel waarschuwingen in voor onverwachte uitvoeringspatronen  
   - **Goedkeuringsworkflows**: Vereis expliciete gebruikersgoedkeuring voor toolwijzigingen en capaciteitsaanpassingen  

## 4. **Toegangscontrole & Machtigingen**

**Principe van minimale rechten:**
   - Geef MCP-servers alleen de minimale machtigingen die nodig zijn voor de beoogde functionaliteit  
   - Implementeer rolgebaseerde toegangscontrole (RBAC) met fijnmazige machtigingen  
   - Regelmatige machtigingsreviews en continue monitoring op privilege-escalatie  

**Runtime machtigingscontroles:**
   - Pas resourcebeperkingen toe om aanvallen met resource-uitputting te voorkomen  
   - Gebruik containerisolatie voor tooluitvoeringsomgevingen  
   - Implementeer just-in-time toegang voor administratieve functies  

## 5. **Inhoudsveiligheid & Monitoring**

**Implementatie van inhoudsveiligheid:**
   - **Azure Content Safety-integratie**: Gebruik Azure Content Safety om schadelijke inhoud, jailbreakpogingen en beleidsinbreuken te detecteren  
   - **Gedragsanalyse**: Implementeer runtimegedragsmonitoring om anomalieën in MCP-server en tooluitvoering te detecteren  
   - **Uitgebreide logging**: Log alle authenticatiepogingen, tooloproepen en beveiligingsevenementen met veilige, manipulatiebestendige opslag  

**Continue monitoring:**
   - Real-time waarschuwingen voor verdachte patronen en ongeautoriseerde toegangspogingen  
   - Integratie met SIEM-systemen voor gecentraliseerd beheer van beveiligingsevenementen  
   - Regelmatige beveiligingsaudits en penetratietests van MCP-implementaties  

## 6. **Beveiliging van de toeleveringsketen**

**Componentverificatie:**
   - **Afhankelijkheidsscanning**: Gebruik geautomatiseerde kwetsbaarheidsscanning voor alle softwareafhankelijkheden en AI-componenten  
   - **Herkomstvalidatie**: Verifieer de oorsprong, licenties en integriteit van modellen, gegevensbronnen en externe diensten  
   - **Ondertekende pakketten**: Gebruik cryptografisch ondertekende pakketten en verifieer handtekeningen vóór implementatie  

**Veilige ontwikkelingspipeline:**
   - **GitHub Advanced Security**: Implementeer geheimenscanning, afhankelijkheidsanalyse en CodeQL statische analyse  
   - **CI/CD-beveiliging**: Integreer beveiligingsvalidatie in geautomatiseerde implementatiepijplijnen  
   - **Artefactintegriteit**: Implementeer cryptografische verificatie voor geïmplementeerde artefacten en configuraties  

## 7. **OAuth-beveiliging & Preventie van Confused Deputy**

**OAuth 2.1-implementatie:**
   - **PKCE-implementatie**: Gebruik Proof Key for Code Exchange (PKCE) voor alle autorisatieverzoeken  
   - **Expliciete toestemming**: Verkrijg gebruikers toestemming voor elke dynamisch geregistreerde client om confused deputy-aanvallen te voorkomen  
   - **Validatie van redirect-URI's**: Implementeer strikte validatie van redirect-URI's en client-ID's  

**Proxybeveiliging:**
   - Voorkom autorisatieomzeiling via exploitatie van statische client-ID's  
   - Implementeer correcte toestemmingsworkflows voor toegang tot API's van derden  
   - Monitor op diefstal van autorisatiecodes en ongeautoriseerde API-toegang  

## 8. **Incidentrespons & Herstel**

**Snelle responsmogelijkheden:**
   - **Geautomatiseerde respons**: Implementeer geautomatiseerde systemen voor referentierotatie en bedreigingsbeheersing  
   - **Rollbackprocedures**: Mogelijkheid om snel terug te keren naar bekende goede configuraties en componenten  
   - **Forensische mogelijkheden**: Gedetailleerde audit trails en logging voor incidentonderzoek  

**Communicatie & Coördinatie:**
   - Duidelijke escalatieprocedures voor beveiligingsincidenten  
   - Integratie met organisatorische incidentresponsteams  
   - Regelmatige simulaties van beveiligingsincidenten en tabletop-oefeningen  

## 9. **Naleving & Governance**

**Regelgevingsnaleving:**
   - Zorg ervoor dat MCP-implementaties voldoen aan branchespecifieke vereisten (GDPR, HIPAA, SOC 2)  
   - Implementeer gegevensclassificatie en privacycontroles voor AI-gegevensverwerking  
   - Onderhoud uitgebreide documentatie voor nalevingsaudits  

**Wijzigingsbeheer:**
   - Formele beveiligingsreviewprocessen voor alle MCP-systeemwijzigingen  
   - Versiebeheer en goedkeuringsworkflows voor configuratiewijzigingen  
   - Regelmatige nalevingsbeoordelingen en gap-analyse  

## 10. **Geavanceerde beveiligingscontroles**

**Zero Trust Architectuur:**
   - **Nooit vertrouwen, altijd verifiëren**: Continue verificatie van gebruikers, apparaten en verbindingen  
   - **Micro-segmentatie**: Granulaire netwerkcontroles die individuele MCP-componenten isoleren  
   - **Voorwaardelijke toegang**: Risicogebaseerde toegangscontroles die zich aanpassen aan de huidige context en gedrag  

**Runtime applicatiebescherming:**
   - **Runtime Application Self-Protection (RASP)**: Gebruik RASP-technieken voor realtime bedreigingsdetectie  
   - **Applicatieprestatiemonitoring**: Monitor op prestatie-anomalieën die aanvallen kunnen aangeven  
   - **Dynamische beveiligingsbeleid**: Implementeer beveiligingsbeleid dat zich aanpast aan de huidige dreigingsomgeving  

## 11. **Integratie met Microsoft Beveiligingsecosysteem**

**Uitgebreide Microsoft-beveiliging:**
   - **Microsoft Defender for Cloud**: Beheer van cloudbeveiligingshouding voor MCP-werklasten  
   - **Azure Sentinel**: Cloud-native SIEM en SOAR-mogelijkheden voor geavanceerde bedreigingsdetectie  
   - **Microsoft Purview**: Gegevensbeheer en naleving voor AI-workflows en gegevensbronnen  

**Identiteits- en toegangsbeheer:**
   - **Microsoft Entra ID**: Enterprise identiteitsbeheer met voorwaardelijke toegangsbeleid  
   - **Privileged Identity Management (PIM)**: Just-in-time toegang en goedkeuringsworkflows voor administratieve functies  
   - **Identity Protection**: Risicogebaseerde voorwaardelijke toegang en geautomatiseerde bedreigingsrespons  

## 12. **Continue beveiligingsevolutie**

**Bijblijven:**
   - **Specificatiemonitoring**: Regelmatige review van MCP-specificatie-updates en wijzigingen in beveiligingsrichtlijnen  
   - **Threat Intelligence**: Integratie van AI-specifieke dreigingsfeeds en indicatoren van compromittering  
   - **Beveiligingsgemeenschap**: Actieve deelname aan MCP-beveiligingsgemeenschap en programma's voor kwetsbaarheidsmelding  

**Adaptieve beveiliging:**
   - **Machine Learning-beveiliging**: Gebruik ML-gebaseerde anomaliedetectie om nieuwe aanvalspatronen te identificeren  
   - **Voorspellende beveiligingsanalyse**: Implementeer voorspellende modellen voor proactieve dreigingsidentificatie  
   - **Beveiligingsautomatisering**: Geautomatiseerde updates van beveiligingsbeleid op basis van dreigingsinformatie en specificatiewijzigingen  

---

## **Kritieke beveiligingsbronnen**

### **Officiële MCP-documentatie**
- [MCP Specificatie (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Beveiligingsrichtlijnen](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Autorisatiespecificatie](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Beveiligingsoplossingen**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Beveiliging](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Beveiligingsstandaarden**
- [OAuth 2.0 Beveiligingsrichtlijnen (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 voor Grote Taalmodellen](https://genai.owasp.org/)  
- [NIST AI Risicobeheer Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Implementatiegidsen**
- [Azure API Management MCP Authenticatie Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID met MCP-servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Beveiligingsmelding**: MCP-beveiligingspraktijken evolueren snel. Verifieer altijd aan de hand van de huidige [MCP-specificatie](https://spec.modelcontextprotocol.io/) en [officiële beveiligingsdocumentatie](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) vóór implementatie.

**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we ons best doen voor nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.