<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "94c80ae71fb9971e9b57b51ab0912121",
  "translation_date": "2025-08-18T15:15:59+00:00",
  "source_file": "03-GettingStarted/02-client/README.md",
  "language_code": "bn"
}
-->
# ক্লায়েন্ট তৈরি করা

ক্লায়েন্ট হলো কাস্টম অ্যাপ্লিকেশন বা স্ক্রিপ্ট যা সরাসরি MCP সার্ভারের সাথে যোগাযোগ করে রিসোর্স, টুল এবং প্রম্পট অনুরোধ করার জন্য। ইন্সপেক্টর টুল ব্যবহার করার বিপরীতে, যা গ্রাফিকাল ইন্টারফেস সরবরাহ করে, নিজের ক্লায়েন্ট লেখার মাধ্যমে প্রোগ্রাম্যাটিক এবং স্বয়ংক্রিয় ইন্টারঅ্যাকশন সম্ভব হয়। এটি ডেভেলপারদের তাদের নিজস্ব ওয়ার্কফ্লোতে MCP ক্ষমতাগুলি সংযুক্ত করতে, কাজগুলো স্বয়ংক্রিয় করতে এবং নির্দিষ্ট প্রয়োজন অনুযায়ী কাস্টম সমাধান তৈরি করতে সক্ষম করে।

## ওভারভিউ

এই পাঠটি MCP ইকোসিস্টেমে ক্লায়েন্টের ধারণা পরিচয় করিয়ে দেয়। আপনি শিখবেন কীভাবে নিজের ক্লায়েন্ট লিখতে হয় এবং MCP সার্ভারের সাথে সংযোগ স্থাপন করতে হয়।

## শেখার লক্ষ্য

এই পাঠ শেষে, আপনি সক্ষম হবেন:

- ক্লায়েন্ট কী করতে পারে তা বুঝতে।
- নিজের ক্লায়েন্ট লিখতে।
- MCP সার্ভারের সাথে ক্লায়েন্ট সংযোগ এবং পরীক্ষা করতে যাতে নিশ্চিত করা যায় যে সার্ভারটি প্রত্যাশিতভাবে কাজ করছে।

## ক্লায়েন্ট লেখার জন্য কী কী প্রয়োজন?

ক্লায়েন্ট লেখার জন্য আপনাকে নিম্নলিখিত কাজগুলো করতে হবে:

- **সঠিক লাইব্রেরি আমদানি করুন**। আপনি আগের মতো একই লাইব্রেরি ব্যবহার করবেন, শুধু ভিন্ন কনস্ট্রাক্ট।
- **ক্লায়েন্ট ইনস্ট্যান্স তৈরি করুন**। এটি একটি ক্লায়েন্ট ইনস্ট্যান্স তৈরি এবং নির্বাচিত ট্রান্সপোর্ট পদ্ধতির সাথে সংযোগ স্থাপন করবে।
- **কোন রিসোর্স তালিকাভুক্ত করবেন তা নির্ধারণ করুন**। আপনার MCP সার্ভারে রিসোর্স, টুল এবং প্রম্পট রয়েছে, আপনাকে নির্ধারণ করতে হবে কোনটি তালিকাভুক্ত করবেন।
- **ক্লায়েন্টকে হোস্ট অ্যাপ্লিকেশনে সংযুক্ত করুন**। একবার আপনি সার্ভারের ক্ষমতাগুলি জানলে, আপনাকে এটি আপনার হোস্ট অ্যাপ্লিকেশনে সংযুক্ত করতে হবে যাতে ব্যবহারকারী কোনো প্রম্পট বা কমান্ড টাইপ করলে সংশ্লিষ্ট সার্ভার ফিচারটি সক্রিয় হয়।

এখন আমরা উচ্চ পর্যায়ে বুঝেছি কী করতে যাচ্ছি, চলুন একটি উদাহরণ দেখি।

### একটি উদাহরণ ক্লায়েন্ট

চলুন এই উদাহরণ ক্লায়েন্টটি দেখি:

### টাইপস্ক্রিপ্ট

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

উপরের কোডে আমরা:

- লাইব্রেরি আমদানি করেছি।
- একটি ক্লায়েন্ট ইনস্ট্যান্স তৈরি করেছি এবং stdio ব্যবহার করে সংযোগ করেছি।
- প্রম্পট, রিসোর্স এবং টুল তালিকাভুক্ত করেছি এবং সেগুলো সক্রিয় করেছি।

