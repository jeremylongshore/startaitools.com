<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T10:45:57+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "hk"
}
-->
# MCP 安全最佳實踐 - 2025 年 8 月更新

> **重要事項**：本文檔反映了最新的 [MCP 規範 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) 安全要求以及官方的 [MCP 安全最佳實踐](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)。請務必參考當前規範以獲取最新的指導。

## MCP 實現的基本安全實踐

模型上下文協議（MCP）帶來了超越傳統軟件安全的獨特安全挑戰。這些實踐涵蓋了基礎安全要求以及 MCP 特有的威脅，包括提示注入、工具污染、會話劫持、混淆代理問題和令牌傳遞漏洞。

### **強制性安全要求**

**MCP 規範中的關鍵要求：**

> **不得**：MCP 伺服器 **不得** 接受任何未明確為 MCP 伺服器簽發的令牌  
> 
> **必須**：實現授權的 MCP 伺服器 **必須** 驗證所有入站請求  
>  
> **不得**：MCP 伺服器 **不得** 使用會話進行身份驗證  
>
> **必須**：使用靜態客戶端 ID 的 MCP 代理伺服器 **必須** 為每個動態註冊的客戶端獲取用戶同意  

---

## 1. **令牌安全與身份驗證**

**身份驗證與授權控制：**
   - **嚴格的授權審查**：全面審核 MCP 伺服器的授權邏輯，確保只有預期的用戶和客戶端能夠訪問資源  
   - **外部身份提供者集成**：使用如 Microsoft Entra ID 等成熟的身份提供者，而非自行實現身份驗證  
   - **令牌受眾驗證**：始終驗證令牌是否明確為您的 MCP 伺服器簽發 - 絕不接受上游令牌  
   - **正確的令牌生命周期管理**：實現安全的令牌輪換、過期策略，並防止令牌重放攻擊  

**受保護的令牌存儲：**
   - 使用 Azure Key Vault 或類似的安全憑證存儲來存儲所有機密  
   - 實現令牌在靜態和傳輸中的加密  
   - 定期輪換憑證並監控未經授權的訪問  

## 2. **會話管理與傳輸安全**

**安全的會話實踐：**
   - **加密安全的會話 ID**：使用安全的、非確定性的會話 ID，並通過安全隨機數生成器生成  
   - **用戶特定綁定**：將會話 ID 綁定到用戶身份，例如使用 `<user_id>:<session_id>` 格式，以防止跨用戶會話濫用  
   - **會話生命周期管理**：實現適當的過期、輪換和失效機制，以限制漏洞窗口  
   - **強制 HTTPS/TLS**：所有通信必須使用 HTTPS 以防止會話 ID 被攔截  

**傳輸層安全：**
   - 優先配置 TLS 1.3，並進行適當的證書管理  
   - 為關鍵連接實現證書釘扎  
   - 定期輪換證書並驗證其有效性  

## 3. **AI 特有威脅防護** 🤖

**提示注入防禦：**
   - **Microsoft Prompt Shields**：部署 AI Prompt Shields 以檢測和過濾惡意指令  
   - **輸入清理**：驗證並清理所有輸入，以防止注入攻擊和混淆代理問題  
   - **內容邊界**：使用分隔符和數據標記系統來區分受信指令和外部內容  

**工具污染預防：**
   - **工具元數據驗證**：實施工具定義的完整性檢查，並監控意外更改  
   - **動態工具監控**：監控運行時行為，並設置異常執行模式的警報  
   - **批准工作流**：要求用戶明確批准工具修改和功能更改  

## 4. **訪問控制與權限管理**

**最小權限原則：**
   - 僅為 MCP 伺服器授予執行功能所需的最低權限  
   - 實現基於角色的訪問控制（RBAC），並設置細粒度的權限  
   - 定期審查權限，並持續監控權限提升  

**運行時權限控制：**
   - 設置資源限制以防止資源耗盡攻擊  
   - 使用容器隔離工具執行環境  
   - 為管理功能實現按需訪問  

## 5. **內容安全與監控**

**內容安全實現：**
   - **Azure Content Safety 集成**：使用 Azure Content Safety 檢測有害內容、越獄嘗試和政策違規  
   - **行為分析**：實現運行時行為監控，以檢測 MCP 伺服器和工具執行中的異常  
   - **全面日誌記錄**：安全、不可篡改地記錄所有身份驗證嘗試、工具調用和安全事件  

**持續監控：**
   - 實時警報以應對可疑模式和未經授權的訪問嘗試  
   - 與 SIEM 系統集成以集中管理安全事件  
   - 定期對 MCP 實現進行安全審核和滲透測試  

## 6. **供應鏈安全**

**組件驗證：**
   - **依賴性掃描**：對所有軟件依賴項和 AI 組件進行自動漏洞掃描  
   - **來源驗證**：驗證模型、數據源和外部服務的來源、許可和完整性  
   - **簽名包**：使用加密簽名的包，並在部署前驗證簽名  

