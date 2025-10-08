<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:45:16+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "zh"
}
-->
# 📘 作业解决方案：为你的计算器 MCP 服务器添加平方根工具

## 概述
在本次作业中，你通过添加一个计算数字平方根的新工具，增强了你的计算器 MCP 服务器。这个新增功能使你的 AI 代理能够处理更复杂的数学问题，比如“16 的平方根是多少？”或“计算 √49”，并通过自然语言提示完成计算。

## 🛠️ 实现平方根工具
为了实现这个功能，你在 server.py 文件中定义了一个新的工具函数。实现代码如下：

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

## 🔍 工作原理

- **导入 `math` 模块**：为了执行基本算术之外的数学运算，Python 提供了内置的 `math` 模块。该模块包含多种数学函数和常量。通过 `import math` 导入后，你可以使用如 `math.sqrt()` 这样的函数来计算数字的平方根。
- **函数定义**：使用 `@server.tool()` 装饰器将 `sqrt` 函数注册为 AI 代理可调用的工具。
- **输入参数**：该函数接受一个类型为 `float` 的参数 `a`。
- **错误处理**：如果 `a` 为负数，函数会抛出 `ValueError`，以防止计算负数的平方根，因为 `math.sqrt()` 不支持负数输入。
- **返回值**：对于非负输入，函数使用 Python 内置的 `math.sqrt()` 方法返回 `a` 的平方根。

## 🔄 重启服务器
添加新的 `sqrt` 工具后，务必重启 MCP 服务器，以确保代理能够识别并使用新增的功能。

## 💬 测试新工具的示例提示
以下是一些可以用来测试平方根功能的自然语言提示：

- “25 的平方根是多少？”
- “计算 81 的平方根。”
- “求 0 的平方根。”
- “2.25 的平方根是多少？”

这些提示应触发代理调用 `sqrt` 工具并返回正确结果。

## ✅ 总结
通过完成本次作业，你已经：

- 为计算器 MCP 服务器扩展了新的 `sqrt` 工具。
- 使 AI 代理能够通过自然语言提示处理平方根计算。
- 练习了添加新工具并重启服务器以集成新功能。

欢迎继续尝试添加更多数学工具，比如指数运算或对数函数，进一步提升你的代理能力！

**免责声明**：  
本文件使用 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 进行翻译。虽然我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始文件的母语版本应被视为权威来源。对于重要信息，建议使用专业人工翻译。对于因使用本翻译而产生的任何误解或误释，我们不承担任何责任。