<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:06:17+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "bg"
}
-->
# Стартиране на пример

## Настройване на виртуална среда

```sh
python -m venv venv
source ./venv/bin/activate
```

## Инсталиране на зависимости

```sh
pip install "mcp[cli]"
```

## Стартиране на код

```sh
python client.py
```

Трябва да видите текста:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI услуга за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи може да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Не носим отговорност за недоразумения или погрешни интерпретации, произтичащи от използването на този превод.