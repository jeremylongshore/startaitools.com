<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T13:20:26+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "de"
}
-->
# Erstellen eines Clients mit LLM

Bisher haben Sie gesehen, wie man einen Server und einen Client erstellt. Der Client konnte den Server explizit aufrufen, um dessen Tools, Ressourcen und Eingabeaufforderungen aufzulisten. Dies ist jedoch keine besonders praktische Herangehensweise. Ihre Nutzer leben in der agentischen Ära und erwarten, dass sie Eingabeaufforderungen verwenden und mit einem LLM kommunizieren können, um dies zu tun. Für Ihre Nutzer spielt es keine Rolle, ob Sie MCP verwenden, um Ihre Fähigkeiten zu speichern, aber sie erwarten, dass sie natürliche Sprache zur Interaktion nutzen können. Wie lösen wir das? Die Lösung besteht darin, ein LLM in den Client zu integrieren.

## Überblick

In dieser Lektion konzentrieren wir uns darauf, ein LLM in Ihren Client einzubinden und zu zeigen, wie dies eine viel bessere Benutzererfahrung bietet.

## Lernziele

Am Ende dieser Lektion werden Sie in der Lage sein:

- Einen Client mit einem LLM zu erstellen.
- Nahtlos mit einem MCP-Server über ein LLM zu interagieren.
- Eine bessere Endbenutzererfahrung auf der Client-Seite bereitzustellen.

## Ansatz

Lassen Sie uns den Ansatz verstehen, den wir verfolgen müssen. Ein LLM hinzuzufügen klingt einfach, aber wie machen wir das tatsächlich?

So wird der Client mit dem Server interagieren:

1. Verbindung zum Server herstellen.

1. Fähigkeiten, Eingabeaufforderungen, Ressourcen und Tools auflisten und deren Schema speichern.

1. Ein LLM hinzufügen und die gespeicherten Fähigkeiten und deren Schema in einem Format übergeben, das das LLM versteht.

1. Eine Benutzereingabeaufforderung verarbeiten, indem sie zusammen mit den vom Client aufgelisteten Tools an das LLM übergeben wird.

Gut, jetzt verstehen wir, wie wir dies auf hoher Ebene umsetzen können. Probieren wir es in der folgenden Übung aus.

## Übung: Erstellen eines Clients mit einem LLM

In dieser Übung lernen wir, wie man ein LLM zu unserem Client hinzufügt.

### Authentifizierung mit GitHub Personal Access Token

Das Erstellen eines GitHub-Tokens ist ein einfacher Prozess. So geht's:

- Gehen Sie zu GitHub-Einstellungen – Klicken Sie auf Ihr Profilbild oben rechts und wählen Sie Einstellungen.
- Navigieren Sie zu Entwickler-Einstellungen – Scrollen Sie nach unten und klicken Sie auf Entwickler-Einstellungen.
- Wählen Sie Personal Access Tokens – Klicken Sie auf Fine-grained tokens und dann auf Neues Token generieren.
- Konfigurieren Sie Ihr Token – Fügen Sie eine Notiz zur Referenz hinzu, legen Sie ein Ablaufdatum fest und wählen Sie die erforderlichen Berechtigungen aus. Stellen Sie sicher, dass Sie die Berechtigung für Modelle hinzufügen.
- Token generieren und kopieren – Klicken Sie auf Token generieren und kopieren Sie es sofort, da Sie es später nicht mehr sehen können.

### -1- Verbindung zum Server herstellen

Lassen Sie uns zuerst unseren Client erstellen:

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

Im obigen Code haben wir:

- Die benötigten Bibliotheken importiert.
- Eine Klasse mit zwei Mitgliedern erstellt, `client` und `openai`, die uns helfen, einen Client zu verwalten und mit einem LLM zu interagieren.
- Unsere LLM-Instanz so konfiguriert, dass sie GitHub-Modelle verwendet, indem `baseUrl` auf die Inferenz-API verweist.

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

