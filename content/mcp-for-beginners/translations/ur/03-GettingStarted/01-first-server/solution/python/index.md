<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d4c162484df410632550a4a357d40341",
  "translation_date": "2025-09-03T15:57:57+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "ur"
}
-->
# اس نمونے کو چلانا

آپ کو `uv` انسٹال کرنے کی تجویز دی جاتی ہے لیکن یہ لازمی نہیں ہے، مزید معلومات کے لیے دیکھیں [instructions](https://docs.astral.sh/uv/#highlights)

## -0- ایک ورچوئل ماحول بنائیں

```bash
python -m venv venv
```

## -1- ورچوئل ماحول کو فعال کریں

```bash
venv\Scripts\activate
```

## -2- ضروریات انسٹال کریں

```bash
pip install "mcp[cli]"
```

## -3- نمونہ چلائیں

```bash
mcp run server.py
```

## -4- نمونہ ٹیسٹ کریں

جب سرور ایک ٹرمینل میں چل رہا ہو، تو دوسرا ٹرمینل کھولیں اور درج ذیل کمانڈ چلائیں:

```bash
mcp dev server.py
```

یہ ایک ویب سرور شروع کرے گا جس میں ایک بصری انٹرفیس ہوگا جو آپ کو نمونہ ٹیسٹ کرنے کی اجازت دے گا۔

جب سرور جڑ جائے:

- ٹولز کی فہرست بنانے کی کوشش کریں اور `add` چلائیں، دلائل 2 اور 4 کے ساتھ، آپ کو نتیجے میں 6 نظر آنا چاہیے۔

- وسائل اور وسائل کے سانچے پر جائیں اور `get_greeting` کو کال کریں، ایک نام ٹائپ کریں اور آپ کو فراہم کردہ نام کے ساتھ ایک سلام نظر آئے گا۔

### CLI موڈ میں ٹیسٹنگ

جو انسپکٹر آپ نے چلایا ہے وہ دراصل ایک Node.js ایپ ہے اور `mcp dev` اس کے ارد گرد ایک ریپر ہے۔

آپ اسے CLI موڈ میں براہ راست درج ذیل کمانڈ چلا کر لانچ کر سکتے ہیں:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

یہ سرور میں دستیاب تمام ٹولز کی فہرست دے گا۔ آپ کو درج ذیل آؤٹ پٹ نظر آنا چاہیے:

```text
{
  "tools": [
    {
      "name": "add",
      "description": "Add two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "title": "A",
            "type": "integer"
          },
          "b": {
            "title": "B",
            "type": "integer"
          }
        },
        "required": [
          "a",
          "b"
        ],
        "title": "addArguments"
      }
    }
  ]
}
```

کسی ٹول کو چلانے کے لیے درج کریں:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

آپ کو درج ذیل آؤٹ پٹ نظر آنا چاہیے:

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
> عام طور پر انسپکٹر کو CLI موڈ میں چلانا براؤزر کے مقابلے میں بہت تیز ہوتا ہے۔
> انسپکٹر کے بارے میں مزید پڑھیں [یہاں](https://github.com/modelcontextprotocol/inspector)۔

---

**ڈسکلیمر**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کا استعمال کرتے ہوئے ترجمہ کی گئی ہے۔ ہم درستگی کے لیے کوشش کرتے ہیں، لیکن براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا غیر درستیاں ہو سکتی ہیں۔ اصل دستاویز کو اس کی اصل زبان میں مستند ذریعہ سمجھا جانا چاہیے۔ اہم معلومات کے لیے، پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ ہم اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کے ذمہ دار نہیں ہیں۔