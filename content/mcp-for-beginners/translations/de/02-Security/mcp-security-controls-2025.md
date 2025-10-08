<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T11:52:45+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "de"
}
-->
# MCP-Sicherheitskontrollen – Update August 2025

> **Aktueller Standard**: Dieses Dokument spiegelt die Sicherheitsanforderungen der [MCP-Spezifikation 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) und die offiziellen [MCP-Sicherheitsbest Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) wider.

Das Model Context Protocol (MCP) hat sich erheblich weiterentwickelt und bietet verbesserte Sicherheitskontrollen, die sowohl traditionelle Software-Sicherheitsrisiken als auch KI-spezifische Bedrohungen adressieren. Dieses Dokument liefert umfassende Sicherheitskontrollen für sichere MCP-Implementierungen ab August 2025.

## **VERPFLICHTENDE Sicherheitsanforderungen**

### **Kritische Verbote aus der MCP-Spezifikation:**

> **VERBOTEN**: MCP-Server **DÜRFEN KEINE** Tokens akzeptieren, die nicht explizit für den MCP-Server ausgestellt wurden  
>
> **UNTERSAGT**: MCP-Server **DÜRFEN KEINE** Sitzungen für die Authentifizierung verwenden  
>
> **ERFORDERLICH**: MCP-Server, die Autorisierung implementieren, **MÜSSEN** ALLE eingehenden Anfragen überprüfen  
>
> **VERPFLICHTEND**: MCP-Proxy-Server, die statische Client-IDs verwenden, **MÜSSEN** die Zustimmung der Nutzer für jeden dynamisch registrierten Client einholen  

---

## 1. **Authentifizierungs- und Autorisierungskontrollen**

### **Integration externer Identitätsanbieter**

Der **aktuelle MCP-Standard (2025-06-18)** erlaubt MCP-Servern, die Authentifizierung an externe Identitätsanbieter zu delegieren, was eine erhebliche Sicherheitsverbesserung darstellt:

**Sicherheitsvorteile:**
1. **Vermeidung von Risiken durch eigene Authentifizierung**: Reduziert die Angriffsfläche durch Verzicht auf eigene Authentifizierungslösungen  
2. **Sicherheitsstandards auf Unternehmensebene**: Nutzt etablierte Identitätsanbieter wie Microsoft Entra ID mit erweiterten Sicherheitsfunktionen  
3. **Zentralisiertes Identitätsmanagement**: Vereinfacht das Management des Nutzerlebenszyklus, Zugriffssteuerung und Compliance-Audits  
4. **Multi-Faktor-Authentifizierung**: Übernimmt MFA-Funktionen von Unternehmens-Identitätsanbietern  
5. **Bedingte Zugriffsrichtlinien**: Nutzt risikobasierte Zugriffskontrollen und adaptive Authentifizierung  

**Implementierungsanforderungen:**
- **Validierung des Token-Zielpublikums**: Überprüfen, dass alle Tokens explizit für den MCP-Server ausgestellt wurden  
- **Prüfung des Ausstellers**: Sicherstellen, dass der Token-Aussteller mit dem erwarteten Identitätsanbieter übereinstimmt  
- **Signaturprüfung**: Kryptografische Validierung der Token-Integrität  
- **Durchsetzung von Ablaufzeiten**: Strikte Einhaltung der Token-Lebensdauer  
- **Validierung des Geltungsbereichs**: Sicherstellen, dass Tokens die erforderlichen Berechtigungen für angeforderte Operationen enthalten  

### **Sicherheit der Autorisierungslogik**

**Kritische Kontrollen:**
- **Umfassende Autorisierungsprüfungen**: Regelmäßige Sicherheitsüberprüfungen aller Autorisierungsentscheidungen  
- **Fehlersichere Standards**: Zugriff verweigern, wenn die Autorisierungslogik keine eindeutige Entscheidung treffen kann  
- **Berechtigungsgrenzen**: Klare Trennung zwischen verschiedenen Berechtigungsebenen und Ressourcenzugriffen  
- **Audit-Protokollierung**: Vollständige Protokollierung aller Autorisierungsentscheidungen zur Sicherheitsüberwachung  
- **Regelmäßige Zugriffsüberprüfungen**: Periodische Validierung von Nutzerberechtigungen und Privilegienzuweisungen  

