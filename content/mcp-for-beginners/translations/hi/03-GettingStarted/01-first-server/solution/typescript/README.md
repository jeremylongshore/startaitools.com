<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "6ebbb78b04c9b1f6c2367c713524fc95",
  "translation_date": "2025-09-03T16:02:18+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/typescript/README.md",
  "language_code": "hi"
}
-->
# इस सैंपल को चलाना

आपको `uv` इंस्टॉल करने की सलाह दी जाती है, लेकिन यह अनिवार्य नहीं है। [निर्देश](https://docs.astral.sh/uv/#highlights) देखें।

## -1- डिपेंडेंसीज़ इंस्टॉल करें

```bash
npm install
```

## -3- सैंपल चलाएं

```bash
npm run build
```

## -4- सैंपल का परीक्षण करें

सर्वर को एक टर्मिनल में चलाने के बाद, दूसरा टर्मिनल खोलें और निम्नलिखित कमांड चलाएं:

```bash
npm run inspector
```

यह एक वेब सर्वर शुरू करेगा जिसमें एक विज़ुअल इंटरफ़ेस होगा, जो आपको सैंपल का परीक्षण करने की अनुमति देगा।

सर्वर कनेक्ट होने के बाद:

- टूल्स की सूची बनाएं और `add` चलाएं, जिसमें 2 और 4 के आर्ग्युमेंट्स हों। आपको परिणाम में 6 दिखाई देना चाहिए।
- रिसोर्सेस और रिसोर्स टेम्पलेट पर जाएं और "greeting" कॉल करें। एक नाम टाइप करें और आपको उस नाम के साथ एक ग्रीटिंग दिखाई देगी जो आपने प्रदान किया है।

### CLI मोड में परीक्षण करना

जो इंस्पेक्टर आपने चलाया है, वह वास्तव में एक Node.js ऐप है और `mcp dev` इसका एक रैपर है।

आप इसे सीधे CLI मोड में निम्नलिखित कमांड चलाकर लॉन्च कर सकते हैं:

```bash
npx @modelcontextprotocol/inspector --cli node ./build/index.js --method tools/list
```

यह सर्वर में उपलब्ध सभी टूल्स की सूची दिखाएगा। आपको निम्नलिखित आउटपुट दिखाई देना चाहिए:

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

किसी टूल को इनवोक करने के लिए टाइप करें:

```bash
nnpx @modelcontextprotocol/inspector --cli node ./build/index.js --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

आपको निम्नलिखित आउटपुट दिखाई देना चाहिए:

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
> ब्राउज़र की तुलना में CLI मोड में इंस्पेक्टर चलाना आमतौर पर बहुत तेज़ होता है।
> इंस्पेक्टर के बारे में अधिक पढ़ें [यहां](https://github.com/modelcontextprotocol/inspector)।

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।