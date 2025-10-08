<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:55:50+00:00",
  "source_file": "changelog.md",
  "language_code": "sk"
}
-->
# Zmeny: MCP pre začiatočníkov

Tento dokument slúži ako záznam všetkých významných zmien vykonaných v učebných osnovách Model Context Protocol (MCP) pre začiatočníkov. Zmeny sú dokumentované v obrátenom chronologickom poradí (najnovšie zmeny sú uvedené ako prvé).

## 6. október 2025

### Rozšírenie sekcie Začíname – Pokročilé používanie serverov & Jednoduchá autentifikácia

#### Pokročilé používanie serverov (03-GettingStarted/10-advanced)
- **Pridaná nová kapitola**: Predstavený komplexný sprievodca pokročilým používaním MCP serverov, pokrývajúci bežné aj nízkoúrovňové serverové architektúry.
  - **Bežné vs. nízkoúrovňové servery**: Podrobný porovnávací prehľad a ukážky kódu v Python a TypeScript pre oba prístupy.
  - **Dizajn založený na handleroch**: Vysvetlenie správy nástrojov/zdrojov/promptov založenej na handleroch pre škálovateľné a flexibilné implementácie serverov.
  - **Praktické vzory**: Scenáre z reálneho sveta, kde sú nízkoúrovňové serverové vzory prospešné pre pokročilé funkcie a architektúru.

#### Jednoduchá autentifikácia (03-GettingStarted/11-simple-auth)
- **Pridaná nová kapitola**: Krok za krokom sprievodca implementáciou jednoduchej autentifikácie na MCP serveroch.
  - **Koncepty autentifikácie**: Jasné vysvetlenie rozdielu medzi autentifikáciou a autorizáciou, a správa poverení.
  - **Implementácia základnej autentifikácie**: Vzory autentifikácie založené na middleware v Python (Starlette) a TypeScript (Express), s ukážkami kódu.
  - **Prechod na pokročilú bezpečnosť**: Odporúčania, ako začať s jednoduchou autentifikáciou a prejsť na OAuth 2.1 a RBAC, s odkazmi na pokročilé bezpečnostné moduly.

Tieto doplnky poskytujú praktické, praktické pokyny na vytváranie robustnejších, bezpečnejších a flexibilnejších implementácií MCP serverov, spájajúc základné koncepty s pokročilými produkčnými vzormi.

## 29. september 2025

### MCP Server Database Integration Labs - Komplexná praktická učebná cesta

#### 11-MCPServerHandsOnLabs - Nový kompletný učebný plán integrácie databáz
- **Kompletná 13-laboratórna učebná cesta**: Pridaný komplexný praktický učebný plán na vytváranie produkčne pripravených MCP serverov s integráciou databázy PostgreSQL.
  - **Implementácia z reálneho sveta**: Prípadová štúdia Zava Retail analytics demonštrujúca vzory na podnikovej úrovni.
  - **Štruktúrovaný učebný postup**:
    - **Laboratóriá 00-03: Základy** - Úvod, základná architektúra, bezpečnosť & multi-tenancy, nastavenie prostredia.
    - **Laboratóriá 04-06: Budovanie MCP servera** - Návrh databázy & schéma, implementácia MCP servera, vývoj nástrojov.
    - **Laboratóriá 07-09: Pokročilé funkcie** - Integrácia semantického vyhľadávania, testovanie & ladenie, integrácia VS Code.
    - **Laboratóriá 10-12: Produkcia & najlepšie postupy** - Stratégie nasadenia, monitorovanie & observabilita, optimalizácia & najlepšie postupy.
  - **Podnikové technológie**: FastMCP framework, PostgreSQL s pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Pokročilé funkcie**: Row Level Security (RLS), semantické vyhľadávanie, multi-tenantný prístup k dátam, vektorové embeddings, monitorovanie v reálnom čase.

#### Štandardizácia terminológie - Konverzia z "Module" na "Lab"
- **Komplexná aktualizácia dokumentácie**: Systematicky aktualizované všetky README súbory v 11-MCPServerHandsOnLabs na používanie terminológie "Lab" namiesto "Module".
  - **Hlavičky sekcií**: Aktualizované "What This Module Covers" na "What This Lab Covers" vo všetkých 13 laboratóriách.
  - **Popis obsahu**: Zmenené "This module provides..." na "This lab provides..." v celej dokumentácii.
  - **Ciele učenia**: Aktualizované "By the end of this module..." na "By the end of this lab...".
  - **Navigačné odkazy**: Konvertované všetky odkazy "Module XX:" na "Lab XX:" v krížových odkazoch a navigácii.
  - **Sledovanie dokončenia**: Aktualizované "After completing this module..." na "After completing this lab...".
  - **Zachované technické odkazy**: Zachované odkazy na Python moduly v konfiguračných súboroch (napr. `"module": "mcp_server.main"`).