## 2. **Token-Sicherheit & Schutz vor Token-Durchleitung**

### **Verhinderung von Token-Durchleitung**

**Token-Durchleitung ist in der MCP-Autorisierungsspezifikation ausdrücklich verboten** aufgrund kritischer Sicherheitsrisiken:

**Adressierte Sicherheitsrisiken:**
- **Umgehung von Kontrollen**: Umgeht wesentliche Sicherheitskontrollen wie Ratenbegrenzung, Anfragenvalidierung und Verkehrsüberwachung  
- **Verlust der Verantwortlichkeit**: Erschwert die Identifikation von Clients, was Audit-Trails und Vorfalluntersuchungen beeinträchtigt  
- **Proxy-basierte Datenexfiltration**: Ermöglicht böswilligen Akteuren die Nutzung von Servern als Proxies für unbefugten Datenzugriff  
- **Verletzung von Vertrauensgrenzen**: Zerstört Annahmen über die Herkunft von Tokens bei nachgelagerten Diensten  
- **Laterale Bewegung**: Kompromittierte Tokens über mehrere Dienste hinweg ermöglichen eine breitere Angriffsausweitung  

**Implementierungskontrollen:**
```yaml
Token Validation Requirements:
  audience_validation: MANDATORY
  issuer_verification: MANDATORY  
  signature_check: MANDATORY
  expiration_enforcement: MANDATORY
  scope_validation: MANDATORY
  
Token Lifecycle Management:
  rotation_frequency: "Short-lived tokens preferred"
  secure_storage: "Azure Key Vault or equivalent"
  transmission_security: "TLS 1.3 minimum"
  replay_protection: "Implemented via nonce/timestamp"
```

### **Sichere Token-Management-Muster**

**Best Practices:**
- **Kurzlebige Tokens**: Minimierung des Expositionsfensters durch häufige Token-Rotation  
- **Just-in-Time-Ausstellung**: Tokens nur bei Bedarf für spezifische Operationen ausstellen  
- **Sichere Speicherung**: Verwendung von Hardware-Sicherheitsmodulen (HSMs) oder sicheren Schlüsselspeichern  
- **Token-Bindung**: Tokens an spezifische Clients, Sitzungen oder Operationen binden, wo möglich  
- **Überwachung & Alarmierung**: Echtzeit-Erkennung von Token-Missbrauch oder unbefugten Zugriffsmustern  

## 3. **Sicherheitskontrollen für Sitzungen**

### **Verhinderung von Sitzungsübernahmen**

**Adressierte Angriffsvektoren:**
- **Sitzungsübernahme durch Eingabeaufforderung**: Böswillige Ereignisse, die in den gemeinsamen Sitzungsstatus injiziert werden  
- **Sitzungsimitation**: Unbefugte Nutzung gestohlener Sitzungs-IDs zur Umgehung der Authentifizierung  
- **Angriffe auf wiederaufnehmbare Streams**: Ausnutzung der Wiederaufnahme von Server-gesendeten Ereignissen für bösartige Inhalte  

**Verpflichtende Sitzungs-Kontrollen:**
```yaml
Session ID Generation:
  randomness_source: "Cryptographically secure RNG"
  entropy_bits: 128 # Minimum recommended
  format: "Base64url encoded"
  predictability: "MUST be non-deterministic"

Session Binding:
  user_binding: "REQUIRED - <user_id>:<session_id>"
  additional_identifiers: "Device fingerprint, IP validation"
  context_binding: "Request origin, user agent validation"
  
Session Lifecycle:
  expiration: "Configurable timeout policies"
  rotation: "After privilege escalation events"
  invalidation: "Immediate on security events"
  cleanup: "Automated expired session removal"
```

