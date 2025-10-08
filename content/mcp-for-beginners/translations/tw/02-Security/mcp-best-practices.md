<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T10:39:40+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "tw"
}
-->
# MCP 安全最佳實踐 2025

本指南全面概述了基於最新 **MCP 規範 2025-06-18** 和當前行業標準的 Model Context Protocol (MCP) 系統實施的關鍵安全最佳實踐。這些實踐涵蓋了傳統安全問題以及 MCP 部署中獨特的 AI 特定威脅。

## 關鍵安全要求

### 強制性安全控制（MUST 要求）

1. **令牌驗證**：MCP 伺服器 **絕不可** 接受任何未明確為 MCP 伺服器本身簽發的令牌。
2. **授權驗證**：實施授權的 MCP 伺服器 **必須** 驗證所有入站請求，並且 **絕不可** 使用會話進行身份驗證。
3. **用戶同意**：使用靜態客戶端 ID 的 MCP 代理伺服器 **必須** 為每個動態註冊的客戶端獲得明確的用戶同意。
4. **安全會話 ID**：MCP 伺服器 **必須** 使用加密安全的、非確定性的會話 ID，並通過安全的隨機數生成器生成。

## 核心安全實踐

### 1. 輸入驗證與清理
- **全面輸入驗證**：驗證並清理所有輸入，以防止注入攻擊、混淆代理問題以及提示注入漏洞。
- **參數模式強制**：對所有工具參數和 API 輸入實施嚴格的 JSON 模式驗證。
- **內容過濾**：使用 Microsoft Prompt Shields 和 Azure Content Safety 過濾提示和響應中的惡意內容。
- **輸出清理**：在向用戶或下游系統展示之前，驗證並清理所有模型輸出。

### 2. 身份驗證與授權卓越
- **外部身份提供者**：將身份驗證委託給成熟的身份提供者（如 Microsoft Entra ID、OAuth 2.1 提供者），而非實施自定義身份驗證。
- **細粒度權限**：根據最小權限原則，實施工具特定的細粒度權限。
- **令牌生命周期管理**：使用短期訪問令牌，並進行安全輪換和正確的受眾驗證。
- **多因素身份驗證**：要求所有管理訪問和敏感操作使用 MFA。

### 3. 安全通信協議
- **傳輸層安全**：對所有 MCP 通信使用 HTTPS/TLS 1.3，並進行正確的證書驗證。
- **端到端加密**：對在傳輸和靜態存儲的高度敏感數據實施額外的加密層。
- **證書管理**：通過自動更新流程維護正確的證書生命周期管理。
- **協議版本強制**：使用當前 MCP 協議版本（2025-06-18），並進行正確的版本協商。

### 4. 高級速率限制與資源保護
- **多層速率限制**：在用戶、會話、工具和資源層面實施速率限制，以防止濫用。
- **自適應速率限制**：使用基於機器學習的速率限制，根據使用模式和威脅指標進行調整。
- **資源配額管理**：為計算資源、內存使用和執行時間設置適當的限制。
- **DDoS 保護**：部署全面的 DDoS 保護和流量分析系統。

### 5. 全面日誌記錄與監控
- **結構化審計日誌**：為所有 MCP 操作、工具執行和安全事件實施詳細且可搜索的日誌。
- **實時安全監控**：部署具有 AI 驅動異常檢測功能的 SIEM 系統，用於 MCP 工作負載。
- **隱私合規日誌記錄**：在尊重數據隱私要求和法規的同時記錄安全事件。
- **事件響應集成**：將日誌系統連接到自動化事件響應工作流程。

### 6. 增強的安全存儲實踐
- **硬件安全模塊**：使用 HSM 支持的密鑰存儲（如 Azure Key Vault、AWS CloudHSM）進行關鍵加密操作。
- **加密密鑰管理**：實施正確的密鑰輪換、隔離和訪問控制。
- **秘密管理**：將所有 API 密鑰、令牌和憑據存儲在專用的秘密管理系統中。
- **數據分類**：根據敏感性級別對數據進行分類，並採取適當的保護措施。

