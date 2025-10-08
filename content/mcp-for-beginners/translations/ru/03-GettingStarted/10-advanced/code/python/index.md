<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:03:17+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "ru"
}
-->
# Запуск примера

## Настройка виртуального окружения

```sh
python -m venv venv
source ./venv/bin/activate
```

## Установка зависимостей

```sh
pip install "mcp[cli]"
```

## Запуск кода

```sh
python client.py
```

Вы должны увидеть текст:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Отказ от ответственности**:  
Этот документ был переведен с помощью сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия обеспечить точность, автоматические переводы могут содержать ошибки или неточности. Оригинальный документ на его родном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется профессиональный перевод человеком. Мы не несем ответственности за любые недоразумения или неправильные интерпретации, возникшие в результате использования данного перевода.