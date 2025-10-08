<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-07T00:10:51+00:00",
  "source_file": "changelog.md",
  "language_code": "hr"
}
-->
# Dnevnik promjena: MCP za početnike - Kurikulum

Ovaj dokument služi kao zapis svih značajnih promjena napravljenih u kurikulumu Model Context Protocol (MCP) za početnike. Promjene su dokumentirane obrnutim kronološkim redoslijedom (najnovije promjene na vrhu).

## 6. listopada 2025.

### Proširenje odjeljka "Početak rada" – Napredno korištenje servera i jednostavna autentifikacija

#### Napredno korištenje servera (03-GettingStarted/10-advanced)
- **Dodano novo poglavlje**: Uveden sveobuhvatan vodič za napredno korištenje MCP servera, koji pokriva redovne i niskorazinske arhitekture servera.
  - **Redovni vs. niskorazinski server**: Detaljna usporedba i primjeri koda u Pythonu i TypeScriptu za oba pristupa.
  - **Dizajn temeljen na handlerima**: Objašnjenje upravljanja alatima/resursima/promtovima temeljenog na handlerima za skalabilne i fleksibilne implementacije servera.
  - **Praktični obrasci**: Scenariji iz stvarnog svijeta gdje su obrasci niskorazinskog servera korisni za napredne značajke i arhitekturu.

#### Jednostavna autentifikacija (03-GettingStarted/11-simple-auth)
- **Dodano novo poglavlje**: Korak-po-korak vodič za implementaciju jednostavne autentifikacije na MCP serverima.
  - **Koncepti autentifikacije**: Jasno objašnjenje razlike između autentifikacije i autorizacije te upravljanja vjerodajnicama.
  - **Implementacija osnovne autentifikacije**: Obrasci autentifikacije temeljeni na middlewareu u Pythonu (Starlette) i TypeScriptu (Express), s primjerima koda.
  - **Prijelaz na naprednu sigurnost**: Smjernice za početak s jednostavnom autentifikacijom i napredovanje prema OAuth 2.1 i RBAC-u, uz reference na napredne sigurnosne module.

Ova proširenja pružaju praktične, praktične smjernice za izgradnju robusnijih, sigurnijih i fleksibilnijih implementacija MCP servera, povezujući osnovne koncepte s naprednim obrascima za produkciju.

## 29. rujna 2025.

### MCP Server laboratoriji za integraciju baze podataka – Sveobuhvatan put učenja kroz praksu

#### 11-MCPServerHandsOnLabs - Novi kompletni kurikulum za integraciju baze podataka
- **Kompletan put učenja kroz 13 laboratorija**: Dodan sveobuhvatan kurikulum za izgradnju produkcijski spremnih MCP servera s integracijom PostgreSQL baze podataka.
  - **Implementacija iz stvarnog svijeta**: Zava Retail analitički slučaj korištenja koji demonstrira obrasce na razini poduzeća.
  - **Strukturirani napredak u učenju**:
    - **Laboratoriji 00-03: Osnove** - Uvod, osnovna arhitektura, sigurnost i višekorisnički pristup, postavljanje okruženja.
    - **Laboratoriji 04-06: Izgradnja MCP servera** - Dizajn baze podataka i shema, implementacija MCP servera, razvoj alata.
    - **Laboratoriji 07-09: Napredne značajke** - Integracija semantičke pretrage, testiranje i otklanjanje pogrešaka, integracija s VS Codeom.
    - **Laboratoriji 10-12: Produkcija i najbolje prakse** - Strategije implementacije, praćenje i preglednost, najbolje prakse i optimizacija.
  - **Tehnologije na razini poduzeća**: FastMCP framework, PostgreSQL s pgvectorom, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Napredne značajke**: Sigurnost na razini redaka (RLS), semantička pretraga, višekorisnički pristup podacima, vektorski embeddings, praćenje u stvarnom vremenu.

