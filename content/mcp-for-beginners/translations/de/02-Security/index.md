<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T11:50:32+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "de"
}
-->
# MCP-Sicherheit: Umfassender Schutz für KI-Systeme

[![MCP Security Best Practices](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.de.png)](https://youtu.be/88No8pw706o)

_(Klicken Sie auf das Bild oben, um das Video zu dieser Lektion anzusehen)_

Sicherheit ist ein grundlegender Bestandteil des Designs von KI-Systemen, weshalb wir sie als zweiten Abschnitt priorisieren. Dies steht im Einklang mit Microsofts **Secure by Design**-Prinzip aus der [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Das Model Context Protocol (MCP) bietet leistungsstarke neue Funktionen für KI-gesteuerte Anwendungen, bringt jedoch einzigartige Sicherheitsherausforderungen mit sich, die über die traditionellen Software-Risiken hinausgehen. MCP-Systeme sind sowohl etablierten Sicherheitsbedenken (sicheres Programmieren, Prinzip der minimalen Rechte, Lieferkettensicherheit) als auch neuen KI-spezifischen Bedrohungen ausgesetzt, darunter Prompt Injection, Tool Poisoning, Session Hijacking, Confused Deputy-Angriffe, Token-Passthrough-Schwachstellen und dynamische Fähigkeitsmodifikationen.

Diese Lektion untersucht die kritischsten Sicherheitsrisiken bei MCP-Implementierungen – einschließlich Authentifizierung, Autorisierung, übermäßiger Berechtigungen, indirekter Prompt Injection, Sitzungs-Sicherheit, Confused Deputy-Problemen, Token-Management und Lieferketten-Schwachstellen. Sie lernen umsetzbare Kontrollen und Best Practices kennen, um diese Risiken zu mindern, und erfahren, wie Sie Microsoft-Lösungen wie Prompt Shields, Azure Content Safety und GitHub Advanced Security nutzen können, um Ihre MCP-Bereitstellung zu stärken.

## Lernziele

Am Ende dieser Lektion werden Sie in der Lage sein:

- **MCP-spezifische Bedrohungen zu identifizieren**: Erkennen Sie einzigartige Sicherheitsrisiken in MCP-Systemen, darunter Prompt Injection, Tool Poisoning, übermäßige Berechtigungen, Session Hijacking, Confused Deputy-Probleme, Token-Passthrough-Schwachstellen und Lieferketten-Risiken
- **Sicherheitskontrollen anzuwenden**: Implementieren Sie effektive Maßnahmen wie robuste Authentifizierung, Zugriff mit minimalen Rechten, sicheres Token-Management, Sitzungs-Sicherheitskontrollen und Lieferketten-Überprüfung
- **Microsoft-Sicherheitslösungen zu nutzen**: Verstehen und implementieren Sie Microsoft Prompt Shields, Azure Content Safety und GitHub Advanced Security zum Schutz von MCP-Workloads
- **Tool-Sicherheit zu validieren**: Erkennen Sie die Bedeutung der Validierung von Tool-Metadaten, der Überwachung dynamischer Änderungen und der Verteidigung gegen indirekte Prompt Injection-Angriffe
- **Best Practices zu integrieren**: Kombinieren Sie etablierte Sicherheitsgrundlagen (sicheres Programmieren, Server-Härtung, Zero Trust) mit MCP-spezifischen Kontrollen für umfassenden Schutz

# MCP-Sicherheitsarchitektur & Kontrollen

Moderne MCP-Implementierungen erfordern mehrschichtige Sicherheitsansätze, die sowohl traditionelle Software-Sicherheit als auch KI-spezifische Bedrohungen adressieren. Die sich schnell entwickelnde MCP-Spezifikation verbessert kontinuierlich ihre Sicherheitskontrollen und ermöglicht eine bessere Integration in Unternehmenssicherheitsarchitekturen und etablierte Best Practices.

Forschungen aus dem [Microsoft Digital Defense Report](https://aka.ms/mddr) zeigen, dass **98 % der gemeldeten Sicherheitsverletzungen durch robuste Sicherheitsmaßnahmen verhindert werden könnten**. Die effektivste Schutzstrategie kombiniert grundlegende Sicherheitspraktiken mit MCP-spezifischen Kontrollen – bewährte Basissicherheitsmaßnahmen bleiben die wirkungsvollsten zur Reduzierung des gesamten Sicherheitsrisikos.

## Aktuelle Sicherheitslandschaft

> **Hinweis:** Diese Informationen spiegeln die MCP-Sicherheitsstandards vom **18. August 2025** wider. Das MCP-Protokoll entwickelt sich schnell weiter, und zukünftige Implementierungen könnten neue Authentifizierungsmuster und verbesserte Kontrollen einführen. Konsultieren Sie stets die aktuelle [MCP-Spezifikation](https://spec.modelcontextprotocol.io/), das [MCP GitHub-Repository](https://github.com/modelcontextprotocol) und die [Dokumentation zu Sicherheitsbest Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) für die neuesten Richtlinien.

### Entwicklung der MCP-Authentifizierung

Die MCP-Spezifikation hat sich erheblich in ihrem Ansatz zur Authentifizierung und Autorisierung weiterentwickelt:

- **Ursprünglicher Ansatz**: Frühere Spezifikationen verlangten von Entwicklern die Implementierung benutzerdefinierter Authentifizierungsserver, wobei MCP-Server als OAuth 2.0-Authorisierungsserver fungierten und die Benutzer-Authentifizierung direkt verwalteten
- **Aktueller Standard (2025-06-18)**: Die aktualisierte Spezifikation ermöglicht es MCP-Servern, die Authentifizierung an externe Identitätsanbieter (wie Microsoft Entra ID) zu delegieren, wodurch die Sicherheitslage verbessert und die Implementierung vereinfacht wird
- **Transport Layer Security**: Verbesserte Unterstützung für sichere Transportmechanismen mit geeigneten Authentifizierungsmustern für lokale (STDIO) und entfernte (Streamable HTTP) Verbindungen

## Authentifizierungs- & Autorisierungs-Sicherheit

### Aktuelle Sicherheitsherausforderungen

Moderne MCP-Implementierungen stehen vor mehreren Herausforderungen bei Authentifizierung und Autorisierung:

### Risiken & Bedrohungsvektoren

- **Fehlkonfigurierte Autorisierungslogik**: Fehlerhafte Implementierung der Autorisierung in MCP-Servern kann sensible Daten offenlegen und Zugriffsrechte falsch anwenden
- **OAuth-Token-Kompromittierung**: Diebstahl lokaler MCP-Server-Token ermöglicht Angreifern, Server zu imitieren und auf nachgelagerte Dienste zuzugreifen
- **Token-Passthrough-Schwachstellen**: Unsachgemäße Token-Verarbeitung schafft Umgehungen von Sicherheitskontrollen und Lücken in der Verantwortlichkeit
- **Übermäßige Berechtigungen**: Überprivilegierte MCP-Server verletzen das Prinzip der minimalen Rechte und erweitern die Angriffsfläche

#### Token-Passthrough: Ein kritisches Anti-Pattern

**Token-Passthrough ist in der aktuellen MCP-Autorisierungs-Spezifikation ausdrücklich verboten** aufgrund schwerwiegender Sicherheitsimplikationen:

##### Umgehung von Sicherheitskontrollen
- MCP-Server und nachgelagerte APIs implementieren kritische Sicherheitskontrollen (Rate-Limiting, Anforderungsvalidierung, Verkehrsüberwachung), die von ordnungsgemäßer Token-Validierung abhängen
- Direkte Nutzung von Client-zu-API-Token umgeht diese wesentlichen Schutzmaßnahmen und untergräbt die Sicherheitsarchitektur

##### Herausforderungen bei Verantwortlichkeit & Audit  
- MCP-Server können nicht zwischen Clients unterscheiden, die von Upstream ausgestellte Tokens verwenden, wodurch Audit-Trails unterbrochen werden
- Protokolle nachgelagerter Ressourcenserver zeigen irreführende Ursprünge von Anfragen anstelle tatsächlicher MCP-Server-Zwischenstellen
- Vorfalluntersuchungen und Compliance-Audits werden erheblich erschwert

##### Risiken der Datenexfiltration
- Nicht validierte Token-Claims ermöglichen böswilligen Akteuren mit gestohlenen Tokens, MCP-Server als Proxy für Datenexfiltration zu nutzen
- Verletzungen der Vertrauensgrenzen erlauben unbefugte Zugriffsmuster, die beabsichtigte Sicherheitskontrollen umgehen

##### Angriffsvektoren über mehrere Dienste
- Kompromittierte Tokens, die von mehreren Diensten akzeptiert werden, ermöglichen laterale Bewegungen über verbundene Systeme hinweg
- Vertrauensannahmen zwischen Diensten können verletzt werden, wenn Token-Ursprünge nicht überprüft werden können

### Sicherheitskontrollen & Maßnahmen

**Kritische Sicherheitsanforderungen:**

> **VERPFLICHTEND**: MCP-Server **DÜRFEN KEINE** Tokens akzeptieren, die nicht ausdrücklich für den MCP-Server ausgestellt wurden

#### Authentifizierungs- & Autorisierungs-Kontrollen

- **Strenge Autorisierungsprüfung**: Führen Sie umfassende Audits der Autorisierungslogik von MCP-Servern durch, um sicherzustellen, dass nur beabsichtigte Benutzer und Clients auf sensible Ressourcen zugreifen können
  - **Implementierungsleitfaden**: [Azure API Management als Authentifizierungs-Gateway für MCP-Server](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Identitätsintegration**: [Microsoft Entra ID für MCP-Server-Authentifizierung verwenden](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Sicheres Token-Management**: Implementieren Sie [Microsofts Best Practices für Token-Validierung und Lebenszyklus](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Validieren Sie, dass Token-Audience-Claims mit der Identität des MCP-Servers übereinstimmen
  - Implementieren Sie ordnungsgemäße Token-Rotation und Ablaufrichtlinien
  - Verhindern Sie Token-Replay-Angriffe und unbefugte Nutzung

- **Geschützte Token-Speicherung**: Sichere Token-Speicherung mit Verschlüsselung sowohl im Ruhezustand als auch während der Übertragung
  - **Best Practices**: [Richtlinien zur sicheren Token-Speicherung und Verschlüsselung](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementierung von Zugriffskontrollen

- **Prinzip der minimalen Rechte**: Gewähren Sie MCP-Servern nur die minimalen Berechtigungen, die für die beabsichtigte Funktionalität erforderlich sind
  - Regelmäßige Überprüfung und Aktualisierung von Berechtigungen, um Rechteausweitung zu verhindern
  - **Microsoft-Dokumentation**: [Sicherer Zugriff mit minimalen Rechten](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Rollenbasierte Zugriffskontrolle (RBAC)**: Implementieren Sie fein abgestimmte Rollenzuweisungen
  - Begrenzen Sie Rollen strikt auf spezifische Ressourcen und Aktionen
  - Vermeiden Sie breite oder unnötige Berechtigungen, die die Angriffsfläche erweitern

- **Kontinuierliche Berechtigungsüberwachung**: Implementieren Sie fortlaufende Audits und Überwachung des Zugriffs
  - Überwachen Sie Nutzungsmuster von Berechtigungen auf Anomalien
  - Beheben Sie übermäßige oder ungenutzte Berechtigungen umgehend

## KI-spezifische Sicherheitsbedrohungen

### Prompt Injection & Tool Manipulation Angriffe

Moderne MCP-Implementierungen sind ausgeklügelten KI-spezifischen Angriffsvektoren ausgesetzt, die traditionelle Sicherheitsmaßnahmen nicht vollständig adressieren können:

#### **Indirekte Prompt Injection (Cross-Domain Prompt Injection)**

**Indirekte Prompt Injection** stellt eine der kritischsten Schwachstellen in MCP-fähigen KI-Systemen dar. Angreifer betten böswillige Anweisungen in externe Inhalte ein – Dokumente, Webseiten, E-Mails oder Datenquellen –, die von KI-Systemen anschließend als legitime Befehle verarbeitet werden.

**Angriffsszenarien:**
- **Dokumentenbasierte Injection**: Böswillige Anweisungen, die in verarbeiteten Dokumenten versteckt sind und unbeabsichtigte KI-Aktionen auslösen
- **Webinhaltsausnutzung**: Kompromittierte Webseiten mit eingebetteten Prompts, die das KI-Verhalten bei Scraping manipulieren
- **E-Mail-basierte Angriffe**: Böswillige Prompts in E-Mails, die KI-Assistenten dazu bringen, Informationen preiszugeben oder unbefugte Aktionen auszuführen
- **Datenquellen-Kontamination**: Kompromittierte Datenbanken oder APIs, die manipulierte Inhalte an KI-Systeme liefern

**Reale Auswirkungen**: Diese Angriffe können zu Datenexfiltration, Datenschutzverletzungen, der Erstellung schädlicher Inhalte und der Manipulation von Benutzerinteraktionen führen. Für eine detaillierte Analyse siehe [Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Prompt Injection Angriff Diagramm](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.de.png)

#### **Tool Poisoning Angriffe**

**Tool Poisoning** zielt auf die Metadaten ab, die MCP-Tools definieren, und nutzt aus, wie LLMs Tool-Beschreibungen und Parameter interpretieren, um Ausführungsentscheidungen zu treffen.

**Angriffsmechanismen:**
- **Manipulation von Metadaten**: Angreifer injizieren böswillige Anweisungen in Tool-Beschreibungen, Parameterdefinitionen oder Nutzungshinweise
- **Unsichtbare Anweisungen**: Versteckte Prompts in Tool-Metadaten, die von KI-Modellen verarbeitet werden, aber für menschliche Benutzer unsichtbar sind
- **Dynamische Tool-Modifikation ("Rug Pulls")**: Tools, die von Benutzern genehmigt wurden, werden später modifiziert, um böswillige Aktionen auszuführen, ohne dass Benutzer dies bemerken
- **Parameter-Injection**: Böswillige Inhalte, die in Tool-Parameter-Schemata eingebettet sind und das Modellverhalten beeinflussen

**Risiken bei gehosteten Servern**: Remote-MCP-Server stellen erhöhte Risiken dar, da Tool-Definitionen nach der anfänglichen Benutzerfreigabe aktualisiert werden können, wodurch Szenarien entstehen, in denen zuvor sichere Tools böswillig werden. Für eine umfassende Analyse siehe [Tool Poisoning Angriffe (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Tool Injection Angriff Diagramm](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.de.png)

#### **Weitere KI-Angriffsvektoren**

- **Cross-Domain Prompt Injection (XPIA)**: Ausgeklügelte Angriffe, die Inhalte aus mehreren Domänen nutzen, um Sicherheitskontrollen zu umgehen
- **Dynamische Fähigkeitsmodifikation**: Echtzeitänderungen an Tool-Fähigkeiten, die initiale Sicherheitsbewertungen umgehen
- **Context Window Poisoning**: Angriffe, die große Kontextfenster manipulieren, um böswillige Anweisungen zu verstecken
- **Model Confusion Angriffe**: Ausnutzen von Modellbeschränkungen, um unvorhersehbare oder unsichere Verhaltensweisen zu erzeugen

### Auswirkungen von KI-Sicherheitsrisiken

**Hochgradige Konsequenzen:**
- **Datenexfiltration**: Unbefugter Zugriff und Diebstahl sensibler Unternehmens- oder persönlicher Daten
- **Datenschutzverletzungen**: Offenlegung personenbezogener Informationen (PII) und vertraulicher Geschäftsdaten  
- **Systemmanipulation**: Unbeabsichtigte Änderungen an kritischen Systemen und Arbeitsabläufen
- **Diebstahl von Zugangsdaten**: Kompromittierung von Authentifizierungs-Tokens und Dienstanmeldeinformationen
- **Laterale Bewegung**: Nutzung kompromittierter KI-Systeme als Dreh- und Angelpunkt für breitere Netzwerkangriffe

### Microsoft KI-Sicherheitslösungen

#### **AI Prompt Shields: Erweiterter Schutz vor Injection-Angriffen**

Microsoft **AI Prompt Shields** bieten umfassenden Schutz vor sowohl direkten als auch indirekten Prompt Injection-Angriffen durch mehrere Sicherheitsschichten:

##### **Kernschutzmechanismen:**

1. **Erweiterte Erkennung & Filterung**
   - Maschinelle Lernalgorithmen und NLP-Techniken erkennen böswillige Anweisungen in externen Inhalten
   - Echtzeitanalyse von Dokumenten, Webseiten, E-Mails und Datenquellen auf eingebettete Bedrohungen
   - Kontextuelles Verständnis von legitimen vs. böswilligen Prompt-Mustern

2. **Spotlighting-Techniken**  
   - Unterscheidet zwischen vertrauenswürdigen Systemanweisungen und potenziell kompromittierten externen Eingaben
   - Texttransformationstechniken, die die Modellrelevanz verbessern und gleichzeitig böswillige Inhalte isolieren
   - Hilft KI-Systemen, die richtige Anweisungshierarchie beizubehalten und injizierte Befehle zu ignorieren

3. **Delimiter- & Datamarking-Systeme**
   - Explizite Grenzdefinition zwischen vertrauenswürdigen Systemnachrichten und externem Eingabetext
   - Spezielle Markierungen heben Grenzen zwischen vertrauenswürdigen und nicht vertrauenswürdigen Datenquellen hervor
   - Klare Trennung verhindert Anweisungsverwirrung und unbefugte Befehlsausführung

4. **Kontinuierliche Bedrohungsintelligenz**
   - Microsoft überwacht kontinuierlich aufkommende Angriffsmuster und aktualisiert Abwehrmaßnahmen
   - Proaktive Bedrohungssuche nach neuen Injection-Techniken und Angriffsvektoren
   - Regelmäßige Sicherheitsmodell-Updates, um die Wirksamkeit gegen sich entwickelnde Bedrohungen aufrechtzuerhalten

5. **Integration von Azure Content Safety**
   - Teil der umfassenden Azure AI Content Safety Suite
   - Zusätzliche Erkennung von Jailbreak-Versuchen, schädlichen Inhalten und Sicherheitsrichtlinienverletzungen
   - Einheitliche Sicherheitskontrollen über KI-Anwendungskomponenten hinweg

**Implementierungsressourcen**: [Microsoft Prompt Shields Dokumentation](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)

![Microsoft Prompt Shields Schutz](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.de.png)

## Erweiterte MCP-Sicherheitsbedrohungen

### Schwachstellen bei Sitzungs-Hijacking

**Sitzungs-Hijacking** stellt einen kritischen Angriffsvektor in zustandsbehafteten MCP-Implementierungen dar, bei denen unbefugte Parteien legitime Sitzungskennungen erhalten und missbrauchen, um Clients zu imitieren und unbefugte Aktionen auszuführen.

#### **Angriffsszenarien & Risiken**

- **Prompt Injection durch Sitzungs-Hijacking**: Angreifer mit gestohlenen Sitzungs-IDs injizieren böswillige Ereignisse in Server, die Sitzungszustände teilen, und können dadurch schädliche Aktionen auslösen oder auf sensible Daten zugreifen
- **Direkte Imitation**: Gestohlene Sitzungs-IDs ermöglichen direkte MCP-Server-Aufrufe, die die Authentifizierung umgehen und Angreifer als legitime Benutzer behandeln
- **Kompromittierte wiederaufnehmb
- **Sichere Sitzungs-Generierung**: Verwenden Sie kryptografisch sichere, nicht-deterministische Sitzungs-IDs, die mit sicheren Zufallszahlengeneratoren erstellt werden.  
- **Benutzergebundene Verknüpfung**: Verknüpfen Sie Sitzungs-IDs mit benutzerspezifischen Informationen, z. B. im Format `<user_id>:<session_id>`, um Missbrauch zwischen Benutzersitzungen zu verhindern.  
- **Sitzungslebenszyklus-Management**: Implementieren Sie eine ordnungsgemäße Ablaufsteuerung, Rotation und Ungültigmachung, um Schwachstellenfenster zu minimieren.  
- **Transportsicherheit**: HTTPS ist für alle Kommunikationen obligatorisch, um die Abfangung von Sitzungs-IDs zu verhindern.  

### Problem des verwirrten Stellvertreters  

Das **Problem des verwirrten Stellvertreters** tritt auf, wenn MCP-Server als Authentifizierungsproxies zwischen Clients und Drittanbieterdiensten agieren, wodurch Möglichkeiten für Autorisierungsumgehungen durch die Ausnutzung statischer Client-IDs entstehen.  

#### **Angriffsmechanismen & Risiken**  

- **Umgehung der Cookie-basierten Zustimmung**: Frühere Benutzer-Authentifizierungen erzeugen Zustimmungs-Cookies, die Angreifer durch manipulierte Autorisierungsanfragen mit speziell gestalteten Redirect-URIs ausnutzen.  
- **Diebstahl von Autorisierungscodes**: Bestehende Zustimmungs-Cookies können dazu führen, dass Autorisierungsserver Zustimmungsbildschirme überspringen und Codes an von Angreifern kontrollierte Endpunkte weiterleiten.  
- **Unbefugter API-Zugriff**: Gestohlene Autorisierungscodes ermöglichen den Token-Austausch und die Benutzer-Imitation ohne ausdrückliche Zustimmung.  

#### **Minderungsstrategien**  

**Obligatorische Maßnahmen:**  
- **Explizite Zustimmungsanforderungen**: MCP-Proxy-Server, die statische Client-IDs verwenden, **MÜSSEN** die Zustimmung des Benutzers für jeden dynamisch registrierten Client einholen.  
- **OAuth 2.1 Sicherheitsimplementierung**: Befolgen Sie aktuelle OAuth-Sicherheitsbest-Practices, einschließlich PKCE (Proof Key for Code Exchange) für alle Autorisierungsanfragen.  
- **Strikte Client-Validierung**: Implementieren Sie eine rigorose Validierung von Redirect-URIs und Client-Identifikatoren, um Ausnutzung zu verhindern.  

### Schwachstellen bei Token-Passthrough  

**Token-Passthrough** stellt ein explizites Anti-Muster dar, bei dem MCP-Server Client-Tokens ohne ordnungsgemäße Validierung akzeptieren und an nachgelagerte APIs weiterleiten, wodurch MCP-Autorisierungsspezifikationen verletzt werden.  

#### **Sicherheitsimplikationen**  

- **Umgehung von Kontrollmechanismen**: Die direkte Nutzung von Client-zu-API-Tokens umgeht wichtige Ratenbegrenzungen, Validierungen und Überwachungsmechanismen.  
- **Manipulation der Audit-Trails**: Von Upstream ausgestellte Tokens machen die Identifikation von Clients unmöglich und behindern die Untersuchung von Vorfällen.  
- **Proxy-basierte Datenexfiltration**: Nicht validierte Tokens ermöglichen es böswilligen Akteuren, Server als Proxies für unbefugten Datenzugriff zu nutzen.  
- **Verletzung von Vertrauensgrenzen**: Die Vertrauensannahmen nachgelagerter Dienste können verletzt werden, wenn die Herkunft von Tokens nicht überprüft werden kann.  
- **Erweiterung von Angriffen auf mehrere Dienste**: Kompromittierte Tokens, die über mehrere Dienste akzeptiert werden, ermöglichen laterale Bewegungen.  

#### **Erforderliche Sicherheitskontrollen**  

**Nicht verhandelbare Anforderungen:**  
- **Token-Validierung**: MCP-Server **DÜRFEN KEINE** Tokens akzeptieren, die nicht explizit für den MCP-Server ausgestellt wurden.  
- **Überprüfung der Zielgruppe**: Validieren Sie stets, dass die Zielgruppenansprüche von Tokens mit der Identität des MCP-Servers übereinstimmen.  
- **Ordnungsgemäßer Token-Lebenszyklus**: Implementieren Sie kurzlebige Zugriffstokens mit sicheren Rotationspraktiken.  

## Sicherheit der Lieferkette für KI-Systeme  

Die Sicherheit der Lieferkette hat sich über traditionelle Softwareabhängigkeiten hinaus entwickelt und umfasst das gesamte KI-Ökosystem. Moderne MCP-Implementierungen müssen alle KI-bezogenen Komponenten rigoros überprüfen und überwachen, da jede potenzielle Schwachstellen einführen kann, die die Systemintegrität gefährden.  

### Erweiterte Komponenten der KI-Lieferkette  

**Traditionelle Softwareabhängigkeiten:**  
- Open-Source-Bibliotheken und Frameworks  
- Container-Images und Basissysteme  
- Entwicklungstools und Build-Pipelines  
- Infrastrukturkomponenten und -dienste  

**KI-spezifische Lieferkettenelemente:**  
- **Grundlagenmodelle**: Vorgefertigte Modelle von verschiedenen Anbietern, die eine Herkunftsüberprüfung erfordern  
- **Einbettungsdienste**: Externe Vektorisierungs- und semantische Suchdienste  
- **Kontextanbieter**: Datenquellen, Wissensbasen und Dokumenten-Repositories  
- **Drittanbieter-APIs**: Externe KI-Dienste, ML-Pipelines und Datenverarbeitungsendpunkte  
- **Modellartefakte**: Gewichte, Konfigurationen und feinabgestimmte Modellvarianten  
- **Trainingsdatenquellen**: Datensätze, die für das Training und die Feinabstimmung von Modellen verwendet werden  

### Umfassende Sicherheitsstrategie für die Lieferkette  

#### **Komponentenüberprüfung & Vertrauen**  
- **Herkunftsvalidierung**: Überprüfen Sie die Herkunft, Lizenzierung und Integrität aller KI-Komponenten vor der Integration.  
- **Sicherheitsbewertung**: Führen Sie Schwachstellenscans und Sicherheitsüberprüfungen für Modelle, Datenquellen und KI-Dienste durch.  
- **Reputationsanalyse**: Bewerten Sie die Sicherheitsbilanz und Praktiken von KI-Dienstanbietern.  
- **Compliance-Überprüfung**: Stellen Sie sicher, dass alle Komponenten den Sicherheits- und regulatorischen Anforderungen der Organisation entsprechen.  

#### **Sichere Bereitstellungspipelines**  
- **Automatisierte CI/CD-Sicherheit**: Integrieren Sie Sicherheitsüberprüfungen in automatisierte Bereitstellungspipelines.  
- **Artefaktintegrität**: Implementieren Sie kryptografische Überprüfungen für alle bereitgestellten Artefakte (Code, Modelle, Konfigurationen).  
- **Stufenweise Bereitstellung**: Verwenden Sie progressive Bereitstellungsstrategien mit Sicherheitsvalidierung in jeder Phase.  
- **Vertrauenswürdige Artefakt-Repositories**: Stellen Sie nur aus überprüften, sicheren Artefakt-Registries und -Repositories bereit.  

#### **Kontinuierliche Überwachung & Reaktion**  
- **Abhängigkeitsscans**: Laufende Schwachstellenüberwachung für alle Software- und KI-Komponentenabhängigkeiten.  
- **Modellüberwachung**: Kontinuierliche Bewertung des Modellverhaltens, von Leistungsabweichungen und Sicherheitsanomalien.  
- **Überwachung der Dienstgesundheit**: Überwachen Sie externe KI-Dienste auf Verfügbarkeit, Sicherheitsvorfälle und Richtlinienänderungen.  
- **Bedrohungsintelligenz-Integration**: Integrieren Sie Bedrohungsfeeds, die speziell auf KI- und ML-Sicherheitsrisiken ausgerichtet sind.  

#### **Zugriffskontrolle & Minimalprinzip**  
- **Komponentenbasierte Berechtigungen**: Beschränken Sie den Zugriff auf Modelle, Daten und Dienste auf geschäftliche Notwendigkeiten.  
- **Verwaltung von Dienstkonten**: Implementieren Sie dedizierte Dienstkonten mit minimal erforderlichen Berechtigungen.  
- **Netzwerksegmentierung**: Isolieren Sie KI-Komponenten und beschränken Sie den Netzwerkzugriff zwischen Diensten.  
- **API-Gateway-Kontrollen**: Verwenden Sie zentrale API-Gateways, um den Zugriff auf externe KI-Dienste zu steuern und zu überwachen.  

#### **Vorfallreaktion & Wiederherstellung**  
- **Schnelle Reaktionsverfahren**: Etablierte Prozesse zum Patchen oder Ersetzen kompromittierter KI-Komponenten.  
- **Anmeldeinformationen-Rotation**: Automatisierte Systeme zur Rotation von Geheimnissen, API-Schlüsseln und Dienstanmeldeinformationen.  
- **Rollback-Fähigkeiten**: Möglichkeit, schnell auf vorherige, bekannte gute Versionen von KI-Komponenten zurückzukehren.  
- **Wiederherstellung nach Lieferkettenverletzungen**: Spezifische Verfahren zur Reaktion auf Kompromittierungen von Upstream-KI-Diensten.  

### Microsoft-Sicherheitswerkzeuge & Integration  

**GitHub Advanced Security** bietet umfassenden Schutz der Lieferkette, einschließlich:  
- **Geheimnisscans**: Automatische Erkennung von Anmeldeinformationen, API-Schlüsseln und Tokens in Repositories.  
- **Abhängigkeitsscans**: Schwachstellenbewertung für Open-Source-Abhängigkeiten und -Bibliotheken.  
- **CodeQL-Analyse**: Statische Codeanalyse zur Erkennung von Sicherheitslücken und Codierungsproblemen.  
- **Einblicke in die Lieferkette**: Sichtbarkeit des Zustands und der Sicherheit von Abhängigkeiten.  

**Azure DevOps & Azure Repos Integration:**  
- Nahtlose Integration von Sicherheitsüberprüfungen in Microsoft-Entwicklungsplattformen.  
- Automatisierte Sicherheitsprüfungen in Azure Pipelines für KI-Arbeitslasten.  
- Richtlinienerzwingung für die sichere Bereitstellung von KI-Komponenten.  

**Microsoft Interne Praktiken:**  
Microsoft implementiert umfassende Sicherheitspraktiken für die Lieferkette in allen Produkten. Erfahren Sie mehr über bewährte Ansätze in [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Microsoft-Sicherheitslösungen**
- [Microsoft Prompt Shields Dokumentation](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety Service](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID-Sicherheit](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Best Practices für Azure Token Management](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Implementierungsleitfäden & Tutorials**
- [Azure API Management als MCP-Authentifizierungs-Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID-Authentifizierung mit MCP-Servern](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Sichere Token-Speicherung und Verschlüsselung (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps & Sicherheit in der Lieferkette**
- [Azure DevOps-Sicherheit](https://azure.microsoft.com/products/devops)
- [Azure Repos-Sicherheit](https://azure.microsoft.com/products/devops/repos/)
- [Microsofts Reise zur Sicherung der Lieferkette](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Zusätzliche Sicherheitsdokumentation**

Für umfassende Sicherheitsrichtlinien beziehen Sie sich auf die folgenden spezialisierten Dokumente in diesem Abschnitt:

- **[MCP Sicherheits-Best Practices 2025](./mcp-security-best-practices-2025.md)** - Vollständige Sicherheits-Best Practices für MCP-Implementierungen  
- **[Azure Content Safety Implementierung](./azure-content-safety-implementation.md)** - Praktische Implementierungsbeispiele für die Integration von Azure Content Safety  
- **[MCP Sicherheitskontrollen 2025](./mcp-security-controls-2025.md)** - Neueste Sicherheitskontrollen und -techniken für MCP-Bereitstellungen  
- **[MCP Best Practices Schnellreferenz](./mcp-best-practices.md)** - Schnellreferenz für wesentliche MCP-Sicherheitspraktiken  

---

## Was kommt als Nächstes

Weiter: [Kapitel 3: Erste Schritte](../03-GettingStarted/README.md)

**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, weisen wir darauf hin, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner ursprünglichen Sprache sollte als maßgebliche Quelle betrachtet werden. Für kritische Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die sich aus der Nutzung dieser Übersetzung ergeben.