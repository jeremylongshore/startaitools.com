<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T17:31:06+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "it"
}
-->
# Migliori Pratiche di Sicurezza MCP 2025

Questa guida completa descrive le pratiche essenziali di sicurezza per implementare sistemi Model Context Protocol (MCP) basati sull'ultima **Specifica MCP 2025-06-18** e sugli standard attuali del settore. Queste pratiche affrontano sia le preoccupazioni di sicurezza tradizionali che le minacce specifiche dell'IA uniche per le implementazioni MCP.

## Requisiti Critici di Sicurezza

### Controlli di Sicurezza Obbligatori (Requisiti MUST)

1. **Validazione dei Token**: I server MCP **NON DEVONO** accettare token che non siano stati esplicitamente emessi per il server MCP stesso.
2. **Verifica dell'Autorizzazione**: I server MCP che implementano l'autorizzazione **DEVONO** verificare TUTTE le richieste in entrata e **NON DEVONO** utilizzare sessioni per l'autenticazione.  
3. **Consenso dell'Utente**: I server proxy MCP che utilizzano ID client statici **DEVONO** ottenere il consenso esplicito dell'utente per ogni client registrato dinamicamente.
4. **ID di Sessione Sicuri**: I server MCP **DEVONO** utilizzare ID di sessione crittograficamente sicuri e non deterministici generati con generatori di numeri casuali sicuri.

## Pratiche di Sicurezza Fondamentali

### 1. Validazione e Sanitizzazione degli Input
- **Validazione Completa degli Input**: Validare e sanitizzare tutti gli input per prevenire attacchi di injection, problemi di confused deputy e vulnerabilità di prompt injection.
- **Applicazione dello Schema dei Parametri**: Implementare una rigorosa validazione dello schema JSON per tutti i parametri degli strumenti e gli input delle API.
- **Filtraggio dei Contenuti**: Utilizzare Microsoft Prompt Shields e Azure Content Safety per filtrare contenuti dannosi nei prompt e nelle risposte.
- **Sanitizzazione degli Output**: Validare e sanitizzare tutti gli output del modello prima di presentarli agli utenti o ai sistemi a valle.

### 2. Eccellenza in Autenticazione e Autorizzazione  
- **Provider di Identità Esterni**: Delegare l'autenticazione a provider di identità consolidati (Microsoft Entra ID, provider OAuth 2.1) anziché implementare autenticazioni personalizzate.
- **Permessi Granulari**: Implementare permessi specifici per strumento seguendo il principio del minimo privilegio.
- **Gestione del Ciclo di Vita dei Token**: Utilizzare token di accesso a breve durata con rotazione sicura e corretta validazione del pubblico.
- **Autenticazione Multi-Fattore**: Richiedere MFA per tutti gli accessi amministrativi e le operazioni sensibili.

### 3. Protocolli di Comunicazione Sicuri
- **Sicurezza del Livello di Trasporto**: Utilizzare HTTPS/TLS 1.3 per tutte le comunicazioni MCP con corretta validazione dei certificati.
- **Crittografia End-to-End**: Implementare ulteriori livelli di crittografia per dati altamente sensibili in transito e a riposo.
- **Gestione dei Certificati**: Mantenere una corretta gestione del ciclo di vita dei certificati con processi di rinnovo automatizzati.
- **Applicazione della Versione del Protocollo**: Utilizzare la versione corrente del protocollo MCP (2025-06-18) con corretta negoziazione della versione.

### 4. Limitazione Avanzata del Tasso e Protezione delle Risorse
- **Limitazione del Tasso Multi-livello**: Implementare limitazioni del tasso a livello di utente, sessione, strumento e risorsa per prevenire abusi.
- **Limitazione del Tasso Adattiva**: Utilizzare limitazioni del tasso basate su machine learning che si adattano ai modelli di utilizzo e agli indicatori di minaccia.
- **Gestione delle Quote delle Risorse**: Impostare limiti appropriati per risorse computazionali, utilizzo della memoria e tempo di esecuzione.
- **Protezione DDoS**: Implementare protezioni DDoS complete e sistemi di analisi del traffico.

### 5. Registrazione e Monitoraggio Completi
- **Registrazione Audit Strutturata**: Implementare log dettagliati e ricercabili per tutte le operazioni MCP, esecuzioni di strumenti ed eventi di sicurezza.
- **Monitoraggio della Sicurezza in Tempo Reale**: Distribuire sistemi SIEM con rilevamento delle anomalie basato su IA per i carichi di lavoro MCP.
- **Registrazione Conforme alla Privacy**: Registrare eventi di sicurezza rispettando i requisiti e le normative sulla privacy dei dati.
- **Integrazione della Risposta agli Incidenti**: Collegare i sistemi di registrazione a flussi di lavoro automatizzati per la risposta agli incidenti.

