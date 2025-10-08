<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T22:56:12+00:00",
  "source_file": "changelog.md",
  "language_code": "it"
}
-->
# Registro delle modifiche: Curriculum MCP per principianti

Questo documento funge da registro di tutte le modifiche significative apportate al curriculum del Model Context Protocol (MCP) per principianti. Le modifiche sono documentate in ordine cronologico inverso (le modifiche più recenti per prime).

## 6 ottobre 2025

### Espansione della sezione Introduzione – Uso avanzato del server e autenticazione semplice

#### Uso avanzato del server (03-GettingStarted/10-advanced)
- **Nuovo capitolo aggiunto**: Introdotta una guida completa all'uso avanzato del server MCP, che copre sia le architetture server regolari che quelle a basso livello.
  - **Server regolare vs. a basso livello**: Confronto dettagliato e esempi di codice in Python e TypeScript per entrambi gli approcci.
  - **Design basato su handler**: Spiegazione della gestione di strumenti/risorse/prompts basata su handler per implementazioni server scalabili e flessibili.
  - **Pattern pratici**: Scenari reali in cui i pattern server a basso livello sono utili per funzionalità avanzate e architetture.

#### Autenticazione semplice (03-GettingStarted/11-simple-auth)
- **Nuovo capitolo aggiunto**: Guida passo-passo per implementare un'autenticazione semplice nei server MCP.
  - **Concetti di autenticazione**: Spiegazione chiara della differenza tra autenticazione e autorizzazione e gestione delle credenziali.
  - **Implementazione di autenticazione di base**: Pattern di autenticazione basati su middleware in Python (Starlette) e TypeScript (Express), con esempi di codice.
  - **Progressione verso sicurezza avanzata**: Indicazioni su come iniziare con l'autenticazione semplice e avanzare verso OAuth 2.1 e RBAC, con riferimenti a moduli di sicurezza avanzati.

Queste aggiunte forniscono una guida pratica e concreta per costruire implementazioni server MCP più robuste, sicure e flessibili, collegando concetti fondamentali a pattern avanzati di produzione.

## 29 settembre 2025

### Laboratori di integrazione del database del server MCP - Percorso di apprendimento pratico completo

#### 11-MCPServerHandsOnLabs - Nuovo curriculum completo di integrazione del database
- **Percorso di apprendimento completo di 13 laboratori**: Aggiunto un curriculum pratico completo per costruire server MCP pronti per la produzione con integrazione del database PostgreSQL.
  - **Implementazione reale**: Caso d'uso di analisi retail Zava che dimostra pattern di livello enterprise.
  - **Progressione strutturata dell'apprendimento**:
    - **Laboratori 00-03: Fondamenti** - Introduzione, Architettura di base, Sicurezza e multi-tenancy, Configurazione dell'ambiente.
    - **Laboratori 04-06: Costruzione del server MCP** - Design e schema del database, Implementazione del server MCP, Sviluppo degli strumenti.
    - **Laboratori 07-09: Funzionalità avanzate** - Integrazione della ricerca semantica, Test e debug, Integrazione con VS Code.
    - **Laboratori 10-12: Produzione e migliori pratiche** - Strategie di distribuzione, Monitoraggio e osservabilità, Ottimizzazione e migliori pratiche.
  - **Tecnologie enterprise**: Framework FastMCP, PostgreSQL con pgvector, embedding Azure OpenAI, Azure Container Apps, Application Insights.
  - **Funzionalità avanzate**: Sicurezza a livello di riga (RLS), ricerca semantica, accesso ai dati multi-tenant, embedding vettoriali, monitoraggio in tempo reale.

