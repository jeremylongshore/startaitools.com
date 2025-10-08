<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T10:54:04+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "ur"
}
-->
# 🚀 10 مائیکروسافٹ MCP سرورز جو ڈویلپر کی پیداواریت کو بدل رہے ہیں

## 🎯 اس رہنما میں آپ کیا سیکھیں گے

یہ عملی رہنما دس مائیکروسافٹ MCP سرورز کو پیش کرتا ہے جو فعال طور پر یہ بدل رہے ہیں کہ ڈویلپرز AI اسسٹنٹس کے ساتھ کیسے کام کرتے ہیں۔ صرف یہ بتانے کے بجائے کہ MCP سرورز *کیا* کر سکتے ہیں، ہم آپ کو ایسے سرورز دکھائیں گے جو مائیکروسافٹ اور اس سے آگے روزمرہ کی ترقیاتی ورک فلو میں حقیقی فرق لا رہے ہیں۔

اس رہنما میں شامل ہر سرور کو حقیقی دنیا کے استعمال اور ڈویلپرز کی رائے کی بنیاد پر منتخب کیا گیا ہے۔ آپ نہ صرف یہ جانیں گے کہ ہر سرور کیا کرتا ہے بلکہ یہ بھی کہ یہ کیوں اہم ہے اور آپ اپنے پروجیکٹس میں اس سے زیادہ سے زیادہ فائدہ کیسے اٹھا سکتے ہیں۔ چاہے آپ MCP میں بالکل نئے ہوں یا اپنے موجودہ سیٹ اپ کو بڑھانا چاہتے ہوں، یہ سرورز مائیکروسافٹ کے ماحولیاتی نظام میں دستیاب سب سے عملی اور مؤثر ٹولز کی نمائندگی کرتے ہیں۔

> **💡 فوری آغاز کا مشورہ**
> 
> MCP میں نئے ہیں؟ پریشان نہ ہوں! یہ رہنما ابتدائی افراد کے لیے آسان بنایا گیا ہے۔ ہم تصورات کو مرحلہ وار سمجھائیں گے، اور آپ ہمیشہ ہمارے [Introduction to MCP](../00-Introduction/README.md) اور [Core Concepts](../01-CoreConcepts/README.md) ماڈیولز کو گہرائی میں سمجھنے کے لیے دیکھ سکتے ہیں۔

## جائزہ

یہ جامع رہنما دس مائیکروسافٹ MCP سرورز کا جائزہ لیتا ہے جو ڈویلپرز کے AI اسسٹنٹس اور بیرونی ٹولز کے ساتھ تعامل کے طریقے کو بدل رہے ہیں۔ Azure ریسورس مینجمنٹ سے لے کر دستاویزات کی پروسیسنگ تک، یہ سرورز Model Context Protocol کی طاقت کو ظاہر کرتے ہیں جو ہموار اور پیداواری ترقیاتی ورک فلو بنانے میں مدد دیتے ہیں۔

## سیکھنے کے مقاصد

اس رہنما کے آخر تک آپ:
- سمجھیں گے کہ MCP سرورز ڈویلپر کی پیداواریت کو کیسے بڑھاتے ہیں
- مائیکروسافٹ کے سب سے مؤثر MCP سرور نفاذات کے بارے میں جانیں گے
- ہر سرور کے عملی استعمال کے کیسز دریافت کریں گے
- VS Code اور Visual Studio میں ان سرورز کو سیٹ اپ اور کنفیگر کرنا سیکھیں گے
- MCP کے وسیع ماحولیاتی نظام اور مستقبل کے رجحانات کو سمجھیں گے

## 🔧 MCP سرورز کو سمجھنا: ابتدائیوں کے لیے رہنما

### MCP سرورز کیا ہیں؟

اگر آپ Model Context Protocol (MCP) میں نئے ہیں، تو آپ سوچ سکتے ہیں: "MCP سرور کیا ہوتا ہے، اور مجھے اس کی پرواہ کیوں کرنی چاہیے؟" آئیے ایک آسان مثال سے شروع کرتے ہیں۔

MCP سرورز کو ایسے خاص اسسٹنٹس سمجھیں جو آپ کے AI کوڈنگ ساتھی (جیسے GitHub Copilot) کو بیرونی ٹولز اور خدمات سے جوڑنے میں مدد دیتے ہیں۔ جیسے آپ اپنے فون پر مختلف کاموں کے لیے مختلف ایپس استعمال کرتے ہیں—ایک موسم کے لیے، ایک نیویگیشن کے لیے، ایک بینکنگ کے لیے—ویسے ہی MCP سرورز آپ کے AI اسسٹنٹ کو مختلف ترقیاتی ٹولز اور خدمات کے ساتھ بات چیت کرنے کی صلاحیت دیتے ہیں۔

### MCP سرورز کون سا مسئلہ حل کرتے ہیں

MCP سرورز سے پہلے، اگر آپ چاہتے تھے کہ:
- اپنے Azure ریسورسز چیک کریں
- GitHub پر مسئلہ بنائیں
- اپنے ڈیٹا بیس سے سوال کریں
- دستاویزات میں تلاش کریں

تو آپ کو کوڈنگ روک کر براؤزر کھولنا پڑتا، متعلقہ ویب سائٹ پر جانا پڑتا، اور یہ کام دستی طور پر کرنا پڑتا۔ یہ بار بار سیاق و سباق بدلنا آپ کے کام کے بہاؤ کو توڑ دیتا اور پیداواریت کم کر دیتا تھا۔

### MCP سرورز آپ کے ترقیاتی تجربے کو کیسے بدلتے ہیں

MCP سرورز کے ساتھ، آپ اپنے ترقیاتی ماحول (VS Code، Visual Studio وغیرہ) میں رہ کر اپنے AI اسسٹنٹ سے یہ کام کروا سکتے ہیں۔ مثال کے طور پر:

**روایتی ورک فلو کی جگہ:**
1. کوڈنگ روکیں
2. براؤزر کھولیں
3. Azure پورٹل پر جائیں
4. اسٹوریج اکاؤنٹ کی تفصیلات دیکھیں
5. VS Code پر واپس آئیں
6. کوڈنگ دوبارہ شروع کریں

**اب آپ یہ کر سکتے ہیں:**
1. AI سے پوچھیں: "میرے Azure اسٹوریج اکاؤنٹس کی حالت کیا ہے؟"
2. فراہم کردہ معلومات کے ساتھ کوڈنگ جاری رکھیں

### ابتدائیوں کے لیے اہم فوائد

#### 1. 🔄 **اپنے بہاؤ کی حالت میں رہیں**
- متعدد ایپلیکیشنز کے درمیان سوئچنگ نہیں
- اپنے لکھے ہوئے کوڈ پر توجہ مرکوز رکھیں
- مختلف ٹولز کو سنبھالنے کی ذہنی بوجھ کم کریں

#### 2. 🤖 **پیچیدہ کمانڈز کی بجائے قدرتی زبان استعمال کریں**
- SQL کی ترکیب یاد رکھنے کی بجائے بتائیں کہ آپ کو کون سا ڈیٹا چاہیے
- Azure CLI کمانڈز یاد رکھنے کی بجائے بتائیں کہ آپ کیا کرنا چاہتے ہیں
- AI تکنیکی تفصیلات سنبھالے جبکہ آپ منطق پر توجہ دیں

#### 3. 🔗 **متعدد ٹولز کو آپس میں جوڑیں**
- مختلف خدمات کو ملا کر طاقتور ورک فلو بنائیں
- مثال: "تمام حالیہ GitHub مسائل حاصل کریں اور ان کے مطابق Azure DevOps ورک آئٹمز بنائیں"
- پیچیدہ اسکرپٹس لکھے بغیر خودکار نظام بنائیں

