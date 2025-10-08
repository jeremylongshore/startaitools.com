<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:58:44+00:00",
  "source_file": "changelog.md",
  "language_code": "ro"
}
-->
# Jurnal de modificări: Curriculum MCP pentru Începători

Acest document servește ca o înregistrare a tuturor modificărilor semnificative aduse curriculumului Model Context Protocol (MCP) pentru Începători. Modificările sunt documentate în ordine invers cronologică (cele mai recente modificări primele).

## 6 octombrie 2025

### Extinderea secțiunii Introducere – Utilizare avansată a serverului și autentificare simplă

#### Utilizare avansată a serverului (03-GettingStarted/10-advanced)
- **Capitol nou adăugat**: Ghid cuprinzător pentru utilizarea avansată a serverului MCP, acoperind atât arhitecturile serverului obișnuit, cât și cele de nivel scăzut.
  - **Server obișnuit vs. de nivel scăzut**: Comparație detaliată și exemple de cod în Python și TypeScript pentru ambele abordări.
  - **Design bazat pe handler**: Explicație despre gestionarea scalabilă și flexibilă a instrumentelor/resurselor/prompts prin design bazat pe handler.
  - **Modele practice**: Scenarii reale în care modelele de server de nivel scăzut sunt benefice pentru funcționalități avansate și arhitectură.

#### Autentificare simplă (03-GettingStarted/11-simple-auth)
- **Capitol nou adăugat**: Ghid pas cu pas pentru implementarea autentificării simple în serverele MCP.
  - **Concepte de autentificare**: Explicație clară despre diferența dintre autentificare și autorizare, și gestionarea acreditivelor.
  - **Implementare de autentificare de bază**: Modele de autentificare bazate pe middleware în Python (Starlette) și TypeScript (Express), cu exemple de cod.
  - **Progresie către securitate avansată**: Ghid pentru trecerea de la autentificare simplă la OAuth 2.1 și RBAC, cu referințe la modulele de securitate avansată.

Aceste adăugiri oferă îndrumări practice pentru construirea unor implementări de server MCP mai robuste, sigure și flexibile, făcând legătura între conceptele fundamentale și modelele avansate de producție.

## 29 septembrie 2025

### Laboratoare de integrare a bazei de date pentru serverul MCP - Parcurs de învățare practic cuprinzător

#### 11-MCPServerHandsOnLabs - Curriculum complet pentru integrarea bazei de date
- **Parcurs de învățare cu 13 laboratoare complete**: Adăugat curriculum practic cuprinzător pentru construirea serverelor MCP pregătite pentru producție cu integrare PostgreSQL.
  - **Implementare reală**: Studiu de caz Zava Retail Analytics demonstrând modele de nivel enterprise.
  - **Progresie structurată a învățării**:
    - **Laboratoare 00-03: Fundamente** - Introducere, Arhitectură de bază, Securitate și multi-tenancy, Configurare mediu
    - **Laboratoare 04-06: Construirea serverului MCP** - Design și schemă bază de date, Implementare server MCP, Dezvoltare instrumente  
    - **Laboratoare 07-09: Funcționalități avansate** - Integrare căutare semantică, Testare și depanare, Integrare VS Code
    - **Laboratoare 10-12: Producție și bune practici** - Strategii de implementare, Monitorizare și observabilitate, Optimizare și bune practici
  - **Tehnologii enterprise**: Framework FastMCP, PostgreSQL cu pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights
  - **Funcționalități avansate**: Securitate la nivel de rând (RLS), căutare semantică, acces multi-tenant la date, embeddings vectoriale, monitorizare în timp real

#### Standardizarea terminologiei - Conversia modulelor în laboratoare
- **Actualizare cuprinzătoare a documentației**: Actualizate sistematic toate fișierele README din 11-MCPServerHandsOnLabs pentru utilizarea terminologiei "Laborator" în loc de "Modul".
  - **Titluri secțiuni**: Actualizat "Ce acoperă acest modul" în "Ce acoperă acest laborator" în toate cele 13 laboratoare.
  - **Descriere conținut**: Schimbat "Acest modul oferă..." în "Acest laborator oferă..." în întreaga documentație.
  - **Obiective de învățare**: Actualizat "Până la finalul acestui modul..." în "Până la finalul acestui laborator..."
  - **Linkuri de navigare**: Convertit toate referințele "Modul XX:" în "Laborator XX:" în referințele încrucișate și navigare.
  - **Urmărirea progresului**: Actualizat "După finalizarea acestui modul..." în "După finalizarea acestui laborator..."
  - **Referințe tehnice păstrate**: Menținute referințele la modulele Python în fișierele de configurare (ex.: `"module": "mcp_server.main"`).

