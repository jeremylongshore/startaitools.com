<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3f68294760a11dd3fdd175bd7f904a92",
  "translation_date": "2025-10-07T01:29:59+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/basic/python/README.md",
  "language_code": "hi"
}
-->
# नमूना चलाएँ

यह नमूना एक MCP सर्वर शुरू करता है जिसमें एक मिडलवेयर शामिल है जो वैध Authorization हेडर की जांच करता है।

## डिपेंडेंसी इंस्टॉल करें

```bash
pip install "mcp[cli]" 
```

## सर्वर शुरू करें

```bash
python server.py
```

दूसरे टर्मिनल में क्लाइंट शुरू करें

```bash
python client.py
```

आपको कुछ ऐसा परिणाम दिखाई देगा:

```text
2025-09-30 13:25:54 - mcp_client - INFO - Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-09-30T13:25:54.311900",\n  "timezone": "UTC",\n  "timestamp": 1759238754.3119,\n  "formatted": "2025-09-30 13:25:54"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-09-30T13:25:54.311900', 'timezone': 'UTC', 'timestamp': 1759238754.3119, 'formatted': '2025-09-30 13:25:54'} isError=False
```

इसका मतलब है कि भेजा गया क्रेडेंशियल स्वीकार किया जा रहा है।

`client.py` में क्रेडेंशियल को "secret-token2" में बदलने की कोशिश करें, फिर आपको प्रतिक्रिया में यह टेक्स्ट दिखाई देगा:

```text
2025-09-30 13:27:44 - httpx - INFO - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 403 Forbidden"
```

इसका मतलब है कि आप प्रमाणित हुए (आपके पास क्रेडेंशियल था), लेकिन वह अमान्य था।

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में दस्तावेज़ को आधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।