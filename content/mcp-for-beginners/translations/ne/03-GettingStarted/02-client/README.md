<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "94c80ae71fb9971e9b57b51ab0912121",
  "translation_date": "2025-08-18T16:17:50+00:00",
  "source_file": "03-GettingStarted/02-client/README.md",
  "language_code": "ne"
}
-->
# क्लाइन्ट बनाउने

क्लाइन्टहरू कस्टम एप्लिकेसन वा स्क्रिप्टहरू हुन् जसले MCP सर्भरसँग सिधै संवाद गरेर स्रोतहरू, उपकरणहरू, र प्रम्प्टहरू अनुरोध गर्छन्। इन्स्पेक्टर टुल प्रयोग गरेर सर्भरसँग अन्तरक्रिया गर्न ग्राफिकल इन्टरफेस प्रदान गर्ने तरिकाभन्दा फरक, आफ्नै क्लाइन्ट लेख्दा प्रोग्रामेटिक र स्वचालित अन्तरक्रियाहरू सम्भव हुन्छ। यसले विकासकर्ताहरूलाई MCP क्षमताहरू आफ्नै कार्यप्रवाहमा एकीकृत गर्न, कार्यहरू स्वचालित गर्न, र विशेष आवश्यकताहरूका लागि कस्टम समाधानहरू निर्माण गर्न सक्षम बनाउँछ।

## परिचय

यो पाठले मोडल कन्टेक्स्ट प्रोटोकल (MCP) इकोसिस्टमभित्र क्लाइन्टहरूको अवधारणालाई परिचय गराउँछ। तपाईंले आफ्नै क्लाइन्ट कसरी लेख्ने र यसलाई MCP सर्भरसँग कसरी जडान गर्ने भन्ने कुरा सिक्नुहुनेछ।

## सिकाइका उद्देश्यहरू

यो पाठको अन्त्यसम्ममा, तपाईंले निम्न गर्न सक्षम हुनुहुनेछ:

- क्लाइन्टले के गर्न सक्छ भन्ने बुझ्ने।
- आफ्नै क्लाइन्ट लेख्ने।
- MCP सर्भरसँग क्लाइन्ट जडान गर्ने र यो अपेक्षाअनुसार काम गर्छ कि गर्दैन भनेर परीक्षण गर्ने।

## क्लाइन्ट लेख्न के आवश्यक छ?

क्लाइन्ट लेख्नका लागि तपाईंले निम्न कार्यहरू गर्नुपर्नेछ:

- **सही लाइब्रेरीहरू आयात गर्नुहोस्।** तपाईंले पहिले प्रयोग गरिएको लाइब्रेरी नै प्रयोग गर्नुहुनेछ, तर फरक संरचनाहरू।
- **क्लाइन्टको उदाहरण बनाउनुहोस्।** यसमा क्लाइन्टको उदाहरण सिर्जना गर्ने र यसलाई रोजिएको ट्रान्सपोर्ट विधिसँग जडान गर्ने समावेश छ।
- **सूचीबद्ध गर्न स्रोतहरू चयन गर्नुहोस्।** तपाईंको MCP सर्भरमा स्रोतहरू, उपकरणहरू, र प्रम्प्टहरू छन्, तपाईंले कुन सूचीबद्ध गर्ने निर्णय गर्नुपर्नेछ।
- **क्लाइन्टलाई होस्ट एप्लिकेसनमा एकीकृत गर्नुहोस्।** सर्भरको क्षमताहरू थाहा पाएपछि, तपाईंले यसलाई आफ्नो होस्ट एप्लिकेसनमा एकीकृत गर्नुपर्नेछ ताकि प्रयोगकर्ताले कुनै प्रम्प्ट वा अन्य आदेश टाइप गर्दा, सम्बन्धित सर्भर सुविधा सक्रिय होस्।

अब हामीले उच्च स्तरमा के गर्न गइरहेका छौं भन्ने कुरा बुझिसकेपछि, अब उदाहरण हेर्ने समय आएको छ।

### एउटा उदाहरण क्लाइन्ट

अब हामी एउटा उदाहरण क्लाइन्ट हेरौं:

### टाइपस्क्रिप्ट

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"]
});

const client = new Client(
  {
    name: "example-client",
    version: "1.0.0"
  }
);

await client.connect(transport);

// List prompts
const prompts = await client.listPrompts();

// Get a prompt
const prompt = await client.getPrompt({
  name: "example-prompt",
  arguments: {
    arg1: "value"
  }
});

// List resources
const resources = await client.listResources();

// Read a resource
const resource = await client.readResource({
  uri: "file:///example.txt"
});

