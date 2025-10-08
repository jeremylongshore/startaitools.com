<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "706b9b075dc484b73a053e6e9c709b4b",
  "translation_date": "2025-07-13T23:31:46+00:00",
  "source_file": "04-PracticalImplementation/samples/python/README.md",
  "language_code": "ne"
}
-->
# Model Context Protocol (MCP) Python कार्यान्वयन

यो रिपोजिटरीमा Model Context Protocol (MCP) को Python कार्यान्वयन समावेश छ, जसले कसरी MCP मानक प्रयोग गरेर सर्भर र क्लाइन्ट एप्लिकेशन दुवै बनाउन सकिन्छ भन्ने देखाउँछ।

## अवलोकन

MCP कार्यान्वयन दुई मुख्य भागहरूमा विभाजित छ:

1. **MCP Server (`server.py`)** - एउटा सर्भर जसले प्रदान गर्छ:
   - **Tools**: रिमोटली कल गर्न सकिने फङ्सनहरू
   - **Resources**: प्राप्त गर्न सकिने डाटा
   - **Prompts**: भाषा मोडेलका लागि प्रॉम्प्टहरू तयार पार्ने टेम्प्लेटहरू

2. **MCP Client (`client.py`)** - एउटा क्लाइन्ट एप्लिकेशन जसले सर्भरसँग जडान भएर यसको सुविधाहरू प्रयोग गर्छ

## सुविधाहरू

यस कार्यान्वयनले MCP का केही मुख्य सुविधाहरू देखाउँछ:

### Tools
- `completion` - AI मोडेलबाट टेक्स्ट कम्प्लीसनहरू उत्पादन गर्छ (नक्कली)
- `add` - दुई संख्या जोड्ने सरल क्यालकुलेटर

### Resources
- `models://` - उपलब्ध AI मोडेलहरूको जानकारी फर्काउँछ
- `greeting://{name}` - दिइएको नामका लागि व्यक्तिगत अभिवादन फर्काउँछ

### Prompts
- `review_code` - कोड समीक्षा गर्नको लागि प्रॉम्प्ट तयार पार्छ

## स्थापना

यस MCP कार्यान्वयन प्रयोग गर्न, आवश्यक प्याकेजहरू इन्स्टल गर्नुहोस्:

```powershell
pip install mcp-server mcp-client
```

## सर्भर र क्लाइन्ट चलाउने तरिका

### सर्भर सुरु गर्ने

एउटा टर्मिनल विन्डोमा सर्भर चलाउनुहोस्:

```powershell
python server.py
```

सर्भरलाई विकास मोडमा MCP CLI प्रयोग गरेर पनि चलाउन सकिन्छ:

```powershell
mcp dev server.py
```

वा Claude Desktop मा इन्स्टल गरेर (यदि उपलब्ध छ भने):

```powershell
mcp install server.py
```

### क्लाइन्ट चलाउने

अर्को टर्मिनल विन्डोमा क्लाइन्ट चलाउनुहोस्:

```powershell
python client.py
```

यसले सर्भरसँग जडान गरी सबै उपलब्ध सुविधाहरू प्रदर्शन गर्नेछ।

### क्लाइन्ट प्रयोग

क्लाइन्ट (`client.py`) ले MCP का सबै क्षमता देखाउँछ:

```powershell
python client.py
```

यसले सर्भरसँग जडान गरी सबै सुविधाहरू जस्तै tools, resources, र prompts प्रयोग गर्नेछ। आउटपुटमा देखिनेछ:

1. क्यालकुलेटर टुलको नतिजा (5 + 7 = 12)
2. "What is the meaning of life?" को लागि completion टुलको प्रतिक्रिया
3. उपलब्ध AI मोडेलहरूको सूची
4. "MCP Explorer" को लागि व्यक्तिगत अभिवादन
5. कोड समीक्षा प्रॉम्प्ट टेम्प्लेट

## कार्यान्वयन विवरण

सर्भर `FastMCP` API प्रयोग गरेर बनाइएको छ, जसले MCP सेवाहरू परिभाषित गर्न उच्च स्तरका एब्स्ट्र्याक्सनहरू प्रदान गर्छ। यहाँ कसरी tools परिभाषित गरिन्छ भन्ने सरल उदाहरण छ:

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

क्लाइन्टले MCP क्लाइन्ट लाइब्रेरी प्रयोग गरेर सर्भरसँग जडान गरी कल गर्छ:

```python
async with stdio_client(server_params) as (reader, writer):
    async with ClientSession(reader, writer) as session:
        await session.initialize()
        result = await session.call_tool("add", arguments={"a": 5, "b": 7})
```

## थप जानकारी

MCP सम्बन्धी थप जानकारीका लागि यहाँ जानुहोस्: https://modelcontextprotocol.io/

**अस्वीकरण**:  
यो दस्तावेज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी शुद्धताका लागि प्रयासरत छौं भने पनि, कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटि वा अशुद्धता हुन सक्छ। मूल दस्तावेज यसको मूल भाषामा नै अधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलतफहमी वा गलत व्याख्याका लागि हामी जिम्मेवार छैनौं।