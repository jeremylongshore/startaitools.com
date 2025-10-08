<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-19T17:50:00+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "hr"
}
-->
# MCP Sigurnost: Sveobuhvatna zaštita za AI sustave

[![MCP Sigurnosne najbolje prakse](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.hr.png)](https://youtu.be/88No8pw706o)

_(Kliknite na sliku iznad za pregled videa ove lekcije)_

Sigurnost je temeljni dio dizajna AI sustava, zbog čega je stavljamo kao naš drugi odjeljak. Ovo je u skladu s Microsoftovim načelom **Secure by Design** iz [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) donosi snažne nove mogućnosti za aplikacije temeljene na AI-u, ali također uvodi jedinstvene sigurnosne izazove koji nadilaze tradicionalne softverske rizike. MCP sustavi suočavaju se s već poznatim sigurnosnim problemima (sigurno kodiranje, najmanje privilegije, sigurnost opskrbnog lanca) i novim prijetnjama specifičnim za AI, uključujući ubrizgavanje prompta, trovanje alata, otmicu sesija, napade zbunjenog zamjenika, ranjivosti prijenosa tokena i dinamičke izmjene sposobnosti.

Ova lekcija istražuje najkritičnije sigurnosne rizike u MCP implementacijama—pokrivajući autentifikaciju, autorizaciju, prekomjerne privilegije, neizravno ubrizgavanje prompta, sigurnost sesija, probleme zbunjenog zamjenika, upravljanje tokenima i ranjivosti opskrbnog lanca. Naučit ćete praktične kontrole i najbolje prakse za ublažavanje ovih rizika, koristeći Microsoftova rješenja poput Prompt Shields, Azure Content Safety i GitHub Advanced Security za jačanje vaše MCP implementacije.

## Ciljevi učenja

Na kraju ove lekcije, moći ćete:

- **Prepoznati prijetnje specifične za MCP**: Identificirati jedinstvene sigurnosne rizike u MCP sustavima, uključujući ubrizgavanje prompta, trovanje alata, prekomjerne privilegije, otmicu sesija, probleme zbunjenog zamjenika, ranjivosti prijenosa tokena i rizike opskrbnog lanca
- **Primijeniti sigurnosne kontrole**: Implementirati učinkovite mjere poput robusne autentifikacije, pristupa s najmanje privilegija, sigurnog upravljanja tokenima, kontrola sigurnosti sesija i provjere opskrbnog lanca
- **Iskoristiti Microsoftova sigurnosna rješenja**: Razumjeti i implementirati Microsoft Prompt Shields, Azure Content Safety i GitHub Advanced Security za zaštitu MCP radnih opterećenja
- **Validirati sigurnost alata**: Prepoznati važnost validacije metapodataka alata, praćenja dinamičkih promjena i obrane od neizravnih napada ubrizgavanja prompta
- **Integrirati najbolje prakse**: Kombinirati uspostavljene sigurnosne temelje (sigurno kodiranje, učvršćivanje poslužitelja, zero trust) s kontrolama specifičnim za MCP za sveobuhvatnu zaštitu

# MCP Sigurnosna arhitektura i kontrole

Moderne MCP implementacije zahtijevaju slojevite sigurnosne pristupe koji adresiraju i tradicionalne softverske sigurnosne prijetnje i prijetnje specifične za AI. Brzo razvijajuća MCP specifikacija nastavlja unapređivati svoje sigurnosne kontrole, omogućujući bolju integraciju s korporativnim sigurnosnim arhitekturama i uspostavljenim najboljim praksama.

Istraživanje iz [Microsoft Digital Defense Report](https://aka.ms/mddr) pokazuje da bi **98% prijavljenih povreda bilo spriječeno robusnom sigurnosnom higijenom**. Najučinkovitija strategija zaštite kombinira temeljne sigurnosne prakse s kontrolama specifičnim za MCP—dokazane osnovne sigurnosne mjere ostaju najutjecajnije u smanjenju ukupnog sigurnosnog rizika.

## Trenutni sigurnosni pejzaž

> **Napomena:** Ove informacije odražavaju MCP sigurnosne standarde od **18. kolovoza 2025.** MCP protokol se brzo razvija, a buduće implementacije mogu uvesti nove obrasce autentifikacije i poboljšane kontrole. Uvijek se referirajte na trenutnu [MCP Specifikaciju](https://spec.modelcontextprotocol.io/), [MCP GitHub repozitorij](https://github.com/modelcontextprotocol) i [dokumentaciju najboljih sigurnosnih praksi](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) za najnovije smjernice.

### Evolucija MCP autentifikacije

MCP specifikacija značajno je evoluirala u svom pristupu autentifikaciji i autorizaciji:

- **Izvorni pristup**: Rane specifikacije zahtijevale su od developera implementaciju prilagođenih autentifikacijskih poslužitelja, pri čemu su MCP poslužitelji djelovali kao OAuth 2.0 poslužitelji za autorizaciju koji izravno upravljaju korisničkom autentifikacijom
- **Trenutni standard (2025-06-18)**: Ažurirana specifikacija omogućuje MCP poslužiteljima delegiranje autentifikacije vanjskim pružateljima identiteta (poput Microsoft Entra ID), poboljšavajući sigurnosni položaj i smanjujući složenost implementacije
- **Sigurnost transportnog sloja**: Poboljšana podrška za sigurne transportne mehanizme s odgovarajućim obrascima autentifikacije za lokalne (STDIO) i udaljene (Streamable HTTP) veze

## Sigurnost autentifikacije i autorizacije

### Trenutni sigurnosni izazovi

Moderne MCP implementacije suočavaju se s nekoliko izazova vezanih uz autentifikaciju i autorizaciju:

### Rizici i vektori prijetnji

- **Pogrešno konfigurirana logika autorizacije**: Pogrešna implementacija autorizacije u MCP poslužiteljima može izložiti osjetljive podatke i nepravilno primijeniti kontrole pristupa
- **Kompromitacija OAuth tokena**: Krađa tokena lokalnog MCP poslužitelja omogućuje napadačima da se predstavljaju kao poslužitelji i pristupe nizvodnim uslugama
- **Ranjivosti prijenosa tokena**: Nepravilno rukovanje tokenima stvara zaobilaznice sigurnosnih kontrola i praznine u odgovornosti
- **Prekomjerne privilegije**: MCP poslužitelji s previše privilegija krše načelo najmanjih privilegija i proširuju površinu napada

#### Prijenos tokena: Kritični antipattern

**Prijenos tokena izričito je zabranjen** u trenutnoj MCP specifikaciji autorizacije zbog ozbiljnih sigurnosnih implikacija:

##### Zaobilaženje sigurnosnih kontrola
- MCP poslužitelji i nizvodni API-ji implementiraju ključne sigurnosne kontrole (ograničavanje brzine, validacija zahtjeva, praćenje prometa) koje ovise o pravilnoj validaciji tokena
- Izravno korištenje tokena klijenta za API zaobilazi ove ključne zaštite, potkopavajući sigurnosnu arhitekturu

##### Izazovi odgovornosti i revizije  
- MCP poslužitelji ne mogu razlikovati klijente koji koriste tokene izdane uzvodno, narušavajući tragove revizije
- Dnevnici nizvodnih poslužitelja resursa prikazuju pogrešno podrijetlo zahtjeva umjesto stvarnih MCP poslužitelja posrednika
- Istraga incidenata i revizije usklađenosti postaju znatno teže

##### Rizici eksfiltracije podataka
- Nevalidirane tvrdnje tokena omogućuju zlonamjernim akterima s ukradenim tokenima da koriste MCP poslužitelje kao proxyje za eksfiltraciju podataka
- Kršenja granica povjerenja omogućuju neovlaštene obrasce pristupa koji zaobilaze predviđene sigurnosne kontrole

##### Vektori napada na više usluga
- Kompromitirani tokeni prihvaćeni od strane više usluga omogućuju lateralno kretanje kroz povezane sustave
- Pretpostavke povjerenja između usluga mogu biti narušene kada se ne može provjeriti podrijetlo tokena

### Sigurnosne kontrole i mjere ublažavanja

**Ključni sigurnosni zahtjevi:**

> **OBAVEZNO**: MCP poslužitelji **NE SMIJU** prihvaćati tokene koji nisu izričito izdani za MCP poslužitelj

#### Kontrole autentifikacije i autorizacije

- **Temeljita revizija autorizacije**: Provedite sveobuhvatne revizije logike autorizacije MCP poslužitelja kako biste osigurali da samo namijenjeni korisnici i klijenti mogu pristupiti osjetljivim resursima  
  - **Vodič za implementaciju**: [Azure API Management kao autentifikacijska vrata za MCP poslužitelje](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
  - **Integracija identiteta**: [Korištenje Microsoft Entra ID za autentifikaciju MCP poslužitelja](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Sigurno upravljanje tokenima**: Implementirajte [Microsoftove najbolje prakse za validaciju i životni ciklus tokena](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)  
  - Validirajte tvrdnje o publici tokena kako bi odgovarale identitetu MCP poslužitelja  
  - Implementirajte pravilnu rotaciju i politike isteka tokena  
  - Spriječite napade ponovnog korištenja tokena i neovlaštenu upotrebu  

- **Zaštićeno pohranjivanje tokena**: Osigurajte pohranu tokena enkripcijom i u mirovanju i u prijenosu  
  - **Najbolje prakse**: [Smjernice za sigurnu pohranu i enkripciju tokena](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementacija kontrole pristupa

- **Načelo najmanjih privilegija**: Dodijelite MCP poslužiteljima samo minimalne privilegije potrebne za predviđenu funkcionalnost  
  - Redoviti pregledi i ažuriranja privilegija kako bi se spriječilo njihovo povećanje  
  - **Microsoftova dokumentacija**: [Siguran pristup s najmanje privilegija](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Kontrola pristupa temeljena na ulogama (RBAC)**: Implementirajte precizno definirane uloge  
  - Ograničite uloge na specifične resurse i radnje  
  - Izbjegavajte široke ili nepotrebne privilegije koje proširuju površinu napada  

- **Kontinuirano praćenje privilegija**: Implementirajte stalno praćenje i reviziju pristupa  
  - Pratite obrasce korištenja privilegija radi anomalija  
  - Odmah ispravite prekomjerne ili neiskorištene privilegije  

## Sigurnosne prijetnje specifične za AI

### Napadi ubrizgavanja prompta i manipulacije alatima

Moderne MCP implementacije suočavaju se sa sofisticiranim vektorima napada specifičnim za AI koje tradicionalne sigurnosne mjere ne mogu u potpunosti adresirati:

#### **Neizravno ubrizgavanje prompta (Cross-Domain Prompt Injection)**

**Neizravno ubrizgavanje prompta** predstavlja jednu od najkritičnijih ranjivosti u MCP sustavima temeljenim na AI-u. Napadači ugrađuju zlonamjerne upute unutar vanjskog sadržaja—dokumenata, web stranica, e-poruka ili izvora podataka—koje AI sustavi kasnije obrađuju kao legitimne naredbe.

**Scenariji napada:**  
- **Ubrizgavanje putem dokumenata**: Zlonamjerne upute skrivene u obrađenim dokumentima koje pokreću neželjene AI radnje  
- **Eksploatacija web sadržaja**: Kompromitirane web stranice s ugrađenim promptovima koji manipuliraju ponašanjem AI-a prilikom pretraživanja  
- **Napadi putem e-pošte**: Zlonamjerni promptovi u e-porukama koji uzrokuju curenje informacija ili neovlaštene radnje  
- **Kontaminacija izvora podataka**: Kompromitirane baze podataka ili API-ji koji poslužuju zaraženi sadržaj AI sustavima  

**Utjecaj u stvarnom svijetu**: Ovi napadi mogu rezultirati eksfiltracijom podataka, povredama privatnosti, generiranjem štetnog sadržaja i manipulacijom korisničkih interakcija. Za detaljnu analizu, pogledajte [Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).  

![Dijagram napada ubrizgavanja prompta](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.hr.png)  

#### **Napadi trovanja alata**

**Trovanje alata** cilja metapodatke koji definiraju MCP alate, iskorištavajući način na koji LLM-ovi interpretiraju opise alata i parametre za donošenje odluka o izvršenju.  

**Mehanizmi napada:**  
- **Manipulacija metapodataka**: Napadači ubacuju zlonamjerne upute u opise alata, definicije parametara ili primjere korištenja  
- **Nevidljive upute**: Skriveni promptovi u metapodacima alata koje AI modeli obrađuju, ali su nevidljivi ljudskim korisnicima  
- **Dinamička izmjena alata ("Rug Pulls")**: Alati odobreni od strane korisnika kasnije se mijenjaju kako bi izvršavali zlonamjerne radnje bez korisnikove svijesti  
- **Ubrizgavanje parametara**: Zlonamjerni sadržaj ugrađen u sheme parametara alata koji utječe na ponašanje modela  

**Rizici na hostiranim poslužiteljima**: Udaljeni MCP poslužitelji predstavljaju povećane rizike jer se definicije alata mogu ažurirati nakon početnog odobrenja korisnika, stvarajući scenarije u kojima prethodno sigurni alati postaju zlonamjerni. Za sveobuhvatnu analizu, pogledajte [Tool Poisoning Attacks (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).  

![Dijagram ubrizgavanja alata](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.hr.png)  

#### **Dodatni AI vektori napada**

- **Cross-Domain Prompt Injection (XPIA)**: Sofisticirani napadi koji koriste sadržaj iz više domena za zaobilaženje sigurnosnih kontrola  
- **Dinamička izmjena sposobnosti**: Promjene u stvarnom vremenu sposobnosti alata koje izbjegavaju početne sigurnosne procjene  
- **Trovanje kontekstnog prozora**: Napadi koji manipuliraju velikim kontekstnim prozorima kako bi sakrili zlonamjerne upute  
- **Napadi zbunjivanja modela**: Iskorištavanje ograničenja modela za stvaranje nepredvidivog ili nesigurnog ponašanja  

### Utjecaj sigurnosnih rizika specifičnih za AI

**Posljedice visokog utjecaja:**  
- **Eksfiltracija podataka**: Neovlašteni pristup i krađa osjetljivih poslovnih ili osobnih podataka  
- **Povrede privatnosti**: Izlaganje osobnih identifikacijskih podataka (PII) i povjerljivih poslovnih podataka  
- **Manipulacija sustavom**: Neželjene izmjene kritičnih sustava i radnih tokova  
- **Krađa vjerodajnica**: Kompromitacija autentifikacijskih tokena i vjerodajnica usluga  
- **Lateralno kretanje**: Korištenje kompromitiranih AI sustava kao polazišta za šire mrežne napade  

### Microsoftova sigurnosna rješenja za AI

#### **AI Prompt Shields: Napredna zaštita od napada ubrizgavanja**

Microsoft **AI Prompt Shields** pruža sveobuhvatnu obranu od izravnih i neizravnih napada ubrizgavanja prompta kroz više sigurnosnih slojeva:  

##### **Osnovni mehanizmi zaštite:**  

1. **Napredna detekcija i filtriranje**  
   - Algoritmi strojnog učenja i NLP tehnike otkrivaju zlonamjerne upute u vanjskom sadržaju  
   - Analiza u stvarnom vremenu dokumenata, web stranica, e-poruka i izvora podataka za ugražene prijetnje  
   - Kontekstualno razumijevanje obrazaca legitimnih i zlonamjernih promptova  

2. **Tehnike isticanja**  
   - Razlikuje između pouzdanih sistemskih uputa i potencijalno kompromitiranih vanjskih unosa  
   - Metode transformacije teksta koje poboljšavaju
- **Sigurno generiranje sesije**: Koristite kriptografski sigurne, nedeterminističke ID-ove sesija generirane pomoću sigurnih generatora slučajnih brojeva  
- **Veza specifična za korisnika**: Povežite ID-ove sesija s informacijama specifičnim za korisnika koristeći formate poput `<user_id>:<session_id>` kako biste spriječili zloupotrebu sesija između korisnika  
- **Upravljanje životnim ciklusom sesije**: Implementirajte pravilno istecanje, rotaciju i poništavanje kako biste ograničili prozore ranjivosti  
- **Sigurnost prijenosa**: Obavezni HTTPS za svu komunikaciju kako bi se spriječilo presretanje ID-ova sesija  

### Problem zbunjenog zamjenika

**Problem zbunjenog zamjenika** nastaje kada MCP poslužitelji djeluju kao autentifikacijski posrednici između klijenata i usluga trećih strana, stvarajući prilike za zaobilaženje autorizacije iskorištavanjem statičnih ID-ova klijenata.

#### **Mehanika napada i rizici**

- **Zaobilaženje pristanka putem kolačića**: Prethodna autentifikacija korisnika stvara kolačiće pristanka koje napadači iskorištavaju putem zlonamjernih zahtjeva za autorizaciju s prilagođenim URI-jevima za preusmjeravanje  
- **Krađa autorizacijskog koda**: Postojeći kolačići pristanka mogu uzrokovati da poslužitelji za autorizaciju preskoče ekrane za pristanak, preusmjeravajući kodove na krajnje točke pod kontrolom napadača  
- **Neovlašteni pristup API-ju**: Ukradeni autorizacijski kodovi omogućuju razmjenu tokena i lažno predstavljanje korisnika bez eksplicitnog odobrenja  

#### **Strategije ublažavanja**

**Obavezne kontrole:**
- **Zahtjevi za eksplicitni pristanak**: MCP proxy poslužitelji koji koriste statične ID-ove klijenata **MORAJU** dobiti pristanak korisnika za svakog dinamički registriranog klijenta  
- **Implementacija sigurnosti OAuth 2.1**: Slijedite trenutne najbolje prakse sigurnosti OAuth-a, uključujući PKCE (Proof Key for Code Exchange) za sve zahtjeve za autorizaciju  
- **Stroga validacija klijenata**: Provedite rigoroznu validaciju URI-jeva za preusmjeravanje i identifikatora klijenata kako biste spriječili zloupotrebu  

### Ranjivosti prosljeđivanja tokena  

**Prosljeđivanje tokena** predstavlja eksplicitni antipattern gdje MCP poslužitelji prihvaćaju tokene klijenata bez odgovarajuće validacije i prosljeđuju ih prema dolje API-jevima, kršeći MCP specifikacije autorizacije.

#### **Sigurnosne implikacije**

- **Zaobilaženje kontrole**: Izravno korištenje tokena klijent-API zaobilazi ključne kontrole poput ograničavanja brzine, validacije i praćenja  
- **Kompromitiranje revizijskog traga**: Tokeni izdani uzvodno onemogućuju identifikaciju klijenata, narušavajući mogućnosti istrage incidenata  
- **Eksfiltracija podataka putem proxyja**: Nevalidirani tokeni omogućuju zlonamjernim akterima korištenje poslužitelja kao proxyja za neovlašteni pristup podacima  
- **Kršenje granica povjerenja**: Pretpostavke povjerenja usluga prema dolje mogu biti narušene kada se ne može potvrditi podrijetlo tokena  
- **Širenje napada na više usluga**: Kompromitirani tokeni prihvaćeni na više usluga omogućuju lateralno kretanje  

#### **Potrebne sigurnosne kontrole**

**Nepregovarački zahtjevi:**
- **Validacija tokena**: MCP poslužitelji **NE SMIJU** prihvaćati tokene koji nisu izričito izdani za MCP poslužitelj  
- **Provjera publike**: Uvijek provjerite da tvrdnje o publici tokena odgovaraju identitetu MCP poslužitelja  
- **Pravilni životni ciklus tokena**: Implementirajte kratkotrajne pristupne tokene s praksama sigurne rotacije  

## Sigurnost opskrbnog lanca za AI sustave

Sigurnost opskrbnog lanca evoluirala je izvan tradicionalnih softverskih ovisnosti kako bi obuhvatila cijeli AI ekosustav. Moderne MCP implementacije moraju rigorozno provjeravati i nadzirati sve AI komponente, jer svaka od njih uvodi potencijalne ranjivosti koje mogu ugroziti integritet sustava.

### Proširene komponente opskrbnog lanca za AI

**Tradicionalne softverske ovisnosti:**
- Open-source biblioteke i okviri  
- Slike kontejnera i osnovni sustavi  
- Alati za razvoj i CI/CD pipelineovi  
- Infrastrukturne komponente i usluge  

**AI-specifični elementi opskrbnog lanca:**
- **Osnovni modeli**: Pretrenirani modeli od različitih pružatelja koji zahtijevaju provjeru podrijetla  
- **Usluge ugradnje**: Vanjske usluge za vektorizaciju i semantičko pretraživanje  
- **Pružatelji konteksta**: Izvori podataka, baze znanja i repozitoriji dokumenata  
- **API-ji trećih strana**: Vanjske AI usluge, ML pipelineovi i krajnje točke za obradu podataka  
- **Artefakti modela**: Težine, konfiguracije i varijante modela prilagođene za specifične zadatke  
- **Izvori podataka za treniranje**: Skupovi podataka korišteni za treniranje i prilagodbu modela  

### Sveobuhvatna strategija sigurnosti opskrbnog lanca

#### **Provjera komponenti i povjerenje**
- **Validacija podrijetla**: Provjerite podrijetlo, licenciranje i integritet svih AI komponenti prije integracije  
- **Sigurnosna procjena**: Provedite skeniranje ranjivosti i sigurnosne preglede za modele, izvore podataka i AI usluge  
- **Analiza reputacije**: Procijenite sigurnosni dosje i prakse pružatelja AI usluga  
- **Provjera usklađenosti**: Osigurajte da sve komponente zadovoljavaju sigurnosne i regulatorne zahtjeve organizacije  

#### **Sigurni pipelineovi za implementaciju**  
- **Automatizirana sigurnost CI/CD-a**: Integrirajte sigurnosno skeniranje kroz automatizirane pipelineove implementacije  
- **Integritet artefakata**: Implementirajte kriptografsku provjeru za sve implementirane artefakte (kod, modeli, konfiguracije)  
- **Postupna implementacija**: Koristite strategije postupne implementacije sa sigurnosnom validacijom u svakoj fazi  
- **Pouzdani repozitoriji artefakata**: Implementirajte samo iz provjerenih, sigurnih repozitorija artefakata  

#### **Kontinuirano praćenje i odgovor**
- **Skeniranje ovisnosti**: Neprekidno praćenje ranjivosti za sve softverske i AI komponente  
- **Praćenje modela**: Kontinuirana procjena ponašanja modela, odstupanja u performansama i sigurnosnih anomalija  
- **Praćenje zdravlja usluga**: Nadziranje vanjskih AI usluga za dostupnost, sigurnosne incidente i promjene politika  
- **Integracija obavještajnih podataka o prijetnjama**: Uključivanje feedova prijetnji specifičnih za AI i ML sigurnosne rizike  

#### **Kontrola pristupa i najmanje privilegije**
- **Dozvole na razini komponenata**: Ograničite pristup modelima, podacima i uslugama na temelju poslovne potrebe  
- **Upravljanje servisnim računima**: Implementirajte namjenske servisne račune s minimalno potrebnim dozvolama  
- **Segmentacija mreže**: Izolirajte AI komponente i ograničite mrežni pristup između usluga  
- **Kontrole API gatewaya**: Koristite centralizirane API gatewaye za kontrolu i praćenje pristupa vanjskim AI uslugama  

#### **Odgovor na incidente i oporavak**
- **Postupci brzog odgovora**: Uspostavljeni procesi za zakrpe ili zamjenu kompromitiranih AI komponenti  
- **Rotacija vjerodajnica**: Automatizirani sustavi za rotaciju tajni, API ključeva i servisnih vjerodajnica  
- **Sposobnosti vraćanja**: Mogućnost brzog vraćanja na prethodne poznate dobre verzije AI komponenti  
- **Oporavak od kompromitacije opskrbnog lanca**: Specifični postupci za odgovaranje na kompromise AI usluga uzvodno  

### Microsoft alati za sigurnost i integraciju

**GitHub Advanced Security** pruža sveobuhvatnu zaštitu opskrbnog lanca uključujući:
- **Skeniranje tajni**: Automatizirano otkrivanje vjerodajnica, API ključeva i tokena u repozitorijima  
- **Skeniranje ovisnosti**: Procjena ranjivosti za open-source ovisnosti i biblioteke  
- **CodeQL analiza**: Statička analiza koda za sigurnosne ranjivosti i probleme u kodiranju  
- **Uvidi u opskrbni lanac**: Vidljivost u zdravlje i sigurnosni status ovisnosti  

**Integracija s Azure DevOps i Azure Repos:**
- Besprijekorna integracija sigurnosnog skeniranja na Microsoftovim platformama za razvoj  
- Automatizirane sigurnosne provjere u Azure Pipelineovima za AI radna opterećenja  
- Provedba politika za sigurnu implementaciju AI komponenti  

**Interna praksa Microsofta:**
Microsoft implementira opsežne prakse sigurnosti opskrbnog lanca u svim proizvodima. Saznajte više o dokazanim pristupima u [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).
### **Microsoft Sigurnosna Rješenja**
- [Microsoft Prompt Shields Dokumentacija](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety Service](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID Sigurnost](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Najbolje Prakse za Upravljanje Tokenima u Azureu](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Napredna Sigurnost](https://github.com/security/advanced-security)

### **Vodiči za Implementaciju i Tutorijali**
- [Azure API Management kao MCP Autentifikacijska Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID Autentifikacija s MCP Serverima](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Sigurno Pohranjivanje Tokena i Enkripcija (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps i Sigurnost Opskrbnog Lanca**
- [Azure DevOps Sigurnost](https://azure.microsoft.com/products/devops)
- [Azure Repos Sigurnost](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft Put Sigurnosti Opskrbnog Lanca](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Dodatna Sigurnosna Dokumentacija**

Za sveobuhvatne sigurnosne smjernice, pogledajte ove specijalizirane dokumente u ovom odjeljku:

- **[MCP Najbolje Sigurnosne Prakse 2025](./mcp-security-best-practices-2025.md)** - Potpune najbolje prakse za MCP implementacije
- **[Implementacija Azure Content Safety](./azure-content-safety-implementation.md)** - Praktični primjeri implementacije za integraciju Azure Content Safety  
- **[MCP Sigurnosne Kontrole 2025](./mcp-security-controls-2025.md)** - Najnovije sigurnosne kontrole i tehnike za MCP implementacije
- **[Brzi Referentni Vodič za MCP Najbolje Prakse](./mcp-best-practices.md)** - Brzi vodič za ključne MCP sigurnosne prakse

---

## Što Slijedi

Sljedeće: [Poglavlje 3: Početak](../03-GettingStarted/README.md)

**Odricanje od odgovornosti**:  
Ovaj dokument je preveden pomoću AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za kritične informacije preporučuje se profesionalni prijevod od strane čovjeka. Ne preuzimamo odgovornost za nesporazume ili pogrešna tumačenja koja mogu proizaći iz korištenja ovog prijevoda.