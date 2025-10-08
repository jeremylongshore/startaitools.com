<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "94c80ae71fb9971e9b57b51ab0912121",
  "translation_date": "2025-08-18T14:36:35+00:00",
  "source_file": "03-GettingStarted/02-client/README.md",
  "language_code": "th"
}
-->
# การสร้างไคลเอนต์

ไคลเอนต์คือแอปพลิเคชันหรือสคริปต์ที่ปรับแต่งเองเพื่อสื่อสารโดยตรงกับ MCP Server เพื่อร้องขอทรัพยากร เครื่องมือ และคำสั่งต่างๆ การเขียนไคลเอนต์ของคุณเองช่วยให้สามารถโต้ตอบกับเซิร์ฟเวอร์ได้แบบโปรแกรมและอัตโนมัติ ซึ่งช่วยให้นักพัฒนาสามารถผสานความสามารถของ MCP เข้ากับเวิร์กโฟลว์ของตนเอง อัตโนมัติการทำงาน และสร้างโซลูชันที่ปรับแต่งให้เหมาะกับความต้องการเฉพาะ

## ภาพรวม

บทเรียนนี้จะแนะนำแนวคิดของไคลเอนต์ในระบบนิเวศของ Model Context Protocol (MCP) คุณจะได้เรียนรู้วิธีเขียนไคลเอนต์ของคุณเองและเชื่อมต่อกับ MCP Server

## วัตถุประสงค์การเรียนรู้

เมื่อจบบทเรียนนี้ คุณจะสามารถ:

- เข้าใจว่าไคลเอนต์สามารถทำอะไรได้บ้าง
- เขียนไคลเอนต์ของคุณเอง
- เชื่อมต่อและทดสอบไคลเอนต์กับ MCP Server เพื่อให้แน่ใจว่าเซิร์ฟเวอร์ทำงานตามที่คาดไว้

## อะไรบ้างที่เกี่ยวข้องกับการเขียนไคลเอนต์?

ในการเขียนไคลเอนต์ คุณจะต้องทำสิ่งต่อไปนี้:

- **นำเข้าไลบรารีที่ถูกต้อง** คุณจะใช้ไลบรารีเดียวกับที่เคยใช้มาก่อน แต่จะใช้โครงสร้างที่แตกต่างกัน
- **สร้างไคลเอนต์** ซึ่งจะเกี่ยวข้องกับการสร้างอินสแตนซ์ของไคลเอนต์และเชื่อมต่อกับวิธีการขนส่งที่เลือก
- **ตัดสินใจว่าจะลิสต์ทรัพยากรอะไร** MCP Server ของคุณมาพร้อมกับทรัพยากร เครื่องมือ และคำสั่ง คุณต้องตัดสินใจว่าจะลิสต์สิ่งใด
- **ผสานไคลเอนต์เข้ากับแอปพลิเคชันโฮสต์** เมื่อคุณทราบความสามารถของเซิร์ฟเวอร์แล้ว คุณต้องผสานสิ่งนี้เข้ากับแอปพลิเคชันโฮสต์ของคุณ เพื่อให้เมื่อผู้ใช้พิมพ์คำสั่งหรือคำสั่งอื่นๆ ฟีเจอร์ที่เกี่ยวข้องของเซิร์ฟเวอร์จะถูกเรียกใช้งาน

เมื่อเราเข้าใจในระดับสูงว่าเรากำลังจะทำอะไร ต่อไปเรามาดูตัวอย่างกัน

### ตัวอย่างไคลเอนต์

มาดูตัวอย่างไคลเอนต์นี้กัน:

### TypeScript

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

ในโค้ดข้างต้นเรา:

- นำเข้าไลบรารี
- สร้างอินสแตนซ์ของไคลเอนต์และเชื่อมต่อโดยใช้ stdio เป็นวิธีการขนส่ง
- ลิสต์คำสั่ง ทรัพยากร และเครื่องมือ และเรียกใช้งานทั้งหมด

