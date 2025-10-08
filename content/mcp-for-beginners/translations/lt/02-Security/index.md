<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-26T19:04:49+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "lt"
}
-->
# MCP Saugumas: Išsamus AI sistemų apsaugos vadovas

[![MCP Saugumo Geriausios Praktikos](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.lt.png)](https://youtu.be/88No8pw706o)

_(Spustelėkite paveikslėlį aukščiau, kad peržiūrėtumėte šios pamokos vaizdo įrašą)_

Saugumas yra esminis AI sistemų projektavimo elementas, todėl mes jį laikome prioritetu antrame skyriuje. Tai atitinka „Microsoft“ principą **Saugumas pagal dizainą** iš [Saugios ateities iniciatyvos](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Modelio konteksto protokolas (MCP) suteikia naujų galingų galimybių AI pagrįstoms programoms, tačiau kartu kelia unikalius saugumo iššūkius, kurie viršija tradicinės programinės įrangos rizikas. MCP sistemos susiduria tiek su įprastais saugumo klausimais (saugus kodavimas, minimalūs leidimai, tiekimo grandinės saugumas), tiek su naujomis AI specifinėmis grėsmėmis, tokiomis kaip komandų injekcija, įrankių užnuodijimas, sesijos užgrobimas, klaidingo atstovo atakos, žetonų perdavimo pažeidžiamumai ir dinaminis galimybių keitimas.

Šioje pamokoje aptariamos svarbiausios saugumo rizikos MCP įgyvendinimuose—autentifikacija, autorizacija, per dideli leidimai, netiesioginė komandų injekcija, sesijos saugumas, klaidingo atstovo problemos, žetonų valdymas ir tiekimo grandinės pažeidžiamumai. Sužinosite praktinius kontrolės metodus ir geriausias praktikas, kaip sumažinti šias rizikas, pasitelkiant „Microsoft“ sprendimus, tokius kaip „Prompt Shields“, „Azure Content Safety“ ir „GitHub Advanced Security“, kad sustiprintumėte savo MCP diegimą.

## Mokymosi tikslai

Pamokos pabaigoje galėsite:

- **Atpažinti MCP specifines grėsmes**: Suprasti unikalius saugumo pavojus MCP sistemose, įskaitant komandų injekciją, įrankių užnuodijimą, per didelius leidimus, sesijos užgrobimą, klaidingo atstovo problemas, žetonų perdavimo pažeidžiamumus ir tiekimo grandinės rizikas
- **Taikyti saugumo kontrolės priemones**: Įgyvendinti veiksmingas priemones, tokias kaip patikima autentifikacija, minimalūs leidimai, saugus žetonų valdymas, sesijos saugumo kontrolė ir tiekimo grandinės patikrinimas
- **Pasinaudoti „Microsoft“ saugumo sprendimais**: Suprasti ir pritaikyti „Microsoft Prompt Shields“, „Azure Content Safety“ ir „GitHub Advanced Security“ MCP darbo krūvio apsaugai
- **Patikrinti įrankių saugumą**: Suprasti įrankių metaduomenų patikrinimo svarbą, stebėti dinaminius pokyčius ir apsisaugoti nuo netiesioginių komandų injekcijos atakų
- **Integruoti geriausias praktikas**: Derinti įprastus saugumo pagrindus (saugus kodavimas, serverių stiprinimas, nulinio pasitikėjimo principas) su MCP specifinėmis kontrolės priemonėmis, kad užtikrintumėte visapusišką apsaugą

# MCP Saugumo architektūra ir kontrolės priemonės

Šiuolaikiniai MCP įgyvendinimai reikalauja sluoksniuoto saugumo požiūrio, kuris apima tiek tradicinės programinės įrangos saugumą, tiek AI specifines grėsmes. Greitai besivystanti MCP specifikacija toliau tobulina savo saugumo kontrolės priemones, leidžiančias geriau integruotis su įmonių saugumo architektūromis ir nusistovėjusiomis geriausiomis praktikomis.

Tyrimai iš [Microsoft Digital Defense Report](https://aka.ms/mddr) rodo, kad **98% praneštų pažeidimų būtų galima išvengti taikant tinkamą saugumo higieną**. Efektyviausia apsaugos strategija derina pagrindines saugumo praktikas su MCP specifinėmis kontrolės priemonėmis—patikrintos bazinės saugumo priemonės išlieka pačios veiksmingiausios mažinant bendrą saugumo riziką.

## Dabartinė saugumo situacija

> **Pastaba:** Ši informacija atspindi MCP saugumo standartus, galiojančius **2025 m. rugpjūčio 18 d.** MCP protokolas greitai vystosi, o būsimi įgyvendinimai gali pristatyti naujus autentifikacijos modelius ir patobulintas kontrolės priemones. Visada remkitės dabartine [MCP specifikacija](https://spec.modelcontextprotocol.io/), [MCP GitHub saugykla](https://github.com/modelcontextprotocol) ir [saugumo geriausių praktikų dokumentacija](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices), kad gautumėte naujausią informaciją.

### MCP autentifikacijos evoliucija

MCP specifikacija reikšmingai pasikeitė savo požiūriu į autentifikaciją ir autorizaciją:

- **Pradinis požiūris**: Ankstyvos specifikacijos reikalavo, kad kūrėjai įgyvendintų individualius autentifikacijos serverius, o MCP serveriai veiktų kaip OAuth 2.0 autorizacijos serveriai, tiesiogiai valdantys vartotojų autentifikaciją
- **Dabartinis standartas (2025-06-18)**: Atnaujinta specifikacija leidžia MCP serveriams deleguoti autentifikaciją išoriniams tapatybės tiekėjams (pvz., „Microsoft Entra ID“), gerinant saugumo lygį ir mažinant įgyvendinimo sudėtingumą
- **Transporto sluoksnio saugumas**: Patobulinta saugių transporto mechanizmų palaikymas su tinkamais autentifikacijos modeliais tiek vietiniams (STDIO), tiek nuotoliniams (Streamable HTTP) ryšiams

## Autentifikacijos ir autorizacijos saugumas

### Dabartiniai saugumo iššūkiai

Šiuolaikiniai MCP įgyvendinimai susiduria su keliais autentifikacijos ir autorizacijos iššūkiais:

### Rizikos ir grėsmių vektoriai

- **Netinkamai sukonfigūruota autorizacijos logika**: Klaidingas autorizacijos įgyvendinimas MCP serveriuose gali atskleisti jautrius duomenis ir neteisingai taikyti prieigos kontrolę
- **OAuth žetonų kompromitavimas**: Vietinių MCP serverių žetonų vagystė leidžia užpuolikams apsimesti serveriais ir pasiekti paslaugas
- **Žetonų perdavimo pažeidžiamumai**: Netinkamas žetonų tvarkymas sukuria saugumo kontrolės apėjimus ir atsakomybės spragas
- **Per dideli leidimai**: Per daug privilegijuoti MCP serveriai pažeidžia minimalios prieigos principus ir padidina atakos paviršių

#### Žetonų perdavimas: Kritinis anti-modelis

**Žetonų perdavimas yra griežtai draudžiamas** dabartinėje MCP autorizacijos specifikacijoje dėl rimtų saugumo pasekmių:

##### Saugumo kontrolės apėjimas
- MCP serveriai ir žemyniniai API įgyvendina svarbias saugumo kontrolės priemones (užklausų ribojimas, užklausų validacija, srauto stebėjimas), kurios priklauso nuo tinkamo žetonų validavimo
- Tiesioginis klientų ir API žetonų naudojimas apeina šias esmines apsaugos priemones, silpnindamas saugumo architektūrą

##### Atsakomybės ir audito iššūkiai  
- MCP serveriai negali atskirti klientų, naudojančių aukštyn išduotus žetonus, todėl audito pėdsakai tampa neaiškūs
- Žemyninių resursų serverių žurnalai rodo klaidingą užklausų kilmę, o ne tikruosius MCP serverių tarpininkus
- Incidentų tyrimas ir atitikties auditas tampa žymiai sudėtingesni

##### Duomenų nutekėjimo rizika
- Nevaliduoti žetonų teiginiai leidžia piktybiniams veikėjams su pavogtais žetonais naudoti MCP serverius kaip tarpininkus duomenų nutekėjimui
- Pasitikėjimo ribų pažeidimai leidžia neteisėtus prieigos modelius, kurie apeina numatytas saugumo kontrolės priemones

##### Daugiapaslaugės atakos vektoriai
- Kompromituoti žetonai, priimami keliose paslaugose, leidžia šoninius judesius per susijusias sistemas
- Pasitikėjimo prielaidos tarp paslaugų gali būti pažeistos, kai žetonų kilmė negali būti patvirtinta

### Saugumo kontrolės priemonės ir mažinimo strategijos

**Esminiai saugumo reikalavimai:**

> **PRIVALOMA**: MCP serveriai **NETURI** priimti jokių žetonų, kurie nebuvo aiškiai išduoti MCP serveriui

#### Autentifikacijos ir autorizacijos kontrolės priemonės

- **Griežta autorizacijos peržiūra**: Atlikite išsamias MCP serverių autorizacijos logikos auditus, kad užtikrintumėte, jog tik numatyti vartotojai ir klientai gali pasiekti jautrius resursus
  - **Įgyvendinimo vadovas**: [Azure API valdymas kaip autentifikacijos vartai MCP serveriams](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Tapatybės integracija**: [Microsoft Entra ID naudojimas MCP serverių autentifikacijai](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Saugus žetonų valdymas**: Įgyvendinkite [Microsoft žetonų validavimo ir gyvavimo ciklo geriausias praktikas](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Patikrinkite, ar žetonų auditorijos teiginiai atitinka MCP serverio tapatybę
  - Įgyvendinkite tinkamą žetonų rotaciją ir galiojimo politiką
  - Užkirsti kelią žetonų pakartotiniam naudojimui ir neteisėtam naudojimui

- **Apsaugotas žetonų saugojimas**: Užtikrinkite žetonų saugojimą su šifravimu tiek ramybės būsenoje, tiek perduodant
  - **Geriausios praktikos**: [Saugus žetonų saugojimas ir šifravimo gairės](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Prieigos kontrolės įgyvendinimas

- **Minimalios prieigos principas**: Suteikite MCP serveriams tik minimalias privilegijas, reikalingas numatytai funkcijai
  - Reguliarūs leidimų peržiūros ir atnaujinimai, kad būtų išvengta privilegijų kaupimosi
  - **Microsoft dokumentacija**: [Saugus minimalios prieigos valdymas](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Prieigos kontrolė pagal vaidmenis (RBAC)**: Įgyvendinkite smulkiai apibrėžtus vaidmenų priskyrimus
  - Vaidmenis apribokite konkrečiais resursais ir veiksmais
  - Venkite plačių ar nereikalingų leidimų, kurie padidina atakos paviršių

- **Nuolatinis leidimų stebėjimas**: Įgyvendinkite nuolatinį prieigos auditą ir stebėjimą
  - Stebėkite leidimų naudojimo modelius, kad aptiktumėte anomalijas
  - Nedelsiant pašalinkite per dideles ar nenaudojamas privilegijas

## AI specifinės saugumo grėsmės

### Komandų injekcija ir įrankių manipuliavimo atakos

Šiuolaikiniai MCP įgyvendinimai susiduria su sudėtingais AI specifiniais atakos vektoriais, kurių tradicinės saugumo priemonės negali visiškai spręsti:

#### **Netiesioginė komandų injekcija (kryžminio domeno komandų injekcija)**

**Netiesioginė komandų injekcija** yra viena iš kritinių pažeidžiamumų MCP pagrįstose AI sistemose. Užpuolikai įterpia piktybines instrukcijas į išorinį turinį—dokumentus, tinklalapius, el. laiškus ar duomenų šaltinius—kurį AI sistemos vėliau apdoroja kaip teisėtus nurodymus.

**Atakos scenarijai:**
- **Dokumentų pagrindu vykdoma injekcija**: Piktybinės instrukcijos, paslėptos apdorojamuose dokumentuose, kurios sukelia nepageidaujamus AI veiksmus
- **Tinklalapių turinio išnaudojimas**: Kompromituoti tinklalapiai su įterptais nurodymais, kurie manipuliuoja AI elgesiu, kai yra nuskaityti
- **El. laiškų pagrindu vykdomos atakos**: Piktybinės instrukcijos el. laiškuose, kurios priverčia AI asistentus nutekinti informaciją arba atlikti neteisėtus veiksmus
- **Duomenų šaltinių užteršimas**: Kompromituotos duomenų bazės ar API, teikiančios užnuodytą turinį AI sistemoms

**Reali pasaulio įtaka**: Šios atakos gali sukelti duomenų nutekėjimą, privatumo pažeidimus, kenksmingo turinio generavimą ir vartotojų sąveikos manipuliavimą. Išsamią analizę rasite [Komandų injekcija MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Komandų injekcijos atakos diagrama](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.lt.png)

#### **Įrankių užnuodijimo atakos**

**Įrankių užnuodijimas** taikosi į metaduomenis, apibrėžiančius MCP įrankius, išnaudodamas tai, kaip LLM interpretuoja įrankių aprašymus ir parametrus, kad priimtų vykdymo sprendimus.

**Atakos mechanizmai:**
- **Metaduomenų manipuliavimas**: Užpuolikai įterpia piktybines instrukcijas į įrankių aprašymus, parametrų apibrėžimus ar naudojimo pavyzdžius
- **Nematomos instrukcijos**: Paslėptos instrukcijos įrankių metaduomenyse, kurias apdoroja AI modeliai, bet kurios nematomos žmonėms
- **Dinaminis įrankių keitimas („Rug Pulls“) **: Vartotojų patvirtinti įrankiai vėliau modifikuojami, kad atliktų piktybinius veiksmus be vartotojo žinios
- **Parametrų injekcija**: Piktybinis turinys, įterptas į įrankių parametrų schemas, kuris daro įtaką modelio elgesiui

**Nuotolinių serverių rizika**: Nuotoliniai MCP serveriai kelia didesnę riziką, nes įrankių apibrėžimai gali būti atnaujinti po pradinio vartotojo patvirtinimo, sukuriant scenarijus, kai anksčiau saugūs įrankiai tampa piktybiniais. Išsamią analizę rasite [Įrankių užnuodijimo atakos (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Įrankių injekcijos atakos diagrama](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.lt.png)

#### **Papildomi AI atakos vektoriai**

- **Kryžminio domeno komandų injekcija (XPIA)**: Sudėtingos atakos, kurios naudoja turinį iš kelių domenų, kad apeitų saugumo kontrolės priemones
- **Dinaminis galimybių keitimas**: Realiojo laiko įrankių galimybių pakeitimai, kurie išvengia pradinio saugumo vertinimo
- **Konteksto lango užteršimas**: Atakos, kurios
- **Saugus sesijos generavimas**: Naudokite kriptografiškai saugius, nedeterministinius sesijos ID, generuojamus su saugiais atsitiktinių skaičių generatoriais  
- **Vartotojui pritaikytas susiejimas**: Susiekite sesijos ID su vartotojo specifine informacija, naudodami formatus, pvz., `<user_id>:<session_id>`, kad išvengtumėte sesijų piktnaudžiavimo tarp vartotojų  
- **Sesijos gyvavimo ciklo valdymas**: Įgyvendinkite tinkamą galiojimo pabaigą, rotaciją ir anuliavimą, kad sumažintumėte pažeidžiamumo langus  
- **Transporto saugumas**: Privalomas HTTPS visai komunikacijai, kad būtų išvengta sesijos ID perėmimo  

### Supainioto tarpininko problema  

**Supainioto tarpininko problema** atsiranda, kai MCP serveriai veikia kaip autentifikavimo tarpininkai tarp klientų ir trečiųjų šalių paslaugų, sudarydami galimybes apeiti autorizaciją, naudojant statinius kliento ID.  

#### **Atakos mechanizmai ir rizikos**  

- **Slapukais pagrįsto sutikimo apeitis**: Ankstesnis vartotojo autentifikavimas sukuria sutikimo slapukus, kuriuos užpuolikai išnaudoja, pateikdami kenkėjiškus autorizacijos užklausas su suklastotais peradresavimo URI  
- **Autorizacijos kodo vagystė**: Esami sutikimo slapukai gali priversti autorizacijos serverius praleisti sutikimo ekranus, nukreipiant kodus į užpuoliko valdomus galinius taškus  
- **Neleistina API prieiga**: Pavogti autorizacijos kodai leidžia keistis žetonais ir apsimesti vartotoju be aiškaus patvirtinimo  

#### **Švelninimo strategijos**  

**Privalomos kontrolės:**  
- **Aiškūs sutikimo reikalavimai**: MCP tarpiniai serveriai, naudojantys statinius kliento ID, **PRIVALĖTŲ** gauti vartotojo sutikimą kiekvienam dinamiškai registruotam klientui  
- **OAuth 2.1 saugumo įgyvendinimas**: Laikykitės dabartinių OAuth saugumo geriausių praktikų, įskaitant PKCE (Proof Key for Code Exchange) visoms autorizacijos užklausoms  
- **Griežtas kliento tikrinimas**: Įgyvendinkite griežtą peradresavimo URI ir kliento identifikatorių tikrinimą, kad išvengtumėte išnaudojimo  

### Žetonų perdavimo pažeidžiamumai  

**Žetonų perdavimas** yra aiškus antipatternas, kai MCP serveriai priima kliento žetonus be tinkamo patikrinimo ir perduoda juos žemyn esančioms API, pažeisdami MCP autorizacijos specifikacijas.  

#### **Saugumo pasekmės**  

- **Kontrolės apeitis**: Tiesioginis kliento ir API žetonų naudojimas apeina svarbias greičio ribojimo, tikrinimo ir stebėjimo kontrolės priemones  
- **Audito pėdsakų sugadinimas**: Aukštesnio lygio išduoti žetonai neleidžia identifikuoti kliento, trukdant incidentų tyrimams  
- **Tarpinio serverio duomenų nutekėjimas**: Nepatikrinti žetonai leidžia kenkėjiškiems veikėjams naudoti serverius kaip tarpininkus neleistinai prieigai prie duomenų  
- **Pasitikėjimo ribų pažeidimai**: Žemyn esančių paslaugų pasitikėjimo prielaidos gali būti pažeistos, kai negalima patikrinti žetonų kilmės  
- **Daugiapaslaugės atakos plėtra**: Kompromituoti žetonai, priimami keliose paslaugose, leidžia judėti šoniniu būdu  

#### **Reikalingos saugumo kontrolės**  

**Nesiderėtini reikalavimai:**  
- **Žetonų tikrinimas**: MCP serveriai **NETURI** priimti žetonų, kurie nėra aiškiai išduoti MCP serveriui  
- **Auditorijos patikrinimas**: Visada tikrinkite, ar žetonų auditorijos teiginiai atitinka MCP serverio tapatybę  
- **Tinkamas žetonų gyvavimo ciklas**: Įgyvendinkite trumpalaikius prieigos žetonus su saugiomis rotacijos praktikomis  

## Tiekimo grandinės saugumas AI sistemoms  

Tiekimo grandinės saugumas išsiplėtė už tradicinių programinės įrangos priklausomybių ribų, apimdamas visą AI ekosistemą. Modernios MCP įgyvendinimo priemonės turi griežtai tikrinti ir stebėti visus su AI susijusius komponentus, nes kiekvienas iš jų gali sukelti pažeidžiamumų, galinčių pakenkti sistemos vientisumui.  

### Išplėstiniai AI tiekimo grandinės komponentai  

**Tradicinės programinės įrangos priklausomybės:**  
- Atvirojo kodo bibliotekos ir karkasai  
- Konteinerių atvaizdai ir bazinės sistemos  
- Kūrimo įrankiai ir kūrimo vamzdynai  
- Infrastruktūros komponentai ir paslaugos  

**AI specifiniai tiekimo grandinės elementai:**  
- **Pagrindiniai modeliai**: Iš anksto apmokyti modeliai iš įvairių tiekėjų, kuriems reikalingas kilmės patikrinimas  
- **Įterpimo paslaugos**: Išorinės vektorizacijos ir semantinės paieškos paslaugos  
- **Konteksto teikėjai**: Duomenų šaltiniai, žinių bazės ir dokumentų saugyklos  
- **Trečiųjų šalių API**: Išorinės AI paslaugos, ML vamzdynai ir duomenų apdorojimo galiniai taškai  
- **Modelio artefaktai**: Svoris, konfigūracijos ir pritaikyti modelio variantai  
- **Mokymo duomenų šaltiniai**: Duomenų rinkiniai, naudojami modelio mokymui ir pritaikymui  

### Išsami tiekimo grandinės saugumo strategija  

#### **Komponentų tikrinimas ir pasitikėjimas**  
- **Kilmės patikrinimas**: Patikrinkite visų AI komponentų kilmę, licencijavimą ir vientisumą prieš integraciją  
- **Saugumo vertinimas**: Atlikite pažeidžiamumo skenavimus ir saugumo peržiūras modeliams, duomenų šaltiniams ir AI paslaugoms  
- **Reputacijos analizė**: Įvertinkite AI paslaugų teikėjų saugumo istoriją ir praktiką  
- **Atitikties patikrinimas**: Užtikrinkite, kad visi komponentai atitiktų organizacijos saugumo ir reguliavimo reikalavimus  

#### **Saugios diegimo linijos**  
- **Automatizuotas CI/CD saugumas**: Integruokite saugumo skenavimą visoje automatizuoto diegimo linijoje  
- **Artefaktų vientisumas**: Įgyvendinkite kriptografinį visų diegiamų artefaktų (kodo, modelių, konfigūracijų) patikrinimą  
- **Etapinis diegimas**: Naudokite progresyvaus diegimo strategijas su saugumo patikrinimu kiekviename etape  
- **Patikimos artefaktų saugyklos**: Diekite tik iš patikrintų, saugių artefaktų registrų ir saugyklų  

#### **Nuolatinis stebėjimas ir reagavimas**  
- **Priklausomybių skenavimas**: Nuolatinis pažeidžiamumo stebėjimas visoms programinės įrangos ir AI komponentų priklausomybėms  
- **Modelio stebėjimas**: Nuolatinis modelio elgsenos, našumo nukrypimų ir saugumo anomalijų vertinimas  
- **Paslaugų sveikatos stebėjimas**: Stebėkite išorines AI paslaugas dėl prieinamumo, saugumo incidentų ir politikos pokyčių  
- **Grėsmių žvalgybos integracija**: Įtraukite grėsmių srautus, susijusius su AI ir ML saugumo rizikomis  

#### **Prieigos kontrolė ir minimalus privilegijų principas**  
- **Komponentų lygio leidimai**: Apribokite prieigą prie modelių, duomenų ir paslaugų pagal verslo poreikį  
- **Paslaugų paskyrų valdymas**: Įgyvendinkite specialias paslaugų paskyras su minimaliomis reikalingomis teisėmis  
- **Tinklo segmentacija**: Izoliuokite AI komponentus ir apribokite tinklo prieigą tarp paslaugų  
- **API vartų kontrolė**: Naudokite centralizuotus API vartus, kad kontroliuotumėte ir stebėtumėte prieigą prie išorinių AI paslaugų  

#### **Incidentų reagavimas ir atkūrimas**  
- **Greito reagavimo procedūros**: Nustatytos procedūros, skirtos pataisyti ar pakeisti pažeistus AI komponentus  
- **Kredencialų rotacija**: Automatizuotos sistemos, skirtos paslapčių, API raktų ir paslaugų kredencialų rotacijai  
- **Atstatymo galimybės**: Galimybė greitai grįžti prie ankstesnių, patikrintų AI komponentų versijų  
- **Tiekimo grandinės pažeidimų atkūrimas**: Konkretūs veiksmai, skirti reaguoti į aukštesnio lygio AI paslaugų kompromisus  


### **Microsoft saugumo sprendimai**
- [Microsoft Prompt Shields dokumentacija](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure turinio saugumo paslauga](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID saugumas](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Azure žetonų valdymo geriausios praktikos](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub pažangus saugumas](https://github.com/security/advanced-security)

### **Įgyvendinimo vadovai ir pamokos**
- [Azure API valdymas kaip MCP autentifikavimo vartai](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID autentifikavimas su MCP serveriais](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Saugus žetonų saugojimas ir šifravimas (vaizdo įrašas)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps ir tiekimo grandinės saugumas**
- [Azure DevOps saugumas](https://azure.microsoft.com/products/devops)
- [Azure Repos saugumas](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft tiekimo grandinės saugumo kelionė](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Papildoma saugumo dokumentacija**

Norėdami gauti išsamias saugumo rekomendacijas, peržiūrėkite šiuos specializuotus dokumentus šiame skyriuje:

- **[MCP saugumo geriausios praktikos 2025](./mcp-security-best-practices-2025.md)** - Išsamios saugumo geriausios praktikos MCP įgyvendinimui
- **[Azure turinio saugumo įgyvendinimas](./azure-content-safety-implementation.md)** - Praktiniai pavyzdžiai, kaip integruoti Azure turinio saugumą  
- **[MCP saugumo kontrolės 2025](./mcp-security-controls-2025.md)** - Naujausios saugumo kontrolės ir technikos MCP diegimui
- **[MCP geriausių praktikų greita nuoroda](./mcp-best-practices.md)** - Greita nuoroda į esmines MCP saugumo praktikas

---

## Kas toliau

Toliau: [3 skyrius: Pradžia](../03-GettingStarted/README.md)

---

**Atsakomybės apribojimas**:  
Šis dokumentas buvo išverstas naudojant AI vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojama naudoti profesionalų žmogaus vertimą. Mes neprisiimame atsakomybės už nesusipratimus ar klaidingus interpretavimus, atsiradusius dėl šio vertimo naudojimo.