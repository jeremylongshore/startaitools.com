<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2aa9dbc165e104764fa57e8a0d3f1c73",
  "translation_date": "2025-07-14T07:20:15+00:00",
  "source_file": "10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab1/README.md",
  "language_code": "zh"
}
-->
# 🚀 模块 1：AI 工具包基础

[![Duration](https://img.shields.io/badge/Duration-15%20minutes-blue.svg)]()
[![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green.svg)]()
[![Prerequisites](https://img.shields.io/badge/Prerequisites-VS%20Code-orange.svg)]()

## 📋 学习目标

完成本模块后，您将能够：
- ✅ 安装并配置 Visual Studio Code 的 AI 工具包
- ✅ 浏览模型目录并了解不同的模型来源
- ✅ 使用 Playground 进行模型测试和实验
- ✅ 使用 Agent Builder 创建自定义 AI 代理
- ✅ 比较不同提供商的模型性能
- ✅ 应用提示工程的最佳实践

## 🧠 AI 工具包（AITK）简介

**Visual Studio Code 的 AI 工具包**是微软的旗舰扩展，将 VS Code 转变为一个全面的 AI 开发环境。它架起了 AI 研究与实际应用开发之间的桥梁，让各个技能水平的开发者都能轻松使用生成式 AI。

### 🌟 主要功能

| 功能 | 描述 | 使用场景 |
|---------|-------------|----------|
| **🗂️ 模型目录** | 访问来自 GitHub、ONNX、OpenAI、Anthropic、Google 的 100+ 模型 | 模型发现与选择 |
| **🔌 BYOM 支持** | 集成您自己的模型（本地/远程） | 自定义模型部署 |
| **🎮 交互式 Playground** | 通过聊天界面实时测试模型 | 快速原型设计与测试 |
| **📎 多模态支持** | 处理文本、图像和附件 | 复杂的 AI 应用 |
| **⚡ 批量处理** | 同时运行多个提示 | 高效测试流程 |
| **📊 模型评估** | 内置指标（F1、相关性、相似度、一致性） | 性能评估 |

### 🎯 AI 工具包的重要性

- **🚀 加速开发**：从想法到原型只需几分钟
- **🔄 统一工作流**：一个界面支持多个 AI 提供商
- **🧪 简单实验**：无需复杂设置即可比较模型
- **📈 生产就绪**：无缝从原型过渡到部署

## 🛠️ 前置条件与设置

### 📦 安装 AI 工具包扩展

**步骤 1：访问扩展市场**
1. 打开 Visual Studio Code
2. 进入扩展视图（`Ctrl+Shift+X` 或 `Cmd+Shift+X`）
3. 搜索 “AI Toolkit”

**步骤 2：选择版本**
- **🟢 正式版**：推荐用于生产环境
- **🔶 预发布版**：抢先体验最新功能

**步骤 3：安装并激活**

![AI Toolkit Extension](../../../../translated_images/aitkext.d28945a03eed003c39fc39bc96ae655af9b64b9b922e78e88b07214420ed7985.zh.png)

### ✅ 验证清单
- [ ] AI 工具包图标出现在 VS Code 侧边栏
- [ ] 扩展已启用并激活
- [ ] 输出面板无安装错误

## 🧪 实操练习 1：探索 GitHub 模型

**🎯 目标**：掌握模型目录并测试您的第一个 AI 模型

### 📊 第 1 步：浏览模型目录

模型目录是您进入 AI 生态系统的门户。它汇聚了多个提供商的模型，方便您发现和比较选项。

**🔍 导航指南：**

点击 AI 工具包侧边栏中的 **MODELS - Catalog**

![Model Catalog](../../../../translated_images/aimodel.263ed2be013d8fb0e2265c4f742cfe490f6f00eca5e132ec50438c8e826e34ed.zh.png)

**💡 小贴士**：寻找具备特定功能且符合您用例的模型（例如代码生成、创意写作、分析）。

**⚠️ 注意**：GitHub 托管的模型（即 GitHub 模型）免费使用，但请求和令牌有速率限制。如果您想访问非 GitHub 模型（即通过 Azure AI 或其他端点托管的外部模型），需要提供相应的 API 密钥或认证信息。

### 🚀 第 2 步：添加并配置您的第一个模型

**模型选择策略：**
- **GPT-4.1**：适合复杂推理和分析
- **Phi-4-mini**：轻量快速，适合简单任务

**🔧 配置流程：**
1. 从目录中选择 **OpenAI GPT-4.1**
2. 点击 **Add to My Models** —— 将模型注册到您的模型列表
3. 选择 **Try in Playground** 启动测试环境
4. 等待模型初始化（首次设置可能需要一些时间）

![Playground Setup](../../../../translated_images/playground.dd6f5141344878ca4d4f3de819775da7b113518941accf37c291117c602f85db.zh.png)

**⚙️ 理解模型参数：**
- **Temperature**：控制创造力（0 = 确定性，1 = 创造性）
- **Max Tokens**：最大响应长度
- **Top-p**：核采样，控制响应多样性

### 🎯 第 3 步：掌握 Playground 界面

Playground 是您的 AI 实验室。以下是最大化其潜力的方法：

**🎨 提示工程最佳实践：**
1. **具体明确**：清晰详细的指令效果更好
2. **提供上下文**：包含相关背景信息
3. **使用示例**：用示例告诉模型您的需求
4. **反复迭代**：根据初步结果优化提示

**🧪 测试场景：**
```markdown
# Example 1: Code Generation
"Write a Python function that calculates the factorial of a number using recursion. Include error handling and docstrings."

# Example 2: Creative Writing
"Write a professional email to a client explaining a project delay, maintaining a positive tone while being transparent about challenges."

# Example 3: Data Analysis
"Analyze this sales data and provide insights: [paste your data]. Focus on trends, anomalies, and actionable recommendations."
```

![Testing Results](../../../../translated_images/result.1dfcf211fb359cf65902b09db191d3bfc65713ca15e279c1a30be213bb526949.zh.png)

### 🏆 挑战练习：模型性能对比

**🎯 目标**：使用相同提示比较不同模型，了解它们的优势

**📋 操作说明：**
1. 将 **Phi-4-mini** 添加到您的工作区
2. 对 GPT-4.1 和 Phi-4-mini 使用相同的提示

![set](../../../../translated_images/set.88132df189ecde2cbbda256c1841db5aac8e9bdeba1a4e343dfa031b9545d6c9.zh.png)

3. 比较响应质量、速度和准确性
4. 在结果部分记录您的发现

![Model Comparison](../../../../translated_images/compare.97746cd0f907495503c1fc217739f3890dc76ea5f6fd92379a6db0cc331feb58.zh.png)

**💡 关键洞察：**
- 何时使用大型语言模型（LLM）与小型语言模型（SLM）
- 成本与性能的权衡
- 不同模型的专长能力

## 🤖 实操练习 2：使用 Agent Builder 构建自定义代理

**🎯 目标**：创建针对特定任务和工作流的专用 AI 代理

### 🏗️ 第 1 步：了解 Agent Builder

Agent Builder 是 AI 工具包的核心亮点。它允许您创建定制的 AI 助手，将大型语言模型的强大能力与自定义指令、特定参数和专业知识结合起来。

**🧠 代理架构组成：**
- **核心模型**：基础 LLM（GPT-4、Groks、Phi 等）
- **系统提示**：定义代理的个性和行为
- **参数**：针对性能优化的细节设置
- **工具集成**：连接外部 API 和 MCP 服务
- **记忆**：对话上下文和会话持久化

![Agent Builder Interface](../../../../translated_images/agentbuilder.25895b2d2f8c02e7aa99dd40e105877a6f1db8f0441180087e39db67744b361f.zh.png)

### ⚙️ 第 2 步：深入代理配置

**🎨 创建有效的系统提示：**
```markdown
# Template Structure:
## Role Definition
You are a [specific role] with expertise in [domain].

## Capabilities
- List specific abilities
- Define scope of knowledge
- Clarify limitations

## Behavior Guidelines
- Response style (formal, casual, technical)
- Output format preferences
- Error handling approach

## Examples
Provide 2-3 examples of ideal interactions
```

*当然，您也可以使用 Generate System Prompt 让 AI 帮助生成和优化提示*

**🔧 参数优化：**
| 参数 | 推荐范围 | 使用场景 |
|-----------|------------------|----------|
| **Temperature** | 0.1-0.3 | 技术性/事实性回答 |
| **Temperature** | 0.7-0.9 | 创意/头脑风暴任务 |
| **Max Tokens** | 500-1000 | 简洁回答 |
| **Max Tokens** | 2000-4000 | 详细解释 |

### 🐍 第 3 步：实战练习 - Python 编程代理

**🎯 任务**：创建专门的 Python 编程助手

**📋 配置步骤：**

1. **模型选择**：选择 **Claude 3.5 Sonnet**（非常适合代码相关任务）

2. **系统提示设计**：
```markdown
# Python Programming Expert Agent

## Role
You are a senior Python developer with 10+ years of experience. You excel at writing clean, efficient, and well-documented Python code.

## Capabilities
- Write production-ready Python code
- Debug complex issues
- Explain code concepts clearly
- Suggest best practices and optimizations
- Provide complete working examples

## Response Format
- Always include docstrings
- Add inline comments for complex logic
- Suggest testing approaches
- Mention relevant libraries when applicable

## Code Quality Standards
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Handle exceptions gracefully
- Write readable, maintainable code
```

3. **参数配置**：
   - Temperature：0.2（保证代码稳定可靠）
   - Max Tokens：2000（详细解释）
   - Top-p：0.9（平衡创造力）

![Python Agent Configuration](../../../../translated_images/pythonagent.5e51b406401c165fcabfd66f2d943c27f46b5fed0f9fb73abefc9e91ca3489d4.zh.png)

### 🧪 第 4 步：测试您的 Python 代理

**测试场景：**
1. **基础功能**：“创建一个判断质数的函数”
2. **复杂算法**：“实现一个包含插入、删除和查找方法的二叉搜索树”
3. **实际问题**：“构建一个支持速率限制和重试机制的网页爬虫”
4. **调试**：“修复这段代码 [粘贴有问题的代码]”

**🏆 成功标准：**
- ✅ 代码无错误运行
- ✅ 包含适当的文档说明
- ✅ 遵循 Python 最佳实践
- ✅ 提供清晰解释
- ✅ 给出改进建议

## 🎓 模块 1 总结与后续步骤

### 📊 知识检测

测试您的理解：
- [ ] 能否解释目录中模型的区别？
- [ ] 是否成功创建并测试了自定义代理？
- [ ] 是否理解如何针对不同用例优化参数？
- [ ] 能否设计有效的系统提示？

### 📚 额外资源

- **AI 工具包文档**：[微软官方文档](https://github.com/microsoft/vscode-ai-toolkit)
- **提示工程指南**：[最佳实践](https://platform.openai.com/docs/guides/prompt-engineering)
- **AI 工具包中的模型**：[开发中的模型](https://github.com/microsoft/vscode-ai-toolkit/blob/main/doc/models.md)

**🎉 恭喜！** 您已掌握 AI 工具包的基础知识，准备好构建更高级的 AI 应用！

### 🔜 继续下一模块

准备好学习更高级功能了吗？请继续阅读 **[模块 2：MCP 与 AI 工具包基础](../lab2/README.md)**，您将学习如何：
- 使用模型上下文协议（MCP）连接代理与外部工具
- 使用 Playwright 构建浏览器自动化代理
- 将 MCP 服务器与 AI 工具包代理集成
- 利用外部数据和能力增强您的代理

**免责声明**：  
本文件使用 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 进行翻译。虽然我们力求准确，但请注意自动翻译可能包含错误或不准确之处。原始文件的母语版本应被视为权威来源。对于重要信息，建议使用专业人工翻译。对于因使用本翻译而产生的任何误解或误释，我们概不负责。