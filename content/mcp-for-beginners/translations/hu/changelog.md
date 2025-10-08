<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:48:44+00:00",
  "source_file": "changelog.md",
  "language_code": "hu"
}
-->
# Változások naplója: MCP kezdőknek szóló tananyag

Ez a dokumentum a Model Context Protocol (MCP) kezdőknek szóló tananyagában történt jelentős változások nyilvántartására szolgál. A változások fordított időrendben vannak dokumentálva (a legújabb változások elöl).

## 2025. október 6.

### Kezdő lépések szekció bővítése – Haladó szerverhasználat és egyszerű hitelesítés

#### Haladó szerverhasználat (03-GettingStarted/10-advanced)
- **Új fejezet hozzáadva**: Átfogó útmutató a haladó MCP szerverhasználathoz, amely a normál és alacsony szintű szerverarchitektúrákat is lefedi.
  - **Normál vs. alacsony szintű szerver**: Részletes összehasonlítás és Python, valamint TypeScript kódpéldák mindkét megközelítéshez.
  - **Handler-alapú tervezés**: Eszközök/erőforrások/promptok kezelésének magyarázata skálázható, rugalmas szervermegvalósításokhoz.
  - **Gyakorlati minták**: Valós példák arra, hogy az alacsony szintű szerverminták hogyan lehetnek előnyösek haladó funkciók és architektúrák esetén.

#### Egyszerű hitelesítés (03-GettingStarted/11-simple-auth)
- **Új fejezet hozzáadva**: Lépésről lépésre bemutató az egyszerű hitelesítés megvalósításához MCP szerverekben.
  - **Hitelesítési fogalmak**: Az autentikáció és az autorizáció, valamint a hitelesítő adatok kezelésének világos magyarázata.
  - **Egyszerű hitelesítés megvalósítása**: Middleware-alapú hitelesítési minták Pythonban (Starlette) és TypeScriptben (Express), kódmintákkal.
  - **Haladás a fejlettebb biztonság felé**: Útmutató az egyszerű hitelesítéssel való kezdéshez, majd az OAuth 2.1 és RBAC irányába történő fejlődéshez, hivatkozásokkal haladó biztonsági modulokra.

Ezek a kiegészítések gyakorlati, kézzelfogható útmutatást nyújtanak robusztusabb, biztonságosabb és rugalmasabb MCP szervermegvalósítások építéséhez, összekötve az alapvető fogalmakat a haladó gyártási mintákkal.

## 2025. szeptember 29.

### MCP szerver adatbázis-integrációs laborok – Átfogó gyakorlati tanulási útvonal

#### 11-MCPServerHandsOnLabs - Új teljes adatbázis-integrációs tananyag
- **Teljes 13-laboros tanulási útvonal**: Átfogó gyakorlati tananyag hozzáadva, amely bemutatja a gyártásra kész MCP szerverek PostgreSQL adatbázis-integrációval történő építését.
  - **Valós megvalósítás**: Zava Retail analitikai esettanulmány, amely vállalati szintű mintákat mutat be.
  - **Strukturált tanulási folyamat**:
    - **Laborok 00-03: Alapok** - Bevezetés, alapvető architektúra, biztonság és több-bérlős megoldások, környezet beállítása.
    - **Laborok 04-06: MCP szerver építése** - Adatbázis-tervezés és séma, MCP szerver megvalósítása, eszközfejlesztés.
    - **Laborok 07-09: Haladó funkciók** - Szemantikus keresés integrációja, tesztelés és hibakeresés, VS Code integráció.
    - **Laborok 10-12: Gyártás és legjobb gyakorlatok** - Telepítési stratégiák, monitorozás és megfigyelhetőség, legjobb gyakorlatok és optimalizálás.
  - **Vállalati technológiák**: FastMCP keretrendszer, PostgreSQL pgvectorral, Azure OpenAI beágyazások, Azure Container Apps, Application Insights.
  - **Haladó funkciók**: Sor szintű biztonság (RLS), szemantikus keresés, több-bérlős adat-hozzáférés, vektor beágyazások, valós idejű monitorozás.

