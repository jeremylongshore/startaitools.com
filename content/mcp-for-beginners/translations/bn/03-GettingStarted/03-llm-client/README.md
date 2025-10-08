<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T13:55:11+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "bn"
}
-->
# ক্লায়েন্ট তৈরি করা LLM সহ

এখন পর্যন্ত, আপনি কীভাবে একটি সার্ভার এবং একটি ক্লায়েন্ট তৈরি করতে হয় তা দেখেছেন। ক্লায়েন্টটি সার্ভারকে স্পষ্টভাবে কল করে তার টুল, রিসোর্স এবং প্রম্পটগুলি তালিকাভুক্ত করতে সক্ষম হয়েছে। তবে এটি খুব ব্যবহারিক পদ্ধতি নয়। আপনার ব্যবহারকারী এজেন্টিক যুগে বাস করে এবং প্রম্পট ব্যবহার করতে এবং একটি LLM এর সাথে যোগাযোগ করতে চায়। আপনার ব্যবহারকারী MCP ব্যবহার করছেন কিনা তা নিয়ে চিন্তা করে না, তবে তারা প্রাকৃতিক ভাষা ব্যবহার করে যোগাযোগের প্রত্যাশা করে। তাহলে আমরা কীভাবে এটি সমাধান করব? সমাধানটি হল ক্লায়েন্টে একটি LLM যোগ করা।

## ওভারভিউ

এই পাঠে আমরা একটি LLM যোগ করার উপর ফোকাস করব এবং দেখাব কীভাবে এটি আপনার ব্যবহারকারীর জন্য একটি অনেক ভালো অভিজ্ঞতা প্রদান করে।

## শেখার লক্ষ্য

এই পাঠ শেষে, আপনি সক্ষম হবেন:

- একটি LLM সহ একটি ক্লায়েন্ট তৈরি করতে।
- একটি MCP সার্ভারের সাথে LLM ব্যবহার করে নির্বিঘ্নে যোগাযোগ করতে।
- ক্লায়েন্ট সাইডে ব্যবহারকারীর জন্য একটি উন্নত অভিজ্ঞতা প্রদান করতে।

## পদ্ধতি

চলুন আমরা যে পদ্ধতি গ্রহণ করতে হবে তা বুঝি। একটি LLM যোগ করা সহজ শোনায়, তবে আমরা কি আসলে এটি করব?

ক্লায়েন্টটি সার্ভারের সাথে এভাবে যোগাযোগ করবে:

1. সার্ভারের সাথে সংযোগ স্থাপন করুন।

1. সক্ষমতা, প্রম্পট, রিসোর্স এবং টুল তালিকাভুক্ত করুন এবং তাদের স্কিমা সংরক্ষণ করুন।

1. একটি LLM যোগ করুন এবং সংরক্ষিত সক্ষমতা এবং তাদের স্কিমা এমন একটি ফরম্যাটে পাস করুন যা LLM বুঝতে পারে।

1. একটি ব্যবহারকারীর প্রম্পট পরিচালনা করুন এবং এটি LLM-এ পাস করুন ক্লায়েন্ট দ্বারা তালিকাভুক্ত টুলগুলির সাথে।

দারুণ, এখন আমরা উচ্চ স্তরে এটি কীভাবে করতে পারি তা বুঝতে পেরেছি, নিচের অনুশীলনে এটি চেষ্টা করি।

## অনুশীলন: একটি LLM সহ ক্লায়েন্ট তৈরি করা

এই অনুশীলনে, আমরা আমাদের ক্লায়েন্টে একটি LLM যোগ করতে শিখব।

### GitHub Personal Access Token ব্যবহার করে প্রমাণীকরণ

GitHub টোকেন তৈরি করা একটি সহজ প্রক্রিয়া। এটি কীভাবে করবেন:

- GitHub সেটিংসে যান – উপরের ডান কোণে আপনার প্রোফাইল ছবিতে ক্লিক করুন এবং সেটিংস নির্বাচন করুন।
- Developer Settings-এ যান – স্ক্রল করুন এবং Developer Settings-এ ক্লিক করুন।
- Personal Access Tokens নির্বাচন করুন – Fine-grained tokens-এ ক্লিক করুন এবং নতুন টোকেন তৈরি করুন।
- আপনার টোকেন কনফিগার করুন – রেফারেন্সের জন্য একটি নোট যোগ করুন, একটি মেয়াদ শেষ হওয়ার তারিখ সেট করুন এবং প্রয়োজনীয় স্কোপ (অনুমতি) নির্বাচন করুন। এই ক্ষেত্রে নিশ্চিত করুন যে আপনি Models অনুমতি যোগ করেছেন।
- টোকেন তৈরি করুন এবং কপি করুন – Generate token-এ ক্লিক করুন এবং এটি অবিলম্বে কপি করুন, কারণ আপনি এটি আবার দেখতে পারবেন না।

### -1- সার্ভারের সাথে সংযোগ স্থাপন করুন

চলুন প্রথমে আমাদের ক্লায়েন্ট তৈরি করি:

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

উপরের কোডে আমরা:

- প্রয়োজনীয় লাইব্রেরি আমদানি করেছি।
- দুটি সদস্য `client` এবং `openai` সহ একটি ক্লাস তৈরি করেছি যা আমাদের ক্লায়েন্ট পরিচালনা করতে এবং একটি LLM-এর সাথে যোগাযোগ করতে সাহায্য করবে।
- আমাদের LLM ইনস্ট্যান্স কনফিগার করেছি যাতে GitHub Models ব্যবহার করা যায় `baseUrl` সেট করে ইনফারেন্স API-তে নির্দেশ করার জন্য।

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

উপরের কোডে আমরা:

- MCP-এর জন্য প্রয়োজনীয় লাইব্রেরি আমদানি করেছি।
- একটি ক্লায়েন্ট তৈরি করেছি।

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

প্রথমে, আপনাকে আপনার `pom.xml` ফাইলে LangChain4j ডিপেনডেন্সি যোগ করতে হবে। MCP ইন্টিগ্রেশন এবং GitHub Models সমর্থন সক্ষম করতে এই ডিপেনডেন্সি যোগ করুন:

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

তারপর আপনার Java ক্লায়েন্ট ক্লাস তৈরি করুন:

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

উপরের কোডে আমরা:

- **LangChain4j ডিপেনডেন্সি যোগ করেছি**: MCP ইন্টিগ্রেশন, OpenAI অফিসিয়াল ক্লায়েন্ট এবং GitHub Models সমর্থনের জন্য প্রয়োজনীয়।
- **LangChain4j লাইব্রেরি আমদানি করেছি**: MCP ইন্টিগ্রেশন এবং OpenAI চ্যাট মডেল কার্যকারিতার জন্য।
- **একটি `ChatLanguageModel` তৈরি করেছি**: GitHub টোকেন ব্যবহার করে GitHub Models কনফিগার করেছি।
- **HTTP ট্রান্সপোর্ট সেট আপ করেছি**: Server-Sent Events (SSE) ব্যবহার করে MCP সার্ভারের সাথে সংযোগ স্থাপন করেছি।
- **একটি MCP ক্লায়েন্ট তৈরি করেছি**: যা সার্ভারের সাথে যোগাযোগ পরিচালনা করবে।
- **LangChain4j-এর বিল্ট-ইন MCP সমর্থন ব্যবহার করেছি**: যা LLM এবং MCP সার্ভারের মধ্যে ইন্টিগ্রেশন সহজ করে।

#### Rust

এই উদাহরণটি ধরে নিচ্ছে যে আপনার একটি Rust ভিত্তিক MCP সার্ভার চলছে। যদি আপনার কাছে এটি না থাকে, তাহলে [01-first-server](../01-first-server/README.md) পাঠে ফিরে যান এবং সার্ভার তৈরি করুন।

