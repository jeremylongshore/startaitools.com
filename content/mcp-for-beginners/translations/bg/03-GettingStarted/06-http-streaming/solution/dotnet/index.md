<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "dde4e32e4b55ef4962c411b39d2340a7",
  "translation_date": "2025-09-03T16:17:53+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/dotnet/README.md",
  "language_code": "bg"
}
-->
# Изпълнение на този пример

## -1- Инсталирайте зависимостите

```bash
dotnet restore
```

## -2- Стартирайте примера

```bash
dotnet run
```

## -3- Тествайте примера

Стартирайте отделен терминал, преди да изпълните командите по-долу (уверете се, че сървърът все още работи).

Докато сървърът работи в един терминал, отворете друг терминал и изпълнете следната команда:

```bash
npx @modelcontextprotocol/inspector http://localhost:3001
```

Това трябва да стартира уеб сървър с визуален интерфейс, който ви позволява да тествате примера.

> Уверете се, че **Streamable HTTP** е избран като тип транспорт, а URL е `http://localhost:3001/mcp`.

След като сървърът се свърже:

- опитайте да изброите инструментите и изпълнете `add` с аргументи 2 и 4, трябва да видите 6 като резултат.
- отидете на ресурси и шаблон за ресурси и извикайте "greeting", въведете име и трябва да видите поздрав с въведеното от вас име.

### Тестване в CLI режим

Можете да го стартирате директно в CLI режим, като изпълните следната команда:

```bash 
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/list
```

Това ще изброи всички налични инструменти в сървъра. Трябва да видите следния изход:

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

За да извикате инструмент, въведете:

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/call --tool-name AddNumbers --tool-arg a=1 --tool-arg b=2
```

Трябва да видите следния изход:

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
> Обикновено е много по-бързо да стартирате инспектора в CLI режим, отколкото в браузъра.
> Прочетете повече за инспектора [тук](https://github.com/modelcontextprotocol/inspector).

---

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI услуга за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи може да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за недоразумения или погрешни интерпретации, произтичащи от използването на този превод.