<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "9d799c4a30a8383e0a74af9153262972",
  "translation_date": "2025-08-26T20:05:36+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/typescript/README.md",
  "language_code": "ar"
}
-->
# خادم MCP stdio - حل TypeScript

> **⚠️ مهم**: تم تحديث هذا الحل لاستخدام **stdio transport** كما هو موصى به في مواصفات MCP بتاريخ 2025-06-18. تم إيقاف استخدام النقل القديم SSE.

## نظرة عامة

يُظهر هذا الحل المكتوب بلغة TypeScript كيفية بناء خادم MCP باستخدام النقل الحالي stdio. يُعتبر النقل stdio أبسط وأكثر أمانًا ويوفر أداءً أفضل مقارنةً بالنهج القديم SSE الذي تم إيقافه.

## المتطلبات الأساسية

- Node.js 18 أو أحدث
- مدير الحزم npm أو yarn

## تعليمات الإعداد

### الخطوة 1: تثبيت التبعيات

```bash
npm install
```

### الخطوة 2: بناء المشروع

```bash
npm run build
```

## تشغيل الخادم

يعمل خادم stdio بطريقة مختلفة عن خادم SSE القديم. بدلاً من تشغيل خادم ويب، يتواصل الخادم عبر stdin/stdout:

```bash
npm start
```

**مهم**: قد يبدو أن الخادم متوقف - هذا طبيعي! فهو ينتظر رسائل JSON-RPC من stdin.

## اختبار الخادم

### الطريقة 1: باستخدام MCP Inspector (موصى بها)

```bash
npm run inspector
```

هذا سيقوم بـ:
1. تشغيل الخادم كعملية فرعية
2. فتح واجهة ويب للاختبار
3. تمكينك من اختبار جميع أدوات الخادم بشكل تفاعلي

### الطريقة 2: الاختبار عبر سطر الأوامر مباشرة

يمكنك أيضًا الاختبار عن طريق تشغيل Inspector مباشرة:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

### الأدوات المتاحة

يوفر الخادم الأدوات التالية:

- **add(a, b)**: جمع رقمين معًا
- **multiply(a, b)**: ضرب رقمين معًا  
- **get_greeting(name)**: إنشاء تحية مخصصة
- **get_server_info()**: الحصول على معلومات حول الخادم

### الاختبار باستخدام Claude Desktop

لاستخدام هذا الخادم مع Claude Desktop، أضف هذا التكوين إلى ملف `claude_desktop_config.json`:

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

## هيكل المشروع

```
typescript/
├── src/
│   └── index.ts          # Main server implementation
├── build/                # Compiled JavaScript (generated)
├── package.json          # Project configuration
├── tsconfig.json         # TypeScript configuration
└── README.md            # This file
```

## الفروقات الرئيسية عن SSE

**نقل stdio (الحالي):**
- ✅ إعداد أبسط - لا حاجة لخادم HTTP
- ✅ أمان أفضل - لا توجد نقاط نهاية HTTP
- ✅ تواصل يعتمد على العمليات الفرعية
- ✅ JSON-RPC عبر stdin/stdout
- ✅ أداء أفضل

**نقل SSE (المتوقف):**
- ❌ يتطلب إعداد خادم Express
- ❌ يحتاج إلى إدارة معقدة للتوجيه والجلسات
- ❌ المزيد من التبعيات (Express، معالجة HTTP)
- ❌ اعتبارات أمان إضافية
- ❌ تم إيقافه الآن في MCP بتاريخ 2025-06-18

## نصائح للتطوير

- استخدم `console.error()` لتسجيل الأخطاء (لا تستخدم `console.log()` لأنه يكتب إلى stdout)
- قم بالبناء باستخدام `npm run build` قبل الاختبار
- اختبر باستخدام Inspector للحصول على تصحيح بصري
- تأكد من أن جميع رسائل JSON مُنسقة بشكل صحيح
- يتعامل الخادم تلقائيًا مع الإغلاق السلس عند استقبال SIGINT/SIGTERM

يتبع هذا الحل مواصفات MCP الحالية ويُظهر أفضل الممارسات لتنفيذ النقل stdio باستخدام TypeScript.

---

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو معلومات غير دقيقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق. للحصول على معلومات حاسمة، يُوصى بالاستعانة بترجمة بشرية احترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة تنشأ عن استخدام هذه الترجمة.