#### Standardizzazione della terminologia - Conversione da modulo a laboratorio
- **Aggiornamento completo della documentazione**: Aggiornati sistematicamente tutti i file README in 11-MCPServerHandsOnLabs per utilizzare la terminologia "Laboratorio" invece di "Modulo".
  - **Intestazioni delle sezioni**: Aggiornato "Cosa copre questo modulo" in "Cosa copre questo laboratorio" in tutti i 13 laboratori.
  - **Descrizione del contenuto**: Modificato "Questo modulo fornisce..." in "Questo laboratorio fornisce..." in tutta la documentazione.
  - **Obiettivi di apprendimento**: Aggiornato "Alla fine di questo modulo..." in "Alla fine di questo laboratorio...".
  - **Link di navigazione**: Convertiti tutti i riferimenti "Modulo XX:" in "Laboratorio XX:" nei riferimenti incrociati e nella navigazione.
  - **Tracciamento del completamento**: Aggiornato "Dopo aver completato questo modulo..." in "Dopo aver completato questo laboratorio...".
  - **Riferimenti tecnici preservati**: Mantenuti i riferimenti ai moduli Python nei file di configurazione (es. `"module": "mcp_server.main"`).

#### Miglioramento della guida di studio (study_guide.md)
- **Mappa visiva del curriculum**: Aggiunta nuova sezione "11. Laboratori di integrazione del database" con visualizzazione completa della struttura dei laboratori.
- **Struttura del repository**: Aggiornata da dieci a undici sezioni principali con descrizione dettagliata di 11-MCPServerHandsOnLabs.
- **Guida al percorso di apprendimento**: Istruzioni di navigazione migliorate per coprire le sezioni 00-11.
- **Copertura tecnologica**: Aggiunti dettagli sull'integrazione di FastMCP, PostgreSQL e servizi Azure.
- **Risultati dell'apprendimento**: Enfatizzato lo sviluppo di server pronti per la produzione, i pattern di integrazione del database e la sicurezza di livello enterprise.

#### Miglioramento della struttura del README principale
- **Terminologia basata sui laboratori**: Aggiornato il README.md principale in 11-MCPServerHandsOnLabs per utilizzare in modo coerente la struttura "Laboratorio".
- **Organizzazione del percorso di apprendimento**: Progressione chiara dai concetti fondamentali attraverso l'implementazione avanzata fino alla distribuzione in produzione.
- **Focus sul mondo reale**: Enfasi sull'apprendimento pratico e concreto con pattern e tecnologie di livello enterprise.

### Miglioramenti alla qualità e alla coerenza della documentazione
- **Enfasi sull'apprendimento pratico**: Rafforzato l'approccio pratico basato sui laboratori in tutta la documentazione.
- **Focus sui pattern enterprise**: Evidenziate implementazioni pronte per la produzione e considerazioni sulla sicurezza di livello enterprise.
- **Integrazione tecnologica**: Copertura completa dei moderni servizi Azure e dei pattern di integrazione AI.
- **Progressione dell'apprendimento**: Percorso chiaro e strutturato dai concetti di base alla distribuzione in produzione.

## 26 settembre 2025

### Miglioramento dei casi studio - Integrazione del registro MCP di GitHub

#### Casi studio (09-CaseStudy/) - Focus sullo sviluppo dell'ecosistema
- **README.md**: Espansione significativa con un caso studio completo sul registro MCP di GitHub.
  - **Caso studio sul registro MCP di GitHub**: Nuovo caso studio completo che esamina il lancio del registro MCP di GitHub a settembre 2025.
    - **Analisi del problema**: Esame dettagliato delle sfide di scoperta e distribuzione frammentata dei server MCP.
    - **Architettura della soluzione**: Approccio centralizzato del registro di GitHub con installazione con un clic in VS Code.
    - **Impatto aziendale**: Miglioramenti misurabili nell'onboarding e nella produttività degli sviluppatori.
    - **Valore strategico**: Focus sulla distribuzione modulare degli agenti e sull'interoperabilità tra strumenti.
    - **Sviluppo dell'ecosistema**: Posizionamento come piattaforma fondamentale per l'integrazione agentica.
  - **Struttura migliorata dei casi studio**: Aggiornati tutti e sette i casi studio con formattazione coerente e descrizioni complete.
    - Azure AI Travel Agents: Enfasi sull'orchestrazione multi-agente.
    - Integrazione con Azure DevOps: Focus sull'automazione dei flussi di lavoro.
    - Recupero della documentazione in tempo reale: Implementazione client console Python.
    - Generatore di piani di studio interattivo: App web conversazionale Chainlit.
    - Documentazione in-editor: Integrazione con VS Code e GitHub Copilot.
    - Gestione API Azure: Pattern di integrazione API di livello enterprise.
    - Registro MCP di GitHub: Sviluppo dell'ecosistema e piattaforma comunitaria.
  - **Conclusione completa**: Riscritta la sezione conclusiva evidenziando sette casi studio che coprono molteplici dimensioni di implementazione MCP.
    - Integrazione enterprise, orchestrazione multi-agente, produttività degli sviluppatori.
    - Sviluppo dell'ecosistema, applicazioni educative.
    - Approfondimenti migliorati sui pattern architetturali, strategie di implementazione e migliori pratiche.
    - Enfasi su MCP come protocollo maturo e pronto per la produzione.

