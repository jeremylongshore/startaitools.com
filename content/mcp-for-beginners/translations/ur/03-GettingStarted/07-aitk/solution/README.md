<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:45:08+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "ur"
}
-->
# 📘 اسائنمنٹ حل: اپنے کیلکولیٹر MCP سرور میں اسکوائر روٹ ٹول شامل کرنا

## جائزہ  
اس اسائنمنٹ میں، آپ نے اپنے کیلکولیٹر MCP سرور کو ایک نئے ٹول کے ذریعے بہتر بنایا جو کسی عدد کا اسکوائر روٹ نکالتا ہے۔ اس اضافے سے آپ کا AI ایجنٹ زیادہ پیچیدہ ریاضیاتی سوالات جیسے "16 کا اسکوائر روٹ کیا ہے؟" یا "√49 کا حساب لگائیں" قدرتی زبان کے ذریعے سمجھ کر حل کر سکتا ہے۔

## 🛠️ اسکوائر روٹ ٹول کا نفاذ  
اس فنکشن کو شامل کرنے کے لیے، آپ نے اپنے server.py فائل میں ایک نیا ٹول فنکشن ڈیفائن کیا۔ یہاں اس کا نفاذ دیا گیا ہے:

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

## 🔍 یہ کیسے کام کرتا ہے  

- **`math` ماڈیول کو امپورٹ کریں**: بنیادی حساب کتاب سے آگے ریاضیاتی آپریشنز کرنے کے لیے، Python میں بلٹ ان `math` ماڈیول موجود ہے۔ اس ماڈیول میں مختلف ریاضیاتی فنکشنز اور مستقل شامل ہوتے ہیں۔ `import math` کے ذریعے آپ کو `math.sqrt()` جیسی فنکشنز تک رسائی ملتی ہے جو کسی عدد کا اسکوائر روٹ نکالتی ہے۔  
- **فنکشن کی تعریف**: `@server.tool()` ڈیکوریٹر `sqrt` فنکشن کو ایک ٹول کے طور پر رجسٹر کرتا ہے جسے آپ کا AI ایجنٹ استعمال کر سکتا ہے۔  
- **ان پٹ پیرامیٹر**: یہ فنکشن ایک عدد `a` لیتا ہے جو `float` ٹائپ کا ہوتا ہے۔  
- **ایرر ہینڈلنگ**: اگر `a` منفی ہو تو فنکشن `ValueError` اٹھاتا ہے تاکہ منفی عدد کا اسکوائر روٹ نکالنے کی کوشش نہ کی جائے، کیونکہ `math.sqrt()` منفی اعداد کو سپورٹ نہیں کرتا۔  
- **ریٹرن ویلیو**: غیر منفی ان پٹ کے لیے، یہ فنکشن Python کے بلٹ ان `math.sqrt()` میتھڈ سے `a` کا اسکوائر روٹ واپس کرتا ہے۔  

## 🔄 سرور کو دوبارہ شروع کرنا  
نیا `sqrt` ٹول شامل کرنے کے بعد، ضروری ہے کہ آپ اپنا MCP سرور دوبارہ شروع کریں تاکہ ایجنٹ نئی فنکشنلٹی کو پہچان سکے اور استعمال کر سکے۔

## 💬 نئے ٹول کی جانچ کے لیے مثال کے پرامپٹس  
یہاں کچھ قدرتی زبان کے پرامپٹس دیے گئے ہیں جنہیں آپ اسکوائر روٹ فنکشن کی جانچ کے لیے استعمال کر سکتے ہیں:

- "25 کا اسکوائر روٹ کیا ہے؟"  
- "81 کا اسکوائر روٹ نکالیں۔"  
- "0 کا اسکوائر روٹ معلوم کریں۔"  
- "2.25 کا اسکوائر روٹ کیا ہے؟"  

یہ پرامپٹس ایجنٹ کو `sqrt` ٹول کال کرنے اور درست نتائج واپس کرنے کی ترغیب دیں گے۔

## ✅ خلاصہ  
اس اسائنمنٹ کو مکمل کر کے آپ نے:

- اپنے کیلکولیٹر MCP سرور میں نیا `sqrt` ٹول شامل کیا۔  
- اپنے AI ایجنٹ کو قدرتی زبان کے پرامپٹس کے ذریعے اسکوائر روٹ کے حسابات کرنے کے قابل بنایا۔  
- نئے ٹولز شامل کرنے اور سرور کو دوبارہ شروع کرنے کی مشق کی تاکہ اضافی فنکشنلٹیز کو ضم کیا جا سکے۔  

مزید ریاضیاتی ٹولز جیسے ایکسپونینشیئشن یا لاگرتھمک فنکشنز شامل کر کے اپنے ایجنٹ کی صلاحیتوں کو مزید بڑھانے کی کوشش کریں!

**دستخطی نوٹ**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ اگرچہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنی مادری زبان میں معتبر ماخذ سمجھی جانی چاہیے۔ اہم معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم پر عائد نہیں ہوتی۔