এখানে আপনার কাছে একটি ক্লায়েন্ট রয়েছে যা MCP সার্ভারের সাথে কথা বলতে পারে।

পরবর্তী অনুশীলন অংশে আমরা প্রতিটি কোড স্নিপেট বিশ্লেষণ করব এবং ব্যাখ্যা করব কী ঘটছে।

## অনুশীলন: ক্লায়েন্ট লেখা

উপরের মতো, চলুন কোডটি ব্যাখ্যা করতে সময় নিই, এবং আপনি চাইলে কোডটি অনুসরণ করতে পারেন।

### -১- লাইব্রেরি আমদানি

চলুন আমরা প্রয়োজনীয় লাইব্রেরি আমদানি করি। আমাদের একটি ক্লায়েন্ট এবং আমাদের নির্বাচিত ট্রান্সপোর্ট প্রোটোকল, stdio-এর রেফারেন্স প্রয়োজন। stdio হলো একটি প্রোটোকল যা আপনার লোকাল মেশিনে চলার জন্য তৈরি। SSE হলো আরেকটি ট্রান্সপোর্ট প্রোটোকল যা আমরা ভবিষ্যতের অধ্যায়ে দেখাব, তবে এটি আপনার অন্য বিকল্প। আপাতত, চলুন stdio দিয়ে চালিয়ে যাই।

#### টাইপস্ক্রিপ্ট

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
```

#### পাইথন

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

#### জাভা

জাভার জন্য, আপনি আগের অনুশীলন থেকে MCP সার্ভারের সাথে সংযোগ স্থাপনকারী একটি ক্লায়েন্ট তৈরি করবেন। [Getting Started with MCP Server](../../../../03-GettingStarted/01-first-server/solution/java) থেকে একই জাভা স্প্রিং বুট প্রকল্প কাঠামো ব্যবহার করে `SDKClient` নামে একটি নতুন জাভা ক্লাস তৈরি করুন এবং নিম্নলিখিত আমদানিগুলি যোগ করুন:

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

#### রাস্ট

আপনার `Cargo.toml` ফাইলে নিম্নলিখিত ডিপেনডেন্সি যোগ করতে হবে।

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

এরপর, আপনি আপনার ক্লায়েন্ট কোডে প্রয়োজনীয় লাইব্রেরি আমদানি করতে পারেন।

```rust
use rmcp::{
    RmcpError,
    model::CallToolRequestParam,
    service::ServiceExt,
    transport::{ConfigureCommandExt, TokioChildProcess},
};
use tokio::process::Command;
```

চলুন ইনস্ট্যান্স তৈরি করার দিকে এগিয়ে যাই।

### -২- ক্লায়েন্ট এবং ট্রান্সপোর্ট ইনস্ট্যান্স তৈরি করা

আমাদের একটি ট্রান্সপোর্ট এবং একটি ক্লায়েন্ট ইনস্ট্যান্স তৈরি করতে হবে:

#### টাইপস্ক্রিপ্ট

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

উপরের কোডে আমরা:

- একটি stdio ট্রান্সপোর্ট ইনস্ট্যান্স তৈরি করেছি। লক্ষ্য করুন এটি কীভাবে কমান্ড এবং আর্গুমেন্ট নির্দিষ্ট করে সার্ভারটি খুঁজে এবং চালু করতে।
  
    ```typescript
    const transport = new StdioClientTransport({
        command: "node",
        args: ["server.js"]
    });
    ```

- একটি ক্লায়েন্ট ইনস্ট্যান্স তৈরি করেছি, যেখানে নাম এবং ভার্সন দিয়েছি।

    ```typescript
    const client = new Client(
    {
        name: "example-client",
        version: "1.0.0"
    });
    ```

- ক্লায়েন্টকে নির্বাচিত ট্রান্সপোর্টে সংযুক্ত করেছি।

    ```typescript
    await client.connect(transport);
    ```

#### পাইথন

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

উপরের কোডে আমরা:

- প্রয়োজনীয় লাইব্রেরি আমদানি করেছি।
- একটি সার্ভার প্যারামিটার অবজেক্ট ইনস্ট্যান্স তৈরি করেছি যা আমরা সার্ভার চালানোর জন্য ব্যবহার করব যাতে আমাদের ক্লায়েন্টের সাথে সংযোগ স্থাপন করা যায়।
- একটি `run` মেথড সংজ্ঞায়িত করেছি যা `stdio_client` কল করে এবং একটি ক্লায়েন্ট সেশন শুরু করে।
- একটি এন্ট্রি পয়েন্ট তৈরি করেছি যেখানে আমরা `asyncio.run`-এ `run` মেথড সরবরাহ করি।

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

উপরের কোডে আমরা:

- প্রয়োজনীয় লাইব্রেরি আমদানি করেছি।
- একটি stdio ট্রান্সপোর্ট তৈরি করেছি এবং একটি ক্লায়েন্ট `mcpClient` তৈরি করেছি। এটি MCP সার্ভারে ফিচার তালিকাভুক্ত এবং সক্রিয় করতে ব্যবহার করা হবে।

লক্ষ্য করুন, "Arguments"-এ আপনি *.csproj* বা এক্সিকিউটেবল পয়েন্ট করতে পারেন।

#### জাভা

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

উপরের কোডে আমরা:

- একটি মেইন মেথড তৈরি করেছি যা `http://localhost:8080`-এ চলমান MCP সার্ভারের জন্য SSE ট্রান্সপোর্ট সেট আপ করে।
- একটি ক্লায়েন্ট ক্লাস তৈরি করেছি যা ট্রান্সপোর্টকে কনস্ট্রাক্টর প্যারামিটার হিসেবে গ্রহণ করে।
- `run` মেথডে, আমরা একটি সিঙ্ক্রোনাস MCP ক্লায়েন্ট তৈরি করেছি এবং সংযোগটি ইনিশিয়ালাইজ করেছি।
- SSE (Server-Sent Events) ট্রান্সপোর্ট ব্যবহার করেছি যা জাভা স্প্রিং বুট MCP সার্ভারের সাথে HTTP-ভিত্তিক যোগাযোগের জন্য উপযুক্ত।

