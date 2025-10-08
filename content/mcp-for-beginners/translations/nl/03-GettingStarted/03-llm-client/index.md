<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:42:02+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "nl"
}
-->
# Een client maken met LLM

Tot nu toe heb je gezien hoe je een server en een client kunt maken. De client kon expliciet de server aanroepen om zijn tools, bronnen en prompts op te vragen. Dit is echter geen erg praktische aanpak. Jouw gebruiker leeft in het agentische tijdperk en verwacht prompts te gebruiken en te communiceren met een LLM om dit te doen. Voor jouw gebruiker maakt het niet uit of je MCP gebruikt om je mogelijkheden op te slaan, maar ze verwachten wel dat ze natuurlijke taal kunnen gebruiken om te communiceren. Hoe lossen we dit op? De oplossing is het toevoegen van een LLM aan de client.

## Overzicht

In deze les richten we ons op het toevoegen van een LLM aan je client en laten we zien hoe dit een veel betere ervaring biedt voor je gebruiker.

## Leerdoelen

Aan het einde van deze les kun je:

- Een client maken met een LLM.
- Naadloos communiceren met een MCP-server via een LLM.
- Een betere gebruikerservaring bieden aan de clientzijde.

## Aanpak

Laten we proberen de aanpak te begrijpen die we moeten volgen. Het toevoegen van een LLM klinkt eenvoudig, maar hoe doen we dit precies?

Zo zal de client communiceren met de server:

1. Maak verbinding met de server.

1. Lijst mogelijkheden, prompts, bronnen en tools op en sla hun schema op.

1. Voeg een LLM toe en geef de opgeslagen mogelijkheden en hun schema door in een formaat dat de LLM begrijpt.

1. Verwerk een gebruikersprompt door deze samen met de tools die door de client zijn vermeld, door te geven aan de LLM.

Goed, nu begrijpen we op hoog niveau hoe we dit kunnen doen. Laten we dit proberen in de onderstaande oefening.

## Oefening: Een client maken met een LLM

In deze oefening leren we hoe we een LLM aan onze client kunnen toevoegen.

### Authenticatie met GitHub Personal Access Token

Het maken van een GitHub-token is een eenvoudig proces. Hier is hoe je dit doet:

- Ga naar GitHub-instellingen – Klik op je profielfoto in de rechterbovenhoek en selecteer Instellingen.
- Navigeer naar Developer Settings – Scroll naar beneden en klik op Developer Settings.
- Selecteer Personal Access Tokens – Klik op Fine-grained tokens en vervolgens op Generate new token.
- Configureer je token – Voeg een notitie toe ter referentie, stel een vervaldatum in en selecteer de benodigde scopes (machtigingen). Zorg er in dit geval voor dat je de Models-machtiging toevoegt.
- Genereer en kopieer het token – Klik op Generate token en zorg ervoor dat je het onmiddellijk kopieert, want je kunt het later niet meer bekijken.

### -1- Verbinden met de server

Laten we eerst onze client maken:

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

In de bovenstaande code hebben we:

- De benodigde bibliotheken geïmporteerd.
- Een klasse gemaakt met twee leden, `client` en `openai`, die ons helpen een client te beheren en te communiceren met een LLM.
- Onze LLM-instantie geconfigureerd om GitHub Models te gebruiken door `baseUrl` in te stellen om naar de inference API te wijzen.

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

In de bovenstaande code hebben we:

- De benodigde bibliotheken voor MCP geïmporteerd.
- Een client gemaakt.

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

Eerst moet je de LangChain4j-afhankelijkheden toevoegen aan je `pom.xml`-bestand. Voeg deze afhankelijkheden toe om MCP-integratie en ondersteuning voor GitHub Models mogelijk te maken:

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

Maak vervolgens je Java-clientklasse:

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

In de bovenstaande code hebben we:

- **LangChain4j-afhankelijkheden toegevoegd**: Vereist voor MCP-integratie, officiële OpenAI-client en ondersteuning voor GitHub Models.
- **LangChain4j-bibliotheken geïmporteerd**: Voor MCP-integratie en OpenAI-chatmodel functionaliteit.
- **Een `ChatLanguageModel` gemaakt**: Geconfigureerd om GitHub Models te gebruiken met je GitHub-token.
- **HTTP-transport ingesteld**: Met behulp van Server-Sent Events (SSE) om verbinding te maken met de MCP-server.
- **Een MCP-client gemaakt**: Die de communicatie met de server afhandelt.
- **LangChain4j's ingebouwde MCP-ondersteuning gebruikt**: Wat de integratie tussen LLM's en MCP-servers vereenvoudigt.

#### Rust

Dit voorbeeld gaat ervan uit dat je een op Rust gebaseerde MCP-server hebt draaien. Als je er geen hebt, raadpleeg dan de les [01-first-server](../01-first-server/README.md) om de server te maken.

Zodra je je Rust MCP-server hebt, open je een terminal en navigeer je naar dezelfde map als de server. Voer vervolgens de volgende opdracht uit om een nieuw LLM-clientproject te maken:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Voeg de volgende afhankelijkheden toe aan je `Cargo.toml`-bestand:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Er is geen officiële Rust-bibliotheek voor OpenAI, maar de `async-openai` crate is een [community onderhouden bibliotheek](https://platform.openai.com/docs/libraries/rust#rust) die vaak wordt gebruikt.

Open het bestand `src/main.rs` en vervang de inhoud door de volgende code:

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

Deze code stelt een basis Rust-toepassing in die verbinding maakt met een MCP-server en GitHub Models voor LLM-interacties.

> [!IMPORTANT]
> Zorg ervoor dat je de omgevingsvariabele `OPENAI_API_KEY` instelt met je GitHub-token voordat je de toepassing uitvoert.

Goed, voor onze volgende stap gaan we de mogelijkheden van de server opsommen.

### -2- Servermogelijkheden opsommen

Nu gaan we verbinding maken met de server en vragen naar zijn mogelijkheden:

#### TypeScript

Voeg in dezelfde klasse de volgende methoden toe:

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

In de bovenstaande code hebben we:

- Code toegevoegd om verbinding te maken met de server, `connectToServer`.
- Een `run`-methode gemaakt die verantwoordelijk is voor het afhandelen van de app-flow. Tot nu toe somt deze alleen de tools op, maar we zullen er binnenkort meer aan toevoegen.

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

Hier is wat we hebben toegevoegd:

- Bronnen en tools opgesomd en afgedrukt. Voor tools hebben we ook `inputSchema` opgesomd, wat we later gebruiken.

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

In de bovenstaande code hebben we:

- De beschikbare tools op de MCP-server opgesomd.
- Voor elke tool de naam, beschrijving en het schema opgesomd. Het laatste is iets dat we binnenkort zullen gebruiken om de tools aan te roepen.

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

In de bovenstaande code hebben we:

- Een `McpToolProvider` gemaakt die automatisch alle tools van de MCP-server ontdekt en registreert.
- De toolprovider verwerkt intern de conversie tussen MCP-toolschemas en LangChain4j's toolformaat.
- Deze aanpak abstraheert het handmatig opsommen en converteren van tools.

#### Rust

Tools ophalen van de MCP-server gebeurt met de methode `list_tools`. Voeg in je `main`-functie, na het instellen van de MCP-client, de volgende code toe:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Servermogelijkheden converteren naar LLM-tools

De volgende stap na het opsommen van servermogelijkheden is om ze te converteren naar een formaat dat de LLM begrijpt. Zodra we dat doen, kunnen we deze mogelijkheden als tools aan de LLM aanbieden.

#### TypeScript

1. Voeg de volgende code toe om de respons van de MCP-server te converteren naar een toolformaat dat de LLM kan gebruiken:

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

    De bovenstaande code neemt een respons van de MCP-server en converteert deze naar een tooldefinitieformaat dat de LLM kan begrijpen.

1. Laten we de `run`-methode bijwerken om servermogelijkheden op te sommen:

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

    In de bovenstaande code hebben we de `run`-methode bijgewerkt om door het resultaat te mappen en voor elke invoer `openAiToolAdapter` aan te roepen.

#### Python

1. Laten we eerst de volgende converterfunctie maken:

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

    In de bovenstaande functie `convert_to_llm_tools` nemen we een MCP-toolrespons en converteren deze naar een formaat dat de LLM kan begrijpen.

1. Vervolgens werken we onze clientcode bij om gebruik te maken van deze functie zoals hieronder:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Hier voegen we een oproep toe aan `convert_to_llm_tool` om de MCP-toolrespons te converteren naar iets dat we later aan de LLM kunnen doorgeven.

#### .NET

1. Laten we code toevoegen om de MCP-toolrespons te converteren naar iets dat de LLM kan begrijpen:

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

In de bovenstaande code hebben we:

- Een functie `ConvertFrom` gemaakt die naam, beschrijving en invoerschema accepteert.
- Functionaliteit gedefinieerd die een FunctionDefinition maakt die wordt doorgegeven aan een ChatCompletionsDefinition. Dit laatste is iets dat de LLM kan begrijpen.

1. Laten we zien hoe we bestaande code kunnen bijwerken om gebruik te maken van bovenstaande functie:

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

In de bovenstaande code hebben we:

- Een eenvoudige `Bot`-interface gedefinieerd voor natuurlijke taalinteracties.
- LangChain4j's `AiServices` gebruikt om automatisch de LLM te koppelen aan de MCP-toolprovider.
- Het framework verwerkt automatisch toolschema-conversie en functieaanroepen achter de schermen.
- Deze aanpak elimineert handmatige toolconversie - LangChain4j verwerkt alle complexiteit van het converteren van MCP-tools naar LLM-compatibel formaat.

#### Rust

Om de MCP-toolrespons te converteren naar een formaat dat de LLM kan begrijpen, voegen we een hulpfunctie toe die de toolslijst formatteert. Voeg de volgende code toe aan je `main.rs`-bestand onder de `main`-functie. Deze wordt aangeroepen bij het maken van verzoeken aan de LLM:

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

Goed, we zijn nu klaar om gebruikersverzoeken te verwerken, dus laten we dat als volgende aanpakken.

### -4- Gebruikerspromptverzoek verwerken

In dit deel van de code gaan we gebruikersverzoeken verwerken.

#### TypeScript

1. Voeg een methode toe die wordt gebruikt om onze LLM aan te roepen:

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

    In de bovenstaande code hebben we:

    - Een methode `callTools` toegevoegd.
    - De methode controleert een LLM-respons om te zien welke tools zijn aangeroepen, indien van toepassing:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Roept een tool aan, indien de LLM aangeeft dat deze moet worden aangeroepen:

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

1. Werk de `run`-methode bij om oproepen naar de LLM en `callTools` op te nemen:

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

Goed, laten we de volledige code bekijken:

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

1. Laten we enkele imports toevoegen die nodig zijn om een LLM aan te roepen:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Voeg vervolgens de functie toe die de LLM aanroept:

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

    In de bovenstaande code hebben we:

    - Onze functies, die we op de MCP-server hebben gevonden en geconverteerd, doorgegeven aan de LLM.
    - Vervolgens hebben we de LLM aangeroepen met deze functies.
    - Daarna inspecteren we het resultaat om te zien welke functies we moeten aanroepen, indien van toepassing.
    - Tot slot geven we een array van functies door om aan te roepen.

1. Laatste stap, werk onze hoofdcode bij:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Daar, dat was de laatste stap. In de bovenstaande code:

    - Roepen we een MCP-tool aan via `call_tool` met een functie die de LLM dacht dat we moesten aanroepen op basis van onze prompt.
    - Printen we het resultaat van de toolaanroep naar de MCP-server.

#### .NET

1. Laten we wat code tonen voor het doen van een LLM-promptverzoek:

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

    In de bovenstaande code hebben we:

    - Tools opgehaald van de MCP-server, `var tools = await GetMcpTools()`.
    - Een gebruikersprompt gedefinieerd `userMessage`.
    - Een optiesobject geconstrueerd waarin model en tools worden gespecificeerd.
    - Een verzoek gedaan aan de LLM.

1. Eén laatste stap, laten we zien of de LLM denkt dat we een functie moeten aanroepen:

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

    In de bovenstaande code hebben we:

    - Door een lijst van functieaanroepen gelopen.
    - Voor elke toolaanroep de naam en argumenten uitgepakt en de tool op de MCP-server aangeroepen met behulp van de MCP-client. Tot slot printen we de resultaten.

Hier is de volledige code:

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

In de bovenstaande code hebben we:

- Eenvoudige natuurlijke taalprompts gebruikt om te communiceren met de MCP-servertools.
- Het LangChain4j-framework verwerkt automatisch:
  - Het converteren van gebruikersprompts naar toolaanroepen indien nodig.
  - Het aanroepen van de juiste MCP-tools op basis van de beslissing van de LLM.
  - Het beheren van de conversatiestroom tussen de LLM en MCP-server.
- De methode `bot.chat()` retourneert natuurlijke taalantwoorden die resultaten van MCP-tooluitvoeringen kunnen bevatten.
- Deze aanpak biedt een naadloze gebruikerservaring waarbij gebruikers niets hoeven te weten over de onderliggende MCP-implementatie.

Volledig codevoorbeeld:

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

Hier vindt het meeste werk plaats. We zullen de LLM aanroepen met de initiële gebruikersprompt, vervolgens de respons verwerken om te zien of er tools moeten worden aangeroepen. Indien nodig zullen we die tools aanroepen en doorgaan met de conversatie met de LLM totdat er geen toolaanroepen meer nodig zijn en we een definitief antwoord hebben.

We zullen meerdere oproepen doen naar de LLM, dus laten we een functie definiëren die de LLM-aanroep afhandelt. Voeg de volgende functie toe aan je `main.rs`-bestand:

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

Deze functie neemt de LLM-client, een lijst met berichten (inclusief de gebruikersprompt), tools van de MCP-server en stuurt een verzoek naar de LLM, waarbij de respons wordt geretourneerd.
De respons van de LLM bevat een array van `choices`. We moeten het resultaat verwerken om te zien of er `tool_calls` aanwezig zijn. Dit laat ons weten dat de LLM vraagt om een specifiek hulpmiddel aan te roepen met argumenten. Voeg de volgende code toe aan het einde van je `main.rs`-bestand om een functie te definiëren die de LLM-respons afhandelt:

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

Als er `tool_calls` aanwezig zijn, haalt het de informatie over het hulpmiddel op, roept de MCP-server aan met het hulpmiddelverzoek en voegt de resultaten toe aan de conversatieberichten. Vervolgens gaat het gesprek verder met de LLM en worden de berichten bijgewerkt met de reactie van de assistent en de resultaten van de hulpmiddeloproep.

Om de informatie over hulpmiddeloproepen die de LLM retourneert voor MCP-oproepen te extraheren, voegen we een andere hulpfunctie toe om alles te verzamelen wat nodig is om de oproep te doen. Voeg de volgende code toe aan het einde van je `main.rs`-bestand:

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

Met alle onderdelen op hun plaats kunnen we nu de initiële gebruikersprompt afhandelen en de LLM aanroepen. Werk je `main`-functie bij om de volgende code op te nemen:

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

Dit zal de LLM raadplegen met de initiële gebruikersprompt waarin wordt gevraagd om de som van twee getallen, en het zal de respons verwerken om hulpmiddeloproepen dynamisch af te handelen.

Goed gedaan, je hebt het voor elkaar!

## Opdracht

Neem de code uit de oefening en bouw de server verder uit met meer hulpmiddelen. Maak vervolgens een client met een LLM, zoals in de oefening, en test deze met verschillende prompts om ervoor te zorgen dat al je serverhulpmiddelen dynamisch worden aangeroepen. Deze manier van het bouwen van een client zorgt ervoor dat de eindgebruiker een geweldige gebruikerservaring heeft, omdat ze prompts kunnen gebruiken in plaats van exacte clientcommando's, en zich niet bewust hoeven te zijn van een MCP-server die wordt aangeroepen.

## Oplossing

[Oplossing](/03-GettingStarted/03-llm-client/solution/README.md)

## Belangrijke inzichten

- Het toevoegen van een LLM aan je client biedt een betere manier voor gebruikers om met MCP-servers te communiceren.
- Je moet de respons van de MCP-server omzetten naar iets dat de LLM kan begrijpen.

## Voorbeelden

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## Aanvullende bronnen

## Wat komt hierna?

- Volgende: [Een server gebruiken met Visual Studio Code](../04-vscode/README.md)

---

**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.