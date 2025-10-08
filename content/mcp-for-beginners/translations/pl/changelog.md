<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:00:08+00:00",
  "source_file": "changelog.md",
  "language_code": "pl"
}
-->
# Dziennik zmian: Program nauczania MCP dla początkujących

Ten dokument stanowi zapis wszystkich istotnych zmian wprowadzonych w programie nauczania Model Context Protocol (MCP) dla początkujących. Zmiany są dokumentowane w odwrotnej kolejności chronologicznej (najpierw najnowsze).

## 6 października 2025

### Rozszerzenie sekcji „Pierwsze kroki” – Zaawansowane użycie serwera i prosta autentykacja

#### Zaawansowane użycie serwera (03-GettingStarted/10-advanced)
- **Dodano nowy rozdział**: Wprowadzono kompleksowy przewodnik po zaawansowanym użyciu serwera MCP, obejmujący zarówno regularne, jak i niskopoziomowe architektury serwerowe.
  - **Regularny vs. niskopoziomowy serwer**: Szczegółowe porównanie i przykłady kodu w Pythonie i TypeScript dla obu podejść.
  - **Projekt oparty na handlerach**: Wyjaśnienie zarządzania narzędziami/zasobami/promptami opartego na handlerach dla skalowalnych i elastycznych implementacji serwerowych.
  - **Praktyczne wzorce**: Scenariusze z życia wzięte, w których wzorce niskopoziomowych serwerów są korzystne dla zaawansowanych funkcji i architektury.

#### Prosta autentykacja (03-GettingStarted/11-simple-auth)
- **Dodano nowy rozdział**: Przewodnik krok po kroku dotyczący implementacji prostej autentykacji w serwerach MCP.
  - **Koncepcje autentykacji**: Jasne wyjaśnienie różnicy między autentykacją a autoryzacją oraz obsługą poświadczeń.
  - **Implementacja podstawowej autentykacji**: Wzorce autentykacji oparte na middleware w Pythonie (Starlette) i TypeScript (Express), z przykładami kodu.
  - **Przejście do zaawansowanego bezpieczeństwa**: Wskazówki dotyczące rozpoczęcia od prostej autentykacji i przejścia do OAuth 2.1 oraz RBAC, z odniesieniami do zaawansowanych modułów bezpieczeństwa.

Te dodatki zapewniają praktyczne, praktyczne wskazówki dotyczące budowania bardziej solidnych, bezpiecznych i elastycznych implementacji serwerów MCP, łącząc podstawowe koncepcje z zaawansowanymi wzorcami produkcyjnymi.

## 29 września 2025

### Laboratoria integracji baz danych serwera MCP – kompleksowa ścieżka nauki praktycznej

#### 11-MCPServerHandsOnLabs – Nowy kompletny program nauczania integracji baz danych
- **Kompletna ścieżka nauki obejmująca 13 laboratoriów**: Dodano kompleksowy program nauczania praktycznego dotyczący budowy serwerów MCP gotowych do produkcji z integracją bazy danych PostgreSQL.
  - **Implementacja w rzeczywistości**: Przypadek użycia analityki Zava Retail demonstrujący wzorce na poziomie przedsiębiorstwa.
  - **Struktura nauki**:
    - **Laboratoria 00-03: Podstawy** – Wprowadzenie, podstawowa architektura, bezpieczeństwo i wielodostępność, konfiguracja środowiska.
    - **Laboratoria 04-06: Budowa serwera MCP** – Projektowanie bazy danych i schemat, implementacja serwera MCP, rozwój narzędzi.
    - **Laboratoria 07-09: Zaawansowane funkcje** – Integracja wyszukiwania semantycznego, testowanie i debugowanie, integracja z VS Code.
    - **Laboratoria 10-12: Produkcja i najlepsze praktyki** – Strategie wdrażania, monitorowanie i obserwowalność, najlepsze praktyki i optymalizacja.
  - **Technologie na poziomie przedsiębiorstwa**: Framework FastMCP, PostgreSQL z pgvector, osadzenia Azure OpenAI, Azure Container Apps, Application Insights.
  - **Zaawansowane funkcje**: Bezpieczeństwo na poziomie wiersza (RLS), wyszukiwanie semantyczne, dostęp do danych wielodostępnych, osadzenia wektorowe, monitorowanie w czasie rzeczywistym.

