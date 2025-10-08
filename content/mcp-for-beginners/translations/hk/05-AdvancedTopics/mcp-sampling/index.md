<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "193889b580c86bbb1e4f577114a5ce4e",
  "translation_date": "2025-07-16T21:14:00+00:00",
  "source_file": "05-AdvancedTopics/mcp-sampling/README.md",
  "language_code": "hk"
}
-->
# Sampling in Model Context Protocol

Sampling 是 MCP 的一個強大功能，允許伺服器透過客戶端請求 LLM 的完成結果，從而實現複雜的代理行為，同時保持安全性和私隱。合適的 sampling 配置能顯著提升回應質素和效能。MCP 提供了一種標準化方式，透過特定參數控制模型生成文本的隨機性、創意和連貫性。

## 介紹

本課程將探討如何在 MCP 請求中配置 sampling 參數，並了解 sampling 的底層協議機制。

## 學習目標

完成本課程後，你將能夠：

- 理解 MCP 中可用的主要 sampling 參數。
- 為不同使用場景配置 sampling 參數。
- 實現可重現結果的確定性 sampling。
- 根據上下文和用戶偏好動態調整 sampling 參數。
- 應用 sampling 策略提升模型在各種場景下的表現。
- 理解 MCP 客戶端與伺服器間 sampling 的運作流程。

## MCP 中的 Sampling 運作方式

MCP 的 sampling 流程如下：

1. 伺服器向客戶端發送 `sampling/createMessage` 請求
2. 客戶端審核請求並可進行修改
3. 客戶端從 LLM 進行抽樣
4. 客戶端審核完成結果
5. 客戶端將結果返回給伺服器

這種人機互動設計確保用戶能掌控 LLM 所見及生成的內容。

## Sampling 參數概覽

MCP 定義了以下可在客戶端請求中配置的 sampling 參數：

| 參數 | 說明 | 典型範圍 |
|-----------|-------------|---------------|
| `temperature` | 控制選擇 token 的隨機程度 | 0.0 - 1.0 |
| `maxTokens` | 最大生成 token 數量 | 整數值 |
| `stopSequences` | 遇到自訂停止序列即停止生成 | 字串陣列 |
| `metadata` | 其他供應商特定參數 | JSON 物件 |

許多 LLM 供應商透過 `metadata` 欄位支持額外參數，包括：

| 常見擴展參數 | 說明 | 典型範圍 |
|-----------|-------------|---------------|
| `top_p` | Nucleus sampling，限制 token 選擇於累積概率最高部分 | 0.0 - 1.0 |
| `top_k` | 限制 token 選擇於前 K 個選項 | 1 - 100 |
| `presence_penalty` | 根據文本中 token 出現與否進行懲罰 | -2.0 - 2.0 |
| `frequency_penalty` | 根據文本中 token 出現頻率進行懲罰 | -2.0 - 2.0 |
| `seed` | 指定隨機種子以實現可重現結果 | 整數值 |

## 範例請求格式

以下是 MCP 中向客戶端請求 sampling 的範例：

```json
{
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "What files are in the current directory?"
        }
      }
    ],
    "systemPrompt": "You are a helpful file system assistant.",
    "includeContext": "thisServer",
    "maxTokens": 100,
    "temperature": 0.7
  }
}
```

## 回應格式

客戶端返回完成結果：

```json
{
  "model": "string",  // Name of the model used
  "stopReason": "endTurn" | "stopSequence" | "maxTokens" | "string",
  "role": "assistant",
  "content": {
    "type": "text",
    "text": "string"
  }
}
```

## 人機互動控制

MCP sampling 設計時考慮了人類監督：

- **對於提示詞**：
  - 客戶端應向用戶展示建議的提示詞
  - 用戶應能修改或拒絕提示詞
  - 系統提示詞可被過濾或修改
  - 上下文包含由客戶端控制

- **對於完成結果**：
  - 客戶端應向用戶展示完成結果
  - 用戶應能修改或拒絕完成結果
  - 客戶端可過濾或修改完成結果
  - 用戶控制使用哪個模型

基於這些原則，接下來我們將展示如何在不同程式語言中實作 sampling，重點放在各大 LLM 供應商普遍支持的參數。

## 安全考量

實作 MCP sampling 時，請注意以下安全最佳實踐：

