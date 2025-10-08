<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c40c54fa74ded9c223bc0ebfc8a2de7c",
  "translation_date": "2025-07-13T19:02:19+00:00",
  "source_file": "03-GettingStarted/03-llm-client/solution/dotnet/README.md",
  "language_code": "hi"
}
-->
# इस सैंपल को चलाएं

> [!NOTE]
> यह सैंपल मानता है कि आप GitHub Codespaces का उपयोग कर रहे हैं। यदि आप इसे लोकल रूप से चलाना चाहते हैं, तो आपको GitHub पर एक personal access token (PAT) सेटअप करना होगा।
>
> ```bash
> # zsh/bash
> export GITHUB_TOKEN="{{YOUR_GITHUB_PAT}}"
> ```
>
> ```powershell
> # PowerShell
> $env:GITHUB_TOKEN = "{{YOUR_GITHUB_PAT}}"
> ```

## लाइब्रेरी इंस्टॉल करें

```sh
dotnet restore
```

निम्नलिखित लाइब्रेरी इंस्टॉल होनी चाहिए: Azure AI Inference, Azure Identity, Microsoft.Extension, Model.Hosting, ModelContextProtcol

## चलाएं

```sh 
dotnet run
```

आपको इस तरह का आउटपुट दिखना चाहिए:

```text
Setting up stdio transport
Listing tools
Connected to server with tools: Add
Tool description: Adds two numbers
Tool parameters: {"title":"Add","description":"Adds two numbers","type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}
Tool definition: Azure.AI.Inference.ChatCompletionsToolDefinition
Properties: {"a":{"type":"integer"},"b":{"type":"integer"}}
MCP Tools def: 0: Azure.AI.Inference.ChatCompletionsToolDefinition
Tool call 0: Add with arguments {"a":2,"b":4}
Sum 6
```

आउटपुट का अधिकांश हिस्सा डिबगिंग के लिए है, लेकिन महत्वपूर्ण यह है कि आप MCP Server से टूल्स की लिस्टिंग कर रहे हैं, उन्हें LLM टूल्स में बदल रहे हैं और अंत में आपको MCP क्लाइंट का जवाब "Sum 6" मिल रहा है।

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही अधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।