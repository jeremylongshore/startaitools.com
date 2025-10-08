<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "dde4e32e4b55ef4962c411b39d2340a7",
  "translation_date": "2025-09-03T16:21:04+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/dotnet/README.md",
  "language_code": "uk"
}
-->
# Запуск цього прикладу

## -1- Встановіть залежності

```bash
dotnet restore
```

## -2- Запустіть приклад

```bash
dotnet run
```

## -3- Протестуйте приклад

Запустіть окремий термінал перед виконанням нижченаведених команд (переконайтеся, що сервер все ще працює).

Коли сервер працює в одному терміналі, відкрийте інший термінал і виконайте наступну команду:

```bash
npx @modelcontextprotocol/inspector http://localhost:3001
```

Це має запустити веб-сервер із візуальним інтерфейсом, який дозволяє протестувати приклад.

> Переконайтеся, що **Streamable HTTP** вибрано як тип транспорту, а URL — `http://localhost:3001/mcp`.

Коли сервер підключений:

- спробуйте перелічити інструменти та виконати `add` з аргументами 2 і 4, ви повинні побачити результат 6.
- перейдіть до ресурсів і шаблону ресурсу та викличте "greeting", введіть ім'я, і ви повинні побачити привітання з введеним вами ім'ям.

### Тестування в режимі CLI

Ви можете запустити його безпосередньо в режимі CLI, виконавши наступну команду:

```bash 
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/list
```

Це перелічить усі інструменти, доступні на сервері. Ви повинні побачити наступний результат:

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

Щоб викликати інструмент, введіть:

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/call --tool-name AddNumbers --tool-arg a=1 --tool-arg b=2
```

Ви повинні побачити наступний результат:

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
> Зазвичай набагато швидше запускати інспектор у режимі CLI, ніж у браузері.
> Дізнайтеся більше про інспектор [тут](https://github.com/modelcontextprotocol/inspector).

---

**Відмова від відповідальності**:  
Цей документ був перекладений за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ на його рідній мові слід вважати авторитетним джерелом. Для критичної інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникають внаслідок використання цього перекладу.