- **驗證所有訊息內容**，確保安全後再發送給客戶端
- **清理提示詞和完成結果中的敏感資訊**
- **實施速率限制**以防止濫用
- **監控 sampling 使用情況**，偵測異常模式
- **使用安全協議加密傳輸資料**
- **依照相關法規處理用戶資料私隱**
- **審計 sampling 請求**以確保合規與安全
- **控制成本暴露**，設定適當限制
- **為 sampling 請求設置逾時機制**
- **妥善處理模型錯誤**，提供適當備援方案

Sampling 參數可微調語言模型行為，達成確定性與創意輸出間的理想平衡。

接下來看看如何在不同程式語言中配置這些參數。

# [.NET](../../../../05-AdvancedTopics/mcp-sampling)

```csharp
// .NET Example: Configuring sampling parameters in MCP
public class SamplingExample
{
    public async Task RunWithSamplingAsync()
    {
        // Create MCP client with sampling configuration
        var client = new McpClient("https://mcp-server-url.com");
        
        // Create request with specific sampling parameters
        var request = new McpRequest
        {
            Prompt = "Generate creative ideas for a mobile app",
            SamplingParameters = new SamplingParameters
            {
                Temperature = 0.8f,     // Higher temperature for more creative outputs
                TopP = 0.95f,           // Nucleus sampling parameter
                TopK = 40,              // Limit token selection to top K options
                FrequencyPenalty = 0.5f, // Reduce repetition
                PresencePenalty = 0.2f   // Encourage diversity
            },
            AllowedTools = new[] { "ideaGenerator", "marketAnalyzer" }
        };
        
        // Send request using specific sampling configuration
        var response = await client.SendRequestAsync(request);
        
        // Output results
        Console.WriteLine($"Generated with Temperature={request.SamplingParameters.Temperature}:");
        Console.WriteLine(response.GeneratedText);
    }
}
```

在上述程式碼中，我們：

- 建立了帶有特定伺服器 URL 的 MCP 客戶端。
- 配置了包含 `temperature`、`top_p` 和 `top_k` 等 sampling 參數的請求。
- 發送請求並列印生成的文本。
- 使用了：
    - `allowedTools` 指定模型生成時可使用的工具，此例中允許 `ideaGenerator` 和 `marketAnalyzer` 工具協助產生創意應用點子。
    - `frequencyPenalty` 和 `presencePenalty` 控制輸出中的重複度與多樣性。
    - `temperature` 控制輸出的隨機性，數值越高回應越具創意。
    - `top_p` 限制 token 選擇於累積概率最高部分，提升生成文本質量。
    - `top_k` 限制模型只從前 K 個最可能的 token 中選擇，有助生成更連貫的回應。
    - `frequencyPenalty` 和 `presencePenalty` 減少重複並鼓勵多樣性。

# [JavaScript](../../../../05-AdvancedTopics/mcp-sampling)

```javascript
// JavaScript Example: Temperature and Top-P sampling configuration
const { McpClient } = require('@mcp/client');

async function demonstrateSampling() {
  // Initialize the MCP client
  const client = new McpClient({
    serverUrl: 'https://mcp-server-example.com',
    apiKey: process.env.MCP_API_KEY
  });
  
  // Configure request with different sampling parameters
  const creativeSampling = {
    temperature: 0.9,    // Higher temperature = more randomness/creativity
    topP: 0.92,          // Consider tokens with top 92% probability mass
    frequencyPenalty: 0.6, // Reduce repetition of token sequences
    presencePenalty: 0.4   // Penalize tokens that have appeared in the text so far
  };
  
  const factualSampling = {
    temperature: 0.2,    // Lower temperature = more deterministic/factual
    topP: 0.85,          // Slightly more focused token selection
    frequencyPenalty: 0.2, // Minimal repetition penalty
    presencePenalty: 0.1   // Minimal presence penalty
  };
  
  try {
    // Send two requests with different sampling configurations
    const creativeResponse = await client.sendPrompt(
      "Generate innovative ideas for sustainable urban transportation",
      {
        allowedTools: ['ideaGenerator', 'environmentalImpactTool'],
        ...creativeSampling
      }
    );
    
    const factualResponse = await client.sendPrompt(
      "Explain how electric vehicles impact carbon emissions",
      {
        allowedTools: ['factChecker', 'dataAnalysisTool'],
        ...factualSampling
      }
    );
    
    console.log('Creative Response (temperature=0.9):');
    console.log(creativeResponse.generatedText);
    
    console.log('\nFactual Response (temperature=0.2):');
    console.log(factualResponse.generatedText);
    
  } catch (error) {
    console.error('Error demonstrating sampling:', error);
  }
}

demonstrateSampling();
```

