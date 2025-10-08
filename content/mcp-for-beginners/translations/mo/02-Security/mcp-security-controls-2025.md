<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T14:38:04+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "mo"
}
-->
# MCP 安全控制 - 2025 年 8 月更新

> **目前標準**：本文件反映 [MCP 規範 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) 的安全要求以及官方 [MCP 安全最佳實踐](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)。

模型上下文協議（MCP）已顯著成熟，增強的安全控制涵蓋了傳統軟體安全和 AI 特定威脅。本文件提供截至 2025 年 8 月的安全 MCP 實施的全面安全控制。

## **強制性安全要求**

### **MCP 規範中的關鍵禁止事項：**

> **禁止**：MCP 伺服器 **不得** 接受任何未明確為 MCP 伺服器發行的令牌  
>
> **禁止**：MCP 伺服器 **不得** 使用會話進行身份驗證  
>
> **要求**：實施授權的 MCP 伺服器 **必須** 驗證所有入站請求  
>
> **強制性**：使用靜態客戶端 ID 的 MCP 代理伺服器 **必須** 為每個動態註冊的客戶端獲得用戶同意  

---

## 1. **身份驗證與授權控制**

### **外部身份提供者整合**

**目前 MCP 標準（2025-06-18）** 允許 MCP 伺服器將身份驗證委派給外部身份提供者，這代表了顯著的安全改進：

**安全效益：**
1. **消除自定義身份驗證風險**：避免自定義身份驗證實現，減少漏洞面
2. **企業級安全**：利用 Microsoft Entra ID 等成熟身份提供者的高級安全功能
3. **集中化身份管理**：簡化用戶生命周期管理、訪問控制和合規審計
4. **多因素身份驗證**：繼承企業身份提供者的 MFA 功能
5. **條件訪問策略**：受益於基於風險的訪問控制和自適應身份驗證

**實施要求：**
- **令牌受眾驗證**：驗證所有令牌是否明確為 MCP 伺服器發行
- **發行者驗證**：驗證令牌發行者是否與預期身份提供者匹配
- **簽名驗證**：對令牌完整性進行加密驗證
- **過期強制執行**：嚴格執行令牌的有效期限限制
- **範圍驗證**：確保令牌包含適當的操作權限

### **授權邏輯安全**

**關鍵控制：**
- **全面授權審計**：定期對所有授權決策點進行安全審查
- **安全默認設置**：當授權邏輯無法做出明確決定時拒絕訪問
- **權限邊界**：清晰區分不同的特權級別和資源訪問
- **審計日誌**：完整記錄所有授權決策以進行安全監控
- **定期訪問審查**：定期驗證用戶權限和特權分配

## 2. **令牌安全與防止透傳控制**

### **防止令牌透傳**

**令牌透傳在 MCP 授權規範中被明確禁止**，因為其存在重大安全風險：

**解決的安全風險：**
- **控制繞過**：繞過基本安全控制，如速率限制、請求驗證和流量監控
- **責任分解**：使客戶端識別變得不可能，損害審計追蹤和事件調查
- **基於代理的數據外洩**：使惡意行為者能利用伺服器作為代理進行未授權的數據訪問
- **信任邊界違反**：破壞下游服務對令牌來源的信任假設
- **橫向移動**：跨多個服務的令牌被攻擊者利用，擴大攻擊範圍

**實施控制：**
```yaml
Token Validation Requirements:
  audience_validation: MANDATORY
  issuer_verification: MANDATORY  
  signature_check: MANDATORY
  expiration_enforcement: MANDATORY
  scope_validation: MANDATORY
  
Token Lifecycle Management:
  rotation_frequency: "Short-lived tokens preferred"
  secure_storage: "Azure Key Vault or equivalent"
  transmission_security: "TLS 1.3 minimum"
  replay_protection: "Implemented via nonce/timestamp"
```

### **安全令牌管理模式**

**最佳實踐：**
- **短期令牌**：通過頻繁令牌輪換最小化暴露窗口
- **即時發行**：僅在需要特定操作時發行令牌
- **安全存儲**：使用硬件安全模塊（HSM）或安全密鑰保管庫
- **令牌綁定**：將令牌綁定到特定客戶端、會話或操作（如果可能）
- **監控與警報**：實時檢測令牌濫用或未授權訪問模式

## 3. **會話安全控制**

### **防止會話劫持**

**解決的攻擊向量：**
- **會話劫持提示注入**：惡意事件注入到共享會話狀態
- **會話冒充**：未授權使用被盜的會話 ID 以繞過身份驗證
- **可恢復流攻擊**：利用伺服器發送事件恢復進行惡意內容注入

**強制性會話控制：**
```yaml
Session ID Generation:
  randomness_source: "Cryptographically secure RNG"
  entropy_bits: 128 # Minimum recommended
  format: "Base64url encoded"
  predictability: "MUST be non-deterministic"

Session Binding:
  user_binding: "REQUIRED - <user_id>:<session_id>"
  additional_identifiers: "Device fingerprint, IP validation"
  context_binding: "Request origin, user agent validation"
  
Session Lifecycle:
  expiration: "Configurable timeout policies"
  rotation: "After privilege escalation events"
  invalidation: "Immediate on security events"
  cleanup: "Automated expired session removal"
```

