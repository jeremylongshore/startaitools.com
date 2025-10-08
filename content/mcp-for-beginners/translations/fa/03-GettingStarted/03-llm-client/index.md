<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T13:28:39+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "fa"
}
-->
# ایجاد یک کلاینت با LLM

تا اینجا، شما یاد گرفتید که چگونه یک سرور و یک کلاینت ایجاد کنید. کلاینت توانسته است به طور صریح سرور را فراخوانی کند تا ابزارها، منابع و درخواست‌های آن را لیست کند. با این حال، این روش چندان عملی نیست. کاربران شما در عصر عامل‌ها زندگی می‌کنند و انتظار دارند از درخواست‌ها استفاده کنند و با یک LLM ارتباط برقرار کنند. برای کاربران شما، مهم نیست که آیا شما از MCP برای ذخیره قابلیت‌های خود استفاده می‌کنید یا نه، اما آنها انتظار دارند که از زبان طبیعی برای تعامل استفاده کنند. پس چگونه این مشکل را حل کنیم؟ راه‌حل اضافه کردن یک LLM به کلاینت است.

## نمای کلی

در این درس، ما بر اضافه کردن یک LLM به کلاینت شما تمرکز می‌کنیم و نشان می‌دهیم که چگونه این کار تجربه بهتری برای کاربران شما فراهم می‌کند.

## اهداف یادگیری

در پایان این درس، شما قادر خواهید بود:

- یک کلاینت با LLM ایجاد کنید.
- به طور یکپارچه با یک سرور MCP از طریق LLM تعامل کنید.
- تجربه کاربری بهتری در سمت کلاینت ارائه دهید.

## رویکرد

بیایید رویکردی که باید اتخاذ کنیم را درک کنیم. اضافه کردن یک LLM ساده به نظر می‌رسد، اما آیا واقعاً این کار را انجام خواهیم داد؟

در اینجا نحوه تعامل کلاینت با سرور آمده است:

1. اتصال به سرور برقرار کنید.

1. قابلیت‌ها، درخواست‌ها، منابع و ابزارها را لیست کنید و طرح آنها را ذخیره کنید.

1. یک LLM اضافه کنید و قابلیت‌های ذخیره شده و طرح آنها را در قالبی که LLM می‌فهمد، منتقل کنید.

1. یک درخواست کاربر را با انتقال آن به LLM همراه با ابزارهای لیست شده توسط کلاینت مدیریت کنید.

عالی، حالا ما در سطح بالا فهمیدیم که چگونه این کار را انجام دهیم، بیایید این را در تمرین زیر امتحان کنیم.

## تمرین: ایجاد یک کلاینت با LLM

در این تمرین، ما یاد می‌گیریم که چگونه یک LLM به کلاینت خود اضافه کنیم.

### احراز هویت با استفاده از GitHub Personal Access Token

ایجاد یک توکن GitHub فرآیندی ساده است. در اینجا نحوه انجام آن آمده است:

- به تنظیمات GitHub بروید – روی تصویر پروفایل خود در گوشه بالا سمت راست کلیک کنید و تنظیمات را انتخاب کنید.
- به تنظیمات توسعه‌دهنده بروید – پایین بروید و روی تنظیمات توسعه‌دهنده کلیک کنید.
- توکن‌های دسترسی شخصی را انتخاب کنید – روی توکن‌های دقیق کلیک کنید و سپس توکن جدید ایجاد کنید.
- توکن خود را پیکربندی کنید – یک یادداشت برای مرجع اضافه کنید، تاریخ انقضا تنظیم کنید و محدوده‌های لازم (مجوزها) را انتخاب کنید. در این مورد، مطمئن شوید که مجوز مدل‌ها را اضافه کنید.
- توکن را ایجاد و کپی کنید – روی ایجاد توکن کلیک کنید و مطمئن شوید که فوراً آن را کپی کنید، زیرا بعداً نمی‌توانید آن را ببینید.

### -1- اتصال به سرور

ابتدا کلاینت خود را ایجاد کنیم:

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

در کد بالا ما:

- کتابخانه‌های مورد نیاز را وارد کردیم.
- یک کلاس با دو عضو، `client` و `openai` ایجاد کردیم که به ما کمک می‌کند یک کلاینت مدیریت کنیم و با یک LLM تعامل کنیم.
- نمونه LLM خود را پیکربندی کردیم تا از مدل‌های GitHub استفاده کند با تنظیم `baseUrl` به API استنتاج.

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

در کد بالا ما:

- کتابخانه‌های مورد نیاز برای MCP را وارد کردیم.
- یک کلاینت ایجاد کردیم.

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

ابتدا باید وابستگی‌های LangChain4j را به فایل `pom.xml` خود اضافه کنید. این وابستگی‌ها را اضافه کنید تا MCP و مدل‌های GitHub را فعال کنید:

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

سپس کلاس کلاینت جاوا خود را ایجاد کنید:

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

در کد بالا ما:

- **وابستگی‌های LangChain4j را اضافه کردیم**: برای یکپارچه‌سازی MCP، کلاینت رسمی OpenAI و پشتیبانی از مدل‌های GitHub.
- **کتابخانه‌های LangChain4j را وارد کردیم**: برای یکپارچه‌سازی MCP و قابلیت مدل چت OpenAI.
- **یک `ChatLanguageModel` ایجاد کردیم**: که برای استفاده از مدل‌های GitHub با توکن GitHub شما پیکربندی شده است.
- **انتقال HTTP را تنظیم کردیم**: با استفاده از Server-Sent Events (SSE) برای اتصال به سرور MCP.
- **یک کلاینت MCP ایجاد کردیم**: که ارتباط با سرور را مدیریت می‌کند.
- **از پشتیبانی داخلی MCP LangChain4j استفاده کردیم**: که یکپارچه‌سازی بین LLM‌ها و سرورهای MCP را ساده می‌کند.

#### Rust

این مثال فرض می‌کند که شما یک سرور MCP مبتنی بر Rust دارید. اگر ندارید، به درس [01-first-server](../01-first-server/README.md) مراجعه کنید تا سرور را ایجاد کنید.

پس از داشتن سرور MCP Rust، یک ترمینال باز کنید و به همان دایرکتوری سرور بروید. سپس دستور زیر را اجرا کنید تا یک پروژه کلاینت LLM جدید ایجاد کنید:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

