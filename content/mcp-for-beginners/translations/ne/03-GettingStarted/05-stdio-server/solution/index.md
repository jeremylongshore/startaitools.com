<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T20:00:51+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "ne"
}
-->
# MCP stdio सर्भर समाधानहरू

> **⚠️ महत्त्वपूर्ण**: यी समाधानहरू **stdio transport** प्रयोग गर्न अद्यावधिक गरिएका छन्, जसलाई MCP Specification 2025-06-18 ले सिफारिस गरेको छ। पुरानो SSE (Server-Sent Events) transport अब प्रयोगमा छैन।

यहाँ प्रत्येक रनटाइममा stdio transport प्रयोग गरेर MCP सर्भर निर्माणका लागि पूर्ण समाधानहरू छन्:

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - पूर्ण stdio सर्भर कार्यान्वयन
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - asyncio सहितको Python stdio सर्भर
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - dependency injection सहितको .NET stdio सर्भर

प्रत्येक समाधानले निम्न कुरा प्रदर्शन गर्दछ:
- stdio transport सेटअप गर्ने
- सर्भर उपकरणहरू परिभाषित गर्ने
- JSON-RPC सन्देशहरूको उचित ह्यान्डलिङ
- Claude जस्ता MCP क्लाइन्टहरूसँग एकीकरण

सबै समाधानहरूले हालको MCP विशिष्टता पालना गर्छन् र उच्च प्रदर्शन र सुरक्षाका लागि सिफारिस गरिएको stdio transport प्रयोग गर्छन्।

---

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको छ। हामी शुद्धताको लागि प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छ। यसको मूल भाषा मा रहेको मूल दस्तावेज़लाई आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीको लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुने छैनौं।