### 6. Pratiche Avanzate di Archiviazione Sicura
- **Moduli di Sicurezza Hardware**: Utilizzare archiviazione di chiavi supportata da HSM (Azure Key Vault, AWS CloudHSM) per operazioni crittografiche critiche.
- **Gestione delle Chiavi di Crittografia**: Implementare una corretta rotazione, segregazione e controlli di accesso per le chiavi di crittografia.
- **Gestione dei Segreti**: Archiviare tutte le chiavi API, i token e le credenziali in sistemi dedicati di gestione dei segreti.
- **Classificazione dei Dati**: Classificare i dati in base ai livelli di sensibilità e applicare misure di protezione appropriate.

### 7. Gestione Avanzata dei Token
- **Prevenzione del Passaggio dei Token**: Proibire esplicitamente i modelli di passaggio dei token che bypassano i controlli di sicurezza.
- **Validazione del Pubblico**: Verificare sempre che le affermazioni sul pubblico dei token corrispondano all'identità del server MCP previsto.
- **Autorizzazione Basata su Affermative**: Implementare autorizzazioni granulari basate sulle affermazioni dei token e sugli attributi degli utenti.
- **Associazione dei Token**: Associare i token a sessioni, utenti o dispositivi specifici, ove appropriato.

### 8. Gestione Sicura delle Sessioni
- **ID di Sessione Crittografici**: Generare ID di sessione utilizzando generatori di numeri casuali crittograficamente sicuri (non sequenze prevedibili).
- **Associazione Specifica per Utente**: Associare gli ID di sessione a informazioni specifiche dell'utente utilizzando formati sicuri come `<user_id>:<session_id>`.
- **Controlli del Ciclo di Vita delle Sessioni**: Implementare meccanismi adeguati di scadenza, rotazione e invalidazione delle sessioni.
- **Header di Sicurezza delle Sessioni**: Utilizzare header HTTP appropriati per la protezione delle sessioni.

### 9. Controlli di Sicurezza Specifici per l'IA
- **Difesa contro il Prompt Injection**: Distribuire Microsoft Prompt Shields con tecniche di spotlighting, delimitatori e datamarking.
- **Prevenzione dell'Avvelenamento degli Strumenti**: Validare i metadati degli strumenti, monitorare i cambiamenti dinamici e verificare l'integrità degli strumenti.
- **Validazione degli Output del Modello**: Analizzare gli output del modello per potenziali fughe di dati, contenuti dannosi o violazioni delle politiche di sicurezza.
- **Protezione della Finestra di Contesto**: Implementare controlli per prevenire avvelenamenti e manipolazioni della finestra di contesto.

### 10. Sicurezza nell'Esecuzione degli Strumenti
- **Sandboxing dell'Esecuzione**: Eseguire gli strumenti in ambienti containerizzati e isolati con limiti di risorse.
- **Separazione dei Privilegi**: Eseguire gli strumenti con i privilegi minimi richiesti e account di servizio separati.
- **Isolamento della Rete**: Implementare segmentazione della rete per gli ambienti di esecuzione degli strumenti.
- **Monitoraggio dell'Esecuzione**: Monitorare l'esecuzione degli strumenti per comportamenti anomali, utilizzo delle risorse e violazioni della sicurezza.

### 11. Validazione Continua della Sicurezza
- **Test di Sicurezza Automatizzati**: Integrare i test di sicurezza nelle pipeline CI/CD con strumenti come GitHub Advanced Security.
- **Gestione delle Vulnerabilità**: Scansionare regolarmente tutte le dipendenze, inclusi modelli di IA e servizi esterni.
- **Test di Penetrazione**: Condurre regolari valutazioni di sicurezza mirate specificamente alle implementazioni MCP.
- **Revisione del Codice di Sicurezza**: Implementare revisioni obbligatorie del codice per tutte le modifiche relative a MCP.

### 12. Sicurezza della Catena di Fornitura per l'IA
- **Verifica dei Componenti**: Verificare la provenienza, l'integrità e la sicurezza di tutti i componenti IA (modelli, embedding, API).
- **Gestione delle Dipendenze**: Mantenere inventari aggiornati di tutte le dipendenze software e IA con tracciamento delle vulnerabilità.
- **Repository Fidati**: Utilizzare fonti verificate e affidabili per tutti i modelli, le librerie e gli strumenti IA.
- **Monitoraggio della Catena di Fornitura**: Monitorare continuamente compromissioni nei fornitori di servizi IA e nei repository di modelli.

## Modelli Avanzati di Sicurezza

### Architettura Zero Trust per MCP
- **Mai Fidarsi, Sempre Verificare**: Implementare una verifica continua per tutti i partecipanti MCP.
- **Micro-segmentazione**: Isolare i componenti MCP con controlli granulari di rete e identità.
- **Accesso Condizionale**: Implementare controlli di accesso basati sul rischio che si adattano al contesto e al comportamento.
- **Valutazione Continua del Rischio**: Valutare dinamicamente la postura di sicurezza basandosi sugli indicatori di minaccia attuali.

### Implementazione dell'IA con Preservazione della Privacy
- **Minimizzazione dei Dati**: Esporre solo i dati strettamente necessari per ogni operazione MCP.
- **Privacy Differenziale**: Implementare tecniche di preservazione della privacy per l'elaborazione di dati sensibili.
- **Crittografia Omomorfica**: Utilizzare tecniche avanzate di crittografia per calcoli sicuri su dati crittografati.
- **Apprendimento Federato**: Implementare approcci di apprendimento distribuito che preservano la località e la privacy dei dati.

