<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4d846ebb88fbb0f00549e2ff8cc3f746",
  "translation_date": "2025-10-06T14:05:45+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "pa"
}
-->
# LLM ਨਾਲ ਕਲਾਇੰਟ ਬਣਾਉਣਾ

ਅਜੇ ਤੱਕ, ਤੁਸੀਂ ਦੇਖਿਆ ਕਿ ਸਰਵਰ ਅਤੇ ਕਲਾਇੰਟ ਕਿਵੇਂ ਬਣਾਉਣਾ ਹੈ। ਕਲਾਇੰਟ ਨੇ ਸਰਵਰ ਨੂੰ ਸਪਸ਼ਟ ਤੌਰ 'ਤੇ ਕਾਲ ਕਰਕੇ ਇਸਦੇ ਟੂਲ, ਸਰੋਤ ਅਤੇ ਪ੍ਰੋੰਪਟ ਦੀ ਸੂਚੀ ਬਣਾਈ ਹੈ। ਹਾਲਾਂਕਿ, ਇਹ ਬਹੁਤ ਹੀ ਵਿਆਵਹਾਰਿਕ ਪਹੁੰਚ ਨਹੀਂ ਹੈ। ਤੁਹਾਡਾ ਯੂਜ਼ਰ ਏਜੰਟਿਕ ਯੁੱਗ ਵਿੱਚ ਰਹਿੰਦਾ ਹੈ ਅਤੇ ਪ੍ਰੋੰਪਟ ਵਰਤਣ ਅਤੇ LLM ਨਾਲ ਸੰਚਾਰ ਕਰਨ ਦੀ ਉਮੀਦ ਕਰਦਾ ਹੈ। ਤੁਹਾਡੇ ਯੂਜ਼ਰ ਲਈ, ਇਹ ਮਹੱਤਵਪੂਰਨ ਨਹੀਂ ਹੈ ਕਿ ਤੁਸੀਂ ਆਪਣੀਆਂ ਸਮਰੱਥਾਵਾਂ ਸਟੋਰ ਕਰਨ ਲਈ MCP ਵਰਤਦੇ ਹੋ ਜਾਂ ਨਹੀਂ, ਪਰ ਉਹ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਵਰਤ ਕੇ ਸੰਚਾਰ ਕਰਨ ਦੀ ਉਮੀਦ ਕਰਦੇ ਹਨ। ਤਾਂ ਅਸੀਂ ਇਸਨੂੰ ਕਿਵੇਂ ਹੱਲ ਕਰੀਏ? ਹੱਲ ਕਲਾਇੰਟ ਵਿੱਚ LLM ਸ਼ਾਮਲ ਕਰਨ ਬਾਰੇ ਹੈ।

## ਝਲਕ

ਇਸ ਪਾਠ ਵਿੱਚ ਅਸੀਂ ਤੁਹਾਡੇ ਕਲਾਇੰਟ ਵਿੱਚ LLM ਸ਼ਾਮਲ ਕਰਨ 'ਤੇ ਧਿਆਨ ਦਿੰਦੇ ਹਾਂ ਅਤੇ ਦਿਖਾਉਂਦੇ ਹਾਂ ਕਿ ਇਹ ਤੁਹਾਡੇ ਯੂਜ਼ਰ ਲਈ ਕਿਵੇਂ ਬਿਹਤਰ ਅਨੁਭਵ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ।

## ਸਿੱਖਣ ਦੇ ਉਦੇਸ਼

ਇਸ ਪਾਠ ਦੇ ਅੰਤ ਤੱਕ, ਤੁਸੀਂ ਇਹ ਕਰਨ ਦੇ ਯੋਗ ਹੋਵੋਗੇ:

- LLM ਨਾਲ ਕਲਾਇੰਟ ਬਣਾਉਣਾ।
- LLM ਦੀ ਵਰਤੋਂ ਕਰਕੇ MCP ਸਰਵਰ ਨਾਲ ਬਿਨਾਂ ਰੁਕਾਵਟ ਸੰਚਾਰ ਕਰਨਾ।
- ਕਲਾਇੰਟ ਪਾਸੇ ਬਿਹਤਰ ਅੰਤ ਯੂਜ਼ਰ ਅਨੁਭਵ ਪ੍ਰਦਾਨ ਕਰਨਾ।

## ਪਹੁੰਚ

ਆਓ ਅਸੀਂ ਸਮਝਣ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰੀਏ ਕਿ ਸਾਨੂੰ ਕਿਹੜੀ ਪਹੁੰਚ ਲੈਣੀ ਚਾਹੀਦੀ ਹੈ। LLM ਸ਼ਾਮਲ ਕਰਨਾ ਸਧਾਰਨ ਲੱਗਦਾ ਹੈ, ਪਰ ਕੀ ਅਸੀਂ ਵਾਸਤਵ ਵਿੱਚ ਇਹ ਕਰਦੇ ਹਾਂ?

ਇਹ ਹੈ ਕਿ ਕਲਾਇੰਟ ਸਰਵਰ ਨਾਲ ਕਿਵੇਂ ਸੰਚਾਰ ਕਰੇਗਾ:

1. ਸਰਵਰ ਨਾਲ ਕਨੈਕਸ਼ਨ ਸਥਾਪਤ ਕਰੋ।