#### Standardizacija terminologije - Pretvorba "Modula" u "Laboratorij"
- **Sveobuhvatno ažuriranje dokumentacije**: Sustavno ažurirani svi README datoteke u 11-MCPServerHandsOnLabs kako bi se koristila terminologija "Laboratorij" umjesto "Modul".
  - **Naslovi odjeljaka**: Ažurirano "Što ovaj modul pokriva" u "Što ovaj laboratorij pokriva" u svih 13 laboratorija.
  - **Opis sadržaja**: Promijenjeno "Ovaj modul pruža..." u "Ovaj laboratorij pruža..." u cijeloj dokumentaciji.
  - **Ciljevi učenja**: Ažurirano "Na kraju ovog modula..." u "Na kraju ovog laboratorija...".
  - **Navigacijske poveznice**: Pretvorene sve reference "Modul XX:" u "Laboratorij XX:" u međusobnim referencama i navigaciji.
  - **Praćenje završetka**: Ažurirano "Nakon završetka ovog modula..." u "Nakon završetka ovog laboratorija...".
  - **Očuvane tehničke reference**: Održane reference na Python module u konfiguracijskim datotekama (npr. `"module": "mcp_server.main"`).

#### Poboljšanje vodiča za učenje (study_guide.md)
- **Vizualna mapa kurikuluma**: Dodan novi odjeljak "11. Laboratoriji za integraciju baze podataka" s vizualizacijom strukture laboratorija.
- **Struktura repozitorija**: Ažurirano s deset na jedanaest glavnih odjeljaka s detaljnim opisom 11-MCPServerHandsOnLabs.
- **Smjernice za put učenja**: Poboljšane navigacijske upute za pokrivanje odjeljaka 00-11.
- **Pokriće tehnologija**: Dodani detalji o integraciji FastMCP-a, PostgreSQL-a i Azure usluga.
- **Rezultati učenja**: Naglašena izgradnja produkcijski spremnih servera, obrasci integracije baze podataka i sigurnost na razini poduzeća.

#### Poboljšanje strukture glavnog README-a
- **Terminologija temeljena na laboratorijima**: Ažuriran glavni README.md u 11-MCPServerHandsOnLabs za dosljedno korištenje strukture "Laboratorij".
- **Organizacija puta učenja**: Jasna progresija od osnovnih koncepata preko napredne implementacije do produkcijske implementacije.
- **Fokus na stvarni svijet**: Naglasak na praktično, praktično učenje s obrascima i tehnologijama na razini poduzeća.

### Poboljšanja kvalitete i dosljednosti dokumentacije
- **Naglasak na praktično učenje**: Pojačan praktični, laboratorijski pristup kroz cijelu dokumentaciju.
- **Fokus na obrasce na razini poduzeća**: Istaknute produkcijski spremne implementacije i sigurnosni aspekti na razini poduzeća.
- **Integracija tehnologija**: Sveobuhvatno pokrivanje modernih Azure usluga i AI obrazaca integracije.
- **Progresija u učenju**: Jasna, strukturirana staza od osnovnih koncepata do produkcijske implementacije.

## 26. rujna 2025.

### Poboljšanje studija slučaja - Integracija GitHub MCP Registryja

