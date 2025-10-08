<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T17:27:56+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "it"
}
-->
# MCP Best Practice di Sicurezza - Aggiornamento Agosto 2025

> **Importante**: Questo documento riflette i più recenti requisiti di sicurezza della [Specifica MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) e le [Migliori Pratiche di Sicurezza MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Fare sempre riferimento alla specifica attuale per ottenere le linee guida più aggiornate.

## Pratiche Essenziali di Sicurezza per le Implementazioni MCP

Il Model Context Protocol introduce sfide di sicurezza uniche che vanno oltre la sicurezza software tradizionale. Queste pratiche affrontano sia i requisiti di sicurezza fondamentali che le minacce specifiche di MCP, tra cui injection di prompt, avvelenamento degli strumenti, dirottamento di sessioni, problemi di confused deputy e vulnerabilità di token passthrough.

### **Requisiti di Sicurezza OBBLIGATORI**

**Requisiti Critici dalla Specifica MCP:**

> **MUST NOT**: I server MCP **NON DEVONO** accettare token che non siano stati esplicitamente emessi per il server MCP  
> 
> **MUST**: I server MCP che implementano l'autorizzazione **DEVONO** verificare TUTTE le richieste in entrata  
>  
> **MUST NOT**: I server MCP **NON DEVONO** utilizzare sessioni per l'autenticazione  
>
> **MUST**: I server proxy MCP che utilizzano ID client statici **DEVONO** ottenere il consenso dell'utente per ogni client registrato dinamicamente  

---

## 1. **Sicurezza dei Token e Autenticazione**

**Controlli di Autenticazione e Autorizzazione:**
   - **Revisione Rigorosa dell'Autorizzazione**: Effettuare audit completi della logica di autorizzazione del server MCP per garantire che solo utenti e client autorizzati possano accedere alle risorse  
   - **Integrazione con Provider di Identità Esterni**: Utilizzare provider di identità consolidati come Microsoft Entra ID invece di implementare soluzioni di autenticazione personalizzate  
   - **Validazione del Pubblico dei Token**: Validare sempre che i token siano stati esplicitamente emessi per il proprio server MCP - non accettare mai token upstream  
   - **Gestione Corretta del Ciclo di Vita dei Token**: Implementare rotazione sicura dei token, politiche di scadenza e prevenire attacchi di replay dei token  

**Archiviazione Protetta dei Token:**
   - Utilizzare Azure Key Vault o archivi sicuri simili per tutte le credenziali  
   - Implementare la crittografia per i token sia a riposo che in transito  
   - Rotazione regolare delle credenziali e monitoraggio per accessi non autorizzati  

## 2. **Gestione delle Sessioni e Sicurezza del Trasporto**

**Pratiche Sicure per le Sessioni:**
   - **ID di Sessione Criptograficamente Sicuri**: Utilizzare ID di sessione sicuri e non deterministici generati con generatori di numeri casuali sicuri  
   - **Associazione Specifica per Utente**: Associare gli ID di sessione alle identità degli utenti utilizzando formati come `<user_id>:<session_id>` per prevenire abusi tra utenti  
   - **Gestione del Ciclo di Vita delle Sessioni**: Implementare scadenza, rotazione e invalidazione adeguate per limitare le finestre di vulnerabilità  
   - **Applicazione di HTTPS/TLS**: HTTPS obbligatorio per tutte le comunicazioni per prevenire intercettazioni degli ID di sessione  

**Sicurezza del Livello di Trasporto:**
   - Configurare TLS 1.3 ove possibile con una gestione adeguata dei certificati  
   - Implementare il pinning dei certificati per connessioni critiche  
   - Rotazione regolare dei certificati e verifica della loro validità  

## 3. **Protezione da Minacce Specifiche per l'AI** 🤖

**Difesa contro Prompt Injection:**
   - **Microsoft Prompt Shields**: Distribuire AI Prompt Shields per il rilevamento avanzato e il filtraggio di istruzioni dannose  
   - **Sanitizzazione degli Input**: Validare e sanitizzare tutti gli input per prevenire attacchi di injection e problemi di confused deputy  
   - **Confini di Contenuto**: Utilizzare sistemi di delimitazione e marcatura dei dati per distinguere tra istruzioni fidate e contenuti esterni  

**Prevenzione dell'Avvelenamento degli Strumenti:**
   - **Validazione dei Metadati degli Strumenti**: Implementare controlli di integrità per le definizioni degli strumenti e monitorare eventuali modifiche inattese  
   - **Monitoraggio Dinamico degli Strumenti**: Monitorare il comportamento in tempo reale e configurare avvisi per schemi di esecuzione inattesi  
   - **Flussi di Approvazione**: Richiedere l'approvazione esplicita dell'utente per modifiche agli strumenti e cambiamenti di capacità  

## 4. **Controllo degli Accessi e Permessi**

**Principio del Minimo Privilegio:**
   - Concedere ai server MCP solo i permessi minimi necessari per la funzionalità prevista  
   - Implementare il controllo degli accessi basato sui ruoli (RBAC) con permessi granulari  
   - Revisioni regolari dei permessi e monitoraggio continuo per escalation di privilegi  

**Controlli dei Permessi in Esecuzione:**
   - Applicare limiti alle risorse per prevenire attacchi di esaurimento delle risorse  
   - Utilizzare l'isolamento dei container per gli ambienti di esecuzione degli strumenti  
   - Implementare accessi just-in-time per le funzioni amministrative  

## 5. **Sicurezza dei Contenuti e Monitoraggio**

**Implementazione della Sicurezza dei Contenuti:**
   - **Integrazione con Azure Content Safety**: Utilizzare Azure Content Safety per rilevare contenuti dannosi, tentativi di jailbreak e violazioni delle policy  
   - **Analisi Comportamentale**: Implementare il monitoraggio comportamentale in tempo reale per rilevare anomalie nell'esecuzione del server MCP e degli strumenti  
   - **Logging Completo**: Registrare tutti i tentativi di autenticazione, invocazioni di strumenti ed eventi di sicurezza con archiviazione sicura e a prova di manomissione  

**Monitoraggio Continuo:**
   - Avvisi in tempo reale per schemi sospetti e tentativi di accesso non autorizzati  
   - Integrazione con sistemi SIEM per la gestione centralizzata degli eventi di sicurezza  
   - Audit di sicurezza regolari e test di penetrazione delle implementazioni MCP  

## 6. **Sicurezza della Supply Chain**

**Verifica dei Componenti:**
   - **Scansione delle Dipendenze**: Utilizzare scansioni automatiche delle vulnerabilità per tutte le dipendenze software e i componenti AI  
   - **Validazione della Provenienza**: Verificare l'origine, le licenze e l'integrità di modelli, fonti di dati e servizi esterni  
   - **Pacchetti Firmati**: Utilizzare pacchetti firmati crittograficamente e verificare le firme prima del deployment  

**Pipeline di Sviluppo Sicura:**
   - **GitHub Advanced Security**: Implementare scansione dei segreti, analisi delle dipendenze e analisi statica con CodeQL  
   - **Sicurezza CI/CD**: Integrare la validazione della sicurezza in tutte le pipeline di deployment automatizzate  
   - **Integrità degli Artefatti**: Implementare la verifica crittografica per artefatti e configurazioni distribuiti  

## 7. **Sicurezza OAuth e Prevenzione dei Confused Deputy**

**Implementazione di OAuth 2.1:**
   - **Implementazione PKCE**: Utilizzare Proof Key for Code Exchange (PKCE) per tutte le richieste di autorizzazione  
   - **Consenso Esplicito**: Ottenere il consenso dell'utente per ogni client registrato dinamicamente per prevenire attacchi di confused deputy  
   - **Validazione degli URI di Reindirizzamento**: Implementare una validazione rigorosa degli URI di reindirizzamento e degli identificatori dei client  

**Sicurezza dei Proxy:**
   - Prevenire bypass di autorizzazione tramite sfruttamento di ID client statici  
   - Implementare flussi di consenso adeguati per l'accesso alle API di terze parti  
   - Monitorare il furto di codici di autorizzazione e accessi non autorizzati alle API  

## 8. **Risposta agli Incidenti e Recupero**

**Capacità di Risposta Rapida:**
   - **Risposta Automatica**: Implementare sistemi automatizzati per la rotazione delle credenziali e il contenimento delle minacce  
   - **Procedure di Rollback**: Capacità di tornare rapidamente a configurazioni e componenti noti come sicuri  
   - **Capacità Forensi**: Tracce di audit dettagliate e registrazioni per l'indagine sugli incidenti  

**Comunicazione e Coordinamento:**
   - Procedure chiare di escalation per gli incidenti di sicurezza  
   - Integrazione con i team di risposta agli incidenti dell'organizzazione  
   - Simulazioni regolari di incidenti di sicurezza ed esercitazioni tabletop  

## 9. **Conformità e Governance**

**Conformità Regolamentare:**
   - Garantire che le implementazioni MCP soddisfino i requisiti specifici del settore (GDPR, HIPAA, SOC 2)  
   - Implementare controlli di classificazione dei dati e privacy per l'elaborazione dei dati AI  
   - Mantenere una documentazione completa per gli audit di conformità  

**Gestione delle Modifiche:**
   - Processi formali di revisione della sicurezza per tutte le modifiche ai sistemi MCP  
   - Controllo delle versioni e flussi di approvazione per le modifiche di configurazione  
   - Valutazioni regolari della conformità e analisi delle lacune  

## 10. **Controlli di Sicurezza Avanzati**

**Architettura Zero Trust:**
   - **Mai Fidarsi, Verificare Sempre**: Verifica continua di utenti, dispositivi e connessioni  
   - **Micro-segmentazione**: Controlli di rete granulari che isolano i singoli componenti MCP  
   - **Accesso Condizionale**: Controlli di accesso basati sul rischio che si adattano al contesto e al comportamento attuale  

**Protezione delle Applicazioni in Esecuzione:**
   - **Runtime Application Self-Protection (RASP)**: Distribuire tecniche RASP per il rilevamento delle minacce in tempo reale  
   - **Monitoraggio delle Prestazioni delle Applicazioni**: Monitorare anomalie nelle prestazioni che potrebbero indicare attacchi  
   - **Policy di Sicurezza Dinamiche**: Implementare policy di sicurezza che si adattano in base al panorama delle minacce attuale  

## 11. **Integrazione con l'Ecosistema di Sicurezza Microsoft**

**Sicurezza Completa Microsoft:**
   - **Microsoft Defender for Cloud**: Gestione della postura di sicurezza cloud per i carichi di lavoro MCP  
   - **Azure Sentinel**: Capacità SIEM e SOAR native per il rilevamento avanzato delle minacce  
   - **Microsoft Purview**: Governance dei dati e conformità per i flussi di lavoro AI e le fonti di dati  

**Gestione delle Identità e degli Accessi:**
   - **Microsoft Entra ID**: Gestione delle identità aziendali con policy di accesso condizionale  
   - **Privileged Identity Management (PIM)**: Accesso just-in-time e flussi di approvazione per le funzioni amministrative  
   - **Protezione delle Identità**: Accesso condizionale basato sul rischio e risposta automatizzata alle minacce  

## 12. **Evoluzione Continua della Sicurezza**

**Rimanere Aggiornati:**
   - **Monitoraggio delle Specifiche**: Revisione regolare degli aggiornamenti delle specifiche MCP e delle modifiche alle linee guida di sicurezza  
   - **Intelligence sulle Minacce**: Integrazione di feed di minacce specifici per l'AI e indicatori di compromissione  
   - **Coinvolgimento nella Comunità di Sicurezza**: Partecipazione attiva alla comunità di sicurezza MCP e ai programmi di divulgazione delle vulnerabilità  

**Sicurezza Adattiva:**
   - **Sicurezza Basata sul Machine Learning**: Utilizzare il rilevamento delle anomalie basato su ML per identificare schemi di attacco nuovi  
   - **Analisi Predittiva della Sicurezza**: Implementare modelli predittivi per l'identificazione proattiva delle minacce  
   - **Automazione della Sicurezza**: Aggiornamenti automatici delle policy di sicurezza basati su intelligence sulle minacce e modifiche alle specifiche  

---

## **Risorse Critiche di Sicurezza**

### **Documentazione Ufficiale MCP**
- [Specifiche MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Migliori Pratiche di Sicurezza MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Specifiche di Autorizzazione MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Soluzioni di Sicurezza Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Sicurezza Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Standard di Sicurezza**
- [Migliori Pratiche di Sicurezza OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 per i Modelli di Linguaggio di Grandi Dimensioni](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Guide all'Implementazione**
- [Gateway di Autenticazione MCP con Azure API Management](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID con Server MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Avviso di Sicurezza**: Le pratiche di sicurezza MCP evolvono rapidamente. Verificare sempre rispetto alla [specifica MCP attuale](https://spec.modelcontextprotocol.io/) e alla [documentazione ufficiale di sicurezza](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) prima dell'implementazione.

**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si consiglia una traduzione professionale eseguita da un traduttore umano. Non siamo responsabili per eventuali fraintendimenti o interpretazioni errate derivanti dall'uso di questa traduzione.