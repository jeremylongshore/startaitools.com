<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T13:58:27+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "mr"
}
-->
# LLM सह क्लायंट तयार करणे

आतापर्यंत, तुम्ही सर्व्हर आणि क्लायंट कसे तयार करायचे ते पाहिले आहे. क्लायंटने सर्व्हरला त्याची साधने, संसाधने आणि प्रॉम्प्ट्स स्पष्टपणे सूचीबद्ध करण्यासाठी कॉल करण्यास सक्षम केले आहे. तथापि, ही फारशी व्यावहारिक पद्धत नाही. तुमचा वापरकर्ता एजेंटिक युगात राहतो आणि प्रॉम्प्ट्स वापरण्याची आणि LLM शी संवाद साधण्याची अपेक्षा करतो. तुमच्या वापरकर्त्यासाठी, तुम्ही तुमच्या क्षमता साठवण्यासाठी MCP वापरता की नाही याची त्यांना पर्वा नाही, परंतु ते नैसर्गिक भाषेचा वापर करून संवाद साधण्याची अपेक्षा करतात. तर आपण हे कसे सोडवतो? उपाय म्हणजे क्लायंटमध्ये LLM जोडणे.

## विहंगावलोकन

या धड्यात आपण आपल्या क्लायंटमध्ये LLM जोडण्यावर लक्ष केंद्रित करू आणि हे तुमच्या वापरकर्त्यासाठी किती चांगला अनुभव प्रदान करते ते दाखवू.

## शिकण्याची उद्दिष्टे

या धड्याच्या शेवटी, तुम्ही हे करू शकता:

- LLM सह क्लायंट तयार करा.
- MCP सर्व्हरशी LLM वापरून सहजपणे संवाद साधा.
- क्लायंट साइडवर अंतिम वापरकर्ता अनुभव सुधारित करा.

## दृष्टिकोन

आपण कोणता दृष्टिकोन स्वीकारायचा आहे ते समजून घेण्याचा प्रयत्न करूया. LLM जोडणे सोपे वाटते, परंतु आपण प्रत्यक्षात हे कसे करू?

क्लायंट सर्व्हरशी खालीलप्रमाणे संवाद साधेल:

1. सर्व्हरशी कनेक्शन स्थापित करा.

1. क्षमता, प्रॉम्प्ट्स, संसाधने आणि साधने सूचीबद्ध करा आणि त्यांची स्कीमा सेव्ह करा.

1. LLM जोडा आणि सेव्ह केलेल्या क्षमता आणि त्यांची स्कीमा LLM ला समजणाऱ्या स्वरूपात पास करा.

1. वापरकर्ता प्रॉम्प्ट हाताळा, ते LLM ला पास करून क्लायंटने सूचीबद्ध केलेल्या साधनांसह.

छान, आता आपल्याला उच्च स्तरावर हे कसे करायचे ते समजले आहे, चला खालील व्यायामात हे करून पाहूया.

## व्यायाम: LLM सह क्लायंट तयार करणे

या व्यायामात, आपण आपल्या क्लायंटमध्ये LLM कसे जोडायचे ते शिकू.

### GitHub वैयक्तिक प्रवेश टोकन वापरून प्रमाणीकरण

GitHub टोकन तयार करणे सोपे आहे. हे कसे करायचे ते येथे आहे:

- GitHub सेटिंग्जवर जा – वरच्या उजव्या कोपर्यात तुमच्या प्रोफाइल चित्रावर क्लिक करा आणि सेटिंग्ज निवडा.
- डेव्हलपर सेटिंग्जवर जा – खाली स्क्रोल करा आणि डेव्हलपर सेटिंग्जवर क्लिक करा.
- वैयक्तिक प्रवेश टोकन निवडा – फाइन-ग्रेन्ड टोकनवर क्लिक करा आणि नवीन टोकन तयार करा.
- तुमचे टोकन कॉन्फिगर करा – संदर्भासाठी एक नोट जोडा, समाप्ती तारीख सेट करा आणि आवश्यक स्कोप्स (परवानग्या) निवडा. या प्रकरणात मॉडेल्स परवानगी जोडण्याची खात्री करा.
- टोकन तयार करा आणि कॉपी करा – टोकन तयार करा क्लिक करा आणि ते त्वरित कॉपी करा, कारण तुम्ही ते पुन्हा पाहू शकणार नाही.

### -1- सर्व्हरशी कनेक्ट करा

चला प्रथम आपला क्लायंट तयार करूया:

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

वरील कोडमध्ये आम्ही:

- आवश्यक लायब्ररी आयात केल्या आहेत.
- दोन सदस्यांसह एक वर्ग तयार केला आहे, `client` आणि `openai`, जे आम्हाला क्लायंट व्यवस्थापित करण्यात आणि LLM शी संवाद साधण्यात मदत करतील.
- `baseUrl` सेट करून GitHub Models वापरण्यासाठी आमच्या LLM उदाहरणाची कॉन्फिगर केली आहे.

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

वरील कोडमध्ये आम्ही:

- MCP साठी आवश्यक लायब्ररी आयात केल्या आहेत.
- क्लायंट तयार केला आहे.

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

प्रथम, तुम्हाला तुमच्या `pom.xml` फाइलमध्ये LangChain4j अवलंबित्व जोडणे आवश्यक आहे. MCP एकत्रीकरण आणि GitHub Models समर्थन सक्षम करण्यासाठी ही अवलंबित्व जोडा:

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

त्यानंतर तुमचा Java क्लायंट वर्ग तयार करा:

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

वरील कोडमध्ये आम्ही:

- **LangChain4j अवलंबित्व जोडले**: MCP एकत्रीकरण, OpenAI अधिकृत क्लायंट आणि GitHub Models समर्थनासाठी आवश्यक.
- **LangChain4j लायब्ररी आयात केल्या**: MCP एकत्रीकरण आणि OpenAI चॅट मॉडेल कार्यक्षमतेसाठी.
- **`ChatLanguageModel` तयार केले**: GitHub Models वापरण्यासाठी तुमच्या GitHub टोकनसह कॉन्फिगर केले.
- **HTTP ट्रान्सपोर्ट सेट केले**: MCP सर्व्हरशी कनेक्ट करण्यासाठी Server-Sent Events (SSE) वापरून.
- **MCP क्लायंट तयार केला**: जो सर्व्हरशी संवाद हाताळेल.
- **LangChain4j च्या अंगभूत MCP समर्थनाचा वापर केला**: जे LLM आणि MCP सर्व्हरमधील एकत्रीकरण सुलभ करते.

#### Rust

हा उदाहरण Rust आधारित MCP सर्व्हर चालू असल्याचे गृहीत धरतो. जर तुमच्याकडे एक नसेल, तर [01-first-server](../01-first-server/README.md) धड्याचा संदर्भ घ्या आणि सर्व्हर तयार करा.

तुमच्याकडे Rust MCP सर्व्हर असल्यावर, टर्मिनल उघडा आणि सर्व्हरसारख्या डिरेक्टरीमध्ये जा. नंतर नवीन LLM क्लायंट प्रकल्प तयार करण्यासाठी खालील आदेश चालवा:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

