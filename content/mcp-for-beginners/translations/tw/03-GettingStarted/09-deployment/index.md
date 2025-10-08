<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1d9dc83260576b76f272d330ed93c51f",
  "translation_date": "2025-07-13T22:06:51+00:00",
  "source_file": "03-GettingStarted/09-deployment/README.md",
  "language_code": "tw"
}
-->
# 部署 MCP 伺服器

部署您的 MCP 伺服器可以讓其他人超越本地環境，存取其工具和資源。根據您對擴展性、可靠性和管理便利性的需求，有多種部署策略可供選擇。以下將提供在本地、容器以及雲端部署 MCP 伺服器的指引。

## 概覽

本課程將介紹如何部署您的 MCP Server 應用程式。

## 學習目標

完成本課程後，您將能夠：

- 評估不同的部署方式。
- 部署您的應用程式。

## 本地開發與部署

如果您的伺服器是要在使用者機器上執行並被使用，您可以依照以下步驟：

1. **下載伺服器**。如果您不是自行撰寫伺服器，請先將其下載到您的機器。  
1. **啟動伺服器程序**：執行您的 MCP 伺服器應用程式。

針對 SSE（stdio 類型伺服器不需要）：

1. **設定網路**：確保伺服器在預期的埠口可被存取。  
1. **連接客戶端**：使用像是 `http://localhost:3000` 的本地連線 URL。

## 雲端部署

MCP 伺服器可以部署到多種雲端平台：

- **無伺服器函式**：將輕量級 MCP 伺服器部署為無伺服器函式。  
- **容器服務**：使用 Azure Container Apps、AWS ECS 或 Google Cloud Run 等服務。  
- **Kubernetes**：在 Kubernetes 叢集部署並管理 MCP 伺服器，以達到高可用性。

### 範例：Azure Container Apps

Azure Container Apps 支援部署 MCP 伺服器。此功能仍在開發中，目前支援 SSE 伺服器。

以下是操作步驟：

1. 複製一個 repo：

  ```sh
  git clone https://github.com/anthonychu/azure-container-apps-mcp-sample.git
  ```

1. 在本地執行以測試：

  ```sh
  uv venv
  uv sync

  # linux/macOS
  export API_KEYS=<AN_API_KEY>
  # windows
  set API_KEYS=<AN_API_KEY>

  uv run fastapi dev main.py
  ```

1. 若要在本地嘗試，請在 *.vscode* 目錄下建立 *mcp.json* 檔案，並加入以下內容：

  ```json
  {
      "inputs": [
          {
              "type": "promptString",
              "id": "weather-api-key",
              "description": "Weather API Key",
              "password": true
          }
      ],
      "servers": {
          "weather-sse": {
              "type": "sse",
              "url": "http://localhost:8000/sse",
              "headers": {
                  "x-api-key": "${input:weather-api-key}"
              }
          }
      }
  }
  ```

  SSE 伺服器啟動後，您可以點擊 JSON 檔案中的播放圖示，您應該會看到 GitHub Copilot 偵測到伺服器上的工具，並顯示工具圖示。

1. 部署時，執行以下指令：

  ```sh
  az containerapp up -g <RESOURCE_GROUP_NAME> -n weather-mcp --environment mcp -l westus --env-vars API_KEYS=<AN_API_KEY> --source .
  ```

就這樣，您可以透過這些步驟在本地或 Azure 上部署。

## 其他資源

- [Azure Functions + MCP](https://learn.microsoft.com/en-us/samples/azure-samples/remote-mcp-functions-dotnet/remote-mcp-functions-dotnet/)
- [Azure Container Apps 文章](https://techcommunity.microsoft.com/blog/appsonazureblog/host-remote-mcp-servers-in-azure-container-apps/4403550)
- [Azure Container Apps MCP repo](https://github.com/anthonychu/azure-container-apps-mcp-sample)

## 接下來

- 下一步：[實務應用](../../04-PracticalImplementation/README.md)

**免責聲明**：  
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保翻譯的準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤譯負責。