<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T15:29:34+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "my"
}
-->
# LLM ဖြင့် Client တစ်ခု ဖန်တီးခြင်း

ယခုအချိန်ထိ သင်သည် Server နှင့် Client တို့ကို ဖန်တီးပုံကို ကြည့်ရှုပြီးဖြစ်ပါပြီ။ Client သည် Server ကို Tools, Resources နှင့် Prompts များကို ဖော်ပြရန် တိုက်ရိုက်ခေါ်ဆိုနိုင်ခဲ့သည်။ သို့သော်၊ ယင်းနည်းလမ်းသည် အလွန်လက်တွေ့ကျသော နည်းလမ်းမဟုတ်ပါ။ သင့်အသုံးပြုသူသည် Agentic Era တွင် နေထိုင်ပြီး Prompts များကို အသုံးပြုရန်နှင့် LLM နှင့် ဆက်သွယ်ရန် မျှော်လင့်နေသည်။ သင့်အသုံးပြုသူအတွက် MCP ကို သင့်စွမ်းရည်များကို သိမ်းဆည်းရန် အသုံးပြုမည်မဟုတ်သော်လည်း သဘာဝဘာသာစကားကို အသုံးပြု၍ ဆက်သွယ်နိုင်ရန် မျှော်လင့်နေသည်။ ဒါကြောင့် ကျွန်ုပ်တို့သည် ဤပြဿနာကို မည်သို့ ဖြေရှင်းမည်နည်း။ ဖြေရှင်းချက်မှာ Client တွင် LLM တစ်ခု ထည့်သွင်းခြင်းဖြင့် ဖြစ်သည်။

## အကျဉ်းချုပ်

ဤသင်ခန်းစာတွင် သင့် Client တွင် LLM တစ်ခု ထည့်သွင်းခြင်းနှင့် သင့်အသုံးပြုသူအတွက် ပိုမိုကောင်းမွန်သော အတွေ့အကြုံကို မည်သို့ပေးနိုင်သည်ကို အဓိကထားဆွေးနွေးပါမည်။

## သင်ယူရမည့် ရည်မှန်းချက်များ

ဤသင်ခန်းစာအဆုံးတွင် သင်သည် အောက်ပါအတိုင်း ပြုလုပ်နိုင်မည်ဖြစ်သည်-

- LLM ဖြင့် Client တစ်ခု ဖန်တီးခြင်း။
- LLM ကို အသုံးပြု၍ MCP Server နှင့် ချောမွေ့စွာ ဆက်သွယ်ခြင်း။
- Client ဘက်တွင် အသုံးပြုသူအတွက် ပိုမိုကောင်းမွန်သော အတွေ့အကြုံ ပေးခြင်း။

## နည်းလမ်း

ကျွန်ုပ်တို့ လိုက်နာရမည့် နည်းလမ်းကို နားလည်ကြည့်ရှုကြပါစို့။ LLM တစ်ခု ထည့်သွင်းခြင်းသည် ရိုးရှင်းသလို ထင်ရပေမယ့် ကျွန်ုပ်တို့ အမှန်တကယ် မည်သို့ ပြုလုပ်မည်နည်း။

Client သည် Server နှင့် မည်သို့ ဆက်သွယ်မည်နည်းဆိုသည်မှာ-

1. Server နှင့် ချိတ်ဆက်မှု တည်ဆောက်ပါ။

1. စွမ်းရည်များ၊ Prompts, Resources နှင့် Tools များကို ဖော်ပြပြီး ၎င်းတို့၏ Schema ကို သိမ်းဆည်းပါ။

1. LLM တစ်ခု ထည့်သွင်းပြီး သိမ်းဆည်းထားသော စွမ်းရည်များနှင့် ၎င်းတို့၏ Schema ကို LLM နားလည်နိုင်သော Format ဖြင့် ပေးပို့ပါ။

1. အသုံးပြုသူ၏ Prompt ကို LLM သို့ Client မှ ဖော်ပြထားသော Tools များနှင့်အတူ ပေးပို့ပါ။

ကောင်းပါပြီ၊ ကျွန်ုပ်တို့သည် ဤအဆင့်ဆင့်ကို နားလည်ပြီးဖြစ်သောကြောင့် အောက်ပါ လေ့ကျင့်ခန်းတွင် စမ်းသပ်ကြည့်ရအောင်။

