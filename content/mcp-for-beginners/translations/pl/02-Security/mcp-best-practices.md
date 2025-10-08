<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T12:20:25+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "pl"
}
-->
# Najlepsze praktyki bezpieczeństwa MCP 2025

Ten kompleksowy przewodnik przedstawia kluczowe praktyki bezpieczeństwa dla wdrażania systemów Model Context Protocol (MCP) zgodnie z najnowszą **Specyfikacją MCP 2025-06-18** oraz aktualnymi standardami branżowymi. Praktyki te dotyczą zarówno tradycyjnych zagrożeń bezpieczeństwa, jak i specyficznych dla AI zagrożeń związanych z wdrożeniami MCP.

## Kluczowe wymagania bezpieczeństwa

### Obowiązkowe mechanizmy bezpieczeństwa (wymagania MUST)

1. **Walidacja tokenów**: Serwery MCP **NIE MOGĄ** akceptować tokenów, które nie zostały wyraźnie wydane dla danego serwera MCP.
2. **Weryfikacja autoryzacji**: Serwery MCP implementujące autoryzację **MUSZĄ** weryfikować WSZYSTKIE przychodzące żądania i **NIE MOGĄ** używać sesji do uwierzytelniania.  
3. **Zgoda użytkownika**: Serwery proxy MCP używające statycznych identyfikatorów klientów **MUSZĄ** uzyskać wyraźną zgodę użytkownika dla każdego dynamicznie rejestrowanego klienta.
4. **Bezpieczne identyfikatory sesji**: Serwery MCP **MUSZĄ** używać kryptograficznie bezpiecznych, niedeterministycznych identyfikatorów sesji generowanych za pomocą bezpiecznych generatorów liczb losowych.

## Podstawowe praktyki bezpieczeństwa

### 1. Walidacja i oczyszczanie danych wejściowych
- **Kompleksowa walidacja danych wejściowych**: Waliduj i oczyszczaj wszystkie dane wejściowe, aby zapobiec atakom typu injection, problemom z zaufaniem oraz podatnościom na manipulację promptami.
- **Egzekwowanie schematów parametrów**: Wdroż ścisłą walidację schematów JSON dla wszystkich parametrów narzędzi i danych wejściowych API.
- **Filtrowanie treści**: Używaj Microsoft Prompt Shields i Azure Content Safety do filtrowania złośliwych treści w promptach i odpowiedziach.
- **Oczyszczanie danych wyjściowych**: Waliduj i oczyszczaj wszystkie dane wyjściowe modelu przed ich prezentacją użytkownikom lub systemom downstream.

### 2. Doskonałość w uwierzytelnianiu i autoryzacji  
- **Zewnętrzni dostawcy tożsamości**: Deleguj uwierzytelnianie do uznanych dostawców tożsamości (Microsoft Entra ID, dostawcy OAuth 2.1) zamiast implementować własne rozwiązania.
- **Precyzyjne uprawnienia**: Wdroż granularne, specyficzne dla narzędzi uprawnienia zgodnie z zasadą najmniejszych uprawnień.
- **Zarządzanie cyklem życia tokenów**: Używaj tokenów dostępu o krótkim czasie życia z bezpieczną rotacją i odpowiednią walidacją odbiorców.
- **Uwierzytelnianie wieloskładnikowe**: Wymagaj MFA dla wszystkich dostępów administracyjnych i operacji wrażliwych.

### 3. Bezpieczne protokoły komunikacyjne
- **Transport Layer Security**: Używaj HTTPS/TLS 1.3 dla wszystkich komunikacji MCP z odpowiednią walidacją certyfikatów.
- **Szyfrowanie end-to-end**: Wdroż dodatkowe warstwy szyfrowania dla danych o wysokiej wrażliwości w tranzycie i w spoczynku.
- **Zarządzanie certyfikatami**: Utrzymuj odpowiedni cykl życia certyfikatów z automatycznymi procesami odnawiania.
- **Egzekwowanie wersji protokołu**: Używaj aktualnej wersji protokołu MCP (2025-06-18) z odpowiednią negocjacją wersji.