#### রাস্ট

এই রাস্ট ক্লায়েন্টটি ধরে নিচ্ছে সার্ভারটি একই ডিরেক্টরিতে "calculator-server" নামে একটি সিবলিং প্রকল্প। নিচের কোডটি সার্ভার শুরু করবে এবং এর সাথে সংযোগ স্থাপন করবে।

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

### -৩- সার্ভারের ফিচার তালিকাভুক্ত করা

এখন, আমাদের কাছে একটি ক্লায়েন্ট রয়েছে যা প্রোগ্রাম চালানো হলে সংযোগ করতে পারে। তবে, এটি আসলে এর ফিচার তালিকাভুক্ত করে না, তাই চলুন এটি করি:

#### টাইপস্ক্রিপ্ট

```typescript
// List prompts
const prompts = await client.listPrompts();

// List resources
const resources = await client.listResources();

// list tools
const tools = await client.listTools();
```

#### পাইথন

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

এখানে আমরা উপলব্ধ রিসোর্স `list_resources()` এবং টুল `list_tools` তালিকাভুক্ত করেছি এবং সেগুলো প্রিন্ট করেছি।

#### .NET

```dotnet
foreach (var tool in await client.ListToolsAsync())
{
    Console.WriteLine($"{tool.Name} ({tool.Description})");
}
```

উপরের উদাহরণে আমরা সার্ভারের টুলগুলো তালিকাভুক্ত করেছি। প্রতিটি টুলের জন্য, আমরা এর নাম প্রিন্ট করেছি।

#### জাভা

```java
// List and demonstrate tools
ListToolsResult toolsList = client.listTools();
System.out.println("Available Tools = " + toolsList);

// You can also ping the server to verify connection
client.ping();
```

উপরের কোডে আমরা:

- `listTools()` কল করে MCP সার্ভার থেকে সমস্ত উপলব্ধ টুল পেয়েছি।
- `ping()` ব্যবহার করে নিশ্চিত করেছি যে সার্ভারের সাথে সংযোগ কাজ করছে।
- `ListToolsResult`-এ সমস্ত টুলের তথ্য রয়েছে, যেমন নাম, বিবরণ এবং ইনপুট স্কিমা।