#### 4. 🌐 **ایک بڑھتا ہوا ماحولیاتی نظام تک رسائی**
- مائیکروسافٹ، GitHub، اور دیگر کمپنیوں کے بنائے ہوئے سرورز سے فائدہ اٹھائیں
- مختلف فراہم کنندگان کے ٹولز کو آسانی سے ملائیں
- ایک معیاری ماحولیاتی نظام کا حصہ بنیں جو مختلف AI اسسٹنٹس کے ساتھ کام کرتا ہے

#### 5. 🛠️ **عملی تجربے سے سیکھیں**
- پہلے سے بنے ہوئے سرورز سے شروع کریں تاکہ تصورات سمجھ سکیں
- جیسے جیسے آپ کو اعتماد آئے، اپنے سرورز بنائیں
- دستیاب SDKs اور دستاویزات سے رہنمائی حاصل کریں

### ابتدائیوں کے لیے حقیقی دنیا کی مثال

فرض کریں آپ ویب ڈویلپمنٹ میں نئے ہیں اور اپنا پہلا پروجیکٹ کر رہے ہیں۔ MCP سرورز آپ کی کیسے مدد کر سکتے ہیں:

**روایتی طریقہ:**
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**MCP سرورز کے ساتھ:**
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### انٹرپرائز اسٹینڈرڈ کا فائدہ

MCP ایک صنعت گیر معیار بنتا جا رہا ہے، جس کا مطلب ہے:
- **یکسانیت**: مختلف ٹولز اور کمپنیوں میں ایک جیسا تجربہ
- **انٹرآپریبلٹی**: مختلف فراہم کنندگان کے سرورز ایک ساتھ کام کرتے ہیں
- **مستقبل کی تیاری**: مہارتیں اور سیٹ اپ مختلف AI اسسٹنٹس کے درمیان منتقل ہو سکتے ہیں
- **کمیونٹی**: وسیع ماحولیاتی نظام جس میں مشترکہ علم اور وسائل موجود ہیں

### شروع کرنے کے لیے: آپ کیا سیکھیں گے

اس رہنما میں، ہم 10 مائیکروسافٹ MCP سرورز کا جائزہ لیں گے جو ہر سطح کے ڈویلپرز کے لیے خاص طور پر مفید ہیں۔ ہر سرور کو اس طرح ڈیزائن کیا گیا ہے کہ:
- عام ترقیاتی چیلنجز حل کرے
- بار بار ہونے والے کاموں کو کم کرے
- کوڈ کی کوالٹی بہتر بنائے
- سیکھنے کے مواقع بڑھائے

> **💡 سیکھنے کا مشورہ**
> 
> اگر آپ MCP میں بالکل نئے ہیں، تو پہلے ہمارے [Introduction to MCP](../00-Introduction/README.md) اور [Core Concepts](../01-CoreConcepts/README.md) ماڈیولز دیکھیں۔ پھر یہاں واپس آ کر مائیکروسافٹ کے حقیقی ٹولز کے ساتھ ان تصورات کو عملی طور پر دیکھیں۔
>
> MCP کی اہمیت کے بارے میں مزید معلومات کے لیے، Maria Naggaga کی پوسٹ دیکھیں: [Connect Once, Integrate Anywhere with MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps).

## VS Code اور Visual Studio میں MCP کے ساتھ شروع کریں 🚀

اگر آپ Visual Studio Code یا Visual Studio 2022 کو GitHub Copilot کے ساتھ استعمال کر رہے ہیں تو ان MCP سرورز کو سیٹ اپ کرنا آسان ہے۔

### VS Code سیٹ اپ

VS Code کے لیے بنیادی عمل یہ ہے:

1. **Agent Mode فعال کریں**: VS Code میں Copilot Chat ونڈو میں Agent موڈ پر سوئچ کریں
2. **MCP سرورز کی ترتیب دیں**: اپنے VS Code کی settings.json فائل میں سرور کی کنفیگریشنز شامل کریں
3. **سرورز شروع کریں**: ہر سرور کے لیے "Start" بٹن پر کلک کریں جسے آپ استعمال کرنا چاہتے ہیں
4. **ٹولز منتخب کریں**: اپنے موجودہ سیشن کے لیے MCP سرورز کو فعال کریں

