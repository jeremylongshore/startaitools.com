<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "94c80ae71fb9971e9b57b51ab0912121",
  "translation_date": "2025-08-18T15:48:23+00:00",
  "source_file": "03-GettingStarted/02-client/README.md",
  "language_code": "mr"
}
-->
# क्लायंट तयार करणे

क्लायंट म्हणजे सानुकूल अनुप्रयोग किंवा स्क्रिप्ट्स, जे MCP सर्व्हरशी थेट संवाद साधून संसाधने, साधने आणि प्रॉम्प्ट्सची विनंती करतात. MCP सर्व्हरशी संवाद साधण्यासाठी ग्राफिकल इंटरफेस पुरवणाऱ्या इन्स्पेक्टर टूलच्या वापरापेक्षा, स्वतःचा क्लायंट लिहिणे प्रोग्रामॅटिक आणि स्वयंचलित संवाद सक्षम करते. यामुळे विकसकांना MCP क्षमतांचा त्यांच्या कार्यप्रवाहात समावेश करण्याची, कार्ये स्वयंचलित करण्याची आणि विशिष्ट गरजांसाठी सानुकूल उपाय तयार करण्याची परवानगी मिळते.

## आढावा

या धड्यात, मॉडेल कॉन्टेक्स्ट प्रोटोकॉल (MCP) इकोसिस्टममधील क्लायंट्सची संकल्पना सादर केली आहे. तुम्ही स्वतःचा क्लायंट कसा लिहायचा आणि MCP सर्व्हरशी कसा कनेक्ट करायचा हे शिकाल.

## शिकण्याची उद्दिष्टे

या धड्याच्या शेवटी, तुम्ही हे करू शकाल:

- क्लायंट काय करू शकतो हे समजून घ्या.
- स्वतःचा क्लायंट लिहा.
- MCP सर्व्हरशी कनेक्ट करा आणि क्लायंटची चाचणी करा, जेणेकरून सर्व्हर अपेक्षेप्रमाणे कार्य करत आहे याची खात्री होईल.

## क्लायंट लिहिण्यासाठी काय आवश्यक आहे?

क्लायंट लिहिण्यासाठी, तुम्हाला खालील गोष्टी कराव्या लागतील:

- **योग्य लायब्ररी आयात करा**. तुम्ही यापूर्वी वापरलेल्या लायब्ररीचा वापर कराल, फक्त वेगळ्या संरचना वापरून.
- **क्लायंट तयार करा**. यामध्ये क्लायंटचे उदाहरण तयार करणे आणि निवडलेल्या ट्रान्सपोर्ट पद्धतीशी कनेक्ट करणे समाविष्ट आहे.
- **कोणती संसाधने सूचीबद्ध करायची ते ठरवा**. तुमच्या MCP सर्व्हरमध्ये संसाधने, साधने आणि प्रॉम्प्ट्स असतात, तुम्हाला कोणती सूचीबद्ध करायची आहेत ते ठरवावे लागेल.
- **क्लायंटला होस्ट अनुप्रयोगाशी एकत्रित करा**. एकदा तुम्हाला सर्व्हरच्या क्षमतांची माहिती झाल्यावर, तुम्हाला हा क्लायंट तुमच्या होस्ट अनुप्रयोगाशी एकत्रित करावा लागेल, जेणेकरून वापरकर्ता प्रॉम्प्ट किंवा इतर कमांड टाइप केल्यावर संबंधित सर्व्हर वैशिष्ट्य सक्रिय होईल.

आता आपण उच्च-स्तरीय समजून घेतले आहे की आपण काय करणार आहोत, पुढील उदाहरण पाहूया.

### एक उदाहरण क्लायंट

चला या उदाहरण क्लायंटकडे पाहूया:

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

वरील कोडमध्ये आपण:

- लायब्ररी आयात केल्या.
- क्लायंटचे उदाहरण तयार केले आणि stdio वापरून कनेक्ट केले.
- प्रॉम्प्ट्स, संसाधने आणि साधने सूचीबद्ध केली आणि त्यांना सक्रिय केले.

आता तुमच्याकडे MCP सर्व्हरशी संवाद साधणारा क्लायंट आहे.

चला पुढील व्यायाम विभागात प्रत्येक कोड स्निपेटचे विश्लेषण करूया आणि काय चालले आहे ते समजून घेऊया.

## व्यायाम: क्लायंट लिहिणे

वर सांगितल्याप्रमाणे, कोड समजावून सांगण्यासाठी वेळ काढूया, आणि तुम्हाला हवे असल्यास कोडसह सराव करा.

### -1- लायब्ररी आयात करा

आपल्याला आवश्यक लायब्ररी आयात करूया. आपल्याला क्लायंट आणि निवडलेल्या ट्रान्सपोर्ट प्रोटोकॉल (stdio) संदर्भांची आवश्यकता असेल. stdio हा प्रोटोकॉल स्थानिक मशीनवर चालवण्यासाठी आहे. SSE हा आणखी एक ट्रान्सपोर्ट प्रोटोकॉल आहे, जो आपण पुढील अध्यायांमध्ये पाहू, परंतु सध्या आपण stdio वापरणे सुरू ठेवू.

#### टाइपस्क्रिप्ट

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
```

#### पायथन

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

#### जावा

जावासाठी, तुम्ही मागील व्यायामातील MCP सर्व्हरशी कनेक्ट होणारा क्लायंट तयार कराल. [Getting Started with MCP Server](../../../../03-GettingStarted/01-first-server/solution/java) मधील जावा स्प्रिंग बूट प्रोजेक्ट स्ट्रक्चर वापरून, `src/main/java/com/microsoft/mcp/sample/client/` फोल्डरमध्ये `SDKClient` नावाचा नवीन जावा क्लास तयार करा आणि खालील आयात जोडा:

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

तुमच्या `Cargo.toml` फाइलमध्ये खालील अवलंबित्वे जोडा.

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

त्यानंतर, तुम्ही तुमच्या क्लायंट कोडमध्ये आवश्यक लायब्ररी आयात करू शकता.

```rust
use rmcp::{
    RmcpError,
    model::CallToolRequestParam,
    service::ServiceExt,
    transport::{ConfigureCommandExt, TokioChildProcess},
};
use tokio::process::Command;
```

चला आता क्लायंट तयार करण्याकडे वळूया.

### -2- क्लायंट आणि ट्रान्सपोर्ट तयार करणे

आपल्याला ट्रान्सपोर्टचे उदाहरण आणि क्लायंटचे उदाहरण तयार करणे आवश्यक आहे:

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

वरील कोडमध्ये आपण:

- stdio ट्रान्सपोर्टचे उदाहरण तयार केले. लक्षात घ्या की ते सर्व्हर कसे शोधायचे आणि सुरू करायचे यासाठी कमांड आणि args निर्दिष्ट करते, कारण क्लायंट तयार करताना आपल्याला ते करावे लागेल.

    ```typescript
    const transport = new StdioClientTransport({
        command: "node",
        args: ["server.js"]
    });
    ```

- क्लायंटचे नाव आणि आवृत्ती देऊन त्याचे उदाहरण तयार केले.

    ```typescript
    const client = new Client(
    {
        name: "example-client",
        version: "1.0.0"
    });
    ```

- निवडलेल्या ट्रान्सपोर्टशी क्लायंट कनेक्ट केला.

    ```typescript
    await client.connect(transport);
    ```

#### पायथन

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

वरील कोडमध्ये आपण:

- आवश्यक लायब्ररी आयात केल्या.
- सर्व्हर पॅरामीटर्स ऑब्जेक्ट तयार केला, कारण आपण याचा वापर सर्व्हर चालवण्यासाठी करू, जेणेकरून आपण त्याच्याशी क्लायंटद्वारे कनेक्ट होऊ शकू.
- `run` नावाची पद्धत परिभाषित केली, जी `stdio_client` कॉल करते, जे क्लायंट सत्र सुरू करते.
- प्रवेश बिंदू तयार केला, जिथे आम्ही `run` पद्धत `asyncio.run` ला प्रदान करतो.

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

वरील कोडमध्ये आपण:

- आवश्यक लायब्ररी आयात केल्या.
- stdio ट्रान्सपोर्ट तयार केला आणि `mcpClient` नावाचा क्लायंट तयार केला. MCP सर्व्हरवरील वैशिष्ट्ये सूचीबद्ध आणि सक्रिय करण्यासाठी आपण याचा वापर करू.

टीप: "Arguments" मध्ये, तुम्ही *.csproj* किंवा executable कडे निर्देश करू शकता.

#### जावा

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

वरील कोडमध्ये आपण:

- मुख्य पद्धत तयार केली, जी `http://localhost:8080` वर चालणाऱ्या MCP सर्व्हरकडे SSE ट्रान्सपोर्ट पॉइंट करते.
- ट्रान्सपोर्टला कन्स्ट्रक्टर पॅरामीटर म्हणून घेणारा क्लायंट क्लास तयार केला.
- `run` पद्धतीमध्ये, ट्रान्सपोर्ट वापरून समक्रमित MCP क्लायंट तयार केला आणि कनेक्शन सुरू केले.
- SSE (Server-Sent Events) ट्रान्सपोर्ट वापरला, जो जावा स्प्रिंग बूट MCP सर्व्हरशी HTTP-आधारित संवादासाठी योग्य आहे.

