<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T15:25:34+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "sl"
}
-->
# Ustvarjanje odjemalca z LLM

Do sedaj ste videli, kako ustvariti strežnik in odjemalca. Odjemalec je lahko izrecno klical strežnik za seznam njegovih orodij, virov in pozivov. Vendar pa to ni zelo praktičen pristop. Vaš uporabnik živi v agentni dobi in pričakuje, da bo uporabljal pozive ter komuniciral z LLM za izvedbo nalog. Za vašega uporabnika ni pomembno, ali uporabljate MCP za shranjevanje svojih zmogljivosti, vendar pričakujejo, da bodo lahko komunicirali v naravnem jeziku. Kako torej to rešimo? Rešitev je v dodajanju LLM odjemalcu.

## Pregled

V tej lekciji se osredotočamo na dodajanje LLM vašemu odjemalcu in prikaz, kako to zagotavlja veliko boljšo izkušnjo za vašega uporabnika.

## Cilji učenja

Do konca te lekcije boste lahko:

- Ustvarili odjemalca z LLM.
- Brez težav komunicirali z MCP strežnikom prek LLM.
- Zagotovili boljšo uporabniško izkušnjo na strani odjemalca.

## Pristop

Poskusimo razumeti pristop, ki ga moramo sprejeti. Dodajanje LLM se sliši preprosto, vendar kako to dejansko izvedemo?

Tako bo odjemalec komuniciral s strežnikom:

1. Vzpostavite povezavo s strežnikom.

1. Pridobite seznam zmogljivosti, pozivov, virov in orodij ter shranite njihovo shemo.

1. Dodajte LLM in posredujte shranjene zmogljivosti ter njihove sheme v formatu, ki ga LLM razume.

1. Obdelajte uporabniški poziv tako, da ga posredujete LLM skupaj z orodji, ki jih je navedel odjemalec.

Odlično, zdaj razumemo, kako to lahko izvedemo na visoki ravni. Poskusimo to v spodnji vaji.

## Vaja: Ustvarjanje odjemalca z LLM

V tej vaji se bomo naučili dodati LLM našemu odjemalcu.

### Avtentikacija z GitHub osebno dostopnim žetonom

Ustvarjanje GitHub žetona je preprost postopek. Tukaj je, kako to storite:

- Pojdite v GitHub Nastavitve – Kliknite na svojo profilno sliko v zgornjem desnem kotu in izberite Nastavitve.
- Pomaknite se do Nastavitve za razvijalce – Pomaknite se navzdol in kliknite na Nastavitve za razvijalce.
- Izberite Osebni dostopni žetoni – Kliknite na žetone z natančno določenimi pravicami in nato Ustvari nov žeton.
- Konfigurirajte svoj žeton – Dodajte opombo za referenco, nastavite datum poteka in izberite potrebne obsege (dovoljenja). V tem primeru se prepričajte, da dodate dovoljenje za modele.
- Ustvarite in kopirajte žeton – Kliknite Ustvari žeton in ga takoj kopirajte, saj ga kasneje ne boste mogli več videti.

### -1- Povezava s strežnikom

Najprej ustvarimo našega odjemalca:

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

V zgornji kodi smo:

- Uvozili potrebne knjižnice.
- Ustvarili razred z dvema članoma, `client` in `openai`, ki nam bosta pomagala upravljati odjemalca in komunicirati z LLM.
- Konfigurirali našo LLM instanco za uporabo GitHub modelov z nastavitvijo `baseUrl`, ki kaže na API za sklepanje.

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

V zgornji kodi smo:

- Uvozili potrebne knjižnice za MCP.
- Ustvarili odjemalca.

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

Najprej boste morali dodati odvisnosti LangChain4j v datoteko `pom.xml`. Dodajte te odvisnosti za omogočanje integracije MCP in podporo za GitHub modele:

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

Nato ustvarite razred odjemalca v Javi:

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

V zgornji kodi smo:

- **Dodali odvisnosti LangChain4j**: Potrebne za integracijo MCP, uradni odjemalec OpenAI in podporo za GitHub modele.
- **Uvozili knjižnice LangChain4j**: Za integracijo MCP in funkcionalnost modela za klepet OpenAI.
- **Ustvarili `ChatLanguageModel`**: Konfiguriran za uporabo GitHub modelov z vašim GitHub žetonom.
- **Nastavili HTTP transport**: Z uporabo dogodkov, poslanih s strežnikom (SSE), za povezavo z MCP strežnikom.
- **Ustvarili MCP odjemalca**: Ki bo upravljal komunikacijo s strežnikom.
- **Uporabili vgrajeno podporo MCP v LangChain4j**: Ki poenostavi integracijo med LLM in MCP strežniki.

#### Rust

Ta primer predpostavlja, da imate strežnik MCP, ki temelji na Rustu. Če ga nimate, se vrnite na lekcijo [01-prvi-strežnik](../01-first-server/README.md) za ustvarjanje strežnika.

Ko imate strežnik MCP, ki temelji na Rustu, odprite terminal in se pomaknite v isto mapo kot strežnik. Nato zaženite naslednji ukaz za ustvarjanje novega projekta odjemalca LLM:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Dodajte naslednje odvisnosti v datoteko `Cargo.toml`:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Uradna knjižnica za OpenAI v Rustu ne obstaja, vendar je `async-openai` knjižnica [vzdrževana s strani skupnosti](https://platform.openai.com/docs/libraries/rust#rust), ki se pogosto uporablja.

Odprite datoteko `src/main.rs` in zamenjajte njeno vsebino z naslednjo kodo:

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

Ta koda nastavi osnovno aplikacijo v Rustu, ki se bo povezala z MCP strežnikom in GitHub modeli za interakcije z LLM.

> [!IMPORTANT]
> Pred zagonom aplikacije nastavite okoljsko spremenljivko `OPENAI_API_KEY` z vašim GitHub žetonom.

Odlično, v naslednjem koraku bomo pridobili seznam zmogljivosti na strežniku.

### -2- Pridobitev zmogljivosti strežnika

Zdaj se bomo povezali s strežnikom in zahtevali njegove zmogljivosti:

#### TypeScript

V istem razredu dodajte naslednje metode:

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

V zgornji kodi smo:

- Dodali kodo za povezavo s strežnikom, `connectToServer`.
- Ustvarili metodo `run`, ki je odgovorna za upravljanje poteka naše aplikacije. Zaenkrat samo navaja orodja, vendar bomo kmalu dodali več.

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

Tukaj je, kaj smo dodali:

- Pridobili seznam virov in orodij ter jih natisnili. Za orodja smo prav tako navedli `inputSchema`, ki ga bomo uporabili kasneje.

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

V zgornji kodi smo:

- Pridobili seznam orodij, ki so na voljo na MCP strežniku.
- Za vsako orodje navedli ime, opis in njegovo shemo. Slednje bomo uporabili za klicanje orodij kmalu.

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

V zgornji kodi smo:

- Ustvarili `McpToolProvider`, ki samodejno odkrije in registrira vsa orodja s MCP strežnika.
- Ponudnik orodij interno upravlja pretvorbo med shemami orodij MCP in formatom orodij LangChain4j.
- Ta pristop abstrahira ročno navajanje orodij in proces pretvorbe.

#### Rust

Pridobivanje orodij s MCP strežnika se izvede z metodo `list_tools`. V vaši funkciji `main`, po nastavitvi MCP odjemalca, dodajte naslednjo kodo:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Pretvorba zmogljivosti strežnika v orodja LLM

Naslednji korak po pridobitvi zmogljivosti strežnika je njihova pretvorba v format, ki ga LLM razume. Ko to storimo, lahko te zmogljivosti zagotovimo kot orodja LLM.

#### TypeScript

1. Dodajte naslednjo kodo za pretvorbo odgovora MCP strežnika v format orodja, ki ga LLM lahko uporabi:

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

    Zgornja koda vzame odgovor MCP strežnika in ga pretvori v definicijo orodja, ki jo LLM lahko razume.

1. Posodobimo metodo `run`, da pridobi zmogljivosti strežnika:

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

    V zgornji kodi smo posodobili metodo `run`, da pregleduje rezultat in za vsak vnos pokliče `openAiToolAdapter`.

#### Python

1. Najprej ustvarimo naslednjo funkcijo za pretvorbo:

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

    V zgornji funkciji `convert_to_llm_tools` vzamemo odgovor MCP orodja in ga pretvorimo v format, ki ga LLM lahko razume.

1. Nato posodobimo našo kodo odjemalca, da izkoristi to funkcijo, kot sledi:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Tukaj dodajamo klic `convert_to_llm_tool`, da pretvorimo odgovor MCP orodja v nekaj, kar lahko kasneje posredujemo LLM.

#### .NET

1. Dodajmo kodo za pretvorbo odgovora MCP orodja v nekaj, kar LLM lahko razume:

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

V zgornji kodi smo:

- Ustvarili funkcijo `ConvertFrom`, ki sprejme ime, opis in shemo vnosa.
- Določili funkcionalnost, ki ustvari FunctionDefinition, ki se posreduje ChatCompletionsDefinition. Slednje je nekaj, kar LLM lahko razume.

1. Posodobimo obstoječo kodo, da izkoristi zgornjo funkcijo:

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

V zgornji kodi smo:

- Določili preprost vmesnik `Bot` za interakcije v naravnem jeziku.
- Uporabili LangChain4j `AiServices` za samodejno povezovanje LLM z ponudnikom orodij MCP.
- Okvir samodejno upravlja pretvorbo sheme orodij in klic funkcij v ozadju.
- Ta pristop odpravi ročno pretvorbo orodij - LangChain4j upravlja vso kompleksnost pretvorbe MCP orodij v format, združljiv z LLM.

#### Rust

Za pretvorbo odgovora MCP orodja v format, ki ga LLM lahko razume, bomo dodali pomožno funkcijo, ki oblikuje seznam orodij. Dodajte naslednjo kodo v datoteko `main.rs` pod funkcijo `main`. To bo poklicano pri pošiljanju zahtev LLM:

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

Odlično, zdaj smo pripravljeni na obdelavo uporabniških zahtev, zato se lotimo tega naslednje.

### -4- Obdelava uporabniškega poziva

V tem delu kode bomo obdelali uporabniške zahteve.

#### TypeScript

1. Dodajte metodo, ki bo uporabljena za klic našega LLM:

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

    V zgornji kodi smo:

    - Dodali metodo `callTools`.
    - Metoda vzame odgovor LLM in preveri, katera orodja so bila poklicana, če sploh:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Pokliče orodje, če LLM nakaže, da bi ga bilo treba poklicati:

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

1. Posodobite metodo `run`, da vključuje klice LLM in klic `callTools`:

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

Odlično, tukaj je celotna koda:

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

1. Dodajmo nekaj uvozov, potrebnih za klic LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Nato dodajmo funkcijo, ki bo klicala LLM:

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

    V zgornji kodi smo:

    - Posredovali naše funkcije, ki smo jih našli na MCP strežniku in jih pretvorili, LLM.
    - Nato smo poklicali LLM z omenjenimi funkcijami.
    - Nato smo pregledali rezultat, da vidimo, katere funkcije bi morali poklicati, če sploh.
    - Na koncu smo posredovali seznam funkcij za klicanje.

1. Zadnji korak, posodobimo našo glavno kodo:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Tam, to je bil zadnji korak. V zgornji kodi:

    - Kličemo MCP orodje prek `call_tool` z uporabo funkcije, za katero je LLM menil, da bi jo morali poklicati glede na naš poziv.
    - Natisnemo rezultat klica orodja na MCP strežnik.

#### .NET

1. Poglejmo kodo za izvedbo zahteve LLM poziva:

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

    V zgornji kodi smo:

    - Pridobili orodja s MCP strežnika, `var tools = await GetMcpTools()`.
    - Določili uporabniški poziv `userMessage`.
    - Sestavili objekt z možnostmi, ki določa model in orodja.
    - Poslali zahtevo proti LLM.

1. Zadnji korak, preverimo, ali LLM meni, da bi morali poklicati funkcijo:

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

    V zgornji kodi smo:

    - Zagnali zanko skozi seznam klicev funkcij.
    - Za vsak klic orodja razčlenili ime in argumente ter poklicali orodje na MCP strežniku z uporabo MCP odjemalca. Na koncu natisnemo rezultate.

Tukaj je celotna koda:

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

V zgornji kodi smo:

- Uporabili preproste pozive v naravnem jeziku za interakcijo z orodji MCP strežnika.
- Okvir LangChain4j samodejno upravlja:
  - Pretvorbo uporabniških pozivov v klice orodij, kadar je to potrebno.
  - Klic ustreznih MCP orodij na podlagi odločitve LLM.
  - Upravljanje poteka pogovora med LLM in MCP strežnikom.
- Metoda `bot.chat()` vrne odgovore v naravnem jeziku, ki lahko vključujejo rezultate izvedb MCP orodij.
- Ta pristop zagotavlja brezhibno uporabniško izkušnjo, kjer uporabniki ne potrebujejo vedeti o osnovni implementaciji MCP.

Celoten primer kode:

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

Tukaj se zgodi večina dela. Poklicali bomo LLM z začetnim uporabniškim pozivom, nato obdelali odgovor, da vidimo, ali je treba poklicati kakšna orodja. Če je tako, bomo poklicali ta orodja in nadaljevali pogovor z LLM, dokler ne bo več potrebnih klicev orodij in ne bomo imeli končnega odgovora.

Izvedli bomo več klicev LLM, zato definirajmo funkcijo, ki bo upravljala klic LLM. Dodajte naslednjo funkcijo v datoteko `main.rs`:

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

Ta funkcija vzame odjemalca LLM, seznam sporočil (vključno z uporabniškim pozivom), orodja s MCP strežnika in pošlje zahtevo LLM ter vrne odgovor.
Odziv LLM bo vseboval polje `choices`. Rezultat bomo morali obdelati, da preverimo, ali so prisotni kakšni `tool_calls`. To nam pove, da LLM zahteva, da se določenemu orodju posredujejo argumenti. Dodajte naslednjo kodo na dno datoteke `main.rs`, da definirate funkcijo za obravnavo odziva LLM:

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

Če so prisotni `tool_calls`, funkcija izvleče informacije o orodju, pokliče MCP strežnik z zahtevo za orodje in doda rezultate v sporočila pogovora. Nato nadaljuje pogovor z LLM, pri čemer se sporočila posodobijo z odzivom asistenta in rezultati klica orodja.

Za izvlečenje informacij o klicu orodja, ki jih LLM vrne za MCP klice, bomo dodali še eno pomožno funkcijo, ki bo izvlekla vse potrebno za izvedbo klica. Dodajte naslednjo kodo na dno datoteke `main.rs`:

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

Ko imamo vse sestavne dele, lahko obravnavamo začetni uporabniški poziv in pokličemo LLM. Posodobite svojo funkcijo `main`, da vključuje naslednjo kodo:

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

Ta koda bo poizvedovala LLM z začetnim uporabniškim pozivom, ki zahteva vsoto dveh števil, in obdelala odziv za dinamično obravnavo klicev orodij.

Odlično, uspelo vam je!

## Naloga

Vzemite kodo iz vaje in razširite strežnik z več orodji. Nato ustvarite odjemalca z LLM, kot v vaji, in ga preizkusite z različnimi pozivi, da zagotovite, da se vsa orodja strežnika dinamično pokličejo. Tak način gradnje odjemalca omogoča končnemu uporabniku odlično uporabniško izkušnjo, saj lahko uporablja pozive namesto natančnih ukazov odjemalca in je neveden glede kakršnih koli MCP strežnikov, ki se kličejo.

## Rešitev

[Rešitev](/03-GettingStarted/03-llm-client/solution/README.md)

## Ključne ugotovitve

- Dodajanje LLM vašemu odjemalcu omogoča boljši način interakcije z MCP strežniki.
- Odziv MCP strežnika morate pretvoriti v nekaj, kar LLM razume.

## Primeri

- [Java Kalkulator](../samples/java/calculator/README.md)
- [.Net Kalkulator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Kalkulator](../samples/javascript/README.md)
- [TypeScript Kalkulator](../samples/typescript/README.md)
- [Python Kalkulator](../../../../03-GettingStarted/samples/python)
- [Rust Kalkulator](../../../../03-GettingStarted/samples/rust)

## Dodatni viri

## Kaj sledi

- Naprej: [Uporaba strežnika z Visual Studio Code](../04-vscode/README.md)

---

**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve za prevajanje z umetno inteligenco [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da lahko avtomatski prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za ključne informacije priporočamo profesionalni človeški prevod. Ne prevzemamo odgovornosti za morebitna nesporazumevanja ali napačne razlage, ki bi nastale zaradi uporabe tega prevoda.