দারুণ, এখন আমরা সমস্ত ফিচার সংগ্রহ করেছি। প্রশ্ন হলো, আমরা কখন সেগুলো ব্যবহার করব? এই ক্লায়েন্টটি বেশ সহজ, সহজ এই অর্থে যে আমাদের স্পষ্টভাবে ফিচারগুলো কল করতে হবে যখন আমরা সেগুলো চাই। পরবর্তী অধ্যায়ে, আমরা একটি আরও উন্নত ক্লায়েন্ট তৈরি করব যার নিজস্ব বড় ভাষার মডেল (LLM) থাকবে। আপাতত, চলুন দেখি কীভাবে আমরা সার্ভারের ফিচারগুলো সক্রিয় করতে পারি:

#### রাস্ট

মেইন ফাংশনে, ক্লায়েন্ট ইনিশিয়ালাইজ করার পরে, আমরা সার্ভার ইনিশিয়ালাইজ করতে পারি এবং এর কিছু ফিচার তালিকাভুক্ত করতে পারি।

```rust
// Initialize
let server_info = client.peer_info();
println!("Server info: {:?}", server_info);

// List tools
let tools = client.list_tools(Default::default()).await?;
println!("Available tools: {:?}", tools);
```

### -৪- ফিচার সক্রিয় করা

ফিচার সক্রিয় করতে আমাদের সঠিক আর্গুমেন্ট এবং কিছু ক্ষেত্রে আমরা যা সক্রিয় করতে চাই তার নাম নির্দিষ্ট করতে হবে।

#### টাইপস্ক্রিপ্ট

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

উপরের কোডে আমরা:

- একটি রিসোর্স পড়েছি, আমরা `readResource()` কল করে `uri` নির্দিষ্ট করেছি। এটি সার্ভার সাইডে সম্ভবত এরকম দেখাবে:

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

    আমাদের `uri` মান `file://example.txt` সার্ভারের `file://{name}`-এর সাথে মিলে যায়। `example.txt` `name`-এ ম্যাপ হবে।

- একটি টুল কল করেছি, আমরা এটি `name` এবং `arguments` নির্দিষ্ট করে কল করেছি, যেমন:

    ```typescript
    const result = await client.callTool({
        name: "example-tool",
        arguments: {
            arg1: "value"
        }
    });
    ```

- একটি প্রম্পট পেয়েছি, প্রম্পট পেতে আমরা `getPrompt()` কল করেছি `name` এবং `arguments` দিয়ে। সার্ভার কোডটি এরকম দেখাবে:

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

    এবং আপনার ক্লায়েন্ট কোডটি এরকম দেখাবে যাতে এটি সার্ভারে ঘোষিত কোডের সাথে মিলে যায়:

    ```typescript
    const promptResult = await client.getPrompt({
        name: "review-code",
        arguments: {
            code: "console.log(\"Hello world\")"
        }
    })
    ```

#### পাইথন

```python
# Read a resource
print("READING RESOURCE")
content, mime_type = await session.read_resource("greeting://hello")

# Call a tool
print("CALL TOOL")
result = await session.call_tool("add", arguments={"a": 1, "b": 7})
print(result.content)
```

উপরের কোডে আমরা:

- `read_resource` ব্যবহার করে `greeting` নামে একটি রিসোর্স কল করেছি।
- `call_tool` ব্যবহার করে `add` নামে একটি টুল সক্রিয় করেছি।

#### .NET

1. একটি টুল কল করার জন্য কিছু কোড যোগ করুন:

  ```csharp
  var result = await mcpClient.CallToolAsync(
      "Add",
      new Dictionary<string, object?>() { ["a"] = 1, ["b"] = 3  },
      cancellationToken:CancellationToken.None);
  ```

1. ফলাফল প্রিন্ট করার জন্য, এখানে কিছু কোড রয়েছে:

  ```csharp
  Console.WriteLine(result.Content.First(c => c.Type == "text").Text);
  // Sum 4
  ```

#### জাভা

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

উপরের কোডে আমরা:

- `callTool()` মেথড ব্যবহার করে `CallToolRequest` অবজেক্ট দিয়ে একাধিক ক্যালকুলেটর টুল কল করেছি।
- প্রতিটি টুল কল নির্দিষ্ট টুলের নাম এবং সেই টুলের প্রয়োজনীয় আর্গুমেন্টের একটি `Map` নির্দিষ্ট করে।
- সার্ভার টুলগুলো নির্দিষ্ট প্যারামিটার নাম (যেমন "a", "b" গাণিতিক অপারেশনের জন্য) প্রত্যাশা করে।
- ফলাফলগুলো `CallToolResult` অবজেক্ট হিসেবে ফেরত আসে যা সার্ভার থেকে প্রতিক্রিয়া ধারণ করে।