**安全開發管道：**
   - **GitHub 高級安全**：實現密鑰掃描、依賴性分析和 CodeQL 靜態分析  
   - **CI/CD 安全**：在自動部署管道中集成安全驗證  
   - **工件完整性**：對部署的工件和配置進行加密驗證  

## 7. **OAuth 安全與混淆代理預防**

**OAuth 2.1 實現：**
   - **PKCE 實現**：對所有授權請求使用 Proof Key for Code Exchange (PKCE)  
   - **明確同意**：為每個動態註冊的客戶端獲取用戶同意，以防止混淆代理攻擊  
   - **重定向 URI 驗證**：對重定向 URI 和客戶端標識符進行嚴格驗證  

**代理安全：**
   - 防止通過靜態客戶端 ID 利用進行授權繞過  
   - 為第三方 API 訪問實現適當的同意工作流  
   - 監控授權碼盜竊和未經授權的 API 訪問  

## 8. **事件響應與恢復**

**快速響應能力：**
   - **自動化響應**：實現自動化系統以進行憑證輪換和威脅遏制  
   - **回滾程序**：能夠快速恢復到已知的良好配置和組件  
   - **取證能力**：提供詳細的審計記錄和日誌以進行事件調查  

**溝通與協調：**
   - 明確的安全事件升級程序  
   - 與組織事件響應團隊集成  
   - 定期進行安全事件模擬和桌面演練  

## 9. **合規與治理**

**法規合規：**
   - 確保 MCP 實現符合行業特定要求（如 GDPR、HIPAA、SOC 2）  
   - 為 AI 數據處理實現數據分類和隱私控制  
   - 維護全面的文檔以供合規審計  

**變更管理：**
   - 對所有 MCP 系統修改進行正式的安全審查流程  
   - 配置更改的版本控制和批准工作流  
   - 定期進行合規評估和差距分析  

## 10. **高級安全控制**

**零信任架構：**
   - **永不信任，始終驗證**：持續驗證用戶、設備和連接  
   - **微分段**：對 MCP 組件進行細粒度的網絡控制隔離  
   - **條件訪問**：基於風險的訪問控制，根據當前上下文和行為進行調整  

**運行時應用保護：**
   - **運行時應用自我保護 (RASP)**：部署 RASP 技術以實時檢測威脅  
   - **應用性能監控**：監控性能異常，這可能表明存在攻擊  
   - **動態安全策略**：根據當前威脅形勢調整安全策略  

## 11. **Microsoft 安全生態系統集成**

**全面的 Microsoft 安全解決方案：**
   - **Microsoft Defender for Cloud**：為 MCP 工作負載提供雲安全態勢管理  
   - **Azure Sentinel**：雲原生 SIEM 和 SOAR 功能，用於高級威脅檢測  
   - **Microsoft Purview**：為 AI 工作流和數據源提供數據治理和合規性  

**身份與訪問管理：**
   - **Microsoft Entra ID**：企業身份管理，支持條件訪問策略  
   - **特權身份管理 (PIM)**：按需訪問和管理功能的批准工作流  
   - **身份保護**：基於風險的條件訪問和自動化威脅響應  

## 12. **持續安全演進**

**保持最新：**
   - **規範監控**：定期審查 MCP 規範更新和安全指導變更  
   - **威脅情報**：集成 AI 特有的威脅源和妥協指標  
   - **安全社區參與**：積極參與 MCP 安全社區和漏洞披露計劃  

**自適應安全：**
   - **機器學習安全**：使用基於 ML 的異常檢測來識別新型攻擊模式  
   - **預測性安全分析**：實現預測模型以主動識別威脅  
   - **安全自動化**：根據威脅情報和規範變更自動更新安全策略  

---

## **關鍵安全資源**

### **官方 MCP 文檔**
- [MCP 規範 (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP 安全最佳實踐](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP 授權規範](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft 安全解決方案**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID 安全](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub 高級安全](https://github.com/security/advanced-security)  

### **安全標準**
- [OAuth 2.0 安全最佳實踐 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP 大型語言模型十大安全風險](https://genai.owasp.org/)  
- [NIST AI 風險管理框架](https://www.nist.gov/itl/ai-risk-management-framework)  

### **實現指南**
- [Azure API Management MCP 身份驗證網關](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID 與 MCP 伺服器](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **安全提示**：MCP 安全實踐發展迅速。在實現之前，請始終根據當前的 [MCP 規範](https://spec.modelcontextprotocol.io/) 和 [官方安全文檔](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) 進行驗證。

**免責聲明**：  
此文件已使用人工智能翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯。我們致力於提供準確的翻譯，但請注意，自動翻譯可能包含錯誤或不準確之處。應以原始語言的文件作為權威來源。對於關鍵資訊，建議尋求專業的人工作翻譯。我們對因使用此翻譯而引起的任何誤解或誤釋不承擔責任。