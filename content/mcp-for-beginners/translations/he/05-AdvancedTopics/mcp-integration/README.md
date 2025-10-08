<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "f84eaea79c8fa9ab318a494f40891814",
  "translation_date": "2025-08-18T16:49:24+00:00",
  "source_file": "05-AdvancedTopics/mcp-integration/README.md",
  "language_code": "he"
}
-->
# אינטגרציה ארגונית

כאשר בונים שרתי MCP בהקשר ארגוני, לעיתים קרובות יש צורך להשתלב עם פלטפורמות ושירותי AI קיימים. חלק זה עוסק באיך לשלב את MCP עם מערכות ארגוניות כמו Azure OpenAI ו-Microsoft AI Foundry, כדי לאפשר יכולות AI מתקדמות ותזמור כלים.

## מבוא

בשיעור זה תלמדו כיצד לשלב את פרוטוקול Model Context Protocol (MCP) עם מערכות AI ארגוניות, תוך התמקדות ב-Azure OpenAI ו-Microsoft AI Foundry. שילובים אלו מאפשרים לכם לנצל מודלים וכלים חזקים של AI תוך שמירה על הגמישות וההרחבה של MCP.

## מטרות למידה

בסיום השיעור, תוכלו:

- לשלב את MCP עם Azure OpenAI כדי לנצל את יכולות ה-AI שלו.
- ליישם תזמור כלים של MCP עם Azure OpenAI.
- לשלב את MCP עם Microsoft AI Foundry לצורך יכולות מתקדמות של סוכני AI.
- לנצל את Azure Machine Learning (ML) לביצוע פייפליינים של ML ורישום מודלים ככלים של MCP.

## שילוב עם Azure OpenAI

Azure OpenAI מספק גישה למודלים חזקים של AI כמו GPT-4 ואחרים. שילוב MCP עם Azure OpenAI מאפשר לכם לנצל את המודלים הללו תוך שמירה על הגמישות של תזמור הכלים של MCP.

### מימוש ב-C#

בקטע הקוד הבא, אנו מדגימים כיצד לשלב את MCP עם Azure OpenAI באמצעות Azure OpenAI SDK.

```csharp
// .NET Azure OpenAI Integration
using Microsoft.Mcp.Client;
using Azure.AI.OpenAI;
using Microsoft.Extensions.Configuration;
using System.Threading.Tasks;

namespace EnterpriseIntegration
{
    public class AzureOpenAiMcpClient
    {
        private readonly string _endpoint;
        private readonly string _apiKey;
        private readonly string _deploymentName;
        
        public AzureOpenAiMcpClient(IConfiguration config)
        {
            _endpoint = config["AzureOpenAI:Endpoint"];
            _apiKey = config["AzureOpenAI:ApiKey"];
            _deploymentName = config["AzureOpenAI:DeploymentName"];
        }
        
        public async Task<string> GetCompletionWithToolsAsync(string prompt, params string[] allowedTools)
        {
            // Create OpenAI client
            var client = new OpenAIClient(new Uri(_endpoint), new AzureKeyCredential(_apiKey));
            
            // Create completion options with tools
            var completionOptions = new ChatCompletionsOptions
            {
                DeploymentName = _deploymentName,
                Messages = { new ChatMessage(ChatRole.User, prompt) },
                Temperature = 0.7f,
                MaxTokens = 800
            };
            
            // Add tool definitions
            foreach (var tool in allowedTools)
            {
                completionOptions.Tools.Add(new ChatCompletionsFunctionToolDefinition
                {
                    Name = tool,
                    // In a real implementation, you'd add the tool schema here
                });
            }
            
            // Get completion response
            var response = await client.GetChatCompletionsAsync(completionOptions);
            
            // Handle tool calls in the response
            foreach (var toolCall in response.Value.Choices[0].Message.ToolCalls)
            {
                // Implementation to handle Azure OpenAI tool calls with MCP
                // ...
            }
            
            return response.Value.Choices[0].Message.Content;
        }
    }
}
```

בקטע הקוד הקודם:

- הגדרנו את לקוח Azure OpenAI עם נקודת הקצה, שם הפריסה ומפתח ה-API.
- יצרנו מתודה `GetCompletionWithToolsAsync` לקבלת השלמות עם תמיכה בכלים.
- טיפלנו בקריאות לכלים בתגובה.

מומלץ ליישם את הלוגיקה בפועל לטיפול בכלים בהתבסס על ההגדרות הספציפיות של שרת ה-MCP שלכם.

## שילוב עם Microsoft AI Foundry

Azure AI Foundry מספק פלטפורמה לבניית והפעלת סוכני AI. שילוב MCP עם AI Foundry מאפשר לכם לנצל את היכולות שלו תוך שמירה על הגמישות של MCP.

בקטע הקוד הבא, אנו מפתחים אינטגרציה של סוכן שמטפלת בבקשות ומנהלת קריאות לכלים באמצעות MCP.

### מימוש ב-Java

```java
// Java AI Foundry Agent Integration
package com.example.mcp.enterprise;

import com.microsoft.aifoundry.AgentClient;
import com.microsoft.aifoundry.AgentToolResponse;
import com.microsoft.aifoundry.models.AgentRequest;
import com.microsoft.aifoundry.models.AgentResponse;
import com.mcp.client.McpClient;
import com.mcp.tools.ToolRequest;
import com.mcp.tools.ToolResponse;

public class AIFoundryMcpBridge {
    private final AgentClient agentClient;
    private final McpClient mcpClient;
    
    public AIFoundryMcpBridge(String aiFoundryEndpoint, String mcpServerUrl) {
        this.agentClient = new AgentClient(aiFoundryEndpoint);
        this.mcpClient = new McpClient.Builder()
            .setServerUrl(mcpServerUrl)
            .build();
    }
    
    public AgentResponse processAgentRequest(AgentRequest request) {
        // Process the AI Foundry Agent request
        AgentResponse initialResponse = agentClient.processRequest(request);
        
        // Check if the agent requested to use tools
        if (initialResponse.getToolCalls() != null && !initialResponse.getToolCalls().isEmpty()) {
            // For each tool call, route it to the appropriate MCP tool
            for (AgentToolCall toolCall : initialResponse.getToolCalls()) {
                String toolName = toolCall.getName();
                Map<String, Object> parameters = toolCall.getArguments();
                
                // Execute the tool using MCP
                ToolResponse mcpResponse = mcpClient.executeTool(toolName, parameters);
                
                // Create tool response for AI Foundry
                AgentToolResponse toolResponse = new AgentToolResponse(
                    toolCall.getId(),
                    mcpResponse.getResult()
                );
                
                // Submit tool response back to the agent
                initialResponse = agentClient.submitToolResponse(
                    request.getConversationId(), 
                    toolResponse
                );
            }
        }
        
        return initialResponse;
    }
}
```

בקטע הקוד הקודם:

- יצרנו מחלקה `AIFoundryMcpBridge` שמשתלבת עם AI Foundry ו-MCP.
- יישמנו מתודה `processAgentRequest` שמטפלת בבקשת סוכן של AI Foundry.
- טיפלנו בקריאות לכלים על ידי ביצוען דרך לקוח MCP והחזרת התוצאות לסוכן של AI Foundry.

## שילוב MCP עם Azure ML

שילוב MCP עם Azure Machine Learning (ML) מאפשר לכם לנצל את היכולות החזקות של Azure ML תוך שמירה על הגמישות של MCP. שילוב זה יכול לשמש לביצוע פייפליינים של ML, רישום מודלים ככלים, וניהול משאבי מחשוב.

### מימוש ב-Python

