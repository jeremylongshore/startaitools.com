<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-07T00:14:10+00:00",
  "source_file": "changelog.md",
  "language_code": "sl"
}
-->
# Dnevnik sprememb: Učni načrt MCP za začetnike

Ta dokument služi kot zapis vseh pomembnih sprememb, ki so bile narejene v učnem načrtu Model Context Protocol (MCP) za začetnike. Spremembe so dokumentirane v obratnem kronološkem vrstnem redu (najprej najnovejše spremembe).

## 6. oktober 2025

### Razširitev razdelka Začetek – Napredna uporaba strežnika in enostavna avtentikacija

#### Napredna uporaba strežnika (03-GettingStarted/10-advanced)
- **Dodano novo poglavje**: Predstavljen obsežen vodič za napredno uporabo MCP strežnika, ki pokriva tako običajne kot nizkonivojske strežniške arhitekture.
  - **Običajni vs. nizkonivojski strežnik**: Podrobna primerjava in primeri kode v Pythonu in TypeScriptu za oba pristopa.
  - **Načrtovanje na podlagi upravljalnikov**: Razlaga upravljanja orodij/virov/promtov na podlagi upravljalnikov za skalabilne in prilagodljive strežniške implementacije.
  - **Praktični vzorci**: Scenariji iz resničnega sveta, kjer so nizkonivojski strežniški vzorci koristni za napredne funkcije in arhitekturo.

#### Enostavna avtentikacija (03-GettingStarted/11-simple-auth)
- **Dodano novo poglavje**: Korak za korakom vodič za implementacijo enostavne avtentikacije v MCP strežnikih.
  - **Koncepti avtentikacije**: Jasna razlaga razlike med avtentikacijo in avtorizacijo ter ravnanja s poverilnicami.
  - **Osnovna implementacija avtentikacije**: Vzorci avtentikacije na podlagi middleware v Pythonu (Starlette) in TypeScriptu (Express), s primeri kode.
  - **Prehod na napredno varnost**: Smernice za začetek z enostavno avtentikacijo in napredovanje do OAuth 2.1 in RBAC, z referencami na napredne varnostne module.

Te dodatke zagotavljajo praktične, praktične smernice za gradnjo bolj robustnih, varnih in prilagodljivih MCP strežniških implementacij, ki povezujejo osnovne koncepte z naprednimi produkcijskimi vzorci.

## 29. september 2025

### Laboratoriji za integracijo podatkovnih baz MCP strežnika – Celovita učna pot

#### 11-MCPServerHandsOnLabs - Nov popoln učni načrt za integracijo podatkovnih baz
- **Popolna učna pot s 13 laboratoriji**: Dodan celovit praktični učni načrt za gradnjo produkcijsko pripravljenih MCP strežnikov z integracijo podatkovne baze PostgreSQL.
  - **Implementacija iz resničnega sveta**: Primer uporabe analitike Zava Retail, ki prikazuje vzorce na ravni podjetja.
  - **Strukturiran učni napredek**:
    - **Laboratoriji 00-03: Osnove** - Uvod, osnovna arhitektura, varnost in večnajemniška okolja, nastavitev okolja.
    - **Laboratoriji 04-06: Gradnja MCP strežnika** - Načrtovanje podatkovne baze in sheme, implementacija MCP strežnika, razvoj orodij.
    - **Laboratoriji 07-09: Napredne funkcije** - Integracija semantičnega iskanja, testiranje in odpravljanje napak, integracija z VS Code.
    - **Laboratoriji 10-12: Produkcija in najboljše prakse** - Strategije uvajanja, spremljanje in opazovanje, najboljše prakse in optimizacija.
  - **Tehnologije na ravni podjetja**: Okvir FastMCP, PostgreSQL s pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Napredne funkcije**: Varnost na ravni vrstic (RLS), semantično iskanje, večnajemniški dostop do podatkov, vektorski embeddings, spremljanje v realnem času.