### 7. 高級令牌管理
- **禁止令牌透傳**：明確禁止繞過安全控制的令牌透傳模式。
- **受眾驗證**：始終驗證令牌的受眾聲明是否與預期的 MCP 伺服器身份匹配。
- **基於聲明的授權**：基於令牌聲明和用戶屬性實施細粒度授權。
- **令牌綁定**：在適當情況下將令牌綁定到特定的會話、用戶或設備。

### 8. 安全會話管理
- **加密會話 ID**：使用加密安全的隨機數生成器生成會話 ID（非可預測序列）。
- **用戶特定綁定**：使用安全格式（如 `<user_id>:<session_id>`）將會話 ID 綁定到用戶特定信息。
- **會話生命周期控制**：實施正確的會話過期、輪換和失效機制。
- **會話安全標頭**：使用適當的 HTTP 安全標頭保護會話。

### 9. AI 特定安全控制
- **提示注入防禦**：部署 Microsoft Prompt Shields，並使用聚焦、分隔符和數據標記技術。
- **工具中毒防範**：驗證工具元數據，監控動態變更，並檢查工具完整性。
- **模型輸出驗證**：掃描模型輸出是否存在潛在數據洩漏、有害內容或安全政策違規。
- **上下文窗口保護**：實施控制措施以防止上下文窗口中毒和操縱攻擊。

### 10. 工具執行安全
- **執行沙盒**：在容器化、隔離的環境中運行工具執行，並設置資源限制。
- **特權分離**：以最低必要特權執行工具，並使用獨立的服務帳戶。
- **網絡隔離**：對工具執行環境實施網絡分段。
- **執行監控**：監控工具執行的異常行為、資源使用和安全違規。

### 11. 持續安全驗證
- **自動化安全測試**：將安全測試集成到 CI/CD 管道中，使用如 GitHub Advanced Security 的工具。
- **漏洞管理**：定期掃描所有依賴項，包括 AI 模型和外部服務。
- **滲透測試**：定期進行專門針對 MCP 實施的安全評估。
- **安全代碼審查**：對所有 MCP 相關代碼更改實施強制性安全審查。

### 12. AI 供應鏈安全
- **組件驗證**：驗證所有 AI 組件（模型、嵌入、API）的來源、完整性和安全性。
- **依賴項管理**：維護所有軟件和 AI 依賴項的最新清單，並進行漏洞跟踪。
- **可信存儲庫**：使用已驗證的可信來源獲取所有 AI 模型、庫和工具。
- **供應鏈監控**：持續監控 AI 服務提供商和模型存儲庫中的妥協情況。

## 高級安全模式

### MCP 零信任架構
- **永不信任，始終驗證**：對所有 MCP 參與者實施持續驗證。
- **微分段**：使用細粒度的網絡和身份控制隔離 MCP 組件。
- **條件訪問**：實施基於風險的訪問控制，根據上下文和行為進行調整。
- **持續風險評估**：根據當前威脅指標動態評估安全狀態。

### 隱私保護的 AI 實施
- **數據最小化**：僅暴露每個 MCP 操作所需的最低數據。
- **差分隱私**：對敏感數據處理實施隱私保護技術。
- **同態加密**：使用高級加密技術實現加密數據上的安全計算。
- **聯邦學習**：實施分佈式學習方法，保護數據的本地性和隱私。

### AI 系統事件響應
- **AI 特定事件程序**：制定針對 AI 和 MCP 特定威脅的事件響應程序。
- **自動化響應**：對常見 AI 安全事件實施自動化遏制和修復。
- **取證能力**：為 AI 系統妥協和數據洩漏保持取證準備。
- **恢復程序**：建立從 AI 模型中毒、提示注入攻擊和服務妥協中恢復的程序。

## 實施資源與標準

