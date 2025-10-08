<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "9d799c4a30a8383e0a74af9153262972",
  "translation_date": "2025-08-26T20:07:32+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/typescript/README.md",
  "language_code": "hi"
}
-->
# MCP stdio सर्वर - TypeScript समाधान

> **⚠️ महत्वपूर्ण**: इस समाधान को **stdio transport** का उपयोग करने के लिए अपडेट किया गया है, जैसा कि MCP Specification 2025-06-18 में अनुशंसित किया गया है। मूल SSE transport को अब बंद कर दिया गया है।

## अवलोकन

यह TypeScript समाधान दिखाता है कि वर्तमान stdio transport का उपयोग करके MCP सर्वर कैसे बनाया जाए। stdio transport सरल, अधिक सुरक्षित और पुराने SSE दृष्टिकोण की तुलना में बेहतर प्रदर्शन प्रदान करता है।

## आवश्यकताएँ

- Node.js 18+ या बाद का संस्करण
- npm या yarn पैकेज मैनेजर

## सेटअप निर्देश

### चरण 1: डिपेंडेंसी इंस्टॉल करें

```bash
npm install
```

### चरण 2: प्रोजेक्ट को बिल्ड करें

```bash
npm run build
```

## सर्वर चलाना

stdio सर्वर पुराने SSE सर्वर से अलग तरीके से चलता है। वेब सर्वर शुरू करने के बजाय, यह stdin/stdout के माध्यम से संवाद करता है:

```bash
npm start
```

**महत्वपूर्ण**: सर्वर रुका हुआ प्रतीत होगा - यह सामान्य है! यह stdin से JSON-RPC संदेशों की प्रतीक्षा कर रहा है।

## सर्वर का परीक्षण

### विधि 1: MCP Inspector का उपयोग करना (अनुशंसित)

```bash
npm run inspector
```

यह करेगा:
1. आपके सर्वर को एक subprocess के रूप में लॉन्च करेगा
2. परीक्षण के लिए एक वेब इंटरफ़ेस खोलेगा
3. आपको सभी सर्वर टूल्स को इंटरैक्टिव तरीके से परीक्षण करने की अनुमति देगा

### विधि 2: सीधे कमांड लाइन परीक्षण

आप Inspector को सीधे लॉन्च करके भी परीक्षण कर सकते हैं:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

### उपलब्ध टूल्स

सर्वर निम्नलिखित टूल्स प्रदान करता है:

- **add(a, b)**: दो संख्याओं को जोड़ें
- **multiply(a, b)**: दो संख्याओं को गुणा करें  
- **get_greeting(name)**: एक व्यक्तिगत अभिवादन उत्पन्न करें
- **get_server_info()**: सर्वर की जानकारी प्राप्त करें

### Claude Desktop के साथ परीक्षण

इस सर्वर को Claude Desktop के साथ उपयोग करने के लिए, अपने `claude_desktop_config.json` में यह कॉन्फ़िगरेशन जोड़ें:

```json
{
  "mcpServers": {
    "example-stdio-server": {
      "command": "node",
      "args": ["path/to/build/index.js"]
    }
  }
}
```

## प्रोजेक्ट संरचना

```
typescript/
├── src/
│   └── index.ts          # Main server implementation
├── build/                # Compiled JavaScript (generated)
├── package.json          # Project configuration
├── tsconfig.json         # TypeScript configuration
└── README.md            # This file
```

## SSE से मुख्य अंतर

**stdio transport (वर्तमान):**
- ✅ सरल सेटअप - HTTP सर्वर की आवश्यकता नहीं
- ✅ बेहतर सुरक्षा - कोई HTTP endpoints नहीं
- ✅ subprocess-आधारित संवाद
- ✅ stdin/stdout पर JSON-RPC
- ✅ बेहतर प्रदर्शन

**SSE transport (बंद):**
- ❌ Express सर्वर सेटअप की आवश्यकता थी
- ❌ जटिल रूटिंग और सत्र प्रबंधन की आवश्यकता थी
- ❌ अधिक डिपेंडेंसी (Express, HTTP हैंडलिंग)
- ❌ अतिरिक्त सुरक्षा विचार
- ❌ अब MCP 2025-06-18 में बंद कर दिया गया है

## विकास के सुझाव

- लॉगिंग के लिए `console.error()` का उपयोग करें (कभी भी `console.log()` का उपयोग न करें क्योंकि यह stdout पर लिखता है)
- परीक्षण से पहले `npm run build` के साथ बिल्ड करें
- विज़ुअल डिबगिंग के लिए Inspector के साथ परीक्षण करें
- सुनिश्चित करें कि सभी JSON संदेश सही तरीके से स्वरूपित हैं
- सर्वर SIGINT/SIGTERM पर स्वचालित रूप से ग्रेसफुल शटडाउन को संभालता है

यह समाधान वर्तमान MCP विनिर्देश का पालन करता है और TypeScript का उपयोग करके stdio transport कार्यान्वयन के लिए सर्वोत्तम प्रथाओं को प्रदर्शित करता है।

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल दस्तावेज़, जो इसकी मूल भाषा में है, को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।