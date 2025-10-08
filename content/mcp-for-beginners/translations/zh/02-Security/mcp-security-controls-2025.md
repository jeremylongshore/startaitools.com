<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T10:30:18+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "zh"
}
-->
# MCP安全控制 - 2025年8月更新

> **当前标准**：本文档反映了[MCP规范2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/)的安全要求以及官方[MCP安全最佳实践](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)。

模型上下文协议（MCP）在安全控制方面取得了显著进展，涵盖了传统软件安全和针对AI的特定威胁。本文档提供了截至2025年8月的安全MCP实施的全面安全控制。

## **强制性安全要求**

### **MCP规范中的关键禁止事项：**

> **禁止**：MCP服务器**不得**接受任何未明确为MCP服务器签发的令牌  
>
> **禁止**：MCP服务器**不得**使用会话进行身份验证  
>
> **要求**：实施授权的MCP服务器**必须**验证所有入站请求  
>
> **强制性**：使用静态客户端ID的MCP代理服务器**必须**为每个动态注册的客户端获取用户同意  

---

## 1. **身份验证与授权控制**

### **外部身份提供商集成**

**当前MCP标准（2025-06-18）**允许MCP服务器将身份验证委托给外部身份提供商，这代表了显著的安全改进：

**安全优势：**
1. **消除自定义身份验证风险**：通过避免自定义身份验证实现，减少漏洞面
2. **企业级安全**：利用诸如Microsoft Entra ID等成熟的身份提供商，提供高级安全功能
3. **集中化身份管理**：简化用户生命周期管理、访问控制和合规审计
4. **多因素身份验证**：继承企业身份提供商的MFA功能
5. **条件访问策略**：受益于基于风险的访问控制和自适应身份验证

**实施要求：**
- **令牌受众验证**：验证所有令牌是否明确为MCP服务器签发
- **发行者验证**：验证令牌发行者是否与预期的身份提供商匹配
- **签名验证**：对令牌完整性进行加密验证
- **过期时间强制**：严格执行令牌的生命周期限制
- **范围验证**：确保令牌包含适当的权限以执行请求的操作

### **授权逻辑安全**

**关键控制：**
- **全面授权审计**：定期对所有授权决策点进行安全审查
- **安全默认设置**：当授权逻辑无法做出明确决策时拒绝访问
- **权限边界**：明确区分不同权限级别和资源访问
- **审计日志记录**：完整记录所有授权决策以进行安全监控
- **定期访问审查**：定期验证用户权限和权限分配

## 2. **令牌安全与防止传递控制**

### **防止令牌传递**

**令牌传递在MCP授权规范中被明确禁止**，因为其存在重大安全风险：

**解决的安全风险：**
- **控制规避**：绕过速率限制、请求验证和流量监控等关键安全控制
- **责任链断裂**：无法识别客户端身份，破坏审计记录和事件调查
- **基于代理的数据泄露**：允许恶意行为者利用服务器作为代理进行未经授权的数据访问
- **信任边界违规**：破坏下游服务对令牌来源的信任假设
- **横向移动**：跨多个服务的令牌泄露可能导致更广泛的攻击扩展

**实施控制：**
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

**最佳实践：**
- **短生命周期令牌**：通过频繁令牌轮换减少暴露窗口
- **按需签发**：仅在特定操作需要时签发令牌
- **安全存储**：使用硬件安全模块（HSM）或安全密钥库
- **令牌绑定**：尽可能将令牌绑定到特定客户端、会话或操作
- **监控与警报**：实时检测令牌滥用或未经授权的访问模式

## 3. **会话安全控制**

### **防止会话劫持**

**解决的攻击向量：**
- **会话劫持提示注入**：恶意事件注入共享会话状态
- **会话冒充**：未经授权使用被盗会话ID绕过身份验证
- **可恢复流攻击**：利用服务器发送事件恢复进行恶意内容注入

**强制性会话控制：**
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

**传输安全：**
- **强制HTTPS**：所有会话通信均通过TLS 1.3
- **安全Cookie属性**：HttpOnly、Secure、SameSite=Strict
- **证书绑定**：关键连接的证书绑定以防止中间人攻击

### **有状态与无状态的考虑**

**对于有状态实现：**
- 共享会话状态需要额外保护以防止注入攻击
- 基于队列的会话管理需要完整性验证
- 多个服务器实例需要安全的会话状态同步

**对于无状态实现：**
- 基于JWT或类似令牌的会话管理
- 会话状态完整性的加密验证
- 攻击面减少，但需要强大的令牌验证

## 4. **AI特定安全控制**