#### Aggiornamenti alla guida di studio (study_guide.md)
- **Mappa visiva del curriculum**: Aggiornata la mappa mentale per includere il registro MCP di GitHub nella sezione Casi studio.
- **Descrizione dei casi studio**: Migliorata da descrizioni generiche a una suddivisione dettagliata di sette casi studio completi.
- **Struttura del repository**: Aggiornata la sezione 10 per riflettere la copertura completa dei casi studio con dettagli specifici di implementazione.
- **Integrazione del registro delle modifiche**: Aggiunta voce del 26 settembre 2025 che documenta l'aggiunta del registro MCP di GitHub e i miglioramenti ai casi studio.
- **Aggiornamenti delle date**: Aggiornato il timestamp del footer per riflettere l'ultima revisione (26 settembre 2025).

### Miglioramenti alla qualità della documentazione
- **Miglioramento della coerenza**: Formattazione e struttura standardizzate dei casi studio in tutti e sette gli esempi.
- **Copertura completa**: I casi studio ora coprono scenari di integrazione enterprise, produttività degli sviluppatori e sviluppo dell'ecosistema.
- **Posizionamento strategico**: Focus migliorato su MCP come piattaforma fondamentale per la distribuzione di sistemi agentici.
- **Integrazione delle risorse**: Aggiornate le risorse aggiuntive per includere il link al registro MCP di GitHub.

## 15 settembre 2025

### Espansione degli argomenti avanzati - Trasporti personalizzati e ingegneria del contesto

#### Trasporti personalizzati MCP (05-AdvancedTopics/mcp-transport/) - Nuova guida avanzata all'implementazione
- **README.md**: Guida completa all'implementazione di meccanismi di trasporto MCP personalizzati.
  - **Trasporto Azure Event Grid**: Implementazione serverless completa basata su eventi.
    - Esempi in C#, TypeScript e Python con integrazione Azure Functions.
    - Pattern architetturali basati su eventi per soluzioni MCP scalabili.
    - Ricevitori webhook e gestione dei messaggi push.
  - **Trasporto Azure Event Hubs**: Implementazione di trasporto streaming ad alta velocità.
    - Capacità di streaming in tempo reale per scenari a bassa latenza.
    - Strategie di partizionamento e gestione dei checkpoint.
    - Ottimizzazione delle prestazioni e batching dei messaggi.
  - **Pattern di integrazione enterprise**: Esempi architetturali pronti per la produzione.
    - Elaborazione MCP distribuita su più Azure Functions.
    - Architetture di trasporto ibride che combinano più tipi di trasporto.
    - Strategie di durabilità, affidabilità e gestione degli errori dei messaggi.
  - **Sicurezza e monitoraggio**: Integrazione con Azure Key Vault e pattern di osservabilità.
    - Autenticazione con identità gestite e accesso con privilegi minimi.
    - Telemetria Application Insights e monitoraggio delle prestazioni.
    - Circuit breaker e pattern di tolleranza agli errori.
  - **Framework di test**: Strategie di test complete per trasporti personalizzati.
    - Test unitari con test doubles e framework di mocking.
    - Test di integrazione con Azure Test Containers.
    - Considerazioni su test di prestazioni e carico.

