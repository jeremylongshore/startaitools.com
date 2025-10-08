<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:55:46+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "my"
}
-->
# 📘 အလုပ်အပ်ချက် ဖြေရှင်းချက် - သင်၏ ကိန်းဂဏန်း MCP ဆာဗာကို စတုရန်းမြစ်ကိရိယာဖြင့် တိုးချဲ့ခြင်း

## အနှစ်ချုပ်  
ဤအလုပ်အပ်ချက်တွင် သင်၏ ကိန်းဂဏန်း MCP ဆာဗာကို နံပါတ်တစ်ခု၏ စတုရန်းမြစ်ကိုတွက်ချက်ပေးနိုင်သော ကိရိယာအသစ်ဖြင့် တိုးချဲ့ခဲ့ပါသည်။ ၎င်းဖြင့် သင်၏ AI ကိုယ်စားလှယ်သည် "၁၆ ၏ စတုရန်းမြစ် ဘာလဲ?" သို့မဟုတ် "√၄၉ ကိုတွက်ပါ" ကဲ့သို့သော သဘာဝဘာသာစကားဖြင့် မေးခွန်းများကို ပိုမိုတိကျစွာ ဖြေရှင်းနိုင်ပါသည်။

## 🛠️ စတုရန်းမြစ်ကိရိယာကို အကောင်အထည်ဖော်ခြင်း  
ဤလုပ်ဆောင်ချက်အတွက် သင်၏ server.py ဖိုင်တွင် ကိရိယာအသစ်တစ်ခုအဖြစ် function ကို သတ်မှတ်ခဲ့ပါသည်။ အကောင်အထည်ဖော်မှုမှာ အောက်ပါအတိုင်းဖြစ်သည်-

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

## 🔍 လုပ်ဆောင်ပုံ  
- **`math` module ကို import လုပ်ခြင်း** - အခြေခံဂဏန်းတွက်ချက်မှုများအပြင် ပိုမိုရှုပ်ထွေးသော သင်္ချာဆိုင်ရာ လုပ်ဆောင်ချက်များအတွက် Python တွင် built-in `math` module ရှိသည်။ ၎င်းတွင် သင်္ချာဆိုင်ရာ function များနှင့် constant များပါဝင်သည်။ `import math` ဖြင့် import လုပ်ခြင်းအားဖြင့် `math.sqrt()` ကဲ့သို့သော နံပါတ်တစ်ခု၏ စတုရန်းမြစ်ကိုတွက်ချက်ပေးသော function များကို အသုံးပြုနိုင်ပါသည်။  
- **Function သတ်မှတ်ချက်** - `@server.tool()` decorator သည် `sqrt` function ကို သင်၏ AI ကိုယ်စားလှယ်မှ အသုံးပြုနိုင်သော ကိရိယာအဖြစ် မှတ်ပုံတင်ပေးသည်။  
- **Input Parameter** - function သည် `float` အမျိုးအစားရှိသော `a` တစ်ခုကို လက်ခံသည်။  
- **အမှားကိုင်တွယ်မှု** - `a` သည် အနုတ်တစ်ခုဖြစ်ပါက `math.sqrt()` သည် အနုတ်နံပါတ်၏ စတုရန်းမြစ်ကိုတွက်ချက်၍ မရနိုင်သောကြောင့် `ValueError` ကို ထုတ်ပေးသည်။  
- **Return Value** - အနုတ်မဖြစ်သော input များအတွက် Python built-in `math.sqrt()` method ဖြင့် `a` ၏ စတုရန်းမြစ်ကို ပြန်လည်ပေးပို့သည်။  

## 🔄 ဆာဗာကို ပြန်လည်စတင်ခြင်း  
အသစ်ထည့်သွင်းထားသော `sqrt` ကိရိယာကို အသုံးပြုနိုင်ရန် MCP ဆာဗာကို ပြန်လည်စတင်ပေးရမည်ဖြစ်သည်။

## 💬 စတုရန်းမြစ်ကိရိယာကို စမ်းသပ်ရန် ဥပမာ မေးခွန်းများ  
အောက်ပါ သဘာဝဘာသာစကား မေးခွန်းများဖြင့် စတုရန်းမြစ်ကိရိယာကို စမ်းသပ်နိုင်ပါသည်-  

- "၂၅ ၏ စတုရန်းမြစ် ဘာလဲ?"  
- "၈၁ ၏ စတုရန်းမြစ်ကိုတွက်ပါ။"  
- "၀ ၏ စတုရန်းမြစ် ဘာလဲ?"  
- "၂.၂၅ ၏ စတုရန်းမြစ် ဘာလဲ?"  

ဤမေးခွန်းများသည် AI ကိုယ်စားလှယ်အား `sqrt` ကိရိယာကို ခေါ်ယူပြီး မှန်ကန်သော ရလဒ်များကို ပြန်ပေးပို့ရန် ဖြစ်စေပါသည်။

## ✅ အနှစ်ချုပ်  
ဤအလုပ်အပ်ချက်ကို ပြီးမြောက်စွာ ဆောင်ရွက်ခြင်းဖြင့်-  

- သင်၏ ကိန်းဂဏန်း MCP ဆာဗာကို `sqrt` ကိရိယာအသစ်ဖြင့် တိုးချဲ့နိုင်ခဲ့သည်။  
- သင်၏ AI ကိုယ်စားလှယ်အား သဘာဝဘာသာစကားဖြင့် စတုရန်းမြစ်တွက်ချက်မှုများကို ကိုင်တွယ်နိုင်စေခဲ့သည်။  
- ကိရိယာအသစ်များ ထည့်သွင်းခြင်းနှင့် ဆာဗာကို ပြန်လည်စတင်ခြင်းကို လေ့ကျင့်ခဲ့သည်။  

သင်၏ ကိုယ်စားလှယ်၏ စွမ်းဆောင်ရည်များကို ပိုမိုတိုးတက်စေရန် exponentiation သို့မဟုတ် logarithmic function ကဲ့သို့သော သင်္ချာကိရိယာများကို ထပ်မံထည့်သွင်း၍ စမ်းသပ်နိုင်ပါသည်။

**အကြောင်းကြားချက်**  
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) ဖြင့် ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးစားသော်လည်း အလိုအလျောက် ဘာသာပြန်ခြင်းတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် မေတ္တာရပ်ခံအပ်ပါသည်။ မူရင်းစာတမ်းကို မူလဘာသာဖြင့်သာ တရားဝင်အချက်အလက်အဖြစ် ယူဆသင့်ပါသည်။ အရေးကြီးသော အချက်အလက်များအတွက် လူ့ဘာသာပြန်ပညာရှင်မှ ဘာသာပြန်ခြင်းကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုရာမှ ဖြစ်ပေါ်လာနိုင်သည့် နားလည်မှုမှားယွင်းမှုများအတွက် ကျွန်ုပ်တို့သည် တာဝန်မခံပါ။