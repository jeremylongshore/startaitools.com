<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:51:42+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "pa"
}
-->
# 📘 ਅਸਾਈਨਮੈਂਟ ਹੱਲ: ਆਪਣੇ ਕੈਲਕੁਲੇਟਰ MCP ਸਰਵਰ ਵਿੱਚ ਵਰਗਮੂਲ ਟੂਲ ਸ਼ਾਮਲ ਕਰਨਾ

## ਝਲਕ
ਇਸ ਅਸਾਈਨਮੈਂਟ ਵਿੱਚ, ਤੁਸੀਂ ਆਪਣੇ ਕੈਲਕੁਲੇਟਰ MCP ਸਰਵਰ ਨੂੰ ਇੱਕ ਨਵਾਂ ਟੂਲ ਜੋੜ ਕੇ ਸੁਧਾਰਿਆ ਹੈ ਜੋ ਕਿਸੇ ਸੰਖਿਆ ਦਾ ਵਰਗਮੂਲ ਕੱਢਦਾ ਹੈ। ਇਸ ਨਾਲ ਤੁਹਾਡਾ AI ਏਜੰਟ ਹੋਰ ਉੱਚ ਦਰਜੇ ਦੇ ਗਣਿਤੀ ਪ੍ਰਸ਼ਨਾਂ ਨੂੰ ਸਮਝ ਕੇ ਜਵਾਬ ਦੇ ਸਕਦਾ ਹੈ, ਜਿਵੇਂ "16 ਦਾ ਵਰਗਮੂਲ ਕੀ ਹੈ?" ਜਾਂ "√49 ਕੱਢੋ," ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਦੇ ਪ੍ਰੰਪਟਾਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ।

## 🛠️ ਵਰਗਮੂਲ ਟੂਲ ਲਾਗੂ ਕਰਨਾ
ਇਸ ਫੰਕਸ਼ਨਲਿਟੀ ਨੂੰ ਸ਼ਾਮਲ ਕਰਨ ਲਈ, ਤੁਸੀਂ ਆਪਣੇ server.py ਫਾਇਲ ਵਿੱਚ ਇੱਕ ਨਵਾਂ ਟੂਲ ਫੰਕਸ਼ਨ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤਾ। ਇੱਥੇ ਇਸ ਦੀ ਲਾਗੂਆਤ ਹੈ:

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

## 🔍 ਇਹ ਕਿਵੇਂ ਕੰਮ ਕਰਦਾ ਹੈ

- **`math` ਮੋਡੀਊਲ ਨੂੰ ਇੰਪੋਰਟ ਕਰੋ**: ਬੁਨਿਆਦੀ ਗਣਿਤ ਤੋਂ ਅੱਗੇ ਗਣਿਤੀ ਕਾਰਵਾਈਆਂ ਕਰਨ ਲਈ, Python ਵਿੱਚ built-in `math` ਮੋਡੀਊਲ ਹੈ। ਇਸ ਮੋਡੀਊਲ ਵਿੱਚ ਕਈ ਗਣਿਤੀ ਫੰਕਸ਼ਨ ਅਤੇ ਸਥਿਰਾਂ ਹਨ। `import math` ਕਰਕੇ ਤੁਸੀਂ `math.sqrt()` ਵਰਗੇ ਫੰਕਸ਼ਨਾਂ ਤੱਕ ਪਹੁੰਚ ਪ੍ਰਾਪਤ ਕਰਦੇ ਹੋ, ਜੋ ਕਿਸੇ ਸੰਖਿਆ ਦਾ ਵਰਗਮੂਲ ਕੱਢਦਾ ਹੈ।
- **ਫੰਕਸ਼ਨ ਪਰਿਭਾਸ਼ਾ**: `@server.tool()` ਡੈਕੋਰੇਟਰ `sqrt` ਫੰਕਸ਼ਨ ਨੂੰ ਇੱਕ ਟੂਲ ਵਜੋਂ ਦਰਜ ਕਰਦਾ ਹੈ ਜੋ ਤੁਹਾਡੇ AI ਏਜੰਟ ਲਈ ਉਪਲਬਧ ਹੈ।
- **ਇਨਪੁੱਟ ਪੈਰਾਮੀਟਰ**: ਫੰਕਸ਼ਨ ਇੱਕ ਹੀ ਆਰਗੁਮੈਂਟ `a` ਲੈਂਦਾ ਹੈ ਜੋ `float` ਕਿਸਮ ਦਾ ਹੁੰਦਾ ਹੈ।
- **ਗਲਤੀ ਸੰਭਾਲਣਾ**: ਜੇ `a` ਨਕਾਰਾਤਮਕ ਹੈ, ਤਾਂ ਫੰਕਸ਼ਨ `ValueError` ਉਠਾਉਂਦਾ ਹੈ ਤਾਂ ਜੋ ਨਕਾਰਾਤਮਕ ਸੰਖਿਆ ਦਾ ਵਰਗਮੂਲ ਕੱਢਣ ਤੋਂ ਰੋਕਿਆ ਜਾ ਸਕੇ, ਕਿਉਂਕਿ `math.sqrt()` ਇਸ ਨੂੰ ਸਹਿਯੋਗ ਨਹੀਂ ਦਿੰਦਾ।
- **ਵਾਪਸੀ ਮੁੱਲ**: ਗੈਰ-ਨਕਾਰਾਤਮਕ ਇਨਪੁੱਟ ਲਈ, ਫੰਕਸ਼ਨ Python ਦੇ built-in `math.sqrt()` ਮੈਥਡ ਦੀ ਵਰਤੋਂ ਕਰਕੇ `a` ਦਾ ਵਰਗਮੂਲ ਵਾਪਸ ਕਰਦਾ ਹੈ।