## လေ့ကျင့်ခန်း- LLM ဖြင့် Client တစ်ခု ဖန်တီးခြင်း

ဤလေ့ကျင့်ခန်းတွင် ကျွန်ုပ်တို့ Client တွင် LLM တစ်ခု ထည့်သွင်းပုံကို သင်ယူပါမည်။

### GitHub Personal Access Token ဖြင့် Authentication ပြုလုပ်ခြင်း

GitHub Token တစ်ခု ဖန်တီးခြင်းသည် ရိုးရှင်းသော လုပ်ငန်းစဉ်တစ်ခုဖြစ်သည်။ အောက်ပါအတိုင်း ပြုလုပ်နိုင်ပါသည်-

- GitHub Settings သို့ သွားပါ – အပေါ်ယံညာဘက်ထောင့်ရှိ သင့် Profile ပုံကို နှိပ်ပြီး Settings ကို ရွေးပါ။
- Developer Settings သို့ သွားပါ – Developer Settings ကို နှိပ်ပါ။
- Personal Access Tokens ကို ရွေးပါ – Fine-grained tokens ကို နှိပ်ပြီး Generate new token ကို ရွေးပါ။
- သင့် Token ကို Configure လုပ်ပါ – မှတ်သားရန် Note တစ်ခု ထည့်ပါ၊ သက်တမ်းကုန်ဆုံးရက်ကို သတ်မှတ်ပါ၊ လိုအပ်သော Scopes (ခွင့်ပြုချက်များ) ကို ရွေးပါ။ ဤအခါတွင် Models ခွင့်ပြုချက်ကို ထည့်သွင်းရန် သေချာပါစေ။
- Token ကို Generate နှင့် Copy လုပ်ပါ – Generate token ကို နှိပ်ပြီး၊ ၎င်းကို ချက်ချင်း Copy လုပ်ပါ၊ ပြန်လည်ကြည့်ရှုနိုင်မည်မဟုတ်ပါ။

### -1- Server နှင့် ချိတ်ဆက်ခြင်း

ပထမဦးဆုံး Client ကို ဖန်တီးကြပါစို့-

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

အထက်ပါ Code တွင်-

- လိုအပ်သော Libraries များကို Import ပြုလုပ်ထားသည်။
- `client` နှင့် `openai` ဟူသော Member နှစ်ခုပါရှိသော Class တစ်ခု ဖန်တီးထားသည်။ ၎င်းတို့သည် Client ကို စီမံရန်နှင့် LLM နှင့် ဆက်သွယ်ရန် ကူညီမည်။
- GitHub Models ကို အသုံးပြုရန် LLM Instance ကို Configure ပြုလုပ်ထားပြီး၊ `baseUrl` ကို Inference API သို့ ညွှန်းထားသည်။

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

အထက်ပါ Code တွင်-

- MCP အတွက် လိုအပ်သော Libraries များကို Import ပြုလုပ်ထားသည်။
- Client တစ်ခု ဖန်တီးထားသည်။

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

ပထမဦးဆုံး LangChain4j Dependencies များကို `pom.xml` ဖိုင်တွင် ထည့်သွင်းရန် လိုအပ်ပါမည်။ MCP Integration နှင့် GitHub Models ကို ပံ့ပိုးရန် Dependencies များကို ထည့်သွင်းပါ-

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

ထို့နောက် Java Client Class ကို ဖန်တီးပါ-

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

အထက်ပါ Code တွင်-

- **LangChain4j Dependencies များ ထည့်သွင်းထားသည်**: MCP Integration, OpenAI Official Client နှင့် GitHub Models ကို ပံ့ပိုးရန် လိုအပ်သည်။
- **LangChain4j Libraries များ Import ပြုလုပ်ထားသည်**: MCP Integration နှင့် OpenAI Chat Model Functionality အတွက်။
- **`ChatLanguageModel` တစ်ခု ဖန်တီးထားသည်**: GitHub Models ကို သင့် GitHub Token ဖြင့် Configure ပြုလုပ်ထားသည်။
- **HTTP Transport ကို Set Up ပြုလုပ်ထားသည်**: Server-Sent Events (SSE) ကို အသုံးပြု၍ MCP Server နှင့် ချိတ်ဆက်ရန်။
- **MCP Client တစ်ခု ဖန်တီးထားသည်**: Server နှင့် ဆက်သွယ်မှုကို စီမံရန်။
- **LangChain4j ၏ Built-in MCP Support ကို အသုံးပြုထားသည်**: LLM များနှင့် MCP Servers အကြား Integration ကို လွယ်ကူစေသည်။

