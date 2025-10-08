<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3f68294760a11dd3fdd175bd7f904a92",
  "translation_date": "2025-10-07T01:29:11+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/basic/python/README.md",
  "language_code": "ar"
}
-->
# تشغيل المثال

يبدأ هذا المثال خادم MCP مع وسيط يتحقق من وجود رأس تفويض صالح.

## تثبيت التبعيات

```bash
pip install "mcp[cli]" 
```

## بدء تشغيل الخادم

```bash
python server.py
```

قم بتشغيل العميل في نافذة طرفية أخرى

```bash
python client.py
```

يجب أن ترى نتيجة مشابهة لـ:

```text
2025-09-30 13:25:54 - mcp_client - INFO - Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-09-30T13:25:54.311900",\n  "timezone": "UTC",\n  "timestamp": 1759238754.3119,\n  "formatted": "2025-09-30 13:25:54"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-09-30T13:25:54.311900', 'timezone': 'UTC', 'timestamp': 1759238754.3119, 'formatted': '2025-09-30 13:25:54'} isError=False
```

هذا يعني أن بيانات الاعتماد المرسلة يتم السماح بها.

حاول تغيير بيانات الاعتماد في `client.py` إلى "secret-token2"، ثم يجب أن ترى هذا النص كجزء من الاستجابة:

```text
2025-09-30 13:27:44 - httpx - INFO - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 403 Forbidden"
```

هذا يعني أنك تم التحقق من هويتك (لديك بيانات اعتماد)، لكنها غير صالحة.

---

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو معلومات غير دقيقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق. للحصول على معلومات حاسمة، يُوصى بالاستعانة بترجمة بشرية احترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة ناتجة عن استخدام هذه الترجمة.