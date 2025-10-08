<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3880d89fa60abc699e1a17a82ae514ef",
  "translation_date": "2025-10-07T01:24:44+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/typescript/README.md",
  "language_code": "sr"
}
-->
# Покрени пример

## Инсталирај зависности

```sh
npm install
```

## Изгради

```sh
npm run build
```

## Генериши токене

```sh
npm run generate
```

Ово креира токен у датотеци *.env*. Клијент ће читати из ове датотеке.

## Покрени код

Покрените сервер са:

```sh
npm start
```

Покрените клијент, у одвојеном терминалу, са:

```sh
npm run client
```

У терминалу сервера, требало би да видите излаз сличан:

```text
User exists
User has required scopes
Middleware executed
```

а у терминалу клијента, требало би да видите излаз сличан:

```text
Connected to MCP server with session ID: c1e50d7b-acff-4f11-8f96-5ae490ca1eaa
Available tools: { tools: [ { name: 'process-files', inputSchema: [Object] } ] }
Client disconnected.
Exiting...
```

### Промене

Хајде да се уверимо да разумемо опсеге. Пронађите датотеку *server.ts* и овај код:

```typescript
 if(!hasScopes(token, ["User.Read"])){
        res.status(403).send('Forbidden - insufficient scopes');
    }
```

Ово каже да прослеђени токен мора да има "User.Read", хајде да то променимо у "User.Write". Сада покрените `npm run build` и поново покрените сервер `npm start`. Сада би требало да видите да аутентификација не успева јер немамо овај опсег (имамо User.Read и Admin.Write):

Клијент сада каже

```text
Error initializing client: Error: Error POSTing to endpoint (HTTP 403): Forbidden - insufficient scopes
```

а можете видети у терминалу сервера да каже:

```text
User exists
```

и да не иде даље од ове тачке.

Или додајте овај опсег "User.Write" и покрените `npm run generate` и поново покрените клијент ИЛИ промените серверски код назад.

---

**Одрицање од одговорности**:  
Овај документ је преведен помоћу услуге за превођење уз помоћ вештачке интелигенције [Co-op Translator](https://github.com/Azure/co-op-translator). Иако се трудимо да обезбедимо тачност, молимо вас да имате у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати меродавним извором. За критичне информације препоручује се професионални превод од стране људског преводиоца. Не преузимамо одговорност за било каква погрешна тумачења или неспоразуме који могу произаћи из коришћења овог превода.