1. ਸਮਰੱਥਾਵਾਂ, ਪ੍ਰੋੰਪਟ, ਸਰੋਤ ਅਤੇ ਟੂਲ ਦੀ ਸੂਚੀ ਬਣਾਓ ਅਤੇ ਉਨ੍ਹਾਂ ਦੀ ਸਕੀਮਾ ਸੇਵ ਕਰੋ।

1. ਇੱਕ LLM ਸ਼ਾਮਲ ਕਰੋ ਅਤੇ ਸੇਵ ਕੀਤੀਆਂ ਸਮਰੱਥਾਵਾਂ ਅਤੇ ਉਨ੍ਹਾਂ ਦੀ ਸਕੀਮਾ ਨੂੰ ਇੱਕ ਫਾਰਮੈਟ ਵਿੱਚ ਪਾਸ ਕਰੋ ਜੋ LLM ਨੂੰ ਸਮਝ ਆਉਂਦਾ ਹੈ।

1. ਯੂਜ਼ਰ ਪ੍ਰੋੰਪਟ ਨੂੰ LLM ਨੂੰ ਪਾਸ ਕਰਕੇ ਸੰਭਾਲੋ, ਨਾਲ ਹੀ ਉਹ ਟੂਲ ਜੋ ਕਲਾਇੰਟ ਦੁਆਰਾ ਸੂਚੀਬੱਧ ਕੀਤੇ ਗਏ ਹਨ।

ਵਧੀਆ, ਹੁਣ ਅਸੀਂ ਸਮਝ ਗਏ ਕਿ ਅਸੀਂ ਇਸਨੂੰ ਉੱਚ ਪੱਧਰ 'ਤੇ ਕਿਵੇਂ ਕਰ ਸਕਦੇ ਹਾਂ, ਆਓ ਹੇਠਾਂ ਦਿੱਤੇ ਅਭਿਆਸ ਵਿੱਚ ਇਸਨੂੰ ਅਜ਼ਮਾਈਏ।

## ਅਭਿਆਸ: LLM ਨਾਲ ਕਲਾਇੰਟ ਬਣਾਉਣਾ

ਇਸ ਅਭਿਆਸ ਵਿੱਚ, ਅਸੀਂ ਆਪਣੇ ਕਲਾਇੰਟ ਵਿੱਚ LLM ਸ਼ਾਮਲ ਕਰਨਾ ਸਿੱਖਾਂਗੇ।

### GitHub Personal Access Token ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਪ੍ਰਮਾਣਿਕਤਾ

GitHub ਟੋਕਨ ਬਣਾਉਣਾ ਇੱਕ ਸਧਾਰਨ ਪ੍ਰਕਿਰਿਆ ਹੈ। ਇਹ ਹੈ ਕਿ ਤੁਸੀਂ ਇਸਨੂੰ ਕਿਵੇਂ ਕਰ ਸਕਦੇ ਹੋ:

- GitHub ਸੈਟਿੰਗਜ਼ 'ਤੇ ਜਾਓ – ਆਪਣੇ ਪ੍ਰੋਫਾਈਲ ਤਸਵੀਰ 'ਤੇ ਕਲਿੱਕ ਕਰੋ ਅਤੇ ਸੈਟਿੰਗਜ਼ ਚੁਣੋ।
- Developer Settings 'ਤੇ ਜਾਓ – ਹੇਠਾਂ ਸਕ੍ਰੋਲ ਕਰੋ ਅਤੇ Developer Settings 'ਤੇ ਕਲਿੱਕ ਕਰੋ।
- Personal Access Tokens ਚੁਣੋ – Fine-grained tokens 'ਤੇ ਕਲਿੱਕ ਕਰੋ ਅਤੇ ਨਵਾਂ ਟੋਕਨ ਬਣਾਓ।
- ਆਪਣੇ ਟੋਕਨ ਨੂੰ ਕਨਫਿਗਰ ਕਰੋ – ਹਵਾਲੇ ਲਈ ਇੱਕ ਨੋਟ ਸ਼ਾਮਲ ਕਰੋ, ਮਿਆਦ ਦੀ ਮਿਤੀ ਸੈਟ ਕਰੋ, ਅਤੇ ਜ਼ਰੂਰੀ ਸਕੋਪ (ਅਧਿਕਾਰ) ਚੁਣੋ। ਇਸ ਮਾਮਲੇ ਵਿੱਚ ਯਕੀਨੀ ਬਣਾਓ ਕਿ Models ਅਧਿਕਾਰ ਸ਼ਾਮਲ ਕੀਤਾ ਗਿਆ ਹੈ।
- ਟੋਕਨ ਬਣਾਓ ਅਤੇ ਕਾਪੀ ਕਰੋ – Generate token 'ਤੇ ਕਲਿੱਕ ਕਰੋ, ਅਤੇ ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਇਸਨੂੰ ਤੁਰੰਤ ਕਾਪੀ ਕਰ ਲਓ, ਕਿਉਂਕਿ ਤੁਸੀਂ ਇਸਨੂੰ ਦੁਬਾਰਾ ਨਹੀਂ ਦੇਖ ਸਕਦੇ।

### -1- ਸਰਵਰ ਨਾਲ ਕਨੈਕਟ ਕਰੋ

