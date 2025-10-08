<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "67ecbca6a060477ded3e13ddbeba64f7",
  "translation_date": "2025-08-18T14:43:03+00:00",
  "source_file": "03-GettingStarted/06-http-streaming/solution/python/README.md",
  "language_code": "mo"
}
-->
# 執行此範例

以下是如何使用 Python 執行經典 HTTP 串流伺服器與客戶端，以及 MCP 串流伺服器與客戶端的說明。

### 概述

- 您將設置一個 MCP 伺服器，該伺服器在處理項目時向客戶端串流進度通知。
- 客戶端將即時顯示每個通知。
- 本指南涵蓋了前置條件、設置、執行以及故障排除。

### 前置條件

- Python 3.9 或更新版本
- `mcp` Python 套件（使用 `pip install mcp` 安裝）

### 安裝與設置

1. 克隆此存儲庫或下載解決方案檔案。

   ```pwsh
   git clone https://github.com/microsoft/mcp-for-beginners
   ```

1. **建立並啟用虛擬環境（建議）：**

   ```pwsh
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # On Windows
   # or
   source venv/bin/activate      # On Linux/macOS
   ```

1. **安裝所需的依賴項：**

   ```pwsh
   pip install "mcp[cli]" fastapi requests
   ```

### 檔案

- **伺服器：** [server.py](../../../../../../03-GettingStarted/06-http-streaming/solution/python/server.py)
- **客戶端：** [client.py](../../../../../../03-GettingStarted/06-http-streaming/solution/python/client.py)

### 執行經典 HTTP 串流伺服器

1. 移動到解決方案目錄：

   ```pwsh
   cd 03-GettingStarted/06-http-streaming/solution
   ```

2. 啟動經典 HTTP 串流伺服器：

   ```pwsh
   python server.py
   ```

3. 伺服器將啟動並顯示：

   ```
   Starting FastAPI server for classic HTTP streaming...
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   ```

### 執行經典 HTTP 串流客戶端

1. 開啟一個新的終端（啟用相同的虛擬環境並進入相同目錄）：

   ```pwsh
   cd 03-GettingStarted/06-http-streaming/solution
   python client.py
   ```

2. 您應該會看到串流的訊息依序列印出來：

   ```text
   Running classic HTTP streaming client...
   Connecting to http://localhost:8000/stream with message: hello
   --- Streaming Progress ---
   Processing file 1/3...
   Processing file 2/3...
   Processing file 3/3...
   Here's the file content: hello
   --- Stream Ended ---
   ```

### 執行 MCP 串流伺服器

1. 移動到解決方案目錄：
   ```pwsh
   cd 03-GettingStarted/06-http-streaming/solution
   ```
2. 使用 streamable-http 傳輸啟動 MCP 伺服器：
   ```pwsh
   python server.py mcp
   ```
3. 伺服器將啟動並顯示：
   ```
   Starting MCP server with streamable-http transport...
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   ```

### 執行 MCP 串流客戶端

1. 開啟一個新的終端（啟用相同的虛擬環境並進入相同目錄）：
   ```pwsh
   cd 03-GettingStarted/06-http-streaming/solution
   python client.py mcp
   ```
2. 當伺服器處理每個項目時，您應該會即時看到通知被列印出來：
   ```
   Running MCP client...
   Starting client...
   Session ID before init: None
   Session ID after init: a30ab7fca9c84f5fa8f5c54fe56c9612
   Session initialized, ready to call tools.
   Received message: root=LoggingMessageNotification(...)
   NOTIFICATION: root=LoggingMessageNotification(...)
   ...
   Tool result: meta=None content=[TextContent(type='text', text='Processed files: file_1.txt, file_2.txt, file_3.txt | Message: hello from client')]
   ```

### 關鍵實作步驟

1. **使用 FastMCP 建立 MCP 伺服器。**
2. **定義一個工具來處理清單，並使用 `ctx.info()` 或 `ctx.log()` 發送通知。**
3. **使用 `transport="streamable-http"` 啟動伺服器。**
4. **實作一個客戶端，包含一個訊息處理器來顯示收到的通知。**

### 程式碼講解
- 伺服器使用非同步函數以及 MCP 上下文來發送進度更新。
- 客戶端實作了一個非同步訊息處理器來列印通知與最終結果。

### 提示與故障排除

- 使用 `async/await` 來進行非阻塞操作。
- 在伺服器與客戶端中始終處理例外情況以提高穩定性。
- 使用多個客戶端進行測試以觀察即時更新。
- 如果遇到錯誤，請檢查您的 Python 版本並確保所有依賴項已安裝。

**免責聲明**：  
本文檔已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。我們致力於提供準確的翻譯，但請注意，自動翻譯可能包含錯誤或不準確之處。應以原始語言的文件作為權威來源。對於關鍵信息，建議尋求專業人工翻譯。我們對因使用此翻譯而引起的任何誤解或錯誤解讀概不負責。