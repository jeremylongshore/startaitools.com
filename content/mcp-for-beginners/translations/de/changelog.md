<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T21:57:19+00:00",
  "source_file": "changelog.md",
  "language_code": "de"
}
-->
# Änderungsprotokoll: MCP für Anfänger Curriculum

Dieses Dokument dient als Aufzeichnung aller wesentlichen Änderungen am Curriculum des Model Context Protocol (MCP) für Anfänger. Änderungen werden in umgekehrt chronologischer Reihenfolge dokumentiert (neueste Änderungen zuerst).

## 6. Oktober 2025

### Erweiterung des Abschnitts "Erste Schritte" – Erweiterte Servernutzung & Einfache Authentifizierung

#### Erweiterte Servernutzung (03-GettingStarted/10-advanced)
- **Neues Kapitel hinzugefügt**: Einführung in die erweiterte Nutzung von MCP-Servern, einschließlich regulärer und Low-Level-Serverarchitekturen.
  - **Reguläre vs. Low-Level-Server**: Detaillierter Vergleich und Codebeispiele in Python und TypeScript für beide Ansätze.
  - **Handler-basierte Gestaltung**: Erklärung der handler-basierten Verwaltung von Tools/Ressourcen/Prompts für skalierbare und flexible Serverimplementierungen.
  - **Praktische Muster**: Szenarien aus der Praxis, in denen Low-Level-Servermuster für erweiterte Funktionen und Architekturen von Vorteil sind.

#### Einfache Authentifizierung (03-GettingStarted/11-simple-auth)
- **Neues Kapitel hinzugefügt**: Schritt-für-Schritt-Anleitung zur Implementierung einfacher Authentifizierung in MCP-Servern.
  - **Auth-Konzepte**: Klare Erklärung von Authentifizierung vs. Autorisierung und Umgang mit Zugangsdaten.
  - **Implementierung der Basis-Authentifizierung**: Middleware-basierte Authentifizierungsmuster in Python (Starlette) und TypeScript (Express) mit Codebeispielen.
  - **Fortschritt zu erweiterter Sicherheit**: Anleitung zum Einstieg mit einfacher Authentifizierung und Weiterentwicklung zu OAuth 2.1 und RBAC, mit Verweisen auf erweiterte Sicherheitsmodule.

Diese Ergänzungen bieten praktische, praxisorientierte Anleitungen für den Aufbau robuster, sicherer und flexibler MCP-Serverimplementierungen und schlagen eine Brücke zwischen grundlegenden Konzepten und fortgeschrittenen Produktionsmustern.

## 29. September 2025

### MCP Server Datenbank-Integrations-Labs – Umfassender praxisorientierter Lernpfad

#### 11-MCPServerHandsOnLabs - Neuer vollständiger Lehrplan zur Datenbankintegration
- **Vollständiger 13-Lab-Lernpfad**: Hinzugefügt wurde ein umfassender praxisorientierter Lehrplan für den Aufbau produktionsreifer MCP-Server mit PostgreSQL-Datenbankintegration.
  - **Praxisnahe Implementierung**: Zava Retail Analytics Anwendungsfall, der Unternehmensmuster demonstriert.
  - **Strukturierter Lernfortschritt**:
    - **Labs 00-03: Grundlagen** - Einführung, Kernarchitektur, Sicherheit & Multi-Tenancy, Einrichtung der Umgebung
    - **Labs 04-06: Aufbau des MCP-Servers** - Datenbankdesign & Schema, MCP-Server-Implementierung, Tool-Entwicklung  
    - **Labs 07-09: Erweiterte Funktionen** - Integration semantischer Suche, Testen & Debugging, VS Code-Integration
    - **Labs 10-12: Produktion & Best Practices** - Bereitstellungsstrategien, Überwachung & Beobachtbarkeit, Best Practices & Optimierung
  - **Unternehmens-Technologien**: FastMCP-Framework, PostgreSQL mit pgvector, Azure OpenAI-Embeddings, Azure Container Apps, Application Insights
  - **Erweiterte Funktionen**: Row Level Security (RLS), semantische Suche, Multi-Tenant-Datenzugriff, Vektor-Embeddings, Echtzeitüberwachung

