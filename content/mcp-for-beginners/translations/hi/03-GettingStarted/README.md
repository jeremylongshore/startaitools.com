<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "f400d87053221363769113c24f117248",
  "translation_date": "2025-10-06T22:32:28+00:00",
  "source_file": "03-GettingStarted/README.md",
  "language_code": "hi"
}
-->
## शुरुआत करें  

[![अपना पहला MCP सर्वर बनाएं](../../../translated_images/04.0ea920069efd979a0b2dad51e72c1df7ead9c57b3305796068a6cee1f0dd6674.hi.png)](https://youtu.be/sNDZO9N4m9Y)

_(इस पाठ का वीडियो देखने के लिए ऊपर दी गई छवि पर क्लिक करें)_

इस अनुभाग में कई पाठ शामिल हैं:

- **1 आपका पहला सर्वर**, इस पहले पाठ में, आप सीखेंगे कि अपना पहला सर्वर कैसे बनाएं और इसे इंस्पेक्टर टूल के साथ जांचें, जो आपके सर्वर का परीक्षण और डिबग करने का एक उपयोगी तरीका है, [पाठ पर जाएं](01-first-server/README.md)

- **2 क्लाइंट**, इस पाठ में, आप सीखेंगे कि ऐसा क्लाइंट कैसे लिखें जो आपके सर्वर से कनेक्ट हो सके, [पाठ पर जाएं](02-client/README.md)

- **3 LLM के साथ क्लाइंट**, क्लाइंट लिखने का एक और बेहतर तरीका है इसमें LLM जोड़ना ताकि यह आपके सर्वर के साथ "समझौता" कर सके कि क्या करना है, [पाठ पर जाएं](03-llm-client/README.md)

- **4 GitHub Copilot Agent मोड में Visual Studio Code के साथ सर्वर का उपयोग करना**। यहां, हम Visual Studio Code के भीतर से अपना MCP सर्वर चलाने पर ध्यान केंद्रित करेंगे, [पाठ पर जाएं](04-vscode/README.md)

- **5 stdio Transport Server** stdio transport वर्तमान विनिर्देश में MCP सर्वर-से-क्लाइंट संचार के लिए अनुशंसित मानक है, जो सुरक्षित subprocess-आधारित संचार प्रदान करता है [पाठ पर जाएं](05-stdio-server/README.md)

- **6 MCP के साथ HTTP स्ट्रीमिंग (Streamable HTTP)**। आधुनिक HTTP स्ट्रीमिंग, प्रगति सूचनाओं, और Streamable HTTP का उपयोग करके स्केलेबल, रीयल-टाइम MCP सर्वर और क्लाइंट को लागू करने के बारे में जानें। [पाठ पर जाएं](06-http-streaming/README.md)

- **7 VSCode के लिए AI Toolkit का उपयोग करना** अपने MCP क्लाइंट्स और सर्वर का उपभोग और परीक्षण करने के लिए [पाठ पर जाएं](07-aitk/README.md)

- **8 परीक्षण**। यहां हम विशेष रूप से ध्यान केंद्रित करेंगे कि हम अपने सर्वर और क्लाइंट का विभिन्न तरीकों से परीक्षण कैसे कर सकते हैं, [पाठ पर जाएं](08-testing/README.md)

- **9 परिनियोजन**। यह अध्याय आपके MCP समाधानों को परिनियोजित करने के विभिन्न तरीकों को देखेगा, [पाठ पर जाएं](09-deployment/README.md)

- **10 उन्नत सर्वर उपयोग**। यह अध्याय उन्नत सर्वर उपयोग को कवर करता है, [पाठ पर जाएं](./10-advanced/README.md)

- **11 प्रमाणीकरण**। यह अध्याय सरल प्रमाणीकरण जोड़ने को कवर करता है, Basic Auth से लेकर JWT और RBAC तक। आपको यहां से शुरू करने और फिर अध्याय 5 में उन्नत विषयों को देखने और अध्याय 2 में अनुशंसाओं के माध्यम से अतिरिक्त सुरक्षा सख्ती करने के लिए प्रोत्साहित किया जाता है, [पाठ पर जाएं](./11-simple-auth/README.md)

Model Context Protocol (MCP) एक खुला प्रोटोकॉल है जो मानकीकृत करता है कि एप्लिकेशन LLMs को संदर्भ कैसे प्रदान करते हैं। MCP को AI एप्लिकेशन के लिए USB-C पोर्ट की तरह सोचें - यह AI मॉडल को विभिन्न डेटा स्रोतों और टूल्स से कनेक्ट करने का एक मानकीकृत तरीका प्रदान करता है।

## सीखने के उद्देश्य

इस पाठ के अंत तक, आप सक्षम होंगे:

- MCP के लिए C#, Java, Python, TypeScript, और JavaScript में विकास वातावरण सेट करें
- कस्टम सुविधाओं (संसाधन, प्रॉम्प्ट, और टूल्स) के साथ बुनियादी MCP सर्वर बनाएं और परिनियोजित करें
- MCP सर्वर से कनेक्ट होने वाले होस्ट एप्लिकेशन बनाएं
- MCP कार्यान्वयन का परीक्षण और डिबग करें
- सामान्य सेटअप चुनौतियों और उनके समाधान को समझें
- अपने MCP कार्यान्वयन को लोकप्रिय LLM सेवाओं से कनेक्ट करें

## अपना MCP वातावरण सेट करना

MCP के साथ काम शुरू करने से पहले, अपने विकास वातावरण को तैयार करना और बुनियादी वर्कफ़्लो को समझना महत्वपूर्ण है। यह अनुभाग आपको MCP के साथ एक सुचारू शुरुआत सुनिश्चित करने के लिए प्रारंभिक सेटअप चरणों के माध्यम से मार्गदर्शन करेगा।

### आवश्यकताएँ

MCP विकास में उतरने से पहले, सुनिश्चित करें कि आपके पास है:

- **विकास वातावरण**: आपके चुने हुए भाषा (C#, Java, Python, TypeScript, या JavaScript) के लिए
- **IDE/एडिटर**: Visual Studio, Visual Studio Code, IntelliJ, Eclipse, PyCharm, या कोई आधुनिक कोड एडिटर
- **पैकेज मैनेजर**: NuGet, Maven/Gradle, pip, या npm/yarn
- **API कुंजियाँ**: उन AI सेवाओं के लिए जिन्हें आप अपने होस्ट एप्लिकेशन में उपयोग करने की योजना बना रहे हैं

### आधिकारिक SDKs

आगामी अध्यायों में आप Python, TypeScript, Java और .NET का उपयोग करके बनाए गए समाधान देखेंगे। यहां सभी आधिकारिक रूप से समर्थित SDKs हैं।

MCP कई भाषाओं के लिए आधिकारिक SDKs प्रदान करता है:
- [C# SDK](https://github.com/modelcontextprotocol/csharp-sdk) - Microsoft के सहयोग से बनाए रखा गया
- [Java SDK](https://github.com/modelcontextprotocol/java-sdk) - Spring AI के सहयोग से बनाए रखा गया
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) - आधिकारिक TypeScript कार्यान्वयन
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) - आधिकारिक Python कार्यान्वयन
- [Kotlin SDK](https://github.com/modelcontextprotocol/kotlin-sdk) - आधिकारिक Kotlin कार्यान्वयन
- [Swift SDK](https://github.com/modelcontextprotocol/swift-sdk) - Loopwork AI के सहयोग से बनाए रखा गया
- [Rust SDK](https://github.com/modelcontextprotocol/rust-sdk) - आधिकारिक Rust कार्यान्वयन

## मुख्य बातें

- MCP विकास वातावरण सेट करना भाषा-विशिष्ट SDKs के साथ सरल है
- MCP सर्वर बनाना स्पष्ट स्कीमाओं के साथ टूल्स को बनाना और पंजीकृत करना शामिल है
- MCP क्लाइंट सर्वर और मॉडल से कनेक्ट होते हैं ताकि विस्तारित क्षमताओं का लाभ उठाया जा सके
- विश्वसनीय MCP कार्यान्वयन के लिए परीक्षण और डिबगिंग आवश्यक हैं
- परिनियोजन विकल्प स्थानीय विकास से लेकर क्लाउड-आधारित समाधानों तक होते हैं

## अभ्यास

हमारे पास नमूनों का एक सेट है जो इस अनुभाग के सभी अध्यायों में दिखाए गए अभ्यासों को पूरक करता है। इसके अलावा प्रत्येक अध्याय में अपने स्वयं के अभ्यास और असाइनमेंट भी हैं।

- [Java कैलकुलेटर](./samples/java/calculator/README.md)
- [.Net कैलकुलेटर](../../../03-GettingStarted/samples/csharp)
- [JavaScript कैलकुलेटर](./samples/javascript/README.md)
- [TypeScript कैलकुलेटर](./samples/typescript/README.md)
- [Python कैलकुलेटर](../../../03-GettingStarted/samples/python)

## अतिरिक्त संसाधन

- [Azure पर Model Context Protocol का उपयोग करके एजेंट बनाएं](https://learn.microsoft.com/azure/developer/ai/intro-agents-mcp)
- [Azure Container Apps के साथ Remote MCP (Node.js/TypeScript/JavaScript)](https://learn.microsoft.com/samples/azure-samples/mcp-container-ts/mcp-container-ts/)
- [.NET OpenAI MCP Agent](https://learn.microsoft.com/samples/azure-samples/openai-mcp-agent-dotnet/openai-mcp-agent-dotnet/)

## आगे क्या है

अगला: [अपना पहला MCP सर्वर बनाना](01-first-server/README.md)

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को आधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।