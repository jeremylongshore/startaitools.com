<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T19:59:22+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "ar"
}
-->
# حلول خوادم MCP باستخدام stdio

> **⚠️ مهم**: تم تحديث هذه الحلول لاستخدام **stdio transport** كما هو موصى به في مواصفات MCP بتاريخ 2025-06-18. تم إيقاف استخدام النقل الأصلي SSE (Server-Sent Events).

فيما يلي الحلول الكاملة لبناء خوادم MCP باستخدام stdio transport لكل بيئة تشغيل:

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - تنفيذ كامل لخادم stdio
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - خادم stdio بلغة Python باستخدام asyncio
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - خادم stdio بلغة .NET مع حقن التبعيات

كل حل يوضح:
- إعداد stdio transport
- تعريف أدوات الخادم
- التعامل الصحيح مع رسائل JSON-RPC
- التكامل مع عملاء MCP مثل Claude

جميع الحلول تتبع مواصفات MCP الحالية وتستخدم stdio transport الموصى به لتحقيق الأداء الأمثل والأمان.

---

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو معلومات غير دقيقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي. للحصول على معلومات حاسمة، يُوصى بالاستعانة بترجمة بشرية احترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة ناتجة عن استخدام هذه الترجمة.