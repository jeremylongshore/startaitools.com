<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "dde4e32e4b55ef4962c411b39d2340a7",
  "translation_date": "2025-09-03T16:03:53+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/dotnet/README.md",
  "language_code": "ne"
}
-->
# यो नमूना चलाउनुहोस्

## -1- आवश्यकताहरू स्थापना गर्नुहोस्

```bash
dotnet restore
```

## -2- नमूना चलाउनुहोस्

```bash
dotnet run
```

## -3- नमूना परीक्षण गर्नुहोस्

तलको आदेश चलाउनु अघि छुट्टै टर्मिनल सुरु गर्नुहोस् (पक्का गर्नुहोस् कि सर्भर अझै चलिरहेको छ)।

सर्भर एक टर्मिनलमा चलिरहेको अवस्थामा, अर्को टर्मिनल खोल्नुहोस् र तलको आदेश चलाउनुहोस्:

```bash
npx @modelcontextprotocol/inspector http://localhost:3001
```

यसले दृश्य इन्टरफेससहितको वेब सर्भर सुरु गर्नुपर्छ जसले तपाईंलाई नमूना परीक्षण गर्न अनुमति दिन्छ।

> सुनिश्चित गर्नुहोस् कि **Streamable HTTP** ट्रान्सपोर्ट प्रकारको रूपमा चयन गरिएको छ, र URL `http://localhost:3001/mcp` हो।

सर्भर जडान भएपछि:

- उपकरणहरूको सूची बनाउने प्रयास गर्नुहोस् र `add` चलाउनुहोस्, 2 र 4 को आर्ग्ससहित, परिणाममा तपाईंले 6 देख्नुहुनेछ।
- स्रोतहरूमा जानुहोस् र स्रोत टेम्प्लेटमा "greeting" कल गर्नुहोस्, नाम टाइप गर्नुहोस् र तपाईंले प्रदान गरेको नामसहितको अभिवादन देख्नुहुनेछ।

### CLI मोडमा परीक्षण गर्दै

तपाईं यसलाई CLI मोडमा सिधै तलको आदेश चलाएर सुरु गर्न सक्नुहुन्छ:

```bash 
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/list
```

यसले सर्भरमा उपलब्ध सबै उपकरणहरूको सूची देखाउनेछ। तपाईंले निम्न आउटपुट देख्नुहुनेछ:

```text
{
  "tools": [
    {
      "name": "AddNumbers",
      "description": "Add two numbers together.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "description": "The first number",
            "type": "integer"
          },
          "b": {
            "description": "The second number",
            "type": "integer"
          }
        },
        "title": "AddNumbers",
        "description": "Add two numbers together.",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

एउटा उपकरण चलाउन टाइप गर्नुहोस्:

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/call --tool-name AddNumbers --tool-arg a=1 --tool-arg b=2
```

तपाईंले निम्न आउटपुट देख्नुहुनेछ:

```text
{
  "content": [
    {
      "type": "text",
      "text": "3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> ब्राउजरको तुलनामा CLI मोडमा निरीक्षक चलाउनु सामान्यतया धेरै छिटो हुन्छ।
> निरीक्षकको बारेमा थप पढ्नुहोस् [यहाँ](https://github.com/modelcontextprotocol/inspector)।

---

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी यथासम्भव सटीकता सुनिश्चित गर्न प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादहरूमा त्रुटि वा अशुद्धि हुन सक्छ। यसको मूल भाषामा रहेको मूल दस्तावेज़लाई आधिकारिक स्रोत मानिनुपर्छ। महत्त्वपूर्ण जानकारीका लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याका लागि हामी जिम्मेवार हुने छैनौं।  