#### Ingegneria del contesto (05-AdvancedTopics/mcp-contextengineering/) - Disciplina emergente dell'AI
- **README.md**: Esplorazione completa dell'ingegneria del contesto come campo emergente.
  - **Principi fondamentali**: Condivisione completa del contesto, consapevolezza delle decisioni di azione e gestione delle finestre di contesto.
  - **Allineamento al protocollo MCP**: Come il design MCP affronta le sfide dell'ingegneria del contesto.
    - Limitazioni delle finestre di contesto e strategie di caricamento progressivo.
    - Determinazione della rilevanza e recupero dinamico del contesto.
    - Gestione multi-modale del contesto e considerazioni sulla sicurezza.
  - **Approcci di implementazione**: Architetture single-threaded vs. multi-agente.
    - Tecniche di suddivisione e prioritizzazione del contesto.
    - Strategie di caricamento progressivo e compressione del contesto.
    - Approcci stratificati al contesto e ottimizzazione del recupero.
  - **Framework di misurazione**: Metriche emergenti per la valutazione dell'efficacia del contesto.
    - Efficienza degli input, prestazioni, qualità e considerazioni sull'esperienza utente.
    - Approcci sperimentali per l'ottimizzazione del contesto.
    - Analisi dei fallimenti e metodologie di miglioramento.

#### Aggiornamenti alla navigazione del curriculum (README.md)
- **Struttura migliorata dei moduli**: Aggiornata la tabella del curriculum per includere nuovi argomenti avanzati.
  - Aggiunti Ingegneria del contesto (5.14) e Trasporto personalizzato (5.15).
  - Formattazione coerente e link di navigazione in tutti i moduli.
  - Descrizioni aggiornate per riflettere l'ambito attuale dei contenuti.

### Miglioramenti alla struttura delle directory
- **Standardizzazione dei nomi**: Rinominato "mcp transport" in "mcp-transport" per coerenza con altre cartelle di argomenti avanzati.
- **Organizzazione dei contenuti**: Tutte le cartelle 05-AdvancedTopics ora seguono un pattern di denominazione coerente (mcp-[topic]).

### Miglioramenti alla qualità della documentazione
- **Allineamento alla specifica MCP**: Tutti i nuovi contenuti fanno riferimento alla specifica MCP corrente 2025-06-18.
- **Esempi multi-lingua**: Esempi di codice completi in C#, TypeScript e Python.
- **Focus enterprise**: Pattern pronti per la produzione e integrazione cloud Azure in tutto.
- **Documentazione visiva**: Diagrammi Mermaid per visualizzazione di architettura e flussi.

## 18 agosto 2025

### Aggiornamento completo della documentazione - Standard MCP 2025-06-18

#### Migliori pratiche di sicurezza MCP (02-Security/) - Modernizzazione completa
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Riscrittura completa allineata alla specifica MCP 2025-06-18.
  - **Requisiti obbligatori**: Aggiunti requisiti espliciti MUST/MUST NOT dalla specifica ufficiale con chiari indicatori visivi.
  - **12 pratiche di sicurezza fondamentali**: Ristrutturato da una lista di 15 elementi a domini di sicurezza completi.
    - Sicurezza dei token e autenticazione con integrazione di provider di identità esterni.
    - Gestione delle sessioni e sicurezza del trasporto con requisiti crittografici.
    - Protezione dalle minacce specifiche dell'AI con integrazione Microsoft Prompt Shields.
    - Controllo degli accessi e permessi con principio del privilegio minimo.
    - Sicurezza dei contenuti e monitoraggio con integrazione Azure Content Safety.
    - Sicurezza della supply chain con verifica completa dei componenti.
    - Sicurezza OAuth e prevenzione degli attacchi Confused Deputy con implementazione PKCE.
    - Risposta agli incidenti e recupero con capacità automatizzate.
    - Conformità e governance con allineamento normativo.
    - Controlli di sicurezza avanzati con architettura zero trust.
    - Integrazione dell'ecosistema di sicurezza Microsoft con soluzioni complete.
    - Evoluzione continua della sicurezza con pratiche adattive.
  - **Soluzioni di sicurezza Microsoft**: Guida migliorata all'integrazione di Prompt Shields, Azure Content Safety, Entra ID e GitHub Advanced Security.
  - **Risorse di implementazione**: Link a risorse complete categorizzati per Documentazione ufficiale MCP, Soluzioni di sicurezza Microsoft, Standard di sicurezza e Guide di implementazione.

