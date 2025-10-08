<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T11:07:47+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "hi"
}
-->
# 🚀 10 Microsoft MCP सर्वर जो डेवलपर उत्पादकता को बदल रहे हैं

## 🎯 इस गाइड में आप क्या सीखेंगे

यह व्यावहारिक गाइड दस Microsoft MCP सर्वरों को दिखाता है जो सक्रिय रूप से यह बदल रहे हैं कि डेवलपर्स AI असिस्टेंट्स के साथ कैसे काम करते हैं। केवल यह बताने के बजाय कि MCP सर्वर *क्या* कर सकते हैं, हम आपको ऐसे सर्वर दिखाएंगे जो Microsoft और उससे आगे के दैनिक विकास कार्यप्रवाहों में वास्तविक बदलाव ला रहे हैं।

इस गाइड में प्रत्येक सर्वर को वास्तविक उपयोग और डेवलपर प्रतिक्रिया के आधार पर चुना गया है। आप न केवल जानेंगे कि प्रत्येक सर्वर क्या करता है, बल्कि यह भी समझेंगे कि यह क्यों महत्वपूर्ण है और अपने प्रोजेक्ट्स में इसका अधिकतम लाभ कैसे उठाएं। चाहे आप MCP में बिल्कुल नए हों या अपने मौजूदा सेटअप का विस्तार करना चाहते हों, ये सर्वर Microsoft इकोसिस्टम में उपलब्ध सबसे व्यावहारिक और प्रभावशाली टूल्स का प्रतिनिधित्व करते हैं।

> **💡 त्वरित शुरुआत टिप**
> 
> MCP में नए हैं? चिंता मत करें! यह गाइड शुरुआती लोगों के लिए डिज़ाइन की गई है। हम चलते-चलते अवधारणाओं को समझाएंगे, और आप हमेशा हमारे [Introduction to MCP](../00-Introduction/README.md) और [Core Concepts](../01-CoreConcepts/README.md) मॉड्यूल्स को गहराई से समझने के लिए देख सकते हैं।

## अवलोकन

यह व्यापक गाइड दस Microsoft MCP सर्वरों का अन्वेषण करता है जो डेवलपर्स के AI असिस्टेंट्स और बाहरी टूल्स के साथ इंटरैक्शन के तरीके को क्रांतिकारी बना रहे हैं। Azure संसाधन प्रबंधन से लेकर दस्तावेज़ प्रसंस्करण तक, ये सर्वर Model Context Protocol की शक्ति को दिखाते हैं जो सहज और उत्पादक विकास कार्यप्रवाह बनाते हैं।

## सीखने के उद्देश्य

इस गाइड के अंत तक, आप:
- समझेंगे कि MCP सर्वर डेवलपर उत्पादकता को कैसे बढ़ाते हैं
- Microsoft के सबसे प्रभावशाली MCP सर्वर कार्यान्वयन के बारे में जानेंगे
- प्रत्येक सर्वर के व्यावहारिक उपयोग के मामले खोजेंगे
- जानेंगे कि इन सर्वरों को VS Code और Visual Studio में कैसे सेटअप और कॉन्फ़िगर करें
- व्यापक MCP इकोसिस्टम और भविष्य की दिशा का अन्वेषण करेंगे

## 🔧 MCP सर्वरों को समझना: शुरुआती के लिए गाइड

### MCP सर्वर क्या हैं?

Model Context Protocol (MCP) में नए होने के नाते, आप सोच सकते हैं: "MCP सर्वर वास्तव में क्या है, और मुझे इसकी परवाह क्यों करनी चाहिए?" आइए एक सरल उपमा से शुरू करें।

MCP सर्वरों को ऐसे विशेष सहायक के रूप में सोचें जो आपके AI कोडिंग साथी (जैसे GitHub Copilot) को बाहरी टूल्स और सेवाओं से जोड़ने में मदद करते हैं। जैसे आप अपने फोन पर अलग-अलग कामों के लिए अलग-अलग ऐप्स का उपयोग करते हैं—एक मौसम के लिए, एक नेविगेशन के लिए, एक बैंकिंग के लिए—वैसे ही MCP सर्वर आपके AI असिस्टेंट को विभिन्न विकास टूल्स और सेवाओं के साथ इंटरैक्ट करने की क्षमता देते हैं।

### MCP सर्वर किस समस्या को हल करते हैं

MCP सर्वरों से पहले, यदि आप चाहते थे:
- अपने Azure संसाधनों की जांच करें
- GitHub इश्यू बनाएं
- अपने डेटाबेस से क्वेरी करें
- दस्तावेज़ों में खोज करें

तो आपको कोडिंग रोकनी पड़ती थी, ब्राउज़र खोलना पड़ता था, संबंधित वेबसाइट पर जाना पड़ता था, और ये कार्य मैन्युअली करने पड़ते थे। यह लगातार संदर्भ बदलना आपके काम के प्रवाह को तोड़ता है और उत्पादकता कम करता है।

### MCP सर्वर आपके विकास अनुभव को कैसे बदलते हैं

MCP सर्वरों के साथ, आप अपने विकास वातावरण (VS Code, Visual Studio आदि) में रह सकते हैं और बस अपने AI असिस्टेंट से ये कार्य करने को कह सकते हैं। उदाहरण के लिए:

**पारंपरिक कार्यप्रवाह के बजाय:**
1. कोडिंग रोकें
2. ब्राउज़र खोलें
3. Azure पोर्टल पर जाएं
4. स्टोरेज अकाउंट विवरण देखें
5. VS Code पर वापस आएं
6. कोडिंग फिर से शुरू करें

**अब आप ऐसा कर सकते हैं:**
1. AI से पूछें: "मेरे Azure स्टोरेज अकाउंट्स की स्थिति क्या है?"
2. प्राप्त जानकारी के साथ कोडिंग जारी रखें

### शुरुआती लोगों के लिए मुख्य लाभ

#### 1. 🔄 **अपने फ्लो स्टेट में बने रहें**
- कई ऐप्स के बीच स्विचिंग नहीं करनी पड़ती
- आप जिस कोड पर काम कर रहे हैं उस पर ध्यान केंद्रित रखें
- विभिन्न टूल्स को मैनेज करने का मानसिक बोझ कम करें

#### 2. 🤖 **जटिल कमांड्स की बजाय प्राकृतिक भाषा का उपयोग करें**
- SQL सिंटैक्स याद रखने के बजाय बताएं कि आपको कौन सा डेटा चाहिए
- Azure CLI कमांड याद रखने के बजाय बताएं कि आप क्या करना चाहते हैं
- तकनीकी विवरण AI पर छोड़ें और आप लॉजिक पर ध्यान दें

#### 3. 🔗 **कई टूल्स को एक साथ जोड़ें**
- विभिन्न सेवाओं को मिलाकर शक्तिशाली वर्कफ़्लो बनाएं
- उदाहरण: "सभी हाल के GitHub इश्यू प्राप्त करें और उनके अनुसार Azure DevOps वर्क आइटम बनाएं"
- जटिल स्क्रिप्ट लिखे बिना ऑटोमेशन बनाएं

#### 4. 🌐 **एक बढ़ता हुआ इकोसिस्टम एक्सेस करें**
- Microsoft, GitHub और अन्य कंपनियों द्वारा बनाए गए सर्वरों का लाभ उठाएं
- विभिन्न विक्रेताओं के टूल्स को सहजता से मिलाएं
- एक मानकीकृत इकोसिस्टम का हिस्सा बनें जो विभिन्न AI असिस्टेंट्स के साथ काम करता है

#### 5. 🛠️ **करते हुए सीखें**
- अवधारणाओं को समझने के लिए पहले से बने सर्वरों से शुरुआत करें
- जैसे-जैसे आप सहज हों, अपने खुद के सर्वर बनाएं
- उपलब्ध SDKs और दस्तावेज़ों का उपयोग करके सीखने में मदद लें

### शुरुआती लोगों के लिए वास्तविक दुनिया का उदाहरण

मान लीजिए आप वेब विकास में नए हैं और अपने पहले प्रोजेक्ट पर काम कर रहे हैं। MCP सर्वर आपकी कैसे मदद कर सकते हैं:

**पारंपरिक तरीका:**
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**MCP सर्वरों के साथ:**
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### एंटरप्राइज स्टैंडर्ड का लाभ

MCP एक उद्योग-व्यापी मानक बनता जा रहा है, जिसका मतलब है:
- **संगति**: विभिन्न टूल्स और कंपनियों में समान अनुभव
- **इंटरऑपरेबिलिटी**: विभिन्न विक्रेताओं के सर्वर एक साथ काम करते हैं
- **भविष्य के लिए तैयार**: कौशल और सेटअप विभिन्न AI असिस्टेंट्स के बीच ट्रांसफर होते हैं
- **समुदाय**: साझा ज्ञान और संसाधनों का बड़ा इकोसिस्टम

### शुरुआत कैसे करें: आप क्या सीखेंगे

इस गाइड में, हम 10 Microsoft MCP सर्वरों का अन्वेषण करेंगे जो सभी स्तरों के डेवलपर्स के लिए विशेष रूप से उपयोगी हैं। प्रत्येक सर्वर को इस तरह डिज़ाइन किया गया है कि:
- सामान्य विकास चुनौतियों को हल करें
- दोहराए जाने वाले कार्यों को कम करें
- कोड की गुणवत्ता में सुधार करें
- सीखने के अवसर बढ़ाएं

> **💡 सीखने की टिप**
> 
> यदि आप MCP में बिल्कुल नए हैं, तो पहले हमारे [Introduction to MCP](../00-Introduction/README.md) और [Core Concepts](../01-CoreConcepts/README.md) मॉड्यूल्स से शुरुआत करें। फिर यहां वापस आकर इन अवधारणाओं को Microsoft के वास्तविक टूल्स के साथ देखें।
>
> MCP के महत्व पर अतिरिक्त संदर्भ के लिए, Maria Naggaga की पोस्ट देखें: [Connect Once, Integrate Anywhere with MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps)।

## VS Code और Visual Studio में MCP के साथ शुरुआत 🚀

यदि आप Visual Studio Code या Visual Studio 2022 के साथ GitHub Copilot का उपयोग कर रहे हैं, तो इन MCP सर्वरों को सेटअप करना आसान है।

### VS Code सेटअप

VS Code के लिए मूल प्रक्रिया इस प्रकार है:

1. **Agent Mode सक्षम करें**: VS Code में Copilot Chat विंडो में Agent मोड पर स्विच करें
2. **MCP सर्वर कॉन्फ़िगर करें**: अपने VS Code settings.json फ़ाइल में सर्वर कॉन्फ़िगरेशन जोड़ें
3. **सर्वर शुरू करें**: जिन सर्वरों का उपयोग करना चाहते हैं, उनके लिए "Start" बटन पर क्लिक करें
4. **टूल्स चुनें**: अपनी वर्तमान सत्र के लिए कौन से MCP सर्वर सक्षम करने हैं, चुनें