#### रस्ट

हा रस्ट क्लायंट गृहीत धरतो की सर्व्हर त्याच डिरेक्टरीतील "calculator-server" नावाचा सिबलिंग प्रोजेक्ट आहे. खालील कोड सर्व्हर सुरू करेल आणि त्याच्याशी कनेक्ट होईल.

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

### -3- सर्व्हर वैशिष्ट्ये सूचीबद्ध करणे

आता, आमच्याकडे एक क्लायंट आहे, जो प्रोग्राम चालवला गेला तर कनेक्ट होऊ शकतो. तथापि, तो त्याची वैशिष्ट्ये सूचीबद्ध करत नाही, म्हणून पुढील गोष्ट करूया:

#### टाइपस्क्रिप्ट

```typescript
// List prompts
const prompts = await client.listPrompts();

// List resources
const resources = await client.listResources();

// list tools
const tools = await client.listTools();
```

#### पायथन

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

येथे आम्ही उपलब्ध संसाधने `list_resources()` आणि साधने `list_tools` सूचीबद्ध करतो आणि त्यांना प्रिंट करतो.

#### .NET

```dotnet
foreach (var tool in await client.ListToolsAsync())
{
    Console.WriteLine($"{tool.Name} ({tool.Description})");
}
```

वरील कोडमध्ये, आम्ही सर्व्हरवरील साधने कशी सूचीबद्ध करू शकतो याचे उदाहरण दिले आहे. प्रत्येक साधनासाठी, आम्ही त्याचे नाव प्रिंट करतो.

#### जावा

```java
// List and demonstrate tools
ListToolsResult toolsList = client.listTools();
System.out.println("Available Tools = " + toolsList);

// You can also ping the server to verify connection
client.ping();
```

वरील कोडमध्ये आपण:

- MCP सर्व्हरकडून उपलब्ध सर्व साधने मिळवण्यासाठी `listTools()` कॉल केला.
- सर्व्हरशी कनेक्शन कार्यरत आहे का हे तपासण्यासाठी `ping()` वापरले.
- `ListToolsResult` मध्ये सर्व साधनांची माहिती असते, ज्यात त्यांची नावे, वर्णने आणि इनपुट स्कीमा समाविष्ट असतात.