#### Standaryzacja terminologii – Konwersja „Moduł” na „Laboratorium”
- **Kompleksowa aktualizacja dokumentacji**: Systematycznie zaktualizowano wszystkie pliki README w 11-MCPServerHandsOnLabs, aby używać terminologii „Laboratorium” zamiast „Moduł”.
  - **Nagłówki sekcji**: Zmieniono „Co obejmuje ten moduł” na „Co obejmuje to laboratorium” we wszystkich 13 laboratoriach.
  - **Opis treści**: Zmieniono „Ten moduł zapewnia...” na „To laboratorium zapewnia...” w całej dokumentacji.
  - **Cele nauki**: Zmieniono „Na końcu tego modułu...” na „Na końcu tego laboratorium...”.
  - **Linki nawigacyjne**: Przekonwertowano wszystkie odniesienia „Moduł XX:” na „Laboratorium XX:” w odniesieniach krzyżowych i nawigacji.
  - **Śledzenie ukończenia**: Zmieniono „Po ukończeniu tego modułu...” na „Po ukończeniu tego laboratorium...”.
  - **Zachowane odniesienia techniczne**: Zachowano odniesienia do modułów Pythona w plikach konfiguracyjnych (np. `"module": "mcp_server.main"`).

#### Ulepszenie przewodnika nauki (study_guide.md)
- **Wizualna mapa programu nauczania**: Dodano nową sekcję „11. Laboratoria integracji baz danych” z kompleksową wizualizacją struktury laboratoriów.
- **Struktura repozytorium**: Zaktualizowano z dziesięciu do jedenastu głównych sekcji z szczegółowym opisem 11-MCPServerHandsOnLabs.
- **Wskazówki dotyczące ścieżki nauki**: Ulepszono instrukcje nawigacyjne, aby obejmowały sekcje 00-11.
- **Pokrycie technologiczne**: Dodano szczegóły integracji FastMCP, PostgreSQL, usług Azure.
- **Rezultaty nauki**: Podkreślono rozwój serwerów gotowych do produkcji, wzorce integracji baz danych i bezpieczeństwo na poziomie przedsiębiorstwa.

#### Ulepszenie struktury głównego README
- **Terminologia oparta na laboratoriach**: Zaktualizowano główny README.md w 11-MCPServerHandsOnLabs, aby konsekwentnie używać struktury „Laboratorium”.
- **Organizacja ścieżki nauki**: Jasna progresja od podstawowych koncepcji przez zaawansowaną implementację do wdrożenia produkcyjnego.
- **Skupienie na rzeczywistości**: Nacisk na praktyczne, praktyczne uczenie się z wzorcami i technologiami na poziomie przedsiębiorstwa.

### Ulepszenia jakości i spójności dokumentacji
- **Nacisk na naukę praktyczną**: Wzmocniono praktyczne, podejście oparte na laboratoriach w całej dokumentacji.
- **Skupienie na wzorcach przedsiębiorstwa**: Podkreślono implementacje gotowe do produkcji i rozważania dotyczące bezpieczeństwa na poziomie przedsiębiorstwa.
- **Integracja technologii**: Kompleksowe pokrycie nowoczesnych usług Azure i wzorców integracji AI.
- **Progresja nauki**: Jasna, uporządkowana ścieżka od podstawowych koncepcji do wdrożenia produkcyjnego.

## 26 września 2025

### Ulepszenie studiów przypadków – Integracja rejestru MCP GitHub

