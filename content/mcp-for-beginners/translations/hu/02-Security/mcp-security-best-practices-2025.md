<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-19T15:02:09+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "hu"
}
-->
# MCP Biztonsági Legjobb Gyakorlatok - 2025 Augusztusi Frissítés

> **Fontos**: Ez a dokumentum a legfrissebb [MCP Specifikáció 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) biztonsági követelményeit és hivatalos [MCP Biztonsági Legjobb Gyakorlatokat](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) tükrözi. Mindig az aktuális specifikációra hivatkozzon a legfrissebb útmutatás érdekében.

## Alapvető Biztonsági Gyakorlatok MCP Implementációkhoz

A Model Context Protocol egyedi biztonsági kihívásokat vezet be, amelyek túlmutatnak a hagyományos szoftverbiztonságon. Ezek a gyakorlatok az alapvető biztonsági követelményeket és az MCP-specifikus fenyegetéseket kezelik, beleértve a prompt injekciót, eszközmérgezést, munkamenet-eltérítést, zavart helyettesítő problémákat és token átadási sebezhetőségeket.

### **KÖTELEZŐ Biztonsági Követelmények**

**Kritikus Követelmények az MCP Specifikációból:**

> **NEM SZABAD**: MCP szerverek **NEM SZABAD** elfogadniuk olyan tokeneket, amelyeket nem kifejezetten az MCP szerver számára bocsátottak ki  
> 
> **KELL**: Az engedélyezést megvalósító MCP szervereknek **KELL** ellenőrizniük MINDEN bejövő kérést  
>  
> **NEM SZABAD**: MCP szerverek **NEM SZABAD** munkameneteket használniuk hitelesítésre  
>
> **KELL**: Az MCP proxy szervereknek, amelyek statikus kliensazonosítókat használnak, **KELL** felhasználói beleegyezést szerezniük minden dinamikusan regisztrált klienshez  

---

## 1. **Token Biztonság és Hitelesítés**

**Hitelesítési és Engedélyezési Ellenőrzések:**
   - **Alapos Engedélyezési Felülvizsgálat**: Végezzen átfogó auditokat az MCP szerver engedélyezési logikáján, hogy biztosítsa, csak a szándékolt felhasználók és kliensek férhetnek hozzá az erőforrásokhoz  
   - **Külső Identitásszolgáltató Integráció**: Használjon bevált identitásszolgáltatókat, mint például a Microsoft Entra ID, ahelyett, hogy egyedi hitelesítést valósítana meg  
   - **Token Célközönség Ellenőrzése**: Mindig ellenőrizze, hogy a tokeneket kifejezetten az Ön MCP szerveréhez bocsátották-e ki - soha ne fogadjon el upstream tokeneket  
   - **Megfelelő Token Életciklus**: Valósítson meg biztonságos token rotációt, lejárati szabályokat, és akadályozza meg a token újrajátszási támadásokat  

**Védett Token Tárolás:**
   - Használjon Azure Key Vault-ot vagy hasonló biztonságos hitelesítő tárolókat minden titokhoz  
   - Valósítson meg titkosítást a tokenek számára nyugalmi állapotban és átvitel közben  
   - Rendszeres hitelesítő rotáció és jogosulatlan hozzáférés monitorozása  

## 2. **Munkamenet Kezelés és Átvitel Biztonság**

**Biztonságos Munkamenet Gyakorlatok:**
   - **Kriptográfiailag Biztonságos Munkamenet Azonosítók**: Használjon biztonságos, nem determinisztikus munkamenet azonosítókat, amelyeket biztonságos véletlenszám-generátorokkal hoznak létre  
   - **Felhasználó-specifikus Kötés**: Kösse a munkamenet azonosítókat a felhasználói identitásokhoz olyan formátumokkal, mint `<user_id>:<session_id>`, hogy megakadályozza a keresztfelhasználói munkamenet visszaéléseket  
   - **Munkamenet Életciklus Kezelés**: Valósítson meg megfelelő lejáratot, rotációt és érvénytelenítést a sebezhetőségi ablakok korlátozása érdekében  
   - **HTTPS/TLS Kötelezővé Tétele**: Kötelező HTTPS minden kommunikációhoz, hogy megakadályozza a munkamenet azonosítók elfogását  

**Átvitel Réteg Biztonság:**
   - Konfigurálja a TLS 1.3-at, ahol lehetséges, megfelelő tanúsítványkezeléssel  
   - Valósítson meg tanúsítvány rögzítést kritikus kapcsolatokhoz  
   - Rendszeres tanúsítvány rotáció és érvényesség ellenőrzés  

## 3. **AI-specifikus Fenyegetésvédelem** 🤖

**Prompt Injekció Elleni Védelem:**
   - **Microsoft Prompt Shields**: Telepítse az AI Prompt Shields-t a rosszindulatú utasítások fejlett észlelésére és szűrésére  
   - **Bemenet Tisztítása**: Ellenőrizze és tisztítsa meg minden bemenetet, hogy megakadályozza az injekciós támadásokat és zavart helyettesítő problémákat  
   - **Tartalom Határok**: Használjon elválasztó és adatjelölő rendszereket, hogy megkülönböztesse a megbízható utasításokat a külső tartalomtól  