तुमच्या `Cargo.toml` फाइलमध्ये खालील अवलंबित्व जोडा:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> OpenAI साठी अधिकृत Rust लायब्ररी नाही, तथापि, `async-openai` क्रेट ही [समुदाय-देखरेख केलेली लायब्ररी](https://platform.openai.com/docs/libraries/rust#rust) आहे जी सामान्यतः वापरली जाते.

`src/main.rs` फाइल उघडा आणि त्यातील सामग्री खालील कोडने बदला:

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

हा कोड MCP सर्व्हर आणि GitHub Models शी LLM संवादासाठी कनेक्ट करणारा मूलभूत Rust अनुप्रयोग सेट करतो.

> [!IMPORTANT]
> अनुप्रयोग चालवण्यापूर्वी `OPENAI_API_KEY` पर्यावरणीय व्हेरिएबल तुमच्या GitHub टोकनसह सेट करण्याची खात्री करा.

छान, पुढील चरणासाठी, चला सर्व्हरवरील क्षमता सूचीबद्ध करूया.

### -2- सर्व्हर क्षमता सूचीबद्ध करा

आता आपण सर्व्हरशी कनेक्ट करू आणि त्याच्या क्षमता विचारू:

#### Typescript

त्याच वर्गात खालील पद्धती जोडा:

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

वरील कोडमध्ये आम्ही:

- सर्व्हरशी कनेक्ट होण्यासाठी कोड जोडले आहे, `connectToServer`.
- आमच्या अॅप फ्लो हाताळण्यासाठी जबाबदार `run` पद्धत तयार केली आहे. आतापर्यंत ते फक्त साधने सूचीबद्ध करते परंतु आम्ही लवकरच त्यात अधिक जोडू.

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

आम्ही काय जोडले आहे:

- संसाधने आणि साधने सूचीबद्ध केली आणि ती प्रिंट केली. साधनांसाठी आम्ही `inputSchema` देखील सूचीबद्ध करतो जे आम्ही नंतर वापरतो.

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

वरील कोडमध्ये आम्ही:

- MCP सर्व्हरवर उपलब्ध साधने सूचीबद्ध केली.
- प्रत्येक साधनासाठी, नाव, वर्णन आणि त्याची स्कीमा सूचीबद्ध केली. नंतर साधने कॉल करण्यासाठी आम्ही स्कीमा वापरणार आहोत.

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

वरील कोडमध्ये आम्ही:

- `McpToolProvider` तयार केला जो MCP सर्व्हरवरील सर्व साधने स्वयंचलितपणे शोधतो आणि नोंदवतो.
- टूल प्रदाता MCP टूल स्कीमा आणि LangChain4j च्या टूल स्वरूपामधील रूपांतरण अंतर्गत हाताळतो.
- हा दृष्टिकोन मॅन्युअल टूल सूचीबद्ध करणे आणि रूपांतरण प्रक्रिया दूर करतो.

#### Rust

MCP सर्व्हरकडून साधने मिळवणे `list_tools` पद्धती वापरून केले जाते. तुमच्या `main` फंक्शनमध्ये, MCP क्लायंट सेट केल्यानंतर, खालील कोड जोडा:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- सर्व्हर क्षमता LLM साधनांमध्ये रूपांतरित करा

सर्व्हर क्षमता सूचीबद्ध केल्यानंतर पुढील चरण म्हणजे त्यांना LLM ला समजणाऱ्या स्वरूपात रूपांतरित करणे. एकदा आपण ते केले की, आपण LLM ला ही क्षमता साधन म्हणून प्रदान करू शकतो.

#### TypeScript

1. MCP सर्व्हरकडून प्रतिसाद LLM ला वापरण्यासाठी टूल स्वरूपात रूपांतरित करण्यासाठी खालील कोड जोडा:

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

    वरील कोड MCP सर्व्हरकडून प्रतिसाद घेतो आणि LLM ला समजणाऱ्या टूल परिभाषा स्वरूपात रूपांतरित करतो.

1. पुढे, `run` पद्धत अपडेट करूया:

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

    वरील कोडमध्ये, आम्ही `run` पद्धत अपडेट केली आहे ज्यामध्ये परिणामांमधून मॅप केले जाते आणि प्रत्येक नोंदीसाठी `openAiToolAdapter` कॉल केला जातो.

#### Python

1. प्रथम, खालील कन्व्हर्टर फंक्शन तयार करूया:

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

    वरील `convert_to_llm_tools` फंक्शनमध्ये आम्ही MCP टूल प्रतिसाद घेतो आणि LLM ला समजणाऱ्या स्वरूपात रूपांतरित करतो.

1. पुढे, आमच्या क्लायंट कोडला या फंक्शनचा लाभ घेण्यासाठी अपडेट करूया:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    येथे, आम्ही MCP टूल प्रतिसाद LLM ला फीड करण्यासाठी काहीतरी रूपांतरित करण्यासाठी `convert_to_llm_tool` कॉल जोडत आहोत.

#### .NET

1. MCP टूल प्रतिसाद LLM ला समजणाऱ्या स्वरूपात रूपांतरित करण्यासाठी कोड जोडा:

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

वरील कोडमध्ये आम्ही:

- `ConvertFrom` नावाची फंक्शन तयार केली जी नाव, वर्णन आणि इनपुट स्कीमा घेते.
- FunctionDefinition तयार करण्याची कार्यक्षमता परिभाषित केली जी ChatCompletionsDefinition मध्ये पास केली जाते. हे LLM ला समजणारे काहीतरी आहे.

1. वरच्या फंक्शनचा फायदा घेण्यासाठी काही विद्यमान कोड कसे अपडेट करू शकतो ते पाहूया:

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

वरील कोडमध्ये आम्ही:

- नैसर्गिक भाषेच्या संवादासाठी एक सोपा `Bot` इंटरफेस परिभाषित केला.
- LangChain4j च्या `AiServices` चा वापर करून LLM MCP टूल प्रदात्यासह स्वयंचलितपणे बांधला.
- फ्रेमवर्क स्वयंचलितपणे टूल स्कीमा रूपांतरण आणि फंक्शन कॉलिंग हाताळते.
- MCP टूल्स LLM-सुसंगत स्वरूपात रूपांतरित करण्याची सर्व गुंतागुंत LangChain4j हाताळतो.

#### Rust

MCP टूल प्रतिसाद LLM ला समजणाऱ्या स्वरूपात रूपांतरित करण्यासाठी, आम्ही टूल्स लिस्टिंग स्वरूपित करणारा एक हेल्पर फंक्शन जोडू. MCP सर्व्हरकडून LLM ला विनंत्या करताना हे कॉल केले जाईल:

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

छान, आता आम्ही कोणत्याही वापरकर्ता विनंत्या हाताळण्यासाठी सेट केले आहे, त्यामुळे पुढील भागावर काम करूया.

### -4- वापरकर्ता प्रॉम्प्ट विनंती हाताळा

या कोडच्या भागात, आम्ही वापरकर्ता विनंत्या हाताळू.

#### TypeScript

1. आमच्या LLM ला कॉल करण्यासाठी वापरले जाणारे एक पद्धत जोडा:

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

    वरील कोडमध्ये आम्ही:

    - `callTools` नावाची पद्धत जोडली आहे.
    - पद्धत LLM प्रतिसाद घेते आणि तपासते की कोणती साधने कॉल केली गेली आहेत, जर काही असेल तर:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - LLM सूचित केल्यास टूल कॉल करते:

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

1. `run` पद्धत अपडेट करा:

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

छान, पूर्ण कोड सूचीबद्ध करूया:

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

1. LLM कॉल करण्यासाठी आवश्यक काही आयात जोडा:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. पुढे, LLM ला कॉल करणारे फंक्शन जोडा:

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

    वरील कोडमध्ये आम्ही:

    - MCP सर्व्हरवर सापडलेल्या आणि रूपांतरित केलेल्या फंक्शन्स LLM ला पास केल्या आहेत.
    - नंतर आम्ही LLM ला त्या फंक्शन्ससह कॉल केले आहे.
    - नंतर, आम्ही कोणते फंक्शन्स कॉल करायचे आहेत ते पाहण्यासाठी परिणाम तपासत आहोत.
    - शेवटी, आम्ही कॉल करण्यासाठी फंक्शन्सची यादी पास करतो.

1. अंतिम चरण, मुख्य कोड अपडेट करूया:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    तेथे, अंतिम चरण होता, वरील कोडमध्ये आम्ही:

    - MCP सर्व्हरवरील MCP टूल `call_tool` वापरून कॉल करत आहोत.
    - MCP सर्व्हरवरील टूल कॉलचा परिणाम प्रिंट करत आहोत.

#### .NET

1. LLM प्रॉम्प्ट विनंती करण्यासाठी कोड दाखवा:

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

    वरील कोडमध्ये आम्ही:

    - MCP सर्व्हरकडून साधने मिळवली आहेत, `var tools = await GetMcpTools()`.
    - वापरकर्ता प्रॉम्प्ट `userMessage` परिभाषित केला आहे.
    - मॉडेल आणि साधने निर्दिष्ट करणारा पर्याय ऑब्जेक्ट तयार केला आहे.
    - LLM कडे विनंती केली आहे.

1. शेवटचा चरण, LLM विचार करतो की आम्ही फंक्शन कॉल करावे का ते पाहूया:

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

    वरील कोडमध्ये आम्ही:

    - फंक्शन कॉल्सच्या यादीतून लूप केले आहे.
    - प्रत्येक टूल कॉलसाठी, नाव आणि युक्तिवाद बाहेर काढा आणि MCP क्लायंट वापरून MCP सर्व्हरवर टूल कॉल करा. शेवटी आम्ही परिणाम प्रिंट करतो.

पूर्ण कोड येथे आहे:

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

वरील कोडमध्ये आम्ही:

- साधनांच्या MCP सर्व्हरशी संवाद साधण्यासाठी सोप्या नैसर्गिक भाषेच्या प्रॉम्प्ट्सचा वापर केला आहे.
- LangChain4j फ्रेमवर्क स्वयंचलितपणे हाताळते:
  - वापरकर्ता प्रॉम्प्ट्सना आवश्यक असल्यास टूल कॉल्समध्ये रूपांतरित करणे.
  - LLM च्या निर्णयावर आधारित योग्य MCP साधने कॉल करणे.
  - LLM आणि MCP सर्व्हरमधील संभाषण प्रवाह व्यवस्थापित करणे.
- `bot.chat()` पद्धत नैसर्गिक भाषेतील प्रतिसाद परत करते ज्यामध्ये MCP टूल अंमलबजावणीचे परिणाम समाविष्ट असू शकतात.
- हा दृष्टिकोन अखंड वापरकर्ता अनुभव प्रदान करतो जिथे वापरकर्त्यांना अंतर्गत MCP अंमलबजावणीबद्दल माहिती असणे आवश्यक नाही.

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

येथे बहुतेक काम होते. आम्ही प्रारंभिक वापरकर्ता प्रॉम्प्टसह LLM ला कॉल करू, नंतर प्रतिसाद प्रक्रिया करू की कोणती साधने कॉल करायची आहेत का ते पाहू. जर तसे असेल तर, आम्ही ती साधने कॉल करू आणि अंतिम प्रतिसाद मिळेपर्यंत LLM सह संभाषण सुरू ठेवू.

आम्ही LLM ला अनेक कॉल करणार आहोत, त्यामुळे LLM कॉल हाताळणारा फंक्शन परिभाषित करूया. तुमच्या `main.rs` फाइलमध्ये खालील फंक्शन जोडा:

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

हा फंक्शन LLM क्लायंट, संदेशांची यादी (वापरकर्ता प्रॉम्प्टसह), MCP सर्व्हरवरील साधने घेतो आणि LLM ला विनंती पाठवतो आणि प्रतिसाद परत करतो.
LLM च्या प्रतिसादामध्ये `choices` नावाचा एक array असतो. आपल्याला परिणाम प्रक्रिया करावी लागेल आणि तपासावे लागेल की `tool_calls` उपस्थित आहेत का. यामुळे आपल्याला कळते की LLM विशिष्ट टूलला काही arguments सह कॉल करण्याची विनंती करत आहे. आपल्या `main.rs` फाइलच्या शेवटी खालील कोड जोडा, ज्यामुळे LLM प्रतिसाद हाताळण्यासाठी एक फंक्शन परिभाषित करता येईल:

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

जर `tool_calls` उपस्थित असतील, तर ते टूलची माहिती काढते, MCP सर्व्हरला टूल विनंतीसह कॉल करते आणि परिणाम संवादाच्या संदेशांमध्ये जोडते. त्यानंतर LLM सह संवाद सुरू ठेवते आणि संदेश सहाय्यकाच्या प्रतिसादासह आणि टूल कॉल परिणामांसह अद्यतनित केले जातात.

MCP कॉलसाठी LLM परताव्यातून टूल कॉल माहिती काढण्यासाठी, आम्ही आणखी एक हेल्पर फंक्शन जोडणार आहोत, जे कॉल करण्यासाठी आवश्यक सर्व गोष्टी काढेल. खालील कोड आपल्या `main.rs` फाइलच्या शेवटी जोडा:

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

सर्व घटक तयार झाल्यानंतर, आपण प्रारंभिक वापरकर्ता प्रॉम्प्ट हाताळू शकतो आणि LLM ला कॉल करू शकतो. आपल्या `main` फंक्शनमध्ये खालील कोड समाविष्ट करा:

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

हे LLM ला दोन संख्यांचा बेरीज विचारणारा प्रारंभिक वापरकर्ता प्रॉम्प्ट क्वेरी करेल आणि टूल कॉल्स गतिशीलपणे हाताळण्यासाठी प्रतिसाद प्रक्रिया करेल.

छान, तुम्ही पूर्ण केले!

## असाइनमेंट

व्यायामातील कोड वापरून सर्व्हर तयार करा आणि त्यामध्ये आणखी काही टूल्स जोडा. नंतर LLM सह एक क्लायंट तयार करा, जसे की व्यायामात दिले आहे, आणि वेगवेगळ्या प्रॉम्प्टसह चाचणी करा, जेणेकरून सर्व्हर टूल्स गतिशीलपणे कॉल केले जातील याची खात्री होईल. क्लायंट तयार करण्याचा हा मार्ग अंतिम वापरकर्त्याला उत्कृष्ट अनुभव देतो, कारण ते प्रॉम्प्ट्स वापरू शकतात आणि MCP सर्व्हर कॉल होत असल्याची जाणीव न ठेवता कार्य करू शकतात.

## समाधान

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## मुख्य मुद्दे

- आपल्या क्लायंटमध्ये LLM जोडल्याने MCP सर्व्हर्सशी संवाद साधण्याचा वापरकर्त्यांसाठी चांगला मार्ग उपलब्ध होतो.
- MCP सर्व्हर प्रतिसाद LLM ला समजण्यायोग्य स्वरूपात रूपांतरित करणे आवश्यक आहे.

## नमुने

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## अतिरिक्त संसाधने

## पुढे काय?

- पुढील: [Visual Studio Code वापरून सर्व्हर कसे वापरायचे](../04-vscode/README.md)

---

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी कृपया लक्षात ठेवा की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेचा अभाव असू शकतो. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून निर्माण होणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.