<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-19T16:05:28+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "sk"
}
-->
# MCP Bezpečnostné Najlepšie Praktiky 2025

Tento komplexný sprievodca obsahuje základné bezpečnostné najlepšie praktiky pre implementáciu systémov Model Context Protocol (MCP) na základe najnovšej **MCP Špecifikácie 2025-06-18** a aktuálnych priemyselných štandardov. Tieto praktiky sa zaoberajú tradičnými bezpečnostnými otázkami, ako aj hrozbami špecifickými pre AI, ktoré sú jedinečné pre nasadenie MCP.

## Kritické Bezpečnostné Požiadavky

### Povinné Bezpečnostné Kontroly (MUST Požiadavky)

1. **Validácia Tokenov**: MCP servery **NESMÚ** akceptovať žiadne tokeny, ktoré neboli výslovne vydané pre samotný MCP server.
2. **Overenie Autorizácie**: MCP servery implementujúce autorizáciu **MUSIA** overiť VŠETKY prichádzajúce požiadavky a **NESMÚ** používať relácie na autentifikáciu.
3. **Súhlas Používateľa**: MCP proxy servery používajúce statické ID klientov **MUSIA** získať výslovný súhlas používateľa pre každého dynamicky registrovaného klienta.
4. **Bezpečné ID Relácií**: MCP servery **MUSIA** používať kryptograficky bezpečné, nedeterministické ID relácií generované pomocou bezpečných generátorov náhodných čísel.

## Základné Bezpečnostné Praktiky

### 1. Validácia a Sanitácia Vstupov
- **Komplexná Validácia Vstupov**: Validujte a sanitizujte všetky vstupy, aby ste zabránili útokom typu injekcia, problémom zmätku zástupcu a zraniteľnostiam prompt injekcie.
- **Vynucovanie Schémy Parametrov**: Implementujte prísnu validáciu JSON schém pre všetky parametre nástrojov a API vstupy.
- **Filtrácia Obsahu**: Používajte Microsoft Prompt Shields a Azure Content Safety na filtrovanie škodlivého obsahu v promptoch a odpovediach.
- **Sanitácia Výstupov**: Validujte a sanitizujte všetky výstupy modelu pred ich prezentáciou používateľom alebo downstream systémom.

### 2. Excelentná Autentifikácia a Autorizácia  
- **Externí Poskytovatelia Identity**: Delegujte autentifikáciu na etablovaných poskytovateľov identity (Microsoft Entra ID, OAuth 2.1 poskytovatelia) namiesto implementácie vlastnej autentifikácie.
- **Jemne Zrnité Povolenia**: Implementujte granulárne, nástrojovo špecifické povolenia podľa princípu najmenšieho privilégia.
- **Správa Životného Cyklu Tokenov**: Používajte krátkodobé prístupové tokeny s bezpečnou rotáciou a správnou validáciou publika.
- **Viacfaktorová Autentifikácia**: Vyžadujte MFA pre všetky administratívne prístupy a citlivé operácie.

### 3. Bezpečné Komunikačné Protokoly
- **Transport Layer Security**: Používajte HTTPS/TLS 1.3 pre všetku MCP komunikáciu s riadnou validáciou certifikátov.
- **End-to-End Šifrovanie**: Implementujte dodatočné vrstvy šifrovania pre vysoko citlivé údaje v prenose a v pokoji.
- **Správa Certifikátov**: Udržiavajte správny životný cyklus certifikátov s automatizovanými procesmi obnovy.
- **Vynucovanie Verzie Protokolu**: Používajte aktuálnu verziu MCP protokolu (2025-06-18) s riadnym vyjednávaním verzie.

### 4. Pokročilé Obmedzovanie Rýchlosti a Ochrana Zdroja
- **Viacvrstvové Obmedzovanie Rýchlosti**: Implementujte obmedzovanie rýchlosti na úrovni používateľa, relácie, nástroja a zdroja, aby ste zabránili zneužitiu.
- **Adaptívne Obmedzovanie Rýchlosti**: Používajte obmedzovanie rýchlosti založené na strojovom učení, ktoré sa prispôsobuje vzorom používania a indikátorom hrozieb.
- **Správa Kvót Zdroja**: Nastavte vhodné limity pre výpočtové zdroje, využitie pamäte a čas vykonávania.
- **Ochrana proti DDoS**: Nasadzujte komplexné systémy ochrany proti DDoS a analýzy prevádzky.

### 5. Komplexné Logovanie a Monitorovanie
- **Štruktúrované Auditné Logovanie**: Implementujte podrobné, vyhľadávateľné logy pre všetky MCP operácie, vykonávania nástrojov a bezpečnostné udalosti.
- **Monitorovanie Bezpečnosti v Reálnom Čase**: Nasadzujte SIEM systémy s AI-poháňanou detekciou anomálií pre MCP pracovné zaťaženia.
- **Logovanie v Súlade s Ochranou Súkromia**: Logujte bezpečnostné udalosti pri rešpektovaní požiadaviek na ochranu údajov a regulácií.
- **Integrácia Incidentnej Reakcie**: Pripojte logovacie systémy k automatizovaným pracovným postupom reakcie na incidenty.

