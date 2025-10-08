<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T13:25:50+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "ar"
}
-->
# إنشاء عميل باستخدام LLM

حتى الآن، رأيت كيفية إنشاء خادم وعميل. كان العميل قادرًا على الاتصال بالخادم بشكل صريح لعرض أدواته وموارده ومطالبه. ومع ذلك، فإن هذه الطريقة ليست عملية جدًا. يعيش المستخدم الخاص بك في عصر الوكلاء ويتوقع استخدام المطالبات والتواصل مع LLM للقيام بذلك. بالنسبة للمستخدم الخاص بك، لا يهم إذا كنت تستخدم MCP لتخزين قدراتك أم لا، ولكنهم يتوقعون استخدام اللغة الطبيعية للتفاعل. إذًا كيف يمكننا حل هذه المشكلة؟ الحل هو إضافة LLM إلى العميل.

## نظرة عامة

في هذا الدرس، نركز على إضافة LLM إلى العميل الخاص بك ونوضح كيف يوفر هذا تجربة أفضل بكثير للمستخدم.

## أهداف التعلم

بنهاية هذا الدرس، ستكون قادرًا على:

- إنشاء عميل باستخدام LLM.
- التفاعل بسلاسة مع خادم MCP باستخدام LLM.
- توفير تجربة مستخدم نهائية أفضل على جانب العميل.

## النهج

دعونا نحاول فهم النهج الذي نحتاج إلى اتخاذه. إضافة LLM تبدو بسيطة، ولكن هل سنقوم بذلك بالفعل؟

إليك كيفية تفاعل العميل مع الخادم:

1. إنشاء اتصال بالخادم.

1. عرض القدرات والمطالب والموارد والأدوات، وحفظ مخططها.

1. إضافة LLM وتمرير القدرات المحفوظة ومخططها بتنسيق يفهمه LLM.

1. معالجة مطالبة المستخدم عن طريق تمريرها إلى LLM مع الأدوات المدرجة بواسطة العميل.

رائع، الآن نفهم كيف يمكننا القيام بذلك على مستوى عالٍ، دعونا نجرب ذلك في التمرين أدناه.

## تمرين: إنشاء عميل باستخدام LLM

في هذا التمرين، سنتعلم كيفية إضافة LLM إلى العميل الخاص بنا.

### المصادقة باستخدام GitHub Personal Access Token

إن إنشاء رمز GitHub هو عملية مباشرة. إليك كيفية القيام بذلك:

- انتقل إلى إعدادات GitHub – انقر على صورة ملفك الشخصي في الزاوية العلوية اليمنى وحدد إعدادات.
- انتقل إلى إعدادات المطور – قم بالتمرير لأسفل وانقر على إعدادات المطور.
- اختر Personal Access Tokens – انقر على Fine-grained tokens ثم Generate new token.
- قم بتكوين الرمز الخاص بك – أضف ملاحظة للمرجع، حدد تاريخ انتهاء الصلاحية، واختر النطاقات الضرورية (الأذونات). في هذه الحالة، تأكد من إضافة إذن النماذج.
- قم بإنشاء ونسخ الرمز – انقر على Generate token، وتأكد من نسخه فورًا، حيث لن تتمكن من رؤيته مرة أخرى.

### -1- الاتصال بالخادم

لنقم بإنشاء العميل الخاص بنا أولاً:

#### TypeScript

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js";
import OpenAI from "openai";
import { z } from "zod"; // Import zod for schema validation

class MCPClient {
    private openai: OpenAI;
    private client: Client;
    constructor(){
        this.openai = new OpenAI({
            baseURL: "https://models.inference.ai.azure.com", 
            apiKey: process.env.GITHUB_TOKEN,
        });

        this.client = new Client(
            {
                name: "example-client",
                version: "1.0.0"
            },
            {
                capabilities: {
                prompts: {},
                resources: {},
                tools: {}
                }
            }
            );    
    }
}
```

في الكود السابق قمنا بـ:

- استيراد المكتبات اللازمة.
- إنشاء فئة تحتوي على عضوين، `client` و `openai`، لمساعدتنا في إدارة العميل والتفاعل مع LLM على التوالي.
- تكوين مثيل LLM الخاص بنا لاستخدام نماذج GitHub عن طريق تعيين `baseUrl` للإشارة إلى واجهة API للاستدلال.

#### Python

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="mcp",  # Executable
    args=["run", "server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())

```

في الكود السابق قمنا بـ:

- استيراد المكتبات اللازمة لـ MCP.
- إنشاء عميل.

#### .NET

```csharp
using Azure;
using Azure.AI.Inference;
using Azure.Identity;
using System.Text.Json;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;
using System.Text.Json;

var clientTransport = new StdioClientTransport(new()
{
    Name = "Demo Server",
    Command = "/workspaces/mcp-for-beginners/03-GettingStarted/02-client/solution/server/bin/Debug/net8.0/server",
    Arguments = [],
});

await using var mcpClient = await McpClientFactory.CreateAsync(clientTransport);
```

#### Java

أولاً، ستحتاج إلى إضافة تبعيات LangChain4j إلى ملف `pom.xml` الخاص بك. أضف هذه التبعيات لتمكين تكامل MCP ودعم نماذج GitHub:

```xml
<properties>
    <langchain4j.version>1.0.0-beta3</langchain4j.version>
</properties>

<dependencies>
    <!-- LangChain4j MCP Integration -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-mcp</artifactId>
        <version>${langchain4j.version}</version>
    </dependency>
    
    <!-- OpenAI Official API Client -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-open-ai-official</artifactId>
        <version>${langchain4j.version}</version>
    </dependency>
    
    <!-- GitHub Models Support -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-github-models</artifactId>
        <version>${langchain4j.version}</version>
    </dependency>
    
    <!-- Spring Boot Starter (optional, for production apps) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>
```

ثم قم بإنشاء فئة العميل الخاصة بك في Java:

```java
import dev.langchain4j.mcp.McpToolProvider;
import dev.langchain4j.mcp.client.DefaultMcpClient;
import dev.langchain4j.mcp.client.McpClient;
import dev.langchain4j.mcp.client.transport.McpTransport;
import dev.langchain4j.mcp.client.transport.http.HttpMcpTransport;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openaiofficial.OpenAiOfficialChatModel;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.tool.ToolProvider;

import java.time.Duration;
import java.util.List;

public class LangChain4jClient {
    
    public static void main(String[] args) throws Exception {        // Configure the LLM to use GitHub Models
        ChatLanguageModel model = OpenAiOfficialChatModel.builder()
                .isGitHubModels(true)
                .apiKey(System.getenv("GITHUB_TOKEN"))
                .timeout(Duration.ofSeconds(60))
                .modelName("gpt-4.1-nano")
                .build();

        // Create MCP transport for connecting to server
        McpTransport transport = new HttpMcpTransport.Builder()
                .sseUrl("http://localhost:8080/sse")
                .timeout(Duration.ofSeconds(60))
                .logRequests(true)
                .logResponses(true)
                .build();

        // Create MCP client
        McpClient mcpClient = new DefaultMcpClient.Builder()
                .transport(transport)
                .build();
    }
}
```

في الكود السابق قمنا بـ:

- **إضافة تبعيات LangChain4j**: المطلوبة لتكامل MCP، عميل OpenAI الرسمي، ودعم نماذج GitHub.
- **استيراد مكتبات LangChain4j**: لتكامل MCP ووظائف نموذج الدردشة OpenAI.
- **إنشاء `ChatLanguageModel`**: تم تكوينه لاستخدام نماذج GitHub مع رمز GitHub الخاص بك.
- **إعداد النقل عبر HTTP**: باستخدام أحداث الخادم المرسلة (SSE) للاتصال بخادم MCP.
- **إنشاء عميل MCP**: الذي سيتولى الاتصال بالخادم.
- **استخدام دعم MCP المدمج في LangChain4j**: الذي يبسط التكامل بين LLM وخوادم MCP.

#### Rust

يفترض هذا المثال أن لديك خادم MCP يعتمد على Rust قيد التشغيل. إذا لم يكن لديك واحد، ارجع إلى درس [01-first-server](../01-first-server/README.md) لإنشاء الخادم.

بمجرد أن يكون لديك خادم MCP يعتمد على Rust، افتح نافذة الأوامر وانتقل إلى نفس الدليل الذي يوجد فيه الخادم. ثم قم بتشغيل الأمر التالي لإنشاء مشروع عميل LLM جديد:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

