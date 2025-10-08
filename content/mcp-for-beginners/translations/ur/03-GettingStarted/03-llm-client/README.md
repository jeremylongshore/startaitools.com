<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T13:31:28+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "ur"
}
-->
# کلائنٹ کو LLM کے ساتھ بنانا

اب تک، آپ نے دیکھا کہ سرور اور کلائنٹ کیسے بنائے جاتے ہیں۔ کلائنٹ سرور کو واضح طور پر کال کر سکتا ہے تاکہ اس کے ٹولز، وسائل اور پرامپٹس کی فہرست حاصل کی جا سکے۔ تاہم، یہ طریقہ زیادہ عملی نہیں ہے۔ آپ کا صارف ایجنٹک دور میں رہتا ہے اور توقع کرتا ہے کہ وہ پرامپٹس استعمال کرے اور LLM کے ساتھ بات چیت کرے۔ آپ کے صارف کو اس بات سے فرق نہیں پڑتا کہ آپ اپنی صلاحیتوں کو ذخیرہ کرنے کے لیے MCP استعمال کرتے ہیں یا نہیں، لیکن وہ قدرتی زبان کے ذریعے بات چیت کی توقع رکھتے ہیں۔ تو ہم اس مسئلے کو کیسے حل کریں؟ حل یہ ہے کہ کلائنٹ میں LLM شامل کیا جائے۔

## جائزہ

اس سبق میں ہم کلائنٹ میں LLM شامل کرنے پر توجہ مرکوز کریں گے اور دکھائیں گے کہ یہ آپ کے صارف کے لیے کس طرح بہتر تجربہ فراہم کرتا ہے۔

## سیکھنے کے مقاصد

اس سبق کے اختتام تک، آپ یہ کرنے کے قابل ہوں گے:

- LLM کے ساتھ کلائنٹ بنانا۔
- LLM کے ذریعے MCP سرور کے ساتھ بغیر کسی رکاوٹ کے بات چیت کرنا۔
- کلائنٹ سائیڈ پر صارف کے لیے بہتر تجربہ فراہم کرنا۔

## طریقہ کار

آئیے اس طریقہ کار کو سمجھنے کی کوشش کریں جو ہمیں اپنانا ہوگا۔ LLM شامل کرنا آسان لگتا ہے، لیکن کیا ہم واقعی ایسا کریں گے؟

یہاں کلائنٹ سرور کے ساتھ کیسے بات چیت کرے گا:

1. سرور کے ساتھ کنکشن قائم کریں۔

1. صلاحیتوں، پرامپٹس، وسائل اور ٹولز کی فہرست بنائیں اور ان کی اسکیمہ محفوظ کریں۔

1. LLM شامل کریں اور محفوظ کردہ صلاحیتوں اور ان کی اسکیمہ کو ایسے فارمیٹ میں پاس کریں جو LLM سمجھ سکے۔

1. صارف کے پرامپٹ کو ہینڈل کریں اور اسے LLM کے ساتھ کلائنٹ کے درج کردہ ٹولز کے ساتھ پاس کریں۔

زبردست، اب ہم سمجھ گئے کہ ہم یہ اعلیٰ سطح پر کیسے کر سکتے ہیں، آئیے نیچے دیے گئے مشق میں اسے آزما کر دیکھتے ہیں۔

## مشق: LLM کے ساتھ کلائنٹ بنانا

اس مشق میں، ہم اپنے کلائنٹ میں LLM شامل کرنا سیکھیں گے۔

### GitHub پرسنل ایکسیس ٹوکن کے ذریعے تصدیق

GitHub ٹوکن بنانا ایک آسان عمل ہے۔ یہاں یہ کیسے کیا جا سکتا ہے:

- GitHub سیٹنگز پر جائیں – اوپر دائیں کونے میں اپنی پروفائل تصویر پر کلک کریں اور سیٹنگز منتخب کریں۔
- ڈیولپر سیٹنگز پر جائیں – نیچے سکرول کریں اور ڈیولپر سیٹنگز پر کلک کریں۔
- پرسنل ایکسیس ٹوکنز منتخب کریں – Fine-grained tokens پر کلک کریں اور پھر نیا ٹوکن بنائیں۔
- اپنے ٹوکن کو ترتیب دیں – حوالہ کے لیے ایک نوٹ شامل کریں، ایکسپائریشن ڈیٹ سیٹ کریں، اور ضروری اسکوپس (اجازتیں) منتخب کریں۔ اس صورت میں، یقینی بنائیں کہ Models کی اجازت شامل کریں۔
- ٹوکن بنائیں اور کاپی کریں – Generate token پر کلک کریں، اور اسے فوراً کاپی کرنا یقینی بنائیں، کیونکہ آپ اسے دوبارہ نہیں دیکھ سکیں گے۔

