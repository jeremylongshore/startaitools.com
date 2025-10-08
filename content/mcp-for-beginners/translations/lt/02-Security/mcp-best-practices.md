<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-26T19:07:23+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "lt"
}
-->
# MCP saugumo geriausios praktikos 2025

Šis išsamus vadovas apibūdina esmines saugumo geriausias praktikas, skirtas Model Context Protocol (MCP) sistemų įgyvendinimui pagal naujausią **MCP specifikaciją 2025-06-18** ir dabartinius pramonės standartus. Šios praktikos apima tiek tradicinius saugumo aspektus, tiek AI specifines grėsmes, būdingas MCP diegimui.

## Kritiniai saugumo reikalavimai

### Privalomos saugumo kontrolės (MUST reikalavimai)

1. **Tokenų validacija**: MCP serveriai **NETURI** priimti jokių tokenų, kurie nebuvo aiškiai išduoti MCP serveriui
2. **Autorizacijos patikrinimas**: MCP serveriai, įgyvendinantys autorizaciją, **PRIVALO** patikrinti VISUS gaunamus užklausimus ir **NETURI** naudoti sesijų autentifikacijai  
3. **Vartotojo sutikimas**: MCP proxy serveriai, naudojantys statinius klientų ID, **PRIVALO** gauti aiškų vartotojo sutikimą kiekvienam dinamiškai registruotam klientui
4. **Saugūs sesijos ID**: MCP serveriai **PRIVALO** naudoti kriptografiškai saugius, nedeterministinius sesijos ID, generuojamus naudojant saugius atsitiktinių skaičių generatorius

## Pagrindinės saugumo praktikos

### 1. Įvesties validacija ir valymas
- **Išsami įvesties validacija**: Validuokite ir išvalykite visas įvestis, kad išvengtumėte injekcijos atakų, klaidingo delegavimo problemų ir prompt injekcijos pažeidžiamumų
- **Parametrų schemos laikymasis**: Įgyvendinkite griežtą JSON schemos validaciją visiems įrankių parametrams ir API įvestims
- **Turinio filtravimas**: Naudokite Microsoft Prompt Shields ir Azure Content Safety, kad filtruotumėte kenksmingą turinį promptuose ir atsakymuose
- **Išvesties valymas**: Validuokite ir išvalykite visus modelio išvesties duomenis prieš pateikdami juos vartotojams ar kitoms sistemoms

### 2. Autentifikacija ir autorizacija
- **Išoriniai tapatybės tiekėjai**: Deleguokite autentifikaciją patikimiems tapatybės tiekėjams (Microsoft Entra ID, OAuth 2.1 tiekėjai), o ne kurkite savo autentifikacijos sprendimus
- **Smulkios teisės**: Įgyvendinkite detalias, įrankiams specifines teises, laikydamiesi mažiausio privilegijų principo
- **Tokenų gyvavimo ciklo valdymas**: Naudokite trumpalaikius prieigos tokenus su saugiu rotavimu ir tinkamu auditorijos validavimu
- **Daugiafaktorinė autentifikacija**: Reikalaukite MFA visam administraciniam priėjimui ir jautrioms operacijoms

### 3. Saugūs komunikacijos protokolai
- **Transporto sluoksnio saugumas**: Naudokite HTTPS/TLS 1.3 visoms MCP komunikacijoms su tinkamu sertifikatų validavimu
- **End-to-End šifravimas**: Įgyvendinkite papildomus šifravimo sluoksnius itin jautriems duomenims perduodant ir saugant
- **Sertifikatų valdymas**: Užtikrinkite tinkamą sertifikatų gyvavimo ciklo valdymą su automatizuotais atnaujinimo procesais
- **Protokolo versijos laikymasis**: Naudokite dabartinę MCP protokolo versiją (2025-06-18) su tinkamu versijos derinimu

### 4. Pažangus greičio ribojimas ir resursų apsauga
- **Daugiapakopis greičio ribojimas**: Įgyvendinkite greičio ribojimą vartotojo, sesijos, įrankio ir resursų lygmenyse, kad išvengtumėte piktnaudžiavimo
- **Adaptuojamas greičio ribojimas**: Naudokite mašininio mokymosi pagrindu veikiančius greičio ribojimo mechanizmus, kurie prisitaiko prie naudojimo modelių ir grėsmių indikatorių
- **Resursų kvotų valdymas**: Nustatykite tinkamas ribas skaičiavimo resursams, atminties naudojimui ir vykdymo laikui
- **DDoS apsauga**: Diegkite išsamią DDoS apsaugą ir srauto analizės sistemas

### 5. Išsamus logavimas ir stebėjimas
- **Struktūrizuotas audito logavimas**: Įgyvendinkite detalius, paieškos galimybes turinčius logus visoms MCP operacijoms, įrankių vykdymams ir saugumo įvykiams
- **Realaus laiko saugumo stebėjimas**: Diegkite SIEM sistemas su AI pagrindu veikiančia anomalijų detekcija MCP darbo krūviams
- **Privatumo laikymasis loguose**: Loguokite saugumo įvykius, laikydamiesi duomenų privatumo reikalavimų ir reglamentų
- **Incidentų reagavimo integracija**: Jungkite logavimo sistemas su automatizuotais incidentų reagavimo procesais