在上述程式碼中，我們：

- 初始化了帶有伺服器 URL 和 API 金鑰的 MCP 客戶端。
- 配置了兩組 sampling 參數：一組用於創意任務，另一組用於事實性任務。
- 使用這些配置發送請求，允許模型針對不同任務使用特定工具。
- 列印生成的回應，展示不同 sampling 參數的效果。
- 使用 `allowedTools` 指定模型生成時可使用的工具，創意任務允許 `ideaGenerator` 和 `environmentalImpactTool`，事實性任務允許 `factChecker` 和 `dataAnalysisTool`。
- 使用 `temperature` 控制輸出的隨機性，數值越高回應越具創意。
- 使用 `top_p` 限制 token 選擇於累積概率最高部分，提升生成文本質量。
- 使用 `frequencyPenalty` 和 `presencePenalty` 減少重複並鼓勵多樣性。
- 使用 `top_k` 限制模型只從前 K 個最可能的 token 中選擇，有助生成更連貫的回應。

---

## 確定性 Sampling

對於需要一致輸出的應用，確定性 sampling 可確保結果可重現。其方法是使用固定的隨機種子並將 temperature 設為零。

以下示範如何在不同程式語言中實作確定性 sampling。

# [Java](../../../../05-AdvancedTopics/mcp-sampling)

```java
// Java Example: Deterministic responses with fixed seed
public class DeterministicSamplingExample {
    public void demonstrateDeterministicResponses() {
        McpClient client = new McpClient.Builder()
            .setServerUrl("https://mcp-server-example.com")
            .build();
            
        long fixedSeed = 12345; // Using a fixed seed for deterministic results
        
        // First request with fixed seed
        McpRequest request1 = new McpRequest.Builder()
            .setPrompt("Generate a random number between 1 and 100")
            .setSeed(fixedSeed)
            .setTemperature(0.0) // Zero temperature for maximum determinism
            .build();
            
        // Second request with the same seed
        McpRequest request2 = new McpRequest.Builder()
            .setPrompt("Generate a random number between 1 and 100")
            .setSeed(fixedSeed)
            .setTemperature(0.0)
            .build();
        
        // Execute both requests
        McpResponse response1 = client.sendRequest(request1);
        McpResponse response2 = client.sendRequest(request2);
        
        // Responses should be identical due to same seed and temperature=0
        System.out.println("Response 1: " + response1.getGeneratedText());
        System.out.println("Response 2: " + response2.getGeneratedText());
        System.out.println("Are responses identical: " + 
            response1.getGeneratedText().equals(response2.getGeneratedText()));
    }
}
```

在上述程式碼中，我們：

- 建立了帶有指定伺服器 URL 的 MCP 客戶端。
- 配置了兩個請求，使用相同提示詞、固定種子和零 temperature。
- 發送兩個請求並列印生成文本。
- 展示由於 sampling 配置的確定性（相同種子和 temperature），回應結果完全相同。
- 使用 `setSeed` 指定固定隨機種子，確保相同輸入每次生成相同輸出。
- 將 `temperature` 設為零，確保最大確定性，模型總是選擇最可能的下一個 token，無隨機性。

# [JavaScript](../../../../05-AdvancedTopics/mcp-sampling)

```javascript
// JavaScript Example: Deterministic responses with seed control
const { McpClient } = require('@mcp/client');

async function deterministicSampling() {
  const client = new McpClient({
    serverUrl: 'https://mcp-server-example.com'
  });
  
  const fixedSeed = 12345;
  const prompt = "Generate a random password with 8 characters";
  
  try {
    // First request with fixed seed
    const response1 = await client.sendPrompt(prompt, {
      seed: fixedSeed,
      temperature: 0.0  // Zero temperature for maximum determinism
    });
    
    // Second request with same seed and temperature
    const response2 = await client.sendPrompt(prompt, {
      seed: fixedSeed,
      temperature: 0.0
    });
    
    // Third request with different seed but same temperature
    const response3 = await client.sendPrompt(prompt, {
      seed: 67890,
      temperature: 0.0
    });
    
    console.log('Response 1:', response1.generatedText);
    console.log('Response 2:', response2.generatedText);
    console.log('Response 3:', response3.generatedText);
    console.log('Responses 1 and 2 match:', response1.generatedText === response2.generatedText);
    console.log('Responses 1 and 3 match:', response1.generatedText === response3.generatedText);
    
  } catch (error) {
    console.error('Error in deterministic sampling demo:', error);
  }
}

deterministicSampling();
```

