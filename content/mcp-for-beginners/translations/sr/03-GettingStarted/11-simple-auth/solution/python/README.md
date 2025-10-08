<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:19:14+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "sr"
}
-->
# Покрени пример

## Креирај окружење

```sh
python -m venv venv
source ./venv/bin/activate
```

## Инсталирај зависности

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## Генериши токен

Биће потребно да генеришете токен који ће клијент користити за комуникацију са сервером.

Позовите:

```sh
python util.py
```

## Покрени код

Покрените код са:

```sh
python server.py
```

У другом терминалу, укуцајте:

```sh
python client.py
```

У терминалу сервера, требало би да видите нешто попут:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

У прозору клијента, требало би да видите текст сличан:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

То значи да све ради.

### Промените информације да бисте видели грешку

Пронађите овај код у *server.py*:

```python
 if not has_scope(has_header, "Admin.Write"):
```

Промените га тако да каже "User.Write". Ваш тренутни токен нема тај ниво дозволе, па ако поново покренете сервер и покушате поново да покренете клијента, требало би да видите грешку сличну следећој у терминалу сервера:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

Можете или да вратите свој серверски код на претходно стање или да генеришете нови токен који садржи овај додатни опсег, избор је на вама.

---

**Одрицање од одговорности**:  
Овај документ је преведен помоћу услуге за превођење вештачке интелигенције [Co-op Translator](https://github.com/Azure/co-op-translator). Иако настојимо да обезбедимо тачност, молимо вас да имате у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати меродавним извором. За критичне информације препоручује се професионални превод од стране људи. Не преузимамо одговорност за било каква погрешна тумачења или неспоразуме који могу настати услед коришћења овог превода.