छान, आता आपण सर्व वैशिष्ट्ये कॅप्चर केली आहेत. आता प्रश्न असा आहे की आपण त्यांचा वापर कधी करतो? हा क्लायंट अगदी सोपा आहे, म्हणजे आपण वैशिष्ट्ये स्पष्टपणे कॉल केल्यावरच ती सक्रिय होतात. पुढील अध्यायात, आम्ही अधिक प्रगत क्लायंट तयार करू, ज्याला स्वतःचा मोठा भाषा मॉडेल (LLM) असेल. सध्या, आपण सर्व्हरवरील वैशिष्ट्ये कशी सक्रिय करू शकतो ते पाहूया:

#### रस्ट

मुख्य फंक्शनमध्ये, क्लायंट प्रारंभ केल्यानंतर, आपण सर्व्हर प्रारंभ करू शकतो आणि त्याची काही वैशिष्ट्ये सूचीबद्ध करू शकतो.

```rust
// Initialize
let server_info = client.peer_info();
println!("Server info: {:?}", server_info);

// List tools
let tools = client.list_tools(Default::default()).await?;
println!("Available tools: {:?}", tools);
```

### -4- वैशिष्ट्ये सक्रिय करणे

वैशिष्ट्ये सक्रिय करण्यासाठी, आपल्याला योग्य arguments आणि काही प्रकरणांमध्ये आपण सक्रिय करू इच्छित असलेल्या गोष्टीचे नाव निर्दिष्ट करणे आवश्यक आहे.

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

वरील कोडमध्ये आपण:

- संसाधन वाचले, आम्ही `readResource()` कॉल करून `uri` निर्दिष्ट करून संसाधनाला कॉल करतो. सर्व्हर साइडवरील कोड असे दिसेल:

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

    आमचा `uri` मूल्य `file://example.txt` सर्व्हरवरील `file://{name}` शी जुळतो. `example.txt` `name` शी मॅप होईल.

- साधनाला कॉल केले, आम्ही त्याला `name` आणि `arguments` निर्दिष्ट करून कॉल करतो:

    ```typescript
    const result = await client.callTool({
        name: "example-tool",
        arguments: {
            arg1: "value"
        }
    });
    ```

- प्रॉम्प्ट मिळवा, प्रॉम्प्ट मिळवण्यासाठी, तुम्ही `getPrompt()` ला `name` आणि `arguments` सह कॉल करता. सर्व्हर कोड असे दिसते:

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

    परिणामी तुमचा क्लायंट कोड सर्व्हरवर घोषित केलेल्या गोष्टींशी जुळण्यासाठी असा दिसतो:

    ```typescript
    const promptResult = await client.getPrompt({
        name: "review-code",
        arguments: {
            code: "console.log(\"Hello world\")"
        }
    })
    ```

#### पायथन

```python
# Read a resource
print("READING RESOURCE")
content, mime_type = await session.read_resource("greeting://hello")

# Call a tool
print("CALL TOOL")
result = await session.call_tool("add", arguments={"a": 1, "b": 7})
print(result.content)
```

वरील कोडमध्ये आपण:

- `read_resource` वापरून `greeting` नावाचे संसाधन कॉल केले.
- `call_tool` वापरून `add` नावाचे साधन सक्रिय केले.

#### .NET

1. साधनाला कॉल करण्यासाठी काही कोड जोडा:

  ```csharp
  var result = await mcpClient.CallToolAsync(
      "Add",
      new Dictionary<string, object?>() { ["a"] = 1, ["b"] = 3  },
      cancellationToken:CancellationToken.None);
  ```

1. परिणाम प्रिंट करण्यासाठी, परिणाम हाताळण्यासाठी खालील कोड जोडा:

  ```csharp
  Console.WriteLine(result.Content.First(c => c.Type == "text").Text);
  // Sum 4
  ```