#### Terminologie-Standardisierung - Umstellung von Modul auf Lab
- **Umfassende Dokumentationsaktualisierung**: Systematische Aktualisierung aller README-Dateien in 11-MCPServerHandsOnLabs zur Verwendung der Terminologie "Lab" statt "Modul".
  - **Abschnittsüberschriften**: Aktualisiert "Was dieses Modul behandelt" zu "Was dieses Lab behandelt" in allen 13 Labs.
  - **Inhaltsbeschreibung**: Geändert von "Dieses Modul bietet..." zu "Dieses Lab bietet..." in der gesamten Dokumentation.
  - **Lernziele**: Aktualisiert von "Am Ende dieses Moduls..." zu "Am Ende dieses Labs..."
  - **Navigationslinks**: Alle Verweise auf "Modul XX:" wurden zu "Lab XX:" in Querverweisen und Navigation umgewandelt.
  - **Abschlussverfolgung**: Aktualisiert von "Nach Abschluss dieses Moduls..." zu "Nach Abschluss dieses Labs..."
  - **Technische Referenzen beibehalten**: Python-Modulreferenzen in Konfigurationsdateien (z. B. `"module": "mcp_server.main"`) wurden unverändert gelassen.

#### Verbesserung des Studienleitfadens (study_guide.md)
- **Visuelle Lehrplanübersicht**: Neuer Abschnitt "11. Datenbank-Integrations-Labs" mit umfassender Lab-Strukturvisualisierung hinzugefügt.
- **Repository-Struktur**: Aktualisiert von zehn auf elf Hauptabschnitte mit detaillierter Beschreibung von 11-MCPServerHandsOnLabs.
- **Lernpfad-Anleitung**: Verbesserte Navigationsanweisungen für die Abschnitte 00-11.
- **Technologieabdeckung**: Details zur Integration von FastMCP, PostgreSQL und Azure-Diensten hinzugefügt.
- **Lernergebnisse**: Betonung auf produktionsreife Serverentwicklung, Datenbankintegrationsmuster und Unternehmenssicherheit.

#### Verbesserung der Haupt-README-Struktur
- **Lab-basierte Terminologie**: Haupt-README.md in 11-MCPServerHandsOnLabs aktualisiert, um konsistent die "Lab"-Struktur zu verwenden.
- **Organisation des Lernpfads**: Klare Progression von grundlegenden Konzepten über erweiterte Implementierung bis hin zur Produktionsbereitstellung.
- **Praxisorientierung**: Betonung auf praktischem, praxisorientiertem Lernen mit Unternehmensmustern und Technologien.

### Verbesserungen der Dokumentationsqualität & Konsistenz
- **Betonung des praxisorientierten Lernens**: Verstärkung des praktischen, lab-basierten Ansatzes in der gesamten Dokumentation.
- **Fokus auf Unternehmensmuster**: Hervorhebung produktionsreifer Implementierungen und Überlegungen zur Unternehmenssicherheit.
- **Technologieintegration**: Umfassende Abdeckung moderner Azure-Dienste und KI-Integrationsmuster.
- **Lernfortschritt**: Klarer, strukturierter Weg von grundlegenden Konzepten bis zur Produktionsbereitstellung.

## 26. September 2025

### Verbesserung der Fallstudien – GitHub MCP Registry Integration