### 6. Patobulintos saugaus saugojimo praktikos
- **Aparatinės saugumo moduliai**: Naudokite HSM pagrįstą raktų saugojimą (Azure Key Vault, AWS CloudHSM) kritinėms kriptografinėms operacijoms
- **Šifravimo raktų valdymas**: Įgyvendinkite tinkamą raktų rotavimą, atskyrimą ir prieigos kontrolę šifravimo raktams
- **Paslapčių valdymas**: Saugojimo visus API raktus, tokenus ir kredencialus dedikuotose paslapčių valdymo sistemose
- **Duomenų klasifikacija**: Klasifikuokite duomenis pagal jautrumo lygius ir taikykite tinkamas apsaugos priemones

### 7. Pažangus tokenų valdymas
- **Tokenų perdavimo prevencija**: Aiškiai draudžiama tokenų perdavimo modelius, kurie apeina saugumo kontrolę
- **Auditorijos validacija**: Visada tikrinkite, ar tokenų auditorijos teiginiai atitinka numatytą MCP serverio tapatybę
- **Teiginių pagrindu autorizacija**: Įgyvendinkite detalią autorizaciją, pagrįstą tokenų teiginiais ir vartotojų atributais
- **Tokenų susiejimas**: Susiekite tokenus su konkrečiomis sesijomis, vartotojais ar įrenginiais, kur tai tinkama

### 8. Saugus sesijų valdymas
- **Kriptografiniai sesijos ID**: Generuokite sesijos ID, naudodami kriptografiškai saugius atsitiktinių skaičių generatorius (ne nuspėjamas sekas)
- **Vartotojo specifinis susiejimas**: Susiekite sesijos ID su vartotojo specifine informacija, naudodami saugius formatus, pvz., `<user_id>:<session_id>`
- **Sesijos gyvavimo ciklo kontrolė**: Įgyvendinkite tinkamą sesijos galiojimo pabaigą, rotavimą ir panaikinimo mechanizmus
- **Sesijos saugumo antraštės**: Naudokite tinkamas HTTP saugumo antraštes sesijos apsaugai

### 9. AI specifinės saugumo kontrolės
- **Prompt injekcijos gynyba**: Diegkite Microsoft Prompt Shields su apšvietimo, ribotuvų ir duomenų žymėjimo technikomis
- **Įrankių užnuodijimo prevencija**: Validuokite įrankių metaduomenis, stebėkite dinamiškus pokyčius ir tikrinkite įrankių vientisumą
- **Modelio išvesties validacija**: Tikrinkite modelio išvestį dėl galimo duomenų nutekėjimo, kenksmingo turinio ar saugumo politikos pažeidimų
- **Konteksto lango apsauga**: Įgyvendinkite kontrolę, kad išvengtumėte konteksto lango užnuodijimo ir manipuliavimo atakų

### 10. Įrankių vykdymo saugumas
- **Vykdymo izoliacija**: Vykdykite įrankių operacijas konteinerizuotose, izoliuotose aplinkose su resursų ribomis
- **Privilegijų atskyrimas**: Vykdykite įrankius su minimaliomis reikalingomis privilegijomis ir atskirtais paslaugų paskyromis
- **Tinklo izoliacija**: Įgyvendinkite tinklo segmentaciją įrankių vykdymo aplinkoms
- **Vykdymo stebėjimas**: Stebėkite įrankių vykdymą dėl anomalijų, resursų naudojimo ir saugumo pažeidimų

### 11. Nuolatinė saugumo validacija
- **Automatizuotas saugumo testavimas**: Integruokite saugumo testavimą į CI/CD procesus su tokiais įrankiais kaip GitHub Advanced Security
- **Pažeidžiamumų valdymas**: Reguliariai tikrinkite visas priklausomybes, įskaitant AI modelius ir išorines paslaugas
- **Penetracijos testavimas**: Reguliariai vykdykite saugumo vertinimus, specialiai orientuotus į MCP įgyvendinimus
- **Saugumo kodo peržiūros**: Įgyvendinkite privalomas saugumo peržiūras visiems MCP susijusiems kodo pakeitimams

### 12. AI tiekimo grandinės saugumas
- **Komponentų patikrinimas**: Tikrinkite visų AI komponentų (modelių, įterpimų, API) kilmę, vientisumą ir saugumą
- **Priklausomybių valdymas**: Palaikykite dabartinius visų programinės įrangos ir AI priklausomybių inventorius su pažeidžiamumų stebėjimu
- **Patikimi saugyklos**: Naudokite patikrintus, patikimus šaltinius visiems AI modeliams, bibliotekoms ir įrankiams
- **Tiekimo grandinės stebėjimas**: Nuolat stebėkite AI paslaugų tiekėjų ir modelių saugyklų kompromisus

