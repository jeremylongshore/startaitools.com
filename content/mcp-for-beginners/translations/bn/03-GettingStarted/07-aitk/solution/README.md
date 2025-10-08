<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:46:11+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "bn"
}
-->
# 📘 অ্যাসাইনমেন্ট সমাধান: আপনার Calculator MCP সার্ভারে একটি স্কয়ার রুট টুল যোগ করা

## ওভারভিউ
এই অ্যাসাইনমেন্টে, আপনি আপনার calculator MCP সার্ভারকে উন্নত করেছেন একটি নতুন টুল যোগ করে যা একটি সংখ্যার বর্গমূল নির্ণয় করে। এই সংযোজনের মাধ্যমে আপনার AI এজেন্ট আরও জটিল গাণিতিক প্রশ্ন যেমন "16 এর বর্গমূল কত?" বা "√49 হিসাব করো" প্রাকৃতিক ভাষার মাধ্যমে বুঝতে এবং সমাধান করতে সক্ষম হবে।

## 🛠️ স্কয়ার রুট টুল বাস্তবায়ন
এই ফাংশনালিটি যোগ করার জন্য, আপনি আপনার server.py ফাইলে একটি নতুন টুল ফাংশন সংজ্ঞায়িত করেছেন। এখানে তার বাস্তবায়ন:

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

## 🔍 এটি কীভাবে কাজ করে

- **`math` মডিউল ইমপোর্ট করা**: মৌলিক গণিতের বাইরে আরও জটিল গাণিতিক অপারেশন করার জন্য, পাইথন বিল্ট-ইন `math` মডিউল প্রদান করে। এই মডিউলে বিভিন্ন গাণিতিক ফাংশন এবং ধ্রুবক থাকে। `import math` ব্যবহার করে এটি ইমপোর্ট করলে আপনি `math.sqrt()` এর মতো ফাংশন ব্যবহার করতে পারবেন, যা একটি সংখ্যার বর্গমূল নির্ণয় করে।
- **ফাংশন সংজ্ঞা**: `@server.tool()` ডেকোরেটর `sqrt` ফাংশনটিকে একটি টুল হিসেবে রেজিস্টার করে যা আপনার AI এজেন্ট ব্যবহার করতে পারে।
- **ইনপুট প্যারামিটার**: ফাংশনটি একটি মাত্র আর্গুমেন্ট `a` গ্রহণ করে, যার টাইপ `float`।
- **ত্রুটি পরিচালনা**: যদি `a` নেতিবাচক হয়, তাহলে ফাংশনটি `ValueError` ছুঁড়ে দেয় কারণ নেতিবাচক সংখ্যার বর্গমূল গণনা `math.sqrt()` ফাংশন দ্বারা সমর্থিত নয়।
- **রিটার্ন মান**: নেতিবাচক নয় এমন ইনপুটের জন্য, ফাংশনটি পাইথনের বিল্ট-ইন `math.sqrt()` পদ্ধতি ব্যবহার করে `a` এর বর্গমূল রিটার্ন করে।

## 🔄 সার্ভার পুনরায় চালু করা
নতুন `sqrt` টুল যোগ করার পর, MCP সার্ভার পুনরায় চালু করা জরুরি যাতে এজেন্ট নতুন ফাংশনালিটি চিনতে পারে এবং ব্যবহার করতে পারে।

## 💬 নতুন টুল পরীক্ষা করার জন্য উদাহরণ প্রম্পট
স্কয়ার রুট ফাংশনালিটি পরীক্ষা করার জন্য নিচের প্রাকৃতিক ভাষার প্রম্পটগুলো ব্যবহার করতে পারেন:

- "25 এর বর্গমূল কত?"
- "81 এর বর্গমূল হিসাব করো।"
- "0 এর বর্গমূল খুঁজে বের করো।"
- "2.25 এর বর্গমূল কত?"

এই প্রম্পটগুলো এজেন্টকে `sqrt` টুল কল করতে এবং সঠিক ফলাফল প্রদান করতে উৎসাহিত করবে।

## ✅ সারাংশ
এই অ্যাসাইনমেন্ট সম্পন্ন করে আপনি:

- আপনার calculator MCP সার্ভারে একটি নতুন `sqrt` টুল যোগ করেছেন।
- আপনার AI এজেন্টকে প্রাকৃতিক ভাষার মাধ্যমে বর্গমূল হিসাব করার ক্ষমতা দিয়েছেন।
- নতুন টুল যোগ করা এবং সার্ভার পুনরায় চালু করার মাধ্যমে অতিরিক্ত ফাংশনালিটি সংযুক্ত করার অভিজ্ঞতা অর্জন করেছেন।

আপনার এজেন্টের ক্ষমতা আরও বাড়াতে exponentiation বা logarithmic ফাংশনের মতো আরও গাণিতিক টুল যোগ করে পরীক্ষা চালিয়ে যেতে পারেন!

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ সেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। আমরা যথাসাধ্য সঠিকতার চেষ্টা করি, তবে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার নিজস্ব ভাষায়ই কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ গ্রহণ করার পরামর্শ দেওয়া হয়। এই অনুবাদের ব্যবহারে সৃষ্ট কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।