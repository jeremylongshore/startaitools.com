<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:06:42+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "uk"
}
-->
# Запуск прикладу

## Налаштування віртуального середовища

```sh
python -m venv venv
source ./venv/bin/activate
```

## Встановлення залежностей

```sh
pip install "mcp[cli]"
```

## Запуск коду

```sh
python client.py
```

Ви повинні побачити текст:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Відмова від відповідальності**:  
Цей документ був перекладений за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ на його рідній мові слід вважати авторитетним джерелом. Для критичної інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникають внаслідок використання цього перекладу.