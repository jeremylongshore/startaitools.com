<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:16:15+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "hi"
}
-->
# नमूना चलाएं

## वातावरण बनाएं

```sh
python -m venv venv
source ./venv/bin/activate
```

## निर्भरताएँ स्थापित करें

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## टोकन उत्पन्न करें

आपको एक टोकन उत्पन्न करना होगा जिसे क्लाइंट सर्वर से बात करने के लिए उपयोग करेगा।

कॉल करें:

```sh
python util.py
```

## कोड चलाएं

कोड चलाने के लिए:

```sh
python server.py
```

एक अलग टर्मिनल में टाइप करें:

```sh
python client.py
```

सर्वर टर्मिनल में, आपको कुछ इस तरह दिखाई देना चाहिए:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

क्लाइंट विंडो में, आपको कुछ इस तरह का टेक्स्ट दिखाई देना चाहिए:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

इसका मतलब है कि सब कुछ सही तरीके से काम कर रहा है।

### जानकारी बदलें, इसे विफल होते देखने के लिए

*server.py* में इस कोड को ढूंढें:

```python
 if not has_scope(has_header, "Admin.Write"):
```

इसे बदलें ताकि यह "User.Write" कहे। आपके वर्तमान टोकन में यह अनुमति स्तर नहीं है, इसलिए यदि आप सर्वर को पुनः प्रारंभ करते हैं और क्लाइंट को फिर से चलाने का प्रयास करते हैं, तो आपको सर्वर टर्मिनल में निम्नलिखित जैसी त्रुटि दिखाई देनी चाहिए:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

आप या तो अपने सर्वर कोड को वापस बदल सकते हैं या एक नया टोकन उत्पन्न कर सकते हैं जिसमें यह अतिरिक्त स्कोप शामिल हो, यह आपकी पसंद है।

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।