### 官方 MCP 文檔
- [MCP 規範 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - 當前 MCP 協議規範
- [MCP 安全最佳實踐](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - 官方安全指導
- [MCP 授權規範](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - 身份驗證和授權模式
- [MCP 傳輸安全](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - 傳輸層安全要求

### Microsoft 安全解決方案
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - 高級提示注入保護
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - 全面 AI 內容過濾
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - 企業身份和訪問管理
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - 安全的秘密和憑據管理
- [GitHub Advanced Security](https://github.com/security/advanced-security) - 供應鏈和代碼安全掃描

### 安全標準與框架
- [OAuth 2.1 安全最佳實踐](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - 當前 OAuth 安全指導
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - 網絡應用安全風險
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI 特定安全風險
- [NIST AI 風險管理框架](https://www.nist.gov/itl/ai-risk-management-framework) - 全面 AI 風險管理
- [ISO 27001:2022](https://www.iso.org/standard/27001) - 信息安全管理系統

### 實施指南與教程
- [Azure API Management 作為 MCP 授權網關](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - 企業身份驗證模式
- [Microsoft Entra ID 與 MCP 伺服器](https://den.dev/blog/mcp-server-auth-entra-id-session/) - 身份提供者集成
- [安全令牌存儲實施](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - 令牌管理最佳實踐
- [AI 的端到端加密](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - 高級加密模式

### 高級安全資源
- [Microsoft 安全開發生命周期](https://www.microsoft.com/sdl) - 安全開發實踐
- [AI 紅隊指導](https://learn.microsoft.com/security/ai-red-team/) - AI 特定安全測試
- [AI 系統威脅建模](https://learn.microsoft.com/security/adoption/approach/threats-ai) - AI 威脅建模方法
- [AI 隱私工程](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - 隱私保護 AI 技術

### 合規與治理
- [AI 的 GDPR 合規](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - AI 系統中的隱私合規
- [AI 治理框架](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - 負責任的 AI 實施
- [AI 服務的 SOC 2](https://learn.microsoft.com/compliance/regulatory/offering-soc) - AI 服務提供商的安全控制
- [AI 的 HIPAA 合規](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - 醫療 AI 合規要求

### DevSecOps 與自動化
- [AI 的 DevSecOps 管道](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - 安全的 AI 開發管道
- [自動化安全測試](https://learn.microsoft.com/security/engineering/devsecops) - 持續安全驗證
- [基礎設施即代碼安全](https://learn.microsoft.com/security/engineering/infrastructure-security) - 安全的基礎設施部署
- [AI 的容器安全](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - AI 工作負載容器化安全

### 監控與事件響應
- [Azure Monitor 用於 AI 工作負載](https://learn.microsoft.com/azure/azure-monitor/overview) - 全面監控解決方案
- [AI 安全事件響應](https://learn.microsoft.com/security/compass/incident-response-playbooks) - AI 特定事件程序
- [AI 系統的 SIEM](https://learn.microsoft.com/azure/sentinel/overview) - 安全信息和事件管理
- [AI 的威脅情報](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - AI 威脅情報來源

## 🔄 持續改進

### 跟上標準的演變
- **MCP 規範更新**：監控官方 MCP 規範變更和安全公告。
- **威脅情報**：訂閱 AI 安全威脅源和漏洞數據庫。
- **社區參與**：參與 MCP 安全社區討論和工作組。
- **定期評估**：每季度進行安全狀態評估並相應更新實踐。

### 為 MCP 安全做出貢獻
- **安全研究**：參與 MCP 安全研究和漏洞披露計劃。
- **最佳實踐分享**：與社區分享安全實施和經驗教訓。
- **標準開發**：參與 MCP 規範開發和安全標準創建。
- **工具開發**：開發並分享適用於 MCP 生態系統的安全工具和函式庫

---

*本文件反映截至 2025 年 8 月 18 日的 MCP 安全最佳實踐，基於 MCP 規範 2025-06-18。隨著協議和威脅環境的演變，安全實踐應定期檢視並更新。*

**免責聲明**：  
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。我們致力於提供準確的翻譯，但請注意，自動翻譯可能包含錯誤或不準確之處。應以原始語言的文件作為權威來源。對於關鍵資訊，建議尋求專業人工翻譯。我們對於因使用此翻譯而產生的任何誤解或錯誤解讀概不負責。