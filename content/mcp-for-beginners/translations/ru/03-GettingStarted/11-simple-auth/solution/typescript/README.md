<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3880d89fa60abc699e1a17a82ae514ef",
  "translation_date": "2025-10-07T01:20:22+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/typescript/README.md",
  "language_code": "ru"
}
-->
# Запуск примера

## Установка зависимостей

```sh
npm install
```

## Сборка

```sh
npm run build
```

## Генерация токенов

```sh
npm run generate
```

Это создаст токен в файле *.env*. Клиент будет считывать данные из этого файла.

## Запуск кода

Запустите сервер с помощью:

```sh
npm start
```

Запустите клиент в отдельном терминале с помощью:

```sh
npm run client
```

В терминале сервера вы должны увидеть вывод, похожий на:

```text
User exists
User has required scopes
Middleware executed
```

а в терминале клиента вы должны увидеть вывод, похожий на:

```text
Connected to MCP server with session ID: c1e50d7b-acff-4f11-8f96-5ae490ca1eaa
Available tools: { tools: [ { name: 'process-files', inputSchema: [Object] } ] }
Client disconnected.
Exiting...
```

### Изменение параметров

Давайте убедимся, что мы понимаем области действия. Найдите файл *server.ts* и этот код:

```typescript
 if(!hasScopes(token, ["User.Read"])){
        res.status(403).send('Forbidden - insufficient scopes');
    }
```

Здесь указано, что переданный токен должен иметь область "User.Read". Давайте изменим это на "User.Write". Теперь выполните `npm run build` и перезапустите сервер с помощью `npm start`. Вы должны увидеть, что аутентификация не удалась, так как у нас нет этой области (у нас есть User.Read и Admin.Write):

Теперь клиент сообщает:

```text
Error initializing client: Error: Error POSTing to endpoint (HTTP 403): Forbidden - insufficient scopes
```

а в терминале сервера вы увидите сообщение:

```text
User exists
```

и выполнение не продолжается дальше.

Либо добавьте эту область "User.Write", выполните `npm run generate` и перезапустите клиент, либо верните изменения в коде сервера.

---

**Отказ от ответственности**:  
Этот документ был переведен с помощью сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия обеспечить точность, автоматические переводы могут содержать ошибки или неточности. Оригинальный документ на его родном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется профессиональный перевод человеком. Мы не несем ответственности за любые недоразумения или неправильные интерпретации, возникшие в результате использования данного перевода.