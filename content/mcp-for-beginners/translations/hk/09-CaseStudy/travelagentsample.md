<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d3415b9d2bf58bc69be07f945a69e07",
  "translation_date": "2025-07-14T05:56:10+00:00",
  "source_file": "09-CaseStudy/travelagentsample.md",
  "language_code": "hk"
}
-->
# 案例研究：Azure AI 旅遊代理 – 參考實作

## 概覽

[Azure AI Travel Agents](https://github.com/Azure-Samples/azure-ai-travel-agents) 是由微軟開發的完整參考解決方案，展示如何利用 Model Context Protocol (MCP)、Azure OpenAI 及 Azure AI Search 建立多代理、AI 驅動的旅遊規劃應用程式。此專案示範了多個 AI 代理的協調最佳實踐、企業資料整合，以及提供安全且可擴充的平台以應對真實世界場景。

## 主要功能
- **多代理協調：** 利用 MCP 協調專門代理（如航班、酒店及行程代理），共同完成複雜的旅遊規劃任務。
- **企業資料整合：** 連接 Azure AI Search 及其他企業資料來源，提供最新且相關的旅遊建議資訊。
- **安全且可擴展的架構：** 採用 Azure 服務進行身份驗證、授權及可擴展部署，遵循企業安全最佳實務。
- **可擴充工具：** 實作可重用的 MCP 工具及提示範本，快速適應新領域或業務需求。
- **使用者體驗：** 提供由 Azure OpenAI 及 MCP 支援的對話介面，讓使用者與旅遊代理互動。

## 架構
![Architecture](https://raw.githubusercontent.com/Azure-Samples/azure-ai-travel-agents/main/docs/ai-travel-agents-architecture-diagram.png)

### 架構圖說明

Azure AI Travel Agents 解決方案的架構設計強調模組化、可擴展性及多個 AI 代理與企業資料來源的安全整合。主要元件及資料流程如下：

- **使用者介面：** 使用者透過對話式 UI（如網頁聊天或 Teams 機器人）與系統互動，發送查詢並接收旅遊建議。
- **MCP 伺服器：** 作為中央協調者，接收使用者輸入、管理上下文，並透過 Model Context Protocol 協調專門代理（如 FlightAgent、HotelAgent、ItineraryAgent）的行動。
- **AI 代理：** 每個代理負責特定領域（航班、酒店、行程），以 MCP 工具形式實作，利用提示範本及邏輯處理請求並產生回應。
- **Azure OpenAI 服務：** 提供先進的自然語言理解與生成，協助代理解讀使用者意圖並產生對話式回應。
- **Azure AI Search 及企業資料：** 代理查詢 Azure AI Search 及其他企業資料來源，取得最新的航班、酒店及旅遊選項資訊。
- **身份驗證與安全：** 整合 Microsoft Entra ID 進行安全身份驗證，並對所有資源實施最小權限存取控制。
- **部署：** 設計於 Azure Container Apps 上部署，確保可擴展性、監控及運營效率。

此架構實現多個 AI 代理的無縫協調、企業資料的安全整合，以及建構領域專屬 AI 解決方案的穩健且可擴充平台。

## 架構圖逐步說明
想像你正在規劃一趟大型旅程，有一隊專家助理幫你處理每個細節。Azure AI Travel Agents 系統的運作方式類似，使用不同的部分（就像團隊成員）各司其職。以下是整體運作方式：

### 使用者介面 (UI)：
把它想像成你的旅遊代理櫃台。你（使用者）在這裡提出問題或需求，例如「幫我找一班飛往巴黎的航班」。這可以是網站上的聊天視窗或通訊應用程式。

### MCP 伺服器（協調者）：
MCP 伺服器就像櫃台的經理，聽取你的需求並決定由哪位專家負責處理。它會追蹤對話內容，確保流程順暢。

### AI 代理（專家助理）：
每位代理都是特定領域的專家——有的專精航班，有的專精酒店，還有的專精行程規劃。當你提出旅遊需求時，MCP 伺服器會將請求分派給適合的代理。這些代理利用自身知識和工具，為你尋找最佳方案。

### Azure OpenAI 服務（語言專家）：
就像有位語言專家能準確理解你說的話，不論你怎麼表達。它幫助代理理解你的需求，並以自然、對話式的語言回應。

### Azure AI Search 及企業資料（資訊圖書館）：
想像一座龐大且最新的圖書館，收藏所有最新的旅遊資訊——航班時刻、酒店空房等。代理會在這裡搜尋，為你提供最精確的答案。

### 身份驗證與安全（保安）：
就像保安檢查誰能進入特定區域，這部分確保只有授權的人員和代理能存取敏感資訊，保障你的資料安全與隱私。

### 部署於 Azure Container Apps（大樓）：
所有助理和工具都在一棟安全且可擴展的大樓（雲端）內協同工作。這代表系統能同時處理大量使用者，並隨時可用。

## 整體運作流程：

你從櫃台（UI）提出問題。
經理（MCP 伺服器）判斷由哪位專家（代理）協助。
專家利用語言專家（OpenAI）理解需求，並透過圖書館（AI Search）尋找最佳答案。
保安（身份驗證）確保一切安全無虞。
所有流程都在可靠且可擴展的大樓（Azure Container Apps）內進行，讓你的體驗順暢且安全。
這種團隊合作讓系統能快速且安全地協助你規劃旅程，就像一群專業旅遊代理在現代辦公室中協同工作！

## 技術實作
- **MCP 伺服器：** 承載核心協調邏輯，公開代理工具，並管理多步驟旅遊規劃工作流程的上下文。
- **代理：** 每個代理（如 FlightAgent、HotelAgent）以 MCP 工具形式實作，擁有自己的提示範本及邏輯。
- **Azure 整合：** 使用 Azure OpenAI 進行自然語言理解，並利用 Azure AI Search 進行資料檢索。
- **安全性：** 整合 Microsoft Entra ID 進行身份驗證，並對所有資源實施最小權限存取控制。
- **部署：** 支援部署至 Azure Container Apps，以確保可擴展性及運營效率。

## 成果與影響
- 展示 MCP 如何在真實、具生產等級的場景中協調多個 AI 代理。
- 透過提供可重用的代理協調、資料整合及安全部署模式，加速解決方案開發。
- 作為使用 MCP 及 Azure 服務建構領域專屬 AI 應用的藍圖。

## 參考資料
- [Azure AI Travel Agents GitHub Repository](https://github.com/Azure-Samples/azure-ai-travel-agents)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
- [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

**免責聲明**：  
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或誤釋承擔責任。