<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "92af35e8c34923031f3d228dffad9ebb",
  "translation_date": "2025-09-03T15:57:40+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/dotnet/README.md",
  "language_code": "fa"
}
-->
# اجرای این نمونه

## -1- نصب وابستگی‌ها

```bash
dotnet restore
```

## -3- اجرای نمونه

```bash
dotnet run
```

## -4- آزمایش نمونه

با اجرای سرور در یک ترمینال، یک ترمینال دیگر باز کنید و دستور زیر را اجرا کنید:

```bash
npx @modelcontextprotocol/inspector dotnet run
```

این باید یک وب سرور با رابط بصری راه‌اندازی کند که به شما امکان آزمایش نمونه را می‌دهد.

پس از اتصال سرور:

- ابزارها را لیست کنید و `add` را اجرا کنید، با آرگومان‌های ۲ و ۴، باید نتیجه ۶ را مشاهده کنید.
- به منابع و قالب منابع بروید و "greeting" را فراخوانی کنید، یک نام وارد کنید و باید یک خوش‌آمدگویی با نامی که وارد کرده‌اید مشاهده کنید.

### آزمایش در حالت CLI

می‌توانید آن را مستقیماً در حالت CLI با اجرای دستور زیر راه‌اندازی کنید:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/list
```

این تمام ابزارهای موجود در سرور را لیست می‌کند. باید خروجی زیر را مشاهده کنید:

```text
{
  "tools": [
    {
      "name": "Add",
      "description": "Adds two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer"
          },
          "b": {
            "type": "integer"
          }
        },
        "title": "Add",
        "description": "Adds two numbers",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

برای فراخوانی یک ابزار تایپ کنید:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/call --tool-name Add --tool-arg a=1 --tool-arg b=2
```

باید خروجی زیر را مشاهده کنید:

```text
{
  "content": [
    {
      "type": "text",
      "text": "Sum 3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> معمولاً اجرای بازرس در حالت CLI بسیار سریع‌تر از مرورگر است.
> اطلاعات بیشتر درباره بازرس را [اینجا](https://github.com/modelcontextprotocol/inspector) بخوانید.

---

**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما تلاش می‌کنیم دقت را حفظ کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌ها باشند. سند اصلی به زبان اصلی آن باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حساس، توصیه می‌شود از ترجمه حرفه‌ای انسانی استفاده کنید. ما مسئولیتی در قبال سوء تفاهم‌ها یا تفسیرهای نادرست ناشی از استفاده از این ترجمه نداریم.