**Transportsicherheit:**
- **Erzwingung von HTTPS**: Alle Sitzungs-Kommunikation über TLS 1.3  
- **Sichere Cookie-Attribute**: HttpOnly, Secure, SameSite=Strict  
- **Zertifikat-Pinning**: Für kritische Verbindungen zur Verhinderung von MITM-Angriffen  

### **Überlegungen zu zustandsbehafteten vs. zustandslosen Implementierungen**

**Für zustandsbehaftete Implementierungen:**
- Gemeinsamer Sitzungsstatus erfordert zusätzlichen Schutz vor Injektionsangriffen  
- Sitzungsmanagement auf Warteschlangenbasis benötigt Integritätsüberprüfung  
- Mehrere Serverinstanzen erfordern sichere Synchronisation des Sitzungsstatus  

**Für zustandslose Implementierungen:**
- JWT oder ähnliche tokenbasierte Sitzungsverwaltung  
- Kryptografische Überprüfung der Sitzungsstatus-Integrität  
- Reduzierte Angriffsfläche, aber robuste Token-Validierung erforderlich  

## 4. **KI-spezifische Sicherheitskontrollen**

### **Schutz vor Eingabeaufforderungs-Injektionen**

**Integration von Microsoft Prompt Shields:**
```yaml
Detection Mechanisms:
  - "Advanced ML-based instruction detection"
  - "Contextual analysis of external content"
  - "Real-time threat pattern recognition"
  
Protection Techniques:
  - "Spotlighting trusted vs untrusted content"
  - "Delimiter systems for content boundaries"  
  - "Data marking for content source identification"
  
Integration Points:
  - "Azure Content Safety service"
  - "Real-time content filtering"
  - "Threat intelligence updates"
```

**Implementierungskontrollen:**
- **Eingabevalidierung**: Umfassende Überprüfung und Filterung aller Nutzereingaben  
- **Definition von Inhaltsgrenzen**: Klare Trennung zwischen Systemanweisungen und Nutzerinhalten  
- **Anweisungshierarchie**: Korrekte Priorisierungsregeln für widersprüchliche Anweisungen  
- **Ausgabeüberwachung**: Erkennung potenziell schädlicher oder manipulierter Ausgaben  

### **Verhinderung von Tool-Vergiftungen**

**Sicherheitsrahmen für Tools:**
```yaml
Tool Definition Protection:
  validation:
    - "Schema validation against expected formats"
    - "Content analysis for malicious instructions" 
    - "Parameter injection detection"
    - "Hidden instruction identification"
  
  integrity_verification:
    - "Cryptographic hashing of tool definitions"
    - "Digital signatures for tool packages"
    - "Version control with change auditing"
    - "Tamper detection mechanisms"
  
  monitoring:
    - "Real-time change detection"
    - "Behavioral analysis of tool usage"
    - "Anomaly detection for execution patterns"
    - "Automated alerting for suspicious modifications"
```

**Dynamisches Tool-Management:**
- **Genehmigungs-Workflows**: Explizite Nutzerzustimmung für Tool-Änderungen  
- **Rollback-Funktionen**: Möglichkeit zur Wiederherstellung vorheriger Tool-Versionen  
- **Änderungsüberwachung**: Vollständige Historie von Tool-Definitionen  
- **Risikobewertung**: Automatisierte Bewertung der Sicherheit von Tools  

## 5. **Verhinderung von Confused Deputy-Angriffen**

### **OAuth-Proxy-Sicherheit**

**Angriffsverhinderungs-Kontrollen:**
```yaml
Client Registration:
  static_client_protection:
    - "Explicit user consent for dynamic registration"
    - "Consent bypass prevention mechanisms"  
    - "Cookie-based consent validation"
    - "Redirect URI strict validation"
    
  authorization_flow:
    - "PKCE implementation (OAuth 2.1)"
    - "State parameter validation"
    - "Authorization code binding"
    - "Nonce verification for ID tokens"
```

**Implementierungsanforderungen:**
- **Überprüfung der Nutzerzustimmung**: Zustimmungsschirme für dynamische Client-Registrierungen niemals überspringen  
- **Validierung von Redirect-URIs**: Strikte Whitelist-basierte Validierung von Weiterleitungszielen  
- **Schutz von Autorisierungscodes**: Kurzlebige Codes mit Einmalverwendung durchsetzen  
- **Validierung der Client-Identität**: Robuste Überprüfung von Client-Anmeldedaten und Metadaten  