#### Fallstudien (09-CaseStudy/) - Fokus auf Ökosystementwicklung
- **README.md**: Umfangreiche Erweiterung mit einer umfassenden Fallstudie zur GitHub MCP Registry.
  - **GitHub MCP Registry Fallstudie**: Neue umfassende Fallstudie zur Einführung des GitHub MCP Registry im September 2025.
    - **Problemanalyse**: Detaillierte Untersuchung der Herausforderungen bei der fragmentierten Entdeckung und Bereitstellung von MCP-Servern.
    - **Lösungsarchitektur**: Zentralisierter Registry-Ansatz von GitHub mit Installation per Mausklick in VS Code.
    - **Geschäftliche Auswirkungen**: Messbare Verbesserungen bei der Entwickler-Einarbeitung und Produktivität.
    - **Strategischer Wert**: Fokus auf modulare Agentenbereitstellung und Interoperabilität zwischen Tools.
    - **Ökosystementwicklung**: Positionierung als grundlegende Plattform für agentenbasierte Integration.
  - **Verbesserte Struktur der Fallstudien**: Alle sieben Fallstudien mit konsistenter Formatierung und umfassenden Beschreibungen aktualisiert.
    - Azure AI Travel Agents: Schwerpunkt auf Multi-Agenten-Orchestrierung.
    - Azure DevOps Integration: Fokus auf Workflow-Automatisierung.
    - Echtzeit-Dokumentationsabruf: Python-Konsolenclient-Implementierung.
    - Interaktiver Studienplan-Generator: Chainlit-konversationale Web-App.
    - In-Editor-Dokumentation: VS Code und GitHub Copilot Integration.
    - Azure API Management: Unternehmens-API-Integrationsmuster.
    - GitHub MCP Registry: Ökosystementwicklung und Community-Plattform.
  - **Umfassender Abschluss**: Neu geschriebener Abschnitt, der sieben Fallstudien hervorhebt, die mehrere MCP-Implementierungsdimensionen abdecken.
    - Unternehmensintegration, Multi-Agenten-Orchestrierung, Entwicklerproduktivität.
    - Ökosystementwicklung, Bildungsanwendungen Kategorisierung.
    - Verbesserte Einblicke in Architektur-Muster, Implementierungsstrategien und Best Practices.
    - Betonung von MCP als ausgereiftem, produktionsbereitem Protokoll.

#### Updates des Studienleitfadens (study_guide.md)
- **Visuelle Lehrplanübersicht**: Mindmap aktualisiert, um GitHub MCP Registry im Abschnitt Fallstudien einzuschließen.
- **Beschreibung der Fallstudien**: Von allgemeinen Beschreibungen zu detaillierten Aufschlüsselungen der sieben umfassenden Fallstudien erweitert.
- **Repository-Struktur**: Abschnitt 10 aktualisiert, um umfassende Fallstudienabdeckung mit spezifischen Implementierungsdetails widerzuspiegeln.
- **Integration des Änderungsprotokolls**: Eintrag vom 26. September 2025 hinzugefügt, der die Ergänzung der GitHub MCP Registry und die Verbesserungen der Fallstudien dokumentiert.
- **Datumsaktualisierungen**: Fußzeilen-Zeitstempel aktualisiert, um die neueste Revision (26. September 2025) widerzuspiegeln.

### Verbesserungen der Dokumentationsqualität
- **Konsistenzverbesserung**: Standardisierte Formatierung und Struktur der Fallstudien über alle sieben Beispiele hinweg.
- **Umfassende Abdeckung**: Fallstudien decken nun Szenarien aus Unternehmensintegration, Entwicklerproduktivität und Ökosystementwicklung ab.
- **Strategische Positionierung**: Verbesserter Fokus auf MCP als grundlegende Plattform für die Bereitstellung agentenbasierter Systeme.
- **Ressourcenintegration**: Zusätzliche Ressourcen aktualisiert, um den Link zur GitHub MCP Registry einzuschließen.

## 15. September 2025

### Erweiterung der fortgeschrittenen Themen – Benutzerdefinierte Transports & Kontext-Engineering