### 4. Zaawansowane ograniczanie szybkości i ochrona zasobów
- **Wielowarstwowe ograniczanie szybkości**: Wdroż ograniczanie szybkości na poziomie użytkownika, sesji, narzędzia i zasobów, aby zapobiec nadużyciom.
- **Adaptacyjne ograniczanie szybkości**: Używaj ograniczania szybkości opartego na uczeniu maszynowym, które dostosowuje się do wzorców użytkowania i wskaźników zagrożeń.
- **Zarządzanie kwotami zasobów**: Ustal odpowiednie limity dla zasobów obliczeniowych, użycia pamięci i czasu wykonania.
- **Ochrona przed DDoS**: Wdroż kompleksowe systemy ochrony przed DDoS i analizy ruchu.

### 5. Kompleksowe logowanie i monitorowanie
- **Strukturalne logowanie audytowe**: Wdroż szczegółowe, przeszukiwalne logi dla wszystkich operacji MCP, wykonania narzędzi i zdarzeń bezpieczeństwa.
- **Monitorowanie bezpieczeństwa w czasie rzeczywistym**: Wdroż systemy SIEM z wykrywaniem anomalii opartym na AI dla obciążeń MCP.
- **Logowanie zgodne z prywatnością**: Loguj zdarzenia bezpieczeństwa, przestrzegając wymagań dotyczących prywatności danych i regulacji.
- **Integracja z reakcją na incydenty**: Połącz systemy logowania z automatycznymi przepływami pracy reagowania na incydenty.

### 6. Ulepszone praktyki bezpiecznego przechowywania
- **Moduły bezpieczeństwa sprzętowego**: Używaj przechowywania kluczy wspieranego przez HSM (Azure Key Vault, AWS CloudHSM) dla kluczowych operacji kryptograficznych.
- **Zarządzanie kluczami szyfrowania**: Wdroż odpowiednią rotację kluczy, ich segregację i kontrolę dostępu.
- **Zarządzanie sekretami**: Przechowuj wszystkie klucze API, tokeny i dane uwierzytelniające w dedykowanych systemach zarządzania sekretami.
- **Klasyfikacja danych**: Klasyfikuj dane na podstawie poziomów wrażliwości i stosuj odpowiednie środki ochrony.

### 7. Zaawansowane zarządzanie tokenami
- **Zapobieganie przekazywaniu tokenów**: Wyraźnie zabroń wzorców przekazywania tokenów, które omijają mechanizmy bezpieczeństwa.
- **Walidacja odbiorców**: Zawsze weryfikuj, czy odbiorcy tokenów odpowiadają tożsamości docelowego serwera MCP.
- **Autoryzacja oparta na roszczeniach**: Wdroż precyzyjną autoryzację opartą na roszczeniach tokenów i atrybutach użytkownika.
- **Powiązanie tokenów**: Powiąż tokeny z konkretnymi sesjami, użytkownikami lub urządzeniami, jeśli to możliwe.

### 8. Bezpieczne zarządzanie sesjami
- **Kryptograficzne identyfikatory sesji**: Generuj identyfikatory sesji za pomocą kryptograficznie bezpiecznych generatorów liczb losowych (nieprzewidywalnych sekwencji).
- **Powiązanie specyficzne dla użytkownika**: Powiąż identyfikatory sesji z informacjami specyficznymi dla użytkownika, używając bezpiecznych formatów, takich jak `<user_id>:<session_id>`.
- **Kontrola cyklu życia sesji**: Wdroż odpowiednie mechanizmy wygaśnięcia, rotacji i unieważnienia sesji.
- **Nagłówki bezpieczeństwa sesji**: Używaj odpowiednich nagłówków HTTP dla ochrony sesji.