#### Studia przypadków (09-CaseStudy/) – Skupienie na rozwoju ekosystemu
- **README.md**: Główne rozszerzenie z kompleksowym studium przypadku rejestru MCP GitHub.
  - **Studium przypadku rejestru MCP GitHub**: Nowe kompleksowe studium przypadku analizujące uruchomienie rejestru MCP GitHub we wrześniu 2025 r.
    - **Analiza problemu**: Szczegółowe badanie wyzwań związanych z fragmentacją odkrywania i wdrażania serwerów MCP.
    - **Architektura rozwiązania**: Podejście GitHub do scentralizowanego rejestru z instalacją jednym kliknięciem w VS Code.
    - **Wpływ biznesowy**: Mierzalne poprawy w onboardingu i produktywności deweloperów.
    - **Wartość strategiczna**: Skupienie na modułowym wdrażaniu agentów i interoperacyjności narzędzi.
    - **Rozwój ekosystemu**: Pozycjonowanie jako platforma podstawowa dla integracji agentów.
  - **Ulepszona struktura studiów przypadków**: Zaktualizowano wszystkie siedem studiów przypadków z jednolitym formatowaniem i kompleksowymi opisami.
    - Azure AI Travel Agents: Nacisk na orkiestrację wieloagentową.
    - Integracja Azure DevOps: Skupienie na automatyzacji przepływu pracy.
    - Pobieranie dokumentacji w czasie rzeczywistym: Implementacja klienta konsoli Python.
    - Interaktywny generator planu nauki: Konwersacyjna aplikacja webowa Chainlit.
    - Dokumentacja w edytorze: Integracja VS Code i GitHub Copilot.
    - Zarządzanie API Azure: Wzorce integracji API na poziomie przedsiębiorstwa.
    - Rejestr MCP GitHub: Rozwój ekosystemu i platforma społecznościowa.
  - **Kompleksowe zakończenie**: Przepisana sekcja zakończenia podkreślająca siedem studiów przypadków obejmujących różne wymiary implementacji MCP.
    - Integracja na poziomie przedsiębiorstwa, orkiestracja wieloagentowa, produktywność deweloperów.
    - Rozwój ekosystemu, kategorie zastosowań edukacyjnych.
    - Ulepszone wglądy w wzorce architektoniczne, strategie implementacji i najlepsze praktyki.
    - Nacisk na MCP jako dojrzały, gotowy do produkcji protokół.

#### Aktualizacje przewodnika nauki (study_guide.md)
- **Wizualna mapa programu nauczania**: Zaktualizowano mapę myśli, aby uwzględnić rejestr MCP GitHub w sekcji studiów przypadków.
- **Opis studiów przypadków**: Ulepszono z ogólnych opisów do szczegółowego podziału siedmiu kompleksowych studiów przypadków.
- **Struktura repozytorium**: Zaktualizowano sekcję 10, aby odzwierciedlała kompleksowe pokrycie studiów przypadków ze szczegółami implementacji.
- **Integracja dziennika zmian**: Dodano wpis z 26 września 2025 r. dokumentujący dodanie rejestru MCP GitHub i ulepszenia studiów przypadków.
- **Aktualizacje daty**: Zaktualizowano stopkę z datą ostatniej rewizji (26 września 2025 r.).

### Ulepszenia jakości dokumentacji
- **Poprawa spójności**: Ujednolicono formatowanie i strukturę studiów przypadków we wszystkich siedmiu przykładach.
- **Kompleksowe pokrycie**: Studia przypadków obejmują teraz scenariusze na poziomie przedsiębiorstwa, produktywności deweloperów i rozwoju ekosystemu.
- **Pozycjonowanie strategiczne**: Wzmocniono nacisk na MCP jako platformę podstawową dla wdrażania systemów agentowych.
- **Integracja zasobów**: Zaktualizowano dodatkowe zasoby, aby uwzględnić link do rejestru MCP GitHub.

## 15 września 2025

### Rozszerzenie zaawansowanych tematów – Niestandardowe transporty i inżynieria kontekstu

