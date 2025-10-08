<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T10:49:55+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "ar"
}
-->
# 🚀 10 خوادم Microsoft MCP التي تُحدث ثورة في إنتاجية المطورين

## 🎯 ما الذي ستتعلمه في هذا الدليل

يعرض هذا الدليل العملي عشرة خوادم Microsoft MCP التي تُغير بشكل فعّال طريقة عمل المطورين مع مساعدي الذكاء الاصطناعي. بدلاً من مجرد شرح ما *يمكن* أن تفعله خوادم MCP، سنعرض لك خوادم تُحدث فرقًا حقيقيًا في سير العمل اليومي للتطوير داخل مايكروسوفت وخارجها.

تم اختيار كل خادم في هذا الدليل بناءً على الاستخدام الفعلي وردود فعل المطورين. ستكتشف ليس فقط ما يفعله كل خادم، بل لماذا هو مهم وكيف تستفيد منه بأقصى قدر في مشاريعك الخاصة. سواء كنت جديدًا تمامًا على MCP أو ترغب في توسيع إعداداتك الحالية، تمثل هذه الخوادم بعضًا من أكثر الأدوات العملية والمؤثرة المتاحة في نظام مايكروسوفت البيئي.

> **💡 نصيحة بداية سريعة**
> 
> جديد على MCP؟ لا تقلق! هذا الدليل مصمم ليكون مناسبًا للمبتدئين. سنشرح المفاهيم أثناء التقدم، ويمكنك دائمًا الرجوع إلى [مقدمة MCP](../00-Introduction/README.md) و[المفاهيم الأساسية](../01-CoreConcepts/README.md) لمزيد من الخلفية المتعمقة.

## نظرة عامة

يستكشف هذا الدليل الشامل عشرة خوادم Microsoft MCP التي تُحدث ثورة في طريقة تفاعل المطورين مع مساعدي الذكاء الاصطناعي والأدوات الخارجية. من إدارة موارد Azure إلى معالجة المستندات، تُظهر هذه الخوادم قوة بروتوكول سياق النموذج في خلق سير عمل تطوير سلس ومنتج.

## أهداف التعلم

بنهاية هذا الدليل، ستتمكن من:
- فهم كيف تعزز خوادم MCP إنتاجية المطورين
- التعرف على أكثر تطبيقات خوادم MCP تأثيرًا من مايكروسوفت
- اكتشاف حالات استخدام عملية لكل خادم
- معرفة كيفية إعداد وتكوين هذه الخوادم في VS Code وVisual Studio
- استكشاف النظام البيئي الأوسع لـ MCP والاتجاهات المستقبلية

## 🔧 فهم خوادم MCP: دليل للمبتدئين

### ما هي خوادم MCP؟

كمبتدئ في بروتوكول سياق النموذج (MCP)، قد تتساءل: "ما هو خادم MCP بالضبط، ولماذا يجب أن أهتم؟" لنبدأ بتشبيه بسيط.

فكر في خوادم MCP كمساعدين متخصصين يساعدون رفيقك في الترميز بالذكاء الاصطناعي (مثل GitHub Copilot) على الاتصال بالأدوات والخدمات الخارجية. تمامًا كما تستخدم تطبيقات مختلفة على هاتفك لمهام مختلفة—واحد للطقس، وآخر للملاحة، وآخر للبنك—تمنح خوادم MCP مساعد الذكاء الاصطناعي الخاص بك القدرة على التفاعل مع أدوات وخدمات تطوير مختلفة.

### المشكلة التي تحلها خوادم MCP

قبل وجود خوادم MCP، إذا أردت أن:
- تتحقق من موارد Azure الخاصة بك
- تنشئ مشكلة في GitHub
- تستعلم قاعدة بياناتك
- تبحث في الوثائق

كان عليك التوقف عن الترميز، وفتح المتصفح، والانتقال إلى الموقع المناسب، وأداء هذه المهام يدويًا. هذا التبديل المستمر في السياق يكسر تدفق عملك ويقلل من إنتاجيتك.

### كيف تُغير خوادم MCP تجربة تطويرك

مع خوادم MCP، يمكنك البقاء في بيئة التطوير الخاصة بك (VS Code، Visual Studio، إلخ) وطلب من مساعد الذكاء الاصطناعي التعامل مع هذه المهام ببساطة. على سبيل المثال:

**بدلاً من هذا سير العمل التقليدي:**
1. التوقف عن الترميز  
2. فتح المتصفح  
3. الانتقال إلى بوابة Azure  
4. البحث عن تفاصيل حساب التخزين  
5. العودة إلى VS Code  
6. استئناف الترميز  

**يمكنك الآن القيام بهذا:**
1. اسأل الذكاء الاصطناعي: "ما حالة حسابات تخزين Azure الخاصة بي؟"  
2. استمر في الترميز مع المعلومات المقدمة  

### الفوائد الرئيسية للمبتدئين

#### 1. 🔄 **ابقَ في حالة التركيز**
- لا مزيد من التنقل بين تطبيقات متعددة  
- حافظ على تركيزك على الكود الذي تكتبه  
- قلل العبء الذهني لإدارة أدوات مختلفة  

#### 2. 🤖 **استخدم اللغة الطبيعية بدلاً من الأوامر المعقدة**
- بدلاً من حفظ صياغة SQL، صف البيانات التي تحتاجها  
- بدلاً من تذكر أوامر Azure CLI، اشرح ما تريد تحقيقه  
- دع الذكاء الاصطناعي يتولى التفاصيل التقنية بينما تركز على المنطق  

#### 3. 🔗 **اربط أدوات متعددة معًا**
- أنشئ سير عمل قوي بدمج خدمات مختلفة  
- مثال: "احصل على جميع مشكلات GitHub الحديثة وأنشئ عناصر عمل مقابلة في Azure DevOps"  
- ابني أتمتة بدون كتابة سكربتات معقدة  