### 9. Specyficzne dla AI mechanizmy bezpieczeństwa
- **Obrona przed manipulacją promptami**: Wdroż Microsoft Prompt Shields z technikami spotlightingu, delimitacji i oznaczania danych.
- **Zapobieganie zatruwaniu narzędzi**: Waliduj metadane narzędzi, monitoruj dynamiczne zmiany i weryfikuj integralność narzędzi.
- **Walidacja danych wyjściowych modelu**: Skanuj dane wyjściowe modelu pod kątem potencjalnych wycieków danych, szkodliwych treści lub naruszeń polityki bezpieczeństwa.
- **Ochrona okna kontekstowego**: Wdroż mechanizmy zapobiegające zatruwaniu okna kontekstowego i atakom manipulacyjnym.

### 10. Bezpieczeństwo wykonywania narzędzi
- **Izolacja wykonywania**: Uruchamiaj narzędzia w konteneryzowanych, izolowanych środowiskach z ograniczeniami zasobów.
- **Oddzielenie uprawnień**: Wykonuj narzędzia z minimalnymi wymaganymi uprawnieniami i oddzielnymi kontami usługowymi.
- **Izolacja sieciowa**: Wdroż segmentację sieci dla środowisk wykonywania narzędzi.
- **Monitorowanie wykonywania**: Monitoruj wykonywanie narzędzi pod kątem anomalii, użycia zasobów i naruszeń bezpieczeństwa.

### 11. Ciągła walidacja bezpieczeństwa
- **Automatyczne testy bezpieczeństwa**: Zintegruj testy bezpieczeństwa z pipeline'ami CI/CD, używając narzędzi takich jak GitHub Advanced Security.
- **Zarządzanie podatnościami**: Regularnie skanuj wszystkie zależności, w tym modele AI i usługi zewnętrzne.
- **Testy penetracyjne**: Regularnie przeprowadzaj oceny bezpieczeństwa, szczególnie ukierunkowane na implementacje MCP.
- **Przeglądy kodu pod kątem bezpieczeństwa**: Wdroż obowiązkowe przeglądy bezpieczeństwa dla wszystkich zmian kodu związanych z MCP.

### 12. Bezpieczeństwo łańcucha dostaw dla AI
- **Weryfikacja komponentów**: Weryfikuj pochodzenie, integralność i bezpieczeństwo wszystkich komponentów AI (modeli, osadzeń, API).
- **Zarządzanie zależnościami**: Utrzymuj aktualne inwentarze wszystkich zależności oprogramowania i AI z monitorowaniem podatności.
- **Zaufane repozytoria**: Używaj zweryfikowanych, zaufanych źródeł dla wszystkich modeli AI, bibliotek i narzędzi.
- **Monitorowanie łańcucha dostaw**: Ciągle monitoruj kompromitacje u dostawców usług AI i w repozytoriach modeli.

## Zaawansowane wzorce bezpieczeństwa

### Architektura Zero Trust dla MCP
- **Nigdy nie ufaj, zawsze weryfikuj**: Wdroż ciągłą weryfikację dla wszystkich uczestników MCP.
- **Mikrosegmentacja**: Izoluj komponenty MCP za pomocą granularnych kontroli sieciowych i tożsamościowych.
- **Dostęp warunkowy**: Wdroż kontrolę dostępu opartą na ryzyku, dostosowującą się do kontekstu i zachowań.
- **Ciągła ocena ryzyka**: Dynamicznie oceniaj postawę bezpieczeństwa na podstawie aktualnych wskaźników zagrożeń.

### Implementacja AI z zachowaniem prywatności
- **Minimalizacja danych**: Udostępniaj tylko minimalnie niezbędne dane dla każdej operacji MCP.
- **Prywatność różnicowa**: Wdroż techniki zachowania prywatności dla przetwarzania danych wrażliwych.
- **Szyfrowanie homomorficzne**: Używaj zaawansowanych technik szyfrowania dla bezpiecznych obliczeń na zaszyfrowanych danych.
- **Uczenie federacyjne**: Wdroż podejścia do uczenia rozproszonego, które zachowują lokalność danych i prywatność.