### Risposta agli Incidenti per Sistemi IA
- **Procedure Specifiche per l'IA**: Sviluppare procedure di risposta agli incidenti mirate alle minacce specifiche di IA e MCP.
- **Risposta Automatica**: Implementare contenimento e rimedi automatizzati per incidenti comuni di sicurezza IA.  
- **Capacità Forensi**: Mantenere prontezza forense per compromissioni di sistemi IA e violazioni dei dati.
- **Procedure di Recupero**: Stabilire procedure per il recupero da avvelenamenti di modelli IA, attacchi di prompt injection e compromissioni di servizi.

## Risorse e Standard per l'Implementazione

### Documentazione Ufficiale MCP
- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Specifica corrente del protocollo MCP
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Guida ufficiale alla sicurezza
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Modelli di autenticazione e autorizzazione
- [MCP Transport Security](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Requisiti di sicurezza del livello di trasporto

### Soluzioni di Sicurezza Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Protezione avanzata contro il prompt injection
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Filtraggio completo dei contenuti IA
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Gestione aziendale di identità e accessi
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Gestione sicura di segreti e credenziali
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Scansione della sicurezza del codice e della catena di fornitura

### Standard e Framework di Sicurezza
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Linee guida attuali sulla sicurezza OAuth
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Rischi di sicurezza per applicazioni web
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Rischi di sicurezza specifici per l'IA
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Gestione completa dei rischi IA
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sistemi di gestione della sicurezza delle informazioni

### Guide e Tutorial per l'Implementazione
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Modelli di autenticazione aziendale
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integrazione con provider di identità
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Migliori pratiche per la gestione dei token
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Modelli avanzati di crittografia

### Risorse Avanzate di Sicurezza
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Pratiche di sviluppo sicuro
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - Test di sicurezza specifici per l'IA
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologia di modellazione delle minacce IA
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Tecniche di preservazione della privacy per l'IA

### Conformità e Governance
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Conformità alla privacy nei sistemi IA
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementazione di IA responsabile
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Controlli di sicurezza per fornitori di servizi IA
- [HIPAA Compliance for AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Requisiti di conformità per IA in ambito sanitario

### DevSecOps e Automazione
- [DevSecOps Pipeline for AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Pipeline di sviluppo sicuro per l'IA
- [Automated Security Testing](https://learn.microsoft.com/security/engineering/devsecops) - Validazione continua della sicurezza
- [Infrastructure as Code Security](https://learn.microsoft.com/security/engineering/infrastructure-security) - Distribuzione sicura dell'infrastruttura
- [Container Security for AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Sicurezza nella containerizzazione dei carichi di lavoro IA

### Monitoraggio e Risposta agli Incidenti  
- [Azure Monitor for AI Workloads](https://learn.microsoft.com/azure/azure-monitor/overview) - Soluzioni di monitoraggio complete
- [AI Security Incident Response](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Procedure specifiche per incidenti di sicurezza IA
- [SIEM for AI Systems](https://learn.microsoft.com/azure/sentinel/overview) - Gestione delle informazioni e degli eventi di sicurezza
- [Threat Intelligence for AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Fonti di intelligence sulle minacce IA

## 🔄 Miglioramento Continuo

### Rimanere Aggiornati con gli Standard in Evoluzione
- **Aggiornamenti della Specifica MCP**: Monitorare i cambiamenti ufficiali della specifica MCP e gli avvisi di sicurezza.
- **Intelligence sulle Minacce**: Iscriversi a feed di minacce di sicurezza IA e database di vulnerabilità.  
- **Coinvolgimento della Comunità**: Partecipare a discussioni e gruppi di lavoro sulla sicurezza MCP.
- **Valutazione Regolare**: Condurre valutazioni trimestrali della postura di sicurezza e aggiornare le pratiche di conseguenza.

### Contribuire alla Sicurezza MCP
- **Ricerca sulla Sicurezza**: Contribuire alla ricerca sulla sicurezza MCP e ai programmi di divulgazione delle vulnerabilità.
- **Condivisione delle Migliori Pratiche**: Condividere implementazioni di sicurezza e lezioni apprese con la comunità.
- **Sviluppo degli Standard**: Partecipare allo sviluppo delle specifiche MCP e alla creazione di standard di sicurezza.
- **Sviluppo di Strumenti**: Sviluppare e condividere strumenti e librerie di sicurezza per l'ecosistema MCP

---

*Questo documento riflette le migliori pratiche di sicurezza MCP al 18 agosto 2025, basate sulla Specifica MCP 2025-06-18. Le pratiche di sicurezza dovrebbero essere regolarmente riviste e aggiornate man mano che il protocollo e il panorama delle minacce evolvono.*

**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si consiglia una traduzione professionale eseguita da un traduttore umano. Non siamo responsabili per eventuali fraintendimenti o interpretazioni errate derivanti dall'uso di questa traduzione.