#### Controlli di sicurezza avanzati (02-Security/) - Implementazione enterprise
- **MCP-SECURITY-CONTROLS-2025.md**: Revisione completa con framework di sicurezza di livello enterprise.
  - **9 domini di sicurezza completi**: Espanso da controlli di base a framework dettagliato di livello enterprise.
    - Autenticazione e autorizzazione avanzate con integrazione Microsoft Entra ID.
    - Sicurezza dei token e controlli anti-passthrough con validazione completa.
    - Controlli di sicurezza delle sessioni con prevenzione di hijacking.
    - Controlli di sicurezza specifici dell'AI con prevenzione di injection di prompt e avvelenamento degli strumenti.
    - Prevenzione degli attacchi Confused Deputy con sicurezza proxy OAuth.
    - Sicurezza dell'esecuzione degli strumenti con sandboxing e isolamento.
    - Controlli di sicurezza della supply chain con verifica delle dipendenze.
    - Controlli di monitoraggio e rilevamento con integrazione SIEM.
    - Risposta agli incidenti e recupero con capacità automatizzate.
  - **Esempi di implementazione**: Aggiunti blocchi di configurazione YAML dettagliati e esempi di codice.
  - **Integrazione delle soluzioni Microsoft**: Cop
#### Argomenti Avanzati Sicurezza (05-AdvancedTopics/mcp-security/) - Implementazione Pronta per la Produzione
- **README.md**: Riscrittura completa per l'implementazione della sicurezza aziendale
  - **Allineamento alla Specifica Corrente**: Aggiornato alla Specifica MCP 2025-06-18 con requisiti di sicurezza obbligatori
  - **Autenticazione Avanzata**: Integrazione con Microsoft Entra ID e esempi completi in .NET e Java Spring Security
  - **Integrazione Sicurezza AI**: Implementazione di Microsoft Prompt Shields e Azure Content Safety con esempi dettagliati in Python
  - **Mitigazione Avanzata delle Minacce**: Esempi di implementazione completi per:
    - Prevenzione degli attacchi Confused Deputy con PKCE e validazione del consenso dell'utente
    - Prevenzione del passaggio di token con validazione del pubblico e gestione sicura dei token
    - Prevenzione del dirottamento delle sessioni con binding crittografico e analisi comportamentale
  - **Integrazione Sicurezza Aziendale**: Monitoraggio con Azure Application Insights, pipeline di rilevamento delle minacce e sicurezza della supply chain
  - **Checklist di Implementazione**: Controlli di sicurezza obbligatori vs. raccomandati con i vantaggi dell'ecosistema di sicurezza Microsoft

### Qualità della Documentazione e Allineamento agli Standard
- **Riferimenti alla Specifica**: Aggiornati tutti i riferimenti alla Specifica MCP 2025-06-18
- **Ecosistema di Sicurezza Microsoft**: Guida migliorata per l'integrazione in tutta la documentazione sulla sicurezza
- **Implementazione Pratica**: Aggiunti esempi di codice dettagliati in .NET, Java e Python con modelli aziendali
- **Organizzazione delle Risorse**: Categorizzazione completa della documentazione ufficiale, degli standard di sicurezza e delle guide di implementazione
- **Indicatori Visivi**: Chiarezza tra requisiti obbligatori e pratiche raccomandate

#### Concetti Fondamentali (01-CoreConcepts/) - Modernizzazione Completa
- **Aggiornamento Versione Protocollo**: Aggiornato per fare riferimento alla Specifica MCP 2025-06-18 con versionamento basato sulla data (formato YYYY-MM-DD)
- **Raffinamento dell'Architettura**: Descrizioni migliorate di Host, Client e Server per riflettere i modelli di architettura MCP attuali
  - Gli Host ora definiti chiaramente come applicazioni AI che coordinano più connessioni client MCP
  - I Client descritti come connettori di protocollo che mantengono relazioni uno-a-uno con i server
  - I Server migliorati con scenari di distribuzione locale vs. remota