أضف التبعيات التالية إلى ملف `Cargo.toml` الخاص بك:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> لا توجد مكتبة Rust رسمية لـ OpenAI، ومع ذلك، فإن مكتبة `async-openai` هي [مكتبة مدارة من قبل المجتمع](https://platform.openai.com/docs/libraries/rust#rust) تُستخدم بشكل شائع.

افتح ملف `src/main.rs` واستبدل محتواه بالكود التالي:

```rust
use async_openai::{Client, config::OpenAIConfig};
use rmcp::{
    RmcpError,
    model::{CallToolRequestParam, ListToolsResult},
    service::{RoleClient, RunningService, ServiceExt},
    transport::{ConfigureCommandExt, TokioChildProcess},
};
use serde_json::{Value, json};
use std::error::Error;
use tokio::process::Command;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Initial message
    let mut messages = vec![json!({"role": "user", "content": "What is the sum of 3 and 2?"})];

    // Setup OpenAI client
    let api_key = std::env::var("OPENAI_API_KEY")?;
    let openai_client = Client::with_config(
        OpenAIConfig::new()
            .with_api_base("https://models.github.ai/inference/chat")
            .with_api_key(api_key),
    );

    // Setup MCP client
    let server_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("calculator-server");

    let mcp_client = ()
        .serve(
            TokioChildProcess::new(Command::new("cargo").configure(|cmd| {
                cmd.arg("run").current_dir(server_dir);
            }))
            .map_err(RmcpError::transport_creation::<TokioChildProcess>)?,
        )
        .await?;

    // TODO: Get MCP tool listing 

    // TODO: LLM conversation with tool calls

    Ok(())
}
```

يقوم هذا الكود بإعداد تطبيق Rust أساسي سيتصل بخادم MCP ونماذج GitHub للتفاعل مع LLM.

> [!IMPORTANT]
> تأكد من تعيين متغير البيئة `OPENAI_API_KEY` باستخدام رمز GitHub الخاص بك قبل تشغيل التطبيق.

رائع، في الخطوة التالية، دعونا نعرض القدرات على الخادم.

### -2- عرض قدرات الخادم

الآن سنقوم بالاتصال بالخادم وطلب قدراته:

#### TypeScript

في نفس الفئة، أضف الطرق التالية:

```typescript
async connectToServer(transport: Transport) {
     await this.client.connect(transport);
     this.run();
     console.error("MCPClient started on stdin/stdout");
}

async run() {
    console.log("Asking server for available tools");

    // listing tools
    const toolsResult = await this.client.listTools();
}
```

في الكود السابق قمنا بـ:

- إضافة كود للاتصال بالخادم، `connectToServer`.
- إنشاء طريقة `run` مسؤولة عن إدارة تدفق التطبيق الخاص بنا. حتى الآن، تعرض الأدوات فقط ولكننا سنضيف المزيد قريبًا.

#### Python

```python
# List available resources
resources = await session.list_resources()
print("LISTING RESOURCES")
for resource in resources:
    print("Resource: ", resource)

# List available tools
tools = await session.list_tools()
print("LISTING TOOLS")
for tool in tools.tools:
    print("Tool: ", tool.name)
    print("Tool", tool.inputSchema["properties"])
```

إليك ما أضفناه:

- عرض الموارد والأدوات وطبعها. بالنسبة للأدوات، نعرض أيضًا `inputSchema` الذي نستخدمه لاحقًا.

#### .NET

```csharp
async Task<List<ChatCompletionsToolDefinition>> GetMcpTools()
{
    Console.WriteLine("Listing tools");
    var tools = await mcpClient.ListToolsAsync();

    List<ChatCompletionsToolDefinition> toolDefinitions = new List<ChatCompletionsToolDefinition>();

    foreach (var tool in tools)
    {
        Console.WriteLine($"Connected to server with tools: {tool.Name}");
        Console.WriteLine($"Tool description: {tool.Description}");
        Console.WriteLine($"Tool parameters: {tool.JsonSchema}");

        // TODO: convert tool definition from MCP tool to LLm tool     
    }

    return toolDefinitions;
}
```

في الكود السابق قمنا بـ:

- عرض الأدوات المتاحة على خادم MCP.
- لكل أداة، عرض الاسم والوصف ومخططها. الأخير هو شيء سنستخدمه لاستدعاء الأدوات قريبًا.

#### Java

```java
// Create a tool provider that automatically discovers MCP tools
ToolProvider toolProvider = McpToolProvider.builder()
        .mcpClients(List.of(mcpClient))
        .build();

// The MCP tool provider automatically handles:
// - Listing available tools from the MCP server
// - Converting MCP tool schemas to LangChain4j format
// - Managing tool execution and responses
```

في الكود السابق قمنا بـ:

- إنشاء `McpToolProvider` الذي يكتشف ويسجل جميع الأدوات تلقائيًا من خادم MCP.
- يتولى موفر الأدوات تحويل مخططات أدوات MCP إلى تنسيق أدوات LangChain4j داخليًا.
- هذا النهج يلغي عملية عرض الأدوات وتحويلها يدويًا.

#### Rust

يتم استرداد الأدوات من خادم MCP باستخدام طريقة `list_tools`. في وظيفة `main` الخاصة بك، بعد إعداد عميل MCP، أضف الكود التالي:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- تحويل قدرات الخادم إلى أدوات LLM

الخطوة التالية بعد عرض قدرات الخادم هي تحويلها إلى تنسيق يفهمه LLM. بمجرد القيام بذلك، يمكننا توفير هذه القدرات كأدوات لـ LLM.

#### TypeScript

1. أضف الكود التالي لتحويل الاستجابة من خادم MCP إلى تنسيق أداة يمكن لـ LLM استخدامه:

    ```typescript
    openAiToolAdapter(tool: {
        name: string;
        description?: string;
        input_schema: any;
        }) {
        // Create a zod schema based on the input_schema
        const schema = z.object(tool.input_schema);
    
        return {
            type: "function" as const, // Explicitly set type to "function"
            function: {
            name: tool.name,
            description: tool.description,
            parameters: {
            type: "object",
            properties: tool.input_schema.properties,
            required: tool.input_schema.required,
            },
            },
        };
    }

    ```

    يأخذ الكود أعلاه استجابة من خادم MCP ويحولها إلى تعريف أداة يمكن لـ LLM فهمه.

1. دعونا نحدث طريقة `run` التالية لعرض قدرات الخادم:

    ```typescript
    async run() {
        console.log("Asking server for available tools");
        const toolsResult = await this.client.listTools();
        const tools = toolsResult.tools.map((tool) => {
            return this.openAiToolAdapter({
            name: tool.name,
            description: tool.description,
            input_schema: tool.inputSchema,
            });
        });
    }
    ```

    في الكود السابق، قمنا بتحديث طريقة `run` لتقوم بالتكرار عبر النتيجة ولكل إدخال استدعاء `openAiToolAdapter`.

#### Python

1. أولاً، دعونا ننشئ وظيفة المحول التالية:

    ```python
    def convert_to_llm_tool(tool):
        tool_schema = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "type": "function",
                "parameters": {
                    "type": "object",
                    "properties": tool.inputSchema["properties"]
                }
            }
        }

        return tool_schema
    ```

    في الوظيفة أعلاه `convert_to_llm_tools`، نأخذ استجابة أداة MCP ونحولها إلى تنسيق يمكن لـ LLM فهمه.

1. بعد ذلك، دعونا نحدث كود العميل الخاص بنا للاستفادة من هذه الوظيفة كما يلي:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    هنا، نضيف استدعاء لـ `convert_to_llm_tool` لتحويل استجابة أداة MCP إلى شيء يمكننا تغذيته لـ LLM لاحقًا.

#### .NET

1. دعونا نضيف كود لتحويل استجابة أداة MCP إلى شيء يمكن لـ LLM فهمه:

```csharp
ChatCompletionsToolDefinition ConvertFrom(string name, string description, JsonElement jsonElement)
{ 
    // convert the tool to a function definition
    FunctionDefinition functionDefinition = new FunctionDefinition(name)
    {
        Description = description,
        Parameters = BinaryData.FromObjectAsJson(new
        {
            Type = "object",
            Properties = jsonElement
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase })
    };

    // create a tool definition
    ChatCompletionsToolDefinition toolDefinition = new ChatCompletionsToolDefinition(functionDefinition);
    return toolDefinition;
}
```

في الكود السابق قمنا بـ:

- إنشاء وظيفة `ConvertFrom` التي تأخذ الاسم والوصف ومخطط الإدخال.
- تعريف وظيفة تقوم بإنشاء FunctionDefinition يتم تمريرها إلى ChatCompletionsDefinition. الأخير هو شيء يمكن لـ LLM فهمه.

1. دعونا نرى كيف يمكننا تحديث بعض الكود الحالي للاستفادة من هذه الوظيفة أعلاه:

    ```csharp
    async Task<List<ChatCompletionsToolDefinition>> GetMcpTools()
    {
        Console.WriteLine("Listing tools");
        var tools = await mcpClient.ListToolsAsync();

        List<ChatCompletionsToolDefinition> toolDefinitions = new List<ChatCompletionsToolDefinition>();

        foreach (var tool in tools)
        {
            Console.WriteLine($"Connected to server with tools: {tool.Name}");
            Console.WriteLine($"Tool description: {tool.Description}");
            Console.WriteLine($"Tool parameters: {tool.JsonSchema}");

            JsonElement propertiesElement;
            tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

            var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
            Console.WriteLine($"Tool definition: {def}");
            toolDefinitions.Add(def);

            Console.WriteLine($"Properties: {propertiesElement}");        
        }

        return toolDefinitions;
    }
    ```    In the preceding code, we've:

    - Update the function to convert the MCP tool response to an LLm tool. Let's highlight the code we added:

        ```csharp
        JsonElement propertiesElement;
        tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

        var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
        Console.WriteLine($"Tool definition: {def}");
        toolDefinitions.Add(def);
        ```

        The input schema is part of the tool response but on the "properties" attribute, so we need to extract. Furthermore, we now call `ConvertFrom` with the tool details. Now we've done the heavy lifting, let's see how it call comes together as we handle a user prompt next.

#### Java

```java
// Create a Bot interface for natural language interaction
public interface Bot {
    String chat(String prompt);
}

// Configure the AI service with LLM and MCP tools
Bot bot = AiServices.builder(Bot.class)
        .chatLanguageModel(model)
        .toolProvider(toolProvider)
        .build();
```

في الكود السابق قمنا بـ:

- تعريف واجهة `Bot` بسيطة للتفاعلات باللغة الطبيعية.
- استخدام خدمات LangChain4j لربط LLM تلقائيًا بموفر أدوات MCP.
- يتولى الإطار تلقائيًا تحويل مخططات الأدوات واستدعاء الوظائف وراء الكواليس.
- هذا النهج يلغي عملية تحويل الأدوات يدويًا - يتولى LangChain4j جميع التعقيدات لتحويل أدوات MCP إلى تنسيق متوافق مع LLM.

#### Rust

لتحويل استجابة أداة MCP إلى تنسيق يمكن لـ LLM فهمه، سنضيف وظيفة مساعدة تقوم بتنسيق قائمة الأدوات. أضف الكود التالي إلى ملف `main.rs` الخاص بك أسفل وظيفة `main`. سيتم استدعاء هذا عند تقديم الطلبات إلى LLM:

```rust
async fn format_tools(tools: &ListToolsResult) -> Result<Vec<Value>, Box<dyn Error>> {
    let tools_json = serde_json::to_value(tools)?;
    let Some(tools_array) = tools_json.get("tools").and_then(|t| t.as_array()) else {
        return Ok(vec![]);
    };

    let formatted_tools = tools_array
        .iter()
        .filter_map(|tool| {
            let name = tool.get("name")?.as_str()?;
            let description = tool.get("description")?.as_str()?;
            let schema = tool.get("inputSchema")?;

            Some(json!({
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": schema.get("properties").unwrap_or(&json!({})),
                        "required": schema.get("required").unwrap_or(&json!([]))
                    }
                }
            }))
        })
        .collect();

    Ok(formatted_tools)
}
```

رائع، نحن الآن جاهزون لمعالجة أي طلبات من المستخدم، لذا دعونا نتعامل مع ذلك بعد ذلك.

### -4- معالجة طلب مطالبة المستخدم

في هذا الجزء من الكود، سنتعامل مع طلبات المستخدم.

#### TypeScript

1. أضف طريقة سيتم استخدامها لاستدعاء LLM:

    ```typescript
    async callTools(
        tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[],
        toolResults: any[]
    ) {
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);


        // 2. Call the server's tool 
        const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
        });

        console.log("Tool result: ", toolResult);

        // 3. Do something with the result
        // TODO  

        }
    }
    ```

    في الكود السابق قمنا بـ:

    - إضافة طريقة `callTools`.
    - الطريقة تأخذ استجابة LLM وتتحقق لمعرفة الأدوات التي تم استدعاؤها، إن وجدت:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - استدعاء أداة، إذا أشار LLM إلى أنه يجب استدعاؤها:

        ```typescript
        // 2. Call the server's tool 
        const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
        });

        console.log("Tool result: ", toolResult);

        // 3. Do something with the result
        // TODO  
        ```

1. تحديث طريقة `run` لتشمل استدعاءات LLM واستدعاء `callTools`:

    ```typescript

    // 1. Create messages that's input for the LLM
    const prompt = "What is the sum of 2 and 3?"

    const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
            {
                role: "user",
                content: prompt,
            },
        ];

    console.log("Querying LLM: ", messages[0].content);

    // 2. Calling the LLM
    let response = this.openai.chat.completions.create({
        model: "gpt-4o-mini",
        max_tokens: 1000,
        messages,
        tools: tools,
    });    

    let results: any[] = [];

    // 3. Go through the LLM response,for each choice, check if it has tool calls 
    (await response).choices.map(async (choice: { message: any; }) => {
        const message = choice.message;
        if (message.tool_calls) {
            console.log("Making tool call")
            await this.callTools(message.tool_calls, results);
        }
    });
    ```

رائع، دعونا نعرض الكود بالكامل:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js";
import OpenAI from "openai";
import { z } from "zod"; // Import zod for schema validation

class MyClient {
    private openai: OpenAI;
    private client: Client;
    constructor(){
        this.openai = new OpenAI({
            baseURL: "https://models.inference.ai.azure.com", // might need to change to this url in the future: https://models.github.ai/inference
            apiKey: process.env.GITHUB_TOKEN,
        });

        this.client = new Client(
            {
                name: "example-client",
                version: "1.0.0"
            },
            {
                capabilities: {
                prompts: {},
                resources: {},
                tools: {}
                }
            }
            );    
    }

    async connectToServer(transport: Transport) {
        await this.client.connect(transport);
        this.run();
        console.error("MCPClient started on stdin/stdout");
    }

    openAiToolAdapter(tool: {
        name: string;
        description?: string;
        input_schema: any;
          }) {
          // Create a zod schema based on the input_schema
          const schema = z.object(tool.input_schema);
      
          return {
            type: "function" as const, // Explicitly set type to "function"
            function: {
              name: tool.name,
              description: tool.description,
              parameters: {
              type: "object",
              properties: tool.input_schema.properties,
              required: tool.input_schema.required,
              },
            },
          };
    }
    
    async callTools(
        tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[],
        toolResults: any[]
      ) {
        for (const tool_call of tool_calls) {
          const toolName = tool_call.function.name;
          const args = tool_call.function.arguments;
    
          console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);
    
    
          // 2. Call the server's tool 
          const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
          });
    
          console.log("Tool result: ", toolResult);
    
          // 3. Do something with the result
          // TODO  
    
         }
    }

    async run() {
        console.log("Asking server for available tools");
        const toolsResult = await this.client.listTools();
        const tools = toolsResult.tools.map((tool) => {
            return this.openAiToolAdapter({
              name: tool.name,
              description: tool.description,
              input_schema: tool.inputSchema,
            });
        });

        const prompt = "What is the sum of 2 and 3?";
    
        const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
            {
                role: "user",
                content: prompt,
            },
        ];

        console.log("Querying LLM: ", messages[0].content);
        let response = this.openai.chat.completions.create({
            model: "gpt-4o-mini",
            max_tokens: 1000,
            messages,
            tools: tools,
        });    

        let results: any[] = [];
    
        // 1. Go through the LLM response,for each choice, check if it has tool calls 
        (await response).choices.map(async (choice: { message: any; }) => {
          const message = choice.message;
          if (message.tool_calls) {
              console.log("Making tool call")
              await this.callTools(message.tool_calls, results);
          }
        });
    }
    
}