#### Studije slučaja (09-CaseStudy/) - Fokus na razvoj ekosustava
- **README.md**: Veliko proširenje s detaljnom studijom slučaja GitHub MCP Registryja.
  - **Studija slučaja GitHub MCP Registryja**: Nova sveobuhvatna studija slučaja koja ispituje lansiranje GitHub MCP Registryja u rujnu 2025.
    - **Analiza problema**: Detaljno ispitivanje fragmentiranih izazova otkrivanja i implementacije MCP servera.
    - **Arhitektura rješenja**: Pristup centraliziranom registru GitHuba s instalacijom jednim klikom u VS Codeu.
    - **Poslovni utjecaj**: Mjerljiva poboljšanja u procesu onboardinga i produktivnosti developera.
    - **Strateška vrijednost**: Fokus na modularnu implementaciju agenata i interoperabilnost alata.
    - **Razvoj ekosustava**: Pozicioniranje kao temeljna platforma za integraciju agenata.
  - **Poboljšana struktura studija slučaja**: Ažurirane sve studije slučaja s dosljednim formatiranjem i sveobuhvatnim opisima.
    - Azure AI Travel Agents: Naglasak na orkestraciji više agenata.
    - Integracija Azure DevOpsa: Fokus na automatizaciju tijeka rada.
    - Dohvaćanje dokumentacije u stvarnom vremenu: Implementacija Python konzolnog klijenta.
    - Interaktivni generator plana učenja: Chainlit konverzacijska web aplikacija.
    - Dokumentacija u editoru: Integracija VS Codea i GitHub Copilota.
    - Upravljanje Azure API-jem: Obrasci integracije API-ja na razini poduzeća.
    - GitHub MCP Registry: Razvoj ekosustava i platforma za zajednicu.
  - **Sveobuhvatan zaključak**: Prepisan zaključni odjeljak koji ističe sedam studija slučaja koje pokrivaju različite dimenzije implementacije MCP-a.
    - Kategorije: Integracija na razini poduzeća, orkestracija više agenata, produktivnost developera.
    - Razvoj ekosustava, obrazovne aplikacije.
    - Poboljšani uvidi u arhitektonske obrasce, strategije implementacije i najbolje prakse.
    - Naglasak na MCP kao zreli, produkcijski spremni protokol.

#### Ažuriranja vodiča za učenje (study_guide.md)
- **Vizualna mapa kurikuluma**: Ažurirana mentalna mapa za uključivanje GitHub MCP Registryja u odjeljak studija slučaja.
- **Opis studija slučaja**: Poboljšan od generičkih opisa do detaljnog pregleda sedam sveobuhvatnih studija slučaja.
- **Struktura repozitorija**: Ažuriran odjeljak 10 kako bi odražavao sveobuhvatno pokrivanje studija slučaja sa specifičnim detaljima implementacije.
- **Integracija dnevnika promjena**: Dodan unos za 26. rujna 2025. koji dokumentira dodatak GitHub MCP Registryja i poboljšanja studija slučaja.
- **Ažuriranja datuma**: Ažuriran vremenski pečat u podnožju kako bi odražavao najnoviju reviziju (26. rujna 2025.).

### Poboljšanja kvalitete dokumentacije
- **Poboljšanje dosljednosti**: Standardizirano formatiranje i struktura studija slučaja kroz svih sedam primjera.
- **Sveobuhvatno pokrivanje**: Studije slučaja sada pokrivaju scenarije na razini poduzeća, produktivnost developera i razvoj ekosustava.
- **Strateško pozicioniranje**: Pojačan fokus na MCP kao temeljnu platformu za implementaciju agentičkih sustava.
- **Integracija resursa**: Ažurirani dodatni resursi za uključivanje poveznice na GitHub MCP Registry.

## 15. rujna 2025.

### Proširenje naprednih tema - Prilagođeni transporti i inženjering konteksta

#### MCP Prilagođeni transporti (05-AdvancedTopics/mcp-transport/) - Novi vodič za naprednu implementaciju
- **README.md**: Kompletan vodič za implementaciju prilagođenih transportnih mehanizama MCP-a.
  - **Azure Event Grid Transport**: Sveobuhvatna implementacija serverless transporta temeljenog na događajima.
    - Primjeri u C#, TypeScriptu i Pythonu s integracijom Azure Functions.
    - Obrasci arhitekture temeljene na događajima za skalabilna MCP rješenja.
    - Primanje webhooks i rukovanje porukama temeljenim na pushu.
  - **Azure Event Hubs Transport**: Implementacija transporta za visokoprotočno strujanje.
    - Sposobnosti strujanja u stvarnom vremenu za scenarije niske latencije.
    - Strategije particioniranja i upravljanje kontrolnim točkama.
    - Grupiranje poruka i optimizacija performansi.
  - **Obrasci integracije na razini poduzeća**: Primjeri arhitekture spremni za produkciju.
    - Distribuirana obrada MCP-a preko više Azure Functions.
    - Hibridne transportne arhitekture koje kombiniraju više vrsta transporta.
    - Strategije trajnosti poruka, pouzdanosti i rukovanja pogreškama.
  - **Sigurnost i praćenje**: Integracija Azure Key Vaulta i obrasci preglednosti.
    - Autentifikacija pomoću upravljanog identiteta i pristup s najmanjim privilegijama.
    - Telemetrija Application Insightsa i praćenje performansi.
    - Obrasci za prekidače i toleranciju na greške.
  - **Okviri za testiranje**: Sveobuhvatne strategije testiranja za prilagođene transporte.
    - Jedinično testiranje s testnim duplikatima i okvirima za simulaciju.
    - Integracijsko testiranje s Azure Test Containers.
    - Razmatranja za testiranje performansi i opterećenja.

