<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "dde4e32e4b55ef4962c411b39d2340a7",
  "translation_date": "2025-09-03T16:18:30+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/dotnet/README.md",
  "language_code": "sr"
}
-->
# Покретање овог примера

## -1- Инсталирајте зависности

```bash
dotnet restore
```

## -2- Покрените пример

```bash
dotnet run
```

## -3- Тестирајте пример

Покрените посебан терминал пре него што извршите наредбу испод (уверите се да сервер још увек ради).

Док сервер ради у једном терминалу, отворите други терминал и покрените следећу команду:

```bash
npx @modelcontextprotocol/inspector http://localhost:3001
```

Ово би требало да покрене веб сервер са визуелним интерфејсом који вам омогућава тестирање примера.

> Уверите се да је **Streamable HTTP** изабран као тип транспорта, а URL је `http://localhost:3001/mcp`.

Када се сервер повеже:

- пробајте да наведете алатке и покренете `add`, са аргументима 2 и 4, требало би да видите 6 као резултат.
- идите на ресурсе и шаблон ресурса и позовите "greeting", унесите име и требало би да видите поздрав са именом које сте унели.

### Тестирање у CLI режиму

Можете га директно покренути у CLI режиму извршавањем следеће команде:

```bash 
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/list
```

Ово ће приказати све доступне алатке на серверу. Требало би да видите следећи излаз:

```text
{
  "tools": [
    {
      "name": "AddNumbers",
      "description": "Add two numbers together.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "description": "The first number",
            "type": "integer"
          },
          "b": {
            "description": "The second number",
            "type": "integer"
          }
        },
        "title": "AddNumbers",
        "description": "Add two numbers together.",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

Да бисте позвали алатку, унесите:

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/call --tool-name AddNumbers --tool-arg a=1 --tool-arg b=2
```

Требало би да видите следећи излаз:

```text
{
  "content": [
    {
      "type": "text",
      "text": "3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> Обично је много брже покренути инспектор у CLI режиму него у прегледачу.
> Прочитајте више о инспектору [овде](https://github.com/modelcontextprotocol/inspector).

---

**Одрицање од одговорности**:  
Овај документ је преведен коришћењем услуге за превођење помоћу вештачке интелигенције [Co-op Translator](https://github.com/Azure/co-op-translator). Иако се трудимо да превод буде тачан, молимо вас да имате у виду да аутоматизовани преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитативним извором. За критичне информације препоручује се професионални превод од стране људи. Не преузимамо одговорност за било каква погрешна тумачења или неспоразуме који могу настати услед коришћења овог превода.