#### রাস্ট

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

### -৫- ক্লায়েন্ট চালানো

ক্লায়েন্ট চালানোর জন্য টার্মিনালে নিম্নলিখিত কমান্ড টাইপ করুন:

#### টাইপস্ক্রিপ্ট

আপনার *package.json*-এর "scripts" সেকশনে নিম্নলিখিত এন্ট্রি যোগ করুন:

```json
"client": "tsc && node build/client.js"
```

```sh
npm run client
```

#### পাইথন

নিম্নলিখিত কমান্ড দিয়ে ক্লায়েন্ট কল করুন:

```sh
python client.py
```

#### .NET

```sh
dotnet run
```

#### জাভা

প্রথমে নিশ্চিত করুন আপনার MCP সার্ভার `http://localhost:8080`-এ চলছে। এরপর ক্লায়েন্ট চালান:

```bash
# Build you project
./mvnw clean compile

# Run the client
./mvnw exec:java -Dexec.mainClass="com.microsoft.mcp.sample.client.SDKClient"
```

অথবা, আপনি সম্পূর্ণ ক্লায়েন্ট প্রকল্প চালাতে পারেন যা `03-GettingStarted\02-client\solution\java` ফোল্ডারে সরবরাহ করা হয়েছে:

```bash
# Navigate to the solution directory
cd 03-GettingStarted/02-client/solution/java

# Build and run the JAR
./mvnw clean package
java -jar target/calculator-client-0.0.1-SNAPSHOT.jar
```

#### রাস্ট

```bash
cargo fmt
cargo run
```

## অ্যাসাইনমেন্ট

এই অ্যাসাইনমেন্টে, আপনি যা শিখেছেন তা ব্যবহার করে একটি ক্লায়েন্ট তৈরি করবেন, তবে নিজের ক্লায়েন্ট তৈরি করবেন।

এখানে একটি সার্ভার রয়েছে যা আপনি আপনার ক্লায়েন্ট কোডের মাধ্যমে কল করতে পারেন, দেখুন আপনি সার্ভারে আরও ফিচার যোগ করতে পারেন কিনা যাতে এটি আরও আকর্ষণীয় হয়।

### টাইপস্ক্রিপ্ট

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

### পাইথন

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

এই প্রকল্পটি দেখুন কীভাবে [প্রম্পট এবং রিসোর্স যোগ করবেন](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/EverythingServer/Program.cs)।

এছাড়াও, এই লিঙ্কটি দেখুন কীভাবে [প্রম্পট এবং রিসোর্স সক্রিয় করবেন](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol/Client/)।

### রাস্ট