Im obigen Code haben wir:

- Die benötigten Bibliotheken für MCP importiert.
- Einen Client erstellt.

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

Zuerst müssen Sie die LangChain4j-Abhängigkeiten zu Ihrer `pom.xml`-Datei hinzufügen. Fügen Sie diese Abhängigkeiten hinzu, um MCP-Integration und GitHub-Modelle zu unterstützen:

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

Erstellen Sie dann Ihre Java-Client-Klasse:

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

Im obigen Code haben wir:

- **LangChain4j-Abhängigkeiten hinzugefügt**: Erforderlich für MCP-Integration, OpenAI-Client und GitHub-Modelle.
- **LangChain4j-Bibliotheken importiert**: Für MCP-Integration und OpenAI-Chat-Modell-Funktionalität.
- **Ein `ChatLanguageModel` erstellt**: Konfiguriert zur Verwendung von GitHub-Modellen mit Ihrem GitHub-Token.
- **HTTP-Transport eingerichtet**: Mit Server-Sent Events (SSE), um eine Verbindung zum MCP-Server herzustellen.
- **Einen MCP-Client erstellt**: Der die Kommunikation mit dem Server übernimmt.
- **LangChain4j's eingebaute MCP-Unterstützung verwendet**: Die die Integration zwischen LLMs und MCP-Servern vereinfacht.

#### Rust

Dieses Beispiel geht davon aus, dass Sie einen MCP-Server auf Rust-Basis betreiben. Falls nicht, schauen Sie sich die Lektion [01-first-server](../01-first-server/README.md) an, um den Server zu erstellen.

Sobald Sie Ihren Rust-MCP-Server haben, öffnen Sie ein Terminal und navigieren Sie in das gleiche Verzeichnis wie der Server. Führen Sie dann den folgenden Befehl aus, um ein neues LLM-Client-Projekt zu erstellen:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Fügen Sie die folgenden Abhängigkeiten zu Ihrer `Cargo.toml`-Datei hinzu:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Es gibt keine offizielle Rust-Bibliothek für OpenAI, jedoch ist das `async-openai`-Crate eine [von der Community gepflegte Bibliothek](https://platform.openai.com/docs/libraries/rust#rust), die häufig verwendet wird.

Öffnen Sie die Datei `src/main.rs` und ersetzen Sie deren Inhalt durch den folgenden Code:

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

Dieser Code richtet eine grundlegende Rust-Anwendung ein, die eine Verbindung zu einem MCP-Server und GitHub-Modellen für LLM-Interaktionen herstellt.

> [!IMPORTANT]
> Stellen Sie sicher, dass die Umgebungsvariable `OPENAI_API_KEY` mit Ihrem GitHub-Token gesetzt ist, bevor Sie die Anwendung ausführen.

Gut, für unseren nächsten Schritt listen wir die Fähigkeiten des Servers auf.

### -2- Fähigkeiten des Servers auflisten

Jetzt verbinden wir uns mit dem Server und fragen nach seinen Fähigkeiten:

#### TypeScript

Fügen Sie in derselben Klasse die folgenden Methoden hinzu:

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

Im obigen Code haben wir:

- Code zum Verbinden mit dem Server hinzugefügt, `connectToServer`.
- Eine `run`-Methode erstellt, die für den Ablauf unserer App verantwortlich ist. Bisher listet sie nur die Tools auf, aber wir werden bald mehr hinzufügen.

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

Hier ist, was wir hinzugefügt haben:

- Ressourcen und Tools aufgelistet und ausgegeben. Für Tools listen wir auch `inputSchema` auf, das wir später verwenden.

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

Im obigen Code haben wir:

- Die auf dem MCP-Server verfügbaren Tools aufgelistet.
- Für jedes Tool Name, Beschreibung und Schema aufgelistet. Letzteres werden wir bald verwenden, um die Tools aufzurufen.

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

Im obigen Code haben wir:

- Einen `McpToolProvider` erstellt, der automatisch alle Tools vom MCP-Server entdeckt und registriert.
- Der Tool-Provider übernimmt intern die Konvertierung zwischen MCP-Tool-Schemas und LangChain4j-Tool-Format.
- Dieser Ansatz abstrahiert den manuellen Prozess der Tool-Auflistung und -Konvertierung.

#### Rust

Das Abrufen von Tools vom MCP-Server erfolgt mit der Methode `list_tools`. Fügen Sie in Ihrer `main`-Funktion nach der Einrichtung des MCP-Clients den folgenden Code hinzu:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Serverfähigkeiten in LLM-Tools umwandeln

Der nächste Schritt nach der Auflistung der Serverfähigkeiten besteht darin, sie in ein Format umzuwandeln, das das LLM versteht. Sobald wir das getan haben, können wir diese Fähigkeiten als Tools für unser LLM bereitstellen.

#### TypeScript

1. Fügen Sie den folgenden Code hinzu, um die Antwort des MCP-Servers in ein Tool-Format umzuwandeln, das das LLM verwenden kann:

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

    Der obige Code nimmt eine Antwort vom MCP-Server und wandelt sie in eine Tool-Definition um, die das LLM verstehen kann.

1. Aktualisieren Sie als Nächstes die `run`-Methode, um die Serverfähigkeiten aufzulisten:

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

    Im obigen Code haben wir die `run`-Methode aktualisiert, um durch das Ergebnis zu iterieren und für jeden Eintrag `openAiToolAdapter` aufzurufen.

#### Python

1. Erstellen Sie zunächst die folgende Konverterfunktion:

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

    In der obigen Funktion `convert_to_llm_tools` nehmen wir eine MCP-Tool-Antwort und wandeln sie in ein Format um, das das LLM verstehen kann.

1. Aktualisieren Sie als Nächstes Ihren Client-Code, um diese Funktion wie folgt zu nutzen:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Hier fügen wir einen Aufruf zu `convert_to_llm_tool` hinzu, um die MCP-Tool-Antwort in etwas umzuwandeln, das wir später dem LLM übergeben können.

#### .NET

1. Fügen Sie Code hinzu, um die MCP-Tool-Antwort in etwas umzuwandeln, das das LLM verstehen kann:

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

Im obigen Code haben wir:

- Eine Funktion `ConvertFrom` erstellt, die Name, Beschreibung und Eingabeschema entgegennimmt.
- Funktionalität definiert, die eine FunctionDefinition erstellt, die an eine ChatCompletionsDefinition übergeben wird. Letztere ist etwas, das das LLM verstehen kann.

1. Sehen wir uns an, wie wir bestehenden Code aktualisieren können, um die obige Funktion zu nutzen:

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

Im obigen Code haben wir:

- Eine einfache `Bot`-Schnittstelle für natürliche Sprachinteraktionen definiert.
- LangChain4j's `AiServices` verwendet, um das LLM automatisch mit dem MCP-Tool-Provider zu verbinden.
- Das Framework übernimmt automatisch die Konvertierung von Tool-Schemas und das Aufrufen von Funktionen im Hintergrund.
- Dieser Ansatz eliminiert die manuelle Tool-Konvertierung - LangChain4j übernimmt die gesamte Komplexität der Konvertierung von MCP-Tools in ein LLM-kompatibles Format.

#### Rust

Um die MCP-Tool-Antwort in ein Format umzuwandeln, das das LLM verstehen kann, fügen wir eine Hilfsfunktion hinzu, die die Tool-Auflistung formatiert. Fügen Sie den folgenden Code zu Ihrer `main.rs`-Datei unterhalb der `main`-Funktion hinzu. Diese wird bei Anfragen an das LLM aufgerufen:

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

Gut, wir sind jetzt bereit, Benutzeranfragen zu bearbeiten. Lassen Sie uns das als Nächstes angehen.

### -4- Benutzeranfragen bearbeiten

In diesem Teil des Codes werden wir Benutzeranfragen bearbeiten.

#### TypeScript

1. Fügen Sie eine Methode hinzu, die verwendet wird, um unser LLM aufzurufen:

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

    Im obigen Code haben wir:

    - Eine Methode `callTools` hinzugefügt.
    - Die Methode nimmt eine LLM-Antwort und überprüft, ob Tools aufgerufen wurden, falls vorhanden:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Ruft ein Tool auf, falls das LLM angibt, dass es aufgerufen werden soll:

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

1. Aktualisieren Sie die `run`-Methode, um Aufrufe an das LLM und `callTools` einzuschließen:

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

Gut, hier ist der vollständige Code:

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

1. Fügen Sie einige Importe hinzu, die benötigt werden, um ein LLM aufzurufen:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Fügen Sie als Nächstes die Funktion hinzu, die das LLM aufruft:

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

    Im obigen Code haben wir:

    - Unsere Funktionen, die wir auf dem MCP-Server gefunden und konvertiert haben, an das LLM übergeben.
    - Dann das LLM mit diesen Funktionen aufgerufen.
    - Anschließend das Ergebnis überprüft, um zu sehen, welche Funktionen aufgerufen werden sollen, falls vorhanden.
    - Schließlich ein Array von Funktionen übergeben, die aufgerufen werden sollen.

1. Letzter Schritt, aktualisieren Sie unseren Hauptcode:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Im obigen Code:

    - Rufen wir ein MCP-Tool über `call_tool` mit einer Funktion auf, die das LLM basierend auf unserer Eingabeaufforderung aufrufen wollte.
    - Geben wir das Ergebnis des Tool-Aufrufs an den MCP-Server aus.

#### .NET

1. Zeigen wir etwas Code für eine LLM-Eingabeaufforderungsanfrage:

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

    Im obigen Code haben wir:

    - Tools vom MCP-Server abgerufen, `var tools = await GetMcpTools()`.
    - Eine Benutzereingabeaufforderung `userMessage` definiert.
    - Ein Optionsobjekt erstellt, das Modell und Tools angibt.
    - Eine Anfrage an das LLM gestellt.

1. Ein letzter Schritt, sehen wir nach, ob das LLM denkt, dass wir eine Funktion aufrufen sollten:

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

    Im obigen Code haben wir:

    - Eine Liste von Funktionsaufrufen durchlaufen.
    - Für jeden Tool-Aufruf Name und Argumente analysiert und das Tool auf dem MCP-Server mit dem MCP-Client aufgerufen. Schließlich geben wir die Ergebnisse aus.

Hier ist der vollständige Code:

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

Im obigen Code haben wir:

- Einfache natürliche Sprachaufforderungen verwendet, um mit den MCP-Server-Tools zu interagieren.
- Das LangChain4j-Framework übernimmt automatisch:
  - Die Konvertierung von Benutzereingabeaufforderungen in Tool-Aufrufe, wenn erforderlich.
  - Das Aufrufen der entsprechenden MCP-Tools basierend auf der Entscheidung des LLM.
  - Die Verwaltung des Gesprächsflusses zwischen dem LLM und dem MCP-Server.
- Die Methode `bot.chat()` gibt natürliche Sprachantworten zurück, die Ergebnisse von MCP-Tool-Ausführungen enthalten können.
- Dieser Ansatz bietet eine nahtlose Benutzererfahrung, bei der die Nutzer nichts über die zugrunde liegende MCP-Implementierung wissen müssen.

Vollständiges Codebeispiel:

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

Hier findet der Großteil der Arbeit statt. Wir rufen das LLM mit der anfänglichen Benutzereingabeaufforderung auf, verarbeiten die Antwort, um zu sehen, ob Tools aufgerufen werden müssen. Falls ja, rufen wir diese Tools auf und setzen die Unterhaltung mit dem LLM fort, bis keine weiteren Tool-Aufrufe erforderlich sind und wir eine endgültige Antwort haben.

Da wir mehrere Aufrufe an das LLM machen werden, definieren wir eine Funktion, die den LLM-Aufruf übernimmt. Fügen Sie die folgende Funktion zu Ihrer `main.rs`-Datei hinzu:

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

Diese Funktion nimmt den LLM-Client, eine Liste von Nachrichten (einschließlich der Benutzereingabeaufforderung), Tools vom MCP-Server und sendet eine Anfrage an das LLM, wobei die Antwort zurückgegeben wird.
Die Antwort des LLM enthält ein Array von `choices`. Wir müssen das Ergebnis verarbeiten, um festzustellen, ob `tool_calls` vorhanden sind. Dies zeigt uns, dass das LLM anfordert, ein bestimmtes Tool mit Argumenten aufzurufen. Fügen Sie den folgenden Code am Ende Ihrer Datei `main.rs` hinzu, um eine Funktion zu definieren, die die LLM-Antwort verarbeitet:

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

Falls `tool_calls` vorhanden sind, werden die Tool-Informationen extrahiert, der MCP-Server mit der Tool-Anfrage aufgerufen und die Ergebnisse zu den Konversationsnachrichten hinzugefügt. Anschließend wird die Konversation mit dem LLM fortgesetzt, und die Nachrichten werden mit der Antwort des Assistenten und den Ergebnissen der Tool-Aufrufe aktualisiert.

Um die Tool-Aufrufinformationen zu extrahieren, die das LLM für MCP-Aufrufe zurückgibt, fügen wir eine weitere Hilfsfunktion hinzu, die alles extrahiert, was für den Aufruf benötigt wird. Fügen Sie den folgenden Code am Ende Ihrer Datei `main.rs` hinzu:

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

Mit allen notwendigen Komponenten können wir nun die anfängliche Benutzeraufforderung verarbeiten und das LLM aufrufen. Aktualisieren Sie Ihre `main`-Funktion, um den folgenden Code einzufügen:

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

Dies wird das LLM mit der anfänglichen Benutzeraufforderung abfragen, die nach der Summe von zwei Zahlen fragt, und die Antwort verarbeiten, um Tool-Aufrufe dynamisch zu handhaben.

Super, Sie haben es geschafft!

## Aufgabe

Nehmen Sie den Code aus der Übung und erweitern Sie den Server mit weiteren Tools. Erstellen Sie anschließend einen Client mit einem LLM, wie in der Übung, und testen Sie ihn mit verschiedenen Eingaben, um sicherzustellen, dass alle Server-Tools dynamisch aufgerufen werden. Diese Art, einen Client zu erstellen, sorgt für eine großartige Benutzererfahrung, da die Endbenutzer Eingaben machen können, ohne genaue Client-Befehle zu kennen, und nicht bemerken, dass ein MCP-Server aufgerufen wird.

## Lösung

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## Wichtige Erkenntnisse

- Die Integration eines LLM in Ihren Client bietet eine bessere Möglichkeit für Benutzer, mit MCP-Servern zu interagieren.
- Sie müssen die Antwort des MCP-Servers in ein Format umwandeln, das das LLM versteht.

## Beispiele

- [Java Rechner](../samples/java/calculator/README.md)
- [.Net Rechner](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Rechner](../samples/javascript/README.md)
- [TypeScript Rechner](../samples/typescript/README.md)
- [Python Rechner](../../../../03-GettingStarted/samples/python)
- [Rust Rechner](../../../../03-GettingStarted/samples/rust)

## Zusätzliche Ressourcen

## Was kommt als Nächstes?

- Weiter: [Einen Server mit Visual Studio Code nutzen](../04-vscode/README.md)

---

**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner ursprünglichen Sprache sollte als maßgebliche Quelle betrachtet werden. Für kritische Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die sich aus der Nutzung dieser Übersetzung ergeben.