আপনার Rust MCP সার্ভার তৈরি করার পরে, একটি টার্মিনাল খুলুন এবং সার্ভারের মতো ডিরেক্টরিতে যান। তারপর একটি নতুন LLM ক্লায়েন্ট প্রকল্প তৈরি করতে নিম্নলিখিত কমান্ড চালান:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

আপনার `Cargo.toml` ফাইলে নিম্নলিখিত ডিপেনডেন্সি যোগ করুন:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> OpenAI-এর জন্য কোনও অফিসিয়াল Rust লাইব্রেরি নেই, তবে `async-openai` ক্রেট একটি [কমিউনিটি দ্বারা রক্ষণাবেক্ষিত লাইব্রেরি](https://platform.openai.com/docs/libraries/rust#rust) যা সাধারণত ব্যবহৃত হয়।

`src/main.rs` ফাইলটি খুলুন এবং এর বিষয়বস্তু নিম্নলিখিত কোড দিয়ে প্রতিস্থাপন করুন:

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

এই কোডটি একটি বেসিক Rust অ্যাপ্লিকেশন সেট আপ করে যা MCP সার্ভার এবং GitHub Models-এর সাথে LLM ইন্টারঅ্যাকশনের জন্য সংযোগ স্থাপন করবে।

> [!IMPORTANT]
> অ্যাপ্লিকেশন চালানোর আগে আপনার GitHub টোকেন দিয়ে `OPENAI_API_KEY` পরিবেশ ভেরিয়েবল সেট করতে ভুলবেন না।

দারুণ, আমাদের পরবর্তী ধাপে, চলুন সার্ভারে সক্ষমতা তালিকাভুক্ত করি।

### -2- সার্ভারের সক্ষমতা তালিকাভুক্ত করুন

এখন আমরা সার্ভারের সাথে সংযোগ করব এবং তার সক্ষমতা জিজ্ঞাসা করব:

#### TypeScript

একই ক্লাসে, নিম্নলিখিত পদ্ধতিগুলি যোগ করুন:

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

উপরের কোডে আমরা:

- সার্ভারের সাথে সংযোগ স্থাপন করার জন্য কোড যোগ করেছি, `connectToServer`।
- একটি `run` পদ্ধতি তৈরি করেছি যা আমাদের অ্যাপের প্রবাহ পরিচালনার জন্য দায়ী। এখন পর্যন্ত এটি শুধুমাত্র টুল তালিকাভুক্ত করে, তবে আমরা শীঘ্রই আরও যোগ করব।

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

এখানে আমরা যোগ করেছি:

- রিসোর্স এবং টুল তালিকাভুক্ত করেছি এবং সেগুলি প্রিন্ট করেছি। টুলগুলির জন্য আমরা `inputSchema` তালিকাভুক্ত করেছি যা আমরা পরে ব্যবহার করব।

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

উপরের কোডে আমরা:

- MCP সার্ভারে উপলব্ধ টুলগুলি তালিকাভুক্ত করেছি।
- প্রতিটি টুলের জন্য নাম, বিবরণ এবং এর স্কিমা তালিকাভুক্ত করেছি। পরবর্তীটি আমরা শীঘ্রই টুলগুলি কল করতে ব্যবহার করব।

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

উপরের কোডে আমরা:

- একটি `McpToolProvider` তৈরি করেছি যা MCP সার্ভার থেকে সমস্ত টুল স্বয়ংক্রিয়ভাবে আবিষ্কার এবং নিবন্ধন করে।
- টুল প্রদানকারী অভ্যন্তরীণভাবে MCP টুল স্কিমা এবং LangChain4j-এর টুল ফরম্যাটের মধ্যে রূপান্তর পরিচালনা করে।
- এই পদ্ধতি ম্যানুয়াল টুল তালিকাভুক্তি এবং রূপান্তর প্রক্রিয়াকে সরিয়ে দেয়।

#### Rust

MCP সার্ভার থেকে টুলগুলি পুনরুদ্ধার করা `list_tools` পদ্ধতি ব্যবহার করে করা হয়। আপনার `main` ফাংশনে, MCP ক্লায়েন্ট সেট আপ করার পরে, নিম্নলিখিত কোড যোগ করুন:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- সার্ভারের সক্ষমতাগুলিকে LLM টুলে রূপান্তর করুন

সার্ভারের সক্ষমতাগুলি তালিকাভুক্ত করার পরের ধাপটি হল সেগুলিকে এমন একটি ফরম্যাটে রূপান্তর করা যা LLM বুঝতে পারে। একবার আমরা এটি করলে, আমরা এই সক্ষমতাগুলি LLM-এ টুল হিসাবে প্রদান করতে পারি।

#### TypeScript

1. MCP সার্ভার থেকে প্রাপ্ত প্রতিক্রিয়াকে LLM-এর জন্য টুল সংজ্ঞা ফরম্যাটে রূপান্তর করতে নিম্নলিখিত কোড যোগ করুন:

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

    উপরের কোডটি MCP সার্ভার থেকে একটি প্রতিক্রিয়া গ্রহণ করে এবং এটি একটি টুল সংজ্ঞা ফরম্যাটে রূপান্তর করে যা LLM বুঝতে পারে।

1. পরবর্তী ধাপে, `run` পদ্ধতিটি আপডেট করুন যাতে সার্ভারের সক্ষমতাগুলি তালিকাভুক্ত করা যায়:

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

    উপরের কোডে, আমরা `run` পদ্ধতিটি আপডেট করেছি যাতে ফলাফলের মাধ্যমে ম্যাপ করা যায় এবং প্রতিটি এন্ট্রির জন্য `openAiToolAdapter` কল করা যায়।

#### Python

1. প্রথমে, নিম্নলিখিত রূপান্তরকারী ফাংশন তৈরি করুন:

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

    উপরের ফাংশনে `convert_to_llm_tools` আমরা MCP টুল প্রতিক্রিয়া গ্রহণ করি এবং এটি এমন একটি ফরম্যাটে রূপান্তর করি যা LLM বুঝতে পারে।

1. পরবর্তী ধাপে, আমাদের ক্লায়েন্ট কোড আপডেট করুন যাতে এই ফাংশনটি ব্যবহার করা যায়:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    এখানে, আমরা MCP টুল প্রতিক্রিয়াকে `convert_to_llm_tool` কল করে রূপান্তর করছি যাতে আমরা পরে LLM-এ এটি ফিড করতে পারি।

#### .NET

1. MCP টুল প্রতিক্রিয়াকে এমন কিছুতে রূপান্তর করতে কোড যোগ করুন যা LLM বুঝতে পারে:

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

উপরের কোডে আমরা:

- একটি `ConvertFrom` ফাংশন তৈরি করেছি যা নাম, বিবরণ এবং ইনপুট স্কিমা গ্রহণ করে।
- একটি FunctionDefinition তৈরি করার কার্যকারিতা সংজ্ঞায়িত করেছি যা একটি ChatCompletionsDefinition-এ পাস করা হয়। এটি এমন কিছু যা LLM বুঝতে পারে।

1. উপরের ফাংশনটি ব্যবহার করার জন্য কিছু বিদ্যমান কোড আপডেট করার উপায় দেখুন:

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

উপরের কোডে আমরা:

- প্রাকৃতিক ভাষার ইন্টারঅ্যাকশনের জন্য একটি সাধারণ `Bot` ইন্টারফেস সংজ্ঞায়িত করেছি।
- LangChain4j-এর `AiServices` ব্যবহার করেছি যাতে LLM এবং MCP টুল প্রদানকারী স্বয়ংক্রিয়ভাবে বাঁধা যায়।
- ফ্রেমওয়ার্কটি অভ্যন্তরীণভাবে টুল স্কিমা রূপান্তর এবং ফাংশন কল পরিচালনা করে।
- এই পদ্ধতি ম্যানুয়াল টুল রূপান্তর দূর করে - LangChain4j MCP টুলগুলিকে LLM-সামঞ্জস্যপূর্ণ ফরম্যাটে রূপান্তর করার সমস্ত জটিলতা পরিচালনা করে।

#### Rust

MCP টুল প্রতিক্রিয়াকে এমন একটি ফরম্যাটে রূপান্তর করতে যা LLM বুঝতে পারে, আমরা একটি হেল্পার ফাংশন যোগ করব যা টুল তালিকাকে ফরম্যাট করে। আপনার `main.rs` ফাইলে `main` ফাংশনের নিচে নিম্নলিখিত কোড যোগ করুন। এটি LLM-এ অনুরোধ করার সময় ডাকা হবে:

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

দারুণ, আমরা এখন কোনও ব্যবহারকারীর অনুরোধ পরিচালনা করতে প্রস্তুত, তাই চলুন এটি পরবর্তী ধাপে মোকাবিলা করি।

### -4- ব্যবহারকারীর প্রম্পট অনুরোধ পরিচালনা করুন

এই অংশে, আমরা ব্যবহারকারীর অনুরোধগুলি পরিচালনা করব।

#### TypeScript

1. একটি পদ্ধতি যোগ করুন যা আমাদের LLM-কে কল করতে ব্যবহার করা হবে:

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

    উপরের কোডে আমরা:

    - একটি `callTools` পদ্ধতি যোগ করেছি।
    - পদ্ধতিটি একটি LLM প্রতিক্রিয়া গ্রহণ করে এবং পরীক্ষা করে যে কোনও টুল কল করা হয়েছে কিনা:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - যদি LLM নির্দেশ করে যে এটি কল করা উচিত, তাহলে একটি টুল কল করে:

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

1. `run` পদ্ধতিটি আপডেট করুন যাতে LLM-এ কল এবং `callTools` কল অন্তর্ভুক্ত থাকে:

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

দারুণ, পুরো কোডটি তালিকাভুক্ত করি:

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

1. LLM কল করার জন্য প্রয়োজনীয় কিছু আমদানি যোগ করুন:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. পরবর্তী ধাপে, LLM-কে কল করার জন্য একটি ফাংশন যোগ করুন:

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

    উপরের কোডে আমরা:

    - আমাদের ফাংশনগুলি, যা আমরা MCP সার্ভারে খুঁজে পেয়েছি এবং রূপান্তর করেছি, LLM-এ পাস করেছি।
    - তারপর আমরা উক্ত ফাংশনগুলির সাথে LLM-কে কল করেছি।
    - তারপর, আমরা ফলাফলটি পরিদর্শন করছি যে কোন ফাংশনগুলি কল করা উচিত কিনা।
    - অবশেষে, আমরা কল করার জন্য একটি ফাংশনের অ্যারে পাস করছি।

1. চূড়ান্ত ধাপ, আমাদের প্রধান কোড আপডেট করুন:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    সেখানে, এটি চূড়ান্ত ধাপ ছিল, উপরের কোডে আমরা:

    - একটি MCP টুল কল করছি `call_tool` ব্যবহার করে একটি ফাংশন যা LLM মনে করে আমাদের প্রম্পটের উপর ভিত্তি করে কল করা উচিত।
    - MCP সার্ভারে টুল কলের ফলাফল প্রিন্ট করছি।

#### .NET

1. একটি LLM প্রম্পট অনুরোধ করার জন্য কিছু কোড দেখাই:

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

    উপরের কোডে আমরা:

    - MCP সার্ভার থেকে টুলগুলি পুনরুদ্ধার করেছি, `var tools = await GetMcpTools()`।
    - একটি ব্যবহারকারীর প্রম্পট `userMessage` সংজ্ঞায়িত করেছি।
    - একটি অপশন অবজেক্ট তৈরি করেছি যা মডেল এবং টুলগুলি নির্দিষ্ট করে।
    - LLM-এর দিকে একটি অনুরোধ করেছি।

1. একটি শেষ ধাপ, দেখি LLM মনে করে আমাদের একটি ফাংশন কল করা উচিত কিনা:

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

    উপরের কোডে আমরা:

    - একটি ফাংশন কলের তালিকার মাধ্যমে লুপ করেছি।
    - প্রতিটি টুল কলের জন্য, নাম এবং আর্গুমেন্টগুলি বের করেছি এবং MCP ক্লায়েন্ট ব্যবহার করে MCP সার্ভারে টুলটি কল করেছি। অবশেষে আমরা ফলাফলগুলি প্রিন্ট করেছি।

এখানে পুরো কোড:

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

উপরের কোডে আমরা:

- MCP সার্ভার টুলগুলির সাথে ইন্টারঅ্যাকশনের জন্য সহজ প্রাকৃতিক ভাষার প্রম্পট ব্যবহার করেছি।
- LangChain4j ফ্রেমওয়ার্ক স্বয়ংক্রিয়ভাবে পরিচালনা করে:
  - প্রম্পট থেকে টুল কল রূপান্তর যখন প্রয়োজন।
  - LLM-এর সিদ্ধান্তের উপর ভিত্তি করে প্রাসঙ্গিক MCP টুল কল করা।
  - LLM এবং MCP সার্ভারের মধ্যে কথোপকথনের প্রবাহ পরিচালনা করা।
- `bot.chat()` পদ্ধতি প্রাকৃতিক ভাষার প্রতিক্রিয়া প্রদান করে যা MCP টুল এক্সিকিউশন থেকে ফলাফল অন্তর্ভুক্ত করতে পারে।
- এই পদ্ধতি একটি নির্বিঘ্ন ব্যবহারকারীর অভিজ্ঞতা প্রদান করে যেখানে ব্যবহারকারীদের অন্তর্নিহিত MCP বাস্তবায়ন সম্পর্কে জানতে হয় না।

সম্পূর্ণ কোড উদাহরণ:

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

এখানে বেশিরভাগ কাজ হয়। আমরা ব্যবহারকারীর প্রাথমিক প্রম্পট সহ LLM-কে কল করব, তারপর প্রতিক্রিয়া প্রক্রিয়া করব এবং দেখব কোনও টুল কল করা দরকার কিনা। যদি প্রয়োজন হয়, আমরা সেই টুলগুলি কল করব এবং LLM-এর সাথে কথোপকথন চালিয়ে যাব যতক্ষণ না আর কোনও টুল কল করার প্রয়োজন হয় এবং আমাদের একটি চূড়ান্ত প্রতিক্রিয়া থাকে।

আমরা LLM-এ একাধিক কল করব, তাই চলুন একটি ফাংশন সংজ্ঞায়িত করি যা LLM কল পরিচালনা করবে। আপনার `main.rs` ফাইলে নিম্নলিখিত ফাংশন যোগ করুন:

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

এই ফাংশনটি LLM ক্লায়েন্ট, বার্তার একটি তালিকা (ব্যবহারকারীর প্রম্পট সহ), MCP সার্ভার থেকে টুলগুলি গ্রহণ করে এবং LLM-এ একটি অনুরোধ পাঠায়, প্রতিক্রিয়া প্রদান করে।
LLM থেকে প্রাপ্ত প্রতিক্রিয়ায় একটি `choices` অ্যারে থাকবে। আমাদের ফলাফল প্রক্রিয়া করতে হবে এবং দেখতে হবে কোনো `tool_calls` উপস্থিত আছে কিনা। এটি আমাদের জানায় যে LLM একটি নির্দিষ্ট টুলকে আর্গুমেন্ট সহ কল করার অনুরোধ করছে। আপনার `main.rs` ফাইলের নিচে নিম্নলিখিত কোড যোগ করুন একটি ফাংশন সংজ্ঞায়িত করতে যা LLM প্রতিক্রিয়া পরিচালনা করবে:

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

যদি `tool_calls` উপস্থিত থাকে, এটি টুলের তথ্য বের করে, টুল অনুরোধ সহ MCP সার্ভারকে কল করে এবং কথোপকথনের বার্তাগুলিতে ফলাফল যোগ করে। এরপর এটি LLM-এর সাথে কথোপকথন চালিয়ে যায় এবং বার্তাগুলি সহকারী প্রতিক্রিয়া এবং টুল কলের ফলাফল দিয়ে আপডেট হয়।

MCP কলের জন্য LLM যে টুল কল তথ্য প্রদান করে তা বের করতে, আমরা একটি সহায়ক ফাংশন যোগ করব যা কল করার জন্য প্রয়োজনীয় সবকিছু বের করবে। আপনার `main.rs` ফাইলের নিচে নিম্নলিখিত কোড যোগ করুন:

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

সবকিছু প্রস্তুত হয়ে গেলে, আমরা প্রাথমিক ব্যবহারকারীর প্রম্পট পরিচালনা করতে এবং LLM-কে কল করতে পারি। আপনার `main` ফাংশন আপডেট করুন নিম্নলিখিত কোড যোগ করে:

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

এটি প্রাথমিক ব্যবহারকারীর প্রম্পটের সাথে LLM-কে প্রশ্ন করবে দুটি সংখ্যার যোগফল জানতে এবং প্রতিক্রিয়া প্রক্রিয়া করবে টুল কলগুলি গতিশীলভাবে পরিচালনা করতে।

অসাধারণ, আপনি এটি সম্পন্ন করেছেন!

## অ্যাসাইনমেন্ট

অনুশীলনের কোডটি নিয়ে সার্ভারটি আরও কিছু টুল দিয়ে তৈরি করুন। এরপর একটি ক্লায়েন্ট তৈরি করুন LLM সহ, যেমন অনুশীলনে দেখানো হয়েছে, এবং বিভিন্ন প্রম্পট দিয়ে এটি পরীক্ষা করুন যাতে নিশ্চিত হওয়া যায় যে আপনার সার্ভারের সব টুল গতিশীলভাবে কল হচ্ছে। এই ধরনের ক্লায়েন্ট তৈরি করার ফলে শেষ ব্যবহারকারী একটি চমৎকার অভিজ্ঞতা পাবে কারণ তারা প্রম্পট ব্যবহার করতে পারবে, নির্দিষ্ট ক্লায়েন্ট কমান্ডের পরিবর্তে, এবং MCP সার্ভার কল হওয়ার বিষয়ে সম্পূর্ণ অজ্ঞ থাকবে।

## সমাধান

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## মূল বিষয়গুলো

- আপনার ক্লায়েন্টে LLM যোগ করলে MCP সার্ভারের সাথে ব্যবহারকারীদের যোগাযোগের একটি উন্নত উপায় প্রদান করে।
- MCP সার্ভারের প্রতিক্রিয়াকে এমন কিছুতে রূপান্তর করতে হবে যা LLM বুঝতে পারে।

## নমুনা

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## অতিরিক্ত সম্পদ

## পরবর্তী কী

- পরবর্তী: [Visual Studio Code ব্যবহার করে একটি সার্ভার ব্যবহার করা](../04-vscode/README.md)

---

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসাধ্য সঠিকতার জন্য চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল ভাষায় থাকা নথিটিকে প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদ ব্যবহারের ফলে কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যা হলে আমরা দায়বদ্ধ থাকব না।