#### Standardizacija terminologije - Pretvorba modulov v laboratorije
- **Celovita posodobitev dokumentacije**: Sistematično posodobljeni vsi README datoteke v 11-MCPServerHandsOnLabs za uporabo terminologije "Laboratorij" namesto "Modul".
  - **Naslovi razdelkov**: Posodobljeno "Kaj pokriva ta modul" v "Kaj pokriva ta laboratorij" v vseh 13 laboratorijih.
  - **Opis vsebine**: Spremenjeno "Ta modul zagotavlja..." v "Ta laboratorij zagotavlja..." v celotni dokumentaciji.
  - **Učni cilji**: Posodobljeno "Do konca tega modula..." v "Do konca tega laboratorija...".
  - **Navigacijske povezave**: Pretvorjene vse reference "Modul XX:" v "Laboratorij XX:" v medsebojnih referencah in navigaciji.
  - **Sledenje dokončanju**: Posodobljeno "Po dokončanju tega modula..." v "Po dokončanju tega laboratorija...".
  - **Ohranjene tehnične reference**: Ohranjen Python modul reference v konfiguracijskih datotekah (npr. `"module": "mcp_server.main"`).

#### Izboljšanje študijskega vodiča (study_guide.md)
- **Vizualni zemljevid učnega načrta**: Dodan nov razdelek "11. Laboratoriji za integracijo podatkovnih baz" z vizualizacijo strukture laboratorijev.
- **Struktura repozitorija**: Posodobljeno z desetih na enajst glavnih razdelkov z podrobnim opisom 11-MCPServerHandsOnLabs.
- **Smernice za učno pot**: Izboljšana navodila za navigacijo, ki pokrivajo razdelke 00-11.
- **Pokritost tehnologij**: Dodane podrobnosti o integraciji FastMCP, PostgreSQL in Azure storitev.
- **Učni rezultati**: Poudarjen razvoj produkcijsko pripravljenih strežnikov, vzorce integracije podatkovnih baz in varnost na ravni podjetja.

#### Izboljšanje strukture glavnega README
- **Terminologija na podlagi laboratorijev**: Posodobljen glavni README.md v 11-MCPServerHandsOnLabs za dosledno uporabo strukture "Laboratorij".
- **Organizacija učne poti**: Jasno napredovanje od osnovnih konceptov prek napredne implementacije do uvajanja v produkcijo.
- **Osredotočenost na resnični svet**: Poudarek na praktičnem, praktičnem učenju z vzorci in tehnologijami na ravni podjetja.

### Izboljšave kakovosti in doslednosti dokumentacije
- **Poudarek na praktičnem učenju**: Okrepljen praktičen pristop, ki temelji na laboratorijih, v celotni dokumentaciji.
- **Osredotočenost na vzorce na ravni podjetja**: Poudarjene produkcijsko pripravljene implementacije in varnostne vidike na ravni podjetja.
- **Integracija tehnologij**: Celovita pokritost sodobnih Azure storitev in vzorcev integracije AI.
- **Učni napredek**: Jasna, strukturirana pot od osnovnih konceptov do uvajanja v produkcijo.

## 26. september 2025

### Izboljšanje študij primerov – Integracija GitHub MCP Registry

