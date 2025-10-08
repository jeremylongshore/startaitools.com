<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d4c162484df410632550a4a357d40341",
  "translation_date": "2025-09-03T16:12:14+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "he"
}
-->
# הפעלת הדוגמה הזו

מומלץ להתקין `uv`, אך זה לא חובה. ראו [הוראות](https://docs.astral.sh/uv/#highlights)

## -0- יצירת סביבה וירטואלית

```bash
python -m venv venv
```

## -1- הפעלת הסביבה הווירטואלית

```bash
venv\Scripts\activate
```

## -2- התקנת התלויות

```bash
pip install "mcp[cli]"
```

## -3- הפעלת הדוגמה

```bash
mcp run server.py
```

## -4- בדיקת הדוגמה

עם השרת פועל באחד הטרמינלים, פתחו טרמינל נוסף והריצו את הפקודה הבאה:

```bash
mcp dev server.py
```

זה אמור להפעיל שרת אינטרנט עם ממשק חזותי שיאפשר לכם לבדוק את הדוגמה.

לאחר שהשרת מחובר:

- נסו לרשום כלים ולהפעיל `add`, עם ארגומנטים 2 ו-4. אתם אמורים לראות 6 בתוצאה.

- עברו למשאבים ולתבנית משאבים וקראו ל-`get_greeting`. הקלידו שם, ואתם אמורים לראות ברכה עם השם שסיפקתם.

### בדיקה במצב CLI

הבודק שהפעלתם הוא למעשה אפליקציית Node.js, ו-`mcp dev` הוא מעטפת שמסביבו.

ניתן להפעיל אותו ישירות במצב CLI על ידי הרצת הפקודה הבאה:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

זה יפרט את כל הכלים הזמינים בשרת. אתם אמורים לראות את הפלט הבא:

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

כדי להפעיל כלי, הקלידו:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

אתם אמורים לראות את הפלט הבא:

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
> בדרך כלל הרבה יותר מהיר להפעיל את הבודק במצב CLI מאשר בדפדפן.
> קראו עוד על הבודק [כאן](https://github.com/modelcontextprotocol/inspector).

---

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עשויים להכיל שגיאות או אי דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור סמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. איננו נושאים באחריות לאי הבנות או לפרשנויות שגויות הנובעות משימוש בתרגום זה.