**傳輸安全：**
- **強制 HTTPS**：所有會話通信均使用 TLS 1.3
- **安全 Cookie 屬性**：HttpOnly、Secure、SameSite=Strict
- **證書固定**：對關鍵連接進行固定以防止中間人攻擊

### **有狀態與無狀態的考量**

**對於有狀態實現：**
- 共享會話狀態需要額外保護以防注入攻擊
- 基於隊列的會話管理需要完整性驗證
- 多個伺服器實例需要安全的會話狀態同步

**對於無狀態實現：**
- 使用 JWT 或類似的基於令牌的會話管理
- 對會話狀態完整性進行加密驗證
- 減少攻擊面，但需要強大的令牌驗證

## 4. **AI 特定安全控制**

### **防止提示注入**

**Microsoft Prompt Shields 整合：**
```yaml
Detection Mechanisms:
  - "Advanced ML-based instruction detection"
  - "Contextual analysis of external content"
  - "Real-time threat pattern recognition"
  
Protection Techniques:
  - "Spotlighting trusted vs untrusted content"
  - "Delimiter systems for content boundaries"  
  - "Data marking for content source identification"
  
Integration Points:
  - "Azure Content Safety service"
  - "Real-time content filtering"
  - "Threat intelligence updates"
```

**實施控制：**
- **輸入清理**：全面驗證和過濾所有用戶輸入
- **內容邊界定義**：清晰區分系統指令與用戶內容
- **指令層級**：對衝突指令設置適當的優先級規則
- **輸出監控**：檢測潛在有害或被操控的輸出

### **防止工具污染**

**工具安全框架：**
```yaml
Tool Definition Protection:
  validation:
    - "Schema validation against expected formats"
    - "Content analysis for malicious instructions" 
    - "Parameter injection detection"
    - "Hidden instruction identification"
  
  integrity_verification:
    - "Cryptographic hashing of tool definitions"
    - "Digital signatures for tool packages"
    - "Version control with change auditing"
    - "Tamper detection mechanisms"
  
  monitoring:
    - "Real-time change detection"
    - "Behavioral analysis of tool usage"
    - "Anomaly detection for execution patterns"
    - "Automated alerting for suspicious modifications"
```

**動態工具管理：**
- **批准工作流**：對工具修改進行明確的用戶同意
- **回滾功能**：能夠恢復到之前的工具版本
- **變更審計**：完整記錄工具定義修改的歷史
- **風險評估**：自動評估工具的安全狀態

## 5. **防止混淆代理攻擊**

### **OAuth 代理安全**

**攻擊防止控制：**
```yaml
Client Registration:
  static_client_protection:
    - "Explicit user consent for dynamic registration"
    - "Consent bypass prevention mechanisms"  
    - "Cookie-based consent validation"
    - "Redirect URI strict validation"
    
  authorization_flow:
    - "PKCE implementation (OAuth 2.1)"
    - "State parameter validation"
    - "Authorization code binding"
    - "Nonce verification for ID tokens"
```

**實施要求：**
- **用戶同意驗證**：對動態客戶端註冊永不跳過同意屏幕
- **重定向 URI 驗證**：嚴格基於白名單的重定向目的地驗證
- **授權碼保護**：短期授權碼並強制單次使用
- **客戶端身份驗證**：對客戶端憑據和元數據進行強大的驗證

## 6. **工具執行安全**

### **沙盒與隔離**

**基於容器的隔離：**
```yaml
Execution Environment:
  containerization: "Docker/Podman with security profiles"
  resource_limits:
    cpu: "Configurable CPU quotas"
    memory: "Memory usage restrictions"
    disk: "Storage access limitations"
    network: "Network policy enforcement"
  
  privilege_restrictions:
    user_context: "Non-root execution mandatory"
    capability_dropping: "Remove unnecessary Linux capabilities"
    syscall_filtering: "Seccomp profiles for syscall restriction"
    filesystem: "Read-only root with minimal writable areas"
```

**進程隔離：**
- **獨立進程上下文**：每個工具執行在隔離的進程空間中
- **進程間通信**：使用經過驗證的安全 IPC 機制
- **進程監控**：運行時行為分析和異常檢測
- **資源限制**：對 CPU、內存和 I/O 操作設置硬性限制

### **最小特權實現**

**權限管理：**
```yaml
Access Control:
  file_system:
    - "Minimal required directory access"
    - "Read-only access where possible"
    - "Temporary file cleanup automation"
    
  network_access:
    - "Explicit allowlist for external connections"
    - "DNS resolution restrictions" 
    - "Port access limitations"
    - "SSL/TLS certificate validation"
  
  system_resources:
    - "No administrative privilege elevation"
    - "Limited system call access"
    - "No hardware device access"
    - "Restricted environment variable access"
```

