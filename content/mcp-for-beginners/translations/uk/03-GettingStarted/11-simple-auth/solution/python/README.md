<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:19:43+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "uk"
}
-->
# Запуск прикладу

## Створення середовища

```sh
python -m venv venv
source ./venv/bin/activate
```

## Встановлення залежностей

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## Генерація токена

Вам потрібно згенерувати токен, який клієнт буде використовувати для взаємодії з сервером.

Виконайте:

```sh
python util.py
```

## Запуск коду

Запустіть код за допомогою:

```sh
python server.py
```

У окремому терміналі введіть:

```sh
python client.py
```

У терміналі сервера ви повинні побачити щось схоже на:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

У вікні клієнта ви повинні побачити текст, схожий на:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

Це означає, що все працює.

### Змініть інформацію, щоб побачити помилку

Знайдіть цей код у *server.py*:

```python
 if not has_scope(has_header, "Admin.Write"):
```

Змініть його так, щоб він показував "User.Write". Ваш поточний токен не має такого рівня дозволів, тому якщо ви перезапустите сервер і спробуєте запустити клієнт ще раз, ви повинні побачити помилку, схожу на наступну, у терміналі сервера:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

Ви можете або повернути код сервера до попереднього стану, або згенерувати новий токен, який містить цей додатковий рівень доступу — вибір за вами.

---

**Відмова від відповідальності**:  
Цей документ був перекладений за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ на його рідній мові слід вважати авторитетним джерелом. Для критичної інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникають внаслідок використання цього перекладу.