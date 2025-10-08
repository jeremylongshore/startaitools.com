<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T10:27:49+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "zh"
}
-->
# MCP安全：AI系统的全面保护

[![MCP安全最佳实践](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.zh.png)](https://youtu.be/88No8pw706o)

_（点击上方图片观看本课视频）_

安全性是AI系统设计的核心，因此我们将其作为第二部分的重点。这与微软的[安全未来计划](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/)中的**安全设计原则**保持一致。

模型上下文协议（MCP）为AI驱动的应用程序带来了强大的新功能，同时也引入了超越传统软件风险的独特安全挑战。MCP系统不仅面临传统的安全问题（如安全编码、最小权限、供应链安全），还面临新的AI特定威胁，包括提示注入、工具污染、会话劫持、混淆代理攻击、令牌传递漏洞以及动态能力修改。

本课程将探讨MCP实施中最关键的安全风险——涵盖认证、授权、权限过度、间接提示注入、会话安全、混淆代理问题、令牌管理和供应链漏洞。您将学习可操作的控制措施和最佳实践，以减轻这些风险，同时利用微软解决方案（如Prompt Shields、Azure内容安全和GitHub高级安全）来增强您的MCP部署。

## 学习目标

完成本课后，您将能够：

- **识别MCP特定威胁**：了解MCP系统中的独特安全风险，包括提示注入、工具污染、权限过度、会话劫持、混淆代理问题、令牌传递漏洞和供应链风险
- **应用安全控制措施**：实施有效的缓解措施，包括强大的认证、最小权限访问、安全令牌管理、会话安全控制和供应链验证
- **利用微软安全解决方案**：理解并部署微软Prompt Shields、Azure内容安全和GitHub高级安全以保护MCP工作负载
- **验证工具安全性**：认识工具元数据验证的重要性，监控动态变化，并防御间接提示注入攻击
- **整合最佳实践**：结合既定的安全基础（如安全编码、服务器加固、零信任）与MCP特定控制措施，实现全面保护

# MCP安全架构与控制

现代MCP实施需要分层的安全方法，既要解决传统软件安全问题，也要应对AI特定威胁。快速发展的MCP规范不断完善其安全控制措施，使其能够更好地与企业安全架构和既定最佳实践集成。

根据[微软数字防御报告](https://aka.ms/mddr)的研究，**98%的报告漏洞可以通过强大的安全卫生措施防止**。最有效的保护策略是将基础安全实践与MCP特定控制措施相结合——经过验证的基础安全措施仍然是降低整体安全风险的最有影响力的方法。

## 当前安全形势

> **注意**：此信息反映截至**2025年8月18日**的MCP安全标准。MCP协议正在快速发展，未来的实施可能会引入新的认证模式和增强的控制措施。请始终参考当前的[MCP规范](https://spec.modelcontextprotocol.io/)、[MCP GitHub仓库](https://github.com/modelcontextprotocol)和[安全最佳实践文档](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)以获取最新指导。

### MCP认证的演变

MCP规范在认证和授权方面经历了显著的演变：

- **初始方法**：早期规范要求开发人员实现自定义认证服务器，MCP服务器充当OAuth 2.0授权服务器，直接管理用户认证
- **当前标准（2025-06-18）**：更新后的规范允许MCP服务器将认证委托给外部身份提供者（如Microsoft Entra ID），提高了安全性并降低了实施复杂性
- **传输层安全**：增强了对本地（STDIO）和远程（可流式HTTP）连接的安全传输机制的支持，并采用适当的认证模式

## 认证与授权安全

### 当前安全挑战

现代MCP实施面临多个认证和授权挑战：

### 风险与威胁向量

- **授权逻辑配置错误**：MCP服务器中的授权实现缺陷可能暴露敏感数据并错误地应用访问控制
- **OAuth令牌泄露**：本地MCP服务器令牌被盗使攻击者能够冒充服务器并访问下游服务
- **令牌传递漏洞**：不当的令牌处理会导致安全控制绕过和责任缺失
- **权限过度**：权限过高的MCP服务器违反最小权限原则，扩大了攻击面

#### 令牌传递：一个关键的反模式

**令牌传递在当前MCP授权规范中被明确禁止**，因为它带来了严重的安全隐患：

##### 安全控制规避
- MCP服务器和下游API依赖于正确的令牌验证来实施关键的安全控制（如速率限制、请求验证、流量监控）
- 客户端直接使用API令牌绕过了这些重要的保护措施，破坏了安全架构

##### 责任与审计挑战  
- MCP服务器无法区分使用上游签发令牌的客户端，破坏了审计轨迹
- 下游资源服务器日志显示误导性的请求来源，而非实际的MCP服务器中介
- 事件调查和合规审计变得更加困难

##### 数据外泄风险
- 未验证的令牌声明使得拥有被盗令牌的恶意行为者能够将MCP服务器作为代理进行数据外泄
- 信任边界被破坏，允许未经授权的访问模式绕过预期的安全控制

##### 多服务攻击向量
- 被多个服务接受的被盗令牌使得攻击者能够在连接的系统之间横向移动
- 当令牌来源无法验证时，服务之间的信任假设可能被破坏

### 安全控制与缓解措施

**关键安全要求：**

> **强制性**：MCP服务器**不得**接受任何未明确为MCP服务器签发的令牌

#### 认证与授权控制

- **严格的授权审查**：对MCP服务器的授权逻辑进行全面审计，以确保只有预期的用户和客户端可以访问敏感资源
  - **实施指南**：[Azure API管理作为MCP服务器的认证网关](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **身份集成**：[使用Microsoft Entra ID进行MCP服务器认证](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **安全令牌管理**：实施[微软的令牌验证和生命周期最佳实践](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - 验证令牌受众声明与MCP服务器身份匹配
  - 实施适当的令牌轮换和过期策略
  - 防止令牌重放攻击和未经授权的使用

- **受保护的令牌存储**：使用静态和传输中的加密技术保护令牌存储
  - **最佳实践**：[安全令牌存储和加密指南](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### 访问控制实施

- **最小权限原则**：仅授予MCP服务器执行预期功能所需的最低权限
  - 定期权限审查和更新以防止权限膨胀
  - **微软文档**：[安全的最小权限访问](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **基于角色的访问控制（RBAC）**：实施细粒度的角色分配
  - 将角色严格限定于特定资源和操作
  - 避免扩展攻击面的广泛或不必要权限

- **持续权限监控**：实施持续的访问审计和监控
  - 监控权限使用模式以发现异常
  - 及时修复过度或未使用的权限

## AI特定安全威胁

### 提示注入与工具操控攻击

现代MCP实施面临复杂的AI特定攻击向量，传统安全措施无法完全应对：

#### **间接提示注入（跨域提示注入）**

**间接提示注入**是MCP支持的AI系统中最关键的漏洞之一。攻击者将恶意指令嵌入外部内容（文档、网页、电子邮件或数据源），AI系统随后将其处理为合法命令。

**攻击场景：**
- **基于文档的注入**：恶意指令隐藏在处理的文档中，触发意外的AI行为
- **网页内容利用**：被攻击的网页包含嵌入的提示，当被抓取时操控AI行为
- **基于电子邮件的攻击**：电子邮件中的恶意提示导致AI助手泄露信息或执行未经授权的操作
- **数据源污染**：被攻击的数据库或API向AI系统提供受污染的内容

**现实影响**：这些攻击可能导致数据外泄、隐私泄露、生成有害内容以及用户交互的操控。详细分析请参阅[Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)。

![提示注入攻击示意图](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.zh.png)

#### **工具污染攻击**

**工具污染**针对定义MCP工具的元数据，利用LLM解释工具描述和参数的方式来影响执行决策。

**攻击机制：**
- **元数据操控**：攻击者将恶意指令注入工具描述、参数定义或使用示例
- **隐形指令**：工具元数据中隐藏的提示被AI模型处理，但对人类用户不可见
- **动态工具修改（“地毯拉动”）**：用户批准的工具随后被修改为执行恶意操作而用户毫不知情
- **参数注入**：工具参数架构中嵌入的恶意内容影响模型行为

**托管服务器风险**：远程MCP服务器风险更高，因为工具定义可以在用户初次批准后更新，导致原本安全的工具变得恶意。详细分析请参阅[Tool Poisoning Attacks (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)。

![工具注入攻击示意图](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.zh.png)

#### **其他AI攻击向量**

- **跨域提示注入（XPIA）**：利用多个域的内容绕过安全控制的复杂攻击
- **动态能力修改**：实时更改工具能力，逃避初始安全评估
- **上下文窗口污染**：操控大上下文窗口以隐藏恶意指令
- **模型混淆攻击**：利用模型局限性制造不可预测或不安全行为

### AI安全风险影响

**高影响后果：**
- **数据外泄**：未经授权的访问和敏感企业或个人数据的盗窃
- **隐私泄露**：暴露个人身份信息（PII）和机密业务数据  
- **系统操控**：对关键系统和工作流程的意外修改
- **凭证盗窃**：认证令牌和服务凭证的泄露
- **横向移动**：利用被攻破的AI系统作为更广泛网络攻击的跳板

### 微软AI安全解决方案

#### **AI Prompt Shields：防御注入攻击的高级保护**

微软**AI Prompt Shields**通过多层安全防护提供对直接和间接提示注入攻击的全面防御：

##### **核心保护机制：**

1. **高级检测与过滤**
   - 机器学习算法和NLP技术检测外部内容中的恶意指令
   - 实时分析文档、网页、电子邮件和数据源中的嵌入威胁
   - 对合法与恶意提示模式的上下文理解

2. **聚焦技术**  
   - 区分可信系统指令与可能被攻破的外部输入
   - 文本转换方法增强模型相关性，同时隔离恶意内容
   - 帮助AI系统保持正确的指令层级，忽略注入的命令

3. **分隔符与数据标记系统**
   - 明确定义可信系统消息与外部输入文本之间的边界
   - 特殊标记突出显示可信与不可信数据源之间的边界
   - 清晰分隔防止指令混淆和未经授权的命令执行

4. **持续威胁情报**
   - 微软持续监控新兴攻击模式并更新防御措施
   - 主动威胁狩猎以发现新的注入技术和攻击向量
   - 定期更新安全模型以保持对不断演变的威胁的有效性

5. **Azure内容安全集成**
   - 综合Azure AI内容安全套件的一部分
   - 额外检测越狱尝试、有害内容和安全策略违规
   - AI应用组件之间的统一安全控制

**实施资源**：[微软Prompt Shields文档](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)

![微软Prompt Shields保护](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.zh.png)


## 高级MCP安全威胁

### 会话劫持漏洞

**会话劫持**是状态化MCP实施中的关键攻击向量，未经授权的方获取并滥用合法会话标识符以冒充客户端并执行未经授权的操作。

#### **攻击场景与风险**

- **会话劫持提示注入**：攻击者通过窃取的会话ID向共享会话状态的服务器注入恶意事件，可能触发有害行为或访问敏感数据
- **直接冒充**：窃取的会话ID使攻击者能够直接调用MCP服务器，绕过认证，将其视为合法用户
- **受损的可恢复流**：攻击者可以提前终止请求，导致合法客户端恢复时可能包含恶意内容

#### **会话管理的安全控制**

**关键要求：**
- **授权验证**：实施授权的MCP服务器**必须**验证所有入站请求，并且**不得**依赖会话进行认证
- **安全会话生成**：使用加密安全的、非确定性的会话 ID，通过安全的随机数生成器生成  
- **用户绑定**：将会话 ID 与用户特定信息绑定，例如使用 `<user_id>:<session_id>` 格式，防止跨用户会话滥用  
- **会话生命周期管理**：实施适当的过期、轮换和失效机制，以限制漏洞窗口  
- **传输安全**：所有通信必须使用 HTTPS，防止会话 ID 被拦截  

### 混淆代理问题

**混淆代理问题**发生在 MCP 服务器作为客户端与第三方服务之间的认证代理时，攻击者可能通过利用静态客户端 ID 绕过授权。

#### **攻击机制与风险**

- **基于 Cookie 的同意绕过**：之前的用户认证会生成同意 Cookie，攻击者通过伪造的重定向 URI 发起恶意授权请求加以利用  
- **授权码窃取**：现有的同意 Cookie 可能导致授权服务器跳过同意屏幕，将授权码重定向到攻击者控制的端点  
- **未授权 API 访问**：窃取的授权码允许攻击者进行令牌交换并冒充用户，无需明确批准  

#### **缓解策略**

**强制性控制：**
- **明确的用户同意要求**：使用静态客户端 ID 的 MCP 代理服务器**必须**为每个动态注册的客户端获取用户同意  
- **OAuth 2.1 安全实施**：遵循当前 OAuth 安全最佳实践，包括在所有授权请求中使用 PKCE（代码交换证明密钥）  
- **严格的客户端验证**：对重定向 URI 和客户端标识符进行严格验证，防止被利用  

### 令牌透传漏洞  

**令牌透传**是一种明确的反模式，MCP 服务器接受未经验证的客户端令牌并将其转发到下游 API，这违反了 MCP 授权规范。

#### **安全影响**

- **控制规避**：直接使用客户端到 API 的令牌绕过了关键的速率限制、验证和监控控制  
- **审计轨迹破坏**：上游签发的令牌使得无法识别客户端，破坏了事件调查能力  
- **基于代理的数据泄露**：未验证的令牌允许恶意行为者利用服务器作为代理进行未授权的数据访问  
- **信任边界破坏**：当令牌来源无法验证时，下游服务的信任假设可能被破坏  
- **多服务攻击扩展**：被攻破的令牌在多个服务间被接受，导致横向移动  

#### **必要的安全控制**

**不可协商的要求：**
- **令牌验证**：MCP 服务器**不得**接受未明确为 MCP 服务器签发的令牌  
- **受众验证**：始终验证令牌的受众声明是否与 MCP 服务器的身份匹配  
- **正确的令牌生命周期管理**：实施短期访问令牌并采用安全的轮换机制  

## AI 系统的供应链安全

供应链安全已超越传统软件依赖，涵盖整个 AI 生态系统。现代 MCP 实现必须严格验证和监控所有与 AI 相关的组件，因为每个组件都可能引入潜在漏洞，危及系统完整性。

### 扩展的 AI 供应链组件

**传统软件依赖：**
- 开源库和框架  
- 容器镜像和基础系统  
- 开发工具和构建流水线  
- 基础设施组件和服务  

**AI 特定的供应链元素：**
- **基础模型**：来自不同提供商的预训练模型，需要验证其来源  
- **嵌入服务**：外部向量化和语义搜索服务  
- **上下文提供者**：数据源、知识库和文档存储库  
- **第三方 API**：外部 AI 服务、机器学习流水线和数据处理端点  
- **模型工件**：权重、配置和微调模型变体  
- **训练数据源**：用于模型训练和微调的数据集  

### 全面的供应链安全策略

#### **组件验证与信任**
- **来源验证**：在集成之前验证所有 AI 组件的来源、许可和完整性  
- **安全评估**：对模型、数据源和 AI 服务进行漏洞扫描和安全审查  
- **声誉分析**：评估 AI 服务提供商的安全记录和实践  
- **合规性验证**：确保所有组件符合组织的安全和监管要求  

#### **安全部署流水线**  
- **自动化 CI/CD 安全**：在自动化部署流水线中集成安全扫描  
- **工件完整性**：对所有部署的工件（代码、模型、配置）实施加密验证  
- **分阶段部署**：采用渐进式部署策略，并在每个阶段进行安全验证  
- **可信工件存储库**：仅从经过验证的安全工件注册表和存储库中部署  

#### **持续监控与响应**
- **依赖扫描**：对所有软件和 AI 组件依赖进行持续漏洞监控  
- **模型监控**：持续评估模型行为、性能漂移和安全异常  
- **服务健康跟踪**：监控外部 AI 服务的可用性、安全事件和策略变化  
- **威胁情报集成**：结合针对 AI 和机器学习安全风险的威胁情报  

#### **访问控制与最小权限**
- **组件级权限**：根据业务需求限制对模型、数据和服务的访问  
- **服务账户管理**：实施专用服务账户，并赋予最小必要权限  
- **网络分段**：隔离 AI 组件并限制服务之间的网络访问  
- **API 网关控制**：使用集中式 API 网关控制和监控对外部 AI 服务的访问  

#### **事件响应与恢复**
- **快速响应程序**：建立针对受损 AI 组件的修补或替换流程  
- **凭据轮换**：自动化系统，用于轮换密钥、API 密钥和服务凭据  
- **回滚能力**：能够快速恢复到之前已知的良好版本的 AI 组件  
- **供应链漏洞恢复**：针对上游 AI 服务妥协的特定响应程序  

### Microsoft 安全工具与集成

**GitHub Advanced Security** 提供全面的供应链保护，包括：  
- **密钥扫描**：自动检测存储库中的凭据、API 密钥和令牌  
- **依赖扫描**：对开源依赖和库进行漏洞评估  
- **CodeQL 分析**：静态代码分析以发现安全漏洞和编码问题  
- **供应链洞察**：了解依赖的健康状况和安全状态  

**Azure DevOps 和 Azure Repos 集成：**
- 在 Microsoft 开发平台中无缝集成安全扫描  
- 在 Azure Pipelines 中对 AI 工作负载进行自动化安全检查  
- 强制执行安全 AI 组件部署的策略  

**Microsoft 内部实践：**
Microsoft 在所有产品中实施了广泛的供应链安全实践。了解更多关于 [Microsoft 软件供应链安全之旅](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/) 的信息。

## 基础安全最佳实践

MCP 的实现继承并构建在组织现有的安全基础之上。加强基础安全实践显著提升了 AI 系统和 MCP 部署的整体安全性。

### 核心安全基础

#### **安全开发实践**
- **遵循 OWASP**：防范 [OWASP Top 10](https://owasp.org/www-project-top-ten/) 的 Web 应用漏洞  
- **AI 特定保护**：实施 [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) 的控制措施  
- **安全的密钥管理**：使用专用的密钥库存储令牌、API 密钥和敏感配置数据  
- **端到端加密**：在所有应用组件和数据流中实施安全通信  
- **输入验证**：严格验证所有用户输入、API 参数和数据源  

#### **基础设施加固**
- **多因素认证**：所有管理和服务账户必须启用 MFA  
- **补丁管理**：对操作系统、框架和依赖进行自动化、及时的补丁更新  
- **身份提供商集成**：通过企业身份提供商（Microsoft Entra ID、Active Directory）集中管理身份  
- **网络分段**：逻辑隔离 MCP 组件，限制横向移动的可能性  
- **最小权限原则**：为所有系统组件和账户分配最小必要权限  

#### **安全监控与检测**
- **全面日志记录**：详细记录 AI 应用活动，包括 MCP 客户端-服务器交互  
- **SIEM 集成**：集中式安全信息和事件管理，用于异常检测  
- **行为分析**：利用 AI 监控系统和用户行为中的异常模式  
- **威胁情报**：集成外部威胁情报和妥协指标（IOCs）  
- **事件响应**：定义明确的安全事件检测、响应和恢复程序  

#### **零信任架构**
- **永不信任，总是验证**：持续验证用户、设备和网络连接  
- **微分段**：对单个工作负载和服务实施精细的网络控制  
- **基于身份的安全**：基于经过验证的身份而非网络位置实施安全策略  
- **持续风险评估**：根据当前上下文和行为动态评估安全态势  
- **条件访问**：基于风险因素、位置和设备信任动态调整访问控制  

### 企业集成模式

#### **Microsoft 安全生态系统集成**
- **Microsoft Defender for Cloud**：全面的云安全态势管理  
- **Azure Sentinel**：云原生 SIEM 和 SOAR 功能，用于 AI 工作负载保护  
- **Microsoft Entra ID**：企业身份和访问管理，支持条件访问策略  
- **Azure Key Vault**：集中式密钥管理，支持硬件安全模块（HSM）  
- **Microsoft Purview**：AI 数据源和工作流的数据治理与合规  

#### **合规与治理**
- **法规对齐**：确保 MCP 实现符合行业特定的合规要求（GDPR、HIPAA、SOC 2）  
- **数据分类**：正确分类和处理 AI 系统处理的敏感数据  
- **审计轨迹**：为合规性和取证调查提供全面的日志记录  
- **隐私控制**：在 AI 系统架构中实施隐私设计原则  
- **变更管理**：对 AI 系统修改进行安全审查的正式流程  

这些基础实践为 MCP 特定的安全控制提供了坚实的安全基线，并为 AI 驱动的应用提供了全面的保护。

## 关键安全要点

- **分层安全方法**：结合基础安全实践（安全编码、最小权限、供应链验证、持续监控）与 AI 特定控制措施，实现全面保护  

- **AI 特定威胁环境**：MCP 系统面临独特风险，包括提示注入、工具中毒、会话劫持、混淆代理问题、令牌透传漏洞和过度权限，这些都需要专门的缓解措施  

- **认证与授权卓越**：使用外部身份提供商（Microsoft Entra ID）实施强大的认证，强制执行正确的令牌验证，绝不接受未明确为 MCP 服务器签发的令牌  

- **AI 攻击防御**：部署 Microsoft Prompt Shields 和 Azure Content Safety 防御间接提示注入和工具中毒攻击，同时验证工具元数据并监控动态变化  

- **会话与传输安全**：使用加密安全的、非确定性的会话 ID 绑定到用户身份，实施正确的会话生命周期管理，绝不将会话用于认证  

- **OAuth 安全最佳实践**：通过动态注册客户端的明确用户同意、PKCE 的正确实施以及严格的重定向 URI 验证，防止混淆代理攻击  

- **令牌安全原则**：避免令牌透传反模式，验证令牌受众声明，实施短期令牌并进行安全轮换，维护清晰的信任边界  

- **全面的供应链安全**：将所有 AI 生态系统组件（模型、嵌入、上下文提供者、外部 API）视为传统软件依赖，实施同等的安全严格性  

- **持续演进**：跟随快速发展的 MCP 规范，参与安全社区标准的制定，并在协议成熟时保持适应性安全态势  

- **Microsoft 安全集成**：利用 Microsoft 的全面安全生态系统（Prompt Shields、Azure Content Safety、GitHub Advanced Security、Entra ID）增强 MCP 部署的保护  

## 综合资源

### **官方 MCP 安全文档**
- [MCP 规范（当前版本：2025-06-18）](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP 安全最佳实践](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP 授权规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  
- [MCP GitHub 仓库](https://github.com/modelcontextprotocol)  

### **安全标准与最佳实践**
- [OAuth 2.0 安全最佳实践 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 Web 应用安全](https://owasp.org/www-project-top-ten/)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/download/43299/?tmstv=1731900559)  
- [Microsoft 数字防御报告](https://aka.ms/mddr)  

### **AI 安全研究与分析**
- [MCP 中的提示注入（Simon Willison）](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)  
- [工具中毒攻击（Invariant Labs）](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)  
- [MCP 安全研究简报（Wiz Security）](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)  
### **Microsoft 安全解决方案**
- [Microsoft Prompt Shields 文档](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure 内容安全服务](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID 安全](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Azure 令牌管理最佳实践](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub 高级安全](https://github.com/security/advanced-security)

### **实施指南与教程**
- [将 Azure API 管理用作 MCP 身份验证网关](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [使用 Microsoft Entra ID 进行 MCP 服务器身份验证](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [安全令牌存储与加密（视频）](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps 与供应链安全**
- [Azure DevOps 安全](https://azure.microsoft.com/products/devops)
- [Azure Repos 安全](https://azure.microsoft.com/products/devops/repos/)
- [Microsoft 供应链安全之旅](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **附加安全文档**

有关全面的安全指导，请参考本部分中的以下专业文档：

- **[MCP 安全最佳实践 2025](./mcp-security-best-practices-2025.md)** - MCP 实施的完整安全最佳实践
- **[Azure 内容安全实施](./azure-content-safety-implementation.md)** - Azure 内容安全集成的实际实施示例  
- **[MCP 安全控制 2025](./mcp-security-controls-2025.md)** - MCP 部署的最新安全控制和技术
- **[MCP 最佳实践快速参考](./mcp-best-practices.md)** - MCP 安全实践的快速参考指南

---

## 下一步

下一步：[第 3 章：入门](../03-GettingStarted/README.md)

**免责声明**：  
本文档使用AI翻译服务[Co-op Translator](https://github.com/Azure/co-op-translator)进行翻译。尽管我们努力确保准确性，但请注意，自动翻译可能包含错误或不准确之处。应以原始语言的文档作为权威来源。对于关键信息，建议使用专业人工翻译。对于因使用本翻译而引起的任何误解或误读，我们概不负责。