## 6. **Sicherheit bei Tool-Ausführung**

### **Sandboxing & Isolation**

**Containerbasierte Isolation:**
```yaml
Execution Environment:
  containerization: "Docker/Podman with security profiles"
  resource_limits:
    cpu: "Configurable CPU quotas"
    memory: "Memory usage restrictions"
    disk: "Storage access limitations"
    network: "Network policy enforcement"
  
  privilege_restrictions:
    user_context: "Non-root execution mandatory"
    capability_dropping: "Remove unnecessary Linux capabilities"
    syscall_filtering: "Seccomp profiles for syscall restriction"
    filesystem: "Read-only root with minimal writable areas"
```

**Prozessisolation:**
- **Separate Prozesskontexte**: Jede Tool-Ausführung in isoliertem Prozessraum  
- **Interprozesskommunikation**: Sichere IPC-Mechanismen mit Validierung  
- **Prozessüberwachung**: Laufzeitanalyse des Verhaltens und Anomalieerkennung  
- **Ressourcendurchsetzung**: Harte Grenzen für CPU, Speicher und I/O-Operationen  

### **Implementierung des Minimalprinzips**

**Berechtigungsmanagement:**
```yaml
Access Control:
  file_system:
    - "Minimal required directory access"
    - "Read-only access where possible"
    - "Temporary file cleanup automation"
    
  network_access:
    - "Explicit allowlist for external connections"
    - "DNS resolution restrictions" 
    - "Port access limitations"
    - "SSL/TLS certificate validation"
  
  system_resources:
    - "No administrative privilege elevation"
    - "Limited system call access"
    - "No hardware device access"
    - "Restricted environment variable access"
```

## 7. **Sicherheitskontrollen für die Lieferkette**

### **Überprüfung von Abhängigkeiten**

**Umfassende Komponentensicherheit:**
```yaml
Software Dependencies:
  scanning: 
    - "Automated vulnerability scanning (GitHub Advanced Security)"
    - "License compliance verification"
    - "Known vulnerability database checks"
    - "Malware detection and analysis"
  
  verification:
    - "Package signature verification"
    - "Checksum validation"
    - "Provenance attestation"
    - "Software Bill of Materials (SBOM)"

AI Components:
  model_verification:
    - "Model provenance validation"
    - "Training data source verification" 
    - "Model behavior testing"
    - "Adversarial robustness assessment"
  
  service_validation:
    - "Third-party API security assessment"
    - "Service level agreement review"
    - "Data handling compliance verification"
    - "Incident response capability evaluation"
```

### **Kontinuierliche Überwachung**

**Erkennung von Bedrohungen in der Lieferkette:**
- **Überwachung der Abhängigkeitsgesundheit**: Kontinuierliche Bewertung aller Abhängigkeiten auf Sicherheitsprobleme  
- **Integration von Bedrohungsinformationen**: Echtzeit-Updates zu neuen Bedrohungen in der Lieferkette  
- **Verhaltensanalyse**: Erkennung ungewöhnlichen Verhaltens externer Komponenten  
- **Automatisierte Reaktion**: Sofortige Eindämmung kompromittierter Komponenten  

## 8. **Überwachungs- und Erkennungskontrollen**

### **Security Information and Event Management (SIEM)**

**Umfassende Protokollierungsstrategie:**
```yaml
Authentication Events:
  - "All authentication attempts (success/failure)"
  - "Token issuance and validation events"
  - "Session creation, modification, termination"
  - "Authorization decisions and policy evaluations"

Tool Execution:
  - "Tool invocation details and parameters"
  - "Execution duration and resource usage"
  - "Output generation and content analysis"
  - "Error conditions and exception handling"

Security Events:
  - "Potential prompt injection attempts"
  - "Tool poisoning detection events"
  - "Session hijacking indicators"
  - "Unusual access patterns and anomalies"
```