### 6. Vylepšené Praktiky Bezpečného Ukladania
- **Hardvérové Bezpečnostné Moduly**: Používajte úložisko kľúčov podporované HSM (Azure Key Vault, AWS CloudHSM) pre kritické kryptografické operácie.
- **Správa Šifrovacích Kľúčov**: Implementujte správnu rotáciu kľúčov, segregáciu a kontrolu prístupu pre šifrovacie kľúče.
- **Správa Tajomstiev**: Ukladajte všetky API kľúče, tokeny a poverenia v dedikovaných systémoch správy tajomstiev.
- **Klasifikácia Údajov**: Klasifikujte údaje na základe úrovní citlivosti a aplikujte vhodné ochranné opatrenia.

### 7. Pokročilá Správa Tokenov
- **Prevencia Passthrough Tokenov**: Výslovne zakážte vzory passthrough tokenov, ktoré obchádzajú bezpečnostné kontroly.
- **Validácia Publika**: Vždy overujte, či tvrdenia publika tokenov zodpovedajú identite zamýšľaného MCP servera.
- **Autorizácia na Základe Tvrdení**: Implementujte jemne zrnité autorizácie na základe tvrdení tokenov a atribútov používateľa.
- **Väzba Tokenov**: Viažte tokeny na konkrétne relácie, používateľov alebo zariadenia, kde je to vhodné.

### 8. Bezpečná Správa Relácií
- **Kryptografické ID Relácií**: Generujte ID relácií pomocou kryptograficky bezpečných generátorov náhodných čísel (nie predvídateľných sekvencií).
- **Väzba na Používateľa**: Viažte ID relácií na informácie špecifické pre používateľa pomocou bezpečných formátov ako `<user_id>:<session_id>`.
- **Kontroly Životného Cyklu Relácií**: Implementujte správne mechanizmy vypršania, rotácie a zneplatnenia relácií.
- **Bezpečnostné Hlavičky Relácií**: Používajte vhodné HTTP bezpečnostné hlavičky na ochranu relácií.

### 9. Bezpečnostné Kontroly Špecifické pre AI
- **Obrana proti Prompt Injekcii**: Nasadzujte Microsoft Prompt Shields s technikami spotlightingu, delimitermi a označovaním údajov.
- **Prevencia Otravy Nástrojov**: Validujte metadáta nástrojov, monitorujte dynamické zmeny a overujte integritu nástrojov.
- **Validácia Výstupov Modelu**: Skenujte výstupy modelu na potenciálne úniky údajov, škodlivý obsah alebo porušenie bezpečnostných politík.
- **Ochrana Kontextového Okna**: Implementujte kontroly na prevenciu otravy kontextového okna a manipulačných útokov.

### 10. Bezpečnosť Vykonávania Nástrojov
- **Sandboxing Vykonávania**: Spúšťajte vykonávania nástrojov v kontajnerizovaných, izolovaných prostrediach s limitmi zdrojov.
- **Oddelenie Privilégií**: Spúšťajte nástroje s minimálnymi potrebnými privilégiami a oddelenými servisnými účtami.
- **Izolácia Siete**: Implementujte segmentáciu siete pre prostredia vykonávania nástrojov.
- **Monitorovanie Vykonávania**: Monitorujte vykonávanie nástrojov na anomálne správanie, využitie zdrojov a bezpečnostné porušenia.

### 11. Kontinuálna Validácia Bezpečnosti
- **Automatizované Bezpečnostné Testovanie**: Integrujte bezpečnostné testovanie do CI/CD pipeline s nástrojmi ako GitHub Advanced Security.
- **Správa Zraniteľností**: Pravidelne skenujte všetky závislosti, vrátane AI modelov a externých služieb.
- **Penetračné Testovanie**: Pravidelne vykonávajte bezpečnostné hodnotenia zamerané špecificky na implementácie MCP.
- **Bezpečnostné Recenzie Kódu**: Implementujte povinné bezpečnostné recenzie pre všetky zmeny kódu súvisiace s MCP.

### 12. Bezpečnosť Dodávateľského Reťazca pre AI
- **Overenie Komponentov**: Overujte pôvod, integritu a bezpečnosť všetkých AI komponentov (modely, embeddings, API).
- **Správa Závislostí**: Udržiavajte aktuálne inventáre všetkých softvérových a AI závislostí s sledovaním zraniteľností.
- **Dôveryhodné Repozitáre**: Používajte overené, dôveryhodné zdroje pre všetky AI modely, knižnice a nástroje.
- **Monitorovanie Dodávateľského Reťazca**: Neustále monitorujte kompromisy u poskytovateľov AI služieb a repozitárov modelov.

## Pokročilé Bezpečnostné Vzory

