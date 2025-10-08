<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-19T16:04:05+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "sk"
}
-->
# MCP Bezpečnosť: Komplexná ochrana pre AI systémy

[![Najlepšie praktiky MCP bezpečnosti](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.sk.png)](https://youtu.be/88No8pw706o)

_(Kliknite na obrázok vyššie pre zobrazenie videa tejto lekcie)_

Bezpečnosť je základom návrhu AI systémov, a preto ju kladieme ako prioritu v našej druhej sekcii. To je v súlade s princípom Microsoftu **Secure by Design** z [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) prináša nové silné schopnosti pre aplikácie poháňané AI, no zároveň zavádza jedinečné bezpečnostné výzvy, ktoré presahujú tradičné softvérové riziká. MCP systémy čelia nielen zavedeným bezpečnostným problémom (bezpečné kódovanie, princíp minimálnych oprávnení, bezpečnosť dodávateľského reťazca), ale aj novým AI-špecifickým hrozbám, ako sú injekcia promptov, otrava nástrojov, únos relácií, útoky zmätku zástupcu, zraniteľnosti pri prechode tokenov a dynamická modifikácia schopností.

Táto lekcia skúma najkritickejšie bezpečnostné riziká pri implementáciách MCP—zahŕňajúc autentifikáciu, autorizáciu, nadmerné oprávnenia, nepriame injekcie promptov, bezpečnosť relácií, problémy zmätku zástupcu, správu tokenov a zraniteľnosti dodávateľského reťazca. Naučíte sa praktické opatrenia a najlepšie praktiky na zmiernenie týchto rizík, pričom využijete riešenia Microsoftu, ako Prompt Shields, Azure Content Safety a GitHub Advanced Security na posilnenie vašej MCP implementácie.

## Ciele učenia

Na konci tejto lekcie budete schopní:

- **Identifikovať MCP-špecifické hrozby**: Rozpoznať jedinečné bezpečnostné riziká v MCP systémoch vrátane injekcie promptov, otravy nástrojov, nadmerných oprávnení, únosu relácií, problémov zmätku zástupcu, zraniteľností pri prechode tokenov a rizík dodávateľského reťazca
- **Aplikovať bezpečnostné opatrenia**: Implementovať efektívne zmiernenia vrátane robustnej autentifikácie, prístupu s minimálnymi oprávneniami, bezpečnej správy tokenov, kontrol bezpečnosti relácií a overovania dodávateľského reťazca
- **Využiť bezpečnostné riešenia Microsoftu**: Pochopiť a nasadiť Microsoft Prompt Shields, Azure Content Safety a GitHub Advanced Security na ochranu MCP pracovných záťaží
- **Overiť bezpečnosť nástrojov**: Rozpoznať dôležitosť validácie metadát nástrojov, monitorovania dynamických zmien a obrany proti nepriamym útokom injekcie promptov
- **Integrovať najlepšie praktiky**: Kombinovať zavedené bezpečnostné základy (bezpečné kódovanie, spevnenie serverov, zero trust) s MCP-špecifickými opatreniami pre komplexnú ochranu

# MCP Bezpečnostná architektúra a opatrenia

Moderné implementácie MCP vyžadujú vrstvené bezpečnostné prístupy, ktoré riešia tradičné softvérové bezpečnostné hrozby aj AI-špecifické riziká. Rýchlo sa vyvíjajúca špecifikácia MCP naďalej zdokonaľuje svoje bezpečnostné opatrenia, čo umožňuje lepšiu integráciu s podnikovou bezpečnostnou architektúrou a zavedenými najlepšími praktikami.

Výskum z [Microsoft Digital Defense Report](https://aka.ms/mddr) ukazuje, že **98 % nahlásených narušení by bolo možné predísť robustnou bezpečnostnou hygienou**. Najefektívnejšia ochranná stratégia kombinuje základné bezpečnostné praktiky s MCP-špecifickými opatreniami—osvedčené základné bezpečnostné opatrenia zostávajú najúčinnejšie pri znižovaní celkového bezpečnostného rizika.

## Súčasná bezpečnostná situácia

> **Poznámka:** Tieto informácie odrážajú bezpečnostné štandardy MCP k **18. augustu 2025**. Špecifikácia MCP sa rýchlo vyvíja a budúce implementácie môžu zaviesť nové autentifikačné vzory a vylepšené opatrenia. Vždy sa odkazujte na aktuálnu [MCP špecifikáciu](https://spec.modelcontextprotocol.io/), [MCP GitHub repozitár](https://github.com/modelcontextprotocol) a [dokumentáciu najlepších bezpečnostných praktík](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) pre najnovšie usmernenia.

### Vývoj autentifikácie MCP

Špecifikácia MCP sa výrazne vyvinula vo svojom prístupe k autentifikácii a autorizácii:

- **Pôvodný prístup**: Skoré špecifikácie vyžadovali, aby vývojári implementovali vlastné autentifikačné servery, pričom MCP servery fungovali ako OAuth 2.0 autorizačné servery, ktoré priamo spravovali autentifikáciu používateľov
- **Súčasný štandard (2025-06-18)**: Aktualizovaná špecifikácia umožňuje MCP serverom delegovať autentifikáciu na externých poskytovateľov identity (ako Microsoft Entra ID), čím sa zlepšuje bezpečnostný postoj a znižuje zložitosť implementácie
- **Transportná vrstva bezpečnosti**: Vylepšená podpora pre bezpečné transportné mechanizmy s vhodnými autentifikačnými vzormi pre lokálne (STDIO) aj vzdialené (Streamable HTTP) pripojenia

## Bezpečnosť autentifikácie a autorizácie

### Súčasné bezpečnostné výzvy

Moderné implementácie MCP čelia viacerým výzvam v oblasti autentifikácie a autorizácie:

### Riziká a hrozby

- **Nesprávne nakonfigurovaná logika autorizácie**: Chybná implementácia autorizácie v MCP serveroch môže odhaliť citlivé údaje a nesprávne aplikovať prístupové kontroly
- **Kompromitácia OAuth tokenov**: Krádež tokenov lokálneho MCP servera umožňuje útočníkom vydávať sa za servery a pristupovať k downstream službám
- **Zraniteľnosti pri prechode tokenov**: Nesprávna manipulácia s tokenmi vytvára obchádzanie bezpečnostných kontrol a medzery v zodpovednosti
- **Nadmerné oprávnenia**: MCP servery s nadmernými oprávneniami porušujú princíp minimálnych oprávnení a rozširujú povrch útoku

#### Prechod tokenov: Kritický anti-vzor

**Prechod tokenov je výslovne zakázaný** v súčasnej špecifikácii autorizácie MCP kvôli vážnym bezpečnostným dôsledkom:

##### Obchádzanie bezpečnostných kontrol
- MCP servery a downstream API implementujú kritické bezpečnostné kontroly (obmedzovanie rýchlosti, validácia požiadaviek, monitorovanie prevádzky), ktoré závisia od správnej validácie tokenov
- Priame použitie tokenov klientom na API obchádza tieto základné ochrany, čím podkopáva bezpečnostnú architektúru

##### Výzvy v oblasti zodpovednosti a auditu  
- MCP servery nedokážu rozlíšiť medzi klientmi používajúcimi upstream vydané tokeny, čím sa narúšajú auditné stopy
- Logy downstream serverov zdrojov ukazujú zavádzajúce pôvody požiadaviek namiesto skutočných MCP serverov ako sprostredkovateľov
- Vyšetrovanie incidentov a audity súladu sa stávajú výrazne náročnejšími

##### Riziká exfiltrácie údajov
- Nevalidované tvrdenia tokenov umožňujú škodlivým aktérom so ukradnutými tokenmi používať MCP servery ako proxy na exfiltráciu údajov
- Porušenie hraníc dôvery umožňuje neoprávnené vzory prístupu, ktoré obchádzajú zamýšľané bezpečnostné kontroly

##### Útoky na viaceré služby
- Kompromitované tokeny akceptované viacerými službami umožňujú laterálny pohyb naprieč prepojenými systémami
- Predpoklady dôvery medzi službami môžu byť porušené, keď nie je možné overiť pôvod tokenov

### Bezpečnostné opatrenia a zmiernenia

**Kritické bezpečnostné požiadavky:**

> **POVINNÉ**: MCP servery **NESMÚ** akceptovať žiadne tokeny, ktoré neboli výslovne vydané pre MCP server

#### Opatrenia pre autentifikáciu a autorizáciu

- **Dôkladná revízia autorizácie**: Vykonajte komplexné audity logiky autorizácie MCP servera, aby ste zabezpečili, že iba zamýšľaní používatelia a klienti môžu pristupovať k citlivým zdrojom
  - **Príručka implementácie**: [Azure API Management ako autentifikačná brána pre MCP servery](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Integrácia identity**: [Použitie Microsoft Entra ID pre autentifikáciu MCP servera](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Bezpečná správa tokenov**: Implementujte [najlepšie praktiky Microsoftu pre validáciu a životný cyklus tokenov](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Validujte tvrdenia o publiku tokenov, aby zodpovedali identite MCP servera
  - Implementujte správne politiky rotácie a expirácie tokenov
  - Zabráňte replay útokom a neoprávnenému použitiu tokenov

- **Chránené úložisko tokenov**: Zabezpečte úložisko tokenov šifrovaním v pokoji aj počas prenosu
  - **Najlepšie praktiky**: [Pokyny pre bezpečné úložisko a šifrovanie tokenov](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementácia prístupových kontrol

- **Princíp minimálnych oprávnení**: Udeľte MCP serverom iba minimálne oprávnenia potrebné na zamýšľanú funkčnosť
  - Pravidelné revízie a aktualizácie oprávnení na zabránenie ich rozširovaniu
  - **Dokumentácia Microsoftu**: [Zabezpečený prístup s minimálnymi oprávneniami](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Role-Based Access Control (RBAC)**: Implementujte jemne zrnité priradenia rolí
  - Role obmedzte na konkrétne zdroje a akcie
  - Vyhnite sa širokým alebo zbytočným oprávneniam, ktoré rozširujú povrch útoku

- **Kontinuálne monitorovanie oprávnení**: Implementujte priebežné audity a monitorovanie prístupu
  - Monitorujte vzory používania oprávnení na anomálie
  - Okamžite riešte nadmerné alebo nepoužívané oprávnenia
- **Generovanie bezpečných relácií**: Používajte kryptograficky bezpečné, nedeterministické ID relácií generované pomocou bezpečných generátorov náhodných čísel  
- **Väzba na používateľa**: Viažte ID relácií na informácie špecifické pre používateľa pomocou formátov ako `<user_id>:<session_id>` na zabránenie zneužitia relácií medzi používateľmi  
- **Správa životného cyklu relácií**: Implementujte správne vypršanie, rotáciu a zneplatnenie relácií na obmedzenie okien zraniteľnosti  
- **Bezpečnosť prenosu**: Povinné používanie HTTPS pre všetku komunikáciu na zabránenie zachytenia ID relácií  

### Problém zmäteného zástupcu

**Problém zmäteného zástupcu** nastáva, keď servery MCP fungujú ako autentifikačné proxy medzi klientmi a službami tretích strán, čím vytvárajú príležitosti na obídenie autorizácie prostredníctvom zneužitia statických ID klientov.

#### **Mechanizmy útoku a riziká**

- **Obídenie súhlasu na základe cookies**: Predchádzajúca autentifikácia používateľa vytvára cookies súhlasu, ktoré útočníci zneužívajú prostredníctvom škodlivých požiadaviek na autorizáciu s upravenými URI presmerovania  
- **Krádež autorizačných kódov**: Existujúce cookies súhlasu môžu spôsobiť, že autorizačné servery preskočia obrazovky súhlasu, čím presmerujú kódy na koncové body kontrolované útočníkmi  
- **Neoprávnený prístup k API**: Ukradnuté autorizačné kódy umožňujú výmenu tokenov a vydávanie sa za používateľa bez výslovného schválenia  

#### **Stratégie zmiernenia**

**Povinné opatrenia:**
- **Požiadavky na výslovný súhlas**: Proxy servery MCP používajúce statické ID klientov **MUSIA** získať súhlas používateľa pre každého dynamicky registrovaného klienta  
- **Implementácia bezpečnosti OAuth 2.1**: Dodržiavajte aktuálne osvedčené postupy bezpečnosti OAuth vrátane PKCE (Proof Key for Code Exchange) pre všetky požiadavky na autorizáciu  
- **Prísna validácia klientov**: Implementujte dôkladnú validáciu URI presmerovania a identifikátorov klientov na zabránenie zneužitiu  

### Zraniteľnosti pri preposielaní tokenov  

**Preposielanie tokenov** predstavuje explicitný anti-vzor, pri ktorom servery MCP prijímajú tokeny klientov bez riadnej validácie a preposielajú ich na downstream API, čím porušujú špecifikácie autorizácie MCP.

#### **Bezpečnostné dôsledky**

- **Obídenie kontroly**: Priame použitie tokenov klienta na API obchádza kritické obmedzenia rýchlosti, validáciu a monitorovacie kontroly  
- **Narušenie auditnej stopy**: Tokeny vydané upstreamom znemožňujú identifikáciu klienta, čím narúšajú schopnosti vyšetrovania incidentov  
- **Proxy pre exfiltráciu dát**: Nevalidované tokeny umožňujú škodlivým aktérom používať servery ako proxy na neoprávnený prístup k dátam  
- **Porušenie hraníc dôvery**: Predpoklady dôvery downstream služieb môžu byť porušené, keď nie je možné overiť pôvod tokenov  
- **Rozšírenie útokov na viaceré služby**: Kompromitované tokeny akceptované viacerými službami umožňujú laterálny pohyb  

#### **Požadované bezpečnostné opatrenia**

**Nepostrádateľné požiadavky:**
- **Validácia tokenov**: Servery MCP **NESMÚ** akceptovať tokeny, ktoré neboli výslovne vydané pre server MCP  
- **Overenie publika**: Vždy overujte, či tvrdenia o publiku tokenov zodpovedajú identite servera MCP  
- **Správny životný cyklus tokenov**: Implementujte krátkodobé prístupové tokeny s bezpečnými praktikami rotácie  

## Bezpečnosť dodávateľského reťazca pre AI systémy

Bezpečnosť dodávateľského reťazca sa vyvinula nad rámec tradičných softvérových závislostí a zahŕňa celý ekosystém AI. Moderné implementácie MCP musia dôkladne overovať a monitorovať všetky komponenty súvisiace s AI, pretože každý z nich predstavuje potenciálne zraniteľnosti, ktoré môžu ohroziť integritu systému.

### Rozšírené komponenty dodávateľského reťazca AI

**Tradičné softvérové závislosti:**
- Open-source knižnice a frameworky  
- Kontajnerové obrazy a základné systémy  
- Nástroje na vývoj a build pipeline  
- Komponenty a služby infraštruktúry  

**AI-špecifické prvky dodávateľského reťazca:**
- **Základné modely**: Predtrénované modely od rôznych poskytovateľov vyžadujúce overenie pôvodu  
- **Služby vkladania**: Externé služby na vektorizáciu a sémantické vyhľadávanie  
- **Poskytovatelia kontextu**: Zdroje dát, znalostné bázy a úložiská dokumentov  
- **API tretích strán**: Externé AI služby, ML pipeline a koncové body na spracovanie dát  
- **Artefakty modelov**: Váhy, konfigurácie a varianty modelov doladené na mieru  
- **Zdroje tréningových dát**: Dátové sady použité na tréning a doladenie modelov  

### Komplexná stratégia bezpečnosti dodávateľského reťazca

#### **Overenie komponentov a dôveryhodnosť**
- **Overenie pôvodu**: Overte pôvod, licencovanie a integritu všetkých AI komponentov pred ich integráciou  
- **Bezpečnostné hodnotenie**: Vykonajte skenovanie zraniteľností a bezpečnostné kontroly modelov, zdrojov dát a AI služieb  
- **Analýza reputácie**: Vyhodnoťte bezpečnostnú históriu a praktiky poskytovateľov AI služieb  
- **Overenie súladu**: Uistite sa, že všetky komponenty spĺňajú bezpečnostné a regulačné požiadavky organizácie  

#### **Bezpečné nasadzovacie pipeline**  
- **Automatizovaná bezpečnosť CI/CD**: Integrujte bezpečnostné skenovanie do automatizovaných pipeline nasadzovania  
- **Integrita artefaktov**: Implementujte kryptografické overenie všetkých nasadených artefaktov (kód, modely, konfigurácie)  
- **Postupné nasadzovanie**: Používajte progresívne stratégie nasadzovania s bezpečnostnou validáciou na každom kroku  
- **Dôveryhodné úložiská artefaktov**: Nasadzujte iba z overených, bezpečných úložísk a repozitárov artefaktov  

#### **Kontinuálne monitorovanie a reakcia**
- **Skenovanie závislostí**: Neustále monitorovanie zraniteľností všetkých softvérových a AI komponentov  
- **Monitorovanie modelov**: Kontinuálne hodnotenie správania modelov, odchýlok výkonu a bezpečnostných anomálií  
- **Sledovanie zdravia služieb**: Monitorovanie externých AI služieb z hľadiska dostupnosti, bezpečnostných incidentov a zmien politík  
- **Integrácia spravodajstva o hrozbách**: Zahrnutie informačných kanálov o hrozbách špecifických pre AI a ML bezpečnostné riziká  

#### **Kontrola prístupu a princíp minimálnych oprávnení**
- **Oprávnenia na úrovni komponentov**: Obmedzte prístup k modelom, dátam a službám na základe obchodnej potreby  
- **Správa servisných účtov**: Implementujte dedikované servisné účty s minimálnymi potrebnými oprávneniami  
- **Segmentácia siete**: Izolujte AI komponenty a obmedzte sieťový prístup medzi službami  
- **Kontroly API brány**: Používajte centralizované API brány na kontrolu a monitorovanie prístupu k externým AI službám  

#### **Reakcia na incidenty a obnova**
- **Postupy rýchlej reakcie**: Zavedené procesy na opravu alebo výmenu kompromitovaných AI komponentov  
- **Rotácia poverení**: Automatizované systémy na rotáciu tajomstiev, API kľúčov a poverení služieb  
- **Možnosti návratu späť**: Schopnosť rýchlo sa vrátiť k predchádzajúcim známym dobrým verziám AI komponentov  
- **Obnova po narušení dodávateľského reťazca**: Špecifické postupy na reakciu na kompromitácie upstream AI služieb  

### Nástroje a integrácia bezpečnosti od Microsoftu

**GitHub Advanced Security** poskytuje komplexnú ochranu dodávateľského reťazca vrátane:  
- **Skenovania tajomstiev**: Automatická detekcia poverení, API kľúčov a tokenov v repozitároch  
- **Skenovania závislostí**: Hodnotenie zraniteľností pre open-source závislosti a knižnice  
- **Analýzy CodeQL**: Statická analýza kódu na zraniteľnosti a problémy s kódovaním  
- **Prehľad dodávateľského reťazca**: Viditeľnosť zdravia a bezpečnostného stavu závislostí  

**Integrácia Azure DevOps a Azure Repos:**
- Bezproblémová integrácia bezpečnostného skenovania naprieč vývojovými platformami Microsoftu  
- Automatizované bezpečnostné kontroly v Azure Pipelines pre AI pracovné záťaže  
- Presadzovanie politík pre bezpečné nasadzovanie AI komponentov  

**Interné praktiky Microsoftu:**
Microsoft implementuje rozsiahle bezpečnostné praktiky dodávateľského reťazca naprieč všetkými produktmi. Viac sa dozviete v [Cesta k zabezpečeniu softvérového dodávateľského reťazca v Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).
### **Microsoft Security Solutions**
- [Microsoft Prompt Shields Dokumentácia](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety Služba](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID Bezpečnosť](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Najlepšie postupy pre správu tokenov v Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Pokročilá bezpečnosť](https://github.com/security/advanced-security)

### **Príručky implementácie a návody**
- [Azure API Management ako MCP autentifikačná brána](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID autentifikácia s MCP servermi](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Bezpečné ukladanie a šifrovanie tokenov (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps a bezpečnosť dodávateľského reťazca**
- [Bezpečnosť Azure DevOps](https://azure.microsoft.com/products/devops)
- [Bezpečnosť Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [Cesta Microsoftu k zabezpečeniu dodávateľského reťazca](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Ďalšia bezpečnostná dokumentácia**

Pre komplexné bezpečnostné pokyny si pozrite tieto špecializované dokumenty v tejto sekcii:

- **[MCP Najlepšie bezpečnostné postupy 2025](./mcp-security-best-practices-2025.md)** - Kompletné najlepšie bezpečnostné postupy pre implementácie MCP
- **[Implementácia Azure Content Safety](./azure-content-safety-implementation.md)** - Praktické príklady implementácie integrácie Azure Content Safety  
- **[MCP Bezpečnostné kontroly 2025](./mcp-security-controls-2025.md)** - Najnovšie bezpečnostné kontroly a techniky pre nasadenia MCP
- **[Rýchly referenčný sprievodca MCP najlepšími postupmi](./mcp-best-practices.md)** - Rýchly sprievodca základnými bezpečnostnými postupmi MCP

---

## Čo ďalej

Ďalej: [Kapitola 3: Začíname](../03-GettingStarted/README.md)

**Upozornenie**:  
Tento dokument bol preložený pomocou služby na automatický preklad [Co-op Translator](https://github.com/Azure/co-op-translator). Aj keď sa snažíme o presnosť, upozorňujeme, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho pôvodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre dôležité informácie sa odporúča profesionálny ľudský preklad. Nezodpovedáme za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.