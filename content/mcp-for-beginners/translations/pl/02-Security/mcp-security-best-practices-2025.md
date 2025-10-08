<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T12:16:53+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "pl"
}
-->
# Najlepsze praktyki bezpieczeństwa MCP - aktualizacja sierpień 2025

> **Ważne**: Ten dokument odzwierciedla najnowsze wymagania bezpieczeństwa [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) oraz oficjalne [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Zawsze odwołuj się do aktualnej specyfikacji, aby uzyskać najbardziej aktualne wskazówki.

## Podstawowe praktyki bezpieczeństwa dla implementacji MCP

Model Context Protocol wprowadza unikalne wyzwania związane z bezpieczeństwem, które wykraczają poza tradycyjne zabezpieczenia oprogramowania. Te praktyki dotyczą zarówno podstawowych wymagań bezpieczeństwa, jak i zagrożeń specyficznych dla MCP, takich jak wstrzykiwanie poleceń, zatruwanie narzędzi, przejęcie sesji, problemy z zdezorientowanym pełnomocnikiem oraz podatności związane z przekazywaniem tokenów.

### **OBOWIĄZKOWE wymagania bezpieczeństwa**

**Kluczowe wymagania ze specyfikacji MCP:**

> **NIE WOLNO**: Serwery MCP **NIE WOLNO** akceptować żadnych tokenów, które nie zostały wyraźnie wydane dla serwera MCP  
> 
> **MUSI**: Serwery MCP implementujące autoryzację **MUSZĄ** weryfikować WSZYSTKIE przychodzące żądania  
>  
> **NIE WOLNO**: Serwery MCP **NIE WOLNO** używać sesji do uwierzytelniania  
>
> **MUSI**: Serwery proxy MCP używające statycznych identyfikatorów klientów **MUSZĄ** uzyskać zgodę użytkownika dla każdego dynamicznie zarejestrowanego klienta  

---

## 1. **Bezpieczeństwo tokenów i uwierzytelnianie**

**Kontrole uwierzytelniania i autoryzacji:**
   - **Dokładna weryfikacja autoryzacji**: Przeprowadzaj kompleksowe audyty logiki autoryzacji serwera MCP, aby upewnić się, że tylko zamierzeni użytkownicy i klienci mają dostęp do zasobów  
   - **Integracja z zewnętrznymi dostawcami tożsamości**: Korzystaj z uznanych dostawców tożsamości, takich jak Microsoft Entra ID, zamiast implementować własne rozwiązania uwierzytelniające  
   - **Walidacja odbiorcy tokenów**: Zawsze sprawdzaj, czy tokeny zostały wyraźnie wydane dla Twojego serwera MCP - nigdy nie akceptuj tokenów z upstream  
   - **Prawidłowy cykl życia tokenów**: Wdrażaj bezpieczną rotację tokenów, polityki ich wygaśnięcia oraz zapobiegaj atakom typu replay  

**Chronione przechowywanie tokenów:**
   - Korzystaj z Azure Key Vault lub podobnych bezpiecznych magazynów poświadczeń dla wszystkich sekretów  
   - Wdrażaj szyfrowanie tokenów zarówno w spoczynku, jak i w tranzycie  
   - Regularna rotacja poświadczeń i monitorowanie nieautoryzowanego dostępu  

## 2. **Zarządzanie sesjami i bezpieczeństwo transportu**

**Bezpieczne praktyki sesji:**
   - **Kryptograficznie bezpieczne identyfikatory sesji**: Używaj bezpiecznych, niedeterministycznych identyfikatorów sesji generowanych za pomocą bezpiecznych generatorów liczb losowych  
   - **Powiązanie z użytkownikiem**: Powiąż identyfikatory sesji z tożsamościami użytkowników, używając formatów takich jak `<user_id>:<session_id>`, aby zapobiec nadużyciom między użytkownikami  
   - **Zarządzanie cyklem życia sesji**: Wdrażaj odpowiednie wygaśnięcie, rotację i unieważnienie, aby ograniczyć okna podatności  
   - **Wymuszenie HTTPS/TLS**: Obowiązkowy HTTPS dla całej komunikacji, aby zapobiec przechwytywaniu identyfikatorów sesji  

**Bezpieczeństwo warstwy transportowej:**
   - Konfiguruj TLS 1.3, gdzie to możliwe, z odpowiednim zarządzaniem certyfikatami  
   - Wdrażaj przypinanie certyfikatów dla kluczowych połączeń  
   - Regularna rotacja certyfikatów i weryfikacja ich ważności  

## 3. **Ochrona przed zagrożeniami specyficznymi dla AI** 🤖

**Obrona przed wstrzykiwaniem poleceń:**
   - **Microsoft Prompt Shields**: Wdrażaj AI Prompt Shields do zaawansowanego wykrywania i filtrowania złośliwych instrukcji  
   - **Sanityzacja wejścia**: Waliduj i oczyszczaj wszystkie dane wejściowe, aby zapobiec atakom typu injection i problemom z zdezorientowanym pełnomocnikiem  
   - **Granice treści**: Używaj systemów delimiterów i oznaczania danych, aby odróżnić zaufane instrukcje od treści zewnętrznych  

**Zapobieganie zatruwaniu narzędzi:**
   - **Walidacja metadanych narzędzi**: Wdrażaj kontrole integralności definicji narzędzi i monitoruj nieoczekiwane zmiany  
   - **Dynamiczne monitorowanie narzędzi**: Monitoruj zachowanie w czasie rzeczywistym i ustaw alerty dla nieoczekiwanych wzorców wykonania  
   - **Procesy zatwierdzania**: Wymagaj wyraźnej zgody użytkownika na modyfikacje narzędzi i zmiany ich możliwości  

## 4. **Kontrola dostępu i uprawnienia**

**Zasada najmniejszych uprawnień:**
   - Przyznawaj serwerom MCP tylko minimalne uprawnienia wymagane do zamierzonej funkcjonalności  
   - Wdrażaj kontrolę dostępu opartą na rolach (RBAC) z precyzyjnymi uprawnieniami  
   - Regularne przeglądy uprawnień i ciągłe monitorowanie eskalacji uprawnień  

**Kontrole uprawnień w czasie rzeczywistym:**
   - Stosuj limity zasobów, aby zapobiec atakom wyczerpującym zasoby  
   - Używaj izolacji kontenerów dla środowisk wykonawczych narzędzi  
   - Wdrażaj dostęp just-in-time dla funkcji administracyjnych  

## 5. **Bezpieczeństwo treści i monitorowanie**

**Implementacja bezpieczeństwa treści:**
   - **Integracja z Azure Content Safety**: Korzystaj z Azure Content Safety do wykrywania szkodliwych treści, prób jailbreak oraz naruszeń polityki  
   - **Analiza behawioralna**: Wdrażaj monitorowanie zachowań w czasie rzeczywistym, aby wykrywać anomalie w działaniu serwera MCP i narzędzi  
   - **Kompleksowe logowanie**: Loguj wszystkie próby uwierzytelnienia, wywołania narzędzi i zdarzenia bezpieczeństwa w bezpiecznym, odpornym na manipulacje magazynie  

**Ciągłe monitorowanie:**
   - Alerty w czasie rzeczywistym dla podejrzanych wzorców i prób nieautoryzowanego dostępu  
   - Integracja z systemami SIEM dla scentralizowanego zarządzania zdarzeniami bezpieczeństwa  
   - Regularne audyty bezpieczeństwa i testy penetracyjne implementacji MCP  

## 6. **Bezpieczeństwo łańcucha dostaw**

**Weryfikacja komponentów:**
   - **Skanowanie zależności**: Korzystaj z automatycznego skanowania podatności dla wszystkich zależności oprogramowania i komponentów AI  
   - **Walidacja pochodzenia**: Weryfikuj pochodzenie, licencjonowanie i integralność modeli, źródeł danych oraz usług zewnętrznych  
   - **Podpisane pakiety**: Korzystaj z kryptograficznie podpisanych pakietów i weryfikuj podpisy przed wdrożeniem  

**Bezpieczny pipeline rozwoju:**
   - **GitHub Advanced Security**: Wdrażaj skanowanie sekretów, analizę zależności i statyczną analizę CodeQL  
   - **Bezpieczeństwo CI/CD**: Integruj walidację bezpieczeństwa w całym zautomatyzowanym pipeline wdrożeniowym  
   - **Integralność artefaktów**: Wdrażaj kryptograficzną weryfikację wdrożonych artefaktów i konfiguracji  

## 7. **Bezpieczeństwo OAuth i zapobieganie zdezorientowanemu pełnomocnikowi**

**Implementacja OAuth 2.1:**
   - **Implementacja PKCE**: Korzystaj z Proof Key for Code Exchange (PKCE) dla wszystkich żądań autoryzacji  
   - **Wyraźna zgoda**: Uzyskaj zgodę użytkownika dla każdego dynamicznie zarejestrowanego klienta, aby zapobiec atakom zdezorientowanego pełnomocnika  
   - **Walidacja URI przekierowania**: Wdrażaj ścisłą walidację URI przekierowania i identyfikatorów klientów  

**Bezpieczeństwo proxy:**
   - Zapobiegaj obejściu autoryzacji poprzez wykorzystanie statycznych identyfikatorów klientów  
   - Wdrażaj odpowiednie procesy zgody dla dostępu do API stron trzecich  
   - Monitoruj kradzież kodów autoryzacyjnych i nieautoryzowany dostęp do API  

## 8. **Reakcja na incydenty i odzyskiwanie**

**Szybkie możliwości reakcji:**
   - **Automatyczna reakcja**: Wdrażaj zautomatyzowane systemy do rotacji poświadczeń i ograniczania zagrożeń  
   - **Procedury wycofywania**: Możliwość szybkiego powrotu do znanych, dobrych konfiguracji i komponentów  
   - **Możliwości śledcze**: Szczegółowe ścieżki audytu i logowanie dla badania incydentów  

**Komunikacja i koordynacja:**
   - Jasne procedury eskalacji dla incydentów bezpieczeństwa  
   - Integracja z zespołami reagowania na incydenty w organizacji  
   - Regularne symulacje incydentów bezpieczeństwa i ćwiczenia scenariuszowe  

## 9. **Zgodność i zarządzanie**

**Zgodność regulacyjna:**
   - Upewnij się, że implementacje MCP spełniają wymagania specyficzne dla branży (GDPR, HIPAA, SOC 2)  
   - Wdrażaj klasyfikację danych i kontrole prywatności dla przetwarzania danych AI  
   - Utrzymuj kompleksową dokumentację dla audytów zgodności  

**Zarządzanie zmianami:**
   - Formalne procesy przeglądu bezpieczeństwa dla wszystkich modyfikacji systemu MCP  
   - Kontrola wersji i procesy zatwierdzania dla zmian konfiguracji  
   - Regularne oceny zgodności i analiza luk  

## 10. **Zaawansowane kontrole bezpieczeństwa**

**Architektura Zero Trust:**
   - **Nigdy nie ufaj, zawsze weryfikuj**: Ciągła weryfikacja użytkowników, urządzeń i połączeń  
   - **Mikrosegmentacja**: Granularne kontrole sieciowe izolujące poszczególne komponenty MCP  
   - **Dostęp warunkowy**: Kontrole dostępu oparte na ryzyku, dostosowujące się do bieżącego kontekstu i zachowania  

**Ochrona aplikacji w czasie rzeczywistym:**
   - **Runtime Application Self-Protection (RASP)**: Wdrażaj techniki RASP do wykrywania zagrożeń w czasie rzeczywistym  
   - **Monitorowanie wydajności aplikacji**: Monitoruj anomalie wydajności, które mogą wskazywać na ataki  
   - **Dynamiczne polityki bezpieczeństwa**: Wdrażaj polityki bezpieczeństwa dostosowujące się do bieżącego krajobrazu zagrożeń  

## 11. **Integracja z ekosystemem bezpieczeństwa Microsoft**

**Kompleksowe bezpieczeństwo Microsoft:**
   - **Microsoft Defender for Cloud**: Zarządzanie postawą bezpieczeństwa chmury dla obciążeń MCP  
   - **Azure Sentinel**: Natywne rozwiązania SIEM i SOAR dla zaawansowanego wykrywania zagrożeń  
   - **Microsoft Purview**: Zarządzanie danymi i zgodność dla przepływów pracy AI i źródeł danych  

**Zarządzanie tożsamością i dostępem:**
   - **Microsoft Entra ID**: Zarządzanie tożsamością przedsiębiorstwa z politykami dostępu warunkowego  
   - **Privileged Identity Management (PIM)**: Dostęp just-in-time i procesy zatwierdzania dla funkcji administracyjnych  
   - **Ochrona tożsamości**: Dostęp warunkowy oparty na ryzyku i zautomatyzowana reakcja na zagrożenia  

## 12. **Ciągła ewolucja bezpieczeństwa**

**Pozostawanie na bieżąco:**
   - **Monitorowanie specyfikacji**: Regularne przeglądy aktualizacji specyfikacji MCP i zmian w wytycznych dotyczących bezpieczeństwa  
   - **Wywiad zagrożeń**: Integracja z kanałami zagrożeń specyficznych dla AI i wskaźnikami kompromitacji  
   - **Zaangażowanie społeczności bezpieczeństwa**: Aktywny udział w społeczności bezpieczeństwa MCP i programach zgłaszania podatności  

**Adaptacyjne bezpieczeństwo:**
   - **Bezpieczeństwo oparte na uczeniu maszynowym**: Korzystaj z wykrywania anomalii opartego na ML do identyfikacji nowych wzorców ataków  
   - **Predykcyjna analiza bezpieczeństwa**: Wdrażaj modele predykcyjne do proaktywnej identyfikacji zagrożeń  
   - **Automatyzacja bezpieczeństwa**: Zautomatyzowane aktualizacje polityk bezpieczeństwa na podstawie wywiadu zagrożeń i zmian w specyfikacji  

---

## **Kluczowe zasoby bezpieczeństwa**

### **Oficjalna dokumentacja MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Rozwiązania bezpieczeństwa Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Security](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Standardy bezpieczeństwa**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Przewodniki implementacyjne**
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Informacja o bezpieczeństwie**: Praktyki bezpieczeństwa MCP ewoluują szybko. Zawsze weryfikuj zgodność z aktualną [specyfikacją MCP](https://spec.modelcontextprotocol.io/) oraz [oficjalną dokumentacją bezpieczeństwa](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) przed wdrożeniem.

**Zastrzeżenie**:  
Ten dokument został przetłumaczony za pomocą usługi tłumaczeniowej AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dokładamy wszelkich starań, aby zapewnić dokładność, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w jego rodzimym języku powinien być uznawany za wiarygodne źródło. W przypadku informacji krytycznych zaleca się skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z korzystania z tego tłumaczenia.