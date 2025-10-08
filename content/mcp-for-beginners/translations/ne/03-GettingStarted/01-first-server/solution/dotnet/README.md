<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "92af35e8c34923031f3d228dffad9ebb",
  "translation_date": "2025-09-03T16:04:20+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/dotnet/README.md",
  "language_code": "ne"
}
-->
# यो नमूना चलाउनुहोस्

## -1- आवश्यकताहरू स्थापना गर्नुहोस्

```bash
dotnet restore
```

## -3- नमूना चलाउनुहोस्

```bash
dotnet run
```

## -4- नमूना परीक्षण गर्नुहोस्

सर्भर एक टर्मिनलमा चलिरहेको अवस्थामा, अर्को टर्मिनल खोल्नुहोस् र निम्न कमाण्ड चलाउनुहोस्:

```bash
npx @modelcontextprotocol/inspector dotnet run
```

यसले भिजुअल इन्टरफेससहितको वेब सर्भर सुरु गर्नेछ जसले तपाईंलाई नमूना परीक्षण गर्न अनुमति दिनेछ।

सर्भर जडान भएपछि:

- उपकरणहरूको सूची बनाउने प्रयास गर्नुहोस् र `add` चलाउनुहोस्, 2 र 4 को आर्ग्ससहित, परिणाममा तपाईंले 6 देख्नुहुनेछ।
- स्रोतहरू र स्रोत टेम्प्लेटमा जानुहोस् र "greeting" कल गर्नुहोस्, नाम टाइप गर्नुहोस् र तपाईंले प्रदान गरेको नामसहितको अभिवादन देख्नुहुनेछ।

### CLI मोडमा परीक्षण गर्दै

तपाईं यसलाई CLI मोडमा सिधै निम्न कमाण्ड चलाएर सुरु गर्न सक्नुहुन्छ:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/list
```

यसले सर्भरमा उपलब्ध सबै उपकरणहरूको सूची देखाउनेछ। तपाईंले निम्न आउटपुट देख्नुहुनेछ:

```text
{
  "tools": [
    {
      "name": "Add",
      "description": "Adds two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer"
          },
          "b": {
            "type": "integer"
          }
        },
        "title": "Add",
        "description": "Adds two numbers",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

उपकरण चलाउन टाइप गर्नुहोस्:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/call --tool-name Add --tool-arg a=1 --tool-arg b=2
```

तपाईंले निम्न आउटपुट देख्नुहुनेछ:

```text
{
  "content": [
    {
      "type": "text",
      "text": "Sum 3"
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
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको छ। हामी शुद्धताको लागि प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादहरूमा त्रुटि वा अशुद्धता हुन सक्छ। यसको मूल भाषा मा रहेको मूल दस्तावेज़लाई आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीको लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुने छैनौं।