#### Îmbunătățirea ghidului de studiu (study_guide.md)
- **Hartă vizuală a curriculumului**: Adăugată secțiunea nouă "11. Laboratoare de integrare a bazei de date" cu vizualizarea structurii laboratoarelor.
- **Structura depozitului**: Actualizat de la zece la unsprezece secțiuni principale cu descriere detaliată a 11-MCPServerHandsOnLabs.
- **Ghid pentru parcursul de învățare**: Îmbunătățite instrucțiunile de navigare pentru a acoperi secțiunile 00-11.
- **Acoperirea tehnologiilor**: Adăugate detalii despre integrarea FastMCP, PostgreSQL, și serviciile Azure.
- **Rezultate ale învățării**: Accentuat dezvoltarea serverelor pregătite pentru producție, modelele de integrare a bazei de date și securitatea enterprise.

#### Îmbunătățirea structurii README principale
- **Terminologie bazată pe laboratoare**: Actualizat README.md principal în 11-MCPServerHandsOnLabs pentru utilizarea consistentă a structurii "Laborator".
- **Organizarea parcursului de învățare**: Progresie clară de la concepte fundamentale la implementare avansată și implementare în producție.
- **Focus pe realitate**: Accent pe învățare practică, cu modele și tehnologii de nivel enterprise.

### Îmbunătățiri ale calității și consistenței documentației
- **Accent pe învățarea practică**: Consolidat abordarea practică, bazată pe laboratoare, în întreaga documentație.
- **Focus pe modele enterprise**: Evidențiat implementările pregătite pentru producție și considerațiile de securitate enterprise.
- **Integrarea tehnologiilor**: Acoperire cuprinzătoare a serviciilor moderne Azure și a modelelor de integrare AI.
- **Progresia învățării**: Parcurs clar și structurat de la concepte de bază la implementare în producție.

## 26 septembrie 2025

### Îmbunătățirea studiilor de caz - Integrarea registrului MCP GitHub

#### Studii de caz (09-CaseStudy/) - Focus pe dezvoltarea ecosistemului
- **README.md**: Extindere majoră cu studiu de caz cuprinzător despre registrul MCP GitHub.
  - **Studiu de caz Registrul MCP GitHub**: Studiu de caz nou, cuprinzător, examinând lansarea registrului MCP GitHub în septembrie 2025.
    - **Analiza problemei**: Examinare detaliată a provocărilor fragmentării descoperirii și implementării serverelor MCP.
    - **Arhitectura soluției**: Abordarea registrului centralizat GitHub cu instalare cu un singur clic în VS Code.
    - **Impactul asupra afacerii**: Îmbunătățiri măsurabile în onboarding-ul și productivitatea dezvoltatorilor.
    - **Valoare strategică**: Focus pe implementarea modulară a agenților și interoperabilitatea între instrumente.
    - **Dezvoltarea ecosistemului**: Poziționare ca platformă fundamentală pentru integrarea agentică.
  - **Structură îmbunătățită a studiilor de caz**: Actualizate toate cele șapte studii de caz cu formatare consistentă și descrieri cuprinzătoare.
    - Agenți AI pentru călătorii Azure: Accent pe orchestrarea multi-agent.
    - Integrarea Azure DevOps: Focus pe automatizarea fluxurilor de lucru.
    - Recuperarea documentației în timp real: Implementare client console Python.
    - Generator interactiv de planuri de studiu: Aplicație web conversațională Chainlit.
    - Documentație în editor: Integrare VS Code și GitHub Copilot.
    - Managementul API Azure: Modele de integrare API enterprise.
    - Registrul MCP GitHub: Dezvoltarea ecosistemului și platforma comunității.
  - **Concluzie cuprinzătoare**: Rescrierea secțiunii de concluzie evidențiind cele șapte studii de caz care acoperă multiple dimensiuni ale implementării MCP.
    - Integrare enterprise, orchestrare multi-agent, productivitatea dezvoltatorilor.
    - Dezvoltarea ecosistemului, aplicații educaționale.
    - Perspective îmbunătățite asupra modelelor arhitecturale, strategiilor de implementare și bunelor practici.
    - Accent pe MCP ca protocol matur, pregătit pentru producție.

