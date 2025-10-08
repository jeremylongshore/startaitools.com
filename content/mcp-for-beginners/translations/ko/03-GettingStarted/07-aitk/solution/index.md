<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:45:54+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "ko"
}
-->
# 📘 과제 해결: 제곱근 도구로 계산기 MCP 서버 확장하기

## 개요
이번 과제에서는 계산기 MCP 서버에 숫자의 제곱근을 계산하는 새로운 도구를 추가했습니다. 이를 통해 AI 에이전트가 "16의 제곱근은 무엇인가요?" 또는 "√49를 계산해 주세요"와 같은 자연어 질문에 더 복잡한 수학 문제를 처리할 수 있게 되었습니다.

## 🛠️ 제곱근 도구 구현하기
이 기능을 추가하기 위해 server.py 파일에 새로운 도구 함수를 정의했습니다. 구현 내용은 다음과 같습니다:

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

## 🔍 동작 원리

- **`math` 모듈 임포트**: 기본 산술 연산을 넘어선 수학 연산을 수행하기 위해 Python 내장 `math` 모듈을 사용합니다. 이 모듈에는 다양한 수학 함수와 상수가 포함되어 있습니다. `import math`로 불러오면 숫자의 제곱근을 계산하는 `math.sqrt()` 같은 함수를 사용할 수 있습니다.
- **함수 정의**: `@server.tool()` 데코레이터는 `sqrt` 함수를 AI 에이전트가 사용할 수 있는 도구로 등록합니다.
- **입력 매개변수**: 함수는 `float` 타입의 단일 인자 `a`를 받습니다.
- **오류 처리**: `a`가 음수일 경우, `math.sqrt()`가 지원하지 않으므로 `ValueError`를 발생시켜 음수 제곱근 계산을 방지합니다.
- **반환 값**: 음수가 아닌 입력에 대해 Python 내장 `math.sqrt()` 메서드를 사용해 `a`의 제곱근을 반환합니다.

## 🔄 서버 재시작
새로운 `sqrt` 도구를 추가한 후에는 MCP 서버를 재시작하여 에이전트가 새 기능을 인식하고 사용할 수 있도록 해야 합니다.

## 💬 새 도구 테스트용 예시 프롬프트
다음과 같은 자연어 문장으로 제곱근 기능을 테스트할 수 있습니다:

- "25의 제곱근은 무엇인가요?"
- "81의 제곱근을 계산해 주세요."
- "0의 제곱근을 찾아 주세요."
- "2.25의 제곱근은 얼마인가요?"

이 프롬프트들은 에이전트가 `sqrt` 도구를 호출해 올바른 결과를 반환하도록 유도합니다.

## ✅ 요약
이번 과제를 통해 다음을 달성했습니다:

- 계산기 MCP 서버에 새로운 `sqrt` 도구를 추가했습니다.
- AI 에이전트가 자연어 프롬프트를 통해 제곱근 계산을 수행할 수 있게 했습니다.
- 새로운 도구를 추가하고 서버를 재시작하여 기능을 통합하는 과정을 익혔습니다.

더 나아가 지수 함수나 로그 함수 같은 수학 도구를 추가해 에이전트의 기능을 계속 확장해 보세요!

**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있으나, 자동 번역에는 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원문은 해당 언어의 원본 문서가 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우 전문적인 인간 번역을 권장합니다. 본 번역의 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.