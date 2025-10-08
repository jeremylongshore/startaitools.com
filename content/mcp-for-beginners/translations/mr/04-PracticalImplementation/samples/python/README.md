<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "706b9b075dc484b73a053e6e9c709b4b",
  "translation_date": "2025-07-13T23:31:37+00:00",
  "source_file": "04-PracticalImplementation/samples/python/README.md",
  "language_code": "mr"
}
-->
# Model Context Protocol (MCP) Python अंमलबजावणी

हा रेपॉझिटरी Model Context Protocol (MCP) ची Python मध्ये अंमलबजावणी करतो, ज्यात दाखवले आहे की कसे एक सर्व्हर आणि क्लायंट अ‍ॅप्लिकेशन तयार करायचे जे MCP स्टँडर्ड वापरून संवाद साधतात.

## आढावा

MCP अंमलबजावणीमध्ये दोन मुख्य घटक आहेत:

1. **MCP Server (`server.py`)** - एक सर्व्हर जो खालील गोष्टी उपलब्ध करतो:
   - **Tools**: दूरस्थपणे कॉल करता येणाऱ्या फंक्शन्स
   - **Resources**: मिळवता येणारी माहिती
   - **Prompts**: भाषा मॉडेलसाठी प्रॉम्प्ट तयार करण्यासाठी टेम्पलेट्स

2. **MCP Client (`client.py`)** - एक क्लायंट अ‍ॅप्लिकेशन जे सर्व्हरशी कनेक्ट होते आणि त्याच्या फिचर्स वापरते

## वैशिष्ट्ये

ही अंमलबजावणी MCP चे काही महत्त्वाचे वैशिष्ट्ये दाखवते:

### Tools
- `completion` - AI मॉडेल्सकडून मजकूर पूर्ण करणे (सिम्युलेटेड)
- `add` - दोन संख्यांची बेरीज करणारा सोपा कॅल्क्युलेटर

### Resources
- `models://` - उपलब्ध AI मॉडेल्सची माहिती परत करते
- `greeting://{name}` - दिलेल्या नावासाठी वैयक्तिकृत अभिवादन परत करते

### Prompts
- `review_code` - कोड पुनरावलोकनासाठी प्रॉम्प्ट तयार करते

## इन्स्टॉलेशन

ही MCP अंमलबजावणी वापरण्यासाठी आवश्यक पॅकेजेस इन्स्टॉल करा:

```powershell
pip install mcp-server mcp-client
```

## सर्व्हर आणि क्लायंट चालविणे

### सर्व्हर सुरू करणे

एका टर्मिनल विंडोमध्ये सर्व्हर चालवा:

```powershell
python server.py
```

सर्व्हर MCP CLI वापरून विकास मोडमध्ये देखील चालवता येतो:

```powershell
mcp dev server.py
```

किंवा Claude Desktop मध्ये इन्स्टॉल करा (जर उपलब्ध असेल तर):

```powershell
mcp install server.py
```

### क्लायंट चालविणे

दुसऱ्या टर्मिनल विंडोमध्ये क्लायंट चालवा:

```powershell
python client.py
```

हे सर्व्हरशी कनेक्ट होईल आणि उपलब्ध सर्व फिचर्स दाखवेल.

### क्लायंट वापर

क्लायंट (`client.py`) MCP च्या सर्व क्षमतांचा वापर दाखवतो:

```powershell
python client.py
```

हे सर्व्हरशी कनेक्ट होईल आणि टूल्स, रिसोर्सेस, आणि प्रॉम्प्टसह सर्व फिचर्स वापरेल. आउटपुटमध्ये दिसेल:

1. कॅल्क्युलेटर टूलचा निकाल (5 + 7 = 12)
2. "What is the meaning of life?" या प्रश्नावर completion टूलचा प्रतिसाद
3. उपलब्ध AI मॉडेल्सची यादी
4. "MCP Explorer" साठी वैयक्तिकृत अभिवादन
5. कोड पुनरावलोकन प्रॉम्प्ट टेम्पलेट

## अंमलबजावणी तपशील

सर्व्हर `FastMCP` API वापरून तयार केला आहे, जो MCP सेवा परिभाषित करण्यासाठी उच्चस्तरीय संकल्पना पुरवतो. टूल्स कसे परिभाषित करतात याचे एक सोपे उदाहरण:

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of the two numbers
    """
    logger.info(f"Adding {a} and {b}")
    return a + b
```

क्लायंट MCP क्लायंट लायब्ररी वापरून सर्व्हरशी कनेक्ट होतो आणि कॉल करतो:

```python
async with stdio_client(server_params) as (reader, writer):
    async with ClientSession(reader, writer) as session:
        await session.initialize()
        result = await session.call_tool("add", arguments={"a": 5, "b": 7})
```

## अधिक जाणून घ्या

MCP बद्दल अधिक माहितीसाठी भेट द्या: https://modelcontextprotocol.io/

**अस्वीकरण**:  
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित केला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये चुका किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी अनुवाद करण्याची शिफारस केली जाते. या अनुवादाच्या वापरामुळे उद्भवलेल्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थलागी आम्ही जबाबदार नाही.