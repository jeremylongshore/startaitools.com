<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:51:45+00:00",
  "source_file": "changelog.md",
  "language_code": "cs"
}
-->
# Změny: Kurikulum MCP pro začátečníky

Tento dokument slouží jako záznam všech významných změn provedených v kurikulu Model Context Protocol (MCP) pro začátečníky. Změny jsou dokumentovány v obráceném chronologickém pořadí (nejnovější změny jako první).

## 6. října 2025

### Rozšíření sekce Začínáme – Pokročilé použití serveru a jednoduché ověřování

#### Pokročilé použití serveru (03-GettingStarted/10-advanced)
- **Přidána nová kapitola**: Zavedena komplexní příručka pro pokročilé použití MCP serveru, zahrnující běžné i nízkoúrovňové serverové architektury.
  - **Běžný vs. nízkoúrovňový server**: Podrobná srovnání a ukázky kódu v Pythonu a TypeScriptu pro oba přístupy.
  - **Design založený na handlerech**: Vysvětlení správy nástrojů/zdrojů/promptů založené na handlerech pro škálovatelné a flexibilní implementace serverů.
  - **Praktické vzory**: Scénáře z reálného světa, kde nízkoúrovňové serverové vzory přinášejí výhody pro pokročilé funkce a architekturu.

#### Jednoduché ověřování (03-GettingStarted/11-simple-auth)
- **Přidána nová kapitola**: Krok za krokem průvodce implementací jednoduchého ověřování na MCP serverech.
  - **Koncepty ověřování**: Jasné vysvětlení rozdílu mezi ověřováním a autorizací a správa přihlašovacích údajů.
  - **Implementace základního ověřování**: Vzory ověřování založené na middleware v Pythonu (Starlette) a TypeScriptu (Express) s ukázkami kódu.
  - **Přechod na pokročilé zabezpečení**: Doporučení, jak začít s jednoduchým ověřováním a postupně přejít na OAuth 2.1 a RBAC, s odkazy na pokročilé bezpečnostní moduly.

Tato rozšíření poskytují praktické, prakticky orientované pokyny pro vytváření robustnějších, bezpečnějších a flexibilnějších implementací MCP serverů, propojující základní koncepty s pokročilými produkčními vzory.

## 29. září 2025

### Laboratoře integrace databáze MCP serveru – Komplexní praktická učební cesta

#### 11-MCPServerHandsOnLabs - Nové kompletní kurikulum integrace databáze
- **Kompletní učební cesta s 13 laboratořemi**: Přidáno komplexní praktické kurikulum pro vytváření produkčně připravených MCP serverů s integrací databáze PostgreSQL.
  - **Implementace z reálného světa**: Případová studie Zava Retail Analytics demonstrující vzory na podnikové úrovni.
  - **Strukturovaný učební postup**:
    - **Laboratoře 00-03: Základy** - Úvod, základní architektura, zabezpečení a multitenance, nastavení prostředí.
    - **Laboratoře 04-06: Vytváření MCP serveru** - Návrh databáze a schéma, implementace MCP serveru, vývoj nástrojů.
    - **Laboratoře 07-09: Pokročilé funkce** - Integrace sémantického vyhledávání, testování a ladění, integrace VS Code.
    - **Laboratoře 10-12: Produkce a osvědčené postupy** - Strategie nasazení, monitorování a pozorovatelnost, optimalizace a osvědčené postupy.
  - **Podnikové technologie**: Framework FastMCP, PostgreSQL s pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Pokročilé funkce**: Řízení přístupu na úrovni řádků (RLS), sémantické vyhledávání, multitenantní přístup k datům, vektorové embeddings, monitorování v reálném čase.

#### Standardizace terminologie – Přechod z modulů na laboratoře
- **Komplexní aktualizace dokumentace**: Systematicky aktualizovány všechny README soubory v 11-MCPServerHandsOnLabs na terminologii "Laboratoř" místo "Modul".
  - **Záhlaví sekcí**: Aktualizováno "Co tento modul pokrývá" na "Co tato laboratoř pokrývá" ve všech 13 laboratořích.
  - **Popis obsahu**: Změněno "Tento modul poskytuje..." na "Tato laboratoř poskytuje..." v celé dokumentaci.
  - **Výukové cíle**: Aktualizováno "Na konci tohoto modulu..." na "Na konci této laboratoře...".
  - **Navigační odkazy**: Převod všech odkazů "Modul XX:" na "Laboratoř XX:" v křížových odkazech a navigaci.
  - **Sledování dokončení**: Aktualizováno "Po dokončení tohoto modulu..." na "Po dokončení této laboratoře...".
  - **Zachování technických odkazů**: Zachovány odkazy na Python moduly v konfiguračních souborech (např. `"module": "mcp_server.main"`).

