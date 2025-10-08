<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:51:23+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "mr"
}
-->
# 📘 असाइनमेंट सोल्यूशन: तुमच्या कॅल्क्युलेटर MCP सर्व्हरमध्ये स्क्वेअर रूट टूल जोडणे

## आढावा
या असाइनमेंटमध्ये, तुम्ही तुमच्या कॅल्क्युलेटर MCP सर्व्हरमध्ये एक नवीन टूल जोडले जे एखाद्या संख्येचा वर्गमुळ (square root) काढते. या वाढीमुळे तुमचा AI एजंट अधिक प्रगत गणितीय प्रश्न हाताळू शकतो, जसे की "16 चा वर्गमुळ काय आहे?" किंवा "√49 काढा," नैसर्गिक भाषेतील प्रश्न वापरून.

## 🛠️ स्क्वेअर रूट टूलची अंमलबजावणी
ही कार्यक्षमता जोडण्यासाठी, तुम्ही तुमच्या server.py फाईलमध्ये एक नवीन टूल फंक्शन परिभाषित केले. अंमलबजावणी अशी आहे:

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

## 🔍 हे कसे कार्य करते

- **`math` मॉड्यूल इम्पोर्ट करा**: मूलभूत अंकगणितापलीकडील गणितीय ऑपरेशन्ससाठी, Python मध्ये अंगभूत `math` मॉड्यूल उपलब्ध आहे. या मॉड्यूलमध्ये विविध गणितीय फंक्शन्स आणि स्थिरांक असतात. `import math` वापरून तुम्हाला `math.sqrt()` सारख्या फंक्शन्सचा वापर करता येतो, जे एखाद्या संख्येचा वर्गमुळ काढते.
- **फंक्शन परिभाषा**: `@server.tool()` डेकोरेटर `sqrt` फंक्शनला टूल म्हणून नोंदवतो, ज्याचा वापर तुमचा AI एजंट करू शकतो.
- **इनपुट पॅरामीटर**: फंक्शन एकच `a` नावाचा `float` प्रकाराचा आर्ग्युमेंट स्वीकारतो.
- **त्रुटी हाताळणी**: जर `a` नकारात्मक असेल, तर फंक्शन `ValueError` उचलते, कारण `math.sqrt()` नकारात्मक संख्येचा वर्गमुळ काढू शकत नाही.
- **परतावा मूल्य**: नकारात्मक नसलेल्या इनपुटसाठी, फंक्शन Python च्या `math.sqrt()` मेथडचा वापर करून `a` चा वर्गमुळ परत करते.

## 🔄 सर्व्हर पुन्हा सुरू करणे
नवीन `sqrt` टूल जोडल्यावर, तुमचा MCP सर्व्हर पुन्हा सुरू करणे आवश्यक आहे जेणेकरून एजंट नवीन कार्यक्षमता ओळखू शकेल आणि वापरू शकेल.

## 💬 नवीन टूल तपासण्यासाठी उदाहरण प्रश्न
स्क्वेअर रूट फंक्शन तपासण्यासाठी खालील नैसर्गिक भाषेतील प्रश्न वापरू शकता:

- "25 चा वर्गमुळ काय आहे?"
- "81 चा वर्गमुळ काढा."
- "0 चा वर्गमुळ शोधा."
- "2.25 चा वर्गमुळ काय आहे?"

हे प्रश्न एजंटला `sqrt` टूल वापरून योग्य उत्तर देण्यासाठी प्रेरित करतील.

## ✅ सारांश
हा असाइनमेंट पूर्ण करून, तुम्ही:

- तुमच्या कॅल्क्युलेटर MCP सर्व्हरमध्ये नवीन `sqrt` टूल जोडले आहे.
- तुमच्या AI एजंटला नैसर्गिक भाषेतील प्रश्नांद्वारे वर्गमुळ काढण्याची क्षमता दिली आहे.
- नवीन टूल्स जोडण्याचा आणि सर्व्हर पुन्हा सुरू करण्याचा सराव केला आहे ज्यामुळे अतिरिक्त कार्यक्षमता समाकलित करता येते.

तुमच्या एजंटच्या क्षमतांना अजून वाढवण्यासाठी, घातांक (exponentiation) किंवा लघुगणकीय (logarithmic) फंक्शन्ससारखे आणखी गणितीय टूल्स जोडून प्रयोग करत राहा!

**अस्वीकरण**:  
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित केला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये चुका किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी अनुवाद करण्याची शिफारस केली जाते. या अनुवादाच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थलागी आम्ही जबाबदार नाही.