<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "9d799c4a30a8383e0a74af9153262972",
  "translation_date": "2025-08-26T20:07:59+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/typescript/README.md",
  "language_code": "mr"
}
-->
# MCP stdio सर्व्हर - TypeScript सोल्यूशन

> **⚠️ महत्त्वाचे**: हे सोल्यूशन **stdio transport** वापरण्यासाठी अद्ययावत केले गेले आहे, जसे की MCP Specification 2025-06-18 मध्ये शिफारस केली आहे. मूळ SSE transport आता कालबाह्य झाले आहे.

## आढावा

हे TypeScript सोल्यूशन सध्याच्या stdio transport वापरून MCP सर्व्हर कसे तयार करायचे ते दाखवते. stdio transport सोपे, अधिक सुरक्षित आणि कालबाह्य SSE पद्धतीपेक्षा चांगली कार्यक्षमता प्रदान करते.

## पूर्वअट

- Node.js 18+ किंवा त्यापुढील आवृत्ती
- npm किंवा yarn पॅकेज मॅनेजर

## सेटअप सूचना

### पायरी 1: dependencies इंस्टॉल करा

```bash
npm install
```

### पायरी 2: प्रकल्प तयार करा

```bash
npm run build
```

## सर्व्हर चालवणे

stdio सर्व्हर जुन्या SSE सर्व्हरपेक्षा वेगळ्या प्रकारे चालतो. वेब सर्व्हर सुरू करण्याऐवजी, तो stdin/stdout द्वारे संवाद साधतो:

```bash
npm start
```

**महत्त्वाचे**: सर्व्हर थांबलेला दिसेल - हे सामान्य आहे! तो stdin वरून JSON-RPC संदेशांची वाट पाहत आहे.

## सर्व्हर चाचणी करणे

### पद्धत 1: MCP Inspector वापरणे (शिफारस केलेले)

```bash
npm run inspector
```

हे करेल:
1. तुमचा सर्व्हर subprocess म्हणून सुरू करेल
2. चाचणीसाठी वेब इंटरफेस उघडेल
3. तुम्हाला सर्व्हर टूल्स परस्पर चाचणी करण्याची परवानगी देईल

### पद्धत 2: थेट कमांड लाइन चाचणी

तुम्ही Inspector थेट सुरू करूनही चाचणी करू शकता:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

### उपलब्ध टूल्स

सर्व्हर खालील टूल्स प्रदान करतो:

- **add(a, b)**: दोन संख्यांची बेरीज करा
- **multiply(a, b)**: दोन संख्यांचे गुणाकार करा  
- **get_greeting(name)**: वैयक्तिक अभिवादन तयार करा
- **get_server_info()**: सर्व्हरची माहिती मिळवा

### Claude Desktop सह चाचणी करणे

हा सर्व्हर Claude Desktop सह वापरण्यासाठी, तुमच्या `claude_desktop_config.json` मध्ये हा कॉन्फिगरेशन जोडा:

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

## प्रकल्प संरचना

```
typescript/
├── src/
│   └── index.ts          # Main server implementation
├── build/                # Compiled JavaScript (generated)
├── package.json          # Project configuration
├── tsconfig.json         # TypeScript configuration
└── README.md            # This file
```

## SSE पासून मुख्य फरक

**stdio transport (सध्याचे):**
- ✅ सोपी सेटअप - HTTP सर्व्हरची गरज नाही
- ✅ चांगली सुरक्षा - HTTP endpoints नाहीत
- ✅ Subprocess-आधारित संवाद
- ✅ stdin/stdout वर JSON-RPC
- ✅ चांगली कार्यक्षमता

**SSE transport (कालबाह्य):**
- ❌ Express सर्व्हर सेटअप आवश्यक
- ❌ क्लिष्ट रूटिंग आणि सत्र व्यवस्थापन आवश्यक
- ❌ अधिक dependencies (Express, HTTP हाताळणी)
- ❌ अतिरिक्त सुरक्षा विचार
- ❌ आता MCP 2025-06-18 मध्ये कालबाह्य

## विकास टिपा

- लॉगिंगसाठी `console.error()` वापरा (`console.log()` कधीही वापरू नका कारण ते stdout वर लिहिते)
- चाचणीपूर्वी `npm run build` वापरून तयार करा
- दृश्य डिबगिंगसाठी Inspector सह चाचणी करा
- सर्व JSON संदेश योग्यरित्या स्वरूपित आहेत याची खात्री करा
- SIGINT/SIGTERM वर सर्व्हर आपोआप व्यवस्थित बंद होतो

हे सोल्यूशन सध्याच्या MCP स्पेसिफिकेशनचे पालन करते आणि TypeScript वापरून stdio transport अंमलबजावणीसाठी सर्वोत्तम पद्धती दाखवते.

---

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेचा अभाव असू शकतो. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर केल्यामुळे उद्भवणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.