let client = new MyClient();
 const transport = new StdioClientTransport({
            command: "node",
            args: ["./build/index.js"]
        });

client.connectToServer(transport);
```

#### Python

1. دعونا نضيف بعض الاستيرادات اللازمة لاستدعاء LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. بعد ذلك، دعونا نضيف الوظيفة التي ستستدعي LLM:

    ```python
    # llm

    def call_llm(prompt, functions):
        token = os.environ["GITHUB_TOKEN"]
        endpoint = "https://models.inference.ai.azure.com"

        model_name = "gpt-4o"

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        print("CALLING LLM")
        response = client.complete(
            messages=[
                {
                "role": "system",
                "content": "You are a helpful assistant.",
                },
                {
                "role": "user",
                "content": prompt,
                },
            ],
            model=model_name,
            tools = functions,
            # Optional parameters
            temperature=1.,
            max_tokens=1000,
            top_p=1.    
        )

        response_message = response.choices[0].message
        
        functions_to_call = []

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                print("TOOL: ", tool_call)
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                functions_to_call.append({ "name": name, "args": args })

        return functions_to_call
    ```

    في الكود السابق قمنا بـ:

    - تمرير وظائفنا، التي وجدناها على خادم MCP وقمنا بتحويلها، إلى LLM.
    - ثم قمنا باستدعاء LLM باستخدام هذه الوظائف.
    - ثم، نقوم بفحص النتيجة لمعرفة الوظائف التي يجب استدعاؤها، إن وجدت.
    - أخيرًا، نمرر مصفوفة من الوظائف للاستدعاء.

1. الخطوة الأخيرة، دعونا نحدث الكود الرئيسي الخاص بنا:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    هناك، كانت هذه الخطوة الأخيرة، في الكود أعلاه نحن:

    - استدعاء أداة MCP عبر `call_tool` باستخدام وظيفة اعتقد LLM أنه يجب استدعاؤها بناءً على مطالبتنا.
    - طباعة نتيجة استدعاء الأداة إلى خادم MCP.

#### .NET

1. دعونا نعرض بعض الكود لطلب مطالبة LLM:

    ```csharp
    var tools = await GetMcpTools();

    for (int i = 0; i < tools.Count; i++)
    {
        var tool = tools[i];
        Console.WriteLine($"MCP Tools def: {i}: {tool}");
    }

    // 0. Define the chat history and the user message
    var userMessage = "add 2 and 4";

    chatHistory.Add(new ChatRequestUserMessage(userMessage));

    // 1. Define tools
    ChatCompletionsToolDefinition def = CreateToolDefinition();


    // 2. Define options, including the tools
    var options = new ChatCompletionsOptions(chatHistory)
    {
        Model = "gpt-4o-mini",
        Tools = { tools[0] }
    };

    // 3. Call the model  

    ChatCompletions? response = await client.CompleteAsync(options);
    var content = response.Content;

    ```

    في الكود السابق قمنا بـ:

    - جلب الأدوات من خادم MCP، `var tools = await GetMcpTools()`.
    - تعريف مطالبة المستخدم `userMessage`.
    - إنشاء كائن خيارات يحدد النموذج والأدوات.
    - تقديم طلب نحو LLM.

1. خطوة أخيرة، دعونا نرى إذا كان LLM يعتقد أنه يجب استدعاء وظيفة:

    ```csharp
    // 4. Check if the response contains a function call
    ChatCompletionsToolCall? calls = response.ToolCalls.FirstOrDefault();
    for (int i = 0; i < response.ToolCalls.Count; i++)
    {
        var call = response.ToolCalls[i];
        Console.WriteLine($"Tool call {i}: {call.Name} with arguments {call.Arguments}");
        //Tool call 0: add with arguments {"a":2,"b":4}

        var dict = JsonSerializer.Deserialize<Dictionary<string, object>>(call.Arguments);
        var result = await mcpClient.CallToolAsync(
            call.Name,
            dict!,
            cancellationToken: CancellationToken.None
        );

        Console.WriteLine(result.Content.First(c => c.Type == "text").Text);

    }
    ```

    في الكود السابق قمنا بـ:

    - التكرار عبر قائمة استدعاءات الوظائف.
    - لكل استدعاء أداة، استخراج الاسم والوسائط واستدعاء الأداة على خادم MCP باستخدام عميل MCP. وأخيرًا نطبع النتائج.

إليك الكود بالكامل:

```csharp
using Azure;
using Azure.AI.Inference;
using Azure.Identity;
using System.Text.Json;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;
using System.Text.Json;

