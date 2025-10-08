<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:44:52+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "he"
}
-->
# יצירת לקוח עם LLM

עד כה ראיתם כיצד ליצור שרת ולקוח. הלקוח יכול לקרוא לשרת באופן מפורש כדי לרשום את הכלים, המשאבים וההנחיות שלו. עם זאת, זו אינה גישה מעשית במיוחד. המשתמש שלכם חי בעידן האג'נטי ומצפה להשתמש בהנחיות ולתקשר עם LLM כדי לעשות זאת. מבחינת המשתמש, לא משנה אם אתם משתמשים ב-MCP או לא כדי לאחסן את היכולות שלכם, אך הם מצפים לתקשר בשפה טבעית. אז איך פותרים את זה? הפתרון הוא להוסיף LLM ללקוח.

## סקירה כללית

בשיעור זה נתמקד בהוספת LLM ללקוח שלכם ונראה כיצד זה מספק חוויית משתמש טובה יותר.

## מטרות למידה

בסוף השיעור הזה תוכלו:

- ליצור לקוח עם LLM.
- לתקשר בצורה חלקה עם שרת MCP באמצעות LLM.
- לספק חוויית משתמש טובה יותר בצד הלקוח.

## גישה

בואו ננסה להבין את הגישה שעלינו לנקוט. הוספת LLM נשמעת פשוטה, אבל האם באמת נעשה זאת?

כך הלקוח יתקשר עם השרת:

1. יצירת חיבור לשרת.

1. רישום יכולות, הנחיות, משאבים וכלים ושמירת הסכימה שלהם.

1. הוספת LLM והעברת היכולות השמורות והסכימה שלהם בפורמט שה-LLM מבין.

1. טיפול בהנחיית משתמש על ידי העברתה ל-LLM יחד עם הכלים שרשומים על ידי הלקוח.

מעולה, עכשיו אנחנו מבינים איך אפשר לעשות זאת ברמה גבוהה, בואו ננסה זאת בתרגיל הבא.

## תרגיל: יצירת לקוח עם LLM

בתרגיל זה נלמד להוסיף LLM ללקוח שלנו.

### אימות באמצעות GitHub Personal Access Token

יצירת טוקן GitHub היא תהליך פשוט. כך עושים זאת:

- גשו להגדרות GitHub – לחצו על תמונת הפרופיל שלכם בפינה הימנית העליונה ובחרו "Settings".
- נווטו ל-Developer Settings – גללו מטה ולחצו על "Developer Settings".
- בחרו ב-Personal Access Tokens – לחצו על "Fine-grained tokens" ואז על "Generate new token".
- הגדירו את הטוקן שלכם – הוסיפו הערה לצורך זיהוי, הגדירו תאריך תפוגה ובחרו את ההרשאות הנדרשות. במקרה זה, ודאו להוסיף את ההרשאה ל-Models.
- צרו והעתיקו את הטוקן – לחצו על "Generate token" וודאו להעתיק אותו מיד, מכיוון שלא תוכלו לראות אותו שוב.

### -1- התחברות לשרת

בואו ניצור את הלקוח שלנו תחילה:

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

בקוד שלמעלה:

- ייבאנו את הספריות הנדרשות.
- יצרנו מחלקה עם שני חברים, `client` ו-`openai`, שיעזרו לנו לנהל לקוח ולתקשר עם LLM בהתאמה.
- הגדרנו את מופע ה-LLM שלנו לשימוש ב-GitHub Models על ידי הגדרת `baseUrl` שיצביע על ה-API.

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

בקוד שלמעלה:

- ייבאנו את הספריות הנדרשות ל-MCP.
- יצרנו לקוח.

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

תחילה, תצטרכו להוסיף את התלויות של LangChain4j לקובץ `pom.xml` שלכם. הוסיפו את התלויות הללו כדי לאפשר אינטגרציה עם MCP ותמיכה ב-GitHub Models:

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

לאחר מכן, צרו את מחלקת הלקוח שלכם ב-Java:

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

בקוד שלמעלה:

- **הוספנו תלויות LangChain4j**: נדרשות לאינטגרציה עם MCP, לקוח OpenAI רשמי ותמיכה ב-GitHub Models.
- **ייבאנו את ספריות LangChain4j**: לאינטגרציה עם MCP ולפונקציונליות מודל הצ'אט של OpenAI.
- **יצרנו `ChatLanguageModel`**: מוגדר לשימוש ב-GitHub Models עם הטוקן שלכם.
- **הגדרנו HTTP transport**: באמצעות Server-Sent Events (SSE) להתחברות לשרת MCP.
- **יצרנו לקוח MCP**: שיטפל בתקשורת עם השרת.
- **השתמשנו בתמיכה המובנית של LangChain4j ב-MCP**: שמפשטת את האינטגרציה בין LLM לשרתים של MCP.

