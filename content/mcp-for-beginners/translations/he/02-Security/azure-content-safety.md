<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "f5300fd1b5e84520d500b2a8f568a1d8",
  "translation_date": "2025-07-17T08:56:28+00:00",
  "source_file": "02-Security/azure-content-safety.md",
  "language_code": "he"
}
-->
# אבטחה מתקדמת של MCP עם Azure Content Safety

Azure Content Safety מספקת כלים רבי עוצמה שיכולים לשפר את האבטחה של יישומי ה-MCP שלך:

## מגן הפקודות (Prompt Shields)

מגן הפקודות של מיקרוסופט מספק הגנה חזקה מפני התקפות הזרקת פקודות ישירות ועקיפות באמצעות:

1. **זיהוי מתקדם**: משתמש בלמידת מכונה לזיהוי הוראות זדוניות המוטמעות בתוכן.
2. **הדגשה**: משנה את הטקסט הנכנס כדי לסייע למערכות ה-AI להבחין בין הוראות תקפות לקלטים חיצוניים.
3. **מפרידים וסימון נתונים**: מסמן גבולות בין נתונים מהימנים לנתונים לא מהימנים.
4. **שילוב עם Content Safety**: עובד עם Azure AI Content Safety לזיהוי ניסיונות פריצה ותוכן מזיק.
5. **עדכונים מתמשכים**: מיקרוסופט מעדכנת באופן שוטף את מנגנוני ההגנה מפני איומים חדשים.

## יישום Azure Content Safety עם MCP

גישה זו מספקת הגנה רב-שכבתית:
- סריקת קלטים לפני עיבוד
- אימות פלטים לפני החזרה
- שימוש ברשימות חסימה לדפוסים מזיקים ידועים
- ניצול מודלים מעודכנים של Azure Content Safety

## משאבים ל-Azure Content Safety

למידע נוסף על יישום Azure Content Safety עם שרתי ה-MCP שלך, עיין במשאבים הרשמיים הבאים:

1. [Azure AI Content Safety Documentation](https://learn.microsoft.com/azure/ai-services/content-safety/) - תיעוד רשמי ל-Azure Content Safety.
2. [Prompt Shield Documentation](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/prompt-shield) - למידה כיצד למנוע התקפות הזרקת פקודות.
3. [Content Safety API Reference](https://learn.microsoft.com/rest/api/contentsafety/) - הפניה מפורטת ל-API ליישום Content Safety.
4. [Quickstart: Azure Content Safety with C#](https://learn.microsoft.com/azure/ai-services/content-safety/quickstart-csharp) - מדריך מהיר ליישום באמצעות C#.
5. [Content Safety Client Libraries](https://learn.microsoft.com/azure/ai-services/content-safety/quickstart-client-libraries-rest-api) - ספריות לקוח לשפות תכנות שונות.
6. [Detecting Jailbreak Attempts](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - הנחיות ספציפיות לזיהוי ומניעת ניסיונות פריצה.
7. [Best Practices for Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/best-practices) - שיטות עבודה מומלצות ליישום אפקטיבי של Content Safety.

ליישום מעמיק יותר, עיין במדריך שלנו ל-[יישום Azure Content Safety](./azure-content-safety-implementation.md).

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון כי תרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. המסמך המקורי בשפת המקור שלו נחשב למקור הסמכותי. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אנושי. אנו לא נושאים באחריות לכל אי-הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.