#### Študije primerov (09-CaseStudy/) - Osredotočenost na razvoj ekosistema
- **README.md**: Velika razširitev s celovito študijo primera GitHub MCP Registry.
  - **Študija primera GitHub MCP Registry**: Nova celovita študija primera, ki preučuje lansiranje GitHub MCP Registry septembra 2025.
    - **Analiza problema**: Podrobna preučitev izzivov pri odkrivanju in uvajanju MCP strežnikov.
    - **Arhitektura rešitve**: Pristop centraliziranega registra GitHub z enostavno namestitvijo v VS Code.
    - **Poslovni vpliv**: Merljive izboljšave pri uvajanju razvijalcev in produktivnosti.
    - **Strateška vrednost**: Osredotočenost na modularno uvajanje agentov in interoperabilnost med orodji.
    - **Razvoj ekosistema**: Pozicioniranje kot temeljna platforma za integracijo agentov.
  - **Izboljšana struktura študij primerov**: Posodobljene vse študije primerov s konsistentnim formatiranjem in celovitimi opisi.
    - Azure AI Travel Agents: Poudarek na orkestraciji več agentov.
    - Integracija Azure DevOps: Osredotočenost na avtomatizacijo delovnih tokov.
    - Pridobivanje dokumentacije v realnem času: Implementacija Python konzolnega odjemalca.
    - Interaktivni generator študijskega načrta: Chainlit pogovorna spletna aplikacija.
    - Dokumentacija v urejevalniku: Integracija VS Code in GitHub Copilot.
    - Upravljanje API-jev Azure: Vzorci integracije API-jev na ravni podjetja.
    - GitHub MCP Registry: Razvoj ekosistema in platforma skupnosti.
  - **Celoviti zaključek**: Preoblikovan zaključni razdelek, ki poudarja sedem študij primerov, ki pokrivajo različne dimenzije implementacije MCP.
    - Integracija na ravni podjetja, orkestracija več agentov, produktivnost razvijalcev.
    - Razvoj ekosistema, kategorizacija izobraževalnih aplikacij.
    - Izboljšani vpogledi v arhitekturne vzorce, strategije implementacije in najboljše prakse.
    - Poudarek na MCP kot zrelem, produkcijsko pripravljenem protokolu.

#### Posodobitve študijskega vodiča (study_guide.md)
- **Vizualni zemljevid učnega načrta**: Posodobljen miselni zemljevid, ki vključuje GitHub MCP Registry v razdelek študij primerov.
- **Opis študij primerov**: Izboljšan iz generičnih opisov v podrobno razčlenitev sedmih celovitih študij primerov.
- **Struktura repozitorija**: Posodobljen razdelek 10, ki odraža celovito pokritost študij primerov s specifičnimi podrobnostmi implementacije.
- **Integracija dnevnika sprememb**: Dodan vnos za 26. september 2025, ki dokumentira dodatek GitHub MCP Registry in izboljšave študij primerov.
- **Posodobitve datumov**: Posodobljen časovni žig v nogi dokumenta, ki odraža najnovejšo revizijo (26. september 2025).

### Izboljšave kakovosti dokumentacije
- **Izboljšanje doslednosti**: Standardizirano formatiranje in struktura študij primerov v vseh sedmih primerih.
- **Celovita pokritost**: Študije primerov zdaj pokrivajo scenarije na ravni podjetja, produktivnost razvijalcev in razvoj ekosistema.
- **Strateško pozicioniranje**: Poudarjen MCP kot temeljna platforma za uvajanje agentnih sistemov.
- **Integracija virov**: Posodobljeni dodatni viri, ki vključujejo povezavo do GitHub MCP Registry.

## 15. september 2025

### Razširitev naprednih tem – Prilagojeni transporti in inženiring konteksta

