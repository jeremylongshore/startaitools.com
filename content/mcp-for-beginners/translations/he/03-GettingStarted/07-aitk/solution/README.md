<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:53:41+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "he"
}
-->
# 📘 פתרון המשימה: הרחבת שרת ה-MCP של המחשבון עם כלי שורש ריבועי

## סקירה  
במשימה זו הרחבת את שרת ה-MCP של המחשבון שלך על ידי הוספת כלי חדש שמחשב את השורש הריבועי של מספר. תוספת זו מאפשרת לסוכן ה-AI שלך להתמודד עם שאילתות מתמטיות מתקדמות יותר, כמו "מהו השורש הריבועי של 16?" או "חשב √49," באמצעות פקודות בשפה טבעית.

## 🛠️ יישום כלי השורש הריבועי  
כדי להוסיף את הפונקציונליות הזו, הגדרת פונקציית כלי חדשה בקובץ server.py שלך. הנה המימוש:

```python
"""
Sample MCP Calculator Server implementation in Python.

This module demonstrates how to create a simple MCP server with calculator tools
that can perform basic arithmetic operations (add, subtract, multiply, divide).
"""

from mcp.server.fastmcp import FastMCP
import math

server = FastMCP("calculator")

@server.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together and return the result."""
    return a + b

@server.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the result."""
    return a - b

@server.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together and return the result."""
    return a * b

@server.tool()
def divide(a: float, b: float) -> float:
    """
    Divide a by b and return the result.
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@server.tool()
def sqrt(a: float) -> float:
    """
    Return the square root of a.

    Raises:
        ValueError: If a is negative.
    """
    if a < 0:
        raise ValueError("Cannot compute the square root of a negative number.")
    return math.sqrt(a)
```

## 🔍 איך זה עובד

- **ייבוא מודול `math`**: כדי לבצע פעולות מתמטיות מעבר לאריתמטיקה בסיסית, פייתון מספקת את מודול ה-`math` המובנה. מודול זה כולל מגוון פונקציות וקבועים מתמטיים. על ידי ייבואו באמצעות `import math`, אתה מקבל גישה לפונקציות כמו `math.sqrt()`, שמחשבת את השורש הריבועי של מספר.  
- **הגדרת הפונקציה**: הדקורטור `@server.tool()` רושם את הפונקציה `sqrt` ככלי שנגיש לסוכן ה-AI שלך.  
- **פרמטר קלט**: הפונקציה מקבלת ארגומנט יחיד `a` מסוג `float`.  
- **טיפול בשגיאות**: אם `a` שלילי, הפונקציה מעלה חריגת `ValueError` כדי למנוע חישוב שורש ריבועי של מספר שלילי, דבר שאינו נתמך על ידי `math.sqrt()`.  
- **ערך החזרה**: עבור קלטים לא שליליים, הפונקציה מחזירה את השורש הריבועי של `a` באמצעות המתודה המובנית `math.sqrt()` של פייתון.

## 🔄 הפעלה מחדש של השרת  
לאחר הוספת כלי ה-`sqrt` החדש, חשוב להפעיל מחדש את שרת ה-MCP שלך כדי לוודא שהסוכן מזהה ויכול להשתמש בפונקציונליות החדשה.

## 💬 דוגמאות לפקודות לבדיקה של הכלי החדש  
הנה כמה פקודות בשפה טבעית שתוכל להשתמש בהן כדי לבדוק את פונקציונליות השורש הריבועי:

- "מהו השורש הריבועי של 25?"  
- "חשב את השורש הריבועי של 81."  
- "מצא את השורש הריבועי של 0."  
- "מהו השורש הריבועי של 2.25?"

פקודות אלו אמורות לגרום לסוכן לקרוא לכלי ה-`sqrt` ולהחזיר את התוצאות הנכונות.

## ✅ סיכום  
על ידי השלמת משימה זו, עשית את הדברים הבאים:

- הרחבת את שרת ה-MCP של המחשבון עם כלי חדש בשם `sqrt`.  
- אפשרת לסוכן ה-AI שלך לטפל בחישובי שורש ריבועי באמצעות פקודות בשפה טבעית.  
- התאמנת בהוספת כלים חדשים ובהפעלה מחדש של השרת כדי לשלב פונקציונליות נוספת.

אל תהסס להמשיך ולנסות להוסיף כלים מתמטיים נוספים, כמו חזקות או פונקציות לוגריתמיות, כדי להמשיך ולשפר את יכולות הסוכן שלך!

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון כי תרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. המסמך המקורי בשפת המקור שלו נחשב למקור הסמכותי. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אנושי. אנו לא נושאים באחריות לכל אי-הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.