#### Rust

דוגמה זו מניחה שיש לכם שרת MCP מבוסס Rust פועל. אם אין לכם אחד כזה, חזרו לשיעור [01-first-server](../01-first-server/README.md) כדי ליצור את השרת.

לאחר שיש לכם שרת MCP מבוסס Rust, פתחו טרמינל ונווטו לאותו ספרייה כמו השרת. לאחר מכן הריצו את הפקודה הבאה כדי ליצור פרויקט לקוח חדש עם LLM:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

הוסיפו את התלויות הבאות לקובץ `Cargo.toml` שלכם:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> אין ספרייה רשמית ל-Rust עבור OpenAI, אך הספרייה `async-openai` היא [ספרייה שמנוהלת על ידי הקהילה](https://platform.openai.com/docs/libraries/rust#rust) ונפוצה בשימוש.

פתחו את קובץ `src/main.rs` והחליפו את תוכנו בקוד הבא:

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

קוד זה מגדיר אפליקציה בסיסית ב-Rust שתתחבר לשרת MCP ול-GitHub Models לצורך אינטראקציות עם LLM.

> [!IMPORTANT]
> ודאו להגדיר את משתנה הסביבה `OPENAI_API_KEY` עם הטוקן שלכם מ-GitHub לפני הרצת האפליקציה.

מעולה, בשלב הבא נרשום את היכולות בשרת.

### -2- רישום יכולות השרת

כעת נתחבר לשרת ונבקש את היכולות שלו:

#### TypeScript

באותה מחלקה, הוסיפו את השיטות הבאות:

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

בקוד שלמעלה:

- הוספנו קוד להתחברות לשרת, `connectToServer`.
- יצרנו שיטה `run` שאחראית על ניהול זרימת האפליקציה שלנו. עד כה היא רק רושמת את הכלים, אך נוסיף לה עוד בהמשך.

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

הנה מה שהוספנו:

- רישום משאבים וכלים והדפסתם. עבור כלים אנו גם רושמים את `inputSchema` שבו נשתמש מאוחר יותר.

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

בקוד שלמעלה:

- רשמנו את הכלים הזמינים בשרת MCP.
- עבור כל כלי, רשמנו שם, תיאור והסכימה שלו. האחרון הוא משהו שנשתמש בו כדי לקרוא לכלים בקרוב.

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

בקוד שלמעלה:

- יצרנו `McpToolProvider` שמגלה ומרשום אוטומטית את כל הכלים מהשרת MCP.
- ספק הכלים מטפל בהמרה בין סכימות הכלים של MCP לפורמט הכלים של LangChain4j באופן פנימי.
- גישה זו מפשטת את תהליך רישום הכלים וההמרה.

#### Rust

רישום כלים מהשרת MCP נעשה באמצעות השיטה `list_tools`. בפונקציה `main` שלכם, לאחר הגדרת לקוח MCP, הוסיפו את הקוד הבא:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- המרת יכולות השרת לכלים של LLM

השלב הבא לאחר רישום יכולות השרת הוא להמיר אותן לפורמט שה-LLM מבין. ברגע שנעשה זאת, נוכל לספק את היכולות הללו ככלים ל-LLM.

#### TypeScript

1. הוסיפו את הקוד הבא להמרת תגובה משרת MCP לפורמט כלי שה-LLM יכול להשתמש בו:

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

    הקוד שלמעלה לוקח תגובה משרת MCP וממיר אותה להגדרת כלי שה-LLM יכול להבין.

1. בואו נעדכן את השיטה `run` הבאה כדי לרשום את יכולות השרת:

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

    בקוד שלמעלה, עדכנו את השיטה `run` כדי למפות את התוצאה ועבור כל ערך לקרוא ל-`openAiToolAdapter`.

#### Python

1. תחילה, בואו ניצור את פונקציית ההמרה הבאה:

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

    בפונקציה `convert_to_llm_tools` אנו לוקחים תגובת כלי MCP וממירים אותה לפורמט שה-LLM יכול להבין.

1. לאחר מכן, בואו נעדכן את קוד הלקוח שלנו כדי לנצל את הפונקציה הזו כך:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    כאן, אנו מוסיפים קריאה ל-`convert_to_llm_tool` כדי להמיר את תגובת כלי MCP למשהו שנוכל להזין ל-LLM מאוחר יותר.

#### .NET

1. בואו נוסיף קוד להמרת תגובת כלי MCP למשהו שה-LLM יכול להבין:

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

בקוד שלמעלה:

- יצרנו פונקציה `ConvertFrom` שלוקחת שם, תיאור וסכימת קלט.
- הגדרנו פונקציונליות שיוצרת FunctionDefinition שמועברת ל-ChatCompletionsDefinition. האחרון הוא משהו שה-LLM יכול להבין.

1. בואו נראה איך אפשר לעדכן קוד קיים כדי לנצל את הפונקציה הזו:

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

בקוד שלמעלה:

- הגדרנו ממשק `Bot` פשוט לאינטראקציות בשפה טבעית.
- השתמשנו ב-AiServices של LangChain4j כדי לקשור אוטומטית את ה-LLM עם ספק הכלים של MCP.
- המסגרת מטפלת אוטומטית בהמרת סכימות הכלים ובקריאות פונקציות מאחורי הקלעים.
- גישה זו מבטלת את הצורך בהמרת כלים ידנית - LangChain4j מטפל בכל המורכבות של המרת כלים של MCP לפורמט תואם ל-LLM.

#### Rust

כדי להמיר את תגובת כלי MCP לפורמט שה-LLM יכול להבין, נוסיף פונקציית עזר שמעצבת את רישום הכלים. הוסיפו את הקוד הבא לקובץ `main.rs` שלכם מתחת לפונקציה `main`. זה ייקרא בעת ביצוע בקשות ל-LLM:

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

מעולה, אנחנו מוכנים לטפל בכל בקשות המשתמש, אז בואו ניגש לזה.

### -4- טיפול בבקשת הנחיית משתמש

בחלק זה של הקוד, נטפל בבקשות משתמש.

#### TypeScript

1. הוסיפו שיטה שתשמש לקריאה ל-LLM:

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

    בקוד שלמעלה:

    - הוספנו שיטה `callTools`.
    - השיטה לוקחת תגובת LLM ובודקת אילו כלים נקראו, אם בכלל:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - קוראת לכלי, אם ה-LLM מציין שיש לקרוא לו:

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

1. עדכנו את השיטה `run` לכלול קריאות ל-LLM וקריאה ל-`callTools`:

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

מעולה, בואו נרשום את הקוד במלואו:

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

1. בואו נוסיף כמה ייבואים שנדרשים לקריאה ל-LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. לאחר מכן, נוסיף את הפונקציה שתבצע קריאה ל-LLM:

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

    בקוד שלמעלה:

    - העברנו את הפונקציות שלנו, שמצאנו בשרת MCP והמרנו, ל-LLM.
    - לאחר מכן קראנו ל-LLM עם הפונקציות הללו.
    - לאחר מכן, אנו בודקים את התוצאה כדי לראות אילו פונקציות יש לקרוא, אם בכלל.
    - לבסוף, אנו מעבירים מערך של פונקציות לקריאה.

1. שלב אחרון, בואו נעדכן את הקוד הראשי שלנו:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    שם, זה היה השלב האחרון, בקוד שלמעלה אנו:

    - קוראים לכלי MCP דרך `call_tool` באמצעות פונקציה שה-LLM חשב שיש לקרוא לה על סמך ההנחיה שלנו.
    - מדפיסים את תוצאת קריאת הכלי לשרת MCP.

#### .NET

1. בואו נראה קוד לביצוע בקשת הנחיית LLM:

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

    בקוד שלמעלה:

    - הבאנו כלים משרת MCP, `var tools = await GetMcpTools()`.
    - הגדרנו הנחיית משתמש `userMessage`.
    - יצרנו אובייקט אפשרויות שמפרט מודל וכלים.
    - ביצענו בקשה ל-LLM.

1. שלב אחד אחרון, בואו נראה אם ה-LLM חושב שיש לקרוא לפונקציה:

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

    בקוד שלמעלה:

    - עברנו על רשימת קריאות פונקציות.
    - עבור כל קריאת כלי, חילצנו שם וארגומנטים וקראנו לכלי בשרת MCP באמצעות לקוח MCP. לבסוף הדפסנו את התוצאות.

הנה הקוד במלואו:

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

בקוד שלמעלה:

- השתמשנו בהנחיות פשוטות בשפה טבעית כדי לתקשר עם כלי שרת MCP.
- המסגרת LangChain4j מטפלת אוטומטית ב:
  - המרת הנחיות משתמש לקריאות כלים בעת הצורך.
  - קריאה לכלי MCP המתאים על סמך החלטת ה-LLM.
  - ניהול זרימת השיחה בין ה-LLM לשרת MCP.
- השיטה `bot.chat()` מחזירה תגובות בשפה טבעית שעשויות לכלול תוצאות מביצועי כלי MCP.
- גישה זו מספקת חוויית משתמש חלקה שבה המשתמשים אינם צריכים לדעת על יישום MCP הבסיסי.

דוגמת קוד מלאה:

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

כאן מתבצע רוב העבודה. נקרא ל-LLM עם הנחיית המשתמש הראשונית, ואז נעבד את התגובה כדי לראות אם יש צורך לקרוא לכלים. אם כן, נקרא לכלים הללו ונמשיך את השיחה עם ה-LLM עד שאין צורך לקרוא לכלים נוספים ויש לנו תגובה סופית.

נבצע קריאות מרובות ל-LLM, אז בואו נגדיר פונקציה שתטפל בקריאת ה-LLM. הוסיפו את הפונקציה הבאה לקובץ `main.rs` שלכם:

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

פונקציה זו לוקחת את לקוח ה-LLM, רשימת הודעות (כולל הנחיית המשתמש), כלים משרת MCP, ושולחת בקשה ל-LLM, ומחזירה את התגובה.
התגובה מה-LLM תכיל מערך של `choices`. נצטרך לעבד את התוצאה כדי לבדוק אם קיימים `tool_calls`. זה מאפשר לנו לדעת שה-LLM מבקש לקרוא לכלי מסוים עם ארגומנטים. הוסף את הקוד הבא לתחתית קובץ `main.rs` שלך כדי להגדיר פונקציה שתטפל בתגובה מה-LLM:

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

אם קיימים `tool_calls`, הפונקציה תחלץ את המידע על הכלי, תבצע קריאה לשרת MCP עם בקשת הכלי, ותוסיף את התוצאות להודעות השיחה. לאחר מכן, היא תמשיך את השיחה עם ה-LLM וההודעות יתעדכנו עם תגובת העוזר ותוצאות קריאת הכלי.

כדי לחלץ מידע על קריאת כלי שה-LLM מחזיר עבור קריאות MCP, נוסיף פונקציית עזר נוספת שתחלץ את כל מה שצריך כדי לבצע את הקריאה. הוסף את הקוד הבא לתחתית קובץ `main.rs` שלך:

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

עם כל החלקים במקום, עכשיו נוכל לטפל בהנחיה הראשונית של המשתמש ולקרוא ל-LLM. עדכן את פונקציית `main` שלך כדי לכלול את הקוד הבא:

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

זה יבצע שאילתה ל-LLM עם ההנחיה הראשונית של המשתמש המבקשת את סכום שני מספרים, ויעבד את התגובה כדי לטפל באופן דינמי בקריאות לכלים.

מעולה, הצלחת!

## משימה

קח את הקוד מהתרגיל ובנה את השרת עם עוד כלים. לאחר מכן צור לקוח עם LLM, כמו בתרגיל, ובדוק אותו עם הנחיות שונות כדי לוודא שכל הכלים של השרת שלך נקראים באופן דינמי. דרך זו של בניית לקוח מבטיחה חוויית משתמש מצוינת, שכן המשתמשים יוכלו להשתמש בהנחיות במקום פקודות לקוח מדויקות, ולא יהיו מודעים לכך שמתבצעת קריאה לשרת MCP.

## פתרון

[פתרון](/03-GettingStarted/03-llm-client/solution/README.md)

## נקודות מפתח

- הוספת LLM ללקוח שלך מספקת דרך טובה יותר למשתמשים לתקשר עם שרתי MCP.
- יש להמיר את תגובת שרת MCP למשהו שה-LLM יכול להבין.

## דוגמאות

- [מחשבון Java](../samples/java/calculator/README.md)
- [מחשבון .Net](../../../../03-GettingStarted/samples/csharp)
- [מחשבון JavaScript](../samples/javascript/README.md)
- [מחשבון TypeScript](../samples/typescript/README.md)
- [מחשבון Python](../../../../03-GettingStarted/samples/python)
- [מחשבון Rust](../../../../03-GettingStarted/samples/rust)

## משאבים נוספים

## מה הלאה

- הבא: [צריכת שרת באמצעות Visual Studio Code](../04-vscode/README.md)

---

**הצהרת אחריות**:  
מסמך זה תורגם באמצעות שירות תרגום AI [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש להיות מודעים לכך שתרגומים אוטומטיים עשויים להכיל שגיאות או אי דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור סמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי אנושי. אנו לא נושאים באחריות לכל אי הבנות או פרשנויות שגויות הנובעות משימוש בתרגום זה.