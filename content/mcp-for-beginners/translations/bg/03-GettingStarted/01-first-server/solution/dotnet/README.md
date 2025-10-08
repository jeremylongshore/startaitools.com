<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "92af35e8c34923031f3d228dffad9ebb",
  "translation_date": "2025-09-03T16:18:22+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/dotnet/README.md",
  "language_code": "bg"
}
-->
# Стартиране на този пример

## -1- Инсталирайте зависимостите

```bash
dotnet restore
```

## -3- Стартирайте примера

```bash
dotnet run
```

## -4- Тествайте примера

С работещ сървър в един терминал, отворете друг терминал и изпълнете следната команда:

```bash
npx @modelcontextprotocol/inspector dotnet run
```

Това трябва да стартира уеб сървър с визуален интерфейс, който ви позволява да тествате примера.

След като сървърът се свърже:

- опитайте да изброите инструментите и изпълнете `add` с аргументи 2 и 4, трябва да видите 6 като резултат.
- отидете на ресурси и шаблон за ресурси и извикайте "greeting", въведете име и трябва да видите поздрав с името, което сте предоставили.

### Тестване в режим CLI

Можете да го стартирате директно в режим CLI, като изпълните следната команда:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/list
```

Това ще изброи всички налични инструменти в сървъра. Трябва да видите следния изход:

```text
{
  "tools": [
    {
      "name": "Add",
      "description": "Adds two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer"
          },
          "b": {
            "type": "integer"
          }
        },
        "title": "Add",
        "description": "Adds two numbers",
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
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/call --tool-name Add --tool-arg a=1 --tool-arg b=2
```

Трябва да видите следния изход:

```text
{
  "content": [
    {
      "type": "text",
      "text": "Sum 3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> Обикновено е много по-бързо да стартирате инспектора в режим CLI, отколкото в браузъра.
> Прочетете повече за инспектора [тук](https://github.com/modelcontextprotocol/inspector).

---

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI услуга за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи може да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за недоразумения или погрешни интерпретации, произтичащи от използването на този превод.