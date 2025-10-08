<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3880d89fa60abc699e1a17a82ae514ef",
  "translation_date": "2025-10-07T01:24:37+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/typescript/README.md",
  "language_code": "bg"
}
-->
# Стартиране на пример

## Инсталиране на зависимости

```sh
npm install
```

## Създаване на проект

```sh
npm run build
```

## Генериране на токени

```sh
npm run generate
```

Това създава токен в файл *.env*. Клиентът ще чете от този файл.

## Стартиране на кода

Стартирайте сървъра с:

```sh
npm start
```

Стартирайте клиента в отделен терминал с:

```sh
npm run client
```

В терминала на сървъра трябва да видите изход, подобен на:

```text
User exists
User has required scopes
Middleware executed
```

а в терминала на клиента трябва да видите изход, подобен на:

```text
Connected to MCP server with session ID: c1e50d7b-acff-4f11-8f96-5ae490ca1eaa
Available tools: { tools: [ { name: 'process-files', inputSchema: [Object] } ] }
Client disconnected.
Exiting...
```

### Промени

Нека се уверим, че разбираме обхватите. Намерете файла *server.ts* и този код:

```typescript
 if(!hasScopes(token, ["User.Read"])){
        res.status(403).send('Forbidden - insufficient scopes');
    }
```

Това казва, че предаденият токен трябва да има "User.Read". Нека го променим на "User.Write". Сега изпълнете `npm run build` и рестартирайте сървъра с `npm start`. Трябва да видите, че удостоверяването се проваля, тъй като нямаме този обхват (имаме User.Read и Admin.Write):

Клиентът сега казва

```text
Error initializing client: Error: Error POSTing to endpoint (HTTP 403): Forbidden - insufficient scopes
```

а в терминала на сървъра можете да видите, че казва:

```text
User exists
```

и че не продължава след тази точка.

Или добавете този обхват "User.Write" и изпълнете `npm run generate`, след което рестартирайте клиента, ИЛИ върнете кода на сървъра обратно.

---

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI услуга за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи може да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да било недоразумения или погрешни интерпретации, произтичащи от използването на този превод.