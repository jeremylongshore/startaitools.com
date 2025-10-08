<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T11:11:55+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "mr"
}
-->
# 🚀 १० Microsoft MCP सर्व्हर्स जे डेव्हलपर उत्पादकतेत क्रांती घडवत आहेत

## 🎯 या मार्गदर्शकातून तुम्हाला काय शिकायला मिळेल

हा व्यावहारिक मार्गदर्शक दहा Microsoft MCP सर्व्हर्स दाखवतो जे AI सहाय्यकांसोबत डेव्हलपर कसे काम करतात यामध्ये सक्रियपणे बदल घडवत आहेत. फक्त MCP सर्व्हर्स काय करू शकतात हे सांगण्याऐवजी, आम्ही तुम्हाला असे सर्व्हर्स दाखवणार आहोत जे Microsoft आणि इतरत्र दररोजच्या विकास प्रक्रियेत खरोखर फरक घडवत आहेत.

या मार्गदर्शकातील प्रत्येक सर्व्हर वास्तविक वापर आणि डेव्हलपर अभिप्रायावर आधारित निवडलेला आहे. तुम्हाला फक्त प्रत्येक सर्व्हर काय करतो हेच नाही तर का महत्त्वाचा आहे आणि तुमच्या स्वतःच्या प्रोजेक्टमध्ये त्याचा कसा सर्वोत्तम उपयोग करायचा हेही समजेल. तुम्ही MCP मध्ये पूर्णपणे नवीन असाल किंवा तुमची विद्यमान सेटअप वाढवू इच्छित असाल, हे सर्व्हर्स Microsoft इकोसिस्टममधील काही सर्वात व्यावहारिक आणि प्रभावी साधने आहेत.

> **💡 जलद सुरुवात टिप**
> 
> MCP मध्ये नवीन आहात? काळजी करू नका! हा मार्गदर्शक सुरुवातीसाठी सोपा ठेवण्यात आला आहे. आम्ही संकल्पना समजावून सांगू आणि तुम्ही नेहमी आमच्या [MCP परिचय](../00-Introduction/README.md) आणि [मूलभूत संकल्पना](../01-CoreConcepts/README.md) मॉड्यूल्सकडे परत जाऊ शकता अधिक सखोल माहिती साठी.

## आढावा

हा सखोल मार्गदर्शक दहा Microsoft MCP सर्व्हर्सची माहिती देतो जे डेव्हलपर आणि AI सहाय्यक तसेच बाह्य साधनांशी संवाद साधण्याच्या पद्धतीत क्रांती घडवत आहेत. Azure रिसोर्स मॅनेजमेंटपासून ते दस्तऐवज प्रक्रिया पर्यंत, हे सर्व्हर्स Model Context Protocol च्या सामर्थ्याने अखंड, उत्पादक विकास कार्यप्रवाह तयार करतात.

## शिकण्याचे उद्दिष्टे

या मार्गदर्शकाच्या शेवटी तुम्ही:
- MCP सर्व्हर्स कसे डेव्हलपर उत्पादकता वाढवतात हे समजून घ्याल
- Microsoft च्या सर्वात प्रभावी MCP सर्व्हर अंमलबजावणीबद्दल शिकाल
- प्रत्येक सर्व्हरचे व्यावहारिक वापर प्रकरणे शोधाल
- VS Code आणि Visual Studio मध्ये हे सर्व्हर्स कसे सेटअप व कॉन्फिगर करायचे ते जाणून घ्याल
- MCP च्या विस्तृत इकोसिस्टम आणि भविष्यातील दिशा यांचा अभ्यास कराल

## 🔧 MCP सर्व्हर्स समजून घेणे: सुरुवातीसाठी मार्गदर्शक

### MCP सर्व्हर्स म्हणजे काय?

Model Context Protocol (MCP) मध्ये नवीन असाल तर तुम्हाला कदाचित वाटेल: "MCP सर्व्हर म्हणजे नेमकं काय आणि मला त्याची गरज का आहे?" चला एक सोपी तुलना करूया.

MCP सर्व्हर्स म्हणजे विशेष सहाय्यक जे तुमच्या AI कोडिंग साथीदाराला (जसे GitHub Copilot) बाह्य साधने आणि सेवा जोडण्यास मदत करतात. जसे तुम्ही तुमच्या फोनवर वेगवेगळ्या कामांसाठी वेगवेगळ्या अॅप्स वापरता—एक हवामानासाठी, एक नेव्हिगेशनसाठी, एक बँकिंगसाठी—तसेच MCP सर्व्हर्स तुमच्या AI सहाय्यकाला वेगवेगळ्या विकास साधनांशी संवाद साधण्याची क्षमता देतात.

### MCP सर्व्हर्स कोणती समस्या सोडवतात

MCP सर्व्हर्स आधी, जर तुम्हाला:
- तुमचे Azure रिसोर्सेस तपासायचे असतील
- GitHub इश्यू तयार करायचा असेल
- तुमच्या डेटाबेसमध्ये क्वेरी करायची असेल
- दस्तऐवज शोधायचा असेल

तर तुम्हाला कोडिंग थांबवून ब्राउझर उघडावा लागायचा, योग्य वेबसाइटवर जावे लागायचे आणि हे सर्व काम हाताने करावे लागायचे. सतत संदर्भ बदलल्यामुळे तुमचा कामाचा प्रवाह तुटतो आणि उत्पादकता कमी होते.

### MCP सर्व्हर्स तुमचा विकास अनुभव कसा बदलतात

MCP सर्व्हर्समुळे तुम्ही तुमच्या विकास वातावरणात (VS Code, Visual Studio इ.) राहून फक्त AI सहाय्यकाला हे काम सांगू शकता. उदाहरणार्थ:

**परंपरागत कार्यप्रवाहाऐवजी:**
1. कोडिंग थांबवा
2. ब्राउझर उघडा
3. Azure पोर्टलवर जा
4. स्टोरेज अकाउंट तपशील पहा
5. VS Code मध्ये परत या
6. कोडिंग सुरू ठेवा

**आता तुम्ही हे करू शकता:**
1. AI ला विचारा: "माझ्या Azure स्टोरेज अकाउंट्सची स्थिती काय आहे?"
2. मिळालेली माहिती वापरून कोडिंग सुरू ठेवा

### सुरुवातीसाठी मुख्य फायदे

#### 1. 🔄 **तुमच्या कामाच्या प्रवाहात रहा**
- अनेक अॅप्समध्ये स्विच करायची गरज नाही
- तुम्ही लिहित असलेल्या कोडवर लक्ष केंद्रित करा
- वेगवेगळ्या साधनांचे व्यवस्थापन करण्याचा मानसिक ताण कमी करा

#### 2. 🤖 **कठीण कमांड्सऐवजी नैसर्गिक भाषा वापरा**
- SQL सिंटॅक्स लक्षात ठेवण्याऐवजी तुम्हाला हवे असलेले डेटा वर्णन करा
- Azure CLI कमांड्स लक्षात ठेवण्याऐवजी तुमचे उद्दिष्ट सांगा
- तांत्रिक तपशील AI कडे सोडा, तुम्ही लॉजिकवर लक्ष द्या

#### 3. 🔗 **अनेक साधने एकत्र जोडा**
- वेगवेगळ्या सेवांचा वापर करून शक्तिशाली कार्यप्रवाह तयार करा
- उदाहरण: "सर्व अलीकडील GitHub इश्यू मिळवा आणि त्यानुसार Azure DevOps वर्क आयटम तयार करा"
- क्लिष्ट स्क्रिप्ट न लिहिता ऑटोमेशन तयार करा

#### 4. 🌐 **वाढत्या इकोसिस्टममध्ये प्रवेश**
- Microsoft, GitHub आणि इतर कंपन्यांनी तयार केलेल्या सर्व्हर्सचा फायदा घ्या
- वेगवेगळ्या विक्रेत्यांच्या साधनांचा सहज वापर करा
- वेगवेगळ्या AI सहाय्यकांमध्ये काम करणाऱ्या मानकीकृत इकोसिस्टमचा भाग व्हा

#### 5. 🛠️ **प्रॅक्टिकल शिकणे**
- आधी तयार केलेल्या सर्व्हर्सपासून सुरुवात करा आणि संकल्पना समजून घ्या
- हळूहळू स्वतःचे सर्व्हर्स तयार करा
- उपलब्ध SDKs आणि दस्तऐवजांचा वापर करून शिकण्यास मदत घ्या

### सुरुवातीसाठी वास्तविक उदाहरण

समजा तुम्ही वेब विकासात नवीन आहात आणि तुमचा पहिला प्रोजेक्ट करत आहात. MCP सर्व्हर्स कसे मदत करू शकतात ते पाहूया:

**परंपरागत पद्धत:**
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**MCP सर्व्हर्ससह:**
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### एंटरप्राइझ मानकाचा फायदा

MCP उद्योगव्यापी मानक बनत आहे, म्हणजे:
- **सुसंगतता**: वेगवेगळ्या साधनांमध्ये आणि कंपन्यांमध्ये समान अनुभव
- **परस्परसंवाद**: वेगवेगळ्या विक्रेत्यांचे सर्व्हर्स एकत्र काम करतात
- **भविष्यात सुरक्षितता**: कौशल्ये आणि सेटअप वेगवेगळ्या AI सहाय्यकांमध्ये वापरता येतात
- **समुदाय**: मोठा ज्ञान आणि संसाधनांचा इकोसिस्टम

### सुरुवात कशी कराल: काय शिकाल

या मार्गदर्शकात, आम्ही १० Microsoft MCP सर्व्हर्स पाहणार आहोत जे सर्व स्तरांवरील डेव्हलपरसाठी उपयुक्त आहेत. प्रत्येक सर्व्हर:
- सामान्य विकास आव्हाने सोडवतो
- पुनरावृत्ती होणारी कामे कमी करतो
- कोडची गुणवत्ता सुधारतो
- शिकण्याच्या संधी वाढवतो

> **💡 शिकण्याची टिप**
> 
> जर तुम्ही MCP मध्ये पूर्णपणे नवीन असाल, तर आधी आमचे [MCP परिचय](../00-Introduction/README.md) आणि [मूलभूत संकल्पना](../01-CoreConcepts/README.md) मॉड्यूल्स पहा. नंतर येथे परत या आणि Microsoft च्या वास्तविक साधनांसह या संकल्पनांचा वापर कसा होतो ते पाहा.
>
> MCP च्या महत्त्वावर अधिक माहिती साठी, Maria Naggaga यांचा लेख वाचा: [Connect Once, Integrate Anywhere with MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps).

## VS Code आणि Visual Studio मध्ये MCP सह सुरुवात 🚀

जर तुम्ही Visual Studio Code किंवा Visual Studio 2022 GitHub Copilot सह वापरत असाल तर हे MCP सर्व्हर्स सेटअप करणे सोपे आहे.

### VS Code सेटअप

VS Code साठी मूलभूत प्रक्रिया:

1. **Agent Mode सक्षम करा**: VS Code मध्ये Copilot Chat विंडोमध्ये Agent मोडवर स्विच करा
2. **MCP सर्व्हर्स कॉन्फिगर करा**: तुमच्या VS Code च्या settings.json फाईलमध्ये सर्व्हर कॉन्फिगरेशन जोडा
3. **सर्व्हर्स सुरू करा**: वापरायचे सर्व्हर्स "Start" बटणावर क्लिक करून सुरू करा
4. **साधने निवडा**: सत्रासाठी कोणते MCP सर्व्हर्स सक्षम करायचे ते निवडा

