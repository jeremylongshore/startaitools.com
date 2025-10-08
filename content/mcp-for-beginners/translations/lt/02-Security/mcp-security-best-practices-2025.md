<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-26T19:02:44+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "lt"
}
-->
# MCP saugumo geriausios praktikos – 2025 m. rugpjūčio atnaujinimas

> **Svarbu**: Šis dokumentas atspindi naujausius [MCP specifikacijos 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) saugumo reikalavimus ir oficialias [MCP saugumo geriausias praktikas](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Visada remkitės dabartine specifikacija, kad gautumėte naujausią informaciją.

## Esminės saugumo praktikos MCP įgyvendinimui

Modelio konteksto protokolas kelia unikalius saugumo iššūkius, kurie viršija tradicinio programinės įrangos saugumo ribas. Šios praktikos apima tiek pagrindinius saugumo reikalavimus, tiek MCP specifines grėsmes, tokias kaip komandų injekcija, įrankių užnuodijimas, sesijos užgrobimas, klaidingo atstovo problemos ir žetonų perdavimo pažeidžiamumai.

### **PRIVALOMI saugumo reikalavimai**

**Kritiški MCP specifikacijos reikalavimai:**

> **NEGALI**: MCP serveriai **NEGALI** priimti jokių žetonų, kurie nebuvo aiškiai išduoti MCP serveriui  
> 
> **PRIVALOMA**: MCP serveriai, įgyvendinantys autorizaciją, **PRIVALOMA** patikrinti VISUS gaunamus užklausimus  
>  
> **NEGALI**: MCP serveriai **NEGALI** naudoti sesijų autentifikacijai  
>
> **PRIVALOMA**: MCP proxy serveriai, naudojantys statinius klientų ID, **PRIVALOMA** gauti vartotojo sutikimą kiekvienam dinamiškai registruotam klientui  

---

## 1. **Žetonų saugumas ir autentifikacija**

**Autentifikacijos ir autorizacijos kontrolė:**
   - **Griežta autorizacijos peržiūra**: Atlikite išsamias MCP serverio autorizacijos logikos auditus, kad užtikrintumėte, jog tik numatyti vartotojai ir klientai gali pasiekti išteklius  
   - **Išorinių tapatybės tiekėjų integracija**: Naudokite patikimus tapatybės tiekėjus, tokius kaip Microsoft Entra ID, vietoj individualios autentifikacijos kūrimo  
   - **Žetonų auditorijos patikra**: Visada patikrinkite, ar žetonai buvo aiškiai išduoti jūsų MCP serveriui – niekada nepriimkite aukštesnio lygio žetonų  
   - **Tinkamas žetonų gyvavimo ciklas**: Įgyvendinkite saugų žetonų rotavimą, galiojimo politiką ir užkirsti kelią žetonų pakartotiniam naudojimui  

**Apsaugotas žetonų saugojimas:**
   - Naudokite Azure Key Vault ar panašias saugių kredencialų saugyklas visiems slaptažodžiams  
   - Įgyvendinkite žetonų šifravimą tiek saugojimo metu, tiek perduodant  
   - Reguliariai rotuokite kredencialus ir stebėkite neleistiną prieigą  

## 2. **Sesijų valdymas ir transporto saugumas**

**Saugios sesijos praktikos:**
   - **Kriptografiškai saugūs sesijos ID**: Naudokite saugius, nedeterministinius sesijos ID, generuojamus naudojant saugius atsitiktinių skaičių generatorius  
   - **Vartotojo specifinis susiejimas**: Susiekite sesijos ID su vartotojo tapatybėmis, naudodami formatus, pvz., `<user_id>:<session_id>`, kad išvengtumėte sesijos piktnaudžiavimo tarp vartotojų  
   - **Sesijos gyvavimo ciklo valdymas**: Įgyvendinkite tinkamą galiojimo, rotavimo ir panaikinimo politiką, kad sumažintumėte pažeidžiamumo langus  
   - **HTTPS/TLS privalomumas**: Privalomas HTTPS visam ryšiui, kad būtų išvengta sesijos ID perėmimo  

**Transporto sluoksnio saugumas:**
   - Konfigūruokite TLS 1.3, kur įmanoma, su tinkamu sertifikatų valdymu  
   - Įgyvendinkite sertifikatų fiksavimą kritiniams ryšiams  
   - Reguliariai rotuokite sertifikatus ir tikrinkite jų galiojimą  

## 3. **AI specifinių grėsmių apsauga** 🤖

**Komandų injekcijos apsauga:**
   - **Microsoft Prompt Shields**: Naudokite AI Prompt Shields pažangiam kenksmingų instrukcijų aptikimui ir filtravimui  
   - **Įvesties valymas**: Patikrinkite ir išvalykite visas įvestis, kad išvengtumėte injekcijos atakų ir klaidingo atstovo problemų  
   - **Turinio ribos**: Naudokite ribotuvus ir duomenų žymėjimo sistemas, kad atskirtumėte patikimas instrukcijas nuo išorinio turinio  

**Įrankių užnuodijimo prevencija:**
   - **Įrankių metaduomenų patikra**: Įgyvendinkite įrankių apibrėžimų vientisumo patikras ir stebėkite netikėtus pokyčius  
   - **Dinaminis įrankių stebėjimas**: Stebėkite vykdymo elgesį ir nustatykite įspėjimus dėl netikėtų vykdymo modelių  
   - **Patvirtinimo darbo eiga**: Reikalaukite aiškaus vartotojo patvirtinimo dėl įrankių pakeitimų ir funkcijų pokyčių  

## 4. **Prieigos kontrolė ir leidimai**

**Mažiausio privilegijos principas:**
   - Suteikite MCP serveriams tik minimalias reikalingas leidimus numatytai funkcijai  
   - Įgyvendinkite vaidmenimis pagrįstą prieigos kontrolę (RBAC) su smulkiomis leidimų detalėmis  
   - Reguliariai peržiūrėkite leidimus ir nuolat stebėkite privilegijų eskalaciją  

**Leidimų kontrolė vykdymo metu:**
   - Taikykite išteklių apribojimus, kad išvengtumėte išteklių išsekimo atakų  
   - Naudokite konteinerių izoliaciją įrankių vykdymo aplinkoms  
   - Įgyvendinkite laiku suteikiamą prieigą administracinėms funkcijoms  

## 5. **Turinio saugumas ir stebėjimas**

**Turinio saugumo įgyvendinimas:**
   - **Azure turinio saugumo integracija**: Naudokite Azure turinio saugumą kenksmingo turinio, jailbreak bandymų ir politikos pažeidimų aptikimui  
   - **Elgesio analizė**: Įgyvendinkite vykdymo elgesio stebėjimą, kad aptiktumėte anomalijas MCP serverio ir įrankių vykdyme  
   - **Išsamus žurnalinimas**: Žurnalizuokite visus autentifikacijos bandymus, įrankių iškvietimus ir saugumo įvykius saugioje, nekeičiamoje saugykloje  

**Nuolatinis stebėjimas:**
   - Realaus laiko įspėjimai dėl įtartinų modelių ir neleistinų prieigos bandymų  
   - Integracija su SIEM sistemomis centralizuotam saugumo įvykių valdymui  
   - Reguliarūs saugumo auditai ir MCP įgyvendinimų įsiskverbimo testavimas  

## 6. **Tiekimo grandinės saugumas**

**Komponentų patikra:**
   - **Priklausomybių skenavimas**: Naudokite automatizuotą pažeidžiamumų skenavimą visoms programinės įrangos priklausomybėms ir AI komponentams  
   - **Kilmės patikra**: Patikrinkite modelių, duomenų šaltinių ir išorinių paslaugų kilmę, licencijavimą ir vientisumą  
   - **Pasirašyti paketai**: Naudokite kriptografiškai pasirašytus paketus ir patikrinkite parašus prieš diegimą  

**Saugus kūrimo procesas:**
   - **GitHub Advanced Security**: Įgyvendinkite slaptažodžių skenavimą, priklausomybių analizę ir CodeQL statinę analizę  
   - **CI/CD saugumas**: Integruokite saugumo patikras visame automatizuotų diegimo procesų cikle  
   - **Artefaktų vientisumas**: Įgyvendinkite kriptografinę diegiamų artefaktų ir konfigūracijų patikrą  

## 7. **OAuth saugumas ir klaidingo atstovo prevencija**

**OAuth 2.1 įgyvendinimas:**
   - **PKCE įgyvendinimas**: Naudokite Proof Key for Code Exchange (PKCE) visoms autorizacijos užklausoms  
   - **Aiškus sutikimas**: Gaukite vartotojo sutikimą kiekvienam dinamiškai registruotam klientui, kad išvengtumėte klaidingo atstovo atakų  
   - **Peradresavimo URI patikra**: Įgyvendinkite griežtą peradresavimo URI ir klientų identifikatorių patikrą  

**Proxy saugumas:**
   - Užkirsti kelią autorizacijos apeigoms per statinių klientų ID išnaudojimą  
   - Įgyvendinkite tinkamas sutikimo darbo eigas trečiųjų šalių API prieigai  
   - Stebėkite autorizacijos kodų vagystes ir neleistiną API prieigą  

## 8. **Incidentų valdymas ir atkūrimas**

**Greito reagavimo galimybės:**
   - **Automatizuotas reagavimas**: Įgyvendinkite automatizuotas sistemas kredencialų rotavimui ir grėsmių suvaldymui  
   - **Atstatymo procedūros**: Galimybė greitai grįžti prie patikrintų konfigūracijų ir komponentų  
   - **Teismo ekspertizės galimybės**: Išsamūs audito pėdsakai ir žurnalai incidentų tyrimui  

**Komunikacija ir koordinavimas:**
   - Aiškios eskalavimo procedūros saugumo incidentams  
   - Integracija su organizacijos incidentų valdymo komandomis  
   - Reguliarios saugumo incidentų simuliacijos ir praktiniai pratimai  

## 9. **Atitiktis ir valdymas**

**Reguliacinė atitiktis:**
   - Užtikrinkite, kad MCP įgyvendinimai atitiktų pramonės specifinius reikalavimus (GDPR, HIPAA, SOC 2)  
   - Įgyvendinkite duomenų klasifikavimo ir privatumo kontrolę AI duomenų apdorojimui  
   - Išlaikykite išsamią dokumentaciją atitikties auditui  

**Pakeitimų valdymas:**
   - Formalūs saugumo peržiūros procesai visiems MCP sistemos pakeitimams  
   - Versijų kontrolė ir patvirtinimo darbo eiga konfigūracijų pakeitimams  
   - Reguliarūs atitikties vertinimai ir spragų analizė  

## 10. **Pažangios saugumo kontrolės**

**Zero Trust architektūra:**
   - **Niekada nepasitikėk, visada tikrink**: Nuolatinis vartotojų, įrenginių ir ryšių tikrinimas  
   - **Mikrosegmentacija**: Smulkios tinklo kontrolės, izoliuojančios atskirus MCP komponentus  
   - **Sąlyginė prieiga**: Rizika pagrįsta prieigos kontrolė, prisitaikanti prie dabartinio konteksto ir elgesio  

**Vykdymo apsauga:**
   - **Runtime Application Self-Protection (RASP)**: Naudokite RASP technikas realaus laiko grėsmių aptikimui  
   - **Programų našumo stebėjimas**: Stebėkite našumo anomalijas, kurios gali rodyti atakas  
   - **Dinaminės saugumo politikos**: Įgyvendinkite saugumo politikas, prisitaikančias prie dabartinio grėsmių kraštovaizdžio  

## 11. **Microsoft saugumo ekosistemos integracija**

**Išsamus Microsoft saugumas:**
   - **Microsoft Defender for Cloud**: Debesų saugumo būklės valdymas MCP darbo krūviams  
   - **Azure Sentinel**: Debesų gimtoji SIEM ir SOAR galimybės pažangiam grėsmių aptikimui  
   - **Microsoft Purview**: Duomenų valdymas ir atitiktis AI darbo eigoms ir duomenų šaltiniams  

**Tapatybės ir prieigos valdymas:**
   - **Microsoft Entra ID**: Įmonės tapatybės valdymas su sąlyginės prieigos politikomis  
   - **Privileged Identity Management (PIM)**: Laiku suteikiama prieiga ir patvirtinimo darbo eiga administracinėms funkcijoms  
   - **Tapatybės apsauga**: Rizika pagrįsta sąlyginė prieiga ir automatizuotas grėsmių reagavimas  

## 12. **Nuolatinė saugumo evoliucija**

**Buvimas aktualiu:**
   - **Specifikacijos stebėjimas**: Reguliarus MCP specifikacijos atnaujinimų ir saugumo gairių pokyčių peržiūra  
   - **Grėsmių žvalgyba**: AI specifinių grėsmių srautų ir kompromisų indikatorių integracija  
   - **Saugumo bendruomenės dalyvavimas**: Aktyvus dalyvavimas MCP saugumo bendruomenėje ir pažeidžiamumų atskleidimo programose  

**Prisitaikantis saugumas:**
   - **Mašininio mokymosi saugumas**: Naudokite ML pagrįstą anomalijų aptikimą naujų atakų modelių identifikavimui  
   - **Prognozuojamoji saugumo analizė**: Įgyvendinkite prognozuojamus modelius, skirtus proaktyviam grėsmių identifikavimui  
   - **Saugumo automatizavimas**: Automatizuoti saugumo politikos atnaujinimai, remiantis grėsmių žvalgyba ir specifikacijos pokyčiais  

---

## **Kritiški saugumo ištekliai**

### **Oficiali MCP dokumentacija**
- [MCP specifikacija (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP saugumo geriausios praktikos](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP autorizacijos specifikacija](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft saugumo sprendimai**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure turinio saugumas](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID saugumas](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Saugumo standartai**
- [OAuth 2.0 saugumo geriausios praktikos (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 dideliems kalbos modeliams](https://genai.owasp.org/)  
- [NIST AI rizikos valdymo sistema](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Įgyvendinimo vadovai**
- [Azure API Management MCP autentifikacijos vartai](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID su MCP serveriais](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Saugumo pranešimas**: MCP saugumo praktikos greitai evoliucionuoja. Visada patikrinkite dabartinę [MCP specifikaciją](https://spec.modelcontextprotocol.io/) ir [oficialią saugumo dokumentaciją](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) prieš įgyvendinimą.

---

**Atsakomybės apribojimas**:  
Šis dokumentas buvo išverstas naudojant AI vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojama naudoti profesionalų žmogaus vertimą. Mes neprisiimame atsakomybės už nesusipratimus ar klaidingus interpretavimus, atsiradusius dėl šio vertimo naudojimo.