## 🔄 ਸਰਵਰ ਨੂੰ ਮੁੜ ਚਾਲੂ ਕਰਨਾ
ਨਵਾਂ `sqrt` ਟੂਲ ਸ਼ਾਮਲ ਕਰਨ ਤੋਂ ਬਾਅਦ, ਇਹ ਜਰੂਰੀ ਹੈ ਕਿ ਤੁਸੀਂ ਆਪਣੇ MCP ਸਰਵਰ ਨੂੰ ਮੁੜ ਚਾਲੂ ਕਰੋ ਤਾਂ ਜੋ ਏਜੰਟ ਨਵੀਂ ਫੰਕਸ਼ਨਲਿਟੀ ਨੂੰ ਪਛਾਣ ਸਕੇ ਅਤੇ ਇਸਦਾ ਸਹੀ ਤਰੀਕੇ ਨਾਲ ਇਸਤੇਮਾਲ ਕਰ ਸਕੇ।

## 💬 ਨਵੀਂ ਟੂਲ ਦੀ ਜਾਂਚ ਲਈ ਉਦਾਹਰਨ ਪ੍ਰੰਪਟ
ਇੱਥੇ ਕੁਝ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਦੇ ਪ੍ਰੰਪਟ ਹਨ ਜੋ ਤੁਸੀਂ ਵਰਗਮੂਲ ਫੰਕਸ਼ਨਲਿਟੀ ਦੀ ਜਾਂਚ ਲਈ ਵਰਤ ਸਕਦੇ ਹੋ:

- "25 ਦਾ ਵਰਗਮੂਲ ਕੀ ਹੈ?"
- "81 ਦਾ ਵਰਗਮੂਲ ਕੱਢੋ।"
- "0 ਦਾ ਵਰਗਮੂਲ ਲੱਭੋ।"
- "2.25 ਦਾ ਵਰਗਮੂਲ ਕੀ ਹੈ?"

ਇਹ ਪ੍ਰੰਪਟ ਏਜੰਟ ਨੂੰ `sqrt` ਟੂਲ ਨੂੰ ਕਾਲ ਕਰਨ ਲਈ ਪ੍ਰੇਰਿਤ ਕਰਨਗੇ ਅਤੇ ਸਹੀ ਨਤੀਜੇ ਵਾਪਸ ਕਰਨਗੇ।

## ✅ ਸਾਰ
ਇਸ ਅਸਾਈਨਮੈਂਟ ਨੂੰ ਪੂਰਾ ਕਰਕੇ, ਤੁਸੀਂ:

- ਆਪਣੇ ਕੈਲਕੁਲੇਟਰ MCP ਸਰਵਰ ਵਿੱਚ ਨਵਾਂ `sqrt` ਟੂਲ ਸ਼ਾਮਲ ਕੀਤਾ ਹੈ।
- ਆਪਣੇ AI ਏਜੰਟ ਨੂੰ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਦੇ ਪ੍ਰੰਪਟਾਂ ਰਾਹੀਂ ਵਰਗਮੂਲ ਦੀ ਗਣਨਾ ਕਰਨ ਯੋਗ ਬਣਾਇਆ ਹੈ।
- ਨਵੇਂ ਟੂਲ ਸ਼ਾਮਲ ਕਰਨ ਅਤੇ ਸਰਵਰ ਨੂੰ ਮੁੜ ਚਾਲੂ ਕਰਨ ਦਾ ਅਭਿਆਸ ਕੀਤਾ ਹੈ ਤਾਂ ਜੋ ਵਾਧੂ ਫੰਕਸ਼ਨਲਿਟੀ ਜੋੜੀ ਜਾ ਸਕੇ।

ਆਪਣੇ ਏਜੰਟ ਦੀ ਸਮਰੱਥਾ ਨੂੰ ਹੋਰ ਵਧਾਉਣ ਲਈ exponentiation ਜਾਂ logarithmic ਫੰਕਸ਼ਨਾਂ ਵਰਗੇ ਹੋਰ ਗਣਿਤੀ ਟੂਲ ਵੀ ਸ਼ਾਮਲ ਕਰਕੇ ਅਜ਼ਮਾਇਸ਼ ਜਾਰੀ ਰੱਖੋ!

**ਅਸਵੀਕਾਰੋਪਣ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦਿਤ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾ ਲਈ ਕੋਸ਼ਿਸ਼ ਕਰਦੇ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮਰਥਤਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਪ੍ਰਮਾਣਿਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਉਤਪੰਨ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆ ਲਈ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।