सविस्तर सेटअप सूचना साठी [VS Code MCP दस्तऐवज](https://code.visualstudio.com/docs/copilot/copilot-mcp) पहा.

> **💡 प्रो टिप: MCP सर्व्हर्स प्रो प्रमाणे व्यवस्थापित करा!**
> 
> VS Code Extensions दृश्यात आता [स्थापित MCP सर्व्हर्स व्यवस्थापित करण्यासाठी नवीन UI](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) उपलब्ध आहे! तुम्हाला कोणतेही MCP सर्व्हर जलद सुरू, थांबवू आणि व्यवस्थापित करता येतात. नक्की वापरून पहा!

### Visual Studio 2022 सेटअप

Visual Studio 2022 (आवृत्ती 17.14 किंवा नंतर) साठी:

1. **Agent Mode सक्षम करा**: GitHub Copilot Chat विंडोतील "Ask" ड्रॉपडाउनवर क्लिक करा आणि "Agent" निवडा
2. **कॉन्फिगरेशन फाईल तयार करा**: तुमच्या सोल्यूशन डायरेक्टरीमध्ये `.mcp.json` फाईल तयार करा (शिफारस केलेले स्थान: `<SOLUTIONDIR>\.mcp.json`)
3. **सर्व्हर्स कॉन्फिगर करा**: मानक MCP फॉरमॅट वापरून सर्व्हर कॉन्फिगरेशन जोडा
4. **साधन मंजुरी**: जेव्हा विचारले जाईल तेव्हा योग्य स्कोप परवानग्यांसह वापरायची साधने मंजूर करा

सविस्तर Visual Studio सेटअप सूचना साठी [Visual Studio MCP दस्तऐवज](https://learn.microsoft.com/visualstudio/ide/mcp-servers) पहा.

प्रत्येक MCP सर्व्हरची स्वतःची कॉन्फिगरेशन गरज (कनेक्शन स्ट्रिंग्ज, प्रमाणीकरण इ.) असते, पण दोन्ही IDE मध्ये सेटअप पद्धत सारखीच आहे.

## Microsoft MCP सर्व्हर्सकडून शिकलेले धडे 🛠️

### 1. 📚 Microsoft Learn Docs MCP Server

[![VS Code मध्ये इंस्टॉल करा](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![VS Code Insiders मध्ये इंस्टॉल करा](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**हे काय करते**: Microsoft Learn Docs MCP Server हा एक क्लाउड-होस्टेड सेवा आहे जो AI सहाय्यकांना Model Context Protocol द्वारे अधिकृत Microsoft दस्तऐवजांवर रिअल-टाइम प्रवेश देतो. तो `https://learn.microsoft.com/api/mcp` शी जोडतो आणि Microsoft Learn, Azure दस्तऐवज, Microsoft 365 दस्तऐवज आणि इतर अधिकृत Microsoft स्रोतांमध्ये सिमॅंटिक शोध सक्षम करतो.

**हे का उपयुक्त आहे**: "फक्त दस्तऐवज" वाटत असले तरी, हा सर्व्हर Microsoft तंत्रज्ञान वापरणाऱ्या प्रत्येक डेव्हलपरसाठी अत्यंत महत्त्वाचा आहे. .NET डेव्हलपरांकडून AI कोडिंग सहाय्यकांबाबत एक मोठी तक्रार म्हणजे ते नवीनतम .NET आणि C# रिलीझबाबत अद्ययावत नसतात. Microsoft Learn Docs MCP Server हे रिअल-टाइममध्ये सर्वात अद्ययावत दस्तऐवज, API संदर्भ आणि सर्वोत्तम पद्धती उपलब्ध करून देतो. तुम्ही नवीनतम Azure SDKs वापरत असाल, C# 13 चे नवीन फिचर्स एक्सप्लोर करत असाल किंवा अत्याधुनिक .NET Aspire पॅटर्न्स अंमलात आणत असाल, हा सर्व्हर तुमच्या AI सहाय्यकाला अचूक, आधुनिक कोड तयार करण्यासाठी अधिकृत आणि अद्ययावत माहिती पुरवतो.

**वास्तविक वापर**: "अधिकृत Microsoft Learn दस्तऐवजांनुसार Azure कंटेनर अॅप तयार करण्यासाठी az cli कमांड्स काय आहेत?" किंवा "ASP.NET Core मध्ये Entity Framework सह dependency injection कसे कॉन्फिगर करायचे?" किंवा "हा कोड Microsoft Learn Documentation मधील परफॉर्मन्स शिफारशींसोबत जुळतो का ते तपासा." हा सर्व्हर Microsoft Learn, Azure docs, आणि Microsoft 365 दस्तऐवजांमध्ये सिमॅंटिक शोध वापरून सर्वात संदर्भानुसार संबंधित माहिती शोधतो. तो १० उच्च-गुणवत्तेच्या कंटेंट चंकसह लेख शीर्षक आणि URL परत करतो, नेहमी नवीनतम Microsoft दस्तऐवजांवर प्रवेश करतो.

**वैशिष्ट्यीकृत उदाहरण**: हा सर्व्हर `microsoft_docs_search` टूल एक्सपोज करतो जे Microsoft च्या अधिकृत तांत्रिक दस्तऐवजांवर सिमॅंटिक शोध करतो. एकदा कॉन्फिगर केल्यावर तुम्ही "ASP.NET Core मध्ये JWT authentication कसे अंमलात आणायचे?" असे प्रश्न विचारू शकता आणि अधिकृत, सविस्तर उत्तरांसह स्रोत लिंक मिळवू शकता. शोधाची गुणवत्ता उत्कृष्ट आहे कारण तो संदर्भ समजतो – Azure संदर्भात "containers" विचारल्यास Azure Container Instances दस्तऐवज परत करतो, तर .NET संदर्भात त्याच शब्दाचा वापर केल्यास संबंधित C# कलेक्शन माहिती परत करतो.

हा विशेषतः जलद बदलणाऱ्या किंवा अलीकडेच अपडेट झालेल्या लायब्ररी आणि वापर प्रकरणांसाठी उपयुक्त आहे. उदाहरणार्थ, काही अलीकडील कोडिंग प्रोजेक्ट्समध्ये मी .NET Aspire आणि Microsoft.Extensions.AI च्या नवीनतम रिलीझमधील फिचर्सचा वापर करायचा होता. Microsoft Learn Docs MCP सर्व्हर समाविष्ट केल्यामुळे मला फक्त API दस्तऐवज नव्हे तर नुकतेच प्रकाशित झालेले वॉकथ्रू आणि मार्गदर्शनही मिळाले.
> **💡 प्रो टिप**  
>  
> टूल-फ्रेंडली मॉडेल्सना देखील MCP टूल्स वापरण्यास प्रोत्साहनाची गरज असते! सिस्टम प्रॉम्प्ट किंवा [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) मध्ये असे काहीतरी समाविष्ट करण्याचा विचार करा: "तुमच्याकडे `microsoft.docs.mcp` ची प्रवेश आहे – Microsoft तंत्रज्ञानांबाबत प्रश्न हाताळताना C#, Azure, ASP.NET Core, किंवा Entity Framework सारख्या विषयांवर Microsoft च्या अधिकृत दस्तऐवजांमध्ये शोध घेण्यासाठी हा टूल वापरा."  
>  
> याचा उत्तम उदाहरण पाहण्यासाठी, Awesome GitHub Copilot रिपॉझिटरीमधील [C# .NET Janitor chat mode](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) पहा. हा मोड विशेषतः Microsoft Learn Docs MCP सर्व्हरचा वापर करून C# कोड स्वच्छ आणि आधुनिक करण्यासाठी नवीनतम पॅटर्न्स आणि सर्वोत्तम पद्धती वापरतो.
### 2. ☁️ Azure MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**हे काय करते**: Azure MCP Server हा 15+ विशेष Azure सेवा कनेक्टर्सचा एक संपूर्ण संच आहे जो संपूर्ण Azure पर्यावरण तुमच्या AI वर्कफ्लोमध्ये आणतो. हा फक्त एक सर्व्हर नाही – तर एक शक्तिशाली संग्रह आहे ज्यात रिसोर्स मॅनेजमेंट, डेटाबेस कनेक्टिव्हिटी (PostgreSQL, SQL Server), Azure Monitor लॉग विश्लेषण KQL सह, Cosmos DB इंटिग्रेशन आणि बरेच काही समाविष्ट आहे.

**हे का उपयुक्त आहे**: फक्त Azure रिसोर्सेसचे व्यवस्थापन करण्यापेक्षा, हा सर्व्हर Azure SDKs सह काम करताना कोडची गुणवत्ता लक्षणीयरीत्या सुधारतो. जेव्हा तुम्ही Azure MCP Agent मोडमध्ये वापरता, तेव्हा तो फक्त कोड लिहिण्यात मदत करत नाही – तो तुम्हाला *चांगला* Azure कोड लिहिण्यात मदत करतो जो सध्याच्या प्रमाणीकरण पद्धती, त्रुटी हाताळणीच्या सर्वोत्तम पद्धती आणि नवीनतम SDK वैशिष्ट्यांचा वापर करतो. सामान्य कोड मिळण्याऐवजी जो कदाचित काम करेल, तुम्हाला Azure च्या शिफारस केलेल्या पद्धतींनुसार उत्पादनासाठी योग्य कोड मिळतो.

**मुख्य मॉड्यूल्समध्ये समाविष्ट आहे**:
- **🗄️ डेटाबेस कनेक्टर्स**: Azure Database for PostgreSQL आणि SQL Server साठी थेट नैसर्गिक भाषा प्रवेश
- **📊 Azure Monitor**: KQL-आधारित लॉग विश्लेषण आणि ऑपरेशनल अंतर्दृष्टी
- **🌐 रिसोर्स मॅनेजमेंट**: संपूर्ण Azure रिसोर्स जीवनचक्र व्यवस्थापन
- **🔐 प्रमाणीकरण**: DefaultAzureCredential आणि मॅनेज्ड आयडेंटिटी पॅटर्न्स
- **📦 स्टोरेज सेवा**: Blob Storage, Queue Storage, आणि Table Storage ऑपरेशन्स
- **🚀 कंटेनर सेवा**: Azure Container Apps, Container Instances, आणि AKS व्यवस्थापन
- **आणि बरेच अधिक विशेष कनेक्टर्स**

**वास्तविक वापर**: "माझे Azure स्टोरेज अकाउंट्स यादी करा", "माझ्या Log Analytics वर्कस्पेसमधील गेल्या तासातील त्रुटी शोधा", किंवा "Node.js वापरून योग्य प्रमाणीकरणासह Azure अॅप्लिकेशन तयार करण्यात मदत करा"

**पूर्ण डेमो उदाहरण**: येथे एक संपूर्ण वॉकथ्रू आहे जे Azure MCP आणि GitHub Copilot for Azure एक्सटेंशन VS Code मध्ये एकत्र वापरण्याची ताकद दाखवते. जेव्हा तुम्ही दोन्ही इन्स्टॉल केलेले असता आणि विचारता:

> "DefaultAzureCredential प्रमाणीकरण वापरून Azure Blob Storage मध्ये फाइल अपलोड करणारा Python स्क्रिप्ट तयार करा. स्क्रिप्ट माझ्या 'mycompanystorage' नावाच्या Azure स्टोरेज अकाउंटशी कनेक्ट होईल, 'documents' नावाच्या कंटेनरमध्ये अपलोड करेल, सध्याच्या टाइमस्टँपसह एक टेस्ट फाइल तयार करेल, त्रुटी नीट हाताळेल आणि माहितीपूर्ण आउटपुट देईल, Azure च्या प्रमाणीकरण आणि त्रुटी हाताळणीच्या सर्वोत्तम पद्धतींचे पालन करेल, DefaultAzureCredential प्रमाणीकरण कसे कार्य करते याचे स्पष्टीकरण देणारे कमेंट्स असतील, आणि स्क्रिप्ट योग्य फंक्शन्स आणि दस्तऐवजीकरणासह व्यवस्थित रचलेली असेल."

Azure MCP Server एक पूर्ण, उत्पादनासाठी तयार Python स्क्रिप्ट तयार करेल जी:
- नवीनतम Azure Blob Storage SDK सह योग्य async पॅटर्न वापरते
- DefaultAzureCredential सह सविस्तर फॉलबॅक चेन स्पष्टीकरण देते
- विशिष्ट Azure अपवाद प्रकारांसह मजबूत त्रुटी हाताळणी करते
- Azure SDK च्या सर्वोत्तम पद्धतींनुसार रिसोर्स मॅनेजमेंट आणि कनेक्शन हाताळणी करते
- सविस्तर लॉगिंग आणि माहितीपूर्ण कन्सोल आउटपुट देते
- फंक्शन्स, दस्तऐवजीकरण आणि टाइप हिन्ट्ससह व्यवस्थित रचलेली स्क्रिप्ट तयार करते

हे विशेष म्हणजे Azure MCP शिवाय तुम्हाला सामान्य blob storage कोड मिळू शकतो जो काम करेल पण सध्याच्या Azure पॅटर्नचे पालन करणार नाही. Azure MCP सह तुम्हाला नवीनतम प्रमाणीकरण पद्धती वापरणारा, Azure-विशिष्ट त्रुटी परिस्थिती हाताळणारा आणि Microsoft च्या शिफारसीनुसार उत्पादनासाठी योग्य कोड मिळतो.

**वैशिष्ट्यीकृत उदाहरण**: मला `az` आणि `azd` CLI कमांड्स आठवणीत ठेवणे नेहमीच कठीण वाटले आहे. माझ्यासाठी नेहमी दोन टप्प्यांची प्रक्रिया असते: प्रथम सिंटॅक्स शोधणे, नंतर कमांड चालवणे. मी बर्‍याचदा पोर्टलमध्ये जाऊन क्लिक करून काम करतो कारण मला CLI सिंटॅक्स लक्षात ठेवता येत नाही हे मान्य करायचे नसते. जे मला हवे ते फक्त वर्णन करून सांगता येणे आश्चर्यकारक आहे, आणि तेही IDE सोडल्याशिवाय!

सुरुवात करण्यासाठी [Azure MCP repository](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) मध्ये वापराच्या अनेक उदाहरणांची यादी आहे. संपूर्ण सेटअप मार्गदर्शक आणि प्रगत कॉन्फिगरेशन पर्यायांसाठी, [अधिकृत Azure MCP दस्तऐवज](https://learn.microsoft.com/azure/developer/azure-mcp-server/) पहा.

### 3. 🐙 GitHub MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**हे काय करते**: अधिकृत GitHub MCP Server GitHub च्या संपूर्ण पर्यावरणाशी अखंड समाकलन प्रदान करतो, ज्यात होस्टेड रिमोट ऍक्सेस आणि स्थानिक Docker डिप्लॉयमेंट पर्याय दोन्ही आहेत. हे फक्त मूलभूत रिपॉझिटरी ऑपरेशन्ससाठी नाही – तर GitHub Actions व्यवस्थापन, पुल रिक्वेस्ट वर्कफ्लोज, इश्यू ट्रॅकिंग, सुरक्षा स्कॅनिंग, सूचना आणि प्रगत ऑटोमेशन क्षमता यांचा समावेश असलेले एक संपूर्ण टूलकिट आहे.

**हे का उपयुक्त आहे**: हा सर्व्हर GitHub सह तुमचा संवाद कसा होतो हे बदलतो, संपूर्ण प्लॅटफॉर्मचा अनुभव थेट तुमच्या विकास वातावरणात आणतो. प्रोजेक्ट व्यवस्थापन, कोड पुनरावलोकन आणि CI/CD मॉनिटरिंगसाठी सतत VS Code आणि GitHub.com यांच्यात स्विच करण्याऐवजी, तुम्ही नैसर्गिक भाषा आदेशांद्वारे सर्व काही हाताळू शकता आणि तुमच्या कोडवर लक्ष केंद्रित ठेवू शकता.

> **ℹ️ टीप: 'एजंट्स' चे वेगवेगळे प्रकार**
> 
> GitHub MCP Server ला GitHub च्या Coding Agent (जो AI एजंट आहे आणि ज्याला इश्यूजवर स्वयंचलित कोडिंग कामांसाठी नियुक्त करता येते) यासोबत गोंधळू नका. GitHub MCP Server VS Code च्या Agent मोडमध्ये GitHub API समाकलन पुरवतो, तर GitHub चा Coding Agent वेगळा फिचर आहे जो GitHub इश्यूजना नियुक्त केल्यावर पुल रिक्वेस्ट तयार करतो.

**मुख्य क्षमता**:
- **⚙️ GitHub Actions**: संपूर्ण CI/CD पाइपलाइन व्यवस्थापन, वर्कफ्लो मॉनिटरिंग, आणि आर्टिफॅक्ट हाताळणी
- **🔀 पुल रिक्वेस्ट्स**: PR तयार करणे, पुनरावलोकन, मर्ज करणे, आणि सविस्तर स्थिती ट्रॅकिंगसह व्यवस्थापन
- **🐛 इश्यूज**: संपूर्ण इश्यू जीवनचक्र व्यवस्थापन, कमेंटिंग, लेबलिंग, आणि असाइनमेंट
- **🔒 सुरक्षा**: कोड स्कॅनिंग अलर्ट्स, सिक्रेट डिटेक्शन, आणि Dependabot समाकलन
- **🔔 सूचना**: स्मार्ट नोटिफिकेशन व्यवस्थापन आणि रिपॉझिटरी सदस्यता नियंत्रण
- **📁 रिपॉझिटरी व्यवस्थापन**: फाइल ऑपरेशन्स, ब्रांच व्यवस्थापन, आणि रिपॉझिटरी प्रशासन
- **👥 सहकार्य**: वापरकर्ता आणि संघ शोध, टीम व्यवस्थापन, आणि प्रवेश नियंत्रण

**वास्तविक वापर**: "माझ्या फिचर ब्रांचवरून पुल रिक्वेस्ट तयार करा", "माझ्या सर्व अयशस्वी CI रनस या आठवड्यात दाखवा", "माझ्या रिपॉझिटरीजसाठी उघडलेले सुरक्षा अलर्ट्स यादी करा", किंवा "माझ्या संघटनांमध्ये मला असाइन केलेले सर्व इश्यूज शोधा"

**पूर्ण डेमो उदाहरण**: GitHub MCP Server च्या क्षमतांचा एक प्रभावी वर्कफ्लो येथे आहे:

> "मला आमच्या स्प्रिंट रिव्ह्यूसाठी तयारी करायची आहे. या आठवड्यात मी तयार केलेल्या सर्व पुल रिक्वेस्ट्स दाखवा, आमच्या CI/CD पाइपलाइनची स्थिती तपासा, कोणतेही सुरक्षा अलर्ट्स ज्यावर लक्ष द्यावे लागेल त्यांचा सारांश तयार करा, आणि 'feature' लेबल असलेल्या मर्ज झालेल्या PRs वरून रिलीज नोट्स तयार करण्यात मदत करा."

GitHub MCP Server:
- तुमच्या अलीकडील पुल रिक्वेस्ट्सची सविस्तर स्थिती माहिती विचारून आणेल
- वर्कफ्लो रनचे विश्लेषण करेल आणि कोणत्याही अयशस्वी किंवा कामगिरीच्या समस्यांवर लक्ष वेधेल
- सुरक्षा स्कॅनिंग निकाल संकलित करेल आणि महत्त्वाच्या अलर्ट्सना प्राधान्य देईल
- मर्ज झालेल्या PRs मधून माहिती काढून सविस्तर रिलीज नोट्स तयार करेल
- स्प्रिंट नियोजन आणि रिलीज तयारीसाठी पुढील कृती सुचवेल

**वैशिष्ट्यीकृत उदाहरण**: मला कोड पुनरावलोकन वर्कफ्लोजसाठी हे वापरणे आवडते. VS Code, GitHub नोटिफिकेशन्स, आणि पुल रिक्वेस्ट पृष्ठांमध्ये उडी मारण्याऐवजी, मी म्हणू शकतो "माझ्या पुनरावलोकनासाठी वाट पाहणाऱ्या सर्व PRs दाखवा" आणि नंतर "PR #123 मध्ये प्रमाणीकरण पद्धतीतील त्रुटी हाताळणीबाबत एक कमेंट जोडा." सर्व्हर GitHub API कॉल्स हाताळतो, चर्चेचा संदर्भ राखतो, आणि मला अधिक रचनात्मक पुनरावलोकन कमेंट्स तयार करण्यात मदत करतो.

**प्रमाणीकरण पर्याय**: सर्व्हर OAuth (VS Code मध्ये सहज) आणि Personal Access Tokens दोन्ही समर्थित आहे, ज्यात फक्त आवश्यक GitHub फंक्शनॅलिटी सक्षम करण्यासाठी कॉन्फिगर करता येणारे टूलसेट्स आहेत. तुम्ही ते रिमोट होस्टेड सेवा म्हणून त्वरित सेटअपसाठी चालवू शकता किंवा पूर्ण नियंत्रणासाठी स्थानिक Docker द्वारे चालवू शकता.

> **💡 प्रो टिप**
> 
> तुमच्या MCP सर्व्हर सेटिंग्जमध्ये `--toolsets` पॅरामीटर कॉन्फिगर करून फक्त आवश्यक टूलसेट्स सक्षम करा, ज्यामुळे संदर्भाचा आकार कमी होतो आणि AI टूल निवड सुधारतो. उदाहरणार्थ, मुख्य विकास वर्कफ्लोजसाठी `"--toolsets", "repos,issues,pull_requests,actions"` जोडा, किंवा जर तुम्हाला मुख्यतः GitHub मॉनिटरिंग हवे असेल तर `"--toolsets", "notifications, security"` वापरा.

### 4. 🔄 Azure DevOps MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_DevOps_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_DevOps_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/azure-devops-mcp)

**हे काय करते**: Azure DevOps सेवांशी कनेक्ट होते जेणेकरून संपूर्ण प्रोजेक्ट व्यवस्थापन, वर्क आयटम ट्रॅकिंग, बिल्ड पाइपलाइन व्यवस्थापन, आणि रिपॉझिटरी ऑपरेशन्स करता येतात.

**हे का उपयुक्त आहे**: Azure DevOps तुमच्या मुख्य DevOps प्लॅटफॉर्म म्हणून वापरणाऱ्या टीमसाठी, हा MCP सर्व्हर तुमच्या विकास वातावरण आणि Azure DevOps वेब इंटरफेसमधील सतत टॅब स्विचिंग टाळतो. तुम्ही वर्क आयटम्स व्यवस्थापित करू शकता, बिल्ड स्थिती तपासू शकता, रिपॉझिटरीज क्वेरी करू शकता, आणि प्रोजेक्ट व्यवस्थापन कार्ये थेट तुमच्या AI सहाय्यकाकडून करू शकता.

**वास्तविक वापर**: "WebApp प्रोजेक्टसाठी चालू स्प्रिंटमधील सर्व सक्रिय वर्क आयटम्स दाखवा", "मी आत्ताच सापडलेल्या लॉगिन समस्येसाठी बग रिपोर्ट तयार करा", किंवा "आमच्या बिल्ड पाइपलाइनची स्थिती तपासा आणि अलीकडील अयशस्वी गोष्टी दाखवा"

**वैशिष्ट्यीकृत उदाहरण**: तुम्ही सहजपणे तुमच्या टीमच्या चालू स्प्रिंटची स्थिती "WebApp प्रोजेक्टसाठी चालू स्प्रिंटमधील सर्व सक्रिय वर्क आयटम्स दाखवा" किंवा "मी आत्ताच सापडलेल्या लॉगिन समस्येसाठी बग रिपोर्ट तयार करा" अशा सोप्या क्वेरीने तपासू शकता, आणि तेही तुमच्या विकास वातावरण सोडल्याशिवाय.

### 5. 📝 MarkItDown MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**हे काय करते**: MarkItDown हा एक सर्वसमावेशक दस्तऐवज रूपांतरण सर्व्हर आहे जो विविध फाइल फॉरमॅट्सना उच्च-गुणवत्तेच्या Markdown मध्ये रूपांतरित करतो, जे LLM वापरासाठी आणि मजकूर विश्लेषणाच्या कार्यप्रवाहांसाठी अनुकूलित आहे.

**हे का उपयुक्त आहे**: आधुनिक दस्तऐवज कार्यप्रवाहांसाठी अत्यावश्यक! MarkItDown अनेक फाइल फॉरमॅट्स हाताळतो आणि महत्त्वाच्या दस्तऐवज रचनेची जसे की शीर्षके, यादी, तक्ते आणि दुवे यांची जपणूक करतो. साध्या मजकूर काढण्याच्या साधनांपेक्षा वेगळे, हे सेमॅंटिक अर्थ आणि स्वरूप जपण्यावर लक्ष केंद्रित करते, जे AI प्रक्रिया आणि मानवी वाचनासाठी उपयुक्त आहे.

**समर्थित फाइल फॉरमॅट्स**:
- **ऑफिस दस्तऐवज**: PDF, PowerPoint (PPTX), Word (DOCX), Excel (XLSX/XLS)
- **मीडिया फाइल्स**: प्रतिमा (EXIF मेटाडेटा आणि OCR सह), ऑडिओ (EXIF मेटाडेटा आणि भाषांतरासह)
- **वेब सामग्री**: HTML, RSS फीड्स, YouTube URLs, Wikipedia पृष्ठे
- **डेटा फॉरमॅट्स**: CSV, JSON, XML, ZIP फाइल्स (आतील सामग्री पुनरावृत्तीने प्रक्रिया करतो)
- **प्रकाशन फॉरमॅट्स**: EPub, Jupyter नोटबुक्स (.ipynb)
- **ईमेल**: Outlook संदेश (.msg)
- **प्रगत**: Azure Document Intelligence एकत्रीकरण PDF प्रक्रियेसाठी

**प्रगत क्षमता**: MarkItDown LLM-शक्तीने प्रतिमा वर्णन (OpenAI क्लायंट दिल्यास), Azure Document Intelligence द्वारे सुधारित PDF प्रक्रिया, भाषण मजकूर रूपांतरण, आणि अतिरिक्त फाइल फॉरमॅट्ससाठी प्लगइन प्रणाली यांना समर्थन देतो.

**वास्तविक वापर**: "या PowerPoint सादरीकरणाला Markdown मध्ये रूपांतरित करा आमच्या दस्तऐवज साइटसाठी", "या PDF मधून योग्य शीर्षक रचनेसह मजकूर काढा", किंवा "हा Excel स्प्रेडशीट वाचण्यायोग्य तक्ता स्वरूपात बदला"

**वैशिष्ट्यीकृत उदाहरण**: [MarkItDown docs](https://github.com/microsoft/markitdown#why-markdown) मधील उद्धरण:

> Markdown हा साध्या मजकूराजवळ खूप जवळचा आहे, ज्यात फारसा मार्कअप किंवा स्वरूप नाही, पण तरीही महत्त्वाच्या दस्तऐवज रचनेचे प्रतिनिधित्व करण्याचा मार्ग देतो. मुख्य प्रवाहातील LLMs, जसे OpenAI चे GPT-4o, नैसर्गिकरित्या Markdown "बोलतात" आणि अनेकदा विनंती न करता त्यांच्या प्रतिसादांमध्ये Markdown वापरतात. याचा अर्थ असा की त्यांना मोठ्या प्रमाणात Markdown-स्वरूपित मजकूरावर प्रशिक्षण दिले गेले आहे आणि ते त्याला चांगले समजतात. एक बाजूची फायद्याची गोष्ट म्हणजे Markdown नियम देखील अत्यंत टोकन-कुशल आहेत.

MarkItDown दस्तऐवज रचना जपण्यात खूप चांगला आहे, जे AI कार्यप्रवाहांसाठी महत्त्वाचे आहे. उदाहरणार्थ, PowerPoint सादरीकरण रूपांतरित करताना, ते स्लाइडचे आयोजन योग्य शीर्षकांसह ठेवते, तक्ते Markdown तक्त्यांमध्ये काढते, प्रतिमांसाठी alt मजकूर समाविष्ट करते, आणि स्पीकर नोट्स देखील प्रक्रिया करते. चार्ट्स वाचण्यायोग्य डेटा तक्त्यांमध्ये रूपांतरित होतात, आणि परिणामी Markdown मूळ सादरीकरणाचा तार्किक प्रवाह जपतो. त्यामुळे हे AI प्रणालींमध्ये सादरीकरण सामग्री पुरवण्यासाठी किंवा विद्यमान स्लाइड्समधून दस्तऐवज तयार करण्यासाठी परिपूर्ण आहे.

### 6. 🗃️ SQL Server MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**हे काय करते**: SQL Server डेटाबेस (ऑन-प्रिमाइसेस, Azure SQL, किंवा Fabric) यांना संभाषणात्मक प्रवेश प्रदान करते

**हे का उपयुक्त आहे**: PostgreSQL सर्व्हर प्रमाणेच, पण Microsoft SQL पर्यावरणासाठी. सोप्या कनेक्शन स्ट्रिंगने कनेक्ट करा आणि नैसर्गिक भाषेत क्वेरी सुरू करा – आता संदर्भ बदलण्याची गरज नाही!

**वास्तविक वापर**: "गेल्या 30 दिवसांत पूर्ण न झालेल्या सर्व ऑर्डर्स शोधा" याला योग्य SQL क्वेरीमध्ये रूपांतरित करून स्वरूपित निकाल परत करतो

**वैशिष्ट्यीकृत उदाहरण**: एकदा डेटाबेस कनेक्शन सेट केल्यावर, तुम्ही लगेचच तुमच्या डेटाशी संभाषण करू शकता. ब्लॉग पोस्टमध्ये एक सोपा प्रश्न दाखवला आहे: "तुम्ही कोणत्या डेटाबेसशी कनेक्ट आहात?" MCP सर्व्हर योग्य डेटाबेस टूल वापरून SQL Server इंस्टन्सशी कनेक्ट होतो आणि सध्याच्या डेटाबेस कनेक्शनची माहिती परत करतो – एकही SQL ओळ न लिहिता. सर्व्हर स्कीमा व्यवस्थापनापासून डेटा हाताळणीपर्यंत सर्व डेटाबेस ऑपरेशन्स नैसर्गिक भाषा प्रॉम्प्ट्सद्वारे समर्थित करतो. VS Code आणि Claude Desktop सह संपूर्ण सेटअप सूचना आणि कॉन्फिगरेशन उदाहरणांसाठी पहा: [Introducing MSSQL MCP Server (Preview)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/).

### 7. 🎭 Playwright MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**हे काय करते**: AI एजंट्सना वेब पृष्ठांशी संवाद साधण्यास सक्षम करते, चाचणी आणि ऑटोमेशनसाठी

> **ℹ️ GitHub Copilot ला पॉवर देते**
> 
> Playwright MCP Server GitHub Copilot च्या Coding Agent ला वेब ब्राउझिंग क्षमता देतो! [या वैशिष्ट्याबद्दल अधिक जाणून घ्या](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/).

**हे का उपयुक्त आहे**: नैसर्गिक भाषेतील वर्णनांवर आधारित स्वयंचलित चाचणीसाठी परिपूर्ण. AI वेबसाइट्सवर नेव्हिगेट करू शकतो, फॉर्म भरू शकतो, आणि संरचित अॅक्सेसिबिलिटी स्नॅपशॉट्सद्वारे डेटा काढू शकतो – हे खूप सामर्थ्यशाली आहे!

**वास्तविक वापर**: "लॉगिन फ्लोची चाचणी करा आणि डॅशबोर्ड योग्यरित्या लोड होतो का तपासा" किंवा "उत्पादने शोधणारी आणि निकाल पृष्ठाची पडताळणी करणारी चाचणी तयार करा" – हे सर्व अॅप्लिकेशनच्या स्रोत कोडशिवाय

**वैशिष्ट्यीकृत उदाहरण**: माझ्या सहकाऱ्याने, Debbie O'Brien ने Playwright MCP Server सह अप्रतिम काम केले आहे! उदाहरणार्थ, तिने अलीकडेच दाखवले की तुम्ही अॅप्लिकेशनच्या स्रोत कोडशिवाय पूर्ण Playwright चाचण्या कशा तयार करू शकता. तिच्या प्रकरणात, तिने Copilot ला एक मूव्ही शोध अॅपसाठी चाचणी तयार करण्यास सांगितले: साइटवर जा, "Garfield" शोधा, आणि निकालांमध्ये मूव्ही दिसते का तपासा. MCP ने ब्राउझर सत्र सुरू केले, DOM स्नॅपशॉट्स वापरून पृष्ठ रचना तपासली, योग्य सिलेक्टर शोधले, आणि पहिल्या प्रयत्नात यशस्वी झालेली पूर्ण TypeScript चाचणी तयार केली.

हे खरोखर सामर्थ्यशाली बनवणारे कारण म्हणजे ते नैसर्गिक भाषा सूचनांपासून कार्यान्वित चाचणी कोडपर्यंतचा अंतर कमी करते. पारंपरिक पद्धतींमध्ये मॅन्युअल चाचणी लेखन किंवा कोडबेस प्रवेश आवश्यक असतो. पण Playwright MCP सह, तुम्ही बाह्य साइट्स, क्लायंट अॅप्लिकेशन्स, किंवा ब्लॅक-बॉक्स चाचणी परिस्थितींमध्ये जिथे कोड प्रवेश नाही तिथेही चाचणी करू शकता.

### 8. 💻 Dev Box MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**हे काय करते**: Microsoft Dev Box पर्यावरण नैसर्गिक भाषेद्वारे व्यवस्थापित करते

**हे का उपयुक्त आहे**: विकास पर्यावरण व्यवस्थापन खूप सोपे करते! विशिष्ट कमांड लक्षात न ठेवता विकास पर्यावरण तयार करा, कॉन्फिगर करा आणि व्यवस्थापित करा.

**वास्तविक वापर**: "नवीन Dev Box तयार करा ज्यात नवीनतम .NET SDK असेल आणि आमच्या प्रोजेक्टसाठी कॉन्फिगर करा", "माझ्या सर्व विकास पर्यावरणांची स्थिती तपासा", किंवा "आमच्या टीम सादरीकरणांसाठी एक प्रमाणित डेमो पर्यावरण तयार करा"

**वैशिष्ट्यीकृत उदाहरण**: मी वैयक्तिक विकासासाठी Dev Box वापरण्याचा मोठा चाहता आहे. माझा 'लाइटबुल' क्षण तेव्हा आला जेव्हा James Montemagno यांनी सांगितले की Dev Box कॉन्फरन्स डेमोसाठी किती छान आहे, कारण त्यात खूप जलद ईथरनेट कनेक्शन आहे, मग मी कोणत्या कॉन्फरन्स / हॉटेल / विमानातील वायफाय वापरत असलो तरी. खरंतर, मी अलीकडेच ब्रुगेस ते अँटवर्प बसने जाताना माझ्या लॅपटॉपला फोन हॉटस्पॉटशी जोडून कॉन्फरन्स डेमो सराव केला! पुढील टप्पा म्हणजे अनेक विकास पर्यावरणे आणि प्रमाणित डेमो पर्यावरणे व्यवस्थापित करणाऱ्या टीमवर अधिक लक्ष देणे. आणखी एक मोठा वापर प्रकरण जे मी ग्राहकांकडून आणि सहकाऱ्यांकडून ऐकत आहे ते म्हणजे Dev Box पूर्व-कॉन्फिगर केलेल्या विकास पर्यावरणासाठी वापरणे. दोन्ही प्रकरणांत, MCP वापरून Dev Boxes चे कॉन्फिगरेशन आणि व्यवस्थापन नैसर्गिक भाषेतील संवादाद्वारे करता येते, आणि तुम्ही तुमच्या विकास पर्यावरणातच राहता.

### 9. 🤖 Azure AI Foundry MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**हे काय करते**: Azure AI Foundry MCP Server विकसकांना Azure च्या AI परिसंस्थेचा संपूर्ण प्रवेश देते, ज्यात मॉडेल कॅटलॉग, तैनाती व्यवस्थापन, Azure AI Search सह ज्ञान निर्देशांक, आणि मूल्यांकन साधने यांचा समावेश आहे. हा प्रयोगात्मक सर्व्हर AI विकास आणि Azure च्या सामर्थ्यशाली AI पायाभूत सुविधांमधील अंतर कमी करतो, ज्यामुळे AI अनुप्रयोग तयार करणे, तैनात करणे आणि मूल्यांकन करणे सोपे होते.

**हे का उपयुक्त आहे**: हा सर्व्हर Azure AI सेवा वापरण्याचा तुमचा अनुभव बदलतो, कारण तो एंटरप्राइझ-ग्रेड AI क्षमता थेट तुमच्या विकास कार्यप्रवाहात आणतो. Azure पोर्टल, दस्तऐवज आणि तुमच्या IDE मध्ये सतत स्विच करण्याऐवजी, तुम्ही नैसर्गिक भाषेच्या आदेशांद्वारे मॉडेल शोधू शकता, सेवा तैनात करू शकता, ज्ञान संच व्यवस्थापित करू शकता आणि AI कार्यक्षमता मूल्यांकन करू शकता. RAG (Retrieval-Augmented Generation) अनुप्रयोग तयार करणाऱ्या, मल्टी-मॉडेल तैनाती व्यवस्थापित करणाऱ्या किंवा व्यापक AI मूल्यांकन पाइपलाइन अंमलात आणणाऱ्या विकसकांसाठी हे विशेषतः प्रभावी आहे.

**मुख्य विकसक क्षमता**:
- **🔍 मॉडेल शोध आणि तैनाती**: Azure AI Foundry चा मॉडेल कॅटलॉग एक्सप्लोर करा, कोड नमुन्यांसह सविस्तर मॉडेल माहिती मिळवा, आणि मॉडेल Azure AI सेवांवर तैनात करा
- **📚 ज्ञान व्यवस्थापन**: Azure AI Search निर्देशांक तयार करा आणि व्यवस्थापित करा, दस्तऐवज जोडा, इंडेक्सर कॉन्फिगर करा, आणि प्रगत RAG प्रणाली तयार करा
- **⚡ AI एजंट एकत्रीकरण**: Azure AI एजंटशी कनेक्ट व्हा, विद्यमान एजंट विचारणा करा, आणि उत्पादन परिस्थितीत एजंट कार्यक्षमता मूल्यांकन करा
- **📊 मूल्यांकन फ्रेमवर्क**: व्यापक मजकूर आणि एजंट मूल्यांकन चालवा, मार्कडाउन अहवाल तयार करा, आणि AI अनुप्रयोगांसाठी गुणवत्ता आश्वासन अंमलात आणा
- **🚀 प्रोटोटायपिंग साधने**: GitHub-आधारित प्रोटोटायपिंगसाठी सेटअप सूचना मिळवा आणि Azure AI Foundry Labs मधील अत्याधुनिक संशोधन मॉडेल्स वापरा

**वास्तविक जगातील विकसक वापर**: "माझ्या अनुप्रयोगासाठी Phi-4 मॉडेल Azure AI सेवांवर तैनात करा", "माझ्या दस्तऐवज RAG सिस्टीमसाठी नवीन शोध निर्देशांक तयार करा", "माझ्या एजंटच्या प्रतिसादांचे गुणवत्ता मेट्रिक्सशी तुलना करा", किंवा "माझ्या गुंतागुंतीच्या विश्लेषण कार्यांसाठी सर्वोत्तम reasoning मॉडेल शोधा"

**पूर्ण डेमो परिस्थिती**: येथे एक सामर्थ्यशाली AI विकास कार्यप्रवाह आहे:

> "मी ग्राहक समर्थन एजंट तयार करत आहे. मला कॅटलॉगमधून चांगला reasoning मॉडेल शोधण्यात मदत करा, तो Azure AI सेवांवर तैनात करा, आमच्या दस्तऐवजांमधून ज्ञान संच तयार करा, प्रतिसाद गुणवत्तेची चाचणी करण्यासाठी मूल्यांकन फ्रेमवर्क सेट करा, आणि नंतर GitHub टोकनसह एकत्रीकरण प्रोटोटाइप करण्यात मदत करा."

Azure AI Foundry MCP Server हे करेल:
- तुमच्या गरजांनुसार सर्वोत्तम reasoning मॉडेल शिफारस करण्यासाठी मॉडेल कॅटलॉग विचारणा करेल
- तुमच्या पसंतीच्या Azure प्रदेशासाठी तैनाती आदेश आणि कोटा माहिती प्रदान करेल
- तुमच्या दस्तऐवजांसाठी योग्य स्कीमासह Azure AI Search निर्देशांक सेट करेल
- गुणवत्ता मेट्रिक्स आणि सुरक्षा तपासणींसह मूल्यांकन पाइपलाइन कॉन्फिगर करेल
- त्वरित चाचणीसाठी GitHub प्रमाणीकरणासह प्रोटोटायपिंग कोड तयार करेल
- तुमच्या तंत्रज्ञान स्टॅकनुसार सविस्तर सेटअप मार्गदर्शक प्रदान करेल

**वैशिष्ट्यीकृत उदाहरण**: विकसक म्हणून, मला वेगवेगळ्या LLM मॉडेल्सशी जुळवून घेणे कठीण जात होते. मला काही मुख्य मॉडेल्स माहित आहेत, पण मला वाटत होते की मी काही उत्पादकता आणि कार्यक्षमता लाभ गमावत आहे. टोकन्स आणि कोटा व्यवस्थापन देखील तणावपूर्ण आणि कठीण आहे – मला कधीच खात्री नसते की मी योग्य कामासाठी योग्य मॉडेल निवडतोय की माझा बजेट वाया घालवत आहे. मी या MCP Server बद्दल James Montemagno कडून ऐकलं जेव्हा मी टीममेट्सकडून MCP Server साठी शिफारसी घेत होतो, आणि मला ते वापरण्यास उत्सुकता आहे! मॉडेल शोधण्याच्या क्षमतांमुळे मला माझ्यासारख्या व्यक्तीसाठी जे सामान्य मॉडेल्सच्या पलीकडे जाऊन विशिष्ट कार्यांसाठी ऑप्टिमाइझ्ड मॉडेल्स शोधू इच्छितात, ते विशेषतः उपयुक्त वाटतात. मूल्यांकन फ्रेमवर्क मला खात्री करण्यास मदत करेल की मी खरंच चांगले निकाल मिळवत आहे, फक्त काहीतरी नवीन करून पाहत नाही.

> **ℹ️ प्रयोगात्मक स्थिती**
> 
> हा MCP सर्व्हर प्रयोगात्मक असून सक्रिय विकासात आहे. वैशिष्ट्ये आणि API बदलू शकतात. Azure AI क्षमता एक्सप्लोर करण्यासाठी आणि प्रोटोटाइप तयार करण्यासाठी उत्तम, पण उत्पादन वापरासाठी स्थिरता आवश्यकतांची पडताळणी करा.

### 10. 🏢 Microsoft 365 Agents Toolkit MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**हे काय करते**: Microsoft 365 आणि Microsoft 365 Copilot सह एकत्रित होणाऱ्या AI एजंट्स आणि अनुप्रयोगांसाठी आवश्यक साधने विकसकांना पुरवते, ज्यात स्कीमा पडताळणी, नमुना कोड मिळवणे, आणि समस्या निवारण सहाय्य यांचा समावेश आहे.

**हे का उपयुक्त आहे**: Microsoft 365 आणि Copilot साठी तयार करताना गुंतागुंतीचे मॅनिफेस्ट स्कीमा आणि विशिष्ट विकास पद्धती लागतात. हा MCP सर्व्हर आवश्यक विकास संसाधने थेट तुमच्या कोडिंग वातावरणात आणतो, ज्यामुळे तुम्हाला स्कीमा पडताळणी, नमुना कोड शोधणे, आणि सामान्य समस्या निवारण करण्यात मदत होते, दस्तऐवज सतत पाहण्याची गरज नाही.

**वास्तविक वापर**: "माझा डिक्लेरेटिव्ह एजंट मॅनिफेस्ट पडताळा आणि स्कीमा त्रुटी दुरुस्त करा", "Microsoft Graph API प्लगइन अंमलात आणण्यासाठी नमुना कोड दाखवा", किंवा "माझ्या Teams अॅपच्या प्रमाणीकरण समस्यांचे निवारण करण्यात मदत करा"

**वैशिष्ट्यीकृत उदाहरण**: मी माझ्या मित्र John Miller शी Build मध्ये M365 Agents बद्दल बोलताना संपर्क साधला आणि त्याने हा MCP शिफारस केला. M365 Agents मध्ये नवीन असलेल्या विकसकांसाठी हा खूप उपयुक्त ठरू शकतो कारण तो टेम्पलेट्स, नमुना कोड, आणि स्कॅफोल्डिंग पुरवतो ज्यामुळे दस्तऐवजांमध्ये हरवले नाही. स्कीमा पडताळणी वैशिष्ट्ये विशेषतः उपयुक्त दिसतात कारण ती मॅनिफेस्ट संरचनेतील त्रुटी टाळण्यास मदत करतात ज्या तासोंत डिबगिंग करायला लावू शकतात.

> **💡 प्रो टिप**
> 
> Microsoft Learn Docs MCP Server सोबत हा सर्व्हर वापरा जेणेकरून M365 विकासासाठी संपूर्ण सहाय्य मिळेल – एक अधिकृत दस्तऐवज पुरवतो तर हा व्यावहारिक विकास साधने आणि समस्या निवारण सहाय्य देतो.

## पुढे काय? 🔮

## 📋 निष्कर्ष

Model Context Protocol (MCP) विकसक आणि AI सहाय्यक तसेच बाह्य साधनांमधील संवाद कसा होतो याला बदलत आहे. हे 10 Microsoft MCP सर्व्हर AI एकत्रीकरणाची सामर्थ्य दाखवतात, ज्यामुळे विकसकांना त्यांच्या कार्यप्रवाहात अखंडपणे सामील होऊन सामर्थ्यशाली बाह्य क्षमता वापरणे शक्य होते.

संपूर्ण Azure परिसंस्थेच्या एकत्रीकरणापासून ते Playwright सारख्या ब्राउझर ऑटोमेशन आणि MarkItDown सारख्या दस्तऐवज प्रक्रिया साधनांपर्यंत, हे सर्व्हर विविध विकास परिस्थितींमध्ये उत्पादकता वाढवतात. मानकीकृत प्रोटोकॉलमुळे हे साधने एकत्र सुरळीत काम करतात, ज्यामुळे एकसंध विकास अनुभव तयार होतो.

MCP परिसंस्था जसजशी विकसित होत आहे, समुदायाशी जोडले राहणे, नवीन सर्व्हर एक्सप्लोर करणे, आणि सानुकूल उपाय तयार करणे हे तुमच्या विकास उत्पादकतेसाठी महत्त्वाचे ठरेल. MCP चा खुला मानक असल्यामुळे तुम्ही वेगवेगळ्या विक्रेत्यांकडून साधने एकत्र करून तुमच्या गरजेनुसार परिपूर्ण कार्यप्रवाह तयार करू शकता.

## 🔗 अतिरिक्त संसाधने

- [अधिकृत Microsoft MCP Repository](https://github.com/microsoft/mcp)
- [MCP समुदाय आणि दस्तऐवज](https://modelcontextprotocol.io/introduction)
- [VS Code MCP दस्तऐवज](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [Visual Studio MCP दस्तऐवज](https://learn.microsoft.com/visualstudio/ide/mcp-servers)
- [Azure MCP दस्तऐवज](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [Let's Learn – MCP इव्हेंट्स](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/lets-learn---mcp-events-a-beginners-guide-to-the-model-context-protocol/4429023)
- [Awesome GitHub Copilot Customizations](https://github.com/awesome-copilot)
- [C# MCP SDK](https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol)
- [MCP Dev Days Live 29th/30th July किंवा मागणीवर पहा](https://aka.ms/mcpdevdays)

## 🎯 सराव

1. **इंस्टॉल आणि कॉन्फिगर करा**: तुमच्या VS Code वातावरणात एक MCP सर्व्हर सेट करा आणि मूलभूत कार्यक्षमता तपासा.
2. **कार्यप्रवाह एकत्रीकरण**: किमान तीन वेगवेगळ्या MCP सर्व्हर एकत्र करून विकास कार्यप्रवाह डिझाइन करा.
3. **सानुकूल सर्व्हर नियोजन**: तुमच्या दैनंदिन विकास कार्यात सानुकूल MCP सर्व्हरची गरज असलेले कार्य ओळखा आणि त्यासाठी तपशीलवार स्पेसिफिकेशन तयार करा.
4. **कार्यक्षमता विश्लेषण**: सामान्य विकास कार्यांसाठी MCP सर्व्हर वापरण्याची कार्यक्षमता पारंपारिक पद्धतींशी तुलना करा.
5. **सुरक्षा मूल्यांकन**: तुमच्या विकास वातावरणात MCP सर्व्हर वापरण्याच्या सुरक्षा परिणामांचे मूल्यांकन करा आणि सर्वोत्तम पद्धती सुचवा.

Next:[Best Practices](../08-BestPractices/README.md)

**अस्वीकरण**:  
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित केला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये चुका किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी अनुवाद करण्याची शिफारस केली जाते. या अनुवादाच्या वापरामुळे उद्भवलेल्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थलागी आम्ही जबाबदार नाही.