#### Actualizări ghid de studiu (study_guide.md)
- **Hartă vizuală a curriculumului**: Actualizat mindmap-ul pentru a include registrul MCP GitHub în secțiunea Studii de caz.
- **Descrierea studiilor de caz**: Îmbunătățită de la descrieri generice la detalii despre cele șapte studii de caz cuprinzătoare.
- **Structura depozitului**: Actualizat secțiunea 10 pentru a reflecta acoperirea cuprinzătoare a studiilor de caz cu detalii specifice de implementare.
- **Integrarea jurnalului de modificări**: Adăugată intrarea din 26 septembrie 2025 documentând adăugarea registrului MCP GitHub și îmbunătățirile studiilor de caz.
- **Actualizări de dată**: Actualizat timestamp-ul din footer pentru a reflecta ultima revizuire (26 septembrie 2025).

### Îmbunătățiri ale calității documentației
- **Îmbunătățirea consistenței**: Standardizarea formatării și structurii studiilor de caz în toate cele șapte exemple.
- **Acoperire cuprinzătoare**: Studiile de caz acoperă acum scenarii enterprise, productivitatea dezvoltatorilor și dezvoltarea ecosistemului.
- **Poziționare strategică**: Accent îmbunătățit pe MCP ca platformă fundamentală pentru implementarea sistemelor agentice.
- **Integrarea resurselor**: Actualizat resursele suplimentare pentru a include linkul registrului MCP GitHub.

## 15 septembrie 2025

### Extinderea subiectelor avansate - Transports personalizate și ingineria contextului

#### Transports personalizate MCP (05-AdvancedTopics/mcp-transport/) - Ghid nou de implementare avansată
- **README.md**: Ghid complet de implementare pentru mecanismele de transport personalizate MCP.
  - **Transport Azure Event Grid**: Implementare serverless completă pentru transport bazat pe evenimente.
    - Exemple în C#, TypeScript și Python cu integrare Azure Functions.
    - Modele arhitecturale bazate pe evenimente pentru soluții MCP scalabile.
    - Recepționare webhook și gestionare mesaje push.
  - **Transport Azure Event Hubs**: Implementare de transport streaming cu debit ridicat.
    - Capacități de streaming în timp real pentru scenarii cu latență redusă.
    - Strategii de partiționare și gestionare checkpoint.
    - Optimizare performanță și batching mesaje.
  - **Modele de integrare enterprise**: Exemple arhitecturale pregătite pentru producție.
    - Procesare MCP distribuită pe multiple funcții Azure.
    - Arhitecturi hibride de transport combinând mai multe tipuri de transport.
    - Durabilitate mesaje, fiabilitate și strategii de gestionare erori.
  - **Securitate și monitorizare**: Integrare Azure Key Vault și modele de observabilitate.
    - Autentificare cu identitate gestionată și acces cu privilegii minime.
    - Telemetrie Application Insights și monitorizare performanță.
    - Modele de toleranță la erori și întrerupătoare de circuit.
  - **Framework-uri de testare**: Strategii cuprinzătoare de testare pentru transports personalizate.
    - Testare unitară cu dubluri de test și framework-uri de mocking.
    - Testare de integrare cu containere de test Azure.
    - Considerații pentru testare de performanță și încărcare.

#### Ingineria contextului (05-AdvancedTopics/mcp-contextengineering/) - Disciplină emergentă AI
- **README.md**: Explorare cuprinzătoare a ingineriei contextului ca domeniu emergent.
  - **Principii de bază**: Partajare completă a contextului, conștientizare decizională și gestionarea ferestrei de context.
  - **Alinierea la protocolul MCP**: Cum designul MCP abordează provocările ingineriei contextului.
    - Limitări ale ferestrei de context și strategii de încărcare progresivă.
    - Determinarea relevanței și recuperarea dinamică a contextului.
    - Gestionarea contextului multi-modal și considerații de securitate.
  - **Abordări de implementare**: Arhitecturi single-threaded vs. multi-agent.
    - Tehnici de fragmentare și prioritizare a contextului.
    - Strategii de încărcare progresivă și comprimare a contextului.
    - Abordări stratificate ale contextului și optimizarea recuperării.
  - **Cadru de măsurare**: Metrici emergente pentru evaluarea eficienței contextului.
    - Eficiența inputului, performanță, calitate și considerații de experiență utilizator.
    - Abordări experimentale pentru optimizarea contextului.
    - Analiza eșecurilor și metodologii de îmbunătățire.