#### Rust

ဤဥပမာသည် Rust အခြေခံ MCP Server တစ်ခု လည်ပတ်နေသည်ဟု သတ်မှတ်ထားသည်။ MCP Server မရှိပါက [01-first-server](../01-first-server/README.md) သင်ခန်းစာကို ပြန်လည်ကြည့်ရှု၍ Server တစ်ခု ဖန်တီးပါ။

Rust MCP Server ရှိပြီးပါက Terminal ကို ဖွင့်ပြီး Server ရှိ Directory သို့ သွားပါ။ ထို့နောက် LLM Client Project အသစ်တစ်ခု ဖန်တီးရန် အောက်ပါ Command ကို Run ပြုလုပ်ပါ-

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

`Cargo.toml` ဖိုင်တွင် အောက်ပါ Dependencies များ ထည့်သွင်းပါ-

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> OpenAI အတွက် တရားဝင် Rust Library မရှိသေးပါ၊ သို့သော် `async-openai` crate သည် [Community Maintained Library](https://platform.openai.com/docs/libraries/rust#rust) တစ်ခုဖြစ်ပြီး အများအားဖြင့် အသုံးပြုလေ့ရှိသည်။

`src/main.rs` ဖိုင်ကို ဖွင့်ပြီး အောက်ပါ Code ဖြင့် အကြောင်းအရာကို အစားထိုးပါ-

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

ဤ Code သည် MCP Server နှင့် GitHub Models တို့ကို LLM Interaction အတွက် ချိတ်ဆက်မည့် Rust Application အခြေခံကို Set Up ပြုလုပ်သည်။

> [!IMPORTANT]
> Application ကို Run မပြုလုပ်မီ `OPENAI_API_KEY` Environment Variable ကို သင့် GitHub Token ဖြင့် သတ်မှတ်ထားရန် သေချာပါစေ။

ကောင်းပါပြီ၊ နောက်တစ်ဆင့်တွင် Server ၏ စွမ်းရည်များကို ဖော်ပြကြပါမည်။

### -2- Server ၏ စွမ်းရည်များကို ဖော်ပြခြင်း

ယခုအခါ Server နှင့် ချိတ်ဆက်ပြီး ၎င်း၏ စွမ်းရည်များကို မေးမြန်းကြည့်ပါမည်-

#### TypeScript

အတူတူသော Class တွင် အောက်ပါ Methods များ ထည့်ပါ-

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

အထက်ပါ Code တွင်-

- Server နှင့် ချိတ်ဆက်ရန် `connectToServer` ကို ထည့်သွင်းထားသည်။
- Tools များကို ဖော်ပြရန် တာဝန်ရှိသော `run` Method တစ်ခု ဖန်တီးထားသည်။ ၎င်းတွင် နောက်ပိုင်းတွင် အခြား Functionality များ ထည့်သွင်းမည်။

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

ထို့နောက်-

- Resources နှင့် Tools များကို ဖော်ပြပြီး Print ပြထားသည်။ Tools များအတွက် `inputSchema` ကိုလည်း ဖော်ပြထားသည်။ ၎င်းကို နောက်ပိုင်းတွင် အသုံးပြုမည်။

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

အထက်ပါ Code တွင်-

- MCP Server တွင် ရရှိနိုင်သော Tools များကို ဖော်ပြထားသည်။
- Tools တစ်ခုစီအတွက် Name, Description နှင့် Schema ကို ဖော်ပြထားသည်။ ၎င်း Schema ကို Tools များကို ခေါ်ဆိုရန် အသုံးပြုမည်။

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

အထက်ပါ Code တွင်-

- `McpToolProvider` တစ်ခု ဖန်တီးထားသည်။ ၎င်းသည် MCP Server မှ Tools များကို အလိုအလျောက် ရှာဖွေပြီး Register ပြုလုပ်သည်။
- Tool Provider သည် MCP Tool Schemas နှင့် LangChain4j Tool Format အကြား Conversion ကို အတွင်းပိုင်းတွင် စီမံဆောင်ရွက်သည်။
- ဤနည်းလမ်းသည် Tool Listing နှင့် Conversion လုပ်ငန်းစဉ်ကို လက်စွဲမလိုအောင် လွယ်ကူစေသည်။

#### Rust

MCP Server မှ Tools များကို Retrieving ပြုလုပ်ရန် `list_tools` Method ကို အသုံးပြုသည်။ `main` Function တွင် MCP Client ကို Set Up ပြုလုပ်ပြီးနောက် အောက်ပါ Code ကို ထည့်ပါ-

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Server ၏ စွမ်းရည်များကို LLM Tools သို့ ပြောင်းခြင်း

Server ၏ စွမ်းရည်များကို LLM နားလည်နိုင်သော Format သို့ ပြောင်းလဲခြင်းသည် နောက်ထပ်အဆင့်ဖြစ်သည်။ ၎င်းကို ပြုလုပ်ပြီးပါက Tools များအဖြစ် LLM သို့ ပေးပို့နိုင်မည်။

#### TypeScript

1. MCP Server မှ Response ကို LLM နားလည်နိုင်သော Tool Format သို့ ပြောင်းလဲရန် အောက်ပါ Code ကို ထည့်ပါ-

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

    အထက်ပါ Code သည် MCP Server မှ Response ကို LLM နားလည်နိုင်သော Tool Definition Format သို့ ပြောင်းလဲသည်။

1. `run` Method ကို Update ပြုလုပ်ပါ-

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

    အထက်ပါ Code တွင် `run` Method ကို Update ပြုလုပ်ပြီး Result တစ်ခုစီအတွက် `openAiToolAdapter` ကို ခေါ်ဆိုထားသည်။

#### Python

1. Converter Function တစ်ခု ဖန်တီးပါ-

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

    အထက်ပါ Function တွင် `convert_to_llm_tools` သည် MCP Tool Response ကို LLM နားလည်နိုင်သော Format သို့ ပြောင်းလဲသည်။

1. Client Code ကို Update ပြုလုပ်ပါ-

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    ဤနေရာတွင် MCP Tool Response ကို LLM သို့ ပေးပို့နိုင်ရန် ပြောင်းလဲထားသည်။

#### .NET

1. MCP Tool Response ကို LLM နားလည်နိုင်သော Format သို့ ပြောင်းလဲရန် Code ထည့်ပါ-

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

အထက်ပါ Code တွင်-

- `ConvertFrom` Function တစ်ခု ဖန်တီးထားသည်။
- FunctionDefinition တစ်ခု ဖန်တီးပြီး ChatCompletionsDefinition သို့ ပေးပို့သည်။

1. ရှိပြီးသား Code ကို Update ပြုလုပ်ပါ-

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

အထက်ပါ Code တွင်-

- Natural Language Interaction များအတွက် `Bot` Interface တစ်ခု သတ်မှတ်ထားသည်။
- LangChain4j ၏ `AiServices` ကို အသုံးပြု၍ LLM နှင့် MCP Tool Provider ကို Bind ပြုလုပ်ထားသည်။
- Framework သည် MCP Tool Schemas နှင့် LLM-Compatible Format အကြား Conversion ကို အလိုအလျောက် စီမံဆောင်ရွက်သည်။

#### Rust

MCP Tool Response ကို LLM နားလည်နိုင်သော Format သို့ ပြောင်းလဲရန် Helper Function တစ်ခု ထည့်ပါ-

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

ကောင်းပါပြီ၊ ယခုအခါ အသုံးပြုသူ၏ Request များကို Handle ပြုလုပ်ရန် ဆက်လက်လုပ်ဆောင်ပါမည်။

### -4- အသုံးပြုသူ၏ Prompt Request ကို Handle ပြုလုပ်ခြင်း

ဤ Code အပိုင်းတွင် အသုံးပြုသူ၏ Request များကို Handle ပြုလုပ်ပါမည်။

#### TypeScript

1. LLM ကို ခေါ်ဆိုရန် Method တစ်ခု ထည့်ပါ-

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

    အထက်ပါ Code တွင်-

    - `callTools` Method ကို ထည့်သွင်းထားသည်။
    - LLM Response ကို ယူပြီး Tools များကို ခေါ်ဆိုရန် လိုအပ်ချက်ရှိမရှိ စစ်ဆေးထားသည်။

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - LLM မှ Tools များကို ခေါ်ဆိုရန် လိုအပ်သည်ဟု ပြောပါက Tools ကို ခေါ်ဆိုထားသည်။

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

1. `run` Method ကို Update ပြုလုပ်ပါ-

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

Code အပြည့်အစုံကို ကြည့်ပါ-

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

1. LLM ကို ခေါ်ဆိုရန် လိုအပ်သော Imports များ ထည့်ပါ-

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. LLM ကို ခေါ်ဆိုမည့် Function ကို ထည့်ပါ-

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

    အထက်ပါ Code တွင်-

    - MCP Server မှ ရရှိသော Functions များကို LLM သို့ ပေးပို့ထားသည်။
    - LLM ကို Functions များဖြင့် ခေါ်ဆိုထားသည်။
    - Result ကို စစ်ဆေးပြီး Functions များကို ခေါ်ဆိုရန် လိုအပ်ချက်ရှိမရှိ စစ်ဆေးထားသည်။

1. Main Code ကို Update ပြုလုပ်ပါ-

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    အထက်ပါ Code တွင်-

    - MCP Server သို့ `call_tool` ဖြင့် MCP Tool ကို LLM မှ Prompt အရ ခေါ်ဆိုထားသည်။
    - MCP Server မှ Tool Call ၏ Result ကို Print ပြုလုပ်ထားသည်။

#### .NET

1. LLM Prompt Request ပြုလုပ်ရန် Code ကို ပြပါ-

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

    အထက်ပါ Code တွင်-

    - MCP Server မှ Tools များကို ရယူထားသည်။
    - User Prompt ကို သတ်မှတ်ထားသည်။
    - Model နှင့် Tools များကို Options Object တစ်ခုဖြင့် သတ်မှတ်ထားသည်။
    - LLM သို့ Request ပြုလုပ်ထားသည်။

1. LLM မှ Function ကို ခေါ်ဆိုရန် Update ပြုလုပ်ပါ-

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

    အထက်ပါ Code တွင်-

    - Function Calls များကို Loop ဖြင့် စစ်ဆေးထားသည်။
    - Tool Call တစ်ခုစီအတွက် Name နှင့် Arguments ကို Parse ပြုလုပ်ပြီး MCP Server တွင် MCP Client ကို အသုံးပြု၍ Tool ကို ခေါ်ဆိုထားသည်။

Code အပြည့်အစုံ-

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

အထက်ပါ Code တွင်-

- Natural Language Prompts များကို အသုံးပြု၍ MCP Server Tools များနှင့် ဆက်သွယ်ထားသည်။
- LangChain4j Framework သည် အလိုအလျောက် စီမံဆောင်ရွက်သည်-
  - User Prompts များကို Tool Calls သို့ ပြောင်းလဲခြင်း။
  - LLM ၏ ဆုံးဖြတ်ချက်အရ MCP Tools များကို ခေါ်ဆိုခြင်း။
  - LLM နှင့် MCP Server အကြား Conversation Flow ကို စီမံခြင်း။
- `bot.chat()` Method သည် MCP Tool Execution များမှ ရလဒ်များပါဝင်သော Natural
LLM response တွင် `choices` အ array ပါဝင်မည်ဖြစ်သည်။ `tool_calls` ရှိမရှိကိုစစ်ဆေးရန်အတွက် ရလဒ်ကို အလုပ်လုပ်စေဖို့လိုအပ်ပါသည်။ ဒါက LLM က အတိအကျ tool ကို arguments ဖြင့်ခေါ်ဆိုရန် တောင်းဆိုနေသည်ကို သိနိုင်စေပါသည်။ `main.rs` ဖိုင်၏ အောက်ဆုံးတွင် LLM response ကို ကိုင်တွယ်ရန် function တစ်ခုကို သတ်မှတ်ရန် အောက်ပါ code ကို ထည့်ပါ။

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

`tool_calls` ရှိပါက tool အချက်အလက်ကို ထုတ်ယူပြီး tool request ဖြင့် MCP server ကို ခေါ်ဆိုပါမည်။ ထို့နောက် ရလဒ်များကို စကားပြော messages တွင် ထည့်သွင်းပါမည်။ LLM နှင့် ဆက်လက်စကားပြောပြီး assistant response နှင့် tool call ရလဒ်များကို messages တွင် update လုပ်ပါမည်။

MCP calls အတွက် LLM က ပြန်ပေးသော tool call အချက်အလက်ကို ထုတ်ယူရန် helper function တစ်ခုကို ထည့်သွင်းပါမည်။ ခေါ်ဆိုရန်လိုအပ်သော အရာအားလုံးကို ထုတ်ယူရန်အတွက် `main.rs` ဖိုင်၏ အောက်ဆုံးတွင် အောက်ပါ code ကို ထည့်ပါ။

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

အပိုင်းအားလုံး ပြည့်စုံပြီးနောက် user prompt အစပိုင်းကို ကိုင်တွယ်ပြီး LLM ကို ခေါ်ဆိုနိုင်ပါသည်။ `main` function ကို အောက်ပါ code ဖြင့် update လုပ်ပါ။

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

ဤ code သည် user prompt အစပိုင်းကို LLM ကို query လုပ်ပြီး tool calls ကို dynamic အနေဖြင့် ကိုင်တွယ်ရန် response ကို အလုပ်လုပ်စေပါမည်။

အိုကေ၊ သင်လုပ်နိုင်ပါပြီ!

## လုပ်ငန်းတာဝန်

လေ့ကျင့်ခန်းမှ code ကို ယူပြီး server ကို tools များဖြင့် တိုးချဲ့ပါ။ ထို့နောက် LLM ပါသော client တစ်ခုကို exercise အတိုင်း ဖန်တီးပြီး prompts များကို အသုံးပြု၍ server tools များကို dynamic အနေဖြင့် ခေါ်ဆိုနိုင်မည်ဖြစ်ကြောင်း စမ်းသပ်ပါ။ ဤ client ဖန်တီးနည်းသည် end user အတွက် prompt များကို အသုံးပြုနိုင်ပြီး MCP server ခေါ်ဆိုမှုကို မသိစိတ်ဖြင့် အတွေ့အကြုံကောင်းများရရှိစေမည်ဖြစ်သည်။

## ဖြေရှင်းချက်

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## အဓိကအချက်များ

- Client တွင် LLM ထည့်သွင်းခြင်းသည် MCP Servers နှင့် အပြန်အလှန် ဆက်သွယ်ရန် ပိုမိုကောင်းမွန်သော နည်းလမ်းကို ပေးစွမ်းသည်။
- MCP Server response ကို LLM နားလည်နိုင်သော အရာတစ်ခုအဖြစ် ပြောင်းလဲရန် လိုအပ်သည်။

## နမူနာများ

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## အပိုဆောင်းအရင်းအမြစ်များ

## နောက်တစ်ခု

- နောက်တစ်ခု: [Visual Studio Code ကို အသုံးပြု၍ server ကို အသုံးပြုခြင်း](../04-vscode/README.md)

---

**အကြောင်းကြားချက်**:  
ဤစာရွက်စာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) ကို အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှုအတွက် ကြိုးစားနေသော်လည်း အလိုအလျောက် ဘာသာပြန်မှုများတွင် အမှားများ သို့မဟုတ် မတိကျမှုများ ပါဝင်နိုင်သည်ကို သတိပြုပါ။ မူရင်းဘာသာစကားဖြင့် ရေးသားထားသော စာရွက်စာတမ်းကို အာဏာတရ အရင်းအမြစ်အဖြစ် သတ်မှတ်သင့်ပါသည်။ အရေးကြီးသော အချက်အလက်များအတွက် လူ့ဘာသာပြန်ပညာရှင်များကို အသုံးပြုရန် အကြံပြုပါသည်။ ဤဘာသာပြန်မှုကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော အလွဲအလွဲအချော်အချော်များ သို့မဟုတ် အနားယူမှုများအတွက် ကျွန်ုပ်တို့သည် တာဝန်မယူပါ။