विस्तृत सेटअप निर्देशों के लिए [VS Code MCP दस्तावेज़](https://code.visualstudio.com/docs/copilot/copilot-mcp) देखें।

> **💡 प्रो टिप: MCP सर्वरों को प्रो की तरह मैनेज करें!**
> 
> VS Code Extensions व्यू में अब [इंस्टॉल किए गए MCP सर्वरों को मैनेज करने के लिए एक नया यूआई](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) शामिल है! आप किसी भी इंस्टॉल किए गए MCP सर्वर को जल्दी से शुरू, बंद और मैनेज कर सकते हैं। इसे आज़माएं!

### Visual Studio 2022 सेटअप

Visual Studio 2022 (संस्करण 17.14 या बाद का) के लिए:

1. **Agent Mode सक्षम करें**: GitHub Copilot Chat विंडो में "Ask" ड्रॉपडाउन पर क्लिक करें और "Agent" चुनें
2. **कॉन्फ़िगरेशन फ़ाइल बनाएं**: अपने सॉल्यूशन डायरेक्टरी में `.mcp.json` फ़ाइल बनाएं (सिफारिश की गई जगह: `<SOLUTIONDIR>\.mcp.json`)
3. **सर्वर कॉन्फ़िगर करें**: मानक MCP फॉर्मेट का उपयोग करके अपने MCP सर्वर कॉन्फ़िगरेशन जोड़ें
4. **टूल अनुमोदन**: जब पूछा जाए, तो उपयुक्त स्कोप अनुमतियों के साथ उपयोग करने के लिए टूल्स को अनुमोदित करें

विस्तृत Visual Studio सेटअप निर्देशों के लिए [Visual Studio MCP दस्तावेज़](https://learn.microsoft.com/visualstudio/ide/mcp-servers) देखें।

प्रत्येक MCP सर्वर के अपने कॉन्फ़िगरेशन आवश्यकताएं होती हैं (कनेक्शन स्ट्रिंग्स, प्रमाणीकरण आदि), लेकिन दोनों IDE में सेटअप पैटर्न समान रहता है।

## Microsoft MCP सर्वरों से सीखा गया पाठ 🛠️

### 1. 📚 Microsoft Learn Docs MCP Server

[![VS Code में इंस्टॉल करें](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![VS Code Insiders में इंस्टॉल करें](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**यह क्या करता है**: Microsoft Learn Docs MCP Server एक क्लाउड-होस्टेड सेवा है जो AI असिस्टेंट्स को Model Context Protocol के माध्यम से आधिकारिक Microsoft दस्तावेज़ों तक रियल-टाइम एक्सेस प्रदान करती है। यह `https://learn.microsoft.com/api/mcp` से जुड़ता है और Microsoft Learn, Azure दस्तावेज़, Microsoft 365 दस्तावेज़ और अन्य आधिकारिक Microsoft स्रोतों में सेमांटिक खोज सक्षम करता है।

**यह क्यों उपयोगी है**: भले ही यह "सिर्फ दस्तावेज़" जैसा लगे, यह सर्वर हर उस डेवलपर के लिए बेहद महत्वपूर्ण है जो Microsoft तकनीकों का उपयोग करता है। .NET डेवलपर्स की AI कोडिंग असिस्टेंट्स के बारे में सबसे बड़ी शिकायत यह है कि वे नवीनतम .NET और C# रिलीज़ के बारे में अपडेट नहीं रहते। Microsoft Learn Docs MCP Server इस समस्या को हल करता है, क्योंकि यह सबसे वर्तमान दस्तावेज़, API संदर्भ और सर्वोत्तम प्रथाओं तक रियल-टाइम पहुंच प्रदान करता है। चाहे आप नवीनतम Azure SDKs के साथ काम कर रहे हों, नए C# 13 फीचर्स का पता लगा रहे हों, या अत्याधुनिक .NET Aspire पैटर्न लागू कर रहे हों, यह सर्वर सुनिश्चित करता है कि आपका AI असिस्टेंट सटीक, आधुनिक कोड बनाने के लिए आधिकारिक और अपडेटेड जानकारी तक पहुंच रखता है।

**वास्तविक दुनिया में उपयोग**: "Microsoft Learn के आधिकारिक दस्तावेज़ के अनुसार Azure कंटेनर ऐप बनाने के लिए az cli कमांड क्या हैं?" या "ASP.NET Core में डिपेंडेंसी इंजेक्शन के साथ Entity Framework को कैसे कॉन्फ़िगर करें?" या "इस कोड की समीक्षा करें कि क्या यह Microsoft Learn Documentation में प्रदर्शन सिफारिशों से मेल खाता है।" यह सर्वर Microsoft Learn, Azure डॉक्यूमेंटेशन, और Microsoft 365 दस्तावेज़ों में व्यापक कवरेज प्रदान करता है, उन्नत सेमांटिक खोज का उपयोग करके सबसे प्रासंगिक जानकारी खोजता है। यह 10 उच्च गुणवत्ता वाली सामग्री खंडों के साथ लेख शीर्षक और URLs लौटाता है, हमेशा नवीनतम Microsoft दस्तावेज़ों तक पहुंच सुनिश्चित करता है।

**विशेष उदाहरण**: यह सर्वर `microsoft_docs_search` टूल प्रदान करता है जो Microsoft के आधिकारिक तकनीकी दस्तावेज़ों के खिलाफ सेमांटिक खोज करता है। एक बार कॉन्फ़िगर हो जाने पर, आप ऐसे प्रश्न पूछ सकते हैं जैसे "ASP.NET Core में JWT प्रमाणीकरण कैसे लागू करें?" और विस्तृत, आधिकारिक उत्तर स्रोत लिंक के साथ प्राप्त कर सकते हैं। खोज की गुणवत्ता असाधारण है क्योंकि यह संदर्भ को समझता है – Azure संदर्भ में "containers" के बारे में पूछने पर Azure Container Instances दस्तावेज़ लौटाता है, जबकि .NET संदर्भ में वही शब्द C# संग्रह जानकारी देता है।

यह विशेष रूप से तेजी से बदलने वाली या हाल ही में अपडेट की गई लाइब्रेरीज़ और उपयोग मामलों के लिए उपयोगी है। उदाहरण के लिए, हाल ही में कुछ कोडिंग प्रोजेक्ट्स में मैंने .NET Aspire और Microsoft.Extensions.AI के नवीनतम रिलीज़ में फीचर्स का उपयोग करना चाहा। Microsoft Learn Docs MCP सर्वर को शामिल करके, मैं न केवल API डॉक्यूमेंटेशन बल्कि हाल ही में प्रकाशित वॉकथ्रू और मार्गदर्शन का भी लाभ उठा पाया।
> **💡 प्रो टिप**  
>  
> यहां तक कि टूल-फ्रेंडली मॉडल्स को भी MCP टूल्स का उपयोग करने के लिए प्रोत्साहन की जरूरत होती है! आप एक सिस्टम प्रॉम्प्ट या [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) जोड़ने पर विचार कर सकते हैं, जैसे: "आपके पास `microsoft.docs.mcp` तक पहुंच है – इस टूल का उपयोग Microsoft तकनीकों जैसे C#, Azure, ASP.NET Core, या Entity Framework से संबंधित प्रश्नों को हल करते समय Microsoft की नवीनतम आधिकारिक दस्तावेज़ीकरण खोजने के लिए करें।"  
>  
> इसका एक बेहतरीन उदाहरण देखने के लिए, Awesome GitHub Copilot रिपॉजिटरी के [C# .NET Janitor चैट मोड](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) को देखें। यह मोड विशेष रूप से Microsoft Learn Docs MCP सर्वर का उपयोग करता है ताकि C# कोड को नवीनतम पैटर्न और सर्वोत्तम प्रथाओं के साथ साफ़ और आधुनिक बनाया जा सके।
### 2. ☁️ Azure MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**यह क्या करता है**: Azure MCP Server 15+ विशेष Azure सेवा कनेक्टर्स का एक व्यापक सेट है जो पूरे Azure इकोसिस्टम को आपके AI वर्कफ़्लो में लाता है। यह केवल एक सर्वर नहीं है – बल्कि एक शक्तिशाली संग्रह है जिसमें रिसोर्स मैनेजमेंट, डेटाबेस कनेक्टिविटी (PostgreSQL, SQL Server), Azure Monitor लॉग विश्लेषण KQL के साथ, Cosmos DB इंटीग्रेशन और भी बहुत कुछ शामिल है।

**यह क्यों उपयोगी है**: Azure संसाधनों के प्रबंधन से परे, यह सर्वर Azure SDKs के साथ काम करते समय कोड की गुणवत्ता को काफी बेहतर बनाता है। जब आप Azure MCP को Agent मोड में उपयोग करते हैं, तो यह केवल कोड लिखने में मदद नहीं करता – बल्कि *बेहतर* Azure कोड लिखने में मदद करता है जो वर्तमान प्रमाणीकरण पैटर्न, त्रुटि हैंडलिंग सर्वोत्तम प्रथाओं का पालन करता है और नवीनतम SDK फीचर्स का उपयोग करता है। आपको सामान्य कोड नहीं मिलता जो शायद काम करे, बल्कि ऐसा कोड मिलता है जो Azure के उत्पादन वर्कलोड के लिए अनुशंसित पैटर्न का पालन करता है।

**मुख्य मॉड्यूल शामिल हैं**:
- **🗄️ डेटाबेस कनेक्टर्स**: Azure Database for PostgreSQL और SQL Server के लिए सीधे प्राकृतिक भाषा एक्सेस
- **📊 Azure Monitor**: KQL-संचालित लॉग विश्लेषण और परिचालन अंतर्दृष्टि
- **🌐 रिसोर्स मैनेजमेंट**: पूर्ण Azure रिसोर्स लाइफसाइकल प्रबंधन
- **🔐 प्रमाणीकरण**: DefaultAzureCredential और मैनेज्ड आइडेंटिटी पैटर्न
- **📦 स्टोरेज सेवाएं**: Blob Storage, Queue Storage, और Table Storage ऑपरेशंस
- **🚀 कंटेनर सेवाएं**: Azure Container Apps, Container Instances, और AKS प्रबंधन
- **और कई अन्य विशेष कनेक्टर्स**

**वास्तविक उपयोग**: "मेरे Azure स्टोरेज अकाउंट्स की सूची बनाओ", "पिछले घंटे में मेरी Log Analytics वर्कस्पेस में त्रुटियों के लिए क्वेरी चलाओ", या "Node.js का उपयोग करके उचित प्रमाणीकरण के साथ एक Azure एप्लिकेशन बनाने में मदद करो"

**पूर्ण डेमो परिदृश्य**: यहाँ एक पूरा वॉकथ्रू है जो दिखाता है कि Azure MCP को GitHub Copilot for Azure एक्सटेंशन के साथ VS Code में मिलाकर कैसे शक्तिशाली बनाया जा सकता है। जब आपके पास दोनों इंस्टॉल हों और आप पूछें:

> "एक Python स्क्रिप्ट बनाओ जो DefaultAzureCredential प्रमाणीकरण का उपयोग करके Azure Blob Storage में एक फ़ाइल अपलोड करे। स्क्रिप्ट को मेरे Azure स्टोरेज अकाउंट 'mycompanystorage' से कनेक्ट होना चाहिए, 'documents' नाम के कंटेनर में अपलोड करना चाहिए, वर्तमान टाइमस्टैम्प के साथ एक टेस्ट फ़ाइल बनानी चाहिए, त्रुटियों को सही ढंग से संभालना चाहिए और सूचनात्मक आउटपुट देना चाहिए, प्रमाणीकरण और त्रुटि हैंडलिंग के लिए Azure की सर्वोत्तम प्रथाओं का पालन करना चाहिए, DefaultAzureCredential प्रमाणीकरण कैसे काम करता है यह समझाने वाले कमेंट्स शामिल होने चाहिए, और स्क्रिप्ट को उचित फ़ंक्शंस और दस्तावेज़ीकरण के साथ अच्छी तरह संरचित बनाना चाहिए।"

Azure MCP Server एक पूर्ण, उत्पादन-तैयार Python स्क्रिप्ट बनाएगा जो:
- नवीनतम Azure Blob Storage SDK का उपयोग करता है और उचित async पैटर्न अपनाता है
- DefaultAzureCredential को व्यापक fallback चेन व्याख्या के साथ लागू करता है
- विशिष्ट Azure अपवाद प्रकारों के साथ मजबूत त्रुटि हैंडलिंग शामिल करता है
- Azure SDK सर्वोत्तम प्रथाओं का पालन करता है जैसे रिसोर्स मैनेजमेंट और कनेक्शन हैंडलिंग
- विस्तृत लॉगिंग और सूचनात्मक कंसोल आउटपुट प्रदान करता है
- फ़ंक्शंस, दस्तावेज़ीकरण, और टाइप हिंट्स के साथ अच्छी तरह से संरचित स्क्रिप्ट बनाता है

इसकी खास बात यह है कि Azure MCP के बिना, आपको सामान्य ब्लॉब स्टोरेज कोड मिल सकता है जो काम तो करता है लेकिन वर्तमान Azure पैटर्न का पालन नहीं करता। Azure MCP के साथ, आपको ऐसा कोड मिलता है जो नवीनतम प्रमाणीकरण विधियों का उपयोग करता है, Azure-विशिष्ट त्रुटि परिदृश्यों को संभालता है, और Microsoft की उत्पादन अनुप्रयोगों के लिए अनुशंसित प्रथाओं का पालन करता है।

**विशेष उदाहरण**: मुझे `az` और `azd` CLI के विशिष्ट कमांड याद रखने में हमेशा दिक्कत होती है। मेरे लिए यह हमेशा दो-चरणीय प्रक्रिया होती है: पहले सिंटैक्स देखना, फिर कमांड चलाना। मैं अक्सर पोर्टल में जाकर क्लिक करके काम करता हूँ क्योंकि मैं स्वीकार नहीं करना चाहता कि मुझे CLI सिंटैक्स याद नहीं है। जो मैं चाहता हूँ उसे बस वर्णन कर पाना अद्भुत है, और उससे भी बेहतर है कि मैं यह सब अपने IDE को छोड़े बिना कर सकूँ!

शुरुआत करने के लिए [Azure MCP रिपॉजिटरी](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) में उपयोग के मामलों की एक बेहतरीन सूची है। व्यापक सेटअप गाइड और उन्नत कॉन्फ़िगरेशन विकल्पों के लिए, [आधिकारिक Azure MCP दस्तावेज़](https://learn.microsoft.com/azure/developer/azure-mcp-server/) देखें।

### 3. 🐙 GitHub MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**यह क्या करता है**: आधिकारिक GitHub MCP Server GitHub के पूरे इकोसिस्टम के साथ सहज एकीकरण प्रदान करता है, जिसमें होस्टेड रिमोट एक्सेस और लोकल Docker डिप्लॉयमेंट विकल्प शामिल हैं। यह केवल बुनियादी रिपॉजिटरी ऑपरेशंस तक सीमित नहीं है – बल्कि एक व्यापक टूलकिट है जिसमें GitHub Actions प्रबंधन, पुल रिक्वेस्ट वर्कफ़्लोज़, इशू ट्रैकिंग, सुरक्षा स्कैनिंग, नोटिफिकेशन, और उन्नत ऑटोमेशन क्षमताएं शामिल हैं।

**यह क्यों उपयोगी है**: यह सर्वर GitHub के साथ आपके इंटरैक्शन को पूरी तरह बदल देता है, जिससे पूरा प्लेटफ़ॉर्म अनुभव सीधे आपके विकास वातावरण में आ जाता है। प्रोजेक्ट प्रबंधन, कोड समीक्षा, और CI/CD मॉनिटरिंग के लिए बार-बार VS Code और GitHub.com के बीच स्विच करने के बजाय, आप प्राकृतिक भाषा कमांड के माध्यम से सब कुछ संभाल सकते हैं और अपने कोड पर ध्यान केंद्रित रख सकते हैं।

> **ℹ️ नोट: 'एजेंट्स' के विभिन्न प्रकार**
> 
> इस GitHub MCP Server को GitHub के Coding Agent (जो AI एजेंट है जिसे आप ऑटोमेटेड कोडिंग कार्यों के लिए इशू असाइन कर सकते हैं) से भ्रमित न करें। GitHub MCP Server VS Code के Agent मोड में GitHub API इंटीग्रेशन प्रदान करता है, जबकि GitHub का Coding Agent एक अलग फीचर है जो GitHub इशूज को असाइन किए जाने पर पुल रिक्वेस्ट बनाता है।

**मुख्य क्षमताएं शामिल हैं**:
- **⚙️ GitHub Actions**: पूर्ण CI/CD पाइपलाइन प्रबंधन, वर्कफ़्लो मॉनिटरिंग, और आर्टिफैक्ट हैंडलिंग
- **🔀 पुल रिक्वेस्ट्स**: PR बनाना, समीक्षा करना, मर्ज करना, और व्यापक स्थिति ट्रैकिंग के साथ प्रबंधन
- **🐛 इशूज**: पूर्ण इशू लाइफसाइकल प्रबंधन, कमेंटिंग, लेबलिंग, और असाइनमेंट
- **🔒 सुरक्षा**: कोड स्कैनिंग अलर्ट, सीक्रेट डिटेक्शन, और Dependabot इंटीग्रेशन
- **🔔 नोटिफिकेशन**: स्मार्ट नोटिफिकेशन प्रबंधन और रिपॉजिटरी सब्सक्रिप्शन नियंत्रण
- **📁 रिपॉजिटरी प्रबंधन**: फ़ाइल ऑपरेशंस, ब्रांच प्रबंधन, और रिपॉजिटरी प्रशासन
- **👥 सहयोग**: उपयोगकर्ता और संगठन खोज, टीम प्रबंधन, और एक्सेस नियंत्रण

**वास्तविक उपयोग**: "मेरी फीचर ब्रांच से एक पुल रिक्वेस्ट बनाओ", "इस सप्ताह मेरी सभी असफल CI रन दिखाओ", "मेरे रिपॉजिटरी के लिए खुले सुरक्षा अलर्ट की सूची बनाओ", या "मेरे सभी संगठनों में मेरे लिए असाइन किए गए सभी इशू खोजो"

**पूर्ण डेमो परिदृश्य**: यहाँ एक शक्तिशाली वर्कफ़्लो है जो GitHub MCP Server की क्षमताओं को दिखाता है:

> "मुझे हमारे स्प्रिंट समीक्षा की तैयारी करनी है। इस सप्ताह मैंने जो सभी पुल रिक्वेस्ट बनाए हैं दिखाओ, हमारे CI/CD पाइपलाइनों की स्थिति जांचो, किसी भी सुरक्षा अलर्ट का सारांश बनाओ जिन्हें हमें संबोधित करना है, और मर्ज किए गए PRs के 'feature' लेबल के आधार पर रिलीज नोट्स ड्राफ्ट करने में मदद करो।"

GitHub MCP Server:
- आपके हाल के पुल रिक्वेस्ट्स की विस्तृत स्थिति जानकारी के साथ क्वेरी करेगा
- वर्कफ़्लो रन का विश्लेषण करेगा और किसी भी विफलता या प्रदर्शन समस्याओं को हाइलाइट करेगा
- सुरक्षा स्कैनिंग परिणामों को संकलित करेगा और महत्वपूर्ण अलर्ट को प्राथमिकता देगा
- मर्ज किए गए PRs से जानकारी निकालकर व्यापक रिलीज नोट्स बनाएगा
- स्प्रिंट योजना और रिलीज तैयारी के लिए क्रियाशील अगले कदम प्रदान करेगा

**विशेष उदाहरण**: मैं इसे कोड समीक्षा वर्कफ़्लोज़ के लिए बहुत पसंद करता हूँ। VS Code, GitHub नोटिफिकेशन, और पुल रिक्वेस्ट पेजों के बीच कूदने के बजाय, मैं कह सकता हूँ "मेरे समीक्षा के लिए सभी PR दिखाओ" और फिर "PR #123 में प्रमाणीकरण विधि में त्रुटि हैंडलिंग के बारे में एक टिप्पणी जोड़ो।" सर्वर GitHub API कॉल्स को संभालता है, चर्चा का संदर्भ बनाए रखता है, और मुझे अधिक रचनात्मक समीक्षा टिप्पणियाँ बनाने में मदद करता है।

**प्रमाणीकरण विकल्प**: सर्वर OAuth (VS Code में सहज) और Personal Access Tokens दोनों का समर्थन करता है, साथ ही कॉन्फ़िगर करने योग्य टूलसेट्स के साथ जो केवल आवश्यक GitHub कार्यक्षमता को सक्षम करते हैं। आप इसे रिमोट होस्टेड सेवा के रूप में तुरंत सेटअप के लिए चला सकते हैं या पूर्ण नियंत्रण के लिए लोकल Docker के माध्यम से चला सकते हैं।

> **💡 प्रो टिप**
> 
> अपने MCP सर्वर सेटिंग्स में `--toolsets` पैरामीटर को कॉन्फ़िगर करके केवल आवश्यक टूलसेट्स सक्षम करें ताकि संदर्भ आकार कम हो और AI टूल चयन बेहतर हो। उदाहरण के लिए, कोर विकास वर्कफ़्लोज़ के लिए `"--toolsets", "repos,issues,pull_requests,actions"` जोड़ें, या यदि आप मुख्य रूप से GitHub मॉनिटरिंग चाहते हैं तो `"--toolsets", "notifications, security"` का उपयोग करें।

### 4. 🔄 Azure DevOps MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_DevOps_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_DevOps_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/azure-devops-mcp)

**यह क्या करता है**: Azure DevOps सेवाओं से कनेक्ट होता है ताकि व्यापक प्रोजेक्ट प्रबंधन, वर्क आइटम ट्रैकिंग, बिल्ड पाइपलाइन प्रबंधन, और रिपॉजिटरी ऑपरेशंस किए जा सकें।

**यह क्यों उपयोगी है**: जिन टीमों के लिए Azure DevOps उनका मुख्य DevOps प्लेटफ़ॉर्म है, यह MCP सर्वर आपके विकास वातावरण और Azure DevOps वेब इंटरफ़ेस के बीच बार-बार टैब स्विचिंग को खत्म कर देता है। आप अपने AI असिस्टेंट से सीधे वर्क आइटम प्रबंधित कर सकते हैं, बिल्ड स्टेटस देख सकते हैं, रिपॉजिटरी क्वेरी कर सकते हैं, और प्रोजेक्ट प्रबंधन कार्य कर सकते हैं।

**वास्तविक उपयोग**: "WebApp प्रोजेक्ट के वर्तमान स्प्रिंट में सभी सक्रिय वर्क आइटम दिखाओ", "मैंने अभी जो लॉगिन समस्या पाई है उसके लिए एक बग रिपोर्ट बनाओ", या "हमारे बिल्ड पाइपलाइनों की स्थिति जांचो और हाल की किसी भी विफलता को दिखाओ"

**विशेष उदाहरण**: आप आसानी से अपनी टीम के वर्तमान स्प्रिंट की स्थिति एक सरल क्वेरी से देख सकते हैं जैसे "WebApp प्रोजेक्ट के वर्तमान स्प्रिंट में सभी सक्रिय वर्क आइटम दिखाओ" या "मैंने अभी जो लॉगिन समस्या पाई है उसके लिए एक बग रिपोर्ट बनाओ" बिना अपने विकास वातावरण छोड़े।

### 5. 📝 MarkItDown MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**यह क्या करता है**: MarkItDown एक व्यापक दस्तावेज़ रूपांतरण सर्वर है जो विभिन्न फ़ाइल स्वरूपों को उच्च गुणवत्ता वाले Markdown में बदलता है, जिसे LLM उपभोग और टेक्स्ट विश्लेषण वर्कफ़्लोज़ के लिए अनुकूलित किया गया है।

**यह क्यों उपयोगी है**: आधुनिक दस्तावेज़ीकरण वर्कफ़्लोज़ के लिए आवश्यक! MarkItDown कई फ़ाइल स्वरूपों को संभालता है और महत्वपूर्ण दस्तावेज़ संरचना जैसे शीर्षक, सूचियाँ, तालिकाएँ, और लिंक को संरक्षित रखता है। साधारण टेक्स्ट एक्सट्रैक्शन टूल्स के विपरीत, यह सेमांटिक अर्थ और फॉर्मेटिंग को बनाए रखने पर केंद्रित है, जो AI प्रोसेसिंग और मानव पठनीयता दोनों के लिए महत्वपूर्ण है।

**समर्थित फ़ाइल स्वरूप**:
- **ऑफिस दस्तावेज़**: PDF, PowerPoint (PPTX), Word (DOCX), Excel (XLSX/XLS)
- **मीडिया फ़ाइलें**: छवियाँ (EXIF मेटाडेटा और OCR के साथ), ऑडियो (EXIF मेटाडेटा और भाषण ट्रांसक्रिप्शन के साथ)
- **वेब सामग्री**: HTML, RSS फ़ीड, YouTube URL, विकिपीडिया पेज
- **डेटा स्वरूप**: CSV, JSON, XML, ZIP फ़ाइलें (सामग्री को पुनरावृत्त रूप से संसाधित करता है)
- **प्रकाशन स्वरूप**: EPub, Jupyter नोटबुक (.ipynb)
- **ईमेल**: Outlook संदेश (.msg)
- **उन्नत**: बेहतर PDF प्रोसेसिंग के लिए Azure Document Intelligence इंटीग्रेशन

**उन्नत क्षमताएँ**: MarkItDown LLM-संचालित छवि विवरण (जब OpenAI क्लाइंट उपलब्ध हो), Azure Document Intelligence के साथ बेहतर PDF प्रोसेसिंग, भाषण सामग्री के लिए ऑडियो ट्रांसक्रिप्शन, और अतिरिक्त फ़ाइल स्वरूपों के लिए प्लगइन सिस्टम का समर्थन करता है।

**वास्तविक उपयोग**: "इस PowerPoint प्रस्तुति को Markdown में बदलें ताकि हमारी दस्तावेज़ साइट पर उपयोग हो सके", "इस PDF से सही शीर्षक संरचना के साथ टेक्स्ट निकालें", या "इस Excel स्प्रेडशीट को पठनीय तालिका स्वरूप में बदलें"

**विशेष उदाहरण**: [MarkItDown दस्तावेज़](https://github.com/microsoft/markitdown#why-markdown) से उद्धरण:


> Markdown लगभग सादा टेक्स्ट के समान है, जिसमें न्यूनतम मार्कअप या फॉर्मेटिंग होती है, फिर भी यह महत्वपूर्ण दस्तावेज़ संरचना को प्रदर्शित करने का तरीका प्रदान करता है। मुख्यधारा के LLMs, जैसे OpenAI का GPT-4o, स्वाभाविक रूप से Markdown "बोलते" हैं, और अक्सर बिना पूछे अपने उत्तरों में Markdown शामिल करते हैं। यह दर्शाता है कि इन्हें विशाल मात्रा में Markdown-फॉर्मेटेड टेक्स्ट पर प्रशिक्षित किया गया है और वे इसे अच्छी तरह समझते हैं। एक अतिरिक्त लाभ के रूप में, Markdown कन्वेंशन्स टोकन-कुशल भी हैं।

MarkItDown दस्तावेज़ संरचना को बनाए रखने में बहुत अच्छा है, जो AI वर्कफ़्लोज़ के लिए महत्वपूर्ण है। उदाहरण के लिए, PowerPoint प्रस्तुति को कन्वर्ट करते समय, यह स्लाइड संगठन को सही शीर्षकों के साथ रखता है, तालिकाओं को Markdown तालिकाओं के रूप में निकालता है, छवियों के लिए alt टेक्स्ट शामिल करता है, और स्पीकर नोट्स को भी प्रोसेस करता है। चार्ट्स को पठनीय डेटा तालिकाओं में बदला जाता है, और परिणामी Markdown मूल प्रस्तुति के तार्किक प्रवाह को बनाए रखता है। यह AI सिस्टम में प्रस्तुति सामग्री फीड करने या मौजूदा स्लाइड से दस्तावेज़ीकरण बनाने के लिए आदर्श बनाता है।

### 6. 🗃️ SQL Server MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**यह क्या करता है**: SQL Server डेटाबेस (ऑन-प्रिमाइसेस, Azure SQL, या Fabric) के लिए संवादात्मक पहुँच प्रदान करता है।

**यह क्यों उपयोगी है**: PostgreSQL सर्वर के समान लेकिन Microsoft SQL इकोसिस्टम के लिए। एक सरल कनेक्शन स्ट्रिंग के साथ जुड़ें और प्राकृतिक भाषा में क्वेरी करना शुरू करें – अब संदर्भ बदलने की जरूरत नहीं!

**वास्तविक उपयोग**: "पिछले 30 दिनों में जिन सभी ऑर्डर को पूरा नहीं किया गया है, उन्हें खोजें" को उपयुक्त SQL क्वेरी में अनुवादित किया जाता है और स्वरूपित परिणाम लौटाता है।

**विशेष उदाहरण**: एक बार जब आप अपना डेटाबेस कनेक्शन सेट कर लेते हैं, तो आप तुरंत अपने डेटा के साथ बातचीत शुरू कर सकते हैं। ब्लॉग पोस्ट में इसे एक सरल प्रश्न के साथ दिखाया गया है: "आप किस डेटाबेस से जुड़े हैं?" MCP सर्वर उपयुक्त डेटाबेस टूल को कॉल करता है, आपके SQL Server इंस्टेंस से जुड़ता है, और आपके वर्तमान डेटाबेस कनेक्शन के विवरण लौटाता है – बिना एक भी SQL लाइन लिखे। सर्वर स्कीमा प्रबंधन से लेकर डेटा हेरफेर तक व्यापक डेटाबेस ऑपरेशंस का समर्थन करता है, सभी प्राकृतिक भाषा प्रॉम्प्ट के माध्यम से। VS Code और Claude Desktop के साथ पूर्ण सेटअप निर्देश और कॉन्फ़िगरेशन उदाहरणों के लिए देखें: [Introducing MSSQL MCP Server (Preview)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/)।

### 7. 🎭 Playwright MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**यह क्या करता है**: AI एजेंट्स को वेब पेजों के साथ इंटरैक्ट करने देता है, जो परीक्षण और ऑटोमेशन के लिए उपयोगी है।

> **ℹ️ GitHub Copilot को शक्ति प्रदान करना**
> 
> Playwright MCP Server GitHub Copilot के Coding Agent को वेब ब्राउज़िंग क्षमताएँ देता है! [इस फीचर के बारे में अधिक जानें](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/)।

**यह क्यों उपयोगी है**: प्राकृतिक भाषा विवरणों द्वारा संचालित स्वचालित परीक्षण के लिए परफेक्ट। AI वेबसाइटों पर नेविगेट कर सकता है, फॉर्म भर सकता है, और संरचित एक्सेसिबिलिटी स्नैपशॉट के माध्यम से डेटा निकाल सकता है – यह बेहद शक्तिशाली है!

**वास्तविक उपयोग**: "लॉगिन फ्लो का परीक्षण करें और सुनिश्चित करें कि डैशबोर्ड सही ढंग से लोड हो रहा है" या "ऐसा परीक्षण बनाएं जो उत्पादों की खोज करे और परिणाम पृष्ठ को सत्यापित करे" – वह भी बिना एप्लिकेशन के स्रोत कोड की जरूरत के।

**विशेष उदाहरण**: मेरी टीम की सदस्य Debbie O'Brien ने हाल ही में Playwright MCP Server के साथ शानदार काम किया है! उदाहरण के लिए, उन्होंने दिखाया कि कैसे बिना एप्लिकेशन के स्रोत कोड के भी पूर्ण Playwright परीक्षण बनाए जा सकते हैं। उनके परिदृश्य में, उन्होंने Copilot से एक मूवी खोज ऐप के लिए परीक्षण बनाने को कहा: साइट पर जाएं, "Garfield" खोजें, और सुनिश्चित करें कि मूवी परिणामों में दिखाई दे। MCP ने ब्राउज़र सत्र शुरू किया, DOM स्नैपशॉट का उपयोग करके पेज संरचना का पता लगाया, सही सेलेक्टर्स खोजे, और एक पूरी तरह काम करने वाला TypeScript परीक्षण बनाया जो पहली बार में पास हो गया।

इसकी ताकत यह है कि यह प्राकृतिक भाषा निर्देशों और निष्पादित परीक्षण कोड के बीच पुल बनाता है। पारंपरिक तरीके या तो मैनुअल परीक्षण लेखन की मांग करते हैं या संदर्भ के लिए कोडबेस की जरूरत होती है। लेकिन Playwright MCP के साथ, आप बाहरी साइटों, क्लाइंट एप्लिकेशन, या ब्लैक-बॉक्स परीक्षण परिदृश्यों में परीक्षण कर सकते हैं जहाँ कोड एक्सेस उपलब्ध नहीं है।

### 8. 💻 Dev Box MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**यह क्या करता है**: प्राकृतिक भाषा के माध्यम से Microsoft Dev Box वातावरणों का प्रबंधन करता है।

**यह क्यों उपयोगी है**: विकास वातावरण प्रबंधन को बेहद सरल बनाता है! विशिष्ट कमांड याद किए बिना विकास वातावरण बनाएं, कॉन्फ़िगर करें और प्रबंधित करें।

**वास्तविक उपयोग**: "नया Dev Box सेट करें जिसमें नवीनतम .NET SDK हो और इसे हमारे प्रोजेक्ट के लिए कॉन्फ़िगर करें", "मेरे सभी विकास वातावरण की स्थिति जांचें", या "हमारी टीम प्रस्तुतियों के लिए एक मानकीकृत डेमो वातावरण बनाएं"

**विशेष उदाहरण**: मैं व्यक्तिगत विकास के लिए Dev Box का उपयोग करना पसंद करता हूँ। मेरा सबसे बड़ा अनुभव तब हुआ जब James Montemagno ने बताया कि Dev Box सम्मेलन डेमो के लिए कितना बढ़िया है, क्योंकि इसमें सुपर-फास्ट ईथरनेट कनेक्शन होता है, चाहे मैं किसी भी सम्मेलन, होटल या हवाई जहाज के वाईफाई का उपयोग कर रहा हूँ। वास्तव में, मैंने हाल ही में बस से Bruges से Antwerp जाते हुए अपने फोन हॉटस्पॉट से जुड़ा लैपटॉप लेकर सम्मेलन डेमो अभ्यास किया! अगला कदम है टीम के लिए कई विकास वातावरणों और मानकीकृत डेमो वातावरणों का प्रबंधन करना। और एक बड़ा उपयोग मामला जो मैंने ग्राहकों और सहकर्मियों से सुना है, वह है Dev Box का प्री-कॉन्फ़िगर विकास वातावरण के लिए उपयोग। दोनों मामलों में, MCP का उपयोग करके Dev Boxes को कॉन्फ़िगर और प्रबंधित करना प्राकृतिक भाषा इंटरैक्शन की सुविधा देता है, जबकि आप अपने विकास वातावरण में ही रहते हैं।

### 9. 🤖 Azure AI Foundry MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**यह क्या करता है**: Azure AI Foundry MCP Server डेवलपर्स को Azure के AI इकोसिस्टम तक व्यापक पहुंच प्रदान करता है, जिसमें मॉडल कैटलॉग, डिप्लॉयमेंट प्रबंधन, Azure AI Search के साथ नॉलेज इंडेक्सिंग, और मूल्यांकन उपकरण शामिल हैं। यह प्रायोगिक सर्वर AI विकास और Azure की शक्तिशाली AI इन्फ्रास्ट्रक्चर के बीच की खाई को पाटता है, जिससे AI एप्लिकेशन बनाना, डिप्लॉय करना और उनका मूल्यांकन करना आसान हो जाता है।

**यह क्यों उपयोगी है**: यह सर्वर Azure AI सेवाओं के साथ आपके काम करने के तरीके को बदल देता है, एंटरप्राइज-ग्रेड AI क्षमताओं को सीधे आपके विकास वर्कफ़्लो में लाकर। Azure पोर्टल, दस्तावेज़, और आपके IDE के बीच बार-बार स्विच करने के बजाय, आप प्राकृतिक भाषा कमांड के माध्यम से मॉडल खोज सकते हैं, सेवाएं डिप्लॉय कर सकते हैं, नॉलेज बेस प्रबंधित कर सकते हैं, और AI प्रदर्शन का मूल्यांकन कर सकते हैं। यह विशेष रूप से उन डेवलपर्स के लिए शक्तिशाली है जो RAG (Retrieval-Augmented Generation) एप्लिकेशन बना रहे हैं, मल्टी-मॉडल डिप्लॉयमेंट्स का प्रबंधन कर रहे हैं, या व्यापक AI मूल्यांकन पाइपलाइनों को लागू कर रहे हैं।

**मुख्य डेवलपर क्षमताएं**:
- **🔍 मॉडल खोज और डिप्लॉयमेंट**: Azure AI Foundry के मॉडल कैटलॉग का अन्वेषण करें, कोड उदाहरणों के साथ विस्तृत मॉडल जानकारी प्राप्त करें, और मॉडल को Azure AI सेवाओं पर डिप्लॉय करें
- **📚 नॉलेज प्रबंधन**: Azure AI Search इंडेक्स बनाएं और प्रबंधित करें, दस्तावेज़ जोड़ें, इंडेक्सर कॉन्फ़िगर करें, और परिष्कृत RAG सिस्टम बनाएं
- **⚡ AI एजेंट इंटीग्रेशन**: Azure AI एजेंट्स से कनेक्ट करें, मौजूदा एजेंट्स से प्रश्न पूछें, और प्रोडक्शन परिदृश्यों में एजेंट प्रदर्शन का मूल्यांकन करें
- **📊 मूल्यांकन फ्रेमवर्क**: व्यापक टेक्स्ट और एजेंट मूल्यांकन चलाएं, मार्कडाउन रिपोर्ट बनाएं, और AI एप्लिकेशन के लिए गुणवत्ता आश्वासन लागू करें
- **🚀 प्रोटोटाइपिंग टूल्स**: GitHub-आधारित प्रोटोटाइपिंग के लिए सेटअप निर्देश प्राप्त करें और Azure AI Foundry Labs तक पहुंचें जो अत्याधुनिक अनुसंधान मॉडल प्रदान करता है

**वास्तविक दुनिया में डेवलपर उपयोग**: "अपने एप्लिकेशन के लिए Phi-4 मॉडल को Azure AI सेवाओं पर डिप्लॉय करें", "मेरे दस्तावेज़ीकरण RAG सिस्टम के लिए नया सर्च इंडेक्स बनाएं", "मेरे एजेंट के उत्तरों का गुणवत्ता मेट्रिक्स के खिलाफ मूल्यांकन करें", या "मेरे जटिल विश्लेषण कार्यों के लिए सबसे अच्छा reasoning मॉडल खोजें"

**पूर्ण डेमो परिदृश्य**: यहाँ एक शक्तिशाली AI विकास वर्कफ़्लो है:


> "मैं एक कस्टमर सपोर्ट एजेंट बना रहा हूँ। मुझे कैटलॉग से एक अच्छा reasoning मॉडल खोजने में मदद करें, उसे Azure AI सेवाओं पर डिप्लॉय करें, हमारे दस्तावेज़ीकरण से एक नॉलेज बेस बनाएं, प्रतिक्रिया गुणवत्ता जांचने के लिए एक मूल्यांकन फ्रेमवर्क सेट करें, और फिर परीक्षण के लिए GitHub टोकन के साथ इंटीग्रेशन प्रोटोटाइप बनाने में मदद करें।"

Azure AI Foundry MCP Server यह करेगा:
- आपकी आवश्यकताओं के आधार पर मॉडल कैटलॉग से उपयुक्त reasoning मॉडल की सिफारिश करेगा
- आपके पसंदीदा Azure क्षेत्र के लिए डिप्लॉयमेंट कमांड और कोटा जानकारी प्रदान करेगा
- आपके दस्तावेज़ीकरण के लिए उचित स्कीमा के साथ Azure AI Search इंडेक्स सेट करेगा
- गुणवत्ता मेट्रिक्स और सुरक्षा जांच के साथ मूल्यांकन पाइपलाइनों को कॉन्फ़िगर करेगा
- तत्काल परीक्षण के लिए GitHub प्रमाणीकरण के साथ प्रोटोटाइपिंग कोड जनरेट करेगा
- आपकी विशिष्ट तकनीकी स्टैक के लिए व्यापक सेटअप गाइड प्रदान करेगा

**विशेष उदाहरण**: एक डेवलपर के रूप में, मैं विभिन्न LLM मॉडलों के साथ बने रहना मुश्किल पाता था। मैं कुछ मुख्य मॉडलों को जानता हूँ, लेकिन ऐसा लगता था कि मैं कुछ उत्पादकता और दक्षता लाभों से वंचित रह रहा हूँ। टोकन और कोटा प्रबंधन तनावपूर्ण और जटिल है – मुझे कभी पता नहीं चलता कि मैं सही कार्य के लिए सही मॉडल चुन रहा हूँ या बजट को अनावश्यक रूप से खर्च कर रहा हूँ। मैंने इस MCP Server के बारे में James Montemagno से सुना जब मैं टीम के साथ MCP Server की सिफारिशों के बारे में बात कर रहा था, और मैं इसे इस्तेमाल करने के लिए उत्साहित हूँ! मॉडल खोज क्षमताएं खासकर मेरे जैसे किसी के लिए प्रभावशाली हैं जो सामान्य मॉडलों से परे जाकर विशिष्ट कार्यों के लिए अनुकूलित मॉडल खोजना चाहता है। मूल्यांकन फ्रेमवर्क मुझे यह सुनिश्चित करने में मदद करेगा कि मैं वास्तव में बेहतर परिणाम प्राप्त कर रहा हूँ, न कि केवल कुछ नया आज़माने के लिए।

> **ℹ️ प्रायोगिक स्थिति**
> 
> यह MCP सर्वर प्रायोगिक है और सक्रिय विकास में है। फीचर्स और APIs में बदलाव हो सकते हैं। Azure AI क्षमताओं का अन्वेषण करने और प्रोटोटाइप बनाने के लिए उपयुक्त, लेकिन उत्पादन उपयोग के लिए स्थिरता आवश्यकताओं का सत्यापन करें।

### 10. 🏢 Microsoft 365 Agents Toolkit MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**यह क्या करता है**: डेवलपर्स को Microsoft 365 और Microsoft 365 Copilot के साथ इंटीग्रेट होने वाले AI एजेंट्स और एप्लिकेशन बनाने के लिए आवश्यक टूल्स प्रदान करता है, जिसमें स्कीमा वैलिडेशन, सैंपल कोड प्राप्ति, और समस्या निवारण सहायता शामिल है।

**यह क्यों उपयोगी है**: Microsoft 365 और Copilot के लिए विकास में जटिल मैनिफेस्ट स्कीमा और विशिष्ट विकास पैटर्न शामिल होते हैं। यह MCP सर्वर आपके कोडिंग वातावरण में सीधे आवश्यक विकास संसाधन लाता है, जिससे आप स्कीमा वैलिडेट कर सकते हैं, सैंपल कोड खोज सकते हैं, और सामान्य समस्याओं का समाधान कर सकते हैं बिना बार-बार दस्तावेज़ों को देखे।

**वास्तविक दुनिया में उपयोग**: "मेरे डिक्लेरेटिव एजेंट मैनिफेस्ट को वैलिडेट करें और कोई भी स्कीमा त्रुटि ठीक करें", "Microsoft Graph API प्लगइन लागू करने के लिए सैंपल कोड दिखाएं", या "मेरे Teams ऐप प्रमाणीकरण मुद्दों को हल करने में मदद करें"

**विशेष उदाहरण**: मैंने Build में M365 Agents के बारे में बात करते हुए अपने दोस्त John Miller से संपर्क किया, और उन्होंने इस MCP की सिफारिश की। यह नए डेवलपर्स के लिए बहुत अच्छा हो सकता है क्योंकि यह टेम्पलेट्स, सैंपल कोड, और स्कैफोल्डिंग प्रदान करता है जिससे दस्तावेज़ों में डूबे बिना शुरुआत की जा सके। स्कीमा वैलिडेशन फीचर्स खासकर मैनिफेस्ट संरचना त्रुटियों से बचने में मददगार लगते हैं, जो घंटों की डिबगिंग का कारण बन सकती हैं।

> **💡 प्रो टिप**
> 
> व्यापक M365 विकास समर्थन के लिए इस सर्वर का Microsoft Learn Docs MCP Server के साथ उपयोग करें – एक आधिकारिक दस्तावेज़ प्रदान करता है जबकि यह व्यावहारिक विकास टूल्स और समस्या निवारण सहायता देता है।

## आगे क्या? 🔮

## 📋 निष्कर्ष

Model Context Protocol (MCP) डेवलपर्स के AI असिस्टेंट्स और बाहरी टूल्स के साथ इंटरैक्शन के तरीके को बदल रहा है। ये 10 Microsoft MCP सर्वर मानकीकृत AI इंटीग्रेशन की शक्ति दिखाते हैं, जो निर्बाध वर्कफ़्लो सक्षम करते हैं और डेवलपर्स को उनके काम में पूरी तरह से डूबे रहने देते हैं जबकि वे शक्तिशाली बाहरी क्षमताओं तक पहुंचते हैं।

व्यापक Azure इकोसिस्टम इंटीग्रेशन से लेकर Playwright जैसे ब्राउज़र ऑटोमेशन और MarkItDown जैसे दस्तावेज़ प्रसंस्करण के विशेष टूल्स तक, ये सर्वर दिखाते हैं कि MCP कैसे विभिन्न विकास परिदृश्यों में उत्पादकता बढ़ा सकता है। मानकीकृत प्रोटोकॉल सुनिश्चित करता है कि ये टूल्स एक साथ सहजता से काम करें, एक सुसंगत विकास अनुभव बनाते हुए।

जैसे-जैसे MCP इकोसिस्टम विकसित होता रहेगा, समुदाय के साथ जुड़ा रहना, नए सर्वरों का अन्वेषण करना, और कस्टम समाधान बनाना आपकी विकास उत्पादकता को अधिकतम करने की कुंजी होगी। MCP की खुली मानक प्रकृति का मतलब है कि आप विभिन्न विक्रेताओं के टूल्स को मिलाकर अपनी विशिष्ट आवश्यकताओं के लिए आदर्श वर्कफ़्लो बना सकते हैं।

## 🔗 अतिरिक्त संसाधन

- [Official Microsoft MCP Repository](https://github.com/microsoft/mcp)
- [MCP Community & Documentation](https://modelcontextprotocol.io/introduction)
- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [Visual Studio MCP Documentation](https://learn.microsoft.com/visualstudio/ide/mcp-servers)
- [Azure MCP Documentation](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [Let's Learn – MCP Events](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/lets-learn---mcp-events-a-beginners-guide-to-the-model-context-protocol/4429023)
- [Awesome GitHub Copilot Customizations](https://github.com/awesome-copilot)
- [C# MCP SDK](https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol)
- [MCP Dev Days Live 29th/30th July or watch on Demand ](https://aka.ms/mcpdevdays)

## 🎯 अभ्यास

1. **इंस्टॉल और कॉन्फ़िगर करें**: अपने VS Code वातावरण में किसी एक MCP सर्वर को सेटअप करें और बुनियादी कार्यक्षमता का परीक्षण करें।
2. **वर्कफ़्लो इंटीग्रेशन**: कम से कम तीन अलग-अलग MCP सर्वरों को मिलाकर एक विकास वर्कफ़्लो डिज़ाइन करें।
3. **कस्टम सर्वर योजना**: अपनी दैनिक विकास दिनचर्या में एक ऐसा कार्य पहचानें जो कस्टम MCP सर्वर से लाभान्वित हो सकता है और उसके लिए एक विनिर्देशन बनाएं।
4. **प्रदर्शन विश्लेषण**: सामान्य विकास कार्यों के लिए MCP सर्वरों के उपयोग की दक्षता की तुलना पारंपरिक तरीकों से करें।
5. **सुरक्षा मूल्यांकन**: अपने विकास वातावरण में MCP सर्वरों के उपयोग के सुरक्षा प्रभावों का मूल्यांकन करें और सर्वोत्तम प्रथाओं का प्रस्ताव करें।

Next:[Best Practices](../08-BestPractices/README.md)

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या असंगतियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही अधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।