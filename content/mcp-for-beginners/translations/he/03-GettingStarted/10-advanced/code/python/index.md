<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:05:29+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "he"
}
-->
# הפעלת דוגמה

## הגדרת סביבת עבודה וירטואלית

```sh
python -m venv venv
source ./venv/bin/activate
```

## התקנת תלותים

```sh
pip install "mcp[cli]"
```

## הפעלת הקוד

```sh
python client.py
```

אתם אמורים לראות את הטקסט:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עשויים להכיל שגיאות או אי דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור הסמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. אנו לא נושאים באחריות לאי הבנות או לפרשנויות שגויות הנובעות משימוש בתרגום זה.