#### 4. 🌐 **الوصول إلى نظام بيئي متنامي**
- استفد من الخوادم التي تبنيها مايكروسوفت، GitHub، وشركات أخرى  
- امزج ووافق بين أدوات من بائعين مختلفين بسلاسة  
- انضم إلى نظام بيئي موحد يعمل عبر مساعدي الذكاء الاصطناعي المختلفين  

#### 5. 🛠️ **تعلم بالممارسة**
- ابدأ بخوادم جاهزة لفهم المفاهيم  
- طور خوادمك الخاصة تدريجيًا مع ازدياد خبرتك  
- استخدم SDKs والوثائق المتاحة لتوجيه تعلمك  

### مثال عملي للمبتدئين

لنفترض أنك جديد في تطوير الويب وتعمل على مشروعك الأول. إليك كيف يمكن لخوادم MCP أن تساعدك:

**الطريقة التقليدية:**
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**مع خوادم MCP:**
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### ميزة المعيار المؤسسي

يصبح MCP معيارًا صناعيًا واسع الانتشار، مما يعني:
- **الاتساق**: تجربة متشابهة عبر أدوات وشركات مختلفة  
- **التشغيل البيني**: خوادم من بائعين مختلفين تعمل معًا  
- **مستقبلية**: تنتقل المهارات والإعدادات بين مساعدي الذكاء الاصطناعي المختلفين  
- **المجتمع**: نظام بيئي كبير من المعرفة والموارد المشتركة  

### البداية: ما الذي ستتعلمه

في هذا الدليل، سنستعرض 10 خوادم Microsoft MCP مفيدة بشكل خاص للمطورين على جميع المستويات. كل خادم مصمم لـ:
- حل تحديات تطوير شائعة  
- تقليل المهام المتكررة  
- تحسين جودة الكود  
- تعزيز فرص التعلم  

> **💡 نصيحة تعلم**
> 
> إذا كنت جديدًا تمامًا على MCP، ابدأ بوحدات [مقدمة MCP](../00-Introduction/README.md) و[المفاهيم الأساسية](../01-CoreConcepts/README.md) أولاً. ثم عد هنا لترى هذه المفاهيم مطبقة مع أدوات مايكروسوفت الحقيقية.  
>
> لمزيد من السياق حول أهمية MCP، اطلع على منشور ماريا ناجاجا: [اتصل مرة واحدة، وادمج في أي مكان مع MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps).

## البدء مع MCP في VS Code وVisual Studio 🚀

إعداد هذه الخوادم بسيط إذا كنت تستخدم Visual Studio Code أو Visual Studio 2022 مع GitHub Copilot.

### إعداد VS Code

إليك الخطوات الأساسية لـ VS Code:

1. **تفعيل وضع الوكيل**: في VS Code، انتقل إلى وضع الوكيل في نافذة محادثة Copilot  
2. **تكوين خوادم MCP**: أضف إعدادات الخادم إلى ملف settings.json الخاص بـ VS Code  
3. **تشغيل الخوادم**: اضغط على زر "تشغيل" لكل خادم تريد استخدامه  
4. **اختيار الأدوات**: حدد خوادم MCP التي تريد تفعيلها للجلسة الحالية  