وابستگی‌های زیر را به فایل `Cargo.toml` خود اضافه کنید:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> کتابخانه رسمی Rust برای OpenAI وجود ندارد، اما crate `async-openai` یک [کتابخانه نگهداری شده توسط جامعه](https://platform.openai.com/docs/libraries/rust#rust) است که معمولاً استفاده می‌شود.

فایل `src/main.rs` را باز کنید و محتوای آن را با کد زیر جایگزین کنید:

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

این کد یک برنامه Rust پایه تنظیم می‌کند که به یک سرور MCP و مدل‌های GitHub برای تعاملات LLM متصل می‌شود.

> [!IMPORTANT]
> مطمئن شوید که متغیر محیطی `OPENAI_API_KEY` را با توکن GitHub خود تنظیم کنید قبل از اجرای برنامه.

عالی، برای مرحله بعدی، بیایید قابلیت‌های سرور را لیست کنیم.

### -2- لیست قابلیت‌های سرور

حالا ما به سرور متصل می‌شویم و از قابلیت‌های آن می‌پرسیم:

#### TypeScript

در همان کلاس، روش‌های زیر را اضافه کنید:

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

در کد بالا ما:

- کدی برای اتصال به سرور، `connectToServer` اضافه کردیم.
- یک روش `run` ایجاد کردیم که مسئول مدیریت جریان برنامه ما است. تا اینجا فقط ابزارها را لیست می‌کند اما به زودی موارد بیشتری به آن اضافه خواهیم کرد.

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

در اینجا چیزی که اضافه کردیم:

- منابع و ابزارها را لیست کردیم و آنها را چاپ کردیم. برای ابزارها همچنین `inputSchema` را لیست کردیم که بعداً از آن استفاده می‌کنیم.

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

در کد بالا ما:

- ابزارهای موجود در سرور MCP را لیست کردیم.
- برای هر ابزار، نام، توضیحات و طرح آن را لیست کردیم. مورد آخر چیزی است که به زودی برای فراخوانی ابزارها استفاده خواهیم کرد.

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

در کد بالا ما:

- یک `McpToolProvider` ایجاد کردیم که به طور خودکار همه ابزارها را از سرور MCP کشف و ثبت می‌کند.
- ارائه‌دهنده ابزار تبدیل بین طرح‌های ابزار MCP و فرمت ابزار LangChain4j را به صورت داخلی مدیریت می‌کند.
- این رویکرد فرآیند لیست کردن و تبدیل ابزارها را به صورت دستی انتزاع می‌کند.

#### Rust

دریافت ابزارها از سرور MCP با استفاده از روش `list_tools` انجام می‌شود. در تابع `main` خود، پس از تنظیم کلاینت MCP، کد زیر را اضافه کنید:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- تبدیل قابلیت‌های سرور به ابزارهای LLM

مرحله بعدی پس از لیست کردن قابلیت‌های سرور، تبدیل آنها به قالبی است که LLM می‌فهمد. پس از انجام این کار، می‌توانیم این قابلیت‌ها را به عنوان ابزار به LLM ارائه دهیم.

#### TypeScript

1. کد زیر را برای تبدیل پاسخ از سرور MCP به قالب ابزار LLM اضافه کنید:

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

    کد بالا پاسخ از سرور MCP را می‌گیرد و آن را به قالب تعریف ابزار تبدیل می‌کند که LLM می‌تواند درک کند.

1. بیایید روش `run` را به‌روزرسانی کنیم تا قابلیت‌های سرور را لیست کند:

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

    در کد بالا، روش `run` را به‌روزرسانی کردیم تا از طریق نتیجه نقشه‌برداری کند و برای هر ورودی `openAiToolAdapter` را فراخوانی کند.

#### Python

1. ابتدا، تابع تبدیل زیر را ایجاد کنیم:

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

    در تابع بالا `convert_to_llm_tools`، ما یک پاسخ ابزار MCP را می‌گیریم و آن را به قالبی تبدیل می‌کنیم که LLM می‌تواند درک کند.

1. سپس، کد کلاینت خود را به گونه‌ای به‌روزرسانی کنیم که از این تابع استفاده کند:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    در اینجا، ما یک فراخوانی به `convert_to_llm_tool` اضافه می‌کنیم تا پاسخ ابزار MCP را به چیزی تبدیل کنیم که بعداً بتوانیم به LLM تغذیه کنیم.

#### .NET

1. کدی برای تبدیل پاسخ ابزار MCP به چیزی که LLM می‌تواند درک کند اضافه کنیم:

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

در کد بالا ما:

- یک تابع `ConvertFrom` ایجاد کردیم که نام، توضیحات و طرح ورودی را می‌گیرد.
- عملکردی تعریف کردیم که یک FunctionDefinition ایجاد می‌کند که به یک ChatCompletionsDefinition منتقل می‌شود. دومی چیزی است که LLM می‌تواند درک کند.

1. بیایید ببینیم چگونه می‌توانیم کد موجود را به گونه‌ای به‌روزرسانی کنیم که از این تابع استفاده کند:

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

در کد بالا ما:

- یک رابط ساده `Bot` برای تعاملات زبان طبیعی تعریف کردیم.
- از `AiServices` LangChain4j برای اتصال خودکار LLM با ارائه‌دهنده ابزار MCP استفاده کردیم.
- چارچوب به طور خودکار تبدیل طرح ابزار و فراخوانی عملکرد را در پشت صحنه مدیریت می‌کند.
- این رویکرد پیچیدگی تبدیل ابزار MCP به قالب سازگار با LLM را حذف می‌کند - LangChain4j همه پیچیدگی‌ها را مدیریت می‌کند.

#### Rust

برای تبدیل پاسخ ابزار MCP به قالبی که LLM می‌تواند درک کند، یک تابع کمکی اضافه می‌کنیم که لیست ابزارها را قالب‌بندی می‌کند. کد زیر را به فایل `main.rs` خود در زیر تابع `main` اضافه کنید. این تابع هنگام ارسال درخواست‌ها به LLM فراخوانی خواهد شد:

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

عالی، حالا آماده مدیریت درخواست‌های کاربر هستیم، پس بیایید به این موضوع بپردازیم.

### -4- مدیریت درخواست کاربر

در این بخش از کد، ما درخواست‌های کاربر را مدیریت خواهیم کرد.

#### TypeScript

1. یک روش اضافه کنید که برای فراخوانی LLM استفاده خواهد شد:

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

    در کد بالا ما:

    - یک روش `callTools` اضافه کردیم.
    - روش بررسی می‌کند که آیا LLM ابزارهایی را فراخوانی کرده است یا خیر:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - اگر LLM نشان دهد که باید فراخوانی شود، ابزار را فراخوانی می‌کند:

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

1. روش `run` را به‌روزرسانی کنید تا شامل فراخوانی‌های LLM و فراخوانی `callTools` باشد:

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

عالی، بیایید کد کامل را لیست کنیم:

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

1. برخی از واردات مورد نیاز برای فراخوانی LLM را اضافه کنیم:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. سپس، تابعی را اضافه کنیم که LLM را فراخوانی کند:

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

    در کد بالا ما:

    - ابزارهایی که در سرور MCP پیدا کردیم و تبدیل کردیم را به LLM منتقل کردیم.
    - سپس LLM را با ابزارهای مذکور فراخوانی کردیم.
    - سپس، نتیجه را بررسی می‌کنیم تا ببینیم چه ابزارهایی باید فراخوانی شوند، اگر وجود داشته باشد.
    - در نهایت، یک آرایه از ابزارها برای فراخوانی منتقل می‌کنیم.

1. مرحله نهایی، کد اصلی خود را به‌روزرسانی کنیم:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    در کد بالا ما:

    - یک ابزار MCP را از طریق `call_tool` با استفاده از تابعی که LLM فکر می‌کند باید بر اساس درخواست ما فراخوانی شود، فراخوانی کردیم.
    - نتیجه فراخوانی ابزار به سرور MCP را چاپ کردیم.

#### .NET

1. کدی برای انجام درخواست LLM نشان دهیم:

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

    در کد بالا ما:

    - ابزارها را از سرور MCP دریافت کردیم، `var tools = await GetMcpTools()`.
    - یک درخواست کاربر `userMessage` تعریف کردیم.
    - یک شیء گزینه‌ها را مشخص کردیم که مدل و ابزارها را مشخص می‌کند.
    - یک درخواست به سمت LLM ارسال کردیم.

1. یک مرحله آخر، ببینیم آیا LLM فکر می‌کند باید یک عملکرد فراخوانی شود:

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

    در کد بالا ما:

    - از طریق لیستی از فراخوانی‌های عملکرد حلقه زدیم.
    - برای هر فراخوانی ابزار، نام و آرگومان‌ها را تجزیه کردیم و ابزار را در سرور MCP با استفاده از کلاینت MCP فراخوانی کردیم. در نهایت نتایج را چاپ کردیم.

در اینجا کد کامل آمده است:

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

در کد بالا ما:

- از درخواست‌های زبان طبیعی ساده برای تعامل با ابزارهای سرور MCP استفاده کردیم.
- چارچوب LangChain4j به طور خودکار مدیریت می‌کند:
  - تبدیل درخواست‌های کاربر به فراخوانی ابزارها در صورت نیاز.
  - فراخوانی ابزارهای مناسب MCP بر اساس تصمیم LLM.
  - مدیریت جریان مکالمه بین LLM و سرور MCP.
- روش `bot.chat()` پاسخ‌های زبان طبیعی را بازمی‌گرداند که ممکن است شامل نتایج اجرای ابزارهای MCP باشد.
- این رویکرد تجربه کاربری یکپارچه‌ای فراهم می‌کند که کاربران نیازی به دانستن پیاده‌سازی MCP زیرین ندارند.

مثال کامل کد:

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

اینجا جایی است که بیشتر کارها انجام می‌شود. ما با درخواست اولیه کاربر به LLM تماس خواهیم گرفت، سپس پاسخ را پردازش می‌کنیم تا ببینیم آیا ابزارهایی باید فراخوانی شوند یا خیر. اگر چنین باشد، آن ابزارها را فراخوانی می‌کنیم و مکالمه را با LLM ادامه می‌دهیم تا زمانی که دیگر نیازی به فراخوانی ابزارها نباشد و پاسخ نهایی داشته باشیم.

ما چندین بار به LLM تماس خواهیم گرفت، بنابراین بیایید تابعی تعریف کنیم که تماس LLM را مدیریت کند. تابع زیر را به فایل `main.rs` خود اضافه کنید:

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

این تابع کلاینت LLM، لیستی از پیام‌ها (شامل درخواست کاربر)، ابزارها از سرور MCP را می‌گیرد و یک درخواست به LLM ارسال می‌کند و پاسخ را بازمی‌گرداند.
پاسخ LLM شامل یک آرایه از `choices` خواهد بود. ما باید نتیجه را پردازش کنیم تا ببینیم آیا `tool_calls` وجود دارد یا خیر. این به ما اطلاع می‌دهد که LLM درخواست کرده است یک ابزار خاص با آرگومان‌ها فراخوانی شود. کد زیر را به انتهای فایل `main.rs` خود اضافه کنید تا یک تابع برای مدیریت پاسخ LLM تعریف کنید:

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

اگر `tool_calls` وجود داشته باشد، اطلاعات ابزار استخراج می‌شود، درخواست ابزار به سرور MCP ارسال می‌شود و نتایج به پیام‌های مکالمه اضافه می‌شود. سپس مکالمه با LLM ادامه پیدا می‌کند و پیام‌ها با پاسخ دستیار و نتایج فراخوانی ابزار به‌روزرسانی می‌شوند.

برای استخراج اطلاعات فراخوانی ابزار که LLM برای فراخوانی‌های MCP بازمی‌گرداند، یک تابع کمکی دیگر اضافه خواهیم کرد تا همه چیز مورد نیاز برای انجام فراخوانی را استخراج کند. کد زیر را به انتهای فایل `main.rs` خود اضافه کنید:

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

با داشتن همه اجزا، اکنون می‌توانیم درخواست اولیه کاربر را مدیریت کنیم و LLM را فراخوانی کنیم. تابع `main` خود را به‌روزرسانی کنید تا کد زیر را شامل شود:

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

این کد LLM را با درخواست اولیه کاربر که جمع دو عدد را می‌پرسد، فراخوانی می‌کند و پاسخ را پردازش می‌کند تا فراخوانی ابزارها را به صورت پویا مدیریت کند.

عالی، شما موفق شدید!

## تکلیف

کد تمرین را بگیرید و سرور را با ابزارهای بیشتری توسعه دهید. سپس یک کلاینت با یک LLM، مانند تمرین، ایجاد کنید و آن را با درخواست‌های مختلف آزمایش کنید تا مطمئن شوید همه ابزارهای سرور شما به صورت پویا فراخوانی می‌شوند. این روش ساخت کلاینت به این معناست که کاربر نهایی تجربه کاربری عالی خواهد داشت، زیرا می‌تواند از درخواست‌ها استفاده کند، به جای دستورات دقیق کلاینت، و از هرگونه فراخوانی سرور MCP بی‌اطلاع باشد.

## راه‌حل

[راه‌حل](/03-GettingStarted/03-llm-client/solution/README.md)

## نکات کلیدی

- افزودن یک LLM به کلاینت شما راه بهتری برای تعامل کاربران با سرورهای MCP فراهم می‌کند.
- شما باید پاسخ سرور MCP را به چیزی تبدیل کنید که LLM بتواند آن را درک کند.

## نمونه‌ها

- [ماشین حساب جاوا](../samples/java/calculator/README.md)
- [ماشین حساب .Net](../../../../03-GettingStarted/samples/csharp)
- [ماشین حساب جاوااسکریپت](../samples/javascript/README.md)
- [ماشین حساب تایپ‌اسکریپت](../samples/typescript/README.md)
- [ماشین حساب پایتون](../../../../03-GettingStarted/samples/python)
- [ماشین حساب راست](../../../../03-GettingStarted/samples/rust)

## منابع اضافی

## مرحله بعدی

- بعدی: [مصرف یک سرور با استفاده از Visual Studio Code](../04-vscode/README.md)

---

**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما تلاش می‌کنیم دقت را حفظ کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌ها باشند. سند اصلی به زبان اصلی آن باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حساس، توصیه می‌شود از ترجمه حرفه‌ای انسانی استفاده کنید. ما مسئولیتی در قبال سوء تفاهم‌ها یا تفسیرهای نادرست ناشی از استفاده از این ترجمه نداریم.