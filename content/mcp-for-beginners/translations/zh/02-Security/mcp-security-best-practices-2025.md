<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T10:27:10+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "zh"
}
-->
# MCP 安全最佳实践 - 2025年8月更新

> **重要提示**：本文档反映了最新的 [MCP 规范 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) 的安全要求以及官方的 [MCP 安全最佳实践](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)。请始终参考当前规范以获取最新的指导。

## MCP 实现的基本安全实践

模型上下文协议（MCP）引入了超越传统软件安全的新型安全挑战。这些实践涵盖了基础安全要求以及 MCP 特有的威胁，包括提示注入、工具投毒、会话劫持、混淆代理问题和令牌传递漏洞。

### **强制性安全要求**

**MCP 规范中的关键要求：**

> **禁止**：MCP 服务器 **不得** 接受任何未明确为 MCP 服务器签发的令牌  
> 
> **必须**：实现授权的 MCP 服务器 **必须** 验证所有入站请求  
>  
> **禁止**：MCP 服务器 **不得** 使用会话进行身份验证  
>
> **必须**：使用静态客户端 ID 的 MCP 代理服务器 **必须** 为每个动态注册的客户端获取用户同意  

---

## 1. **令牌安全与身份验证**

**身份验证与授权控制：**
   - **严格的授权审查**：对 MCP 服务器的授权逻辑进行全面审计，确保只有预期的用户和客户端可以访问资源  
   - **外部身份提供商集成**：使用 Microsoft Entra ID 等成熟的身份提供商，而非自建身份验证系统  
   - **令牌受众验证**：始终验证令牌是否明确为您的 MCP 服务器签发，绝不接受上游令牌  
   - **正确的令牌生命周期管理**：实施安全的令牌轮换、过期策略，并防止令牌重放攻击  

**受保护的令牌存储：**
   - 使用 Azure Key Vault 或类似的安全凭据存储来管理所有机密  
   - 对令牌进行静态和传输中的加密  
   - 定期轮换凭据并监控未授权访问  

## 2. **会话管理与传输安全**

**安全的会话实践：**
   - **加密安全的会话 ID**：使用安全的、非确定性的会话 ID，并通过安全随机数生成器生成  
   - **用户特定绑定**：将会话 ID 绑定到用户身份，例如使用 `<user_id>:<session_id>` 格式，防止跨用户会话滥用  
   - **会话生命周期管理**：实施适当的过期、轮换和失效机制，以限制漏洞窗口  
   - **强制 HTTPS/TLS**：所有通信必须使用 HTTPS，以防止会话 ID 被拦截  

**传输层安全：**
   - 尽可能配置 TLS 1.3，并正确管理证书  
   - 对关键连接实施证书绑定  
   - 定期轮换证书并验证其有效性  

## 3. **AI 特定威胁防护** 🤖

**提示注入防御：**
   - **Microsoft Prompt Shields**：部署 AI 提示防护工具，以高级检测和过滤恶意指令  
   - **输入清理**：验证并清理所有输入，防止注入攻击和混淆代理问题  
   - **内容边界**：使用分隔符和数据标记系统区分可信指令与外部内容  

**工具投毒预防：**
   - **工具元数据验证**：对工具定义实施完整性检查，并监控意外更改  
   - **动态工具监控**：监控运行时行为，并设置异常执行模式的警报  
   - **审批工作流**：要求对工具修改和功能变更进行明确的用户审批  

## 4. **访问控制与权限管理**

**最小权限原则：**
   - 仅为 MCP 服务器授予实现功能所需的最低权限  
   - 实施基于角色的访问控制（RBAC），并使用细粒度权限  
   - 定期审查权限并持续监控权限提升  

**运行时权限控制：**
   - 应用资源限制以防止资源耗尽攻击  
   - 使用容器隔离工具执行环境  
   - 对管理功能实施按需访问  

## 5. **内容安全与监控**

**内容安全实施：**
   - **Azure 内容安全集成**：使用 Azure 内容安全检测有害内容、越狱尝试和策略违规  
   - **行为分析**：实施运行时行为监控，检测 MCP 服务器和工具执行中的异常  
   - **全面日志记录**：记录所有身份验证尝试、工具调用和安全事件，并使用安全、防篡改的存储  

**持续监控：**
   - 实时警报，监控可疑模式和未授权访问尝试  
   - 与 SIEM 系统集成，实现集中化的安全事件管理  
   - 定期对 MCP 实现进行安全审计和渗透测试  

## 6. **供应链安全**

**组件验证：**
   - **依赖扫描**：对所有软件依赖项和 AI 组件使用自动化漏洞扫描  
   - **来源验证**：验证模型、数据源和外部服务的来源、许可和完整性  
   - **签名包**：使用加密签名的包，并在部署前验证签名  

