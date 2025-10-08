<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "999c5e7623c1e2d5e5a07c2feb39eb67",
  "translation_date": "2025-07-14T08:24:26+00:00",
  "source_file": "10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/README.md",
  "language_code": "hk"
}
-->
# Weather MCP Server

這是一個用 Python 實作的範例 MCP Server，提供模擬的天氣工具回應。你可以用它作為自己 MCP Server 的基礎架構。它包含以下功能：

- **Weather Tool**：根據指定地點提供模擬的天氣資訊。
- **Connect to Agent Builder**：可將 MCP Server 連接到 Agent Builder 以便測試和除錯。
- **Debug in [MCP Inspector](https://github.com/modelcontextprotocol/inspector)**：可使用 MCP Inspector 來除錯 MCP Server。

## 使用 Weather MCP Server 範本快速上手

> **先決條件**
>
> 要在本地開發機器上執行 MCP Server，你需要：
>
> - [Python](https://www.python.org/)
> - （*可選 - 如果你偏好 uv*）[uv](https://github.com/astral-sh/uv)
> - [Python 除錯擴充套件](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)

## 準備環境

有兩種方式可以設定此專案的環境，你可以依照喜好選擇其中一種。

> 注意：建立虛擬環境後，請重新載入 VSCode 或終端機，確保使用虛擬環境的 Python。

| 方式 | 步驟 |
| -------- | ----- |
| 使用 `uv` | 1. 建立虛擬環境：`uv venv` <br>2. 執行 VSCode 指令 "***Python: Select Interpreter***"，選擇剛建立的虛擬環境 Python <br>3. 安裝依賴（包含開發依賴）：`uv pip install -r pyproject.toml --extra dev` |
| 使用 `pip` | 1. 建立虛擬環境：`python -m venv .venv` <br>2. 執行 VSCode 指令 "***Python: Select Interpreter***"，選擇剛建立的虛擬環境 Python <br>3. 安裝依賴（包含開發依賴）：`pip install -e .[dev]` |

設定好環境後，你可以透過 Agent Builder 作為 MCP Client 在本地開發機器上執行伺服器開始使用：
1. 開啟 VS Code 除錯面板。選擇 `Debug in Agent Builder` 或按 `F5` 開始除錯 MCP Server。
2. 使用 AI Toolkit Agent Builder 搭配[此提示](../../../../../../../../../../open_prompt_builder)測試伺服器。伺服器會自動連接到 Agent Builder。
3. 點擊 `Run` 以該提示測試伺服器。

**恭喜**！你已成功透過 Agent Builder 作為 MCP Client 在本地開發機器上執行 Weather MCP Server。
![DebugMCP](https://raw.githubusercontent.com/microsoft/windows-ai-studio-templates/refs/heads/dev/mcpServers/mcp_debug.gif)

## 範本包含內容

| 資料夾 / 檔案 | 內容 |
| ------------ | -------------------------------------------- |
| `.vscode`    | 用於除錯的 VSCode 設定檔案                   |
| `.aitk`      | AI Toolkit 的設定檔                           |
| `src`        | weather mcp server 的原始程式碼               |

## 如何除錯 Weather MCP Server

> 注意：
> - [MCP Inspector](https://github.com/modelcontextprotocol/inspector) 是一款用於測試和除錯 MCP Server 的視覺化開發工具。
> - 所有除錯模式都支援斷點，你可以在工具實作程式碼中加入斷點。

| 除錯模式 | 說明 | 除錯步驟 |
| ---------- | ----------- | --------------- |
| Agent Builder | 透過 AI Toolkit 在 Agent Builder 中除錯 MCP Server。 | 1. 開啟 VS Code 除錯面板。選擇 `Debug in Agent Builder` 並按 `F5` 開始除錯 MCP Server。<br>2. 使用 AI Toolkit Agent Builder 搭配[此提示](../../../../../../../../../../open_prompt_builder)測試伺服器。伺服器會自動連接到 Agent Builder。<br>3. 點擊 `Run` 以該提示測試伺服器。 |
| MCP Inspector | 使用 MCP Inspector 除錯 MCP Server。 | 1. 安裝 [Node.js](https://nodejs.org/)<br>2. 設定 Inspector：`cd inspector` 並執行 `npm install` <br>3. 開啟 VS Code 除錯面板。選擇 `Debug SSE in Inspector (Edge)` 或 `Debug SSE in Inspector (Chrome)`，按 F5 開始除錯。<br>4. MCP Inspector 在瀏覽器啟動後，點擊 `Connect` 按鈕連接此 MCP Server。<br>5. 接著你可以 `List Tools`，選擇工具，輸入參數，並 `Run Tool` 來除錯伺服器程式碼。<br> |

## 預設埠號與自訂設定

| 除錯模式 | 埠號 | 定義檔 | 自訂方式 | 備註 |
| ---------- | ----- | ------------ | -------------- |-------------- |
| Agent Builder | 3001 | [tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json) | 編輯 [launch.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/launch.json)、[tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json)、[__init__.py](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/src/__init__.py)、[mcp.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.aitk/mcp.json) 來更改上述埠號。 | 無 |
| MCP Inspector | 3001（伺服器）；5173 和 3000（Inspector） | [tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json) | 編輯 [launch.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/launch.json)、[tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json)、[__init__.py](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/src/__init__.py)、[mcp.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.aitk/mcp.json) 來更改上述埠號。 | 無 |

## 回饋

如果你對此範本有任何回饋或建議，請在 [AI Toolkit GitHub repository](https://github.com/microsoft/vscode-ai-toolkit/issues) 開啟 issue。

**免責聲明**：  
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或誤釋承擔責任。