#### Inženjering konteksta (05-AdvancedTopics/mcp-contextengineering/) - Nova disciplina u AI-u
- **README.md**: Sveobuhvatno istraživanje inženjeringa konteksta kao nove discipline.
  - **Osnovni principi**: Potpuno dijeljenje konteksta, svijest o donošenju odluka i upravljanje prozorom konteksta.
  - **Usklađenost s MCP protokolom**: Kako dizajn MCP-a rješava izazove inženjeringa konteksta.
    - Ograničenja prozora konteksta i strategije progresivnog učitavanja.
    - Određivanje relevantnosti i dinamičko dohvaćanje konteksta.
    - Višemodalno rukovanje kontekstom i sigurnosni aspekti.
  - **Pristupi implementaciji**: Jednonitne vs. arhitekture s više agenata.
    - Tehnike segmentiranja i prioritizacije konteksta.
    - Progresivno učitavanje i strategije kompresije konteksta.
    - Slojeviti pristupi kontekstu i optimizacija dohvaćanja.
  - **Okvir za mjerenje**: Novi metrički sustavi za procjenu učinkovitosti konteksta.
    - Razmatranja učinkovitosti unosa, performansi, kvalitete i korisničkog iskustva.
    - Eksperimentalni pristupi optimizaciji konteksta.
    - Analiza neuspjeha i metodologije poboljšanja.

#### Ažuriranja navigacije kurikuluma (README.md)
- **Poboljšana struktura modula**: Ažurirana tablica kurikuluma za uključivanje novih naprednih tema.
  - Dodani unosi za Inženjering konteksta (5.14) i Prilagođeni transport (5.15).
  - Dosljedno formatiranje i navigacijske poveznice kroz sve module.
  - Ažurirani opisi kako bi odražavali trenutni opseg sadržaja.

### Poboljšanja strukture direktorija
- **Standardizacija naziva**: Preimenovan "mcp transport" u "mcp-transport" radi dosljednosti s ostalim mapama naprednih tema.
- **Organizacija sadržaja**: Sve mape 05-AdvancedTopics sada slijede dosljedan obrazac imenovanja (mcp-[tema]).

### Poboljšanja kvalitete dokumentacije
- **Usklađenost sa specifikacijom MCP-a**: Sav novi sadržaj referencira trenutnu specifikaciju MCP-a 2025-06-18.
- **Primjeri na više jezika**: Sveobuhvatni primjeri koda u C#, TypeScriptu i Pythonu.
- **Fokus na poduzeće**: Obrasci spremni za produkciju i integracija s Azure cloudom kroz cijeli sadržaj.
- **Vizualna dokumentacija**: Mermaid dijagrami za vizualizaciju arhitekture i tijeka.

## 18. kolovoza 2025.

### Sveobuhvatno ažuriranje dokumentacije - MCP standardi 2025-06-18