تفصیلی سیٹ اپ ہدایات کے لیے [VS Code MCP دستاویزات](https://code.visualstudio.com/docs/copilot/copilot-mcp) دیکھیں۔

> **💡 پرو ٹپ: MCP سرورز کو ماہر کی طرح منظم کریں!**
> 
> VS Code Extensions ویو میں اب [MCP سرورز کو منظم کرنے کے لیے ایک نیا آسان UI](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) شامل ہے! آپ کو کسی بھی انسٹال شدہ MCP سرور کو شروع، روکنے اور منظم کرنے کی فوری رسائی ملتی ہے۔ اسے آزما کر دیکھیں!

### Visual Studio 2022 سیٹ اپ

Visual Studio 2022 (ورژن 17.14 یا بعد) کے لیے:

1. **Agent Mode فعال کریں**: GitHub Copilot Chat ونڈو میں "Ask" ڈراپ ڈاؤن پر کلک کریں اور "Agent" منتخب کریں
2. **کنفیگریشن فائل بنائیں**: اپنے سلوشن ڈائریکٹری میں `.mcp.json` فائل بنائیں (تجویز کردہ جگہ: `<SOLUTIONDIR>\.mcp.json`)
3. **سرورز کی ترتیب دیں**: MCP کے معیاری فارمیٹ میں اپنے MCP سرورز کی کنفیگریشن شامل کریں
4. **ٹول کی منظوری دیں**: جب پوچھا جائے، تو مناسب اسکوپ اجازتوں کے ساتھ استعمال کرنے والے ٹولز کی منظوری دیں

تفصیلی Visual Studio سیٹ اپ ہدایات کے لیے [Visual Studio MCP دستاویزات](https://learn.microsoft.com/visualstudio/ide/mcp-servers) دیکھیں۔

ہر MCP سرور کی اپنی کنفیگریشن کی ضروریات ہوتی ہیں (کنکشن سٹرنگز، توثیق وغیرہ)، لیکن دونوں IDEs میں سیٹ اپ کا طریقہ کار یکساں ہے۔

## مائیکروسافٹ MCP سرورز سے سیکھی گئی باتیں 🛠️

### 1. 📚 Microsoft Learn Docs MCP Server

[![VS Code میں انسٹال کریں](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![VS Code Insiders میں انسٹال کریں](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**یہ کیا کرتا ہے**: Microsoft Learn Docs MCP Server ایک کلاؤڈ ہوسٹڈ سروس ہے جو AI اسسٹنٹس کو Model Context Protocol کے ذریعے مائیکروسافٹ کی سرکاری دستاویزات تک حقیقی وقت میں رسائی فراہم کرتی ہے۔ یہ `https://learn.microsoft.com/api/mcp` سے جڑتا ہے اور Microsoft Learn، Azure دستاویزات، Microsoft 365 دستاویزات، اور دیگر سرکاری مائیکروسافٹ ذرائع میں معنوی تلاش کو فعال کرتا ہے۔

**یہ کیوں مفید ہے**: اگرچہ یہ صرف "دستاویزات" لگتا ہے، یہ سرور ہر مائیکروسافٹ ٹیکنالوجی استعمال کرنے والے ڈویلپر کے لیے انتہائی اہم ہے۔ .NET ڈویلپرز کی سب سے بڑی شکایت AI کوڈنگ اسسٹنٹس کے بارے میں یہ ہے کہ وہ تازہ ترین .NET اور C# ریلیزز سے اپ ٹو ڈیٹ نہیں ہوتے۔ Microsoft Learn Docs MCP Server اس مسئلے کو حل کرتا ہے کیونکہ یہ تازہ ترین دستاویزات، API حوالہ جات، اور بہترین طریقوں تک حقیقی وقت میں رسائی فراہم کرتا ہے۔ چاہے آپ تازہ ترین Azure SDKs کے ساتھ کام کر رہے ہوں، C# 13 کی نئی خصوصیات دریافت کر رہے ہوں، یا جدید .NET Aspire پیٹرنز نافذ کر رہے ہوں، یہ سرور یقینی بناتا ہے کہ آپ کا AI اسسٹنٹ مستند، جدید معلومات تک رسائی رکھتا ہے تاکہ درست اور جدید کوڈ تیار کر سکے۔

**حقیقی دنیا میں استعمال**: "Microsoft Learn کی سرکاری دستاویزات کے مطابق Azure container app بنانے کے لیے az cli کمانڈز کیا ہیں؟" یا "ASP.NET Core میں Entity Framework کو dependency injection کے ساتھ کیسے کنفیگر کیا جائے؟" یا "اس کوڈ کا جائزہ لیں کہ یہ Microsoft Learn Documentation میں کارکردگی کی سفارشات سے میل کھاتا ہے یا نہیں۔" یہ سرور Microsoft Learn، Azure docs، اور Microsoft 365 دستاویزات میں معنوی تلاش کے ذریعے سب سے زیادہ متعلقہ معلومات فراہم کرتا ہے۔ یہ 10 اعلی معیار کے مواد کے ٹکڑے آرٹیکل کے عنوانات اور URLs کے ساتھ واپس کرتا ہے، ہمیشہ تازہ ترین مائیکروسافٹ دستاویزات تک رسائی حاصل کرتا ہے۔

**نمایاں مثال**: یہ سرور `microsoft_docs_search` ٹول فراہم کرتا ہے جو مائیکروسافٹ کی سرکاری تکنیکی دستاویزات کے خلاف معنوی تلاش کرتا ہے۔ ایک بار کنفیگر ہونے کے بعد، آپ سوالات پوچھ سکتے ہیں جیسے "ASP.NET Core میں JWT authentication کیسے نافذ کی جائے؟" اور تفصیلی، سرکاری جوابات حاصل کر سکتے ہیں جن کے ساتھ ماخذ کے لنکس بھی ہوتے ہیں۔ تلاش کا معیار بہترین ہے کیونکہ یہ سیاق و سباق کو سمجھتا ہے – Azure کے تناظر میں "containers" کے بارے میں پوچھنے پر Azure Container Instances کی دستاویزات ملتی ہیں، جبکہ .NET کے تناظر میں یہی اصطلاح C# collection کی متعلقہ معلومات دیتی ہے۔

یہ خاص طور پر تیزی سے بدلنے والی یا حال ہی میں اپ ڈیٹ کی گئی لائبریریوں اور استعمال کے کیسز کے لیے مفید ہے۔ مثال کے طور پر، حالیہ کوڈنگ پروجیکٹس میں میں نے .NET Aspire اور Microsoft.Extensions.AI کی تازہ ترین ریلیزز کی خصوصیات استعمال کرنا چاہیں۔ Microsoft Learn Docs MCP سرور شامل کرنے سے میں نے نہ صرف API دستاویزات بلکہ حال ہی میں شائع شدہ واک تھروز اور رہنمائی بھی حاصل کی۔
> **💡 پرو ٹپ**
> 
> یہاں تک کہ ٹول کے لیے موزوں ماڈلز کو بھی MCP ٹولز استعمال کرنے کی ترغیب کی ضرورت ہوتی ہے! آپ ایک سسٹم پرامپٹ یا [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) شامل کرنے پر غور کریں، جیسے: "آپ کو `microsoft.docs.mcp` تک رسائی حاصل ہے – اس ٹول کو استعمال کریں تاکہ Microsoft کی تازہ ترین سرکاری دستاویزات میں C#، Azure، ASP.NET Core، یا Entity Framework جیسے Microsoft ٹیکنالوجیز کے سوالات کے جواب تلاش کیے جا سکیں۔"
>
> اس کی عملی مثال کے لیے، Awesome GitHub Copilot ریپوزیٹری میں موجود [C# .NET Janitor چیٹ موڈ](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) دیکھیں۔ یہ موڈ خاص طور پر Microsoft Learn Docs MCP سرور کا استعمال کرتا ہے تاکہ جدید ترین پیٹرنز اور بہترین طریقوں کے ذریعے C# کوڈ کو صاف اور جدید بنایا جا سکے۔
### 2. ☁️ Azure MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**یہ کیا کرتا ہے**: Azure MCP Server ایک مکمل مجموعہ ہے جس میں 15 سے زائد مخصوص Azure سروس کنیکٹرز شامل ہیں جو پورے Azure ماحولیاتی نظام کو آپ کے AI ورک فلو میں لاتے ہیں۔ یہ صرف ایک سرور نہیں بلکہ ایک طاقتور مجموعہ ہے جس میں resource management، database connectivity (PostgreSQL, SQL Server)، Azure Monitor لاگ تجزیہ KQL کے ساتھ، Cosmos DB انٹیگریشن، اور بہت کچھ شامل ہے۔

**یہ کیوں مفید ہے**: Azure وسائل کے انتظام سے آگے، یہ سرور Azure SDKs کے ساتھ کام کرتے ہوئے کوڈ کی کوالٹی کو نمایاں طور پر بہتر بناتا ہے۔ جب آپ Azure MCP کو Agent موڈ میں استعمال کرتے ہیں، تو یہ صرف کوڈ لکھنے میں مدد نہیں دیتا بلکہ *بہتر* Azure کوڈ لکھنے میں مدد دیتا ہے جو موجودہ authentication پیٹرنز، error handling کی بہترین مشقوں، اور جدید SDK خصوصیات کو اپناتا ہے۔ آپ کو generic کوڈ نہیں ملتا جو شاید کام کرے، بلکہ وہ کوڈ ملتا ہے جو Azure کی تجویز کردہ production workloads کے پیٹرنز کی پیروی کرتا ہے۔

**اہم ماڈیولز شامل ہیں**:
- **🗄️ Database Connectors**: Azure Database for PostgreSQL اور SQL Server تک براہ راست قدرتی زبان میں رسائی
- **📊 Azure Monitor**: KQL سے چلنے والا لاگ تجزیہ اور آپریشنل بصیرت
- **🌐 Resource Management**: مکمل Azure resource lifecycle کا انتظام
- **🔐 Authentication**: DefaultAzureCredential اور managed identity پیٹرنز
- **📦 Storage Services**: Blob Storage، Queue Storage، اور Table Storage آپریشنز
- **🚀 Container Services**: Azure Container Apps، Container Instances، اور AKS کا انتظام
- **اور بہت سے مخصوص کنیکٹرز**

**حقیقی دنیا میں استعمال**: "میرے Azure storage accounts کی فہرست دکھائیں"، "میرے Log Analytics workspace میں پچھلے ایک گھنٹے کی غلطیوں کی تلاش کریں"، یا "Node.js کے ساتھ صحیح authentication کے ذریعے Azure ایپلیکیشن بنانے میں مدد کریں"

**مکمل ڈیمو منظرنامہ**: یہاں ایک مکمل واک تھرو ہے جو دکھاتا ہے کہ Azure MCP کو GitHub Copilot for Azure ایکسٹینشن کے ساتھ VS Code میں ملانے کی طاقت کیا ہے۔ جب آپ دونوں انسٹال کر لیتے ہیں اور پرامپٹ دیتے ہیں:

> "ایک Python اسکرپٹ بنائیں جو DefaultAzureCredential authentication استعمال کرتے ہوئے Azure Blob Storage میں فائل اپلوڈ کرے۔ اسکرپٹ کو میرے Azure storage اکاؤنٹ 'mycompanystorage' سے کنیکٹ ہونا چاہیے، 'documents' نامی container میں اپلوڈ کرنا چاہیے، موجودہ timestamp کے ساتھ ایک ٹیسٹ فائل بنانی چاہیے، errors کو مؤثر طریقے سے ہینڈل کرنا چاہیے اور معلوماتی آؤٹ پٹ دینا چاہیے، Azure کی authentication اور error handling کی بہترین مشقوں کی پیروی کرنی چاہیے، اور DefaultAzureCredential authentication کے کام کرنے کے طریقہ کار کی وضاحت کرنے والے تبصرے شامل ہونے چاہئیں، نیز اسکرپٹ کو مناسب فنکشنز اور دستاویزات کے ساتھ اچھی طرح منظم کرنا چاہیے۔"

Azure MCP Server ایک مکمل، production-ready Python اسکرپٹ تیار کرے گا جو:
- جدید Azure Blob Storage SDK کو async پیٹرنز کے ساتھ استعمال کرتا ہے
- DefaultAzureCredential کو مکمل fallback چین کی وضاحت کے ساتھ نافذ کرتا ہے
- مخصوص Azure exception اقسام کے ساتھ مضبوط error handling شامل کرتا ہے
- resource management اور connection handling کے لیے Azure SDK کی بہترین مشقوں کی پیروی کرتا ہے
- تفصیلی لاگنگ اور معلوماتی کنسول آؤٹ پٹ فراہم کرتا ہے
- فنکشنز، دستاویزات، اور ٹائپ ہنٹس کے ساتھ مناسب ساخت والا اسکرپٹ بناتا ہے

یہ خاص بات ہے کہ Azure MCP کے بغیر آپ کو generic blob storage کوڈ مل سکتا ہے جو کام کرتا ہے لیکن موجودہ Azure پیٹرنز کی پیروی نہیں کرتا۔ Azure MCP کے ساتھ، آپ کو ایسا کوڈ ملتا ہے جو جدید authentication طریقے استعمال کرتا ہے، Azure مخصوص error scenarios کو ہینڈل کرتا ہے، اور Microsoft کی تجویز کردہ production ایپلیکیشنز کی مشقوں کی پیروی کرتا ہے۔

**نمایاں مثال**: مجھے `az` اور `azd` CLI کمانڈز یاد رکھنے میں مشکل ہوتی ہے جب فوری استعمال کی بات آتی ہے۔ میرے لیے ہمیشہ دو قدم کا عمل ہوتا ہے: پہلے syntax دیکھنا، پھر کمانڈ چلانا۔ میں اکثر پورٹل میں جا کر کام کر لیتا ہوں کیونکہ مجھے تسلیم نہیں کرنا ہوتا کہ CLI syntax یاد نہیں۔ بس یہ بیان کرنا کہ مجھے کیا چاہیے، حیرت انگیز ہے، اور اس سے بھی بہتر یہ کہ میں یہ سب اپنے IDE کو چھوڑے بغیر کر سکتا ہوں!

شروع کرنے کے لیے [Azure MCP repository](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) میں استعمال کے بہت سے کیسز کی فہرست موجود ہے۔ مکمل سیٹ اپ گائیڈز اور جدید کنفیگریشن آپشنز کے لیے [سرکاری Azure MCP دستاویزات](https://learn.microsoft.com/azure/developer/azure-mcp-server/) دیکھیں۔

### 3. 🐙 GitHub MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**یہ کیا کرتا ہے**: سرکاری GitHub MCP Server GitHub کے پورے ماحولیاتی نظام کے ساتھ بے جوڑ انٹیگریشن فراہم کرتا ہے، جس میں ہوسٹڈ ریموٹ رسائی اور لوکل Docker ڈپلائمنٹ کے آپشنز شامل ہیں۔ یہ صرف بنیادی repository آپریشنز تک محدود نہیں بلکہ ایک مکمل ٹول کٹ ہے جس میں GitHub Actions کا انتظام، pull request ورک فلو، issue ٹریکنگ، سیکیورٹی اسکیننگ، نوٹیفیکیشنز، اور جدید آٹومیشن صلاحیتیں شامل ہیں۔

**یہ کیوں مفید ہے**: یہ سرور GitHub کے ساتھ آپ کے تعامل کو بدل دیتا ہے کیونکہ پورا پلیٹ فارم تجربہ آپ کے ڈیولپمنٹ ماحول میں براہ راست آ جاتا ہے۔ VS Code اور GitHub.com کے درمیان بار بار سوئچ کرنے کی بجائے، آپ قدرتی زبان کے کمانڈز کے ذریعے سب کچھ سنبھال سکتے ہیں اور اپنے کوڈ پر توجہ مرکوز رکھ سکتے ہیں۔

> **ℹ️ Note: مختلف قسم کے 'Agents'**
> 
> اس GitHub MCP Server کو GitHub کے Coding Agent (وہ AI ایجنٹ جسے آپ issues کو خودکار کوڈنگ کے لیے تفویض کر سکتے ہیں) سے مت بھولیں۔ GitHub MCP Server VS Code کے Agent موڈ میں GitHub API انٹیگریشن فراہم کرتا ہے، جبکہ GitHub کا Coding Agent ایک الگ فیچر ہے جو GitHub issues کو تفویض کیے جانے پر pull requests بناتا ہے۔

**اہم صلاحیتیں شامل ہیں**:
- **⚙️ GitHub Actions**: مکمل CI/CD پائپ لائن مینجمنٹ، ورک فلو مانیٹرنگ، اور artifact ہینڈلنگ
- **🔀 Pull Requests**: PRs بنانا، جائزہ لینا، مرج کرنا، اور مکمل status ٹریکنگ کے ساتھ انتظام کرنا
- **🐛 Issues**: مکمل issue lifecycle مینجمنٹ، تبصرہ، لیبلنگ، اور تفویض
- **🔒 Security**: کوڈ اسکیننگ الرٹس، سیکریٹ ڈیٹیکشن، اور Dependabot انٹیگریشن
- **🔔 Notifications**: ذہین نوٹیفیکیشن مینجمنٹ اور repository سبسکرپشن کنٹرول
- **📁 Repository Management**: فائل آپریشنز، برانچ مینجمنٹ، اور repository انتظام
- **👥 Collaboration**: یوزر اور آرگنائزیشن سرچ، ٹیم مینجمنٹ، اور رسائی کنٹرول

**حقیقی دنیا میں استعمال**: "میرے feature برانچ سے pull request بنائیں"، "اس ہفتے کی تمام ناکام CI رنز دکھائیں"، "میرے repositories کے لیے کھلے سیکیورٹی الرٹس کی فہرست دکھائیں"، یا "میرے تمام آرگنائزیشنز میں میرے تفویض شدہ issues تلاش کریں"

**مکمل ڈیمو منظرنامہ**: یہاں ایک طاقتور ورک فلو ہے جو GitHub MCP Server کی صلاحیتوں کو ظاہر کرتا ہے:

> "مجھے ہمارے sprint review کی تیاری کرنی ہے۔ اس ہفتے میں نے جو تمام pull requests بنائی ہیں دکھائیں، ہمارے CI/CD پائپ لائنز کی حالت چیک کریں، کسی بھی سیکیورٹی الرٹس کا خلاصہ بنائیں جنہیں حل کرنا ضروری ہے، اور merged PRs جن پر 'feature' لیبل لگا ہو ان کی بنیاد پر release notes تیار کرنے میں مدد کریں۔"

GitHub MCP Server یہ کرے گا:
- آپ کی حالیہ pull requests کی تفصیلی status معلومات کے ساتھ کوئری کرے گا
- ورک فلو رنز کا تجزیہ کرے گا اور کسی بھی ناکامی یا کارکردگی کے مسائل کو نمایاں کرے گا
- سیکیورٹی اسکیننگ کے نتائج مرتب کرے گا اور اہم الرٹس کو ترجیح دے گا
- merged PRs سے معلومات نکال کر مکمل release notes تیار کرے گا
- sprint planning اور release کی تیاری کے لیے قابل عمل اگلے اقدامات فراہم کرے گا

**نمایاں مثال**: میں کوڈ ریویو ورک فلو کے لیے اسے استعمال کرنا پسند کرتا ہوں۔ VS Code، GitHub نوٹیفیکیشنز، اور pull request صفحات کے درمیان چھلانگ لگانے کی بجائے، میں کہہ سکتا ہوں "میرے جائزے کے انتظار میں تمام PRs دکھائیں" اور پھر "PR #123 میں authentication طریقہ کار میں error handling کے بارے میں تبصرہ شامل کریں۔" سرور GitHub API کالز کو ہینڈل کرتا ہے، گفتگو کا سیاق و سباق برقرار رکھتا ہے، اور مجھے زیادہ تعمیری ریویو تبصرے بنانے میں مدد دیتا ہے۔

**Authentication کے اختیارات**: سرور OAuth (VS Code میں seamless) اور Personal Access Tokens دونوں کو سپورٹ کرتا ہے، اور آپ صرف وہی GitHub فنکشنالٹی فعال کر سکتے ہیں جو آپ کو چاہیے۔ آپ اسے فوری سیٹ اپ کے لیے ریموٹ ہوسٹڈ سروس کے طور پر چلا سکتے ہیں یا مکمل کنٹرول کے لیے لوکل Docker کے ذریعے۔

> **💡 Pro Tip**
> 
> MCP سرور کی سیٹنگز میں `--toolsets` پیرامیٹر کو کنفیگر کر کے صرف وہ ٹول سیٹس فعال کریں جو آپ کو چاہیے تاکہ context size کم ہو اور AI ٹول کے انتخاب میں بہتری آئے۔ مثال کے طور پر، بنیادی ڈیولپمنٹ ورک فلو کے لیے `"--toolsets", "repos,issues,pull_requests,actions"` شامل کریں، یا اگر آپ بنیادی طور پر GitHub مانیٹرنگ چاہتے ہیں تو `"--toolsets", "notifications, security"` استعمال کریں۔

### 4. 🔄 Azure DevOps MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_DevOps_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_DevOps_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/azure-devops-mcp)

**یہ کیا کرتا ہے**: Azure DevOps خدمات سے جڑتا ہے تاکہ مکمل پروجیکٹ مینجمنٹ، ورک آئٹم ٹریکنگ، build pipeline مینجمنٹ، اور repository آپریشنز فراہم کرے۔

**یہ کیوں مفید ہے**: جو ٹیمیں Azure DevOps کو اپنے بنیادی DevOps پلیٹ فارم کے طور پر استعمال کرتی ہیں، یہ MCP سرور آپ کے ڈیولپمنٹ ماحول اور Azure DevOps ویب انٹرفیس کے درمیان بار بار ٹیب سوئچنگ کو ختم کر دیتا ہے۔ آپ ورک آئٹمز کا انتظام کر سکتے ہیں، build کی حالت چیک کر سکتے ہیں، repositories کو کوئری کر سکتے ہیں، اور پروجیکٹ مینجمنٹ کے کام براہ راست اپنے AI اسسٹنٹ سے کر سکتے ہیں۔

**حقیقی دنیا میں استعمال**: "WebApp پروجیکٹ کے موجودہ sprint میں تمام فعال ورک آئٹمز دکھائیں"، "میں نے جو لاگ ان مسئلہ پایا ہے اس کے لیے bug رپورٹ بنائیں"، یا "ہمارے build pipelines کی حالت چیک کریں اور حالیہ ناکامیوں کو دکھائیں"

**نمایاں مثال**: آپ آسانی سے اپنی ٹیم کے موجودہ sprint کی حالت چیک کر سکتے ہیں جیسے "WebApp پروجیکٹ کے موجودہ sprint میں تمام فعال ورک آئٹمز دکھائیں" یا "میں نے جو لاگ ان مسئلہ پایا ہے اس کے لیے bug رپورٹ بنائیں" بغیر اپنے ڈیولپمنٹ ماحول کو چھوڑے۔

### 5. 📝 MarkItDown MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**یہ کیا کرتا ہے**: MarkItDown ایک جامع دستاویزات کنورژن سرور ہے جو مختلف فائل فارمیٹس کو اعلیٰ معیار کے Markdown میں تبدیل کرتا ہے، جو LLM کے استعمال اور متن کے تجزیے کے ورک فلو کے لیے بہتر بنایا گیا ہے۔

**یہ کیوں مفید ہے**: جدید دستاویزات کے ورک فلو کے لیے ضروری! MarkItDown مختلف فائل فارمیٹس کو سنبھالتا ہے اور اہم دستاویزاتی ساخت جیسے کہ ہیڈنگز، فہرستیں، جدولیں، اور لنکس کو برقرار رکھتا ہے۔ سادہ متن نکالنے والے ٹولز کے برعکس، یہ معنوی مفہوم اور فارمیٹنگ کو برقرار رکھنے پر توجہ دیتا ہے جو AI پروسیسنگ اور انسانی پڑھنے کے لیے قیمتی ہے۔

**مقبول فائل فارمیٹس**:
- **آفس دستاویزات**: PDF، PowerPoint (PPTX)، Word (DOCX)، Excel (XLSX/XLS)
- **میڈیا فائلز**: تصاویر (EXIF میٹا ڈیٹا اور OCR کے ساتھ)، آڈیو (EXIF میٹا ڈیٹا اور تقریر کی تحریر کے ساتھ)
- **ویب مواد**: HTML، RSS فیڈز، YouTube URLs، ویکیپیڈیا صفحات
- **ڈیٹا فارمیٹس**: CSV، JSON، XML، ZIP فائلز (مواد کو recursive طریقے سے پروسیس کرتا ہے)
- **پبلشنگ فارمیٹس**: EPub، Jupyter نوٹ بکس (.ipynb)
- **ای میل**: Outlook پیغامات (.msg)
- **جدید**: Azure Document Intelligence انٹیگریشن برائے بہتر PDF پروسیسنگ

**جدید صلاحیتیں**: MarkItDown LLM کی مدد سے تصاویر کی وضاحتیں فراہم کرتا ہے (جب OpenAI کلائنٹ مہیا ہو)، Azure Document Intelligence کے ذریعے PDF پروسیسنگ کو بہتر بناتا ہے، تقریر کے مواد کے لیے آڈیو ٹرانسکرپشن کرتا ہے، اور اضافی فائل فارمیٹس کے لیے پلگ ان سسٹم فراہم کرتا ہے۔

**حقیقی دنیا میں استعمال**: "اس PowerPoint پریزنٹیشن کو Markdown میں تبدیل کریں تاکہ ہماری دستاویزات کی سائٹ کے لیے استعمال ہو"، "اس PDF سے متن نکالیں جس میں مناسب ہیڈنگ سٹرکچر ہو"، یا "اس Excel اسپریڈشیٹ کو پڑھنے کے قابل جدول کی شکل میں تبدیل کریں"

**نمایاں مثال**: [MarkItDown docs](https://github.com/microsoft/markitdown#why-markdown) سے اقتباس:


> Markdown سادہ متن کے بہت قریب ہے، جس میں کم سے کم مارک اپ یا فارمیٹنگ ہوتی ہے، لیکن پھر بھی اہم دستاویزاتی ساخت کو ظاہر کرنے کا طریقہ فراہم کرتا ہے۔ معروف LLMs، جیسے OpenAI کا GPT-4o، فطری طور پر Markdown "بولتے" ہیں، اور اکثر بغیر پوچھے اپنے جوابات میں Markdown شامل کرتے ہیں۔ اس سے ظاہر ہوتا ہے کہ انہیں بڑی مقدار میں Markdown فارمیٹ شدہ متن پر تربیت دی گئی ہے اور وہ اسے اچھی طرح سمجھتے ہیں۔ اضافی فائدے کے طور پر، Markdown کنونشنز ٹوکن کی بچت میں بھی بہت مؤثر ہیں۔

MarkItDown دستاویز کی ساخت کو برقرار رکھنے میں واقعی ماہر ہے، جو AI ورک فلو کے لیے بہت اہم ہے۔ مثال کے طور پر، جب PowerPoint پریزنٹیشن کو تبدیل کیا جاتا ہے، تو یہ سلائیڈ کی تنظیم کو درست ہیڈنگز کے ساتھ رکھتا ہے، جدولوں کو Markdown جدولوں کی صورت میں نکالتا ہے، تصاویر کے لیے alt ٹیکسٹ شامل کرتا ہے، اور اسپیکر نوٹس کو بھی پروسیس کرتا ہے۔ چارٹس کو پڑھنے کے قابل ڈیٹا جدولوں میں تبدیل کیا جاتا ہے، اور نتیجے میں بننے والا Markdown اصل پریزنٹیشن کے منطقی بہاؤ کو برقرار رکھتا ہے۔ یہ پریزنٹیشن کے مواد کو AI سسٹمز میں فیڈ کرنے یا موجودہ سلائیڈز سے دستاویزات بنانے کے لیے بہترین بناتا ہے۔
### 6. 🗃️ SQL Server MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**یہ کیا کرتا ہے**: SQL Server ڈیٹا بیسز (آن-پرمیسس، Azure SQL، یا Fabric) تک بات چیت کی رسائی فراہم کرتا ہے۔

**یہ کیوں مفید ہے**: PostgreSQL سرور کی طرح لیکن Microsoft SQL کے ماحولیاتی نظام کے لیے۔ ایک سادہ کنکشن سٹرنگ کے ذریعے جڑیں اور قدرتی زبان میں سوالات کرنا شروع کریں – اب مزید سیاق و سباق بدلنے کی ضرورت نہیں!

**حقیقی دنیا میں استعمال**: "پچھلے 30 دنوں میں جو تمام آرڈرز مکمل نہیں ہوئے ہیں انہیں تلاش کریں" کو مناسب SQL سوالات میں تبدیل کرتا ہے اور فارمیٹ شدہ نتائج واپس کرتا ہے۔

**نمایاں مثال**: ایک بار جب آپ اپنا ڈیٹا بیس کنکشن سیٹ کر لیتے ہیں، تو آپ فوراً اپنے ڈیٹا کے ساتھ بات چیت شروع کر سکتے ہیں۔ بلاگ پوسٹ میں ایک سادہ سوال کے ذریعے یہ دکھایا گیا ہے: "آپ کس ڈیٹا بیس سے جڑے ہیں؟" MCP سرور مناسب ڈیٹا بیس ٹول کو کال کرتا ہے، آپ کے SQL Server انسٹینس سے جڑتا ہے، اور آپ کے موجودہ ڈیٹا بیس کنکشن کی تفصیلات واپس کرتا ہے – وہ بھی ایک لائن SQL لکھے بغیر۔ سرور مکمل ڈیٹا بیس آپریشنز کو سپورٹ کرتا ہے، جیسے اسکیمہ مینجمنٹ سے لے کر ڈیٹا مینپولیشن تک، سب قدرتی زبان کے پرامپٹس کے ذریعے۔ مکمل سیٹ اپ ہدایات اور VS Code اور Claude Desktop کے ساتھ کنفیگریشن کی مثالوں کے لیے دیکھیں: [Introducing MSSQL MCP Server (Preview)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/)۔

### 7. 🎭 Playwright MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**یہ کیا کرتا ہے**: AI ایجنٹس کو ویب صفحات کے ساتھ تعامل کرنے کے قابل بناتا ہے تاکہ ٹیسٹنگ اور آٹومیشن کی جا سکے۔

> **ℹ️ GitHub Copilot کو طاقت دیتا ہے**
> 
> Playwright MCP Server GitHub Copilot کے Coding Agent کو ویب براؤزنگ کی صلاحیتیں دیتا ہے! [اس فیچر کے بارے میں مزید جانیں](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/)۔

**یہ کیوں مفید ہے**: قدرتی زبان کی وضاحتوں سے چلنے والی خودکار ٹیسٹنگ کے لیے بہترین۔ AI ویب سائٹس پر نیویگیٹ کر سکتا ہے، فارم بھر سکتا ہے، اور ساختی accessibility snapshots کے ذریعے ڈیٹا نکال سکتا ہے – یہ بہت طاقتور چیز ہے!

**حقیقی دنیا میں استعمال**: "لاگ ان فلو کی جانچ کریں اور تصدیق کریں کہ ڈیش بورڈ صحیح طریقے سے لوڈ ہو رہا ہے" یا "ایسا ٹیسٹ بنائیں جو مصنوعات تلاش کرے اور نتائج کے صفحے کی تصدیق کرے" – وہ بھی ایپلیکیشن کے سورس کوڈ کی ضرورت کے بغیر۔

**نمایاں مثال**: میری ساتھی Debbie O'Brien نے حال ہی میں Playwright MCP Server کے ساتھ شاندار کام کیا ہے! مثال کے طور پر، اس نے دکھایا کہ آپ بغیر ایپلیکیشن کے سورس کوڈ تک رسائی کے مکمل Playwright ٹیسٹ کیسے بنا سکتے ہیں۔ اس کے منظر نامے میں، اس نے Copilot سے کہا کہ ایک فلم تلاش کرنے والی ایپ کے لیے ٹیسٹ بنائے: سائٹ پر جائیں، "Garfield" تلاش کریں، اور تصدیق کریں کہ فلم نتائج میں ظاہر ہو رہی ہے۔ MCP نے براؤزر سیشن شروع کیا، DOM snapshots کے ذریعے صفحے کی ساخت کو سمجھا، درست سلیکٹرز معلوم کیے، اور ایک مکمل کام کرنے والا TypeScript ٹیسٹ تیار کیا جو پہلی کوشش میں کامیاب رہا۔

اس کی طاقت اس بات میں ہے کہ یہ قدرتی زبان کی ہدایات اور قابل عمل ٹیسٹ کوڈ کے درمیان پل کا کام کرتا ہے۔ روایتی طریقے یا تو دستی ٹیسٹ لکھنے کی ضرورت رکھتے ہیں یا کوڈ بیس تک رسائی۔ لیکن Playwright MCP کے ساتھ، آپ بیرونی سائٹس، کلائنٹ ایپلیکیشنز، یا بلیک باکس ٹیسٹنگ کے منظرناموں میں جہاں کوڈ تک رسائی نہیں ہے، ٹیسٹ کر سکتے ہیں۔

### 8. 💻 Dev Box MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**یہ کیا کرتا ہے**: Microsoft Dev Box ماحولیات کو قدرتی زبان کے ذریعے منظم کرتا ہے۔

**یہ کیوں مفید ہے**: ترقیاتی ماحول کے انتظام کو بہت آسان بناتا ہے! مخصوص کمانڈز یاد رکھے بغیر ترقیاتی ماحول بنائیں، ترتیب دیں، اور سنبھالیں۔

**حقیقی دنیا میں استعمال**: "نیا Dev Box سیٹ اپ کریں جس میں تازہ ترین .NET SDK ہو اور اسے ہمارے پروجیکٹ کے لیے ترتیب دیں"، "میرے تمام ترقیاتی ماحول کی حالت چیک کریں"، یا "ہماری ٹیم کی پریزنٹیشنز کے لیے ایک معیاری ڈیمو ماحول بنائیں"۔

**نمایاں مثال**: میں ذاتی ترقی کے لیے Dev Box استعمال کرنے کا بڑا مداح ہوں۔ میرا وہ لمحہ جب جیمز مونٹیمگن نے بتایا کہ Dev Box کانفرنس ڈیموز کے لیے کتنا زبردست ہے، کیونکہ اس میں تیز ترین ایتھرنیٹ کنکشن ہوتا ہے چاہے کانفرنس، ہوٹل، یا ہوائی جہاز کا وائی فائی ہو۔ حقیقت میں، میں نے حال ہی میں ایک بس میں Bruges سے Antwerp جاتے ہوئے اپنے فون ہاٹ سپاٹ سے جڑا ہوا لیپ ٹاپ استعمال کرتے ہوئے کانفرنس ڈیمو کی مشق کی! میرا اگلا قدم ٹیم کے متعدد ترقیاتی ماحول اور معیاری ڈیمو ماحول کو منظم کرنا ہے۔ اور ایک اور بڑا استعمال جو میں نے صارفین اور ساتھیوں سے سنا ہے، وہ ہے Dev Box کو پہلے سے ترتیب شدہ ترقیاتی ماحول کے طور پر استعمال کرنا۔ دونوں صورتوں میں، MCP کے ذریعے Dev Boxes کو ترتیب دینا اور منظم کرنا قدرتی زبان کے تعامل کو ممکن بناتا ہے، اور آپ اپنے ترقیاتی ماحول میں ہی رہتے ہیں۔

### 9. 🤖 Azure AI Foundry MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**یہ کیا کرتا ہے**: Azure AI Foundry MCP Server ڈویلپرز کو Azure کے AI ماحولیاتی نظام تک مکمل رسائی فراہم کرتا ہے، جس میں ماڈل کیٹلاگز، تعیناتی کا انتظام، Azure AI Search کے ذریعے علم کی انڈیکسنگ، اور تشخیصی اوزار شامل ہیں۔ یہ تجرباتی سرور AI کی ترقی اور Azure کی طاقتور AI انفراسٹرکچر کے درمیان پل کا کام کرتا ہے، جس سے AI ایپلیکیشنز کی تعمیر، تعیناتی، اور تشخیص آسان ہو جاتی ہے۔

**یہ کیوں مفید ہے**: یہ سرور Azure AI خدمات کے ساتھ آپ کے کام کرنے کے طریقے کو بدل دیتا ہے کیونکہ یہ انٹرپرائز گریڈ AI صلاحیتوں کو براہ راست آپ کے ترقیاتی ورک فلو میں لاتا ہے۔ Azure پورٹل، دستاویزات، اور آپ کے IDE کے درمیان بار بار سوئچ کرنے کی بجائے، آپ ماڈلز دریافت کر سکتے ہیں، خدمات تعینات کر سکتے ہیں، علم کے ذخائر کا انتظام کر سکتے ہیں، اور قدرتی زبان کے کمانڈز کے ذریعے AI کی کارکردگی کا جائزہ لے سکتے ہیں۔ یہ خاص طور پر ان ڈویلپرز کے لیے طاقتور ہے جو RAG (Retrieval-Augmented Generation) ایپلیکیشنز بنا رہے ہیں، کثیر ماڈل تعیناتیوں کا انتظام کر رہے ہیں، یا جامع AI تشخیصی پائپ لائنز نافذ کر رہے ہیں۔

**اہم ڈویلپر صلاحیتیں**:
- **🔍 ماڈل کی دریافت اور تعیناتی**: Azure AI Foundry کے ماڈل کیٹلاگ کو دریافت کریں، کوڈ نمونوں کے ساتھ تفصیلی ماڈل معلومات حاصل کریں، اور ماڈلز کو Azure AI Services پر تعینات کریں
- **📚 علم کا انتظام**: Azure AI Search انڈیکسز بنائیں اور ان کا انتظام کریں، دستاویزات شامل کریں، انڈیکسرز کو ترتیب دیں، اور پیچیدہ RAG سسٹمز تیار کریں
- **⚡ AI ایجنٹ انضمام**: Azure AI Agents سے جڑیں، موجودہ ایجنٹس سے سوال کریں، اور پیداوار کے منظرناموں میں ایجنٹ کی کارکردگی کا جائزہ لیں
- **📊 تشخیصی فریم ورک**: جامع متن اور ایجنٹ تشخیصات چلائیں، مارک ڈاؤن رپورٹس تیار کریں، اور AI ایپلیکیشنز کے لیے معیار کی یقین دہانی نافذ کریں
- **🚀 پروٹوٹائپنگ کے اوزار**: GitHub پر مبنی پروٹوٹائپنگ کے لیے سیٹ اپ ہدایات حاصل کریں اور Azure AI Foundry Labs تک رسائی حاصل کریں جہاں جدید تحقیقاتی ماڈلز دستیاب ہیں

**حقیقی دنیا میں ڈویلپر کا استعمال**: "اپنی ایپلیکیشن کے لیے Phi-4 ماڈل کو Azure AI Services پر تعینات کریں"، "اپنے دستاویزاتی RAG سسٹم کے لیے نیا سرچ انڈیکس بنائیں"، "اپنے ایجنٹ کے جوابات کو معیار کے میٹرکس کے خلاف جانچیں"، یا "اپنے پیچیدہ تجزیاتی کاموں کے لیے بہترین استدلالی ماڈل تلاش کریں"

**مکمل ڈیمو منظرنامہ**: یہاں ایک طاقتور AI ترقیاتی ورک فلو ہے:

> "میں ایک کسٹمر سپورٹ ایجنٹ بنا رہا ہوں۔ مجھے کیٹلاگ سے ایک اچھا استدلالی ماڈل تلاش کرنے میں مدد کریں، اسے Azure AI Services پر تعینات کریں، ہماری دستاویزات سے ایک علم کا ذخیرہ بنائیں، جواب کی کوالٹی جانچنے کے لیے ایک تشخیصی فریم ورک ترتیب دیں، اور پھر GitHub ٹوکن کے ساتھ انضمام کا پروٹوٹائپ بنانے میں مدد کریں۔"

Azure AI Foundry MCP Server یہ کرے گا:
- آپ کی ضروریات کی بنیاد پر بہترین استدلالی ماڈلز کی سفارش کے لیے ماڈل کیٹلاگ سے سوال کرے گا
- آپ کے پسندیدہ Azure خطے کے لیے تعیناتی کے کمانڈز اور کوٹہ کی معلومات فراہم کرے گا
- آپ کی دستاویزات کے لیے مناسب اسکیمہ کے ساتھ Azure AI Search انڈیکسز ترتیب دے گا
- معیار کے میٹرکس اور حفاظتی چیکس کے ساتھ تشخیصی پائپ لائنز ترتیب دے گا
- فوری جانچ کے لیے GitHub توثیق کے ساتھ پروٹوٹائپنگ کوڈ تیار کرے گا
- آپ کی مخصوص ٹیکنالوجی اسٹیک کے مطابق مکمل سیٹ اپ گائیڈز فراہم کرے گا

**نمایاں مثال**: ایک ڈویلپر کے طور پر، میں مختلف LLM ماڈلز کے ساتھ قدم ملا کر چلنے میں مشکل محسوس کر رہا تھا۔ میں چند اہم ماڈلز جانتا ہوں، لیکن محسوس ہوتا تھا کہ میں کچھ پیداواری اور کارکردگی کے فوائد سے محروم ہوں۔ ٹوکنز اور کوٹہ کا انتظام بھی پریشان کن اور مشکل تھا – مجھے کبھی معلوم نہیں ہوتا تھا کہ میں صحیح کام کے لیے صحیح ماڈل منتخب کر رہا ہوں یا بجٹ ضائع کر رہا ہوں۔ میں نے حال ہی میں جیمز مونٹیمگنو سے MCP Server کے بارے میں سنا جب میں نے ٹیم کے ساتھیوں سے اس پوسٹ کے لیے MCP Server کی سفارشات پوچھی تھیں، اور میں اسے استعمال کرنے کے لیے پرجوش ہوں! ماڈل دریافت کی صلاحیتیں خاص طور پر متاثر کن لگتی ہیں، خاص طور پر میرے جیسے شخص کے لیے جو عام ماڈلز سے آگے جا کر مخصوص کاموں کے لیے بہتر ماڈلز تلاش کرنا چاہتا ہے۔ تشخیصی فریم ورک مجھے یہ یقینی بنانے میں مدد دے گا کہ میں واقعی بہتر نتائج حاصل کر رہا ہوں، نہ کہ صرف کچھ نیا آزما رہا ہوں۔

> **ℹ️ تجرباتی حیثیت**
> 
> یہ MCP سرور تجرباتی ہے اور فعال ترقی کے مراحل میں ہے۔ خصوصیات اور APIs میں تبدیلی آ سکتی ہے۔ Azure AI صلاحیتوں کو دریافت کرنے اور پروٹوٹائپ بنانے کے لیے بہترین، لیکن پیداوار کے استعمال کے لیے استحکام کی ضروریات کی تصدیق کریں۔

### 10. 🏢 Microsoft 365 Agents Toolkit MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**یہ کیا کرتا ہے**: ڈویلپرز کو Microsoft 365 اور Microsoft 365 Copilot کے ساتھ انضمام کرنے والے AI ایجنٹس اور ایپلیکیشنز بنانے کے لیے ضروری اوزار فراہم کرتا ہے، جن میں اسکیمہ کی توثیق، نمونہ کوڈ کی بازیابی، اور مسئلہ حل کرنے میں مدد شامل ہے۔

**یہ کیوں مفید ہے**: Microsoft 365 اور Copilot کے لیے ترقی پیچیدہ مینفسٹ اسکیمہ اور مخصوص ترقیاتی پیٹرنز پر مشتمل ہوتی ہے۔ یہ MCP سرور آپ کے کوڈنگ ماحول میں ضروری ترقیاتی وسائل لاتا ہے، جس سے آپ اسکیمہ کی توثیق کر سکتے ہیں، نمونہ کوڈ تلاش کر سکتے ہیں، اور عام مسائل کو حل کر سکتے ہیں بغیر بار بار دستاویزات دیکھے۔

**حقیقی دنیا میں استعمال**: "میرا declarative agent manifest درست کریں اور اسکیمہ کی غلطیاں ٹھیک کریں"، "Microsoft Graph API پلگ ان کے نفاذ کے لیے نمونہ کوڈ دکھائیں"، یا "میری Teams ایپ کی توثیق کے مسائل حل کرنے میں مدد کریں"

**نمایاں مثال**: میں نے اپنے دوست John Miller سے رابطہ کیا جب میں نے Build میں M365 Agents کے بارے میں بات کی، اور اس نے یہ MCP تجویز کیا۔ یہ نئے M365 Agents ڈویلپرز کے لیے بہت مفید ہو سکتا ہے کیونکہ یہ ٹیمپلیٹس، نمونہ کوڈ، اور اسکیفولڈنگ فراہم کرتا ہے تاکہ وہ دستاویزات میں گھِرنے کے بغیر شروع کر سکیں۔ اسکیمہ کی توثیق کی خصوصیات خاص طور پر مفید لگتی ہیں تاکہ مینفسٹ کی ساخت کی غلطیوں سے بچا جا سکے جو گھنٹوں کی ڈیبگنگ کا باعث بن سکتی ہیں۔

> **💡 پرو ٹپ**
> 
> اس سرور کو Microsoft Learn Docs MCP Server کے ساتھ استعمال کریں تاکہ M365 کی ترقی کے لیے مکمل مدد حاصل ہو – ایک سرکاری دستاویزات فراہم کرتا ہے جبکہ یہ عملی ترقیاتی اوزار اور مسئلہ حل کرنے میں مدد دیتا ہے۔

## آگے کیا ہے؟ 🔮

## 📋 نتیجہ

Model Context Protocol (MCP) ڈویلپرز کے AI اسسٹنٹس اور بیرونی اوزار کے ساتھ تعامل کے طریقے کو بدل رہا ہے۔ یہ 10 Microsoft MCP سرورز معیاری AI انضمام کی طاقت دکھاتے ہیں، جو ہموار ورک فلو فراہم کرتے ہیں تاکہ ڈویلپرز اپنی توجہ برقرار رکھ سکیں اور طاقتور بیرونی صلاحیتوں تک رسائی حاصل کر سکیں۔

مکمل Azure ماحولیاتی نظام کے انضمام سے لے کر Playwright جیسے مخصوص اوزار براؤزر آٹومیشن کے لیے اور MarkItDown جیسے دستاویزات کی پروسیسنگ کے لیے، یہ سرورز دکھاتے ہیں کہ MCP کس طرح مختلف ترقیاتی منظرناموں میں پیداواری صلاحیت کو بڑھا سکتا ہے۔ معیاری پروٹوکول اس بات کو یقینی بناتا ہے کہ یہ اوزار ایک ساتھ بغیر کسی رکاوٹ کے کام کریں، ایک مربوط ترقیاتی تجربہ تخلیق کرتے ہوئے۔

جیسے جیسے MCP ماحولیاتی نظام ترقی کرتا رہے گا، کمیونٹی کے ساتھ جڑے رہنا، نئے سرورز کو دریافت کرنا، اور اپنی مرضی کے حل بنانا آپ کی ترقیاتی پیداواری صلاحیت کو زیادہ سے زیادہ کرنے کی کلید ہوگا۔ MCP کی کھلی معیاری نوعیت کا مطلب ہے کہ آپ مختلف فروشندگان کے اوزار کو ملا کر اپنی مخصوص ضروریات کے لیے بہترین ورک فلو بنا سکتے ہیں۔

## 🔗 اضافی وسائل

- [Official Microsoft MCP Repository](https://github.com/microsoft/mcp)
- [MCP Community & Documentation](https://modelcontextprotocol.io/introduction)
- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [Visual Studio MCP Documentation](https://learn.microsoft.com/visualstudio/ide/mcp-servers)
- [Azure MCP Documentation](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [Let's Learn – MCP Events](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/lets-learn---mcp-events-a-beginners-guide-to-the-model-context-protocol/4429023)
- [Awesome GitHub Copilot Customizations](https://github.com/awesome-copilot)
- [C# MCP SDK](https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol)
- [MCP Dev Days Live 29th/30th July or watch on Demand ](https://aka.ms/mcpdevdays)

## 🎯 مشقیں

1. **انسٹال اور ترتیب دیں**: اپنے VS Code ماحول میں ایک MCP سرور سیٹ اپ کریں اور بنیادی فعالیت کی جانچ کریں۔
2. **ورک فلو انضمام**: ایک ترقیاتی ورک فلو ڈیزائن کریں جو کم از کم تین مختلف MCP سرورز کو یکجا کرے۔
3. **کسٹم سرور کی منصوبہ بندی**: اپنی روزمرہ کی ترقیاتی روٹین میں ایک ایسا کام شناخت کریں جو کسٹم MCP سرور سے فائدہ اٹھا سکتا ہو اور اس کے لیے وضاحت تیار کریں۔
4. **کارکردگی کا تجزیہ**: MCP سرورز کے استعمال کی کارکردگی کا موازنہ روایتی طریقوں سے کریں عام ترقیاتی کاموں کے لیے۔
5. **سیکیورٹی کا جائزہ**: اپنے ترقیاتی ماحول میں MCP سرورز کے استعمال کے سیکیورٹی پہلوؤں کا جائزہ لیں اور بہترین طریقے تجویز کریں۔

Next:[Best Practices](../08-BestPractices/README.md)

**دستخطی نوٹ**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ اگرچہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنی مادری زبان میں ہی معتبر ماخذ سمجھی جانی چاہیے۔ اہم معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم پر عائد نہیں ہوتی۔