#### Actualizări navigare curriculum (README.md)
- **Structură îmbunătățită a modulelor**: Actualizat tabelul curriculumului pentru a include subiectele avansate noi.
  - Adăugate Ingineria Contextului (5.14) și Transport Personalizat (5.15).
  - Formatare consistentă și linkuri de navigare în toate modulele.
  - Descrieri actualizate pentru a reflecta domeniul actual al conținutului.

### Îmbunătățiri ale structurii directoarelor
- **Standardizarea denumirilor**: Redenumit "mcp transport" în "mcp-transport" pentru consistență cu alte foldere de subiecte avansate.
- **Organizarea conținutului**: Toate folderele 05-AdvancedTopics urmează acum un model de denumire consistent (mcp-[subiect]).

### Îmbunătățiri ale calității documentației
- **Alinierea la specificația MCP**: Tot conținutul nou face referire la specificația MCP actuală 2025-06-18.
- **Exemple multi-limbaj**: Exemple de cod cuprinzătoare în C#, TypeScript și Python.
- **Focus enterprise**: Modele pregătite pentru producție și integrare cloud Azure în întregul conținut.
- **Documentație vizuală**: Diagrame Mermaid pentru vizualizarea arhitecturii și fluxurilor.

## 18 august 2025

### Actualizare cuprinzătoare a documentației - Standarde MCP 2025-06-18

#### Cele mai bune practici de securitate MCP (02-Security/) - Modernizare completă
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Rescriere completă aliniată la specificația MCP 2025-06-18.
  - **Cerințe obligatorii**: Adăugate cerințe explicite MUST/MUST NOT din specificația oficială cu indicatori vizuali clari.
  - **12 Practici de securitate de bază**: Restructurate dintr-o listă de 15 elemente în domenii de securitate cuprinzătoare.
    - Securitatea token-urilor și autentificare cu integrare furnizor extern de identitate.
    - Managementul sesiunilor și securitatea transportului cu cerințe criptografice.
    - Protecție împotriva amenințărilor AI cu integrarea Microsoft Prompt Shields.
    - Controlul accesului și permisiunilor cu principiul privilegiului minim.
    - Siguranța conținutului și monitorizare cu integrarea Azure Content Safety.
    - Securitatea lanțului de aprovizionare cu verificarea cuprinzătoare a componentelor.
    - Securitatea OAuth și prevenirea atacurilor Confused Deputy cu implementarea PKCE.
    - Răspuns la incidente și recuperare cu capabilități automatizate.
    - Conformitate și guvernanță cu aliniere la reglementări.
    - Controale avansate de securitate cu arhitectură zero trust.
    - Integrarea ecosistemului de securitate Microsoft cu soluții cuprinzăto
#### Subiecte Avansate de Securitate (05-AdvancedTopics/mcp-security/) - Implementare Pregătită pentru Producție
- **README.md**: Rescriere completă pentru implementarea securității la nivel enterprise
  - **Aliniere la Specificațiile Curente**: Actualizat conform Specificației MCP 2025-06-18 cu cerințe obligatorii de securitate
  - **Autentificare Avansată**: Integrare Microsoft Entra ID cu exemple detaliate pentru .NET și Java Spring Security
  - **Integrare Securitate AI**: Implementare Microsoft Prompt Shields și Azure Content Safety cu exemple detaliate în Python
  - **Mitigare Avansată a Amenințărilor**: Exemple de implementare cuprinzătoare pentru
    - Prevenirea atacurilor de tip Confused Deputy prin PKCE și validarea consimțământului utilizatorului
    - Prevenirea transmiterii token-urilor prin validarea audienței și gestionarea securizată a token-urilor
    - Prevenirea deturnării sesiunilor prin legături criptografice și analiză comportamentală
  - **Integrare Securitate Enterprise**: Monitorizare Azure Application Insights, pipeline-uri de detectare a amenințărilor și securitatea lanțului de aprovizionare
  - **Lista de Verificare pentru Implementare**: Controale de securitate clare, obligatorii vs. recomandate, cu beneficii ale ecosistemului de securitate Microsoft

### Calitatea Documentației & Alinierea la Standardele Curente
- **Referințe la Specificații**: Actualizate toate referințele conform Specificației MCP 2025-06-18
- **Ecosistemul de Securitate Microsoft**: Ghiduri de integrare îmbunătățite în toată documentația de securitate
- **Implementare Practică**: Adăugate exemple detaliate de cod în .NET, Java și Python cu modele enterprise
- **Organizarea Resurselor**: Categorisire cuprinzătoare a documentației oficiale, standardelor de securitate și ghidurilor de implementare
- **Indicatori Vizuali**: Marcarea clară a cerințelor obligatorii vs. practicilor recomandate