#### Niestandardowe transporty MCP (05-AdvancedTopics/mcp-transport/) – Nowy przewodnik zaawansowanej implementacji
- **README.md**: Kompletny przewodnik implementacji niestandardowych mechanizmów transportu MCP.
  - **Transport Azure Event Grid**: Kompleksowa implementacja transportu bezserwerowego opartego na zdarzeniach.
    - Przykłady w C#, TypeScript i Pythonie z integracją Azure Functions.
    - Wzorce architektury opartej na zdarzeniach dla skalowalnych rozwiązań MCP.
    - Odbiorniki webhooków i obsługa wiadomości oparta na push.
  - **Transport Azure Event Hubs**: Implementacja transportu strumieniowego o wysokiej przepustowości.
    - Możliwości strumieniowania w czasie rzeczywistym dla scenariuszy o niskim opóźnieniu.
    - Strategie partycjonowania i zarządzanie punktami kontrolnymi.
    - Grupowanie wiadomości i optymalizacja wydajności.
  - **Wzorce integracji na poziomie przedsiębiorstwa**: Przykłady architektoniczne gotowe do produkcji.
    - Rozproszone przetwarzanie MCP w wielu funkcjach Azure.
    - Hybrydowe architektury transportowe łączące różne typy transportu.
    - Trwałość wiadomości, niezawodność i strategie obsługi błędów.
  - **Bezpieczeństwo i monitorowanie**: Integracja Azure Key Vault i wzorce obserwowalności.
    - Autentykacja zarządzana tożsamością i dostęp o najmniejszych uprawnieniach.
    - Telemetria Application Insights i monitorowanie wydajności.
    - Wyłączniki obwodów i wzorce tolerancji błędów.
  - **Frameworki testowe**: Kompleksowe strategie testowania niestandardowych transportów.
    - Testowanie jednostkowe z dublerami testowymi i frameworkami do mockowania.
    - Testowanie integracyjne z Azure Test Containers.
    - Rozważania dotyczące testowania wydajności i obciążenia.

#### Inżynieria kontekstu (05-AdvancedTopics/mcp-contextengineering/) – Nowa dziedzina AI
- **README.md**: Kompleksowe badanie inżynierii kontekstu jako rozwijającej się dziedziny.
  - **Podstawowe zasady**: Pełne udostępnianie kontekstu, świadomość decyzji o działaniach i zarządzanie oknem kontekstu.
  - **Dostosowanie do protokołu MCP**: Jak projekt MCP rozwiązuje wyzwania inżynierii kontekstu.
    - Ograniczenia okna kontekstu i strategie progresywnego ładowania.
    - Określanie istotności i dynamiczne pobieranie kontekstu.
    - Obsługa kontekstu wielomodalnego i rozważania dotyczące bezpieczeństwa.
  - **Podejścia do implementacji**: Architektury jednowątkowe vs. wieloagentowe.
    - Techniki dzielenia kontekstu i priorytetyzacji.
    - Progresywne ładowanie kontekstu i strategie kompresji.
    - Warstwowe podejścia do kontekstu i optymalizacja pobierania.
  - **Framework pomiarowy**: Powstające metryki oceny efektywności kontekstu.
    - Rozważania dotyczące efektywności wejścia, wydajności, jakości i doświadczenia użytkownika.
    - Eksperymentalne podejścia do optymalizacji kontekstu.
    - Analiza błędów i metody poprawy.

#### Aktualizacje nawigacji programu nauczania (README.md)
- **Ulepszona struktura modułów**: Zaktualizowano tabelę programu nauczania, aby uwzględnić nowe zaawansowane tematy.
  - Dodano Inżynierię kontekstu (5.14) i Niestandardowy transport (5.15).
  - Spójne formatowanie i linki nawigacyjne we wszystkich modułach.
  - Zaktualizowano opisy, aby odzwierciedlały aktualny zakres treści.

### Ulepszenia struktury katalogów
- **Standaryzacja nazw**: Zmieniono nazwę „mcp transport” na „mcp-transport” dla spójności z innymi folderami zaawansowanych tematów.
- **Organizacja treści**: Wszystkie foldery 05-AdvancedTopics teraz mają spójny wzorzec nazewnictwa (mcp-[temat]).

### Ulepszenia jakości dokumentacji
- **Dostosowanie do specyfikacji MCP**: Wszystkie nowe treści odnoszą się do aktualnej specyfikacji MCP z 18 czerwca 2025 r.
- **Przykłady w wielu językach**: Kompleksowe przykłady kodu w C#, TypeScript i Pythonie.
- **Skupienie na przedsiębiorstwie**: Wzorce gotowe do produkcji i integracja z chmurą Azure w całej dokumentacji.
- **Dokumentacja wizualna**: Diagramy Mermaid dla wizualizacji architektury i przepływu.

## 18 sierpnia 2025

### Kompleksowa aktualizacja dokumentacji – Standardy MCP 2025-06-18

