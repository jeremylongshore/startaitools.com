<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "dde4e32e4b55ef4962c411b39d2340a7",
  "translation_date": "2025-09-03T15:58:58+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/dotnet/README.md",
  "language_code": "mo"
}
-->
# 執行此範例

## -1- 安裝依賴項目

```bash
dotnet restore
```

## -2- 執行範例

```bash
dotnet run
```

## -3- 測試範例

在執行以下指令之前，請先開啟另一個終端機（確保伺服器仍在運行）。

當伺服器在一個終端機中運行時，打開另一個終端機並執行以下指令：

```bash
npx @modelcontextprotocol/inspector http://localhost:3001
```

這將啟動一個帶有視覺介面的網頁伺服器，讓您可以測試此範例。

> 確保選擇 **Streamable HTTP** 作為傳輸類型，並且 URL 為 `http://localhost:3001/mcp`。

伺服器連接後：

- 嘗試列出工具並執行 `add`，參數為 2 和 4，您應該會在結果中看到 6。
- 前往資源和資源模板，調用 "greeting"，輸入一個名字，您應該會看到包含您提供名字的問候語。

### 在 CLI 模式中測試

您可以直接通過執行以下指令啟動 CLI 模式：

```bash 
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/list
```

這將列出伺服器中所有可用的工具。您應該會看到以下輸出：

```text
{
  "tools": [
    {
      "name": "AddNumbers",
      "description": "Add two numbers together.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "description": "The first number",
            "type": "integer"
          },
          "b": {
            "description": "The second number",
            "type": "integer"
          }
        },
        "title": "AddNumbers",
        "description": "Add two numbers together.",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

要調用工具，請輸入：

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:3001 --method tools/call --tool-name AddNumbers --tool-arg a=1 --tool-arg b=2
```

您應該會看到以下輸出：

```text
{
  "content": [
    {
      "type": "text",
      "text": "3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> 通常在 CLI 模式中運行檢查器比在瀏覽器中快得多。
> 在 [這裡](https://github.com/modelcontextprotocol/inspector) 閱讀更多關於檢查器的資訊。

---

**免責聲明**：  
本文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。儘管我們努力確保翻譯的準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於關鍵信息，建議使用專業人工翻譯。我們對因使用此翻譯而引起的任何誤解或誤釋不承擔責任。