- **Ristrutturazione delle Primitivi**: Revisione completa delle primitive di server e client
  - Primitive del Server: Risorse (fonti di dati), Prompt (modelli), Strumenti (funzioni eseguibili) con spiegazioni ed esempi dettagliati
  - Primitive del Client: Campionamento (completamenti LLM), Elicitazione (input utente), Logging (debug/monitoraggio)
  - Aggiornato con i modelli di metodo attuali di scoperta (`*/list`), recupero (`*/get`) ed esecuzione (`*/call`)
- **Architettura del Protocollo**: Introdotto un modello di architettura a due livelli
  - Livello Dati: Fondazione JSON-RPC 2.0 con gestione del ciclo di vita e primitive
  - Livello Trasporto: STDIO (locale) e HTTP Streamable con SSE (remoto) come meccanismi di trasporto
- **Framework di Sicurezza**: Principi di sicurezza completi, inclusi consenso esplicito dell'utente, protezione della privacy dei dati, sicurezza nell'esecuzione degli strumenti e sicurezza del livello di trasporto
- **Modelli di Comunicazione**: Messaggi del protocollo aggiornati per mostrare flussi di inizializzazione, scoperta, esecuzione e notifiche
- **Esempi di Codice**: Esempi multi-lingua aggiornati (.NET, Java, Python, JavaScript) per riflettere i modelli SDK MCP attuali

#### Sicurezza (02-Security/) - Revisione Completa della Sicurezza  
- **Allineamento agli Standard**: Allineamento completo ai requisiti di sicurezza della Specifica MCP 2025-06-18
- **Evoluzione dell'Autenticazione**: Documentata l'evoluzione dai server OAuth personalizzati alla delega a provider di identità esterni (Microsoft Entra ID)
- **Analisi delle Minacce Specifiche per l'AI**: Copertura migliorata dei moderni vettori di attacco AI
  - Scenari dettagliati di attacchi di injection nei prompt con esempi reali
  - Meccanismi di avvelenamento degli strumenti e modelli di attacco "rug pull"
  - Avvelenamento della finestra contestuale e attacchi di confusione del modello
- **Soluzioni di Sicurezza AI Microsoft**: Copertura completa dell'ecosistema di sicurezza Microsoft
  - Prompt Shields AI con tecniche avanzate di rilevamento, spotlighting e delimitazione
  - Modelli di integrazione di Azure Content Safety
  - Sicurezza avanzata di GitHub per la protezione della supply chain
- **Mitigazione Avanzata delle Minacce**: Controlli di sicurezza dettagliati per:
  - Dirottamento delle sessioni con scenari di attacco specifici MCP e requisiti crittografici per ID di sessione
  - Problemi di Confused Deputy negli scenari proxy MCP con requisiti di consenso espliciti
  - Vulnerabilità del passaggio di token con controlli di validazione obbligatori
- **Sicurezza della Supply Chain**: Copertura ampliata della supply chain AI, inclusi modelli di base, servizi di embedding, fornitori di contesto e API di terze parti
- **Sicurezza Fondamentale**: Integrazione migliorata con modelli di sicurezza aziendale, inclusa l'architettura zero trust e l'ecosistema di sicurezza Microsoft
- **Organizzazione delle Risorse**: Collegamenti alle risorse categorizzati per tipo (Documentazione Ufficiale, Standard, Ricerca, Soluzioni Microsoft, Guide di Implementazione)

### Miglioramenti alla Qualità della Documentazione
- **Obiettivi di Apprendimento Strutturati**: Obiettivi di apprendimento migliorati con risultati specifici e attuabili
- **Riferimenti Incrociati**: Aggiunti collegamenti tra argomenti correlati di sicurezza e concetti fondamentali
- **Informazioni Aggiornate**: Aggiornati tutti i riferimenti alle date e i collegamenti alle specifiche agli standard attuali
- **Guida all'Implementazione**: Aggiunte linee guida di implementazione specifiche e attuabili in tutte le sezioni

