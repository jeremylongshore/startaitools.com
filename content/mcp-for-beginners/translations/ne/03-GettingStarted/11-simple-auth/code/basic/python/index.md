<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3f68294760a11dd3fdd175bd7f904a92",
  "translation_date": "2025-10-07T01:30:16+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/basic/python/README.md",
  "language_code": "ne"
}
-->
# नमूना चलाउनुहोस्

यो नमूनाले एक MCP Server सुरु गर्छ जसमा एक middleware हुन्छ, जसले मान्य Authorization हेडर जाँच गर्छ।

## निर्भरता स्थापना गर्नुहोस्

```bash
pip install "mcp[cli]" 
```

## सर्भर सुरु गर्नुहोस्

```bash
python server.py
```

अर्को टर्मिनलमा क्लाइन्ट सुरु गर्नुहोस्

```bash
python client.py
```

तपाईंले निम्न जस्तै नतिजा देख्नु पर्नेछ:

```text
2025-09-30 13:25:54 - mcp_client - INFO - Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-09-30T13:25:54.311900",\n  "timezone": "UTC",\n  "timestamp": 1759238754.3119,\n  "formatted": "2025-09-30 13:25:54"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-09-30T13:25:54.311900', 'timezone': 'UTC', 'timestamp': 1759238754.3119, 'formatted': '2025-09-30 13:25:54'} isError=False
```

यसको मतलब पठाइएको प्रमाणपत्रलाई अनुमति दिइएको छ।

`client.py` मा प्रमाणपत्रलाई "secret-token2" मा परिवर्तन गरेर प्रयास गर्नुहोस्, त्यसपछि तपाईंले यो पाठ प्रतिक्रिया को भागको रूपमा देख्नु पर्नेछ:

```text
2025-09-30 13:27:44 - httpx - INFO - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 403 Forbidden"
```

यसको मतलब तपाईं प्रमाणित हुनुहुन्थ्यो (तपाईंसँग प्रमाणपत्र थियो), तर यो अमान्य थियो।

---

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको छ। हामी यथार्थताको लागि प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छ। मूल दस्तावेज़ यसको मातृभाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीको लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुनेछैनौं।