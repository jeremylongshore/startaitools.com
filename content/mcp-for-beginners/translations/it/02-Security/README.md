<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T17:29:49+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "it"
}
-->
# Sicurezza MCP: Protezione Completa per i Sistemi AI

[![MCP Security Best Practices](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.it.png)](https://youtu.be/88No8pw706o)

_(Clicca sull'immagine sopra per guardare il video di questa lezione)_

La sicurezza è fondamentale nella progettazione dei sistemi AI, motivo per cui la trattiamo come la nostra seconda sezione. Questo è in linea con il principio di Microsoft **Secure by Design** della [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Il Model Context Protocol (MCP) introduce nuove potenti capacità per le applicazioni basate sull'AI, ma anche sfide di sicurezza uniche che vanno oltre i rischi tradizionali del software. I sistemi MCP affrontano sia problemi di sicurezza consolidati (codifica sicura, minimo privilegio, sicurezza della supply chain) sia nuove minacce specifiche per l'AI, come l'iniezione di prompt, l'avvelenamento degli strumenti, il dirottamento delle sessioni, gli attacchi "confused deputy", le vulnerabilità di token passthrough e la modifica dinamica delle capacità.

Questa lezione esplora i rischi di sicurezza più critici nelle implementazioni MCP, trattando autenticazione, autorizzazione, permessi eccessivi, iniezione indiretta di prompt, sicurezza delle sessioni, problemi di "confused deputy", gestione dei token e vulnerabilità della supply chain. Imparerai controlli pratici e best practice per mitigare questi rischi, sfruttando soluzioni Microsoft come Prompt Shields, Azure Content Safety e GitHub Advanced Security per rafforzare il tuo deployment MCP.

## Obiettivi di Apprendimento

Alla fine di questa lezione, sarai in grado di:

- **Identificare le Minacce Specifiche MCP**: Riconoscere i rischi di sicurezza unici nei sistemi MCP, inclusi iniezione di prompt, avvelenamento degli strumenti, permessi eccessivi, dirottamento delle sessioni, problemi di "confused deputy", vulnerabilità di token passthrough e rischi della supply chain
- **Applicare Controlli di Sicurezza**: Implementare mitigazioni efficaci, tra cui autenticazione robusta, accesso con minimo privilegio, gestione sicura dei token, controlli di sicurezza delle sessioni e verifica della supply chain
- **Sfruttare le Soluzioni di Sicurezza Microsoft**: Comprendere e implementare Microsoft Prompt Shields, Azure Content Safety e GitHub Advanced Security per proteggere i carichi di lavoro MCP
- **Validare la Sicurezza degli Strumenti**: Riconoscere l'importanza della validazione dei metadati degli strumenti, monitorare i cambiamenti dinamici e difendersi dagli attacchi di iniezione indiretta di prompt
- **Integrare le Best Practice**: Combinare i fondamenti di sicurezza consolidati (codifica sicura, hardening dei server, zero trust) con controlli specifici MCP per una protezione completa

# Architettura e Controlli di Sicurezza MCP

Le implementazioni moderne di MCP richiedono approcci di sicurezza stratificati che affrontino sia le minacce tradizionali del software sia quelle specifiche per l'AI. La specifica MCP, in rapida evoluzione, continua a migliorare i suoi controlli di sicurezza, consentendo una migliore integrazione con le architetture di sicurezza aziendali e le best practice consolidate.

La ricerca del [Microsoft Digital Defense Report](https://aka.ms/mddr) dimostra che **il 98% delle violazioni segnalate potrebbe essere prevenuto con una solida igiene della sicurezza**. La strategia di protezione più efficace combina pratiche di sicurezza fondamentali con controlli specifici MCP: le misure di sicurezza di base comprovate rimangono le più impattanti nella riduzione del rischio complessivo.

## Panorama Attuale della Sicurezza

> **Nota:** Queste informazioni riflettono gli standard di sicurezza MCP al **18 agosto 2025**. Il protocollo MCP continua a evolversi rapidamente e le implementazioni future potrebbero introdurre nuovi schemi di autenticazione e controlli avanzati. Consulta sempre la [specifica MCP aggiornata](https://spec.modelcontextprotocol.io/), il [repository GitHub MCP](https://github.com/modelcontextprotocol) e la [documentazione sulle best practice di sicurezza](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) per le ultime indicazioni.

### Evoluzione dell'Autenticazione MCP

La specifica MCP ha subito significativi cambiamenti nel suo approccio all'autenticazione e all'autorizzazione:

- **Approccio Originale**: Le prime specifiche richiedevano agli sviluppatori di implementare server di autenticazione personalizzati, con i server MCP che agivano come Authorization Server OAuth 2.0 gestendo direttamente l'autenticazione degli utenti
- **Standard Attuale (2025-06-18)**: La specifica aggiornata consente ai server MCP di delegare l'autenticazione a provider di identità esterni (come Microsoft Entra ID), migliorando la postura di sicurezza e riducendo la complessità di implementazione
- **Sicurezza del Livello di Trasporto**: Supporto migliorato per meccanismi di trasporto sicuri con schemi di autenticazione adeguati sia per connessioni locali (STDIO) che remote (Streamable HTTP)

## Sicurezza di Autenticazione e Autorizzazione

### Sfide di Sicurezza Attuali

Le implementazioni moderne di MCP affrontano diverse sfide di autenticazione e autorizzazione:

### Rischi e Vettori di Minaccia

- **Logica di Autorizzazione Mal Configurata**: Implementazioni errate dell'autorizzazione nei server MCP possono esporre dati sensibili e applicare controlli di accesso in modo scorretto
- **Compromissione dei Token OAuth**: Il furto di token del server MCP locale consente agli attaccanti di impersonare i server e accedere ai servizi a valle
- **Vulnerabilità di Token Passthrough**: Una gestione impropria dei token crea bypass dei controlli di sicurezza e lacune di responsabilità
- **Permessi Eccessivi**: Server MCP con privilegi eccessivi violano i principi del minimo privilegio e ampliano le superfici di attacco

#### Token Passthrough: Un Anti-Pattern Critico

**Il token passthrough è esplicitamente vietato** nella specifica di autorizzazione MCP attuale a causa delle gravi implicazioni di sicurezza:

##### Elusione dei Controlli di Sicurezza
- I server MCP e le API a valle implementano controlli di sicurezza critici (rate limiting, convalida delle richieste, monitoraggio del traffico) che dipendono dalla corretta validazione dei token
- L'uso diretto dei token client-to-API bypassa queste protezioni essenziali, compromettendo l'architettura di sicurezza

##### Sfide di Responsabilità e Audit  
- I server MCP non possono distinguere tra i client che utilizzano token emessi a monte, interrompendo le tracce di audit
- I log dei server di risorse a valle mostrano origini di richieste fuorvianti anziché i veri intermediari del server MCP
- Le indagini sugli incidenti e gli audit di conformità diventano significativamente più difficili

##### Rischi di Esfiltrazione dei Dati
- Le affermazioni dei token non convalidate consentono agli attori malevoli con token rubati di utilizzare i server MCP come proxy per l'esfiltrazione dei dati
- Le violazioni dei confini di fiducia consentono modelli di accesso non autorizzati che bypassano i controlli di sicurezza previsti

##### Vettori di Attacco Multi-Servizio
- I token compromessi accettati da più servizi consentono movimenti laterali attraverso sistemi connessi
- Le ipotesi di fiducia tra i servizi possono essere violate quando le origini dei token non possono essere verificate

### Controlli di Sicurezza e Mitigazioni

**Requisiti di Sicurezza Critici:**

> **OBBLIGATORIO**: I server MCP **NON DEVONO** accettare alcun token che non sia stato esplicitamente emesso per il server MCP

#### Controlli di Autenticazione e Autorizzazione

- **Revisione Rigorosa dell'Autorizzazione**: Condurre audit completi della logica di autorizzazione del server MCP per garantire che solo gli utenti e i client previsti possano accedere alle risorse sensibili
  - **Guida all'Implementazione**: [Azure API Management come Gateway di Autenticazione per i Server MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Integrazione dell'Identità**: [Utilizzo di Microsoft Entra ID per l'Autenticazione del Server MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Gestione Sicura dei Token**: Implementare le [best practice di Microsoft per la validazione e il ciclo di vita dei token](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Validare che le affermazioni dei token corrispondano all'identità del server MCP
  - Implementare politiche adeguate di rotazione ed espirazione dei token
  - Prevenire attacchi di replay dei token e utilizzi non autorizzati

- **Archiviazione Protetta dei Token**: Archiviazione sicura dei token con crittografia sia a riposo che in transito
  - **Best Practice**: [Linee Guida per l'Archiviazione e la Crittografia Sicura dei Token](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementazione del Controllo degli Accessi

- **Principio del Minimo Privilegio**: Concedere ai server MCP solo i permessi minimi necessari per la funzionalità prevista
  - Revisioni regolari dei permessi e aggiornamenti per prevenire l'accumulo di privilegi
  - **Documentazione Microsoft**: [Accesso Sicuro con Minimo Privilegio](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Controllo degli Accessi Basato sui Ruoli (RBAC)**: Implementare assegnazioni di ruoli granulari
  - Limitare i ruoli a risorse e azioni specifiche
  - Evitare permessi ampi o non necessari che ampliano le superfici di attacco

- **Monitoraggio Continuo dei Permessi**: Implementare audit e monitoraggio continui degli accessi
  - Monitorare i modelli di utilizzo dei permessi per rilevare anomalie
  - Correggere tempestivamente privilegi eccessivi o inutilizzati


- **Generazione Sicura delle Sessioni**: Utilizza ID di sessione crittograficamente sicuri e non deterministici generati con generatori di numeri casuali sicuri  
- **Associazione Specifica per Utente**: Associa gli ID di sessione a informazioni specifiche dell'utente utilizzando formati come `<user_id>:<session_id>` per prevenire abusi di sessioni tra utenti  
- **Gestione del Ciclo di Vita delle Sessioni**: Implementa scadenza, rotazione e invalidazione adeguate per limitare le finestre di vulnerabilità  
- **Sicurezza del Trasporto**: HTTPS obbligatorio per tutte le comunicazioni per prevenire l'intercettazione degli ID di sessione  

### Problema del Deputy Confuso

Il **problema del deputy confuso** si verifica quando i server MCP agiscono come proxy di autenticazione tra i client e i servizi di terze parti, creando opportunità per bypassare l'autorizzazione sfruttando ID client statici.

#### **Meccaniche di Attacco e Rischi**

- **Bypass del Consenso Basato su Cookie**: L'autenticazione precedente dell'utente crea cookie di consenso che gli attaccanti sfruttano attraverso richieste di autorizzazione malevole con URI di reindirizzamento manipolati  
- **Furto di Codici di Autorizzazione**: I cookie di consenso esistenti possono indurre i server di autorizzazione a saltare le schermate di consenso, reindirizzando i codici a endpoint controllati dagli attaccanti  
- **Accesso API Non Autorizzato**: I codici di autorizzazione rubati consentono lo scambio di token e l'impersonificazione dell'utente senza approvazione esplicita  

#### **Strategie di Mitigazione**

**Controlli Obbligatori:**
- **Requisiti di Consenso Esplicito**: I server proxy MCP che utilizzano ID client statici **DEVONO** ottenere il consenso dell'utente per ogni client registrato dinamicamente  
- **Implementazione della Sicurezza OAuth 2.1**: Segui le migliori pratiche di sicurezza OAuth attuali, inclusa PKCE (Proof Key for Code Exchange) per tutte le richieste di autorizzazione  
- **Validazione Rigorosa dei Client**: Implementa una rigorosa validazione degli URI di reindirizzamento e degli identificatori dei client per prevenire sfruttamenti  

### Vulnerabilità del Token Passthrough  

Il **token passthrough** rappresenta un anti-pattern esplicito in cui i server MCP accettano token dei client senza una corretta validazione e li inoltrano alle API a valle, violando le specifiche di autorizzazione MCP.

#### **Implicazioni di Sicurezza**

- **Elusione dei Controlli**: L'uso diretto dei token client-API bypassa controlli critici come limitazione della velocità, validazione e monitoraggio  
- **Corruzione della Traccia di Audit**: I token emessi a monte rendono impossibile identificare i client, compromettendo le capacità di indagine sugli incidenti  
- **Esfiltrazione di Dati Basata su Proxy**: I token non validati consentono agli attori malevoli di utilizzare i server come proxy per accedere ai dati non autorizzati  
- **Violazioni dei Confini di Fiducia**: Le assunzioni di fiducia dei servizi a valle possono essere violate quando le origini dei token non possono essere verificate  
- **Espansione degli Attacchi Multi-Servizio**: I token compromessi accettati su più servizi consentono movimenti laterali  

#### **Controlli di Sicurezza Richiesti**

**Requisiti Non Negoziabili:**
- **Validazione dei Token**: I server MCP **NON DEVONO** accettare token non esplicitamente emessi per il server MCP  
- **Verifica dell'Audience**: Verifica sempre che le affermazioni sull'audience dei token corrispondano all'identità del server MCP  
- **Ciclo di Vita Corretto dei Token**: Implementa token di accesso a breve durata con pratiche di rotazione sicure  

## Sicurezza della Supply Chain per i Sistemi AI

La sicurezza della supply chain si è evoluta oltre le dipendenze software tradizionali per includere l'intero ecosistema AI. Le implementazioni moderne di MCP devono verificare e monitorare rigorosamente tutti i componenti AI, poiché ciascuno introduce potenziali vulnerabilità che potrebbero compromettere l'integrità del sistema.

### Componenti Espansi della Supply Chain AI

**Dipendenze Software Tradizionali:**
- Librerie e framework open-source  
- Immagini container e sistemi di base  
- Strumenti di sviluppo e pipeline di build  
- Componenti e servizi infrastrutturali  

**Elementi Specifici dell'AI nella Supply Chain:**
- **Modelli di Base**: Modelli pre-addestrati di vari fornitori che richiedono verifica della provenienza  
- **Servizi di Embedding**: Servizi esterni di vettorizzazione e ricerca semantica  
- **Provider di Contesto**: Fonti di dati, basi di conoscenza e repository di documenti  
- **API di Terze Parti**: Servizi AI esterni, pipeline ML ed endpoint di elaborazione dati  
- **Artefatti del Modello**: Pesi, configurazioni e varianti di modelli ottimizzati  
- **Fonti di Dati per l'Addestramento**: Dataset utilizzati per l'addestramento e l'ottimizzazione dei modelli  

### Strategia Completa di Sicurezza della Supply Chain

#### **Verifica dei Componenti e Fiducia**
- **Validazione della Provenienza**: Verifica l'origine, la licenza e l'integrità di tutti i componenti AI prima dell'integrazione  
- **Valutazione della Sicurezza**: Conduci scansioni di vulnerabilità e revisioni di sicurezza per modelli, fonti di dati e servizi AI  
- **Analisi della Reputazione**: Valuta il track record di sicurezza e le pratiche dei fornitori di servizi AI  
- **Verifica della Conformità**: Assicurati che tutti i componenti soddisfino i requisiti di sicurezza e normativi dell'organizzazione  

#### **Pipeline di Distribuzione Sicure**  
- **Sicurezza CI/CD Automatica**: Integra scansioni di sicurezza in tutte le pipeline di distribuzione automatizzate  
- **Integrità degli Artefatti**: Implementa verifiche crittografiche per tutti gli artefatti distribuiti (codice, modelli, configurazioni)  
- **Distribuzione Graduale**: Utilizza strategie di distribuzione progressiva con validazione della sicurezza a ogni fase  
- **Repository di Artefatti Fidati**: Distribuisci solo da registri e repository di artefatti verificati e sicuri  

#### **Monitoraggio Continuo e Risposta**
- **Scansione delle Dipendenze**: Monitoraggio continuo delle vulnerabilità per tutte le dipendenze software e componenti AI  
- **Monitoraggio dei Modelli**: Valutazione continua del comportamento dei modelli, del degrado delle prestazioni e delle anomalie di sicurezza  
- **Monitoraggio della Salute dei Servizi**: Monitora i servizi AI esterni per disponibilità, incidenti di sicurezza e cambiamenti di policy  
- **Integrazione dell'Intelligence sulle Minacce**: Incorpora feed di minacce specifici per i rischi di sicurezza AI e ML  

#### **Controllo degli Accessi e Minimo Privilegio**
- **Permessi a Livello di Componente**: Restringi l'accesso a modelli, dati e servizi in base alla necessità aziendale  
- **Gestione degli Account di Servizio**: Implementa account di servizio dedicati con i permessi minimi richiesti  
- **Segmentazione della Rete**: Isola i componenti AI e limita l'accesso di rete tra i servizi  
- **Controlli del Gateway API**: Utilizza gateway API centralizzati per controllare e monitorare l'accesso ai servizi AI esterni  

#### **Risposta agli Incidenti e Recupero**
- **Procedure di Risposta Rapida**: Processi stabiliti per correggere o sostituire componenti AI compromessi  
- **Rotazione delle Credenziali**: Sistemi automatizzati per la rotazione di segreti, chiavi API e credenziali di servizio  
- **Capacità di Rollback**: Capacità di tornare rapidamente a versioni precedenti note come sicure dei componenti AI  
- **Recupero da Breach della Supply Chain**: Procedure specifiche per rispondere a compromissioni dei servizi AI a monte  

### Strumenti di Sicurezza Microsoft e Integrazione

**GitHub Advanced Security** offre protezione completa per la supply chain, inclusi:  
- **Scansione dei Segreti**: Rilevamento automatico di credenziali, chiavi API e token nei repository  
- **Scansione delle Dipendenze**: Valutazione delle vulnerabilità per dipendenze open-source e librerie  
- **Analisi CodeQL**: Analisi statica del codice per vulnerabilità di sicurezza e problemi di codifica  
- **Supply Chain Insights**: Visibilità sulla salute e lo stato di sicurezza delle dipendenze  

**Integrazione con Azure DevOps e Azure Repos:**  
- Integrazione fluida delle scansioni di sicurezza nelle piattaforme di sviluppo Microsoft  
- Controlli di sicurezza automatizzati nelle pipeline di Azure per carichi di lavoro AI  
- Applicazione di policy per la distribuzione sicura dei componenti AI  

**Pratiche Interne Microsoft:**  
Microsoft implementa pratiche di sicurezza della supply chain estese in tutti i prodotti. Scopri approcci comprovati in [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Soluzioni di Sicurezza Microsoft**
- [Documentazione Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Servizio Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Sicurezza Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Best practice per la gestione dei token in Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Guide e Tutorial per l'Implementazione**
- [Azure API Management come Gateway di Autenticazione MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Autenticazione Microsoft Entra ID con server MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Archiviazione sicura dei token e crittografia (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps e Sicurezza della Supply Chain**
- [Sicurezza di Azure DevOps](https://azure.microsoft.com/products/devops)
- [Sicurezza di Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [Il percorso di Microsoft verso la sicurezza della supply chain](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Documentazione di Sicurezza Aggiuntiva**

Per una guida completa sulla sicurezza, consulta questi documenti specializzati in questa sezione:

- **[MCP Security Best Practices 2025](./mcp-security-best-practices-2025.md)** - Best practice complete per le implementazioni MCP  
- **[Implementazione di Azure Content Safety](./azure-content-safety-implementation.md)** - Esempi pratici per l'integrazione di Azure Content Safety  
- **[MCP Security Controls 2025](./mcp-security-controls-2025.md)** - Controlli di sicurezza e tecniche più recenti per le implementazioni MCP  
- **[Riferimento rapido alle Best Practice MCP](./mcp-best-practices.md)** - Guida di riferimento rapido per le pratiche di sicurezza essenziali MCP  

---

## Prossimi Passi

Prossimo: [Capitolo 3: Introduzione](../03-GettingStarted/README.md)

**Disclaimer (Avvertenza)**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire l'accuratezza, si prega di notare che le traduzioni automatiche potrebbero contenere errori o imprecisioni. Il documento originale nella sua lingua nativa dovrebbe essere considerato la fonte autorevole. Per informazioni critiche, si consiglia una traduzione professionale eseguita da un traduttore umano. Non siamo responsabili per eventuali fraintendimenti o interpretazioni errate derivanti dall'uso di questa traduzione.