在上述程式碼中，我們：

- 初始化了帶有伺服器 URL 的 MCP 客戶端。
- 配置了兩個請求，使用相同提示詞、固定種子和零 temperature。
- 發送兩個請求並列印生成文本。
- 展示由於 sampling 配置的確定性（相同種子和 temperature），回應結果完全相同。
- 使用 `seed` 指定固定隨機種子，確保相同輸入每次生成相同輸出。
- 將 `temperature` 設為零，確保最大確定性，模型總是選擇最可能的下一個 token，無隨機性。
- 對第三個請求使用不同種子，展示即使提示詞和 temperature 相同，改變種子也會產生不同輸出。

---

## 動態 Sampling 配置

智慧 sampling 會根據每次請求的上下文和需求調整參數。這意味著根據任務類型、用戶偏好或歷史表現，動態調整 temperature、top_p 和懲罰參數。

以下示範如何在不同程式語言中實作動態 sampling。

# [Python](../../../../05-AdvancedTopics/mcp-sampling)

```python
# Python Example: Dynamic sampling based on request context
class DynamicSamplingService:
    def __init__(self, mcp_client):
        self.client = mcp_client
        
    async def generate_with_adaptive_sampling(self, prompt, task_type, user_preferences=None):
        """Uses different sampling strategies based on task type and user preferences"""
        
        # Define sampling presets for different task types
        sampling_presets = {
            "creative": {"temperature": 0.9, "top_p": 0.95, "frequency_penalty": 0.7},
            "factual": {"temperature": 0.2, "top_p": 0.85, "frequency_penalty": 0.2},
            "code": {"temperature": 0.3, "top_p": 0.9, "frequency_penalty": 0.5},
            "analytical": {"temperature": 0.4, "top_p": 0.92, "frequency_penalty": 0.3}
        }
        
        # Select base preset
        sampling_params = sampling_presets.get(task_type, sampling_presets["factual"])
        
        # Adjust based on user preferences if provided
        if user_preferences:
            if "creativity_level" in user_preferences:
                # Scale temperature based on creativity preference (1-10)
                creativity = min(max(user_preferences["creativity_level"], 1), 10) / 10
                sampling_params["temperature"] = 0.1 + (0.9 * creativity)
            
            if "diversity" in user_preferences:
                # Adjust top_p based on desired response diversity
                diversity = min(max(user_preferences["diversity"], 1), 10) / 10
                sampling_params["top_p"] = 0.6 + (0.39 * diversity)
        
        # Create and send request with custom sampling parameters
        response = await self.client.send_request(
            prompt=prompt,
            temperature=sampling_params["temperature"],
            top_p=sampling_params["top_p"],
            frequency_penalty=sampling_params["frequency_penalty"]
        )
        
        # Return response with sampling metadata for transparency
        return {
            "text": response.generated_text,
            "applied_sampling": sampling_params,
            "task_type": task_type
        }
```

在上述程式碼中，我們：

- 建立了 `DynamicSamplingService` 類別，管理自適應 sampling。
- 定義了不同任務類型（創意、事實、程式碼、分析）的 sampling 預設配置。
- 根據任務類型選擇基礎 sampling 預設。
- 根據用戶偏好（如創意程度和多樣性）調整 sampling 參數。
- 發送帶有動態配置 sampling 參數的請求。
- 返回生成文本及所用 sampling 參數和任務類型，確保透明度。
- 使用 `temperature` 控制輸出的隨機性，數值越高回應越具創意。
- 使用 `top_p` 限制 token 選擇於累積概率最高部分，提升生成文本質量。
- 使用 `frequency_penalty` 減少重複並鼓勵多樣性。
- 使用 `user_preferences` 允許根據用戶定義的創意和多樣性等級自訂 sampling 參數。
- 使用 `task_type` 決定請求的適當 sampling 策略，根據任務性質提供更貼切回應。
- 使用 `send_request` 方法發送帶有配置 sampling 參數的提示詞，確保模型依指定需求生成文本。
- 使用 `generated_text` 取得模型回應，並連同 sampling 參數和任務類型一併返回，方便後續分析或展示。
- 使用 `min` 和 `max` 函數確保用戶偏好值在有效範圍內，避免無效配置。