#### Vylepšenie študijného sprievodcu (study_guide.md)
- **Vizualizácia učebného plánu**: Pridaná nová sekcia "11. Database Integration Labs" s komplexnou vizualizáciou štruktúry laboratórií.
- **Štruktúra repozitára**: Aktualizované z desiatich na jedenásť hlavných sekcií s podrobným popisom 11-MCPServerHandsOnLabs.
- **Navigačné pokyny**: Rozšírené pokyny na navigáciu pokrývajúce sekcie 00-11.
- **Pokrytie technológií**: Pridané detaily o integrácii FastMCP, PostgreSQL, Azure služieb.
- **Výsledky učenia**: Zdôraznený vývoj produkčne pripravených serverov, vzory integrácie databáz a podniková bezpečnosť.

#### Vylepšenie hlavného README
- **Terminológia založená na laboratóriách**: Aktualizované hlavné README.md v 11-MCPServerHandsOnLabs na konzistentné používanie štruktúry "Lab".
- **Organizácia učebnej cesty**: Jasný postup od základných konceptov cez pokročilú implementáciu až po nasadenie do produkcie.
- **Zameranie na reálny svet**: Dôraz na praktické, praktické učenie s vzormi a technológiami na podnikovej úrovni.

### Zlepšenia kvality a konzistencie dokumentácie
- **Dôraz na praktické učenie**: Posilnený praktický, laboratórny prístup v celej dokumentácii.
- **Zameranie na podnikové vzory**: Zdôraznené produkčne pripravené implementácie a úvahy o podnikovej bezpečnosti.
- **Integrácia technológií**: Komplexné pokrytie moderných Azure služieb a vzorov AI integrácie.
- **Postup učenia**: Jasná, štruktúrovaná cesta od základných konceptov po nasadenie do produkcie.

## 26. september 2025

### Vylepšenie prípadových štúdií - Integrácia GitHub MCP Registry

#### Prípadové štúdie (09-CaseStudy/) - Zameranie na rozvoj ekosystému
- **README.md**: Významné rozšírenie s komplexnou prípadovou štúdiou GitHub MCP Registry.
  - **Prípadová štúdia GitHub MCP Registry**: Nová komplexná prípadová štúdia skúmajúca spustenie GitHub MCP Registry v septembri 2025.
    - **Analýza problému**: Podrobný rozbor fragmentovaných výziev pri objavovaní a nasadzovaní MCP serverov.
    - **Architektúra riešenia**: Centralizovaný prístup k registru GitHub s jedným kliknutím na inštaláciu VS Code.
    - **Dopad na podnikanie**: Merateľné zlepšenia pri onboardingu vývojárov a produktivite.
    - **Strategická hodnota**: Zameranie na modulárne nasadenie agentov a interoperabilitu medzi nástrojmi.
    - **Rozvoj ekosystému**: Pozicionovanie ako základná platforma pre integráciu agentov.
  - **Vylepšená štruktúra prípadových štúdií**: Aktualizované všetkých sedem prípadových štúdií s konzistentným formátovaním a komplexnými popismi.
    - Azure AI Travel Agents: Dôraz na orchestráciu viacerých agentov.
    - Integrácia Azure DevOps: Zameranie na automatizáciu pracovných postupov.
    - Real-Time Documentation Retrieval: Implementácia klienta Python konzoly.
    - Interaktívny generátor študijných plánov: Chainlit konverzačná webová aplikácia.
    - Dokumentácia v editore: Integrácia VS Code a GitHub Copilot.
    - Azure API Management: Vzory integrácie podnikových API.
    - GitHub MCP Registry: Rozvoj ekosystému a komunitná platforma.
  - **Komplexný záver**: Prepracovaná záverečná sekcia zdôrazňujúca sedem prípadových štúdií pokrývajúcich rôzne dimenzie implementácie MCP.
    - Kategorizácia: Podniková integrácia, orchestrácia viacerých agentov, produktivita vývojárov.
    - Rozvoj ekosystému, vzdelávacie aplikácie.
    - Rozšírené poznatky o architektonických vzoroch, implementačných stratégiách a najlepších postupoch.
    - Dôraz na MCP ako zrelý, produkčne pripravený protokol.

#### Aktualizácie študijného sprievodcu (study_guide.md)
- **Vizualizácia učebného plánu**: Aktualizovaná myšlienková mapa na zahrnutie GitHub MCP Registry v sekcii Prípadové štúdie.
- **Popis prípadových štúdií**: Rozšírené z generických popisov na podrobný rozbor siedmich komplexných prípadových štúdií.
- **Štruktúra repozitára**: Aktualizovaná sekcia 10 na odrážanie komplexného pokrytia prípadových štúdií so špecifickými detailmi implementácie.
- **Integrácia zmien**: Pridaný záznam z 26. septembra 2025 dokumentujúci pridanie GitHub MCP Registry a vylepšenia prípadových štúdií.
- **Aktualizácie dátumu**: Aktualizovaný časový údaj v pätičke na odrážanie najnovšej revízie (26. september 2025).

### Zlepšenia kvality dokumentácie
- **Zlepšenie konzistencie**: Štandardizované formátovanie a štruktúra prípadových štúdií vo všetkých siedmich príkladoch.
- **Komplexné pokrytie**: Prípadové štúdie teraz pokrývajú podnikové, produktivitu vývojárov a scenáre rozvoja ekosystému.
- **Strategické pozicionovanie**: Zdôraznený MCP ako základná platforma pre nasadenie agentických systémov.
- **Integrácia zdrojov**: Aktualizované doplnkové zdroje na zahrnutie odkazu na GitHub MCP Registry.

## 15. september 2025

### Rozšírenie pokročilých tém - Vlastné transporty & Context Engineering

#### MCP Vlastné transporty (05-AdvancedTopics/mcp-transport/) - Nový pokročilý sprievodca implementáciou
- **README.md**: Kompletný sprievodca implementáciou vlastných transportných mechanizmov MCP.
  - **Transport Azure Event Grid**: Komplexná implementácia serverless event-driven transportu.
    - Príklady v C#, TypeScript a Python s integráciou Azure Functions.
    - Vzory architektúry založenej na udalostiach pre škálovateľné MCP riešenia.
    - Prijímače webhookov a spracovanie správ na základe push.
  - **Transport Azure Event Hubs**: Implementácia transportu s vysokou priepustnosťou pre scenáre s nízkou latenciou.
    - Schopnosti streamovania v reálnom čase.
    - Stratégie rozdelenia a správa kontrolných bodov.
    - Optimalizácia výkonu a dávkovanie správ.
  - **Vzory podnikovej integrácie**: Produkčne pripravené architektonické príklady.
    - Distribuované spracovanie MCP naprieč viacerými Azure Functions.
    - Hybridné transportné architektúry kombinujúce viac typov transportov.
    - Stratégie odolnosti správ, spoľahlivosti a spracovania chýb.
  - **Bezpečnosť & monitorovanie**: Integrácia Azure Key Vault a vzory observability.
    - Autentifikácia spravovaných identít a prístup s najnižšími oprávneniami.
    - Telemetria Application Insights a monitorovanie výkonu.
    - Circuit breakers a vzory tolerancie chýb.
  - **Testovacie rámce**: Komplexné testovacie stratégie pre vlastné transporty.
    - Jednotkové testovanie s testovacími dvojníkmi a rámcami na simuláciu.
    - Integračné testovanie s Azure Test Containers.
    - Úvahy o výkonnostnom a záťažovom testovaní.

#### Context Engineering (05-AdvancedTopics/mcp-contextengineering/) - Nová disciplína AI
- **README.md**: Komplexný prieskum Context Engineering ako vznikajúcej oblasti.
  - **Základné princípy**: Kompletné zdieľanie kontextu, uvedomenie si rozhodnutí o akciách a správa kontextového okna.
  - **Zladenie s MCP protokolom**: Ako dizajn MCP rieši výzvy Context Engineering.
    - Obmedzenia kontextového okna a stratégie progresívneho načítania.
    - Určovanie relevantnosti a dynamické získavanie kontextu.
    - Spracovanie multimodálneho kontextu a úvahy o bezpečnosti.
  - **Implementačné prístupy**: Jednovláknové vs. architektúry viacerých agentov.
    - Techniky chunkovania a prioritizácie kontextu.
    - Progresívne načítanie kontextu a kompresné stratégie.
    - Vrstvené prístupy ku kontextu a optimalizácia získavania.
  - **Rámec merania**: Vznikajúce metriky na hodnotenie efektívnosti kontextu.
    - Úvahy o efektívnosti vstupov, výkone, kvalite a používateľskej skúsenosti.
    - Experimentálne prístupy k optimalizácii kontextu.
    - Analýza zlyhaní a metodológie zlepšovania.

