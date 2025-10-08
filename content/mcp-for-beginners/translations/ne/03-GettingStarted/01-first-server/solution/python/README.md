<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d4c162484df410632550a4a357d40341",
  "translation_date": "2025-09-03T16:04:02+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "ne"
}
-->
# यो नमूना चलाउनुहोस्

तपाईंलाई `uv` स्थापना गर्न सिफारिस गरिन्छ तर यो अनिवार्य छैन, [निर्देशनहरू](https://docs.astral.sh/uv/#highlights) हेर्नुहोस्।

## -0- भर्चुअल वातावरण सिर्जना गर्नुहोस्

```bash
python -m venv venv
```

## -1- भर्चुअल वातावरण सक्रिय गर्नुहोस्

```bash
venv\Scripts\activate
```

## -2- आवश्यकताहरू स्थापना गर्नुहोस्

```bash
pip install "mcp[cli]"
```

## -3- नमूना चलाउनुहोस्

```bash
mcp run server.py
```

## -4- नमूना परीक्षण गर्नुहोस्

सर्भर एक टर्मिनलमा चलिरहेको अवस्थामा, अर्को टर्मिनल खोल्नुहोस् र निम्न आदेश चलाउनुहोस्:

```bash
mcp dev server.py
```

यसले भिजुअल इन्टरफेससहितको वेब सर्भर सुरु गर्नुपर्छ जसले तपाईंलाई नमूना परीक्षण गर्न अनुमति दिन्छ।

सर्भर जडान भएपछि:

- उपकरणहरूको सूची बनाउने प्रयास गर्नुहोस् र `add` चलाउनुहोस्, 2 र 4 को आर्ग्ससहित, परिणाममा तपाईंले 6 देख्नुपर्छ।

- स्रोतहरूमा जानुहोस् र स्रोत टेम्प्लेटमा `get_greeting` कल गर्नुहोस्, नाम टाइप गर्नुहोस् र तपाईंले प्रदान गरेको नामसहितको अभिवादन देख्नुपर्छ।

### CLI मोडमा परीक्षण गर्दै

तपाईंले चलाएको निरीक्षक वास्तवमा Node.js एप हो र `mcp dev` यसको वरिपरि एक र्यापर हो।

तपाईं यसलाई CLI मोडमा सिधै निम्न आदेश चलाएर सुरु गर्न सक्नुहुन्छ:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

यसले सर्भरमा उपलब्ध सबै उपकरणहरूको सूची देखाउनेछ। तपाईंले निम्न आउटपुट देख्नुपर्छ:

```text
{
  "tools": [
    {
      "name": "add",
      "description": "Add two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "title": "A",
            "type": "integer"
          },
          "b": {
            "title": "B",
            "type": "integer"
          }
        },
        "required": [
          "a",
          "b"
        ],
        "title": "addArguments"
      }
    }
  ]
}
```

एउटा उपकरण चलाउन टाइप गर्नुहोस्:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

तपाईंले निम्न आउटपुट देख्नुपर्छ:

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
> ब्राउजरमा भन्दा CLI मोडमा निरीक्षक चलाउनु सामान्यतया धेरै छिटो हुन्छ।
> निरीक्षकबारे थप पढ्नुहोस् [यहाँ](https://github.com/modelcontextprotocol/inspector)।

---

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको छ। हामी शुद्धताको लागि प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादहरूमा त्रुटि वा अशुद्धता हुन सक्छ। यसको मूल भाषामा रहेको मूल दस्तावेज़लाई आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीको लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुने छैनौं।