#### Najlepsze praktyki bezpieczeństwa MCP (02-Security/) – Kompleksowa modernizacja
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Kompletny przepis zgodny ze specyfikacją MCP z 18 czerwca 2025 r.
  - **Wymagania obowiązkowe**: Dodano wyraźne wymagania MUST/MUST NOT
#### Zaawansowane tematy bezpieczeństwa (05-AdvancedTopics/mcp-security/) - Implementacja gotowa do produkcji
- **README.md**: Kompletny przepis na wdrożenie bezpieczeństwa w przedsiębiorstwie
  - **Zgodność ze specyfikacją**: Zaktualizowano do specyfikacji MCP z 2025-06-18 z obowiązkowymi wymaganiami bezpieczeństwa
  - **Ulepszona autentykacja**: Integracja z Microsoft Entra ID z kompleksowymi przykładami w .NET i Java Spring Security
  - **Integracja bezpieczeństwa AI**: Implementacja Microsoft Prompt Shields i Azure Content Safety z szczegółowymi przykładami w Pythonie
  - **Zaawansowane łagodzenie zagrożeń**: Kompleksowe przykłady implementacji dla:
    - Zapobiegania atakom typu Confused Deputy z PKCE i walidacją zgody użytkownika
    - Zapobiegania przekazywaniu tokenów z walidacją odbiorców i bezpiecznym zarządzaniem tokenami
    - Zapobiegania przejęciu sesji z wykorzystaniem wiązania kryptograficznego i analizy behawioralnej
  - **Integracja bezpieczeństwa w przedsiębiorstwie**: Monitorowanie Azure Application Insights, wykrywanie zagrożeń i bezpieczeństwo łańcucha dostaw
  - **Lista kontrolna wdrożenia**: Jasne rozróżnienie między obowiązkowymi a zalecanymi kontrolami bezpieczeństwa z korzyściami ekosystemu Microsoft

### Jakość dokumentacji i zgodność ze standardami
- **Odwołania do specyfikacji**: Zaktualizowano wszystkie odwołania do aktualnej specyfikacji MCP z 2025-06-18
- **Ekosystem bezpieczeństwa Microsoft**: Ulepszono wskazówki dotyczące integracji w całej dokumentacji bezpieczeństwa
- **Praktyczna implementacja**: Dodano szczegółowe przykłady kodu w .NET, Java i Python z wzorcami dla przedsiębiorstw
- **Organizacja zasobów**: Kompleksowa kategoryzacja oficjalnej dokumentacji, standardów bezpieczeństwa i przewodników implementacji
- **Wizualne wskaźniki**: Wyraźne oznaczenie wymagań obowiązkowych i zalecanych praktyk

#### Podstawowe koncepcje (01-CoreConcepts/) - Kompleksowa modernizacja
- **Aktualizacja wersji protokołu**: Zaktualizowano odniesienia do aktualnej specyfikacji MCP z 2025-06-18 z wersjonowaniem opartym na dacie (format YYYY-MM-DD)
- **Udoskonalenie architektury**: Ulepszone opisy Hostów, Klientów i Serwerów, odzwierciedlające aktualne wzorce architektury MCP
  - Hosty jasno zdefiniowane jako aplikacje AI koordynujące wiele połączeń klientów MCP
  - Klienci opisani jako konektory protokołu utrzymujące relacje jeden-do-jednego z serwerami
  - Serwery ulepszone o scenariusze lokalnego i zdalnego wdrożenia
- **Restrukturyzacja prymitywów**: Kompletny przegląd prymitywów serwera i klienta
  - Prymitywy serwera: Zasoby (źródła danych), Szablony (prompty), Narzędzia (funkcje wykonywalne) z szczegółowymi wyjaśnieniami i przykładami
  - Prymitywy klienta: Próbkowanie (kompletacje LLM), Elicytacja (wejście użytkownika), Logowanie (debugowanie/monitorowanie)
  - Zaktualizowano o aktualne wzorce odkrywania (`*/list`), pobierania (`*/get`) i wykonywania (`*/call`) metod