#### Prilagojeni transporti MCP (05-AdvancedTopics/mcp-transport/) - Nov vodič za napredno implementacijo
- **README.md**: Celovit vodič za implementacijo prilagojenih transportnih mehanizmov MCP.
  - **Transport Azure Event Grid**: Celovita strežniška implementacija na podlagi dogodkov.
    - Primeri v C#, TypeScriptu in Pythonu z integracijo Azure Functions.
    - Vzorci arhitekture na podlagi dogodkov za skalabilne MCP rešitve.
    - Sprejemniki webhookov in obdelava sporočil na podlagi potiskanja.
  - **Transport Azure Event Hubs**: Implementacija transporta za pretakanje z visoko prepustnostjo.
    - Zmožnosti pretakanja v realnem času za scenarije z nizko zakasnitvijo.
    - Strategije particioniranja in upravljanje kontrolnih točk.
    - Paketna obdelava sporočil in optimizacija zmogljivosti.
  - **Vzorce integracije na ravni podjetja**: Primeri arhitekture, pripravljeni za produkcijo.
    - Distribuirana obdelava MCP prek več Azure Functions.
    - Hibridne transportne arhitekture, ki združujejo več vrst transportov.
    - Strategije trajnosti sporočil, zanesljivosti in obravnave napak.
  - **Varnost in spremljanje**: Integracija Azure Key Vault in vzorci opazovanja.
    - Avtentikacija z upravljano identiteto in dostop z najmanjšimi privilegiji.
    - Telemetrija Application Insights in spremljanje zmogljivosti.
    - Vzorci zaustavljanja in strategije odpornosti na napake.
  - **Okviri za testiranje**: Celovite strategije testiranja za prilagojene transporte.
    - Enotno testiranje z dvojniki testov in okviri za simulacijo.
    - Testiranje integracije z Azure Test Containers.
    - Premisleki o testiranju zmogljivosti in obremenitve.

#### Inženiring konteksta (05-AdvancedTopics/mcp-contextengineering/) - Nastajajoča disciplina AI
- **README.md**: Celovita raziskava inženiringa konteksta kot nastajajočega področja.
  - **Osnovna načela**: Popolno deljenje konteksta, zavedanje odločanja o akcijah in upravljanje okna konteksta.
  - **Poravnava z MCP protokolom**: Kako zasnova MCP obravnava izzive inženiringa konteksta.
    - Omejitve okna konteksta in strategije progresivnega nalaganja.
    - Določanje ustreznosti in dinamično pridobivanje konteksta.
    - Večmodalno upravljanje konteksta in varnostni vidiki.
  - **Pristopi k implementaciji**: Arhitekture z enim nitjo proti večagentnim arhitekturam.
    - Tehnike razdeljevanja in prioritizacije konteksta.
    - Progresivno nalaganje konteksta in strategije stiskanja.
    - Slojeviti pristopi konteksta in optimizacija pridobivanja.
  - **Okvir za merjenje**: Nastajajoče metrike za ocenjevanje učinkovitosti konteksta.
    - Premisleki o učinkovitosti vnosa, zmogljivosti, kakovosti in uporabniški izkušnji.
    - Eksperimentalni pristopi k optimizaciji konteksta.
    - Analiza napak in metodologije izboljšanja.

#### Posodobitve navigacije učnega načrta (README.md)
- **Izboljšana struktura modulov**: Posodobljena tabela učnega načrta za vključitev novih naprednih tem.
  - Dodani vnosi za Inženiring konteksta (5.14) in Prilagojeni transport (5.15).
  - Dosledno formatiranje in navigacijske povezave v vseh modulih.
  - Posodobljeni opisi, ki odražajo trenutni obseg vsebine.

### Izboljšave strukture imenikov
- **Standardizacija poimenovanja**: Preimenovano "mcp transport" v "mcp-transport" za doslednost z drugimi mapami naprednih tem.
- **Organizacija vsebine**: Vse mape 05-AdvancedTopics zdaj sledijo doslednemu vzorcu poimenovanja (mcp-[tema]).

### Izboljšave kakovosti dokumentacije
- **Poravnava s specifikacijo MCP**: Vsa nova vsebina se nanaša na trenutno specifikacijo MCP 2025-06-18.
- **Primeri v več jezikih**: Celoviti primeri kode v C#, TypeScriptu in Pythonu.
- **Osredotočenost na podjetja**: Vzorci, pripravljeni za produkcijo, in integracija Azure oblakov v celotni vsebini.
- **Vizualna dokumentacija**: Diagrami Mermaid za vizualizacijo arhitekture in tokov.

## 18. avgust 2025

### Celovita posodobitev dokumentacije – Standardi MCP 2025-06-18

