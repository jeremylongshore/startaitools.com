<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:44:52+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "ar"
}
-->
# 📘 حل الواجب: توسيع خادم MCP للحاسبة الخاصة بك بأداة الجذر التربيعي

## نظرة عامة  
في هذا الواجب، قمت بتطوير خادم MCP للحاسبة الخاصة بك بإضافة أداة جديدة تحسب الجذر التربيعي لعدد ما. تتيح هذه الإضافة لوكيل الذكاء الاصطناعي الخاص بك التعامل مع استفسارات رياضية أكثر تقدمًا، مثل "ما هو الجذر التربيعي لـ 16؟" أو "احسب √49"، باستخدام أوامر بلغة طبيعية.

## 🛠️ تنفيذ أداة الجذر التربيعي  
لإضافة هذه الوظيفة، قمت بتعريف دالة أداة جديدة في ملف server.py الخاص بك. إليك التنفيذ:

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

## 🔍 كيف تعمل  

- **استيراد وحدة `math`**: لأداء العمليات الرياضية المتقدمة بخلاف الحسابات الأساسية، توفر بايثون الوحدة المدمجة `math`. تحتوي هذه الوحدة على مجموعة متنوعة من الدوال والثوابت الرياضية. باستيرادها باستخدام `import math`، يمكنك الوصول إلى دوال مثل `math.sqrt()` التي تحسب الجذر التربيعي لعدد.
- **تعريف الدالة**: يقوم المزخرف `@server.tool()` بتسجيل دالة `sqrt` كأداة يمكن لوكيل الذكاء الاصطناعي الوصول إليها.
- **معامل الإدخال**: تقبل الدالة وسيطًا واحدًا `a` من نوع `float`.
- **معالجة الأخطاء**: إذا كان `a` سالبًا، ترفع الدالة استثناء `ValueError` لمنع حساب الجذر التربيعي لعدد سالب، وهو أمر غير مدعوم من قبل دالة `math.sqrt()`.
- **قيمة الإرجاع**: بالنسبة للقيم غير السالبة، تعيد الدالة الجذر التربيعي لـ `a` باستخدام دالة `math.sqrt()` المدمجة في بايثون.

## 🔄 إعادة تشغيل الخادم  
بعد إضافة أداة `sqrt` الجديدة، من الضروري إعادة تشغيل خادم MCP الخاص بك لضمان تعرف الوكيل على الوظيفة الجديدة وقدرته على استخدامها.

## 💬 أمثلة على الأوامر لاختبار الأداة الجديدة  
إليك بعض الأوامر بلغة طبيعية التي يمكنك استخدامها لاختبار وظيفة الجذر التربيعي:

- "ما هو الجذر التربيعي لـ 25؟"
- "احسب الجذر التربيعي لـ 81."
- "ابحث عن الجذر التربيعي لـ 0."
- "ما هو الجذر التربيعي لـ 2.25؟"

يجب أن تؤدي هذه الأوامر إلى استدعاء الوكيل لأداة `sqrt` وإرجاع النتائج الصحيحة.

## ✅ ملخص  
من خلال إكمال هذا الواجب، لقد:

- وسعت خادم MCP للحاسبة الخاصة بك بأداة جديدة `sqrt`.
- مكنت وكيل الذكاء الاصطناعي من التعامل مع حسابات الجذر التربيعي عبر أوامر بلغة طبيعية.
- مارست إضافة أدوات جديدة وإعادة تشغيل الخادم لدمج وظائف إضافية.

لا تتردد في التجربة أكثر بإضافة أدوات رياضية أخرى، مثل الأسس أو الدوال اللوغاريتمية، لمواصلة تعزيز قدرات وكيلك!

**إخلاء المسؤولية**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق به. للمعلومات الهامة، يُنصح بالاعتماد على الترجمة البشرية المهنية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.