#### MCP najbolje prakse sigurnosti (02-Security/) - Potpuna modernizacija
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Potpuno prepisano u skladu sa specifikacijom MCP-a 2025-06-18.
  - **Obavezni zahtjevi**: Dodani eksplicitni MUST/MUST NOT zahtjevi iz službene specifikacije s jasnim vizualnim indikatorima.
  - **12 osnovnih sigurnosnih praksi**: Restrukturirano s popisa od 15 stavki u sveobuhvatne sigurnosne domene.
    - Sigurnost tokena i autentifikacija s integracijom vanjskih pružatelja identiteta.
    - Upravljanje sesijama i sigurnost transporta s kriptografskim zahtjevima.
    - Zaštita od AI-specifičnih prijetnji s integracijom Microsoft Prompt Shields.
    - Kontrola pristupa i dozvola s princip
#### Napredne teme sigurnosti (05-AdvancedTopics/mcp-security/) - Implementacija spremna za produkciju
- **README.md**: Potpuno prepisan za implementaciju sigurnosti na razini poduzeća
  - **Usklađenost sa specifikacijom**: Ažurirano prema MCP specifikaciji 2025-06-18 s obveznim sigurnosnim zahtjevima
  - **Poboljšana autentifikacija**: Integracija Microsoft Entra ID-a s detaljnim primjerima za .NET i Java Spring Security
  - **Integracija AI sigurnosti**: Implementacija Microsoft Prompt Shields i Azure Content Safety s detaljnim Python primjerima
  - **Napredna mitigacija prijetnji**: Sveobuhvatni primjeri implementacije za:
    - Prevenciju napada "Confused Deputy" uz PKCE i validaciju korisničkog pristanka
    - Prevenciju prosljeđivanja tokena uz validaciju publike i sigurnu upravu tokenima
    - Prevenciju otmice sesije uz kriptografsko povezivanje i analizu ponašanja
  - **Integracija sigurnosti na razini poduzeća**: Praćenje putem Azure Application Insights, detekcija prijetnji i sigurnost opskrbnog lanca
  - **Kontrolni popis implementacije**: Jasna podjela obveznih i preporučenih sigurnosnih kontrola uz prednosti Microsoft sigurnosnog ekosustava

### Kvaliteta dokumentacije i usklađenost sa standardima
- **Reference na specifikaciju**: Ažurirane sve reference prema aktualnoj MCP specifikaciji 2025-06-18
- **Microsoft sigurnosni ekosustav**: Poboljšane smjernice za integraciju kroz cijelu sigurnosnu dokumentaciju
- **Praktična implementacija**: Dodani detaljni primjeri koda u .NET, Java i Python s obrascima za poduzeća
- **Organizacija resursa**: Sveobuhvatna kategorizacija službene dokumentacije, sigurnosnih standarda i vodiča za implementaciju
- **Vizualni indikatori**: Jasno označavanje obveznih zahtjeva naspram preporučenih praksi

#### Osnovni koncepti (01-CoreConcepts/) - Potpuna modernizacija
- **Ažuriranje verzije protokola**: Ažurirano prema aktualnoj MCP specifikaciji 2025-06-18 s verzioniranjem temeljenim na datumu (format YYYY-MM-DD)
- **Rafiniranje arhitekture**: Poboljšani opisi domaćina, klijenata i poslužitelja u skladu s aktualnim MCP arhitekturnim obrascima
  - Domaćini sada jasno definirani kao AI aplikacije koje koordiniraju više MCP klijentskih veza
  - Klijenti opisani kao konektori protokola koji održavaju odnose jedan-na-jedan s poslužiteljima
  - Poslužitelji poboljšani s lokalnim i udaljenim scenarijima implementacije
- **Restrukturiranje primitiva**: Potpuna revizija primitiva poslužitelja i klijenata
  - Primitivi poslužitelja: Resursi (izvori podataka), Upiti (predlošci), Alati (izvršne funkcije) s detaljnim objašnjenjima i primjerima
  - Primitivi klijenata: Uzorkovanje (LLM dovršavanja), Elicitacija (korisnički unos), Zapisivanje (debugging/nadzor)
  - Ažurirano s aktualnim obrascima za otkrivanje (`*/list`), dohvat (`*/get`) i izvršenje (`*/call`) metoda