#### Najboljše prakse varnosti MCP (02-Security/) - Popolna modernizacija
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Popolna prenova, usklajena s specifikacijo MCP 2025-06-18.
  - **Obvezne zahteve**: Dodane eksplicitne zahteve MUST/MUST NOT iz uradne specifikacije z jasnimi vizualnimi indikatorji.
  - **12 osnovnih varnostnih praks**: Prestrukturirano s 15-točkovnega seznama v celovite varnostne domene.
    - Varnost žetonov in avtentikacija z integracijo zunanjega ponudnika identitete.
    - Upravljanje sej in varnost transporta s kriptografskimi zahtevami.
    - Zaščita pred specifičnimi grož
#### Napredne teme varnosti (05-AdvancedTopics/mcp-security/) - Implementacija pripravljena za produkcijo
- **README.md**: Popolna prenova za implementacijo varnosti na ravni podjetja
  - **Usklajenost s trenutnimi specifikacijami**: Posodobljeno na MCP specifikacijo 2025-06-18 z obveznimi varnostnimi zahtevami
  - **Izboljšana avtentikacija**: Integracija Microsoft Entra ID z obsežnimi primeri v .NET in Java Spring Security
  - **Integracija AI varnosti**: Implementacija Microsoft Prompt Shields in Azure Content Safety z natančnimi primeri v Pythonu
  - **Napredna ublažitev groženj**: Celoviti primeri implementacije za:
    - Preprečevanje napadov "Confused Deputy" z uporabo PKCE in validacijo uporabniškega soglasja
    - Preprečevanje prenosa žetonov z validacijo občinstva in varnim upravljanjem žetonov
    - Preprečevanje ugrabitve sej z uporabo kriptografske vezave in analize vedenja
  - **Integracija varnosti na ravni podjetja**: Spremljanje z Azure Application Insights, detekcija groženj in varnost dobavne verige
  - **Kontrolni seznam implementacije**: Jasna ločitev med obveznimi in priporočenimi varnostnimi ukrepi z ugodnostmi Microsoftovega varnostnega ekosistema

### Kakovost dokumentacije in usklajenost s standardi
- **Reference specifikacij**: Posodobljene vse reference na trenutno MCP specifikacijo 2025-06-18
- **Microsoftov varnostni ekosistem**: Izboljšano vodstvo za integracijo skozi celotno varnostno dokumentacijo
- **Praktična implementacija**: Dodani podrobni primeri kode v .NET, Java in Python z vzorci za podjetja
- **Organizacija virov**: Celovita kategorizacija uradne dokumentacije, varnostnih standardov in vodnikov za implementacijo
- **Vizualni kazalniki**: Jasno označevanje obveznih zahtev v primerjavi s priporočenimi praksami

#### Osnovni koncepti (01-CoreConcepts/) - Popolna modernizacija
- **Posodobitev različice protokola**: Posodobljeno na trenutno MCP specifikacijo 2025-06-18 z datumsko označenimi različicami (format YYYY-MM-DD)
- **Izboljšanje arhitekture**: Izboljšani opisi gostiteljev, odjemalcev in strežnikov, ki odražajo trenutne vzorce MCP arhitekture
  - Gostitelji so zdaj jasno opredeljeni kot AI aplikacije, ki koordinirajo več povezav MCP odjemalcev
  - Odjemalci opisani kot protokolarni konektorji, ki vzdržujejo enojne odnose s strežniki
  - Strežniki izboljšani z lokalnimi in oddaljenimi scenariji namestitve
- **Prestrukturiranje primitivov**: Popolna prenova strežniških in odjemalskih primitivov
  - Strežniški primitivi: Viri (podatkovni viri), Predloge (template), Orodja (izvedljive funkcije) z natančnimi razlagami in primeri
  - Odjemalski primitivi: Vzorčenje (LLM zaključki), Elicitacija (uporabniški vnos), Beleženje (debugging/monitoring)
  - Posodobljeno z aktualnimi metodami za odkrivanje (`*/list`), pridobivanje (`*/get`) in izvajanje (`*/call`)
