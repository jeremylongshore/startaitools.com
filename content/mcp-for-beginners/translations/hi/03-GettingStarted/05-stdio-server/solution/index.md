<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T20:00:28+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "hi"
}
-->
# MCP स्टैंडर्ड इनपुट/आउटपुट सर्वर समाधान

> **⚠️ महत्वपूर्ण**: इन समाधानों को **stdio transport** का उपयोग करने के लिए अपडेट किया गया है, जैसा कि MCP स्पेसिफिकेशन 2025-06-18 में अनुशंसित किया गया है। मूल SSE (Server-Sent Events) transport को अब बंद कर दिया गया है।

यहाँ प्रत्येक रनटाइम में stdio transport का उपयोग करके MCP सर्वर बनाने के लिए संपूर्ण समाधान दिए गए हैं:

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - संपूर्ण stdio सर्वर कार्यान्वयन
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - asyncio के साथ Python stdio सर्वर
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - dependency injection के साथ .NET stdio सर्वर

प्रत्येक समाधान निम्नलिखित को प्रदर्शित करता है:
- stdio transport सेटअप करना
- सर्वर टूल्स को परिभाषित करना
- JSON-RPC संदेशों को सही तरीके से संभालना
- Claude जैसे MCP क्लाइंट्स के साथ एकीकरण

सभी समाधान वर्तमान MCP स्पेसिफिकेशन का पालन करते हैं और बेहतर प्रदर्शन और सुरक्षा के लिए अनुशंसित stdio transport का उपयोग करते हैं।

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।