// Call a tool
const result = await client.callTool({
  name: "example-tool",
  arguments: {
    arg1: "value"
  }
});
```

उपरोक्त कोडमा हामीले:

- लाइब्रेरीहरू आयात गरेका छौं।
- क्लाइन्टको उदाहरण सिर्जना गरेका छौं र stdio प्रयोग गरेर ट्रान्सपोर्टसँग जडान गरेका छौं।
- प्रम्प्टहरू, स्रोतहरू, र उपकरणहरूको सूचीबद्धता गरेका छौं र तिनीहरूलाई सक्रिय गरेका छौं।

यही हो, एउटा क्लाइन्ट जसले MCP सर्भरसँग संवाद गर्न सक्छ।

अब, अर्को अभ्यास खण्डमा, हामी प्रत्येक कोड स्निपेटलाई विस्तारमा व्याख्या गर्नेछौं।

## अभ्यास: क्लाइन्ट लेख्ने

जसरी माथि भनिएको छ, हामी कोड विस्तारमा व्याख्या गर्नेछौं, र तपाईं चाहनुहुन्छ भने कोडसँगै अभ्यास गर्न सक्नुहुन्छ।

### -1- लाइब्रेरीहरू आयात गर्नुहोस्

हामीलाई आवश्यक लाइब्रेरीहरू आयात गरौं। हामीलाई क्लाइन्ट र रोजिएको ट्रान्सपोर्ट प्रोटोकल stdio को सन्दर्भ चाहिन्छ। stdio स्थानीय मेसिनमा चल्ने चीजहरूको लागि प्रोटोकल हो। SSE अर्को ट्रान्सपोर्ट प्रोटोकल हो जुन हामीले भविष्यका अध्यायहरूमा देखाउनेछौं, तर यो तपाईंको अर्को विकल्प हो। अहिलेका लागि, stdio सँग अगाडि बढौं।

#### टाइपस्क्रिप्ट

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
```

#### पाइथन

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
```

#### .NET

```csharp
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;
```

#### जाभा

जाभाका लागि, तपाईंले अघिल्लो अभ्यासबाट MCP सर्भरसँग जडान गर्ने क्लाइन्ट सिर्जना गर्नुहुनेछ। [MCP सर्भरसँग सुरु गर्दै](../../../../03-GettingStarted/01-first-server/solution/java) बाट जाभा स्प्रिङ बुट प्रोजेक्ट संरचना प्रयोग गर्दै, `SDKClient` नामक नयाँ जाभा क्लास `src/main/java/com/microsoft/mcp/sample/client/` फोल्डरमा सिर्जना गर्नुहोस् र निम्न आयातहरू थप्नुहोस्:

```java
import java.util.Map;
import org.springframework.web.reactive.function.client.WebClient;
import io.modelcontextprotocol.client.McpClient;
import io.modelcontextprotocol.client.transport.WebFluxSseClientTransport;
import io.modelcontextprotocol.spec.McpClientTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;
import io.modelcontextprotocol.spec.McpSchema.CallToolResult;
import io.modelcontextprotocol.spec.McpSchema.ListToolsResult;
```

#### रस्ट

तपाईंले आफ्नो `Cargo.toml` फाइलमा निम्न निर्भरताहरू थप्नुपर्नेछ।

```toml
[package]
name = "calculator-client"
version = "0.1.0"
edition = "2024"

[dependencies]
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

त्यसपछि, तपाईं आफ्नो क्लाइन्ट कोडमा आवश्यक लाइब्रेरीहरू आयात गर्न सक्नुहुन्छ।

```rust
use rmcp::{
    RmcpError,
    model::CallToolRequestParam,
    service::ServiceExt,
    transport::{ConfigureCommandExt, TokioChildProcess},
};
use tokio::process::Command;
```

अब, उदाहरण बनाउनेतर्फ अगाडि बढौं।

### -2- क्लाइन्ट र ट्रान्सपोर्टको उदाहरण बनाउनुहोस्

हामीलाई ट्रान्सपोर्टको उदाहरण र हाम्रो क्लाइन्टको उदाहरण सिर्जना गर्नुपर्नेछ:

#### टाइपस्क्रिप्ट

```typescript
const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"]
});

const client = new Client(
  {
    name: "example-client",
    version: "1.0.0"
  }
);

await client.connect(transport);
```

उपरोक्त कोडमा हामीले:

- stdio ट्रान्सपोर्टको उदाहरण सिर्जना गरेका छौं। नोट गर्नुहोस् कि यसले सर्भर कसरी फेला पार्ने र सुरु गर्ने भनेर निर्दिष्ट गर्न आदेश र तर्कहरू निर्दिष्ट गर्दछ, किनभने यो हामीले क्लाइन्ट सिर्जना गर्दा गर्नुपर्ने कुरा हो।

    ```typescript
    const transport = new StdioClientTransport({
        command: "node",
        args: ["server.js"]
    });
    ```

