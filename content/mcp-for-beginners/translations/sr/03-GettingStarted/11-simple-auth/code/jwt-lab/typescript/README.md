<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0f756f0d5b712847bd7d21b5e45c4166",
  "translation_date": "2025-10-07T01:43:34+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/typescript/README.md",
  "language_code": "sr"
}
-->
# Покрени пример

## Инсталирај зависности

```sh
npm install
```

## Покрени код

```sh
npm run build
```

```sh
npm start
```

требало би да видите излаз сличан:

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

**Одрицање од одговорности**:  
Овај документ је преведен помоћу услуге за превођење уз помоћ вештачке интелигенције [Co-op Translator](https://github.com/Azure/co-op-translator). Иако се трудимо да обезбедимо тачност, молимо вас да имате у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитативним извором. За критичне информације препоручује се професионални превод од стране људи. Не сносимо одговорност за било каква погрешна тумачења или неспоразуме који могу произаћи из коришћења овог превода.