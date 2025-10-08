<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T15:22:29+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "hr"
}
-->
# Kreiranje klijenta s LLM-om

Do sada ste vidjeli kako kreirati server i klijenta. Klijent je mogao eksplicitno pozvati server kako bi popisao njegove alate, resurse i upite. Međutim, to nije baš praktičan pristup. Vaš korisnik živi u agentičkom dobu i očekuje da koristi upite i komunicira s LLM-om kako bi to učinio. Korisniku nije važno koristite li MCP za pohranu svojih mogućnosti, ali očekuje da koristi prirodni jezik za interakciju. Kako to riješiti? Rješenje je dodavanje LLM-a klijentu.

## Pregled

U ovoj lekciji fokusiramo se na dodavanje LLM-a vašem klijentu i pokazujemo kako to pruža puno bolje iskustvo za vašeg korisnika.

## Ciljevi učenja

Na kraju ove lekcije, moći ćete:

- Kreirati klijenta s LLM-om.
- Besprijekorno komunicirati s MCP serverom koristeći LLM.
- Pružiti bolje korisničko iskustvo na strani klijenta.

## Pristup

Pokušajmo razumjeti pristup koji trebamo poduzeti. Dodavanje LLM-a zvuči jednostavno, ali kako to zapravo učiniti?

Evo kako će klijent komunicirati sa serverom:

1. Uspostaviti vezu sa serverom.

1. Popisati mogućnosti, upite, resurse i alate te ih spremiti prema njihovoj shemi.

1. Dodati LLM i proslijediti spremljene mogućnosti i njihove sheme u formatu koji LLM razumije.

1. Obraditi korisnički upit prosljeđujući ga LLM-u zajedno s alatima koje je klijent popisao.

Odlično, sada razumijemo kako to možemo učiniti na visokoj razini, pokušajmo to u sljedećoj vježbi.

## Vježba: Kreiranje klijenta s LLM-om

U ovoj vježbi naučit ćemo kako dodati LLM našem klijentu.

### Autentifikacija pomoću GitHub osobnog pristupnog tokena

Kreiranje GitHub tokena je jednostavan proces. Evo kako to možete učiniti:

- Idite na GitHub postavke – Kliknite na svoju profilnu sliku u gornjem desnom kutu i odaberite Settings.
- Navigirajte do Developer Settings – Pomaknite se dolje i kliknite na Developer Settings.
- Odaberite Personal Access Tokens – Kliknite na Fine-grained tokens, a zatim Generate new token.
- Konfigurirajte svoj token – Dodajte bilješku za referencu, postavite datum isteka i odaberite potrebne opsege (dozvole). U ovom slučaju, obavezno dodajte Models dozvolu.
- Generirajte i kopirajte token – Kliknite Generate token i obavezno ga odmah kopirajte jer ga kasnije nećete moći vidjeti.

### -1- Povezivanje sa serverom

Prvo kreirajmo našeg klijenta:

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

U prethodnom kodu smo:

- Uvezli potrebne biblioteke.
- Kreirali klasu s dva člana, `client` i `openai`, koji će nam pomoći upravljati klijentom i komunicirati s LLM-om.
- Konfigurirali našu LLM instancu za korištenje GitHub Models postavljanjem `baseUrl` da pokazuje na inference API.

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

U prethodnom kodu smo:

- Uvezli potrebne biblioteke za MCP.
- Kreirali klijenta.

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

Prvo, trebate dodati LangChain4j ovisnosti u svoj `pom.xml` file. Dodajte ove ovisnosti kako biste omogućili MCP integraciju i podršku za GitHub Models:

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

Zatim kreirajte svoju Java klijent klasu:

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

U prethodnom kodu smo:

- **Dodali LangChain4j ovisnosti**: Potrebne za MCP integraciju, službeni OpenAI klijent i podršku za GitHub Models.
- **Uvezli LangChain4j biblioteke**: Za MCP integraciju i funkcionalnost OpenAI chat modela.
- **Kreirali `ChatLanguageModel`**: Konfiguriran za korištenje GitHub Models s vašim GitHub tokenom.
- **Postavili HTTP transport**: Koristeći Server-Sent Events (SSE) za povezivanje s MCP serverom.
- **Kreirali MCP klijenta**: Koji će upravljati komunikacijom sa serverom.
- **Koristili ugrađenu MCP podršku LangChain4j-a**: Koja pojednostavljuje integraciju između LLM-ova i MCP servera.

