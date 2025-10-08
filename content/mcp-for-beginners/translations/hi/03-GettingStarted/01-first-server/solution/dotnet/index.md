<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "92af35e8c34923031f3d228dffad9ebb",
  "translation_date": "2025-09-03T16:02:28+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/dotnet/README.md",
  "language_code": "hi"
}
-->
# इस नमूने को चलाना

## -1- डिपेंडेंसीज़ इंस्टॉल करें

```bash
dotnet restore
```

## -3- नमूना चलाएं

```bash
dotnet run
```

## -4- नमूने का परीक्षण करें

जब सर्वर एक टर्मिनल में चल रहा हो, तो दूसरा टर्मिनल खोलें और निम्नलिखित कमांड चलाएं:

```bash
npx @modelcontextprotocol/inspector dotnet run
```

यह एक वेब सर्वर शुरू करेगा जिसमें एक विज़ुअल इंटरफ़ेस होगा, जो आपको नमूने का परीक्षण करने की अनुमति देगा।

एक बार सर्वर कनेक्ट हो जाने के बाद:

- टूल्स की सूची बनाने की कोशिश करें और `add` चलाएं, जिसमें 2 और 4 के आर्ग्युमेंट्स हों। आपको परिणाम में 6 दिखाई देना चाहिए।
- संसाधनों और संसाधन टेम्पलेट पर जाएं और "greeting" कॉल करें। एक नाम टाइप करें और आपको उस नाम के साथ एक अभिवादन दिखाई देगा जो आपने प्रदान किया है।

### CLI मोड में परीक्षण करना

आप इसे सीधे CLI मोड में निम्नलिखित कमांड चलाकर लॉन्च कर सकते हैं:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/list
```

यह सर्वर में उपलब्ध सभी टूल्स की सूची दिखाएगा। आपको निम्नलिखित आउटपुट दिखाई देना चाहिए:

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

किसी टूल को चलाने के लिए टाइप करें:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/call --tool-name Add --tool-arg a=1 --tool-arg b=2
```

आपको निम्नलिखित आउटपुट दिखाई देना चाहिए:

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
> आमतौर पर CLI मोड में इंस्पेक्टर को चलाना ब्राउज़र की तुलना में बहुत तेज़ होता है।
> इंस्पेक्टर के बारे में अधिक पढ़ें [यहां](https://github.com/modelcontextprotocol/inspector)।

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।