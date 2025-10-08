<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:59:11+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "sw"
}
-->
# Kuunda Mteja na LLM

Hadi sasa, umejifunza jinsi ya kuunda seva na mteja. Mteja amekuwa na uwezo wa kuwasiliana na seva moja kwa moja ili kuorodhesha zana, rasilimali, na maelekezo yake. Hata hivyo, njia hii si ya vitendo sana. Mtumiaji wako anaishi katika enzi ya mawakala na anatarajia kutumia maelekezo na kuwasiliana na LLM kufanya hivyo. Kwa mtumiaji wako, haijalishi kama unatumia MCP kuhifadhi uwezo wako au la, lakini wanatarajia kutumia lugha ya kawaida kuingiliana. Je, tunatatua hili vipi? Suluhisho ni kuongeza LLM kwa mteja.

## Muhtasari

Katika somo hili tunazingatia kuongeza LLM kwa mteja wako na kuonyesha jinsi hii inavyotoa uzoefu bora kwa mtumiaji wako.

## Malengo ya Kujifunza

Mwisho wa somo hili, utaweza:

- Kuunda mteja na LLM.
- Kuingiliana bila matatizo na seva ya MCP kwa kutumia LLM.
- Kutoa uzoefu bora kwa mtumiaji wa mwisho upande wa mteja.

## Njia

Hebu tujaribu kuelewa njia tunayotakiwa kuchukua. Kuongeza LLM kunaonekana rahisi, lakini je, tutafanya hivyo kwa kweli?

Hivi ndivyo mteja atakavyowasiliana na seva:

1. Kuanzisha muunganisho na seva.

1. Kuorodhesha uwezo, maelekezo, rasilimali, na zana, na kuhifadhi muundo wake.

1. Kuongeza LLM na kupitisha uwezo uliohifadhiwa na muundo wake katika fomati ambayo LLM inaelewa.

1. Kushughulikia maelekezo ya mtumiaji kwa kuyapitisha kwa LLM pamoja na zana zilizoorodheshwa na mteja.

Vizuri, sasa tunaelewa jinsi tunavyoweza kufanya hili kwa kiwango cha juu, hebu tujaribu katika zoezi lililo hapa chini.

## Zoezi: Kuunda mteja na LLM

Katika zoezi hili, tutajifunza jinsi ya kuongeza LLM kwa mteja wetu.

### Uthibitishaji kwa kutumia GitHub Personal Access Token

Kuunda tokeni ya GitHub ni mchakato rahisi. Hivi ndivyo unavyoweza kufanya:

- Nenda kwenye Mipangilio ya GitHub – Bofya kwenye picha yako ya wasifu kwenye kona ya juu kulia na uchague Mipangilio.
- Tembea hadi Mipangilio ya Wasanidi – Shuka chini na bofya Mipangilio ya Wasanidi.
- Chagua Personal Access Tokens – Bofya kwenye Fine-grained tokens kisha Generate new token.
- Sanidi Tokeni Yako – Ongeza maelezo kwa kumbukumbu, weka tarehe ya kumalizika muda, na uchague mawanda muhimu (ruhusa). Katika kesi hii hakikisha umeongeza ruhusa ya Models.
- Tengeneza na Nakili Tokeni – Bofya Generate token, na hakikisha unainakili mara moja, kwani hautaweza kuiona tena.

### -1- Unganisha na seva

Hebu tuunde mteja wetu kwanza:

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

Katika msimbo uliotangulia tumefanya:

- Kuingiza maktaba zinazohitajika.
- Kuunda darasa lenye wanachama wawili, `client` na `openai` ambao watatusaidia kusimamia mteja na kuingiliana na LLM.
- Kuseti mfano wa LLM kutumia GitHub Models kwa kuweka `baseUrl` kuelekeza kwenye API ya inference.

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

Katika msimbo uliotangulia tumefanya:

- Kuingiza maktaba zinazohitajika kwa MCP.
- Kuunda mteja.

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

Kwanza, utahitaji kuongeza utegemezi wa LangChain4j kwenye faili yako ya `pom.xml`. Ongeza utegemezi huu kuwezesha ujumuishaji wa MCP na msaada wa GitHub Models:

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

Kisha unda darasa lako la mteja wa Java:

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

Katika msimbo uliotangulia tumefanya:

- **Kuongeza utegemezi wa LangChain4j**: Zinazohitajika kwa ujumuishaji wa MCP, mteja rasmi wa OpenAI, na msaada wa GitHub Models.
- **Kuingiza maktaba za LangChain4j**: Kwa ujumuishaji wa MCP na utendaji wa modeli ya mazungumzo ya OpenAI.
- **Kuunda `ChatLanguageModel`**: Kuseti kutumia GitHub Models na tokeni yako ya GitHub.
- **Kuseti usafirishaji wa HTTP**: Kutumia Server-Sent Events (SSE) kuunganishwa na seva ya MCP.
- **Kuunda mteja wa MCP**: Ambaye atashughulikia mawasiliano na seva.
- **Kutumia msaada wa MCP wa LangChain4j**: Ambayo inarahisisha ujumuishaji kati ya LLMs na seva za MCP.