ਆਓ ਪਹਿਲਾਂ ਆਪਣਾ ਕਲਾਇੰਟ ਬਣਾਈਏ:

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- ਲੋੜੀਂਦੇ ਲਾਇਬ੍ਰੇਰੀਜ਼ ਇੰਪੋਰਟ ਕੀਤੇ ਹਨ।
- ਦੋ ਮੈਂਬਰਾਂ `client` ਅਤੇ `openai` ਨਾਲ ਇੱਕ ਕਲਾਸ ਬਣਾਈ ਹੈ ਜੋ ਸਾਨੂੰ ਕਲਾਇੰਟ ਨੂੰ ਮੈਨੇਜ ਕਰਨ ਅਤੇ LLM ਨਾਲ ਸੰਚਾਰ ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰੇਗਾ।
- GitHub Models ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ `baseUrl` ਨੂੰ inference API ਵੱਲ ਪੋਇੰਟ ਕਰਕੇ ਆਪਣੇ LLM ਇੰਸਟੈਂਸ ਨੂੰ ਕਨਫਿਗਰ ਕੀਤਾ ਹੈ।

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- MCP ਲਈ ਲੋੜੀਂਦੇ ਲਾਇਬ੍ਰੇਰੀਜ਼ ਇੰਪੋਰਟ ਕੀਤੇ ਹਨ।
- ਇੱਕ ਕਲਾਇੰਟ ਬਣਾਇਆ ਹੈ।

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

ਸਭ ਤੋਂ ਪਹਿਲਾਂ, ਤੁਹਾਨੂੰ ਆਪਣੇ `pom.xml` ਫਾਈਲ ਵਿੱਚ LangChain4j dependencies ਸ਼ਾਮਲ ਕਰਨ ਦੀ ਲੋੜ ਹੋਵੇਗੀ। MCP ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਅਤੇ GitHub Models ਸਪੋਰਟ ਨੂੰ ਯਕੀਨੀ ਬਣਾਉਣ ਲਈ ਇਹ dependencies ਸ਼ਾਮਲ ਕਰੋ:

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

ਫਿਰ ਆਪਣੀ Java ਕਲਾਇੰਟ ਕਲਾਸ ਬਣਾਓ:

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- **LangChain4j dependencies ਸ਼ਾਮਲ ਕੀਤੇ**: MCP ਇੰਟੀਗ੍ਰੇਸ਼ਨ, OpenAI ਅਧਿਕਾਰਤ ਕਲਾਇੰਟ, ਅਤੇ GitHub Models ਸਪੋਰਟ ਲਈ ਲੋੜੀਂਦੇ।
- **LangChain4j ਲਾਇਬ੍ਰੇਰੀਜ਼ ਇੰਪੋਰਟ ਕੀਤੀਆਂ**: MCP ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਅਤੇ OpenAI ਚੈਟ ਮਾਡਲ ਫੰਕਸ਼ਨਲਿਟੀ ਲਈ।
- **`ChatLanguageModel` ਬਣਾਇਆ**: GitHub Models ਨਾਲ GitHub ਟੋਕਨ ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਕਨਫਿਗਰ ਕੀਤਾ।
- **HTTP ਟ੍ਰਾਂਸਪੋਰਟ ਸੈਟ ਕੀਤਾ**: Server-Sent Events (SSE) ਦੀ ਵਰਤੋਂ ਕਰਕੇ MCP ਸਰਵਰ ਨਾਲ ਕਨੈਕਟ ਕਰਨ ਲਈ।
- **MCP ਕਲਾਇੰਟ ਬਣਾਇਆ**: ਜੋ ਸਰਵਰ ਨਾਲ ਸੰਚਾਰ ਨੂੰ ਸੰਭਾਲੇਗਾ।
- **LangChain4j ਦੀ ਬਣਾਈ MCP ਸਪੋਰਟ ਦੀ ਵਰਤੋਂ ਕੀਤੀ**: ਜੋ LLMs ਅਤੇ MCP ਸਰਵਰਾਂ ਦੇ ਵਿਚਕਾਰ ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਨੂੰ ਸਧਾਰਨ ਬਣਾਉਂਦਾ ਹੈ।

#### Rust

ਇਹ ਉਦਾਹਰਣ ਮੰਨਦਾ ਹੈ ਕਿ ਤੁਹਾਡੇ ਕੋਲ Rust ਅਧਾਰਿਤ MCP ਸਰਵਰ ਚੱਲ ਰਿਹਾ ਹੈ। ਜੇ ਤੁਹਾਡੇ ਕੋਲ ਨਹੀਂ ਹੈ, ਤਾਂ [01-first-server](../01-first-server/README.md) ਪਾਠ ਵਿੱਚ ਵਾਪਸ ਜਾਓ ਅਤੇ ਸਰਵਰ ਬਣਾਓ।

ਜਦੋਂ ਤੁਹਾਡੇ ਕੋਲ Rust MCP ਸਰਵਰ ਹੋਵੇ, ਟਰਮੀਨਲ ਖੋਲ੍ਹੋ ਅਤੇ ਸਰਵਰ ਵਾਲੇ ਡਾਇਰੈਕਟਰੀ ਵਿੱਚ ਜਾਓ। ਫਿਰ ਨਵਾਂ LLM ਕਲਾਇੰਟ ਪ੍ਰੋਜੈਕਟ ਬਣਾਉਣ ਲਈ ਹੇਠਾਂ ਦਿੱਤੇ ਕਮਾਂਡ ਚਲਾਓ:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