นี่คือไคลเอนต์ที่สามารถสื่อสารกับ MCP Server ได้

เรามาใช้เวลาในส่วนถัดไปของการฝึกฝนและแยกโค้ดแต่ละส่วนออกมาอธิบายว่าเกิดอะไรขึ้น

## การฝึกฝน: การเขียนไคลเอนต์

ดังที่กล่าวไว้ข้างต้น เรามาใช้เวลาอธิบายโค้ด และหากคุณต้องการ คุณสามารถเขียนโค้ดไปพร้อมกันได้

### -1- นำเข้าไลบรารี

เรามานำเข้าไลบรารีที่เราต้องการ เราจะต้องอ้างอิงถึงไคลเอนต์และโปรโตคอลการขนส่งที่เราเลือก stdio stdio เป็นโปรโตคอลสำหรับสิ่งที่ตั้งใจให้ทำงานบนเครื่องของคุณเอง SSE เป็นโปรโตคอลการขนส่งอีกตัวเลือกหนึ่งที่เราจะแสดงในบทถัดไป แต่สำหรับตอนนี้ เรามาดำเนินการต่อด้วย stdio

#### TypeScript

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
```

#### Python

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

#### Java

สำหรับ Java คุณจะสร้างไคลเอนต์ที่เชื่อมต่อกับ MCP Server จากการฝึกฝนครั้งก่อน โดยใช้โครงสร้างโปรเจกต์ Java Spring Boot เดียวกันจาก [เริ่มต้นใช้งาน MCP Server](../../../../03-GettingStarted/01-first-server/solution/java) สร้างคลาส Java ใหม่ชื่อ `SDKClient` ในโฟลเดอร์ `src/main/java/com/microsoft/mcp/sample/client/` และเพิ่มการนำเข้าต่อไปนี้:

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

#### Rust

คุณจะต้องเพิ่มการพึ่งพาต่อไปนี้ในไฟล์ `Cargo.toml` ของคุณ

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

จากนั้นคุณสามารถนำเข้าไลบรารีที่จำเป็นในโค้ดไคลเอนต์ของคุณ

```rust
use rmcp::{
    RmcpError,
    model::CallToolRequestParam,
    service::ServiceExt,
    transport::{ConfigureCommandExt, TokioChildProcess},
};
use tokio::process::Command;
```

เรามาดำเนินการสร้างอินสแตนซ์กันต่อ

### -2- การสร้างไคลเอนต์และการขนส่ง

เราจะต้องสร้างอินสแตนซ์ของการขนส่งและไคลเอนต์ของเรา:

#### TypeScript

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

ในโค้ดข้างต้นเรา:

- สร้างอินสแตนซ์ stdio transport สังเกตว่ามันระบุคำสั่งและอาร์กิวเมนต์สำหรับวิธีการค้นหาและเริ่มต้นเซิร์ฟเวอร์ เนื่องจากเป็นสิ่งที่เราจะต้องทำเมื่อเราสร้างไคลเอนต์

    ```typescript
    const transport = new StdioClientTransport({
        command: "node",
        args: ["server.js"]
    });
    ```

- สร้างไคลเอนต์โดยให้ชื่อและเวอร์ชัน

    ```typescript
    const client = new Client(
    {
        name: "example-client",
        version: "1.0.0"
    });
    ```

- เชื่อมต่อไคลเอนต์กับวิธีการขนส่งที่เลือก

    ```typescript
    await client.connect(transport);
    ```

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

ในโค้ดข้างต้นเรา:

- นำเข้าไลบรารีที่จำเป็น
- สร้างออบเจ็กต์พารามิเตอร์เซิร์ฟเวอร์ เนื่องจากเราจะใช้สิ่งนี้เพื่อรันเซิร์ฟเวอร์เพื่อให้เราสามารถเชื่อมต่อกับมันด้วยไคลเอนต์ของเรา
- กำหนดเมธอด `run` ซึ่งเรียก `stdio_client` ซึ่งเริ่มเซสชันไคลเอนต์
- สร้างจุดเริ่มต้นที่เราให้เมธอด `run` กับ `asyncio.run`

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

ในโค้ดข้างต้นเรา:

- นำเข้าไลบรารีที่จำเป็น
- สร้าง stdio transport และสร้างไคลเอนต์ `mcpClient` ซึ่งเราจะใช้ลิสต์และเรียกใช้งานฟีเจอร์ต่างๆ บน MCP Server

หมายเหตุ ใน "Arguments" คุณสามารถชี้ไปที่ *.csproj* หรือไฟล์ executable

#### Java

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

ในโค้ดข้างต้นเรา:

- สร้างเมธอดหลักที่ตั้งค่า SSE transport โดยชี้ไปที่ `http://localhost:8080` ซึ่ง MCP Server ของเราจะทำงานอยู่
- สร้างคลาสไคลเอนต์ที่รับ transport เป็นพารามิเตอร์ตัวสร้าง
- ในเมธอด `run` เราสร้าง MCP client แบบ synchronous โดยใช้ transport และเริ่มการเชื่อมต่อ
- ใช้ SSE (Server-Sent Events) transport ซึ่งเหมาะสำหรับการสื่อสารแบบ HTTP กับ MCP Server ที่ใช้ Java Spring Boot