#### Aktualizácie navigácie učebných osnov (README.md)
- **Vylepšená štruktúra modulov**: Aktualizovaná tabuľka učebných osnov na zahrnutie nových pokročilých tém.
  - Pridané Context Engineering (5.14) a Custom Transport (5.15).
  - Konzistentné formátovanie a navigačné odkazy vo všetkých moduloch.
  - Aktualizované popisy na odrážanie aktuálneho rozsahu obsahu.

### Zlepšenia štruktúry adresárov
- **Štandardizácia názvov**: Premenované "mcp transport" na "mcp-transport" pre konzistenciu s ostatnými pokročilými témami.
- **Organizácia obsahu**: Všetky adresáre 05-AdvancedTopics teraz dodržiavajú konzistentný vzor názvov (mcp-[téma]).

### Zlepšenia kvality dokumentácie
- **Zladenie so špecifikáciou MCP**: Všetok nový obsah odkazuje na aktuálnu špecifikáciu MCP 2025-06-18.
- **Príklady vo viacerých jazykoch**: Komplexné ukážky kódu v C#, TypeScript a Python.
- **Zameranie na podniky**: Produkčne pripravené vzory a integrácia Azure cloudových služieb.
- **Vizualizácia dokumentácie**: Diagramy Mermaid na vizualizáciu architektúry a tokov.

## 18. august 2025

### Komplexná aktualizácia dokumentácie - Štandardy MCP 2025-06-18

#### MCP Najlepšie bezpečnostné postupy (02-Security/) - Kompletná modernizácia
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Kompletné prepracovanie v súlade so špecifikáciou MCP 2025-06-18.
  - **Povinné požiadavky**: Pridané explicitné požiadavky MUST/MUST NOT z oficiálnej špecifikácie s jasnými vizuálnymi indikátormi.
  - **12 základných bezpečnostných postupov**: Prepracované z 15-bodového zoznamu na komplexné
#### Pokročilé témy zabezpečenia (05-AdvancedTopics/mcp-security/) - Implementácia pripravená na produkciu
- **README.md**: Kompletné prepracovanie pre podnikové zabezpečenie
  - **Aktuálne zosúladenie špecifikácie**: Aktualizované na MCP špecifikáciu 2025-06-18 s povinnými bezpečnostnými požiadavkami
  - **Vylepšená autentifikácia**: Integrácia Microsoft Entra ID s komplexnými príkladmi v .NET a Java Spring Security
  - **Integrácia AI zabezpečenia**: Implementácia Microsoft Prompt Shields a Azure Content Safety s podrobnými príkladmi v Pythone
  - **Pokročilé zmierňovanie hrozieb**: Komplexné implementačné príklady pre:
    - Prevenciu útokov typu Confused Deputy pomocou PKCE a validácie súhlasu používateľa
    - Prevenciu prenosu tokenov pomocou validácie publika a bezpečného spravovania tokenov
    - Prevenciu únosu relácie pomocou kryptografického prepojenia a analýzy správania
  - **Integrácia podnikového zabezpečenia**: Monitorovanie Azure Application Insights, detekčné pipeline hrozieb a zabezpečenie dodávateľského reťazca
  - **Kontrolný zoznam implementácie**: Jasné rozlíšenie povinných a odporúčaných bezpečnostných opatrení s výhodami ekosystému Microsoft zabezpečenia

### Kvalita dokumentácie a zosúladenie štandardov
- **Referencie špecifikácie**: Aktualizované všetky odkazy na aktuálnu MCP špecifikáciu 2025-06-18
- **Ekosystém Microsoft zabezpečenia**: Vylepšené pokyny na integráciu v celej dokumentácii o zabezpečení
- **Praktická implementácia**: Pridané podrobné príklady kódu v .NET, Java a Python s podnikateľskými vzormi
- **Organizácia zdrojov**: Komplexná kategorizácia oficiálnej dokumentácie, bezpečnostných štandardov a implementačných príručiek
- **Vizualizácia požiadaviek**: Jasné označenie povinných požiadaviek oproti odporúčaným postupom

