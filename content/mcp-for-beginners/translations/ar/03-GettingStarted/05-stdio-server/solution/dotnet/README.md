<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "69372338676e01a2c97f42f70fdfbf42",
  "translation_date": "2025-08-26T20:16:35+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/dotnet/README.md",
  "language_code": "ar"
}
-->
# MCP stdio Server - .NET Solution

> **⚠️ مهم**: تم تحديث هذه الحلول لاستخدام **stdio transport** كما هو موصى به في مواصفات MCP بتاريخ 2025-06-18. تم إيقاف استخدام النقل القديم SSE.

## نظرة عامة

توضح هذه الحلول في .NET كيفية بناء خادم MCP باستخدام النقل الحالي stdio. يعتبر النقل stdio أبسط وأكثر أمانًا ويوفر أداءً أفضل مقارنةً بالطريقة القديمة SSE.

## المتطلبات الأساسية

- .NET 9.0 SDK أو أحدث
- فهم أساسي لحقن التبعيات في .NET

## تعليمات الإعداد

### الخطوة 1: استعادة التبعيات

```bash
dotnet restore
```

### الخطوة 2: بناء المشروع

```bash
dotnet build
```

## تشغيل الخادم

يعمل خادم stdio بشكل مختلف عن الخادم القديم القائم على HTTP. بدلاً من تشغيل خادم ويب، يتواصل عبر stdin/stdout:

```bash
dotnet run
```

**مهم**: سيبدو أن الخادم متوقف - هذا طبيعي! إنه ينتظر رسائل JSON-RPC من stdin.

## اختبار الخادم

### الطريقة الأولى: باستخدام MCP Inspector (موصى به)

```bash
npx @modelcontextprotocol/inspector dotnet run
```

هذا سيقوم بـ:
1. تشغيل الخادم كعملية فرعية
2. فتح واجهة ويب للاختبار
3. السماح لك باختبار جميع أدوات الخادم بشكل تفاعلي

### الطريقة الثانية: اختبار مباشر عبر سطر الأوامر

يمكنك أيضًا الاختبار عن طريق تشغيل Inspector مباشرةً:

```bash
npx @modelcontextprotocol/inspector dotnet run --project .
```

### الأدوات المتاحة

يوفر الخادم الأدوات التالية:

- **AddNumbers(a, b)**: جمع رقمين معًا
- **MultiplyNumbers(a, b)**: ضرب رقمين معًا  
- **GetGreeting(name)**: إنشاء تحية شخصية
- **GetServerInfo()**: الحصول على معلومات حول الخادم

### الاختبار باستخدام Claude Desktop

لاستخدام هذا الخادم مع Claude Desktop، أضف هذا التكوين إلى ملف `claude_desktop_config.json` الخاص بك:

```json
{
  "mcpServers": {
    "example-stdio-server": {
      "command": "dotnet",
      "args": ["run", "--project", "path/to/server.csproj"]
    }
  }
}
```

## هيكل المشروع

```
dotnet/
├── Program.cs           # Main server setup and configuration
├── Tools.cs            # Tool implementations
├── server.csproj       # Project file with dependencies
├── server.sln         # Solution file
├── Properties/         # Project properties
└── README.md          # This file
```

## الفروقات الرئيسية بين HTTP/SSE

**نقل stdio (الحالي):**
- ✅ إعداد أبسط - لا حاجة لخادم ويب
- ✅ أمان أفضل - لا توجد نقاط نهاية HTTP
- ✅ يستخدم `Host.CreateApplicationBuilder()` بدلاً من `WebApplication.CreateBuilder()`
- ✅ `WithStdioTransport()` بدلاً من `WithHttpTransport()`
- ✅ تطبيق كونسول بدلاً من تطبيق ويب
- ✅ أداء أفضل

**نقل HTTP/SSE (الموقوف):**
- ❌ يتطلب خادم ويب ASP.NET Core
- ❌ يحتاج إلى إعداد توجيه `app.MapMcp()`
- ❌ إعداد وتبعيات أكثر تعقيدًا
- ❌ اعتبارات أمان إضافية
- ❌ تم إيقافه في MCP بتاريخ 2025-06-18

## ميزات التطوير

- **حقن التبعيات**: دعم كامل لحقن التبعيات للخدمات وتسجيل الأحداث
- **تسجيل منظم**: تسجيل مناسب إلى stderr باستخدام `ILogger<T>`
- **سمات الأدوات**: تعريف الأدوات بشكل نظيف باستخدام سمات `[McpServerTool]`
- **دعم العمليات غير المتزامنة**: جميع الأدوات تدعم العمليات غير المتزامنة
- **معالجة الأخطاء**: معالجة الأخطاء بشكل سلس وتسجيل الأحداث

## نصائح التطوير

- استخدم `ILogger` لتسجيل الأحداث (لا تكتب مباشرةً إلى stdout)
- قم بالبناء باستخدام `dotnet build` قبل الاختبار
- اختبر باستخدام Inspector للحصول على تصحيح بصري
- يتم تسجيل جميع الأحداث تلقائيًا إلى stderr
- يتعامل الخادم مع إشارات الإيقاف بشكل سلس

تتبع هذه الحلول مواصفات MCP الحالية وتوضح أفضل الممارسات لتنفيذ النقل stdio باستخدام .NET.

---

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو معلومات غير دقيقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي. للحصول على معلومات حاسمة، يُوصى بالاستعانة بترجمة بشرية احترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة تنشأ عن استخدام هذه الترجمة.