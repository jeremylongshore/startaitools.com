<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3880d89fa60abc699e1a17a82ae514ef",
  "translation_date": "2025-10-07T01:25:14+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/typescript/README.md",
  "language_code": "uk"
}
-->
# Запуск прикладу

## Встановлення залежностей

```sh
npm install
```

## Збірка

```sh
npm run build
```

## Генерація токенів

```sh
npm run generate
```

Це створює токен у файлі *.env*. Клієнт буде читати з цього файлу.

## Запуск коду

Запустіть сервер за допомогою:

```sh
npm start
```

Запустіть клієнт у окремому терміналі за допомогою:

```sh
npm run client
```

У терміналі сервера ви повинні побачити вихідні дані, схожі на:

```text
User exists
User has required scopes
Middleware executed
```

а в терміналі клієнта ви повинні побачити вихідні дані, схожі на:

```text
Connected to MCP server with session ID: c1e50d7b-acff-4f11-8f96-5ae490ca1eaa
Available tools: { tools: [ { name: 'process-files', inputSchema: [Object] } ] }
Client disconnected.
Exiting...
```

### Зміна налаштувань

Давайте переконаємося, що ми розуміємо області доступу. Знайдіть файл *server.ts* і цей код:

```typescript
 if(!hasScopes(token, ["User.Read"])){
        res.status(403).send('Forbidden - insufficient scopes');
    }
```

Це означає, що переданий токен повинен мати "User.Read". Давайте змінимо це на "User.Write". Тепер запустіть `npm run build` і перезапустіть сервер за допомогою `npm start`. Тепер ви повинні побачити, що авторизація не вдалася, оскільки у нас немає цієї області доступу (у нас є User.Read і Admin.Write):

Клієнт тепер каже

```text
Error initializing client: Error: Error POSTing to endpoint (HTTP 403): Forbidden - insufficient scopes
```

а в терміналі сервера ви бачите:

```text
User exists
```

і що виконання не йде далі цього моменту.

Або додайте цю область доступу "User.Write" і запустіть `npm run generate`, а потім перезапустіть клієнт, або поверніть код сервера назад.

---

**Відмова від відповідальності**:  
Цей документ був перекладений за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, звертаємо вашу увагу, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ на його рідній мові слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.