- **Arhitektura protokola**: Uveden model arhitekture s dva sloja
  - Sloj podataka: Temeljen na JSON-RPC 2.0 s upravljanjem životnim ciklusom i primitivima
  - Sloj prijenosa: STDIO (lokalno) i Streamable HTTP sa SSE (udaljeno) mehanizmima prijenosa
- **Sigurnosni okvir**: Sveobuhvatni sigurnosni principi uključujući eksplicitan korisnički pristanak, zaštitu privatnosti podataka, sigurnost izvršenja alata i sigurnost sloja prijenosa
- **Obrasci komunikacije**: Ažurirane poruke protokola za prikaz inicijalizacije, otkrivanja, izvršenja i obavijesti
- **Primjeri koda**: Osvježeni primjeri u više jezika (.NET, Java, Python, JavaScript) u skladu s aktualnim MCP SDK obrascima

#### Sigurnost (02-Security/) - Sveobuhvatna revizija sigurnosti  
- **Usklađenost sa standardima**: Potpuna usklađenost s MCP specifikacijom 2025-06-18 sigurnosnih zahtjeva
- **Evolucija autentifikacije**: Dokumentirana evolucija od prilagođenih OAuth poslužitelja do delegacije vanjskim pružateljima identiteta (Microsoft Entra ID)
- **Analiza prijetnji specifičnih za AI**: Poboljšana pokrivenost modernih AI vektora napada
  - Detaljni scenariji napada ubrizgavanja upita s primjerima iz stvarnog svijeta
  - Mehanizmi trovanja alata i obrasci napada "rug pull"
  - Trovanje kontekstnog prozora i napadi zbunjivanja modela
- **Microsoft AI sigurnosna rješenja**: Sveobuhvatna pokrivenost Microsoft sigurnosnog ekosustava
  - AI Prompt Shields s naprednom detekcijom, isticanjem i tehnikama razgraničenja
  - Obrasci integracije Azure Content Safety
  - GitHub Advanced Security za zaštitu opskrbnog lanca
- **Napredna mitigacija prijetnji**: Detaljne sigurnosne kontrole za:
  - Otmicu sesije s MCP-specifičnim scenarijima napada i zahtjevima za kriptografski ID sesije
  - Problemi "Confused Deputy" u MCP proxy scenarijima s eksplicitnim zahtjevima za pristanak
  - Ranljivosti prosljeđivanja tokena s obveznim kontrolama validacije
- **Sigurnost opskrbnog lanca**: Proširena pokrivenost AI opskrbnog lanca uključujući temeljne modele, usluge ugrađivanja, pružatelje konteksta i API-je trećih strana
- **Temeljna sigurnost**: Poboljšana integracija s obrascima sigurnosti na razini poduzeća uključujući arhitekturu nultog povjerenja i Microsoft sigurnosni ekosustav
- **Organizacija resursa**: Kategorizirani sveobuhvatni linkovi na resurse prema vrsti (Službeni dokumenti, Standardi, Istraživanja, Microsoft rješenja, Vodiči za implementaciju)

### Poboljšanja kvalitete dokumentacije
- **Strukturirani ciljevi učenja**: Poboljšani ciljevi učenja s konkretnim, izvedivim ishodima
- **Međusobne reference**: Dodane poveznice između povezanih tema sigurnosti i osnovnih koncepata
- **Aktualne informacije**: Ažurirani svi datumski podaci i poveznice na specifikacije prema aktualnim standardima
- **Smjernice za implementaciju**: Dodane konkretne, izvedive smjernice za implementaciju kroz oba odjeljka

## 16. srpnja 2025.