#### Rust

Ovaj primjer pretpostavlja da imate MCP server baziran na Rustu koji radi. Ako ga nemate, pogledajte lekciju [01-first-server](../01-first-server/README.md) kako biste kreirali server.

Kada imate svoj Rust MCP server, otvorite terminal i navigirajte do istog direktorija kao server. Zatim pokrenite sljedeću naredbu za kreiranje novog LLM klijent projekta:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Dodajte sljedeće ovisnosti u svoj `Cargo.toml` file:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Ne postoji službena Rust biblioteka za OpenAI, međutim, `async-openai` crate je [biblioteka koju održava zajednica](https://platform.openai.com/docs/libraries/rust#rust) i često se koristi.

Otvorite `src/main.rs` file i zamijenite njegov sadržaj sljedećim kodom:

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

Ovaj kod postavlja osnovnu Rust aplikaciju koja će se povezati s MCP serverom i GitHub Models za interakcije s LLM-om.

> [!IMPORTANT]
> Obavezno postavite `OPENAI_API_KEY` varijablu okruženja s vašim GitHub tokenom prije pokretanja aplikacije.

Odlično, za naš sljedeći korak, popisat ćemo mogućnosti na serveru.

### -2- Popis mogućnosti servera

Sada ćemo se povezati sa serverom i zatražiti njegove mogućnosti:

#### TypeScript

U istoj klasi dodajte sljedeće metode:

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

U prethodnom kodu smo:

- Dodali kod za povezivanje sa serverom, `connectToServer`.
- Kreirali `run` metodu odgovornu za upravljanje tokom aplikacije. Za sada samo popisuje alate, ali uskoro ćemo dodati više.

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

Evo što smo dodali:

- Popis resursa i alata te ih ispisali. Za alate također popisujemo `inputSchema` koji ćemo kasnije koristiti.

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

U prethodnom kodu smo:

- Popisali dostupne alate na MCP serveru.
- Za svaki alat popisali ime, opis i njegovu shemu. Potonju ćemo koristiti za pozivanje alata uskoro.

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

U prethodnom kodu smo:

- Kreirali `McpToolProvider` koji automatski otkriva i registrira sve alate s MCP servera.
- Provider alata interno upravlja konverzijom između MCP shema alata i LangChain4j formata alata.
- Ovaj pristup apstrahira ručno popisivanje alata i proces konverzije.

#### Rust

Dobivanje alata s MCP servera obavlja se pomoću metode `list_tools`. U vašoj `main` funkciji, nakon postavljanja MCP klijenta, dodajte sljedeći kod:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Konverzija mogućnosti servera u LLM alate

Sljedeći korak nakon popisivanja mogućnosti servera je njihova konverzija u format koji LLM razumije. Kada to učinimo, možemo te mogućnosti pružiti kao alate LLM-u.

#### TypeScript

1. Dodajte sljedeći kod za konverziju odgovora MCP servera u format alata koji LLM može koristiti:

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

    Gornji kod uzima odgovor MCP servera i konvertira ga u definiciju alata koju LLM može razumjeti.

1. Ažurirajmo `run` metodu kako bismo popisali mogućnosti servera:

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

    U prethodnom kodu smo ažurirali `run` metodu da prolazi kroz rezultat i za svaki unos poziva `openAiToolAdapter`.

#### Python

1. Prvo, kreirajmo sljedeću funkciju za konverziju:

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

    U funkciji `convert_to_llm_tools` uzimamo MCP odgovor alata i konvertiramo ga u format koji LLM može razumjeti.

1. Zatim, ažurirajmo naš klijent kod kako bismo iskoristili ovu funkciju ovako:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Ovdje dodajemo poziv `convert_to_llm_tool` za konverziju MCP odgovora alata u nešto što kasnije možemo proslijediti LLM-u.

#### .NET

1. Dodajmo kod za konverziju MCP odgovora alata u nešto što LLM može razumjeti:

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

U prethodnom kodu smo:

- Kreirali funkciju `ConvertFrom` koja uzima ime, opis i shemu unosa.
- Definirali funkcionalnost koja kreira FunctionDefinition koji se prosljeđuje ChatCompletionsDefinition. Potonji je nešto što LLM može razumjeti.

1. Pogledajmo kako možemo ažurirati postojeći kod kako bismo iskoristili ovu funkciju:

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

U prethodnom kodu smo:

- Definirali jednostavno `Bot` sučelje za interakcije prirodnim jezikom.
- Koristili LangChain4j `AiServices` za automatsko povezivanje LLM-a s providerom alata MCP-a.
- Framework automatski upravlja konverzijom shema alata i pozivanjem funkcija u pozadini.
- Ovaj pristup eliminira ručnu konverziju alata - LangChain4j upravlja svim složenostima konverzije MCP alata u format kompatibilan s LLM-om.

#### Rust

Za konverziju MCP odgovora alata u format koji LLM može razumjeti, dodati ćemo pomoćnu funkciju koja formatira popis alata. Dodajte sljedeći kod u vaš `main.rs` file ispod `main` funkcije. Ovo će se pozvati prilikom slanja zahtjeva LLM-u:

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

Odlično, sada smo spremni za obradu korisničkih zahtjeva, pa krenimo na to.

### -4- Obrada korisničkog upita

U ovom dijelu koda obradit ćemo korisničke zahtjeve.

#### TypeScript

1. Dodajte metodu koja će se koristiti za pozivanje našeg LLM-a:

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

    U prethodnom kodu smo:

    - Dodali metodu `callTools`.
    - Metoda uzima LLM odgovor i provjerava koji alati su pozvani, ako ih ima:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Poziva alat, ako LLM naznači da bi trebao biti pozvan:

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

1. Ažurirajte `run` metodu kako biste uključili pozive LLM-u i pozivanje `callTools`:

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

Odlično, evo cijelog koda:

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

1. Dodajmo neke uvoze potrebne za pozivanje LLM-a:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Zatim, dodajmo funkciju koja će pozvati LLM:

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

    U prethodnom kodu smo:

    - Proslijedili naše funkcije, koje smo pronašli na MCP serveru i konvertirali, LLM-u.
    - Zatim pozvali LLM s navedenim funkcijama.
    - Zatim provjeravamo rezultat kako bismo vidjeli koje funkcije trebamo pozvati, ako ih ima.
    - Na kraju, prosljeđujemo niz funkcija za pozivanje.

1. Posljednji korak, ažurirajmo naš glavni kod:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Tamo, to je bio posljednji korak, u kodu iznad:

    - Pozivamo MCP alat putem `call_tool` koristeći funkciju koju je LLM smatrao da trebamo pozvati na temelju našeg upita.
    - Ispisujemo rezultat poziva alata na MCP server.

#### .NET

1. Prikažimo kod za slanje zahtjeva LLM-u:

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

    U prethodnom kodu smo:

    - Dohvatili alate s MCP servera, `var tools = await GetMcpTools()`.
    - Definirali korisnički upit `userMessage`.
    - Konstruirali objekt opcija koji specificira model i alate.
    - Poslali zahtjev prema LLM-u.

1. Posljednji korak, provjerimo misli li LLM da trebamo pozvati funkciju:

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

    U prethodnom kodu smo:

    - Prošli kroz popis poziva funkcija.
    - Za svaki poziv alata, izdvojili ime i argumente te pozvali alat na MCP serveru koristeći MCP klijent. Na kraju ispisujemo rezultate.

Evo cijelog koda:

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

U prethodnom kodu smo:

- Koristili jednostavne upite prirodnim jezikom za interakciju s MCP alatima servera.
- LangChain4j framework automatski upravlja:
  - Konverzijom korisničkih upita u pozive alata kada je potrebno.
  - Pozivanjem odgovarajućih MCP alata na temelju odluke LLM-a.
  - Upravljanjem toka razgovora između LLM-a i MCP servera.
- Metoda `bot.chat()` vraća odgovore prirodnim jezikom koji mogu uključivati rezultate izvršenja MCP alata.
- Ovaj pristup pruža besprijekorno korisničko iskustvo gdje korisnici ne moraju znati o temeljnoj MCP implementaciji.

Kompletan primjer koda:

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

Ovdje se odvija većina posla. Pozvat ćemo LLM s početnim korisničkim upitom, zatim obraditi odgovor kako bismo vidjeli treba li pozvati neke alate. Ako je tako, pozvat ćemo te alate i nastaviti razgovor s LLM-om dok ne bude potrebno više poziva alata i dok ne dobijemo konačni odgovor.

Budući da ćemo više puta pozivati LLM, definirajmo funkciju koja će upravljati pozivom LLM-u. Dodajte sljedeću funkciju u vaš `main.rs` file:

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

Ova funkcija uzima LLM klijent, popis poruka (uključujući korisnički upit), alate s MCP servera i šalje zahtjev LLM-u, vraćajući odgovor.
Odgovor od LLM-a sadržavat će niz `choices`. Trebat ćemo obraditi rezultat kako bismo provjerili postoje li `tool_calls`. Ovo nam daje do znanja da LLM traži pozivanje određenog alata s argumentima. Dodajte sljedeći kod na dno vaše datoteke `main.rs` kako biste definirali funkciju za obradu odgovora LLM-a:

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

Ako su prisutni `tool_calls`, funkcija izvlači informacije o alatu, poziva MCP poslužitelj s zahtjevom za alat i dodaje rezultate u poruke razgovora. Zatim nastavlja razgovor s LLM-om, a poruke se ažuriraju s odgovorom asistenta i rezultatima poziva alata.

Kako bismo izdvojili informacije o pozivu alata koje LLM vraća za MCP pozive, dodat ćemo još jednu pomoćnu funkciju za izdvajanje svega potrebnog za izvršenje poziva. Dodajte sljedeći kod na dno vaše datoteke `main.rs`:

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

Sada kada su svi dijelovi na mjestu, možemo obraditi početni korisnički upit i pozvati LLM. Ažurirajte svoju funkciju `main` kako biste uključili sljedeći kod:

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

Ovo će poslati upit LLM-u s početnim korisničkim upitom koji traži zbroj dva broja i obraditi odgovor kako bi dinamički upravljalo pozivima alata.

Odlično, uspjeli ste!

## Zadatak

Uzmite kod iz vježbe i proširite poslužitelj s još nekoliko alata. Zatim izradite klijent s LLM-om, kao u vježbi, i testirajte ga s različitim upitima kako biste bili sigurni da se svi alati vašeg poslužitelja dinamički pozivaju. Ovakav način izrade klijenta omogućuje krajnjem korisniku izvrsno korisničko iskustvo jer može koristiti upite umjesto točnih klijentskih naredbi, a da nije svjestan da se MCP poslužitelj poziva.

## Rješenje

[Rješenje](/03-GettingStarted/03-llm-client/solution/README.md)

## Ključne točke

- Dodavanje LLM-a vašem klijentu pruža bolji način za interakciju s MCP poslužiteljima.
- Potrebno je pretvoriti odgovor MCP poslužitelja u nešto što LLM može razumjeti.

## Primjeri

- [Java Kalkulator](../samples/java/calculator/README.md)
- [.Net Kalkulator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Kalkulator](../samples/javascript/README.md)
- [TypeScript Kalkulator](../samples/typescript/README.md)
- [Python Kalkulator](../../../../03-GettingStarted/samples/python)
- [Rust Kalkulator](../../../../03-GettingStarted/samples/rust)

## Dodatni resursi

## Što slijedi

- Sljedeće: [Korištenje poslužitelja pomoću Visual Studio Code-a](../04-vscode/README.md)

---

**Odricanje od odgovornosti**:  
Ovaj dokument je preveden pomoću AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za ključne informacije preporučuje se profesionalni prijevod od strane čovjeka. Ne preuzimamo odgovornost za nesporazume ili pogrešna tumačenja koja mogu proizaći iz korištenja ovog prijevoda.