#### Terminológia szabványosítása - Modulról laborra való átállás
- **Átfogó dokumentáció frissítése**: Az összes README fájl szisztematikus frissítése a 11-MCPServerHandsOnLabs-ban, hogy a "Labor" terminológiát használja a "Modul" helyett.
  - **Szekciófejlécek**: A "Mit tartalmaz ez a modul" frissítése "Mit tartalmaz ez a labor" formára mind a 13 laborban.
  - **Tartalomleírás**: A "Ez a modul biztosítja..." szöveg módosítása "Ez a labor biztosítja..." formára a dokumentációban.
  - **Tanulási célok**: A "A modul végére..." szöveg frissítése "A labor végére..." formára.
  - **Navigációs hivatkozások**: Az összes "Modul XX:" hivatkozás átalakítása "Labor XX:" formára a kereszthivatkozásokban és navigációban.
  - **Teljesítési nyomon követés**: Az "A modul befejezése után..." szöveg frissítése "A labor befejezése után..." formára.
  - **Technikai hivatkozások megőrzése**: A Python modul hivatkozások megőrzése a konfigurációs fájlokban (pl. `"module": "mcp_server.main"`).

#### Tanulási útmutató bővítése (study_guide.md)
- **Vizualizált tananyag térkép**: Új "11. Adatbázis-integrációs laborok" szekció hozzáadása átfogó laborstruktúra vizualizációval.
- **Repository struktúra**: Frissítve tízről tizenegy fő szekcióra, részletes 11-MCPServerHandsOnLabs leírással.
- **Tanulási útvonal útmutató**: Navigációs utasítások bővítése a 00-11 szekciók lefedésére.
- **Technológiai lefedettség**: FastMCP, PostgreSQL, Azure szolgáltatások integrációjának részletei hozzáadva.
- **Tanulási eredmények**: Gyártásra kész szerverfejlesztés, adatbázis-integrációs minták és vállalati biztonság hangsúlyozása.

#### Fő README struktúra bővítése
- **Labor-alapú terminológia**: A fő README.md frissítése a 11-MCPServerHandsOnLabs-ban, hogy következetesen használja a "Labor" struktúrát.
- **Tanulási útvonal szervezése**: Világos haladás az alapvető fogalmaktól a haladó megvalósításon át a gyártási telepítésig.
- **Valós fókusz**: Gyakorlati, kézzelfogható tanulás hangsúlyozása vállalati szintű mintákkal és technológiákkal.

### Dokumentáció minőségi és konzisztencia javítások
- **Gyakorlati tanulás hangsúlyozása**: A dokumentációban megerősítve a gyakorlati, labor-alapú megközelítést.
- **Vállalati minták fókusza**: Gyártásra kész megvalósítások és vállalati biztonsági szempontok kiemelése.
- **Technológiai integráció**: Modern Azure szolgáltatások és AI integrációs minták átfogó lefedettsége.
- **Tanulási folyamat**: Világos, strukturált út az alapvető fogalmaktól a gyártási telepítésig.

## 2025. szeptember 26.

### Esettanulmányok bővítése – GitHub MCP Registry integráció

#### Esettanulmányok (09-CaseStudy/) – Ökoszisztéma fejlesztési fókusz
- **README.md**: Jelentős bővítés átfogó GitHub MCP Registry esettanulmánnyal.
  - **GitHub MCP Registry esettanulmány**: Új átfogó esettanulmány a GitHub MCP Registry szeptemberi 2025-ös bevezetéséről.
    - **Problémaelemzés**: Részletes vizsgálat a töredezett MCP szerver felfedezési és telepítési kihívásokról.
    - **Megoldás architektúra**: GitHub központosított regiszter megközelítése egykattintásos VS Code telepítéssel.
    - **Üzleti hatás**: Mérhető javulások a fejlesztői bevezetésben és termelékenységben.
    - **Stratégiai érték**: Moduláris ügynök telepítés és eszközök közötti interoperabilitás hangsúlyozása.
    - **Ökoszisztéma fejlesztés**: Alapvető platformként való pozícionálás az ügynöki integrációhoz.
  - **Esettanulmányok szerkezetének bővítése**: Mind a hét esettanulmány frissítése következetes formázással és átfogó leírásokkal.
    - Azure AI Travel Agents: Több ügynök összehangolásának hangsúlyozása.
    - Azure DevOps integráció: Workflow automatizálás fókusza.
    - Valós idejű dokumentáció visszakeresés: Python konzol kliens megvalósítás.
    - Interaktív tanulási terv generátor: Chainlit beszélgető webalkalmazás.
    - Szerkesztőben megjelenő dokumentáció: VS Code és GitHub Copilot integráció.
    - Azure API Management: Vállalati API integrációs minták.
    - GitHub MCP Registry: Ökoszisztéma fejlesztés és közösségi platform.
  - **Átfogó következtetés**: Újraírt következtetés szekció, amely kiemeli a hét esettanulmányt, amelyek az MCP megvalósítás több dimenzióját lefedik.
    - Vállalati integráció, több ügynök összehangolása, fejlesztői termelékenység.
    - Ökoszisztéma fejlesztés, oktatási alkalmazások kategorizálása.
    - Mélyebb betekintés az architektúra mintákba, megvalósítási stratégiákba és legjobb gyakorlatokba.
    - Az MCP mint érett, gyártásra kész protokoll hangsúlyozása.

