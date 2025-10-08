<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:46:02+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "hi"
}
-->
# 📘 असाइनमेंट समाधान: अपने कैलकुलेटर MCP सर्वर को स्क्वायर रूट टूल के साथ बढ़ाना

## अवलोकन
इस असाइनमेंट में, आपने अपने कैलकुलेटर MCP सर्वर को एक नए टूल से बढ़ाया है जो किसी संख्या का वर्गमूल निकालता है। इस जोड़ से आपका AI एजेंट अधिक उन्नत गणितीय प्रश्नों को समझ और हल कर सकता है, जैसे "16 का वर्गमूल क्या है?" या "√49 की गणना करें," प्राकृतिक भाषा के संकेतों का उपयोग करके।

## 🛠️ स्क्वायर रूट टूल को लागू करना
इस फ़ंक्शन को जोड़ने के लिए, आपने अपने server.py फ़ाइल में एक नया टूल फ़ंक्शन परिभाषित किया। यहाँ इसका कार्यान्वयन है:

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

## 🔍 यह कैसे काम करता है

- **`math` मॉड्यूल को इम्पोर्ट करें**: बुनियादी अंकगणित से परे गणितीय ऑपरेशन करने के लिए, Python में बिल्ट-इन `math` मॉड्यूल उपलब्ध है। इस मॉड्यूल में कई गणितीय फ़ंक्शन और स्थिरांक होते हैं। `import math` के माध्यम से इसे इम्पोर्ट करने पर आप `math.sqrt()` जैसे फ़ंक्शन का उपयोग कर सकते हैं, जो किसी संख्या का वर्गमूल निकालता है।
- **फ़ंक्शन परिभाषा**: `@server.tool()` डेकोरेटर `sqrt` फ़ंक्शन को एक टूल के रूप में पंजीकृत करता है जिसे आपका AI एजेंट उपयोग कर सकता है।
- **इनपुट पैरामीटर**: यह फ़ंक्शन एक ही तर्क `a` लेता है, जिसका प्रकार `float` है।
- **त्रुटि प्रबंधन**: यदि `a` ऋणात्मक है, तो फ़ंक्शन `ValueError` उठाता है ताकि ऋणात्मक संख्या का वर्गमूल निकालने से रोका जा सके, क्योंकि `math.sqrt()` इसे सपोर्ट नहीं करता।
- **रिटर्न मान**: गैर-ऋणात्मक इनपुट के लिए, यह फ़ंक्शन Python के बिल्ट-इन `math.sqrt()` मेथड का उपयोग करके `a` का वर्गमूल लौटाता है।

## 🔄 सर्वर को पुनः प्रारंभ करना
नया `sqrt` टूल जोड़ने के बाद, यह आवश्यक है कि आप अपने MCP सर्वर को पुनः प्रारंभ करें ताकि एजेंट नई कार्यक्षमता को पहचान सके और उसका उपयोग कर सके।

## 💬 नए टूल का परीक्षण करने के लिए उदाहरण प्रॉम्प्ट
यहाँ कुछ प्राकृतिक भाषा के प्रॉम्प्ट दिए गए हैं जिनका उपयोग आप स्क्वायर रूट फ़ंक्शन की जांच के लिए कर सकते हैं:

- "25 का वर्गमूल क्या है?"
- "81 का वर्गमूल निकालो।"
- "0 का वर्गमूल खोजो।"
- "2.25 का वर्गमूल क्या है?"

ये प्रॉम्प्ट एजेंट को `sqrt` टूल को कॉल करने और सही परिणाम लौटाने के लिए प्रेरित करेंगे।

## ✅ सारांश
इस असाइनमेंट को पूरा करके, आपने:

- अपने कैलकुलेटर MCP सर्वर को नए `sqrt` टूल के साथ बढ़ाया है।
- अपने AI एजेंट को प्राकृतिक भाषा के प्रॉम्प्ट के माध्यम से वर्गमूल की गणना करने में सक्षम बनाया है।
- नए टूल जोड़ने और सर्वर को पुनः प्रारंभ करने का अभ्यास किया है ताकि अतिरिक्त कार्यक्षमताएँ जोड़ी जा सकें।

आप और भी गणितीय टूल जैसे घातांक या लघुगणकीय फ़ंक्शन जोड़कर अपने एजेंट की क्षमताओं को और बढ़ाने के लिए स्वतंत्र हैं!

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही अधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।