#### Základné koncepty (01-CoreConcepts/) - Kompletná modernizácia
- **Aktualizácia verzie protokolu**: Aktualizované na aktuálnu MCP špecifikáciu 2025-06-18 s dátumovým formátovaním verzií (YYYY-MM-DD)
- **Vylepšenie architektúry**: Vylepšené popisy hostiteľov, klientov a serverov na odrážanie aktuálnych vzorov MCP architektúry
  - Hostitelia sú teraz jasne definovaní ako AI aplikácie koordinujúce viacero pripojení MCP klientov
  - Klienti sú opísaní ako konektory protokolu udržiavajúce vzťahy jeden na jedného so servermi
  - Servery sú vylepšené o scenáre lokálneho a vzdialeného nasadenia
- **Restrukturalizácia primitív**: Kompletná revízia primitív servera a klienta
  - Primitívy servera: Zdroje (databázy), Výzvy (šablóny), Nástroje (vykonateľné funkcie) s podrobnými vysvetleniami a príkladmi
  - Primitívy klienta: Sampling (LLM dokončenia), Elicitation (vstup používateľa), Logging (ladenie/monitorovanie)
  - Aktualizované aktuálnymi vzormi metód objavovania (`*/list`), získavania (`*/get`) a vykonávania (`*/call`)
- **Architektúra protokolu**: Predstavený dvojvrstvový model architektúry
  - Dátová vrstva: Základ JSON-RPC 2.0 s riadením životného cyklu a primitívami
  - Transportná vrstva: STDIO (lokálne) a Streamable HTTP so SSE (vzdialené) transportné mechanizmy
- **Bezpečnostný rámec**: Komplexné bezpečnostné princípy vrátane explicitného súhlasu používateľa, ochrany súkromia dát, bezpečnosti vykonávania nástrojov a zabezpečenia transportnej vrstvy
- **Komunikačné vzory**: Aktualizované správy protokolu na zobrazenie inicializácie, objavovania, vykonávania a notifikačných tokov
- **Príklady kódu**: Obnovené viacjazyčné príklady (.NET, Java, Python, JavaScript) na odrážanie aktuálnych vzorov MCP SDK

#### Zabezpečenie (02-Security/) - Komplexná revízia zabezpečenia  
- **Zosúladenie štandardov**: Úplné zosúladenie s bezpečnostnými požiadavkami MCP špecifikácie 2025-06-18
- **Evolúcia autentifikácie**: Dokumentovaná evolúcia od vlastných OAuth serverov k delegácii externých poskytovateľov identity (Microsoft Entra ID)
- **Analýza hrozieb špecifických pre AI**: Rozšírené pokrytie moderných útokov na AI
  - Podrobné scenáre útokov na injekciu výziev s príkladmi z reálneho sveta
  - Mechanizmy otravy nástrojov a vzory útokov typu "rug pull"
  - Otrava kontextového okna a útoky na zmätok modelu
- **Riešenia Microsoft AI zabezpečenia**: Komplexné pokrytie ekosystému Microsoft zabezpečenia
  - AI Prompt Shields s pokročilou detekciou, zvýraznením a technikami delimitácie
  - Vzory integrácie Azure Content Safety
  - GitHub Advanced Security na ochranu dodávateľského reťazca
- **Pokročilé zmierňovanie hrozieb**: Podrobné bezpečnostné opatrenia pre:
  - Únos relácie s MCP špecifickými scenármi útokov a požiadavkami na kryptografické ID relácie
  - Problémy typu Confused Deputy v scenároch MCP proxy s explicitnými požiadavkami na súhlas
  - Zraniteľnosti prenosu tokenov s povinnými kontrolami validácie
- **Zabezpečenie dodávateľského reťazca**: Rozšírené pokrytie AI dodávateľského reťazca vrátane základných modelov, služieb embeddingu, poskytovateľov kontextu a API tretích strán
- **Základné zabezpečenie**: Vylepšená integrácia s podnikateľskými bezpečnostnými vzormi vrátane architektúry nulovej dôvery a ekosystému Microsoft zabezpečenia
- **Organizácia zdrojov**: Kategorizované komplexné odkazy na zdroje podľa typu (Oficiálne dokumenty, Štandardy, Výskum, Riešenia Microsoft, Implementačné príručky)

