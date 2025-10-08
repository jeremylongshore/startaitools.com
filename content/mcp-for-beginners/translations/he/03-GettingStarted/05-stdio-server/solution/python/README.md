<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "68cd055621b3370948a5a1dff7bedc9a",
  "translation_date": "2025-08-26T20:34:34+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/python/README.md",
  "language_code": "he"
}
-->
# MCP stdio Server - פתרון בפייתון

> **⚠️ חשוב**: פתרון זה עודכן לשימוש ב-**stdio transport** כפי שמומלץ במפרט MCP 2025-06-18. התמיכה ב-SSE transport המקורי הופסקה.

## סקירה כללית

פתרון זה בפייתון מדגים כיצד לבנות שרת MCP באמצעות stdio transport הנוכחי. ה-stdio transport פשוט יותר, מאובטח יותר ומספק ביצועים טובים יותר בהשוואה לגישת ה-SSE שהופסקה.

## דרישות מקדימות

- פייתון 3.8 או גרסה מאוחרת יותר
- מומלץ להתקין את `uv` לניהול חבילות, ראו [הוראות](https://docs.astral.sh/uv/#highlights)

## הוראות התקנה

### שלב 1: יצירת סביבה וירטואלית

```bash
python -m venv venv
```

### שלב 2: הפעלת הסביבה הווירטואלית

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### שלב 3: התקנת התלויות

```bash
pip install mcp
```

## הפעלת השרת

שרת ה-stdio פועל בצורה שונה משרת ה-SSE הישן. במקום להפעיל שרת אינטרנט, הוא מתקשר דרך stdin/stdout:

```bash
python server.py
```

**חשוב**: השרת ייראה כאילו הוא "נתקע" - זה נורמלי! הוא ממתין להודעות JSON-RPC מ-stdin.

## בדיקת השרת

### שיטה 1: שימוש ב-MCP Inspector (מומלץ)

```bash
npx @modelcontextprotocol/inspector python server.py
```

זה יבצע:
1. הפעלת השרת כתהליך משנה
2. פתיחת ממשק אינטרנט לבדיקות
3. אפשרות לבדוק את כל הכלים של השרת בצורה אינטראקטיבית

### שיטה 2: בדיקות JSON-RPC ישירות

ניתן גם לבדוק על ידי שליחת הודעות JSON-RPC ישירות:

1. הפעלת השרת: `python server.py`
2. שליחת הודעת JSON-RPC (דוגמה):

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
```

3. השרת יגיב עם הכלים הזמינים

### כלים זמינים

השרת מספק את הכלים הבאים:

- **add(a, b)**: חיבור שני מספרים
- **multiply(a, b)**: כפל שני מספרים  
- **get_greeting(name)**: יצירת ברכה מותאמת אישית
- **get_server_info()**: קבלת מידע על השרת

### בדיקה עם Claude Desktop

כדי להשתמש בשרת זה עם Claude Desktop, הוסיפו את ההגדרה הבאה ל-`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "example-stdio-server": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

## הבדלים מרכזיים מ-SSE

**stdio transport (נוכחי):**
- ✅ התקנה פשוטה יותר - אין צורך בשרת אינטרנט
- ✅ אבטחה טובה יותר - אין נקודות קצה HTTP
- ✅ תקשורת מבוססת תהליכי משנה
- ✅ JSON-RPC דרך stdin/stdout
- ✅ ביצועים טובים יותר

**SSE transport (שהופסק):**
- ❌ דרש התקנת שרת HTTP
- ❌ נדרש מסגרת אינטרנט (Starlette/FastAPI)
- ❌ ניהול ניתוב ומפגשים מורכב יותר
- ❌ שיקולי אבטחה נוספים
- ❌ הופסק במפרט MCP 2025-06-18

## טיפים לדיבוג

- השתמשו ב-`stderr` לרישום (לעולם לא ב-`stdout`)
- בדקו עם ה-Inspector לדיבוג חזותי
- ודאו שכל הודעות ה-JSON מופרדות בשורה חדשה
- בדקו שהשרת מופעל ללא שגיאות

פתרון זה עוקב אחר מפרט MCP הנוכחי ומדגים שיטות עבודה מומלצות ליישום stdio transport.

---

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עשויים להכיל שגיאות או אי דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור סמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. איננו נושאים באחריות לאי הבנות או לפרשנויות שגויות הנובעות משימוש בתרגום זה.