#### Rust

ไคลเอนต์ Rust นี้สมมติว่าเซิร์ฟเวอร์เป็นโปรเจกต์พี่น้องชื่อ "calculator-server" ในไดเรกทอรีเดียวกัน โค้ดด้านล่างจะเริ่มเซิร์ฟเวอร์และเชื่อมต่อกับมัน

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

### -3- การลิสต์ฟีเจอร์ของเซิร์ฟเวอร์

ตอนนี้เราได้ไคลเอนต์ที่สามารถเชื่อมต่อได้เมื่อโปรแกรมถูกเรียกใช้งาน อย่างไรก็ตาม มันยังไม่ได้ลิสต์ฟีเจอร์ของมัน ดังนั้นเรามาทำสิ่งนี้ต่อไป:

#### TypeScript

```typescript
// List prompts
const prompts = await client.listPrompts();

// List resources
const resources = await client.listResources();

// list tools
const tools = await client.listTools();
```

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
```

ที่นี่เราได้ลิสต์ทรัพยากรที่มีอยู่ `list_resources()` และเครื่องมือ `list_tools` และพิมพ์ออกมา

#### .NET

```dotnet
foreach (var tool in await client.ListToolsAsync())
{
    Console.WriteLine($"{tool.Name} ({tool.Description})");
}
```

ด้านบนเป็นตัวอย่างวิธีที่เราสามารถลิสต์เครื่องมือบนเซิร์ฟเวอร์ สำหรับแต่ละเครื่องมือ เราจะพิมพ์ชื่อของมันออกมา

#### Java

```java
// List and demonstrate tools
ListToolsResult toolsList = client.listTools();
System.out.println("Available Tools = " + toolsList);

// You can also ping the server to verify connection
client.ping();
```

ในโค้ดข้างต้นเรา:

- เรียก `listTools()` เพื่อรับเครื่องมือทั้งหมดที่มีอยู่จาก MCP Server
- ใช้ `ping()` เพื่อตรวจสอบว่าการเชื่อมต่อกับเซิร์ฟเวอร์ทำงานอยู่
- `ListToolsResult` มีข้อมูลเกี่ยวกับเครื่องมือทั้งหมด รวมถึงชื่อ คำอธิบาย และสคีมารับข้อมูล

เยี่ยม ตอนนี้เราได้จับฟีเจอร์ทั้งหมดแล้ว คำถามคือเราจะใช้มันเมื่อไหร่? ไคลเอนต์นี้ค่อนข้างเรียบง่าย เรียบง่ายในแง่ที่ว่าเราจะต้องเรียกฟีเจอร์โดยเฉพาะเมื่อเราต้องการ ในบทถัดไป เราจะสร้างไคลเอนต์ที่มีความก้าวหน้ามากขึ้นที่สามารถเข้าถึงโมเดลภาษาขนาดใหญ่ (LLM) ของตัวเองได้ สำหรับตอนนี้ เรามาดูกันว่าเราสามารถเรียกใช้งานฟีเจอร์บนเซิร์ฟเวอร์ได้อย่างไร:

#### Rust

ในฟังก์ชันหลัก หลังจากเริ่มต้นไคลเอนต์ เราสามารถเริ่มเซิร์ฟเวอร์และลิสต์ฟีเจอร์บางส่วนของมัน

```rust
// Initialize
let server_info = client.peer_info();
println!("Server info: {:?}", server_info);

