<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "acd4010e430da00946a154f62847a169",
  "translation_date": "2025-07-13T21:07:50+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/java/README.md",
  "language_code": "ru"
}
-->
# Демонстрация HTTP-стриминга калькулятора

Этот проект демонстрирует HTTP-стриминг с использованием Server-Sent Events (SSE) на базе Spring Boot WebFlux. В него входят два приложения:

- **Calculator Server**: реактивный веб-сервис, который выполняет вычисления и передаёт результаты через SSE
- **Calculator Client**: клиентское приложение, которое потребляет стриминговый эндпоинт

## Требования

- Java 17 или выше
- Maven 3.6 или выше

## Структура проекта

```
java/
├── calculator-server/     # Spring Boot server with SSE endpoint
│   ├── src/main/java/com/example/calculatorserver/
│   │   ├── CalculatorServerApplication.java
│   │   └── CalculatorController.java
│   └── pom.xml
├── calculator-client/     # Spring Boot client application
│   ├── src/main/java/com/example/calculatorclient/
│   │   └── CalculatorClientApplication.java
│   └── pom.xml
└── README.md
```

## Как это работает

1. **Calculator Server** предоставляет эндпоинт `/calculate`, который:
   - Принимает параметры запроса: `a` (число), `b` (число), `op` (операция)
   - Поддерживаемые операции: `add`, `sub`, `mul`, `div`
   - Возвращает Server-Sent Events с прогрессом вычисления и результатом

2. **Calculator Client** подключается к серверу и:
   - Отправляет запрос на вычисление `7 * 5`
   - Обрабатывает стриминговый ответ
   - Выводит каждое событие в консоль

## Запуск приложений

### Вариант 1: Использование Maven (рекомендуется)

#### 1. Запуск Calculator Server

Откройте терминал и перейдите в директорию сервера:

```bash
cd calculator-server
mvn clean package
mvn spring-boot:run
```

Сервер запустится по адресу `http://localhost:8080`

Вы увидите вывод примерно такого вида:
```
Started CalculatorServerApplication in X.XXX seconds
Netty started on port 8080 (http)
```

#### 2. Запуск Calculator Client

Откройте **новый терминал** и перейдите в директорию клиента:

```bash
cd calculator-client
mvn clean package
mvn spring-boot:run
```

Клиент подключится к серверу, выполнит вычисление и отобразит результаты в режиме стриминга.

### Вариант 2: Запуск напрямую через Java

#### 1. Скомпилируйте и запустите сервер:

```bash
cd calculator-server
mvn clean package
java -jar target/calculator-server-0.0.1-SNAPSHOT.jar
```

#### 2. Скомпилируйте и запустите клиент:

```bash
cd calculator-client
mvn clean package
java -jar target/calculator-client-0.0.1-SNAPSHOT.jar
```

## Ручное тестирование сервера

Вы также можете протестировать сервер через браузер или curl:

### Через браузер:
Перейдите по адресу: `http://localhost:8080/calculate?a=10&b=5&op=add`

### Через curl:
```bash
curl "http://localhost:8080/calculate?a=10&b=5&op=add" -H "Accept: text/event-stream"
```

## Ожидаемый вывод

При запуске клиента вы должны увидеть стриминговый вывод, похожий на:

```
event:info
data:Calculating: 7.0 mul 5.0

event:result
data:35.0
```

## Поддерживаемые операции

- `add` — сложение (a + b)
- `sub` — вычитание (a - b)
- `mul` — умножение (a * b)
- `div` — деление (a / b, возвращает NaN, если b = 0)

## Справка по API

### GET /calculate

**Параметры:**
- `a` (обязательный): первое число (double)
- `b` (обязательный): второе число (double)
- `op` (обязательный): операция (`add`, `sub`, `mul`, `div`)

**Ответ:**
- Content-Type: `text/event-stream`
- Возвращает Server-Sent Events с прогрессом вычисления и результатом

**Пример запроса:**
```
GET /calculate?a=7&b=5&op=mul HTTP/1.1
Host: localhost:8080
Accept: text/event-stream
```

**Пример ответа:**
```
event: info
data: Calculating: 7.0 mul 5.0

event: result
data: 35.0
```

## Устранение неполадок

### Частые проблемы

1. **Порт 8080 уже занят**
   - Остановите другие приложения, использующие порт 8080
   - Или измените порт сервера в `calculator-server/src/main/resources/application.yml`

2. **Отказ в подключении**
   - Убедитесь, что сервер запущен перед запуском клиента
   - Проверьте, что сервер успешно стартовал на порту 8080

3. **Проблемы с именами параметров**
   - В проекте настроена компиляция Maven с флагом `-parameters`
   - Если возникают проблемы с привязкой параметров, убедитесь, что проект собран с этой настройкой

### Остановка приложений

- Нажмите `Ctrl+C` в терминале, где запущено приложение
- Или используйте `mvn spring-boot:stop`, если приложение запущено в фоне

## Технологический стек

- **Spring Boot 3.3.1** — фреймворк приложения
- **Spring WebFlux** — реактивный веб-фреймворк
- **Project Reactor** — библиотека реактивных потоков
- **Netty** — сервер с неблокирующим вводом-выводом
- **Maven** — инструмент сборки
- **Java 17+** — язык программирования

## Следующие шаги

Попробуйте изменить код, чтобы:
- Добавить больше математических операций
- Реализовать обработку ошибок для некорректных операций
- Добавить логирование запросов и ответов
- Внедрить аутентификацию
- Написать модульные тесты

**Отказ от ответственности**:  
Этот документ был переведен с помощью сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, просим учитывать, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обращаться к профессиональному переводу, выполненному человеком. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования данного перевода.