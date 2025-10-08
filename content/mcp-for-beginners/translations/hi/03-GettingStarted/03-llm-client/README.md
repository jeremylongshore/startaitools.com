<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T13:51:38+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "hi"
}
-->
# LLM के साथ क्लाइंट बनाना

अब तक, आपने देखा कि सर्वर और क्लाइंट कैसे बनाते हैं। क्लाइंट सर्वर को स्पष्ट रूप से कॉल करके उसके टूल्स, संसाधनों और प्रॉम्प्ट्स की सूची प्राप्त कर सकता है। हालांकि, यह तरीका बहुत व्यावहारिक नहीं है। आपका उपयोगकर्ता एजेंटिक युग में रहता है और वह प्रॉम्प्ट्स का उपयोग करके और LLM के साथ संवाद करके काम करना चाहता है। आपके उपयोगकर्ता को इस बात से फर्क नहीं पड़ता कि आप अपनी क्षमताओं को MCP में संग्रहीत करते हैं या नहीं, लेकिन वे प्राकृतिक भाषा का उपयोग करके संवाद करने की उम्मीद करते हैं। तो हम इसे कैसे हल करें? समाधान क्लाइंट में LLM जोड़ने के बारे में है।

## अवलोकन

इस पाठ में हम आपके क्लाइंट में LLM जोड़ने पर ध्यान केंद्रित करेंगे और दिखाएंगे कि यह आपके उपयोगकर्ता के लिए बेहतर अनुभव कैसे प्रदान करता है।

## सीखने के उद्देश्य

इस पाठ के अंत तक, आप सक्षम होंगे:

- LLM के साथ एक क्लाइंट बनाना।
- MCP सर्वर के साथ LLM का उपयोग करके सहजता से संवाद करना।
- क्लाइंट साइड पर बेहतर उपयोगकर्ता अनुभव प्रदान करना।

## दृष्टिकोण

आइए समझते हैं कि हमें कौन सा दृष्टिकोण अपनाना चाहिए। LLM जोड़ना सरल लगता है, लेकिन क्या हम वास्तव में ऐसा करेंगे?

यहां बताया गया है कि क्लाइंट सर्वर के साथ कैसे संवाद करेगा:

1. सर्वर के साथ कनेक्शन स्थापित करें।

1. क्षमताओं, प्रॉम्प्ट्स, संसाधनों और टूल्स की सूची बनाएं और उनकी स्कीमा को सहेजें।

1. एक LLM जोड़ें और सहेजी गई क्षमताओं और उनकी स्कीमा को उस प्रारूप में पास करें जिसे LLM समझता है।

1. उपयोगकर्ता प्रॉम्प्ट को संभालें और इसे LLM को पास करें, साथ ही क्लाइंट द्वारा सूचीबद्ध टूल्स को भी।

बहुत अच्छा, अब हम समझ गए हैं कि इसे उच्च स्तर पर कैसे किया जा सकता है। आइए इसे नीचे दिए गए अभ्यास में आजमाएं।

## अभ्यास: LLM के साथ क्लाइंट बनाना

इस अभ्यास में, हम अपने क्लाइंट में LLM जोड़ना सीखेंगे।

### GitHub व्यक्तिगत एक्सेस टोकन का उपयोग करके प्रमाणीकरण

GitHub टोकन बनाना एक सरल प्रक्रिया है। इसे कैसे करें:

- GitHub सेटिंग्स पर जाएं – ऊपर दाईं ओर अपने प्रोफ़ाइल चित्र पर क्लिक करें और सेटिंग्स चुनें।
- डेवलपर सेटिंग्स पर जाएं – नीचे स्क्रॉल करें और डेवलपर सेटिंग्स पर क्लिक करें।
- व्यक्तिगत एक्सेस टोकन चुनें – Fine-grained tokens पर क्लिक करें और नया टोकन जनरेट करें।
- अपने टोकन को कॉन्फ़िगर करें – संदर्भ के लिए एक नोट जोड़ें, समाप्ति तिथि सेट करें, और आवश्यक स्कोप (अनुमतियां) चुनें। इस मामले में, सुनिश्चित करें कि Models अनुमति जोड़ें।
- टोकन जनरेट करें और कॉपी करें – Generate token पर क्लिक करें और इसे तुरंत कॉपी करना सुनिश्चित करें, क्योंकि आप इसे फिर से नहीं देख पाएंगे।

### -1- सर्वर से कनेक्ट करें

आइए पहले अपना क्लाइंट बनाएं:

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

ऊपर दिए गए कोड में हमने:

- आवश्यक लाइब्रेरी आयात की हैं।
- एक क्लास बनाई है जिसमें दो सदस्य हैं, `client` और `openai`, जो हमें क्लाइंट प्रबंधन और LLM के साथ संवाद करने में मदद करेंगे।
- हमारे LLM इंस्टेंस को GitHub Models का उपयोग करने के लिए कॉन्फ़िगर किया है, `baseUrl` को इन्फरेंस API की ओर इंगित करके।

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

ऊपर दिए गए कोड में हमने:

- MCP के लिए आवश्यक लाइब्रेरी आयात की हैं।
- एक क्लाइंट बनाया है।

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

सबसे पहले, आपको अपने `pom.xml` फ़ाइल में LangChain4j डिपेंडेंसी जोड़नी होगी। MCP इंटीग्रेशन और GitHub Models समर्थन सक्षम करने के लिए इन डिपेंडेंसी को जोड़ें:

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

फिर अपनी Java क्लाइंट क्लास बनाएं:

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

ऊपर दिए गए कोड में हमने:

- **LangChain4j डिपेंडेंसी जोड़ीं**: MCP इंटीग्रेशन, OpenAI आधिकारिक क्लाइंट, और GitHub Models समर्थन के लिए आवश्यक।
- **LangChain4j लाइब्रेरी आयात कीं**: MCP इंटीग्रेशन और OpenAI चैट मॉडल कार्यक्षमता के लिए।
- **`ChatLanguageModel` बनाया**: GitHub Models का उपयोग करने के लिए आपके GitHub टोकन के साथ कॉन्फ़िगर किया गया।
- **HTTP ट्रांसपोर्ट सेट किया**: MCP सर्वर से कनेक्ट करने के लिए Server-Sent Events (SSE) का उपयोग किया।
- **MCP क्लाइंट बनाया**: जो सर्वर के साथ संवाद को संभालेगा।
- **LangChain4j का बिल्ट-इन MCP समर्थन उपयोग किया**: जो LLMs और MCP सर्वर के बीच इंटीग्रेशन को सरल बनाता है।

#### Rust

यह उदाहरण मानता है कि आपके पास एक Rust आधारित MCP सर्वर चल रहा है। यदि आपके पास ऐसा नहीं है, तो [01-first-server](../01-first-server/README.md) पाठ में वापस जाएं और सर्वर बनाएं।

एक बार जब आपके पास Rust MCP सर्वर हो, तो एक टर्मिनल खोलें और सर्वर के समान डायरेक्टरी में जाएं। फिर एक नया LLM क्लाइंट प्रोजेक्ट बनाने के लिए निम्नलिखित कमांड चलाएं:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

