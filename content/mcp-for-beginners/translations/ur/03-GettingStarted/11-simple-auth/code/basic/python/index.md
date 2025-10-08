<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3f68294760a11dd3fdd175bd7f904a92",
  "translation_date": "2025-10-07T01:29:22+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/basic/python/README.md",
  "language_code": "ur"
}
-->
# نمونہ چلائیں

یہ نمونہ ایک MCP سرور شروع کرتا ہے جس میں ایک مڈل ویئر شامل ہے جو درست Authorization ہیڈر کی جانچ کرتا ہے۔

## ضروریات انسٹال کریں

```bash
pip install "mcp[cli]" 
```

## سرور شروع کریں

```bash
python server.py
```

کلائنٹ کو دوسرے ٹرمینل میں شروع کریں

```bash
python client.py
```

آپ کو ایک نتیجہ اس طرح نظر آنا چاہیے:

```text
2025-09-30 13:25:54 - mcp_client - INFO - Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-09-30T13:25:54.311900",\n  "timezone": "UTC",\n  "timestamp": 1759238754.3119,\n  "formatted": "2025-09-30 13:25:54"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-09-30T13:25:54.311900', 'timezone': 'UTC', 'timestamp': 1759238754.3119, 'formatted': '2025-09-30 13:25:54'} isError=False
```

اس کا مطلب ہے کہ بھیجی گئی اسناد کو اجازت دی جا رہی ہے۔

`client.py` میں اسناد کو "secret-token2" میں تبدیل کرنے کی کوشش کریں، پھر آپ کو جواب میں یہ متن نظر آئے گا:

```text
2025-09-30 13:27:44 - httpx - INFO - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 403 Forbidden"
```

اس کا مطلب ہے کہ آپ کی تصدیق ہو گئی (آپ کے پاس اسناد تھیں)، لیکن وہ غلط تھیں۔

---

**ڈسکلیمر**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کا استعمال کرتے ہوئے ترجمہ کی گئی ہے۔ ہم درستگی کے لیے کوشش کرتے ہیں، لیکن براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا غیر درستیاں ہو سکتی ہیں۔ اصل دستاویز کو اس کی اصل زبان میں مستند ذریعہ سمجھا جانا چاہیے۔ اہم معلومات کے لیے، پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ ہم اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کے ذمہ دار نہیں ہیں۔