<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:24:05+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "el"
}
-->
# Δημιουργία πελάτη με LLM

Μέχρι τώρα, έχετε δει πώς να δημιουργήσετε έναν διακομιστή και έναν πελάτη. Ο πελάτης μπορούσε να καλεί τον διακομιστή ρητά για να καταγράψει τα εργαλεία, τους πόρους και τις προτροπές του. Ωστόσο, αυτή η προσέγγιση δεν είναι πολύ πρακτική. Ο χρήστης σας ζει στην εποχή των πρακτόρων και περιμένει να χρησιμοποιεί προτροπές και να επικοινωνεί με ένα LLM για να το κάνει. Για τον χρήστη σας, δεν έχει σημασία αν χρησιμοποιείτε MCP ή όχι για να αποθηκεύσετε τις δυνατότητές σας, αλλά περιμένει να αλληλεπιδράσει με φυσική γλώσσα. Πώς το λύνουμε αυτό; Η λύση είναι να προσθέσουμε ένα LLM στον πελάτη.

## Επισκόπηση

Σε αυτό το μάθημα επικεντρωνόμαστε στην προσθήκη ενός LLM στον πελάτη σας και δείχνουμε πώς αυτό παρέχει μια πολύ καλύτερη εμπειρία για τον χρήστη σας.

## Στόχοι Μάθησης

Μέχρι το τέλος αυτού του μαθήματος, θα μπορείτε:

- Να δημιουργήσετε έναν πελάτη με LLM.
- Να αλληλεπιδράσετε απρόσκοπτα με έναν MCP διακομιστή χρησιμοποιώντας ένα LLM.
- Να παρέχετε μια καλύτερη εμπειρία χρήστη από την πλευρά του πελάτη.

## Προσέγγιση

Ας προσπαθήσουμε να κατανοήσουμε την προσέγγιση που πρέπει να ακολουθήσουμε. Η προσθήκη ενός LLM ακούγεται απλή, αλλά πώς θα το κάνουμε πραγματικά;

Να πώς θα αλληλεπιδράσει ο πελάτης με τον διακομιστή:

1. Δημιουργία σύνδεσης με τον διακομιστή.

1. Καταγραφή δυνατοτήτων, προτροπών, πόρων και εργαλείων και αποθήκευση του σχήματός τους.

1. Προσθήκη ενός LLM και μεταβίβαση των αποθηκευμένων δυνατοτήτων και του σχήματός τους σε μορφή που κατανοεί το LLM.

1. Διαχείριση μιας προτροπής χρήστη μεταβιβάζοντάς την στο LLM μαζί με τα εργαλεία που καταγράφηκαν από τον πελάτη.

Ωραία, τώρα καταλαβαίνουμε πώς μπορούμε να το κάνουμε σε υψηλό επίπεδο. Ας το δοκιμάσουμε στην παρακάτω άσκηση.

## Άσκηση: Δημιουργία πελάτη με LLM

Σε αυτή την άσκηση, θα μάθουμε να προσθέτουμε ένα LLM στον πελάτη μας.

### Αυθεντικοποίηση χρησιμοποιώντας GitHub Personal Access Token

Η δημιουργία ενός GitHub token είναι μια απλή διαδικασία. Να πώς μπορείτε να το κάνετε:

- Μεταβείτε στις Ρυθμίσεις του GitHub – Κάντε κλικ στη φωτογραφία προφίλ σας στην επάνω δεξιά γωνία και επιλέξτε Ρυθμίσεις.
- Πλοηγηθείτε στις Ρυθμίσεις Προγραμματιστή – Κάντε κύλιση προς τα κάτω και κάντε κλικ στις Ρυθμίσεις Προγραμματιστή.
- Επιλέξτε Personal Access Tokens – Κάντε κλικ στα Fine-grained tokens και στη συνέχεια Generate new token.
- Διαμορφώστε το Token σας – Προσθέστε μια σημείωση για αναφορά, ορίστε ημερομηνία λήξης και επιλέξτε τα απαραίτητα πεδία (άδειες). Σε αυτή την περίπτωση, βεβαιωθείτε ότι έχετε προσθέσει την άδεια Models.
- Δημιουργήστε και Αντιγράψτε το Token – Κάντε κλικ στο Generate token και βεβαιωθείτε ότι το αντιγράψατε αμέσως, καθώς δεν θα μπορείτε να το δείτε ξανά.

### -1- Σύνδεση με τον διακομιστή

Ας δημιουργήσουμε πρώτα τον πελάτη μας:

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

Στον παραπάνω κώδικα έχουμε:

- Εισάγει τις απαραίτητες βιβλιοθήκες.
- Δημιουργήσει μια κλάση με δύο μέλη, `client` και `openai`, που θα μας βοηθήσουν να διαχειριστούμε έναν πελάτη και να αλληλεπιδράσουμε με ένα LLM αντίστοιχα.
- Διαμορφώσει την περίπτωση του LLM μας για να χρησιμοποιεί τα GitHub Models, ορίζοντας το `baseUrl` να δείχνει στο inference API.

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

Στον παραπάνω κώδικα έχουμε:

- Εισάγει τις απαραίτητες βιβλιοθήκες για MCP.
- Δημιουργήσει έναν πελάτη.

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

Πρώτα, θα χρειαστεί να προσθέσετε τις εξαρτήσεις LangChain4j στο αρχείο `pom.xml`. Προσθέστε αυτές τις εξαρτήσεις για να ενεργοποιήσετε την ενσωμάτωση MCP και την υποστήριξη GitHub Models:

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

Στη συνέχεια, δημιουργήστε την κλάση πελάτη Java:

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

Στον παραπάνω κώδικα έχουμε:

- **Προσθέσει εξαρτήσεις LangChain4j**: Απαραίτητες για την ενσωμάτωση MCP, τον επίσημο πελάτη OpenAI και την υποστήριξη GitHub Models.
- **Εισάγει τις βιβλιοθήκες LangChain4j**: Για την ενσωμάτωση MCP και τη λειτουργικότητα του OpenAI chat model.
- **Δημιουργήσει ένα `ChatLanguageModel`**: Διαμορφωμένο να χρησιμοποιεί τα GitHub Models με το GitHub token σας.
- **Ρυθμίσει τη μεταφορά HTTP**: Χρησιμοποιώντας Server-Sent Events (SSE) για σύνδεση με τον MCP διακομιστή.
- **Δημιουργήσει έναν MCP πελάτη**: Που θα χειρίζεται την επικοινωνία με τον διακομιστή.
- **Χρησιμοποιήσει την ενσωματωμένη υποστήριξη MCP του LangChain4j**: Που απλοποιεί την ενσωμάτωση μεταξύ LLMs και MCP διακομιστών.

#### Rust

Αυτό το παράδειγμα υποθέτει ότι έχετε έναν MCP διακομιστή βασισμένο στη Rust που εκτελείται. Αν δεν έχετε, ανατρέξτε στο μάθημα [01-first-server](../01-first-server/README.md) για να δημιουργήσετε τον διακομιστή.

Μόλις έχετε τον MCP διακομιστή σας στη Rust, ανοίξτε ένα τερματικό και πλοηγηθείτε στον ίδιο κατάλογο με τον διακομιστή. Στη συνέχεια, εκτελέστε την παρακάτω εντολή για να δημιουργήσετε ένα νέο έργο πελάτη LLM:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Προσθέστε τις παρακάτω εξαρτήσεις στο αρχείο `Cargo.toml`:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Δεν υπάρχει επίσημη βιβλιοθήκη Rust για το OpenAI, ωστόσο, το `async-openai` crate είναι μια [βιβλιοθήκη που διατηρείται από την κοινότητα](https://platform.openai.com/docs/libraries/rust#rust) και χρησιμοποιείται ευρέως.

Ανοίξτε το αρχείο `src/main.rs` και αντικαταστήστε το περιεχόμενό του με τον παρακάτω κώδικα:

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

Αυτός ο κώδικας δημιουργεί μια βασική εφαρμογή Rust που θα συνδεθεί με έναν MCP διακομιστή και τα GitHub Models για αλληλεπιδράσεις LLM.

> [!IMPORTANT]
> Βεβαιωθείτε ότι έχετε ορίσει τη μεταβλητή περιβάλλοντος `OPENAI_API_KEY` με το GitHub token σας πριν εκτελέσετε την εφαρμογή.

Ωραία, για το επόμενο βήμα, ας καταγράψουμε τις δυνατότητες στον διακομιστή.

### -2- Καταγραφή δυνατοτήτων του διακομιστή

Τώρα θα συνδεθούμε με τον διακομιστή και θα ζητήσουμε τις δυνατότητές του:

#### TypeScript

Στην ίδια κλάση, προσθέστε τις παρακάτω μεθόδους:

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

Στον παραπάνω κώδικα έχουμε:

- Προσθέσει κώδικα για σύνδεση με τον διακομιστή, `connectToServer`.
- Δημιουργήσει μια μέθοδο `run` υπεύθυνη για τη διαχείριση της ροής της εφαρμογής μας. Μέχρι στιγμής καταγράφει μόνο τα εργαλεία, αλλά θα προσθέσουμε περισσότερα σύντομα.

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

Αυτό που προσθέσαμε:

- Καταγραφή πόρων και εργαλείων και εκτύπωσή τους. Για τα εργαλεία καταγράφουμε επίσης το `inputSchema`, το οποίο θα χρησιμοποιήσουμε αργότερα.

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

Στον παραπάνω κώδικα έχουμε:

- Καταγράψει τα εργαλεία που είναι διαθέσιμα στον MCP διακομιστή.
- Για κάθε εργαλείο, καταγράψει το όνομα, την περιγραφή και το σχήμα του. Το τελευταίο είναι κάτι που θα χρησιμοποιήσουμε για να καλέσουμε τα εργαλεία σύντομα.

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

Στον παραπάνω κώδικα έχουμε:

- Δημιουργήσει έναν `McpToolProvider` που ανακαλύπτει και καταγράφει αυτόματα όλα τα εργαλεία από τον MCP διακομιστή.
- Ο πάροχος εργαλείων χειρίζεται την μετατροπή μεταξύ των σχημάτων εργαλείων MCP και της μορφής εργαλείων του LangChain4j εσωτερικά.
- Αυτή η προσέγγιση αφαιρεί τη χειροκίνητη διαδικασία καταγραφής και μετατροπής εργαλείων.

#### Rust

Η ανάκτηση εργαλείων από τον MCP διακομιστή γίνεται χρησιμοποιώντας τη μέθοδο `list_tools`. Στη συνάρτηση `main`, μετά τη ρύθμιση του MCP πελάτη, προσθέστε τον παρακάτω κώδικα:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Μετατροπή δυνατοτήτων του διακομιστή σε εργαλεία LLM

Το επόμενο βήμα μετά την καταγραφή των δυνατοτήτων του διακομιστή είναι να τις μετατρέψουμε σε μορφή που κατανοεί το LLM. Μόλις το κάνουμε αυτό, μπορούμε να παρέχουμε αυτές τις δυνατότητες ως εργαλεία στο LLM.

#### TypeScript

1. Προσθέστε τον παρακάτω κώδικα για να μετατρέψετε την απάντηση από τον MCP διακομιστή σε μορφή εργαλείου που μπορεί να χρησιμοποιήσει το LLM:

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

    Ο παραπάνω κώδικας παίρνει μια απάντηση από τον MCP διακομιστή και τη μετατρέπει σε μορφή ορισμού εργαλείου που μπορεί να κατανοήσει το LLM.

1. Ας ενημερώσουμε τη μέθοδο `run` για να καταγράψουμε τις δυνατότητες του διακομιστή:

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

    Στον παραπάνω κώδικα, έχουμε ενημερώσει τη μέθοδο `run` για να διατρέξει το αποτέλεσμα και για κάθε καταχώρηση να καλέσει το `openAiToolAdapter`.

#### Python

1. Πρώτα, ας δημιουργήσουμε την παρακάτω συνάρτηση μετατροπέα:

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

    Στην παραπάνω συνάρτηση `convert_to_llm_tools` παίρνουμε μια απάντηση εργαλείου MCP και τη μετατρέπουμε σε μορφή που μπορεί να κατανοήσει το LLM.

1. Στη συνέχεια, ας ενημερώσουμε τον κώδικα του πελάτη μας για να αξιοποιήσει αυτή τη συνάρτηση όπως παρακάτω:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Εδώ, προσθέτουμε μια κλήση στο `convert_to_llm_tool` για να μετατρέψουμε την απάντηση εργαλείου MCP σε κάτι που μπορούμε να δώσουμε στο LLM αργότερα.

#### .NET

1. Ας προσθέσουμε κώδικα για να μετατρέψουμε την απάντηση εργαλείου MCP σε κάτι που μπορεί να κατανοήσει το LLM:

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

Στον παραπάνω κώδικα έχουμε:

- Δημιουργήσει μια συνάρτηση `ConvertFrom` που παίρνει όνομα, περιγραφή και σχήμα εισόδου.
- Ορίσει λειτουργικότητα που δημιουργεί έναν FunctionDefinition που περνάει σε έναν ChatCompletionsDefinition. Το τελευταίο είναι κάτι που μπορεί να κατανοήσει το LLM.

1. Ας δούμε πώς μπορούμε να ενημερώσουμε κάποιον υπάρχοντα κώδικα για να αξιοποιήσει αυτή τη συνάρτηση παραπάνω:

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

Στον παραπάνω κώδικα έχουμε:

- Ορίσει μια απλή διεπαφή `Bot` για αλληλεπιδράσεις φυσικής γλώσσας.
- Χρησιμοποιήσει τις `AiServices` του LangChain4j για να συνδέσει αυτόματα το LLM με τον πάροχο εργαλείων MCP.
- Το πλαίσιο χειρίζεται αυτόματα τη μετατροπή σχημάτων εργαλείων και την κλήση λειτουργιών.
- Αυτή η προσέγγιση εξαλείφει τη χειροκίνητη μετατροπή εργαλείων - το LangChain4j χειρίζεται όλη την πολυπλοκότητα της μετατροπής εργαλείων MCP σε μορφή συμβατή με LLM.

#### Rust

Για να μετατρέψουμε την απάντηση εργαλείου MCP σε μορφή που μπορεί να κατανοήσει το LLM, θα προσθέσουμε μια βοηθητική συνάρτηση που μορφοποιεί την καταγραφή εργαλείων. Προσθέστε τον παρακάτω κώδικα στο αρχείο `main.rs` κάτω από τη συνάρτηση `main`. Αυτό θα καλείται κατά την υποβολή αιτημάτων στο LLM:

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

Ωραία, είμαστε έτοιμοι να χειριστούμε οποιαδήποτε αιτήματα χρήστη, οπότε ας το αντιμετωπίσουμε στη συνέχεια.

### -4- Διαχείριση αιτήματος προτροπής χρήστη

Σε αυτό το μέρος του κώδικα, θα διαχειριστούμε αιτήματα χρήστη.

#### TypeScript

1. Προσθέστε μια μέθοδο που θα χρησιμοποιηθεί για να καλέσει το LLM:

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

    Στον παραπάνω κώδικα έχουμε:

    - Προσθέσει μια μέθοδο `callTools`.
    - Η μέθοδος παίρνει μια απάντηση LLM και ελέγχει αν έχουν κληθεί εργαλεία, αν υπάρχουν:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Καλεί ένα εργαλείο, αν το LLM υποδεικνύει ότι πρέπει να κληθεί:

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

1. Ενημερώστε τη μέθοδο `run` για να περιλαμβάνει κλήσεις στο LLM και την κλήση `callTools`:

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

Ωραία, ας καταγράψουμε τον κώδικα πλήρως:

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

1. Ας προσθέσουμε κάποιες εισαγωγές που χρειάζονται για να καλέσουμε ένα LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Στη συνέχεια, ας προσθέσουμε τη συνάρτηση που θα καλέσει το LLM:

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

    Στον παραπάνω κώδικα έχουμε:

    - Μεταβιβάσει τις λειτουργίες μας, που βρήκαμε στον MCP διακομιστή και μετατρέψαμε, στο LLM.
    - Στη συνέχεια, καλέσαμε το LLM με αυτές τις λειτουργίες.
    - Στη συνέχεια, εξετάζουμε το αποτέλεσμα για να δούμε ποιες λειτουργίες πρέπει να καλέσουμε, αν υπάρχουν.
    - Τέλος, μεταβιβάζουμε έναν πίνακα λειτουργιών για κλήση.

1. Τελικό βήμα, ας ενημερώσουμε τον κύριο κώδικα μας:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Εκεί, αυτό ήταν το τελικό βήμα, στον παραπάνω κώδικα:

    - Καλούμε ένα εργαλείο MCP μέσω του `call_tool` χρησιμοποιώντας μια λειτουργία που το LLM σκέφτηκε ότι πρέπει να καλέσουμε βάσει της προτροπής μας.
    - Εκτυπώνουμε το αποτέλεσμα της κλήσης εργαλείου στον MCP διακομιστή.

#### .NET

1. Ας δείξουμε λίγο κώδικα για την υποβολή αιτήματος προτροπής LLM:

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

    Στον παραπάνω κώδικα έχουμε:

    - Ανακτήσει εργαλεία από τον MCP διακομιστή, `var tools = await GetMcpTools()`.
    - Ορίσει μια προτροπή χρήστη `userMessage`.
    - Δημιουργήσει ένα αντικείμενο επιλογών που καθορίζει το μοντέλο και τα εργαλεία.
    - Υποβάλει ένα αίτημα προς το LLM.

1. Ένα τελευταίο βήμα, ας δούμε αν το LLM σκέφτεται ότι πρέπει να καλέσουμε μια λειτουργία:

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

    Σ
Η απάντηση από το LLM θα περιέχει έναν πίνακα `choices`. Θα χρειαστεί να επεξεργαστούμε το αποτέλεσμα για να δούμε αν υπάρχουν `tool_calls`. Αυτό μας ενημερώνει ότι το LLM ζητά να κληθεί ένα συγκεκριμένο εργαλείο με επιχειρήματα. Προσθέστε τον παρακάτω κώδικα στο τέλος του αρχείου `main.rs` για να ορίσετε μια συνάρτηση που θα χειρίζεται την απάντηση του LLM:

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

Αν υπάρχουν `tool_calls`, εξάγει τις πληροφορίες του εργαλείου, καλεί τον MCP server με το αίτημα του εργαλείου και προσθέτει τα αποτελέσματα στα μηνύματα της συνομιλίας. Στη συνέχεια, συνεχίζει τη συνομιλία με το LLM και τα μηνύματα ενημερώνονται με την απάντηση του βοηθού και τα αποτελέσματα της κλήσης του εργαλείου.

Για να εξάγουμε τις πληροφορίες της κλήσης εργαλείου που επιστρέφει το LLM για τις κλήσεις MCP, θα προσθέσουμε μια άλλη βοηθητική συνάρτηση για να εξάγουμε όλα όσα χρειάζονται για την κλήση. Προσθέστε τον παρακάτω κώδικα στο τέλος του αρχείου `main.rs`:

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

Με όλα τα κομμάτια στη θέση τους, μπορούμε τώρα να χειριστούμε την αρχική προτροπή του χρήστη και να καλέσουμε το LLM. Ενημερώστε τη συνάρτηση `main` για να συμπεριλάβετε τον παρακάτω κώδικα:

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

Αυτό θα κάνει ερώτημα στο LLM με την αρχική προτροπή του χρήστη ζητώντας το άθροισμα δύο αριθμών και θα επεξεργαστεί την απάντηση για να χειριστεί δυναμικά τις κλήσεις εργαλείων.

Μπράβο, τα καταφέρατε!

## Ανάθεση

Πάρτε τον κώδικα από την άσκηση και δημιουργήστε τον server με περισσότερα εργαλεία. Στη συνέχεια, δημιουργήστε έναν client με ένα LLM, όπως στην άσκηση, και δοκιμάστε τον με διαφορετικές προτροπές για να βεβαιωθείτε ότι όλα τα εργαλεία του server καλούνται δυναμικά. Αυτός ο τρόπος δημιουργίας ενός client σημαίνει ότι ο τελικός χρήστης θα έχει μια εξαιρετική εμπειρία χρήσης, καθώς θα μπορεί να χρησιμοποιεί προτροπές αντί για ακριβείς εντολές client και θα είναι ανυποψίαστος για οποιονδήποτε MCP server που καλείται.

## Λύση

[Λύση](/03-GettingStarted/03-llm-client/solution/README.md)

## Βασικά Σημεία

- Η προσθήκη ενός LLM στον client σας παρέχει έναν καλύτερο τρόπο για τους χρήστες να αλληλεπιδρούν με MCP Servers.
- Πρέπει να μετατρέψετε την απάντηση του MCP Server σε κάτι που το LLM μπορεί να κατανοήσει.

## Παραδείγματα

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## Πρόσθετοι Πόροι

## Τι Ακολουθεί

- Επόμενο: [Κατανάλωση server χρησιμοποιώντας το Visual Studio Code](../04-vscode/README.md)

---

**Αποποίηση ευθύνης**:  
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία αυτόματης μετάφρασης [Co-op Translator](https://github.com/Azure/co-op-translator). Παρόλο που καταβάλλουμε προσπάθειες για ακρίβεια, παρακαλούμε να έχετε υπόψη ότι οι αυτοματοποιημένες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα θα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή εσφαλμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.