#### MCP Benutzerdefinierte Transports (05-AdvancedTopics/mcp-transport/) - Neuer Leitfaden für fortgeschrittene Implementierungen
- **README.md**: Vollständiger Implementierungsleitfaden für benutzerdefinierte MCP-Transportmechanismen.
  - **Azure Event Grid Transport**: Umfassende serverlose ereignisgesteuerte Transportimplementierung.
    - Beispiele in C#, TypeScript und Python mit Azure Functions-Integration.
    - Architektur-Muster für skalierbare MCP-Lösungen.
    - Webhook-Empfänger und push-basierte Nachrichtenverarbeitung.
  - **Azure Event Hubs Transport**: Implementierung eines Hochdurchsatz-Streaming-Transports.
    - Echtzeit-Streaming-Funktionen für Szenarien mit niedriger Latenz.
    - Partitionierungsstrategien und Checkpoint-Management.
    - Nachrichtenbündelung und Leistungsoptimierung.
  - **Unternehmens-Integrationsmuster**: Produktionsreife Architekturbeispiele.
    - Verteilte MCP-Verarbeitung über mehrere Azure Functions.
    - Hybride Transportarchitekturen, die mehrere Transporttypen kombinieren.
    - Strategien für Nachrichtenhaltbarkeit, Zuverlässigkeit und Fehlerbehandlung.
  - **Sicherheit & Überwachung**: Azure Key Vault-Integration und Beobachtungsmuster.
    - Authentifizierung mit verwalteten Identitäten und minimaler Zugriffsberechtigung.
    - Telemetrie und Leistungsüberwachung mit Application Insights.
    - Circuit Breaker und Fehlertoleranzmuster.
  - **Test-Frameworks**: Umfassende Teststrategien für benutzerdefinierte Transports.
    - Unit-Tests mit Test-Doubles und Mocking-Frameworks.
    - Integrationstests mit Azure Test Containers.
    - Leistungs- und Lasttestüberlegungen.

#### Kontext-Engineering (05-AdvancedTopics/mcp-contextengineering/) - Aufstrebende KI-Disziplin
- **README.md**: Umfassende Untersuchung des Kontext-Engineering als aufstrebendes Feld.
  - **Kernprinzipien**: Vollständige Kontextfreigabe, Bewusstsein für Aktionsentscheidungen und Verwaltung des Kontextfensters.
  - **MCP-Protokollausrichtung**: Wie MCP-Design Herausforderungen des Kontext-Engineering adressiert.
    - Begrenzungen des Kontextfensters und progressive Lade-Strategien.
    - Relevanzbestimmung und dynamische Kontextabrufmethoden.
    - Multi-modale Kontextverarbeitung und Sicherheitsüberlegungen.
  - **Implementierungsansätze**: Single-Threaded vs. Multi-Agenten-Architekturen.
    - Kontext-Chunks und Priorisierungstechniken.
    - Progressive Kontextladung und Komprimierungsstrategien.
    - Geschichtete Kontextansätze und Abrufoptimierung.
  - **Messrahmen**: Aufkommende Metriken zur Bewertung der Kontexteffektivität.
    - Eingabeeffizienz, Leistung, Qualität und Benutzererfahrungsüberlegungen.
    - Experimentelle Ansätze zur Kontextoptimierung.
    - Fehleranalyse und Verbesserungsmethoden.

#### Updates zur Curriculum-Navigation (README.md)
- **Verbesserte Modulstruktur**: Lehrplantabelle aktualisiert, um neue fortgeschrittene Themen einzuschließen.
  - Hinzugefügt: Kontext-Engineering (5.14) und Benutzerdefinierte Transports (5.15).
  - Konsistente Formatierung und Navigationslinks über alle Module hinweg.
  - Beschreibungen aktualisiert, um den aktuellen Inhaltsumfang widerzuspiegeln.

### Verbesserungen der Verzeichnisstruktur
- **Namensstandardisierung**: Umbenennung von "mcp transport" zu "mcp-transport" für Konsistenz mit anderen Ordnern für fortgeschrittene Themen.
- **Inhaltsorganisation**: Alle 05-AdvancedTopics-Ordner folgen nun einem konsistenten Namensmuster (mcp-[Thema]).