- क्लाइन्टलाई नाम र संस्करण दिएर यसको उदाहरण बनाएका छौं।

    ```typescript
    const client = new Client(
    {
        name: "example-client",
        version: "1.0.0"
    });
    ```

- क्लाइन्टलाई रोजिएको ट्रान्सपोर्टसँग जडान गरेका छौं।

    ```typescript
    await client.connect(transport);
    ```

#### पाइथन

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

उपरोक्त कोडमा हामीले:

- आवश्यक लाइब्रेरीहरू आयात गरेका छौं।
- सर्भर प्यारामिटरहरूको वस्तु उदाहरण बनाएका छौं, जसलाई हामी सर्भर चलाउन प्रयोग गर्नेछौं ताकि हामी यससँग हाम्रो क्लाइन्ट जडान गर्न सकौं।
- `run` नामक विधि परिभाषित गरेका छौं, जसले `stdio_client` कल गर्छ र क्लाइन्ट सत्र सुरु गर्छ।
- प्रवेश बिन्दु सिर्जना गरेका छौं, जहाँ हामी `run` विधिलाई `asyncio.run` मा प्रदान गर्छौं।

#### .NET

```dotnet
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;

var builder = Host.CreateApplicationBuilder(args);

builder.Configuration
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>();



var clientTransport = new StdioClientTransport(new()
{
    Name = "Demo Server",
    Command = "dotnet",
    Arguments = ["run", "--project", "path/to/file.csproj"],
});

await using var mcpClient = await McpClientFactory.CreateAsync(clientTransport);
```

उपरोक्त कोडमा हामीले:

- आवश्यक लाइब्रेरीहरू आयात गरेका छौं।
- stdio ट्रान्सपोर्ट सिर्जना गरेका छौं र `mcpClient` नामक क्लाइन्ट सिर्जना गरेका छौं। यो क्लाइन्टलाई हामी MCP सर्भरमा सुविधाहरू सूचीबद्ध गर्न र सक्रिय गर्न प्रयोग गर्नेछौं।

नोट गर्नुहोस्, "Arguments" मा, तपाईं *.csproj* वा कार्यान्वयन योग्य फाइल दुवैलाई संकेत गर्न सक्नुहुन्छ।

#### जाभा

```java
public class SDKClient {
    
    public static void main(String[] args) {
        var transport = new WebFluxSseClientTransport(WebClient.builder().baseUrl("http://localhost:8080"));
        new SDKClient(transport).run();
    }
    
    private final McpClientTransport transport;

    public SDKClient(McpClientTransport transport) {
        this.transport = transport;
    }

    public void run() {
        var client = McpClient.sync(this.transport).build();
        client.initialize();
        
        // Your client logic goes here
    }
}
```

उपरोक्त कोडमा हामीले:

- मुख्य विधि सिर्जना गरेका छौं, जसले `http://localhost:8080` मा चल्ने MCP सर्भरमा SSE ट्रान्सपोर्ट सेटअप गर्छ।
- ट्रान्सपोर्टलाई कन्स्ट्रक्टर प्यारामिटरको रूपमा लिने क्लाइन्ट क्लास सिर्जना गरेका छौं।
- `run` विधिमा, हामी ट्रान्सपोर्ट प्रयोग गरेर एक समकालिक MCP क्लाइन्ट सिर्जना गर्छौं र जडान सुरु गर्छौं।
- SSE (Server-Sent Events) ट्रान्सपोर्ट प्रयोग गरेका छौं, जुन जाभा स्प्रिङ बुट MCP सर्भरसँग HTTP-आधारित संवादका लागि उपयुक्त छ।

#### रस्ट

यो रस्ट क्लाइन्टले सर्भरलाई "calculator-server" नामक समान डाइरेक्टरीमा रहेको परियोजनाको रूपमा मान्छ। तलको कोडले सर्भर सुरु गर्छ र यससँग जडान गर्छ।

```rust
async fn main() -> Result<(), RmcpError> {
    // Assume the server is a sibling project named "calculator-server" in the same directory
    let server_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("failed to locate workspace root")
        .join("calculator-server");

    let client = ()
        .serve(
            TokioChildProcess::new(Command::new("cargo").configure(|cmd| {
                cmd.arg("run").current_dir(server_dir);
            }))
            .map_err(RmcpError::transport_creation::<TokioChildProcess>)?,
        )
        .await?;

    // TODO: Initialize

    // TODO: List tools

    // TODO: Call add tool with arguments = {"a": 3, "b": 2}

    client.cancel().await?;
    Ok(())
}
```

### -3- सर्भर सुविधाहरू सूचीबद्ध गर्नुहोस्

अब, हामीसँग एउटा क्लाइन्ट छ, जसले कार्यक्रम चलाउँदा जडान गर्न सक्छ। तर, यसले वास्तवमा यसको सुविधाहरू सूचीबद्ध गर्दैन, त्यसैले अब हामी यो गर्नेछौं:

#### टाइपस्क्रिप्ट

```typescript
// List prompts
const prompts = await client.listPrompts();

// List resources
const resources = await client.listResources();

// list tools
const tools = await client.listTools();
```

#### पाइथन

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
```

यहाँ हामीले उपलब्ध स्रोतहरू `list_resources()` र उपकरणहरू `list_tools` सूचीबद्ध गरेका छौं र तिनीहरूलाई प्रिन्ट गरेका छौं।

#### .NET

```dotnet
foreach (var tool in await client.ListToolsAsync())
{
    Console.WriteLine($"{tool.Name} ({tool.Description})");
}
```

माथिको कोडमा हामीले सर्भरमा रहेका उपकरणहरूको सूचीबद्धता गरेका छौं। प्रत्येक उपकरणका लागि, हामीले यसको नाम प्रिन्ट गरेका छौं।

#### जाभा

```java
// List and demonstrate tools
ListToolsResult toolsList = client.listTools();
System.out.println("Available Tools = " + toolsList);

// You can also ping the server to verify connection
client.ping();
```

उपरोक्त कोडमा हामीले:

- MCP सर्भरबाट उपलब्ध सबै उपकरणहरू `listTools()` कल गरेर प्राप्त गरेका छौं।
- सर्भरसँगको जडान काम गरिरहेको छ कि छैन भनेर जाँच गर्न `ping()` प्रयोग गरेका छौं।
- `ListToolsResult` ले सबै उपकरणहरूको जानकारी समावेश गर्दछ, जस्तै तिनीहरूको नाम, विवरण, र इनपुट स्किमाहरू।

ठीक छ, अब हामीले सबै सुविधाहरू समेटेका छौं। अब प्रश्न यो हो कि हामी तिनीहरूलाई कहिले प्रयोग गर्नेछौं? यो क्लाइन्ट धेरै साधारण छ, साधारण यस अर्थमा कि हामीले सुविधाहरू स्पष्ट रूपमा कल गर्नुपर्नेछ। अर्को अध्यायमा, हामी एउटा उन्नत क्लाइन्ट सिर्जना गर्नेछौं, जसले आफ्नै ठूलो भाषा मोडेल (LLM) पहुँच गर्नेछ। अहिलेका लागि, हामी सर्भरमा सुविधाहरू कसरी सक्रिय गर्ने देखौं:

#### रस्ट

मुख्य कार्यमा, क्लाइन्ट सुरु गरेपछि, हामी सर्भर सुरु गर्न सक्छौं र यसको केही सुविधाहरू सूचीबद्ध गर्न सक्छौं।

```rust
// Initialize
let server_info = client.peer_info();
println!("Server info: {:?}", server_info);

// List tools
let tools = client.list_tools(Default::default()).await?;
println!("Available tools: {:?}", tools);
```

### -4- सुविधाहरू सक्रिय गर्नुहोस्

फिचरहरू सक्रिय गर्न, हामीले सही तर्कहरू निर्दिष्ट गर्न र केही अवस्थामा हामीले सक्रिय गर्न खोजिरहेको नाम निर्दिष्ट गर्नुपर्नेछ।

#### टाइपस्क्रिप्ट

```typescript

// Read a resource
const resource = await client.readResource({
  uri: "file:///example.txt"
});

// Call a tool
const result = await client.callTool({
  name: "example-tool",
  arguments: {
    arg1: "value"
  }
});

// call prompt
const promptResult = await client.getPrompt({
    name: "review-code",
    arguments: {
        code: "console.log(\"Hello world\")"
    }
})
```

उपरोक्त कोडमा हामीले:

- स्रोत पढेका छौं, हामीले `readResource()` कल गरेर `uri` निर्दिष्ट गरेका छौं। यो सर्भर पक्षमा निम्न जस्तो देखिन्छ:

    ```typescript
    server.resource(
        "readFile",
        new ResourceTemplate("file://{name}", { list: undefined }),
        async (uri, { name }) => ({
          contents: [{
            uri: uri.href,
            text: `Hello, ${name}!`
          }]
        })
    );
    ```

    हाम्रो `uri` मान `file://example.txt` ले सर्भरमा `file://{name}` सँग मेल खान्छ। `example.txt` लाई `name` मा म्याप गरिनेछ।

- उपकरण कल गरेका छौं, हामीले यसको `name` र `arguments` निर्दिष्ट गरेर यसलाई कल गरेका छौं:

    ```typescript
    const result = await client.callTool({
        name: "example-tool",
        arguments: {
            arg1: "value"
        }
    });
    ```

- प्रम्प्ट प्राप्त गरेका छौं, प्रम्प्ट प्राप्त गर्न, तपाईंले `getPrompt()` लाई `name` र `arguments` सँग कल गर्नुहुन्छ। सर्भर कोड यसरी देखिन्छ:

    ```typescript
    server.prompt(
        "review-code",
        { code: z.string() },
        ({ code }) => ({
            messages: [{
            role: "user",
            content: {
                type: "text",
                text: `Please review this code:\n\n${code}`
            }
            }]
        })
    );
    ```

    र तपाईंको परिणामस्वरूप क्लाइन्ट कोड यसरी देखिन्छ, जसले सर्भरमा घोषणा गरिएकोसँग मेल खान्छ:

    ```typescript
    const promptResult = await client.getPrompt({
        name: "review-code",
        arguments: {
            code: "console.log(\"Hello world\")"
        }
    })
    ```

#### पाइथन

```python
# Read a resource
print("READING RESOURCE")
content, mime_type = await session.read_resource("greeting://hello")

# Call a tool
print("CALL TOOL")
result = await session.call_tool("add", arguments={"a": 1, "b": 7})
print(result.content)
```

उपरोक्त कोडमा, हामीले:

- `read_resource` प्रयोग गरेर `greeting` नामक स्रोत कल गरेका छौं।
- `call_tool` प्रयोग गरेर `add` नामक उपकरण सक्रिय गरेका छौं।

#### .NET

1. उपकरण कल गर्न केही कोड थपौं:

  ```csharp
  var result = await mcpClient.CallToolAsync(
      "Add",
      new Dictionary<string, object?>() { ["a"] = 1, ["b"] = 3  },
      cancellationToken:CancellationToken.None);
  ```

1. परिणाम प्रिन्ट गर्न, यहाँ केही कोड छ:

  ```csharp
  Console.WriteLine(result.Content.First(c => c.Type == "text").Text);
  // Sum 4
  ```

#### जाभा

```java
// Call various calculator tools
CallToolResult resultAdd = client.callTool(new CallToolRequest("add", Map.of("a", 5.0, "b", 3.0)));
System.out.println("Add Result = " + resultAdd);

CallToolResult resultSubtract = client.callTool(new CallToolRequest("subtract", Map.of("a", 10.0, "b", 4.0)));
System.out.println("Subtract Result = " + resultSubtract);

CallToolResult resultMultiply = client.callTool(new CallToolRequest("multiply", Map.of("a", 6.0, "b", 7.0)));
System.out.println("Multiply Result = " + resultMultiply);

CallToolResult resultDivide = client.callTool(new CallToolRequest("divide", Map.of("a", 20.0, "b", 4.0)));
System.out.println("Divide Result = " + resultDivide);

CallToolResult resultHelp = client.callTool(new CallToolRequest("help", Map.of()));
System.out.println("Help = " + resultHelp);
```

उपरोक्त कोडमा हामीले:

- `callTool()` विधि प्रयोग गरेर `CallToolRequest` वस्तुहरूसँग धेरै क्याल्कुलेटर उपकरणहरू कल गरेका छौं।
- प्रत्येक उपकरण कलले उपकरणको नाम र सो उपकरणले आवश्यक पर्ने तर्कहरूको `Map` निर्दिष्ट गर्दछ।
- सर्भर उपकरणहरूले विशिष्ट प्यारामिटर नामहरू (जस्तै "a", "b" गणितीय कार्यहरूको लागि) अपेक्षा गर्छन्।
- परिणामहरू `CallToolResult` वस्तुहरूका रूपमा फर्काइन्छ, जसमा सर्भरबाट प्रतिक्रिया समावेश हुन्छ।

#### रस्ट

```rust
// Call add tool with arguments = {"a": 3, "b": 2}
let a = 3;
let b = 2;
let tool_result = client
    .call_tool(CallToolRequestParam {
        name: "add".into(),
        arguments: serde_json::json!({ "a": a, "b": b }).as_object().cloned(),
    })
    .await?;
println!("Result of {:?} + {:?}: {:?}", a, b, tool_result);
```

### -5- क्लाइन्ट चलाउनुहोस्

क्लाइन्ट चलाउन, टर्मिनलमा निम्न आदेश टाइप गर्नुहोस्:

#### टाइपस्क्रिप्ट

*package.json* मा "scripts" खण्डमा निम्न प्रविष्टि थप्नुहोस्:

```json
"client": "tsc && node build/client.js"
```

```sh
npm run client
```

#### पाइथन

क्लाइन्टलाई निम्न आदेशले कल गर्नुहोस्:

```sh
python client.py
```

#### .NET

```sh
dotnet run
```

#### जाभा

पहिले, सुनिश्चित गर्नुहोस् कि तपाईंको MCP सर्भर `http://localhost:8080` मा चलिरहेको छ। त्यसपछि क्लाइन्ट चलाउनुहोस्:

```bash
# Build you project
./mvnw clean compile

# Run the client
./mvnw exec:java -Dexec.mainClass="com.microsoft.mcp.sample.client.SDKClient"
```

वैकल्पिक रूपमा, तपाईं समाधान फोल्डर `03-GettingStarted\02-client\solution\java` मा प्रदान गरिएको पूर्ण क्लाइन्ट प्रोजेक्ट चलाउन सक्नुहुन्छ:

```bash
# Navigate to the solution directory
cd 03-GettingStarted/02-client/solution/java

# Build and run the JAR
./mvnw clean package
java -jar target/calculator-client-0.0.1-SNAPSHOT.jar
```

#### रस्ट

```bash
cargo fmt
cargo run
```

## असाइनमेन्ट

यस असाइनमेन्टमा, तपाईंले क्लाइन्ट सिर्जना गर्दा सिकेको कुरा प्रयोग गर्नुहुनेछ, तर आफ्नै क्लाइन्ट सिर्जना गर्नुहोस्।

यहाँ एउटा सर्भर छ, जसलाई तपाईंले आफ्नो क्लाइन्ट कोडमार्फत कल गर्नुपर्नेछ। हेर्नुहोस् कि तपाईं सर्भरमा थप सुविधाहरू थपेर यसलाई अझ रोचक बनाउन सक्नुहुन्छ कि।

### टाइपस्क्रिप्ट

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "Demo",
  version: "1.0.0"
});

// Add an addition tool
server.tool("add",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }]
  })
);

// Add a dynamic greeting resource
server.resource(
  "greeting",
  new ResourceTemplate("greeting://{name}", { list: undefined }),
  async (uri, { name }) => ({
    contents: [{
      uri: uri.href,
      text: `Hello, ${name}!`
    }]
  })
);

// Start receiving messages on stdin and sending messages on stdout

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCPServer started on stdin/stdout");
}

main().catch((error) => {
  console.error("Fatal error: ", error);
  process.exit(1);
});
```

### पाइथन

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

```

### .NET

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using ModelContextProtocol.Server;
using System.ComponentModel;

var builder = Host.CreateApplicationBuilder(args);
builder.Logging.AddConsole(consoleLogOptions =>
{
    // Configure all logs to go to stderr
    consoleLogOptions.LogToStandardErrorThreshold = LogLevel.Trace;
});

builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();
await builder.Build().RunAsync();

[McpServerToolType]
public static class CalculatorTool
{
    [McpServerTool, Description("Adds two numbers")]
    public static string Add(int a, int b) => $"Sum {a + b}";
}
```

यस परियोजनालाई हेर्नुहोस् कि कसरी [प्रम्प्ट र स्रोतहरू थप्ने](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/EverythingServer/Program.cs)।

साथै, [प्रम्प्ट र स्रोतहरू सक्रिय गर्ने](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol/Client/) बारे जानकारीका लागि यो लिङ्क जाँच गर्नुहोस्।

### रस्ट

[अघिल्लो खण्ड](../../../../03-GettingStarted/01-first-server) मा, तपाईंले रस्टको साथ एक साधारण MCP सर्भर कसरी सिर्जना गर्ने सिक्नुभयो। तपाईं यसलाई निर्माण गर्न जारी राख्न सक्नुहुन्छ वा रस्ट-आधारित MCP सर्भरका थप उदाहरणहरूको लागि यो लिङ्क जाँच गर्नुहोस्: [MCP Server Examples](https://github.com/modelcontextprotocol/rust-sdk/tree/main/examples/servers)

## समाधान

**समाधान फोल्डर** मा यस ट्युटोरियलमा समेटिएका सबै अवधारणाहरू प्रदर्शन गर्ने पूर्ण, तयार-चल्ने क्लाइन्ट कार्यान्वयनहरू समावेश छन्। प्रत्येक समाधानमा क्लाइन्ट र सर्भर कोड अलग, आत्म-निहित परियोजनाहरूमा व्यवस्थित छन्।

### 📁 समाधान संरचना

समाधान निर्देशिका प्रोग्रामिङ भाषाद्वारा व्यवस्थित छ:

```text
solution/
├── typescript/          # TypeScript client with npm/Node.js setup
│   ├── package.json     # Dependencies and scripts
│   ├── tsconfig.json    # TypeScript configuration
│   └── src/             # Source code
├── java/                # Java Spring Boot client project
│   ├── pom.xml          # Maven configuration
│   ├── src/             # Java source files
│   └── mvnw             # Maven wrapper
├── python/              # Python client implementation
│   ├── client.py        # Main client code
│   ├── server.py        # Compatible server
│   └── README.md        # Python-specific instructions
├── dotnet/              # .NET client project
│   ├── dotnet.csproj    # Project configuration
│   ├── Program.cs       # Main client code
│   └── dotnet.sln       # Solution file
├── rust/                # Rust client implementation
|  ├── Cargo.lock        # Cargo lock file
|  ├── Cargo.toml        # Project configuration and dependencies
|  ├── src               # Source code
|  │   └── main.rs       # Main client code
└── server/              # Additional .NET server implementation
    ├── Program.cs       # Server code
    └── server.csproj    # Server project file
