<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-19T16:02:01+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "sk"
}
-->
# MCP Bezpečnostné osvedčené postupy - Aktualizácia august 2025

> **Dôležité**: Tento dokument odráža najnovšie [MCP Špecifikácie 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) bezpečnostné požiadavky a oficiálne [MCP Bezpečnostné osvedčené postupy](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Vždy sa odvolávajte na aktuálnu špecifikáciu pre najnovšie odporúčania.

## Základné bezpečnostné postupy pre implementácie MCP

Model Context Protocol prináša jedinečné bezpečnostné výzvy, ktoré presahujú tradičné softvérové zabezpečenie. Tieto postupy sa zaoberajú základnými bezpečnostnými požiadavkami a hrozbami špecifickými pre MCP, vrátane injekcie promptov, otravy nástrojov, únosu relácií, problémov zmätku zástupcu a zraniteľností pri prechode tokenov.

### **POVINNÉ bezpečnostné požiadavky**

**Kritické požiadavky zo špecifikácie MCP:**

> **NESMIE**: MCP servery **NESMÚ** akceptovať žiadne tokeny, ktoré neboli výslovne vydané pre MCP server  
> 
> **MUSÍ**: MCP servery implementujúce autorizáciu **MUSIA** overiť VŠETKY prichádzajúce požiadavky  
>  
> **NESMIE**: MCP servery **NESMÚ** používať relácie na autentifikáciu  
>
> **MUSÍ**: MCP proxy servery používajúce statické ID klientov **MUSIA** získať súhlas používateľa pre každého dynamicky registrovaného klienta  

---

## 1. **Bezpečnosť tokenov a autentifikácia**

**Kontroly autentifikácie a autorizácie:**
   - **Dôkladná kontrola autorizácie**: Vykonajte komplexné audity logiky autorizácie MCP servera, aby ste zabezpečili, že prístup k zdrojom majú iba zamýšľaní používatelia a klienti  
   - **Integrácia externého poskytovateľa identity**: Používajte zavedených poskytovateľov identity, ako je Microsoft Entra ID, namiesto implementácie vlastnej autentifikácie  
   - **Validácia publika tokenov**: Vždy overte, že tokeny boli výslovne vydané pre váš MCP server - nikdy neakceptujte tokeny z iných zdrojov  
   - **Správny životný cyklus tokenov**: Implementujte bezpečnú rotáciu tokenov, politiky vypršania platnosti a zabráňte útokom na opätovné použitie tokenov  

**Chránené úložisko tokenov:**
   - Používajte Azure Key Vault alebo podobné bezpečné úložiská pre všetky tajomstvá  
   - Implementujte šifrovanie tokenov v pokoji aj počas prenosu  
   - Pravidelná rotácia poverení a monitorovanie neoprávneného prístupu  

## 2. **Správa relácií a bezpečnosť prenosu**

**Bezpečné praktiky relácií:**
   - **Kryptograficky bezpečné ID relácií**: Používajte bezpečné, nedeterministické ID relácií generované pomocou bezpečných generátorov náhodných čísel  
   - **Väzba na používateľa**: Viažte ID relácií na identity používateľov pomocou formátov ako `<user_id>:<session_id>` na zabránenie zneužitia relácií medzi používateľmi  
   - **Správa životného cyklu relácií**: Implementujte správne vypršanie platnosti, rotáciu a zneplatnenie na obmedzenie zraniteľných okien  
   - **Povinné HTTPS/TLS**: Povinné HTTPS pre všetku komunikáciu na zabránenie zachytenia ID relácií  

**Bezpečnosť transportnej vrstvy:**
   - Konfigurujte TLS 1.3, kde je to možné, s riadnou správou certifikátov  
   - Implementujte pripínanie certifikátov pre kritické spojenia  
   - Pravidelná rotácia certifikátov a overovanie platnosti  

## 3. **Ochrana pred hrozbami špecifickými pre AI** 🤖

**Obrana proti injekcii promptov:**
   - **Microsoft Prompt Shields**: Nasadzujte AI Prompt Shields na pokročilú detekciu a filtrovanie škodlivých inštrukcií  
   - **Sanitácia vstupov**: Validujte a čistite všetky vstupy na zabránenie útokom injekcie a problémom zmätku zástupcu  
   - **Obsahové hranice**: Používajte systémy oddelovačov a označovania dát na rozlíšenie medzi dôveryhodnými inštrukciami a externým obsahom  

**Prevencia otravy nástrojov:**
   - **Validácia metadát nástrojov**: Implementujte kontroly integrity definícií nástrojov a monitorujte neočakávané zmeny  
   - **Dynamické monitorovanie nástrojov**: Monitorujte správanie počas behu a nastavte upozornenia na neočakávané vzory vykonávania  
   - **Schvaľovacie procesy**: Vyžadujte výslovné schválenie používateľom pre úpravy nástrojov a zmeny schopností  

## 4. **Kontrola prístupu a oprávnení**

**Princíp minimálnych oprávnení:**
   - Poskytujte MCP serverom iba minimálne oprávnenia potrebné na zamýšľanú funkčnosť  
   - Implementujte kontrolu prístupu na základe rolí (RBAC) s jemne zrnitými oprávneniami  
   - Pravidelné kontroly oprávnení a nepretržité monitorovanie eskalácie oprávnení  

**Kontroly oprávnení počas behu:**
   - Aplikujte limity zdrojov na zabránenie útokom na vyčerpanie zdrojov  
   - Používajte izoláciu kontajnerov pre prostredia vykonávania nástrojov  
   - Implementujte prístup „just-in-time“ pre administratívne funkcie  

## 5. **Bezpečnosť obsahu a monitorovanie**

**Implementácia bezpečnosti obsahu:**
   - **Integrácia Azure Content Safety**: Používajte Azure Content Safety na detekciu škodlivého obsahu, pokusov o jailbreak a porušení politiky  
   - **Behaviorálna analýza**: Implementujte monitorovanie správania počas behu na detekciu anomálií v MCP serveri a vykonávaní nástrojov  
   - **Komplexné logovanie**: Logujte všetky pokusy o autentifikáciu, vyvolania nástrojov a bezpečnostné udalosti s bezpečným, nezmeniteľným úložiskom  

**Nepretržité monitorovanie:**
   - Upozornenia v reálnom čase na podozrivé vzory a pokusy o neoprávnený prístup  
   - Integrácia so systémami SIEM na centralizované riadenie bezpečnostných udalostí  
   - Pravidelné bezpečnostné audity a penetračné testovanie implementácií MCP  

## 6. **Bezpečnosť dodávateľského reťazca**

**Overenie komponentov:**
   - **Skenovanie závislostí**: Používajte automatizované skenovanie zraniteľností pre všetky softvérové závislosti a AI komponenty  
   - **Validácia pôvodu**: Overte pôvod, licencovanie a integritu modelov, zdrojov dát a externých služieb  
   - **Podpísané balíčky**: Používajte kryptograficky podpísané balíčky a overujte podpisy pred nasadením  

**Bezpečný vývojový pipeline:**
   - **GitHub Advanced Security**: Implementujte skenovanie tajomstiev, analýzu závislostí a statickú analýzu CodeQL  
   - **Bezpečnosť CI/CD**: Integrujte bezpečnostné overenie v celom automatizovanom pipeline nasadenia  
   - **Integrita artefaktov**: Implementujte kryptografické overenie nasadených artefaktov a konfigurácií  

## 7. **Bezpečnosť OAuth a prevencia zmätku zástupcu**

**Implementácia OAuth 2.1:**
   - **Implementácia PKCE**: Používajte Proof Key for Code Exchange (PKCE) pre všetky požiadavky na autorizáciu  
   - **Výslovný súhlas**: Získajte súhlas používateľa pre každého dynamicky registrovaného klienta na zabránenie útokom zmätku zástupcu  
   - **Validácia URI presmerovania**: Implementujte prísnu validáciu URI presmerovania a identifikátorov klientov  

**Bezpečnosť proxy:**
   - Zabráňte obchádzaniu autorizácie prostredníctvom zneužitia statického ID klienta  
   - Implementujte správne pracovné postupy súhlasu pre prístup k API tretích strán  
   - Monitorujte krádež autorizačných kódov a neoprávnený prístup k API  

## 8. **Reakcia na incidenty a obnova**

**Schopnosti rýchlej reakcie:**
   - **Automatizovaná reakcia**: Implementujte automatizované systémy na rotáciu poverení a obmedzenie hrozieb  
   - **Postupy návratu**: Schopnosť rýchlo sa vrátiť k známym dobrým konfiguráciám a komponentom  
   - **Forenzné schopnosti**: Podrobné auditné stopy a logovanie na vyšetrovanie incidentov  

**Komunikácia a koordinácia:**
   - Jasné postupy eskalácie pre bezpečnostné incidenty  
   - Integrácia s tímami organizácie na reakciu na incidenty  
   - Pravidelné simulácie bezpečnostných incidentov a cvičenia na stole  

## 9. **Súlad a správa**

**Regulačný súlad:**
   - Zabezpečte, aby implementácie MCP spĺňali požiadavky špecifické pre odvetvie (GDPR, HIPAA, SOC 2)  
   - Implementujte klasifikáciu dát a kontrolu súkromia pre spracovanie dát AI  
   - Udržiavajte komplexnú dokumentáciu pre audity súladu  

**Správa zmien:**
   - Formálne procesy bezpečnostného preskúmania pre všetky modifikácie systému MCP  
   - Kontrola verzií a pracovné postupy schvaľovania pre zmeny konfigurácie  
   - Pravidelné hodnotenia súladu a analýza medzier  

## 10. **Pokročilé bezpečnostné kontroly**

**Architektúra nulovej dôvery:**
   - **Nikdy nedôveruj, vždy overuj**: Neustále overovanie používateľov, zariadení a spojení  
   - **Mikrosegmentácia**: Granulárne sieťové kontroly izolujúce jednotlivé komponenty MCP  
   - **Podmienený prístup**: Kontroly prístupu založené na riziku prispôsobené aktuálnemu kontextu a správaniu  

**Ochrana aplikácií počas behu:**
   - **Runtime Application Self-Protection (RASP)**: Nasadzujte techniky RASP na detekciu hrozieb v reálnom čase  
   - **Monitorovanie výkonu aplikácií**: Monitorujte výkonové anomálie, ktoré môžu naznačovať útoky  
   - **Dynamické bezpečnostné politiky**: Implementujte bezpečnostné politiky, ktoré sa prispôsobujú aktuálnej hrozbe  

## 11. **Integrácia bezpečnostného ekosystému Microsoft**

**Komplexná bezpečnosť Microsoft:**
   - **Microsoft Defender for Cloud**: Správa bezpečnostného stavu cloudu pre pracovné zaťaženia MCP  
   - **Azure Sentinel**: Cloud-native SIEM a SOAR schopnosti na pokročilú detekciu hrozieb  
   - **Microsoft Purview**: Správa dát a súlad pre pracovné postupy AI a zdroje dát  

**Správa identity a prístupu:**
   - **Microsoft Entra ID**: Správa podnikových identít s politikami podmieneného prístupu  
   - **Privileged Identity Management (PIM)**: Prístup „just-in-time“ a pracovné postupy schvaľovania pre administratívne funkcie  
   - **Ochrana identity**: Podmienený prístup založený na riziku a automatizovaná reakcia na hrozby  

## 12. **Nepretržitý vývoj bezpečnosti**

**Udržiavanie aktuálnosti:**
   - **Monitorovanie špecifikácií**: Pravidelné preskúmanie aktualizácií špecifikácií MCP a zmien bezpečnostných odporúčaní  
   - **Inteligencia hrozieb**: Integrácia AI špecifických informačných kanálov o hrozbách a indikátorov kompromitácie  
   - **Zapojenie bezpečnostnej komunity**: Aktívna účasť v bezpečnostnej komunite MCP a programoch na zverejňovanie zraniteľností  

**Adaptívna bezpečnosť:**
   - **Bezpečnosť strojového učenia**: Používajte detekciu anomálií založenú na ML na identifikáciu nových vzorov útokov  
   - **Prediktívna bezpečnostná analytika**: Implementujte prediktívne modely na proaktívnu identifikáciu hrozieb  
   - **Automatizácia bezpečnosti**: Automatizované aktualizácie bezpečnostných politík na základe inteligencie hrozieb a zmien špecifikácií  

---

## **Kritické bezpečnostné zdroje**

### **Oficiálna dokumentácia MCP**
- [MCP Špecifikácia (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Bezpečnostné osvedčené postupy](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Špecifikácia autorizácie](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Bezpečnostné riešenia**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Bezpečnosť](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Bezpečnostné štandardy**
- [OAuth 2.0 Bezpečnostné osvedčené postupy (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 pre veľké jazykové modely](https://genai.owasp.org/)  
- [NIST AI Rámec riadenia rizík](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Implementačné príručky**
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID s MCP servermi](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Bezpečnostné upozornenie**: Bezpečnostné postupy MCP sa rýchlo vyvíjajú. Vždy overte aktuálnu [MCP špecifikáciu](https://spec.modelcontextprotocol.io/) a [oficiálnu bezpečnostnú dokumentáciu](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) pred implementáciou.

**Upozornenie**:  
Tento dokument bol preložený pomocou služby AI prekladu [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, prosím, berte na vedomie, že automatizované preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho rodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za akékoľvek nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.