अपने `Cargo.toml` फ़ाइल में निम्नलिखित डिपेंडेंसी जोड़ें:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> OpenAI के लिए कोई आधिकारिक Rust लाइब्रेरी नहीं है, हालांकि, `async-openai` क्रेट एक [समुदाय द्वारा बनाए रखा लाइब्रेरी](https://platform.openai.com/docs/libraries/rust#rust) है जो आमतौर पर उपयोग की जाती है।

`src/main.rs` फ़ाइल खोलें और इसकी सामग्री को निम्नलिखित कोड से बदलें:

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

यह कोड एक बेसिक Rust एप्लिकेशन सेट करता है जो MCP सर्वर और GitHub Models के साथ LLM इंटरैक्शन के लिए कनेक्ट करेगा।

> [!IMPORTANT]
> एप्लिकेशन चलाने से पहले `OPENAI_API_KEY` पर्यावरण चर को अपने GitHub टोकन के साथ सेट करना सुनिश्चित करें।

बहुत अच्छा, अगले चरण में, आइए सर्वर पर क्षमताओं की सूची बनाएं।

### -2- सर्वर क्षमताओं की सूची बनाएं

अब हम सर्वर से कनेक्ट करेंगे और उसकी क्षमताओं के बारे में पूछेंगे:

#### TypeScript

उसी क्लास में निम्नलिखित विधियां जोड़ें:

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

ऊपर दिए गए कोड में हमने:

- सर्वर से कनेक्ट करने के लिए कोड जोड़ा, `connectToServer`।
- एक `run` विधि बनाई जो हमारे ऐप फ्लो को संभालने के लिए जिम्मेदार है। अभी तक यह केवल टूल्स की सूची बनाता है, लेकिन हम इसमें जल्द ही और जोड़ेंगे।

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

यहां हमने जोड़ा है:

- संसाधनों और टूल्स की सूची बनाई और उन्हें प्रिंट किया। टूल्स के लिए हमने `inputSchema` भी सूचीबद्ध किया है जिसे हम बाद में उपयोग करेंगे।

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

ऊपर दिए गए कोड में हमने:

- MCP सर्वर पर उपलब्ध टूल्स की सूची बनाई।
- प्रत्येक टूल के लिए नाम, विवरण और उसकी स्कीमा सूचीबद्ध की। बाद वाला वह है जिसे हम जल्द ही टूल्स को कॉल करने के लिए उपयोग करेंगे।

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

ऊपर दिए गए कोड में हमने:

- एक `McpToolProvider` बनाया जो MCP सर्वर से सभी टूल्स को स्वचालित रूप से खोजता और पंजीकृत करता है।
- टूल प्रोवाइडर आंतरिक रूप से MCP टूल स्कीमा और LangChain4j के टूल प्रारूप के बीच रूपांतरण को संभालता है।
- यह दृष्टिकोण मैनुअल टूल सूचीकरण और रूपांतरण प्रक्रिया को अमूर्त करता है।

#### Rust

MCP सर्वर से टूल्स प्राप्त करना `list_tools` विधि का उपयोग करके किया जाता है। अपने `main` फ़ंक्शन में, MCP क्लाइंट सेट करने के बाद निम्नलिखित कोड जोड़ें:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- सर्वर क्षमताओं को LLM टूल्स में बदलें

सर्वर क्षमताओं की सूची बनाने के बाद अगला कदम उन्हें उस प्रारूप में बदलना है जिसे LLM समझता है। एक बार जब हम ऐसा कर लेते हैं, तो हम इन क्षमताओं को LLM को टूल्स के रूप में प्रदान कर सकते हैं।

#### TypeScript

1. MCP सर्वर से प्रतिक्रिया को LLM के उपयोग के लिए टूल प्रारूप में बदलने के लिए निम्नलिखित कोड जोड़ें:

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

    ऊपर दिया गया कोड MCP सर्वर से प्रतिक्रिया लेता है और उसे टूल परिभाषा प्रारूप में बदलता है जिसे LLM समझ सकता है।

1. अगला, `run` विधि को अपडेट करें ताकि सर्वर क्षमताओं की सूची बनाई जा सके:

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

    ऊपर दिए गए कोड में, हमने `run` विधि को अपडेट किया है ताकि परिणाम के माध्यम से मैप किया जा सके और प्रत्येक प्रविष्टि के लिए `openAiToolAdapter` को कॉल किया जा सके।

#### Python

1. पहले, निम्नलिखित कन्वर्टर फ़ंक्शन बनाएं:

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

    ऊपर दिए गए `convert_to_llm_tools` फ़ंक्शन में हम MCP टूल प्रतिक्रिया लेते हैं और उसे उस प्रारूप में बदलते हैं जिसे LLM समझ सकता है।

1. अगला, अपने क्लाइंट कोड को इस फ़ंक्शन का लाभ उठाने के लिए अपडेट करें:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    यहां, हम MCP टूल प्रतिक्रिया को बदलने के लिए `convert_to_llm_tool` को कॉल कर रहे हैं ताकि इसे बाद में LLM को फीड किया जा सके।

#### .NET

1. MCP टूल प्रतिक्रिया को उस प्रारूप में बदलने के लिए कोड जोड़ें जिसे LLM समझ सकता है:

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

ऊपर दिए गए कोड में हमने:

- एक फ़ंक्शन `ConvertFrom` बनाया जो नाम, विवरण और इनपुट स्कीमा लेता है।
- एक FunctionDefinition बनाने की कार्यक्षमता परिभाषित की जो ChatCompletionsDefinition को पास की जाती है। बाद वाला वह है जिसे LLM समझ सकता है।

1. आइए देखें कि ऊपर दिए गए फ़ंक्शन का लाभ उठाने के लिए कुछ मौजूदा कोड को कैसे अपडेट किया जा सकता है:

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

ऊ
LLM की प्रतिक्रिया में `choices` का एक array होगा। हमें परिणाम को प्रोसेस करना होगा ताकि यह देखा जा सके कि कोई `tool_calls` मौजूद हैं या नहीं। इससे हमें पता चलता है कि LLM एक विशेष टूल को तर्कों के साथ कॉल करने का अनुरोध कर रहा है। अपने `main.rs` फाइल के अंत में निम्नलिखित कोड जोड़ें ताकि LLM प्रतिक्रिया को संभालने के लिए एक फ़ंक्शन परिभाषित किया जा सके:

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

यदि `tool_calls` मौजूद हैं, तो यह टूल की जानकारी निकालता है, MCP सर्वर को टूल अनुरोध के साथ कॉल करता है, और परिणामों को बातचीत संदेशों में जोड़ता है। इसके बाद यह LLM के साथ बातचीत जारी रखता है और संदेशों को सहायक की प्रतिक्रिया और टूल कॉल परिणामों के साथ अपडेट करता है।

MCP कॉल के लिए LLM द्वारा लौटाए गए टूल कॉल जानकारी को निकालने के लिए, हम एक और हेल्पर फ़ंक्शन जोड़ेंगे जो कॉल करने के लिए आवश्यक सभी चीजें निकालता है। अपने `main.rs` फाइल के अंत में निम्नलिखित कोड जोड़ें:

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

सभी टुकड़ों को जोड़ने के बाद, अब हम प्रारंभिक उपयोगकर्ता प्रॉम्प्ट को संभाल सकते हैं और LLM को कॉल कर सकते हैं। अपने `main` फ़ंक्शन को निम्नलिखित कोड के साथ अपडेट करें:

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

यह प्रारंभिक उपयोगकर्ता प्रॉम्प्ट के साथ LLM को क्वेरी करेगा, जिसमें दो संख्याओं का योग पूछना शामिल है, और प्रतिक्रिया को प्रोसेस करेगा ताकि टूल कॉल को डायनामिक रूप से संभाला जा सके।

बहुत बढ़िया, आपने इसे कर लिया!

## असाइनमेंट

अभ्यास से कोड लें और सर्वर में कुछ और टूल जोड़ें। फिर एक क्लाइंट बनाएं जिसमें LLM हो, जैसे कि अभ्यास में, और इसे विभिन्न प्रॉम्प्ट्स के साथ टेस्ट करें ताकि यह सुनिश्चित हो सके कि आपके सर्वर टूल्स को डायनामिक रूप से कॉल किया जा रहा है। इस प्रकार का क्लाइंट बनाना अंतिम उपयोगकर्ता को एक शानदार अनुभव प्रदान करता है क्योंकि वे प्रॉम्प्ट्स का उपयोग कर सकते हैं, बजाय सटीक क्लाइंट कमांड्स के, और MCP सर्वर के कॉल होने से अनजान रह सकते हैं।

## समाधान

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## मुख्य बातें

- अपने क्लाइंट में LLM जोड़ने से उपयोगकर्ताओं को MCP सर्वर्स के साथ इंटरैक्ट करने का बेहतर तरीका मिलता है।
- आपको MCP सर्वर प्रतिक्रिया को कुछ ऐसा बदलना होगा जिसे LLM समझ सके।

## नमूने

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## अतिरिक्त संसाधन

## आगे क्या

- अगला: [Visual Studio Code का उपयोग करके सर्वर को कंज्यूम करना](../04-vscode/README.md)

---

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को आधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।