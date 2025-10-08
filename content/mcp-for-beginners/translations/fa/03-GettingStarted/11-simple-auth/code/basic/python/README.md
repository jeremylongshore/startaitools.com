<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3f68294760a11dd3fdd175bd7f904a92",
  "translation_date": "2025-10-07T01:29:16+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/basic/python/README.md",
  "language_code": "fa"
}
-->
# اجرای نمونه

این نمونه یک سرور MCP را با یک میان‌افزار که وجود هدر Authorization معتبر را بررسی می‌کند، راه‌اندازی می‌کند.

## نصب وابستگی‌ها

```bash
pip install "mcp[cli]" 
```

## راه‌اندازی سرور

```bash
python server.py
```

کلاینت را در یک ترمینال دیگر اجرا کنید

```bash
python client.py
```

باید نتیجه‌ای مشابه زیر را مشاهده کنید:

```text
2025-09-30 13:25:54 - mcp_client - INFO - Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-09-30T13:25:54.311900",\n  "timezone": "UTC",\n  "timestamp": 1759238754.3119,\n  "formatted": "2025-09-30 13:25:54"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-09-30T13:25:54.311900', 'timezone': 'UTC', 'timestamp': 1759238754.3119, 'formatted': '2025-09-30 13:25:54'} isError=False
```

این به این معناست که اعتبارنامه ارسال شده پذیرفته شده است.

سعی کنید اعتبارنامه در فایل `client.py` را به "secret-token2" تغییر دهید، سپس باید این متن را به عنوان بخشی از پاسخ مشاهده کنید:

```text
2025-09-30 13:27:44 - httpx - INFO - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 403 Forbidden"
```

این به این معناست که شما احراز هویت شده‌اید (اعتبارنامه داشتید)، اما اعتبارنامه نامعتبر بود.

---

**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما تلاش می‌کنیم دقت را حفظ کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است حاوی خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان بومی آن باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حساس، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما هیچ مسئولیتی در قبال سوءتفاهم‌ها یا تفسیرهای نادرست ناشی از استفاده از این ترجمه نداریم.