var endpoint = "https://models.inference.ai.azure.com";
var token = Environment.GetEnvironmentVariable("GITHUB_TOKEN"); // Your GitHub Access Token
var client = new ChatCompletionsClient(new Uri(endpoint), new AzureKeyCredential(token));
var chatHistory = new List<ChatRequestMessage>
{
    new ChatRequestSystemMessage("You are a helpful assistant that knows about AI")
};

var clientTransport = new StdioClientTransport(new()
{
    Name = "Demo Server",
    Command = "/workspaces/mcp-for-beginners/03-GettingStarted/02-client/solution/server/bin/Debug/net8.0/server",
    Arguments = [],
});

Console.WriteLine("Setting up stdio transport");

await using var mcpClient = await McpClientFactory.CreateAsync(clientTransport);

ChatCompletionsToolDefinition ConvertFrom(string name, string description, JsonElement jsonElement)
{ 
    // convert the tool to a function definition
    FunctionDefinition functionDefinition = new FunctionDefinition(name)
    {
        Description = description,
        Parameters = BinaryData.FromObjectAsJson(new
        {
            Type = "object",
            Properties = jsonElement
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase })
    };

    // create a tool definition
    ChatCompletionsToolDefinition toolDefinition = new ChatCompletionsToolDefinition(functionDefinition);
    return toolDefinition;
}



async Task<List<ChatCompletionsToolDefinition>> GetMcpTools()
{
    Console.WriteLine("Listing tools");
    var tools = await mcpClient.ListToolsAsync();

    List<ChatCompletionsToolDefinition> toolDefinitions = new List<ChatCompletionsToolDefinition>();

    foreach (var tool in tools)
    {
        Console.WriteLine($"Connected to server with tools: {tool.Name}");
        Console.WriteLine($"Tool description: {tool.Description}");
        Console.WriteLine($"Tool parameters: {tool.JsonSchema}");

        JsonElement propertiesElement;
        tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

        var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
        Console.WriteLine($"Tool definition: {def}");
        toolDefinitions.Add(def);

        Console.WriteLine($"Properties: {propertiesElement}");        
    }

    return toolDefinitions;
}

// 1. List tools on mcp server

var tools = await GetMcpTools();
for (int i = 0; i < tools.Count; i++)
{
    var tool = tools[i];
    Console.WriteLine($"MCP Tools def: {i}: {tool}");
}

// 2. Define the chat history and the user message
var userMessage = "add 2 and 4";

chatHistory.Add(new ChatRequestUserMessage(userMessage));


// 3. Define options, including the tools
var options = new ChatCompletionsOptions(chatHistory)
{
    Model = "gpt-4o-mini",
    Tools = { tools[0] }
};