### **Echtzeit-Bedrohungserkennung**

**Verhaltensanalytik:**
- **Analyse des Nutzerverhaltens (UBA)**: Erkennung ungewöhnlicher Zugriffsmuster von Nutzern  
- **Analyse des Entitätenverhaltens (EBA)**: Überwachung des Verhaltens von MCP-Servern und Tools  
- **Anomalieerkennung durch maschinelles Lernen**: KI-gestützte Identifikation von Sicherheitsbedrohungen  
- **Korrelation von Bedrohungsinformationen**: Abgleich beobachteter Aktivitäten mit bekannten Angriffsmustern  

## 9. **Vorfallreaktion & Wiederherstellung**

### **Automatisierte Reaktionsfähigkeiten**

**Sofortige Reaktionsmaßnahmen:**
```yaml
Threat Containment:
  session_management:
    - "Immediate session termination"
    - "Account lockout procedures"
    - "Access privilege revocation"
  
  system_isolation:
    - "Network segmentation activation"
    - "Service isolation protocols"
    - "Communication channel restriction"

Recovery Procedures:
  credential_rotation:
    - "Automated token refresh"
    - "API key regeneration"
    - "Certificate renewal"
  
  system_restoration:
    - "Clean state restoration"
    - "Configuration rollback"
    - "Service restart procedures"
```

### **Forensische Fähigkeiten**

**Unterstützung bei Untersuchungen:**
- **Erhaltung von Audit-Trails**: Unveränderliche Protokollierung mit kryptografischer Integrität  
- **Beweissammlung**: Automatisierte Erfassung relevanter Sicherheitsartefakte  
- **Rekonstruktion von Zeitabläufen**: Detaillierte Sequenz von Ereignissen, die zu Sicherheitsvorfällen führten  
- **Bewertung der Auswirkungen**: Analyse des Umfangs der Kompromittierung und der Datenexposition  

## **Wichtige Prinzipien der Sicherheitsarchitektur**

### **Verteidigung in der Tiefe**
- **Mehrere Sicherheitsschichten**: Kein einzelner Ausfallpunkt in der Sicherheitsarchitektur  
- **Redundante Kontrollen**: Überlappende Sicherheitsmaßnahmen für kritische Funktionen  
- **Fehlersichere Mechanismen**: Sichere Standards bei Systemfehlern oder Angriffen  

### **Zero-Trust-Implementierung**
- **Niemals vertrauen, immer überprüfen**: Kontinuierliche Validierung aller Entitäten und Anfragen  
- **Minimalprinzip**: Minimale Zugriffsrechte für alle Komponenten  
- **Mikrosegmentierung**: Granulare Netzwerk- und Zugriffskontrollen  

### **Kontinuierliche Sicherheitsentwicklung**
- **Anpassung an Bedrohungslandschaft**: Regelmäßige Updates zur Adressierung neuer Bedrohungen  
- **Effektivität der Sicherheitskontrollen**: Laufende Bewertung und Verbesserung der Kontrollen  
- **Einhaltung der Spezifikationen**: Ausrichtung an den sich weiterentwickelnden MCP-Sicherheitsstandards  

---

## **Ressourcen zur Implementierung**

### **Offizielle MCP-Dokumentation**
- [MCP-Spezifikation (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP-Sicherheitsbest Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP-Autorisierungsspezifikation](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft-Sicherheitslösungen**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Sicherheitsstandards**
- [OAuth 2.0 Sicherheitsbest Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 für Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Wichtig**: Diese Sicherheitskontrollen spiegeln die aktuelle MCP-Spezifikation (2025-06-18) wider. Überprüfen Sie stets die [offizielle Dokumentation](https://spec.modelcontextprotocol.io/), da sich Standards schnell weiterentwickeln.  

**Haftungsausschluss**:  
Dieses Dokument wurde mithilfe des KI-Übersetzungsdienstes [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, weisen wir darauf hin, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner ursprünglichen Sprache sollte als maßgebliche Quelle betrachtet werden. Für kritische Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Nutzung dieser Übersetzung entstehen.