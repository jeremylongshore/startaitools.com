<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:39:16+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "fi"
}
-->
# Luominen asiakasohjelma LLM:n avulla

Tähän mennessä olet nähnyt, kuinka luodaan palvelin ja asiakasohjelma. Asiakasohjelma on voinut kutsua palvelinta eksplisiittisesti listatakseen sen työkalut, resurssit ja kehotteet. Tämä ei kuitenkaan ole kovin käytännöllinen lähestymistapa. Käyttäjäsi elää agenttien aikakaudella ja odottaa voivansa käyttää kehotteita ja kommunikoida LLM:n kanssa. Käyttäjääsi ei kiinnosta, käytätkö MCP:tä kykyjesi tallentamiseen, mutta hän odottaa voivansa käyttää luonnollista kieltä vuorovaikutukseen. Kuinka tämä ratkaistaan? Ratkaisu on lisätä LLM asiakasohjelmaan.

## Yleiskatsaus

Tässä oppitunnissa keskitymme LLM:n lisäämiseen asiakasohjelmaan ja näytämme, kuinka tämä parantaa käyttäjäkokemusta.

## Oppimistavoitteet

Oppitunnin lopussa osaat:

- Luoda asiakasohjelman, jossa on LLM.
- Vuorovaikuttaa saumattomasti MCP-palvelimen kanssa LLM:n avulla.
- Tarjota paremman loppukäyttäjäkokemuksen asiakasohjelman puolella.

## Lähestymistapa

Yritetään ymmärtää, mitä lähestymistapaa meidän tulee käyttää. LLM:n lisääminen kuulostaa yksinkertaiselta, mutta miten se oikeasti tehdään?

Näin asiakasohjelma vuorovaikuttaa palvelimen kanssa:

1. Yhdistä palvelimeen.

1. Listaa kyvyt, kehotteet, resurssit ja työkalut, ja tallenna niiden skeema.

1. Lisää LLM ja välitä tallennetut kyvyt ja niiden skeema muodossa, jonka LLM ymmärtää.

1. Käsittele käyttäjän kehotetta välittämällä se LLM:lle yhdessä asiakasohjelman listaamien työkalujen kanssa.

Hienoa, nyt ymmärrämme, kuinka tämä tehdään yleisellä tasolla. Kokeillaan tätä seuraavassa harjoituksessa.

## Harjoitus: Asiakasohjelman luominen LLM:n avulla

Tässä harjoituksessa opimme lisäämään LLM:n asiakasohjelmaan.

### Autentikointi GitHubin henkilökohtaisen käyttöoikeustunnuksen avulla

GitHub-tunnuksen luominen on yksinkertainen prosessi. Näin se tehdään:

- Siirry GitHub-asetuksiin – Klikkaa profiilikuvaasi oikeassa yläkulmassa ja valitse Asetukset.
- Siirry Kehittäjäasetuksiin – Vieritä alas ja klikkaa Kehittäjäasetukset.
- Valitse Henkilökohtaiset käyttöoikeustunnukset – Klikkaa Tarkasti määritellyt tunnukset ja sitten Luo uusi tunnus.
- Määritä tunnuksesi – Lisää viitehuomautus, aseta vanhenemispäivä ja valitse tarvittavat käyttöoikeudet (lupat). Tässä tapauksessa varmista, että lisäät Mallit-käyttöoikeuden.
- Luo ja kopioi tunnus – Klikkaa Luo tunnus ja varmista, että kopioit sen heti, sillä et voi nähdä sitä uudelleen.

### -1- Yhdistä palvelimeen

Luodaan ensin asiakasohjelma:

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

Edellä olevassa koodissa olemme:

- Tuoneet tarvittavat kirjastot.
- Luoneet luokan, jossa on kaksi jäsentä, `client` ja `openai`, jotka auttavat hallitsemaan asiakasohjelmaa ja vuorovaikuttamaan LLM:n kanssa.
- Konfiguroineet LLM-instanssin käyttämään GitHub-malleja asettamalla `baseUrl` osoittamaan inferenssi-API:hen.

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

Edellä olevassa koodissa olemme:

- Tuoneet tarvittavat MCP-kirjastot.
- Luoneet asiakasohjelman.

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

Ensiksi sinun täytyy lisätä LangChain4j-riippuvuudet `pom.xml`-tiedostoosi. Lisää nämä riippuvuudet mahdollistamaan MCP-integraatio ja GitHub-mallien tuki:

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

Luo sitten Java-asiakasohjelmaluokka:

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

Edellä olevassa koodissa olemme:

- **Lisänneet LangChain4j-riippuvuudet**: Tarvitaan MCP-integraatioon, OpenAI:n viralliseen asiakasohjelmaan ja GitHub-mallien tukeen.
- **Tuoneet LangChain4j-kirjastot**: MCP-integraatiota ja OpenAI:n chat-mallin toiminnallisuutta varten.
- **Luoneet `ChatLanguageModel`**: Konfiguroitu käyttämään GitHub-malleja GitHub-tunnuksesi avulla.
- **Asettaneet HTTP-siirron**: Käyttäen Server-Sent Events (SSE) -tekniikkaa MCP-palvelimeen yhdistämiseen.
- **Luoneet MCP-asiakasohjelman**: Joka hoitaa kommunikoinnin palvelimen kanssa.
- **Käyttäneet LangChain4j:n sisäänrakennettua MCP-tukea**: Joka yksinkertaistaa LLM:n ja MCP-palvelimien välistä integraatiota.

#### Rust

Tämä esimerkki olettaa, että sinulla on Rust-pohjainen MCP-palvelin käynnissä. Jos sinulla ei ole sellaista, katso [01-first-server](../01-first-server/README.md) -oppitunti palvelimen luomiseksi.