### Vylepšenia kvality dokumentácie
- **Štruktúrované vzdelávacie ciele**: Vylepšené vzdelávacie ciele s konkrétnymi, akčnými výsledkami
- **Krížové odkazy**: Pridané odkazy medzi súvisiacimi témami zabezpečenia a základných konceptov
- **Aktuálne informácie**: Aktualizované všetky dátumové odkazy a odkazy na špecifikácie na aktuálne štandardy
- **Pokyny na implementáciu**: Pridané konkrétne, akčné pokyny na implementáciu v celom oboch sekciách

## 16. júl 2025

### README a vylepšenia navigácie
- Kompletný redizajn navigácie v README.md
- Nahradené značky `<details>` prístupnejším formátom tabuľky
- Vytvorené alternatívne možnosti rozloženia v novom priečinku "alternative_layouts"
- Pridané príklady navigácie založené na kartách, záložkách a akordeónoch
- Aktualizovaná sekcia štruktúry úložiska na zahrnutie všetkých najnovších súborov
- Vylepšená sekcia "Ako používať tento učebný plán" s jasnými odporúčaniami
- Aktualizované odkazy na MCP špecifikácie na správne URL
- Pridaná sekcia Kontextové inžinierstvo (5.14) do štruktúry učebného plánu

### Aktualizácie študijného sprievodcu
- Kompletná revízia študijného sprievodcu na zosúladenie s aktuálnou štruktúrou úložiska
- Pridané nové sekcie pre MCP klientov a nástroje a populárne MCP servery
- Aktualizovaná vizuálna mapa učebného plánu na presné odrážanie všetkých tém
- Vylepšené popisy pokročilých tém na pokrytie všetkých špecializovaných oblastí
- Aktualizovaná sekcia prípadových štúdií na odrážanie skutočných príkladov
- Pridaný tento komplexný changelog

### Príspevky komunity (06-CommunityContributions/)
- Pridané podrobné informácie o MCP serveroch na generovanie obrázkov
- Pridaná komplexná sekcia o používaní Claude vo VSCode
- Pridané pokyny na nastavenie a používanie klienta Cline v termináli
- Aktualizovaná sekcia MCP klientov na zahrnutie všetkých populárnych možností klientov
- Vylepšené príklady príspevkov s presnejšími ukážkami kódu

### Pokročilé témy (05-AdvancedTopics/)
- Organizované všetky špecializované priečinky tém s konzistentným názvoslovím
- Pridané materiály a príklady kontextového inžinierstva
- Pridaná dokumentácia integrácie agenta Foundry
- Vylepšená dokumentácia integrácie zabezpečenia Entra ID

## 11. jún 2025

### Počiatočné vytvorenie
- Vydaná prvá verzia učebného plánu MCP pre začiatočníkov
- Vytvorená základná štruktúra pre všetkých 10 hlavných sekcií
- Implementovaná vizuálna mapa učebného plánu na navigáciu
- Pridané počiatočné vzorové projekty v rôznych programovacích jazykoch

### Začíname (03-GettingStarted/)
- Vytvorené prvé príklady implementácie servera
- Pridané pokyny na vývoj klienta
- Zahrnuté pokyny na integráciu klienta LLM
- Pridaná dokumentácia integrácie VS Code
- Implementované príklady serverov SSE (Server-Sent Events)

### Základné koncepty (01-CoreConcepts/)
- Pridané podrobné vysvetlenie architektúry klient-server
- Vytvorená dokumentácia o kľúčových komponentoch protokolu
- Dokumentované vzory správ v MCP

## 23. máj 2025

### Štruktúra úložiska
- Inicializované úložisko so základnou štruktúrou priečinkov
- Vytvorené README súbory pre každú hlavnú sekciu
- Nastavená infraštruktúra prekladov
- Pridané obrazové zdroje a diagramy

### Dokumentácia
- Vytvorený počiatočný README.md s prehľadom učebného plánu
- Pridané CODE_OF_CONDUCT.md a SECURITY.md
- Nastavený SUPPORT.md s pokynmi na získanie pomoci
- Vytvorená predbežná štruktúra študijného sprievodcu

## 15. apríl 2025

### Plánovanie a rámec
- Počiatočné plánovanie učebného plánu MCP pre začiatočníkov
- Definované vzdelávacie ciele a cieľová skupina
- Načrtnutá 10-sekčná štruktúra učebného plánu
- Vyvinutý konceptuálny rámec pre príklady a prípadové štúdie
- Vytvorené počiatočné prototypové príklady pre kľúčové koncepty

---

**Upozornenie**:  
Tento dokument bol preložený pomocou služby AI prekladu [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, prosím, berte na vedomie, že automatizované preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho rodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.