#### Tanulási útmutató frissítések (study_guide.md)
- **Vizualizált tananyag térkép**: Frissített gondolattérkép, amely tartalmazza a GitHub MCP Registry-t az esettanulmányok szekcióban.
- **Esettanulmányok leírása**: Általános leírások helyett részletes bontás a hét átfogó esettanulmányról.
- **Repository struktúra**: A 10. szekció frissítése, hogy átfogó esettanulmány lefedettséget tükrözzön konkrét megvalósítási részletekkel.
- **Változások naplója integráció**: 2025. szeptember 26-i bejegyzés hozzáadása, amely dokumentálja a GitHub MCP Registry kiegészítést és az esettanulmányok bővítéseit.
- **Dátum frissítések**: A lábléc időbélyegének frissítése a legutóbbi módosítás dátumára (2025. szeptember 26.).

### Dokumentáció minőségi javítások
- **Konzisztencia javítása**: Az esettanulmányok formázásának és szerkezetének szabványosítása mind a hét példában.
- **Átfogó lefedettség**: Az esettanulmányok most már lefedik a vállalati, fejlesztői termelékenységi és ökoszisztéma fejlesztési forgatókönyveket.
- **Stratégiai pozícionálás**: Az MCP mint alapvető platform hangsúlyozása az ügynöki rendszer telepítéséhez.
- **Erőforrás integráció**: További erőforrások frissítése, beleértve a GitHub MCP Registry linket.

## 2025. szeptember 15.

### Haladó témák bővítése – Egyedi transzportok és kontextus mérnökség

#### MCP egyedi transzportok (05-AdvancedTopics/mcp-transport/) – Új haladó megvalósítási útmutató
- **README.md**: Teljes megvalósítási útmutató egyedi MCP transzport mechanizmusokhoz.
  - **Azure Event Grid transzport**: Átfogó szerver nélküli eseményvezérelt transzport megvalósítás.
    - C#, TypeScript és Python példák Azure Functions integrációval.
    - Eseményvezérelt architektúra minták skálázható MCP megoldásokhoz.
    - Webhook fogadók és push-alapú üzenetkezelés.
  - **Azure Event Hubs transzport**: Nagy áteresztőképességű streaming transzport megvalósítás.
    - Valós idejű streaming képességek alacsony késleltetésű forgatókönyvekhez.
    - Particionálási stratégiák és ellenőrzési pontok kezelése.
    - Üzenetcsomagolás és teljesítményoptimalizálás.
  - **Vállalati integrációs minták**: Gyártásra kész architektúra példák.
    - Elosztott MCP feldolgozás több Azure Functions között.
    - Hibrid transzport architektúrák több transzport típus kombinálásával.
    - Üzenet tartósság, megbízhatóság és hibakezelési stratégiák.
  - **Biztonság és monitorozás**: Azure Key Vault integráció és megfigyelhetőségi minták.
    - Kezelt identitás hitelesítés és legkisebb jogosultság elve.
    - Application Insights telemetria és teljesítmény monitorozás.
    - Áramköri megszakítók és hibatűrési minták.
  - **Tesztelési keretrendszerek**: Átfogó tesztelési stratégiák egyedi transzportokhoz.
    - Egységtesztelés tesztduplikátumokkal és mock keretrendszerekkel.
    - Integrációs tesztelés Azure Test Containers segítségével.
    - Teljesítmény- és terhelés tesztelési szempontok.