**Eszközmérgezés Megelőzése:**
   - **Eszköz Metaadat Ellenőrzés**: Valósítson meg integritásellenőrzéseket az eszközdefiníciókhoz, és monitorozza a váratlan változásokat  
   - **Dinamikus Eszköz Monitorozás**: Figyelje a futásidejű viselkedést, és állítson be riasztásokat a váratlan végrehajtási mintákhoz  
   - **Jóváhagyási Munkafolyamatok**: Követelje meg a felhasználói jóváhagyást az eszköz módosításokhoz és képességváltozásokhoz  

## 4. **Hozzáférés-ellenőrzés és Jogosultságok**

**Minimális Jogosultság Elve:**
   - Adjon MCP szervereknek csak minimális jogosultságokat, amelyek szükségesek a tervezett funkciókhoz  
   - Valósítson meg szerepkör-alapú hozzáférés-ellenőrzést (RBAC) finomhangolt jogosultságokkal  
   - Rendszeres jogosultság felülvizsgálatok és folyamatos monitorozás a jogosultságok emelkedésének megelőzésére  

**Futásidejű Jogosultság Ellenőrzések:**
   - Alkalmazzon erőforrás-korlátokat, hogy megakadályozza az erőforrás kimerítési támadásokat  
   - Használjon konténer izolációt az eszköz végrehajtási környezetekhez  
   - Valósítson meg just-in-time hozzáférést az adminisztratív funkciókhoz  

## 5. **Tartalom Biztonság és Monitorozás**

**Tartalom Biztonság Megvalósítása:**
   - **Azure Content Safety Integráció**: Használja az Azure Content Safety-t káros tartalom, jailbreak kísérletek és szabályszegések észlelésére  
   - **Viselkedési Elemzés**: Valósítson meg futásidejű viselkedés monitorozást az MCP szerver és eszköz végrehajtás anomáliáinak észlelésére  
   - **Átfogó Naplózás**: Naplózzon minden hitelesítési kísérletet, eszköz hívást és biztonsági eseményt biztonságos, manipulációbiztos tárolással  

**Folyamatos Monitorozás:**
   - Valós idejű riasztások gyanús minták és jogosulatlan hozzáférési kísérletek esetén  
   - Integráció SIEM rendszerekkel a központosított biztonsági eseménykezelés érdekében  
   - Rendszeres biztonsági auditok és penetrációs tesztek az MCP implementációkhoz  

## 6. **Ellátási Lánc Biztonság**

**Komponens Ellenőrzés:**
   - **Függőség Vizsgálat**: Használjon automatizált sebezhetőség vizsgálatot minden szoftverfüggőséghez és AI komponenshez  
   - **Származás Ellenőrzés**: Ellenőrizze a modellek, adatforrások és külső szolgáltatások eredetét, licencelését és integritását  
   - **Aláírt Csomagok**: Használjon kriptográfiailag aláírt csomagokat, és ellenőrizze az aláírásokat telepítés előtt  

**Biztonságos Fejlesztési Folyamat:**
   - **GitHub Advanced Security**: Valósítson meg titokvizsgálatot, függőség elemzést és CodeQL statikus elemzést  
   - **CI/CD Biztonság**: Integrálja a biztonsági validációt az automatizált telepítési folyamatokba  
   - **Artefakt Integritás**: Valósítson meg kriptográfiai ellenőrzést a telepített artefaktok és konfigurációk számára  

## 7. **OAuth Biztonság és Zavart Helyettesítő Megelőzés**

**OAuth 2.1 Megvalósítás:**
   - **PKCE Megvalósítás**: Használjon Proof Key for Code Exchange (PKCE) minden engedélykéréshez  
   - **Kifejezett Beleegyezés**: Szerezzen felhasználói beleegyezést minden dinamikusan regisztrált klienshez, hogy megakadályozza a zavart helyettesítő támadásokat  
   - **Átirányítás URI Ellenőrzés**: Valósítson meg szigorú ellenőrzést az átirányítási URI-k és kliensazonosítók esetében  

**Proxy Biztonság:**
   - Akadályozza meg az engedélyezési megkerülést statikus kliensazonosító kihasználásával  
   - Valósítson meg megfelelő beleegyezési munkafolyamatokat harmadik fél API hozzáféréshez  
   - Monitorozza az engedélyezési kód lopást és jogosulatlan API hozzáférést  

## 8. **Incidenskezelés és Helyreállítás**

**Gyors Reagálási Képességek:**
   - **Automatizált Reagálás**: Valósítson meg automatizált rendszereket hitelesítő rotációhoz és fenyegetés elhárításhoz  
   - **Visszaállítási Eljárások**: Képesség gyorsan visszaállni ismert-jó konfigurációkra és komponensekre  
   - **Forenzikai Képességek**: Részletes audit nyomvonalak és naplózás incidens vizsgálathoz  