- **Architektura protokołu**: Wprowadzono model architektury dwuwarstwowej
  - Warstwa danych: Podstawa JSON-RPC 2.0 z zarządzaniem cyklem życia i prymitywami
  - Warstwa transportowa: STDIO (lokalna) i Streamable HTTP z SSE (zdalna) mechanizmy transportowe
- **Ramka bezpieczeństwa**: Kompleksowe zasady bezpieczeństwa, w tym wyraźna zgoda użytkownika, ochrona prywatności danych, bezpieczeństwo wykonywania narzędzi i bezpieczeństwo warstwy transportowej
- **Wzorce komunikacji**: Zaktualizowano wiadomości protokołu, aby pokazać przepływy inicjalizacji, odkrywania, wykonywania i powiadomień
- **Przykłady kodu**: Odświeżono wielojęzyczne przykłady (.NET, Java, Python, JavaScript), aby odzwierciedlały aktualne wzorce MCP SDK

#### Bezpieczeństwo (02-Security/) - Kompleksowa przebudowa bezpieczeństwa  
- **Zgodność ze standardami**: Pełna zgodność z wymaganiami bezpieczeństwa specyfikacji MCP z 2025-06-18
- **Ewolucja autentykacji**: Udokumentowano przejście od niestandardowych serwerów OAuth do delegacji zewnętrznych dostawców tożsamości (Microsoft Entra ID)
- **Analiza zagrożeń specyficznych dla AI**: Rozszerzone omówienie nowoczesnych wektorów ataków AI
  - Szczegółowe scenariusze ataków typu prompt injection z przykładami z rzeczywistego świata
  - Mechanizmy zatruwania narzędzi i wzorce ataków typu "rug pull"
  - Zatruwanie okna kontekstowego i ataki na dezorientację modelu
- **Rozwiązania bezpieczeństwa AI Microsoft**: Kompleksowe omówienie ekosystemu bezpieczeństwa Microsoft
  - AI Prompt Shields z zaawansowanym wykrywaniem, spotlightingiem i technikami delimitacji
  - Wzorce integracji Azure Content Safety
  - GitHub Advanced Security dla ochrony łańcucha dostaw
- **Zaawansowane łagodzenie zagrożeń**: Szczegółowe kontrole bezpieczeństwa dla:
  - Przejęcia sesji z scenariuszami ataków specyficznych dla MCP i wymaganiami kryptograficznego identyfikatora sesji
  - Problemów typu Confused Deputy w scenariuszach proxy MCP z wyraźnymi wymaganiami zgody
  - Wrażliwości przekazywania tokenów z obowiązkowymi kontrolami walidacji
- **Bezpieczeństwo łańcucha dostaw**: Rozszerzone omówienie łańcucha dostaw AI, w tym modele podstawowe, usługi osadzania, dostawców kontekstu i zewnętrzne API
- **Podstawowe bezpieczeństwo**: Ulepszona integracja z wzorcami bezpieczeństwa przedsiębiorstwa, w tym architekturą zero trust i ekosystemem bezpieczeństwa Microsoft
- **Organizacja zasobów**: Skategoryzowane kompleksowe linki do zasobów według typu (Oficjalne dokumenty, Standardy, Badania, Rozwiązania Microsoft, Przewodniki implementacji)

### Ulepszenia jakości dokumentacji
- **Struktura celów edukacyjnych**: Ulepszone cele edukacyjne z konkretnymi, możliwymi do realizacji wynikami
- **Odnośniki krzyżowe**: Dodano linki między powiązanymi tematami bezpieczeństwa i podstawowych koncepcji
- **Aktualne informacje**: Zaktualizowano wszystkie odniesienia do dat i linki do specyfikacji zgodnie z aktualnymi standardami
- **Wskazówki implementacyjne**: Dodano konkretne, możliwe do realizacji wskazówki implementacyjne w całej dokumentacji

## 16 lipca 2025

### README i ulepszenia nawigacji
- Całkowicie przeprojektowano nawigację w README.md
- Zastąpiono tagi `<details>` bardziej dostępnym formatem tabelowym
- Utworzono alternatywne opcje układu w nowym folderze "alternative_layouts"
- Dodano przykłady nawigacji w stylu kart, zakładek i akordeonu
- Zaktualizowano sekcję struktury repozytorium, aby uwzględnić wszystkie najnowsze pliki
- Ulepszono sekcję "Jak korzystać z tego programu nauczania" z jasnymi rekomendacjami
- Zaktualizowano linki do specyfikacji MCP, aby wskazywały poprawne adresy URL
- Dodano sekcję Inżynieria kontekstowa (5.14) do struktury programu nauczania