### **防止提示注入**

**Microsoft Prompt Shields集成：**
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

**实施控制：**
- **输入清理**：全面验证和过滤所有用户输入
- **内容边界定义**：明确区分系统指令与用户内容
- **指令层级**：为冲突指令设置适当的优先级规则
- **输出监控**：检测潜在有害或被操纵的输出

### **防止工具投毒**

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

**动态工具管理：**
- **审批工作流**：工具修改需明确用户同意
- **回滚功能**：能够恢复到之前的工具版本
- **变更审计**：完整记录工具定义的修改历史
- **风险评估**：自动评估工具的安全状况

## 5. **防止混淆代理攻击**

### **OAuth代理安全**

**攻击预防控制：**
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

**实施要求：**
- **用户同意验证**：动态客户端注册时不得跳过同意屏幕
- **重定向URI验证**：严格基于白名单验证重定向目标
- **授权码保护**：短生命周期代码并强制单次使用
- **客户端身份验证**：强大的客户端凭据和元数据验证

## 6. **工具执行安全**

### **沙箱与隔离**

**基于容器的隔离：**
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

**进程隔离：**
- **独立进程上下文**：每个工具执行在隔离的进程空间中
- **进程间通信**：使用验证的安全IPC机制
- **进程监控**：运行时行为分析和异常检测
- **资源限制**：对CPU、内存和I/O操作设置硬性限制

### **最小权限实施**

**权限管理：**
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

## 7. **供应链安全控制**

### **依赖验证**

**全面组件安全：**
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

### **持续监控**

**供应链威胁检测：**
- **依赖健康监控**：持续评估所有依赖项的安全问题
- **威胁情报集成**：实时更新新兴供应链威胁
- **行为分析**：检测外部组件的异常行为
- **自动响应**：立即隔离受损组件

## 8. **监控与检测控制**

### **安全信息与事件管理（SIEM）**

**全面日志策略：**
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

### **实时威胁检测**

**行为分析：**
- **用户行为分析（UBA）**：检测异常用户访问模式
- **实体行为分析（EBA）**：监控MCP服务器和工具行为
- **机器学习异常检测**：AI驱动的安全威胁识别
- **威胁情报关联**：将观察到的活动与已知攻击模式匹配

## 9. **事件响应与恢复**

### **自动响应能力**

**即时响应行动：**
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

### **取证能力**

**调查支持：**
- **审计记录保存**：不可变日志记录并具有加密完整性
- **证据收集**：自动收集相关安全工件
- **时间线重建**：详细记录导致安全事件的事件序列
- **影响评估**：评估妥协范围和数据暴露情况

## **关键安全架构原则**

### **深度防御**
- **多层安全**：安全架构中无单点故障
- **冗余控制**：关键功能的重叠安全措施
- **安全故障机制**：系统遇到错误或攻击时的安全默认设置

### **零信任实施**
- **永不信任，总是验证**：持续验证所有实体和请求
- **最小权限原则**：所有组件的访问权限最小化
- **微分段**：细粒度的网络和访问控制

### **持续安全演进**
- **威胁环境适应**：定期更新以应对新兴威胁
- **安全控制有效性**：持续评估和改进控制措施
- **规范合规性**：与不断发展的MCP安全标准保持一致

---

## **实施资源**

### **官方MCP文档**
- [MCP规范（2025-06-18）](https://spec.modelcontextprotocol.io/specification/2025-06-18/)
- [MCP安全最佳实践](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [MCP授权规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

### **Microsoft安全解决方案**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure内容安全](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [GitHub高级安全](https://github.com/security/advanced-security)
- [Azure密钥库](https://learn.microsoft.com/azure/key-vault/)

### **安全标准**
- [OAuth 2.0安全最佳实践（RFC 9700）](https://datatracker.ietf.org/doc/html/rfc9700)
- [OWASP大型语言模型十大安全问题](https://genai.owasp.org/)
- [NIST网络安全框架](https://www.nist.gov/cyberframework)

---

> **重要**：这些安全控制反映了当前MCP规范（2025-06-18）。由于标准快速演变，请始终根据最新的[官方文档](https://spec.modelcontextprotocol.io/)进行验证。

**免责声明**：  
本文档使用AI翻译服务[Co-op Translator](https://github.com/Azure/co-op-translator)进行翻译。尽管我们努力确保准确性，但请注意，自动翻译可能包含错误或不准确之处。应以原始语言的文档作为权威来源。对于关键信息，建议使用专业人工翻译。对于因使用本翻译而引起的任何误解或误读，我们概不负责。