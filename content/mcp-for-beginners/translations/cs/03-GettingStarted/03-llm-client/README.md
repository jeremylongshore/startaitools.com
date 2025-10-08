<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T15:06:27+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "cs"
}
-->
# Vytvoření klienta s LLM

Doposud jste viděli, jak vytvořit server a klienta. Klient mohl explicitně volat server, aby získal seznam jeho nástrojů, zdrojů a promptů. To však není příliš praktický přístup. Váš uživatel žije v agentické éře a očekává, že bude používat prompty a komunikovat s LLM. Uživatelům je jedno, jestli používáte MCP k ukládání svých schopností, ale očekávají, že budou moci komunikovat přirozeným jazykem. Jak to tedy vyřešíme? Řešením je přidání LLM do klienta.

## Přehled

V této lekci se zaměříme na přidání LLM do klienta a ukážeme, jak to poskytuje mnohem lepší uživatelský zážitek.

## Cíle učení

Na konci této lekce budete schopni:

- Vytvořit klienta s LLM.
- Bezproblémově komunikovat s MCP serverem pomocí LLM.
- Poskytnout lepší uživatelský zážitek na straně klienta.

## Přístup

Pojďme si vysvětlit přístup, který musíme zvolit. Přidání LLM zní jednoduše, ale jak to vlastně uděláme?

Takto bude klient komunikovat se serverem:

1. Navázání spojení se serverem.

1. Seznam schopností, promptů, zdrojů a nástrojů a uložení jejich schématu.

1. Přidání LLM a předání uložených schopností a jejich schématu ve formátu, kterému LLM rozumí.

1. Zpracování uživatelského promptu jeho předáním LLM spolu s nástroji uvedenými klientem.

Skvělé, teď rozumíme, jak to můžeme udělat na vysoké úrovni, pojďme si to vyzkoušet v následujícím cvičení.

## Cvičení: Vytvoření klienta s LLM

V tomto cvičení se naučíme přidat LLM do našeho klienta.

### Autentizace pomocí GitHub Personal Access Token

Vytvoření GitHub tokenu je jednoduchý proces. Zde je postup:

- Přejděte do Nastavení GitHub – Klikněte na svůj profilový obrázek v pravém horním rohu a vyberte Nastavení.
- Přejděte do Nastavení vývojáře – Posuňte se dolů a klikněte na Nastavení vývojáře.
- Vyberte Osobní přístupové tokeny – Klikněte na Jemně odstupňované tokeny a poté Generovat nový token.
- Nakonfigurujte svůj token – Přidejte poznámku pro referenci, nastavte datum vypršení platnosti a vyberte potřebné rozsahy (oprávnění). V tomto případě nezapomeňte přidat oprávnění Models.
- Vygenerujte a zkopírujte token – Klikněte na Generovat token a ihned jej zkopírujte, protože jej později již neuvidíte.

### -1- Připojení k serveru

Nejprve vytvořme našeho klienta:

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

V předchozím kódu jsme:

- Importovali potřebné knihovny.
- Vytvořili třídu se dvěma členy, `client` a `openai`, které nám pomohou spravovat klienta a komunikovat s LLM.
- Nakonfigurovali naši instanci LLM tak, aby používala GitHub Models nastavením `baseUrl` na inference API.

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

V předchozím kódu jsme:

- Importovali potřebné knihovny pro MCP.
- Vytvořili klienta.

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

Nejprve budete muset přidat závislosti LangChain4j do svého souboru `pom.xml`. Přidejte tyto závislosti pro povolení integrace MCP a podporu GitHub Models:

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

Poté vytvořte svou třídu klienta v Javě:

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

V předchozím kódu jsme:

- **Přidali závislosti LangChain4j**: Potřebné pro integraci MCP, oficiálního klienta OpenAI a podporu GitHub Models.
- **Importovali knihovny LangChain4j**: Pro integraci MCP a funkčnost chatovacího modelu OpenAI.
- **Vytvořili `ChatLanguageModel`**: Nakonfigurovaný pro použití GitHub Models s vaším GitHub tokenem.
- **Nastavili HTTP transport**: Pomocí Server-Sent Events (SSE) pro připojení k MCP serveru.
- **Vytvořili MCP klienta**: Který bude zpracovávat komunikaci se serverem.
- **Použili vestavěnou podporu MCP v LangChain4j**: Která zjednodušuje integraci mezi LLM a MCP servery.