#### Kontextus mérnökség (05-AdvancedTopics/mcp-contextengineering/) – Feltörekvő AI diszciplína
- **README.md**: Átfogó feltárás a kontextus mérnökség mint feltörekvő terület kapcsán.
  - **Alapelvek**: Teljes kontextus megosztás, akciódöntési tudatosság és kontextusablak kezelés.
  - **MCP protokoll igazítása**: Hogyan kezeli az MCP tervezés a kontextus mérnökség kihívásait.
    - Kontextusablak korlátai és progresszív betöltési stratégiák.
    - Relevancia meghatározás és dinamikus kontextus visszakeresés.
    - Többmódú kontextus kezelés és biztonsági szempontok.
  - **Megvalósítási megközelítések**: Egy szálú vs. több ügynök architektúrák.
    - Kontextus darabolás és prioritási technikák.
    - Progresszív kontextus betöltés és tömörítési stratégiák.
    - Rétegezett kontextus megközelítések és visszakeresési optimalizálás.
  - **Mérési keretrendszer**: Feltörekvő metrikák a kontextus hatékonyságának értékelésére.
    - Bemeneti hatékonyság, teljesítmény, minőség és felhasználói élmény szempontok.
    - Kísérleti megközelítések a kontextus optimalizálására.
    - Hibaanalízis és javítási módszertanok.

#### Tananyag navigációs frissítések (README.md)
- **Fejlett modulstruktúra**: A tananyag táblázatának frissítése új haladó témák hozzáadásával.
  - Kontextus mérnökség (5.14) és Egyedi transzport (5.15) bejegyzések hozzáadása.
  - Következetes formázás és navigációs hivatkozások az összes modulban.

#### Haladó Témák Biztonság (05-AdvancedTopics/mcp-security/) - Gyártásra Kész Megvalósítás
- **README.md**: Teljes újraírás vállalati biztonsági megvalósításhoz
  - **Jelenlegi Specifikációhoz Igazítás**: Frissítve az MCP Specifikáció 2025-06-18-hoz kötelező biztonsági követelményekkel
  - **Fejlett Hitelesítés**: Microsoft Entra ID integráció átfogó .NET és Java Spring Security példákkal
  - **AI Biztonsági Integráció**: Microsoft Prompt Shields és Azure Content Safety megvalósítás részletes Python példákkal
  - **Fejlett Fenyegetéscsökkentés**: Átfogó megvalósítási példák
    - Confused Deputy támadás megelőzése PKCE és felhasználói beleegyezés ellenőrzéssel
    - Token továbbítás megelőzése közönségellenőrzéssel és biztonságos tokenkezeléssel
    - Munkamenet eltérítés megelőzése kriptográfiai kötés és viselkedéselemzés segítségével
  - **Vállalati Biztonsági Integráció**: Azure Application Insights monitorozás, fenyegetésészlelési csatornák és ellátási lánc biztonság
  - **Megvalósítási Ellenőrzőlista**: Egyértelmű kötelező és ajánlott biztonsági kontrollok Microsoft biztonsági ökoszisztéma előnyeivel

### Dokumentáció Minősége és Szabványokhoz Igazítás
- **Specifikáció Hivatkozások**: Minden hivatkozás frissítve az MCP Specifikáció 2025-06-18-hoz
- **Microsoft Biztonsági Ökoszisztéma**: Fejlesztett integrációs útmutató az összes biztonsági dokumentációban
- **Gyakorlati Megvalósítás**: Részletes kódpéldák hozzáadva .NET, Java és Python nyelveken vállalati mintákkal
- **Erőforrás Szervezés**: Átfogó kategorizálás hivatalos dokumentációk, biztonsági szabványok és megvalósítási útmutatók szerint
- **Vizualizációs Jelölők**: Kötelező követelmények és ajánlott gyakorlatok egyértelmű megjelölése

#### Alapvető Fogalmak (01-CoreConcepts/) - Teljes Modernizáció
- **Protokoll Verzió Frissítés**: Frissítve az MCP Specifikáció 2025-06-18-ra dátum-alapú verziózással (YYYY-MM-DD formátum)
- **Architektúra Finomítás**: Hostok, kliensek és szerverek leírásának fejlesztése az aktuális MCP architektúra minták tükrében
  - Hostok most egyértelműen AI alkalmazásokként definiálva, amelyek több MCP klienskapcsolatot koordinálnak
  - Kliensek protokoll csatlakozóként leírva, amelyek egy-egy szerverkapcsolatot tartanak fenn
  - Szerverek helyi és távoli telepítési forgatókönyvekkel bővítve