### -1- سرور سے کنکشن قائم کریں

آئیے پہلے اپنا کلائنٹ بنائیں:

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

اوپر دیے گئے کوڈ میں ہم نے:

- ضروری لائبریریاں درآمد کیں۔
- ایک کلاس بنائی جس میں دو ممبرز ہیں، `client` اور `openai`، جو ہمیں کلائنٹ کو منظم کرنے اور LLM کے ساتھ بات چیت کرنے میں مدد دیں گے۔
- اپنے LLM انسٹینس کو GitHub Models استعمال کرنے کے لیے ترتیب دیا، `baseUrl` کو انفرنس API کی طرف اشارہ کرنے کے لیے سیٹ کیا۔

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

اوپر دیے گئے کوڈ میں ہم نے:

- MCP کے لیے ضروری لائبریریاں درآمد کیں۔
- ایک کلائنٹ بنایا۔

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

سب سے پہلے، آپ کو اپنے `pom.xml` فائل میں LangChain4j ڈیپینڈنسیز شامل کرنے کی ضرورت ہوگی۔ MCP انٹیگریشن اور GitHub Models سپورٹ کو فعال کرنے کے لیے یہ ڈیپینڈنسیز شامل کریں:

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

پھر اپنی جاوا کلائنٹ کلاس بنائیں:

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

اوپر دیے گئے کوڈ میں ہم نے:

- **LangChain4j ڈیپینڈنسیز شامل کیں**: MCP انٹیگریشن، OpenAI آفیشل کلائنٹ، اور GitHub Models سپورٹ کے لیے ضروری ہیں۔
- **LangChain4j لائبریریاں درآمد کیں**: MCP انٹیگریشن اور OpenAI چیٹ ماڈل کی فعالیت کے لیے۔
- **ایک `ChatLanguageModel` بنایا**: GitHub Models کو آپ کے GitHub ٹوکن کے ساتھ استعمال کرنے کے لیے ترتیب دیا۔
- **HTTP ٹرانسپورٹ سیٹ اپ کیا**: MCP سرور سے کنیکٹ کرنے کے لیے Server-Sent Events (SSE) استعمال کیا۔
- **MCP کلائنٹ بنایا**: جو سرور کے ساتھ بات چیت کو ہینڈل کرے گا۔
- **LangChain4j کے بلٹ ان MCP سپورٹ کا استعمال کیا**: جو LLMs اور MCP سرورز کے درمیان انٹیگریشن کو آسان بناتا ہے۔

#### Rust

یہ مثال فرض کرتی ہے کہ آپ کے پاس Rust پر مبنی MCP سرور چل رہا ہے۔ اگر آپ کے پاس نہیں ہے، تو [01-first-server](../01-first-server/README.md) سبق میں واپس جائیں اور سرور بنائیں۔

جب آپ کے پاس Rust MCP سرور ہو، تو ایک ٹرمینل کھولیں اور سرور کے ساتھ اسی ڈائریکٹری میں جائیں۔ پھر ایک نیا LLM کلائنٹ پروجیکٹ بنانے کے لیے درج ذیل کمانڈ چلائیں:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