[পূর্ববর্তী অধ্যায়ে](../../../../03-GettingStarted/01-first-server) আপনি শিখেছেন কীভাবে রাস্ট দিয়ে একটি সাধারণ MCP সার্ভার তৈরি করবেন। আপনি এটি চালিয়ে যেতে পারেন বা আরও রাস্ট-ভিত্তিক MCP সার্ভার উদাহরণ দেখতে এই লিঙ্কটি দেখুন: [MCP Server Examples](https://github.com/modelcontextprotocol/rust-sdk/tree/main/examples/servers)

## সমাধান

**সমাধান ফোল্ডার** সম্পূর্ণ, চালানোর জন্য প্রস্তুত ক্লায়েন্ট ইমপ্লিমেন্টেশন ধারণ করে যা এই টিউটোরিয়ালে আলোচনা করা সমস্ত ধারণা প্রদর্শন করে। প্রতিটি সমাধানে ক্লায়েন্ট এবং সার্ভার কোড রয়েছে যা পৃথক, স্বয়ংসম্পূর্ণ প্রকল্পে সংগঠিত।

### 📁 সমাধানের কাঠামো

সমাধান ডিরেক্টরি প্রোগ্রামিং ভাষা অনুযায়ী সংগঠিত:

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

### 🚀 প্রতিটি সমাধানে কী রয়েছে

প্রতিটি ভাষা-নির্দিষ্ট সমাধান প্রদান করে:

- **সম্পূর্ণ ক্লায়েন্ট ইমপ্লিমেন্টেশন** যা টিউটোরিয়ালের সমস্ত ফিচার ধারণ করে।
- **কাজের প্রকল্প কাঠামো** সঠিক ডিপেনডেন্সি এবং কনফিগারেশন সহ।
- **বিল্ড এবং রান স্ক্রিপ্ট** সহজ সেটআপ এবং এক্সিকিউশনের জন্য।
- **বিস্তারিত README** ভাষা-নির্দিষ্ট নির্দেশনা সহ।
- **এরর হ্যান্ডলিং** এবং ফলাফল প্রক্রিয়াকরণের উদাহরণ।

### 📖 সমাধান ব্যবহার করা

1. **আপনার পছন্দের ভাষার ফোল্ডারে যান**:

   ```bash
   cd solution/typescript/    # For TypeScript
   cd solution/java/          # For Java
   cd solution/python/        # For Python
   cd solution/dotnet/        # For .NET
   ```

2. **প্রতিটি ফোল্ডারের README নির্দেশনা অনুসরণ করুন**:
   - ডিপেনডেন্সি ইনস্টল করা
   - প্রকল্প তৈরি করা
   - ক্লায়েন্ট চালানো

3. **উদাহরণ আউটপুট** যা আপনি দেখতে পারেন:

   ```text
   Prompt: Please review this code: console.log("hello");
   Resource template: file
   Tool result: { content: [ { type: 'text', text: '9' } ] }
   ```

সম্পূর্ণ ডকুমেন্টেশন এবং ধাপে ধাপে নির্দেশনার জন্য দেখুন: **[📖 সমাধান ডকুমেন্টেশন](./solution/README.md)**

## 🎯 সম্পূর্ণ উদাহরণ

আমরা এই টিউটোরিয়ালে আলোচনা করা সমস্ত কার্যকারিতা প্রদর্শনকারী সম্পূর্ণ, কাজের ক্লায়েন্ট ইমপ্লিমেন্টেশন সরবরাহ করেছি। এই উদাহরণগুলো রেফারেন্স ইমপ্লিমেন্টেশন বা আপনার নিজস্ব প্রকল্পের জন্য শুরুর পয়েন্ট হিসেবে ব্যবহার করা যেতে পারে।

### উপলব্ধ সম্পূর্ণ উদাহরণ

| ভাষা | ফাইল | বিবরণ |
|----------|------|-------------|
| **জাভা** | [`client_example_java.java`](../../../../03-GettingStarted/02-client/client_example_java.java) | SSE ট্রান্সপোর্ট ব্যবহার করে সম্পূর্ণ জাভা ক্লায়েন্ট, ব্যাপক এরর হ্যান্ডলিং সহ |
| **C#** | [`client_example_csharp.cs`](../../../../03-GettingStarted/02-client/client_example_csharp.cs) | stdio ট্রান্সপোর্ট ব্যবহার করে সম্পূর্ণ C# ক্লায়েন্ট, স্বয়ংক্রিয় সার্ভার স্টার্টআপ সহ |
| **টাইপস্ক্রিপ্ট** | [`client_example_typescript.ts`](../../../../03-GettingStarted/02-client/client_example_typescript.ts) | সম্পূর্ণ টাইপস্ক্রিপ্ট ক্লায়েন্ট, সম্পূর্ণ MCP প্রোটোকল সমর্থন সহ |
| **পাইথন** | [`client_example_python.py`](../../../../03-GettingStarted/02-client/client_example_python.py) | সম্পূর্ণ পাইথন ক্লায়েন্ট, async/await প্যাটার্ন ব্যবহার করে |
| **রাস্ট** | [`client_example_rust.rs`](../../../../03-GettingStarted/02-client/client_example_rust.rs) | সম্পূর্ণ রাস্ট ক্লায়েন্ট, async অপারেশনের জন্য Tokio ব্যবহার করে |
প্রতিটি সম্পূর্ণ উদাহরণ অন্তর্ভুক্ত করে:

- ✅ **সংযোগ স্থাপন** এবং ত্রুটি পরিচালনা
- ✅ **সার্ভার আবিষ্কার** (যন্ত্র, সম্পদ, প্রম্পট যেখানে প্রযোজ্য)
- ✅ **ক্যালকুলেটর অপারেশন** (যোগ, বিয়োগ, গুণ, ভাগ, সাহায্য)
- ✅ **ফলাফল প্রক্রিয়াকরণ** এবং ফরম্যাটেড আউটপুট
- ✅ **সম্পূর্ণ ত্রুটি পরিচালনা**
- ✅ **পরিষ্কার, ডকুমেন্টেড কোড** ধাপে ধাপে মন্তব্য সহ

### সম্পূর্ণ উদাহরণ দিয়ে শুরু করা

1. **আপনার পছন্দের ভাষা নির্বাচন করুন** উপরের টেবিল থেকে
2. **সম্পূর্ণ উদাহরণ ফাইল পর্যালোচনা করুন** সম্পূর্ণ বাস্তবায়ন বুঝতে
3. **উদাহরণ চালান** [`complete_examples.md`](./complete_examples.md)-এ নির্দেশনা অনুসরণ করে
4. **আপনার নির্দিষ্ট ব্যবহারের জন্য উদাহরণ সংশোধন এবং প্রসারিত করুন**

এই উদাহরণগুলি চালানো এবং কাস্টমাইজ করার বিস্তারিত ডকুমেন্টেশনের জন্য দেখুন: **[📖 সম্পূর্ণ উদাহরণ ডকুমেন্টেশন](./complete_examples.md)**

### 💡 সমাধান বনাম সম্পূর্ণ উদাহরণ

| **সমাধান ফোল্ডার** | **সম্পূর্ণ উদাহরণ** |
|--------------------|--------------------- |
| বিল্ড ফাইল সহ পূর্ণ প্রকল্প কাঠামো | একক-ফাইল বাস্তবায়ন |
| নির্ভরশীলতা সহ চালানোর জন্য প্রস্তুত | ফোকাসড কোড উদাহরণ |
| প্রোডাকশন-সদৃশ সেটআপ | শিক্ষামূলক রেফারেন্স |
| ভাষা-নির্দিষ্ট টুলিং | ভাষা-ক্রস তুলনা |

উভয় পদ্ধতিই মূল্যবান - **সমাধান ফোল্ডার** ব্যবহার করুন সম্পূর্ণ প্রকল্পের জন্য এবং **সম্পূর্ণ উদাহরণ** শেখা এবং রেফারেন্সের জন্য।

## মূল বিষয়বস্তু

এই অধ্যায়ের মূল বিষয়বস্তু ক্লায়েন্ট সম্পর্কে নিম্নরূপ:

- সার্ভারে বৈশিষ্ট্য আবিষ্কার এবং আহ্বান করার জন্য ব্যবহার করা যেতে পারে।
- নিজে শুরু করার সময় সার্ভার শুরু করতে পারে (যেমন এই অধ্যায়ে) তবে ক্লায়েন্ট চলমান সার্ভারেও সংযোগ করতে পারে।
- সার্ভারের সক্ষমতা পরীক্ষা করার একটি চমৎকার উপায়, বিকল্প যেমন Inspector-এর পাশাপাশি যা আগের অধ্যায়ে বর্ণনা করা হয়েছে।

## অতিরিক্ত সম্পদ

- [MCP-এ ক্লায়েন্ট তৈরি করা](https://modelcontextprotocol.io/quickstart/client)

## নমুনা

- [জাভা ক্যালকুলেটর](../samples/java/calculator/README.md)
- [.Net ক্যালকুলেটর](../../../../03-GettingStarted/samples/csharp)
- [জাভাস্ক্রিপ্ট ক্যালকুলেটর](../samples/javascript/README.md)
- [টাইপস্ক্রিপ্ট ক্যালকুলেটর](../samples/typescript/README.md)
- [পাইথন ক্যালকুলেটর](../../../../03-GettingStarted/samples/python)
- [রাস্ট ক্যালকুলেটর](../../../../03-GettingStarted/samples/rust)

## পরবর্তী কী

- পরবর্তী: [একটি LLM দিয়ে ক্লায়েন্ট তৈরি করা](../03-llm-client/README.md)

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসম্ভব সঠিক অনুবাদের চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। নথিটির মূল ভাষায় থাকা সংস্করণটিকেই প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ ব্যবহার করার পরামর্শ দেওয়া হয়। এই অনুবাদ ব্যবহারের ফলে সৃষ্ট কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।