**Kommunikáció és Koordináció:**
   - Egyértelmű eszkalációs eljárások biztonsági incidensekhez  
   - Integráció a szervezeti incidenskezelő csapatokkal  
   - Rendszeres biztonsági incidens szimulációk és gyakorlatok  

## 9. **Megfelelőség és Irányítás**

**Szabályozási Megfelelőség:**
   - Biztosítsa, hogy az MCP implementációk megfeleljenek az iparág-specifikus követelményeknek (GDPR, HIPAA, SOC 2)  
   - Valósítson meg adatbesorolási és adatvédelmi ellenőrzéseket az AI adatfeldolgozáshoz  
   - Tartson átfogó dokumentációt a megfelelőségi auditokhoz  

**Változáskezelés:**
   - Formális biztonsági felülvizsgálati folyamatok minden MCP rendszer módosításhoz  
   - Verziókezelés és jóváhagyási munkafolyamatok konfigurációs változásokhoz  
   - Rendszeres megfelelőségi értékelések és hiányosság elemzések  

## 10. **Fejlett Biztonsági Ellenőrzések**

**Zero Trust Architektúra:**
   - **Soha Ne Bízz, Mindig Ellenőrizd**: Folyamatos ellenőrzés felhasználók, eszközök és kapcsolatok esetében  
   - **Mikroszegmentáció**: Finomhangolt hálózati ellenőrzések, amelyek izolálják az egyes MCP komponenseket  
   - **Feltételes Hozzáférés**: Kockázat-alapú hozzáférés-ellenőrzések, amelyek alkalmazkodnak az aktuális kontextushoz és viselkedéshez  

**Futásidejű Alkalmazás Védelem:**
   - **Futásidejű Alkalmazás Önvédelem (RASP)**: Telepítse a RASP technikákat valós idejű fenyegetés észleléshez  
   - **Alkalmazás Teljesítmény Monitorozás**: Figyelje a teljesítmény anomáliákat, amelyek támadásokat jelezhetnek  
   - **Dinamikus Biztonsági Szabályok**: Valósítson meg biztonsági szabályokat, amelyek alkalmazkodnak az aktuális fenyegetési környezethez  

## 11. **Microsoft Biztonsági Ökoszisztéma Integráció**

**Átfogó Microsoft Biztonság:**
   - **Microsoft Defender for Cloud**: Felhőbiztonsági helyzetkezelés MCP munkaterhelésekhez  
   - **Azure Sentinel**: Felhőalapú SIEM és SOAR képességek fejlett fenyegetés észleléshez  
   - **Microsoft Purview**: Adatirányítás és megfelelőség AI munkafolyamatokhoz és adatforrásokhoz  

**Identitás és Hozzáférés Kezelés:**
   - **Microsoft Entra ID**: Vállalati identitáskezelés feltételes hozzáférési szabályokkal  
   - **Privilegizált Identitáskezelés (PIM)**: Just-in-time hozzáférés és jóváhagyási munkafolyamatok adminisztratív funkciókhoz  
   - **Identitásvédelem**: Kockázat-alapú feltételes hozzáférés és automatizált fenyegetés reagálás  

## 12. **Folyamatos Biztonsági Fejlődés**

**Naprakészség Fenntartása:**
   - **Specifikáció Monitorozás**: Rendszeres áttekintés az MCP specifikáció frissítéseiről és biztonsági útmutatás változásairól  
   - **Fenyegetés Intelligencia**: AI-specifikus fenyegetési hírcsatornák és kompromisszum indikátorok integrációja  
   - **Biztonsági Közösségi Részvétel**: Aktív részvétel az MCP biztonsági közösségben és sebezhetőség bejelentési programokban  

**Adaptív Biztonság:**
   - **Gépi Tanulás Biztonság**: Használjon ML-alapú anomália észlelést új támadási minták azonosítására  
   - **Prediktív Biztonsági Analitika**: Valósítson meg prediktív modelleket proaktív fenyegetés azonosításhoz  
   - **Biztonsági Automatizáció**: Automatizált biztonsági szabályfrissítések fenyegetés intelligencia és specifikáció változások alapján  

---

## **Kritikus Biztonsági Források**

### **Hivatalos MCP Dokumentáció**
- [MCP Specifikáció (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Biztonsági Legjobb Gyakorlatok](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Engedélyezési Specifikáció](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Biztonsági Megoldások**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Biztonság](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Biztonsági Szabványok**
- [OAuth 2.0 Biztonsági Legjobb Gyakorlatok (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc

**Felelősségkizárás**:  
Ez a dokumentum az [Co-op Translator](https://github.com/Azure/co-op-translator) AI fordítási szolgáltatás segítségével készült. Bár törekszünk a pontosságra, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az eredeti nyelvén tekintendő hiteles forrásnak. Kritikus információk esetén javasolt a professzionális, emberi fordítás igénybevétele. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy téves értelmezésekért.