<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3f68294760a11dd3fdd175bd7f904a92",
  "translation_date": "2025-10-07T01:30:10+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/basic/python/README.md",
  "language_code": "mr"
}
-->
# नमुना चालवा

हा नमुना एक MCP सर्व्हर सुरू करतो ज्यामध्ये एक मिडलवेअर आहे जो वैध Authorization हेडर तपासतो.

## आवश्यक गोष्टी स्थापित करा

```bash
pip install "mcp[cli]" 
```

## सर्व्हर सुरू करा

```bash
python server.py
```

दुसऱ्या टर्मिनलमध्ये क्लायंट सुरू करा

```bash
python client.py
```

तुम्हाला खालीलप्रमाणे परिणाम दिसेल:

```text
2025-09-30 13:25:54 - mcp_client - INFO - Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-09-30T13:25:54.311900",\n  "timezone": "UTC",\n  "timestamp": 1759238754.3119,\n  "formatted": "2025-09-30 13:25:54"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-09-30T13:25:54.311900', 'timezone': 'UTC', 'timestamp': 1759238754.3119, 'formatted': '2025-09-30 13:25:54'} isError=False
```

याचा अर्थ असा आहे की पाठवलेली क्रेडेन्शियल स्वीकारली जात आहे.

`client.py` मध्ये क्रेडेन्शियल "secret-token2" मध्ये बदलून पहा, मग तुम्हाला प्रतिसादाचा भाग म्हणून हा मजकूर दिसेल:

```text
2025-09-30 13:27:44 - httpx - INFO - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 403 Forbidden"
```

याचा अर्थ तुम्ही प्रमाणित केले गेले (तुमच्याकडे क्रेडेन्शियल होते), पण ते अवैध होते.

---

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात ठेवा की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेचा अभाव असू शकतो. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून निर्माण होणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.