#### Vylepšení studijního průvodce (study_guide.md)
- **Vizualizace kurikula**: Přidána nová sekce "11. Laboratoře integrace databáze" s vizualizací struktury laboratoří.
- **Struktura repozitáře**: Aktualizováno z deseti na jedenáct hlavních sekcí s podrobným popisem 11-MCPServerHandsOnLabs.
- **Pokyny k učební cestě**: Rozšířeny navigační pokyny na pokrytí sekcí 00-11.
- **Pokrytí technologií**: Přidány podrobnosti o integraci FastMCP, PostgreSQL a služeb Azure.
- **Výukové výsledky**: Zdůrazněn vývoj produkčně připravených serverů, vzory integrace databáze a podnikové zabezpečení.

#### Vylepšení struktury hlavního README
- **Terminologie založená na laboratořích**: Aktualizováno hlavní README.md v 11-MCPServerHandsOnLabs pro konzistentní použití struktury "Laboratoř".
- **Organizace učební cesty**: Jasný postup od základních konceptů přes pokročilou implementaci až po nasazení do produkce.
- **Zaměření na reálný svět**: Důraz na praktické, prakticky orientované učení s vzory a technologiemi na podnikové úrovni.

### Vylepšení kvality a konzistence dokumentace
- **Důraz na praktické učení**: Posílen praktický přístup založený na laboratořích v celé dokumentaci.
- **Zaměření na podnikové vzory**: Zdůrazněny produkčně připravené implementace a úvahy o podnikové bezpečnosti.
- **Integrace technologií**: Komplexní pokrytí moderních služeb Azure a vzorů integrace AI.
- **Postup učení**: Jasná, strukturovaná cesta od základních konceptů k nasazení do produkce.

## 26. září 2025

### Vylepšení případových studií – Integrace GitHub MCP Registry

#### Případové studie (09-CaseStudy/) – Zaměření na rozvoj ekosystému
- **README.md**: Rozšíření s komplexní případovou studií GitHub MCP Registry.
  - **Případová studie GitHub MCP Registry**: Nová komplexní případová studie zkoumající spuštění GitHub MCP Registry v září 2025.
    - **Analýza problému**: Podrobný rozbor roztříštěného vyhledávání a nasazování MCP serverů.
    - **Architektura řešení**: Centralizovaný přístup registru GitHub s instalací jedním kliknutím ve VS Code.
    - **Dopad na podnikání**: Měřitelné zlepšení onboardingu vývojářů a produktivity.
    - **Strategická hodnota**: Důraz na modulární nasazení agentů a interoperabilitu mezi nástroji.
    - **Rozvoj ekosystému**: Pozice jako základní platforma pro integraci agentů.
  - **Vylepšená struktura případových studií**: Aktualizovány všechny sedm případových studií s konzistentním formátováním a podrobnými popisy.
    - Azure AI Travel Agents: Důraz na orchestraci více agentů.
    - Integrace Azure DevOps: Zaměření na automatizaci pracovních postupů.
    - Real-Time Documentation Retrieval: Implementace klienta Python konzole.
    - Interaktivní generátor studijních plánů: Konverzační webová aplikace Chainlit.
    - Dokumentace v editoru: Integrace VS Code a GitHub Copilot.
    - Správa API Azure: Vzory integrace podnikových API.
    - GitHub MCP Registry: Rozvoj ekosystému a komunitní platforma.
  - **Komplexní závěr**: Přepsána závěrečná sekce zdůrazňující sedm případových studií pokrývajících různé dimenze implementace MCP.
    - Kategorizace: Podniková integrace, orchestrace více agentů, produktivita vývojářů.
    - Rozvoj ekosystému, vzdělávací aplikace.
    - Rozšířené poznatky o architektonických vzorech, implementačních strategiích a osvědčených postupech.
    - Důraz na MCP jako vyspělý, produkčně připravený protokol.

