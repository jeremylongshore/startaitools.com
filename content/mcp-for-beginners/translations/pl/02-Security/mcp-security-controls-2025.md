<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T12:21:19+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "pl"
}
-->
# MCP Kontrole Bezpieczeństwa - Aktualizacja sierpień 2025

> **Obowiązujący Standard**: Ten dokument odzwierciedla wymagania bezpieczeństwa [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) oraz oficjalne [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Model Context Protocol (MCP) znacząco się rozwinął, wprowadzając ulepszone kontrole bezpieczeństwa, które uwzględniają zarówno tradycyjne zagrożenia związane z oprogramowaniem, jak i specyficzne dla AI. Ten dokument przedstawia kompleksowe kontrole bezpieczeństwa dla bezpiecznych implementacji MCP na sierpień 2025.

## **OBOWIĄZKOWE Wymagania Bezpieczeństwa**

### **Kluczowe Zakazy z MCP Specification:**

> **ZABRONIONE**: Serwery MCP **NIE MOGĄ** akceptować żadnych tokenów, które nie zostały wyraźnie wydane dla serwera MCP  
>
> **ZAKAZANE**: Serwery MCP **NIE MOGĄ** używać sesji do uwierzytelniania  
>
> **WYMAGANE**: Serwery MCP implementujące autoryzację **MUSZĄ** weryfikować WSZYSTKIE przychodzące żądania  
>
> **OBOWIĄZKOWE**: Serwery proxy MCP używające statycznych identyfikatorów klientów **MUSZĄ** uzyskać zgodę użytkownika dla każdego dynamicznie zarejestrowanego klienta  

---

## 1. **Kontrole Uwierzytelniania i Autoryzacji**

### **Integracja z Zewnętrznymi Dostawcami Tożsamości**

**Obowiązujący standard MCP (2025-06-18)** pozwala serwerom MCP delegować uwierzytelnianie zewnętrznym dostawcom tożsamości, co stanowi istotne ulepszenie bezpieczeństwa:

**Korzyści Bezpieczeństwa:**
1. **Eliminacja Ryzyk Własnych Rozwiązań**: Zmniejszenie powierzchni podatności poprzez unikanie własnych implementacji uwierzytelniania  
2. **Bezpieczeństwo na Poziomie Korporacyjnym**: Wykorzystanie zaawansowanych funkcji bezpieczeństwa dostawców takich jak Microsoft Entra ID  
3. **Centralne Zarządzanie Tożsamością**: Ułatwienie zarządzania cyklem życia użytkownika, kontrolą dostępu i audytami zgodności  
4. **Uwierzytelnianie Wieloskładnikowe**: Dziedziczenie funkcji MFA od dostawców tożsamości korporacyjnych  
5. **Polityki Dostępu Warunkowego**: Korzystanie z adaptacyjnych mechanizmów kontroli dostępu opartych na ryzyku  

**Wymagania Implementacyjne:**
- **Walidacja Odbiorcy Tokenu**: Weryfikacja, że wszystkie tokeny zostały wyraźnie wydane dla serwera MCP  
- **Weryfikacja Wydawcy**: Sprawdzenie, czy wydawca tokenu odpowiada oczekiwanemu dostawcy tożsamości  
- **Weryfikacja Podpisu**: Kryptograficzna weryfikacja integralności tokenu  
- **Egzekwowanie Wygaśnięcia**: Ścisłe przestrzeganie limitów czasu życia tokenu  
- **Walidacja Zakresu**: Upewnienie się, że tokeny zawierają odpowiednie uprawnienia dla żądanych operacji  

### **Bezpieczeństwo Logiki Autoryzacji**

**Kluczowe Kontrole:**
- **Kompleksowe Audyty Autoryzacji**: Regularne przeglądy bezpieczeństwa wszystkich punktów decyzyjnych autoryzacji  
- **Domyślne Bezpieczne Ustawienia**: Odmowa dostępu, gdy logika autoryzacji nie może podjąć jednoznacznej decyzji  
- **Granice Uprawnień**: Wyraźne rozdzielenie różnych poziomów uprawnień i dostępu do zasobów  
- **Rejestrowanie Audytów**: Pełne logowanie wszystkich decyzji autoryzacyjnych dla monitorowania bezpieczeństwa  
- **Regularne Przeglądy Dostępu**: Okresowa weryfikacja uprawnień użytkowników i przypisanych przywilejów  

## 2. **Bezpieczeństwo Tokenów i Kontrole Przeciwko Przekazywaniu**

### **Zapobieganie Przekazywaniu Tokenów**

**Przekazywanie tokenów jest wyraźnie zabronione** w MCP Authorization Specification ze względu na krytyczne zagrożenia bezpieczeństwa:

**Zagrożenia Bezpieczeństwa:**
- **Omijanie Kontroli**: Pomijanie kluczowych mechanizmów bezpieczeństwa, takich jak ograniczanie szybkości, walidacja żądań i monitorowanie ruchu  
- **Rozpad Odpowiedzialności**: Uniemożliwienie identyfikacji klienta, co psuje ścieżki audytu i dochodzenia incydentów  
- **Eksfiltracja przez Proxy**: Umożliwienie złośliwym aktorom wykorzystania serwerów jako proxy do nieautoryzowanego dostępu do danych  
- **Naruszenie Granic Zaufania**: Złamanie założeń usług downstream dotyczących pochodzenia tokenów  
- **Ruch Lateralny**: Kompromitacja tokenów w wielu usługach umożliwia rozszerzenie ataku  

**Kontrole Implementacyjne:**
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

### **Bezpieczne Wzorce Zarządzania Tokenami**

**Najlepsze Praktyki:**
- **Tokeny Krótkoterminowe**: Minimalizacja okna ekspozycji poprzez częstą rotację tokenów  
- **Wydawanie na Żądanie**: Wydawanie tokenów tylko wtedy, gdy są potrzebne do konkretnych operacji  
- **Bezpieczne Przechowywanie**: Wykorzystanie modułów bezpieczeństwa sprzętowego (HSM) lub bezpiecznych skarbców kluczy  
- **Powiązanie Tokenów**: Powiązanie tokenów z konkretnymi klientami, sesjami lub operacjami, jeśli to możliwe  
- **Monitorowanie i Alarmowanie**: Wykrywanie w czasie rzeczywistym nadużyć tokenów lub nieautoryzowanych wzorców dostępu  

## 3. **Kontrole Bezpieczeństwa Sesji**

### **Zapobieganie Przejęciu Sesji**

**Adresowane Wektory Ataku:**
- **Wstrzykiwanie Zdarzeń do Sesji**: Złośliwe zdarzenia wprowadzane do współdzielonego stanu sesji  
- **Podszywanie się pod Sesję**: Nieautoryzowane użycie skradzionych identyfikatorów sesji w celu obejścia uwierzytelniania  
- **Ataki na Wznowienie Strumienia**: Wykorzystanie wznowienia zdarzeń wysyłanych przez serwer do wstrzykiwania złośliwych treści  

**Obowiązkowe Kontrole Sesji:**
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

**Bezpieczeństwo Transportu:**
- **Wymuszenie HTTPS**: Cała komunikacja sesji przez TLS 1.3  
- **Atrybuty Bezpiecznych Ciasteczek**: HttpOnly, Secure, SameSite=Strict  
- **Pinning Certyfikatów**: Dla kluczowych połączeń w celu zapobiegania atakom MITM  

### **Rozważania Stateful vs Stateless**

**Dla Implementacji Stateful:**
- Współdzielony stan sesji wymaga dodatkowej ochrony przed atakami wstrzykiwania  
- Zarządzanie sesjami oparte na kolejkach wymaga weryfikacji integralności  
- Wiele instancji serwerów wymaga bezpiecznej synchronizacji stanu sesji  

**Dla Implementacji Stateless:**
- Zarządzanie sesjami oparte na tokenach JWT lub podobnych  
- Kryptograficzna weryfikacja integralności stanu sesji  
- Zmniejszona powierzchnia ataku, ale wymaga solidnej walidacji tokenów  

## 4. **Specyficzne dla AI Kontrole Bezpieczeństwa**

### **Obrona przed Wstrzykiwaniem Poleceń**

**Integracja Microsoft Prompt Shields:**
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

**Kontrole Implementacyjne:**
- **Sanityzacja Wejścia**: Kompleksowa walidacja i filtrowanie wszystkich danych wejściowych użytkownika  
- **Definicja Granic Treści**: Wyraźne rozdzielenie instrukcji systemowych od treści użytkownika  
- **Hierarchia Instrukcji**: Odpowiednie zasady precedencji dla sprzecznych instrukcji  
- **Monitorowanie Wyjścia**: Wykrywanie potencjalnie szkodliwych lub zmanipulowanych wyników  

### **Zapobieganie Zatruciu Narzędzi**

**Ramowe Bezpieczeństwo Narzędzi:**
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

**Dynamiczne Zarządzanie Narzędziami:**
- **Procesy Zatwierdzania**: Wyraźna zgoda użytkownika na modyfikacje narzędzi  
- **Możliwości Wycofania**: Możliwość powrotu do poprzednich wersji narzędzi  
- **Audyt Zmian**: Pełna historia modyfikacji definicji narzędzi  
- **Ocena Ryzyka**: Automatyczna ocena bezpieczeństwa narzędzi  

## 5. **Zapobieganie Atakom na Zdezorientowanego Zastępcę**

### **Bezpieczeństwo Proxy OAuth**

**Kontrole Zapobiegania Atakom:**
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

**Wymagania Implementacyjne:**
- **Weryfikacja Zgody Użytkownika**: Nigdy nie pomijaj ekranów zgody dla dynamicznej rejestracji klientów  
- **Walidacja URI Przekierowania**: Ścisła walidacja na podstawie białej listy docelowych adresów przekierowania  
- **Ochrona Kodów Autoryzacyjnych**: Krótkoterminowe kody z egzekwowaniem jednorazowego użycia  
- **Weryfikacja Tożsamości Klienta**: Solidna walidacja poświadczeń i metadanych klienta  

## 6. **Bezpieczeństwo Wykonywania Narzędzi**

### **Izolacja i Sandboxing**

**Izolacja oparta na kontenerach:**
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

**Izolacja Procesów:**
- **Oddzielne Konteksty Procesów**: Każde wykonanie narzędzia w izolowanej przestrzeni procesowej  
- **Komunikacja Międzyprocesowa**: Bezpieczne mechanizmy IPC z walidacją  
- **Monitorowanie Procesów**: Analiza zachowania w czasie rzeczywistym i wykrywanie anomalii  
- **Egzekwowanie Zasobów**: Twarde limity na CPU, pamięć i operacje I/O  

### **Implementacja Zasady Najmniejszych Uprawnień**

**Zarządzanie Uprawnieniami:**
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

## 7. **Kontrole Bezpieczeństwa Łańcucha Dostaw**

### **Weryfikacja Zależności**

**Kompleksowe Bezpieczeństwo Komponentów:**
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

### **Ciągłe Monitorowanie**

**Wykrywanie Zagrożeń Łańcucha Dostaw:**
- **Monitorowanie Zdrowia Zależności**: Ciągła ocena wszystkich zależności pod kątem problemów bezpieczeństwa  
- **Integracja Wywiadu Zagrożeń**: Aktualizacje w czasie rzeczywistym dotyczące pojawiających się zagrożeń w łańcuchu dostaw  
- **Analiza Behawioralna**: Wykrywanie nietypowego zachowania w komponentach zewnętrznych  
- **Automatyczna Reakcja**: Natychmiastowe ograniczenie skompromitowanych komponentów  

## 8. **Kontrole Monitorowania i Wykrywania**

### **Zarządzanie Informacjami i Zdarzeniami Bezpieczeństwa (SIEM)**

**Kompleksowa Strategia Logowania:**
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

### **Wykrywanie Zagrożeń w Czasie Rzeczywistym**

**Analiza Behawioralna:**
- **Analiza Zachowań Użytkowników (UBA)**: Wykrywanie nietypowych wzorców dostępu użytkowników  
- **Analiza Zachowań Jednostek (EBA)**: Monitorowanie zachowań serwera MCP i narzędzi  
- **Wykrywanie Anomalii za pomocą AI**: Identyfikacja zagrożeń bezpieczeństwa za pomocą sztucznej inteligencji  
- **Korelacja Wywiadu Zagrożeń**: Dopasowanie zaobserwowanych działań do znanych wzorców ataków  

## 9. **Reakcja na Incydenty i Odzyskiwanie**

### **Automatyczne Możliwości Reakcji**

**Natychmiastowe Działania:**
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

### **Możliwości Kryminalistyczne**

**Wsparcie Dochodzeniowe:**
- **Zachowanie Ścieżek Audytu**: Niezmienialne logowanie z kryptograficzną integralnością  
- **Zbieranie Dowodów**: Automatyczne gromadzenie odpowiednich artefaktów bezpieczeństwa  
- **Rekonstrukcja Linii Czasu**: Szczegółowa sekwencja zdarzeń prowadzących do incydentów bezpieczeństwa  
- **Ocena Wpływu**: Ocena zakresu kompromitacji i ekspozycji danych  

## **Kluczowe Zasady Architektury Bezpieczeństwa**

### **Obrona w Głębi**
- **Wielowarstwowe Mechanizmy Bezpieczeństwa**: Brak pojedynczego punktu awarii w architekturze bezpieczeństwa  
- **Redundantne Kontrole**: Nakładające się środki bezpieczeństwa dla kluczowych funkcji  
- **Mechanizmy Bezpieczne w Awarii**: Bezpieczne ustawienia domyślne w przypadku błędów systemowych lub ataków  

### **Implementacja Zero Trust**
- **Nigdy Nie Ufaj, Zawsze Weryfikuj**: Ciągła walidacja wszystkich jednostek i żądań  
- **Zasada Najmniejszych Uprawnień**: Minimalne prawa dostępu dla wszystkich komponentów  
- **Mikrosegmentacja**: Granularne kontrole sieci i dostępu  

### **Ciągła Ewolucja Bezpieczeństwa**
- **Adaptacja do Krajobrazu Zagrożeń**: Regularne aktualizacje w celu przeciwdziałania nowym zagrożeniom  
- **Skuteczność Kontroli Bezpieczeństwa**: Ciągła ocena i ulepszanie mechanizmów bezpieczeństwa  
- **Zgodność ze Specyfikacją**: Dopasowanie do ewoluujących standardów bezpieczeństwa MCP  

---

## **Zasoby Implementacyjne**

### **Oficjalna Dokumentacja MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Rozwiązania Bezpieczeństwa Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Standardy Bezpieczeństwa**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **Ważne**: Te kontrole bezpieczeństwa odzwierciedlają obowiązującą specyfikację MCP (2025-06-18). Zawsze weryfikuj zgodność z najnowszą [oficjalną dokumentacją](https://spec.modelcontextprotocol.io/), ponieważ standardy szybko się rozwijają.  

**Zastrzeżenie**:  
Ten dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dokładamy wszelkich starań, aby zapewnić poprawność tłumaczenia, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w jego rodzimym języku powinien być uznawany za autorytatywne źródło. W przypadku informacji o kluczowym znaczeniu zaleca się skorzystanie z profesjonalnego tłumaczenia przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z korzystania z tego tłumaczenia.