```python
# Python Azure AI Integration
from mcp_client import McpClient
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Environment, AmlCompute
import os
import asyncio

class EnterpriseAiIntegration:
    def __init__(self, mcp_server_url, subscription_id, resource_group, workspace_name):
        # Set up MCP client
        self.mcp_client = McpClient(server_url=mcp_server_url)
        
        # Set up Azure ML client
        self.credential = DefaultAzureCredential()
        self.ml_client = MLClient(
            self.credential,
            subscription_id,
            resource_group,
            workspace_name
        )
    
    async def execute_ml_pipeline(self, pipeline_name, input_data):
        """Executes an ML pipeline in Azure ML"""
        # First process the input data using MCP tools
        processed_data = await self.mcp_client.execute_tool(
            "dataPreprocessor",
            {
                "data": input_data,
                "operations": ["normalize", "clean", "transform"]
            }
        )
        
        # Submit the pipeline to Azure ML
        pipeline_job = self.ml_client.jobs.create_or_update(
            entity={
                "name": pipeline_name,
                "display_name": f"MCP-triggered {pipeline_name}",
                "experiment_name": "mcp-integration",
                "inputs": {
                    "processed_data": processed_data.result
                }
            }
        )
        
        # Return job information
        return {
            "job_id": pipeline_job.id,
            "status": pipeline_job.status,
            "creation_time": pipeline_job.creation_context.created_at
        }
    
    async def register_ml_model_as_tool(self, model_name, model_version="latest"):
        """Registers an Azure ML model as an MCP tool"""
        # Get model details
        if model_version == "latest":
            model = self.ml_client.models.get(name=model_name, label="latest")
        else:
            model = self.ml_client.models.get(name=model_name, version=model_version)
        
        # Create deployment environment
        env = Environment(
            name="mcp-model-env",
            conda_file="./environments/inference-env.yml"
        )
        
        # Set up compute
        compute = self.ml_client.compute.get("mcp-inference")
        
        # Deploy model as online endpoint
        deployment = self.ml_client.online_deployments.create_or_update(
            endpoint_name=f"mcp-{model_name}",
            deployment={
                "name": f"mcp-{model_name}-deployment",
                "model": model.id,
                "environment": env,
                "compute": compute,
                "scale_settings": {
                    "scale_type": "auto",
                    "min_instances": 1,
                    "max_instances": 3
                }
            }
        )
        
        # Create MCP tool schema based on model schema
        tool_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # Add input properties based on model schema
        for input_name, input_spec in model.signature.inputs.items():
            tool_schema["properties"][input_name] = {
                "type": self._map_ml_type_to_json_type(input_spec.type)
            }
            tool_schema["required"].append(input_name)
        
        # Register as MCP tool
        # In a real implementation, you would create a tool that calls the endpoint
        return {
            "model_name": model_name,
            "model_version": model.version,
            "endpoint": deployment.endpoint_uri,
            "tool_schema": tool_schema
        }
    
    def _map_ml_type_to_json_type(self, ml_type):
        """Maps ML data types to JSON schema types"""
        mapping = {
            "float": "number",
            "int": "integer",
            "bool": "boolean",
            "str": "string",
            "object": "object",
            "array": "array"
        }
        return mapping.get(ml_type, "string")
```

בקטע הקוד הקודם:

- יצרנו מחלקה `EnterpriseAiIntegration` שמשתלבת עם MCP ו-Azure ML.
- יישמנו מתודה `execute_ml_pipeline` שמעבדת נתוני קלט באמצעות כלים של MCP ושולחת פייפליין ML ל-Azure ML.
- יישמנו מתודה `register_ml_model_as_tool` שרושמת מודל של Azure ML ככלי MCP, כולל יצירת סביבת פריסה ומשאבי מחשוב נדרשים.
- מיפינו סוגי נתונים של Azure ML לסוגי JSON schema לצורך רישום כלים.
- השתמשנו בתכנות אסינכרוני לטיפול בפעולות שעשויות להיות ארוכות, כמו ביצוע פייפליינים של ML ורישום מודלים.

## מה הלאה

- [5.2 מולטימודליות](../mcp-multi-modality/README.md)

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש להיות מודעים לכך שתרגומים אוטומטיים עשויים להכיל שגיאות או אי דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור סמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. איננו נושאים באחריות לאי הבנות או לפרשנויות שגויות הנובעות משימוש בתרגום זה.