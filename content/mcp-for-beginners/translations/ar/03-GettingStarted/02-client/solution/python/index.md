<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0ab9613fc9595f493847f91275859a18",
  "translation_date": "2025-07-13T18:39:29+00:00",
  "source_file": "03-GettingStarted/02-client/solution/python/README.md",
  "language_code": "ar"
}
-->
# تشغيل هذا المثال

يوصى بتثبيت `uv` لكنه ليس ضروريًا، راجع [التعليمات](https://docs.astral.sh/uv/#highlights)

## -0- إنشاء بيئة افتراضية

```bash
python -m venv venv
```

## -1- تفعيل البيئة الافتراضية

```bash
venv\Scrips\activate
```

## -2- تثبيت التبعيات

```bash
pip install "mcp[cli]"
```

## -3- تشغيل المثال


```bash
python client.py
```

يجب أن ترى مخرجات مشابهة لـ:

```text
LISTING RESOURCES
Resource:  ('meta', None)
Resource:  ('nextCursor', None)
Resource:  ('resources', [])
                    INFO     Processing request of type ListToolsRequest                                                                               server.py:534
LISTING TOOLS
Tool:  add
READING RESOURCE
                    INFO     Processing request of type ReadResourceRequest                                                                            server.py:534
CALL TOOL
                    INFO     Processing request of type CallToolRequest                                                                                server.py:534
[TextContent(type='text', text='8', annotations=None)]
```

**إخلاء المسؤولية**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق به. للمعلومات الهامة، يُنصح بالاعتماد على الترجمة البشرية المهنية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.