<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:45:00+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "fa"
}
-->
# 📘 راه‌حل تمرین: افزودن ابزار جذر به سرور MCP ماشین‌حساب شما

## مرور کلی  
در این تمرین، سرور MCP ماشین‌حساب خود را با افزودن ابزاری جدید که جذر یک عدد را محاسبه می‌کند، ارتقا دادید. این افزودنی به عامل هوش مصنوعی شما امکان می‌دهد تا به سوالات ریاضی پیشرفته‌تری مانند «جذر ۱۶ چقدر است؟» یا «√۴۹ را حساب کن» با استفاده از دستورات زبان طبیعی پاسخ دهد.

## 🛠️ پیاده‌سازی ابزار جذر  
برای اضافه کردن این قابلیت، یک تابع ابزار جدید در فایل server.py خود تعریف کردید. پیاده‌سازی به این صورت است:

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

## 🔍 نحوه عملکرد

- **وارد کردن ماژول `math`**: برای انجام عملیات ریاضی فراتر از حساب ساده، پایتون ماژول داخلی `math` را ارائه می‌دهد. این ماژول شامل توابع و ثابت‌های متنوع ریاضی است. با وارد کردن آن به صورت `import math`، به توابعی مانند `math.sqrt()` دسترسی پیدا می‌کنید که جذر یک عدد را محاسبه می‌کند.  
- **تعریف تابع**: دکوراتور `@server.tool()` تابع `sqrt` را به عنوان ابزاری در دسترس عامل هوش مصنوعی شما ثبت می‌کند.  
- **پارامتر ورودی**: این تابع یک آرگومان از نوع `float` به نام `a` می‌پذیرد.  
- **مدیریت خطا**: اگر مقدار `a` منفی باشد، تابع یک `ValueError` ایجاد می‌کند تا از محاسبه جذر عدد منفی جلوگیری کند، چرا که `math.sqrt()` این حالت را پشتیبانی نمی‌کند.  
- **مقدار بازگشتی**: برای ورودی‌های غیرمنفی، تابع جذر `a` را با استفاده از متد داخلی `math.sqrt()` پایتون برمی‌گرداند.

## 🔄 راه‌اندازی مجدد سرور  
پس از افزودن ابزار جدید `sqrt`، ضروری است سرور MCP خود را مجدداً راه‌اندازی کنید تا عامل بتواند قابلیت جدید را شناسایی و استفاده کند.

## 💬 نمونه دستورات برای آزمایش ابزار جدید  
در اینجا چند دستور به زبان طبیعی برای تست عملکرد جذر آورده شده است:

- «جذر ۲۵ چقدر است؟»  
- «جذر ۸۱ را حساب کن.»  
- «جذر ۰ را پیدا کن.»  
- «جذر ۲.۲۵ چقدر است؟»

این دستورات باید باعث شوند عامل ابزار `sqrt` را فراخوانی کرده و نتایج صحیح را بازگرداند.

## ✅ خلاصه  
با انجام این تمرین، شما:

- سرور MCP ماشین‌حساب خود را با ابزار جدید `sqrt` گسترش دادید.  
- به عامل هوش مصنوعی خود امکان دادید تا محاسبات جذر را از طریق دستورات زبان طبیعی انجام دهد.  
- تمرین افزودن ابزارهای جدید و راه‌اندازی مجدد سرور برای ادغام قابلیت‌های بیشتر را انجام دادید.

می‌توانید با افزودن ابزارهای ریاضی دیگر مانند توان یا توابع لگاریتمی، به تقویت قابلیت‌های عامل خود ادامه دهید!

**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است حاوی خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان بومی خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما مسئول هیچ گونه سوءتفاهم یا تفسیر نادرستی که از استفاده از این ترجمه ناشی شود، نیستیم.