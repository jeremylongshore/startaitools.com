<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "cc12267d65091b22e39026fccfcaa22b",
  "translation_date": "2025-10-07T01:37:14+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/python/README.md",
  "language_code": "ar"
}
-->
# تشغيل المثال

## إعداد البيئة

```sh
python -m venv
source ./venv/bin/activate
```

## تثبيت التبعيات

```sh
pip install PyJWT
```

## تشغيل الكود

```sh
python lab.py
```

يجب أن ترى مخرجات مشابهة لـ:

```text
Encoded JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlVzZXIgVXNlcnNvbiIsImFkbWluIjp0cnVlLCJpYXQiOjE3NTkxNjgzMDEsImV4cCI6MTc1OTE3MTkwMX0.tz0UYNNtGVC61DWjVDF8xlhpNkp5XBtxmQH3m_RNwe8
✅ Token is valid.
Decoded claims:
  sub: 1234567890
  name: User Userson
  admin: True
  iat: 1759168301
  exp: 1759171901
```

---

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي. للحصول على معلومات حاسمة، يُوصى بالترجمة البشرية الاحترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة ناتجة عن استخدام هذه الترجمة.