Kun sinulla on Rust MCP-palvelin, avaa terminaali ja siirry samaan hakemistoon kuin palvelin. Suorita sitten seuraava komento luodaksesi uuden LLM-asiakasohjelmaprojektin:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Lisää seuraavat riippuvuudet `Cargo.toml`-tiedostoosi:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Rustille ei ole virallista OpenAI-kirjastoa, mutta `async-openai`-paketti on [yhteisön ylläpitämä kirjasto](https://platform.openai.com/docs/libraries/rust#rust), jota käytetään yleisesti.

Avaa `src/main.rs`-tiedosto ja korvaa sen sisältö seuraavalla koodilla:

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

Tämä koodi asettaa perus Rust-sovelluksen, joka yhdistää MCP-palvelimeen ja GitHub-malleihin LLM-vuorovaikutusta varten.

> [!IMPORTANT]
> Varmista, että asetat `OPENAI_API_KEY` -ympäristömuuttujan GitHub-tunnuksesi avulla ennen sovelluksen suorittamista.

Hienoa, seuraavaksi listataan palvelimen kyvyt.

### -2- Listaa palvelimen kyvyt

Nyt yhdistämme palvelimeen ja kysymme sen kykyjä:

#### TypeScript

Lisää samaan luokkaan seuraavat metodit:

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

Edellä olevassa koodissa olemme:

- Lisänneet koodin palvelimeen yhdistämiseen, `connectToServer`.
- Luoneet `run`-metodin, joka vastaa sovelluksen kulun hallinnasta. Tällä hetkellä se vain listaa työkalut, mutta lisäämme siihen pian lisää.

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

Tässä olemme lisänneet:

- Resurssien ja työkalujen listaamisen ja niiden tulostamisen. Työkaluista listaamme myös `inputSchema`, jota käytämme myöhemmin.

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

Edellä olevassa koodissa olemme:

- Listanneet MCP-palvelimen saatavilla olevat työkalut.
- Jokaiselle työkalulle listanneet nimen, kuvauksen ja sen skeeman. Jälkimmäistä käytämme työkalujen kutsumiseen pian.

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

Edellä olevassa koodissa olemme:

- Luoneet `McpToolProvider`-luokan, joka automaattisesti löytää ja rekisteröi kaikki työkalut MCP-palvelimelta.
- Työkaluntarjoaja hoitaa MCP-työkaluskeemojen ja LangChain4j:n työkalumuodon välisen muunnoksen sisäisesti.
- Tämä lähestymistapa abstrahoi manuaalisen työkalujen listaamisen ja muunnosprosessin.

#### Rust

Työkalujen hakeminen MCP-palvelimelta tehdään `list_tools`-metodilla. Lisää `main`-funktioon MCP-asiakasohjelman asettamisen jälkeen seuraava koodi:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Muunna palvelimen kyvyt LLM-työkaluiksi

Seuraava askel palvelimen kykyjen listaamisen jälkeen on muuntaa ne muotoon, jonka LLM ymmärtää. Kun tämä on tehty, voimme tarjota nämä kyvyt työkaluina LLM:lle.

#### TypeScript

1. Lisää seuraava koodi muuntaaksesi MCP-palvelimen vastauksen työkalumuotoon, jonka LLM voi käyttää:

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

    Edellä oleva koodi ottaa MCP-palvelimen vastauksen ja muuntaa sen työkalumääritelmäksi, jonka LLM voi ymmärtää.

1. Päivitä seuraavaksi `run`-metodi listaamaan palvelimen kyvyt:

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

    Edellä olevassa koodissa olemme päivittäneet `run`-metodin käymään läpi tuloksen ja kutsumaan `openAiToolAdapter`-metodia jokaiselle merkinnälle.

#### Python

1. Luo ensin seuraava muunnosfunktio:

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

    Yllä olevassa `convert_to_llm_tools`-funktiossa otamme MCP-työkaluvastauksen ja muunnamme sen muotoon, jonka LLM voi ymmärtää.

1. Päivitä seuraavaksi asiakasohjelmakoodi hyödyntämään tätä funktiota seuraavasti:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Tässä lisäämme kutsun `convert_to_llm_tool`-funktioon muuntaaksemme MCP-työkaluvastauksen muotoon, jonka voimme syöttää LLM:lle myöhemmin.

#### .NET

1. Lisää koodi MCP-työkaluvastauksen muuntamiseksi muotoon, jonka LLM voi ymmärtää:

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

Edellä olevassa koodissa olemme:

- Luoneet `ConvertFrom`-funktion, joka ottaa nimen, kuvauksen ja syöttöskeeman.
- Määrittäneet toiminnallisuuden, joka luo FunctionDefinitionin, joka välitetään ChatCompletionsDefinitionille. Jälkimmäinen on jotain, jonka LLM voi ymmärtää.

1. Katsotaan, kuinka voimme päivittää olemassa olevaa koodia hyödyntämään yllä olevaa funktiota:

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

Edellä olevassa koodissa olemme:

- Määrittäneet yksinkertaisen `Bot`-rajapinnan luonnollisen kielen vuorovaikutusta varten.
- Käyttäneet LangChain4j:n `AiServices`-palveluita sitomaan LLM MCP-työkaluntarjoajaan automaattisesti.
- Kehys hoitaa automaattisesti työkaluskeemojen muunnoksen ja funktiokutsut kulissien takana.
- Tämä lähestymistapa poistaa manuaalisen työkalumuunnoksen - LangChain4j hoitaa kaiken MCP-työkalujen muuntamisen LLM-yhteensopivaan muotoon.

#### Rust

MCP-työkaluvastauksen muuntamiseksi muotoon, jonka LLM voi ymmärtää, lisää apufunktio, joka muotoilee työkalulistauksen. Lisää seuraava koodi `main.rs`-tiedostoon `main`-funktion alapuolelle. Tätä kutsutaan LLM-pyyntöjä tehdessä:

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

Hienoa, nyt olemme valmiita käsittelemään käyttäjän pyyntöjä, joten siirrytään seuraavaan vaiheeseen.

### -4- Käsittele käyttäjän kehotepyyntö

Tässä osassa koodia käsittelemme käyttäjän pyyntöjä.

#### TypeScript

1. Lisää metodi, jota käytetään LLM:n kutsumiseen:

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

    Edellä olevassa koodissa olemme:

    - Lisänneet `callTools`-metodin.
    - Metodi ottaa LLM:n vastauksen ja tarkistaa, mitä työkaluja on kutsuttu, jos niitä on:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Kutsuu työkalua, jos LLM ilmoittaa, että sitä tulisi kutsua:

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

1. Päivitä `run`-metodi sisältämään LLM-kutsut ja `callTools`-kutsut:

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

Hienoa, listataan koodi kokonaisuudessaan:

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

1. Lisätään joitakin tuontikomentoja LLM:n kutsumista varten:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Seuraavaksi lisätään funktio, joka kutsuu LLM:ää:

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

    Edellä olevassa koodissa olemme:

    - Välittäneet LLM:lle MCP-palvelimelta löydetyt ja muunnetut funktiot.
    - Kutsuneet LLM:ää näillä funktioilla.
    - Tarkistaneet tuloksen, mitä funktioita tulisi kutsua, jos niitä on.
    - Lopuksi välittäneet kutsuttavien funktioiden taulukon.

1. Viimeinen vaihe, päivitetään pääkoodi:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Siinä, tämä oli viimeinen vaihe. Yllä olevassa koodissa olemme:

    - Kutsuneet MCP-työkalua `call_tool`-metodilla käyttäen funktiota, jonka LLM katsoi meidän tulisi kutsua kehotteemme perusteella.
    - Tulostaneet MCP-palvelimen työkaluvalinnan tuloksen.

#### .NET

1. Näytetään koodi LLM-kehotepyynnön tekemiseen:

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

    Edellä olevassa koodissa olemme:

    - Hakeneet työkalut MCP-palvelimelta, `var tools = await GetMcpTools()`.
    - Määrittäneet käyttäjän kehotteen `userMessage`.
    - Rakentaneet vaihtoehto-objektin, joka määrittää mallin ja työkalut.
    - Tehneet pyynnön LLM:lle.

1. Viimeinen vaihe, katsotaan, haluaako LLM kutsua funktiota:

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

    Edellä olevassa koodissa olemme:

    - Käyneet läpi funktiokutsujen listan.
    - Jokaiselle työkalukutsulle erottaneet nimen ja argumentit ja kutsuneet työkalua MCP-palvelimella MCP-asiakasohjelman avulla. Lopuksi tulostimme tulokset.

Tässä koodi kokonaisuudessaan:

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

Edellä olevassa koodissa olemme:

- Käyttäneet yksinkertaisia luonnollisen kielen kehotteita vuorovaikuttamiseen MCP-palvelimen työkalujen kanssa.
- LangChain4j-kehys hoitaa automaattisesti:
  - Käyttäjän kehotteiden muuntamisen työkalukutsuiksi tarvittaessa.
  - Sopivien MCP-työkalujen kutsumisen LLM:n päätöksen perusteella.
  - Keskustelun kulun hallinnan LLM:n ja MCP-palvelimen välillä.
- `bot.chat()`-metodi palauttaa luonnollisen kielen vastauksia, jotka voivat sisältää MCP-työkalujen suorittamisen tuloksia.
- Tämä lähestymistapa tarjoaa saumattoman käyttäjäkokemuksen, jossa käyttäjien ei tarvitse tietää MCP-toteutuksesta.

Täydellinen koodiesimerkki:

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

Tässä tapahtuu suurin osa työstä. Kutsumme LLM:ää käyttäjän alkuperäisellä kehotteella, sitten käsittelemme vastauksen nähdäksemme, onko työkaluja kutsuttava. Jos on, kutsumme näitä työkaluja ja jatkamme keskustelua LLM:n kanssa, kunnes työkutsuja ei enää tarvita ja meillä on lopullinen vastaus.

Teemme useita kutsuja LLM:lle, joten määritellään funktio, joka hoitaa LLM-kutsun. Lisää seuraava funktio `main.rs`-tiedostoon:

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

Tämä funktio ottaa LLM-asiakasohjelman, viestilistan (mukaan lukien käyttäjän kehotteen), MCP-palvelimen työkalut ja lähettää pyynnön LLM:lle, palauttaen vastauksen.
Vastaus LLM:ltä sisältää taulukon `choices`. Meidän täytyy käsitellä tulos ja tarkistaa, onko mukana `tool_calls`. Tämä kertoo, että LLM pyytää tiettyä työkalua kutsuttavaksi argumenttien kanssa. Lisää seuraava koodi `main.rs`-tiedostosi loppuun määrittääksesi funktion LLM-vastauksen käsittelyyn:

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

Jos `tool_calls` on mukana, se poimii työkalutiedot, kutsuu MCP-palvelinta työkalupyynnöllä ja lisää tulokset keskusteluviesteihin. Sen jälkeen se jatkaa keskustelua LLM:n kanssa, ja viestit päivitetään avustajan vastauksella ja työkalukutsujen tuloksilla.

Jotta voimme poimia työkalukutsutiedot, jotka LLM palauttaa MCP-kutsuja varten, lisäämme toisen apufunktion, joka poimii kaiken tarvittavan kutsun tekemiseksi. Lisää seuraava koodi `main.rs`-tiedostosi loppuun:

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

Kun kaikki osat ovat valmiina, voimme nyt käsitellä alkuperäisen käyttäjän kehotteen ja kutsua LLM:n. Päivitä `main`-funktiosi sisältämään seuraava koodi:

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

Tämä kysyy LLM:ltä alkuperäisen käyttäjän kehotteen, jossa pyydetään kahden luvun summaa, ja käsittelee vastauksen dynaamisesti työkalukutsujen käsittelyä varten.

Hienoa, onnistuit!

## Tehtävä

Ota harjoituksen koodi ja rakenna palvelin lisäämällä siihen enemmän työkaluja. Luo sitten asiakas LLM:n kanssa, kuten harjoituksessa, ja testaa sitä erilaisilla kehotteilla varmistaaksesi, että kaikki palvelimen työkalut kutsutaan dynaamisesti. Tällainen asiakasrakentamistapa tarjoaa loppukäyttäjälle erinomaisen käyttökokemuksen, sillä he voivat käyttää kehotteita tarkkojen asiakaskomentojen sijaan ja olla tietämättömiä MCP-palvelimen kutsumisesta.

## Ratkaisu

[Ratkaisu](/03-GettingStarted/03-llm-client/solution/README.md)

## Keskeiset Opit

- LLM:n lisääminen asiakkaaseen tarjoaa paremman tavan käyttäjille olla vuorovaikutuksessa MCP-palvelimien kanssa.
- MCP-palvelimen vastaus täytyy muuntaa muotoon, jonka LLM ymmärtää.

## Esimerkit

- [Java-laskin](../samples/java/calculator/README.md)
- [.Net-laskin](../../../../03-GettingStarted/samples/csharp)
- [JavaScript-laskin](../samples/javascript/README.md)
- [TypeScript-laskin](../samples/typescript/README.md)
- [Python-laskin](../../../../03-GettingStarted/samples/python)
- [Rust-laskin](../../../../03-GettingStarted/samples/rust)

## Lisäresurssit

## Mitä Seuraavaksi

- Seuraavaksi: [Palvelimen kuluttaminen Visual Studio Codella](../04-vscode/README.md)

---

**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, huomioithan, että automaattiset käännökset voivat sisältää virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäisellä kielellä tulisi pitää ensisijaisena lähteenä. Kriittisen tiedon osalta suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa väärinkäsityksistä tai virhetulkinnoista, jotka johtuvat tämän käännöksen käytöstä.