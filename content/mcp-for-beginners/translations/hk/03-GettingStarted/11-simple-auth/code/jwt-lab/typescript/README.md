<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0f756f0d5b712847bd7d21b5e45c4166",
  "translation_date": "2025-10-07T01:41:14+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/typescript/README.md",
  "language_code": "hk"
}
-->
# 執行範例

## 安裝依賴項

```sh
npm install
```

## 執行程式碼

```sh
npm run build
```

```sh
npm start
```

你應該會看到類似以下的輸出：

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

**免責聲明**：  
本文件已使用人工智能翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。儘管我們致力於提供準確的翻譯，請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要信息，建議使用專業人工翻譯。我們對因使用此翻譯而引起的任何誤解或錯誤解釋概不負責。