#### जावा

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

वरील कोडमध्ये आपण:

- `callTool()` पद्धतीचा वापर करून `CallToolRequest` ऑब्जेक्ट्ससह अनेक कॅल्क्युलेटर साधने सक्रिय केली.
- प्रत्येक साधन कॉलमध्ये त्या साधनाचे नाव आणि आवश्यक arguments असलेला `Map` निर्दिष्ट केला.
- सर्व्हर साधनांना विशिष्ट पॅरामीटर नावे अपेक्षित असतात (उदा. गणितीय ऑपरेशन्ससाठी "a", "b").
- परिणाम `CallToolResult` ऑब्जेक्ट्स म्हणून परत केले जातात, ज्यामध्ये सर्व्हरकडून प्रतिसाद असतो.

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

### -5- क्लायंट चालवा

क्लायंट चालवण्यासाठी, टर्मिनलमध्ये खालील कमांड टाइप करा:

#### टाइपस्क्रिप्ट

तुमच्या *package.json* फाइलमधील "scripts" विभागात खालील एंट्री जोडा:

```json
"client": "tsc && node build/client.js"
```

```sh
npm run client
```

#### पायथन

खालील कमांडसह क्लायंट कॉल करा:

```sh
python client.py
```

#### .NET

```sh
dotnet run
```

#### जावा

प्रथम, तुमचा MCP सर्व्हर `http://localhost:8080` वर चालू असल्याची खात्री करा. नंतर क्लायंट चालवा:

```bash
# Build you project
./mvnw clean compile

# Run the client
./mvnw exec:java -Dexec.mainClass="com.microsoft.mcp.sample.client.SDKClient"
```

पर्यायी, तुम्ही `03-GettingStarted\02-client\solution\java` सोल्यूशन फोल्डरमधील पूर्ण क्लायंट प्रोजेक्ट चालवू शकता:

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

## असाइनमेंट

या असाइनमेंटमध्ये, तुम्ही क्लायंट तयार करण्यासाठी शिकलेल्या गोष्टींचा वापर करून स्वतःचा क्लायंट तयार कराल.

तुमच्या क्लायंट कोडद्वारे कॉल करण्यासाठी खालील सर्व्हर वापरा, आणि सर्व्हरमध्ये अधिक वैशिष्ट्ये जोडून तो अधिक मनोरंजक बनवण्याचा प्रयत्न करा.

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

### पायथन

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

या प्रोजेक्टमध्ये पहा की तुम्ही [प्रॉम्प्ट्स आणि संसाधने कशी जोडू शकता](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/EverythingServer/Program.cs).

तसेच, [प्रॉम्प्ट्स आणि संसाधने कसे सक्रिय करायचे](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol/Client/) यासाठी हा दुवा तपासा.

### रस्ट