#### Aktualizace studijního průvodce (study_guide.md)
- **Vizualizace kurikula**: Aktualizována myšlenková mapa, aby zahrnovala GitHub MCP Registry v sekci případových studií.
- **Popis případových studií**: Rozšířeno z obecných popisů na podrobný rozbor sedmi komplexních případových studií.
- **Struktura repozitáře**: Aktualizována sekce 10, aby odrážela komplexní pokrytí případových studií s konkrétními detaily implementace.
- **Integrace změn**: Přidán záznam z 26. září 2025 dokumentující přidání GitHub MCP Registry a vylepšení případových studií.
- **Aktualizace dat**: Aktualizováno datum v zápatí na nejnovější revizi (26. září 2025).

### Vylepšení kvality dokumentace
- **Zlepšení konzistence**: Standardizováno formátování a struktura případových studií napříč všemi sedmi příklady.
- **Komplexní pokrytí**: Případové studie nyní pokrývají scénáře podnikové integrace, produktivity vývojářů a rozvoje ekosystému.
- **Strategické umístění**: Posílen důraz na MCP jako základní platformu pro nasazení agentických systémů.
- **Integrace zdrojů**: Aktualizovány další zdroje, aby zahrnovaly odkaz na GitHub MCP Registry.

## 15. září 2025

### Rozšíření pokročilých témat – Vlastní transporty a inženýrství kontextu

#### Vlastní transporty MCP (05-AdvancedTopics/mcp-transport/) – Nový průvodce pokročilou implementací
- **README.md**: Kompletní průvodce implementací vlastních transportních mechanismů MCP.
  - **Transport Azure Event Grid**: Komplexní implementace serverless event-driven transportu.
    - Ukázky v C#, TypeScriptu a Pythonu s integrací Azure Functions.
    - Vzory architektury založené na událostech pro škálovatelné MCP řešení.
    - Příjemci webhooků a zpracování zpráv na základě push.
  - **Transport Azure Event Hubs**: Implementace transportu pro vysokou propustnost streamování.
    - Funkce streamování v reálném čase pro scénáře s nízkou latencí.
    - Strategie rozdělení a správa kontrolních bodů.
    - Optimalizace výkonu a dávkování zpráv.
  - **Podnikové integrační vzory**: Produkčně připravené architektonické příklady.
    - Distribuované zpracování MCP napříč více funkcemi Azure.
    - Hybridní transportní architektury kombinující více typů transportů.
    - Strategie trvanlivosti zpráv, spolehlivosti a zpracování chyb.
  - **Zabezpečení a monitorování**: Integrace Azure Key Vault a vzory pozorovatelnosti.
    - Autentizace spravované identity a přístup s minimálními oprávněními.
    - Telemetrie Application Insights a monitorování výkonu.
    - Vzory přerušovačů obvodů a odolnosti proti chybám.
  - **Testovací rámce**: Komplexní strategie testování vlastních transportů.
    - Jednotkové testování s testovacími dvojníky a frameworky pro mocking.
    - Integrační testování s Azure Test Containers.
    - Úvahy o výkonu a zátěžovém testování.

#### Inženýrství kontextu (05-AdvancedTopics/mcp-contextengineering/) – Nová disciplína AI
- **README.md**: Komplexní průzkum inženýrství kontextu jako vznikajícího oboru.
  - **Základní principy**: Kompletní sdílení kontextu, povědomí o rozhodování akcí a správa kontextového okna.
  - **Zarovnání s protokolem MCP**: Jak návrh MCP řeší výzvy inženýrství kontextu.
    - Omezení kontextového okna a strategie progresivního načítání.
    - Určování relevance a dynamické získávání kontextu.
    - Multimodální zpracování kontextu a úvahy o zabezpečení.
  - **Implementační přístupy**: Jednovláknové vs. víceagentové architektury.
    - Techniky chunkování a prioritizace kontextu.
    - Progresivní načítání kontextu a strategie komprese.
    - Vrstvené přístupy ke kontextu a optimalizace získávání.
  - **Rámec měření**: Vznikající metriky pro hodnocení efektivity kontextu.
    - Úvahy o efektivitě vstupu, výkonu, kvalitě a uživatelské zkušenosti.
    - Experimentální přístupy k optimalizaci kontextu.
    - Analýza selhání a metodologie zlepšení.