// List tools
let tools = client.list_tools(Default::default()).await?;
println!("Available tools: {:?}", tools);
```

### -4- การเรียกใช้งานฟีเจอร์

ในการเรียกใช้งานฟีเจอร์ เราต้องแน่ใจว่าเราได้ระบุอาร์กิวเมนต์ที่ถูกต้อง และในบางกรณีชื่อของสิ่งที่เรากำลังเรียกใช้งาน

#### TypeScript

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

ในโค้ดข้างต้นเรา:

- อ่านทรัพยากร เราเรียกทรัพยากรโดยเรียก `readResource()` โดยระบุ `uri` นี่คือสิ่งที่มันน่าจะดูเหมือนในฝั่งเซิร์ฟเวอร์:

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

    ค่า `uri` ของเรา `file://example.txt` ตรงกับ `file://{name}` บนเซิร์ฟเวอร์ `example.txt` จะถูกแมปกับ `name`

- เรียกเครื่องมือ เราเรียกมันโดยระบุ `name` และ `arguments` ดังนี้:

    ```typescript
    const result = await client.callTool({
        name: "example-tool",
        arguments: {
            arg1: "value"
        }
    });
    ```

- รับคำสั่ง เพื่อรับคำสั่ง คุณเรียก `getPrompt()` พร้อม `name` และ `arguments` โค้ดเซิร์ฟเวอร์ดูเหมือนดังนี้:

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

    และโค้ดไคลเอนต์ของคุณจึงดูเหมือนดังนี้เพื่อให้ตรงกับสิ่งที่ประกาศบนเซิร์ฟเวอร์:

    ```typescript
    const promptResult = await client.getPrompt({
        name: "review-code",
        arguments: {
            code: "console.log(\"Hello world\")"
        }
    })
    ```

#### Python

```python
# Read a resource
print("READING RESOURCE")
content, mime_type = await session.read_resource("greeting://hello")

# Call a tool
print("CALL TOOL")
result = await session.call_tool("add", arguments={"a": 1, "b": 7})
print(result.content)
```

ในโค้ดข้างต้นเรา:

- เรียกทรัพยากรชื่อ `greeting` โดยใช้ `read_resource`
- เรียกเครื่องมือชื่อ `add` โดยใช้ `call_tool`

#### .NET

1. เพิ่มโค้ดเพื่อเรียกเครื่องมือ:

  ```csharp
  var result = await mcpClient.CallToolAsync(
      "Add",
      new Dictionary<string, object?>() { ["a"] = 1, ["b"] = 3  },
      cancellationToken:CancellationToken.None);
  ```

1. เพื่อพิมพ์ผลลัพธ์ นี่คือโค้ดบางส่วนเพื่อจัดการสิ่งนั้น:

  ```csharp
  Console.WriteLine(result.Content.First(c => c.Type == "text").Text);
  // Sum 4
  ```

#### Java

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

ในโค้ดข้างต้นเรา:

- เรียกเครื่องมือคำนวณหลายตัวโดยใช้เมธอด `callTool()` พร้อมออบเจ็กต์ `CallToolRequest`
- การเรียกเครื่องมือแต่ละครั้งระบุชื่อเครื่องมือและ `Map` ของอาร์กิวเมนต์ที่เครื่องมือดังกล่าวต้องการ
- เครื่องมือเซิร์ฟเวอร์คาดหวังชื่อพารามิเตอร์เฉพาะ (เช่น "a", "b" สำหรับการดำเนินการทางคณิตศาสตร์)
- ผลลัพธ์จะถูกส่งกลับเป็นออบเจ็กต์ `CallToolResult` ที่มีการตอบกลับจากเซิร์ฟเวอร์

#### Rust

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

### -5- การรันไคลเอนต์

ในการรันไคลเอนต์ ให้พิมพ์คำสั่งต่อไปนี้ในเทอร์มินัล:

#### TypeScript

เพิ่มรายการต่อไปนี้ในส่วน "scripts" ใน *package.json*:

```json
"client": "tsc && node build/client.js"
```

```sh
npm run client
```

#### Python

เรียกไคลเอนต์ด้วยคำสั่งต่อไปนี้:

```sh
python client.py
```

#### .NET

```sh
dotnet run
```

#### Java

ก่อนอื่น ตรวจสอบให้แน่ใจว่า MCP Server ของคุณทำงานอยู่ที่ `http://localhost:8080` จากนั้นรันไคลเอนต์:

```bash
# Build you project
./mvnw clean compile

# Run the client
./mvnw exec:java -Dexec.mainClass="com.microsoft.mcp.sample.client.SDKClient"
```

หรือคุณสามารถรันโปรเจกต์ไคลเอนต์ที่สมบูรณ์ซึ่งมีให้ในโฟลเดอร์โซลูชัน `03-GettingStarted\02-client\solution\java`:

```bash
# Navigate to the solution directory
cd 03-GettingStarted/02-client/solution/java

# Build and run the JAR
./mvnw clean package
java -jar target/calculator-client-0.0.1-SNAPSHOT.jar
```

#### Rust

```bash
cargo fmt
cargo run
```

## งานที่ได้รับมอบหมาย

ในงานนี้ คุณจะใช้สิ่งที่คุณได้เรียนรู้ในการสร้างไคลเอนต์ แต่สร้างไคลเอนต์ของคุณเอง

นี่คือเซิร์ฟเวอร์ที่คุณสามารถใช้ซึ่งคุณต้องเรียกผ่านโค้ดไคลเอนต์ของคุณ ลองดูว่าคุณสามารถเพิ่มฟีเจอร์เพิ่มเติมให้กับเซิร์ฟเวอร์เพื่อทำให้มันน่าสนใจยิ่งขึ้นได้หรือไม่

### TypeScript

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

### Python

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

ดูโปรเจกต์นี้เพื่อดูวิธี [เพิ่มคำสั่งและทรัพยากร](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/EverythingServer/Program.cs)

นอกจากนี้ ตรวจสอบลิงก์นี้เพื่อดูวิธีการเรียกใช้ [คำสั่งและทรัพยากร](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol/Client/)

### Rust

ใน [ส่วนก่อนหน้า](../../../../03-GettingStarted/01-first-server) คุณได้เรียนรู้วิธีสร้าง MCP Server แบบง่ายๆ ด้วย Rust คุณสามารถสร้างต่อจากนั้นหรือดูลิงก์นี้สำหรับตัวอย่าง MCP Server ที่ใช้ Rust เพิ่มเติม: [MCP Server Examples](https://github.com/modelcontextprotocol/rust-sdk/tree/main/examples/servers)

## โซลูชัน

**โฟลเดอร์โซลูชัน** มีการใช้งานไคลเอนต์ที่สมบูรณ์และพร้อมใช้งานซึ่งแสดงแนวคิดทั้งหมดที่ครอบคลุมในบทเรียนนี้ แต่ละโซลูชันมีทั้งโค้ดไคลเอนต์และเซิร์ฟเวอร์ที่จัดระเบียบในโปรเจกต์ที่แยกออกจากกันและสมบูรณ์ในตัวเอง

### 📁 โครงสร้างโซลูชัน

ไดเรกทอรีโซลูชันถูกจัดระเบียบตามภาษาการเขียนโปรแกรม:

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

### 🚀 สิ่งที่แต่ละโซลูชันมี

แต่ละโซลูชันเฉพาะภาษามี:

- **การใช้งานไคลเอนต์ที่สมบูรณ์** พร้อมฟีเจอร์ทั้งหมดจากบทเรียน
- **โครงสร้างโปรเจกต์ที่ใช้งานได้** พร้อมการพึ่งพาและการกำหนดค่าที่เหมาะสม
- **สคริปต์การสร้างและการรัน** เพื่อการตั้งค่าและการดำเนินการที่ง่าย
- **README ที่ละเอียด** พร้อมคำแนะนำเฉพาะภาษา
- **ตัวอย่างการจัดการข้อผิดพลาด** และการประมวลผลผลลัพธ์

### 📖 การใช้โซลูชัน

1. **ไปยังโฟลเดอร์ภาษาที่คุณต้องการ**:

   ```bash
   cd solution/typescript/    # For TypeScript
   cd solution/java/          # For Java
   cd solution/python/        # For Python
   cd solution/dotnet/        # For .NET
   ```

2. **ทำตามคำแนะนำใน README** ในแต่ละโฟลเดอร์สำหรับ:
   - การติดตั้งการพึ่งพา
   - การสร้างโปรเจกต์
   - การรันไคลเอนต์

3. **ตัวอย่างผลลัพธ์** ที่คุณควรเห็น:

   ```text
   Prompt: Please review this code: console.log("hello");
   Resource template: file
   Tool result: { content: [ { type: 'text', text: '9' } ] }
   ```

สำหรับเอกสารประกอบและคำแนะนำทีละขั้นตอน ดู: **[📖 เอกสารโซลูชัน](./solution/README.md)**

## 🎯 ตัวอย่างที่สมบูรณ์

เราได้จัดเตรียมการใช้งานไคลเอนต์ที่สมบูรณ์และใช้งานได้สำหรับทุกภาษาการเขียนโปรแกรมที่ครอบคลุมในบทเรียนนี้ ตัวอย่างเหล่านี้แสดงฟังก์ชันการทำงานเต็มรูปแบบที่อธิบายไว้ข้างต้นและสามารถใช้เป็นการอ้างอิงหรือจุดเริ่มต้นสำหรับโปรเจกต์ของคุณเอง

### ตัวอย่างที่สมบูรณ์ที่มีให้

| ภาษา | ไฟล์ | คำอธิบาย |
|------|------|----------|
| **Java** | [`client_example_java.java`](../../../../03-GettingStarted/02-client/client_example_java.java) | ไคลเอนต์ Java ที่สมบูรณ์โดยใช้ SSE transport พร้อมการจัดการข้อผิดพลาดที่ครอบคลุม |
| **C#** | [`client_example_csharp.cs`](../../../../03-GettingStarted/02-client/client_example_csharp.cs) | ไคลเอนต์ C# ที่สมบูรณ์โดยใช้ stdio transport พร้อมการเริ่มต้นเซิร์ฟเวอร์อัตโนมัติ |
| **TypeScript** | [`client_example_typescript.ts
ตัวอย่างที่สมบูรณ์แต่ละตัวอย่างประกอบด้วย:

- ✅ **การสร้างการเชื่อมต่อ** และการจัดการข้อผิดพลาด  
- ✅ **การค้นหาเซิร์ฟเวอร์** (เครื่องมือ, ทรัพยากร, คำแนะนำเมื่อเหมาะสม)  
- ✅ **การทำงานของเครื่องคิดเลข** (บวก, ลบ, คูณ, หาร, ความช่วยเหลือ)  
- ✅ **การประมวลผลผลลัพธ์** และการแสดงผลลัพธ์ในรูปแบบที่จัดรูปแบบ  
- ✅ **การจัดการข้อผิดพลาดอย่างครอบคลุม**  
- ✅ **โค้ดที่สะอาดและมีคำอธิบาย** พร้อมคำอธิบายทีละขั้นตอน  

### เริ่มต้นใช้งานตัวอย่างที่สมบูรณ์

1. **เลือกภาษาที่คุณต้องการ** จากตารางด้านบน  
2. **ตรวจสอบไฟล์ตัวอย่างที่สมบูรณ์** เพื่อทำความเข้าใจการใช้งานทั้งหมด  
3. **รันตัวอย่าง** ตามคำแนะนำใน [`complete_examples.md`](./complete_examples.md)  
4. **ปรับแต่งและขยาย** ตัวอย่างให้เหมาะสมกับกรณีการใช้งานของคุณ  

สำหรับเอกสารประกอบโดยละเอียดเกี่ยวกับการรันและปรับแต่งตัวอย่างเหล่านี้ ดูได้ที่: **[📖 เอกสารตัวอย่างที่สมบูรณ์](./complete_examples.md)**  

### 💡 ความแตกต่างระหว่างโซลูชันและตัวอย่างที่สมบูรณ์

| **โฟลเดอร์โซลูชัน** | **ตัวอย่างที่สมบูรณ์** |
|--------------------|--------------------- |
| โครงสร้างโปรเจกต์แบบเต็มพร้อมไฟล์ Build | การใช้งานในไฟล์เดียว |
| พร้อมรันพร้อมกับ Dependencies | ตัวอย่างโค้ดที่เน้นการศึกษา |
| การตั้งค่าแบบ Production | การอ้างอิงเพื่อการเรียนรู้ |
| เครื่องมือเฉพาะภาษา | การเปรียบเทียบข้ามภาษา |

ทั้งสองวิธีมีคุณค่า - ใช้ **โฟลเดอร์โซลูชัน** สำหรับโปรเจกต์ที่สมบูรณ์ และใช้ **ตัวอย่างที่สมบูรณ์** เพื่อการเรียนรู้และอ้างอิง  

## ประเด็นสำคัญ

ประเด็นสำคัญสำหรับบทนี้เกี่ยวกับไคลเอนต์มีดังนี้:

- สามารถใช้เพื่อค้นหาและเรียกใช้งานฟีเจอร์บนเซิร์ฟเวอร์  
- สามารถเริ่มเซิร์ฟเวอร์ในขณะที่ตัวเองเริ่มทำงาน (เหมือนในบทนี้) แต่ไคลเอนต์สามารถเชื่อมต่อกับเซิร์ฟเวอร์ที่กำลังทำงานอยู่ได้เช่นกัน  
- เป็นวิธีที่ยอดเยี่ยมในการทดสอบความสามารถของเซิร์ฟเวอร์ ควบคู่ไปกับทางเลือกอื่น เช่น Inspector ที่ได้กล่าวถึงในบทก่อนหน้า  

## ทรัพยากรเพิ่มเติม

- [การสร้างไคลเอนต์ใน MCP](https://modelcontextprotocol.io/quickstart/client)  

## ตัวอย่าง

- [Java Calculator](../samples/java/calculator/README.md)  
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)  
- [JavaScript Calculator](../samples/javascript/README.md)  
- [TypeScript Calculator](../samples/typescript/README.md)  
- [Python Calculator](../../../../03-GettingStarted/samples/python)  
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)  

## สิ่งที่จะทำต่อไป

- ถัดไป: [การสร้างไคลเอนต์ด้วย LLM](../03-llm-client/README.md)  

**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) แม้ว่าเราจะพยายามให้การแปลมีความถูกต้อง แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่แม่นยำ เอกสารต้นฉบับในภาษาต้นทางควรถือเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ขอแนะนำให้ใช้บริการแปลภาษามนุษย์มืออาชีพ เราจะไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดซึ่งเกิดจากการใช้การแปลนี้