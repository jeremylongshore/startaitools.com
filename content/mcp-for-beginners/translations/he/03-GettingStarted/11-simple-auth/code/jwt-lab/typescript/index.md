<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0f756f0d5b712847bd7d21b5e45c4166",
  "translation_date": "2025-10-07T01:42:46+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/typescript/README.md",
  "language_code": "he"
}
-->
# הפעלת דוגמה

## התקנת תלותים

```sh
npm install
```

## הפעלת קוד

```sh
npm run build
```

```sh
npm start
```

אתם אמורים לראות פלט דומה ל:

```text
JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlVzZXIgdXNlcnNzb24iLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNzU5MTY4NzIyLCJleHAiOjE3NTkxNzIzMjJ9.JAMGCX_sHdqHzsKqqg6jHFUGk6zYZB7N77mWDqcRMcY
Decoded Payload: {
  sub: '1234567890',
  name: 'User usersson',
  admin: true,
  iat: 1759168722,
  exp: 1759172322
```

---

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עשויים להכיל שגיאות או אי-דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור סמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. איננו נושאים באחריות לאי-הבנות או לפרשנויות שגויות הנובעות משימוש בתרגום זה.