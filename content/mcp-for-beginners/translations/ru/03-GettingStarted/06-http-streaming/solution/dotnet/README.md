<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "dde4e32e4b55ef4962c411b39d2340a7",
  "translation_date": "2025-09-03T15:55:59+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/dotnet/README.md",
  "language_code": "ru"
}
-->
# Запуск этого примера

## -1- Установите зависимости

```bash
dotnet restore
```

## -2- Запустите пример

```bash
dotnet run
```

## -3- Протестируйте пример

Перед выполнением следующего шага откройте отдельный терминал (убедитесь, что сервер все еще работает).

С работающим сервером в одном терминале откройте другой терминал и выполните следующую команду:

```bash
npx @modelcontextprotocol/inspector http://localhost:3001
```

Это запустит веб-сервер с визуальным интерфейсом, который позволит вам протестировать пример.

> Убедитесь, что **Streamable HTTP** выбран в качестве типа транспорта, а URL — `http://localhost:3001/mcp`.

После подключения к серверу:

- попробуйте перечислить инструменты и выполнить `add` с аргументами 2 и 4, результат должен быть равен 6.
- перейдите к ресурсам и шаблону ресурса, вызовите "greeting", введите имя, и вы увидите приветствие с указанным именем.

### Тестирование в режиме CLI

Вы можете запустить пример напрямую в режиме CLI, выполнив следующую команду:

```bash 
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/list
```

Это выведет список всех доступных инструментов на сервере. Вы должны увидеть следующий вывод:

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

Чтобы вызвать инструмент, введите:

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/call --tool-name AddNumbers --tool-arg a=1 --tool-arg b=2
```

Вы должны увидеть следующий вывод:

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
> Обычно запуск инспектора в режиме CLI происходит гораздо быстрее, чем в браузере.
> Подробнее об инспекторе читайте [здесь](https://github.com/modelcontextprotocol/inspector).

---

**Отказ от ответственности**:  
Этот документ был переведен с помощью сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия обеспечить точность, автоматические переводы могут содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется профессиональный перевод человеком. Мы не несем ответственности за любые недоразумения или неправильные интерпретации, возникающие в результате использования данного перевода.