#### Concepte de Bază (01-CoreConcepts/) - Modernizare Completă
- **Actualizare Versiune Protocol**: Actualizat pentru a face referire la Specificația MCP 2025-06-18 cu versiuni bazate pe date (format YYYY-MM-DD)
- **Rafinarea Arhitecturii**: Descrieri îmbunătățite ale Gazdelor, Clienților și Serverelor pentru a reflecta modelele actuale de arhitectură MCP
  - Gazdele sunt acum definite clar ca aplicații AI care coordonează multiple conexiuni ale clienților MCP
  - Clienții descriși ca conectori de protocol care mențin relații unu-la-unu cu serverele
  - Serverele îmbunătățite cu scenarii de implementare locală vs. la distanță
- **Restructurarea Primitivelor**: Revizuire completă a primitivelor server și client
  - Primitive Server: Resurse (surse de date), Prompts (șabloane), Tools (funcții executabile) cu explicații și exemple detaliate
  - Primitive Client: Sampling (completări LLM), Elicitation (input utilizator), Logging (debugging/monitorizare)
  - Actualizat cu modelele curente de descoperire (`*/list`), recuperare (`*/get`) și execuție (`*/call`)
- **Arhitectura Protocolului**: Introducerea unui model de arhitectură pe două straturi
  - Strat de Date: Fundație JSON-RPC 2.0 cu gestionarea ciclului de viață și primitive
  - Strat de Transport: STDIO (local) și HTTP Streamable cu SSE (la distanță)
- **Cadru de Securitate**: Principii de securitate cuprinzătoare, inclusiv consimțământ explicit al utilizatorului, protecția confidențialității datelor, siguranța execuției instrumentelor și securitatea stratului de transport
- **Modele de Comunicare**: Mesaje de protocol actualizate pentru a arăta fluxurile de inițializare, descoperire, execuție și notificare
- **Exemple de Cod**: Exemple multi-limbaj actualizate (.NET, Java, Python, JavaScript) pentru a reflecta modelele curente MCP SDK

#### Securitate (02-Security/) - Revizuire Completă a Securității  
- **Alinierea la Standardele Curente**: Aliniere completă cu cerințele de securitate ale Specificației MCP 2025-06-18
- **Evoluția Autentificării**: Documentarea evoluției de la servere OAuth personalizate la delegarea furnizorilor externi de identitate (Microsoft Entra ID)
- **Analiza Amenințărilor AI**: Acoperire îmbunătățită a vectorilor moderni de atac AI
  - Scenarii detaliate de atac prin injectare de prompturi cu exemple din lumea reală
  - Mecanisme de otrăvire a instrumentelor și modele de atac "rug pull"
  - Otrăvirea ferestrei de context și atacuri de confuzie a modelului
- **Soluții de Securitate AI Microsoft**: Acoperire cuprinzătoare a ecosistemului de securitate Microsoft
  - AI Prompt Shields cu tehnici avansate de detectare, evidențiere și delimitare
  - Modele de integrare Azure Content Safety
  - GitHub Advanced Security pentru protecția lanțului de aprovizionare
- **Mitigare Avansată a Amenințărilor**: Controale de securitate detaliate pentru
  - Deturnarea sesiunilor cu scenarii de atac specifice MCP și cerințe criptografice pentru ID-ul sesiunii
  - Probleme de tip Confused Deputy în scenarii proxy MCP cu cerințe explicite de consimțământ
  - Vulnerabilități de transmitere a token-urilor cu controale obligatorii de validare
- **Securitatea Lanțului de Aprovizionare**: Acoperire extinsă a lanțului de aprovizionare AI, inclusiv modele de bază, servicii de embeddings, furnizori de context și API-uri terțe
- **Securitate Fundamentală**: Integrare îmbunătățită cu modelele de securitate enterprise, inclusiv arhitectura zero trust și ecosistemul de securitate Microsoft
- **Organizarea Resurselor**: Linkuri cuprinzătoare la resurse categorisite pe tip (Documentație Oficială, Standarde, Cercetare, Soluții Microsoft, Ghiduri de Implementare)

### Îmbunătățiri ale Calității Documentației
- **Obiective Structurate de Învățare**: Obiective de învățare îmbunătățite cu rezultate specifice și acționabile
- **Referințe Încrocișate**: Adăugate linkuri între subiectele de securitate și conceptele de bază
- **Informații Curente**: Actualizate toate referințele de date și linkurile la specificații conform standardelor curente
- **Ghiduri de Implementare**: Adăugate ghiduri specifice și acționabile de implementare în toate secțiunile

