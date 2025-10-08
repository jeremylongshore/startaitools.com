<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:01:27+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "ne"
}
-->
# LLM प्रयोग गरेर क्लाइन्ट बनाउने

अहिलेसम्म, तपाईंले सर्भर र क्लाइन्ट कसरी बनाउने देख्नुभएको छ। क्लाइन्टले सर्भरलाई स्पष्ट रूपमा यसको उपकरणहरू, स्रोतहरू र प्रम्प्टहरूको सूची दिन कल गर्न सक्षम भएको छ। तर, यो धेरै व्यावहारिक दृष्टिकोण होइन। तपाईंको प्रयोगकर्ता एजेन्टिक युगमा बस्छन् र प्रम्प्टहरू प्रयोग गर्न र LLM सँग संवाद गर्न चाहन्छन्। तपाईंको प्रयोगकर्तालाई तपाईंले MCP प्रयोग गरेर आफ्नो क्षमताहरू भण्डारण गर्नुहुन्छ कि हुँदैन भन्ने कुराले मतलब छैन, तर उनीहरूले प्राकृतिक भाषाको माध्यमबाट अन्तरक्रिया गर्न चाहन्छन्। त्यसो भए हामी यसलाई कसरी समाधान गर्ने? समाधान भनेको क्लाइन्टमा LLM थप्नु हो।

## अवलोकन

यस पाठमा हामी क्लाइन्टमा LLM थप्नमा केन्द्रित छौं र यो तपाईंको प्रयोगकर्ताको लागि धेरै राम्रो अनुभव कसरी प्रदान गर्दछ भनेर देखाउँछौं।

## सिक्ने उद्देश्यहरू

यस पाठको अन्त्यसम्ममा, तपाईं सक्षम हुनुहुनेछ:

- LLM सहित क्लाइन्ट बनाउनुहोस्।
- MCP सर्भरसँग LLM प्रयोग गरेर सहज रूपमा अन्तरक्रिया गर्नुहोस्।
- क्लाइन्ट पक्षमा अन्तिम प्रयोगकर्ता अनुभव सुधार गर्नुहोस्।

## दृष्टिकोण

हामीले लिनुपर्ने दृष्टिकोण बुझ्ने प्रयास गरौं। LLM थप्नु सरल लाग्छ, तर के हामी वास्तवमा यो गर्नेछौं?

यहाँ क्लाइन्टले सर्भरसँग कसरी अन्तरक्रिया गर्नेछ:

1. सर्भरसँग जडान स्थापना गर्नुहोस्।

1. क्षमताहरू, प्रम्प्टहरू, स्रोतहरू र उपकरणहरूको सूची बनाउनुहोस्, र तिनीहरूको स्किमालाई सुरक्षित गर्नुहोस्।

1. LLM थप्नुहोस् र सुरक्षित गरिएको क्षमताहरू र तिनीहरूको स्किमालाई LLM ले बुझ्ने ढाँचामा पास गर्नुहोस्।

1. प्रयोगकर्ताको प्रम्प्टलाई LLM मा पास गर्नुहोस्, क्लाइन्टले सूचीबद्ध गरेको उपकरणहरूसँगै।

ठीक छ, अब हामीले उच्च स्तरमा यो कसरी गर्न सकिन्छ भन्ने कुरा बुझ्यौं, तलको अभ्यासमा यसलाई प्रयास गरौं।

## अभ्यास: LLM सहित क्लाइन्ट बनाउने

यस अभ्यासमा, हामी हाम्रो क्लाइन्टमा LLM थप्न सिक्नेछौं।

### GitHub व्यक्तिगत पहुँच टोकन प्रयोग गरेर प्रमाणीकरण

GitHub टोकन बनाउने प्रक्रिया सरल छ। यहाँ कसरी गर्न सकिन्छ:

- GitHub सेटिङमा जानुहोस् – माथि दायाँ कुनामा आफ्नो प्रोफाइल चित्रमा क्लिक गर्नुहोस् र सेटिङ चयन गर्नुहोस्।
- डेभलपर सेटिङमा जानुहोस् – तल स्क्रोल गर्नुहोस् र डेभलपर सेटिङमा क्लिक गर्नुहोस्।
- व्यक्तिगत पहुँच टोकन चयन गर्नुहोस् – Fine-grained टोकनमा क्लिक गर्नुहोस् र नयाँ टोकन सिर्जना गर्नुहोस्।
- आफ्नो टोकन कन्फिगर गर्नुहोस् – सन्दर्भको लागि नोट थप्नुहोस्, समाप्ति मिति सेट गर्नुहोस्, र आवश्यक स्कोपहरू (अनुमतिहरू) चयन गर्नुहोस्। यस अवस्थामा, Models अनुमति थप्न निश्चित हुनुहोस्।
- टोकन सिर्जना गर्नुहोस् र प्रतिलिपि गर्नुहोस् – टोकन सिर्जना क्लिक गर्नुहोस्, र तुरुन्तै प्रतिलिपि गर्नुहोस्, किनकि तपाईंले यसलाई फेरि हेर्न सक्नुहुन्न।

### -1- सर्भरसँग जडान गर्नुहोस्

पहिला हाम्रो क्लाइन्ट बनाऔं:

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

माथिको कोडमा हामीले:

- आवश्यक लाइब्रेरीहरू आयात गरेका छौं।
- दुई सदस्यहरू `client` र `openai` सहितको कक्षा बनाएका छौं, जसले क्लाइन्ट व्यवस्थापन गर्न र LLM सँग अन्तरक्रिया गर्न मद्दत गर्नेछ।
- हाम्रो LLM इन्स्ट्यान्सलाई GitHub Models प्रयोग गर्न कन्फिगर गरेका छौं, `baseUrl` लाई inference API मा संकेत गर्दै।

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

माथिको कोडमा हामीले:

- MCP का लागि आवश्यक लाइब्रेरीहरू आयात गरेका छौं।
- क्लाइन्ट बनाएका छौं।

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

पहिला, तपाईंले `pom.xml` फाइलमा LangChain4j निर्भरता थप्नुपर्नेछ। MCP एकीकरण र GitHub Models समर्थन सक्षम गर्न यी निर्भरता थप्नुहोस्:

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

त्यसपछि आफ्नो Java क्लाइन्ट कक्षा बनाउनुहोस्:

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

माथिको कोडमा हामीले:

- **LangChain4j निर्भरता थपेका छौं**: MCP एकीकरण, OpenAI आधिकारिक क्लाइन्ट, र GitHub Models समर्थनका लागि आवश्यक।
- **LangChain4j लाइब्रेरीहरू आयात गरेका छौं**: MCP एकीकरण र OpenAI च्याट मोडेल कार्यक्षमताका लागि।
- **`ChatLanguageModel` बनाएका छौं**: GitHub टोकनको साथ GitHub Models प्रयोग गर्न कन्फिगर गरिएको।
- **HTTP ट्रान्सपोर्ट सेट अप गरेका छौं**: Server-Sent Events (SSE) प्रयोग गरेर MCP सर्भरसँग जडान गर्न।
- **MCP क्लाइन्ट बनाएका छौं**: जसले सर्भरसँगको सञ्चार व्यवस्थापन गर्नेछ।
- **LangChain4j को बिल्ट-इन MCP समर्थन प्रयोग गरेका छौं**: जसले LLM र MCP सर्भरहरू बीचको एकीकरणलाई सरल बनाउँछ।

#### Rust

यो उदाहरणले Rust आधारित MCP सर्भर चलिरहेको छ भन्ने मान्छ। यदि तपाईंसँग छैन भने, [01-first-server](../01-first-server/README.md) पाठमा फर्केर सर्भर बनाउनुहोस्।

एकपटक तपाईंको Rust MCP सर्भर भए पछि, टर्मिनल खोल्नुहोस् र सर्भरको समान डाइरेक्टरीमा नेभिगेट गर्नुहोस्। त्यसपछि नयाँ LLM क्लाइन्ट प्रोजेक्ट बनाउन निम्न आदेश चलाउनुहोस्:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