**安全开发管道：**
   - **GitHub 高级安全**：实施密钥扫描、依赖分析和 CodeQL 静态分析  
   - **CI/CD 安全**：在自动化部署管道中集成安全验证  
   - **工件完整性**：对部署的工件和配置实施加密验证  

## 7. **OAuth 安全与混淆代理预防**

**OAuth 2.1 实现：**
   - **PKCE 实现**：对所有授权请求使用代码交换证明（PKCE）  
   - **明确同意**：为每个动态注册的客户端获取用户同意，以防止混淆代理攻击  
   - **重定向 URI 验证**：严格验证重定向 URI 和客户端标识符  

**代理安全：**
   - 防止通过静态客户端 ID 利用进行授权绕过  
   - 为第三方 API 访问实施适当的同意工作流  
   - 监控授权代码盗窃和未授权的 API 访问  

## 8. **事件响应与恢复**

**快速响应能力：**
   - **自动响应**：实施自动化系统进行凭据轮换和威胁遏制  
   - **回滚程序**：能够快速恢复到已知的良好配置和组件  
   - **取证能力**：提供详细的审计记录和日志以支持事件调查  

**沟通与协调：**
   - 明确的安全事件升级程序  
   - 与组织的事件响应团队集成  
   - 定期进行安全事件模拟和桌面演练  

## 9. **合规与治理**

**法规合规：**
   - 确保 MCP 实现符合行业特定要求（如 GDPR、HIPAA、SOC 2）  
   - 为 AI 数据处理实施数据分类和隐私控制  
   - 保持全面的文档以支持合规审计  

**变更管理：**
   - 对 MCP 系统的所有修改进行正式的安全审查流程  
   - 配置更改的版本控制和审批工作流  
   - 定期进行合规评估和差距分析  

## 10. **高级安全控制**

**零信任架构：**
   - **永不信任，总是验证**：持续验证用户、设备和连接  
   - **微分段**：对单个 MCP 组件实施细粒度的网络控制  
   - **条件访问**：基于风险的访问控制，适应当前上下文和行为  

**运行时应用保护：**
   - **运行时应用自我保护（RASP）**：部署 RASP 技术以实时检测威胁  
   - **应用性能监控**：监控性能异常，这可能表明存在攻击  
   - **动态安全策略**：根据当前威胁环境调整安全策略  

## 11. **微软安全生态系统集成**

**全面的微软安全解决方案：**
   - **Microsoft Defender for Cloud**：为 MCP 工作负载提供云安全态势管理  
   - **Azure Sentinel**：云原生 SIEM 和 SOAR 功能，用于高级威胁检测  
   - **Microsoft Purview**：为 AI 工作流和数据源提供数据治理和合规性  

**身份与访问管理：**
   - **Microsoft Entra ID**：企业身份管理，支持条件访问策略  
   - **特权身份管理（PIM）**：按需访问和管理功能的审批工作流  
   - **身份保护**：基于风险的条件访问和自动化威胁响应  

## 12. **持续安全演进**

**保持最新：**
   - **规范监控**：定期审查 MCP 规范更新和安全指导变更  
   - **威胁情报**：集成 AI 特定的威胁情报和攻击指标  
   - **安全社区参与**：积极参与 MCP 安全社区和漏洞披露计划  

**自适应安全：**
   - **机器学习安全**：使用基于 ML 的异常检测识别新型攻击模式  
   - **预测性安全分析**：实施预测模型以主动识别威胁  
   - **安全自动化**：根据威胁情报和规范变更自动更新安全策略  

---

## **关键安全资源**

### **官方 MCP 文档**
- [MCP 规范 (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP 安全最佳实践](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP 授权规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **微软安全解决方案**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure 内容安全](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID 安全](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub 高级安全](https://github.com/security/advanced-security)  

### **安全标准**
- [OAuth 2.0 安全最佳实践 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP 大型语言模型十大安全风险](https://genai.owasp.org/)  
- [NIST AI 风险管理框架](https://www.nist.gov/itl/ai-risk-management-framework)  

### **实施指南**
- [Azure API 管理 MCP 身份验证网关](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID 与 MCP 服务器集成](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **安全提示**：MCP 安全实践发展迅速。在实施之前，请始终根据当前的 [MCP 规范](https://spec.modelcontextprotocol.io/) 和 [官方安全文档](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) 进行验证。

**免责声明**：  
本文档使用AI翻译服务[Co-op Translator](https://github.com/Azure/co-op-translator)进行翻译。尽管我们努力确保准确性，但请注意，自动翻译可能包含错误或不准确之处。应以原始语言的文档作为权威来源。对于关键信息，建议使用专业人工翻译。因使用本翻译而导致的任何误解或误读，我们概不负责。