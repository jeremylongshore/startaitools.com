<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:16:35+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "ne"
}
-->
# नमूना चलाउनुहोस्

## वातावरण सिर्जना गर्नुहोस्

```sh
python -m venv venv
source ./venv/bin/activate
```

## निर्भरता स्थापना गर्नुहोस्

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## टोकन उत्पन्न गर्नुहोस्

तपाईंलाई टोकन उत्पन्न गर्न आवश्यक छ जसलाई क्लाइन्टले सर्भरसँग कुरा गर्न प्रयोग गर्नेछ।

कल गर्नुहोस्:

```sh
python util.py
```

## कोड चलाउनुहोस्

कोड चलाउन:

```sh
python server.py
```

अर्को टर्मिनलमा टाइप गर्नुहोस्:

```sh
python client.py
```

सर्भर टर्मिनलमा, तपाईंले निम्न जस्तै केही देख्नुहुनेछ:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

क्लाइन्ट विन्डोमा, तपाईंले निम्न जस्तै पाठ देख्नुहुनेछ:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

यसको मतलब सबै ठीकसँग काम गरिरहेको छ।

### जानकारी परिवर्तन गर्नुहोस्, असफल भएको हेर्न

*server.py* मा यो कोड खोज्नुहोस्:

```python
 if not has_scope(has_header, "Admin.Write"):
```

यसलाई "User.Write" भन्नको लागि परिवर्तन गर्नुहोस्। तपाईंको हालको टोकनसँग यो अनुमति स्तर छैन, त्यसैले यदि तपाईंले सर्भर पुनः सुरु गर्नुभयो र क्लाइन्टलाई फेरि चलाउन प्रयास गर्नुभयो भने तपाईंले सर्भर टर्मिनलमा निम्न जस्तै त्रुटि देख्नुहुनेछ:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

तपाईं आफ्नो सर्भर कोडलाई पुनः परिवर्तन गर्न सक्नुहुन्छ वा यो थप स्कोप समावेश गर्ने नयाँ टोकन उत्पन्न गर्न सक्नुहुन्छ, यो तपाईंको निर्णयमा निर्भर छ।

---

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी यथासम्भव शुद्धता सुनिश्चित गर्न प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छ। मूल दस्तावेज़ यसको मातृभाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीको लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुने छैनौं।