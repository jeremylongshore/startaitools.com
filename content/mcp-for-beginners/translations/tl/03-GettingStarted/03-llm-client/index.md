<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:56:05+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "tl"
}
-->
# Paglikha ng kliyente gamit ang LLM

Sa ngayon, nakita mo kung paano gumawa ng server at kliyente. Ang kliyente ay nagawang tawagan ang server nang direkta upang ilista ang mga tool, resources, at mga prompt nito. Gayunpaman, hindi ito masyadong praktikal na paraan. Ang iyong user ay nabubuhay sa agentic era at inaasahan na gumamit ng mga prompt at makipag-usap sa isang LLM upang magawa ito. Para sa iyong user, hindi mahalaga kung gumagamit ka ng MCP o hindi upang i-store ang iyong mga kakayahan, ngunit inaasahan nilang gumamit ng natural na wika para makipag-ugnayan. Paano natin ito masosolusyunan? Ang solusyon ay ang pagdaragdag ng LLM sa kliyente.

## Pangkalahatang-ideya

Sa araling ito, magtutuon tayo sa pagdaragdag ng LLM sa iyong kliyente at ipapakita kung paano ito nagbibigay ng mas mahusay na karanasan para sa iyong user.

## Mga Layunin sa Pag-aaral

Sa pagtatapos ng araling ito, magagawa mo ang:

- Gumawa ng kliyente na may LLM.
- Walang kahirap-hirap na makipag-ugnayan sa MCP server gamit ang LLM.
- Magbigay ng mas mahusay na karanasan para sa end user sa panig ng kliyente.

## Paraan

Subukan nating unawain ang paraan na kailangan nating gawin. Ang pagdaragdag ng LLM ay mukhang simple, ngunit paano natin ito aktwal na gagawin?

Ganito makikipag-ugnayan ang kliyente sa server:

1. Magtatag ng koneksyon sa server.

1. Ilista ang mga kakayahan, prompt, resources, at mga tool, at i-save ang kanilang schema.

1. Magdagdag ng LLM at ipasa ang mga na-save na kakayahan at ang kanilang schema sa format na naiintindihan ng LLM.

1. Pangasiwaan ang user prompt sa pamamagitan ng pagpasa nito sa LLM kasama ang mga tool na nakalista ng kliyente.

Magaling, ngayon naiintindihan natin kung paano natin ito magagawa sa mataas na antas, subukan natin ito sa ibaba ng ehersisyo.

## Ehersisyo: Paglikha ng kliyente gamit ang LLM

Sa ehersisyong ito, matututo tayong magdagdag ng LLM sa ating kliyente.

### Pag-authenticate gamit ang GitHub Personal Access Token

Ang paggawa ng GitHub token ay isang simpleng proseso. Narito kung paano mo ito magagawa:

- Pumunta sa GitHub Settings – I-click ang iyong profile picture sa kanang itaas na sulok at piliin ang Settings.
- Mag-navigate sa Developer Settings – Mag-scroll pababa at i-click ang Developer Settings.
- Piliin ang Personal Access Tokens – I-click ang Fine-grained tokens at pagkatapos ay Generate new token.
- I-configure ang Iyong Token – Magdagdag ng tala para sa reference, magtakda ng expiration date, at piliin ang mga kinakailangang scope (mga pahintulot). Sa kasong ito, siguraduhing idagdag ang Models permission.
- I-generate at Kopyahin ang Token – I-click ang Generate token, at siguraduhing kopyahin ito kaagad, dahil hindi mo na ito makikita muli.

### -1- Kumonekta sa server

Gumawa muna tayo ng kliyente:

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

Sa nakaraang code, ginawa natin ang:

- Pag-import ng mga kinakailangang library
- Gumawa ng klase na may dalawang miyembro, `client` at `openai` na tutulong sa atin na pamahalaan ang kliyente at makipag-ugnayan sa isang LLM.
- I-configure ang ating LLM instance upang gumamit ng GitHub Models sa pamamagitan ng pagtatakda ng `baseUrl` upang ituro sa inference API.

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

Sa nakaraang code, ginawa natin ang:

- Pag-import ng mga kinakailangang library para sa MCP
- Gumawa ng kliyente

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

Una, kakailanganin mong idagdag ang LangChain4j dependencies sa iyong `pom.xml` file. Idagdag ang mga dependencies na ito upang paganahin ang MCP integration at suporta sa GitHub Models:

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

Pagkatapos ay gumawa ng iyong Java client class:

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

Sa nakaraang code, ginawa natin ang:

- **Pagdagdag ng LangChain4j dependencies**: Kinakailangan para sa MCP integration, OpenAI official client, at suporta sa GitHub Models
- **Pag-import ng LangChain4j libraries**: Para sa MCP integration at OpenAI chat model functionality
- **Paglikha ng `ChatLanguageModel`**: I-configure upang gumamit ng GitHub Models gamit ang iyong GitHub token
- **Pag-set up ng HTTP transport**: Gamit ang Server-Sent Events (SSE) upang kumonekta sa MCP server
- **Paglikha ng MCP client**: Na hahawak sa komunikasyon sa server
- **Paggamit ng built-in MCP support ng LangChain4j**: Na nagpapadali sa integration sa pagitan ng LLMs at MCP servers

#### Rust

Ang halimbawang ito ay nagpapalagay na mayroon kang Rust-based MCP server na tumatakbo. Kung wala ka nito, bumalik sa [01-first-server](../01-first-server/README.md) na aralin upang gumawa ng server.

Kapag mayroon ka nang Rust MCP server, buksan ang terminal at mag-navigate sa parehong direktoryo ng server. Pagkatapos ay patakbuhin ang sumusunod na command upang gumawa ng bagong LLM client project:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Idagdag ang mga sumusunod na dependencies sa iyong `Cargo.toml` file:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Walang opisyal na Rust library para sa OpenAI, gayunpaman, ang `async-openai` crate ay isang [community maintained library](https://platform.openai.com/docs/libraries/rust#rust) na karaniwang ginagamit.

Buksan ang `src/main.rs` file at palitan ang nilalaman nito ng sumusunod na code:

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

Ang code na ito ay nagse-set up ng basic Rust application na kokonekta sa MCP server at GitHub Models para sa LLM interactions.

> [!IMPORTANT]
> Siguraduhing itakda ang `OPENAI_API_KEY` environment variable gamit ang iyong GitHub token bago patakbuhin ang application.

Magaling, para sa susunod na hakbang, ilista natin ang mga kakayahan sa server.

### -2- Ilista ang mga kakayahan ng server

Ngayon ay kokonekta tayo sa server at hihilingin ang mga kakayahan nito:

#### Typescript

Sa parehong klase, idagdag ang sumusunod na mga method:

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

Sa nakaraang code, ginawa natin ang:

- Idinagdag ang code para sa pagkonekta sa server, `connectToServer`.
- Gumawa ng `run` method na responsable para sa paghawak ng daloy ng ating app. Sa ngayon, inililista lamang nito ang mga tool ngunit magdadagdag pa tayo dito sa lalong madaling panahon.

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

Narito ang mga idinagdag natin:

- Paglista ng mga resources at tool at pag-print ng mga ito. Para sa mga tool, inilista rin natin ang `inputSchema` na gagamitin natin mamaya.

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

Sa nakaraang code, ginawa natin ang:

- Paglista ng mga tool na available sa MCP Server
- Para sa bawat tool, inilista ang pangalan, deskripsyon, at ang schema nito. Ang huli ay isang bagay na gagamitin natin upang tawagan ang mga tool sa lalong madaling panahon.

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

Sa nakaraang code, ginawa natin ang:

- Gumawa ng `McpToolProvider` na awtomatikong nagdi-discover at nagre-rehistro ng lahat ng tool mula sa MCP server
- Ang tool provider ay humahawak sa conversion sa pagitan ng MCP tool schemas at LangChain4j's tool format internally
- Ang approach na ito ay nag-a-abstract sa manual tool listing at conversion process

#### Rust

Ang pagkuha ng mga tool mula sa MCP server ay ginagawa gamit ang `list_tools` method. Sa iyong `main` function, pagkatapos i-set up ang MCP client, idagdag ang sumusunod na code:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- I-convert ang mga kakayahan ng server sa LLM tools

Ang susunod na hakbang pagkatapos ilista ang mga kakayahan ng server ay i-convert ang mga ito sa format na naiintindihan ng LLM. Kapag nagawa natin ito, maibibigay natin ang mga kakayahan bilang mga tool sa ating LLM.

#### TypeScript

1. Idagdag ang sumusunod na code upang i-convert ang response mula sa MCP Server sa tool format na magagamit ng LLM:

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

    Ang code sa itaas ay kumukuha ng response mula sa MCP Server at kino-convert ito sa tool definition format na naiintindihan ng LLM.

1. I-update ang `run` method upang ilista ang mga kakayahan ng server:

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

    Sa nakaraang code, in-update natin ang `run` method upang i-map ang resulta at para sa bawat entry ay tawagan ang `openAiToolAdapter`.

#### Python

1. Una, gumawa ng sumusunod na converter function:

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

    Sa function sa itaas na `convert_to_llm_tools`, kinukuha natin ang MCP tool response at kino-convert ito sa format na naiintindihan ng LLM.

1. Susunod, i-update ang ating client code upang magamit ang function na ito tulad ng sumusunod:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Dito, nagdagdag tayo ng tawag sa `convert_to_llm_tool` upang i-convert ang MCP tool response sa isang bagay na maipapakain natin sa LLM mamaya.

#### .NET

1. Magdagdag ng code upang i-convert ang MCP tool response sa isang bagay na naiintindihan ng LLM:

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

Sa nakaraang code, ginawa natin ang:

- Gumawa ng function na `ConvertFrom` na kumukuha ng pangalan, deskripsyon, at input schema.
- Nag-defina ng functionality na gumagawa ng FunctionDefinition na ipinapasa sa ChatCompletionsDefinition. Ang huli ay isang bagay na naiintindihan ng LLM.

1. Tingnan kung paano natin ma-update ang ilang umiiral na code upang magamit ang function sa itaas:

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

Sa nakaraang code, ginawa natin ang:

- Nag-defina ng simpleng `Bot` interface para sa natural language interactions
- Ginamit ang LangChain4j's `AiServices` upang awtomatikong i-bind ang LLM sa MCP tool provider
- Ang framework ay awtomatikong humahawak sa tool schema conversion at function calling sa likod ng eksena
- Ang approach na ito ay nag-aalis ng manual tool conversion - LangChain4j ang humahawak sa lahat ng complexity ng pag-convert ng MCP tools sa LLM-compatible format

#### Rust

Upang i-convert ang MCP tool response sa format na naiintindihan ng LLM, magdagdag tayo ng helper function na nagfo-format ng tools listing. Idagdag ang sumusunod na code sa iyong `main.rs` file sa ibaba ng `main` function. Tatawagin ito kapag gumagawa ng mga request sa LLM:

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

Magaling, handa na tayo upang pangasiwaan ang anumang user requests, kaya't harapin natin iyon sa susunod.

### -4- Pangasiwaan ang user prompt request

Sa bahaging ito ng code, hahawakan natin ang mga user requests.

#### TypeScript

1. Magdagdag ng method na gagamitin upang tawagan ang ating LLM:

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

    Sa nakaraang code, ginawa natin ang:

    - Nagdagdag ng method na `callTools`.
    - Ang method ay kumukuha ng LLM response at tinitingnan kung anong mga tool ang tinawag, kung mayroon:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Tumatawag ng tool, kung ipinahiwatig ng LLM na dapat itong tawagan:

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

1. I-update ang `run` method upang isama ang mga tawag sa LLM at tawagan ang `callTools`:

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

Magaling, ilista natin ang code nang buo:

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

1. Magdagdag ng ilang imports na kinakailangan upang tawagan ang LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Susunod, magdagdag ng function na tatawag sa LLM:

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

    Sa nakaraang code, ginawa natin ang:

    - Ipinasa ang ating mga function, na natagpuan sa MCP server at na-convert, sa LLM.
    - Pagkatapos ay tinawag ang LLM gamit ang mga nasabing function.
    - Pagkatapos, iniinspeksyon ang resulta upang makita kung anong mga function ang dapat tawagan, kung mayroon.
    - Sa wakas, ipinapasa ang array ng mga function upang tawagan.

1. Huling hakbang, i-update ang ating pangunahing code:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Doon, iyon ang huling hakbang, sa code sa itaas, ginawa natin ang:

    - Pagtawag sa MCP tool sa pamamagitan ng `call_tool` gamit ang function na sa tingin ng LLM ay dapat tawagan batay sa ating prompt.
    - Pag-print ng resulta ng tool call sa MCP Server.

#### .NET

1. Ipakita ang ilang code para sa paggawa ng LLM prompt request:

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

    Sa nakaraang code, ginawa natin ang:

    - Kinuha ang mga tool mula sa MCP server, `var tools = await GetMcpTools()`.
    - Nag-defina ng user prompt `userMessage`.
    - Gumawa ng options object na tumutukoy sa model at tools.
    - Gumawa ng request patungo sa LLM.

1. Isang huling hakbang, tingnan kung sa tingin ng LLM ay dapat tawagan ang isang function:

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

    Sa nakaraang code, ginawa natin ang:

    - Nag-loop sa listahan ng function calls.
    - Para sa bawat tool call, i-parse ang pangalan at mga argumento at tawagan ang tool sa MCP server gamit ang MCP client. Sa wakas, i-print ang mga resulta.

Narito ang code nang buo:

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

Sa nakaraang code, ginawa natin ang:

- Gumamit ng simpleng natural language prompts upang makipag-ugnayan sa MCP server tools
- Ang LangChain4j framework ay awtomatikong humahawak sa:
  - Pag-convert ng user prompts sa tool calls kapag kinakailangan
  - Pagtawag sa naaangkop na MCP tools batay sa desisyon ng LLM
  - Pamamahala sa daloy ng pag-uusap sa pagitan ng LLM at MCP server
- Ang `bot.chat()` method ay nagbabalik ng natural language responses na maaaring kasama ang mga resulta mula sa MCP tool executions
- Ang approach na ito ay nagbibigay ng seamless user experience kung saan hindi kailangang malaman ng mga user ang tungkol sa underlying MCP implementation

Kumpletong halimbawa ng code:

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

Dito nagaganap ang karamihan ng trabaho. Tatawagin natin ang LLM gamit ang initial user prompt, pagkatapos ay iproseso ang response upang makita kung may mga tool na kailangang tawagan. Kung mayroon, tatawagin natin ang mga tool na iyon at ipagpapatuloy ang pag-uusap sa LLM hanggang sa walang tool calls na kailangan at mayroon na tayong final response.

Gagawa tayo ng maraming tawag sa LLM, kaya't mag-define tayo ng function na hahawak sa LLM call. Idagdag ang sumusunod na function sa iyong `main.rs` file:

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

Ang function na ito ay kumukuha ng LLM client, listahan ng mga mensahe (kasama ang user prompt), mga tool mula sa MCP server, at nagpapadala ng request sa LLM, na nagbabalik ng response.
Ang tugon mula sa LLM ay maglalaman ng isang array ng `choices`. Kailangan nating iproseso ang resulta upang makita kung mayroong anumang `tool_calls`. Ipinapakita nito na ang LLM ay humihiling na tawagin ang isang partikular na tool gamit ang mga argumento. Idagdag ang sumusunod na code sa ibaba ng iyong `main.rs` file upang magtakda ng isang function na hahawak sa tugon ng LLM:

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

Kung mayroong `tool_calls`, kukunin nito ang impormasyon ng tool, tatawagin ang MCP server gamit ang kahilingan ng tool, at idadagdag ang mga resulta sa mga mensahe ng pag-uusap. Pagkatapos, ipagpapatuloy nito ang pag-uusap sa LLM at ang mga mensahe ay maa-update gamit ang tugon ng assistant at mga resulta ng tool call.

Upang makuha ang impormasyon ng tool call na ibinabalik ng LLM para sa mga tawag sa MCP, magdaragdag tayo ng isa pang helper function upang makuha ang lahat ng kinakailangan para sa tawag. Idagdag ang sumusunod na code sa ibaba ng iyong `main.rs` file:

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

Sa lahat ng mga piraso na nasa lugar na, maaari na nating hawakan ang paunang prompt ng user at tawagin ang LLM. I-update ang iyong `main` function upang isama ang sumusunod na code:

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

Ito ay magtatanong sa LLM gamit ang paunang prompt ng user na humihiling ng kabuuan ng dalawang numero, at ipoproseso nito ang tugon upang dinamikong hawakan ang mga tool calls.

Magaling, nagawa mo na!

## Takdang-Aralin

Kunin ang code mula sa ehersisyo at buuin ang server na may mas maraming tools. Pagkatapos, gumawa ng isang client na may LLM, tulad ng sa ehersisyo, at subukan ito gamit ang iba't ibang mga prompt upang matiyak na lahat ng iyong mga server tools ay tinatawag nang dinamikal. Ang ganitong paraan ng paggawa ng client ay nagbibigay ng mahusay na karanasan sa user dahil magagamit nila ang mga prompt, sa halip na eksaktong mga command ng client, at hindi nila kailangang malaman na may tinatawag na MCP server.

## Solusyon

[Solusyon](/03-GettingStarted/03-llm-client/solution/README.md)

## Mahahalagang Aral

- Ang pagdaragdag ng LLM sa iyong client ay nagbibigay ng mas mahusay na paraan para makipag-ugnayan ang mga user sa MCP Servers.
- Kailangan mong i-convert ang tugon ng MCP Server sa isang bagay na maiintindihan ng LLM.

## Mga Halimbawa

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## Karagdagang Mga Mapagkukunan

## Ano'ng Susunod

- Susunod: [Pagkonsumo ng server gamit ang Visual Studio Code](../04-vscode/README.md)

---

**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't sinisikap naming maging tumpak, mangyaring tandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa kanyang katutubong wika ang dapat ituring na opisyal na sanggunian. Para sa mahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na dulot ng paggamit ng pagsasaling ito.