#### Rust

Tento příklad předpokládá, že máte spuštěný MCP server založený na Rustu. Pokud jej nemáte, vraťte se k lekci [01-first-server](../01-first-server/README.md) a vytvořte server.

Jakmile máte svůj Rust MCP server, otevřete terminál a přejděte do stejného adresáře jako server. Poté spusťte následující příkaz pro vytvoření nového projektu klienta LLM:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Přidejte následující závislosti do svého souboru `Cargo.toml`:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Neexistuje oficiální Rust knihovna pro OpenAI, avšak `async-openai` je [komunitou udržovaná knihovna](https://platform.openai.com/docs/libraries/rust#rust), která se běžně používá.

Otevřete soubor `src/main.rs` a nahraďte jeho obsah následujícím kódem:

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

Tento kód nastavuje základní aplikaci v Rustu, která se připojí k MCP serveru a GitHub Models pro interakce s LLM.

> [!IMPORTANT]
> Před spuštěním aplikace nezapomeňte nastavit proměnnou prostředí `OPENAI_API_KEY` s vaším GitHub tokenem.

Skvělé, v dalším kroku si vylistujeme schopnosti na serveru.

### -2- Seznam schopností serveru

Nyní se připojíme k serveru a požádáme o jeho schopnosti:

#### TypeScript

Do stejné třídy přidejte následující metody:

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

V předchozím kódu jsme:

- Přidali kód pro připojení k serveru, `connectToServer`.
- Vytvořili metodu `run`, která je zodpovědná za zpracování toku naší aplikace. Zatím pouze vypisuje nástroje, ale brzy přidáme další funkce.

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

Zde jsme přidali:

- Výpis zdrojů a nástrojů a jejich vytištění. U nástrojů také vypisujeme `inputSchema`, které později použijeme.

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

V předchozím kódu jsme:

- Vypsali nástroje dostupné na MCP serveru.
- Pro každý nástroj vypsali název, popis a jeho schéma. To poslední použijeme pro volání nástrojů.

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

V předchozím kódu jsme:

- Vytvořili `McpToolProvider`, který automaticky objevuje a registruje všechny nástroje z MCP serveru.
- Poskytovatel nástrojů interně zpracovává převod mezi schématy nástrojů MCP a formátem nástrojů LangChain4j.
- Tento přístup abstrahuje manuální proces výpisu a převodu nástrojů.

#### Rust

Získání nástrojů z MCP serveru se provádí pomocí metody `list_tools`. Ve své funkci `main`, po nastavení MCP klienta, přidejte následující kód:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Převod schopností serveru na nástroje LLM

Dalším krokem po výpisu schopností serveru je převést je do formátu, kterému LLM rozumí. Jakmile to uděláme, můžeme tyto schopnosti poskytnout jako nástroje našemu LLM.

#### TypeScript

1. Přidejte následující kód pro převod odpovědi z MCP serveru na formát nástroje, kterému LLM rozumí:

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

    Výše uvedený kód vezme odpověď z MCP serveru a převede ji na definici nástroje, které LLM rozumí.

1. Aktualizujte metodu `run`, aby vypsala schopnosti serveru:

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

    V předchozím kódu jsme aktualizovali metodu `run`, aby procházela výsledky a pro každý záznam volala `openAiToolAdapter`.

#### Python

1. Nejprve vytvořme následující konverzní funkci:

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

    Ve funkci `convert_to_llm_tools` bereme odpověď nástroje MCP a převádíme ji do formátu, kterému LLM rozumí.

1. Dále aktualizujeme kód klienta, aby využíval tuto funkci:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Zde přidáváme volání `convert_to_llm_tool` pro převod odpovědi nástroje MCP na něco, co můžeme později předat LLM.

#### .NET

1. Přidejme kód pro převod odpovědi nástroje MCP na něco, čemu LLM rozumí:

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

V předchozím kódu jsme:

- Vytvořili funkci `ConvertFrom`, která bere název, popis a vstupní schéma.
- Definovali funkčnost, která vytváří FunctionDefinition, jež se předává do ChatCompletionsDefinition. To je něco, čemu LLM rozumí.

1. Podívejme se, jak můžeme aktualizovat existující kód, aby využíval výše uvedenou funkci:

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

V předchozím kódu jsme:

- Definovali jednoduché rozhraní `Bot` pro interakce v přirozeném jazyce.
- Použili `AiServices` z LangChain4j pro automatické propojení LLM s poskytovatelem nástrojů MCP.
- Framework automaticky zpracovává převod schémat nástrojů a volání funkcí na pozadí.
- Tento přístup eliminuje manuální převod nástrojů - LangChain4j se stará o veškerou složitost převodu nástrojů MCP na formát kompatibilní s LLM.

#### Rust

Pro převod odpovědi nástroje MCP na formát, kterému LLM rozumí, přidáme pomocnou funkci, která formátuje seznam nástrojů. Přidejte následující kód do svého souboru `main.rs` pod funkci `main`. Tato funkce bude volána při vytváření požadavků na LLM:

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

Skvělé, nyní jsme připraveni zpracovat jakékoli uživatelské požadavky, takže se na to podíváme dále.

### -4- Zpracování uživatelského promptu

V této části kódu budeme zpracovávat uživatelské požadavky.

#### TypeScript

1. Přidejte metodu, která bude použita pro volání našeho LLM:

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

    V předchozím kódu jsme:

    - Přidali metodu `callTools`.
    - Metoda bere odpověď LLM a kontroluje, zda byly volány nějaké nástroje:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Volá nástroj, pokud LLM naznačuje, že by měl být volán:

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

1. Aktualizujte metodu `run`, aby zahrnovala volání LLM a volání `callTools`:

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

Skvělé, zde je celý kód:

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

1. Přidejme některé importy potřebné pro volání LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Dále přidejme funkci, která bude volat LLM:

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

    V předchozím kódu jsme:

    - Předali naše funkce, které jsme našli na MCP serveru a převedli, LLM.
    - Poté jsme zavolali LLM s těmito funkcemi.
    - Poté kontrolujeme výsledek, abychom zjistili, jaké funkce bychom měli volat, pokud nějaké.
    - Nakonec předáváme pole funkcí k volání.

1. Poslední krok, aktualizujme náš hlavní kód:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Tam, to byl poslední krok, v kódu výše:

    - Voláme nástroj MCP přes `call_tool` pomocí funkce, kterou LLM považovalo za vhodnou na základě našeho promptu.
    - Tiskneme výsledek volání nástroje na MCP server.

#### .NET

1. Ukážeme kód pro vytvoření požadavku na prompt LLM:

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

    V předchozím kódu jsme:

    - Načetli nástroje z MCP serveru, `var tools = await GetMcpTools()`.
    - Definovali uživatelský prompt `userMessage`.
    - Sestavili objekt možností specifikující model a nástroje.
    - Vytvořili požadavek na LLM.

1. Poslední krok, podívejme se, zda LLM považuje za vhodné volat funkci:

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

    V předchozím kódu jsme:

    - Prošli seznam volání funkcí.
    - Pro každé volání nástroje jsme analyzovali název a argumenty a zavolali nástroj na MCP serveru pomocí MCP klienta. Nakonec jsme vytiskli výsledky.

Zde je celý kód:

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

V předchozím kódu jsme:

- Použili jednoduché prompty v přirozeném jazyce pro interakci s nástroji MCP serveru.
- Framework LangChain4j automaticky zpracovává:
  - Převod uživatelských promptů na volání nástrojů, pokud je to potřeba.
  - Volání příslušných nástrojů MCP na základě rozhodnutí LLM.
  - Správu toku konverzace mezi LLM a MCP serverem.
- Metoda `bot.chat()` vrací odpovědi v přirozeném jazyce, které mohou zahrnovat výsledky z provedení nástrojů MCP.
- Tento přístup poskytuje bezproblémový uživatelský zážitek, kde uživatelé nemusí vědět o podkladové implementaci MCP.

Kompletní příklad kódu:

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

Zde se odehrává většina práce. Budeme volat LLM s počátečním uživatelským promptem, poté zpracovávat odpověď, abychom zjistili, zda je potřeba volat nějaké nástroje. Pokud ano, zavoláme tyto nástroje a budeme pokračovat v konverzaci s LLM, dokud nebudou všechny volání nástrojů dokončeny a nebudeme mít finální odpověď.

Budeme provádět více volání na LLM, takže definujme funkci, která bude zpracovávat volání LLM. Přidejte následující funkci do svého souboru `main.rs`:

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

Tato funkce bere klienta LLM, seznam zpráv (včetně uživatelského promptu), nástroje z MCP serveru a odesílá požadavek na LLM, přičemž vrací odpověď.
Odezva od LLM bude obsahovat pole `choices`. Budeme muset zpracovat výsledek, abychom zjistili, zda jsou přítomny nějaké `tool_calls`. To nám dá vědět, že LLM požaduje, aby byl zavolán konkrétní nástroj s argumenty. Přidejte následující kód na konec vašeho souboru `main.rs`, abyste definovali funkci pro zpracování odpovědi od LLM:

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

Pokud jsou přítomny `tool_calls`, funkce extrahuje informace o nástroji, zavolá MCP server s požadavkem na nástroj a přidá výsledky do zpráv konverzace. Poté pokračuje v konverzaci s LLM a zprávy jsou aktualizovány odpovědí asistenta a výsledky volání nástroje.

Pro extrakci informací o volání nástroje, které LLM vrací pro MCP volání, přidáme další pomocnou funkci, která extrahuje vše potřebné pro provedení volání. Přidejte následující kód na konec vašeho souboru `main.rs`:

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

S těmito částmi na místě nyní můžeme zpracovat počáteční uživatelský dotaz a zavolat LLM. Aktualizujte svou funkci `main`, aby obsahovala následující kód:

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

Tímto způsobem dotazujete LLM s počátečním uživatelským dotazem, který se ptá na součet dvou čísel, a zpracováváte odpověď tak, aby dynamicky zpracovala volání nástrojů.

Skvělé, máte to hotové!

## Úkol

Vezměte kód z cvičení a rozšiřte server o další nástroje. Poté vytvořte klienta s LLM, podobně jako v cvičení, a otestujte jej s různými dotazy, abyste se ujistili, že všechny vaše serverové nástroje jsou volány dynamicky. Tento způsob budování klienta znamená, že koncový uživatel bude mít skvělý uživatelský zážitek, protože bude moci používat dotazy místo přesných příkazů klienta a nebude si vědom žádného volání MCP serveru.

## Řešení

[Řešení](/03-GettingStarted/03-llm-client/solution/README.md)

## Klíčové poznatky

- Přidání LLM do vašeho klienta poskytuje lepší způsob, jak uživatelé mohou interagovat s MCP servery.
- Je potřeba převést odpověď MCP serveru na něco, čemu LLM rozumí.

## Ukázky

- [Java Kalkulačka](../samples/java/calculator/README.md)
- [.Net Kalkulačka](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Kalkulačka](../samples/javascript/README.md)
- [TypeScript Kalkulačka](../samples/typescript/README.md)
- [Python Kalkulačka](../../../../03-GettingStarted/samples/python)
- [Rust Kalkulačka](../../../../03-GettingStarted/samples/rust)

## Další zdroje

## Co dál

- Další: [Spotřeba serveru pomocí Visual Studio Code](../04-vscode/README.md)

---

**Prohlášení**:  
Tento dokument byl přeložen pomocí služby AI pro překlady [Co-op Translator](https://github.com/Azure/co-op-translator). Ačkoliv se snažíme o přesnost, mějte prosím na paměti, že automatické překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho rodném jazyce by měl být považován za autoritativní zdroj. Pro důležité informace doporučujeme profesionální lidský překlad. Neodpovídáme za žádná nedorozumění nebo nesprávné interpretace vyplývající z použití tohoto překladu.