### Verbesserungen der Dokumentationsqualität
- **Ausrichtung an MCP-Spezifikation**: Alle neuen Inhalte beziehen sich auf die aktuelle MCP-Spezifikation 2025-06-18.
- **Mehrsprachige Beispiele**: Umfassende Codebeispiele in C#, TypeScript und Python.
- **Unternehmensfokus**: Produktionsreife Muster und Azure-Cloud-Integration durchgehend.
- **Visuelle Dokumentation**: Mermaid-Diagramme zur Architektur- und Ablaufvisualisierung.

## 18. August 2025

### Umfassendes Dokumentationsupdate – MCP 2025-06-18 Standards

#### MCP Sicherheits-Best Practices (02-Security/) - Vollständige Modernisierung
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Vollständige Überarbeitung gemäß MCP-Spezifikation 2025-06-18.
  - **Verpflichtende Anforderungen**: Hinzugefügt wurden explizite MUSS/MUSS NICHT-Anforderungen aus der offiziellen Spezifikation mit klaren visuellen Indikatoren.
  - **12 Kern-Sicherheitspraktiken**: Umstrukturiert von einer 15-Punkte-Liste zu umfassenden Sicherheitsdomänen.
    - Token-Sicherheit & Authentifizierung mit Integration externer Identitätsanbieter.
    - Sitzungsmanagement & Transportsicherheit mit kryptografischen Anforderungen.
    - KI-spezifischer Bedrohungsschutz mit Microsoft Prompt Shields-Integration.
    - Zugriffskontrolle & Berechtigungen mit dem Prinzip der minimalen Berechtigung.
    - Inhaltsicherheit & Überwachung mit Azure Content Safety-Integration.
    - Lieferkettensicherheit mit umfassender Komponentenüberprüfung.
    - OAuth-Sicherheit & Vermeidung von Confused Deputy-Angriffen mit PKCE-Implementierung.
    - Vorfallreaktion & Wiederherstellung mit automatisierten Fähigkeiten.
    - Compliance & Governance mit regulatorischer Ausrichtung.
    - Erweiterte Sicherheitskontrollen mit Zero-Trust-Architektur.
    - Integration des Microsoft-Sicherheitsökosystems mit umfassenden Lösungen.
    - Kontinuierliche Sicherheitsentwicklung mit adaptiven Praktiken.
  - **Microsoft Sicherheitslösungen**: Verbesserte Integrationsanleitung für Prompt Shields, Azure Content Safety, Entra ID und GitHub Advanced Security.
  - **Implementierungsressourcen**: Umfassende Ressourcenkategorien nach Offizieller MCP-Dokumentation, Microsoft Sicherheitslösungen, Sicherheitsstandards und Implementierungsleitfäden.

#### Erweiterte Sicherheitskontrollen (02-Security/) - Unternehmensimplementierung
- **MCP-SECURITY-CONTROLS-2025.md**: Vollständige Überarbeitung mit einem unternehmensgerechten Sicherheitsrahmen.
  - **9 umfassende Sicherheitsdomänen**: Erweiterung von grundlegenden Kontrollen zu einem detaillierten Unternehmensrahmen.
    - Erweiterte Authentifizierung & Autorisierung mit Microsoft Entra ID-Integration.
    - Token-Sicherheit & Anti-Passthrough-Kontrollen mit umfassender Validierung.
    - Sicherheitskontrollen für Sitzungen mit Schutz vor Hijacking.
    - KI-spezifische Sicherheitskontrollen mit Schutz vor Prompt-Injection und Tool-Vergiftung.
    - Vermeidung von Confused Deputy-Angriffen mit OAuth-Proxy-Sicherheit.
    - Tool-Ausführungssicherheit mit Sandboxing und Isolation.
    - Sicherheitskontrollen für die Lieferkette mit Abhängigkeitsüberprüfung.
    - Überwachungs- & Erkennungskontrollen mit SIEM-Integration.
    - Vorfallreaktion & Wiederherstellung mit automatisierten Fähigkeiten.
  - **Implementierungsbeispiele**: Detaillierte YAML-Konfigurationsblöcke und Codebeispiele hinzugefügt.
  - **Integration von Microsoft-Lösungen**: Umfassende Abdeckung von Azure-Sicherheitsdiensten, GitHub Advanced Security und Unternehmensidentitätsmanagement.