اپنے `Cargo.toml` فائل میں درج ذیل ڈیپینڈنسیز شامل کریں:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> OpenAI کے لیے کوئی آفیشل Rust لائبریری نہیں ہے، تاہم، `async-openai` کریٹ ایک [کمیونٹی کی طرف سے برقرار رکھی گئی لائبریری](https://platform.openai.com/docs/libraries/rust#rust) ہے جو عام طور پر استعمال کی جاتی ہے۔

اپنے `src/main.rs` فائل کو کھولیں اور اس کے مواد کو درج ذیل کوڈ سے تبدیل کریں:

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

یہ کوڈ ایک بنیادی Rust ایپلیکیشن سیٹ اپ کرتا ہے جو MCP سرور اور GitHub Models کے ساتھ LLM انٹریکشن کے لیے کنیکٹ کرے گا۔

> [!IMPORTANT]
> ایپلیکیشن چلانے سے پہلے `OPENAI_API_KEY` ماحول متغیر کو اپنے GitHub ٹوکن کے ساتھ سیٹ کرنا یقینی بنائیں۔

زبردست، اگلے مرحلے میں، آئیے سرور کی صلاحیتوں کی فہرست بنائیں۔

### -2- سرور کی صلاحیتوں کی فہرست بنائیں

اب ہم سرور سے کنیکٹ کریں گے اور اس کی صلاحیتوں کے بارے میں پوچھیں گے:

#### TypeScript

اسی کلاس میں درج ذیل میتھڈز شامل کریں:

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

اوپر دیے گئے کوڈ میں ہم نے:

- سرور سے کنیکٹ کرنے کے لیے کوڈ شامل کیا، `connectToServer`۔
- ایک `run` میتھڈ بنایا جو ہماری ایپ کے فلو کو ہینڈل کرنے کا ذمہ دار ہے۔ ابھی تک یہ صرف ٹولز کی فہرست بناتا ہے لیکن ہم جلد ہی اس میں مزید شامل کریں گے۔

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

یہاں ہم نے شامل کیا:

- وسائل اور ٹولز کی فہرست بنائی اور انہیں پرنٹ کیا۔ ٹولز کے لیے ہم `inputSchema` بھی فہرست میں شامل کرتے ہیں جسے ہم بعد میں استعمال کریں گے۔

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

اوپر دیے گئے کوڈ میں ہم نے:

- MCP سرور پر دستیاب ٹولز کی فہرست بنائی۔
- ہر ٹول کے لیے نام، تفصیل اور اس کی اسکیمہ کی فہرست بنائی۔ اسکیمہ وہ چیز ہے جسے ہم جلد ہی ٹولز کو کال کرنے کے لیے استعمال کریں گے۔

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

اوپر دیے گئے کوڈ میں ہم نے:

- ایک `McpToolProvider` بنایا جو MCP سرور سے تمام ٹولز کو خود بخود دریافت اور رجسٹر کرتا ہے۔
- ٹول پرووائیڈر اندرونی طور پر MCP ٹول اسکیمہ اور LangChain4j کے ٹول فارمیٹ کے درمیان کنورژن کو ہینڈل کرتا ہے۔
- یہ طریقہ کار دستی ٹول لسٹنگ اور کنورژن کے عمل کو ختم کرتا ہے۔

#### Rust

MCP سرور سے ٹولز حاصل کرنا `list_tools` میتھڈ کے ذریعے کیا جاتا ہے۔ اپنے `main` فنکشن میں، MCP کلائنٹ سیٹ اپ کرنے کے بعد درج ذیل کوڈ شامل کریں:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- سرور کی صلاحیتوں کو LLM ٹولز میں تبدیل کریں

سرور کی صلاحیتوں کی فہرست بنانے کے بعد اگلا مرحلہ انہیں ایسے فارمیٹ میں تبدیل کرنا ہے جو LLM سمجھ سکے۔ ایک بار جب ہم یہ کر لیں، تو ہم ان صلاحیتوں کو LLM کو ٹولز کے طور پر فراہم کر سکتے ہیں۔

#### TypeScript

1. درج ذیل کوڈ شامل کریں تاکہ MCP سرور کے جواب کو ایسے ٹول فارمیٹ میں تبدیل کیا جا سکے جو LLM استعمال کر سکے:

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

    اوپر دیا گیا کوڈ MCP سرور کے جواب کو لیتا ہے اور اسے ایسے ٹول ڈیفینیشن فارمیٹ میں تبدیل کرتا ہے جو LLM سمجھ سکے۔

1. اگلا، `run` میتھڈ کو اپ ڈیٹ کریں تاکہ سرور کی صلاحیتوں کی فہرست بنائی جا سکے:

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

    اوپر دیے گئے کوڈ میں، ہم نے `run` میتھڈ کو اپ ڈیٹ کیا تاکہ نتیجہ کے ذریعے میپ کیا جا سکے اور ہر انٹری کے لیے `openAiToolAdapter` کو کال کیا جا سکے۔

#### Python

1. پہلے، درج ذیل کنورٹر فنکشن بنائیں:

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

    اوپر دیے گئے فنکشن `convert_to_llm_tools` میں ہم MCP ٹول کے جواب کو لیتے ہیں اور اسے ایسے فارمیٹ میں تبدیل کرتے ہیں جو LLM سمجھ سکے۔

1. اگلا، اپنے کلائنٹ کوڈ کو اس فنکشن کا فائدہ اٹھانے کے لیے اپ ڈیٹ کریں:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    یہاں، ہم MCP ٹول کے جواب کو ایسے فارمیٹ میں تبدیل کرنے کے لیے `convert_to_llm_tool` کو کال کر رہے ہیں جو ہم بعد میں LLM کو فیڈ کر سکیں۔

#### .NET

1. MCP ٹول کے جواب کو ایسے فارمیٹ میں تبدیل کرنے کے لیے کوڈ شامل کریں جو LLM سمجھ سکے:

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

اوپر دیے گئے کوڈ میں ہم نے:

- ایک فنکشن `ConvertFrom` بنایا جو نام، تفصیل اور انپٹ اسکیمہ لیتا ہے۔
- ایک فنکشن ڈیفینیشن بنانے کی فعالیت کو ڈیفائن کیا جو ChatCompletionsDefinition کو پاس کیا جاتا ہے۔ یہ وہ چیز ہے جو LLM سمجھ سکتا ہے۔

1. آئیے دیکھتے ہیں کہ ہم موجودہ کوڈ کو اوپر دیے گئے فنکشن کا فائدہ اٹھانے کے لیے کیسے اپ ڈیٹ کر سکتے ہیں:

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

اوپر دیے گئے کوڈ میں ہم نے:

- قدرتی زبان کے انٹریکشن کے لیے ایک سادہ `Bot` انٹرفیس ڈیفائن کیا۔
- LangChain4j کے `AiServices` کا استعمال کیا تاکہ LLM کو MCP ٹول پرووائیڈر کے ساتھ خود بخود بائنڈ کیا جا سکے۔
- فریم ورک خود بخود ٹول اسکیمہ کنورژن اور فنکشن کالنگ کو ہینڈل کرتا ہے۔
- یہ طریقہ کار MCP ٹولز کو LLM-کمپیٹیبل فارمیٹ میں تبدیل کرنے کی دستی کوشش کو ختم کرتا ہے۔

#### Rust

MCP ٹول کے جواب کو ایسے فارمیٹ میں تبدیل کرنے کے لیے جو LLM سمجھ سکے، ہم ایک ہیلپر فنکشن شامل کریں گے جو ٹولز لسٹنگ کو فارمیٹ کرے گا۔ اپنے `main.rs` فائل میں `main` فنکشن کے نیچے درج ذیل کوڈ شامل کریں۔ یہ LLM کو درخواست کرتے وقت کال کیا جائے گا:

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

زبردست، اب ہم کسی بھی صارف کی درخواست کو ہینڈل کرنے کے لیے تیار ہیں، تو آئیے اگلے مرحلے میں اس پر کام کریں۔

### -4- صارف کی پرامپٹ درخواست کو ہینڈل کریں

اس کوڈ کے اس حصے میں، ہم صارف کی درخواستوں کو ہینڈل کریں گے۔

#### TypeScript

1. ایک میتھڈ شامل کریں جو ہمارے LLM کو کال کرنے کے لیے استعمال ہوگا:

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

    اوپر دیے گئے کوڈ میں ہم نے:

    - ایک میتھڈ `callTools` شامل کیا۔
    - میتھڈ LLM کے جواب کو لیتا ہے اور چیک کرتا ہے کہ آیا کوئی ٹولز کال کیے گئے ہیں یا نہیں:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - اگر LLM اشارہ کرے تو ٹول کو کال کرتا ہے:

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

1. `run` میتھڈ کو اپ ڈیٹ کریں تاکہ LLM کو کالز اور `callTools` کو شامل کیا جا سکے:

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

زبردست، آئیے مکمل کوڈ کی فہرست بنائیں:

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

1. LLM کو کال کرنے کے لیے ضروری امپورٹس شامل کریں:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. اگلا، وہ فنکشن شامل کریں جو LLM کو کال کرے گا:

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

    اوپر دیے گئے کوڈ میں ہم نے:

    - اپنے فنکشنز، جو ہم نے MCP سرور پر پائے اور تبدیل کیے، LLM کو پاس کیے۔
    - پھر ہم نے ان فنکشنز کے ساتھ LLM کو کال کیا۔
    - پھر، ہم نتیجہ کا معائنہ کر رہے ہیں تاکہ دیکھ سکیں کہ کون سے فنکشنز کو کال کرنا چاہیے، اگر کوئی ہو۔
    - آخر میں، ہم فنکشنز کی ایک ارے کو کال کرنے کے لیے پاس کر رہے ہیں۔

1. آخری مرحلہ، اپنے مین کوڈ کو اپ ڈیٹ کریں:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    وہاں، یہ آخری مرحلہ تھا، اوپر دیے گئے کوڈ میں ہم:

    - ایک MCP ٹول کو `call_tool` کے ذریعے کال کر رہے ہیں، ایک فنکشن کا استعمال کرتے ہوئے جو LLM نے ہمارے پرامپٹ کی بنیاد پر کال کرنے کا سوچا۔
    - MCP سرور پر ٹول کال کے نتیجہ کو پرنٹ کر رہے ہیں۔

#### .NET

1. LLM پرامپٹ درخواست کے لیے کچھ کوڈ دکھائیں:

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

    اوپر دیے گئے کوڈ میں ہم نے:

    - MCP سرور سے ٹولز حاصل کیے، `var tools = await GetMcpTools()`۔
    - ایک صارف پرامپٹ `userMessage` ڈیفائن کیا۔
    - ایک آپشنز آبجیکٹ بنایا جس میں ماڈل اور ٹولز کی وضاحت کی گئی۔
    - LLM کی طرف ایک درخواست کی۔

1. ایک آخری مرحلہ، دیکھتے ہیں کہ آیا LLM سوچتا ہے کہ ہمیں کوئی فنکشن کال کرنا چاہیے:

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

    اوپر دیے گئے کوڈ میں ہم نے:

    - فنکشن کالز کی ایک فہرست کے ذریعے لوپ کیا۔
    - ہر ٹول کال کے لیے، نام اور آرگومنٹس کو پارس کیا اور MCP کلائنٹ کا استعمال کرتے ہوئے MCP سرور پر ٹول کو کال کیا۔ آخر میں ہم نتائج کو پرنٹ کرتے ہیں۔

یہ مکمل کوڈ ہے:

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

اوپر دیے گئے کوڈ میں ہم نے:

- سادہ قدرتی زبان کے پرامپٹس کا استعمال کرتے ہوئے MCP سرور ٹولز کے ساتھ بات چیت کی۔
- LangChain4j فریم ورک خود بخود ہینڈل کرتا ہے:
  - صارف پرامپٹس کو ٹول کالز میں تبدیل کرنا جب ضرورت ہو۔
  - LLM کے فیصلے کی بنیاد پر مناسب MCP ٹولز کو کال کرنا۔
  - LLM اور MCP سرور کے درمیان بات چیت کے فلو کو منظم کرنا۔
- `bot.chat()` میتھڈ قدرتی زبان کے جوابات واپس کرتا ہے جن میں MCP ٹول ایگزیکیوشنز کے نتائج شامل ہو سکتے ہیں۔
- یہ طریقہ کار ایک ہموار صارف تجربہ فراہم کرتا ہے جہاں صارفین کو بنیادی MCP عمل درآمد کے بارے میں جاننے کی ضرورت نہیں ہوتی۔

مکمل کوڈ کی مثال:

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

یہاں زیادہ تر کام ہوتا ہے۔ ہم ابتدائی صارف پرامپٹ کے ساتھ LLM کو کال کریں گے، پھر جواب کو پروسیس کریں گے تاکہ دیکھ سکیں کہ آیا کوئی ٹولز کال کرنے کی ضرورت ہے۔ اگر ایسا ہے، تو ہم ان ٹولز کو کال کریں گے اور LLM کے ساتھ بات چیت جاری رکھیں گے جب تک کہ مزید ٹول کالز کی ضرورت نہ ہو اور ہمارے پاس حتمی جواب نہ ہو۔

ہم LLM کو متعدد بار کال کریں گے، لہذا آئیے ایک فنکشن ڈیفائن کریں جو LLM کال کو ہینڈل کرے گا۔ اپنے `main.rs` فائل میں درج ذیل فنکشن شامل کریں:

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

یہ فنکشن LLM کلائنٹ، میسجز کی ایک فہرست (جس میں صارف پرامپٹ شامل ہے)، MCP سرور سے ٹولز لیتا ہے، اور LLM کو درخواست بھیجتا ہے، جواب واپس کرتا ہے۔
جواب میں `choices` کی ایک array شامل ہوگی۔ ہمیں نتیجہ کو پراسیس کرنا ہوگا تاکہ یہ معلوم ہو سکے کہ آیا کوئی `tool_calls` موجود ہیں۔ یہ ہمیں بتاتا ہے کہ LLM کسی مخصوص ٹول کو دلائل کے ساتھ کال کرنے کی درخواست کر رہا ہے۔ اپنے `main.rs` فائل کے آخر میں درج ذیل کوڈ شامل کریں تاکہ LLM کے جواب کو ہینڈل کرنے کے لیے ایک فنکشن کو ڈیفائن کیا جا سکے:

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

اگر `tool_calls` موجود ہوں، تو یہ ٹول کی معلومات نکالتا ہے، MCP سرور کو ٹول کی درخواست کے ساتھ کال کرتا ہے، اور نتائج کو گفتگو کے پیغامات میں شامل کرتا ہے۔ پھر یہ LLM کے ساتھ گفتگو جاری رکھتا ہے اور پیغامات کو اسسٹنٹ کے جواب اور ٹول کال کے نتائج کے ساتھ اپ ڈیٹ کرتا ہے۔

MCP کالز کے لیے LLM کی طرف سے واپس کیے گئے ٹول کال کی معلومات نکالنے کے لیے، ہم ایک اور ہیلپر فنکشن شامل کریں گے تاکہ کال کرنے کے لیے درکار تمام چیزیں نکالی جا سکیں۔ اپنے `main.rs` فائل کے آخر میں درج ذیل کوڈ شامل کریں:

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

تمام حصے مکمل ہونے کے بعد، ہم ابتدائی یوزر پرامپٹ کو ہینڈل کر سکتے ہیں اور LLM کو کال کر سکتے ہیں۔ اپنے `main` فنکشن کو درج ذیل کوڈ شامل کرنے کے لیے اپ ڈیٹ کریں:

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

یہ ابتدائی یوزر پرامپٹ کے ساتھ LLM کو کوئری کرے گا، دو نمبروں کے مجموعے کے بارے میں پوچھے گا، اور جواب کو پراسیس کرے گا تاکہ ٹول کالز کو ڈائنامک طریقے سے ہینڈل کیا جا سکے۔

زبردست، آپ نے یہ کر لیا!

## اسائنمنٹ

ایکسسرسائز سے کوڈ لیں اور سرور کو مزید ٹولز کے ساتھ تیار کریں۔ پھر ایک کلائنٹ بنائیں جس میں LLM ہو، جیسے کہ ایکسرسائز میں، اور مختلف پرامپٹس کے ساتھ اس کا ٹیسٹ کریں تاکہ یہ یقینی بنایا جا سکے کہ آپ کے سرور کے تمام ٹولز ڈائنامک طریقے سے کال ہو رہے ہیں۔ اس طرح کلائنٹ بنانے کا مطلب ہے کہ اینڈ یوزر کو ایک بہترین یوزر ایکسپیرینس ملے گا کیونکہ وہ پرامپٹس استعمال کر سکیں گے، بجائے اس کے کہ وہ کلائنٹ کے عین کمانڈز استعمال کریں، اور MCP سرور کے کال ہونے سے بے خبر رہیں گے۔

## حل

[حل](/03-GettingStarted/03-llm-client/solution/README.md)

## اہم نکات

- اپنے کلائنٹ میں LLM شامل کرنا یوزرز کو MCP سرورز کے ساتھ انٹریکٹ کرنے کا بہتر طریقہ فراہم کرتا ہے۔
- آپ کو MCP سرور کے جواب کو ایسی شکل میں تبدیل کرنا ہوگا جو LLM سمجھ سکے۔

## نمونے

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## اضافی وسائل

## آگے کیا ہے

- اگلا: [Visual Studio Code کا استعمال کرتے ہوئے سرور کو کنزیوم کرنا](../04-vscode/README.md)

---

**ڈسکلیمر**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کا استعمال کرتے ہوئے ترجمہ کی گئی ہے۔ ہم درستگی کے لیے کوشش کرتے ہیں، لیکن براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا غیر درستیاں ہو سکتی ہیں۔ اصل دستاویز کو اس کی اصل زبان میں مستند ذریعہ سمجھا جانا چاہیے۔ اہم معلومات کے لیے، پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کے لیے ہم ذمہ دار نہیں ہیں۔