// 4. Call the model  

ChatCompletions? response = await client.CompleteAsync(options);
var content = response.Content;

// 5. Check if the response contains a function call
ChatCompletionsToolCall? calls = response.ToolCalls.FirstOrDefault();
for (int i = 0; i < response.ToolCalls.Count; i++)
{
    var call = response.ToolCalls[i];
    Console.WriteLine($"Tool call {i}: {call.Name} with arguments {call.Arguments}");
    //Tool call 0: add with arguments {"a":2,"b":4}

    var dict = JsonSerializer.Deserialize<Dictionary<string, object>>(call.Arguments);
    var result = await mcpClient.CallToolAsync(
        call.Name,
        dict!,
        cancellationToken: CancellationToken.None
    );

    Console.WriteLine(result.Content.First(c => c.Type == "text").Text);

}

// 5. Print the generic response
Console.WriteLine($"Assistant response: {content}");
```

#### Java

```java
try {
    // Execute natural language requests that automatically use MCP tools
    String response = bot.chat("Calculate the sum of 24.5 and 17.3 using the calculator service");
    System.out.println(response);

    response = bot.chat("What's the square root of 144?");
    System.out.println(response);

    response = bot.chat("Show me the help for the calculator service");
    System.out.println(response);
} finally {
    mcpClient.close();
}
```

في الكود السابق قمنا بـ:

- استخدام مطالبات بسيطة باللغة الطبيعية للتفاعل مع أدوات خادم MCP.
- يتولى إطار LangChain4j تلقائيًا:
  - تحويل مطالبات المستخدم إلى استدعاءات أدوات عند الحاجة.
  - استدعاء الأدوات المناسبة لـ MCP بناءً على قرار LLM.
  - إدارة تدفق المحادثة بين LLM وخادم MCP.
- طريقة `bot.chat()` تعيد استجابات باللغة الطبيعية قد تتضمن نتائج من تنفيذ أدوات MCP.
- هذا النهج يوفر تجربة مستخدم سلسة حيث لا يحتاج المستخدمون إلى معرفة التنفيذ الداخلي لـ MCP.

مثال كامل على الكود:

```java
public class LangChain4jClient {
    