## Pažangūs saugumo modeliai

### Zero Trust architektūra MCP
- **Niekada nepasitikėk, visada tikrink**: Įgyvendinkite nuolatinį visų MCP dalyvių tikrinimą
- **Mikrosegmentacija**: Izoliuokite MCP komponentus su detaliomis tinklo ir tapatybės kontrolėmis
- **Sąlyginė prieiga**: Įgyvendinkite rizika pagrįstas prieigos kontrolės priemones, kurios prisitaiko prie konteksto ir elgsenos
- **Nuolatinis rizikos vertinimas**: Dinamiškai vertinkite saugumo būklę pagal dabartinius grėsmių indikatorius

### Privatumo išsaugojimo AI įgyvendinimas
- **Duomenų minimizavimas**: Atskleiskite tik būtiniausius duomenis kiekvienai MCP operacijai
- **Diferencialinis privatumas**: Įgyvendinkite privatumo išsaugojimo technikas jautrių duomenų apdorojimui
- **Homomorfinis šifravimas**: Naudokite pažangias šifravimo technikas saugiam skaičiavimui su šifruotais duomenimis
- **Federuotas mokymasis**: Įgyvendinkite paskirstytus mokymosi metodus, kurie išsaugo duomenų lokalumą ir privatumą

### Incidentų reagavimas AI sistemoms
- **AI specifinės incidentų procedūros**: Sukurkite incidentų reagavimo procedūras, pritaikytas AI ir MCP specifinėms grėsmėms
- **Automatizuotas reagavimas**: Įgyvendinkite automatizuotą izoliavimą ir problemų sprendimą dažniems AI saugumo incidentams  
- **Teismo ekspertizės galimybės**: Užtikrinkite pasirengimą AI sistemų kompromisams ir duomenų nutekėjimams
- **Atkūrimo procedūros**: Nustatykite procedūras, skirtas atsigauti po AI modelių užnuodijimo, prompt injekcijos atakų ir paslaugų kompromisų

## Įgyvendinimo ištekliai ir standartai

### Oficialūs MCP dokumentai
- [MCP specifikacija 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Dabartinė MCP protokolo specifikacija
- [MCP saugumo geriausios praktikos](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Oficialios saugumo gairės
- [MCP autorizacijos specifikacija](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Autentifikacijos ir autorizacijos modeliai
- [MCP transporto saugumas](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Transporto sluoksnio saugumo reikalavimai

### Microsoft saugumo sprendimai
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Pažangi prompt injekcijos apsauga
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Išsamus AI turinio filtravimas
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Įmonės tapatybės ir prieigos valdymas
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Saugus paslapčių ir kredencialų valdymas
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Tiekimo grandinės ir kodo saugumo tikrinimas

### Saugumo standartai ir struktūros
- [OAuth 2.1 saugumo geriausios praktikos](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Dabartinės OAuth saugumo gairės
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Interneto aplikacijų saugumo rizikos
- [OWASP Top 10 LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI specifinės saugumo rizikos
- [NIST AI rizikos valdymo struktūra](https://www.nist.gov/itl/ai-risk-management-framework) - Išsamus AI rizikos valdymas
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Informacijos saugumo valdymo sistemos

### Įgyvendinimo vadovai ir pamokos
- [Azure API Management kaip MCP autentifikacijos vartai](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Įmonės autentifikacijos modeliai
- [Microsoft Entra ID su MCP serveriais](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Tapatybės tiekėjo integracija
- [Saugaus tokenų saugojimo įgyvendinimas](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Tokenų valdymo geriausios praktikos
- [End-to-End šifravimas AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Pažangūs šifravimo modeliai

### Pažangūs saugumo ištekliai
- [Microsoft saugumo kūrimo ciklas](https://www.microsoft.com/sdl) - Saugios kūrimo praktikos
- [AI Red Team gairės](https://learn.microsoft.com/security/ai-red-team/) - AI specifinis saugumo testavimas
- [Grėsmių modeliavimas AI sistemoms](https://learn.microsoft.com/security/adoption/approach/threats-ai) - AI grėsmių modeliavimo metodologija
- [Privatumo inžinerija AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Privatumo išsaugojimo AI technikos

### Atitiktis ir valdymas
- [GDPR atitiktis AI](https://learn.microsoft.com/com
- **Įrankių kūrimas**: Kurkite ir dalinkitės saugumo įrankiais bei bibliotekomis MCP ekosistemai

---

*Šis dokumentas atspindi MCP saugumo geriausias praktikas, galiojančias 2025 m. rugpjūčio 18 d., remiantis MCP specifikacija 2025-06-18. Saugumo praktikos turėtų būti reguliariai peržiūrimos ir atnaujinamos, atsižvelgiant į protokolo ir grėsmių aplinkos pokyčius.*

---

**Atsakomybės apribojimas**:  
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, atkreipiame dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojama naudoti profesionalų žmogaus vertimą. Mes neprisiimame atsakomybės už nesusipratimus ar klaidingus aiškinimus, kylančius dėl šio vertimo naudojimo.