#### Aktualizace navigace kurikula (README.md)
- **Vylepšená struktura modulů**: Aktualizována tabulka kurikula, aby zahrnovala nová pokročilá témata.
  - Přidány položky Inženýrství kontextu (5.14) a Vlastní transporty (5.15).
  - Konzistentní formátování a navigační odkazy napříč všemi moduly.
  - Aktualizovány popisy, aby odrážely aktuální rozsah obsahu.

### Vylepšení struktury adresářů
- **Standardizace názvů**: Přejmenováno "mcp transport" na "mcp-transport" pro konzistenci s ostatními složkami pokročilých témat.
- **Organizace obsahu**: Všechny složky 05-AdvancedTopics nyní dodržují konzistentní vzor názvů (mcp-[téma]).

### Vylepšení kvality dokumentace
- **Zarovnání se specifikací MCP**: Veškerý nový obsah odkazuje na aktuální specifikaci MCP 2025-06-18.
- **Ukázky ve více jazycích**: Komplexní ukázky kódu v C#, TypeScriptu a Pythonu.
- **Zaměření na podniky**: Produkčně připravené vzory a integrace Azure cloudových služeb.
- **Vizualizace dokumentace**: Diagramy Mermaid pro vizualizaci architektury a toků.

## 18. srpna 2025

### Komplexní aktualizace dokumentace – Standardy MCP 2025-06-18

#### Osvědčené postupy zabezpečení MCP (02-Security/) – Kompletní modernizace
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Kompletní přepis zarovnaný se specifikací MCP 2025-06-18.
  - **Povinné požadavky**: Přidány explicitní požadavky MUST/MUST NOT z oficiální specifikace s jasnými vizuálními indikátory.
  - **12 základních bezpečnostních praktik**: Restrukturalizováno z 15 položek na komplexní bezpečnostní domény.
    - Zabezpečení tokenů a ověřování s integrací externích poskytovatelů identity.
    - Správa relací a transportní zabezpečení s kryptografickými požadavky.
    - Ochrana proti AI-specifickým hrozbám s integrací Microsoft Prompt Shields.
    - Řízení příst
#### Pokročilá témata zabezpečení (05-AdvancedTopics/mcp-security/) - Implementace připravená pro produkci
- **README.md**: Kompletní přepis pro implementaci podnikové bezpečnosti
  - **Aktualizace specifikace**: Aktualizováno na MCP Specifikaci 2025-06-18 s povinnými bezpečnostními požadavky
  - **Vylepšené ověřování**: Integrace Microsoft Entra ID s komplexními příklady v .NET a Java Spring Security
  - **Integrace AI zabezpečení**: Implementace Microsoft Prompt Shields a Azure Content Safety s podrobnými příklady v Pythonu
  - **Pokročilé zmírnění hrozeb**: Komplexní příklady implementace pro:
    - Prevence útoků typu Confused Deputy pomocí PKCE a validace uživatelského souhlasu
    - Prevence předávání tokenů pomocí validace publika a bezpečné správy tokenů
    - Prevence únosu relace pomocí kryptografického propojení a analýzy chování
  - **Integrace podnikové bezpečnosti**: Monitorování Azure Application Insights, detekční pipeline hrozeb a zabezpečení dodavatelského řetězce
  - **Kontrolní seznam implementace**: Jasné rozlišení povinných a doporučených bezpečnostních opatření s výhodami ekosystému Microsoft

### Kvalita dokumentace a sladění se standardy
- **Odkazy na specifikace**: Aktualizovány všechny odkazy na aktuální MCP Specifikaci 2025-06-18
- **Ekosystém zabezpečení Microsoft**: Vylepšené pokyny k integraci v celé dokumentaci o zabezpečení
- **Praktická implementace**: Přidány podrobné příklady kódu v .NET, Java a Python s podnikových vzory
- **Organizace zdrojů**: Komplexní kategorizace oficiální dokumentace, bezpečnostních standardů a implementačních příruček
- **Vizualizace požadavků**: Jasné označení povinných požadavků oproti doporučeným postupům