    public static void main(String[] args) throws Exception {        ChatLanguageModel model = OpenAiOfficialChatModel.builder()
                .isGitHubModels(true)
                .apiKey(System.getenv("GITHUB_TOKEN"))
                .timeout(Duration.ofSeconds(60))
                .modelName("gpt-4.1-nano")
                .timeout(Duration.ofSeconds(60))
                .build();

        McpTransport transport = new HttpMcpTransport.Builder()
                .sseUrl("http://localhost:8080/sse")
                .timeout(Duration.ofSeconds(60))
                .logRequests(true)
                .logResponses(true)
                .build();

        McpClient mcpClient = new DefaultMcpClient.Builder()
                .transport(transport)
                .build();

        ToolProvider toolProvider = McpToolProvider.builder()
                .mcpClients(List.of(mcpClient))
                .build();

        Bot bot = AiServices.builder(Bot.class)
                .chatLanguageModel(model)
                .toolProvider(toolProvider)
                .build();

        try {
            String response = bot.chat("Calculate the sum of 24.5 and 17.3 using the calculator service");
            System.out.println(response);

            response = bot.chat("What's the square root of 144?");
            System.out.println(response);

            response = bot.chat("Show me the help for the calculator service");
            System.out.println(response);
        } finally {
            mcpClient.close();
        }
    }
}
```

#### Rust

هنا حيث يحدث الجزء الأكبر من العمل. سنقوم باستدعاء LLM مع مطالبة المستخدم الأولية، ثم معالجة الاستجابة لمعرفة ما إذا كانت هناك حاجة لاستدعاء أي أدوات. إذا كان الأمر كذلك، سنقوم باستدعاء تلك الأدوات ومواصلة المحادثة مع LLM حتى لا تكون هناك حاجة لمزيد من استدعاءات الأدوات ونحصل على استجابة نهائية.

سنقوم بإجراء استدعاءات متعددة لـ LLM، لذا دعونا نحدد وظيفة ستتعامل مع استدعاء LLM. أضف الوظيفة التالية إلى ملف `main.rs` الخاص بك:

```rust
async fn call_llm(
    client: &Client<OpenAIConfig>,
    messages: &[Value],
    tools: &ListToolsResult,
) -> Result<Value, Box<dyn Error>> {
    let response = client
        .completions()
        .create_byot(json!({
            "messages": messages,
            "model": "openai/gpt-4.1",
            "tools": format_tools(tools).await?,
        }))
        .await?;
    Ok(response)
}
```

تأخذ هذه الوظيفة عميل LLM، قائمة بالرسائل (بما في ذلك مطالبة المستخدم)، الأدوات من خادم MCP، وترسل طلبًا إلى LLM، وتعيد الاستجابة.
تحتوي الاستجابة من LLM على مصفوفة من `choices`. سنحتاج إلى معالجة النتيجة لمعرفة ما إذا كانت هناك أي `tool_calls` موجودة. هذا يخبرنا أن LLM يطلب استدعاء أداة معينة مع المعطيات. أضف الكود التالي إلى نهاية ملف `main.rs` لتعريف وظيفة للتعامل مع استجابة LLM:

```rust
async fn process_llm_response(
    llm_response: &Value,
    mcp_client: &RunningService<RoleClient, ()>,
    openai_client: &Client<OpenAIConfig>,
    mcp_tools: &ListToolsResult,
    messages: &mut Vec<Value>,
) -> Result<(), Box<dyn Error>> {
    let Some(message) = llm_response
        .get("choices")
        .and_then(|c| c.as_array())
        .and_then(|choices| choices.first())
        .and_then(|choice| choice.get("message"))
    else {
        return Ok(());
    };

    // Print content if available
    if let Some(content) = message.get("content").and_then(|c| c.as_str()) {
        println!("🤖 {}", content);
    }

    // Handle tool calls
    if let Some(tool_calls) = message.get("tool_calls").and_then(|tc| tc.as_array()) {
        messages.push(message.clone()); // Add assistant message

        // Execute each tool call
        for tool_call in tool_calls {
            let (tool_id, name, args) = extract_tool_call_info(tool_call)?;
            println!("⚡ Calling tool: {}", name);

            let result = mcp_client
                .call_tool(CallToolRequestParam {
                    name: name.into(),
                    arguments: serde_json::from_str::<Value>(&args)?.as_object().cloned(),
                })
                .await?;

            // Add tool result to messages
            messages.push(json!({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": serde_json::to_string_pretty(&result)?
            }));
        }

        // Continue conversation with tool results
        let response = call_llm(openai_client, messages, mcp_tools).await?;
        Box::pin(process_llm_response(
            &response,
            mcp_client,
            openai_client,
            mcp_tools,
            messages,
        ))
        .await?;
    }
    Ok(())
}
```

إذا كانت `tool_calls` موجودة، يتم استخراج معلومات الأداة، واستدعاء خادم MCP مع طلب الأداة، وإضافة النتائج إلى رسائل المحادثة. ثم تستمر المحادثة مع LLM ويتم تحديث الرسائل باستجابة المساعد ونتائج استدعاء الأداة.

لاستخراج معلومات استدعاء الأداة التي يعيدها LLM لاستدعاءات MCP، سنضيف وظيفة مساعدة أخرى لاستخراج كل ما هو مطلوب لإجراء الاستدعاء. أضف الكود التالي إلى نهاية ملف `main.rs`:

```rust
fn extract_tool_call_info(tool_call: &Value) -> Result<(String, String, String), Box<dyn Error>> {
    let tool_id = tool_call
        .get("id")
        .and_then(|id| id.as_str())
        .unwrap_or("")
        .to_string();
    let function = tool_call.get("function").ok_or("Missing function")?;
    let name = function
        .get("name")
        .and_then(|n| n.as_str())
        .unwrap_or("")
        .to_string();
    let args = function
        .get("arguments")
        .and_then(|a| a.as_str())
        .unwrap_or("{}")
        .to_string();
    Ok((tool_id, name, args))
}
```

مع وجود جميع الأجزاء في مكانها، يمكننا الآن التعامل مع الطلب الأولي للمستخدم واستدعاء LLM. قم بتحديث وظيفة `main` لتتضمن الكود التالي:

```rust
// LLM conversation with tool calls
let response = call_llm(&openai_client, &messages, &tools).await?;
process_llm_response(
    &response,
    &mcp_client,
    &openai_client,
    &tools,
    &mut messages,
)
.await?;
```

سيقوم هذا باستعلام LLM مع الطلب الأولي للمستخدم الذي يسأل عن مجموع رقمين، وسيقوم بمعالجة الاستجابة للتعامل ديناميكيًا مع استدعاءات الأدوات.

رائع، لقد أنجزت المهمة!

## المهمة

خذ الكود من التمرين وقم ببناء الخادم مع المزيد من الأدوات. ثم قم بإنشاء عميل مع LLM، كما في التمرين، واختبره باستخدام طلبات مختلفة للتأكد من أن جميع أدوات الخادم يتم استدعاؤها ديناميكيًا. هذه الطريقة في بناء العميل تعني أن المستخدم النهائي سيحظى بتجربة مستخدم رائعة حيث يمكنه استخدام الطلبات بدلاً من أوامر العميل الدقيقة، دون أن يدرك أن خادم MCP يتم استدعاؤه.

## الحل

[الحل](/03-GettingStarted/03-llm-client/solution/README.md)

## النقاط الرئيسية

- إضافة LLM إلى عميلك يوفر طريقة أفضل للمستخدمين للتفاعل مع خوادم MCP.
- تحتاج إلى تحويل استجابة خادم MCP إلى شيء يمكن لـ LLM فهمه.

## أمثلة

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## موارد إضافية

## ما التالي

- التالي: [استهلاك خادم باستخدام Visual Studio Code](../04-vscode/README.md)

---

**إخلاء المسؤولية**:  
تم ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي. للحصول على معلومات حاسمة، يُوصى بالترجمة البشرية الاحترافية. نحن غير مسؤولين عن أي سوء فهم أو تفسيرات خاطئة ناتجة عن استخدام هذه الترجمة.