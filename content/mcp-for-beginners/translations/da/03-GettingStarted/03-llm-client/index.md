<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:33:20+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "da"
}
-->
# Oprettelse af en klient med LLM

Indtil nu har du set, hvordan man opretter en server og en klient. Klienten har kunnet kalde serveren eksplicit for at liste dens værktøjer, ressourcer og prompts. Men det er ikke en særlig praktisk tilgang. Din bruger lever i den agentiske æra og forventer at bruge prompts og kommunikere med en LLM for at gøre dette. For din bruger er det ligegyldigt, om du bruger MCP til at gemme dine funktioner, men de forventer at kunne interagere med naturligt sprog. Så hvordan løser vi dette? Løsningen er at tilføje en LLM til klienten.

## Oversigt

I denne lektion fokuserer vi på at tilføje en LLM til din klient og viser, hvordan dette giver en meget bedre oplevelse for din bruger.

## Læringsmål

Ved afslutningen af denne lektion vil du kunne:

- Oprette en klient med en LLM.
- Problemfrit interagere med en MCP-server ved hjælp af en LLM.
- Give en bedre brugeroplevelse på klientsiden.

## Fremgangsmåde

Lad os prøve at forstå den tilgang, vi skal tage. At tilføje en LLM lyder enkelt, men hvordan gør vi det egentlig?

Sådan vil klienten interagere med serveren:

1. Opret forbindelse til serveren.

1. Liste funktioner, prompts, ressourcer og værktøjer og gem deres skema.

1. Tilføj en LLM og videregiv de gemte funktioner og deres skema i et format, som LLM forstår.

1. Håndter en brugerprompt ved at videregive den til LLM sammen med de værktøjer, der er listet af klienten.

Godt, nu forstår vi, hvordan vi kan gøre dette på et højt niveau. Lad os prøve det i øvelsen nedenfor.

## Øvelse: Oprettelse af en klient med en LLM

I denne øvelse vil vi lære at tilføje en LLM til vores klient.

### Autentificering med GitHub Personal Access Token

Oprettelse af et GitHub-token er en enkel proces. Sådan gør du:

- Gå til GitHub-indstillinger – Klik på dit profilbillede øverst til højre og vælg Indstillinger.
- Naviger til Developer Settings – Rul ned og klik på Developer Settings.
- Vælg Personal Access Tokens – Klik på Fine-grained tokens og derefter Generate new token.
- Konfigurer dit token – Tilføj en note til reference, angiv en udløbsdato, og vælg de nødvendige scopes (tilladelser). Sørg i dette tilfælde for at tilføje Models-tilladelsen.
- Generer og kopier tokenet – Klik på Generate token, og sørg for at kopiere det med det samme, da du ikke vil kunne se det igen.

### -1- Opret forbindelse til serveren

Lad os først oprette vores klient:

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

I den foregående kode har vi:

- Importeret de nødvendige biblioteker.
- Oprettet en klasse med to medlemmer, `client` og `openai`, der hjælper os med at administrere en klient og interagere med en LLM.
- Konfigureret vores LLM-instans til at bruge GitHub Models ved at indstille `baseUrl` til at pege på inferens-API'en.

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

I den foregående kode har vi:

- Importeret de nødvendige biblioteker til MCP.
- Oprettet en klient.

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

Først skal du tilføje LangChain4j-afhængigheder til din `pom.xml`-fil. Tilføj disse afhængigheder for at aktivere MCP-integration og GitHub Models-support:

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

Opret derefter din Java-klientklasse:

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

I den foregående kode har vi:

- **Tilføjet LangChain4j-afhængigheder**: Nødvendige for MCP-integration, OpenAI's officielle klient og GitHub Models-support.
- **Importeret LangChain4j-bibliotekerne**: Til MCP-integration og OpenAI chatmodel-funktionalitet.
- **Oprettet en `ChatLanguageModel`**: Konfigureret til at bruge GitHub Models med dit GitHub-token.
- **Opsat HTTP-transport**: Brug af Server-Sent Events (SSE) til at oprette forbindelse til MCP-serveren.
- **Oprettet en MCP-klient**: Der håndterer kommunikationen med serveren.
- **Brugt LangChain4j's indbyggede MCP-support**: Som forenkler integrationen mellem LLM'er og MCP-servere.

#### Rust

Dette eksempel antager, at du har en Rust-baseret MCP-server kørende. Hvis du ikke har en, kan du vende tilbage til lektionen [01-first-server](../01-first-server/README.md) for at oprette serveren.

Når du har din Rust MCP-server, skal du åbne en terminal og navigere til samme mappe som serveren. Kør derefter følgende kommando for at oprette et nyt LLM-klientprojekt:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Tilføj følgende afhængigheder til din `Cargo.toml`-fil:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Der findes ikke et officielt Rust-bibliotek til OpenAI, men `async-openai`-pakken er et [community-vedligeholdt bibliotek](https://platform.openai.com/docs/libraries/rust#rust), der ofte bruges.

Åbn filen `src/main.rs` og erstat dens indhold med følgende kode:

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

Denne kode opsætter en grundlæggende Rust-applikation, der opretter forbindelse til en MCP-server og GitHub Models for LLM-interaktioner.

> [!IMPORTANT]
> Sørg for at indstille miljøvariablen `OPENAI_API_KEY` med dit GitHub-token, før du kører applikationen.

Godt, lad os i næste trin liste funktionerne på serveren.

### -2- Liste serverfunktioner

Nu vil vi oprette forbindelse til serveren og spørge om dens funktioner:

#### TypeScript

I den samme klasse skal du tilføje følgende metoder:

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

I den foregående kode har vi:

- Tilføjet kode til at oprette forbindelse til serveren, `connectToServer`.
- Oprettet en `run`-metode, der er ansvarlig for at håndtere vores app-flow. Indtil videre lister den kun værktøjerne, men vi vil snart tilføje mere.

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

Her er, hvad vi har tilføjet:

- Listet ressourcer og værktøjer og udskrevet dem. For værktøjer lister vi også `inputSchema`, som vi bruger senere.

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

I den foregående kode har vi:

- Listet de værktøjer, der er tilgængelige på MCP-serveren.
- For hvert værktøj listet navn, beskrivelse og dets skema. Det sidste er noget, vi vil bruge til at kalde værktøjerne snart.

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

I den foregående kode har vi:

- Oprettet en `McpToolProvider`, der automatisk opdager og registrerer alle værktøjer fra MCP-serveren.
- Tool provideren håndterer konverteringen mellem MCP-værktøjsskemaer og LangChain4j's værktøjsformat internt.
- Denne tilgang abstraherer den manuelle værktøjsliste og konverteringsproces.

#### Rust

Hentning af værktøjer fra MCP-serveren udføres ved hjælp af metoden `list_tools`. I din `main`-funktion, efter opsætning af MCP-klienten, skal du tilføje følgende kode:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Konverter serverfunktioner til LLM-værktøjer

Næste trin efter at have listet serverfunktioner er at konvertere dem til et format, som LLM forstår. Når vi gør det, kan vi give disse funktioner som værktøjer til vores LLM.

#### TypeScript

1. Tilføj følgende kode for at konvertere svar fra MCP-serveren til et værktøjsformat, som LLM kan bruge:

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

    Ovenstående kode tager et svar fra MCP-serveren og konverterer det til en værktøjsdefinition, som LLM kan forstå.

1. Lad os opdatere `run`-metoden for at liste serverfunktioner:

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

    I den foregående kode har vi opdateret `run`-metoden til at gennemgå resultatet og for hver post kalde `openAiToolAdapter`.

#### Python

1. Først skal vi oprette følgende konverteringsfunktion:

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

    I funktionen ovenfor `convert_to_llm_tools` tager vi et MCP-værktøjssvar og konverterer det til et format, som LLM kan forstå.

1. Dernæst skal vi opdatere vores klientkode til at udnytte denne funktion som følger:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Her tilføjer vi et kald til `convert_to_llm_tool` for at konvertere MCP-værktøjssvaret til noget, vi kan give LLM senere.

#### .NET

1. Lad os tilføje kode for at konvertere MCP-værktøjssvaret til noget, LLM kan forstå:

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

I den foregående kode har vi:

- Oprettet en funktion `ConvertFrom`, der tager navn, beskrivelse og inputskema.
- Defineret funktionalitet, der opretter en FunctionDefinition, som videregives til en ChatCompletionsDefinition. Sidstnævnte er noget, LLM kan forstå.

1. Lad os se, hvordan vi kan opdatere eksisterende kode for at drage fordel af denne funktion ovenfor:

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

I den foregående kode har vi:

- Defineret en simpel `Bot`-grænseflade til interaktion med naturligt sprog.
- Brug LangChain4j's `AiServices` til automatisk at binde LLM med MCP tool provideren.
- Frameworket håndterer automatisk værktøjsskema-konvertering og funktionskald bag kulisserne.
- Denne tilgang eliminerer manuel værktøjskonvertering - LangChain4j håndterer al kompleksiteten ved at konvertere MCP-værktøjer til LLM-kompatibelt format.

#### Rust

For at konvertere MCP-værktøjssvaret til et format, som LLM kan forstå, tilføjer vi en hjælpefunktion, der formaterer værktøjslisten. Tilføj følgende kode til din `main.rs`-fil under `main`-funktionen. Dette vil blive kaldt, når der laves forespørgsler til LLM:

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

Godt, vi er nu klar til at håndtere brugerforespørgsler, så lad os tackle det næste.

### -4- Håndter brugerpromptforespørgsel

I denne del af koden vil vi håndtere brugerforespørgsler.

#### TypeScript

1. Tilføj en metode, der vil blive brugt til at kalde vores LLM:

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

    I den foregående kode har vi:

    - Tilføjet en metode `callTools`.
    - Metoden tager et LLM-svar og tjekker, hvilke værktøjer der er blevet kaldt, hvis nogen:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Kalder et værktøj, hvis LLM angiver, at det skal kaldes:

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

1. Opdater `run`-metoden for at inkludere kald til LLM og kald til `callTools`:

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

Godt, lad os liste koden i sin helhed:

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

1. Lad os tilføje nogle imports, der er nødvendige for at kalde en LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Dernæst skal vi tilføje funktionen, der vil kalde LLM:

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

    I den foregående kode har vi:

    - Videregivet vores funktioner, som vi fandt på MCP-serveren og konverterede, til LLM.
    - Derefter kaldte vi LLM med disse funktioner.
    - Derefter inspicerer vi resultatet for at se, hvilke funktioner vi skal kalde, hvis nogen.
    - Til sidst videregiver vi en liste over funktioner, der skal kaldes.

1. Sidste trin, lad os opdatere vores hovedkode:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Der, det var det sidste trin. I koden ovenfor:

    - Kalder vi et MCP-værktøj via `call_tool` ved hjælp af en funktion, som LLM mente, vi skulle kalde baseret på vores prompt.
    - Udskriver resultatet af værktøjskaldet til MCP-serveren.

#### .NET

1. Lad os vise noget kode til at lave en LLM-promptforespørgsel:

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

    I den foregående kode har vi:

    - Hentet værktøjer fra MCP-serveren, `var tools = await GetMcpTools()`.
    - Defineret en brugerprompt `userMessage`.
    - Konstrueret en optionsobjekt, der specificerer model og værktøjer.
    - Lavet en forespørgsel mod LLM.

1. Et sidste trin, lad os se, om LLM mener, vi skal kalde en funktion:

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

    I den foregående kode har vi:

    - Gennemgået en liste over funktionskald.
    - For hvert værktøjskald, udtrukket navn og argumenter og kaldt værktøjet på MCP-serveren ved hjælp af MCP-klienten. Til sidst udskriver vi resultaterne.

Her er koden i sin helhed:

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

I den foregående kode har vi:

- Brugt enkle prompts med naturligt sprog til at interagere med MCP-serverværktøjer.
- LangChain4j-frameworket håndterer automatisk:
  - Konvertering af brugerprompts til værktøjskald, når det er nødvendigt.
  - Kald af de relevante MCP-værktøjer baseret på LLM's beslutning.
  - Håndtering af samtaleflowet mellem LLM og MCP-serveren.
- Metoden `bot.chat()` returnerer svar med naturligt sprog, der kan inkludere resultater fra MCP-værktøjsudførelser.
- Denne tilgang giver en problemfri brugeroplevelse, hvor brugerne ikke behøver at kende til den underliggende MCP-implementering.

Komplet kodeeksempel:

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

Her sker det meste af arbejdet. Vi vil kalde LLM med den oprindelige brugerprompt, derefter behandle svaret for at se, om der skal kaldes værktøjer. Hvis ja, vil vi kalde disse værktøjer og fortsætte samtalen med LLM, indtil der ikke er flere værktøjskald nødvendige, og vi har et endeligt svar.

Vi vil lave flere kald til LLM, så lad os definere en funktion, der vil håndtere LLM-kaldet. Tilføj følgende funktion til din `main.rs`-fil:

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

Denne funktion tager LLM-klienten, en liste over beskeder (inklusive brugerprompten), værktøjer fra MCP-serveren og sender en forespørgsel til LLM, der returnerer svaret.
Svaret fra LLM vil indeholde et array af `choices`. Vi skal behandle resultatet for at se, om der er nogen `tool_calls` til stede. Dette fortæller os, at LLM anmoder om, at et specifikt værktøj skal kaldes med argumenter. Tilføj følgende kode nederst i din `main.rs`-fil for at definere en funktion til at håndtere LLM-svaret:

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

Hvis `tool_calls` er til stede, udtrækker den værktøjsinformationen, kalder MCP-serveren med værktøjsanmodningen og tilføjer resultaterne til samtalebeskederne. Den fortsætter derefter samtalen med LLM, og beskederne opdateres med assistentens svar og værktøjsresultater.

For at udtrække værktøjsopkaldsinformation, som LLM returnerer til MCP-opkald, tilføjer vi en anden hjælpefunktion for at udtrække alt, der er nødvendigt for at foretage opkaldet. Tilføj følgende kode nederst i din `main.rs`-fil:

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

Med alle brikkerne på plads kan vi nu håndtere den indledende brugerprompt og kalde LLM. Opdater din `main`-funktion til at inkludere følgende kode:

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

Dette vil forespørge LLM med den indledende brugerprompt, der spørger om summen af to tal, og det vil behandle svaret for dynamisk at håndtere værktøjsopkald.

Godt klaret, du gjorde det!

## Opgave

Tag koden fra øvelsen og byg serveren ud med nogle flere værktøjer. Opret derefter en klient med en LLM, som i øvelsen, og test den med forskellige prompts for at sikre, at alle dine serverværktøjer bliver kaldt dynamisk. Denne måde at bygge en klient på betyder, at slutbrugeren vil få en fantastisk brugeroplevelse, da de kan bruge prompts i stedet for præcise klientkommandoer og være uvidende om, at en MCP-server bliver kaldt.

## Løsning

[Løsning](/03-GettingStarted/03-llm-client/solution/README.md)

## Vigtige pointer

- At tilføje en LLM til din klient giver en bedre måde for brugere at interagere med MCP-servere.
- Du skal konvertere MCP-serverens svar til noget, LLM kan forstå.

## Eksempler

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## Yderligere ressourcer

## Hvad er det næste

- Næste: [Forbrug af en server ved hjælp af Visual Studio Code](../04-vscode/README.md)

---

**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal det bemærkes, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os ikke ansvar for misforståelser eller fejltolkninger, der måtte opstå som følge af brugen af denne oversættelse.