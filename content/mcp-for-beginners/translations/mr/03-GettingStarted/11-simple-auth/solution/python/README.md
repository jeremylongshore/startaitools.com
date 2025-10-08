<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:16:28+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "mr"
}
-->
# नमुना चालवा

## वातावरण तयार करा

```sh
python -m venv venv
source ./venv/bin/activate
```

## अवलंबित्व स्थापित करा

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## टोकन तयार करा

क्लायंटला सर्व्हरशी संवाद साधण्यासाठी टोकन तयार करणे आवश्यक आहे.

कॉल करा:

```sh
python util.py
```

## कोड चालवा

कोड चालवण्यासाठी:

```sh
python server.py
```

वेगळ्या टर्मिनलमध्ये टाइप करा:

```sh
python client.py
```

सर्व्हर टर्मिनलमध्ये तुम्हाला असे काहीतरी दिसेल:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

क्लायंट विंडोमध्ये तुम्हाला यासारखा मजकूर दिसेल:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

याचा अर्थ सर्व काही व्यवस्थित चालू आहे.

### माहिती बदला, अपयश पाहण्यासाठी

*server.py* मध्ये हा कोड शोधा:

```python
 if not has_scope(has_header, "Admin.Write"):
```

त्याला "User.Write" असे म्हणण्यासाठी बदला. तुमच्या वर्तमान टोकनमध्ये तो परवानगी स्तर नाही, त्यामुळे जर तुम्ही सर्व्हर रीस्टार्ट केला आणि पुन्हा एकदा क्लायंट चालवण्याचा प्रयत्न केला तर तुम्हाला सर्व्हर टर्मिनलमध्ये खालीलप्रमाणे त्रुटी दिसेल:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

तुम्ही तुमचा सर्व्हर कोड परत बदलू शकता किंवा या अतिरिक्त स्कोपसह नवीन टोकन तयार करू शकता, तुमच्यावर आहे.

---

**अस्वीकृती**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात ठेवा की स्वयंचलित भाषांतरे त्रुटी किंवा अचूकतेच्या अभावाने युक्त असू शकतात. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून उद्भवलेल्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.