للحصول على تعليمات إعداد مفصلة، راجع [توثيق MCP لـ VS Code](https://code.visualstudio.com/docs/copilot/copilot-mcp).

> **💡 نصيحة احترافية: إدارة خوادم MCP كالمحترفين!**
> 
> يعرض قسم الإضافات في VS Code الآن [واجهة مستخدم جديدة لإدارة خوادم MCP المثبتة](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode)! يمكنك الوصول السريع لتشغيل، إيقاف، وإدارة أي خادم MCP مثبت باستخدام واجهة واضحة وبسيطة. جربها!

### إعداد Visual Studio 2022

لـ Visual Studio 2022 (الإصدار 17.14 أو أحدث):

1. **تفعيل وضع الوكيل**: اضغط على القائمة المنسدلة "اسأل" في نافذة محادثة GitHub Copilot واختر "وكيل"  
2. **إنشاء ملف التكوين**: أنشئ ملف `.mcp.json` في مجلد الحل الخاص بك (الموقع الموصى به: `<SOLUTIONDIR>\.mcp.json`)  
3. **تكوين الخوادم**: أضف إعدادات خوادم MCP باستخدام صيغة MCP القياسية  
4. **الموافقة على الأدوات**: عند الطلب، وافق على الأدوات التي تريد استخدامها مع الأذونات المناسبة  

للحصول على تعليمات إعداد مفصلة لـ Visual Studio، راجع [توثيق MCP لـ Visual Studio](https://learn.microsoft.com/visualstudio/ide/mcp-servers).

كل خادم MCP يأتي مع متطلبات تكوين خاصة به (سلاسل الاتصال، المصادقة، إلخ)، لكن نمط الإعداد متسق عبر كلا بيئتي التطوير.

## الدرس المستفاد من خوادم Microsoft MCP 🛠️

### 1. 📚 خادم Microsoft Learn Docs MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**ما يفعله**: خادم Microsoft Learn Docs MCP هو خدمة مستضافة سحابياً توفر لمساعدي الذكاء الاصطناعي وصولًا فوريًا إلى الوثائق الرسمية لمايكروسوفت عبر بروتوكول سياق النموذج. يتصل بـ `https://learn.microsoft.com/api/mcp` ويمكّن البحث الدلالي عبر Microsoft Learn، وثائق Azure، وثائق Microsoft 365، ومصادر مايكروسوفت الرسمية الأخرى.

**لماذا هو مفيد**: قد يبدو الأمر كأنه "مجرد وثائق"، لكن هذا الخادم حيوي لكل مطور يستخدم تقنيات مايكروسوفت. واحدة من أكبر الشكاوى من مطوري .NET حول مساعدي الترميز بالذكاء الاصطناعي هي أنهم ليسوا محدثين بأحدث إصدارات .NET وC#. يحل خادم Microsoft Learn Docs MCP هذه المشكلة من خلال توفير وصول فوري إلى أحدث الوثائق، مراجع API، وأفضل الممارسات. سواء كنت تعمل مع أحدث SDKs لـ Azure، تستكشف ميزات C# 13 الجديدة، أو تطبق أنماط .NET Aspire المتطورة، يضمن هذا الخادم أن يكون لدى مساعدك الذكي وصول إلى المعلومات الرسمية والمحدثة اللازمة لتوليد كود دقيق وحديث.

**الاستخدام في العالم الحقيقي**: "ما هي أوامر az cli لإنشاء تطبيق حاوية Azure وفقًا لوثائق Microsoft Learn الرسمية؟" أو "كيف أُكوّن Entity Framework مع حقن التبعيات في ASP.NET Core؟" أو ماذا عن "راجع هذا الكود للتأكد من مطابقته لتوصيات الأداء في وثائق Microsoft Learn." يوفر الخادم تغطية شاملة عبر Microsoft Learn، وثائق Azure، ووثائق Microsoft 365 باستخدام بحث دلالي متقدم للعثور على المعلومات الأكثر صلة بالسياق. يعيد ما يصل إلى 10 مقاطع محتوى عالية الجودة مع عناوين المقالات وروابطها، مع الوصول دائمًا إلى أحدث الوثائق المنشورة.

**مثال مميز**: يكشف الخادم عن أداة `microsoft_docs_search` التي تنفذ بحثًا دلاليًا ضد الوثائق التقنية الرسمية لمايكروسوفت. بمجرد التكوين، يمكنك طرح أسئلة مثل "كيف أطبق مصادقة JWT في ASP.NET Core؟" والحصول على ردود مفصلة ورسمية مع روابط المصادر. جودة البحث استثنائية لأنه يفهم السياق – السؤال عن "الحاويات" في سياق Azure سيُرجع وثائق Azure Container Instances، بينما نفس المصطلح في سياق .NET يعيد معلومات ذات صلة بمجموعات C#.

هذا مفيد بشكل خاص للمكتبات وحالات الاستخدام التي تتغير بسرعة أو تم تحديثها مؤخرًا. على سبيل المثال، في بعض مشاريع الترميز الأخيرة أردت الاستفادة من ميزات في أحدث إصدارات .NET Aspire وMicrosoft.Extensions.AI. من خلال تضمين خادم Microsoft Learn Docs MCP، تمكنت من الاستفادة ليس فقط من وثائق API، بل من الشروحات والإرشادات التي تم نشرها حديثًا.
> **💡 نصيحة احترافية**
> 
> حتى النماذج الموجهة للأدوات تحتاج إلى تحفيز لاستخدام أدوات MCP! فكّر في إضافة موجه نظام أو [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) مثل: "لديك حق الوصول إلى `microsoft.docs.mcp` – استخدم هذه الأداة للبحث في أحدث الوثائق الرسمية لمايكروسوفت عند التعامل مع أسئلة حول تقنيات مايكروسوفت مثل C#، Azure، ASP.NET Core، أو Entity Framework."
>
> للحصول على مثال رائع على ذلك قيد التنفيذ، اطلع على [وضع دردشة Janitor الخاص بـ C# .NET](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) من مستودع Awesome GitHub Copilot. هذا الوضع يستفيد بشكل خاص من خادم Microsoft Learn Docs MCP للمساعدة في تنظيف وتحديث كود C# باستخدام أحدث الأنماط وأفضل الممارسات.
### 2. ☁️ خادم Azure MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**ما الذي يفعله**: خادم Azure MCP هو مجموعة شاملة تضم أكثر من 15 موصلًا متخصصًا لخدمات Azure، يجلب لك كامل نظام Azure البيئي إلى سير عمل الذكاء الاصطناعي الخاص بك. هذا ليس مجرد خادم واحد – بل هو مجموعة قوية تشمل إدارة الموارد، الاتصال بقواعد البيانات (PostgreSQL، SQL Server)، تحليل سجلات Azure Monitor باستخدام KQL، تكامل Cosmos DB، وأكثر من ذلك بكثير.

**لماذا هو مفيد**: بالإضافة إلى إدارة موارد Azure، يحسن هذا الخادم جودة الكود بشكل كبير عند العمل مع Azure SDKs. عند استخدام Azure MCP في وضع Agent، لا يساعدك فقط في كتابة الكود – بل يساعدك على كتابة كود Azure *أفضل* يتبع أنماط المصادقة الحالية، وأفضل ممارسات التعامل مع الأخطاء، ويستفيد من أحدث ميزات SDK. بدلاً من الحصول على كود عام قد يعمل، تحصل على كود يتبع أنماط Azure الموصى بها لأعباء العمل الإنتاجية.

**الوحدات الرئيسية تشمل**:
- **🗄️ موصلات قواعد البيانات**: وصول مباشر باستخدام اللغة الطبيعية إلى Azure Database لـ PostgreSQL و SQL Server
- **📊 Azure Monitor**: تحليل السجلات باستخدام KQL ورؤى تشغيلية
- **🌐 إدارة الموارد**: إدارة دورة حياة كاملة لموارد Azure
- **🔐 المصادقة**: أنماط DefaultAzureCredential والهوية المُدارة
- **📦 خدمات التخزين**: عمليات Blob Storage، Queue Storage، و Table Storage
- **🚀 خدمات الحاويات**: إدارة Azure Container Apps، Container Instances، و AKS
- **وغيرها من الموصلات المتخصصة**

**الاستخدام العملي**: "اعرض لي حسابات التخزين الخاصة بي في Azure"، "استعلم عن أخطاء في مساحة عمل Log Analytics خلال الساعة الماضية"، أو "ساعدني في بناء تطبيق Azure باستخدام Node.js مع مصادقة صحيحة"

**سيناريو العرض الكامل**: إليك شرحًا كاملاً يوضح قوة دمج Azure MCP مع امتداد GitHub Copilot لـ Azure في VS Code. عند تثبيت كلاهما وإدخال الأمر:

> "أنشئ سكريبت Python يرفع ملفًا إلى Azure Blob Storage باستخدام مصادقة DefaultAzureCredential. يجب أن يتصل السكريبت بحساب التخزين الخاص بي المسمى 'mycompanystorage'، يرفع إلى حاوية باسم 'documents'، ينشئ ملف اختبار مع الطابع الزمني الحالي للرفع، يتعامل مع الأخطاء بسلاسة ويعطي مخرجات مفيدة، يتبع أفضل ممارسات Azure للمصادقة والتعامل مع الأخطاء، يتضمن تعليقات تشرح كيفية عمل مصادقة DefaultAzureCredential، ويجعل السكريبت منظمًا بشكل جيد مع دوال ووثائق مناسبة."

سيولد خادم Azure MCP سكريبت Python كامل وجاهز للإنتاج يقوم بـ:
- استخدام أحدث SDK لـ Azure Blob Storage مع أنماط async الصحيحة
- تنفيذ DefaultAzureCredential مع شرح شامل لسلسلة التراجع
- تضمين معالجة أخطاء قوية مع أنواع استثناءات Azure المحددة
- اتباع أفضل ممارسات Azure SDK لإدارة الموارد والتوصيل
- توفير تسجيل مفصل ومخرجات معلوماتية على الكونسول
- إنشاء سكريبت منظم بشكل صحيح مع دوال، توثيق، وتلميحات نوعية

ما يجعل هذا مميزًا هو أنه بدون Azure MCP، قد تحصل على كود تخزين عام يعمل لكنه لا يتبع أنماط Azure الحالية. مع Azure MCP، تحصل على كود يستفيد من أحدث طرق المصادقة، يتعامل مع سيناريوهات الأخطاء الخاصة بـ Azure، ويتبع ممارسات مايكروسوفت الموصى بها للتطبيقات الإنتاجية.

**مثال مميز**: كنت أواجه صعوبة في تذكر الأوامر المحددة لـ `az` و `azd` للاستخدام العشوائي. دائمًا ما تكون عملية من خطوتين بالنسبة لي: أولًا أبحث عن الصياغة، ثم أنفذ الأمر. غالبًا ما ألجأ إلى البوابة وأتصفح لإنجاز العمل لأنني لا أريد الاعتراف بأنني لا أتذكر صياغة CLI. القدرة على وصف ما أريد فقط أمر مذهل، والأفضل من ذلك أن أتمكن من فعل ذلك دون مغادرة بيئة التطوير الخاصة بي!

هناك قائمة رائعة من حالات الاستخدام في [مستودع Azure MCP](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) لتبدأ بها. للحصول على أدلة إعداد شاملة وخيارات تكوين متقدمة، اطلع على [التوثيق الرسمي لـ Azure MCP](https://learn.microsoft.com/azure/developer/azure-mcp-server/).

### 3. 🐙 خادم GitHub MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**ما الذي يفعله**: يوفر خادم GitHub MCP الرسمي تكاملًا سلسًا مع كامل نظام GitHub البيئي، مع خيارات استضافة عن بُعد أو نشر محلي عبر Docker. هذا ليس مجرد عمليات مستودع أساسية – بل هو مجموعة أدوات شاملة تشمل إدارة GitHub Actions، سير عمل طلبات السحب، تتبع القضايا، فحص الأمان، الإشعارات، وقدرات أتمتة متقدمة.

**لماذا هو مفيد**: يحول هذا الخادم طريقة تفاعلك مع GitHub من خلال جلب تجربة المنصة الكاملة مباشرة إلى بيئة تطويرك. بدلاً من التنقل المستمر بين VS Code و GitHub.com لإدارة المشاريع، مراجعة الكود، ومراقبة CI/CD، يمكنك التعامل مع كل شيء عبر أوامر اللغة الطبيعية مع البقاء مركزًا على الكود الخاص بك.

> **ℹ️ ملاحظة: أنواع مختلفة من "الوكلاء"**
> 
> لا تخلط بين خادم GitHub MCP هذا و GitHub Coding Agent (الوكيل الذكي الذي يمكنك تعيين القضايا إليه للمهام البرمجية الآلية). يعمل خادم GitHub MCP ضمن وضع Agent في VS Code لتوفير تكامل API الخاص بـ GitHub، بينما GitHub Coding Agent هو ميزة منفصلة تنشئ طلبات سحب عند تعيينها لقضايا GitHub.

**القدرات الرئيسية تشمل**:
- **⚙️ GitHub Actions**: إدارة كاملة لأنابيب CI/CD، مراقبة سير العمل، والتعامل مع القطع الأثرية
- **🔀 طلبات السحب**: إنشاء، مراجعة، دمج، وإدارة طلبات السحب مع تتبع حالة شامل
- **🐛 القضايا**: إدارة دورة حياة القضايا كاملة، التعليق، التصنيف، والتعيين
- **🔒 الأمان**: تنبيهات فحص الكود، كشف الأسرار، وتكامل Dependabot
- **🔔 الإشعارات**: إدارة ذكية للإشعارات والتحكم في الاشتراك بالمستودعات
- **📁 إدارة المستودعات**: عمليات الملفات، إدارة الفروع، وإدارة المستودعات
- **👥 التعاون**: البحث عن المستخدمين والمنظمات، إدارة الفرق، والتحكم في الوصول

**الاستخدام العملي**: "أنشئ طلب سحب من فرع الميزات الخاص بي"، "أرني كل عمليات CI الفاشلة هذا الأسبوع"، "اعرض لي تنبيهات الأمان المفتوحة لمستودعاتي"، أو "ابحث عن كل القضايا المعينة لي عبر منظماتي"

**سيناريو العرض الكامل**: إليك سير عمل قوي يوضح قدرات خادم GitHub MCP:

> "أحتاج للتحضير لمراجعة السبرينت. أرني كل طلبات السحب التي أنشأتها هذا الأسبوع، تحقق من حالة أنابيب CI/CD الخاصة بنا، أنشئ ملخصًا لأي تنبيهات أمان نحتاج لمعالجتها، وساعدني في صياغة ملاحظات الإصدار بناءً على طلبات السحب المدمجة التي تحمل تصنيف 'feature'."

سيقوم خادم GitHub MCP بـ:
- استعلام طلبات السحب الأخيرة مع معلومات حالة مفصلة
- تحليل تشغيلات سير العمل وتسليط الضوء على أي إخفاقات أو مشاكل أداء
- تجميع نتائج فحص الأمان وترتيب التنبيهات الحرجة
- إنشاء ملاحظات إصدار شاملة من خلال استخراج المعلومات من طلبات السحب المدمجة
- تقديم خطوات قابلة للتنفيذ للتخطيط للسبرينت والتحضير للإصدار

**مثال مميز**: أحب استخدام هذا لسير عمل مراجعة الكود. بدلاً من التنقل بين VS Code، إشعارات GitHub، وصفحات طلبات السحب، يمكنني قول "أرني كل طلبات السحب التي تنتظر مراجعتي" ثم "أضف تعليقًا على PR #123 يسأل عن التعامل مع الأخطاء في طريقة المصادقة." يتولى الخادم استدعاءات API الخاصة بـ GitHub، يحافظ على سياق النقاش، ويساعدني حتى في صياغة تعليقات مراجعة أكثر بناءة.

**خيارات المصادقة**: يدعم الخادم كل من OAuth (بشكل سلس في VS Code) ورموز الوصول الشخصية، مع مجموعات أدوات قابلة للتكوين لتمكين وظائف GitHub التي تحتاجها فقط. يمكنك تشغيله كخدمة مستضافة عن بُعد للإعداد الفوري أو محليًا عبر Docker للتحكم الكامل.

> **💡 نصيحة احترافية**
> 
> فعّل فقط مجموعات الأدوات التي تحتاجها عن طريق تكوين معلمة `--toolsets` في إعدادات خادم MCP لتقليل حجم السياق وتحسين اختيار أدوات الذكاء الاصطناعي. على سبيل المثال، أضف `"--toolsets", "repos,issues,pull_requests,actions"` إلى وسائط تكوين MCP لسير عمل التطوير الأساسي، أو استخدم `"--toolsets", "notifications, security"` إذا كنت تريد بشكل أساسي قدرات مراقبة GitHub.

### 4. 🔄 خادم Azure DevOps MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_DevOps_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_DevOps_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/azure-devops-mcp)

**ما الذي يفعله**: يتصل بخدمات Azure DevOps لإدارة المشاريع الشاملة، تتبع عناصر العمل، إدارة أنابيب البناء، وعمليات المستودع.

**لماذا هو مفيد**: للفرق التي تستخدم Azure DevOps كمنصة DevOps الأساسية، يلغي هذا الخادم الحاجة للتنقل المستمر بين بيئة التطوير وواجهة الويب الخاصة بـ Azure DevOps. يمكنك إدارة عناصر العمل، التحقق من حالة البناء، استعلام المستودعات، والتعامل مع مهام إدارة المشاريع مباشرة من مساعد الذكاء الاصطناعي الخاص بك.

**الاستخدام العملي**: "أرني كل عناصر العمل النشطة في السبرينت الحالي لمشروع WebApp"، "أنشئ تقرير خطأ لمشكلة تسجيل الدخول التي اكتشفتها للتو"، أو "تحقق من حالة أنابيب البناء لدينا وأرني أي إخفاقات حديثة"

**مثال مميز**: يمكنك بسهولة التحقق من حالة السبرينت الحالي لفريقك باستعلام بسيط مثل "أرني كل عناصر العمل النشطة في السبرينت الحالي لمشروع WebApp" أو "أنشئ تقرير خطأ لمشكلة تسجيل الدخول التي اكتشفتها للتو" دون مغادرة بيئة التطوير الخاصة بك.

### 5. 📝 خادم MarkItDown MCP
[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**ما يفعله**: MarkItDown هو خادم تحويل مستندات شامل يحول تنسيقات ملفات متنوعة إلى Markdown عالي الجودة، مُحسّن لاستهلاك نماذج اللغة الكبيرة (LLM) وسير عمل تحليل النصوص.

**لماذا هو مفيد**: ضروري لسير عمل التوثيق الحديث! يتعامل MarkItDown مع مجموعة واسعة من تنسيقات الملفات مع الحفاظ على الهيكل الأساسي للمستند مثل العناوين، القوائم، الجداول، والروابط. على عكس أدوات استخراج النصوص البسيطة، يركز على الحفاظ على المعنى الدلالي والتنسيق الذي يفيد كل من المعالجة بالذكاء الاصطناعي وقابلية القراءة البشرية.

**تنسيقات الملفات المدعومة**:
- **مستندات Office**: PDF، PowerPoint (PPTX)، Word (DOCX)، Excel (XLSX/XLS)
- **ملفات الوسائط**: الصور (مع بيانات EXIF وOCR)، الصوت (مع بيانات EXIF ونصوص الكلام)
- **محتوى الويب**: HTML، خلاصات RSS، روابط YouTube، صفحات ويكيبيديا
- **تنسيقات البيانات**: CSV، JSON، XML، ملفات ZIP (تعالج المحتويات بشكل متكرر)
- **تنسيقات النشر**: EPub، دفاتر Jupyter (.ipynb)
- **البريد الإلكتروني**: رسائل Outlook (.msg)
- **متقدم**: تكامل Azure Document Intelligence لتحسين معالجة ملفات PDF

**القدرات المتقدمة**: يدعم MarkItDown وصف الصور باستخدام نماذج اللغة الكبيرة (عند توفير عميل OpenAI)، Azure Document Intelligence لتحسين معالجة PDF، نسخ النصوص الصوتية للمحتوى الكلامي، ونظام الإضافات لتوسيع الدعم لتنسيقات ملفات إضافية.

**الاستخدام العملي**: "حوّل هذا العرض التقديمي من PowerPoint إلى Markdown لموقع التوثيق الخاص بنا"، "استخرج النص من هذا PDF مع الحفاظ على هيكل العناوين الصحيح"، أو "حوّل جدول Excel هذا إلى تنسيق جدول قابل للقراءة".

**مثال مميز**: للاقتباس من [وثائق MarkItDown](https://github.com/microsoft/markitdown#why-markdown):

> Markdown قريب جدًا من النص العادي، مع أقل قدر من العلامات أو التنسيق، لكنه يوفر طريقة لتمثيل الهيكل المهم للمستند. نماذج اللغة الكبيرة الشائعة، مثل GPT-4o من OpenAI، "تتحدث" Markdown بطبيعتها، وغالبًا ما تدمج Markdown في ردودها دون طلب. هذا يشير إلى أنها تدربت على كميات هائلة من النصوص المنسقة بـ Markdown، وتفهمها جيدًا. كميزة جانبية، قواعد Markdown فعالة جدًا من حيث عدد الرموز المستخدمة.

MarkItDown بارع جدًا في الحفاظ على هيكل المستند، وهو أمر مهم لسير عمل الذكاء الاصطناعي. على سبيل المثال، عند تحويل عرض PowerPoint، يحافظ على تنظيم الشرائح مع العناوين المناسبة، يستخرج الجداول كجداول Markdown، يضيف نص بديل للصور، ويعالج حتى ملاحظات المتحدث. تتحول المخططات إلى جداول بيانات قابلة للقراءة، ويحافظ Markdown الناتج على التسلسل المنطقي للعرض الأصلي. هذا يجعله مثاليًا لإدخال محتوى العروض التقديمية في أنظمة الذكاء الاصطناعي أو لإنشاء التوثيق من الشرائح الموجودة.

### 6. 🗃️ خادم SQL Server MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**ما يفعله**: يوفر وصولًا حواريًا إلى قواعد بيانات SQL Server (محليًا، Azure SQL، أو Fabric)

**لماذا هو مفيد**: مشابه لخادم PostgreSQL لكنه مخصص لنظام Microsoft SQL. اتصل بسلسلة اتصال بسيطة وابدأ الاستعلام باستخدام اللغة الطبيعية – لا حاجة لتبديل السياق بعد الآن!

**الاستخدام العملي**: "ابحث عن جميع الطلبات التي لم تُنفذ خلال الثلاثين يومًا الماضية" تُترجم إلى استعلامات SQL مناسبة وتُرجع النتائج بتنسيق منسق.

**مثال مميز**: بمجرد إعداد اتصال قاعدة البيانات، يمكنك بدء المحادثة مع بياناتك فورًا. يعرض منشور المدونة هذا من خلال سؤال بسيط: "ما قاعدة البيانات التي تتصل بها؟" يرد خادم MCP باستدعاء أداة قاعدة البيانات المناسبة، ويتصل بمثيل SQL Server الخاص بك، ويُرجع تفاصيل اتصال قاعدة البيانات الحالية – كل ذلك دون كتابة سطر SQL واحد. يدعم الخادم عمليات قاعدة البيانات الشاملة من إدارة المخطط إلى التلاعب بالبيانات، كلها من خلال أوامر باللغة الطبيعية. للحصول على تعليمات الإعداد الكاملة وأمثلة التكوين مع VS Code وClaude Desktop، راجع: [تقديم خادم MSSQL MCP (معاينة)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/).

### 7. 🎭 خادم Playwright MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**ما يفعله**: يمكّن وكلاء الذكاء الاصطناعي من التفاعل مع صفحات الويب للاختبار والأتمتة

> **ℹ️ يدعم GitHub Copilot**
> 
> خادم Playwright MCP يدعم وكيل الترميز في GitHub Copilot، مما يمنحه قدرات تصفح الويب! [تعرف على المزيد حول هذه الميزة](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/).

**لماذا هو مفيد**: مثالي للاختبار الآلي المدفوع بوصف اللغة الطبيعية. يمكن للذكاء الاصطناعي تصفح المواقع، ملء النماذج، واستخراج البيانات من خلال لقطات وصول منظمة – هذه قدرات قوية جدًا!

**الاستخدام العملي**: "اختبر تدفق تسجيل الدخول وتحقق من تحميل لوحة التحكم بشكل صحيح" أو "أنشئ اختبارًا يبحث عن المنتجات ويتحقق من صفحة النتائج" – كل ذلك دون الحاجة إلى كود مصدر التطبيق.

**مثال مميز**: زميلتي ديبي أوبراين قامت بعمل رائع مؤخرًا مع خادم Playwright MCP! على سبيل المثال، أظهرت مؤخرًا كيف يمكن إنشاء اختبارات Playwright كاملة دون الحاجة إلى الوصول إلى كود التطبيق. في سيناريوها، طلبت من Copilot إنشاء اختبار لتطبيق بحث عن الأفلام: تصفح الموقع، ابحث عن "Garfield"، وتحقق من ظهور الفيلم في النتائج. أطلق MCP جلسة متصفح، استكشف هيكل الصفحة باستخدام لقطات DOM، حدد المحددات الصحيحة، وأنشأ اختبار TypeScript يعمل بالكامل ونجح من المحاولة الأولى.

ما يجعل هذا قويًا حقًا هو أنه يجسر الفجوة بين تعليمات اللغة الطبيعية وكود الاختبار القابل للتنفيذ. الطرق التقليدية تتطلب كتابة الاختبارات يدويًا أو الوصول إلى قاعدة الكود للسياق. لكن مع Playwright MCP، يمكنك اختبار المواقع الخارجية، تطبيقات العملاء، أو العمل في سيناريوهات اختبار الصندوق الأسود حيث لا يتوفر الوصول إلى الكود.

### 8. 💻 خادم Dev Box MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**ما يفعله**: يدير بيئات Microsoft Dev Box من خلال اللغة الطبيعية

**لماذا هو مفيد**: يبسط إدارة بيئات التطوير بشكل كبير! أنشئ، قم بتكوين، وأدر بيئات التطوير دون الحاجة لتذكر الأوامر المحددة.

**الاستخدام العملي**: "أنشئ Dev Box جديد مع أحدث .NET SDK وقم بتكوينه لمشروعنا"، "تحقق من حالة جميع بيئات التطوير الخاصة بي"، أو "أنشئ بيئة عرض توضيحي موحدة لعروض الفريق".

**مثال مميز**: أنا من المعجبين باستخدام Dev Box للتطوير الشخصي. لحظة الإلهام كانت عندما شرح جيمس مونتيماغنو مدى روعة Dev Box لعروض المؤتمرات، لأنه يحتوي على اتصال إيثرنت فائق السرعة بغض النظر عن شبكة المؤتمر أو الفندق أو الواي فاي في الطائرة التي أستخدمها في ذلك الوقت. في الواقع، قمت مؤخرًا ببعض التدريبات على عروض المؤتمرات بينما كان حاسوبي المحمول متصلًا بنقطة اتصال هاتفي أثناء ركوب الحافلة من بروج إلى أنتويرب! لكن خطوتي التالية هي التعمق في إدارة الفريق لعدة بيئات تطوير وبيئات عرض توضيحي موحدة. وحالة استخدام كبيرة أخرى سمعتها من العملاء والزملاء هي استخدام Dev Box لبيئات تطوير مُعدة مسبقًا. في كلتا الحالتين، يتيح استخدام MCP لتكوين وإدارة Dev Boxes التفاعل باللغة الطبيعية، وكل ذلك أثناء البقاء في بيئة التطوير الخاصة بك.

### 9. 🤖 خادم Azure AI Foundry MCP
[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**ما الذي يفعله**: يوفر خادم Azure AI Foundry MCP للمطورين وصولاً شاملاً إلى نظام Azure البيئي للذكاء الاصطناعي، بما في ذلك كتالوجات النماذج، إدارة النشر، فهرسة المعرفة باستخدام Azure AI Search، وأدوات التقييم. هذا الخادم التجريبي يجسر الفجوة بين تطوير الذكاء الاصطناعي وبنية Azure القوية، مما يسهل بناء ونشر وتقييم تطبيقات الذكاء الاصطناعي.

**لماذا هو مفيد**: يحول هذا الخادم طريقة عملك مع خدمات Azure AI من خلال جلب قدرات الذكاء الاصطناعي على مستوى المؤسسات مباشرة إلى سير عمل التطوير الخاص بك. بدلاً من التنقل بين بوابة Azure، الوثائق، وبيئة التطوير المتكاملة، يمكنك اكتشاف النماذج، نشر الخدمات، إدارة قواعد المعرفة، وتقييم أداء الذكاء الاصطناعي عبر أوامر اللغة الطبيعية. وهو قوي بشكل خاص للمطورين الذين يبنون تطبيقات RAG (التوليد المعزز بالاسترجاع)، يديرون نشرات متعددة للنماذج، أو ينفذون خطوط تقييم شاملة للذكاء الاصطناعي.

**القدرات الرئيسية للمطورين**:
- **🔍 اكتشاف النماذج والنشر**: استعرض كتالوج نماذج Azure AI Foundry، احصل على معلومات مفصلة مع أمثلة برمجية، وانشر النماذج إلى خدمات Azure AI
- **📚 إدارة المعرفة**: أنشئ وأدر فهارس Azure AI Search، أضف مستندات، قم بتكوين الفهارس، وابنِ أنظمة RAG متقدمة
- **⚡ تكامل وكلاء الذكاء الاصطناعي**: اتصل بوكلاء Azure AI، استعلم عن الوكلاء الحاليين، وقيم أداء الوكلاء في سيناريوهات الإنتاج
- **📊 إطار التقييم**: نفذ تقييمات شاملة للنصوص والوكلاء، أنشئ تقارير بتنسيق markdown، وطبق ضمان الجودة لتطبيقات الذكاء الاصطناعي
- **🚀 أدوات النماذج الأولية**: احصل على تعليمات الإعداد للنماذج الأولية المستندة إلى GitHub وادخل إلى Azure AI Foundry Labs لأحدث نماذج البحث

**استخدام المطورين في العالم الحقيقي**: "أنشر نموذج Phi-4 إلى خدمات Azure AI لتطبيقي"، "أنشئ فهرس بحث جديد لنظام RAG الخاص بوثائقي"، "قيّم ردود وكيلي مقابل معايير الجودة"، أو "ابحث عن أفضل نموذج استدلال لمهام التحليل المعقدة الخاصة بي"

**سيناريو العرض الكامل**: إليك سير عمل قوي لتطوير الذكاء الاصطناعي:

> "أنا أبني وكيل دعم العملاء. ساعدني في العثور على نموذج استدلال جيد من الكتالوج، نشره إلى خدمات Azure AI، إنشاء قاعدة معرفة من وثائقنا، إعداد إطار تقييم لاختبار جودة الردود، ثم ساعدني في بناء نموذج أولي للتكامل مع GitHub باستخدام رمز التوثيق للاختبار."

سيقوم خادم Azure AI Foundry MCP بـ:
- استعلام كتالوج النماذج لتوصية أفضل نماذج الاستدلال بناءً على متطلباتك
- توفير أوامر النشر ومعلومات الحصص لمنطقتك المفضلة في Azure
- إعداد فهارس Azure AI Search مع المخطط المناسب لوثائقك
- تكوين خطوط تقييم مع معايير الجودة وفحوصات الأمان
- إنشاء كود النماذج الأولية مع توثيق GitHub للاختبار الفوري
- توفير أدلة إعداد شاملة مخصصة لتقنية التطوير الخاصة بك

**مثال مميز**: كمطور، كنت أجد صعوبة في متابعة نماذج LLM المختلفة المتاحة. أعرف بعض النماذج الرئيسية، لكنني شعرت أنني أفوت بعض مكاسب الإنتاجية والكفاءة. إدارة الرموز والحصص مرهقة وصعبة – لا أعرف أبدًا إذا كنت أختار النموذج المناسب للمهمة أو أستهلك ميزانيتي بشكل غير فعال. سمعت عن هذا الخادم MCP من جيمس مونتيماغنو أثناء استشارتي مع زملائي حول توصيات MCP، وأنا متحمس لاستخدامه! تبدو قدرات اكتشاف النماذج مثيرة للإعجاب لشخص مثلي يريد استكشاف ما هو أبعد من النماذج المعتادة والعثور على نماذج محسنة لمهام محددة. يجب أن يساعدني إطار التقييم في التأكد من أنني أحصل فعلاً على نتائج أفضل، وليس مجرد تجربة شيء جديد لمجرد التجربة.

> **ℹ️ الحالة التجريبية**
> 
> هذا الخادم MCP تجريبي وقيد التطوير النشط. قد تتغير الميزات وواجهات برمجة التطبيقات. مثالي لاستكشاف قدرات Azure AI وبناء النماذج الأولية، لكن تحقق من متطلبات الاستقرار للاستخدام في الإنتاج.

### 10. 🏢 خادم أدوات وكلاء Microsoft 365 MCP

[![التثبيت في VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![التثبيت في VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**ما الذي يفعله**: يوفر للمطورين أدوات أساسية لبناء وكلاء الذكاء الاصطناعي والتطبيقات التي تتكامل مع Microsoft 365 وMicrosoft 365 Copilot، بما في ذلك التحقق من صحة المخططات، استرجاع أمثلة الكود، والمساعدة في استكشاف الأخطاء وإصلاحها.

**لماذا هو مفيد**: البناء لـ Microsoft 365 وCopilot يتطلب مخططات معقدة وأنماط تطوير محددة. يجلب هذا الخادم MCP موارد التطوير الأساسية مباشرة إلى بيئة الترميز الخاصة بك، مما يساعدك على التحقق من صحة المخططات، العثور على أمثلة الكود، وحل المشكلات الشائعة دون الحاجة للرجوع المستمر إلى الوثائق.

**الاستخدام في العالم الحقيقي**: "تحقق من صحة ملف تعريف الوكيل الإعلاني الخاص بي وأصلح أي أخطاء في المخطط"، "أرني مثالاً على كود لتنفيذ مكون إضافي لـ Microsoft Graph API"، أو "ساعدني في استكشاف مشكلات مصادقة تطبيق Teams الخاص بي"

**مثال مميز**: تواصلت مع صديقي جون ميلر بعد حديثنا في مؤتمر Build عن وكلاء M365، وأوصى بهذا MCP. قد يكون هذا رائعًا للمطورين الجدد على وكلاء M365 لأنه يوفر قوالب، أمثلة كود، وهياكل للبدء دون الغرق في الوثائق. تبدو ميزات التحقق من صحة المخططات مفيدة بشكل خاص لتجنب أخطاء هيكل الملف التعريفي التي قد تسبب ساعات من تصحيح الأخطاء.

> **💡 نصيحة احترافية**
> 
> استخدم هذا الخادم جنبًا إلى جنب مع خادم Microsoft Learn Docs MCP للحصول على دعم تطوير M365 شامل – حيث يوفر أحدهما الوثائق الرسمية بينما يقدم هذا أدوات تطوير عملية ومساعدة في استكشاف الأخطاء.

## ما التالي؟ 🔮

## 📋 الخاتمة

يغير بروتوكول سياق النموذج (MCP) طريقة تفاعل المطورين مع مساعدي الذكاء الاصطناعي والأدوات الخارجية. توضح هذه الخوادم العشرة من Microsoft MCP قوة التكامل الموحد للذكاء الاصطناعي، مما يتيح سير عمل سلس يحافظ على تركيز المطورين أثناء الوصول إلى قدرات خارجية قوية.

من التكامل الشامل لنظام Azure البيئي إلى الأدوات المتخصصة مثل Playwright لأتمتة المتصفح وMarkItDown لمعالجة المستندات، تعرض هذه الخوادم كيف يمكن لـ MCP تعزيز الإنتاجية عبر سيناريوهات تطوير متنوعة. يضمن البروتوكول الموحد عمل هذه الأدوات معًا بسلاسة، مما يخلق تجربة تطوير متماسكة.

مع استمرار تطور نظام MCP البيئي، سيكون البقاء على تواصل مع المجتمع، استكشاف الخوادم الجديدة، وبناء حلول مخصصة مفتاحًا لتعظيم إنتاجيتك في التطوير. تعني الطبيعة المفتوحة لـ MCP أنه يمكنك مزج ومطابقة الأدوات من بائعين مختلفين لإنشاء سير عمل مثالي لاحتياجاتك الخاصة.

## 🔗 موارد إضافية

- [المستودع الرسمي لـ Microsoft MCP](https://github.com/microsoft/mcp)
- [مجتمع MCP والوثائق](https://modelcontextprotocol.io/introduction)
- [وثائق MCP لـ VS Code](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [وثائق MCP لـ Visual Studio](https://learn.microsoft.com/visualstudio/ide/mcp-servers)
- [وثائق Azure MCP](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [لنبدأ – فعاليات MCP](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/lets-learn---mcp-events-a-beginners-guide-to-the-model-context-protocol/4429023)
- [تخصيصات رائعة لـ GitHub Copilot](https://github.com/awesome-copilot)
- [SDK MCP لـ C#](https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol)
- [أيام تطوير MCP مباشرة 29/30 يوليو أو المشاهدة عند الطلب](https://aka.ms/mcpdevdays)

## 🎯 تمارين

1. **التثبيت والتكوين**: قم بإعداد أحد خوادم MCP في بيئة VS Code الخاصة بك واختبر الوظائف الأساسية.
2. **تكامل سير العمل**: صمم سير عمل تطوير يجمع بين ثلاثة خوادم MCP مختلفة على الأقل.
3. **تخطيط خادم مخصص**: حدد مهمة في روتين تطويرك اليومي يمكن أن تستفيد من خادم MCP مخصص وأنشئ مواصفات لها.
4. **تحليل الأداء**: قارن كفاءة استخدام خوادم MCP مقابل الطرق التقليدية للمهام التطويرية الشائعة.
5. **تقييم الأمان**: قيّم تداعيات الأمان لاستخدام خوادم MCP في بيئة التطوير الخاصة بك واقترح أفضل الممارسات.

التالي: [أفضل الممارسات](../08-BestPractices/README.md)

**إخلاء مسؤولية**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق به. للمعلومات الهامة، يُنصح بالاعتماد على الترجمة البشرية المهنية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.