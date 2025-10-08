<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:19:06+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "bg"
}
-->
# Стартиране на пример

## Създаване на среда

```sh
python -m venv venv
source ./venv/bin/activate
```

## Инсталиране на зависимости

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## Генериране на токен

Ще трябва да генерирате токен, който клиентът ще използва, за да комуникира със сървъра.

Извикайте:

```sh
python util.py
```

## Стартиране на кода

Стартирайте кода с:

```sh
python server.py
```

В отделен терминал напишете:

```sh
python client.py
```

В терминала на сървъра трябва да видите нещо подобно на:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

В прозореца на клиента трябва да видите текст, подобен на:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

Това означава, че всичко работи.

### Променете информацията, за да видите как не успява

Намерете този код в *server.py*:

```python
 if not has_scope(has_header, "Admin.Write"):
```

Променете го така, че да казва "User.Write". Вашият текущ токен няма това ниво на разрешение, така че ако рестартирате сървъра и опитате да стартирате клиента отново, трябва да видите грешка, подобна на следната в терминала на сървъра:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

Можете или да върнете обратно кода на сървъра, или да генерирате нов токен, който съдържа този допълнителен обхват – изборът е ваш.

---

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI услуга за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи може да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за недоразумения или погрешни интерпретации, произтичащи от използването на този превод.