# [JavaScript Dynamic](../../../../05-AdvancedTopics/mcp-sampling)

```javascript
// JavaScript Example: Dynamic sampling configuration based on user context
class AdaptiveSamplingManager {
  constructor(mcpClient) {
    this.client = mcpClient;
    
    // Define base sampling profiles
    this.samplingProfiles = {
      creative: { temperature: 0.85, topP: 0.94, frequencyPenalty: 0.7, presencePenalty: 0.5 },
      factual: { temperature: 0.2, topP: 0.85, frequencyPenalty: 0.3, presencePenalty: 0.1 },
      code: { temperature: 0.25, topP: 0.9, frequencyPenalty: 0.4, presencePenalty: 0.3 },
      conversational: { temperature: 0.7, topP: 0.9, frequencyPenalty: 0.6, presencePenalty: 0.4 }
    };
    
    // Track historical performance
    this.performanceHistory = [];
  }
  
  // Detect task type from prompt
  detectTaskType(prompt, context = {}) {
    const promptLower = prompt.toLowerCase();
    
    // Simple heuristic detection - could be enhanced with ML classification
    if (context.taskType) return context.taskType;
    
    if (promptLower.includes('code') || 
        promptLower.includes('function') || 
        promptLower.includes('program')) {
      return 'code';
    }
    
    if (promptLower.includes('explain') || 
        promptLower.includes('what is') || 
        promptLower.includes('how does')) {
      return 'factual';
    }
    
    if (promptLower.includes('creative') || 
        promptLower.includes('imagine') || 
        promptLower.includes('story')) {
      return 'creative';
    }
    
    // Default to conversational if no clear type is detected
    return 'conversational';
  }
  
  // Calculate sampling parameters based on context and user preferences
  getSamplingParameters(prompt, context = {}) {
    // Detect the type of task
    const taskType = this.detectTaskType(prompt, context);
    
    // Get base profile
    let params = {...this.samplingProfiles[taskType]};
    
    // Adjust based on user preferences
    if (context.userPreferences) {
      const { creativity, precision, consistency } = context.userPreferences;
      
      if (creativity !== undefined) {
        // Scale from 1-10 to appropriate temperature range
        params.temperature = 0.1 + (creativity * 0.09); // 0.1-1.0
      }
      
      if (precision !== undefined) {
        // Higher precision means lower topP (more focused selection)
        params.topP = 1.0 - (precision * 0.05); // 0.5-1.0
      }
      
      if (consistency !== undefined) {
        // Higher consistency means lower penalties
        params.frequencyPenalty = 0.1 + ((10 - consistency) * 0.08); // 0.1-0.9
      }
    }
    
    // Apply learned adjustments from performance history
    this.applyLearnedAdjustments(params, taskType);
    
    return params;
  }
  
  applyLearnedAdjustments(params, taskType) {
    // Simple adaptive logic - could be enhanced with more sophisticated algorithms
    const relevantHistory = this.performanceHistory
      .filter(entry => entry.taskType === taskType)
      .slice(-5); // Only consider recent history
    
    if (relevantHistory.length > 0) {
      // Calculate average performance scores
      const avgScore = relevantHistory.reduce((sum, entry) => sum + entry.score, 0) / relevantHistory.length;
      
      // If performance is below threshold, adjust parameters
      if (avgScore < 0.7) {
        // Slight adjustment toward safer values
        params.temperature = Math.max(params.temperature * 0.9, 0.1);
        params.topP = Math.max(params.topP * 0.95, 0.5);
      }
    }
  }
  
  recordPerformance(prompt, samplingParams, response, score) {
    // Record performance for future adjustments
    this.performanceHistory.push({
      timestamp: Date.now(),
      taskType: this.detectTaskType(prompt),
      samplingParams,
      responseLength: response.generatedText.length,
      score // 0-1 rating of response quality
    });
    
    // Limit history size
    if (this.performanceHistory.length > 100) {
      this.performanceHistory.shift();
    }
  }
  
  async generateResponse(prompt, context = {}) {
    // Get optimized sampling parameters
    const samplingParams = this.getSamplingParameters(prompt, context);
    
    // Send request with optimized parameters
    const response = await this.client.sendPrompt(prompt, {
      ...samplingParams,
      allowedTools: context.allowedTools || []
    });
    
    // If user provides feedback, record it for future optimization
    if (context.recordPerformance) {
      this.recordPerformance(prompt, samplingParams, response, context.feedbackScore || 0.5);
    }
    
    return {
      response,
      appliedSamplingParams: samplingParams,
      detectedTaskType: this.detectTaskType(prompt, context)
    };
  }
}

// Example usage
async function demonstrateAdaptiveSampling() {
  const client = new McpClient({
    serverUrl: 'https://mcp-server-example.com'
  });
  
  const samplingManager = new AdaptiveSamplingManager(client);
  
  try {
    // Creative task with custom user preferences
    const creativeResult = await samplingManager.generateResponse(
      "Write a short poem about artificial intelligence",
      {
        userPreferences: {
          creativity: 9,  // High creativity (1-10)
          consistency: 3  // Low consistency (1-10)
        }
      }
    );
    
    console.log('Creative Task:');
    console.log(`Detected type: ${creativeResult.detectedTaskType}`);
    console.log('Applied sampling:', creativeResult.appliedSamplingParams);
    console.log(creativeResult.response.generatedText);
    
    // Code generation task
    const codeResult = await samplingManager.generateResponse(
      "Write a JavaScript function to calculate the Fibonacci sequence",
      {
        userPreferences: {
          creativity: 2,  // Low creativity
          precision: 8,   // High precision
          consistency: 9  // High consistency
        }
      }
    );
    
    console.log('\nCode Task:');
    console.log(`Detected type: ${codeResult.detectedTaskType}`);
    console.log('Applied sampling:', codeResult.appliedSamplingParams);
    console.log(codeResult.response.generatedText);
    
  } catch (error) {
    console.error('Error in adaptive sampling demo:', error);
  }
}

demonstrateAdaptiveSampling();
```

