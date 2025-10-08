<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-19T15:04:13+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "hu"
}
-->
# MCP Biztonság: Átfogó védelem AI rendszerek számára

[![MCP Biztonsági Legjobb Gyakorlatok](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.hu.png)](https://youtu.be/88No8pw706o)

_(Kattints a fenti képre a leckéhez tartozó videó megtekintéséhez)_

A biztonság alapvető fontosságú az AI rendszerek tervezésében, ezért kiemelt helyet kap a második szekciónkban. Ez összhangban áll a Microsoft **Secure by Design** elvével, amelyet a [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/) keretében vezettek be.

A Model Context Protocol (MCP) új, erőteljes képességeket hoz az AI-alapú alkalmazásokba, miközben egyedi biztonsági kihívásokat is felvet, amelyek túlmutatnak a hagyományos szoftveres kockázatokon. Az MCP rendszerek szembesülnek mind a már ismert biztonsági problémákkal (biztonságos kódolás, minimális jogosultság, ellátási lánc biztonsága), mind az új, AI-specifikus fenyegetésekkel, mint például a prompt injekció, eszközmérgezés, munkamenet-eltérítés, zavart helyettesítő támadások, token átadási sérülékenységek és dinamikus képességmódosítás.

Ez a lecke az MCP implementációk legkritikusabb biztonsági kockázatait tárgyalja—beleértve az autentikációt, az autorizációt, a túlzott jogosultságokat, az indirekt prompt injekciót, a munkamenet biztonságát, a zavart helyettesítő problémákat, a tokenkezelést és az ellátási lánc sérülékenységeit. Megtanulhatod azokat a gyakorlati kontrollokat és legjobb gyakorlatokat, amelyekkel ezek a kockázatok csökkenthetők, miközben olyan Microsoft megoldásokat használsz, mint a Prompt Shields, az Azure Content Safety és a GitHub Advanced Security az MCP implementációk megerősítésére.

## Tanulási célok

A lecke végére képes leszel:

- **MCP-specifikus fenyegetések azonosítása**: Felismerni az MCP rendszerek egyedi biztonsági kockázatait, beleértve a prompt injekciót, eszközmérgezést, túlzott jogosultságokat, munkamenet-eltérítést, zavart helyettesítő problémákat, token átadási sérülékenységeket és ellátási lánc kockázatokat
- **Biztonsági kontrollok alkalmazása**: Hatékony mitigációk bevezetése, mint például robusztus autentikáció, minimális jogosultság hozzáférés, biztonságos tokenkezelés, munkamenet biztonsági kontrollok és ellátási lánc ellenőrzés
- **Microsoft biztonsági megoldások használata**: Megérteni és bevezetni a Microsoft Prompt Shields, Azure Content Safety és GitHub Advanced Security megoldásait az MCP munkaterhelések védelmére
- **Eszközbiztonság validálása**: Felismerni az eszköz metaadatok validálásának, dinamikus változások monitorozásának és az indirekt prompt injekció elleni védekezés fontosságát
- **Legjobb gyakorlatok integrálása**: Kombinálni a bevált biztonsági alapelveket (biztonságos kódolás, szerver megerősítés, zero trust) az MCP-specifikus kontrollokkal az átfogó védelem érdekében

# MCP Biztonsági Architektúra és Kontrollok

A modern MCP implementációk rétegezett biztonsági megközelítéseket igényelnek, amelyek mind a hagyományos szoftverbiztonságot, mind az AI-specifikus fenyegetéseket kezelik. Az MCP specifikáció gyorsan fejlődik, folyamatosan javítva biztonsági kontrolljait, lehetővé téve a jobb integrációt a vállalati biztonsági architektúrákkal és a bevált gyakorlatokkal.

A [Microsoft Digital Defense Report](https://aka.ms/mddr) kutatása szerint **a jelentett biztonsági incidensek 98%-a megelőzhető lenne robusztus biztonsági higiénia alkalmazásával**. A leghatékonyabb védelmi stratégia az alapvető biztonsági gyakorlatok és az MCP-specifikus kontrollok kombinációja—a bevált alapbiztonsági intézkedések továbbra is a legnagyobb hatással vannak az általános biztonsági kockázatok csökkentésére.

## Jelenlegi Biztonsági Környezet

> **Note:** Ez az információ az MCP biztonsági szabványokat tükrözi **2025. augusztus 18**-i állapot szerint. Az MCP protokoll gyorsan fejlődik, és a jövőbeli implementációk új autentikációs mintákat és továbbfejlesztett kontrollokat vezethetnek be. Mindig hivatkozz az aktuális [MCP Specifikációra](https://spec.modelcontextprotocol.io/), [MCP GitHub repository](https://github.com/modelcontextprotocol) és [biztonsági legjobb gyakorlatok dokumentációjára](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) a legfrissebb útmutatásért.

### MCP Autentikáció Evolúciója

Az MCP specifikáció jelentős fejlődésen ment keresztül az autentikáció és autorizáció megközelítésében:

- **Eredeti megközelítés**: A korai specifikációk megkövetelték, hogy a fejlesztők egyedi autentikációs szervereket implementáljanak, az MCP szerverek pedig OAuth 2.0 Authorization Serverként működtek, közvetlenül kezelve a felhasználói autentikációt
- **Jelenlegi szabvány (2025-06-18)**: A frissített specifikáció lehetővé teszi, hogy az MCP szerverek delegálják az autentikációt külső identitásszolgáltatóknak (például Microsoft Entra ID), javítva a biztonsági helyzetet és csökkentve az implementációs komplexitást
- **Transport Layer Security**: Továbbfejlesztett támogatás a biztonságos szállítási mechanizmusokhoz, megfelelő autentikációs mintákkal mind helyi (STDIO), mind távoli (Streamable HTTP) kapcsolatokhoz

## Autentikáció és Autorizáció Biztonság

### Jelenlegi Biztonsági Kihívások

A modern MCP implementációk számos autentikációs és autorizációs kihívással szembesülnek:

### Kockázatok és Fenyegetési Vektorok

- **Hibásan konfigurált autorizációs logika**: Az MCP szerverek hibás autorizációs implementációja érzékeny adatokhoz való hozzáférést és helytelen hozzáférés-ellenőrzést eredményezhet
- **OAuth token kompromittálása**: Helyi MCP szerver tokenek ellopása lehetővé teszi a támadók számára, hogy szervereket megszemélyesítsenek és hozzáférjenek downstream szolgáltatásokhoz
- **Token átadási sérülékenységek**: Nem megfelelő tokenkezelés biztonsági kontrollok megkerülését és felelősségi hiányosságokat okoz
- **Túlzott jogosultságok**: Túlzott jogosultságokkal rendelkező MCP szerverek megsértik a minimális jogosultság elvét, és növelik a támadási felületet

#### Token Átadás: Kritikus Anti-Pattern

**A token átadás kifejezetten tiltott** az aktuális MCP autorizációs specifikációban a súlyos biztonsági következmények miatt:

##### Biztonsági Kontroll Megkerülése
- Az MCP szerverek és downstream API-k kritikus biztonsági kontrollokat implementálnak (sebességkorlátozás, kérésvalidáció, forgalommonitorozás), amelyek megfelelő tokenvalidációtól függenek
- A közvetlen kliens-API tokenhasználat megkerüli ezeket az alapvető védelmeket, aláásva a biztonsági architektúrát

##### Felelősség és Audit Kihívások  
- Az MCP szerverek nem tudják megkülönböztetni a kliens által használt upstream által kiadott tokeneket, megszakítva az audit nyomvonalakat
- A downstream erőforrás-szerver naplók félrevezető kérés eredeteket mutatnak, nem pedig az MCP szerver közvetítőket
- Az incidensvizsgálat és a megfelelőségi audit jelentősen nehezebbé válik

##### Adatlopási Kockázatok
- Nem validált token állítások lehetővé teszik a rosszindulatú szereplők számára, hogy ellopott tokenekkel az MCP szervereket proxyként használják adatlopásra
- A bizalmi határok megsértése engedélyezi a jogosulatlan hozzáférési mintákat, amelyek megkerülik a tervezett biztonsági kontrollokat

##### Több Szolgáltatást Érintő Támadási Vektorok
- Kompromittált tokenek, amelyeket több szolgáltatás elfogad, lehetővé teszik az oldalirányú mozgást a kapcsolt rendszerek között
- A szolgáltatások közötti bizalmi feltételezések megsérülhetnek, ha a token eredete nem igazolható

### Biztonsági Kontrollok és Mitigációk

**Kritikus Biztonsági Követelmények:**

> **KÖTELEZŐ**: Az MCP szerverek **NEM FOGADHATNAK EL** olyan tokeneket, amelyeket nem kifejezetten az MCP szerver számára bocsátottak ki

#### Autentikáció és Autorizáció Kontrollok

- **Alapos autorizációs felülvizsgálat**: Végezzen átfogó auditokat az MCP szerver autorizációs logikájáról, hogy biztosítsa, csak a szándékolt felhasználók és kliensek férhetnek hozzá érzékeny erőforrásokhoz
  - **Implementációs Útmutató**: [Azure API Management mint autentikációs átjáró MCP szerverekhez](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Identitás Integráció**: [Microsoft Entra ID használata MCP szerver autentikációhoz](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Biztonságos tokenkezelés**: Implementálja [Microsoft token validációs és életciklus legjobb gyakorlatokat](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Validálja, hogy a token közönség állításai megfelelnek az MCP szerver identitásának
  - Implementálja a megfelelő token rotációs és lejárati politikákat
  - Előzze meg a token újrajátszási támadásokat és jogosulatlan használatot

- **Védett token tárolás**: Biztosítsa a token tárolást titkosítással mind nyugalmi állapotban, mind átvitel közben
  - **Legjobb Gyakorlatok**: [Biztonságos token tárolási és titkosítási irányelvek](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Hozzáférés-ellenőrzési Implementáció

- **Minimális jogosultság elve**: Csak a minimálisan szükséges jogosultságokat adja meg az MCP szervereknek a tervezett funkcionalitás érdekében
  - Rendszeres jogosultság felülvizsgálatok és frissítések a jogosultságok növekedésének megelőzésére
  - **Microsoft Dokumentáció**: [Biztonságos minimális jogosultságú hozzáférés](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Szerepkör-alapú hozzáférés-ellenőrzés (RBAC)**: Implementáljon finomhangolt szerepkör-hozzárendeléseket
  - Szűkítse a szerepköröket konkrét erőforrásokra és műveletekre
  - Kerülje a széles vagy szükségtelen jogosultságokat, amelyek növelik a támadási felületet

- **Folyamatos jogosultság monitorozás**: Implementáljon folyamatos hozzáférés auditálást és monitorozást
  - Monitorozza a jogosultság használati mintákat anomáliákért
  - Azonnal orvosolja a túlzott vagy nem használt jogosultságokat

## AI-specifikus Biztonsági Fenyegetések

### Prompt Injekció és Eszköz Manipulációs Támadások

A modern MCP implementációk kifinomult AI-specifikus támadási vektorokkal szembesülnek, amelyeket a hagyományos biztonsági intézkedések nem tudnak teljes mértékben kezelni:

#### **Indirekt Prompt Injekció (Kereszt-Domain Prompt Injekció)**

**Az indirekt prompt injekció** az MCP-alapú AI rendszerek egyik legkritikusabb sérülékenységét képviseli. A támadók rosszindulatú utasításokat ágyaznak be külső tartalmakba—dokumentumokba, weboldalakba, e-mailekbe vagy adatforrásokba—amelyeket az AI rendszerek később legitim parancsként dolgoznak fel.

**Támadási Forgatókönyvek:**
- **Dokumentum-alapú injekció**: Rosszindulatú utasítások elrejtése feldolgozott dokumentumokban, amelyek nem kívánt AI műveleteket váltanak ki
- **Webtartalom kihasználása**: Kompromittált weboldalak beágyazott promptokkal, amelyek manipulálják az AI viselkedését, amikor azokat lekérik
- **E-mail-alapú támadások**: Rosszindulatú promptok e-mailekben, amelyek az AI asszisztenseket információk kiszivárogtatására vagy jogosulatlan műveletek végrehajtására késztetik
- **Adatforrás szennyezés**: Kompromittált adatbázisok vagy API-k, amelyek szennyezett tartalmat szolgáltatnak az AI rendszereknek

**Valós Hatás**: Ezek a támadások adatlopást, adatvédelmi megsértéseket, káros tartalom generálását és felhasználói interakciók manipulálását eredményezhetik. Részletes elemzésért lásd: [Prompt Injekció az MCP-ben (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Prompt Injekció Támadás Diagram](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.hu.png)

#### **Eszköz Mérgezési Támadások**

**Az eszköz mérgezés** az MCP eszközöket meghatározó metaadatokat célozza meg, kihasználva, hogy az LLM-ek hogyan értelmezik az eszközleírásokat és paramétereket a végrehajtási döntések meghozatalához.

**Támadási Mechanizmusok:**
- **Metaadat Manipuláció**: A támadók rosszindulatú utasításokat injektálnak az eszközleírásokba, paraméterdefiníciókba vagy használati példákba
- **Láthatatlan Utasítások**: Rejtett promptok az eszköz metaadatokban, amelyeket az AI modellek feldolgoznak, de emberi felhasználók számára láthatatlanok
- **Dinamikus Eszköz Módosítás ("Rug Pulls")**: A felhasználók által jóváhagyott eszközök később módosulnak, hogy rosszindulatú műveleteket hajtsanak végre a felhasználók tudta nélkül
- **Paraméter Injekció**: Rosszindulatú tartalom beágyazása az eszköz paraméter sémákba, amelyek befolyásolják a modell viselkedését

**Távoli Szerver Kockázatok**: A távoli MCP szerverek fokozott kockázatot jelentenek, mivel az eszközdefiníciók frissíthetők a kezdeti felhasználói jóváhagyás után, olyan helyzeteket teremtve, ahol a korábban biztonságos eszközök rosszindulatúvá válnak. Részletes elemzésért lásd: [Eszköz Mérgezési Támadások (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Eszköz Injekció Támadás
- **Biztonságos munkamenet-generálás**: Használj kriptográfiailag biztonságos, nem-determinisztikus munkamenet-azonosítókat, amelyeket biztonságos véletlenszám-generátorokkal hozol létre.
- **Felhasználó-specifikus kötés**: Kösd a munkamenet-azonosítókat felhasználó-specifikus információkhoz olyan formátumokkal, mint `<user_id>:<session_id>`, hogy megakadályozd a munkamenetek keresztfelhasználói visszaéléseit.
- **Munkamenet-életciklus kezelése**: Valósíts meg megfelelő lejárati, rotációs és érvénytelenítési mechanizmusokat a sebezhetőségi időablakok korlátozása érdekében.
- **Átvitelbiztonság**: Kötelező HTTPS minden kommunikációhoz, hogy megakadályozd a munkamenet-azonosítók elfogását.

### Zavarodott helyettes probléma

A **zavarodott helyettes probléma** akkor fordul elő, amikor az MCP szerverek hitelesítési proxyként működnek az ügyfelek és harmadik fél szolgáltatások között, lehetőséget teremtve az engedélyezési megkerülésre statikus ügyfélazonosítók kihasználásával.

#### **Támadási mechanizmusok és kockázatok**

- **Süti-alapú beleegyezés megkerülése**: Korábbi felhasználói hitelesítés beleegyezési sütiket hoz létre, amelyeket támadók kihasználhatnak rosszindulatú engedélyezési kérésekkel, manipulált átirányítási URI-k használatával.
- **Engedélyezési kód lopás**: A meglévő beleegyezési sütik miatt az engedélyezési szerverek kihagyhatják a beleegyezési képernyőket, és a kódokat támadó által irányított végpontokra irányíthatják.
- **Jogosulatlan API hozzáférés**: Ellopott engedélyezési kódok lehetővé teszik a tokencserét és a felhasználói megszemélyesítést explicit jóváhagyás nélkül.

#### **Megelőzési stratégiák**

**Kötelező kontrollok:**
- **Explicit beleegyezési követelmények**: Az MCP proxy szerverek, amelyek statikus ügyfélazonosítókat használnak, **KÖTELESEK** minden dinamikusan regisztrált ügyfél esetében felhasználói beleegyezést szerezni.
- **OAuth 2.1 biztonsági megvalósítás**: Kövesd az aktuális OAuth biztonsági legjobb gyakorlatokat, beleértve a PKCE-t (Proof Key for Code Exchange) minden engedélyezési kéréshez.
- **Szigorú ügyfél-ellenőrzés**: Valósíts meg alapos ellenőrzést az átirányítási URI-k és ügyfélazonosítók esetében, hogy megakadályozd a visszaéléseket.

### Token továbbítási sebezhetőségek  

A **token továbbítás** egy kifejezett anti-minta, ahol az MCP szerverek ügyfél tokeneket fogadnak el megfelelő ellenőrzés nélkül, és továbbítják azokat downstream API-khoz, megsértve az MCP engedélyezési specifikációit.

#### **Biztonsági következmények**

- **Kontroll megkerülése**: Az ügyfél-API közvetlen tokenhasználat megkerüli a kritikus sebességkorlátozási, ellenőrzési és monitorozási kontrollokat.
- **Audit nyomvonal korrupciója**: A felfelé kiadott tokenek lehetetlenné teszik az ügyfél azonosítását, megszakítva az incidens vizsgálati képességeket.
- **Proxy-alapú adatlopás**: Nem ellenőrzött tokenek lehetővé teszik rosszindulatú szereplők számára, hogy szervereket használjanak proxyként jogosulatlan adat-hozzáféréshez.
- **Bizalmi határ megsértése**: A downstream szolgáltatások bizalmi feltételezései megsérülhetnek, ha a tokenek eredete nem igazolható.
- **Több szolgáltatás elleni támadás kiterjesztése**: Kompromittált tokenek, amelyeket több szolgáltatás elfogad, lehetővé teszik az oldalirányú mozgást.

#### **Szükséges biztonsági kontrollok**

**Nem tárgyalható követelmények:**
- **Token ellenőrzés**: Az MCP szerverek **NEM FOGADHATNAK EL** olyan tokeneket, amelyeket nem kifejezetten az MCP szerver számára bocsátottak ki.
- **Célközönség ellenőrzése**: Mindig ellenőrizd, hogy a token célközönség állításai megfelelnek-e az MCP szerver identitásának.
- **Megfelelő token életciklus**: Valósíts meg rövid élettartamú hozzáférési tokeneket biztonságos rotációs gyakorlatokkal.

## Ellátási lánc biztonsága AI rendszerekhez

Az ellátási lánc biztonsága túllépett a hagyományos szoftverfüggőségeken, és magában foglalja az egész AI ökoszisztémát. A modern MCP megvalósításoknak szigorúan ellenőrizniük és monitorozniuk kell az összes AI-hoz kapcsolódó komponenst, mivel mindegyik potenciális sebezhetőségeket hozhat, amelyek veszélyeztethetik a rendszer integritását.

### Kibővített AI ellátási lánc elemek

**Hagyományos szoftverfüggőségek:**
- Nyílt forráskódú könyvtárak és keretrendszerek
- Konténerképek és alap rendszerek  
- Fejlesztői eszközök és build pipeline-ok
- Infrastruktúra komponensek és szolgáltatások

**AI-specifikus ellátási lánc elemek:**
- **Alapmodellek**: Különböző szolgáltatóktól származó előre betanított modellek, amelyek származásának ellenőrzése szükséges.
- **Beágyazási szolgáltatások**: Külső vektorizációs és szemantikai keresési szolgáltatások.
- **Kontekstszervezők**: Adatforrások, tudásbázisok és dokumentumtárak.  
- **Harmadik fél API-k**: Külső AI szolgáltatások, ML pipeline-ok és adatfeldolgozó végpontok.
- **Modell artefaktumok**: Súlyok, konfigurációk és finomhangolt modellváltozatok.
- **Képzési adatforrások**: Adathalmazok, amelyeket modellképzéshez és finomhangoláshoz használnak.

### Átfogó ellátási lánc biztonsági stratégia

#### **Komponens ellenőrzés és bizalom**
- **Származás ellenőrzése**: Ellenőrizd az összes AI komponens eredetét, licencelését és integritását integráció előtt.
- **Biztonsági értékelés**: Végezzen sebezhetőségi vizsgálatokat és biztonsági áttekintéseket modellek, adatforrások és AI szolgáltatások esetében.
- **Hírnév elemzés**: Értékeld az AI szolgáltatók biztonsági előéletét és gyakorlatát.
- **Megfelelőség ellenőrzése**: Győződj meg arról, hogy minden komponens megfelel a szervezeti biztonsági és szabályozási követelményeknek.

#### **Biztonságos telepítési pipeline-ok**  
- **Automatizált CI/CD biztonság**: Integráld a biztonsági vizsgálatokat az automatizált telepítési pipeline-okba.
- **Artefaktum integritás**: Valósíts meg kriptográfiai ellenőrzést minden telepített artefaktumhoz (kód, modellek, konfigurációk).
- **Szakaszos telepítés**: Használj progresszív telepítési stratégiákat biztonsági validációval minden szakaszban.
- **Megbízható artefaktum tárolók**: Csak ellenőrzött, biztonságos artefaktum regiszterekből és tárolókból telepíts.

#### **Folyamatos monitorozás és válaszadás**
- **Függőség vizsgálat**: Folyamatos sebezhetőségi monitorozás minden szoftver és AI komponens függőség esetében.
- **Modell monitorozás**: Folyamatos értékelés a modell viselkedéséről, teljesítmény eltéréséről és biztonsági anomáliákról.
- **Szolgáltatás egészségügyi követés**: Külső AI szolgáltatások monitorozása elérhetőség, biztonsági incidensek és szabályváltozások szempontjából.
- **Fenyegetés hírszerzés integráció**: AI és ML biztonsági kockázatokra specifikus fenyegetés hírcsatornák beépítése.

#### **Hozzáférés-ellenőrzés és minimális jogosultság**
- **Komponens szintű engedélyek**: Korlátozd a hozzáférést modellekhez, adatokhoz és szolgáltatásokhoz üzleti szükségesség alapján.
- **Szolgáltatásfiók kezelés**: Valósíts meg dedikált szolgáltatásfiókokat minimális szükséges engedélyekkel.
- **Hálózati szegmentáció**: Izoláld az AI komponenseket és korlátozd a hálózati hozzáférést a szolgáltatások között.
- **API átjáró kontrollok**: Használj központosított API átjárókat a külső AI szolgáltatásokhoz való hozzáférés ellenőrzésére és monitorozására.

#### **Incidens válaszadás és helyreállítás**
- **Gyors válasz eljárások**: Létrehozott folyamatok a kompromittált AI komponensek javítására vagy cseréjére.
- **Hitelesítő adatok rotációja**: Automatizált rendszerek titkok, API kulcsok és szolgáltatás hitelesítési adatok rotációjára.
- **Visszaállítási képességek**: Képesség gyorsan visszatérni az AI komponensek korábbi, ismert jó verzióira.
- **Ellátási lánc megsértés helyreállítása**: Specifikus eljárások az upstream AI szolgáltatások kompromittálására való reagáláshoz.

### Microsoft biztonsági eszközök és integráció

**GitHub Advanced Security** átfogó ellátási lánc védelmet nyújt, beleértve:
- **Titokvizsgálat**: Automatizált hitelesítési adatok, API kulcsok és tokenek észlelése a tárolókban.
- **Függőség vizsgálat**: Nyílt forráskódú függőségek és könyvtárak sebezhetőségi értékelése.
- **CodeQL elemzés**: Statikus kód elemzés biztonsági sebezhetőségek és kódolási problémák esetében.
- **Ellátási lánc betekintések**: Függőségek egészségi állapotának és biztonsági státuszának láthatósága.

**Azure DevOps és Azure Repos integráció:**
- Zökkenőmentes biztonsági vizsgálati integráció a Microsoft fejlesztési platformokon.
- Automatizált biztonsági ellenőrzések az Azure Pipelines-ban AI munkaterhelésekhez.
- Politika érvényesítése biztonságos AI komponens telepítéshez.

**Microsoft belső gyakorlatok:**
A Microsoft kiterjedt ellátási lánc biztonsági gyakorlatokat valósít meg minden termék esetében. Tudj meg többet a bevált megközelítésekről a [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/) oldalon.
### **Microsoft Biztonsági Megoldások**
- [Microsoft Prompt Shields Dokumentáció](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Tartalomvédelem Szolgáltatás](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID Biztonság](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Azure Tokenkezelési Legjobb Gyakorlatok](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Fejlett Biztonság](https://github.com/security/advanced-security)

### **Megvalósítási Útmutatók és Oktatóanyagok**
- [Azure API Management mint MCP Hitelesítési Átjáró](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID Hitelesítés MCP Szerverekkel](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Biztonságos Token Tárolás és Titkosítás (Videó)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps és Ellátási Lánc Biztonság**
- [Azure DevOps Biztonság](https://azure.microsoft.com/products/devops)
- [Azure Repos Biztonság](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft Ellátási Lánc Biztonsági Útja](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **További Biztonsági Dokumentáció**

Átfogó biztonsági útmutatásért tekintse meg az alábbi speciális dokumentumokat ebben a szekcióban:

- **[MCP Biztonsági Legjobb Gyakorlatok 2025](./mcp-security-best-practices-2025.md)** - Teljes körű biztonsági legjobb gyakorlatok MCP megvalósításokhoz
- **[Azure Tartalomvédelem Megvalósítása](./azure-content-safety-implementation.md)** - Gyakorlati megvalósítási példák Azure Tartalomvédelem integrációhoz  
- **[MCP Biztonsági Kontrollok 2025](./mcp-security-controls-2025.md)** - Legújabb biztonsági kontrollok és technikák MCP telepítésekhez
- **[MCP Legjobb Gyakorlatok Gyors Referencia](./mcp-best-practices.md)** - Gyors referenciaútmutató az alapvető MCP biztonsági gyakorlatokhoz

---

## Hogyan Tovább

Következő: [3. fejezet: Első lépések](../03-GettingStarted/README.md)

**Felelősségkizárás**:  
Ez a dokumentum az [Co-op Translator](https://github.com/Azure/co-op-translator) AI fordítási szolgáltatás segítségével készült. Bár törekszünk a pontosságra, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az eredeti nyelvén tekintendő hiteles forrásnak. Kritikus információk esetén javasolt a professzionális, emberi fordítás igénybevétele. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy téves értelmezésekért.