#### Základní koncepty (01-CoreConcepts/) - Kompletní modernizace
- **Aktualizace verze protokolu**: Aktualizováno na aktuální MCP Specifikaci 2025-06-18 s verzováním podle data (formát YYYY-MM-DD)
- **Vylepšení architektury**: Zlepšené popisy Hostů, Klientů a Serverů, které odrážejí aktuální vzory MCP architektury
  - Hosté nyní jasně definováni jako AI aplikace koordinující více připojení MCP klientů
  - Klienti popsáni jako konektory protokolu udržující vztahy jeden na jednoho se servery
  - Servery vylepšeny o scénáře lokálního vs. vzdáleného nasazení
- **Restrukturalizace primitiv**: Kompletní přepracování primitiv serveru a klienta
  - Primitivy serveru: Zdroje (datové zdroje), Výzvy (šablony), Nástroje (spustitelné funkce) s podrobnými vysvětleními a příklady
  - Primitivy klienta: Sampling (LLM dokončení), Elicitation (uživatelský vstup), Logging (ladění/monitorování)
  - Aktualizováno s aktuálními metodami pro objevování (`*/list`), získávání (`*/get`) a provádění (`*/call`)
- **Architektura protokolu**: Představen dvouvrstvý model architektury
  - Datová vrstva: Základ JSON-RPC 2.0 s řízením životního cyklu a primitivy
  - Transportní vrstva: STDIO (lokální) a Streamable HTTP se SSE (vzdálené) transportní mechanismy
- **Bezpečnostní rámec**: Komplexní bezpečnostní principy včetně explicitního uživatelského souhlasu, ochrany soukromí dat, bezpečnosti nástrojů a zabezpečení transportní vrstvy
- **Komunikační vzory**: Aktualizovány zprávy protokolu pro zobrazení inicializace, objevování, provádění a toků oznámení
- **Příklady kódu**: Aktualizovány příklady v různých jazycích (.NET, Java, Python, JavaScript), aby odrážely aktuální vzory MCP SDK

#### Zabezpečení (02-Security/) - Komplexní přepracování zabezpečení  
- **Sladění se standardy**: Plné sladění s bezpečnostními požadavky MCP Specifikace 2025-06-18
- **Evoluce ověřování**: Dokumentována evoluce od vlastních OAuth serverů k delegaci externích poskytovatelů identity (Microsoft Entra ID)
- **Analýza hrozeb specifických pro AI**: Rozšířené pokrytí moderních útoků na AI
  - Podrobné scénáře útoků na injekci výzev s příklady z reálného světa
  - Mechanismy otravy nástrojů a vzory útoků typu "rug pull"
  - Otrava kontextového okna a útoky na zmatení modelu
- **Řešení zabezpečení AI od Microsoftu**: Komplexní pokrytí ekosystému zabezpečení Microsoft
  - AI Prompt Shields s pokročilou detekcí, zvýrazněním a technikami oddělovačů
  - Vzory integrace Azure Content Safety
  - GitHub Advanced Security pro ochranu dodavatelského řetězce
- **Pokročilé zmírnění hrozeb**: Podrobné bezpečnostní kontroly pro:
  - Únos relace s MCP-specifickými scénáři útoků a požadavky na kryptografické ID relace
  - Problémy typu Confused Deputy v proxy scénářích MCP s explicitními požadavky na souhlas
  - Zranitelnosti předávání tokenů s povinnými kontrolami validace
- **Zabezpečení dodavatelského řetězce**: Rozšířené pokrytí AI dodavatelského řetězce včetně základních modelů, služeb embeddingů, poskytovatelů kontextu a API třetích stran
- **Základní zabezpečení**: Vylepšená integrace s podnikovými bezpečnostními vzory včetně architektury nulové důvěry a ekosystému Microsoft
- **Organizace zdrojů**: Kategorizovány komplexní odkazy na zdroje podle typu (Oficiální dokumentace, Standardy, Výzkum, Řešení Microsoft, Implementační příručky)

### Vylepšení kvality dokumentace
- **Strukturované vzdělávací cíle**: Vylepšené vzdělávací cíle s konkrétními, akčními výsledky
- **Křížové odkazy**: Přidány odkazy mezi souvisejícími tématy zabezpečení a základních konceptů
- **Aktuální informace**: Aktualizovány všechny odkazy na data a specifikace na aktuální standardy
- **Pokyny k implementaci**: Přidány konkrétní, akční pokyny k implementaci v celém obou sekcích