## 16 iulie 2025

### Îmbunătățiri README și Navigare
- Redesenarea completă a navigării în README.md
- Înlocuirea tagurilor `<details>` cu format tabelar mai accesibil
- Crearea opțiunilor de layout alternativ în noul folder "alternative_layouts"
- Adăugarea exemplelor de navigare în stil carduri, taburi și acordeon
- Actualizarea secțiunii de structură a depozitului pentru a include toate fișierele recente
- Îmbunătățirea secțiunii "Cum să folosești acest curriculum" cu recomandări clare
- Actualizarea linkurilor la specificațiile MCP pentru a indica URL-urile corecte
- Adăugarea secțiunii de Inginerie Contextuală (5.14) în structura curriculumului

### Actualizări Ghid de Studiu
- Revizuirea completă a ghidului de studiu pentru alinierea la structura curentă a depozitului
- Adăugarea de secțiuni noi pentru Clienți MCP și Instrumente, și Servere MCP Populare
- Actualizarea Hărții Vizuale a Curriculumului pentru a reflecta toate subiectele
- Îmbunătățirea descrierilor Subiectelor Avansate pentru a acoperi toate domeniile specializate
- Actualizarea secțiunii Studii de Caz pentru a reflecta exemple reale
- Adăugarea acestui changelog cuprinzător

### Contribuții Comunitare (06-CommunityContributions/)
- Adăugarea informațiilor detaliate despre serverele MCP pentru generarea de imagini
- Adăugarea unei secțiuni cuprinzătoare despre utilizarea Claude în VSCode
- Adăugarea instrucțiunilor de configurare și utilizare pentru clientul terminal Cline
- Actualizarea secțiunii de clienți MCP pentru a include toate opțiunile populare de clienți
- Îmbunătățirea exemplelor de contribuții cu mostre de cod mai precise

### Subiecte Avansate (05-AdvancedTopics/)
- Organizarea tuturor folderelor de subiecte specializate cu denumiri consistente
- Adăugarea materialelor și exemplelor de inginerie contextuală
- Adăugarea documentației de integrare pentru agenții Foundry
- Îmbunătățirea documentației de integrare a securității Entra ID

## 11 iunie 2025

### Creare Inițială
- Lansarea primei versiuni a curriculumului MCP pentru Începători
- Crearea structurii de bază pentru toate cele 10 secțiuni principale
- Implementarea Hărții Vizuale a Curriculumului pentru navigare
- Adăugarea proiectelor de exemplu inițiale în mai multe limbaje de programare

### Început (03-GettingStarted/)
- Crearea primelor exemple de implementare server
- Adăugarea ghidului de dezvoltare pentru clienți
- Incluzionarea instrucțiunilor de integrare a clienților LLM
- Adăugarea documentației de integrare VS Code
- Implementarea exemplelor de server cu Server-Sent Events (SSE)

### Concepte de Bază (01-CoreConcepts/)
- Adăugarea explicațiilor detaliate despre arhitectura client-server
- Crearea documentației despre componentele cheie ale protocolului
- Documentarea modelelor de mesagerie în MCP

## 23 mai 2025

### Structura Depozitului
- Inițializarea depozitului cu structura de bază a folderelor
- Crearea fișierelor README pentru fiecare secțiune majoră
- Configurarea infrastructurii de traducere
- Adăugarea resurselor de imagine și diagramelor

### Documentație
- Crearea README.md inițial cu o privire de ansamblu asupra curriculumului
- Adăugarea CODE_OF_CONDUCT.md și SECURITY.md
- Configurarea SUPPORT.md cu ghiduri pentru obținerea ajutorului
- Crearea structurii preliminare a ghidului de studiu

## 15 aprilie 2025

### Planificare și Cadru
- Planificarea inițială pentru curriculumul MCP pentru Începători
- Definirea obiectivelor de învățare și a publicului țintă
- Schițarea structurii de 10 secțiuni a curriculumului
- Dezvoltarea cadrului conceptual pentru exemple și studii de caz
- Crearea prototipurilor inițiale pentru conceptele cheie

---

**Declinare de responsabilitate**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim să asigurăm acuratețea, vă rugăm să fiți conștienți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa natală ar trebui considerat sursa autoritară. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care pot apărea din utilizarea acestei traduceri.