在上述程式碼中，我們：

- 建立了 `AdaptiveSamplingManager` 類別，根據任務類型和用戶偏好管理動態 sampling。
- 定義了不同任務類型（創意、事實、程式碼、對話）的 sampling 配置檔。
- 實作方法透過簡單啟發式判斷提示詞的任務類型。
- 根據偵測到的任務類型和用戶偏好計算 sampling 參數。
- 應用基於歷史表現的學習調整，優化 sampling 參數。
- 記錄表現以便未來調整，讓系統能從過往互動中學習。
- 發送帶有動態配置 sampling 參數的請求，並返回生成文本及所用參數和偵測到的任務類型。
- 使用了：
    - `userPreferences` 允許根據用戶定義的創意、精確度和一致性等級自訂 sampling 參數。
    - `detectTaskType` 根據提示詞判斷任務性質，提供更貼切回應。
    - `recordPerformance` 記錄生成回應的表現，讓系統能持續調整和改進。
    - `applyLearnedAdjustments` 根據歷史表現調整 sampling 參數，提升模型生成高質量回應的能力。
    - `generateResponse` 封裝整個生成流程，方便以不同提示詞和上下文呼叫。
    - `allowedTools` 指定模型生成時可使用的工具，提升回應的上下文感知能力。
    - `feedbackScore` 允許用戶對生成回應質量提供反饋，進一步優化模型表現。
    - `performanceHistory` 保存過往互動紀錄，讓系統從成功與失敗中學習。
    - `getSamplingParameters` 根據請求上下文動態調整 sampling 參數，使模型行為更靈活且具回應性。
    - `detectTaskType` 分類提示詞所屬任務，讓系統針對不同請求採用適當 sampling 策略。
    - `samplingProfiles` 定義不同任務類型的基礎 sampling 配置，方便根據請求性質快速調整。

---

## 下一步

- [5.7 Scaling](../mcp-scaling/README.md)

**免責聲明**：  
本文件乃使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或誤釋承擔責任。