### Reakcja na incydenty w systemach AI
- **Procedury specyficzne dla AI**: Opracuj procedury reagowania na incydenty dostosowane do zagrożeń specyficznych dla AI i MCP.
- **Automatyczna reakcja**: Wdroż automatyczne mechanizmy ograniczania i naprawy dla typowych incydentów bezpieczeństwa AI.  
- **Zdolności do analizy kryminalistycznej**: Utrzymuj gotowość do analizy kryminalistycznej w przypadku kompromitacji systemów AI i wycieków danych.
- **Procedury odzyskiwania**: Ustal procedury odzyskiwania po zatruwaniu modeli AI, atakach na prompty i kompromitacji usług.

## Zasoby wdrożeniowe i standardy

### Oficjalna dokumentacja MCP
- [Specyfikacja MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Aktualna specyfikacja protokołu MCP
- [Najlepsze praktyki bezpieczeństwa MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Oficjalne wytyczne dotyczące bezpieczeństwa
- [Specyfikacja autoryzacji MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Wzorce uwierzytelniania i autoryzacji
- [Bezpieczeństwo transportu MCP](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Wymagania dotyczące bezpieczeństwa warstwy transportowej

### Rozwiązania bezpieczeństwa Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Zaawansowana ochrona przed manipulacją promptami
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Kompleksowe filtrowanie treści AI
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Zarządzanie tożsamością i dostępem w przedsiębiorstwie
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Bezpieczne zarządzanie sekretami i danymi uwierzytelniającymi
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Skanowanie bezpieczeństwa kodu i łańcucha dostaw

### Standardy bezpieczeństwa i ramy
- [Najlepsze praktyki bezpieczeństwa OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Aktualne wytyczne dotyczące bezpieczeństwa OAuth
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Ryzyka bezpieczeństwa aplikacji webowych
- [OWASP Top 10 dla LLM](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Ryzyka bezpieczeństwa specyficzne dla AI
- [Ramy zarządzania ryzykiem AI NIST](https://www.nist.gov/itl/ai-risk-management-framework) - Kompleksowe zarządzanie ryzykiem AI
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Systemy zarządzania bezpieczeństwem informacji

### Przewodniki wdrożeniowe i samouczki
- [Azure API Management jako brama autoryzacji MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Wzorce uwierzytelniania w przedsiębiorstwie
- [Microsoft Entra ID z serwerami MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integracja dostawcy tożsamości
- [Implementacja bezpiecznego przechowywania tokenów](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Najlepsze praktyki zarządzania tokenami
- [Szyfrowanie end-to-end dla AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Zaawansowane wzorce szyfrowania

### Zaawansowane zasoby bezpieczeństwa
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Praktyki bezpiecznego rozwoju
- [Wytyczne dla zespołów red AI](https://learn.microsoft.com/security/ai-red-team/) - Testowanie bezpieczeństwa specyficzne dla AI
- [Modelowanie zagrożeń dla systemów AI](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologia modelowania zagrożeń AI
- [Inżynieria prywatności dla AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Techniki zachowania prywatności w AI

### Zgodność i zarządzanie
- [Zgodność z RODO dla AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Zgodność z przepisami dotyczącymi prywatności w systemach AI
- [Ramy zarządzania AI](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Odpowiedzialne wdrożenie AI
- [SOC 2 dla usług AI](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Kontrole bezpieczeństwa dla dostawców usług AI
- [Zgodność z HIPAA dla AI](https://learn.microsoft.com
- **Rozwój narzędzi**: Tworzenie i udostępnianie narzędzi oraz bibliotek bezpieczeństwa dla ekosystemu MCP

---

*Ten dokument odzwierciedla najlepsze praktyki bezpieczeństwa MCP na dzień 18 sierpnia 2025 roku, zgodnie ze Specyfikacją MCP 2025-06-18. Praktyki bezpieczeństwa powinny być regularnie przeglądane i aktualizowane w miarę rozwoju protokołu i zmieniającego się krajobrazu zagrożeń.*

**Zastrzeżenie**:  
Ten dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dokładamy wszelkich starań, aby tłumaczenie było precyzyjne, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w jego rodzimym języku powinien być uznawany za autorytatywne źródło. W przypadku informacji o kluczowym znaczeniu zaleca się skorzystanie z profesjonalnego tłumaczenia przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.