## 7. **供應鏈安全控制**

### **依賴性驗證**

**全面的組件安全：**
```yaml
Software Dependencies:
  scanning: 
    - "Automated vulnerability scanning (GitHub Advanced Security)"
    - "License compliance verification"
    - "Known vulnerability database checks"
    - "Malware detection and analysis"
  
  verification:
    - "Package signature verification"
    - "Checksum validation"
    - "Provenance attestation"
    - "Software Bill of Materials (SBOM)"

AI Components:
  model_verification:
    - "Model provenance validation"
    - "Training data source verification" 
    - "Model behavior testing"
    - "Adversarial robustness assessment"
  
  service_validation:
    - "Third-party API security assessment"
    - "Service level agreement review"
    - "Data handling compliance verification"
    - "Incident response capability evaluation"
```

### **持續監控**

**供應鏈威脅檢測：**
- **依賴性健康監控**：持續評估所有依賴性是否存在安全問題
- **威脅情報整合**：實時更新新興供應鏈威脅
- **行為分析**：檢測外部組件的異常行為
- **自動響應**：立即隔離受損的組件

## 8. **監控與檢測控制**

### **安全信息與事件管理（SIEM）**

**全面的日誌策略：**
```yaml
Authentication Events:
  - "All authentication attempts (success/failure)"
  - "Token issuance and validation events"
  - "Session creation, modification, termination"
  - "Authorization decisions and policy evaluations"

Tool Execution:
  - "Tool invocation details and parameters"
  - "Execution duration and resource usage"
  - "Output generation and content analysis"
  - "Error conditions and exception handling"

Security Events:
  - "Potential prompt injection attempts"
  - "Tool poisoning detection events"
  - "Session hijacking indicators"
  - "Unusual access patterns and anomalies"
```

### **實時威脅檢測**

**行為分析：**
- **用戶行為分析（UBA）**：檢測異常的用戶訪問模式
- **實體行為分析（EBA）**：監控 MCP 伺服器和工具行為
- **機器學習異常檢測**：AI 驅動的安全威脅識別
- **威脅情報關聯**：將觀察到的活動與已知攻擊模式匹配

## 9. **事件響應與恢復**

### **自動響應能力**

**立即響應行動：**
```yaml
Threat Containment:
  session_management:
    - "Immediate session termination"
    - "Account lockout procedures"
    - "Access privilege revocation"
  
  system_isolation:
    - "Network segmentation activation"
    - "Service isolation protocols"
    - "Communication channel restriction"

Recovery Procedures:
  credential_rotation:
    - "Automated token refresh"
    - "API key regeneration"
    - "Certificate renewal"
  
  system_restoration:
    - "Clean state restoration"
    - "Configuration rollback"
    - "Service restart procedures"
```

### **法證能力**

**調查支持：**
- **審計追蹤保存**：不可變日誌，具有加密完整性
- **證據收集**：自動收集相關的安全工件
- **時間線重建**：詳細的事件序列，追溯安全事件
- **影響評估**：評估妥協範圍和數據暴露

## **關鍵安全架構原則**

### **深度防禦**
- **多層安全**：安全架構中無單一故障點
- **冗餘控制**：對關鍵功能的重疊安全措施
- **安全默認機制**：系統遇到錯誤或攻擊時的安全默認設置

### **零信任實施**
- **永不信任，始終驗證**：對所有實體和請求進行持續驗證
- **最小特權原則**：所有組件的最低訪問權限
- **微分段**：細粒度的網絡和訪問控制

### **持續安全演進**
- **威脅環境適應**：定期更新以應對新興威脅
- **安全控制有效性**：持續評估和改進控制措施
- **規範合規性**：與不斷演變的 MCP 安全標準保持一致

---

## **實施資源**

### **官方 MCP 文件**
- [MCP 規範（2025-06-18）](https://spec.modelcontextprotocol.io/specification/2025-06-18/)
- [MCP 安全最佳實踐](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [MCP 授權規範](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

### **Microsoft 安全解決方案**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [GitHub Advanced Security](https://github.com/security/advanced-security)
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)

### **安全標準**
- [OAuth 2.0 安全最佳實踐（RFC 9700）](https://datatracker.ietf.org/doc/html/rfc9700)
- [OWASP 大型語言模型十大安全風險](https://genai.owasp.org/)
- [NIST 網絡安全框架](https://www.nist.gov/cyberframework)

---

> **重要**：這些安全控制反映了目前的 MCP 規範（2025-06-18）。由於標準快速演變，請始終根據最新的 [官方文件](https://spec.modelcontextprotocol.io/) 進行驗證。

**免責聲明**：  
本文檔使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。儘管我們努力確保準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始語言的文件應被視為權威來源。對於關鍵信息，建議使用專業人工翻譯。我們對因使用此翻譯而引起的任何誤解或錯誤解釋不承擔責任。