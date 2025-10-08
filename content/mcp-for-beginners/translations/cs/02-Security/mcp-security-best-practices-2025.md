<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-19T15:34:52+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "cs"
}
-->
# MCP Bezpečnostní nejlepší praktiky - Aktualizace srpen 2025

> **Důležité**: Tento dokument odráží nejnovější [MCP Specifikaci 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) bezpečnostní požadavky a oficiální [MCP Bezpečnostní nejlepší praktiky](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Vždy se odkazujte na aktuální specifikaci pro nejnovější doporučení.

## Základní bezpečnostní praktiky pro implementace MCP

Model Context Protocol přináší jedinečné bezpečnostní výzvy, které přesahují tradiční softwarovou bezpečnost. Tyto praktiky se zaměřují na základní bezpečnostní požadavky i na specifické hrozby MCP, včetně injekce promptů, otravy nástrojů, únosu relací, problémů zmateného zástupce a zranitelností při předávání tokenů.

### **POVINNÉ bezpečnostní požadavky**

**Kritické požadavky ze specifikace MCP:**

> **NESMÍ**: MCP servery **NESMÍ** přijímat žádné tokeny, které nebyly výslovně vydány pro MCP server  
> 
> **MUSÍ**: MCP servery implementující autorizaci **MUSÍ** ověřovat VŠECHNY příchozí požadavky  
>  
> **NESMÍ**: MCP servery **NESMÍ** používat relace pro autentizaci  
>
> **MUSÍ**: MCP proxy servery používající statické ID klientů **MUSÍ** získat souhlas uživatele pro každého dynamicky registrovaného klienta  

---

## 1. **Bezpečnost tokenů a autentizace**

**Kontroly autentizace a autorizace:**
   - **Důkladná revize autorizace**: Provádějte komplexní audity logiky autorizace MCP serveru, aby bylo zajištěno, že přístup k prostředkům mají pouze zamýšlení uživatelé a klienti  
   - **Integrace externího poskytovatele identity**: Používejte zavedené poskytovatele identity, jako je Microsoft Entra ID, místo implementace vlastní autentizace  
   - **Validace publika tokenů**: Vždy ověřujte, že tokeny byly výslovně vydány pro váš MCP server - nikdy nepřijímejte tokeny z jiných zdrojů  
   - **Správný životní cyklus tokenů**: Implementujte bezpečnou rotaci tokenů, politiky expirace a zabraňte útokům na opětovné použití tokenů  

**Chráněné úložiště tokenů:**
   - Používejte Azure Key Vault nebo podobné bezpečné úložiště pro všechny tajné klíče  
   - Implementujte šifrování tokenů jak při ukládání, tak při přenosu  
   - Pravidelná rotace přihlašovacích údajů a monitorování neoprávněného přístupu  

## 2. **Správa relací a bezpečnost přenosu**

**Bezpečné praktiky pro relace:**
   - **Kryptograficky bezpečné ID relací**: Používejte bezpečné, nedeterministické ID relací generované pomocí bezpečných generátorů náhodných čísel  
   - **Vazba na uživatele**: Vážte ID relací na identitu uživatele pomocí formátů jako `<user_id>:<session_id>` k prevenci zneužití relací mezi uživateli  
   - **Správa životního cyklu relací**: Implementujte správnou expiraci, rotaci a zneplatnění relací k omezení zranitelnosti  
   - **Vynucení HTTPS/TLS**: Povinné HTTPS pro veškerou komunikaci k prevenci zachycení ID relací  

**Bezpečnost transportní vrstvy:**
   - Konfigurujte TLS 1.3, kde je to možné, s řádnou správou certifikátů  
   - Implementujte připnutí certifikátů pro kritické spojení  
   - Pravidelná rotace certifikátů a ověřování jejich platnosti  

## 3. **Ochrana proti AI-specifickým hrozbám** 🤖

**Obrana proti injekci promptů:**
   - **Microsoft Prompt Shields**: Nasazení AI Prompt Shields pro pokročilou detekci a filtrování škodlivých instrukcí  
   - **Sanitace vstupů**: Validujte a čistěte všechny vstupy k prevenci útoků injekcí a problémů zmateného zástupce  
   - **Obsahové hranice**: Používejte systémy oddělovačů a označování dat k rozlišení mezi důvěryhodnými instrukcemi a externím obsahem  

**Prevence otravy nástrojů:**
   - **Validace metadat nástrojů**: Implementujte kontroly integrity definic nástrojů a monitorujte neočekávané změny  
   - **Dynamické monitorování nástrojů**: Monitorujte chování za běhu a nastavte upozornění na neočekávané vzory provádění  
   - **Schvalovací procesy**: Vyžadujte explicitní schválení uživatelem pro úpravy nástrojů a změny schopností  

## 4. **Kontrola přístupu a oprávnění**

**Princip minimálních oprávnění:**
   - Udělujte MCP serverům pouze minimální oprávnění potřebná pro zamýšlenou funkčnost  
   - Implementujte kontrolu přístupu založenou na rolích (RBAC) s jemně granulovanými oprávněními  
   - Pravidelné revize oprávnění a nepřetržité monitorování eskalace oprávnění  

**Kontroly oprávnění za běhu:**
   - Aplikujte limity zdrojů k prevenci útoků na vyčerpání zdrojů  
   - Používejte izolaci kontejnerů pro prostředí provádění nástrojů  
   - Implementujte přístup "just-in-time" pro administrativní funkce  

## 5. **Bezpečnost obsahu a monitorování**

**Implementace bezpečnosti obsahu:**
   - **Integrace Azure Content Safety**: Používejte Azure Content Safety k detekci škodlivého obsahu, pokusů o obejití pravidel a porušení politik  
   - **Analýza chování**: Implementujte monitorování chování za běhu k detekci anomálií v MCP serveru a provádění nástrojů  
   - **Komplexní logování**: Logujte všechny pokusy o autentizaci, vyvolání nástrojů a bezpečnostní události s bezpečným, nezměnitelným úložištěm  

**Nepřetržité monitorování:**
   - Upozornění v reálném čase na podezřelé vzory a neoprávněné pokusy o přístup  
   - Integrace se systémy SIEM pro centralizovanou správu bezpečnostních událostí  
   - Pravidelné bezpečnostní audity a penetrační testování implementací MCP  

## 6. **Bezpečnost dodavatelského řetězce**

**Ověření komponent:**
   - **Skenování závislostí**: Používejte automatizované skenování zranitelností pro všechny softwarové závislosti a AI komponenty  
   - **Validace původu**: Ověřujte původ, licencování a integritu modelů, datových zdrojů a externích služeb  
   - **Podepsané balíčky**: Používejte kryptograficky podepsané balíčky a ověřujte podpisy před nasazením  

**Bezpečný vývojový pipeline:**
   - **GitHub Advanced Security**: Implementujte skenování tajných klíčů, analýzu závislostí a statickou analýzu CodeQL  
   - **Bezpečnost CI/CD**: Integrujte bezpečnostní validaci do automatizovaných pipeline nasazení  
   - **Integrita artefaktů**: Implementujte kryptografické ověřování nasazených artefaktů a konfigurací  

## 7. **Bezpečnost OAuth a prevence zmateného zástupce**

**Implementace OAuth 2.1:**
   - **Implementace PKCE**: Používejte Proof Key for Code Exchange (PKCE) pro všechny autorizační požadavky  
   - **Explicitní souhlas**: Získejte souhlas uživatele pro každého dynamicky registrovaného klienta k prevenci útoků zmateného zástupce  
   - **Validace URI přesměrování**: Implementujte přísnou validaci URI přesměrování a identifikátorů klientů  

**Bezpečnost proxy:**
   - Zabraňte obcházení autorizace prostřednictvím zneužití statických ID klientů  
   - Implementujte správné workflow souhlasu pro přístup k API třetích stran  
   - Monitorujte krádež autorizačních kódů a neoprávněný přístup k API  

## 8. **Reakce na incidenty a obnova**

**Schopnosti rychlé reakce:**
   - **Automatizovaná reakce**: Implementujte automatizované systémy pro rotaci přihlašovacích údajů a omezení hrozeb  
   - **Postupy pro návrat zpět**: Schopnost rychle se vrátit k známým dobrým konfiguracím a komponentám  
   - **Forenzní schopnosti**: Detailní auditní stopy a logování pro vyšetřování incidentů  

**Komunikace a koordinace:**
   - Jasné postupy eskalace pro bezpečnostní incidenty  
   - Integrace s organizačními týmy pro reakci na incidenty  
   - Pravidelné simulace bezpečnostních incidentů a cvičení na stole  

## 9. **Soulad a správa**

**Regulační soulad:**
   - Zajistěte, že implementace MCP splňují požadavky specifické pro dané odvětví (GDPR, HIPAA, SOC 2)  
   - Implementujte klasifikaci dat a kontrolu soukromí pro zpracování AI dat  
   - Udržujte komplexní dokumentaci pro audity souladu  

**Správa změn:**
   - Formální procesy bezpečnostní revize pro všechny změny systému MCP  
   - Řízení verzí a workflow schvalování pro změny konfigurace  
   - Pravidelné hodnocení souladu a analýza mezer  

## 10. **Pokročilé bezpečnostní kontroly**

**Architektura Zero Trust:**
   - **Nikdy nedůvěřujte, vždy ověřujte**: Nepřetržité ověřování uživatelů, zařízení a spojení  
   - **Mikrosegmentace**: Granulární síťové kontroly izolující jednotlivé komponenty MCP  
   - **Podmíněný přístup**: Kontroly přístupu založené na riziku, přizpůsobující se aktuálnímu kontextu a chování  

**Ochrana aplikací za běhu:**
   - **Runtime Application Self-Protection (RASP)**: Nasazení technik RASP pro detekci hrozeb v reálném čase  
   - **Monitorování výkonu aplikací**: Monitorování výkonových anomálií, které mohou indikovat útoky  
   - **Dynamické bezpečnostní politiky**: Implementace bezpečnostních politik, které se přizpůsobují aktuálnímu prostředí hrozeb  

## 11. **Integrace s bezpečnostním ekosystémem Microsoftu**

**Komplexní bezpečnost Microsoftu:**
   - **Microsoft Defender for Cloud**: Správa bezpečnostního stavu cloudu pro pracovní zátěže MCP  
   - **Azure Sentinel**: Nativní cloudové SIEM a SOAR schopnosti pro pokročilou detekci hrozeb  
   - **Microsoft Purview**: Správa dat a soulad pro AI workflowy a datové zdroje  

**Správa identity a přístupu:**
   - **Microsoft Entra ID**: Podniková správa identity s politikami podmíněného přístupu  
   - **Privileged Identity Management (PIM)**: Přístup "just-in-time" a workflow schvalování pro administrativní funkce  
   - **Ochrana identity**: Podmíněný přístup založený na riziku a automatizovaná reakce na hrozby  

## 12. **Nepřetržitý vývoj bezpečnosti**

**Udržování aktuálnosti:**
   - **Monitorování specifikace**: Pravidelná revize aktualizací specifikace MCP a změn bezpečnostního doporučení  
   - **Inteligence hrozeb**: Integrace AI-specifických zdrojů hrozeb a indikátorů kompromitace  
   - **Zapojení do bezpečnostní komunity**: Aktivní účast v bezpečnostní komunitě MCP a programech pro zveřejňování zranitelností  

**Adaptivní bezpečnost:**
   - **Bezpečnost strojového učení**: Používání detekce anomálií založené na ML k identifikaci nových vzorů útoků  
   - **Prediktivní bezpečnostní analýzy**: Implementace prediktivních modelů pro proaktivní identifikaci hrozeb  
   - **Automatizace bezpečnosti**: Automatizované aktualizace bezpečnostních politik na základě inteligence hrozeb a změn specifikace  

---

## **Klíčové bezpečnostní zdroje**

### **Oficiální dokumentace MCP**
- [MCP Specifikace (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Bezpečnostní nejlepší praktiky](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Specifikace autorizace](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Bezpečnostní řešení Microsoftu**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Bezpečnost](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Bezpečnostní standardy**
- [OAuth 2.0 Bezpečnostní nejlepší praktiky (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 pro velké jazykové modely](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Implementační příručky**
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID s MCP servery](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Bezpečnostní upozornění**: Bezpečnostní praktiky MCP se rychle vyvíjejí. Vždy ověřujte podle aktuální [specifikace MCP](https://spec.modelcontextprotocol.io/) a [oficiální bezpečnostní dokumentace](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) před implementací.

**Prohlášení:**  
Tento dokument byl přeložen pomocí služby pro automatický překlad [Co-op Translator](https://github.com/Azure/co-op-translator). I když se snažíme o přesnost, mějte prosím na paměti, že automatické překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho původním jazyce by měl být považován za závazný zdroj. Pro důležité informace doporučujeme profesionální lidský překlad. Neodpovídáme za žádná nedorozumění nebo nesprávné interpretace vyplývající z použití tohoto překladu.