तपाईंको `Cargo.toml` फाइलमा निम्न निर्भरता थप्नुहोस्:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> OpenAI को लागि आधिकारिक Rust लाइब्रेरी छैन, तर `async-openai` क्रेट [समुदायद्वारा मर्मत गरिएको लाइब्रेरी](https://platform.openai.com/docs/libraries/rust#rust) हो जुन सामान्यतया प्रयोग गरिन्छ।

`src/main.rs` फाइल खोल्नुहोस् र यसको सामग्रीलाई निम्न कोडले प्रतिस्थापन गर्नुहोस्:

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

यो कोडले MCP सर्भर र GitHub Models सँग LLM अन्तरक्रियाको लागि जडान गर्ने आधारभूत Rust एप्लिकेसन सेट अप गर्दछ।

> [!IMPORTANT]
> एप्लिकेसन चलाउनु अघि `OPENAI_API_KEY` वातावरण चरलाई आफ्नो GitHub टोकनको साथ सेट गर्न निश्चित गर्नुहोस्।

ठीक छ, हाम्रो अर्को चरणको लागि, सर्भरमा क्षमताहरू सूचीबद्ध गरौं।

### -2- सर्भर क्षमताहरू सूचीबद्ध गर्नुहोस्

अब हामी सर्भरसँग जडान गर्नेछौं र यसको क्षमताहरू सोध्नेछौं:

#### TypeScript

उही कक्षामा, निम्न विधिहरू थप्नुहोस्:

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

माथिको कोडमा हामीले:

- सर्भरसँग जडान गर्नको लागि कोड थपेका छौं, `connectToServer`।
- हाम्रो एप फ्लो व्यवस्थापन गर्ने जिम्मेवार `run` विधि बनाएका छौं। अहिलेसम्म यसले उपकरणहरूको मात्र सूची बनाउँछ तर हामी यसमा चाँडै थप्नेछौं।

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

यहाँ हामीले थपेका छौं:

- स्रोतहरू र उपकरणहरूको सूची बनाएका छौं र तिनीहरूलाई प्रिन्ट गरेका छौं। उपकरणहरूको लागि हामीले `inputSchema` पनि सूचीबद्ध गरेका छौं, जुन हामी पछि प्रयोग गर्नेछौं।

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

माथिको कोडमा हामीले:

- MCP सर्भरमा उपलब्ध उपकरणहरूको सूची बनाएका छौं।
- प्रत्येक उपकरणको लागि नाम, विवरण र यसको स्किमा सूचीबद्ध गरेका छौं। पछिल्लो कुरा हामी चाँडै उपकरणहरू कल गर्न प्रयोग गर्नेछौं।

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

माथिको कोडमा हामीले:

- `McpToolProvider` बनाएका छौं जसले MCP सर्भरबाट सबै उपकरणहरू स्वचालित रूपमा पत्ता लगाउँछ र दर्ता गर्दछ।
- उपकरण प्रदायकले MCP उपकरण स्किमाहरू र LangChain4j को उपकरण ढाँचाको बीच रूपान्तरण आन्तरिक रूपमा व्यवस्थापन गर्दछ।
- यो दृष्टिकोणले म्यानुअल उपकरण सूचीकरण र रूपान्तरण प्रक्रियालाई हटाउँछ।

#### Rust

MCP सर्भरबाट उपकरणहरू पुनःप्राप्ति `list_tools` विधि प्रयोग गरेर गरिन्छ। तपाईंको `main` कार्यमा, MCP क्लाइन्ट सेट अप गरेपछि, निम्न कोड थप्नुहोस्:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- सर्भर क्षमताहरूलाई LLM उपकरणमा रूपान्तरण गर्नुहोस्

सर्भर क्षमताहरू सूचीबद्ध गरेपछि अर्को चरण भनेको तिनीहरूलाई LLM ले बुझ्ने ढाँचामा रूपान्तरण गर्नु हो। एकपटक हामीले यो गरेपछि, हामी यी क्षमताहरूलाई LLM लाई उपकरणको रूपमा प्रदान गर्न सक्छौं।

#### TypeScript

1. MCP सर्भरबाट प्रतिक्रिया रूपान्तरण गर्न निम्न कोड थप्नुहोस्:

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

    माथिको कोडले MCP सर्भरबाट प्रतिक्रिया लिन्छ र LLM ले बुझ्न सक्ने उपकरण परिभाषा ढाँचामा रूपान्तरण गर्दछ।

1. `run` विधि अपडेट गरौं:

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

    माथिको कोडमा, हामीले परिणामको माध्यमबाट म्याप गरेका छौं र प्रत्येक प्रविष्टिको लागि `openAiToolAdapter` कल गरेका छौं।

#### Python

1. पहिलो, निम्न रूपान्तरणकर्ता कार्य बनाऔं:

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

    माथिको `convert_to_llm_tools` कार्यमा हामी MCP उपकरण प्रतिक्रियालाई LLM ले बुझ्न सक्ने ढाँचामा रूपान्तरण गर्छौं।

1. हाम्रो क्लाइन्ट कोडलाई यस कार्य प्रयोग गर्न अपडेट गरौं:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    यहाँ, हामीले MCP उपकरण प्रतिक्रियालाई LLM मा फिड गर्न सक्ने ढाँचामा रूपान्तरण गर्न `convert_to_llm_tool` कल थपेका छौं।

#### .NET

1. MCP उपकरण प्रतिक्रियालाई LLM ले बुझ्न सक्ने ढाँचामा रूपान्तरण गर्न कोड थपौं:

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

माथिको कोडमा हामीले:

- `ConvertFrom` नाम, विवरण र इनपुट स्किमा लिने कार्य बनाएका छौं।
- `FunctionDefinition` बनाउने कार्यक्षमता परिभाषित गरेका छौं जुन `ChatCompletionsDefinition` मा पास गरिन्छ। पछिल्लो कुरा LLM ले बुझ्न सक्छ।

1. माथिको कार्य प्रयोग गर्न केही विद्यमान कोड अपडेट गरौं:

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

माथिको कोडमा हामीले:

- प्राकृतिक भाषाको अन्तरक्रियाका लागि सरल `Bot` इन्टरफेस परिभाषित गरेका छौं।
- LangChain4j को `AiServices` प्रयोग गरेर LLM लाई MCP उपकरण प्रदायकसँग स्वचालित रूपमा बाँधेका छौं।
- फ्रेमवर्कले उपकरण स्किमा रूपान्तरण र कार्य कलिंग आन्तरिक रूपमा व्यवस्थापन गर्दछ।
- यो दृष्टिकोणले म्यानुअल उपकरण रूपान्तरणलाई हटाउँछ - LangChain4j ले MCP उपकरणहरूलाई LLM-संगत ढाँचामा रूपान्तरण गर्ने सम्पूर्ण जटिलता व्यवस्थापन गर्दछ।

#### Rust

MCP उपकरण प्रतिक्रियालाई LLM ले बुझ्न सक्ने ढाँचामा रूपान्तरण गर्न, हामी उपकरण सूचीबद्ध गर्दा प्रयोग हुने सहायक कार्य थप्नेछौं। तपाईंको `main.rs` फाइलमा `main` कार्यको तल निम्न कोड थप्नुहोस्:

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

ठीक छ, अब हामी प्रयोगकर्ताको अनुरोधहरूलाई व्यवस्थापन गर्न तयार छौं, त्यसैले त्यसलाई अगाडि बढाऔं।

### -4- प्रयोगकर्ताको प्रम्प्ट अनुरोध व्यवस्थापन गर्नुहोस्

यस भागमा, हामी प्रयोगकर्ताको अनुरोधहरूलाई व्यवस्थापन गर्नेछौं।

#### TypeScript

1. हाम्रो LLM कल गर्न प्रयोग हुने विधि थपौं:

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

    माथिको कोडमा हामीले:

    - `callTools` विधि थपेका छौं।
    - विधिले LLM प्रतिक्रियालाई लिन्छ र जाँच गर्छ कि कुनै उपकरणहरू कल गरिएको छ कि छैन:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - LLM ले उपकरण कल गर्न संकेत गरेमा उपकरण कल गर्छ:

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

1. `run` विधि अपडेट गरौं:

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

ठीक छ, कोडलाई पूर्ण रूपमा सूचीबद्ध गरौं:

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

1. LLM कल गर्न आवश्यक आयातहरू थपौं:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. LLM कल गर्ने कार्य थपौं:

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

    माथिको कोडमा हामीले:

    - हाम्रो कार्यहरू, जुन हामीले MCP सर्भरमा फेला पारेका थियौं र रूपान्तरण गरेका थियौं, LLM मा पास गरेका छौं।
    - त्यसपछि हामीले ती कार्यहरू सहित LLM कल गरेका छौं।
    - त्यसपछि, हामीले परिणामलाई निरीक्षण गरेका छौं कि कुनै कार्यहरू कल गर्नुपर्नेछ कि छैन।
    - अन्तमा, हामीले कल गर्न कार्यहरूको एरे पास गरेका छौं।

1. अन्तिम चरण, हाम्रो मुख्य कोड अपडेट गरौं:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    त्यहाँ, यो अन्तिम चरण थियो, माथिको कोडमा हामी:

    - MCP उपकरणलाई `call_tool` मार्फत कल गर्दैछौं, LLM ले हाम्रो प्रम्प्टको आधारमा कल गर्नुपर्ने कार्य सोचेको थियो।
    - MCP सर्भरमा उपकरण कलको परिणाम प्रिन्ट गर्दैछौं।

#### .NET

1. LLM प्रम्प्ट अनुरोधको लागि कोड देखाऔं:

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

    माथिको कोडमा हामीले:

    - MCP सर्भरबाट उपकरणहरू पुनःप्राप्त गरेका छौं, `var tools = await GetMcpTools()`।
    - प्रयोगकर्ता प्रम्प्ट `userMessage` परिभाषित गरेका छौं।
    - विकल्प वस्तु निर्माण गरेका छौं जसले मोडेल र उपकरणहरू निर्दिष्ट गर्दछ।
    - LLM तर्फ अनुरोध गरेका छौं।

1. अन्तिम चरण, LLM ले कार्य कल गर्नुपर्ने सोचेको छ कि छैन हेर्नुहोस्:

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

    माथिको कोडमा हामीले:

    - कार्य कलहरूको सूचीमा लूप गरेका छौं।
    - प्रत्येक उपकरण कलको लागि, नाम र तर्कहरू पार्स गरेर MCP सर्भरमा MCP क्लाइन्ट प्रयोग गरेर उपकरण कल गरेका छौं। अन्तमा हामी परिणामहरू प्रिन्ट गर्छौं।

यहाँ पूर्ण कोड:

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

माथिको कोडमा हामीले:

- MCP सर्भर उपकरणहरूसँग अन्तरक्रिया गर्न सरल प्राकृतिक भाषा प्रम्प्टहरू प्रयोग गरेका छौं।
- LangChain4j फ्रेमवर्कले स्वचालित रूपमा व्यवस्थापन गर्दछ:
  - प्रयोगकर्ता प्रम्प्टहरूलाई आवश्यक पर्दा उपकरण कलमा रूपान्तरण गर्ने।
  - LLM को निर्णयको आधारमा उपयुक्त MCP उपकरणहरू कल गर्ने।
  - LLM र MCP सर्भर बीचको संवाद प्रवाह व्यवस्थापन गर्ने।
- `bot.chat()` विधिले MCP उपकरण कार्यान्वयनबाट परिणामहरू समावेश गर्न सक्ने प्राकृतिक भाषा प्रतिक्रियाहरू फर्काउँछ।
- यो दृष्टिकोणले प्रयोगकर्तालाई अन्तर्निहित MCP कार्यान्वयनको बारेमा जान्न आवश्यक छैन भन्ने सहज प्रयोगकर्ता अनुभव प्रदान गर्दछ।

पूर्ण कोड उदाहरण:

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

यहाँ मुख्य काम हुन्छ। हामी प्रारम्भिक प्रयोगकर्ता प्रम्प्टको साथ LLM कल गर्नेछौं, त्यसपछि प्रतिक्रिया प्रक्रिया गर्नेछौं कि कुनै उपकरणहरू कल गर्नुपर्नेछ कि छैन। यदि हो भने, हामी ती उपकरणहरू कल गर्नेछौं र अन्तिम प्रतिक्रिया प्राप्त नभएसम्म LLM सँग संवाद जारी राख्नेछौं।

हामी LLM लाई धेरै पटक कल गर्नेछौं, त्यसैले LLM कललाई व्यवस्थापन गर्ने कार्य परिभाषित गरौं। तपाईंको `main.rs` फाइलमा निम्न कार्य थप्नुहोस्:

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

यो कार्यले LLM क्लाइन्ट, सन्देशहरूको सूची (प्रयोगकर्ता प्रम्प्ट सहित), MCP सर्भरबाट उपकरणहरू लिन्छ, र LLM तर्फ अनुरोध पठाउँछ, प्रतिक्रिया फर्काउँछ।
LLM बाट प्रतिक्रिया `choices` को एक एरे समावेश गर्दछ। हामीले परिणामलाई प्रक्रिया गर्न आवश्यक छ कि कुनै `tool_calls` उपस्थित छन् कि छैनन्। यसले हामीलाई थाहा दिन्छ कि LLM ले विशेष उपकरणलाई तर्कसहित बोलाउन अनुरोध गरिरहेको छ। आफ्नो `main.rs` फाइलको अन्त्यमा निम्न कोड थप्नुहोस् जसले LLM प्रतिक्रिया ह्यान्डल गर्ने कार्य परिभाषित गर्दछ:

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

यदि `tool_calls` उपस्थित छन् भने, यो उपकरणको जानकारी निकाल्छ, MCP सर्भरलाई उपकरण अनुरोधसहित बोलाउँछ, र परिणामलाई संवाद सन्देशहरूमा थप्छ। त्यसपछि यो LLM सँग संवाद जारी राख्छ र सन्देशहरू सहायकको प्रतिक्रिया र उपकरण कल परिणामहरूसँग अद्यावधिक गरिन्छ।

MCP कलहरूको लागि LLM ले फर्काएको उपकरण कल जानकारी निकाल्न, हामी अर्को सहायक कार्य थप्नेछौं जसले कल गर्न आवश्यक सबै कुरा निकाल्छ। आफ्नो `main.rs` फाइलको अन्त्यमा निम्न कोड थप्नुहोस्:

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

सबै टुक्राहरू तयार भएपछि, हामी प्रारम्भिक प्रयोगकर्ता प्रम्प्ट ह्यान्डल गर्न र LLM बोलाउन सक्छौं। आफ्नो `main` कार्यलाई निम्न कोड समावेश गर्न अद्यावधिक गर्नुहोस्:

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

यसले दुई संख्याको योग सोध्ने प्रारम्भिक प्रयोगकर्ता प्रम्प्टसहित LLM सोध्छ, र उपकरण कलहरूलाई गतिशील रूपमा ह्यान्डल गर्न प्रतिक्रिया प्रक्रिया गर्दछ।

शानदार, तपाईंले यो पूरा गर्नुभयो!

## असाइनमेन्ट

अभ्यासबाट कोड लिई सर्भरलाई थप उपकरणहरूसहित निर्माण गर्नुहोस्। त्यसपछि अभ्यासमा जस्तै LLM सहित क्लाइन्ट बनाउनुहोस् र विभिन्न प्रम्प्टहरूसँग परीक्षण गर्नुहोस् ताकि तपाईंको सर्भर उपकरणहरू गतिशील रूपमा बोलाइन्छ। क्लाइन्ट निर्माण गर्ने यो तरिकाले अन्त प्रयोगकर्ताले उत्कृष्ट प्रयोगकर्ता अनुभव प्राप्त गर्नेछन् किनभने उनीहरूले प्रम्प्टहरू प्रयोग गर्न सक्नेछन्, सटीक क्लाइन्ट आदेशहरूको सट्टा, र कुनै पनि MCP सर्भर बोलाइएको छ भन्ने कुराबाट अनभिज्ञ हुनेछन्।

## समाधान

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## मुख्य सिकाइहरू

- आफ्नो क्लाइन्टमा LLM थप्दा MCP सर्भरहरूसँग अन्त प्रयोगकर्ताको अन्तरक्रिया गर्ने राम्रो तरिका प्रदान गर्दछ।
- तपाईंले MCP सर्भर प्रतिक्रियालाई LLM ले बुझ्न सक्ने केहीमा रूपान्तरण गर्न आवश्यक छ।

## नमूनाहरू

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## थप स्रोतहरू

## अब के गर्ने

- अगाडि: [Visual Studio Code प्रयोग गरेर सर्भर उपभोग गर्ने](../04-vscode/README.md)

---

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको छ। हामी यथार्थताको लागि प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छ। यसको मूल भाषा मा रहेको मूल दस्तावेज़लाई आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीको लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुनेछैनौं।