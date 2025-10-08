<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:51:32+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "ne"
}
-->
# 📘 असाइनमेन्ट समाधान: तपाईँको क्याल्कुलेटर MCP सर्भरमा स्क्वायर रुट टुल थप्दै

## अवलोकन
यस असाइनमेन्टमा, तपाईँले आफ्नो क्याल्कुलेटर MCP सर्भरमा एउटा नयाँ टुल थप्नुभयो जसले कुनै संख्याको वर्गमूल निकाल्छ। यसले तपाईँको AI एजेन्टलाई "१६ को वर्गमूल के हो?" वा "√४९ गणना गर" जस्ता उन्नत गणितीय प्रश्नहरू प्राकृतिक भाषामा बुझ्न र समाधान गर्न सक्षम बनाउँछ।

## 🛠️ स्क्वायर रुट टुल कार्यान्वयन
यो कार्यक्षमता थप्नका लागि, तपाईँले आफ्नो server.py फाइलमा नयाँ टुल फङ्सन परिभाषित गर्नुभयो। यहाँ यसको कार्यान्वयन छ:

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

## 🔍 यो कसरी काम गर्छ

- **`math` मोड्युल आयात गर्नुहोस्**: आधारभूत अंकगणितभन्दा माथिका गणितीय अपरेसनहरू गर्नका लागि, Python ले `math` नामक बिल्ट-इन मोड्युल प्रदान गर्छ। यसमा विभिन्न गणितीय फङ्सन र स्थिरांकहरू हुन्छन्। `import math` गरेर, तपाईँले `math.sqrt()` जस्ता फङ्सनहरू प्रयोग गर्न सक्नुहुन्छ, जसले कुनै संख्याको वर्गमूल निकाल्छ।
- **फङ्सन परिभाषा**: `@server.tool()` डेकोरेटरले `sqrt` फङ्सनलाई तपाईँको AI एजेन्टले पहुँच गर्न सक्ने टुलको रूपमा दर्ता गर्छ।
- **इनपुट प्यारामिटर**: फङ्सनले `float` प्रकारको एक मात्र आर्गुमेन्ट `a` लिन्छ।
- **त्रुटि व्यवस्थापन**: यदि `a` ऋणात्मक छ भने, फङ्सनले `ValueError` उठाउँछ किनभने `math.sqrt()` ले ऋणात्मक संख्याको वर्गमूल निकाल्न सक्दैन।
- **रिटर्न मान**: गैर-ऋणात्मक इनपुटका लागि, फङ्सनले Python को बिल्ट-इन `math.sqrt()` विधि प्रयोग गरी `a` को वर्गमूल फर्काउँछ।

## 🔄 सर्भर पुनः सुरु गर्नुहोस्
नयाँ `sqrt` टुल थपिसकेपछि, तपाईँको MCP सर्भर पुनः सुरु गर्नु आवश्यक छ ताकि एजेन्टले नयाँ कार्यक्षमता चिन्न र प्रयोग गर्न सकोस्।

## 💬 नयाँ टुल परीक्षण गर्नका लागि उदाहरण प्रॉम्प्टहरू
स्क्वायर रुट कार्यक्षमता परीक्षण गर्नका लागि यी प्राकृतिक भाषा प्रॉम्प्टहरू प्रयोग गर्न सक्नुहुन्छ:

- "२५ को वर्गमूल के हो?"
- "८१ को वर्गमूल गणना गर।"
- "० को वर्गमूल फेला पार।"
- "२.२५ को वर्गमूल के हो?"

यी प्रॉम्प्टहरूले एजेन्टलाई `sqrt` टुल कल गर्न र सही परिणाम फर्काउन प्रेरित गर्नेछन्।

## ✅ सारांश
यस असाइनमेन्ट पूरा गरेर, तपाईँले:

- आफ्नो क्याल्कुलेटर MCP सर्भरमा नयाँ `sqrt` टुल थप्नुभयो।
- तपाईँको AI एजेन्टलाई प्राकृतिक भाषा प्रॉम्प्टमार्फत वर्गमूल गणना गर्न सक्षम बनाउनुभयो।
- नयाँ टुलहरू थप्ने र सर्भर पुनः सुरु गर्ने अभ्यास गर्नुभयो।

आफ्नो एजेन्टको क्षमता अझै बढाउन exponentiation वा logarithmic फङ्सनहरू जस्ता थप गणितीय टुलहरू थपेर थप प्रयोग गर्न नहिचकिचाउनुहोस्!

**अस्वीकरण**:  
यो दस्तावेज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी शुद्धताका लागि प्रयासरत छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटि वा अशुद्धता हुन सक्छ। मूल दस्तावेज यसको मूल भाषामा नै अधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलतफहमी वा गलत व्याख्याका लागि हामी जिम्मेवार छैनौं।