<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T15:03:22+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "hu"
}
-->
# LLM kliens létrehozása

Eddig láthattad, hogyan hozhatsz létre szervert és klienst. A kliens képes volt kifejezetten hívni a szervert, hogy listázza az eszközeit, erőforrásait és promptjait. Ez azonban nem túl praktikus megközelítés. A felhasználóid az ügynöki korszakban élnek, és azt várják, hogy promptokat használjanak, és egy LLM-mel kommunikáljanak. Számukra nem számít, hogy MCP-t használsz-e a képességeid tárolására, de elvárják, hogy természetes nyelven kommunikáljanak. Hogyan oldjuk meg ezt? A megoldás az, hogy egy LLM-et adunk a klienshez.

## Áttekintés

Ebben a leckében arra koncentrálunk, hogyan adjunk hozzá egy LLM-et a klienshez, és bemutatjuk, hogy ez hogyan biztosít sokkal jobb élményt a felhasználóid számára.

## Tanulási célok

A lecke végére képes leszel:

- Létrehozni egy LLM-mel rendelkező klienst.
- Zökkenőmentesen kommunikálni egy MCP szerverrel egy LLM segítségével.
- Jobb felhasználói élményt nyújtani a kliens oldalon.

## Megközelítés

Próbáljuk megérteni, milyen megközelítést kell alkalmaznunk. Egy LLM hozzáadása egyszerűnek hangzik, de tényleg így van?

Így fog a kliens kommunikálni a szerverrel:

1. Kapcsolatot létesít a szerverrel.

1. Listázza a képességeket, promptokat, erőforrásokat és eszközöket, majd elmenti azok sémáját.

1. Hozzáad egy LLM-et, és átadja a mentett képességeket és azok sémáját olyan formátumban, amelyet az LLM megért.

1. Kezeli a felhasználói promptot úgy, hogy átadja azt az LLM-nek az eszközökkel együtt, amelyeket a kliens listázott.

Nagyszerű, most már értjük, hogyan valósíthatjuk meg ezt magas szinten. Próbáljuk ki az alábbi gyakorlatban.

## Gyakorlat: LLM-mel rendelkező kliens létrehozása

Ebben a gyakorlatban megtanuljuk, hogyan adjunk hozzá egy LLM-et a kliensünkhöz.

### Hitelesítés GitHub személyes hozzáférési tokennel

GitHub token létrehozása egyszerű folyamat. Így teheted meg:

- Menj a GitHub Beállításokhoz – Kattints a profilképedre a jobb felső sarokban, majd válaszd a Beállítások lehetőséget.
- Navigálj a Fejlesztői Beállításokhoz – Görgess le, és kattints a Fejlesztői Beállítások lehetőségre.
- Válaszd a Személyes Hozzáférési Tokeneket – Kattints a Finomhangolt tokenekre, majd válaszd az Új token létrehozása lehetőséget.
- Konfiguráld a tokenedet – Adj hozzá egy megjegyzést referenciaként, állíts be lejárati dátumot, és válaszd ki a szükséges jogosultságokat (engedélyeket). Ebben az esetben győződj meg róla, hogy hozzáadod a Modellek engedélyt.
- Generáld és másold a tokent – Kattints a Token generálása gombra, és győződj meg róla, hogy azonnal lemásolod, mivel később nem fogod tudni újra megtekinteni.

### -1- Kapcsolódás a szerverhez

Először hozzuk létre a kliensünket:

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

A fenti kódban:

- Importáltuk a szükséges könyvtárakat.
- Létrehoztunk egy osztályt két taggal, `client` és `openai`, amelyek segítenek a kliens kezelésében és az LLM-mel való interakcióban.
- Konfiguráltuk az LLM példányt, hogy a GitHub Modelleket használja, beállítva a `baseUrl`-t az inference API-ra mutató értékre.

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

A fenti kódban:

- Importáltuk az MCP-hez szükséges könyvtárakat.
- Létrehoztunk egy klienst.

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

Először hozzá kell adnod a LangChain4j függőségeket a `pom.xml` fájlodhoz. Add hozzá ezeket a függőségeket az MCP integráció és a GitHub Modellek támogatásának engedélyezéséhez:

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

Ezután hozd létre a Java kliens osztályodat:

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

A fenti kódban:

- **Hozzáadtuk a LangChain4j függőségeket**: Szükséges az MCP integrációhoz, az OpenAI hivatalos klienséhez és a GitHub Modellek támogatásához.
- **Importáltuk a LangChain4j könyvtárakat**: Az MCP integrációhoz és az OpenAI chat modell funkcionalitásához.
- **Létrehoztunk egy `ChatLanguageModel`-t**: Konfiguráltuk, hogy a GitHub Modelleket használja a GitHub tokeneddel.
- **Beállítottuk a HTTP transportot**: Server-Sent Events (SSE) használatával kapcsolódunk az MCP szerverhez.
- **Létrehoztunk egy MCP klienst**: Ez kezeli a kommunikációt a szerverrel.
- **Használtuk a LangChain4j beépített MCP támogatását**: Ez leegyszerűsíti az LLM-ek és MCP szerverek közötti integrációt.

#### Rust

Ez a példa feltételezi, hogy van egy Rust alapú MCP szervered. Ha nincs, térj vissza az [01-first-server](../01-first-server/README.md) leckéhez, hogy létrehozd a szervert.

Miután megvan a Rust MCP szervered, nyiss meg egy terminált, és navigálj ugyanabba a könyvtárba, mint a szerver. Ezután futtasd az alábbi parancsot egy új LLM kliens projekt létrehozásához:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Add hozzá a következő függőségeket a `Cargo.toml` fájlodhoz:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Nincs hivatalos Rust könyvtár az OpenAI-hoz, azonban az `async-openai` crate egy [közösség által karbantartott könyvtár](https://platform.openai.com/docs/libraries/rust#rust), amelyet gyakran használnak.

Nyisd meg a `src/main.rs` fájlt, és cseréld le a tartalmát az alábbi kódra:

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

Ez a kód egy alapvető Rust alkalmazást állít be, amely kapcsolódik egy MCP szerverhez és a GitHub Modellekhez az LLM interakciókhoz.

> [!IMPORTANT]
> Győződj meg róla, hogy beállítod az `OPENAI_API_KEY` környezeti változót a GitHub tokeneddel, mielőtt futtatnád az alkalmazást.

Nagyszerű, a következő lépésben listázzuk a szerver képességeit.

### -2- A szerver képességeinek listázása

Most csatlakozunk a szerverhez, és kérjük a képességeit:

#### TypeScript

Ugyanabban az osztályban add hozzá a következő metódusokat:

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

A fenti kódban:

- Hozzáadtuk a kódot a szerverhez való csatlakozáshoz, `connectToServer`.
- Létrehoztunk egy `run` metódust, amely felelős az alkalmazásunk folyamatának kezeléséért. Eddig csak az eszközöket listázza, de hamarosan többet adunk hozzá.

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

Amit hozzáadtunk:

- Listáztuk az erőforrásokat és eszközöket, majd kiírtuk őket. Az eszközöknél az `inputSchema`-t is listázzuk, amelyet később használunk.

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

A fenti kódban:

- Listáztuk az MCP szerveren elérhető eszközöket.
- Minden eszköznél listáztuk a nevet, leírást és annak sémáját. Ez utóbbit hamarosan használni fogjuk az eszközök hívásához.

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

A fenti kódban:

- Létrehoztunk egy `McpToolProvider`-t, amely automatikusan felfedezi és regisztrálja az összes eszközt az MCP szerverről.
- Az eszközszolgáltató belsőleg kezeli az MCP eszközsémák és a LangChain4j eszközformátum közötti átalakítást.
- Ez a megközelítés elvonja a manuális eszközlistázás és átalakítás folyamatát.

#### Rust

Az MCP szerverről származó eszközök lekérése a `list_tools` metódussal történik. A `main` függvényedben, miután beállítottad az MCP klienst, add hozzá a következő kódot:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- A szerver képességeinek átalakítása LLM eszközökké

A szerver képességeinek listázása után a következő lépés az, hogy átalakítsuk őket olyan formátumba, amelyet az LLM megért. Miután ezt megtettük, ezeket a képességeket eszközökként tudjuk biztosítani az LLM számára.

#### TypeScript

1. Add hozzá a következő kódot, amely átalakítja az MCP szerver válaszát egy olyan eszközformátumba, amelyet az LLM használhat:

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

    A fenti kód az MCP szerver válaszát egy eszközdefiníciós formátumba alakítja, amelyet az LLM megért.

1. Frissítsük a `run` metódust, hogy listázza a szerver képességeit:

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

    A fenti kódban frissítettük a `run` metódust, hogy végigmenjen az eredményen, és minden bejegyzéshez hívja az `openAiToolAdapter`-t.

#### Python

1. Először hozzuk létre a következő átalakító függvényt:

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

    A fenti `convert_to_llm_tools` függvényben az MCP eszközválaszt átalakítjuk olyan formátumba, amelyet az LLM megért.

1. Ezután frissítsük a klienskódunkat, hogy kihasználja ezt a függvényt, így:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Itt hozzáadunk egy hívást a `convert_to_llm_tool`-hoz, hogy az MCP eszközválaszt olyan formátumba alakítsuk, amelyet később az LLM-nek tudunk átadni.

#### .NET

1. Adjunk hozzá kódot az MCP eszközválasz átalakításához olyan formátumba, amelyet az LLM megért:

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

A fenti kódban:

- Létrehoztunk egy `ConvertFrom` függvényt, amely nevet, leírást és bemeneti sémát vesz át.
- Meghatároztuk a funkcionalitást, amely létrehoz egy FunctionDefinition-t, amelyet egy ChatCompletionsDefinition-nek adunk át. Ez utóbbi az, amit az LLM megért.

1. Nézzük meg, hogyan frissíthetünk néhány meglévő kódot, hogy kihasználjuk a fenti függvényt:

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

A fenti kódban:

- Meghatároztunk egy egyszerű `Bot` interfészt a természetes nyelvi interakciókhoz.
- Használtuk a LangChain4j `AiServices`-t, hogy automatikusan összekapcsoljuk az LLM-et az MCP eszközszolgáltatóval.
- A keretrendszer automatikusan kezeli az eszközséma átalakítást és a funkcióhívásokat a háttérben.
- Ez a megközelítés kiküszöböli a manuális eszközátalakítást - a LangChain4j kezeli az MCP eszközök LLM-kompatibilis formátumba való átalakításának összes bonyolultságát.

#### Rust

Az MCP eszközválasz olyan formátumba való átalakításához, amelyet az LLM megért, hozzáadunk egy segédfüggvényt, amely formázza az eszközlistát. Add hozzá a következő kódot a `main.rs` fájlodhoz a `main` függvény alá. Ezt akkor hívjuk meg, amikor kéréseket teszünk az LLM-hez:

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

Nagyszerű, most már készen állunk a felhasználói kérések kezelésére, így foglalkozzunk ezzel a következő lépésben.

### -4- Felhasználói prompt kérés kezelése

Ebben a kódrészben a felhasználói kéréseket fogjuk kezelni.

#### TypeScript

1. Adjunk hozzá egy metódust, amelyet az LLM hívására használunk:

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

    A fenti kódban:

    - Hozzáadtunk egy `callTools` metódust.
    - A metódus veszi az LLM válaszát, és ellenőrzi, hogy milyen eszközöket kell hívni, ha vannak ilyenek:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Meghív egy eszközt, ha az LLM jelzi, hogy hívni kell:

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

1. Frissítsük a `run` metódust, hogy tartalmazza az LLM hívásokat és a `callTools` hívását:

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

Nagyszerű, nézzük meg a teljes kódot:

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

1. Adjunk hozzá néhány importot, amelyek szükségesek az LLM hívásához:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Ezután adjuk hozzá a függvényt, amely az LLM-et hívja:

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

    A fenti kódban:

    - Átadtuk az MCP szerveren talált és átalakított funkciókat az LLM-nek.
    - Ezután hívtuk az LLM-et ezekkel a funkciókkal.
    - Ezután megvizsgáljuk az eredményt, hogy lássuk, milyen funkciókat kell hívni, ha vannak ilyenek.
    - Végül átadunk egy funkciókat tartalmazó tömböt a híváshoz.

1. Utolsó lépésként frissítsük a fő kódunkat:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Ott van, ez volt az utolsó lépés. A fenti kódban:

    - Meghívunk egy MCP eszközt a `call_tool` segítségével, egy olyan funkcióval, amelyet az LLM gondolt, hogy hívni kell a promptunk alapján.
    - Kiírjuk az MCP szerver eszközhívásának eredményét.

#### .NET

1. Mutassunk néhány kódot egy LLM prompt kéréshez:

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

    A fenti kódban:

    - Lekértük az eszközöket az MCP szerverről, `var tools = await GetMcpTools()`.
    - Meghatároztunk egy felhasználói promptot, `userMessage`.
    - Létrehoztunk egy opciós objektumot, amely megadja a modellt és az eszközöket.
    - Kérést tettünk az LLM felé.

1. Egy utolsó lépés, nézzük meg, hogy az LLM szerint hívnunk kell-e egy funkciót:

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

    A fenti kódban:

    - Végigmentünk egy funkcióhívások listáján.
    - Minden eszközhívásnál kinyertük a nevet és az argumentumokat, majd meghívtuk az eszközt az MCP szerveren az MCP kliens segítségével. Végül kiírtuk az eredményeket.

Itt a teljes kód:

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

A fenti kódban:

- Egyszerű természetes nyelvi promptokat használtunk az MCP szerver eszközeivel való interakcióhoz.
- A LangChain4j keretrendszer automatikusan kezeli:
  - A felhasználói promptok eszközhívás
Az LLM válasza egy `choices` tömböt fog tartalmazni. A kapott eredményt fel kell dolgoznunk, hogy megállapítsuk, vannak-e `tool_calls`. Ez jelzi, hogy az LLM egy konkrét eszköz használatát kéri argumentumokkal. Adja hozzá az alábbi kódot a `main.rs` fájl végéhez, hogy definiáljon egy függvényt az LLM válaszának kezelésére:

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

Ha `tool_calls` jelen vannak, a kód kinyeri az eszköz információit, meghívja az MCP szervert az eszköz kérésével, és hozzáadja az eredményeket a beszélgetési üzenetekhez. Ezután folytatja a beszélgetést az LLM-mel, és az üzenetek frissülnek az asszisztens válaszával és az eszköz hívás eredményeivel.

Az MCP hívásokhoz szükséges eszköz hívási információk kinyeréséhez hozzáadunk egy segédfüggvényt, amely mindent kinyer, ami a híváshoz szükséges. Adja hozzá az alábbi kódot a `main.rs` fájl végéhez:

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

Most, hogy minden szükséges elem rendelkezésre áll, kezelhetjük a kezdeti felhasználói promptot és meghívhatjuk az LLM-et. Frissítse a `main` függvényt az alábbi kód hozzáadásával:

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

Ez lekérdezi az LLM-et a kezdeti felhasználói prompttal, amely két szám összegét kéri, és feldolgozza a választ, hogy dinamikusan kezelje az eszköz hívásokat.

Nagyszerű, sikerült!

## Feladat

Vegye az eddigi gyakorlatban használt kódot, és építse ki a szervert további eszközökkel. Ezután hozzon létre egy LLM-et használó klienst, mint a gyakorlatban, és tesztelje különböző promptokkal, hogy megbizonyosodjon arról, hogy az összes szerver eszköz dinamikusan meghívható. Ez a kliensépítési módszer kiváló felhasználói élményt biztosít, mivel a végfelhasználó promptokat használhat, ahelyett, hogy pontos kliens parancsokat adna meg, és nem kell tudnia az MCP szerver hívásairól.

## Megoldás

[Megoldás](/03-GettingStarted/03-llm-client/solution/README.md)

## Fő tanulságok

- Az LLM hozzáadása a klienshez jobb módot biztosít a felhasználóknak az MCP szerverekkel való interakcióra.
- Az MCP szerver válaszát olyan formátumra kell alakítani, amelyet az LLM megért.

## Minták

- [Java Kalkulátor](../samples/java/calculator/README.md)
- [.Net Kalkulátor](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Kalkulátor](../samples/javascript/README.md)
- [TypeScript Kalkulátor](../samples/typescript/README.md)
- [Python Kalkulátor](../../../../03-GettingStarted/samples/python)
- [Rust Kalkulátor](../../../../03-GettingStarted/samples/rust)

## További források

## Mi következik?

- Következő: [Szerver használata Visual Studio Code segítségével](../04-vscode/README.md)

---

**Felelősség kizárása**:  
Ez a dokumentum az [Co-op Translator](https://github.com/Azure/co-op-translator) AI fordítási szolgáltatás segítségével került lefordításra. Bár törekszünk a pontosságra, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az eredeti nyelvén tekintendő hiteles forrásnak. Fontos információk esetén javasolt professzionális emberi fordítást igénybe venni. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely a fordítás használatából eredhet.