## 16 Luglio 2025

### Miglioramenti a README e Navigazione
- Navigazione del curriculum completamente ridisegnata in README.md
- Sostituiti i tag `<details>` con un formato basato su tabelle più accessibile
- Creato opzioni di layout alternative nella nuova cartella "alternative_layouts"
- Aggiunti esempi di navigazione in stile schede, a schede e a fisarmonica
- Aggiornata la sezione sulla struttura del repository per includere tutti i file più recenti
- Migliorata la sezione "Come Utilizzare Questo Curriculum" con raccomandazioni chiare
- Aggiornati i collegamenti alle specifiche MCP per puntare agli URL corretti
- Aggiunta la sezione di Ingegneria del Contesto (5.14) alla struttura del curriculum

### Aggiornamenti alla Guida di Studio
- Guida di studio completamente rivista per allinearsi alla struttura del repository attuale
- Aggiunte nuove sezioni per Client MCP e Strumenti, e Server MCP Popolari
- Aggiornata la Mappa Visiva del Curriculum per riflettere accuratamente tutti gli argomenti
- Migliorate le descrizioni degli Argomenti Avanzati per coprire tutte le aree specializzate
- Aggiornata la sezione Studi di Caso per riflettere esempi reali
- Aggiunto questo changelog completo

### Contributi della Comunità (06-CommunityContributions/)
- Aggiunte informazioni dettagliate sui server MCP per la generazione di immagini
- Aggiunta una sezione completa sull'utilizzo di Claude in VSCode
- Aggiunte istruzioni per la configurazione e l'utilizzo del client terminale Cline
- Aggiornata la sezione client MCP per includere tutte le opzioni client popolari
- Migliorati gli esempi di contributo con campioni di codice più accurati

### Argomenti Avanzati (05-AdvancedTopics/)
- Organizzate tutte le cartelle di argomenti specializzati con una nomenclatura coerente
- Aggiunti materiali ed esempi di ingegneria del contesto
- Aggiunta documentazione sull'integrazione degli agenti Foundry
- Migliorata la documentazione sull'integrazione della sicurezza Entra ID

## 11 Giugno 2025

### Creazione Iniziale
- Rilasciata la prima versione del curriculum MCP per Principianti
- Creata la struttura di base per tutte le 10 sezioni principali
- Implementata la Mappa Visiva del Curriculum per la navigazione
- Aggiunti progetti di esempio iniziali in più linguaggi di programmazione

### Introduzione (03-GettingStarted/)
- Creati i primi esempi di implementazione del server
- Aggiunta guida allo sviluppo del client
- Incluse istruzioni per l'integrazione del client LLM
- Aggiunta documentazione per l'integrazione con VS Code
- Implementati esempi di server con Server-Sent Events (SSE)

### Concetti Fondamentali (01-CoreConcepts/)
- Aggiunta spiegazione dettagliata dell'architettura client-server
- Creata documentazione sui componenti chiave del protocollo
- Documentati i modelli di messaggistica in MCP

## 23 Maggio 2025

### Struttura del Repository
- Inizializzato il repository con una struttura di cartelle di base
- Creati file README per ogni sezione principale
- Configurata l'infrastruttura di traduzione
- Aggiunti asset e diagrammi di immagini

### Documentazione
- Creato README.md iniziale con panoramica del curriculum
- Aggiunti CODE_OF_CONDUCT.md e SECURITY.md
- Configurato SUPPORT.md con indicazioni per ottenere aiuto
- Creata struttura preliminare della guida di studio

## 15 Aprile 2025

### Pianificazione e Framework
- Pianificazione iniziale per il curriculum MCP per Principianti
- Definiti obiettivi di apprendimento e pubblico target
- Delineata la struttura in 10 sezioni del curriculum
- Sviluppato framework concettuale per esempi e studi di caso
- Creati prototipi iniziali per i concetti chiave

---

**Clausola di esclusione della responsabilità**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa dovrebbe essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un traduttore umano. Non siamo responsabili per eventuali incomprensioni o interpretazioni errate derivanti dall'uso di questa traduzione.