#### Erweiterte Themen Sicherheit (05-AdvancedTopics/mcp-security/) - Produktionsreife Implementierung
- **README.md**: Vollständige Überarbeitung für die Implementierung von Unternehmenssicherheit
  - **Aktuelle Spezifikationsausrichtung**: Aktualisiert auf MCP-Spezifikation 2025-06-18 mit obligatorischen Sicherheitsanforderungen
  - **Erweiterte Authentifizierung**: Integration von Microsoft Entra ID mit umfassenden .NET- und Java-Spring-Security-Beispielen
  - **KI-Sicherheitsintegration**: Implementierung von Microsoft Prompt Shields und Azure Content Safety mit detaillierten Python-Beispielen
  - **Erweiterte Bedrohungsminderung**: Umfassende Implementierungsbeispiele für
    - Verhinderung von Confused Deputy Attacken mit PKCE und Validierung der Benutzerzustimmung
    - Verhinderung von Token-Passthrough mit Zielgruppenvalidierung und sicherem Token-Management
    - Verhinderung von Session Hijacking mit kryptografischer Bindung und Verhaltensanalyse
  - **Integration von Unternehmenssicherheit**: Überwachung mit Azure Application Insights, Bedrohungserkennungspipelines und Sicherheit der Lieferkette
  - **Implementierungs-Checkliste**: Klare Unterscheidung zwischen obligatorischen und empfohlenen Sicherheitskontrollen mit Vorteilen des Microsoft-Sicherheitsökosystems

### Dokumentationsqualität & Standardsausrichtung
- **Spezifikationsreferenzen**: Alle Referenzen auf die aktuelle MCP-Spezifikation 2025-06-18 aktualisiert
- **Microsoft-Sicherheitsökosystem**: Verbesserte Integrationsanleitung in der gesamten Sicherheitsdokumentation
- **Praktische Implementierung**: Detaillierte Codebeispiele in .NET, Java und Python mit Unternehmensmustern hinzugefügt
- **Ressourcenorganisation**: Umfassende Kategorisierung offizieller Dokumentation, Sicherheitsstandards und Implementierungsleitfäden
- **Visuelle Indikatoren**: Klare Kennzeichnung von obligatorischen Anforderungen gegenüber empfohlenen Praktiken

#### Kernkonzepte (01-CoreConcepts/) - Vollständige Modernisierung
- **Protokollversions-Update**: Aktualisiert auf die aktuelle MCP-Spezifikation 2025-06-18 mit datumsbasierter Versionierung (Format YYYY-MM-DD)
- **Architekturverfeinerung**: Verbesserte Beschreibungen von Hosts, Clients und Servern, um aktuelle MCP-Architekturmuster widerzuspiegeln
  - Hosts jetzt klar definiert als KI-Anwendungen, die mehrere MCP-Client-Verbindungen koordinieren
  - Clients beschrieben als Protokoll-Connectoren mit Eins-zu-eins-Server-Beziehungen
  - Server erweitert mit Szenarien für lokale und entfernte Bereitstellungen
- **Überarbeitung der Primitiven**: Vollständige Überarbeitung der Server- und Client-Primitiven
  - Server-Primitiven: Ressourcen (Datenquellen), Prompts (Vorlagen), Tools (ausführbare Funktionen) mit detaillierten Erklärungen und Beispielen
  - Client-Primitiven: Sampling (LLM-Abschlüsse), Elicitation (Benutzereingaben), Logging (Debugging/Monitoring)
  - Aktualisiert mit aktuellen Discovery- (`*/list`), Retrieval- (`*/get`) und Execution- (`*/call`) Methodenmustern
- **Protokollarchitektur**: Einführung eines Zwei-Schichten-Architekturmodells
  - Datenebene: JSON-RPC 2.0 Grundlage mit Lebenszyklusmanagement und Primitiven
  - Transporteebene: STDIO (lokal) und Streamable HTTP mit SSE (entfernte) Transportmechanismen
- **Sicherheitsrahmen**: Umfassende Sicherheitsprinzipien einschließlich expliziter Benutzerzustimmung, Datenschutz, Sicherheit bei der Tool-Ausführung und Sicherheit der Transporteebene
- **Kommunikationsmuster**: Aktualisierte Protokollnachrichten zur Darstellung von Initialisierungs-, Discovery-, Ausführungs- und Benachrichtigungsabläufen
- **Codebeispiele**: Aktualisierte mehrsprachige Beispiele (.NET, Java, Python, JavaScript), die aktuelle MCP-SDK-Muster widerspiegeln

#### Sicherheit (02-Security/) - Umfassende Sicherheitsüberarbeitung  
- **Standardsausrichtung**: Vollständige Ausrichtung auf die Sicherheitsanforderungen der MCP-Spezifikation 2025-06-18
- **Entwicklung der Authentifizierung**: Dokumentierte Entwicklung von benutzerdefinierten OAuth-Servern hin zu Delegation an externe Identitätsanbieter (Microsoft Entra ID)
- **KI-spezifische Bedrohungsanalyse**: Erweiterte Abdeckung moderner KI-Angriffsszenarien
  - Detaillierte Szenarien für Prompt-Injection-Angriffe mit realen Beispielen
  - Mechanismen zur Tool-Vergiftung und "Rug Pull"-Angriffsmuster
  - Kontextfenster-Vergiftung und Modellverwirrungsangriffe
- **Microsoft KI-Sicherheitslösungen**: Umfassende Abdeckung des Microsoft-Sicherheitsökosystems
  - KI-Prompt Shields mit fortschrittlicher Erkennung, Hervorhebung und Trenntechniken
  - Azure Content Safety-Integrationsmuster
  - GitHub Advanced Security für den Schutz der Lieferkette
- **Erweiterte Bedrohungsminderung**: Detaillierte Sicherheitskontrollen für
  - Session Hijacking mit MCP-spezifischen Angriffsszenarien und kryptografischen Sitzungs-ID-Anforderungen
  - Confused Deputy-Probleme in MCP-Proxy-Szenarien mit expliziten Zustimmungsanforderungen
  - Token-Passthrough-Schwachstellen mit obligatorischen Validierungskontrollen
- **Sicherheit der Lieferkette**: Erweiterte Abdeckung der KI-Lieferkette einschließlich Basis-Modellen, Embedding-Diensten, Kontextanbietern und Drittanbieter-APIs
- **Grundlagensicherheit**: Verbesserte Integration mit Unternehmenssicherheitsmustern einschließlich Zero-Trust-Architektur und Microsoft-Sicherheitsökosystem
- **Ressourcenorganisation**: Umfassende Kategorisierung von Ressourcenlinks nach Typ (Offizielle Dokumente, Standards, Forschung, Microsoft-Lösungen, Implementierungsleitfäden)

### Verbesserungen der Dokumentationsqualität
- **Strukturierte Lernziele**: Verbesserte Lernziele mit spezifischen, umsetzbaren Ergebnissen 
- **Querverweise**: Links zwischen verwandten Sicherheits- und Kernkonzeptthemen hinzugefügt
- **Aktuelle Informationen**: Alle Datumsreferenzen und Spezifikationslinks auf aktuelle Standards aktualisiert
- **Implementierungsleitfaden**: Spezifische, umsetzbare Implementierungsrichtlinien in beiden Abschnitten hinzugefügt

## 16. Juli 2025

### Verbesserungen an README und Navigation
- Vollständig überarbeitete Navigationsstruktur im README.md
- Ersetzung der `<details>`-Tags durch ein zugänglicheres tabellenbasiertes Format
- Alternative Layoutoptionen im neuen Ordner "alternative_layouts" erstellt
- Kartenbasierte, registerkartenbasierte und akordeonbasierte Navigationsbeispiele hinzugefügt
- Abschnitt zur Repository-Struktur aktualisiert, um alle neuesten Dateien einzuschließen
- Abschnitt "Wie man dieses Curriculum verwendet" mit klaren Empfehlungen verbessert
- MCP-Spezifikationslinks aktualisiert, um auf die richtigen URLs zu verweisen
- Abschnitt Kontext-Engineering (5.14) zur Curriculum-Struktur hinzugefügt

### Aktualisierungen des Studienleitfadens
- Studienleitfaden vollständig überarbeitet, um mit der aktuellen Repository-Struktur übereinzustimmen
- Neue Abschnitte für MCP-Clients und Tools sowie beliebte MCP-Server hinzugefügt
- Visuelle Curriculum-Karte aktualisiert, um alle Themen genau widerzuspiegeln
- Beschreibungen der erweiterten Themen verbessert, um alle spezialisierten Bereiche abzudecken
- Abschnitt Fallstudien aktualisiert, um reale Beispiele widerzuspiegeln
- Diesen umfassenden Änderungsprotokoll hinzugefügt

### Community-Beiträge (06-CommunityContributions/)
- Detaillierte Informationen zu MCP-Servern für die Bildgenerierung hinzugefügt
- Umfassender Abschnitt zur Verwendung von Claude in VSCode hinzugefügt
- Setup- und Nutzungsanweisungen für den Cline-Terminal-Client hinzugefügt
- MCP-Client-Abschnitt aktualisiert, um alle beliebten Client-Optionen einzuschließen
- Verbesserte Beitragsbeispiele mit genaueren Codebeispielen

### Erweiterte Themen (05-AdvancedTopics/)
- Alle spezialisierten Themenordner mit konsistenter Benennung organisiert
- Materialien und Beispiele zum Kontext-Engineering hinzugefügt
- Dokumentation zur Integration des Foundry-Agenten hinzugefügt
- Dokumentation zur Sicherheitsintegration von Entra ID verbessert

## 11. Juni 2025

### Erstmalige Erstellung
- Erste Version des MCP für Anfänger-Curriculums veröffentlicht
- Grundstruktur für alle 10 Hauptabschnitte erstellt
- Visuelle Curriculum-Karte für die Navigation implementiert
- Erste Beispielprojekte in mehreren Programmiersprachen hinzugefügt

### Erste Schritte (03-GettingStarted/)
- Erste Server-Implementierungsbeispiele erstellt
- Anleitung zur Client-Entwicklung hinzugefügt
- Anweisungen zur Integration von LLM-Clients hinzugefügt
- Dokumentation zur Integration von VS Code hinzugefügt
- Server-Sent-Events (SSE)-Server-Beispiele implementiert

### Kernkonzepte (01-CoreConcepts/)
- Detaillierte Erklärung der Client-Server-Architektur hinzugefügt
- Dokumentation zu den wichtigsten Protokollkomponenten erstellt
- Nachrichtenmuster im MCP dokumentiert

## 23. Mai 2025

### Repository-Struktur
- Repository mit grundlegender Ordnerstruktur initialisiert
- README-Dateien für jeden Hauptabschnitt erstellt
- Übersetzungsinfrastruktur eingerichtet
- Bildressourcen und Diagramme hinzugefügt

### Dokumentation
- Erste README.md mit Curriculum-Übersicht erstellt
- CODE_OF_CONDUCT.md und SECURITY.md hinzugefügt
- SUPPORT.md mit Hilfestellungen eingerichtet
- Vorläufige Struktur des Studienleitfadens erstellt

## 15. April 2025

### Planung und Rahmen
- Erste Planung für das MCP für Anfänger-Curriculum
- Lernziele und Zielgruppe definiert
- 10-Abschnitt-Struktur des Curriculums skizziert
- Konzeptueller Rahmen für Beispiele und Fallstudien entwickelt
- Erste Prototyp-Beispiele für Schlüsselkonzepte erstellt

---

**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner ursprünglichen Sprache sollte als maßgebliche Quelle betrachtet werden. Für kritische Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die sich aus der Nutzung dieser Übersetzung ergeben.