#### Rust

Mfano huu unadhani una seva ya MCP inayotumia Rust. Ikiwa huna, rejelea somo la [01-first-server](../01-first-server/README.md) kuunda seva.

Mara tu unapokuwa na seva yako ya MCP inayotumia Rust, fungua terminal na nenda kwenye saraka sawa na seva. Kisha endesha amri ifuatayo kuunda mradi mpya wa mteja wa LLM:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Ongeza utegemezi ufuatao kwenye faili yako ya `Cargo.toml`:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Hakuna maktaba rasmi ya Rust kwa OpenAI, hata hivyo, `async-openai` ni [maktaba inayosimamiwa na jamii](https://platform.openai.com/docs/libraries/rust#rust) ambayo hutumika mara kwa mara.

Fungua faili ya `src/main.rs` na badilisha maudhui yake na msimbo ufuatao:

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

Msimbo huu unaseti programu ya msingi ya Rust ambayo itaunganishwa na seva ya MCP na GitHub Models kwa mwingiliano wa LLM.

> [!IMPORTANT]
> Hakikisha umeweka kigezo cha mazingira `OPENAI_API_KEY` na tokeni yako ya GitHub kabla ya kuendesha programu.

Vizuri, kwa hatua yetu inayofuata, hebu tuorodheshe uwezo kwenye seva.

### -2- Orodhesha uwezo wa seva

Sasa tutaunganishwa na seva na kuuliza kuhusu uwezo wake:

#### TypeScript

Katika darasa lile lile, ongeza mbinu zifuatazo:

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

Katika msimbo uliotangulia tumefanya:

- Kuongeza msimbo wa kuunganishwa na seva, `connectToServer`.
- Kuunda mbinu ya `run` inayohusika na mtiririko wa programu yetu. Hadi sasa inaorodhesha zana tu lakini tutaongeza zaidi hivi karibuni.

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

Hivi ndivyo tulivyoongeza:

- Kuorodhesha rasilimali na zana na kuzichapisha. Kwa zana pia tunaorodhesha `inputSchema` ambayo tutatumia baadaye.

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

Katika msimbo uliotangulia tumefanya:

- Kuorodhesha zana zinazopatikana kwenye seva ya MCP.
- Kwa kila zana, kuorodhesha jina, maelezo, na muundo wake. Muundo huu ni kitu ambacho tutatumia kuita zana hivi karibuni.

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

Katika msimbo uliotangulia tumefanya:

- Kuunda `McpToolProvider` ambayo hugundua na kusajili zana zote kutoka seva ya MCP moja kwa moja.
- Mtoa zana hushughulikia ubadilishaji kati ya miundo ya zana za MCP na fomati ya zana ya LangChain4j ndani.
- Njia hii inaficha mchakato wa kuorodhesha zana na ubadilishaji wa mwongozo.

#### Rust

Kupata zana kutoka seva ya MCP kunafanywa kwa kutumia mbinu ya `list_tools`. Katika kazi yako ya `main`, baada ya kuseti mteja wa MCP, ongeza msimbo ufuatao:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Badilisha uwezo wa seva kuwa zana za LLM

Hatua inayofuata baada ya kuorodhesha uwezo wa seva ni kuubadilisha kuwa fomati ambayo LLM inaelewa. Mara tu tunapofanya hivyo, tunaweza kutoa uwezo huu kama zana kwa LLM.

#### TypeScript

1. Ongeza msimbo ufuatao kubadilisha majibu kutoka seva ya MCP kuwa fomati ya zana ambayo LLM inaweza kutumia:

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

    Msimbo hapo juu unachukua majibu kutoka seva ya MCP na kuyabadilisha kuwa ufafanuzi wa zana ambayo LLM inaweza kuelewa.

1. Hebu tusasishe mbinu ya `run` ili kuorodhesha uwezo wa seva:

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

    Katika msimbo uliotangulia, tumesasisha mbinu ya `run` ili kupitia matokeo na kwa kila kipengele kuita `openAiToolAdapter`.

#### Python

1. Kwanza, hebu tuunde kazi ya kubadilisha ifuatayo:

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

    Katika kazi hapo juu `convert_to_llm_tools` tunachukua majibu ya zana ya MCP na kuyabadilisha kuwa fomati ambayo LLM inaweza kuelewa.

1. Kisha, hebu tusasishe msimbo wa mteja wetu kutumia kazi hii kama ifuatavyo:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Hapa, tunaongeza mwito kwa `convert_to_llm_tool` kubadilisha majibu ya zana ya MCP kuwa kitu ambacho tunaweza kulisha LLM baadaye.

#### .NET

1. Hebu tuongeze msimbo wa kubadilisha majibu ya zana ya MCP kuwa kitu ambacho LLM inaweza kuelewa:

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

Katika msimbo uliotangulia tumefanya:

- Kuunda kazi `ConvertFrom` inayochukua jina, maelezo, na muundo wa pembejeo.
- Kufafanua utendaji unaounda FunctionDefinition ambayo inapita kwa ChatCompletionsDefinition. Hii ni kitu ambacho LLM inaweza kuelewa.

1. Hebu tuone jinsi tunavyoweza kusasisha msimbo uliopo kutumia kazi hii hapo juu:

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

Katika msimbo uliotangulia tumefanya:

- Kufafanua kiolesura rahisi cha `Bot` kwa mwingiliano wa lugha ya kawaida.
- Kutumia `AiServices` ya LangChain4j kuunganisha LLM na mtoa zana wa MCP moja kwa moja.
- Mfumo hushughulikia ubadilishaji wa muundo wa zana na mwito wa kazi kwa nyuma.
- Njia hii inafuta ubadilishaji wa zana wa mwongozo - LangChain4j hushughulikia ugumu wote wa kubadilisha zana za MCP kuwa fomati inayolingana na LLM.

#### Rust

Kubadilisha majibu ya zana ya MCP kuwa fomati ambayo LLM inaweza kuelewa, tutaongeza kazi ya kusaidia inayofomati orodha ya zana. Ongeza msimbo ufuatao kwenye faili yako ya `main.rs` chini ya kazi ya `main`. Hii itaitwa wakati wa kufanya maombi kwa LLM:

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

Vizuri, sasa tumejiandaa kushughulikia maombi yoyote ya mtumiaji, kwa hivyo hebu tushughulikie hilo.

### -4- Shughulikia maombi ya maelekezo ya mtumiaji

Katika sehemu hii ya msimbo, tutashughulikia maombi ya mtumiaji.

#### TypeScript

1. Ongeza mbinu ambayo itatumika kuita LLM:

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

    Katika msimbo uliotangulia tumefanya:

    - Kuongeza mbinu `callTools`.
    - Mbinu inachukua majibu ya LLM na kuangalia kuona ni zana gani zimeitwa, ikiwa zipo:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Inaita zana, ikiwa LLM inaonyesha inapaswa kuitwa:

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

1. Sasisha mbinu ya `run` ili kujumuisha miito kwa LLM na kuita `callTools`:

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

Vizuri, hebu tuorodheshe msimbo wote:

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

1. Hebu tuongeze baadhi ya uingizaji unaohitajika kuita LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Kisha, hebu tuongeze kazi ambayo itaita LLM:

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

    Katika msimbo uliotangulia tumefanya:

    - Kupitisha kazi zetu, ambazo tulipata kwenye seva ya MCP na kuzibadilisha, kwa LLM.
    - Kisha tuliiita LLM na kazi hizo.
    - Kisha, tunachunguza matokeo kuona ni kazi gani tunapaswa kuita, ikiwa zipo.
    - Hatimaye, tunapita safu ya kazi za kuita.

1. Hatua ya mwisho, hebu tusasishe msimbo wetu mkuu:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Hapo, hiyo ilikuwa hatua ya mwisho, katika msimbo hapo juu tunafanya:

    - Kuita zana ya MCP kupitia `call_tool` kwa kutumia kazi ambayo LLM ilifikiri tunapaswa kuita kulingana na maelekezo yetu.
    - Kuchapisha matokeo ya mwito wa zana kwa seva ya MCP.

#### .NET

1. Hebu tuonyeshe msimbo wa kufanya maombi ya maelekezo ya LLM:

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

    Katika msimbo uliotangulia tumefanya:

    - Kupata zana kutoka seva ya MCP, `var tools = await GetMcpTools()`.
    - Kufafanua maelekezo ya mtumiaji `userMessage`.
    - Kuunda chaguo la chaguo linaloeleza modeli na zana.
    - Kufanya maombi kwa LLM.

1. Hatua moja ya mwisho, hebu tuone kama LLM inafikiri tunapaswa kuita kazi:

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

    Katika msimbo uliotangulia tumefanya:

    - Kupitia orodha ya miito ya kazi.
    - Kwa kila mwito wa zana, kuchambua jina na hoja na kuita zana kwenye seva ya MCP kwa kutumia mteja wa MCP. Hatimaye tunachapisha matokeo.

Huu hapa msimbo wote:

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

Katika msimbo uliotangulia tumefanya:

- Kutumia maelekezo rahisi ya lugha ya kawaida kuingiliana na zana za seva ya MCP.
- Mfumo wa LangChain4j hushughulikia moja kwa moja:
  - Kubadilisha maelekezo ya mtumiaji kuwa miito ya zana inapohitajika.
  - Kuita zana sahihi za MCP kulingana na uamuzi wa LLM.
  - Kusimamia mtiririko wa mazungumzo kati ya LLM na seva ya MCP.
- Mbinu ya `bot.chat()` inarudisha majibu ya lugha ya kawaida ambayo yanaweza kujumuisha matokeo kutoka kwa utekelezaji wa zana za MCP.
- Njia hii inatoa uzoefu wa mtumiaji bila matatizo ambapo watumiaji hawahitaji kujua kuhusu utekelezaji wa MCP wa msingi.

Mfano kamili wa msimbo:

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

Hapa ndipo kazi kubwa inafanyika. Tutaita LLM na maelekezo ya awali ya mtumiaji, kisha kuchakata majibu kuona kama kuna zana zinazohitaji kuitwa. Ikiwa zipo, tutaita zana hizo na kuendelea na mazungumzo na LLM hadi hakuna miito zaidi ya zana inayohitajika na tunapata jibu la mwisho.

Tutafanya miito mingi kwa LLM, kwa hivyo hebu tufafanue kazi ambayo itashughulikia mwito wa LLM. Ongeza kazi ifuatayo kwenye faili yako ya `main.rs`:

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

Kazi hii inachukua mteja wa LLM, orodha ya ujumbe (ikiwemo maelekezo ya mtumiaji), zana kutoka seva ya MCP, na kutuma maombi kwa LLM, ikirudisha majibu.
Majibu kutoka kwa LLM yatakuwa na safu ya `choices`. Tutahitaji kuchakata matokeo ili kuona kama kuna `tool_calls` zilizopo. Hii inatufahamisha kuwa LLM inaomba zana maalum itumike pamoja na hoja. Ongeza msimbo ufuatao chini ya faili yako ya `main.rs` ili kufafanua kazi ya kushughulikia majibu ya LLM:

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

Ikiwa `tool_calls` zipo, inachukua taarifa za zana, inaita seva ya MCP na ombi la zana, na inaongeza matokeo kwenye ujumbe wa mazungumzo. Kisha inaendelea na mazungumzo na LLM, na ujumbe unasasishwa na majibu ya msaidizi pamoja na matokeo ya wito wa zana.

Ili kuchukua taarifa za wito wa zana ambazo LLM inarudisha kwa wito wa MCP, tutaongeza kazi nyingine ya msaidizi ili kuchukua kila kitu kinachohitajika kufanya wito. Ongeza msimbo ufuatao chini ya faili yako ya `main.rs`:

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

Kwa kuwa vipande vyote vipo tayari, sasa tunaweza kushughulikia maelekezo ya awali ya mtumiaji na kuita LLM. Sasisha kazi yako ya `main` ili kujumuisha msimbo ufuatao:

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

Hii itahoji LLM na maelekezo ya awali ya mtumiaji ya kuuliza jumla ya namba mbili, na itachakata majibu ili kushughulikia wito wa zana kwa njia ya kiotomatiki.

Vizuri, umefanikiwa!

## Kazi

Chukua msimbo kutoka kwenye zoezi na jenga seva yenye zana zaidi. Kisha unda mteja na LLM, kama ilivyo kwenye zoezi, na ujaribu na maelekezo tofauti ili kuhakikisha zana zote za seva yako zinaitwa kwa njia ya kiotomatiki. Njia hii ya kujenga mteja inamaanisha mtumiaji wa mwisho atakuwa na uzoefu mzuri wa mtumiaji kwa kuwa wanaweza kutumia maelekezo badala ya amri za mteja za moja kwa moja, na hawatakuwa na ufahamu wowote wa seva ya MCP inayoitwa.

## Suluhisho

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## Mambo Muhimu ya Kujifunza

- Kuongeza LLM kwenye mteja wako kunatoa njia bora kwa watumiaji kuingiliana na Seva za MCP.
- Unahitaji kubadilisha majibu ya Seva ya MCP kuwa kitu ambacho LLM inaweza kuelewa.

## Sampuli

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## Rasilimali za Ziada

## Nini Kinachofuata

- Kinachofuata: [Kutumia seva kwa kutumia Visual Studio Code](../04-vscode/README.md)

---

**Kanusho**:  
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kuhakikisha usahihi, tafsiri za kiotomatiki zinaweza kuwa na makosa au kutokuwa sahihi. Hati ya asili katika lugha yake ya awali inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu ya binadamu inapendekezwa. Hatutawajibika kwa kutoelewana au tafsiri zisizo sahihi zinazotokana na matumizi ya tafsiri hii.