- **Primitívek Átszervezése**: Szerver és kliens primitívek teljes átalakítása
  - Szerver Primitívek: Erőforrások (adatforrások), Promptok (sablonok), Eszközök (végrehajtható funkciók) részletes magyarázatokkal és példákkal
  - Kliens Primitívek: Mintavétel (LLM kiegészítések), Kérdezés (felhasználói bemenet), Naplózás (hibakeresés/monitorozás)
  - Frissítve az aktuális felfedezés (`*/list`), lekérés (`*/get`) és végrehajtás (`*/call`) módszer mintákkal
- **Protokoll Architektúra**: Két rétegű architektúra modell bevezetése
  - Adat Réteg: JSON-RPC 2.0 alap lifecycle menedzsmenttel és primitívekkel
  - Szállítási Réteg: STDIO (helyi) és Streamable HTTP SSE-vel (távoli) szállítási mechanizmusok
- **Biztonsági Keretrendszer**: Átfogó biztonsági elvek, beleértve a kifejezett felhasználói beleegyezést, adatvédelem védelmét, eszköz végrehajtási biztonságot és szállítási réteg biztonságot
- **Kommunikációs Minták**: Protokoll üzenetek frissítése inicializálás, felfedezés, végrehajtás és értesítési folyamatok bemutatására
- **Kódpéldák**: Többnyelvű példák frissítése (.NET, Java, Python, JavaScript) az aktuális MCP SDK minták tükrében

#### Biztonság (02-Security/) - Átfogó Biztonsági Átalakítás  
- **Szabványokhoz Igazítás**: Teljes igazítás az MCP Specifikáció 2025-06-18 biztonsági követelményeihez
- **Hitelesítés Fejlődése**: Dokumentálva az egyedi OAuth szerverektől külső identitásszolgáltató delegációig (Microsoft Entra ID)
- **AI-Specifikus Fenyegetés Elemzés**: Modern AI támadási vektorok kiterjesztett lefedettsége
  - Részletes prompt injekció támadási forgatókönyvek valós példákkal
  - Eszköz mérgezési mechanizmusok és "szőnyegkihúzás" támadási minták
  - Kontextusablak mérgezés és modellzavar támadások
- **Microsoft AI Biztonsági Megoldások**: Microsoft biztonsági ökoszisztéma átfogó lefedettsége
  - AI Prompt Shields fejlett észlelési, kiemelési és határolási technikákkal
  - Azure Content Safety integrációs minták
  - GitHub Advanced Security az ellátási lánc védelmére
- **Fejlett Fenyegetéscsökkentés**: Részletes biztonsági kontrollok
  - Munkamenet eltérítés MCP-specifikus támadási forgatókönyvekkel és kriptográfiai munkamenet ID követelményekkel
  - Confused deputy problémák MCP proxy forgatókönyvekben kifejezett beleegyezési követelményekkel
  - Token továbbítási sebezhetőségek kötelező ellenőrzési kontrollokkal
- **Ellátási Lánc Biztonság**: Kiterjesztett AI ellátási lánc lefedettség, beleértve az alapmodelleket, beágyazási szolgáltatásokat, kontextus szolgáltatókat és harmadik fél API-kat
- **Alapvető Biztonság**: Fejlesztett integráció vállalati biztonsági mintákkal, beleértve a zero trust architektúrát és a Microsoft biztonsági ökoszisztémát
- **Erőforrás Szervezés**: Átfogó erőforrás linkek kategorizálása típus szerint (Hivatalos Dokumentumok, Szabványok, Kutatás, Microsoft Megoldások, Megvalósítási Útmutatók)

### Dokumentáció Minőségi Fejlesztések
- **Strukturált Tanulási Célok**: Fejlesztett tanulási célok konkrét, cselekvésre ösztönző eredményekkel
- **Kereszthivatkozások**: Linkek hozzáadása kapcsolódó biztonsági és alapvető fogalmak témák között
- **Aktuális Információk**: Minden dátumhivatkozás és specifikációs link frissítése aktuális szabványokra
- **Megvalósítási Útmutatás**: Konkrét, cselekvésre ösztönző megvalósítási útmutatások hozzáadása mindkét szakaszban

## 2025. július 16.

