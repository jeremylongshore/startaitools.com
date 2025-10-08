<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "706b9b075dc484b73a053e6e9c709b4b",
  "translation_date": "2025-07-13T23:31:20+00:00",
  "source_file": "04-PracticalImplementation/samples/python/README.md",
  "language_code": "hi"
}
-->
# Model Context Protocol (MCP) Python इम्प्लीमेंटेशन

यह रिपॉजिटरी Model Context Protocol (MCP) का Python इम्प्लीमेंटेशन प्रदान करती है, जो दिखाती है कि कैसे MCP स्टैंडर्ड का उपयोग करके एक सर्वर और क्लाइंट एप्लिकेशन बनाया जा सकता है जो आपस में संवाद करते हैं।

## अवलोकन

MCP इम्प्लीमेंटेशन दो मुख्य घटकों से बना है:

1. **MCP Server (`server.py`)** - एक सर्वर जो प्रदान करता है:
   - **Tools**: ऐसे फ़ंक्शन जिन्हें रिमोटली कॉल किया जा सकता है
   - **Resources**: डेटा जिसे प्राप्त किया जा सकता है
   - **Prompts**: भाषा मॉडल के लिए प्रॉम्प्ट बनाने के टेम्पलेट्स

2. **MCP Client (`client.py`)** - एक क्लाइंट एप्लिकेशन जो सर्वर से कनेक्ट होता है और उसकी सुविधाओं का उपयोग करता है

## विशेषताएँ

यह इम्प्लीमेंटेशन MCP की कई मुख्य विशेषताओं को प्रदर्शित करता है:

### Tools
- `completion` - AI मॉडल से टेक्स्ट कम्प्लीशन्स जनरेट करता है (सिम्युलेटेड)
- `add` - एक सरल कैलकुलेटर जो दो नंबर जोड़ता है

### Resources
- `models://` - उपलब्ध AI मॉडलों की जानकारी लौटाता है
- `greeting://{name}` - दिए गए नाम के लिए व्यक्तिगत अभिवादन लौटाता है

### Prompts
- `review_code` - कोड समीक्षा के लिए प्रॉम्प्ट जनरेट करता है

## इंस्टॉलेशन

इस MCP इम्प्लीमेंटेशन का उपयोग करने के लिए आवश्यक पैकेज इंस्टॉल करें:

```powershell
pip install mcp-server mcp-client
```

## सर्वर और क्लाइंट चलाना

### सर्वर शुरू करना

सर्वर को एक टर्मिनल विंडो में चलाएं:

```powershell
python server.py
```

सर्वर को MCP CLI का उपयोग करके डेवलपमेंट मोड में भी चलाया जा सकता है:

```powershell
mcp dev server.py
```

या Claude Desktop में इंस्टॉल किया जा सकता है (यदि उपलब्ध हो):

```powershell
mcp install server.py
```

### क्लाइंट चलाना

क्लाइंट को दूसरी टर्मिनल विंडो में चलाएं:

```powershell
python client.py
```

यह सर्वर से कनेक्ट होगा और सभी उपलब्ध फीचर्स को प्रदर्शित करेगा।

### क्लाइंट उपयोग

क्लाइंट (`client.py`) MCP की सभी क्षमताओं को प्रदर्शित करता है:

```powershell
python client.py
```

यह सर्वर से कनेक्ट होगा और टूल्स, रिसोर्सेज़, और प्रॉम्प्ट्स सहित सभी फीचर्स का उपयोग करेगा। आउटपुट में दिखेगा:

1. कैलकुलेटर टूल का परिणाम (5 + 7 = 12)
2. "What is the meaning of life?" के लिए completion टूल का जवाब
3. उपलब्ध AI मॉडलों की सूची
4. "MCP Explorer" के लिए व्यक्तिगत अभिवादन
5. कोड समीक्षा प्रॉम्प्ट टेम्पलेट

## इम्प्लीमेंटेशन विवरण

सर्वर `FastMCP` API का उपयोग करके बनाया गया है, जो MCP सेवाओं को परिभाषित करने के लिए उच्च स्तरीय एब्स्ट्रैक्शन्स प्रदान करता है। यहाँ टूल्स को परिभाषित करने का एक सरल उदाहरण है:

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

क्लाइंट MCP क्लाइंट लाइब्रेरी का उपयोग करके सर्वर से कनेक्ट होता है और कॉल करता है:

```python
async with stdio_client(server_params) as (reader, writer):
    async with ClientSession(reader, writer) as session:
        await session.initialize()
        result = await session.call_tool("add", arguments={"a": 5, "b": 7})
```

## और जानें

MCP के बारे में अधिक जानकारी के लिए देखें: https://modelcontextprotocol.io/

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही अधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।