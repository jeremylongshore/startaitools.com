<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "9678e0c6945b8e0c23586869b0e26783",
  "translation_date": "2025-10-06T10:50:02+00:00",
  "source_file": "00-Introduction/README.md",
  "language_code": "ar"
}
-->
# مقدمة إلى بروتوكول سياق النموذج (MCP): لماذا هو مهم لتطبيقات الذكاء الاصطناعي القابلة للتوسع

[![مقدمة إلى بروتوكول سياق النموذج](../../../translated_images/01.a467036d886b5fb5b9cf7b39bac0e743b6ca0a4a18a492de90061daaf0cc55f0.ar.png)](https://youtu.be/agBbdiOPLQA)

_(انقر على الصورة أعلاه لمشاهدة فيديو الدرس)_

تُعتبر تطبيقات الذكاء الاصطناعي التوليدي خطوة كبيرة إلى الأمام لأنها غالبًا ما تتيح للمستخدم التفاعل مع التطبيق باستخدام مطالبات اللغة الطبيعية. ومع ذلك، مع زيادة الوقت والموارد المستثمرة في هذه التطبيقات، ستحتاج إلى التأكد من أنه يمكنك دمج الوظائف والموارد بسهولة بطريقة تجعل التوسع سهلاً، وأن تطبيقك يمكنه التعامل مع أكثر من نموذج واحد مستخدم، ومعالجة تعقيدات النماذج المختلفة. باختصار، بناء تطبيقات الذكاء الاصطناعي التوليدي سهل في البداية، ولكن مع نموها وزيادة تعقيدها، ستحتاج إلى البدء في تحديد بنية وقد تحتاج إلى الاعتماد على معيار لضمان بناء تطبيقاتك بطريقة متسقة. هنا يأتي دور MCP لتنظيم الأمور وتوفير معيار.

---

## **🔍 ما هو بروتوكول سياق النموذج (MCP)؟**

**بروتوكول سياق النموذج (MCP)** هو **واجهة مفتوحة ومعيارية** تتيح للنماذج اللغوية الكبيرة (LLMs) التفاعل بسلاسة مع الأدوات الخارجية وواجهات برمجة التطبيقات ومصادر البيانات. يوفر بنية متسقة لتعزيز وظائف نماذج الذكاء الاصطناعي بما يتجاوز بيانات التدريب الخاصة بها، مما يتيح أنظمة ذكاء اصطناعي أكثر ذكاءً وقابلة للتوسع وأكثر استجابة.

---

## **🎯 لماذا يهم التوحيد القياسي في الذكاء الاصطناعي**

مع تعقيد تطبيقات الذكاء الاصطناعي التوليدي، يصبح من الضروري اعتماد معايير تضمن **القابلية للتوسع، والامتداد، والصيانة،** وتجنب **الاعتماد على مورد واحد**. يعالج MCP هذه الاحتياجات من خلال:

- توحيد تكامل النماذج مع الأدوات
- تقليل الحلول المخصصة الهشة
- السماح بتعايش نماذج متعددة من موردين مختلفين داخل نظام واحد

**ملاحظة:** على الرغم من أن MCP يقدم نفسه كمعيار مفتوح، لا توجد خطط لتوحيد MCP من خلال أي هيئات معايير قائمة مثل IEEE، IETF، W3C، ISO، أو أي هيئة معايير أخرى.

---

## **📚 أهداف التعلم**

بنهاية هذه المقالة، ستكون قادرًا على:

- تعريف **بروتوكول سياق النموذج (MCP)** واستخداماته
- فهم كيفية توحيد MCP للتواصل بين النموذج والأدوات
- التعرف على المكونات الأساسية لبنية MCP
- استكشاف تطبيقات MCP في سياقات المؤسسات والتطوير

---

## **💡 لماذا يُعتبر بروتوكول سياق النموذج (MCP) نقطة تحول**

### **🔗 MCP يحل مشكلة التجزئة في تفاعلات الذكاء الاصطناعي**

قبل MCP، كان دمج النماذج مع الأدوات يتطلب:

- كود مخصص لكل زوج من الأدوات والنماذج
- واجهات برمجة تطبيقات غير معيارية لكل مورد
- انقطاعات متكررة بسبب التحديثات
- ضعف القابلية للتوسع مع زيادة الأدوات

### **✅ فوائد توحيد MCP**

| **الفائدة**              | **الوصف**                                                                |
|--------------------------|--------------------------------------------------------------------------------|
| التوافق                  | تعمل النماذج اللغوية الكبيرة بسلاسة مع الأدوات عبر موردين مختلفين                       |
| الاتساق                  | سلوك موحد عبر المنصات والأدوات                                    |
| إعادة الاستخدام          | الأدوات التي يتم بناؤها مرة واحدة يمكن استخدامها عبر المشاريع والأنظمة                       |
| تسريع التطوير            | تقليل وقت التطوير باستخدام واجهات معيارية جاهزة للتوصيل والاستخدام                |

---

## **🧱 نظرة عامة على بنية MCP عالية المستوى**

يتبع MCP نموذج **العميل-الخادم**، حيث:

- **مضيفو MCP** يشغلون نماذج الذكاء الاصطناعي
- **عملاء MCP** يبدؤون الطلبات
- **خوادم MCP** تقدم السياق، الأدوات، والقدرات

### **المكونات الرئيسية:**

- **الموارد** – بيانات ثابتة أو ديناميكية للنماذج  
- **المطالبات** – تدفقات عمل محددة مسبقًا لتوجيه التوليد  
- **الأدوات** – وظائف قابلة للتنفيذ مثل البحث، الحسابات  
- **التجميع** – سلوك وكيل عبر تفاعلات متكررة

---

## كيف تعمل خوادم MCP

تعمل خوادم MCP بالطريقة التالية:

- **تدفق الطلب**:
    1. يبدأ المستخدم النهائي أو البرنامج الذي يعمل نيابة عنه طلبًا.
    2. يرسل **عميل MCP** الطلب إلى **مضيف MCP**، الذي يدير وقت تشغيل نموذج الذكاء الاصطناعي.
    3. يتلقى **نموذج الذكاء الاصطناعي** مطالبة المستخدم وقد يطلب الوصول إلى أدوات أو بيانات خارجية عبر مكالمات أدوات متعددة.
    4. يتواصل **مضيف MCP**، وليس النموذج مباشرة، مع **خوادم MCP** المناسبة باستخدام البروتوكول المعياري.
- **وظائف مضيف MCP**:
    - **سجل الأدوات**: يحتفظ بكاتالوج الأدوات المتاحة وقدراتها.
    - **المصادقة**: يتحقق من أذونات الوصول إلى الأدوات.
    - **معالج الطلبات**: يعالج طلبات الأدوات الواردة من النموذج.
    - **منسق الردود**: يهيكل مخرجات الأدوات بتنسيق يمكن للنموذج فهمه.
- **تنفيذ خادم MCP**:
    - يقوم **مضيف MCP** بتوجيه مكالمات الأدوات إلى واحد أو أكثر من **خوادم MCP**، كل منها يعرض وظائف متخصصة (مثل البحث، الحسابات، استعلامات قواعد البيانات).
    - تقوم **خوادم MCP** بتنفيذ عملياتها الخاصة وتعيد النتائج إلى **مضيف MCP** بتنسيق متسق.
    - يقوم **مضيف MCP** بتنسيق هذه النتائج ويرسلها إلى **نموذج الذكاء الاصطناعي**.
- **إكمال الرد**:
    - يدمج **نموذج الذكاء الاصطناعي** مخرجات الأدوات في رد نهائي.
    - يرسل **مضيف MCP** هذا الرد إلى **عميل MCP**، الذي يقدمه للمستخدم النهائي أو البرنامج الذي قام بالطلب.

```mermaid
---
title: MCP Architecture and Component Interactions
description: A diagram showing the flows of the components in MCP.
---
graph TD
    Client[MCP Client/Application] -->|Sends Request| H[MCP Host]
    H -->|Invokes| A[AI Model]
    A -->|Tool Call Request| H
    H -->|MCP Protocol| T1[MCP Server Tool 01: Web Search]
    H -->|MCP Protocol| T2[MCP Server Tool 02: Calculator tool]
    H -->|MCP Protocol| T3[MCP Server Tool 03: Database Access tool]
    H -->|MCP Protocol| T4[MCP Server Tool 04: File System tool]
    H -->|Sends Response| Client

    subgraph "MCP Host Components"
        H
        G[Tool Registry]
        I[Authentication]
        J[Request Handler]
        K[Response Formatter]
    end

    H <--> G
    H <--> I
    H <--> J
    H <--> K

    style A fill:#f9d5e5,stroke:#333,stroke-width:2px
    style H fill:#eeeeee,stroke:#333,stroke-width:2px
    style Client fill:#d5e8f9,stroke:#333,stroke-width:2px
    style G fill:#fffbe6,stroke:#333,stroke-width:1px
    style I fill:#fffbe6,stroke:#333,stroke-width:1px
    style J fill:#fffbe6,stroke:#333,stroke-width:1px
    style K fill:#fffbe6,stroke:#333,stroke-width:1px
    style T1 fill:#c2f0c2,stroke:#333,stroke-width:1px
    style T2 fill:#c2f0c2,stroke:#333,stroke-width:1px
    style T3 fill:#c2f0c2,stroke:#333,stroke-width:1px
    style T4 fill:#c2f0c2,stroke:#333,stroke-width:1px
```

## 👨‍💻 كيفية بناء خادم MCP (مع أمثلة)

تتيح خوادم MCP توسيع قدرات النماذج اللغوية الكبيرة من خلال توفير البيانات والوظائف.

هل أنت جاهز لتجربتها؟ إليك حزم تطوير البرمجيات (SDKs) الخاصة بلغات وتقنيات مختلفة مع أمثلة لإنشاء خوادم MCP بسيطة:

- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk

- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk

- **Java SDK**: https://github.com/modelcontextprotocol/java-sdk

- **C#/.NET SDK**: https://github.com/modelcontextprotocol/csharp-sdk


## 🌍 حالات استخدام MCP في العالم الحقيقي

يتيح MCP مجموعة واسعة من التطبيقات من خلال توسيع قدرات الذكاء الاصطناعي:

| **التطبيق**              | **الوصف**                                                                |
|--------------------------|--------------------------------------------------------------------------------|
| تكامل بيانات المؤسسات    | ربط النماذج اللغوية الكبيرة بقواعد البيانات، أنظمة إدارة علاقات العملاء (CRMs)، أو الأدوات الداخلية                             |
| أنظمة الذكاء الاصطناعي الوكيلية | تمكين الوكلاء المستقلين من الوصول إلى الأدوات وعمليات اتخاذ القرار        |
| التطبيقات متعددة الوسائط  | دمج النصوص، الصور، والأدوات الصوتية داخل تطبيق ذكاء اصطناعي موحد            |
| تكامل البيانات في الوقت الفعلي | إدخال البيانات الحية في تفاعلات الذكاء الاصطناعي للحصول على مخرجات أكثر دقة وحداثة        |


### 🧠 MCP = معيار عالمي لتفاعلات الذكاء الاصطناعي

يعمل بروتوكول سياق النموذج (MCP) كمعيار عالمي لتفاعلات الذكاء الاصطناعي، تمامًا كما قام USB-C بتوحيد الاتصالات الفيزيائية للأجهزة. في عالم الذكاء الاصطناعي، يوفر MCP واجهة متسقة، مما يسمح للنماذج (العملاء) بالتكامل بسلاسة مع الأدوات الخارجية ومزودي البيانات (الخوادم). هذا يلغي الحاجة إلى بروتوكولات مخصصة ومتنوعة لكل واجهة برمجة تطبيقات أو مصدر بيانات.

تحت MCP، الأداة المتوافقة مع MCP (المشار إليها باسم خادم MCP) تتبع معيارًا موحدًا. يمكن لهذه الخوادم سرد الأدوات أو الإجراءات التي تقدمها وتنفيذ تلك الإجراءات عند طلبها من قبل وكيل الذكاء الاصطناعي. منصات الوكلاء الذكية التي تدعم MCP قادرة على اكتشاف الأدوات المتاحة من الخوادم واستدعائها من خلال هذا البروتوكول المعياري.

### 💡 تسهيل الوصول إلى المعرفة

إلى جانب تقديم الأدوات، يسهل MCP أيضًا الوصول إلى المعرفة. يتيح للتطبيقات توفير السياق للنماذج اللغوية الكبيرة (LLMs) من خلال ربطها بمصادر بيانات متنوعة. على سبيل المثال، قد يمثل خادم MCP مستودع مستندات الشركة، مما يسمح للوكلاء باسترجاع المعلومات ذات الصلة عند الطلب. يمكن لخادم آخر التعامل مع إجراءات محددة مثل إرسال البريد الإلكتروني أو تحديث السجلات. من منظور الوكيل، هذه ببساطة أدوات يمكنه استخدامها—بعض الأدوات تعيد البيانات (سياق المعرفة)، بينما يقوم البعض الآخر بتنفيذ الإجراءات. يدير MCP كلاهما بكفاءة.

يتعلم الوكيل المتصل بخادم MCP تلقائيًا القدرات المتاحة والبيانات القابلة للوصول من الخادم عبر تنسيق معياري. يتيح هذا التوحيد القياسي توفر الأدوات ديناميكيًا. على سبيل المثال، إضافة خادم MCP جديد إلى نظام الوكيل يجعل وظائفه قابلة للاستخدام فورًا دون الحاجة إلى تخصيص إضافي لتعليمات الوكيل.

يتماشى هذا التكامل المبسط مع التدفق الموضح في الرسم البياني التالي، حيث توفر الخوادم الأدوات والمعرفة، مما يضمن التعاون السلس عبر الأنظمة.

### 👉 مثال: حل وكيل قابل للتوسع

```mermaid
---
title: Scalable Agent Solution with MCP
description: A diagram illustrating how a user interacts with an LLM that connects to multiple MCP servers, with each server providing both knowledge and tools, creating a scalable AI system architecture
---
graph TD
    User -->|Prompt| LLM
    LLM -->|Response| User
    LLM -->|MCP| ServerA
    LLM -->|MCP| ServerB
    ServerA -->|Universal connector| ServerB
    ServerA --> KnowledgeA
    ServerA --> ToolsA
    ServerB --> KnowledgeB
    ServerB --> ToolsB

    subgraph Server A
        KnowledgeA[Knowledge]
        ToolsA[Tools]
    end

    subgraph Server B
        KnowledgeB[Knowledge]
        ToolsB[Tools]
    end
```

الموصل العالمي يتيح لخوادم MCP التواصل ومشاركة القدرات مع بعضها البعض، مما يسمح لـ ServerA بتفويض المهام إلى ServerB أو الوصول إلى أدواته ومعرفته. هذا يتيح توحيد الأدوات والبيانات عبر الخوادم، مما يدعم بنى الوكلاء القابلة للتوسع والمودولارية. نظرًا لأن MCP يوحد عرض الأدوات، يمكن للوكلاء اكتشاف وتوجيه الطلبات بين الخوادم ديناميكيًا دون تكاملات مشفرة.

توحيد الأدوات والمعرفة: يمكن الوصول إلى الأدوات والبيانات عبر الخوادم، مما يتيح بنى وكيلية أكثر قابلية للتوسع والمودولارية.

### 🔄 سيناريوهات MCP المتقدمة مع تكامل LLM على جانب العميل

إلى جانب بنية MCP الأساسية، هناك سيناريوهات متقدمة حيث يحتوي كل من العميل والخادم على نماذج لغوية كبيرة (LLMs)، مما يتيح تفاعلات أكثر تطورًا. في الرسم البياني التالي، يمكن أن يكون **تطبيق العميل** بيئة تطوير متكاملة (IDE) تحتوي على عدد من أدوات MCP المتاحة للاستخدام من قبل النموذج اللغوي الكبير:

```mermaid
---
title: Advanced MCP Scenarios with Client-Server LLM Integration
description: A sequence diagram showing the detailed interaction flow between user, client application, client LLM, multiple MCP servers, and server LLM, illustrating tool discovery, user interaction, direct tool calling, and feature negotiation phases
---
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant ClientApp as 🖥️ Client App
    participant ClientLLM as 🧠 Client LLM
    participant Server1 as 🔧 MCP Server 1
    participant Server2 as 📚 MCP Server 2
    participant ServerLLM as 🤖 Server LLM
    
    %% Discovery Phase
    rect rgb(220, 240, 255)
        Note over ClientApp, Server2: TOOL DISCOVERY PHASE
        ClientApp->>+Server1: Request available tools/resources
        Server1-->>-ClientApp: Return tool list (JSON)
        ClientApp->>+Server2: Request available tools/resources
        Server2-->>-ClientApp: Return tool list (JSON)
        Note right of ClientApp: Store combined tool<br/>catalog locally
    end
    
    %% User Interaction
    rect rgb(255, 240, 220)
        Note over User, ClientLLM: USER INTERACTION PHASE
        User->>+ClientApp: Enter natural language prompt
        ClientApp->>+ClientLLM: Forward prompt + tool catalog
        ClientLLM->>-ClientLLM: Analyze prompt & select tools
    end
    
    %% Scenario A: Direct Tool Calling
    alt Direct Tool Calling
        rect rgb(220, 255, 220)
            Note over ClientApp, Server1: SCENARIO A: DIRECT TOOL CALLING
            ClientLLM->>+ClientApp: Request tool execution
            ClientApp->>+Server1: Execute specific tool
            Server1-->>-ClientApp: Return results
            ClientApp->>+ClientLLM: Process results
            ClientLLM-->>-ClientApp: Generate response
            ClientApp-->>-User: Display final answer
        end
    
    %% Scenario B: Feature Negotiation (VS Code style)
    else Feature Negotiation (VS Code style)
        rect rgb(255, 220, 220)
            Note over ClientApp, ServerLLM: SCENARIO B: FEATURE NEGOTIATION
            ClientLLM->>+ClientApp: Identify needed capabilities
            ClientApp->>+Server2: Negotiate features/capabilities
            Server2->>+ServerLLM: Request additional context
            ServerLLM-->>-Server2: Provide context
            Server2-->>-ClientApp: Return available features
            ClientApp->>+Server2: Call negotiated tools
            Server2-->>-ClientApp: Return results
            ClientApp->>+ClientLLM: Process results
            ClientLLM-->>-ClientApp: Generate response
            ClientApp-->>-User: Display final answer
        end
    end
```

## 🔐 الفوائد العملية لـ MCP

إليك الفوائد العملية لاستخدام MCP:

- **الحداثة**: يمكن للنماذج الوصول إلى معلومات محدثة تتجاوز بيانات التدريب الخاصة بها
- **توسيع القدرات**: يمكن للنماذج الاستفادة من أدوات متخصصة للمهام التي لم يتم تدريبها عليها
- **تقليل الهلوسة**: توفر مصادر البيانات الخارجية أساسًا واقعيًا
- **الخصوصية**: يمكن أن تبقى البيانات الحساسة داخل بيئات آمنة بدلاً من تضمينها في المطالبات

## 📌 النقاط الرئيسية

النقاط الرئيسية لاستخدام MCP هي:

- **MCP** يوحد كيفية تفاعل نماذج الذكاء الاصطناعي مع الأدوات والبيانات
- يعزز **الامتداد، الاتساق، والتوافق**
- يساعد MCP في **تقليل وقت التطوير، تحسين الموثوقية، وتوسيع قدرات النموذج**
- بنية العميل-الخادم **تمكن تطبيقات الذكاء الاصطناعي المرنة والقابلة للتوسع**

## 🧠 تمرين

فكر في تطبيق ذكاء اصطناعي ترغب في بنائه.

- ما هي **الأدوات أو البيانات الخارجية** التي يمكن أن تعزز قدراته؟
- كيف يمكن أن يجعل MCP التكامل **أبسط وأكثر موثوقية؟**

## موارد إضافية

- [مستودع MCP على GitHub](https://github.com/modelcontextprotocol)

## ما التالي

التالي: [الفصل الأول: المفاهيم الأساسية](../01-CoreConcepts/README.md)

---

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي. للحصول على معلومات حاسمة، يُوصى بالترجمة البشرية الاحترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة تنشأ عن استخدام هذه الترجمة.