```

### 🚀 प्रत्येक समाधानले के समावेश गर्दछ

प्रत्येक भाषा-विशिष्ट समाधानले प्रदान गर्दछ:

- **पूर्ण क्लाइन्ट कार्यान्वयन** ट्युटोरियलका सबै सुविधाहरूका साथ
- **कार्यरत परियोजना संरचना** उचित निर्भरताहरू र कन्फिगरेसनका साथ
- **निर्माण र चलाउने स्क्रिप्टहरू** सजिलो सेटअप र कार्यान्वयनका लागि
- **विस्तृत README** भाषा-विशिष्ट निर्देशनहरूसहित
- **त्रुटि ह्यान्डलिङ** र परिणाम प्रशोधनका उदाहरणहरू

### 📖 समाधानहरू प्रयोग गर्दै

1. **आफ्नो मनपर्ने भाषा फोल्डरमा जानुहोस्**:

   ```bash
   cd solution/typescript/    # For TypeScript
   cd solution/java/          # For Java
   cd solution/python/        # For Python
   cd solution/dotnet/        # For .NET
   ```

2. **प्रत्येक फोल्डरको README निर्देशनहरू पालना गर्नुहोस्**:
   - निर्भरताहरू स्थापना गर्दै
   - परियोजना निर्माण गर्दै
   - क्लाइन्ट चलाउँदै

3. **उदाहरण आउटपुट** जुन तपाईंले देख्नुहुनेछ:

   ```text
   Prompt: Please review this code: console.log("hello");
   Resource template: file
   Tool result: { content: [ { type: 'text', text: '9' } ] }
   ```

पूर्ण कागजात र चरण-दर-चरण निर्देशनहरूको लागि, हेर्नुहोस्: **[📖 समाधान कागजात](./solution/README.md)**

## 🎯 पूर्ण उदाहरणहरू

हामीले यस ट्युटोरियलमा समेटिएका सबै प्रोग्रामिङ भाषाहरूका लागि पूर्ण, कार्यरत क्लाइन्ट कार्यान्वयनहरू प्रदान गरेका छौं। यी उदाहरणहरूले माथि वर्णन गरिएको पूर्ण कार्यक्षमता प्रदर्शन गर्छन् र तपाईंका आफ्नै परियोजनाहरूका लागि सन्दर्भ कार्यान्वयन वा सुरुवात बिन्दुका रूपमा प्रयोग गर्न सकिन्छ।

### उपलब्ध पूर्ण उदाहरणहरू

| भाषा | फाइल | विवरण |
|----------|------|-------------|
| **जाभा** | [`client_example_java.java`](../../../../03-GettingStarted/02-client/client_example_java.java) | SSE ट्रान्सपोर्ट प्रयोग गर्ने पूर्ण जाभा क्लाइन्ट, व्यापक त्रुटि ह्यान्डलिङसहित |
| **C#** | [`client_example_csharp.cs`](../../../../03-GettingStarted/02-client/client_example_csharp.cs) | stdio ट्रान्सपोर्ट प्रयोग गर्ने पूर्ण C# क्लाइन्ट, स्वचालित सर्भर स्टार्टअपसहित |
| **टाइपस्क्रिप्ट** | [`client_example_typescript.ts`](../../../../03-GettingStarted/02-client/client_example_typescript.ts) | पूर्ण टाइपस्क्रिप्ट क्लाइन्ट, MCP प्रोटोकलको पूर्ण समर्थनसहित |
| **पाइथन** | [`client_example_python.py`](../../../../03-GettingStarted/02-client/client_example_python.py) | पूर्ण पाइथन क्लाइन्ट, async/await ढाँचाहरू प्रयोग गर्दै |
| **रस्ट** | [`client_example_rust.rs`](../../../../03-GettingStarted/02-client/client_example_rust.rs) | पूर्ण रस्ट क्लाइन्ट, असिन्क अपरेसनका लागि टोकियो प्रयोग गर्दै |
प्रत्येक पूर्ण उदाहरणमा समावेश छ:

- ✅ **जडान स्थापना** र त्रुटि व्यवस्थापन
- ✅ **सर्भर पत्ता लगाउने** (उपकरणहरू, स्रोतहरू, आवश्यक परामर्शहरू)
- ✅ **क्यालकुलेटर अपरेशनहरू** (जोड्ने, घटाउने, गुणा गर्ने, भाग गर्ने, मद्दत)
- ✅ **परिणाम प्रक्रिया** र स्वरूपित आउटपुट
- ✅ **व्यापक त्रुटि व्यवस्थापन**
- ✅ **सफा, दस्तावेजीकृत कोड** चरण-दर-चरण टिप्पणीहरूसँग

### पूर्ण उदाहरणहरू सुरु गर्ने तरिका

1. **आफ्नो मनपर्ने भाषा चयन गर्नुहोस्** माथिको तालिकाबाट
2. **पूर्ण उदाहरण फाइल समीक्षा गर्नुहोस्** सम्पूर्ण कार्यान्वयन बुझ्नका लागि
3. **उदाहरण चलाउनुहोस्** [`complete_examples.md`](./complete_examples.md) मा दिइएका निर्देशनहरू पालना गर्दै
4. **आफ्नो विशेष प्रयोगको लागि परिमार्जन र विस्तार गर्नुहोस्** 

यी उदाहरणहरू चलाउने र अनुकूलन गर्ने विस्तृत दस्तावेजको लागि हेर्नुहोस्: **[📖 पूर्ण उदाहरण दस्तावेज](./complete_examples.md)**

### 💡 समाधान बनाम पूर्ण उदाहरणहरू

| **समाधान फोल्डर** | **पूर्ण उदाहरणहरू** |
|--------------------|--------------------- |
| निर्माण फाइलहरूसहितको पूर्ण परियोजना संरचना | एकल-फाइल कार्यान्वयनहरू |
| निर्भरतासहित तयार-चलाउन सकिने | केन्द्रित कोड उदाहरणहरू |
| उत्पादन-जस्तै सेटअप | शैक्षिक सन्दर्भ |
| भाषा-विशिष्ट उपकरणहरू | क्रस-भाषा तुलना |

दुवै दृष्टिकोणहरू मूल्यवान छन् - **समाधान फोल्डर** पूर्ण परियोजनाहरूको लागि प्रयोग गर्नुहोस् र **पूर्ण उदाहरणहरू** सिकाइ र सन्दर्भको लागि।

## मुख्य कुरा

यस अध्यायको मुख्य कुरा क्लाइन्टहरूको बारेमा निम्न छन्:

- सर्भरमा सुविधाहरू पत्ता लगाउन र प्रयोग गर्न दुवैको लागि प्रयोग गर्न सकिन्छ।
- सर्भर सुरु गर्न सक्छ जब यो आफैं सुरु हुन्छ (जस्तै यस अध्यायमा) तर क्लाइन्टहरू चलिरहेको सर्भरहरूसँग पनि जडान गर्न सक्छन्।
- सर्भर क्षमताहरू परीक्षण गर्न उत्कृष्ट तरिका हो, वैकल्पिकहरू जस्तै इन्स्पेक्टरको साथ, जुन अघिल्लो अध्यायमा वर्णन गरिएको थियो।

## थप स्रोतहरू

- [MCP मा क्लाइन्ट निर्माण गर्ने](https://modelcontextprotocol.io/quickstart/client)

## नमूनाहरू

- [जाभा क्यालकुलेटर](../samples/java/calculator/README.md)
- [.Net क्यालकुलेटर](../../../../03-GettingStarted/samples/csharp)
- [जाभास्क्रिप्ट क्यालकुलेटर](../samples/javascript/README.md)
- [टाइपस्क्रिप्ट क्यालकुलेटर](../samples/typescript/README.md)
- [पाइथन क्यालकुलेटर](../../../../03-GettingStarted/samples/python)
- [रस्ट क्यालकुलेटर](../../../../03-GettingStarted/samples/rust)

## अब के गर्ने

- अगाडि: [LLM को साथ क्लाइन्ट सिर्जना गर्ने](../03-llm-client/README.md)

**अस्वीकरण**:  
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको छ। हामी यथार्थताको लागि प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादहरूमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छ। यसको मूल भाषा मा रहेको मूल दस्तावेज़लाई आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीको लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न हुने कुनै पनि गलतफहमी वा गलत व्याख्याको लागि हामी जिम्मेवार हुने छैनौं।