- **Arhitektura protokola**: Uveden dvoplastni arhitekturni model
  - Podatkovna plast: Temelji na JSON-RPC 2.0 z upravljanjem življenjskega cikla in primitivov
  - Transportna plast: STDIO (lokalno) in Streamable HTTP z SSE (oddaljeni) transportni mehanizmi
- **Varnostni okvir**: Celovita varnostna načela, vključno z eksplicitnim soglasjem uporabnika, zaščito zasebnosti podatkov, varnostjo izvajanja orodij in varnostjo transportne plasti
- **Vzorce komunikacije**: Posodobljena sporočila protokola za prikaz inicializacije, odkrivanja, izvajanja in obveščanja
- **Primeri kode**: Osveženi večjezični primeri (.NET, Java, Python, JavaScript), ki odražajo trenutne vzorce MCP SDK

#### Varnost (02-Security/) - Celovita prenova varnosti  
- **Usklajenost s standardi**: Popolna uskladitev z varnostnimi zahtevami MCP specifikacije 2025-06-18
- **Evolucija avtentikacije**: Dokumentirana evolucija od prilagojenih OAuth strežnikov do delegacije zunanjih ponudnikov identitete (Microsoft Entra ID)
- **Analiza groženj specifičnih za AI**: Izboljšana pokritost sodobnih napadov na AI
  - Podrobni scenariji napadov z vbrizgavanjem v predloge z resničnimi primeri
  - Mehanizmi zastrupitve orodij in vzorci napadov "rug pull"
  - Zastrupitev kontekstnega okna in napadi z zmedo modela
- **Microsoftove rešitve za varnost AI**: Celovita pokritost Microsoftovega varnostnega ekosistema
  - AI Prompt Shields z naprednim zaznavanjem, osvetljevanjem in tehnikami ločevanja
  - Vzorci integracije Azure Content Safety
  - GitHub Advanced Security za zaščito dobavne verige
- **Napredna ublažitev groženj**: Podrobni varnostni ukrepi za:
  - Ugrabitev sej z MCP-specifičnimi scenariji napadov in zahtevami za kriptografske ID-je sej
  - Težave "Confused Deputy" v MCP proxy scenarijih z eksplicitnimi zahtevami za soglasje
  - Ranljivosti prenosa žetonov z obveznimi kontrolami validacije
- **Varnost dobavne verige**: Razširjena pokritost AI dobavne verige, vključno z osnovnimi modeli, storitvami vgrajevanja, ponudniki konteksta in API-ji tretjih oseb
- **Osnovna varnost**: Izboljšana integracija z varnostnimi vzorci na ravni podjetja, vključno z arhitekturo ničelnega zaupanja in Microsoftovim varnostnim ekosistemom
- **Organizacija virov**: Kategorizirani celoviti povezave virov po tipu (Uradni dokumenti, Standardi, Raziskave, Microsoftove rešitve, Vodniki za implementacijo)

### Izboljšave kakovosti dokumentacije
- **Strukturirani učni cilji**: Izboljšani učni cilji s specifičnimi, izvedljivimi rezultati
- **Križne reference**: Dodane povezave med povezanimi temami varnosti in osnovnih konceptov
- **Aktualne informacije**: Posodobljene vse datumske reference in povezave specifikacij na trenutne standarde
- **Vodstvo za implementacijo**: Dodane specifične, izvedljive smernice za implementacijo skozi oba razdelka

## 16. julij 2025

### Izboljšave README in navigacije
- Popolnoma prenovljena navigacija kurikuluma v README.md
- Zamenjani `<details>` oznake z bolj dostopnim formatom na osnovi tabel
- Ustvarjene alternativne možnosti postavitve v novi mapi "alternative_layouts"
- Dodani primeri navigacije v obliki kartic, zavihkov in harmonike
- Posodobljen razdelek strukture repozitorija, da vključuje vse najnovejše datoteke
- Izboljšan razdelek "Kako uporabljati ta kurikulum" z jasnimi priporočili
- Posodobljene povezave MCP specifikacij na pravilne URL-je
- Dodan razdelek o kontekstnem inženiringu (5.14) v strukturo kurikuluma

### Posodobitve študijskega vodnika
- Popolnoma prenovljen študijski vodnik za uskladitev s trenutno strukturo repozitorija
- Dodani novi razdelki za MCP odjemalce in orodja ter priljubljene MCP strežnike
- Posodobljen vizualni zemljevid kurikuluma, da natančno odraža vse teme
- Izboljšani opisi naprednih tem za pokritje vseh specializiranih področij
- Posodobljen razdelek študijskih primerov, da odraža dejanske primere
- Dodan ta celovit dnevnik sprememb

### Prispevki skupnosti (06-CommunityContributions/)
- Dodane podrobne informacije o MCP strežnikih za generiranje slik
- Dodan celovit razdelek o uporabi Claude v VSCode
- Dodana navodila za nastavitev in uporabo terminalskega odjemalca Cline
- Posodobljen razdelek MCP odjemalcev, da vključuje vse priljubljene možnosti odjemalcev
- Izboljšani primeri prispevkov z natančnejšimi vzorci kode

### Napredne teme (05-AdvancedTopics/)
- Organizirane vse mape specializiranih tem z doslednim poimenovanjem
- Dodani materiali in primeri kontekstnega inženiringa
- Dodana dokumentacija za integracijo Foundry agentov
- Izboljšana dokumentacija za integracijo varnosti Entra ID

## 11. junij 2025

### Prva izdaja
- Izdana prva različica kurikuluma MCP za začetnike
- Ustvarjena osnovna struktura za vseh 10 glavnih razdelkov
- Implementiran vizualni zemljevid kurikuluma za navigacijo
- Dodani začetni vzorčni projekti v več programskih jezikih

### Začetek (03-GettingStarted/)
- Ustvarjeni prvi primeri implementacije strežnika
- Dodano vodstvo za razvoj odjemalcev
- Vključena navodila za integracijo LLM odjemalcev
- Dodana dokumentacija za integracijo z VS Code
- Implementirani primeri strežnika z dogodki, poslanimi s strežnika (SSE)

### Osnovni koncepti (01-CoreConcepts/)
- Dodana podrobna razlaga arhitekture odjemalec-strežnik
- Ustvarjena dokumentacija o ključnih komponentah protokola
- Dokumentirani vzorci sporočanja v MCP

## 23. maj 2025

### Struktura repozitorija
- Inicializiran repozitorij z osnovno strukturo map
- Ustvarjeni README datoteke za vsak glavni razdelek
- Nastavljena infrastruktura za prevajanje
- Dodane slikovne datoteke in diagrami

### Dokumentacija
- Ustvarjen začetni README.md s pregledom kurikuluma
- Dodani CODE_OF_CONDUCT.md in SECURITY.md
- Nastavljen SUPPORT.md z navodili za pomoč
- Ustvarjena preliminarna struktura študijskega vodnika

## 15. april 2025

### Načrtovanje in okvir
- Začetno načrtovanje kurikuluma MCP za začetnike
- Določeni učni cilji in ciljno občinstvo
- Obrisana 10-delna struktura kurikuluma
- Razvit konceptualni okvir za primere in študijske primere
- Ustvarjeni začetni prototipni primeri za ključne koncepte

---

**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve AI za prevajanje [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da lahko avtomatizirani prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem maternem jeziku je treba obravnavati kot avtoritativni vir. Za ključne informacije priporočamo profesionalni človeški prevod. Ne prevzemamo odgovornosti za morebitna nesporazumevanja ali napačne razlage, ki izhajajo iz uporabe tega prevoda.