## 16. července 2025

### README a vylepšení navigace
- Kompletně přepracována navigace kurikula v README.md
- Nahrazeny značky `<details>` přístupnějším formátem tabulky
- Vytvořeny alternativní možnosti rozvržení v nové složce "alternative_layouts"
- Přidány příklady navigace ve stylu karet, záložek a akordeonu
- Aktualizována sekce struktury repozitáře, aby zahrnovala všechny nejnovější soubory
- Vylepšena sekce "Jak používat toto kurikulum" s jasnými doporučeními
- Aktualizovány odkazy na MCP specifikace, aby směřovaly na správné URL
- Přidána sekce Context Engineering (5.14) do struktury kurikula

### Aktualizace studijního průvodce
- Kompletně přepracován studijní průvodce, aby odpovídal aktuální struktuře repozitáře
- Přidány nové sekce pro MCP Klienty a Nástroje a Populární MCP Servery
- Aktualizována vizuální mapa kurikula, aby přesně odrážela všechna témata
- Vylepšeny popisy pokročilých témat, aby pokryly všechny specializované oblasti
- Aktualizována sekce případových studií, aby odrážela skutečné příklady
- Přidán tento komplexní changelog

### Příspěvky komunity (06-CommunityContributions/)
- Přidány podrobné informace o MCP serverech pro generování obrázků
- Přidána komplexní sekce o používání Claude ve VSCode
- Přidány pokyny k nastavení a používání klienta Cline v terminálu
- Aktualizována sekce MCP klientů, aby zahrnovala všechny populární možnosti klientů
- Vylepšeny příklady příspěvků s přesnějšími ukázkami kódu

### Pokročilá témata (05-AdvancedTopics/)
- Organizovány všechny složky specializovaných témat s konzistentním pojmenováním
- Přidány materiály a příklady pro context engineering
- Přidána dokumentace k integraci agenta Foundry
- Vylepšena dokumentace k integraci zabezpečení Entra ID

## 11. června 2025

### Počáteční vytvoření
- Vydána první verze kurikula MCP pro začátečníky
- Vytvořena základní struktura pro všech 10 hlavních sekcí
- Implementována vizuální mapa kurikula pro navigaci
- Přidány počáteční ukázkové projekty v různých programovacích jazycích

### Začínáme (03-GettingStarted/)
- Vytvořeny první příklady implementace serveru
- Přidány pokyny pro vývoj klienta
- Zahrnuty pokyny pro integraci klienta LLM
- Přidána dokumentace k integraci VS Code
- Implementovány příklady serveru s událostmi odesílanými serverem (SSE)

### Základní koncepty (01-CoreConcepts/)
- Přidáno podrobné vysvětlení architektury klient-server
- Vytvořena dokumentace o klíčových komponentách protokolu
- Dokumentovány vzory zpráv v MCP

## 23. května 2025

### Struktura repozitáře
- Inicializován repozitář se základní strukturou složek
- Vytvořeny README soubory pro každou hlavní sekci
- Nastavena infrastruktura pro překlady
- Přidány obrazové materiály a diagramy

### Dokumentace
- Vytvořen počáteční README.md s přehledem kurikula
- Přidány CODE_OF_CONDUCT.md a SECURITY.md
- Nastaven SUPPORT.md s pokyny pro získání pomoci
- Vytvořena předběžná struktura studijního průvodce

## 15. dubna 2025

### Plánování a rámec
- Počáteční plánování kurikula MCP pro začátečníky
- Definovány vzdělávací cíle a cílová skupina
- Nastíněna 10-sekční struktura kurikula
- Vyvinut konceptuální rámec pro příklady a případové studie
- Vytvořeny počáteční prototypové příklady pro klíčové koncepty

---

**Prohlášení**:  
Tento dokument byl přeložen pomocí služby AI pro překlady [Co-op Translator](https://github.com/Azure/co-op-translator). I když se snažíme o přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho původním jazyce by měl být považován za autoritativní zdroj. Pro důležité informace se doporučuje profesionální lidský překlad. Neodpovídáme za žádná nedorozumění nebo nesprávné interpretace vyplývající z použití tohoto překladu.