### README és Navigációs Fejlesztések
- Teljesen újratervezett tananyag navigáció README.md-ben
- `<details>` tagek lecserélése hozzáférhetőbb táblázat-alapú formátumra
- Alternatív elrendezési opciók létrehozása az új "alternative_layouts" mappában
- Kártya-alapú, lapozható és harmonika-stílusú navigációs példák hozzáadása
- Frissített adattár szerkezeti szakasz az összes legújabb fájl hozzáadásával
- Fejlesztett "Hogyan Használjuk Ezt a Tananyagot" szakasz egyértelmű ajánlásokkal
- Frissített MCP specifikációs linkek a megfelelő URL-ekre mutatva
- Kontextus Mérnöki szakasz (5.14) hozzáadása a tananyag szerkezetéhez

### Tanulási Útmutató Frissítések
- Teljesen átdolgozott tanulási útmutató az aktuális adattár szerkezetéhez igazítva
- Új szakaszok hozzáadása MCP Kliensek és Eszközök, valamint Népszerű MCP Szerverek témában
- Frissített Vizualizált Tananyag Térkép az összes téma pontos tükrözésére
- Fejlesztett Haladó Témák leírások az összes specializált terület lefedésére
- Frissített Esettanulmányok szakasz valós példák tükrözésére
- Hozzáadva ezt az átfogó változásnaplót

### Közösségi Hozzájárulások (06-CommunityContributions/)
- Részletes információk hozzáadása MCP szerverekről képgeneráláshoz
- Átfogó szakasz hozzáadása Claude használatáról VSCode-ban
- Cline terminál kliens beállítási és használati útmutató hozzáadása
- Frissített MCP kliens szakasz az összes népszerű kliens opcióval
- Fejlesztett hozzájárulási példák pontosabb kódmintákkal

### Haladó Témák (05-AdvancedTopics/)
- Minden specializált téma mappa következetes elnevezéssel szervezve
- Kontextus mérnöki anyagok és példák hozzáadása
- Foundry ügynök integrációs dokumentáció hozzáadása
- Fejlesztett Entra ID biztonsági integrációs dokumentáció

## 2025. június 11.

### Kezdeti Létrehozás
- Az MCP Kezdőknek tananyag első verziójának kiadása
- Alapstruktúra létrehozása mind a 10 fő szakaszhoz
- Vizualizált Tananyag Térkép megvalósítása navigációhoz
- Kezdeti mintaprojektek hozzáadása több programozási nyelven

### Első Lépések (03-GettingStarted/)
- Első szerver megvalósítási példák létrehozása
- Kliens fejlesztési útmutatás hozzáadása
- LLM kliens integrációs utasítások hozzáadása
- VS Code integrációs dokumentáció hozzáadása
- Server-Sent Events (SSE) szerver példák megvalósítása

### Alapvető Fogalmak (01-CoreConcepts/)
- Részletes magyarázat hozzáadása kliens-szerver architektúráról
- Dokumentáció létrehozása a protokoll kulcselemeiről
- Üzenetküldési minták dokumentálása MCP-ben

## 2025. május 23.

### Adattár Szerkezete
- Az adattár inicializálása alapvető mappastruktúrával
- README fájlok létrehozása minden fő szakaszhoz
- Fordítási infrastruktúra beállítása
- Képanyagok és diagramok hozzáadása

### Dokumentáció
- Kezdeti README.md létrehozása tananyag áttekintéssel
- CODE_OF_CONDUCT.md és SECURITY.md hozzáadása
- SUPPORT.md beállítása segítségnyújtási útmutatással
- Előzetes tanulási útmutató struktúra létrehozása

## 2025. április 15.

### Tervezés és Keretrendszer
- Az MCP Kezdőknek tananyag kezdeti tervezése
- Tanulási célok és célközönség meghatározása
- A tananyag 10 szakaszos struktúrájának körvonalazása
- Konceptuális keretrendszer kidolgozása példákhoz és esettanulmányokhoz
- Kulcsfogalmak kezdeti prototípus példáinak létrehozása

---

**Felelősség kizárása**:  
Ez a dokumentum az [Co-op Translator](https://github.com/Azure/co-op-translator) AI fordítási szolgáltatás segítségével került lefordításra. Bár törekszünk a pontosságra, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az eredeti nyelvén tekintendő hiteles forrásnak. Fontos információk esetén javasolt professzionális emberi fordítást igénybe venni. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely a fordítás használatából eredhet.