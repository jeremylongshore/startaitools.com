<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T14:35:19+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "mo"
}
-->
# MCP 安全性：AI 系統的全面保護

[![MCP 安全性最佳實踐](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.mo.png)](https://youtu.be/88No8pw706o)

_(點擊上方圖片觀看本課程影片)_

安全性是 AI 系統設計的基石，因此我們將其作為第二部分的重點，這與微軟的 [**Secure by Design**](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/) 原則一致。

模型上下文協議 (MCP) 為 AI 驅動的應用程式帶來了強大的新功能，但也引入了超越傳統軟體風險的獨特安全挑戰。MCP 系統面臨既有的安全問題（如安全編碼、最小權限、供應鏈安全）以及新的 AI 特定威脅，包括提示注入、工具污染、會話劫持、混淆代理攻擊、令牌傳遞漏洞和動態能力修改。

本課程將探討 MCP 實作中最關鍵的安全風險，涵蓋身份驗證、授權、過度權限、間接提示注入、會話安全性、混淆代理問題、令牌管理和供應鏈漏洞。您將學習如何採取行動控制措施和最佳實踐來減輕這些風險，同時利用微軟的解決方案（如 Prompt Shields、Azure Content Safety 和 GitHub Advanced Security）來加強您的 MCP 部署。

## 學習目標

完成本課程後，您將能夠：

- **識別 MCP 特定威脅**：了解 MCP 系統中的獨特安全風險，包括提示注入、工具污染、過度權限、會話劫持、混淆代理問題、令牌傳遞漏洞和供應鏈風險
- **應用安全控制措施**：實施有效的緩解措施，包括強健的身份驗證、最小權限訪問、安全令牌管理、會話安全控制和供應鏈驗證
- **利用微軟安全解決方案**：了解並部署 Microsoft Prompt Shields、Azure Content Safety 和 GitHub Advanced Security 來保護 MCP 工作負載
- **驗證工具安全性**：認識工具元數據驗證、動態變更監控以及防禦間接提示注入攻擊的重要性
- **整合最佳實踐**：將既有的安全基礎（如安全編碼、伺服器強化、零信任）與 MCP 特定控制措施結合，實現全面保護

# MCP 安全架構與控制措施

現代 MCP 實作需要分層的安全方法，既要應對傳統軟體安全問題，也要處理 AI 特定威脅。快速演進的 MCP 規範持續完善其安全控制，實現與企業安全架構和既有最佳實踐的更好整合。

根據 [Microsoft Digital Defense Report](https://aka.ms/mddr) 的研究，**98% 的已報告漏洞可通過強健的安全衛生措施預防**。最有效的保護策略是將基礎安全實踐與 MCP 特定控制措施結合起來——經證實的基線安全措施在降低整體安全風險方面仍然最具影響力。

## 當前安全形勢

> **注意**：此信息反映截至 **2025 年 8 月 18 日** 的 MCP 安全標準。MCP 協議正在快速演進，未來的實作可能會引入新的身份驗證模式和增強的控制措施。請始終參考最新的 [MCP 規範](https://spec.modelcontextprotocol.io/)、[MCP GitHub 儲存庫](https://github.com/modelcontextprotocol) 和 [安全最佳實踐文檔](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) 以獲取最新指導。

### MCP 身份驗證的演進

MCP 規範在身份驗證和授權方面經歷了顯著的演進：

- **早期方法**：早期規範要求開發者實作自定義身份驗證伺服器，MCP 伺服器作為 OAuth 2.0 授權伺服器直接管理用戶身份驗證
- **當前標準 (2025-06-18)**：更新的規範允許 MCP 伺服器將身份驗證委派給外部身份提供者（如 Microsoft Entra ID），提高了安全性並降低了實作複雜性
- **傳輸層安全性**：增強了對本地（STDIO）和遠端（Streamable HTTP）連接的安全傳輸機制支持，並採用適當的身份驗證模式

## 身份驗證與授權安全性

### 當前安全挑戰

現代 MCP 實作面臨多種身份驗證與授權挑戰：

### 風險與威脅向量

- **授權邏輯配置錯誤**：MCP 伺服器中的授權實作缺陷可能導致敏感數據暴露並錯誤地應用訪問控制
- **OAuth 令牌洩露**：本地 MCP 伺服器令牌被盜可能使攻擊者冒充伺服器並訪問下游服務
- **令牌傳遞漏洞**：不當的令牌處理可能導致安全控制繞過和責任缺失
- **過度權限**：權限過大的 MCP 伺服器違反最小權限原則，擴大了攻擊面

#### 令牌傳遞：一個關鍵的反模式

**令牌傳遞在當前 MCP 授權規範中被明確禁止**，因其帶來嚴重的安全影響：

##### 安全控制繞過
- MCP 伺服器和下游 API 實作的關鍵安全控制（如速率限制、請求驗證、流量監控）依賴於正確的令牌驗證
- 客戶端直接使用 API 令牌會繞過這些基本保護措施，破壞安全架構

##### 責任與審計挑戰  
- MCP 伺服器無法區分使用上游簽發令牌的客戶端，破壞審計追蹤
- 下游資源伺服器日誌顯示誤導性的請求來源，而非實際的 MCP 伺服器中介
- 事件調查和合規審計變得更加困難

##### 數據外洩風險
- 未經驗證的令牌聲明使得擁有被盜令牌的惡意行為者能將 MCP 伺服器作為代理進行數據外洩
- 信任邊界被破壞，允許未經授權的訪問模式繞過預期的安全控制

##### 多服務攻擊向量
- 被盜令牌被多個服務接受，允許在連接系統間進行橫向移動
- 當令牌來源無法驗證時，服務之間的信任假設可能被破壞

### 安全控制與緩解措施

**關鍵安全要求：**

> **強制性**：MCP 伺服器 **必須不接受** 任何未明確為 MCP 伺服器簽發的令牌

#### 身份驗證與授權控制

- **嚴格的授權審查**：對 MCP 伺服器授權邏輯進行全面審核，確保只有預期的用戶和客戶端能訪問敏感資源
  - **實作指南**：[Azure API Management 作為 MCP 伺服器的身份驗證網關](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **身份集成**：[使用 Microsoft Entra ID 進行 MCP 伺服器身份驗證](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **安全令牌管理**：實作 [微軟的令牌驗證與生命周期最佳實踐](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - 驗證令牌受眾聲明與 MCP 伺服器身份匹配
  - 實施適當的令牌輪換和過期策略
  - 防止令牌重放攻擊和未經授權使用

- **受保護的令牌存儲**：使用靜態和傳輸加密來保護令牌存儲
  - **最佳實踐**：[安全令牌存儲與加密指南](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### 訪問控制實作

- **最小權限原則**：僅授予 MCP 伺服器執行預期功能所需的最低權限
  - 定期進行權限審查和更新，以防止權限蔓延
  - **微軟文檔**：[安全的最小權限訪問](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **基於角色的訪問控制 (RBAC)**：實作細粒度的角色分配
  - 將角色嚴格限定於特定資源和操作
  - 避免擴大攻擊面的廣泛或不必要權限

- **持續權限監控**：實施持續的訪問審計和監控
  - 監控權限使用模式以檢測異常
  - 及時修正過度或未使用的權限

## AI 特定安全威脅

### 提示注入與工具操控攻擊

現代 MCP 實作面臨傳統安全措施無法完全應對的複雜 AI 特定攻擊向量：

#### **間接提示注入（跨域提示注入）**

**間接提示注入** 是 MCP 啟用的 AI 系統中最關鍵的漏洞之一。攻擊者將惡意指令嵌入外部內容（如文件、網頁、電子郵件或數據源），AI 系統隨後將其視為合法指令進行處理。

**攻擊場景：**
- **基於文件的注入**：隱藏在處理文件中的惡意指令，觸發非預期的 AI 行為
- **網頁內容利用**：受損網頁包含嵌入的提示，當被抓取時操控 AI 行為
- **基於電子郵件的攻擊**：電子郵件中的惡意提示導致 AI 助手洩露信息或執行未授權操作
- **數據源污染**：受損的數據庫或 API 向 AI 系統提供受污染的內容

**實際影響**：這些攻擊可能導致數據外洩、隱私洩露、生成有害內容以及操控用戶交互。詳細分析請參閱 [MCP 中的提示注入 (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)。

![提示注入攻擊圖示](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.mo.png)

#### **工具污染攻擊**

**工具污染** 針對定義 MCP 工具的元數據，利用 LLM 解讀工具描述和參數的方式來影響執行決策。

**攻擊機制：**
- **元數據操控**：攻擊者將惡意指令注入工具描述、參數定義或使用範例
- **隱形指令**：工具元數據中的隱藏提示被 AI 模型處理，但對人類用戶不可見
- **動態工具修改（"地毯拉動"）**：用戶批准的工具後續被修改為執行惡意操作，且用戶毫無察覺
- **參數注入**：嵌入工具參數架構中的惡意內容影響模型行為

**託管伺服器風險**：遠端 MCP 伺服器風險更高，因為工具定義可在初始用戶批准後更新，導致原本安全的工具變得惡意。詳細分析請參閱 [工具污染攻擊 (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)。

![工具注入攻擊圖示](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.mo.png)

#### **其他 AI 攻擊向量**

- **跨域提示注入 (XPIA)**：利用多個域的內容繞過安全控制的複雜攻擊
- **動態能力修改**：實時更改工具能力，逃避初始安全評估
- **上下文窗口污染**：操控大型上下文窗口以隱藏惡意指令
- **模型混淆攻擊**：利用模型限制創造不可預測或不安全的行為

### AI 安全風險影響

**高影響後果：**
- **數據外洩**：未經授權的訪問和敏感企業或個人數據的盜竊
- **隱私洩露**：暴露個人身份信息 (PII) 和機密業務數據  
- **系統操控**：對關鍵系統和工作流程的非預期修改
- **憑證盜竊**：身份驗證令牌和服務憑證的洩露
- **橫向移動**：利用受損的 AI 系統作為更廣泛網路攻擊的樞紐

### 微軟 AI 安全解決方案

#### **AI Prompt Shields：針對注入攻擊的高級保護**

微軟 **AI Prompt Shields** 通過多層安全防護提供針對直接和間接提示注入攻擊的全面防禦：

##### **核心保護機制：**

1. **高級檢測與過濾**
   - 機器學習算法和 NLP 技術檢測外部內容中的惡意指令
   - 實時分析文件、網頁、電子郵件和數據源中的嵌入威脅
   - 對合法與惡意提示模式的上下文理解

2. **聚焦技術**  
   - 區分受信系統指令與可能受損的外部輸入
   - 文本轉換方法增強模型相關性，同時隔離惡意內容
   - 幫助 AI 系統保持正確的指令層級，忽略注入的命令

3. **分隔符與數據標記系統**
   - 明確定義受信系統消息與外部輸入文本之間的邊界
   - 特殊標記突出顯示受信與不受信數據源之間的邊界
   - 清晰的分隔防止指令混淆和未經授權的命令執行

4. **持續威脅情報**
   - 微軟持續監控新興攻擊模式並更新防禦措施
   - 主動威脅狩獵以應對新的注入技術和攻擊向量
   - 定期更新安全模型以保持對演進威脅的有效性

5. **Azure Content Safety 集成**
   - 作為 Azure AI Content Safety 套件的一部分
   - 額外檢測越獄嘗試、有害內容和安全政策違規行為
   - 在 AI 應用組件間實現統一的安全控制

**實作資源**：[Microsoft Prompt Shields 文檔](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)

![Microsoft Prompt Shields 保護](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.mo.png)


## 高級 MCP 安全威脅

### 會話劫持漏洞

**會話劫持** 是狀態化 MCP 實作中的一個關鍵攻擊向量，未經授權的第三方獲取並濫用合法的會話標識符，冒充客戶端執行未經授權的操作。

#### **攻擊場景與風險**

- **會話劫持提示注入**：攻擊者使用被盜的會話 ID 向共享會話狀態的伺服器注入惡意事件，可能觸發有害操作或訪問敏感數據
- **直接冒充**：被盜的會話 ID 允許直接調用 MCP 伺服器，繞過身份驗證，將攻擊者視為合法用戶
- **受損的可恢復流**：攻擊者可以提前終止請求，導致合法客戶端在恢復時可能處理惡意內容

#### **會話管理的安全控制**

**關鍵要求：**
- **授權驗證**：實作授權的 MCP 伺服器 **必須驗證所有入站
- **安全會話生成**：使用加密安全、非決定性的會話 ID，並通過安全隨機數生成器生成  
- **用戶特定綁定**：使用類似 `<user_id>:<session_id>` 的格式將會話 ID 綁定到用戶特定信息，以防止跨用戶會話濫用  
- **會話生命周期管理**：實施適當的過期、輪換和失效機制，以縮短漏洞窗口  
- **傳輸安全**：所有通信必須使用 HTTPS，以防止會話 ID 被攔截  

### 混淆代理問題

**混淆代理問題**發生在 MCP 伺服器充當客戶端與第三方服務之間的身份驗證代理時，可能因靜態客戶端 ID 的濫用而導致授權繞過。

#### **攻擊機制與風險**

- **基於 Cookie 的同意繞過**：先前的用戶身份驗證會生成同意 Cookie，攻擊者可通過惡意授權請求和精心設計的重定向 URI 利用這些 Cookie  
- **授權碼竊取**：現有的同意 Cookie 可能導致授權伺服器跳過同意屏幕，將授權碼重定向到攻擊者控制的端點  
- **未授權的 API 訪問**：被竊取的授權碼可用於令牌交換，並在未經明確批准的情況下模仿用戶  

#### **緩解策略**

**強制性控制措施：**  
- **明確的同意要求**：使用靜態客戶端 ID 的 MCP 代理伺服器 **必須** 為每個動態註冊的客戶端獲得用戶同意  
- **OAuth 2.1 安全實施**：遵循最新的 OAuth 安全最佳實踐，包括所有授權請求的 PKCE（Proof Key for Code Exchange）  
- **嚴格的客戶端驗證**：實施對重定向 URI 和客戶端標識符的嚴格驗證，以防止濫用  

### 令牌透傳漏洞  

**令牌透傳**是一種明確的反模式，MCP 伺服器接受未經適當驗證的客戶端令牌並將其轉發到下游 API，違反 MCP 授權規範。

#### **安全影響**

- **控制繞過**：直接的客戶端到 API 令牌使用繞過了關鍵的速率限制、驗證和監控控制  
- **審計追蹤損壞**：上游簽發的令牌使客戶端身份無法識別，破壞事件調查能力  
- **基於代理的數據外洩**：未經驗證的令牌使惡意行為者能利用伺服器作為代理進行未授權的數據訪問  
- **信任邊界違反**：當令牌來源無法驗證時，下游服務的信任假設可能被破壞  
- **多服務攻擊擴展**：被攻擊的令牌在多個服務中被接受，可能導致橫向移動  

#### **必要的安全控制**

**不可協商的要求：**  
- **令牌驗證**：MCP 伺服器 **不得** 接受未明確為 MCP 伺服器簽發的令牌  
- **受眾驗證**：始終驗證令牌的受眾聲明是否與 MCP 伺服器的身份匹配  
- **正確的令牌生命周期**：實施短期有效的訪問令牌並採用安全的輪換機制  

## AI 系統的供應鏈安全

供應鏈安全已超越傳統軟件依賴，涵蓋整個 AI 生態系統。現代 MCP 實施必須嚴格驗證並監控所有 AI 相關組件，因為每個組件都可能引入漏洞，威脅系統完整性。

### 擴展的 AI 供應鏈組件

**傳統軟件依賴：**  
- 開源庫和框架  
- 容器映像和基礎系統  
- 開發工具和構建管道  
- 基礎設施組件和服務  

**AI 特定的供應鏈元素：**  
- **基礎模型**：來自不同提供商的預訓練模型，需要進行來源驗證  
- **嵌入服務**：外部向量化和語義搜索服務  
- **上下文提供者**：數據源、知識庫和文檔存儲庫  
- **第三方 API**：外部 AI 服務、ML 管道和數據處理端點  
- **模型工件**：權重、配置和微調模型變體  
- **訓練數據源**：用於模型訓練和微調的數據集  

### 全面的供應鏈安全策略

#### **組件驗證與信任**  
- **來源驗證**：在集成之前驗證所有 AI 組件的來源、許可和完整性  
- **安全評估**：對模型、數據源和 AI 服務進行漏洞掃描和安全審查  
- **聲譽分析**：評估 AI 服務提供商的安全記錄和實踐  
- **合規驗證**：確保所有組件符合組織的安全和監管要求  

#### **安全部署管道**  
- **自動化 CI/CD 安全**：在自動化部署管道中集成安全掃描  
- **工件完整性**：對所有部署的工件（代碼、模型、配置）實施加密驗證  
- **分階段部署**：使用漸進式部署策略，並在每個階段進行安全驗證  
- **可信工件存儲庫**：僅從已驗證的安全工件存儲庫和存儲庫中部署  

#### **持續監控與響應**  
- **依賴掃描**：對所有軟件和 AI 組件依賴進行持續漏洞監控  
- **模型監控**：持續評估模型行為、性能漂移和安全異常  
- **服務健康追蹤**：監控外部 AI 服務的可用性、安全事件和政策變更  
- **威脅情報集成**：整合針對 AI 和 ML 安全風險的威脅信息  

#### **訪問控制與最小權限**  
- **組件級別的權限**：根據業務需求限制對模型、數據和服務的訪問  
- **服務帳戶管理**：實施專用服務帳戶，並僅授予最低必要權限  
- **網絡分段**：隔離 AI 組件並限制服務之間的網絡訪問  
- **API 閘道控制**：使用集中式 API 閘道控制和監控對外部 AI 服務的訪問  

#### **事件響應與恢復**  
- **快速響應程序**：建立修補或替換受損 AI 組件的流程  
- **憑證輪換**：自動化系統，用於輪換密鑰、API 密鑰和服務憑證  
- **回滾能力**：能夠快速恢復到之前已知的良好版本的 AI 組件  
- **供應鏈漏洞恢復**：針對上游 AI 服務受損的特定響應程序  

### 微軟安全工具與集成

**GitHub 高級安全**提供全面的供應鏈保護，包括：  
- **密鑰掃描**：自動檢測存儲庫中的憑證、API 密鑰和令牌  
- **依賴掃描**：對開源依賴和庫進行漏洞評估  
- **CodeQL 分析**：靜態代碼分析，用於檢測安全漏洞和代碼問題  
- **供應鏈洞察**：提供依賴健康和安全狀態的可見性  

**Azure DevOps 和 Azure Repos 集成：**  
- 微軟開發平台上的無縫安全掃描集成  
- Azure Pipelines 中的 AI 工作負載自動安全檢查  
- 用於安全 AI 組件部署的策略執行  

**微軟內部實踐：**  
微軟在所有產品中實施了廣泛的供應鏈安全實踐。了解更多已驗證的方法：[微軟的軟件供應鏈安全之旅](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)  

## 基礎安全最佳實踐

MCP 實施繼承並建立在組織現有的安全基礎之上。加強基礎安全實踐可顯著提升 AI 系統和 MCP 部署的整體安全性。

### 核心安全基本原則

#### **安全開發實踐**  
- **OWASP 合規**：防範 [OWASP Top 10](https://owasp.org/www-project-top-ten/) 網絡應用漏洞  
- **AI 特定保護**：實施 [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) 的控制措施  
- **安全密鑰管理**：使用專用保管庫存儲令牌、API 密鑰和敏感配置數據  
- **端到端加密**：在所有應用組件和數據流中實施安全通信  
- **輸入驗證**：對所有用戶輸入、API 參數和數據源進行嚴格驗證  

#### **基礎設施加固**  
- **多因素身份驗證**：所有管理和服務帳戶必須啟用 MFA  
- **補丁管理**：對操作系統、框架和依賴進行自動化、及時的補丁更新  
- **身份提供者集成**：通過企業身份提供者（Microsoft Entra ID、Active Directory）進行集中身份管理  
- **網絡分段**：邏輯隔離 MCP 組件，以限制橫向移動的可能性  
- **最小權限原則**：所有系統組件和帳戶僅授予最低必要權限  

#### **安全監控與檢測**  
- **全面日誌記錄**：詳細記錄 AI 應用活動，包括 MCP 客戶端-伺服器交互  
- **SIEM 集成**：集中式安全信息和事件管理，用於異常檢測  
- **行為分析**：AI 驅動的監控，用於檢測系統和用戶行為中的異常模式  
- **威脅情報**：整合外部威脅信息和妥協指標（IOCs）  
- **事件響應**：明確定義的安全事件檢測、響應和恢復程序  

#### **零信任架構**  
- **永不信任，始終驗證**：持續驗證用戶、設備和網絡連接  
- **微分段**：粒度化的網絡控制，隔離個別工作負載和服務  
- **基於身份的安全**：基於已驗證身份而非網絡位置的安全策略  
- **持續風險評估**：根據當前上下文和行為進行動態安全姿態評估  
- **條件訪問**：基於風險因素、位置和設備信任的訪問控制  

### 企業集成模式

#### **微軟安全生態系統集成**  
- **Microsoft Defender for Cloud**：全面的雲安全姿態管理  
- **Azure Sentinel**：雲原生 SIEM 和 SOAR 功能，用於 AI 工作負載保護  
- **Microsoft Entra ID**：企業身份和訪問管理，支持條件訪問策略  
- **Azure Key Vault**：集中式密鑰管理，支持硬件安全模塊（HSM）  
- **Microsoft Purview**：數據治理和合規，用於 AI 數據源和工作流  

#### **合規與治理**  
- **監管對齊**：確保 MCP 實施符合行業特定的合規要求（GDPR、HIPAA、SOC 2）  
- **數據分類**：正確分類和處理 AI 系統處理的敏感數據  
- **審計追蹤**：全面的日誌記錄，用於合規性和法證調查  
- **隱私控制**：在 AI 系統架構中實施隱私設計原則  
- **變更管理**：對 AI 系統修改進行安全審查的正式流程  

這些基礎實踐創建了穩健的安全基線，增強了 MCP 特定安全控制的有效性，並為 AI 驅動的應用提供全面保護。

## 關鍵安全要點

- **分層安全方法**：結合基礎安全實踐（安全編碼、最小權限、供應鏈驗證、持續監控）與 AI 特定控制措施，實現全面保護  

- **AI 特定威脅格局**：MCP 系統面臨獨特風險，包括提示注入、工具污染、會話劫持、混淆代理問題、令牌透傳漏洞和過度權限，需採取專門的緩解措施  

- **身份驗證與授權卓越**：使用外部身份提供者（Microsoft Entra ID）實施強大的身份驗證，強制執行正確的令牌驗證，並且絕不接受未明確為 MCP 伺服器簽發的令牌  

- **AI 攻擊防範**：部署 Microsoft Prompt Shields 和 Azure Content Safety，以防範間接提示注入和工具污染攻擊，同時驗證工具元數據並監控動態變更  

- **會話與傳輸安全**：使用加密安全、非決定性的會話 ID，並綁定到用戶身份，實施正確的會話生命周期管理，絕不使用會話進行身份驗證  

- **OAuth 安全最佳實踐**：通過動態註冊客戶端的明確用戶同意、正確的 OAuth 2.1 實施（包括 PKCE）和嚴格的重定向 URI 驗證，防止混淆代理攻擊  

- **令牌安全原則**：避免令牌透傳反模式，驗證令牌受眾聲明，實施短期令牌並採用安全輪換，保持清晰的信任邊界  

- **全面的供應鏈安全**：以與傳統軟件依賴相同的安全嚴謹性對待所有 AI 生態系統組件（模型、嵌入、上下文提供者、外部 API）  

- **持續演進**：保持對快速演變的 MCP 規範的最新了解，為安全社區標準做出貢獻，並隨著協議的成熟保持適應性安全姿態  

- **微軟安全集成**：利用微軟的全面安全生態系統（Prompt Shields、Azure Content Safety、GitHub 高級安全、Entra ID），增強 MCP 部署的保護  

## 全面資源

### **官方 MCP 安全文檔**  
- [MCP 規範（當前版本：2025-06-18）](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP 安全最佳實踐](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP 授權規範](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  
- [MCP GitHub 存儲庫](https://github.com/modelcontextprotocol)  

### **安全標準與最佳實踐**  
- [OAuth 2.0 安全最佳實踐（RFC 9700）](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 網絡應用安全](https://owasp.org/www-project-top-ten/)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/download/43299/?tmstv=1731900559)  
- [微軟數字防禦報告](https://aka.ms/mddr)  

### **AI 安全研究與分析**  
- [MCP 中的提示注入（Simon Willison）](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)  
- [工具污染攻擊（Invariant Labs）](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)  
- [MCP 安全研究簡報（Wiz Security）](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)  
### **Microsoft 安全解決方案**
- [Microsoft Prompt Shields 文件](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure 內容安全服務](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID 安全性](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Azure Token 管理最佳實踐](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub 高級安全性](https://github.com/security/advanced-security)

### **實作指南與教學**
- [將 Azure API Management 作為 MCP 認證閘道](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [使用 Microsoft Entra ID 與 MCP 伺服器進行認證](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [安全的 Token 儲存與加密（影片）](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps 與供應鏈安全**
- [Azure DevOps 安全性](https://azure.microsoft.com/products/devops)
- [Azure Repos 安全性](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft 供應鏈安全之旅](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **其他安全性文件**

如需全面的安全性指導，請參考本節中的以下專業文件：

- **[MCP 安全性最佳實踐 2025](./mcp-security-best-practices-2025.md)** - MCP 實作的完整安全性最佳實踐
- **[Azure 內容安全性實作](./azure-content-safety-implementation.md)** - Azure 內容安全性整合的實際實作範例  
- **[MCP 安全性控制 2025](./mcp-security-controls-2025.md)** - MCP 部署的最新安全性控制與技術
- **[MCP 最佳實踐快速參考](./mcp-best-practices.md)** - MCP 安全性基本實踐的快速參考指南

---

## 下一步

下一步：[第 3 章：開始使用](../03-GettingStarted/README.md)

**免責聲明**：  
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。我們致力於提供準確的翻譯，但請注意，自動翻譯可能包含錯誤或不準確之處。應以原始語言的文件作為權威來源。對於關鍵資訊，建議尋求專業人工翻譯。我們對因使用此翻譯而產生的任何誤解或錯誤解讀概不負責。