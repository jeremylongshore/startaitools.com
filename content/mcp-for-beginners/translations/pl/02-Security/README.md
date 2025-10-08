<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T12:18:52+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "pl"
}
-->
# MCP Security: Kompleksowa Ochrona Systemów AI

[![MCP Security Best Practices](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.pl.png)](https://youtu.be/88No8pw706o)

_(Kliknij obrazek powyżej, aby obejrzeć wideo z tej lekcji)_

Bezpieczeństwo jest kluczowym elementem projektowania systemów AI, dlatego traktujemy je priorytetowo w naszej drugiej sekcji. Jest to zgodne z zasadą Microsoftu **Secure by Design** z [Secure Future Initiative](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Model Context Protocol (MCP) wprowadza potężne nowe możliwości do aplikacji opartych na AI, jednocześnie stawiając przed nami unikalne wyzwania związane z bezpieczeństwem, które wykraczają poza tradycyjne ryzyka związane z oprogramowaniem. Systemy MCP muszą zmierzyć się zarówno z ustalonymi problemami bezpieczeństwa (bezpieczne kodowanie, zasada najmniejszych uprawnień, bezpieczeństwo łańcucha dostaw), jak i nowymi zagrożeniami specyficznymi dla AI, takimi jak wstrzykiwanie poleceń, zatruwanie narzędzi, przejmowanie sesji, ataki na zdezorientowanego pełnomocnika, podatności na przekazywanie tokenów oraz dynamiczne modyfikacje możliwości.

Ta lekcja omawia najważniejsze zagrożenia związane z bezpieczeństwem w implementacjach MCP—w tym uwierzytelnianie, autoryzację, nadmierne uprawnienia, pośrednie wstrzykiwanie poleceń, bezpieczeństwo sesji, problemy z pełnomocnikiem, zarządzanie tokenami oraz podatności łańcucha dostaw. Dowiesz się, jak zastosować praktyczne środki zaradcze i najlepsze praktyki, aby zminimalizować te ryzyka, korzystając z rozwiązań Microsoftu, takich jak Prompt Shields, Azure Content Safety i GitHub Advanced Security, aby wzmocnić wdrożenie MCP.

## Cele nauki

Po ukończeniu tej lekcji będziesz w stanie:

- **Rozpoznać zagrożenia specyficzne dla MCP**: Zidentyfikować unikalne ryzyka bezpieczeństwa w systemach MCP, takie jak wstrzykiwanie poleceń, zatruwanie narzędzi, nadmierne uprawnienia, przejmowanie sesji, problemy z pełnomocnikiem, podatności na przekazywanie tokenów oraz ryzyka łańcucha dostaw
- **Zastosować środki bezpieczeństwa**: Wdrożyć skuteczne środki zaradcze, takie jak solidne uwierzytelnianie, dostęp zgodny z zasadą najmniejszych uprawnień, bezpieczne zarządzanie tokenami, kontrola bezpieczeństwa sesji oraz weryfikacja łańcucha dostaw
- **Wykorzystać rozwiązania Microsoftu w zakresie bezpieczeństwa**: Zrozumieć i wdrożyć Microsoft Prompt Shields, Azure Content Safety oraz GitHub Advanced Security w celu ochrony obciążeń MCP
- **Zweryfikować bezpieczeństwo narzędzi**: Rozpoznać znaczenie walidacji metadanych narzędzi, monitorowania dynamicznych zmian oraz obrony przed pośrednimi atakami wstrzykiwania poleceń
- **Zintegrować najlepsze praktyki**: Połączyć ustalone podstawy bezpieczeństwa (bezpieczne kodowanie, utwardzanie serwerów, zero trust) z kontrolami specyficznymi dla MCP w celu kompleksowej ochrony

# Architektura bezpieczeństwa MCP i środki zaradcze

Nowoczesne implementacje MCP wymagają warstwowego podejścia do bezpieczeństwa, które uwzględnia zarówno tradycyjne zagrożenia związane z oprogramowaniem, jak i te specyficzne dla AI. Szybko rozwijająca się specyfikacja MCP stale doskonali swoje środki bezpieczeństwa, umożliwiając lepszą integrację z architekturami bezpieczeństwa przedsiębiorstw oraz ustalonymi najlepszymi praktykami.

Badania z [Microsoft Digital Defense Report](https://aka.ms/mddr) pokazują, że **98% zgłoszonych naruszeń można by zapobiec dzięki solidnej higienie bezpieczeństwa**. Najskuteczniejsza strategia ochrony łączy podstawowe praktyki bezpieczeństwa z kontrolami specyficznymi dla MCP—sprawdzone środki bezpieczeństwa pozostają najbardziej efektywne w redukcji ogólnego ryzyka.

## Aktualny krajobraz bezpieczeństwa

> **Note:** Informacje te odzwierciedlają standardy bezpieczeństwa MCP na dzień **18 sierpnia 2025**. Specyfikacja MCP szybko się rozwija, a przyszłe implementacje mogą wprowadzić nowe wzorce uwierzytelniania i ulepszone środki zaradcze. Zawsze odwołuj się do aktualnej [Specyfikacji MCP](https://spec.modelcontextprotocol.io/), [repozytorium MCP na GitHub](https://github.com/modelcontextprotocol) oraz [dokumentacji najlepszych praktyk bezpieczeństwa](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) w celu uzyskania najnowszych wskazówek.

### Ewolucja uwierzytelniania MCP

Specyfikacja MCP znacząco ewoluowała w podejściu do uwierzytelniania i autoryzacji:

- **Pierwotne podejście**: Wczesne specyfikacje wymagały od deweloperów implementacji niestandardowych serwerów uwierzytelniania, przy czym serwery MCP działały jako serwery autoryzacji OAuth 2.0, zarządzając bezpośrednio uwierzytelnianiem użytkowników
- **Obecny standard (2025-06-18)**: Zaktualizowana specyfikacja pozwala serwerom MCP delegować uwierzytelnianie zewnętrznym dostawcom tożsamości (takim jak Microsoft Entra ID), poprawiając postawę bezpieczeństwa i redukując złożoność implementacji
- **Transport Layer Security**: Ulepszone wsparcie dla bezpiecznych mechanizmów transportowych z odpowiednimi wzorcami uwierzytelniania zarówno dla lokalnych (STDIO), jak i zdalnych (Streamable HTTP) połączeń

## Bezpieczeństwo uwierzytelniania i autoryzacji

### Aktualne wyzwania bezpieczeństwa

Nowoczesne implementacje MCP napotykają kilka wyzwań związanych z uwierzytelnianiem i autoryzacją:

### Ryzyka i wektory zagrożeń

- **Nieprawidłowa logika autoryzacji**: Wadliwa implementacja autoryzacji w serwerach MCP może ujawnić wrażliwe dane i nieprawidłowo zastosować kontrolę dostępu
- **Kompromitacja tokenów OAuth**: Kradzież tokenów lokalnego serwera MCP umożliwia atakującym podszywanie się pod serwery i dostęp do usług downstream
- **Podatności na przekazywanie tokenów**: Nieprawidłowe zarządzanie tokenami tworzy obejścia kontroli bezpieczeństwa i luki w odpowiedzialności
- **Nadmierne uprawnienia**: Serwery MCP z nadmiernymi uprawnieniami naruszają zasadę najmniejszych uprawnień i zwiększają powierzchnię ataku

#### Przekazywanie tokenów: Krytyczny antywzorzec

**Przekazywanie tokenów jest wyraźnie zabronione** w obecnej specyfikacji autoryzacji MCP ze względu na poważne implikacje bezpieczeństwa:

##### Obejście kontroli bezpieczeństwa
- Serwery MCP i API downstream implementują kluczowe kontrole bezpieczeństwa (ograniczanie szybkości, walidacja żądań, monitorowanie ruchu), które zależą od właściwej walidacji tokenów
- Bezpośrednie użycie tokenów klienta do API omija te istotne zabezpieczenia, podważając architekturę bezpieczeństwa

##### Wyzwania związane z odpowiedzialnością i audytem  
- Serwery MCP nie mogą odróżnić klientów używających tokenów wydanych upstream, co łamie ścieżki audytu
- Logi serwerów zasobów downstream pokazują mylące źródła żądań zamiast rzeczywistych pośredników serwera MCP
- Dochodzenia w sprawie incydentów i audyty zgodności stają się znacznie trudniejsze

##### Ryzyka wycieku danych
- Niezweryfikowane roszczenia tokenów umożliwiają złośliwym aktorom ze skradzionymi tokenami używanie serwerów MCP jako proxy do wycieku danych
- Naruszenia granic zaufania pozwalają na nieautoryzowane wzorce dostępu, które omijają zamierzone kontrole bezpieczeństwa

##### Wektory ataków wielousługowych
- Kompromitowane tokeny akceptowane przez wiele usług umożliwiają ruch lateralny w połączonych systemach
- Założenia zaufania między usługami mogą zostać naruszone, gdy nie można zweryfikować pochodzenia tokenów

### Środki bezpieczeństwa i działania zaradcze

**Krytyczne wymagania bezpieczeństwa:**

> **MANDATORY**: Serwery MCP **NIE MOGĄ** akceptować żadnych tokenów, które nie zostały wyraźnie wydane dla serwera MCP

#### Kontrole uwierzytelniania i autoryzacji

- **Rygorystyczna weryfikacja autoryzacji**: Przeprowadź kompleksowe audyty logiki autoryzacji serwera MCP, aby upewnić się, że tylko zamierzeni użytkownicy i klienci mają dostęp do wrażliwych zasobów
  - **Przewodnik implementacji**: [Azure API Management jako brama uwierzytelniania dla serwerów MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Integracja tożsamości**: [Używanie Microsoft Entra ID do uwierzytelniania serwera MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Bezpieczne zarządzanie tokenami**: Wdrożenie [najlepszych praktyk Microsoftu dotyczących walidacji tokenów i cyklu życia](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Walidacja roszczeń odbiorców tokenów zgodnych z tożsamością serwera MCP
  - Wdrożenie odpowiednich zasad rotacji i wygaśnięcia tokenów
  - Zapobieganie atakom powtórzeniowym tokenów i nieautoryzowanemu użyciu

- **Chronione przechowywanie tokenów**: Bezpieczne przechowywanie tokenów z szyfrowaniem zarówno w spoczynku, jak i w tranzycie
  - **Najlepsze praktyki**: [Wytyczne dotyczące bezpiecznego przechowywania i szyfrowania tokenów](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementacja kontroli dostępu

- **Zasada najmniejszych uprawnień**: Przyznaj serwerom MCP tylko minimalne uprawnienia wymagane do zamierzonej funkcjonalności
  - Regularne przeglądy i aktualizacje uprawnień, aby zapobiec ich nadmiernemu rozrostowi
  - **Dokumentacja Microsoftu**: [Bezpieczny dostęp zgodny z zasadą najmniejszych uprawnień](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Kontrola dostępu oparta na rolach (RBAC)**: Wdrożenie precyzyjnych przypisań ról
  - Ograniczenie ról do konkretnych zasobów i działań
  - Unikanie szerokich lub niepotrzebnych uprawnień, które zwiększają powierzchnię ataku

- **Ciągłe monitorowanie uprawnień**: Wdrożenie bieżącego audytu i monitorowania dostępu
  - Monitorowanie wzorców użycia uprawnień pod kątem anomalii
  - Szybkie usuwanie nadmiernych lub nieużywanych uprawnień

## Zagrożenia specyficzne dla AI

### Ataki wstrzykiwania poleceń i manipulacji narzędziami

Nowoczesne implementacje MCP napotykają zaawansowane wektory ataków specyficzne dla AI, których tradycyjne środki bezpieczeństwa nie są w stanie w pełni rozwiązać:

#### **Pośrednie wstrzykiwanie poleceń (Cross-Domain Prompt Injection)**

**Pośrednie wstrzykiwanie poleceń** stanowi jedno z najpoważniejszych zagrożeń dla systemów AI obsługiwanych przez MCP. Atakujący osadzają złośliwe instrukcje w zewnętrznych treściach—dokumentach, stronach internetowych, e-mailach lub źródłach danych—które systemy AI następnie przetwarzają jako prawidłowe polecenia.

**Scenariusze ataków:**
- **Wstrzykiwanie oparte na dokumentach**: Złośliwe instrukcje ukryte w przetwarzanych dokumentach, które wywołują niezamierzone działania AI
- **Eksploatacja treści internetowych**: Zainfekowane strony internetowe zawierające osadzone polecenia manipulujące zachowaniem AI podczas ich skanowania
- **Ataki oparte na e-mailach**: Złośliwe polecenia w e-mailach powodujące wycieki informacji lub wykonywanie nieautoryzowanych działań przez asystentów AI
- **Zanieczyszczenie źródeł danych**: Zainfekowane bazy danych lub API dostarczające zanieczyszczone treści do systemów AI

**Wpływ w rzeczywistości**: Te ataki mogą prowadzić do wycieku danych, naruszenia prywatności, generowania szkodliwych treści oraz manipulacji interakcjami użytkownika. Szczegółową analizę znajdziesz w [Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Prompt Injection Attack Diagram](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.pl.png)

#### **Ataki zatruwania narzędzi**

**Zatruwanie narzędzi** dotyczy metadanych definiujących narzędzia MCP, wykorzystując sposób, w jaki LLM interpretują opisy narzędzi i parametry do podejmowania decyzji o ich wykonaniu.

**Mechanizmy ataku:**
- **Manipulacja metadanymi**: Atakujący wstrzykują złośliwe instrukcje do opisów narzędzi, definicji parametrów lub przykładów użycia
- **Niewidoczne instrukcje**: Ukryte polecenia w metadanych narzędzi, które są przetwarzane przez modele AI, ale niewidoczne dla użytkowników
- **Dynamiczna modyfikacja narzędzi ("Rug Pulls")**: Narzędzia zatwierdzone przez użytkowników są później modyfikowane, aby wykonywać złośliwe działania bez wiedzy użytkownika
- **Wstrzykiwanie parametrów**: Złośliwe treści osadzone w schematach parametrów narzędzi wpływające na zachowanie modelu

**Ryzyka związane z serwerami hostowanymi**: Zdalne serwery MCP stwarzają podwyższone ryzyko, ponieważ definicje narzędzi mogą być aktualizowane po ich początkowym zatwierdzeniu przez użytkownika, tworząc scenariusze, w których wcześniej bezpieczne narzędzia stają się złośliwe. Szczegółową analizę znajdziesz w [Tool Poisoning Attacks (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Tool Injection Attack Diagram](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.pl.png)

#### **Dodatkowe wektory ataków AI**

- **Cross-Domain Prompt Injection (XPIA)**: Zaawansowane ataki wykorzystujące treści z wielu domen do obejścia kontroli bezpieczeństwa
- **Dynamiczna modyfikacja możliwości**: Zmiany w czasie rzeczywistym możliwości narzędzi, które umykają początkowym ocenom bezpieczeństwa
- **Zanieczyszczenie okna kontekstowego**: Ataki manipulujące dużymi oknami kontekstowymi w celu ukrycia złośliwych instrukcji
- **Ataki na zdezorientowany model**: Wykorzystywanie ograniczeń modelu do tworzenia nieprzewidywalnych lub niebezpiecznych zachowań

### Wpływ ryzyk bezpieczeństwa AI

**Konsekwencje o wysokim wpływie:**
- **Wycieki danych**: Nieautoryzowany dostęp i kradzież wrażliwych danych przedsiębiorstwa lub osobistych
- **Naruszenia prywatności**: Ujawnienie danych osobowych (PII) i poufnych informacji biznesowych  
- **Manipulacja systemem**: Niezamierzone modyfikacje krytycznych systemów i przepływów pracy
- **Kradzież poświadczeń**: Kompromitacja tokenów uwierzytelniających i poświadczeń usług
- **Ruch lateralny**: Wykorzystanie skompromitowanych system
- **Generowanie Bezpiecznych Sesji**: Używaj kryptograficznie bezpiecznych, niedeterministycznych identyfikatorów sesji generowanych za pomocą bezpiecznych generatorów liczb losowych  
- **Powiązanie z Użytkownikiem**: Powiąż identyfikatory sesji z informacjami specyficznymi dla użytkownika, używając formatów takich jak `<user_id>:<session_id>`, aby zapobiec nadużyciom sesji między użytkownikami  
- **Zarządzanie Cyklami Życia Sesji**: Wprowadź odpowiednie mechanizmy wygaśnięcia, rotacji i unieważnienia sesji, aby ograniczyć okna podatności  
- **Bezpieczeństwo Transportu**: Obowiązkowe użycie HTTPS dla całej komunikacji w celu zapobiegania przechwytywaniu identyfikatorów sesji  

### Problem Zdezorientowanego Pełnomocnika  

**Problem zdezorientowanego pełnomocnika** występuje, gdy serwery MCP działają jako proxy uwierzytelniające między klientami a usługami zewnętrznymi, tworząc możliwości obejścia autoryzacji poprzez wykorzystanie statycznych identyfikatorów klienta.

#### **Mechanika Ataku i Ryzyka**

- **Omijanie Zgody na Podstawie Ciasteczek**: Poprzednie uwierzytelnienie użytkownika tworzy ciasteczka zgody, które atakujący wykorzystują za pomocą złośliwych żądań autoryzacji z odpowiednio spreparowanymi URI przekierowania  
- **Kradzież Kodów Autoryzacyjnych**: Istniejące ciasteczka zgody mogą powodować pomijanie ekranów zgody przez serwery autoryzacyjne, przekierowując kody do punktów kontrolowanych przez atakujących  
- **Nieautoryzowany Dostęp do API**: Skradzione kody autoryzacyjne umożliwiają wymianę tokenów i podszywanie się pod użytkowników bez ich wyraźnej zgody  

#### **Strategie Ograniczania Ryzyka**

**Obowiązkowe Kontrole:**  
- **Wymóg Wyraźnej Zgody**: Serwery proxy MCP używające statycznych identyfikatorów klienta **MUSZĄ** uzyskać zgodę użytkownika dla każdego dynamicznie zarejestrowanego klienta  
- **Implementacja Bezpieczeństwa OAuth 2.1**: Stosuj aktualne najlepsze praktyki bezpieczeństwa OAuth, w tym PKCE (Proof Key for Code Exchange) dla wszystkich żądań autoryzacyjnych  
- **Ścisła Walidacja Klientów**: Wprowadź rygorystyczną walidację URI przekierowania i identyfikatorów klientów, aby zapobiec ich wykorzystaniu  

### Luki w Przekazywaniu Tokenów  

**Przekazywanie tokenów** to wyraźny antywzorzec, w którym serwery MCP akceptują tokeny klientów bez odpowiedniej walidacji i przekazują je do API downstream, naruszając specyfikacje autoryzacji MCP.

#### **Implikacje Bezpieczeństwa**

- **Omijanie Kontroli**: Bezpośrednie użycie tokenów klienta w API omija kluczowe mechanizmy ograniczania szybkości, walidacji i monitorowania  
- **Zafałszowanie Ścieżki Audytu**: Tokeny wydane upstream uniemożliwiają identyfikację klienta, utrudniając dochodzenia w przypadku incydentów  
- **Eksfiltracja Danych przez Proxy**: Niewalidowane tokeny umożliwiają złośliwym aktorom użycie serwerów jako proxy do nieautoryzowanego dostępu do danych  
- **Naruszenie Granic Zaufania**: Założenia dotyczące zaufania usług downstream mogą zostać naruszone, gdy nie można zweryfikować pochodzenia tokenów  
- **Rozszerzenie Ataków na Wielu Usługach**: Skompromitowane tokeny akceptowane przez wiele usług umożliwiają ruch lateralny  

#### **Wymagane Kontrole Bezpieczeństwa**

**Wymagania Niepodlegające Negocjacjom:**  
- **Walidacja Tokenów**: Serwery MCP **NIE MOGĄ** akceptować tokenów, które nie zostały wyraźnie wydane dla serwera MCP  
- **Weryfikacja Odbiorcy**: Zawsze sprawdzaj, czy roszczenia odbiorcy tokenów odpowiadają tożsamości serwera MCP  
- **Prawidłowy Cykl Życia Tokenów**: Wprowadź tokeny dostępu o krótkim okresie ważności z bezpiecznymi praktykami rotacji  

## Bezpieczeństwo Łańcucha Dostaw dla Systemów AI  

Bezpieczeństwo łańcucha dostaw ewoluowało poza tradycyjne zależności oprogramowania, obejmując cały ekosystem AI. Współczesne implementacje MCP muszą rygorystycznie weryfikować i monitorować wszystkie komponenty związane z AI, ponieważ każdy z nich może wprowadzać potencjalne podatności, które mogą zagrozić integralności systemu.

### Rozszerzone Komponenty Łańcucha Dostaw AI  

**Tradycyjne Zależności Oprogramowania:**  
- Biblioteki open-source i frameworki  
- Obrazy kontenerów i systemy bazowe  
- Narzędzia deweloperskie i potoki budowania  
- Komponenty infrastruktury i usługi  

**Elementy Specyficzne dla AI:**  
- **Modele Podstawowe**: Wstępnie wytrenowane modele od różnych dostawców wymagające weryfikacji pochodzenia  
- **Usługi Embedding**: Zewnętrzne usługi wektoryzacji i wyszukiwania semantycznego  
- **Dostawcy Kontekstu**: Źródła danych, bazy wiedzy i repozytoria dokumentów  
- **API Zewnętrzne**: Zewnętrzne usługi AI, potoki ML i punkty końcowe przetwarzania danych  
- **Artefakty Modeli**: Wagi, konfiguracje i warianty modeli dostosowanych  
- **Źródła Danych Treningowych**: Zbiory danych używane do trenowania i dostrajania modeli  

### Kompleksowa Strategia Bezpieczeństwa Łańcucha Dostaw  

#### **Weryfikacja Komponentów i Zaufanie**  
- **Walidacja Pochodzenia**: Zweryfikuj pochodzenie, licencjonowanie i integralność wszystkich komponentów AI przed ich integracją  
- **Ocena Bezpieczeństwa**: Przeprowadzaj skanowanie podatności i przeglądy bezpieczeństwa modeli, źródeł danych i usług AI  
- **Analiza Reputacji**: Oceń historię bezpieczeństwa i praktyki dostawców usług AI  
- **Weryfikacja Zgodności**: Upewnij się, że wszystkie komponenty spełniają wymagania bezpieczeństwa i regulacyjne organizacji  

#### **Bezpieczne Potoki Wdrożeniowe**  
- **Automatyczne Bezpieczeństwo CI/CD**: Zintegruj skanowanie bezpieczeństwa w całych automatycznych potokach wdrożeniowych  
- **Integralność Artefaktów**: Wprowadź kryptograficzną weryfikację wszystkich wdrażanych artefaktów (kod, modele, konfiguracje)  
- **Wdrożenie Etapowe**: Używaj progresywnych strategii wdrożeniowych z walidacją bezpieczeństwa na każdym etapie  
- **Zaufane Repozytoria Artefaktów**: Wdrażaj tylko z zweryfikowanych, bezpiecznych rejestrów i repozytoriów artefaktów  

#### **Ciągłe Monitorowanie i Reakcja**  
- **Skanowanie Zależności**: Ciągłe monitorowanie podatności wszystkich zależności oprogramowania i komponentów AI  
- **Monitorowanie Modeli**: Stała ocena zachowania modeli, dryfu wydajności i anomalii bezpieczeństwa  
- **Śledzenie Zdrowia Usług**: Monitorowanie zewnętrznych usług AI pod kątem dostępności, incydentów bezpieczeństwa i zmian polityki  
- **Integracja Wywiadu Zagrożeń**: Włączenie kanałów zagrożeń specyficznych dla bezpieczeństwa AI i ML  

#### **Kontrola Dostępu i Zasada Najmniejszych Uprawnień**  
- **Uprawnienia na Poziomie Komponentów**: Ogranicz dostęp do modeli, danych i usług na podstawie konieczności biznesowej  
- **Zarządzanie Kontami Usługowymi**: Wprowadź dedykowane konta usługowe z minimalnymi wymaganymi uprawnieniami  
- **Segmentacja Sieci**: Izoluj komponenty AI i ogranicz dostęp sieciowy między usługami  
- **Kontrole Bramki API**: Używaj scentralizowanych bramek API do kontrolowania i monitorowania dostępu do zewnętrznych usług AI  

#### **Reakcja na Incydenty i Odzyskiwanie**  
- **Procedury Szybkiej Reakcji**: Ustanowione procesy łatania lub wymiany skompromitowanych komponentów AI  
- **Rotacja Poświadczeń**: Zautomatyzowane systemy rotacji tajemnic, kluczy API i poświadczeń usługowych  
- **Możliwości Wycofania**: Możliwość szybkiego powrotu do poprzednich, znanych dobrych wersji komponentów AI  
- **Odzyskiwanie po Naruszeniu Łańcucha Dostaw**: Specyficzne procedury reagowania na kompromitacje usług AI upstream  

### Narzędzia Bezpieczeństwa Microsoft i Integracja  

**GitHub Advanced Security** zapewnia kompleksową ochronę łańcucha dostaw, w tym:  
- **Skanowanie Tajemnic**: Automatyczne wykrywanie poświadczeń, kluczy API i tokenów w repozytoriach  
- **Skanowanie Zależności**: Ocena podatności dla zależności open-source i bibliotek  
- **Analiza CodeQL**: Statyczna analiza kodu pod kątem podatności bezpieczeństwa i problemów z kodowaniem  
- **Wgląd w Łańcuch Dostaw**: Widoczność zdrowia i statusu bezpieczeństwa zależności  

**Integracja Azure DevOps i Azure Repos:**  
- Bezproblemowa integracja skanowania bezpieczeństwa w platformach deweloperskich Microsoft  
- Automatyczne kontrole bezpieczeństwa w Azure Pipelines dla obciążeń AI  
- Egzekwowanie polityk dla bezpiecznego wdrażania komponentów AI  

**Praktyki Wewnętrzne Microsoft:**  
Microsoft wdraża rozległe praktyki bezpieczeństwa łańcucha dostaw we wszystkich produktach. Dowiedz się więcej o sprawdzonych podejściach w [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  

## Najlepsze Praktyki Bezpieczeństwa Podstawowego  

Implementacje MCP dziedziczą i rozwijają istniejącą postawę bezpieczeństwa organizacji. Wzmocnienie podstawowych praktyk bezpieczeństwa znacząco zwiększa ogólne bezpieczeństwo systemów AI i wdrożeń MCP.  

### Podstawowe Zasady Bezpieczeństwa  

#### **Praktyki Bezpiecznego Rozwoju**  
- **Zgodność z OWASP**: Chroń przed [OWASP Top 10](https://owasp.org/www-project-top-ten/) podatnościami aplikacji webowych  
- **Ochrona Specyficzna dla AI**: Wprowadź kontrole dla [OWASP Top 10 dla LLM](https://genai.owasp.org/download/43299/?tmstv=1731900559)  
- **Bezpieczne Zarządzanie Tajemnicami**: Używaj dedykowanych skarbców do przechowywania tokenów, kluczy API i wrażliwych danych konfiguracyjnych  
- **Szyfrowanie End-to-End**: Wprowadź bezpieczną komunikację między wszystkimi komponentami aplikacji i przepływami danych  
- **Walidacja Wejścia**: Rygorystyczna walidacja wszystkich danych wejściowych użytkownika, parametrów API i źródeł danych  

#### **Utwierdzenie Infrastruktury**  
- **Uwierzytelnianie Wieloskładnikowe**: Obowiązkowe MFA dla wszystkich kont administracyjnych i usługowych  
- **Zarządzanie Łatkami**: Zautomatyzowane, terminowe łatanie systemów operacyjnych, frameworków i zależności  
- **Integracja Dostawcy Tożsamości**: Scentralizowane zarządzanie tożsamością za pomocą dostawców tożsamości przedsiębiorstwa (Microsoft Entra ID, Active Directory)  
- **Segmentacja Sieci**: Logiczna izolacja komponentów MCP w celu ograniczenia potencjału ruchu lateralnego  
- **Zasada Najmniejszych Uprawnień**: Minimalne wymagane uprawnienia dla wszystkich komponentów systemu i kont  

#### **Monitorowanie Bezpieczeństwa i Wykrywanie**  
- **Kompleksowe Logowanie**: Szczegółowe logowanie aktywności aplikacji AI, w tym interakcji klient-serwer MCP  
- **Integracja SIEM**: Scentralizowane zarządzanie informacjami i zdarzeniami bezpieczeństwa w celu wykrywania anomalii  
- **Analiza Behawioralna**: Monitorowanie oparte na AI w celu wykrywania nietypowych wzorców w zachowaniu systemu i użytkowników  
- **Wywiad Zagrożeń**: Integracja zewnętrznych kanałów zagrożeń i wskaźników kompromitacji (IOC)  
- **Reakcja na Incydenty**: Dobrze zdefiniowane procedury wykrywania, reagowania i odzyskiwania po incydentach bezpieczeństwa  

#### **Architektura Zero Trust**  
- **Nigdy Nie Ufaj, Zawsze Weryfikuj**: Ciągła weryfikacja użytkowników, urządzeń i połączeń sieciowych  
- **Mikrosegmentacja**: Granularne kontrole sieciowe izolujące poszczególne obciążenia i usługi  
- **Bezpieczeństwo Oparte na Tożsamości**: Polityki bezpieczeństwa oparte na zweryfikowanych tożsamościach zamiast lokalizacji sieciowej  
- **Ciągła Ocena Ryzyka**: Dynamiczna ocena postawy bezpieczeństwa na podstawie bieżącego kontekstu i zachowania  
- **Dostęp Warunkowy**: Kontrole dostępu dostosowujące się na podstawie czynników ryzyka, lokalizacji i zaufania urządzenia  

### Wzorce Integracji Przedsiębiorstwa  

#### **Integracja Ekosystemu Bezpieczeństwa Microsoft**  
- **Microsoft Defender for Cloud**: Kompleksowe zarządzanie postawą bezpieczeństwa w chmurze  
- **Azure Sentinel**: Natywne dla chmury SIEM i SOAR dla ochrony obciążeń AI  
- **Microsoft Entra ID**: Zarządzanie tożsamością i dostępem przedsiębiorstwa z politykami dostępu warunkowego  
- **Azure Key Vault**: Scentralizowane zarządzanie tajemnicami z wsparciem modułu bezpieczeństwa sprzętowego (HSM)  
- **Microsoft Purview**: Zarządzanie danymi i zgodność dla źródeł danych AI i przepływów pracy  

#### **Zgodność i Zarządzanie**  
- **Dostosowanie Regulacyjne**: Upewnij się, że implementacje MCP spełniają wymagania zgodności specyficzne dla branży (GDPR, HIPAA, SOC 2)  
- **Klasyfikacja Danych**: Właściwa kategoryzacja i obsługa wrażliwych danych przetwarzanych przez systemy AI  
- **Ścieżki Audytu**: Kompleksowe logowanie dla zgodności regulacyjnej i dochodzeń kryminalistycznych  
- **Kontrole Prywatności**: Wprowadzenie zasad prywatności w projektowaniu architektury systemów AI  
- **Zarządzanie Zmianami**: Formalne procesy przeglądów bezpieczeństwa dla modyfikacji systemów AI  

Te podstawowe praktyki tworzą solidną bazę bezpieczeństwa, która zwiększa skuteczność specyficznych dla MCP kontroli bezpieczeństwa i zapewnia kompleksową ochronę dla aplikacji opartych na AI.  

## Kluczowe Wnioski Bezpieczeństwa  

- **Warstwowe Podejście do Bezpieczeństwa**: Połącz podstawowe praktyki bezpieczeństwa (bezpieczne kodowanie, zasada najmniejszych uprawnień, weryfikacja łańcucha dostaw, ciągłe monitorowanie) z kontrolami specyficznymi dla AI dla kompleksowej ochrony  

- **Specyficzny Krajobraz Zagrożeń AI**: Systemy MCP napotykają unikalne ryzyka, takie jak wstrzykiwanie poleceń, zatruwanie narzędzi, przechwytywanie sesji, problemy zdezorientowanego pełnomocnika, luki w przekazywaniu tokenów i nadmierne uprawnienia, które wymagają specjalistycznych działań ograniczających  

- **Doskonałość w Uwierzytelnianiu i Autoryzacji**: Wprowadź solidne uwierzytelnianie za pomocą zewnętrznych dostawców tożsamości (Microsoft Entra ID), egzekwuj prawidłową walidację tokenów i nigdy nie akceptuj tokenów, które nie zostały wyraźnie wydane dla Twojego serwera MCP  

- **Zapobieganie Atakom na AI**: Wdroż Microsoft Prompt Shields i Azure Content Safety, aby bronić się przed pośrednim w
### **Rozwiązania zabezpieczeń Microsoft**
- [Dokumentacja Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Usługa Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Zabezpieczenia Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Najlepsze praktyki zarządzania tokenami w Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Zaawansowane zabezpieczenia GitHub](https://github.com/security/advanced-security)

### **Przewodniki wdrożeniowe i samouczki**
- [Azure API Management jako brama uwierzytelniania MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Uwierzytelnianie Microsoft Entra ID z serwerami MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Bezpieczne przechowywanie tokenów i ich szyfrowanie (wideo)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps i bezpieczeństwo łańcucha dostaw**
- [Zabezpieczenia Azure DevOps](https://azure.microsoft.com/products/devops)
- [Zabezpieczenia Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [Podróż Microsoft w kierunku zabezpieczenia łańcucha dostaw](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Dodatkowa dokumentacja dotycząca bezpieczeństwa**

Aby uzyskać kompleksowe wskazówki dotyczące bezpieczeństwa, zapoznaj się z poniższymi specjalistycznymi dokumentami:

- **[Najlepsze praktyki bezpieczeństwa MCP 2025](./mcp-security-best-practices-2025.md)** - Kompletny zestaw najlepszych praktyk bezpieczeństwa dla wdrożeń MCP  
- **[Wdrożenie Azure Content Safety](./azure-content-safety-implementation.md)** - Praktyczne przykłady integracji Azure Content Safety  
- **[Kontrole bezpieczeństwa MCP 2025](./mcp-security-controls-2025.md)** - Najnowsze techniki i kontrole bezpieczeństwa dla wdrożeń MCP  
- **[Szybki przewodnik po najlepszych praktykach MCP](./mcp-best-practices.md)** - Przewodnik referencyjny po kluczowych praktykach bezpieczeństwa MCP  

---

## Co dalej

Dalej: [Rozdział 3: Pierwsze kroki](../03-GettingStarted/README.md)

**Zastrzeżenie**:  
Ten dokument został przetłumaczony za pomocą usługi tłumaczeniowej AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dokładamy wszelkich starań, aby zapewnić dokładność, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w jego rodzimym języku powinien być uznawany za wiarygodne źródło. W przypadku informacji krytycznych zaleca się skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z korzystania z tego tłumaczenia.