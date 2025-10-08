<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "f5300fd1b5e84520d500b2a8f568a1d8",
  "translation_date": "2025-07-16T23:12:57+00:00",
  "source_file": "02-Security/azure-content-safety.md",
  "language_code": "hk"
}
-->
# 使用 Azure Content Safety 強化 MCP 安全性

Azure Content Safety 提供多種強大工具，能提升你 MCP 實作的安全防護：

## Prompt Shields

Microsoft 的 AI Prompt Shields 透過以下方式，有效防範直接及間接的提示注入攻擊：

1. **先進偵測**：利用機器學習辨識內容中隱藏的惡意指令。
2. **聚焦處理**：轉換輸入文字，協助 AI 系統分辨有效指令與外部輸入。
3. **分隔符與資料標記**：標示可信與不可信資料的界線。
4. **內容安全整合**：結合 Azure AI Content Safety 偵測越獄嘗試及有害內容。
5. **持續更新**：Microsoft 定期更新防護機制，應對新興威脅。

## 在 MCP 中實作 Azure Content Safety

此方法提供多層防護：
- 處理前掃描輸入
- 回傳前驗證輸出
- 使用封鎖清單過濾已知有害模式
- 利用 Azure 持續更新的內容安全模型

## Azure Content Safety 資源

想了解如何在 MCP 伺服器中實作 Azure Content Safety，請參考以下官方資源：

1. [Azure AI Content Safety Documentation](https://learn.microsoft.com/azure/ai-services/content-safety/) - Azure Content Safety 官方文件。
2. [Prompt Shield Documentation](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/prompt-shield) - 學習如何防止提示注入攻擊。
3. [Content Safety API Reference](https://learn.microsoft.com/rest/api/contentsafety/) - 內容安全 API 詳細參考。
4. [Quickstart: Azure Content Safety with C#](https://learn.microsoft.com/azure/ai-services/content-safety/quickstart-csharp) - 使用 C# 的快速入門指南。
5. [Content Safety Client Libraries](https://learn.microsoft.com/azure/ai-services/content-safety/quickstart-client-libraries-rest-api) - 各種程式語言的用戶端函式庫。
6. [Detecting Jailbreak Attempts](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - 偵測及防止越獄嘗試的專門指引。
7. [Best Practices for Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/best-practices) - 有效實作內容安全的最佳實務。

如需更深入的實作說明，請參閱我們的 [Azure Content Safety Implementation guide](./azure-content-safety-implementation.md)。

**免責聲明**：  
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或誤釋承擔責任。