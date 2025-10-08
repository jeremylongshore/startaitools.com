<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "ac2459c0d5cc823922e3d9240a95028c",
  "translation_date": "2025-07-13T19:05:55+00:00",
  "source_file": "03-GettingStarted/03-llm-client/solution/java/README.md",
  "language_code": "ru"
}
-->
# Calculator LLM Client

Java-приложение, демонстрирующее, как использовать LangChain4j для подключения к сервису калькулятора MCP (Model Context Protocol) с интеграцией GitHub Models.

## Требования

- Java 21 или выше  
- Maven 3.6+ (или используйте включённый Maven wrapper)  
- Аккаунт GitHub с доступом к GitHub Models  
- Запущенный сервис калькулятора MCP на `http://localhost:8080`  

## Получение GitHub токена

Это приложение использует GitHub Models, для чего требуется персональный токен доступа GitHub. Следуйте этим шагам, чтобы получить токен:

### 1. Доступ к GitHub Models  
1. Перейдите на [GitHub Models](https://github.com/marketplace/models)  
2. Войдите в свой аккаунт GitHub  
3. Запросите доступ к GitHub Models, если ещё не сделали этого  

### 2. Создание персонального токена доступа  
1. Перейдите в [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)  
2. Нажмите "Generate new token" → "Generate new token (classic)"  
3. Дайте токену понятное имя (например, "MCP Calculator Client")  
4. Установите срок действия по необходимости  
5. Выберите следующие области доступа:  
   - `repo` (если нужен доступ к приватным репозиториям)  
   - `user:email`  
6. Нажмите "Generate token"  
7. **Важно**: Скопируйте токен сразу — после этого он больше не будет отображаться!  

### 3. Установка переменной окружения

#### В Windows (Command Prompt):  
```cmd
set GITHUB_TOKEN=your_github_token_here
```

#### В Windows (PowerShell):  
```powershell
$env:GITHUB_TOKEN="your_github_token_here"
```

#### В macOS/Linux:  
```bash
export GITHUB_TOKEN=your_github_token_here
```

## Настройка и установка

1. **Клонируйте репозиторий или перейдите в директорию проекта**

2. **Установите зависимости**:  
   ```cmd
   mvnw clean install
   ```  
   Или, если Maven установлен глобально:  
   ```cmd
   mvn clean install
   ```

3. **Настройте переменную окружения** (см. раздел "Получение GitHub токена" выше)

4. **Запустите сервис калькулятора MCP**:  
   Убедитесь, что сервис из главы 1 запущен на `http://localhost:8080/sse`. Он должен работать до запуска клиента.

## Запуск приложения

```cmd
mvnw clean package
java -jar target\calculator-llm-client-0.0.1-SNAPSHOT.jar
```

## Что делает приложение

Приложение демонстрирует три основных взаимодействия с сервисом калькулятора:

1. **Сложение**: вычисляет сумму 24.5 и 17.3  
2. **Квадратный корень**: вычисляет квадратный корень из 144  
3. **Помощь**: показывает доступные функции калькулятора  

## Ожидаемый результат

При успешном запуске вы увидите вывод, похожий на:

```
The sum of 24.5 and 17.3 is 41.8.
The square root of 144 is 12.
The calculator service provides the following functions: add, subtract, multiply, divide, sqrt, power...
```

## Устранение неполадок

### Частые проблемы

1. **"GITHUB_TOKEN environment variable not set"**  
   - Убедитесь, что переменная окружения `GITHUB_TOKEN` установлена  
   - Перезапустите терминал/командную строку после установки переменной  

2. **"Connection refused to localhost:8080"**  
   - Проверьте, что сервис калькулятора MCP запущен на порту 8080  
   - Убедитесь, что другой сервис не занимает порт 8080  

3. **"Authentication failed"**  
   - Проверьте, что ваш GitHub токен действителен и имеет нужные права  
   - Убедитесь, что у вас есть доступ к GitHub Models  

4. **Ошибки сборки Maven**  
   - Убедитесь, что используете Java 21 или выше: `java -version`  
   - Попробуйте очистить сборку: `mvnw clean`  

### Отладка

Для включения отладочного логирования добавьте следующий аргумент JVM при запуске:  
```cmd
java -Dlogging.level.dev.langchain4j=DEBUG -jar target\calculator-llm-client-0.0.1-SNAPSHOT.jar
```

## Конфигурация

Приложение настроено на:  
- Использование GitHub Models с моделью `gpt-4.1-nano`  
- Подключение к сервису MCP по адресу `http://localhost:8080/sse`  
- Таймаут запросов 60 секунд  
- Включение логирования запросов и ответов для отладки  

## Зависимости

Основные зависимости проекта:  
- **LangChain4j**: для интеграции ИИ и управления инструментами  
- **LangChain4j MCP**: поддержка Model Context Protocol  
- **LangChain4j GitHub Models**: интеграция с GitHub Models  
- **Spring Boot**: фреймворк приложения и внедрение зависимостей  

## Лицензия

Этот проект лицензирован под Apache License 2.0 — подробности в файле [LICENSE](../../../../../../03-GettingStarted/03-llm-client/solution/java/LICENSE).

**Отказ от ответственности**:  
Этот документ был переведен с помощью сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, просим учитывать, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обращаться к профессиональному переводу, выполненному человеком. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования данного перевода.