[मागील विभागात](../../../../03-GettingStarted/01-first-server), तुम्ही रस्टसह एक साधा MCP सर्व्हर कसा तयार करायचा ते शिकलात. तुम्ही त्यावर काम सुरू ठेवू शकता किंवा MCP सर्व्हरच्या अधिक रस्ट-आधारित उदाहरणांसाठी हा दुवा तपासा: [MCP Server Examples](https://github.com/modelcontextprotocol/rust-sdk/tree/main/examples/servers)

## सोल्यूशन

**सोल्यूशन फोल्डर** मध्ये या ट्यूटोरियलमध्ये समाविष्ट केलेल्या सर्व संकल्पनांचे प्रदर्शन करणारे पूर्ण, तयार-टू-रन क्लायंट अंमलबजावणी समाविष्ट आहे. प्रत्येक सोल्यूशनमध्ये क्लायंट आणि सर्व्हर कोड स्वतंत्र, स्वयंपूर्ण प्रोजेक्ट्समध्ये आयोजित केलेले आहेत.

### 📁 सोल्यूशन स्ट्रक्चर

सोल्यूशन डिरेक्टरी प्रोग्रामिंग भाषेनुसार आयोजित केली आहे:

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

### 🚀 प्रत्येक सोल्यूशनमध्ये काय समाविष्ट आहे

प्रत्येक भाषा-विशिष्ट सोल्यूशनमध्ये खालील गोष्टी समाविष्ट आहेत:

- **पूर्ण क्लायंट अंमलबजावणी** ट्यूटोरियलमधील सर्व वैशिष्ट्यांसह
- **कार्यरत प्रोजेक्ट स्ट्रक्चर** योग्य dependencies आणि कॉन्फिगरेशनसह
- **बिल्ड आणि रन स्क्रिप्ट्स** सोप्या सेटअप आणि अंमलबजावणीसाठी
- **तपशीलवार README** भाषा-विशिष्ट सूचना असलेले
- **त्रुटी हाताळणी** आणि परिणाम प्रक्रिया उदाहरणे

### 📖 सोल्यूशन्सचा वापर

1. **तुमच्या पसंतीच्या भाषेच्या फोल्डरमध्ये जा**:

   ```bash
   cd solution/typescript/    # For TypeScript
   cd solution/java/          # For Java
   cd solution/python/        # For Python
   cd solution/dotnet/        # For .NET
   ```

2. **प्रत्येक फोल्डरमधील README सूचनांचे अनुसरण करा**:
   - Dependencies स्थापित करणे
   - प्रोजेक्ट तयार करणे
   - क्लायंट चालवणे

3. **तुम्हाला दिसणारे उदाहरण आउटपुट**:

   ```text
   Prompt: Please review this code: console.log("hello");
   Resource template: file
   Tool result: { content: [ { type: 'text', text: '9' } ] }
   ```

पूर्ण दस्तऐवज आणि चरण-दर-चरण सूचना यासाठी पहा: **[📖 सोल्यूशन दस्तऐवज](./solution/README.md)**

## 🎯 पूर्ण उदाहरणे

या ट्यूटोरियलमध्ये समाविष्ट केलेल्या सर्व प्रोग्रामिंग भाषांसाठी आम्ही पूर्ण, कार्यरत क्लायंट अंमलबजावणी प्रदान केली आहे. ही उदाहरणे वरील वर्णन केलेल्या संपूर्ण कार्यक्षमतेचे प्रदर्शन करतात आणि तुमच्या स्वतःच्या प्रकल्पांसाठी संदर्भ अंमलबजावणी किंवा प्रारंभिक बिंदू म्हणून वापरली जाऊ शकतात.

### उपलब्ध पूर्ण उदाहरणे

| भाषा | फाइल | वर्णन |
|----------|------|-------------|
| **जावा** | [`client_example_java.java`](../../../../03-GettingStarted/02-client/client_example_java.java) | SSE ट्रान्सपोर्ट वापरून त्रुटी हाताळणीसह पूर्ण जावा क्लायंट |
| **C#** | [`client_example_csharp.cs`](../../../../03-GettingStarted/02-client/client_example_csharp.cs) | stdio ट्रान्सपोर्ट वापरून MCP सर्व्हर स्वयंचलितपणे सुरू करणारा पूर्ण C# क्लायंट |
| **टाइपस्क्रिप्ट** | [`client_example_typescript.ts`](../../../../03-GettingStarted/02-client/client_example_typescript.ts) | MCP प्रोटोकॉलसाठी पूर्ण समर्थन असलेला टाइपस्क्रिप्ट
प्रत्येक संपूर्ण उदाहरणामध्ये समाविष्ट आहे:

- ✅ **कनेक्शन स्थापन करणे** आणि त्रुटी हाताळणी
- ✅ **सर्व्हर शोध** (साधने, संसाधने, प्रॉम्प्ट्स जिथे लागू आहे)
- ✅ **कॅल्क्युलेटर ऑपरेशन्स** (जोडणे, वजाबाकी, गुणाकार, भागाकार, मदत)
- ✅ **परिणाम प्रक्रिया** आणि स्वरूपित आउटपुट
- ✅ **संपूर्ण त्रुटी हाताळणी**
- ✅ **स्वच्छ, दस्तऐवजीकृत कोड** चरण-दर-चरण टिप्पण्या सह

### संपूर्ण उदाहरणांसह सुरुवात करणे

1. **तुमची पसंतीची भाषा निवडा** वर दिलेल्या तक्त्यातून
2. **संपूर्ण उदाहरण फाइल पुनरावलोकन करा** संपूर्ण अंमलबजावणी समजून घेण्यासाठी
3. **उदाहरण चालवा** [`complete_examples.md`](./complete_examples.md) मधील सूचनांचे अनुसरण करून
4. **तुमच्या विशिष्ट उपयोगासाठी उदाहरण बदलवा आणि विस्तारित करा**

या उदाहरणे चालवणे आणि सानुकूलित करण्याबद्दल तपशीलवार दस्तऐवजीकरणासाठी, पहा: **[📖 संपूर्ण उदाहरणे दस्तऐवजीकरण](./complete_examples.md)**

### 💡 उपाय विरुद्ध संपूर्ण उदाहरणे

| **उपाय फोल्डर** | **संपूर्ण उदाहरणे** |
|--------------------|--------------------- |
| बिल्ड फाइल्ससह संपूर्ण प्रकल्प संरचना | सिंगल-फाइल अंमलबजावणी |
| अवलंबनांसह तयार-चालवण्यास योग्य | केंद्रित कोड उदाहरणे |
| उत्पादनासारखी सेटअप | शैक्षणिक संदर्भ |
| भाषा-विशिष्ट साधने | क्रॉस-भाषा तुलना |

दोन्ही दृष्टिकोन उपयुक्त आहेत - **उपाय फोल्डर** संपूर्ण प्रकल्पांसाठी वापरा आणि **संपूर्ण उदाहरणे** शिकण्यासाठी आणि संदर्भासाठी वापरा.

## मुख्य मुद्दे

या अध्यायासाठी मुख्य मुद्दे खालीलप्रमाणे आहेत:

- क्लायंट्स सर्व्हरवरील वैशिष्ट्ये शोधण्यासाठी आणि वापरण्यासाठी वापरले जाऊ शकतात.
- स्वतः सुरू होत असताना सर्व्हर सुरू करू शकतो (जसे या अध्यायात आहे) परंतु क्लायंट्स चालू असलेल्या सर्व्हरशी देखील कनेक्ट होऊ शकतात.
- सर्व्हर क्षमतांची चाचणी घेण्यासाठी एक उत्कृष्ट मार्ग आहे, पर्यायांप्रमाणे जसे की मागील अध्यायात वर्णन केलेला इंस्पेक्टर.

## अतिरिक्त संसाधने

- [MCP मध्ये क्लायंट्स तयार करणे](https://modelcontextprotocol.io/quickstart/client)

## नमुने

- [Java कॅल्क्युलेटर](../samples/java/calculator/README.md)
- [.Net कॅल्क्युलेटर](../../../../03-GettingStarted/samples/csharp)
- [JavaScript कॅल्क्युलेटर](../samples/javascript/README.md)
- [TypeScript कॅल्क्युलेटर](../samples/typescript/README.md)
- [Python कॅल्क्युलेटर](../../../../03-GettingStarted/samples/python)
- [Rust कॅल्क्युलेटर](../../../../03-GettingStarted/samples/rust)

## पुढे काय?

- पुढील: [LLM सह क्लायंट तयार करणे](../03-llm-client/README.md)

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी कृपया लक्षात ठेवा की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेचा अभाव असू शकतो. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून उद्भवलेल्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.