### Poboljšanja README-a i navigacije
- Potpuno redizajnirana navigacija kurikuluma u README.md
- Zamijenjene `<details>` oznake pristupačnijim formatom temeljenim na tablicama
- Kreirane alternativne opcije izgleda u novoj mapi "alternative_layouts"
- Dodani primjeri navigacije u stilu kartica, s tabovima i harmonikom
- Ažuriran odjeljak strukture repozitorija kako bi uključio sve najnovije datoteke
- Poboljšan odjeljak "Kako koristiti ovaj kurikulum" s jasnim preporukama
- Ažurirane poveznice na MCP specifikacije kako bi upućivale na ispravne URL-ove
- Dodan odjeljak o inženjeringu konteksta (5.14) u strukturu kurikuluma

### Ažuriranja vodiča za učenje
- Potpuno revidiran vodič za učenje kako bi bio usklađen s aktualnom strukturom repozitorija
- Dodani novi odjeljci za MCP klijente i alate te popularne MCP poslužitelje
- Ažurirana vizualna karta kurikuluma kako bi točno odražavala sve teme
- Poboljšani opisi naprednih tema kako bi pokrili sva specijalizirana područja
- Ažuriran odjeljak studija slučaja kako bi odražavao stvarne primjere
- Dodan ovaj sveobuhvatni zapis promjena

### Doprinosi zajednice (06-CommunityContributions/)
- Dodane detaljne informacije o MCP poslužiteljima za generiranje slika
- Dodan sveobuhvatan odjeljak o korištenju Claudea u VSCode-u
- Dodane upute za postavljanje i korištenje Cline terminal klijenta
- Ažuriran odjeljak MCP klijenata kako bi uključio sve popularne opcije klijenata
- Poboljšani primjeri doprinosa s točnijim uzorcima koda

### Napredne teme (05-AdvancedTopics/)
- Organizirane sve specijalizirane mape tema s dosljednim nazivima
- Dodani materijali i primjeri za inženjering konteksta
- Dodana dokumentacija za integraciju Foundry agenta
- Poboljšana dokumentacija za sigurnosnu integraciju Entra ID-a

## 11. lipnja 2025.

### Početno stvaranje
- Objavljena prva verzija kurikuluma MCP za početnike
- Kreirana osnovna struktura za svih 10 glavnih odjeljaka
- Implementirana vizualna karta kurikuluma za navigaciju
- Dodani početni uzorci projekata u više programskih jezika

### Početak rada (03-GettingStarted/)
- Kreirani prvi primjeri implementacije poslužitelja
- Dodane smjernice za razvoj klijenata
- Uključene upute za integraciju LLM klijenata
- Dodana dokumentacija za integraciju s VS Code-om
- Implementirani primjeri poslužitelja sa Server-Sent Events (SSE)

### Osnovni koncepti (01-CoreConcepts/)
- Dodano detaljno objašnjenje arhitekture klijent-poslužitelj
- Kreirana dokumentacija o ključnim komponentama protokola
- Dokumentirani obrasci poruka u MCP-u

## 23. svibnja 2025.

### Struktura repozitorija
- Inicijaliziran repozitorij s osnovnom strukturom mapa
- Kreirani README datoteke za svaki glavni odjeljak
- Postavljena infrastruktura za prijevode
- Dodani slikovni materijali i dijagrami

### Dokumentacija
- Kreiran početni README.md s pregledom kurikuluma
- Dodani CODE_OF_CONDUCT.md i SECURITY.md
- Postavljen SUPPORT.md s uputama za dobivanje pomoći
- Kreirana preliminarna struktura vodiča za učenje

## 15. travnja 2025.

### Planiranje i okvir
- Početno planiranje kurikuluma MCP za početnike
- Definirani ciljevi učenja i ciljana publika
- Nacrtana struktura kurikuluma s 10 odjeljaka
- Razvijen konceptualni okvir za primjere i studije slučaja
- Kreirani početni prototipovi primjera za ključne koncepte

---

**Izjava o odricanju odgovornosti**:  
Ovaj dokument je preveden pomoću AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za ključne informacije preporučuje se profesionalni prijevod od strane ljudskog prevoditelja. Ne preuzimamo odgovornost za nesporazume ili pogrešne interpretacije koje mogu proizaći iz korištenja ovog prijevoda.