ਆਪਣੇ `Cargo.toml` ਫਾਈਲ ਵਿੱਚ ਹੇਠਾਂ ਦਿੱਤੀਆਂ dependencies ਸ਼ਾਮਲ ਕਰੋ:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Rust ਲਈ OpenAI ਦੀ ਅਧਿਕਾਰਤ ਲਾਇਬ੍ਰੇਰੀ ਨਹੀਂ ਹੈ, ਹਾਲਾਂਕਿ `async-openai` crate ਇੱਕ [community maintained library](https://platform.openai.com/docs/libraries/rust#rust) ਹੈ ਜੋ ਆਮ ਤੌਰ 'ਤੇ ਵਰਤੀ ਜਾਂਦੀ ਹੈ।

`src/main.rs` ਫਾਈਲ ਖੋਲ੍ਹੋ ਅਤੇ ਇਸਦੀ ਸਮੱਗਰੀ ਨੂੰ ਹੇਠਾਂ ਦਿੱਤੇ ਕੋਡ ਨਾਲ ਬਦਲੋ:

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

ਇਹ ਕੋਡ ਇੱਕ ਬੁਨਿਆਦੀ Rust ਐਪਲੀਕੇਸ਼ਨ ਸੈਟ ਕਰਦਾ ਹੈ ਜੋ MCP ਸਰਵਰ ਅਤੇ GitHub Models ਨਾਲ LLM ਇੰਟਰੈਕਸ਼ਨ ਲਈ ਕਨੈਕਟ ਕਰੇਗਾ।

> [!IMPORTANT]
> ਐਪਲੀਕੇਸ਼ਨ ਚਲਾਉਣ ਤੋਂ ਪਹਿਲਾਂ `OPENAI_API_KEY` ਵਾਤਾਵਰਣ ਵੈਰੀਏਬਲ ਨੂੰ ਆਪਣੇ GitHub ਟੋਕਨ ਨਾਲ ਸੈਟ ਕਰੋ।

ਵਧੀਆ, ਅਗਲੇ ਕਦਮ ਵਿੱਚ, ਆਓ ਸਰਵਰ ਦੀ ਸਮਰੱਥਾਵਾਂ ਦੀ ਸੂਚੀ ਬਣਾਈਏ।

### -2- ਸਰਵਰ ਦੀ ਸਮਰੱਥਾਵਾਂ ਦੀ ਸੂਚੀ ਬਣਾਉਣਾ

ਹੁਣ ਅਸੀਂ ਸਰਵਰ ਨਾਲ ਕਨੈਕਟ ਕਰਾਂਗੇ ਅਤੇ ਇਸ ਦੀ ਸਮਰੱਥਾਵਾਂ ਦੀ ਬੇਨਤੀ ਕਰਾਂਗੇ:

#### TypeScript

ਉਸੇ ਕਲਾਸ ਵਿੱਚ ਹੇਠਾਂ ਦਿੱਤੇ ਮੈਥਡ ਸ਼ਾਮਲ ਕਰੋ:

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- ਸਰਵਰ ਨਾਲ ਕਨੈਕਟ ਕਰਨ ਲਈ ਕੋਡ ਸ਼ਾਮਲ ਕੀਤਾ, `connectToServer`।
- ਇੱਕ `run` ਮੈਥਡ ਬਣਾਇਆ ਜੋ ਸਾਡੇ ਐਪ ਫਲੋ ਨੂੰ ਸੰਭਾਲਣ ਲਈ ਜ਼ਿੰਮੇਵਾਰ ਹੈ। ਹੁਣ ਤੱਕ ਇਹ ਸਿਰਫ ਟੂਲ ਦੀ ਸੂਚੀ ਬਣਾਉਂਦਾ ਹੈ ਪਰ ਅਸੀਂ ਇਸ ਵਿੱਚ ਜਲਦੀ ਹੋਰ ਸ਼ਾਮਲ ਕਰਾਂਗੇ।

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

ਇਹ ਹੈ ਜੋ ਅਸੀਂ ਸ਼ਾਮਲ ਕੀਤਾ:

- ਸਰੋਤ ਅਤੇ ਟੂਲ ਦੀ ਸੂਚੀ ਬਣਾਈ ਅਤੇ ਪ੍ਰਿੰਟ ਕੀਤੇ। ਟੂਲ ਲਈ ਅਸੀਂ `inputSchema` ਦੀ ਵੀ ਸੂਚੀ ਬਣਾਈ ਜੋ ਅਸੀਂ ਬਾਅਦ ਵਿੱਚ ਵਰਤਦੇ ਹਾਂ।

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- MCP ਸਰਵਰ 'ਤੇ ਉਪਲਬਧ ਟੂਲ ਦੀ ਸੂਚੀ ਬਣਾਈ।
- ਹਰ ਟੂਲ ਲਈ, ਨਾਮ, ਵੇਰਵਾ ਅਤੇ ਇਸਦੀ ਸਕੀਮਾ ਦੀ ਸੂਚੀ ਬਣਾਈ। ਇਹ ਅਸੀਂ ਜਲਦੀ ਟੂਲ ਨੂੰ ਕਾਲ ਕਰਨ ਲਈ ਵਰਤਾਂਗੇ।

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- ਇੱਕ `McpToolProvider` ਬਣਾਇਆ ਜੋ MCP ਸਰਵਰ ਤੋਂ ਸਾਰੇ ਟੂਲ ਨੂੰ ਆਟੋਮੈਟਿਕ ਤੌਰ 'ਤੇ ਖੋਜਦਾ ਅਤੇ ਰਜਿਸਟਰ ਕਰਦਾ ਹੈ।
- ਟੂਲ ਪ੍ਰੋਵਾਈਡਰ MCP ਟੂਲ ਸਕੀਮਾਂ ਅਤੇ LangChain4j ਦੇ ਟੂਲ ਫਾਰਮੈਟ ਦੇ ਵਿਚਕਾਰ ਕਨਵਰਜ਼ਨ ਨੂੰ ਅੰਦਰੂਨੀ ਤੌਰ 'ਤੇ ਸੰਭਾਲਦਾ ਹੈ।
- ਇਹ ਪਹੁੰਚ ਮੈਨੂਅਲ ਟੂਲ ਸੂਚੀ ਅਤੇ ਕਨਵਰਜ਼ਨ ਪ੍ਰਕਿਰਿਆ ਨੂੰ ਅਬਸਟਰੈਕਟ ਕਰਦੀ ਹੈ।

#### Rust

MCP ਸਰਵਰ ਤੋਂ ਟੂਲ ਪ੍ਰਾਪਤ ਕਰਨਾ `list_tools` ਮੈਥਡ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। ਆਪਣੇ `main` ਫੰਕਸ਼ਨ ਵਿੱਚ, MCP ਕਲਾਇੰਟ ਸੈਟ ਕਰਨ ਤੋਂ ਬਾਅਦ ਹੇਠਾਂ ਦਿੱਤਾ ਕੋਡ ਸ਼ਾਮਲ ਕਰੋ:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- ਸਰਵਰ ਦੀ ਸਮਰੱਥਾਵਾਂ ਨੂੰ LLM ਟੂਲ ਵਿੱਚ ਕਨਵਰਟ ਕਰੋ

ਸਰਵਰ ਦੀ ਸਮਰੱਥਾਵਾਂ ਦੀ ਸੂਚੀ ਬਣਾਉਣ ਤੋਂ ਬਾਅਦ ਅਗਲਾ ਕਦਮ ਇਹਨਾਂ ਨੂੰ ਇੱਕ ਫਾਰਮੈਟ ਵਿੱਚ ਕਨਵਰਟ ਕਰਨਾ ਹੈ ਜੋ LLM ਨੂੰ ਸਮਝ ਆਉਂਦਾ ਹੈ। ਜਦੋਂ ਅਸੀਂ ਇਹ ਕਰ ਲੈਂਦੇ ਹਾਂ, ਅਸੀਂ ਇਹ ਸਮਰੱਥਾਵਾਂ LLM ਨੂੰ ਟੂਲ ਵਜੋਂ ਪ੍ਰਦਾਨ ਕਰ ਸਕਦੇ ਹਾਂ।

#### TypeScript

1. MCP Server ਤੋਂ ਪ੍ਰਾਪਤ ਜਵਾਬ ਨੂੰ LLM ਲਈ ਵਰਤਣਯੋਗ ਟੂਲ ਫਾਰਮੈਟ ਵਿੱਚ ਕਨਵਰਟ ਕਰਨ ਲਈ ਹੇਠਾਂ ਦਿੱਤਾ ਕੋਡ ਸ਼ਾਮਲ ਕਰੋ:

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

    ਉਪਰੋਕਤ ਕੋਡ MCP Server ਤੋਂ ਪ੍ਰਾਪਤ ਜਵਾਬ ਨੂੰ LLM ਲਈ ਵਰਤਣਯੋਗ ਟੂਲ ਡਿਫਿਨੀਸ਼ਨ ਫਾਰਮੈਟ ਵਿੱਚ ਕਨਵਰਟ ਕਰਦਾ ਹੈ।

1. ਆਓ `run` ਮੈਥਡ ਨੂੰ ਅਪਡੇਟ ਕਰੀਏ:

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

    ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ, ਅਸੀਂ `run` ਮੈਥਡ ਨੂੰ ਅਪਡੇਟ ਕੀਤਾ ਹੈ ਜੋ ਨਤੀਜੇ ਦੇ ਨਾਲ ਮੈਪ ਕਰਦਾ ਹੈ ਅਤੇ ਹਰ ਐਂਟਰੀ ਲਈ `openAiToolAdapter` ਨੂੰ ਕਾਲ ਕਰਦਾ ਹੈ।

#### Python

1. ਪਹਿਲਾਂ, ਹੇਠਾਂ ਦਿੱਤਾ ਕਨਵਰਟਰ ਫੰਕਸ਼ਨ ਬਣਾਓ:

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

    ਉਪਰੋਕਤ ਫੰਕਸ਼ਨ `convert_to_llm_tools` ਵਿੱਚ ਅਸੀਂ MCP ਟੂਲ ਜਵਾਬ ਨੂੰ ਇੱਕ ਫਾਰਮੈਟ ਵਿੱਚ ਕਨਵਰਟ ਕਰਦੇ ਹਾਂ ਜੋ LLM ਨੂੰ ਸਮਝ ਆਉਂਦਾ ਹੈ।

1. ਅਗਲੇ ਕਦਮ ਵਿੱਚ, ਆਪਣੇ ਕਲਾਇੰਟ ਕੋਡ ਨੂੰ ਇਸ ਫੰਕਸ਼ਨ ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਅਪਡੇਟ ਕਰੋ:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    ਇੱਥੇ, ਅਸੀਂ MCP ਟੂਲ ਜਵਾਬ ਨੂੰ ਬਾਅਦ ਵਿੱਚ LLM ਨੂੰ ਫੀਡ ਕਰਨ ਲਈ ਕਨਵਰਟ ਕਰਨ ਲਈ `convert_to_llm_tool` ਨੂੰ ਕਾਲ ਕਰਦੇ ਹਾਂ।

#### .NET

1. ਆਓ MCP ਟੂਲ ਜਵਾਬ ਨੂੰ LLM ਲਈ ਵਰਤਣਯੋਗ ਫਾਰਮੈਟ ਵਿੱਚ ਕਨਵਰਟ ਕਰਨ ਲਈ ਕੋਡ ਸ਼ਾਮਲ ਕਰੀਏ:

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- ਇੱਕ ਫੰਕਸ਼ਨ `ConvertFrom` ਬਣਾਇਆ ਜੋ ਨਾਮ, ਵੇਰਵਾ ਅਤੇ ਇੰਪੁਟ ਸਕੀਮਾ ਲੈਂਦਾ ਹੈ।
- FunctionDefinition ਬਣਾਉਣ ਦੀ ਵਿਵਸਥਾ ਨੂੰ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤਾ ਜੋ ChatCompletionsDefinition ਨੂੰ ਪਾਸ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। ਇਹ LLM ਨੂੰ ਸਮਝ ਆਉਂਦਾ ਹੈ।

1. ਆਓ ਕੁਝ ਮੌਜੂਦਾ ਕੋਡ ਨੂੰ ਅਪਡੇਟ ਕਰਨ ਦੇ ਤਰੀਕੇ ਦੇਖੀਏ:

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

ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

- ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਸੰਚਾਰ ਲਈ ਇੱਕ ਸਧਾਰਨ `Bot` ਇੰਟਰਫੇਸ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤਾ।
- LangChain4j ਦੇ `AiServices` ਦੀ ਵਰਤੋਂ ਕੀਤੀ ਜੋ LLM ਨੂੰ MCP ਟੂਲ ਪ੍ਰੋਵਾਈਡਰ ਨਾਲ ਆਟੋਮੈਟਿਕ ਤੌਰ 'ਤੇ ਬਾਈਂਡ ਕਰਦਾ ਹੈ।
- ਫਰੇਮਵਰਕ ਆਟੋਮੈਟਿਕ ਤੌਰ 'ਤੇ ਟੂਲ ਸਕੀਮਾ ਕਨਵਰਜ਼ਨ ਅਤੇ ਫੰਕਸ਼ਨ ਕਾਲਿੰਗ ਨੂੰ ਸੰਭਾਲਦਾ ਹੈ।
- ਇਹ ਪਹੁੰਚ ਮੈਨੂਅਲ ਟੂਲ ਕਨਵਰਜ਼ਨ ਨੂੰ ਹਟਾਉਂਦੀ ਹੈ - LangChain4j MCP ਟੂਲ ਨੂੰ LLM-ਕੰਪੈਟਿਬਲ ਫਾਰਮੈਟ ਵਿੱਚ ਕਨਵਰਟ ਕਰਨ ਦੀ ਸਾਰੀ ਜਟਿਲਤਾ ਨੂੰ ਸੰਭਾਲਦਾ ਹੈ।

#### Rust

MCP ਟੂਲ ਜਵਾਬ ਨੂੰ ਇੱਕ ਫਾਰਮੈਟ ਵਿੱਚ ਕਨਵਰਟ ਕਰਨ ਲਈ ਜੋ LLM ਨੂੰ ਸਮਝ ਆਉਂਦਾ ਹੈ, ਅਸੀਂ ਇੱਕ ਹੇਲਪਰ ਫੰਕਸ਼ਨ ਸ਼ਾਮਲ ਕਰਾਂਗੇ ਜੋ ਟੂਲ ਸੂਚੀਬੱਧ ਕਰਨ ਦੀ ਵਿਵਸਥਾ ਕਰਦਾ ਹੈ। ਆਪਣੇ `main.rs` ਫਾਈਲ ਵਿੱਚ ਹੇਠਾਂ ਦਿੱਤਾ ਕੋਡ ਸ਼ਾਮਲ ਕਰੋ:

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

ਵਧੀਆ, ਅਸੀਂ ਹੁਣ ਕਿਸੇ ਵੀ ਯੂਜ਼ਰ ਦੀ ਬੇਨਤੀ ਨੂੰ ਸੰਭਾਲਣ ਲਈ ਸੈਟ ਹੋ ਗਏ ਹਾਂ, ਤਾਂ ਆਓ ਅਗਲੇ ਕਦਮ ਵਿੱਚ ਇਸਨੂੰ ਹੱਲ ਕਰੀਏ।

### -4- ਯੂਜ਼ਰ ਪ੍ਰੋੰਪਟ ਬੇਨਤੀ ਨੂੰ ਸੰਭਾਲੋ

ਇਸ ਕੋਡ ਦੇ ਹਿੱਸੇ ਵਿੱਚ, ਅਸੀਂ ਯੂਜ਼ਰ ਦੀਆਂ ਬੇਨਤੀਆਂ ਨੂੰ ਸੰਭਾਲਾਂਗੇ।

#### TypeScript

1. ਇੱਕ ਮੈਥਡ ਸ਼ਾਮਲ ਕਰੋ ਜੋ ਸਾਡੇ LLM ਨੂੰ ਕਾਲ ਕਰਨ ਲਈ ਵਰਤਿਆ ਜਾਵੇਗਾ:

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

    ਉਪਰੋਕਤ ਕੋਡ ਵਿੱਚ ਅਸੀਂ:

    - ਇੱਕ ਮੈਥਡ `callTools` ਸ਼ਾਮਲ ਕੀਤਾ।
    - ਮੈਥਡ LLM ਜਵਾਬ ਲੈਂਦਾ ਹੈ ਅਤੇ ਜਾਂਚਦਾ ਹੈ ਕਿ ਕੀ ਕੋਈ ਟੂਲ ਕਾਲ ਕੀਤੇ ਗਏ ਹਨ:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - ਜੇ LLM ਸੰਕੇਤ ਕਰਦਾ ਹੈ ਤਾਂ ਟੂਲ ਨੂੰ ਕਾਲ ਕਰਦਾ ਹੈ:

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

1. `run` ਮੈਥਡ ਨੂੰ ਅਪਡੇਟ ਕਰੋ:

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

ਵਧੀਆ, ਆਓ ਪੂਰੇ ਕੋਡ ਨੂੰ ਸੂਚੀਬੱਧ ਕਰੀਏ:

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

1. ਆਓ ਕੁਝ ਇੰਪੋਰਟ ਸ਼ਾਮਲ ਕਰੀਏ ਜੋ LLM ਨੂੰ ਕਾਲ ਕਰਨ ਲਈ ਲੋ
LLM ਦੇ ਜਵਾਬ ਵਿੱਚ `choices` ਦੀ ਇੱਕ ਐਰੇ ਸ਼ਾਮਲ ਹੋਵੇਗੀ। ਸਾਨੂੰ ਨਤੀਜੇ ਨੂੰ ਪ੍ਰੋਸੈਸ ਕਰਨਾ ਪਵੇਗਾ ਤਾਂ ਜੋ ਦੇਖਿਆ ਜਾ ਸਕੇ ਕਿ ਕੋਈ `tool_calls` ਮੌਜੂਦ ਹਨ ਜਾਂ ਨਹੀਂ। ਇਹ ਸਾਨੂੰ ਦੱਸਦਾ ਹੈ ਕਿ LLM ਇੱਕ ਖਾਸ ਟੂਲ ਨੂੰ ਦਲੀਲਾਂ ਨਾਲ ਕਾਲ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰ ਰਿਹਾ ਹੈ। ਆਪਣੇ `main.rs` ਫਾਈਲ ਦੇ ਅੰਤ ਵਿੱਚ ਹੇਠਾਂ ਦਿੱਤਾ ਕੋਡ ਸ਼ਾਮਲ ਕਰੋ ਤਾਂ ਜੋ LLM ਦੇ ਜਵਾਬ ਨੂੰ ਸੰਭਾਲਣ ਲਈ ਇੱਕ ਫੰਕਸ਼ਨ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤਾ ਜਾ ਸਕੇ:

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

ਜੇ `tool_calls` ਮੌਜੂਦ ਹਨ, ਤਾਂ ਇਹ ਟੂਲ ਦੀ ਜਾਣਕਾਰੀ ਨਿਕਾਲਦਾ ਹੈ, ਟੂਲ ਬੇਨਤੀ ਨਾਲ MCP ਸਰਵਰ ਨੂੰ ਕਾਲ ਕਰਦਾ ਹੈ, ਅਤੇ ਨਤੀਜਿਆਂ ਨੂੰ ਗੱਲਬਾਤ ਦੇ ਸੁਨੇਹਿਆਂ ਵਿੱਚ ਸ਼ਾਮਲ ਕਰਦਾ ਹੈ। ਇਹ ਫਿਰ LLM ਨਾਲ ਗੱਲਬਾਤ ਜਾਰੀ ਰੱਖਦਾ ਹੈ ਅਤੇ ਸੁਨੇਹੇ ਸਹਾਇਕ ਦੇ ਜਵਾਬ ਅਤੇ ਟੂਲ ਕਾਲ ਨਤੀਜਿਆਂ ਨਾਲ ਅਪਡੇਟ ਕੀਤੇ ਜਾਂਦੇ ਹਨ।

MCP ਕਾਲਾਂ ਲਈ LLM ਵੱਲੋਂ ਵਾਪਸ ਕੀਤੇ ਟੂਲ ਕਾਲ ਜਾਣਕਾਰੀ ਨੂੰ ਨਿਕਾਲਣ ਲਈ, ਸਾਨੂੰ ਇੱਕ ਹੋਰ ਹੇਲਪਰ ਫੰਕਸ਼ਨ ਸ਼ਾਮਲ ਕਰਨਾ ਪਵੇਗਾ ਜੋ ਕਾਲ ਕਰਨ ਲਈ ਲੋੜੀਂਦਾ ਸਭ ਕੁਝ ਨਿਕਾਲੇ। ਆਪਣੇ `main.rs` ਫਾਈਲ ਦੇ ਅੰਤ ਵਿੱਚ ਹੇਠਾਂ ਦਿੱਤਾ ਕੋਡ ਸ਼ਾਮਲ ਕਰੋ:

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

ਸਾਰੇ ਹਿੱਸੇ ਸਥਾਪਿਤ ਹੋਣ ਦੇ ਨਾਲ, ਹੁਣ ਅਸੀਂ ਸ਼ੁਰੂਆਤੀ ਯੂਜ਼ਰ ਪ੍ਰਾਂਪਟ ਨੂੰ ਸੰਭਾਲ ਸਕਦੇ ਹਾਂ ਅਤੇ LLM ਨੂੰ ਕਾਲ ਕਰ ਸਕਦੇ ਹਾਂ। ਆਪਣੇ `main` ਫੰਕਸ਼ਨ ਨੂੰ ਹੇਠਾਂ ਦਿੱਤੇ ਕੋਡ ਨਾਲ ਅਪਡੇਟ ਕਰੋ:

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

ਇਹ LLM ਨੂੰ ਸ਼ੁਰੂਆਤੀ ਯੂਜ਼ਰ ਪ੍ਰਾਂਪਟ ਦੇ ਨਾਲ ਪੁੱਛੇਗਾ ਕਿ ਦੋ ਨੰਬਰਾਂ ਦਾ ਜੋੜ ਕੀ ਹੈ, ਅਤੇ ਜਵਾਬ ਨੂੰ ਪ੍ਰੋਸੈਸ ਕਰੇਗਾ ਤਾਂ ਜੋ ਟੂਲ ਕਾਲਾਂ ਨੂੰ ਗਤੀਸ਼ੀਲ ਤਰੀਕੇ ਨਾਲ ਸੰਭਾਲਿਆ ਜਾ ਸਕੇ।

ਵਧੀਆ, ਤੁਸੀਂ ਕਰ ਲਿਆ!

## ਅਸਾਈਨਮੈਂਟ

ਅਭਿਆਸ ਵਿੱਚ ਦਿੱਤੇ ਕੋਡ ਨੂੰ ਲਓ ਅਤੇ ਸਰਵਰ ਵਿੱਚ ਕੁਝ ਹੋਰ ਟੂਲ ਸ਼ਾਮਲ ਕਰੋ। ਫਿਰ ਇੱਕ LLM ਦੇ ਨਾਲ ਇੱਕ ਕਲਾਇੰਟ ਬਣਾਓ, ਜਿਵੇਂ ਕਿ ਅਭਿਆਸ ਵਿੱਚ, ਅਤੇ ਵੱਖ-ਵੱਖ ਪ੍ਰਾਂਪਟਾਂ ਨਾਲ ਇਸਨੂੰ ਟੈਸਟ ਕਰੋ ਤਾਂ ਕਿ ਤੁਹਾਡੇ ਸਰਵਰ ਟੂਲਾਂ ਨੂੰ ਗਤੀਸ਼ੀਲ ਤਰੀਕੇ ਨਾਲ ਕਾਲ ਕੀਤਾ ਜਾ ਸਕੇ। ਇਸ ਤਰੀਕੇ ਨਾਲ ਕਲਾਇੰਟ ਬਣਾਉਣ ਦਾ ਮਤਲਬ ਹੈ ਕਿ ਅੰਤਮ ਯੂਜ਼ਰ ਨੂੰ ਬਹੁਤ ਵਧੀਆ ਅਨੁਭਵ ਮਿਲੇਗਾ ਕਿਉਂਕਿ ਉਹ ਪ੍ਰਾਂਪਟਾਂ ਦੀ ਵਰਤੋਂ ਕਰਨ ਦੇ ਯੋਗ ਹੋਣਗੇ, ਸਹੀ ਕਲਾਇੰਟ ਕਮਾਂਡਾਂ ਦੀ ਬਜਾਏ, ਅਤੇ ਕਿਸੇ MCP ਸਰਵਰ ਦੇ ਕਾਲ ਹੋਣ ਤੋਂ ਬੇਖ਼ਬਰ ਰਹਿਣਗੇ।

## ਹੱਲ

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## ਮੁੱਖ ਸਿੱਖਿਆ

- ਆਪਣੇ ਕਲਾਇੰਟ ਵਿੱਚ LLM ਸ਼ਾਮਲ ਕਰਨਾ ਯੂਜ਼ਰਾਂ ਨੂੰ MCP ਸਰਵਰਾਂ ਨਾਲ ਸੰਚਾਰ ਕਰਨ ਦਾ ਇੱਕ ਵਧੀਆ ਤਰੀਕਾ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ।
- ਤੁਹਾਨੂੰ MCP ਸਰਵਰ ਦੇ ਜਵਾਬ ਨੂੰ ਕੁਝ ਇਸ ਤਰ੍ਹਾਂ ਰੂਪਾਂਤਰਿਤ ਕਰਨ ਦੀ ਲੋੜ ਹੈ ਜੋ LLM ਨੂੰ ਸਮਝ ਆ ਸਕੇ।

## ਨਮੂਨੇ

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## ਵਾਧੂ ਸਰੋਤ

## ਅਗਲਾ ਕੀ ਹੈ

- ਅਗਲਾ: [Visual Studio Code ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਸਰਵਰ ਨੂੰ ਕਨਜ਼ਿਊਮ ਕਰਨਾ](../04-vscode/README.md)

---

**ਅਸਵੀਕਰਤੀ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਕੀਤਾ ਗਿਆ ਹੈ। ਹਾਲਾਂਕਿ ਅਸੀਂ ਸਹੀ ਹੋਣ ਦਾ ਯਤਨ ਕਰਦੇ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਦਿਓ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸੁਚੀਤਤਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਇਸ ਦਸਤਾਵੇਜ਼ ਦੇ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਲਿਖੇ ਗ੍ਰੰਥ ਨੂੰ ਅਧਿਕਾਰਤ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੇ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆ ਲਈ ਅਸੀਂ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।