### Aktualizacje przewodnika nauki
- Całkowicie zrewidowano przewodnik nauki, aby dostosować go do aktualnej struktury repozytorium
- Dodano nowe sekcje dotyczące klientów MCP i narzędzi oraz popularnych serwerów MCP
- Zaktualizowano wizualną mapę programu nauczania, aby dokładnie odzwierciedlała wszystkie tematy
- Ulepszono opisy zaawansowanych tematów, aby objąć wszystkie specjalistyczne obszary
- Zaktualizowano sekcję studiów przypadków, aby odzwierciedlała rzeczywiste przykłady
- Dodano ten kompleksowy dziennik zmian

### Wkład społeczności (06-CommunityContributions/)
- Dodano szczegółowe informacje o serwerach MCP do generowania obrazów
- Dodano kompleksową sekcję dotyczącą korzystania z Claude w VSCode
- Dodano instrukcje konfiguracji i użytkowania klienta terminalowego Cline
- Zaktualizowano sekcję klientów MCP, aby uwzględnić wszystkie popularne opcje klientów
- Ulepszono przykłady wkładów z bardziej precyzyjnymi próbkami kodu

### Zaawansowane tematy (05-AdvancedTopics/)
- Zorganizowano wszystkie foldery specjalistycznych tematów z jednolitą nazwą
- Dodano materiały i przykłady dotyczące inżynierii kontekstowej
- Dodano dokumentację integracji agenta Foundry
- Ulepszono dokumentację integracji bezpieczeństwa Entra ID

## 11 czerwca 2025

### Pierwsze utworzenie
- Wydano pierwszą wersję programu nauczania MCP dla początkujących
- Utworzono podstawową strukturę dla wszystkich 10 głównych sekcji
- Wdrożono wizualną mapę programu nauczania dla nawigacji
- Dodano początkowe projekty przykładowe w wielu językach programowania

### Pierwsze kroki (03-GettingStarted/)
- Utworzono pierwsze przykłady implementacji serwera
- Dodano wskazówki dotyczące rozwoju klienta
- Uwzględniono instrukcje integracji klienta LLM
- Dodano dokumentację integracji z VS Code
- Wdrożono przykłady serwera z Server-Sent Events (SSE)

### Podstawowe koncepcje (01-CoreConcepts/)
- Dodano szczegółowe wyjaśnienie architektury klient-serwer
- Utworzono dokumentację kluczowych komponentów protokołu
- Udokumentowano wzorce wiadomości w MCP

## 23 maja 2025

### Struktura repozytorium
- Zainicjowano repozytorium z podstawową strukturą folderów
- Utworzono pliki README dla każdej głównej sekcji
- Skonfigurowano infrastrukturę tłumaczeń
- Dodano zasoby graficzne i diagramy

### Dokumentacja
- Utworzono początkowy README.md z przeglądem programu nauczania
- Dodano CODE_OF_CONDUCT.md i SECURITY.md
- Skonfigurowano SUPPORT.md z wskazówkami dotyczącymi uzyskiwania pomocy
- Utworzono wstępną strukturę przewodnika nauki

## 15 kwietnia 2025

### Planowanie i ramy
- Wstępne planowanie programu nauczania MCP dla początkujących
- Zdefiniowano cele edukacyjne i grupę docelową
- Nakreślono 10-sekcyjną strukturę programu nauczania
- Opracowano koncepcyjne ramy dla przykładów i studiów przypadków
- Utworzono początkowe prototypy przykładów dla kluczowych koncepcji

---

**Zastrzeżenie**:  
Ten dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dokładamy wszelkich starań, aby tłumaczenie było precyzyjne, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w jego rodzimym języku powinien być uznawany za źródło autorytatywne. W przypadku informacji krytycznych zaleca się skorzystanie z profesjonalnego tłumaczenia przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.