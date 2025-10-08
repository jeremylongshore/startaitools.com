<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-19T18:15:31+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "sl"
}
-->
# MCP Varnost: Celovita zaščita za AI sisteme

[![MCP Varnostne prakse](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.sl.png)](https://youtu.be/88No8pw706o)

_(Kliknite zgornjo sliko za ogled videa te lekcije)_

Varnost je temeljni del oblikovanja AI sistemov, zato ji dajemo prednost kot drugi sklop. To je skladno z Microsoftovim načelom **Secure by Design** iz [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) prinaša zmogljive nove zmožnosti za aplikacije, ki temeljijo na AI, hkrati pa uvaja edinstvene varnostne izzive, ki presegajo tradicionalna programska tveganja. MCP sistemi se soočajo tako z uveljavljenimi varnostnimi vprašanji (varno kodiranje, najmanjše privilegije, varnost dobavne verige) kot tudi z novimi, specifičnimi grožnjami za AI, kot so vbrizgavanje ukazov, zastrupitev orodij, ugrabitev sej, napadi z zmedo namestnika, ranljivosti pri prenosu žetonov in dinamične spremembe zmožnosti.

Ta lekcija raziskuje najpomembnejša varnostna tveganja pri implementacijah MCP—vključno z avtentikacijo, avtorizacijo, prekomernimi dovoljenji, posrednim vbrizgavanjem ukazov, varnostjo sej, težavami z zmedo namestnika, upravljanjem žetonov in ranljivostmi dobavne verige. Naučili se boste uporabnih ukrepov in najboljših praks za zmanjšanje teh tveganj ter uporabe Microsoftovih rešitev, kot so Prompt Shields, Azure Content Safety in GitHub Advanced Security, za krepitev vaše MCP implementacije.

## Cilji učenja

Do konca te lekcije boste lahko:

- **Prepoznali MCP-specifične grožnje**: Razumeli edinstvena varnostna tveganja v MCP sistemih, vključno z vbrizgavanjem ukazov, zastrupitvijo orodij, prekomernimi dovoljenji, ugrabljanjem sej, težavami z zmedo namestnika, ranljivostmi pri prenosu žetonov in tveganji dobavne verige
- **Uporabili varnostne ukrepe**: Implementirali učinkovite ukrepe, vključno z robustno avtentikacijo, dostopom z najmanjšimi privilegiji, varnim upravljanjem žetonov, nadzorom varnosti sej in preverjanjem dobavne verige
- **Izkoristili Microsoftove varnostne rešitve**: Razumeli in uvedli Microsoft Prompt Shields, Azure Content Safety in GitHub Advanced Security za zaščito MCP delovnih obremenitev
- **Preverili varnost orodij**: Prepoznali pomen validacije metapodatkov orodij, spremljanja dinamičnih sprememb in obrambe pred posrednimi napadi z vbrizgavanjem ukazov
- **Integrirali najboljše prakse**: Združili uveljavljene varnostne temelje (varno kodiranje, utrjevanje strežnikov, ničelno zaupanje) z MCP-specifičnimi ukrepi za celovito zaščito

# MCP Varnostna arhitektura in ukrepi

Sodobne MCP implementacije zahtevajo večplastne varnostne pristope, ki obravnavajo tako tradicionalne programske grožnje kot tudi specifične grožnje za AI. Hitro razvijajoča se specifikacija MCP še naprej izboljšuje svoje varnostne ukrepe, kar omogoča boljšo integracijo z varnostnimi arhitekturami podjetij in uveljavljenimi najboljšimi praksami.

Raziskave iz [Microsoft Digital Defense Report](https://aka.ms/mddr) kažejo, da bi bilo mogoče **98 % prijavljenih vdorov preprečiti z robustno varnostno higieno**. Najbolj učinkovita strategija zaščite združuje temeljne varnostne prakse z MCP-specifičnimi ukrepi—dokazano je, da osnovni varnostni ukrepi najbolj zmanjšujejo splošno varnostno tveganje.

## Trenutna varnostna krajina

> **Opomba:** Te informacije odražajo MCP varnostne standarde na dan **18. avgust 2025**. Specifikacija MCP se hitro razvija, prihodnje implementacije pa lahko uvedejo nove vzorce avtentikacije in izboljšane ukrepe. Vedno se sklicujte na trenutno [MCP specifikacijo](https://spec.modelcontextprotocol.io/), [MCP GitHub repozitorij](https://github.com/modelcontextprotocol) in [dokumentacijo najboljših praks](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) za najnovejša navodila.

### Razvoj MCP avtentikacije

Specifikacija MCP se je bistveno razvila v svojem pristopu k avtentikaciji in avtorizaciji:

- **Prvotni pristop**: Zgodnje specifikacije so zahtevale, da razvijalci implementirajo lastne strežnike za avtentikacijo, pri čemer so MCP strežniki delovali kot OAuth 2.0 strežniki za avtorizacijo, ki neposredno upravljajo uporabniško avtentikacijo
- **Trenutni standard (2025-06-18)**: Posodobljena specifikacija omogoča MCP strežnikom delegiranje avtentikacije zunanjim ponudnikom identitete (kot je Microsoft Entra ID), kar izboljšuje varnostni položaj in zmanjšuje zapletenost implementacije
- **Varnost transportne plasti**: Izboljšana podpora za varne transportne mehanizme z ustreznimi vzorci avtentikacije za lokalne (STDIO) in oddaljene (Streamable HTTP) povezave

## Varnost avtentikacije in avtorizacije

### Trenutni varnostni izzivi

Sodobne MCP implementacije se soočajo z več izzivi pri avtentikaciji in avtorizaciji:

### Tveganja in vektorji groženj

- **Napačno konfigurirana logika avtorizacije**: Napačna implementacija avtorizacije v MCP strežnikih lahko izpostavi občutljive podatke in nepravilno uporabi nadzor dostopa
- **Kompromis OAuth žetonov**: Kraja lokalnih žetonov MCP strežnika omogoča napadalcem, da se predstavljajo kot strežniki in dostopajo do storitev navzdol po toku
- **Ranljivosti pri prenosu žetonov**: Nepravilno ravnanje z žetoni ustvarja obvode varnostnih ukrepov in vrzeli v odgovornosti
- **Prekomerna dovoljenja**: Preveč privilegirani MCP strežniki kršijo načelo najmanjših privilegijev in širijo površino napada

#### Prenos žetonov: Kritični anti-vzorec

**Prenos žetonov je izrecno prepovedan** v trenutni MCP specifikaciji avtorizacije zaradi resnih varnostnih posledic:

##### Obvodi varnostnih ukrepov
- MCP strežniki in API-ji navzdol po toku izvajajo ključne varnostne ukrepe (omejevanje hitrosti, validacija zahtev, spremljanje prometa), ki so odvisni od pravilne validacije žetonov
- Neposredna uporaba žetonov s strani odjemalcev za API-je obide te bistvene zaščite, kar spodkopava varnostno arhitekturo

##### Izzivi pri odgovornosti in reviziji  
- MCP strežniki ne morejo razlikovati med odjemalci, ki uporabljajo žetone, izdane navzgor po toku, kar prekinja revizijske sledi
- Dnevniki strežnikov virov navzdol kažejo zavajajoče izvore zahtev namesto dejanskih posrednikov MCP strežnikov
- Preiskava incidentov in skladnostne revizije postanejo bistveno težje

##### Tveganja iztoka podatkov
- Nevalidirane trditve žetonov omogočajo zlonamernim akterjem s kompromitiranimi žetoni uporabo MCP strežnikov kot posrednikov za iztok podatkov
- Kršitve meja zaupanja omogočajo nepooblaščene vzorce dostopa, ki obidejo predvidene varnostne ukrepe

##### Vektorji napadov na več storitev
- Kompromitirani žetoni, sprejeti s strani več storitev, omogočajo lateralno gibanje po povezanih sistemih
- Predpostavke zaupanja med storitvami so lahko kršene, ko izvor žetonov ni mogoče preveriti

### Varnostni ukrepi in omilitve

**Ključne varnostne zahteve:**

> **OBVEZNO**: MCP strežniki **NE SMEJO** sprejemati nobenih žetonov, ki niso bili izrecno izdani za MCP strežnik

#### Ukrepi za avtentikacijo in avtorizacijo

- **Temeljit pregled avtorizacije**: Izvedite celovite revizije logike avtorizacije MCP strežnikov, da zagotovite, da lahko občutljive vire dostopajo le predvideni uporabniki in odjemalci
  - **Vodnik za implementacijo**: [Azure API Management kot avtentikacijski prehod za MCP strežnike](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Integracija identitete**: [Uporaba Microsoft Entra ID za avtentikacijo MCP strežnikov](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Varno upravljanje žetonov**: Implementirajte [Microsoftove najboljše prakse za validacijo in življenjski cikel žetonov](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Validirajte trditve občinstva žetonov, da se ujemajo z identiteto MCP strežnika
  - Implementirajte pravilno rotacijo in politiko poteka žetonov
  - Preprečite napade z ponovitvijo žetonov in nepooblaščeno uporabo

- **Zaščitena hramba žetonov**: Zavarujte hrambo žetonov z enkripcijo tako v mirovanju kot med prenosom
  - **Najboljše prakse**: [Smernice za varno hrambo in enkripcijo žetonov](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementacija nadzora dostopa

- **Načelo najmanjših privilegijev**: Dodelite MCP strežnikom le minimalna dovoljenja, potrebna za predvideno funkcionalnost
  - Redni pregledi in posodobitve dovoljenj za preprečevanje kopičenja privilegijev
  - **Microsoftova dokumentacija**: [Zagotavljanje dostopa z najmanjšimi privilegiji](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Nadzor dostopa na podlagi vlog (RBAC)**: Implementirajte natančne dodelitve vlog
  - Omejite vloge na specifične vire in dejanja
  - Izogibajte se širokim ali nepotrebnim dovoljenjem, ki širijo površino napada

- **Nenehno spremljanje dovoljenj**: Implementirajte stalno revizijo in spremljanje dostopa
  - Spremljajte vzorce uporabe dovoljenj za anomalije
  - Takoj odpravite prekomerna ali neuporabljena dovoljenja

## Specifične varnostne grožnje za AI

### Napadi z vbrizgavanjem ukazov in manipulacijo orodij

Sodobne MCP implementacije se soočajo s sofisticiranimi napadi, specifičnimi za AI, ki jih tradicionalni varnostni ukrepi ne morejo v celoti nasloviti:

#### **Posredno vbrizgavanje ukazov (Cross-Domain Prompt Injection)**

**Posredno vbrizgavanje ukazov** predstavlja eno najkritičnejših ranljivosti v MCP-podprtih AI sistemih. Napadalci vdelajo zlonamerna navodila v zunanjo vsebino—dokumente, spletne strani, e-pošto ali podatkovne vire—ki jih AI sistemi nato obravnavajo kot legitimne ukaze.

**Scenariji napadov:**
- **Vbrizgavanje v dokumente**: Zlonamerna navodila, skrita v obdelanih dokumentih, ki sprožijo nenamerna dejanja AI
- **Izkoriščanje spletne vsebine**: Kompromitirane spletne strani z vdelanimi ukazi, ki manipulirajo z vedenjem AI ob strganju
- **Napadi prek e-pošte**: Zlonamerni ukazi v e-poštnih sporočilih, ki povzročijo uhajanje informacij ali nepooblaščena dejanja AI pomočnikov
- **Kontaminacija podatkovnih virov**: Kompromitirane baze podatkov ali API-ji, ki strežejo okuženo vsebino AI sistemom

**Vpliv v resničnem svetu**: Ti napadi lahko povzročijo iztok podatkov, kršitve zasebnosti, generiranje škodljive vsebine in manipulacijo uporabniških interakcij. Za podrobno analizo glejte [Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Diagram napada z vbrizgavanjem ukazov](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.sl.png)

#### **Napadi z zastrupitvijo orodij**

**Zastrupitev orodij** cilja na metapodatke, ki definirajo MCP orodja, in izkorišča način, kako LLM-ji interpretirajo opise orodij in parametre za sprejemanje odločitev o izvajanju.

**Mehanizmi napada:**
- **Manipulacija metapodatkov**: Napadalci vbrizgajo zlonamerna navodila v opise orodij, definicije parametrov ali primere uporabe
- **Nevidna navodila**: Skriti ukazi v metapodatkih orodij, ki jih AI modeli obdelajo, a so nevidni za človeške uporabnike
- **Dinamična sprememba orodij ("Rug Pulls")**: Orodja, ki jih uporabniki odobrijo, se kasneje spremenijo, da izvajajo zlonamerna dejanja brez uporabnikovega zavedanja
- **Vbrizgavanje parametrov**: Zlonamerna vsebina, vdelana v sheme parametrov orodij, ki vpliva na vedenje modela

**Tveganja gostovanih strežnikov**: Oddaljeni MCP strežniki predstavljajo povečana tveganja, saj je mogoče definicije orodij posodobiti po začetni odobritvi uporabnika, kar ustvarja scenarije, kjer prej varna orodja postanejo zlonamerna. Za celovito analizo glejte [Tool Poisoning Attacks (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Diagram napada z vbrizgavanjem orodij](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.sl.png)

#### **Dodatni napadi na AI**

- **Posredno vbrizgavanje ukazov med domenami (XPIA)**: Sofisticirani napadi, ki izkoriščajo vsebino iz več domen za obhod varnostnih ukrepov
- **Dinamična sprememba zmožnosti**: Spremembe zmožnosti orodij v realnem času, ki uidejo začetnim varnostnim ocenam
- **Zastrupitev kontekstnega okna**: Napadi, ki manipulirajo z velikimi kontekstnimi okni za skrivanje zlonamernih navodil
- **Napadi z zmedo modela**: Izkoriščanje omejitev modela za ustvarjanje nepredvidljivega ali nevarnega vedenja

### Vpliv varnostnih tveganj za AI

**Visok vpliv posledic:**
- **Iztok podatkov**: Nepooblaščen dostop in kraja občutljivih poslovnih ali osebnih podatkov
- **Kršenje zasebnosti**: Razkritje osebno prepoznavnih informacij (PII) in zaupnih poslovnih podatkov  
- **Manipulacija sistemov**: Nenamerne spremembe kritičnih sistemov in delovnih tokov
- **Kraja poverilnic**: Kompromitiranje avtentikacijskih žetonov in poverilnic storitev
- **Lateralno gibanje**: Uporaba kompromitiranih AI sistemov kot izhodišč za širše napade na omrežje

### Microsoftove varnostne rešitve za AI

#### **AI Prompt Shields: Napredna zaščita pred napadi z vbrizgavanjem**

Microsoft **AI Prompt Shields** zagotavljajo celovito obrambo pred neposrednimi in posrednimi napadi z vbrizgavanjem ukazov prek več varnostnih plasti:

##### **Osnovni zaščitni mehanizmi:**

1. **Napredno zaznavanje in filtriranje**
   - Algoritmi strojnega učenja
- **Varnostna generacija sej**: Uporabljajte kriptografsko varne, nedeterministične ID-je sej, ki jih generirajo varni generatorji naključnih števil
- **Povezava s specifičnim uporabnikom**: Povežite ID-je sej z informacijami, specifičnimi za uporabnika, z uporabo formatov, kot je `<user_id>:<session_id>`, da preprečite zlorabo sej med uporabniki
- **Upravljanje življenjskega cikla sej**: Uvedite pravilno potekanje, rotacijo in preklic sej, da omejite okna ranljivosti
- **Varnost prenosa**: Obvezna uporaba HTTPS za vso komunikacijo, da preprečite prestrezanje ID-jev sej

### Problem zmedenega namestnika

**Problem zmedenega namestnika** se pojavi, ko strežniki MCP delujejo kot avtentikacijski posredniki med odjemalci in storitvami tretjih oseb, kar ustvarja priložnosti za obhod avtorizacije z izkoriščanjem statičnih ID-jev odjemalcev.

#### **Mehanika napada in tveganja**

- **Obhod privolitve na podlagi piškotkov**: Prejšnja avtentikacija uporabnika ustvari piškotke privolitve, ki jih napadalci izkoriščajo z zlonamernimi zahtevami za avtorizacijo z izdelanimi preusmeritvenimi URI-ji
- **Kraja avtorizacijske kode**: Obstoječi piškotki privolitve lahko povzročijo, da strežniki za avtorizacijo preskočijo zaslone za privolitev in preusmerijo kode na končne točke, ki jih nadzorujejo napadalci  
- **Neavtoriziran dostop do API-jev**: Ukradene avtorizacijske kode omogočajo izmenjavo žetonov in impersonacijo uporabnika brez izrecne odobritve

#### **Strategije za zmanjšanje tveganj**

**Obvezni ukrepi:**
- **Izrecne zahteve za privolitev**: Proxy strežniki MCP, ki uporabljajo statične ID-je odjemalcev, **MORAJO** pridobiti privolitev uporabnika za vsakega dinamično registriranega odjemalca
- **Implementacija varnosti OAuth 2.1**: Upoštevajte trenutne najboljše prakse varnosti OAuth, vključno s PKCE (Proof Key for Code Exchange) za vse zahteve za avtorizacijo
- **Stroga validacija odjemalcev**: Uvedite strogo validacijo preusmeritvenih URI-jev in identifikatorjev odjemalcev, da preprečite izkoriščanje

### Ranljivosti pri prenosu žetonov  

**Prenos žetonov** predstavlja eksplicitni anti-vzorec, kjer strežniki MCP sprejemajo žetone odjemalcev brez ustrezne validacije in jih posredujejo navzdol API-jem, kar krši specifikacije avtorizacije MCP.

#### **Varnostne posledice**

- **Obhod nadzora**: Neposredna uporaba žetonov odjemalcev za API-je obide ključne omejitve hitrosti, validacijo in nadzorne ukrepe
- **Korupcija revizijske sledi**: Žetoni, izdani zgoraj, onemogočajo identifikacijo odjemalcev, kar otežuje preiskave incidentov
- **Izvlečenje podatkov prek proxyja**: Nevalidirani žetoni omogočajo zlonamernim akterjem uporabo strežnikov kot proxyjev za neavtoriziran dostop do podatkov
- **Kršitve meja zaupanja**: Predpostavke zaupanja storitev navzdol so lahko kršene, ko izvor žetonov ni mogoče preveriti
- **Razširitev napadov na več storitev**: Kompromitirani žetoni, sprejeti v več storitvah, omogočajo lateralno gibanje

#### **Zahtevani varnostni ukrepi**

**Nepogrešljive zahteve:**
- **Validacija žetonov**: Strežniki MCP **NE SMEJO** sprejemati žetonov, ki niso izrecno izdani za strežnik MCP
- **Preverjanje občinstva**: Vedno preverite, ali trditve o občinstvu žetonov ustrezajo identiteti strežnika MCP
- **Pravilno upravljanje življenjskega cikla žetonov**: Uvedite kratkotrajne dostopne žetone z varnimi praksami rotacije


## Varnost dobavne verige za AI sisteme

Varnost dobavne verige se je razvila onkraj tradicionalnih programskih odvisnosti in zajema celoten ekosistem AI. Sodobne implementacije MCP morajo strogo preverjati in spremljati vse komponente, povezane z AI, saj vsaka predstavlja potencialne ranljivosti, ki lahko ogrozijo celovitost sistema.

### Razširjeni elementi dobavne verige AI

**Tradicionalne programske odvisnosti:**
- Knjižnice in ogrodja odprte kode
- Slike kontejnerjev in osnovni sistemi  
- Orodja za razvoj in gradbene cevovode
- Komponente infrastrukture in storitve

**Specifični elementi dobavne verige AI:**
- **Osnovni modeli**: Predhodno usposobljeni modeli različnih ponudnikov, ki zahtevajo preverjanje izvora
- **Storitve vdelave**: Zunanje storitve za vektorizacijo in semantično iskanje
- **Ponudniki konteksta**: Viri podatkov, baze znanja in dokumentni repozitoriji  
- **API-ji tretjih oseb**: Zunanje AI storitve, ML cevovodi in končne točke za obdelavo podatkov
- **Artefakti modelov**: Teže, konfiguracije in različice modelov, prilagojene za specifične potrebe
- **Viri podatkov za usposabljanje**: Nabori podatkov, uporabljeni za usposabljanje in prilagajanje modelov

### Celovita strategija varnosti dobavne verige

#### **Preverjanje komponent in zaupanje**
- **Validacija izvora**: Preverite izvor, licenciranje in celovitost vseh AI komponent pred integracijo
- **Varnostna ocena**: Izvedite preglede ranljivosti in varnostne preglede za modele, vire podatkov in AI storitve
- **Analiza ugleda**: Ocenite varnostne prakse in zgodovino ponudnikov AI storitev
- **Preverjanje skladnosti**: Zagotovite, da vse komponente izpolnjujejo organizacijske varnostne in regulativne zahteve

#### **Varni cevovodi za uvajanje**  
- **Avtomatizirana varnost CI/CD**: Integrirajte varnostne preglede v avtomatizirane cevovode za uvajanje
- **Celovitost artefaktov**: Uvedite kriptografsko preverjanje za vse uvedene artefakte (koda, modeli, konfiguracije)
- **Postopno uvajanje**: Uporabljajte progresivne strategije uvajanja z varnostnim preverjanjem na vsaki stopnji
- **Zaupanja vredni repozitoriji artefaktov**: Uvajajte samo iz preverjenih, varnih repozitorijev artefaktov

#### **Nenehno spremljanje in odzivanje**
- **Pregled odvisnosti**: Nenehno spremljanje ranljivosti za vse programske in AI komponente
- **Spremljanje modelov**: Nenehna ocena vedenja modelov, odklonov zmogljivosti in varnostnih anomalij
- **Sledenje zdravju storitev**: Spremljanje zunanjih AI storitev glede razpoložljivosti, varnostnih incidentov in sprememb politik
- **Integracija obveščanja o grožnjah**: Vključitev virov groženj, specifičnih za varnost AI in ML

#### **Nadzor dostopa in načelo najmanjših privilegijev**
- **Dovoljenja na ravni komponent**: Omejite dostop do modelov, podatkov in storitev glede na poslovne potrebe
- **Upravljanje računov storitev**: Uvedite namenske račune storitev z minimalno potrebnimi dovoljenji
- **Segmentacija omrežja**: Izolirajte AI komponente in omejite omrežni dostop med storitvami
- **Nadzor API prehodov**: Uporabljajte centralizirane API prehode za nadzor in spremljanje dostopa do zunanjih AI storitev

#### **Odziv na incidente in okrevanje**
- **Postopki hitrega odziva**: Uveljavljeni procesi za popravljanje ali zamenjavo kompromitiranih AI komponent
- **Rotacija poverilnic**: Avtomatizirani sistemi za rotacijo skrivnosti, API ključev in poverilnic storitev
- **Zmožnosti povratka**: Sposobnost hitrega vračanja na prejšnje, preverjene različice AI komponent
- **Okrevanje po kršitvi dobavne verige**: Specifični postopki za odzivanje na kompromitacije storitev AI navzgor

### Microsoftova varnostna orodja in integracija

**GitHub Advanced Security** zagotavlja celovito zaščito dobavne verige, vključno z:
- **Pregledovanje skrivnosti**: Avtomatsko odkrivanje poverilnic, API ključev in žetonov v repozitorijih
- **Pregledovanje odvisnosti**: Ocena ranljivosti za odvisnosti odprte kode in knjižnice
- **Analiza CodeQL**: Statična analiza kode za varnostne ranljivosti in težave pri kodiranju
- **Vpogledi v dobavno verigo**: Vidljivost v zdravje in varnost odvisnosti

**Integracija Azure DevOps in Azure Repos:**
- Brezhibna integracija varnostnega pregledovanja v Microsoftove razvojne platforme
- Avtomatizirani varnostni pregledi v Azure Pipelines za AI delovne obremenitve
- Uveljavljanje politik za varno uvajanje AI komponent

**Notranje prakse Microsofta:**
Microsoft izvaja obsežne prakse varnosti dobavne verige v vseh svojih izdelkih. Več o preverjenih pristopih si preberite v [Pot do varne dobavne verige programske opreme pri Microsoftu](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).


## Osnovne varnostne najboljše prakse

Implementacije MCP podedujejo in gradijo na obstoječi varnostni drži vaše organizacije. Krepitev osnovnih varnostnih praks bistveno izboljša celotno varnost AI sistemov in MCP implementacij.

### Temeljni varnostni principi

#### **Prakse varnega razvoja**
- **Skladnost z OWASP**: Zaščitite se pred [OWASP Top 10](https://owasp.org/www-project-top-ten/) ranljivostmi spletnih aplikacij
- **Zaščite specifične za AI**: Uvedite ukrepe za [OWASP Top 10 za LLM](https://genai.owasp.org/download/43299/?tmstv=1731900559)
- **Varno upravljanje skrivnosti**: Uporabljajte namenske trezorje za žetone, API ključe in občutljive konfiguracijske podatke
- **Šifriranje od konca do konca**: Uvedite varno komunikacijo med vsemi komponentami aplikacije in podatkovnimi tokovi
- **Validacija vhodov**: Stroga validacija vseh uporabniških vnosov, API parametrov in virov podatkov

#### **Utrjevanje infrastrukture**
- **Večfaktorska avtentikacija**: Obvezna MFA za vse administrativne in storitvene račune
- **Upravljanje popravkov**: Avtomatizirano, pravočasno popravljanje operacijskih sistemov, ogrodij in odvisnosti  
- **Integracija ponudnika identitete**: Centralizirano upravljanje identitete prek ponudnikov identitete v podjetju (Microsoft Entra ID, Active Directory)
- **Segmentacija omrežja**: Logična izolacija komponent MCP za omejitev potenciala lateralnega gibanja
- **Načelo najmanjših privilegijev**: Minimalno potrebna dovoljenja za vse sistemske komponente in račune

#### **Spremljanje varnosti in zaznavanje**
- **Celovito beleženje**: Podrobno beleženje aktivnosti AI aplikacij, vključno z interakcijami MCP odjemalec-strežnik
- **Integracija SIEM**: Centralizirano upravljanje informacij o varnosti in dogodkih za zaznavanje anomalij
- **Analitika vedenja**: Spremljanje, ki ga poganja AI, za zaznavanje nenavadnih vzorcev v sistemskem in uporabniškem vedenju
- **Obveščanje o grožnjah**: Integracija zunanjih virov groženj in indikatorjev kompromitacije (IOCs)
- **Odziv na incidente**: Dobro opredeljeni postopki za zaznavanje, odzivanje in okrevanje po varnostnih incidentih

#### **Arhitektura ničelnega zaupanja**
- **Nikoli ne zaupaj, vedno preverjaj**: Nenehno preverjanje uporabnikov, naprav in omrežnih povezav
- **Mikro-segmentacija**: Granularni nadzor omrežja, ki izolira posamezne delovne obremenitve in storitve
- **Varnost, osredotočena na identiteto**: Varnostne politike, ki temeljijo na preverjenih identitetah, ne na lokaciji omrežja
- **Nenehna ocena tveganja**: Dinamična ocena varnostne drže na podlagi trenutnega konteksta in vedenja
- **Pogojni dostop**: Nadzor dostopa, ki se prilagaja glede na dejavnike tveganja, lokacijo in zaupanje naprave

### Vzorci integracije v podjetju

#### **Integracija v Microsoftov varnostni ekosistem**
- **Microsoft Defender za oblak**: Celovito upravljanje varnostne drže v oblaku
- **Azure Sentinel**: SIEM in SOAR zmogljivosti, zasnovane za zaščito AI delovnih obremenitev
- **Microsoft Entra ID**: Upravljanje identitete in dostopa v podjetju s politikami pogojnega dostopa
- **Azure Key Vault**: Centralizirano upravljanje skrivnosti s podporo strojne varnostne module (HSM)
- **Microsoft Purview**: Upravljanje podatkov in skladnost za vire podatkov AI in delovne tokove

#### **Skladnost in upravljanje**
- **Usklajenost z regulativami**: Zagotovite, da implementacije MCP izpolnjujejo zahteve skladnosti, specifične za industrijo (GDPR, HIPAA, SOC 2)
- **Razvrščanje podatkov**: Pravilna kategorizacija in obravnava občutljivih podatkov, ki jih obdelujejo AI sistemi
- **Revizijske sledi**: Celovito beleženje za skladnost z regulativami in forenzične preiskave
- **Nadzor zasebnosti**: Uvedba načel zasebnosti po zasnovi v arhitekturi AI sistema
- **Upravljanje sprememb**: Formalni postopki za varnostne preglede sprememb AI sistema

Te osnovne prakse ustvarjajo robustno varnostno osnovo, ki izboljša učinkovitost specifičnih varnostnih ukrepov MCP in zagotavlja celovito zaščito za aplikacije, ki jih poganja AI.

## Ključni varnostni poudarki

- **Pristop slojevite varnosti**: Združite osnovne varnostne prakse (varno kodiranje, najmanjši privilegiji, preverjanje dobavne verige, nenehno spremljanje) s specifičnimi ukrepi za AI za celovito zaščito

- **Specifična pokrajina groženj za AI**: MCP sistemi se soočajo z edinstvenimi tveganji, vključno z vbrizgavanjem ukazov, zastrupljanjem orodij, ugrabitvijo sej, problemi zmedenega namestnika, ranljivostmi pri prenosu žetonov in prekomernimi dovoljenji, ki zahtevajo specializirane ukrepe

- **Odličnost pri avtentikaciji in avtorizaciji**: Uvedite robustno avtentikacijo z uporabo zunanjih ponudnikov identitete (Microsoft Entra ID), uveljavite pravilno validacijo žetonov in nikoli ne sprejemajte žetonov, ki niso izrecno izdani za vaš strežnik MCP

- **Preprečevanje napadov na AI**: Uvedite Microsoft Prompt Shields in Azure Content Safety za obrambo pred posrednim vbrizgavanjem ukazov in zastrupljanjem orodij, hkrati pa validirajte metapodatke orodij in spremljajte dinamične spremembe

- **Varnost sej in prenosa**: Uporabljajte kriptografsko varne, nedeterministične ID-je sej, povezane z identitetami uporabnikov, uvedite pravilno upravljanje življenjskega cikla sej in nikoli ne uporabljajte sej za avtentikacijo

- **Najboljše prakse varnosti OAuth**: Preprečite napade zmedenega namestnika z
### **Microsoftove varnostne rešitve**
- [Microsoft Prompt Shields dokumentacija](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety storitev](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID varnost](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Najboljše prakse za upravljanje žetonov v Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Vodiči za implementacijo in vadnice**
- [Azure API Management kot avtentikacijski prehod za MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID avtentikacija z MCP strežniki](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Varno shranjevanje žetonov in šifriranje (video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps in varnost dobavne verige**
- [Varnost v Azure DevOps](https://azure.microsoft.com/products/devops)
- [Varnost v Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [Microsoftova pot do varnosti dobavne verige](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Dodatna varnostna dokumentacija**

Za celovita varnostna navodila si oglejte te specializirane dokumente v tem razdelku:

- **[Najboljše prakse za MCP varnost 2025](./mcp-security-best-practices-2025.md)** - Celovite najboljše prakse za MCP implementacije
- **[Implementacija Azure Content Safety](./azure-content-safety-implementation.md)** - Praktični primeri implementacije za integracijo Azure Content Safety  
- **[MCP varnostni nadzori 2025](./mcp-security-controls-2025.md)** - Najnovejši varnostni nadzori in tehnike za MCP uvajanja
- **[Hiter referenčni vodnik za najboljše prakse MCP](./mcp-best-practices.md)** - Hiter referenčni vodnik za ključne MCP varnostne prakse

---

## Kaj sledi

Naprej: [Poglavje 3: Začetek](../03-GettingStarted/README.md)

**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve za prevajanje z umetno inteligenco [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da lahko avtomatizirani prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem maternem jeziku je treba obravnavati kot avtoritativni vir. Za ključne informacije priporočamo profesionalni človeški prevod. Ne prevzemamo odgovornosti za morebitna nesporazumevanja ali napačne razlage, ki bi nastale zaradi uporabe tega prevoda.