### Architektúra Zero Trust pre MCP
- **Nikdy Nedôveruj, Vždy Overuj**: Implementujte kontinuálne overovanie pre všetkých účastníkov MCP.
- **Mikro-segmentácia**: Izolujte komponenty MCP s granulárnymi sieťovými a identitnými kontrolami.
- **Podmienený Prístup**: Implementujte kontroly prístupu založené na riziku, ktoré sa prispôsobujú kontextu a správaniu.
- **Kontinuálne Hodnotenie Rizika**: Dynamicky vyhodnocujte bezpečnostný postoj na základe aktuálnych indikátorov hrozieb.

### Implementácia AI s Ochranu Súkromia
- **Minimalizácia Údajov**: Zverejňujte iba minimálne potrebné údaje pre každú MCP operáciu.
- **Diferenciálna Ochrana Súkromia**: Implementujte techniky ochrany súkromia pri spracovaní citlivých údajov.
- **Homomorfné Šifrovanie**: Používajte pokročilé šifrovacie techniky na bezpečné výpočty na šifrovaných údajoch.
- **Federované Učenie**: Implementujte distribuované metódy učenia, ktoré zachovávajú lokalitu údajov a ochranu súkromia.

### Reakcia na Incidenty pre AI Systémy
- **Postupy Špecifické pre AI Incidenty**: Vyvíjajte postupy reakcie na incidenty prispôsobené hrozbám špecifickým pre AI a MCP.
- **Automatizovaná Reakcia**: Implementujte automatizované obmedzenie a nápravu pre bežné bezpečnostné incidenty AI.
- **Forenzné Schopnosti**: Udržiavajte pripravenosť na forenzné vyšetrovanie kompromisov AI systémov a únikov údajov.
- **Postupy Obnovy**: Zriaďte postupy na obnovu po otrave AI modelov, útokoch prompt injekcie a kompromisoch služieb.

## Implementačné Zdroje & Štandardy

### Oficiálna Dokumentácia MCP
- [MCP Špecifikácia 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Aktuálna špecifikácia MCP protokolu
- [MCP Bezpečnostné Najlepšie Praktiky](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Oficiálne bezpečnostné usmernenia
- [MCP Autorizácia Špecifikácia](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Vzory autentifikácie a autorizácie
- [MCP Transportná Bezpečnosť](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Požiadavky na bezpečnosť transportnej vrstvy

### Microsoft Bezpečnostné Riešenia
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Pokročilá ochrana proti prompt injekcii
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Komplexná filtrácia AI obsahu
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Podniková správa identity a prístupu
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Bezpečná správa tajomstiev a poverení
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Skenovanie bezpečnosti dodávateľského reťazca a kódu

### Bezpečnostné Štandardy & Rámce
- [OAuth 2.1 Bezpečnostné Najlepšie Praktiky](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Aktuálne usmernenia bezpečnosti OAuth
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Riziká webových aplikácií
- [OWASP Top 10 pre LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Riziká špecifické pre AI
- [NIST AI Rámec Riadenia Rizík](https://www.nist.gov/itl/ai-risk-management-framework) - Komplexné riadenie rizík AI
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Systémy riadenia informačnej bezpečnosti

### Implementačné Príručky & Tutoriály
- [Azure API Management ako MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Vzory podnikovej autentifikácie
- [Microsoft Entra ID s MCP Servermi](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integrácia poskytovateľa identity
- [Implementácia Bezpečného Ukladania Tokenov](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Najlepšie praktiky správy tokenov
- [End-to-End Šifrovanie pre AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Pokročilé vzory šifrovania

### Pokročilé Bezpečnostné Zdroje
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Praktiky bezpečného vývoja
- [AI Red Team Usmernenia](https://learn.microsoft.com/security/ai-red-team/) - Testovanie bezpečnosti špecifické pre AI
- [Modelovanie Hrozieb pre AI Systémy](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodológia modelovania hrozieb AI
- [Inžinierstvo Ochrany Súkromia pre AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Techniky ochrany súkromia pre AI

### Súlad & Správa
- [GDPR Súlad pre AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Súlad ochrany súkromia v AI systémoch
- [Rámec Správy AI](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementácia zodpovednej AI
- [SOC 2 pre AI Služby](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Bezpečnostné kontroly pre poskytovateľov AI služieb
- [HIPAA Súlad pre AI](https://learn.microsoft.com/compliance
- **Vývoj nástrojov**: Vyvíjajte a zdieľajte bezpečnostné nástroje a knižnice pre ekosystém MCP

---

*Tento dokument odráža osvedčené bezpečnostné postupy MCP k 18. augustu 2025, na základe špecifikácie MCP 2025-06-18. Bezpečnostné postupy by sa mali pravidelne prehodnocovať a aktualizovať, ako sa protokol a prostredie hrozieb vyvíjajú.*

**Upozornenie**:  
Tento dokument bol preložený pomocou služby na automatický preklad [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, upozorňujeme, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho pôvodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre dôležité informácie odporúčame profesionálny ľudský preklad. Nezodpovedáme za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.