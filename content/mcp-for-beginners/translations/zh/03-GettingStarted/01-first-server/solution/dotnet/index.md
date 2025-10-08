<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "92af35e8c34923031f3d228dffad9ebb",
  "translation_date": "2025-09-03T15:58:49+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/dotnet/README.md",
  "language_code": "zh"
}
-->
# 运行此示例

## -1- 安装依赖项

```bash
dotnet restore
```

## -3- 运行示例

```bash
dotnet run
```

## -4- 测试示例

在一个终端中运行服务器后，打开另一个终端并运行以下命令：

```bash
npx @modelcontextprotocol/inspector dotnet run
```

这将启动一个带有可视化界面的网络服务器，允许您测试该示例。

服务器连接后：

- 尝试列出工具并运行 `add`，参数为 2 和 4，结果应该显示为 6。
- 进入资源和资源模板，调用 "greeting"，输入一个名字，您应该会看到包含您提供名字的问候语。

### 在 CLI 模式下测试

您可以通过运行以下命令直接以 CLI 模式启动：

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/list
```

这将列出服务器中所有可用的工具。您应该会看到以下输出：

```text
{
  "tools": [
    {
      "name": "Add",
      "description": "Adds two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer"
          },
          "b": {
            "type": "integer"
          }
        },
        "title": "Add",
        "description": "Adds two numbers",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

要调用某个工具，请输入：

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/call --tool-name Add --tool-arg a=1 --tool-arg b=2
```

您应该会看到以下输出：

```text
{
  "content": [
    {
      "type": "text",
      "text": "Sum 3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> 通常在 CLI 模式下运行检查器比在浏览器中快得多。
> 在 [这里](https://github.com/modelcontextprotocol/inspector) 阅读更多关于检查器的信息。

---

**免责声明**：  
本文档使用AI翻译服务[Co-op Translator](https://github.com/Azure/co-op-translator)进行翻译。尽管我们努力确保翻译的准确性，但请注意，自动翻译可能包含错误或不准确之处。原始语言的文档应被视为权威来源。对于关键信息，建议使用专业人工翻译。我们不对因使用此翻译而产生的任何误解或误读承担责任。