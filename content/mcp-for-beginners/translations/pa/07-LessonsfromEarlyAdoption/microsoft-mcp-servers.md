<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T11:19:12+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "pa"
}
-->
# 🚀 10 Microsoft MCP ਸਰਵਰ ਜੋ ਡਿਵੈਲਪਰ ਦੀ ਉਤਪਾਦਕਤਾ ਨੂੰ ਬਦਲ ਰਹੇ ਹਨ

## 🎯 ਇਸ ਗਾਈਡ ਵਿੱਚ ਤੁਸੀਂ ਕੀ ਸਿੱਖੋਗੇ

ਇਹ ਪ੍ਰਯੋਗਿਕ ਗਾਈਡ ਦੱਸਦੀ ਹੈ ਕਿ ਕਿਵੇਂ ਦਸ Microsoft MCP ਸਰਵਰ ਡਿਵੈਲਪਰਾਂ ਦੇ ਕੰਮ ਕਰਨ ਦੇ ਢੰਗ ਨੂੰ AI ਸਹਾਇਕਾਂ ਨਾਲ ਬਦਲ ਰਹੇ ਹਨ। ਸਿਰਫ ਇਹ ਨਹੀਂ ਦੱਸਿਆ ਜਾਵੇਗਾ ਕਿ MCP ਸਰਵਰ ਕੀ ਕਰ ਸਕਦੇ ਹਨ, ਸਗੋਂ ਅਸੀਂ ਉਹ ਸਰਵਰ ਵੀ ਦਿਖਾਵਾਂਗੇ ਜੋ ਮਾਇਕ੍ਰੋਸਾਫਟ ਅਤੇ ਹੋਰ ਥਾਵਾਂ ‘ਤੇ ਰੋਜ਼ਾਨਾ ਵਿਕਾਸ ਕਾਰਜਾਂ ਵਿੱਚ ਅਸਲ ਤਬਦੀਲੀ ਲਿਆ ਰਹੇ ਹਨ।

ਇਸ ਗਾਈਡ ਵਿੱਚ ਹਰ ਸਰਵਰ ਨੂੰ ਅਸਲੀ ਵਰਤੋਂ ਅਤੇ ਡਿਵੈਲਪਰਾਂ ਦੀ ਪ੍ਰਤੀਕਿਰਿਆ ਦੇ ਆਧਾਰ ‘ਤੇ ਚੁਣਿਆ ਗਿਆ ਹੈ। ਤੁਸੀਂ ਸਿਰਫ ਇਹ ਨਹੀਂ ਜਾਣੋਗੇ ਕਿ ਹਰ ਸਰਵਰ ਕੀ ਕਰਦਾ ਹੈ, ਬਲਕਿ ਇਹ ਵੀ ਸਮਝੋਗੇ ਕਿ ਇਹ ਕਿਉਂ ਮਹੱਤਵਪੂਰਨ ਹੈ ਅਤੇ ਆਪਣੇ ਪ੍ਰੋਜੈਕਟਾਂ ਵਿੱਚ ਇਸ ਤੋਂ ਵੱਧ ਤੋਂ ਵੱਧ ਲਾਭ ਕਿਵੇਂ ਲੈਣਾ ਹੈ। ਚਾਹੇ ਤੁਸੀਂ MCP ਵਿੱਚ ਨਵੇਂ ਹੋ ਜਾਂ ਆਪਣੇ ਮੌਜੂਦਾ ਸੈਟਅੱਪ ਨੂੰ ਵਧਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ, ਇਹ ਸਰਵਰ ਮਾਇਕ੍ਰੋਸਾਫਟ ਪਰਿਵਾਰ ਵਿੱਚ ਸਭ ਤੋਂ ਪ੍ਰਯੋਗਿਕ ਅਤੇ ਪ੍ਰਭਾਵਸ਼ਾਲੀ ਟੂਲ ਹਨ।

> **💡 ਤੁਰੰਤ ਸ਼ੁਰੂਆਤ ਲਈ ਟਿਪ**
> 
> MCP ਵਿੱਚ ਨਵੇਂ ਹੋ? ਚਿੰਤਾ ਨਾ ਕਰੋ! ਇਹ ਗਾਈਡ ਸ਼ੁਰੂਆਤੀ ਲਈ ਸੌਖੀ ਬਣਾਈ ਗਈ ਹੈ। ਅਸੀਂ ਜਦੋਂ ਜਦੋਂ ਲੋੜ ਹੋਵੇ, ਤੱਤ ਸਮਝਾਵਾਂਗੇ, ਅਤੇ ਤੁਸੀਂ ਸਾਡੇ [Introduction to MCP](../00-Introduction/README.md) ਅਤੇ [Core Concepts](../01-CoreConcepts/README.md) ਮੋਡੀਊਲਾਂ ਨੂੰ ਵੀ ਵਧੇਰੇ ਜਾਣਕਾਰੀ ਲਈ ਵੇਖ ਸਕਦੇ ਹੋ।

## ਓਵਰਵਿਊ

ਇਹ ਵਿਸਤ੍ਰਿਤ ਗਾਈਡ ਦੱਸਦੀ ਹੈ ਕਿ ਕਿਵੇਂ ਦਸ Microsoft MCP ਸਰਵਰ ਡਿਵੈਲਪਰਾਂ ਨੂੰ AI ਸਹਾਇਕਾਂ ਅਤੇ ਬਾਹਰੀ ਟੂਲਾਂ ਨਾਲ ਨਵੀਂ ਤਰ੍ਹਾਂ ਕੰਮ ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰ ਰਹੇ ਹਨ। Azure ਰਿਸੋਰਸ ਮੈਨੇਜਮੈਂਟ ਤੋਂ ਲੈ ਕੇ ਦਸਤਾਵੇਜ਼ ਪ੍ਰੋਸੈਸਿੰਗ ਤੱਕ, ਇਹ ਸਰਵਰ Model Context Protocol ਦੀ ਤਾਕਤ ਨੂੰ ਦਰਸਾਉਂਦੇ ਹਨ ਜੋ ਵਿਕਾਸ ਕਾਰਜਾਂ ਨੂੰ ਬਿਨਾਂ ਰੁਕਾਵਟ ਅਤੇ ਉਤਪਾਦਕ ਬਣਾਉਂਦਾ ਹੈ।

## ਸਿੱਖਣ ਦੇ ਲਕੜੇ

ਇਸ ਗਾਈਡ ਦੇ ਅੰਤ ਤੱਕ, ਤੁਸੀਂ:
- ਸਮਝੋਗੇ ਕਿ MCP ਸਰਵਰ ਡਿਵੈਲਪਰ ਦੀ ਉਤਪਾਦਕਤਾ ਕਿਵੇਂ ਵਧਾਉਂਦੇ ਹਨ
- ਮਾਇਕ੍ਰੋਸਾਫਟ ਦੇ ਸਭ ਤੋਂ ਪ੍ਰਭਾਵਸ਼ਾਲੀ MCP ਸਰਵਰ ਇੰਪਲੀਮੈਂਟੇਸ਼ਨਾਂ ਬਾਰੇ ਜਾਣੋਗੇ
- ਹਰ ਸਰਵਰ ਦੇ ਪ੍ਰਯੋਗਿਕ ਕੇਸਾਂ ਨੂੰ ਜਾਣੋਗੇ
- ਜਾਣੋਗੇ ਕਿ VS Code ਅਤੇ Visual Studio ਵਿੱਚ ਇਹਨਾਂ ਸਰਵਰਾਂ ਨੂੰ ਕਿਵੇਂ ਸੈਟਅੱਪ ਅਤੇ ਕਨਫਿਗਰ ਕਰਨਾ ਹੈ
- MCP ਪਰਿਵਾਰ ਅਤੇ ਭਵਿੱਖ ਦੇ ਰੁਝਾਨਾਂ ਬਾਰੇ ਜਾਣੋਗੇ

## 🔧 MCP ਸਰਵਰਾਂ ਦੀ ਸਮਝ: ਇੱਕ ਸ਼ੁਰੂਆਤੀ ਲਈ ਗਾਈਡ

### MCP ਸਰਵਰ ਕੀ ਹਨ?

Model Context Protocol (MCP) ਵਿੱਚ ਨਵੇਂ ਹੋਣ ਦੇ ਨਾਤੇ, ਤੁਸੀਂ ਸੋਚ ਸਕਦੇ ਹੋ: "MCP ਸਰਵਰ ਕੀ ਹੁੰਦਾ ਹੈ ਅਤੇ ਇਹ ਮੇਰੇ ਲਈ ਕਿਉਂ ਜਰੂਰੀ ਹੈ?" ਆਓ ਇੱਕ ਸਧਾਰਣ ਉਦਾਹਰਨ ਨਾਲ ਸ਼ੁਰੂ ਕਰੀਏ।

MCP ਸਰਵਰਾਂ ਨੂੰ ਖਾਸ ਸਹਾਇਕ ਸਮਝੋ ਜੋ ਤੁਹਾਡੇ AI ਕੋਡਿੰਗ ਸਾਥੀ (ਜਿਵੇਂ GitHub Copilot) ਨੂੰ ਬਾਹਰੀ ਟੂਲਾਂ ਅਤੇ ਸੇਵਾਵਾਂ ਨਾਲ ਜੁੜਨ ਵਿੱਚ ਮਦਦ ਕਰਦੇ ਹਨ। ਜਿਵੇਂ ਤੁਸੀਂ ਆਪਣੇ ਫੋਨ ‘ਤੇ ਵੱਖ-ਵੱਖ ਕੰਮਾਂ ਲਈ ਵੱਖ-ਵੱਖ ਐਪਸ ਵਰਤਦੇ ਹੋ — ਮੌਸਮ ਲਈ ਇੱਕ, ਨੈਵੀਗੇਸ਼ਨ ਲਈ ਇੱਕ, ਬੈਂਕਿੰਗ ਲਈ ਇੱਕ — MCP ਸਰਵਰ ਤੁਹਾਡੇ AI ਸਹਾਇਕ ਨੂੰ ਵੱਖ-ਵੱਖ ਵਿਕਾਸ ਟੂਲਾਂ ਅਤੇ ਸੇਵਾਵਾਂ ਨਾਲ ਗੱਲਬਾਤ ਕਰਨ ਦੀ ਸਮਰੱਥਾ ਦਿੰਦੇ ਹਨ।

### MCP ਸਰਵਰ ਕਿਹੜੀ ਸਮੱਸਿਆ ਹੱਲ ਕਰਦੇ ਹਨ

MCP ਸਰਵਰਾਂ ਤੋਂ ਪਹਿਲਾਂ, ਜੇ ਤੁਸੀਂ:
- ਆਪਣੇ Azure ਰਿਸੋਰਸ ਵੇਖਣੇ ਹੋਣ
- GitHub ਇਸ਼ੂ ਬਣਾਉਣਾ ਹੋਵੇ
- ਡੇਟਾਬੇਸ ਵਿੱਚ ਕੁਝ ਪੁੱਛਣਾ ਹੋਵੇ
- ਦਸਤਾਵੇਜ਼ਾਂ ਵਿੱਚ ਖੋਜ ਕਰਨੀ ਹੋਵੇ

ਤਾਂ ਤੁਹਾਨੂੰ ਕੋਡਿੰਗ ਰੋਕ ਕੇ ਬ੍ਰਾਊਜ਼ਰ ਖੋਲ੍ਹਣਾ ਪੈਂਦਾ ਸੀ, ਸਹੀ ਵੈੱਬਸਾਈਟ ਤੇ ਜਾਣਾ ਪੈਂਦਾ ਸੀ ਅਤੇ ਇਹ ਸਾਰੇ ਕੰਮ ਹੱਥੋਂ ਕਰਨੇ ਪੈਂਦੇ ਸਨ। ਇਹ ਲਗਾਤਾਰ ਸੰਦਰਭ ਬਦਲਣਾ ਤੁਹਾਡੇ ਕੰਮ ਦੇ ਧਾਰਾ ਨੂੰ ਤੋੜਦਾ ਹੈ ਅਤੇ ਉਤਪਾਦਕਤਾ ਘਟਾਉਂਦਾ ਹੈ।

### MCP ਸਰਵਰ ਤੁਹਾਡੇ ਵਿਕਾਸ ਅਨੁਭਵ ਨੂੰ ਕਿਵੇਂ ਬਦਲਦੇ ਹਨ

MCP ਸਰਵਰਾਂ ਨਾਲ, ਤੁਸੀਂ ਆਪਣੇ ਵਿਕਾਸ ਵਾਤਾਵਰਣ (VS Code, Visual Studio ਆਦਿ) ਵਿੱਚ ਹੀ ਰਹਿ ਕੇ ਆਪਣੇ AI ਸਹਾਇਕ ਨੂੰ ਇਹ ਕੰਮ ਕਰਵਾਉ ਸਕਦੇ ਹੋ। ਉਦਾਹਰਨ ਵਜੋਂ:

**ਪੁਰਾਣਾ ਤਰੀਕਾ:**
1. ਕੋਡਿੰਗ ਰੋਕੋ
2. ਬ੍ਰਾਊਜ਼ਰ ਖੋਲ੍ਹੋ
3. Azure ਪੋਰਟਲ ਤੇ ਜਾਓ
4. ਸਟੋਰੇਜ ਅਕਾਊਂਟ ਵੇਰਵੇ ਵੇਖੋ
5. VS Code ਤੇ ਵਾਪਸ ਆਓ
6. ਕੋਡਿੰਗ ਜਾਰੀ ਰੱਖੋ

**ਹੁਣ ਤੁਸੀਂ ਇਹ ਕਰ ਸਕਦੇ ਹੋ:**
1. AI ਨੂੰ ਪੁੱਛੋ: "ਮੇਰੇ Azure ਸਟੋਰੇਜ ਅਕਾਊਂਟਾਂ ਦੀ ਸਥਿਤੀ ਕੀ ਹੈ?"
2. ਮਿਲੀ ਜਾਣਕਾਰੀ ਨਾਲ ਕੋਡਿੰਗ ਜਾਰੀ ਰੱਖੋ

### ਸ਼ੁਰੂਆਤੀਆਂ ਲਈ ਮੁੱਖ ਫਾਇਦੇ

#### 1. 🔄 **ਆਪਣੇ ਧਾਰਾ ਵਿੱਚ ਰਹੋ**
- ਵੱਖ-ਵੱਖ ਐਪਲੀਕੇਸ਼ਨਾਂ ਵਿੱਚ ਬਦਲਾਅ ਨਹੀਂ
- ਆਪਣੇ ਲਿਖੇ ਕੋਡ ‘ਤੇ ਧਿਆਨ ਕੇਂਦਰਿਤ ਰੱਖੋ
- ਵੱਖ-ਵੱਖ ਟੂਲਾਂ ਨੂੰ ਸੰਭਾਲਣ ਦੀ ਮਾਨਸਿਕ ਭਾਰ ਘਟਾਓ

#### 2. 🤖 **ਕਠਿਨ ਹੁਕਮਾਂ ਦੀ ਥਾਂ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਵਰਤੋ**
- SQL ਸਿੰਟੈਕਸ ਯਾਦ ਕਰਨ ਦੀ ਥਾਂ ਦੱਸੋ ਕਿ ਤੁਹਾਨੂੰ ਕਿਹੜਾ ਡੇਟਾ ਚਾਹੀਦਾ ਹੈ
- Azure CLI ਕਮਾਂਡਾਂ ਯਾਦ ਕਰਨ ਦੀ ਥਾਂ ਦੱਸੋ ਕਿ ਤੁਸੀਂ ਕੀ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ
- AI ਨੂੰ ਤਕਨੀਕੀ ਵਿਵਰਣ ਸੰਭਾਲਣ ਦਿਓ, ਤੁਸੀਂ ਲਾਜਿਕ ‘ਤੇ ਧਿਆਨ ਦਿਓ

#### 3. 🔗 **ਕਈ ਟੂਲਾਂ ਨੂੰ ਜੋੜੋ**
- ਵੱਖ-ਵੱਖ ਸੇਵਾਵਾਂ ਨੂੰ ਮਿਲਾ ਕੇ ਸ਼ਕਤੀਸ਼ਾਲੀ ਵਰਕਫਲੋ ਬਣਾਓ
- ਉਦਾਹਰਨ: "ਸਾਰੇ ਹਾਲੀਆ GitHub ਇਸ਼ੂ ਲਵੋ ਅਤੇ ਉਨ੍ਹਾਂ ਲਈ Azure DevOps ਵਰਕ ਆਈਟਮ ਬਣਾਓ"
- ਜਟਿਲ ਸਕ੍ਰਿਪਟਾਂ ਲਿਖਣ ਬਿਨਾਂ ਆਟੋਮੇਸ਼ਨ ਬਣਾਓ

#### 4. 🌐 **ਵਧ ਰਹੇ ਪਰਿਵਾਰ ਤੱਕ ਪਹੁੰਚ**
- Microsoft, GitHub ਅਤੇ ਹੋਰ ਕੰਪਨੀਆਂ ਵੱਲੋਂ ਬਣਾਏ ਸਰਵਰਾਂ ਦਾ ਲਾਭ ਲਵੋ
- ਵੱਖ-ਵੱਖ ਵਿਕਰੇਤਿਆਂ ਦੇ ਟੂਲਾਂ ਨੂੰ ਆਸਾਨੀ ਨਾਲ ਮਿਲਾਓ
- ਇੱਕ ਮਿਆਰੀ ਪਰਿਵਾਰ ਦਾ ਹਿੱਸਾ ਬਣੋ ਜੋ ਵੱਖ-ਵੱਖ AI ਸਹਾਇਕਾਂ ਨਾਲ ਕੰਮ ਕਰਦਾ ਹੈ

#### 5. 🛠️ **ਕਰ ਕੇ ਸਿੱਖੋ**
- ਪਹਿਲਾਂ ਤਿਆਰ ਕੀਤੇ ਸਰਵਰਾਂ ਨਾਲ ਸ਼ੁਰੂ ਕਰੋ ਤਾਂ ਜੋ ਮੂਲ ਧਾਰਣਾ ਸਮਝ ਆ ਜਾਵੇ
- ਜਿਵੇਂ ਜਿਵੇਂ ਆਰਾਮਦਾਇਕ ਹੋਵੋ, ਆਪਣੇ ਸਰਵਰ ਬਣਾਉ
- ਉਪਲਬਧ SDKs ਅਤੇ ਦਸਤਾਵੇਜ਼ਾਂ ਨਾਲ ਸਿੱਖਣ ਵਿੱਚ ਮਦਦ ਲਵੋ

### ਸ਼ੁਰੂਆਤੀਆਂ ਲਈ ਅਸਲੀ ਉਦਾਹਰਨ

ਮਾਨ ਲਓ ਤੁਸੀਂ ਵੈੱਬ ਵਿਕਾਸ ਵਿੱਚ ਨਵੇਂ ਹੋ ਅਤੇ ਆਪਣਾ ਪਹਿਲਾ ਪ੍ਰੋਜੈਕਟ ਕਰ ਰਹੇ ਹੋ। MCP ਸਰਵਰ ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦੇ ਹਨ:

**ਪੁਰਾਣਾ ਤਰੀਕਾ:**
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**MCP ਸਰਵਰਾਂ ਨਾਲ:**
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### ਐਂਟਰਪ੍ਰਾਈਜ਼ ਮਿਆਰੀ ਫਾਇਦਾ

MCP ਇੱਕ ਉਦਯੋਗ-ਵਿਆਪੀ ਮਿਆਰੀ ਬਣ ਰਿਹਾ ਹੈ, ਜਿਸਦਾ ਮਤਲਬ ਹੈ:
- **ਸਮਰੂਪਤਾ**: ਵੱਖ-ਵੱਖ ਟੂਲਾਂ ਅਤੇ ਕੰਪਨੀਆਂ ਵਿੱਚ ਇੱਕੋ ਜਿਹਾ ਅਨੁਭਵ
- **ਇੰਟਰਓਪਰੇਬਿਲਿਟੀ**: ਵੱਖ-ਵੱਖ ਵਿਕਰੇਤਿਆਂ ਦੇ ਸਰਵਰ ਇਕੱਠੇ ਕੰਮ ਕਰਦੇ ਹਨ
- **ਭਵਿੱਖ-ਸੁਰੱਖਿਆ**: ਹੁਨਰ ਅਤੇ ਸੈਟਅੱਪ ਵੱਖ-ਵੱਖ AI ਸਹਾਇਕਾਂ ਵਿੱਚ ਟ੍ਰਾਂਸਫਰ ਹੁੰਦੇ ਹਨ
- **ਕਮਿਊਨਿਟੀ**: ਵੱਡਾ ਪਰਿਵਾਰ ਸਾਂਝੇ ਗਿਆਨ ਅਤੇ ਸਰੋਤਾਂ ਦਾ

### ਸ਼ੁਰੂਆਤ: ਤੁਸੀਂ ਕੀ ਸਿੱਖੋਗੇ

ਇਸ ਗਾਈਡ ਵਿੱਚ ਅਸੀਂ 10 Microsoft MCP ਸਰਵਰਾਂ ਦੀ ਚਰਚਾ ਕਰਾਂਗੇ ਜੋ ਹਰ ਪੱਧਰ ਦੇ ਡਿਵੈਲਪਰਾਂ ਲਈ ਬਹੁਤ ਲਾਭਦਾਇਕ ਹਨ। ਹਰ ਸਰਵਰ ਇਸ ਤਰ੍ਹਾਂ ਬਣਾਇਆ ਗਿਆ ਹੈ ਕਿ:
- ਆਮ ਵਿਕਾਸ ਸਮੱਸਿਆਵਾਂ ਹੱਲ ਕਰੇ
- ਦੁਹਰਾਏ ਜਾਣ ਵਾਲੇ ਕੰਮ ਘਟਾਏ
- ਕੋਡ ਦੀ ਗੁਣਵੱਤਾ ਸੁਧਾਰੇ
- ਸਿੱਖਣ ਦੇ ਮੌਕੇ ਵਧਾਏ

> **💡 ਸਿੱਖਣ ਦੀ ਟਿਪ**
> 
> ਜੇ ਤੁਸੀਂ MCP ਵਿੱਚ ਬਿਲਕੁਲ ਨਵੇਂ ਹੋ, ਤਾਂ ਪਹਿਲਾਂ ਸਾਡੇ [Introduction to MCP](../00-Introduction/README.md) ਅਤੇ [Core Concepts](../01-CoreConcepts/README.md) ਮੋਡੀਊਲਾਂ ਨੂੰ ਦੇਖੋ। ਫਿਰ ਇੱਥੇ ਵਾਪਸ ਆ ਕੇ ਅਸਲ Microsoft ਟੂਲਾਂ ਨਾਲ ਇਹ ਧਾਰਣਾਵਾਂ ਕਿਵੇਂ ਕੰਮ ਕਰਦੀਆਂ ਹਨ, ਵੇਖੋ।
>
> MCP ਦੀ ਮਹੱਤਤਾ ਬਾਰੇ ਵਧੇਰੇ ਜਾਣਕਾਰੀ ਲਈ, Maria Naggaga ਦੀ ਪੋਸਟ ਵੇਖੋ: [Connect Once, Integrate Anywhere with MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps).

## VS Code ਅਤੇ Visual Studio ਵਿੱਚ MCP ਨਾਲ ਸ਼ੁਰੂਆਤ 🚀

ਜੇ ਤੁਸੀਂ Visual Studio Code ਜਾਂ Visual Studio 2022 GitHub Copilot ਨਾਲ ਵਰਤ ਰਹੇ ਹੋ, ਤਾਂ ਇਹ MCP ਸਰਵਰ ਸੈਟਅੱਪ ਕਰਨਾ ਆਸਾਨ ਹੈ।

### VS Code ਸੈਟਅੱਪ

VS Code ਲਈ ਮੁੱਢਲਾ ਪ੍ਰਕਿਰਿਆ ਇਹ ਹੈ:

1. **Agent Mode ਚਾਲੂ ਕਰੋ**: VS Code ਵਿੱਚ Copilot Chat ਵਿੰਡੋ ਵਿੱਚ Agent ਮੋਡ ‘ਤੇ ਜਾਓ
2. **MCP ਸਰਵਰ ਕਨਫਿਗਰ ਕਰੋ**: ਆਪਣੇ VS Code settings.json ਫਾਇਲ ਵਿੱਚ ਸਰਵਰ ਕਨਫਿਗਰੇਸ਼ਨ ਸ਼ਾਮਲ ਕਰੋ
3. **ਸਰਵਰ ਸ਼ੁਰੂ ਕਰੋ**: ਹਰ ਸਰਵਰ ਲਈ "Start" ਬਟਨ ‘ਤੇ ਕਲਿੱਕ ਕਰੋ ਜੋ ਤੁਸੀਂ ਵਰਤਣਾ ਚਾਹੁੰਦੇ ਹੋ
4. **ਟੂਲ ਚੁਣੋ**: ਆਪਣੇ ਮੌਜੂਦਾ ਸੈਸ਼ਨ ਲਈ ਕਿਹੜੇ MCP ਸਰਵਰ ਚਾਲੂ ਕਰਨੇ ਹਨ, ਚੁਣੋ

ਵਿਸਥਾਰ ਵਿੱਚ ਸੈਟਅੱਪ ਲਈ [VS Code MCP ਦਸਤਾਵੇਜ਼](https://code.visualstudio.com/docs/copilot/copilot-mcp) ਵੇਖੋ।

> **💡 ਪ੍ਰੋ ਟਿਪ: MCP ਸਰਵਰਾਂ ਨੂੰ ਪ੍ਰੋ ਵਾਂਗ ਸੰਭਾਲੋ!**
> 
> VS Code Extensions ਵਿਊ ਵਿੱਚ ਹੁਣ [ਇੰਸਟਾਲ ਕੀਤੇ MCP ਸਰਵਰਾਂ ਨੂੰ ਮੈਨੇਜ ਕਰਨ ਲਈ ਨਵਾਂ UI](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) ਹੈ! ਤੁਸੀਂ ਕਿਸੇ ਵੀ MCP ਸਰਵਰ ਨੂੰ ਆਸਾਨੀ ਨਾਲ ਸ਼ੁਰੂ, ਰੋਕ ਅਤੇ ਮੈਨੇਜ ਕਰ ਸਕਦੇ ਹੋ। ਜਰੂਰ ਕੋਸ਼ਿਸ਼ ਕਰੋ!

### Visual Studio 2022 ਸੈਟਅੱਪ

Visual Studio 2022 (ਵਰਜਨ 17.14 ਜਾਂ ਬਾਅਦ) ਲਈ:

1. **Agent Mode ਚਾਲੂ ਕਰੋ**: GitHub Copilot Chat ਵਿੰਡੋ ਵਿੱਚ "Ask" ਡ੍ਰੌਪਡਾਊਨ ‘ਚੋਂ "Agent" ਚੁਣੋ
2. **ਕਨਫਿਗਰੇਸ਼ਨ ਫਾਇਲ ਬਣਾਓ**: ਆਪਣੇ ਸਲੂਸ਼ਨ ਡਾਇਰੈਕਟਰੀ ਵਿੱਚ `.mcp.json` ਫਾਇਲ ਬਣਾਓ (ਸਿਫਾਰਸ਼ੀ ਥਾਂ: `<SOLUTIONDIR>\.mcp.json`)
3. **ਸਰਵਰ ਕਨਫਿਗਰ ਕਰੋ**: MCP ਦੇ ਮਿਆਰੀ ਫਾਰਮੈਟ ਵਿੱਚ ਸਰਵਰ ਕਨਫਿਗਰੇਸ਼ਨ ਸ਼ਾਮਲ ਕਰੋ
4. **ਟੂਲ ਮਨਜ਼ੂਰੀ**: ਜਦੋਂ ਪੁੱਛਿਆ ਜਾਵੇ, ਵਰਤਣ ਵਾਲੇ ਟੂਲਾਂ ਲਈ ਸਹੀ ਅਧਿਕਾਰ ਦਿਓ

Visual Studio ਸੈਟਅੱਪ ਲਈ [Visual Studio MCP ਦਸਤਾਵੇਜ਼](https://learn.microsoft.com/visualstudio/ide/mcp-servers) ਵੇਖੋ।

ਹਰ MCP ਸਰਵਰ ਦੀ ਆਪਣੀ ਕਨਫਿਗਰੇਸ਼ਨ ਲੋੜ ਹੁੰਦੀ ਹੈ (ਕਨੈਕਸ਼ਨ ਸਟਰਿੰਗ, ਪ੍ਰਮਾਣਿਕਤਾ ਆਦਿ), ਪਰ ਦੋਹਾਂ IDEs ਵਿੱਚ ਸੈਟਅੱਪ ਦਾ ਢਾਂਚਾ ਇੱਕੋ ਜਿਹਾ ਹੈ।

## Microsoft MCP ਸਰਵਰਾਂ ਤੋਂ ਸਿੱਖਿਆ 🛠️

### 1. 📚 Microsoft Learn Docs MCP Server

[![VS Code ਵਿੱਚ ਇੰਸਟਾਲ ਕਰੋ](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![VS Code Insiders ਵਿੱਚ ਇੰਸਟਾਲ ਕਰੋ](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: Microsoft Learn Docs MCP Server ਇੱਕ ਕਲਾਉਡ-ਆਧਾਰਿਤ ਸੇਵਾ ਹੈ ਜੋ AI ਸਹਾਇਕਾਂ ਨੂੰ Model Context Protocol ਰਾਹੀਂ ਅਧਿਕਾਰਤ Microsoft ਦਸਤਾਵੇਜ਼ਾਂ ਤੱਕ ਰੀਅਲ-ਟਾਈਮ ਪਹੁੰਚ ਦਿੰਦੀ ਹੈ। ਇਹ `https://learn.microsoft.com/api/mcp` ਨਾਲ ਜੁੜਦਾ ਹੈ ਅਤੇ Microsoft Learn, Azure ਦਸਤਾਵੇਜ਼, Microsoft 365 ਦਸਤਾਵੇਜ਼ ਅਤੇ ਹੋਰ ਅਧਿਕਾਰਤ ਸਰੋਤਾਂ ਵਿੱਚ ਸੈਮਾਂਟਿਕ ਖੋਜ ਯੋਗ ਬਣਾਉਂਦਾ ਹੈ।

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: ਜਦੋਂ ਕਿ ਇਹ ਸਿਰਫ "ਦਸਤਾਵੇਜ਼" ਵਰਗਾ ਲੱਗ ਸਕਦਾ ਹੈ, ਇਹ ਸਰਵਰ ਹਰ ਉਸ ਡਿਵੈਲਪਰ ਲਈ ਬਹੁਤ ਜਰੂਰੀ ਹੈ ਜੋ Microsoft ਤਕਨਾਲੋਜੀ ਵਰਤਦਾ ਹੈ। .NET ਡਿਵੈਲਪਰਾਂ ਵੱਲੋਂ AI ਕੋਡਿੰਗ ਸਹਾਇਕਾਂ ਬਾਰੇ ਸਭ ਤੋਂ ਵੱਡੀ ਸ਼ਿਕਾਇਤ ਇਹ ਹੁੰਦੀ ਹੈ ਕਿ ਉਹ ਨਵੇਂ .NET ਅਤੇ C# ਰਿਲੀਜ਼ਾਂ ਨਾਲ ਅਪ-ਟੂ-ਡੇਟ ਨਹੀਂ ਹੁੰਦੇ। Microsoft Learn Docs MCP Server ਇਸ ਸਮੱਸਿਆ ਨੂੰ ਹੱਲ ਕਰਦਾ ਹੈ ਅਤੇ ਸਭ ਤੋਂ ਤਾਜ਼ਾ ਦਸਤਾਵੇਜ਼, API ਰੈਫਰੈਂਸ ਅਤੇ ਬਿਹਤਰ ਅਭਿਆਸਾਂ ਤੱਕ ਰੀਅਲ-ਟਾਈਮ ਪਹੁੰਚ ਦਿੰਦਾ ਹੈ। ਚਾਹੇ ਤੁਸੀਂ ਨਵੇਂ Azure SDK
> **💡 ਪ੍ਰੋ ਟਿਪ**
> 
> ਹਾਲਾਂਕਿ ਟੂਲ-ਮਿੱਤਰ ਮਾਡਲਾਂ ਨੂੰ MCP ਟੂਲਾਂ ਵਰਤਣ ਲਈ ਪ੍ਰੋਤਸਾਹਨ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ! ਇੱਕ ਸਿਸਟਮ ਪ੍ਰਾਂਪਟ ਜਾਂ [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) ਸ਼ਾਮਲ ਕਰਨ ਬਾਰੇ ਸੋਚੋ, ਜਿਵੇਂ: "ਤੁਹਾਡੇ ਕੋਲ `microsoft.docs.mcp` ਦੀ ਪਹੁੰਚ ਹੈ – ਇਸ ਟੂਲ ਨੂੰ ਵਰਤ ਕੇ Microsoft ਦੀਆਂ ਤਾਜ਼ਾ ਅਧਿਕਾਰਿਕ ਦਸਤਾਵੇਜ਼ਾਂ ਵਿੱਚ C#, Azure, ASP.NET Core ਜਾਂ Entity Framework ਵਰਗੀਆਂ Microsoft ਤਕਨਾਲੋਜੀਆਂ ਬਾਰੇ ਸਵਾਲਾਂ ਨੂੰ ਸੰਭਾਲਣ ਸਮੇਂ ਖੋਜ ਕਰੋ।"
>
> ਇਸਦਾ ਇੱਕ ਵਧੀਆ ਉਦਾਹਰਨ ਦੇਖਣ ਲਈ, Awesome GitHub Copilot ਰਿਪੋਜ਼ਟਰੀ ਵਿੱਚੋਂ [C# .NET Janitor ਚੈਟ ਮੋਡ](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) ਨੂੰ ਵੇਖੋ। ਇਹ ਮੋਡ ਖਾਸ ਤੌਰ 'ਤੇ Microsoft Learn Docs MCP ਸਰਵਰ ਦੀ ਵਰਤੋਂ ਕਰਦਾ ਹੈ ਤਾਂ ਜੋ C# ਕੋਡ ਨੂੰ ਸਾਫ਼ ਅਤੇ ਆਧੁਨਿਕ ਬਣਾਉਣ ਵਿੱਚ ਮਦਦ ਮਿਲੇ, ਨਵੇਂ ਪੈਟਰਨਾਂ ਅਤੇ ਸਭ ਤੋਂ ਵਧੀਆ ਅਭਿਆਸਾਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ।
### 2. ☁️ Azure MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: Azure MCP Server 15+ ਖਾਸ Azure ਸੇਵਾ ਕਨੈਕਟਰਾਂ ਦਾ ਇੱਕ ਵਿਆਪਕ ਸੂਟ ਹੈ ਜੋ ਪੂਰੇ Azure ਪਰਿਵਾਰ ਨੂੰ ਤੁਹਾਡੇ AI ਵਰਕਫਲੋ ਵਿੱਚ ਲਿਆਉਂਦਾ ਹੈ। ਇਹ ਸਿਰਫ ਇੱਕ ਸਰਵਰ ਨਹੀਂ ਹੈ – ਇਹ ਇੱਕ ਸ਼ਕਤੀਸ਼ਾਲੀ ਕਲੈਕਸ਼ਨ ਹੈ ਜਿਸ ਵਿੱਚ ਰਿਸੋਰਸ ਮੈਨੇਜਮੈਂਟ, ਡੇਟਾਬੇਸ ਕਨੈਕਟਿਵਿਟੀ (PostgreSQL, SQL Server), KQL ਨਾਲ Azure Monitor ਲੌਗ ਵਿਸ਼ਲੇਸ਼ਣ, Cosmos DB ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਅਤੇ ਹੋਰ ਬਹੁਤ ਕੁਝ ਸ਼ਾਮਲ ਹੈ।

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: ਸਿਰਫ Azure ਰਿਸੋਰਸਾਂ ਦਾ ਪ੍ਰਬੰਧਨ ਕਰਨ ਤੋਂ ਇਲਾਵਾ, ਇਹ ਸਰਵਰ Azure SDKs ਨਾਲ ਕੰਮ ਕਰਦਿਆਂ ਕੋਡ ਦੀ ਗੁਣਵੱਤਾ ਨੂੰ ਬਹੁਤ ਬਿਹਤਰ ਬਣਾਉਂਦਾ ਹੈ। ਜਦੋਂ ਤੁਸੀਂ Agent ਮੋਡ ਵਿੱਚ Azure MCP ਵਰਤਦੇ ਹੋ, ਤਾਂ ਇਹ ਸਿਰਫ ਕੋਡ ਲਿਖਣ ਵਿੱਚ ਮਦਦ ਨਹੀਂ ਕਰਦਾ – ਇਹ ਤੁਹਾਨੂੰ *ਵਧੀਆ* Azure ਕੋਡ ਲਿਖਣ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹੈ ਜੋ ਮੌਜੂਦਾ ਪ੍ਰਮਾਣਿਕਤਾ ਪੈਟਰਨ, ਗਲਤੀ ਸੰਭਾਲਣ ਦੀਆਂ ਸਭ ਤੋਂ ਵਧੀਆ ਪ੍ਰਥਾਵਾਂ ਅਤੇ ਨਵੀਨਤਮ SDK ਫੀਚਰਾਂ ਦੀ ਪਾਲਣਾ ਕਰਦਾ ਹੈ। ਜਨਰਲ ਕੋਡ ਦੀ ਥਾਂ, ਜੋ ਸ਼ਾਇਦ ਕੰਮ ਕਰੇ, ਤੁਹਾਨੂੰ ਉਹ ਕੋਡ ਮਿਲਦਾ ਹੈ ਜੋ ਉਤਪਾਦਨ ਵਰਕਲੋਡ ਲਈ Azure ਦੀਆਂ ਸਿਫਾਰਸ਼ੀ ਪੈਟਰਨਾਂ ਦੀ ਪਾਲਣਾ ਕਰਦਾ ਹੈ।

**ਮੁੱਖ ਮੋਡੀਊਲ ਸ਼ਾਮਲ ਹਨ**:
- **🗄️ ਡੇਟਾਬੇਸ ਕਨੈਕਟਰ**: Azure Database for PostgreSQL ਅਤੇ SQL Server ਲਈ ਸਿੱਧਾ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਰਾਹੀਂ ਪਹੁੰਚ
- **📊 Azure Monitor**: KQL-ਚਾਲਿਤ ਲੌਗ ਵਿਸ਼ਲੇਸ਼ਣ ਅਤੇ ਓਪਰੇਸ਼ਨਲ ਜਾਣਕਾਰੀਆਂ
- **🌐 ਰਿਸੋਰਸ ਮੈਨੇਜਮੈਂਟ**: ਪੂਰਾ Azure ਰਿਸੋਰਸ ਲਾਈਫਸਾਈਕਲ ਪ੍ਰਬੰਧਨ
- **🔐 ਪ੍ਰਮਾਣਿਕਤਾ**: DefaultAzureCredential ਅਤੇ managed identity ਪੈਟਰਨ
- **📦 ਸਟੋਰੇਜ ਸੇਵਾਵਾਂ**: Blob Storage, Queue Storage, ਅਤੇ Table Storage ਓਪਰੇਸ਼ਨ
- **🚀 ਕੰਟੇਨਰ ਸੇਵਾਵਾਂ**: Azure Container Apps, Container Instances, ਅਤੇ AKS ਪ੍ਰਬੰਧਨ
- **ਅਤੇ ਹੋਰ ਕਈ ਖਾਸ ਕਨੈਕਟਰ**

**ਅਸਲੀ ਦੁਨੀਆ ਵਿੱਚ ਵਰਤੋਂ**: "ਮੇਰੇ Azure ਸਟੋਰੇਜ ਖਾਤਿਆਂ ਦੀ ਸੂਚੀ ਬਣਾਓ", "ਪਿਛਲੇ ਘੰਟੇ ਵਿੱਚ ਮੇਰੇ Log Analytics ਵਰਕਸਪੇਸ ਵਿੱਚ ਗਲਤੀਆਂ ਦੀ ਪੁੱਛਗਿੱਛ ਕਰੋ", ਜਾਂ "ਮੈਨੂੰ Node.js ਨਾਲ ਸਹੀ ਪ੍ਰਮਾਣਿਕਤਾ ਵਰਤ ਕੇ Azure ਐਪਲੀਕੇਸ਼ਨ ਬਣਾਉਣ ਵਿੱਚ ਮਦਦ ਕਰੋ"

**ਪੂਰਾ ਡੈਮੋ ਸਿਨਾਰੀਓ**: ਇੱਥੇ ਇੱਕ ਪੂਰਾ ਵਾਕਫਲੋ ਹੈ ਜੋ ਦਿਖਾਉਂਦਾ ਹੈ ਕਿ ਕਿਵੇਂ Azure MCP ਨੂੰ GitHub Copilot for Azure ਐਕਸਟੈਂਸ਼ਨ ਨਾਲ VS Code ਵਿੱਚ ਮਿਲਾ ਕੇ ਸ਼ਕਤੀਸ਼ਾਲੀ ਨਤੀਜੇ ਮਿਲਦੇ ਹਨ। ਜਦੋਂ ਤੁਹਾਡੇ ਕੋਲ ਦੋਹਾਂ ਇੰਸਟਾਲ ਹੋਣ ਅਤੇ ਤੁਸੀਂ ਪ੍ਰੰਪਟ ਦਿੰਦੇ ਹੋ:

> "ਇੱਕ Python ਸਕ੍ਰਿਪਟ ਬਣਾਓ ਜੋ DefaultAzureCredential ਪ੍ਰਮਾਣਿਕਤਾ ਨਾਲ Azure Blob Storage ਵਿੱਚ ਫਾਇਲ ਅਪਲੋਡ ਕਰੇ। ਸਕ੍ਰਿਪਟ ਮੇਰੇ Azure ਸਟੋਰੇਜ ਖਾਤੇ 'mycompanystorage' ਨਾਲ ਜੁੜੇ, 'documents' ਨਾਂ ਦੇ ਕੰਟੇਨਰ ਵਿੱਚ ਅਪਲੋਡ ਕਰੇ, ਮੌਜੂਦਾ ਸਮੇਂ ਦੇ ਟਾਈਮਸਟੈਂਪ ਨਾਲ ਇੱਕ ਟੈਸਟ ਫਾਇਲ ਬਣਾਏ, ਗਲਤੀਆਂ ਨੂੰ ਸੁਚੱਜੇ ਢੰਗ ਨਾਲ ਸੰਭਾਲੇ ਅਤੇ ਜਾਣਕਾਰੀ ਭਰਪੂਰ ਆਉਟਪੁੱਟ ਦੇਵੇ, ਪ੍ਰਮਾਣਿਕਤਾ ਅਤੇ ਗਲਤੀ ਸੰਭਾਲਣ ਲਈ Azure ਦੀਆਂ ਸਭ ਤੋਂ ਵਧੀਆ ਪ੍ਰਥਾਵਾਂ ਦੀ ਪਾਲਣਾ ਕਰੇ, DefaultAzureCredential ਪ੍ਰਮਾਣਿਕਤਾ ਕਿਵੇਂ ਕੰਮ ਕਰਦੀ ਹੈ ਇਸ ਬਾਰੇ ਟਿੱਪਣੀਆਂ ਸ਼ਾਮਲ ਕਰੇ, ਅਤੇ ਸਕ੍ਰਿਪਟ ਨੂੰ ਢਾਂਚਾਬੱਧ ਅਤੇ ਵਧੀਆ ਫੰਕਸ਼ਨਾਂ ਅਤੇ ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਨਾਲ ਬਣਾਏ।"

Azure MCP Server ਇੱਕ ਪੂਰੀ, ਉਤਪਾਦਨ-ਤਿਆਰ Python ਸਕ੍ਰਿਪਟ ਤਿਆਰ ਕਰੇਗਾ ਜੋ:
- ਨਵੀਨਤਮ Azure Blob Storage SDK ਨੂੰ ਸਹੀ async ਪੈਟਰਨ ਨਾਲ ਵਰਤਦਾ ਹੈ
- DefaultAzureCredential ਨੂੰ ਵਿਆਪਕ fallback ਚੇਨ ਸਮਝਾਉਂਦੇ ਹੋਏ ਲਾਗੂ ਕਰਦਾ ਹੈ
- ਖਾਸ Azure exception ਕਿਸਮਾਂ ਨਾਲ ਮਜ਼ਬੂਤ ਗਲਤੀ ਸੰਭਾਲਣ ਸ਼ਾਮਲ ਕਰਦਾ ਹੈ
- Azure SDK ਦੀਆਂ ਸਭ ਤੋਂ ਵਧੀਆ ਪ੍ਰਥਾਵਾਂ ਦੀ ਪਾਲਣਾ ਕਰਦਾ ਹੈ ਜਿਵੇਂ ਕਿ ਰਿਸੋਰਸ ਮੈਨੇਜਮੈਂਟ ਅਤੇ ਕਨੈਕਸ਼ਨ ਸੰਭਾਲਣਾ
- ਵਿਸਥਾਰਪੂਰਕ ਲੌਗਿੰਗ ਅਤੇ ਜਾਣਕਾਰੀ ਭਰਪੂਰ ਕਨਸੋਲ ਆਉਟਪੁੱਟ ਦਿੰਦਾ ਹੈ
- ਫੰਕਸ਼ਨਾਂ, ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਅਤੇ ਟਾਈਪ ਹਿੰਟਸ ਨਾਲ ਢਾਂਚਾਬੱਧ ਸਕ੍ਰਿਪਟ ਬਣਾਉਂਦਾ ਹੈ

ਇਸ ਗੱਲ ਨੂੰ ਖਾਸ ਬਣਾਉਂਦਾ ਇਹ ਹੈ ਕਿ ਬਿਨਾਂ Azure MCP ਦੇ, ਤੁਹਾਨੂੰ ਜਨਰਲ ਬਲੌਬ ਸਟੋਰੇਜ ਕੋਡ ਮਿਲ ਸਕਦਾ ਹੈ ਜੋ ਕੰਮ ਕਰਦਾ ਹੈ ਪਰ ਮੌਜੂਦਾ Azure ਪੈਟਰਨ ਦੀ ਪਾਲਣਾ ਨਹੀਂ ਕਰਦਾ। Azure MCP ਨਾਲ, ਤੁਹਾਨੂੰ ਉਹ ਕੋਡ ਮਿਲਦਾ ਹੈ ਜੋ ਨਵੀਨਤਮ ਪ੍ਰਮਾਣਿਕਤਾ ਤਰੀਕਿਆਂ ਨੂੰ ਵਰਤਦਾ ਹੈ, Azure-ਖਾਸ ਗਲਤੀ ਸਥਿਤੀਆਂ ਨੂੰ ਸੰਭਾਲਦਾ ਹੈ, ਅਤੇ Microsoft ਦੀਆਂ ਸਿਫਾਰਸ਼ੀ ਪ੍ਰਥਾਵਾਂ ਦੀ ਪਾਲਣਾ ਕਰਦਾ ਹੈ।

**ਮਿਸਾਲ**: ਮੈਂ `az` ਅਤੇ `azd` CLI ਕਮਾਂਡਾਂ ਨੂੰ ਯਾਦ ਰੱਖਣ ਵਿੱਚ ਮੁਸ਼ਕਲ ਮਹਿਸੂਸ ਕਰਦਾ ਹਾਂ। ਮੇਰੇ ਲਈ ਇਹ ਹਮੇਸ਼ਾ ਦੋ ਕਦਮਾਂ ਦੀ ਪ੍ਰਕਿਰਿਆ ਹੁੰਦੀ ਹੈ: ਪਹਿਲਾਂ ਸਿੰਟੈਕਸ ਵੇਖਣਾ, ਫਿਰ ਕਮਾਂਡ ਚਲਾਉਣਾ। ਮੈਂ ਅਕਸਰ ਪੋਰਟਲ ਵਿੱਚ ਜਾ ਕੇ ਕਲਿੱਕ ਕਰਦਾ ਹਾਂ ਕਿਉਂਕਿ ਮੈਨੂੰ ਮੰਨਣਾ ਨਹੀਂ ਚਾਹੀਦਾ ਕਿ ਮੈਂ CLI ਸਿੰਟੈਕਸ ਨਹੀਂ ਯਾਦ ਰੱਖ ਸਕਦਾ। ਜੋ ਮੈਂ ਚਾਹੁੰਦਾ ਹਾਂ ਉਹ ਸਿੱਧਾ ਵਰਣਨ ਕਰ ਸਕਣਾ ਬਹੁਤ ਵਧੀਆ ਹੈ, ਅਤੇ IDE ਛੱਡੇ ਬਿਨਾਂ ਇਹ ਕਰ ਸਕਣਾ ਹੋਰ ਵੀ ਵਧੀਆ ਹੈ!

ਤੁਹਾਨੂੰ ਸ਼ੁਰੂਆਤ ਕਰਨ ਲਈ [Azure MCP repository](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) ਵਿੱਚ ਵਰਤੋਂ ਦੇ ਬਹੁਤ ਸਾਰੇ ਕੇਸ ਮਿਲਣਗੇ। ਵਿਸਥਾਰਪੂਰਕ ਸੈਟਅਪ ਗਾਈਡਾਂ ਅਤੇ ਅਡਵਾਂਸਡ ਕਨਫਿਗਰੇਸ਼ਨ ਵਿਕਲਪਾਂ ਲਈ, [ਅਧਿਕਾਰਿਕ Azure MCP ਦਸਤਾਵੇਜ਼](https://learn.microsoft.com/azure/developer/azure-mcp-server/) ਵੇਖੋ।

### 3. 🐙 GitHub MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: ਅਧਿਕਾਰਿਕ GitHub MCP Server GitHub ਦੇ ਪੂਰੇ ਪਰਿਵਾਰ ਨਾਲ ਬਿਨਾਂ ਰੁਕਾਵਟ ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਦਿੰਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਹੋਸਟ ਕੀਤੇ ਰਿਮੋਟ ਪਹੁੰਚ ਅਤੇ ਲੋਕਲ Docker ਡਿਪਲੋਇਮੈਂਟ ਵਿਕਲਪ ਸ਼ਾਮਲ ਹਨ। ਇਹ ਸਿਰਫ ਬੁਨਿਆਦੀ ਰਿਪੋਜ਼ਟਰੀ ਓਪਰੇਸ਼ਨਾਂ ਬਾਰੇ ਨਹੀਂ ਹੈ – ਇਹ ਇੱਕ ਵਿਆਪਕ ਟੂਲਕਿਟ ਹੈ ਜਿਸ ਵਿੱਚ GitHub Actions ਪ੍ਰਬੰਧਨ, ਪੁਲ ਰਿਕਵੇਸਟ ਵਰਕਫਲੋ, ਇਸ਼ੂ ਟ੍ਰੈਕਿੰਗ, ਸੁਰੱਖਿਆ ਸਕੈਨਿੰਗ, ਸੂਚਨਾਵਾਂ ਅਤੇ ਅਡਵਾਂਸਡ ਆਟੋਮੇਸ਼ਨ ਸਮਰੱਥਾਵਾਂ ਸ਼ਾਮਲ ਹਨ।

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: ਇਹ ਸਰਵਰ GitHub ਨਾਲ ਤੁਹਾਡੇ ਇੰਟਰੈਕਸ਼ਨ ਨੂੰ ਬਦਲ ਦਿੰਦਾ ਹੈ, ਪੂਰੇ ਪਲੇਟਫਾਰਮ ਦਾ ਅਨੁਭਵ ਸਿੱਧਾ ਤੁਹਾਡੇ ਵਿਕਾਸ ਵਾਤਾਵਰਣ ਵਿੱਚ ਲਿਆਉਂਦਾ ਹੈ। VS Code ਅਤੇ GitHub.com ਵਿਚਕਾਰ ਲਗਾਤਾਰ ਬਦਲਣ ਦੀ ਥਾਂ, ਤੁਸੀਂ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਕਮਾਂਡਾਂ ਰਾਹੀਂ ਸਾਰਾ ਕੰਮ ਕਰ ਸਕਦੇ ਹੋ ਅਤੇ ਆਪਣੇ ਕੋਡ 'ਤੇ ਧਿਆਨ ਕੇਂਦਰਿਤ ਰੱਖ ਸਕਦੇ ਹੋ।

> **ℹ️ ਨੋਟ: ਵੱਖ-ਵੱਖ ਕਿਸਮਾਂ ਦੇ 'Agents'**
> 
> ਇਸ GitHub MCP Server ਨੂੰ GitHub ਦੇ Coding Agent (ਜੋ AI ਏਜੰਟ ਹੈ ਜਿਸਨੂੰ ਆਟੋਮੇਟਿਕ ਕੋਡਿੰਗ ਟਾਸਕ ਲਈ ਇਸ਼ੂਜ਼ ਸੌਂਪੇ ਜਾਂਦੇ ਹਨ) ਨਾਲ ਗਲਤ ਨਾ ਸਮਝੋ। GitHub MCP Server VS Code ਦੇ Agent ਮੋਡ ਵਿੱਚ GitHub API ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਦਿੰਦਾ ਹੈ, ਜਦਕਿ GitHub ਦਾ Coding Agent ਇੱਕ ਵੱਖਰਾ ਫੀਚਰ ਹੈ ਜੋ GitHub ਇਸ਼ੂਜ਼ ਨੂੰ ਸੌਂਪੇ ਜਾਣ 'ਤੇ ਪੁਲ ਰਿਕਵੇਸਟ ਬਣਾਉਂਦਾ ਹੈ।

**ਮੁੱਖ ਸਮਰੱਥਾਵਾਂ ਸ਼ਾਮਲ ਹਨ**:
- **⚙️ GitHub Actions**: ਪੂਰੀ CI/CD ਪਾਈਪਲਾਈਨ ਪ੍ਰਬੰਧਨ, ਵਰਕਫਲੋ ਮਾਨੀਟਰਿੰਗ, ਅਤੇ ਆਰਟੀਫੈਕਟ ਹੈਂਡਲਿੰਗ
- **🔀 ਪੁਲ ਰਿਕਵੇਸਟ**: ਬਣਾਉਣਾ, ਸਮੀਖਿਆ ਕਰਨਾ, ਮਰਜ ਕਰਨਾ, ਅਤੇ PRs ਦਾ ਪ੍ਰਬੰਧਨ ਵਿਸਥਾਰਪੂਰਕ ਸਥਿਤੀ ਟ੍ਰੈਕਿੰਗ ਨਾਲ
- **🐛 ਇਸ਼ੂਜ਼**: ਪੂਰਾ ਇਸ਼ੂ ਲਾਈਫਸਾਈਕਲ ਪ੍ਰਬੰਧਨ, ਟਿੱਪਣੀਆਂ, ਲੇਬਲਿੰਗ, ਅਤੇ ਅਸਾਈਨਮੈਂਟ
- **🔒 ਸੁਰੱਖਿਆ**: ਕੋਡ ਸਕੈਨਿੰਗ ਅਲਰਟ, ਸੀਕ੍ਰੇਟ ਡਿਟੈਕਸ਼ਨ, ਅਤੇ Dependabot ਇੰਟੀਗ੍ਰੇਸ਼ਨ
- **🔔 ਸੂਚਨਾਵਾਂ**: ਸਮਾਰਟ ਸੂਚਨਾ ਪ੍ਰਬੰਧਨ ਅਤੇ ਰਿਪੋਜ਼ਟਰੀ ਸਬਸਕ੍ਰਿਪਸ਼ਨ ਕੰਟਰੋਲ
- **📁 ਰਿਪੋਜ਼ਟਰੀ ਪ੍ਰਬੰਧਨ**: ਫਾਇਲ ਓਪਰੇਸ਼ਨ, ਬ੍ਰਾਂਚ ਪ੍ਰਬੰਧਨ, ਅਤੇ ਰਿਪੋਜ਼ਟਰੀ ਪ੍ਰਸ਼ਾਸਨ
- **👥 ਸਹਿਯੋਗ**: ਯੂਜ਼ਰ ਅਤੇ ਸੰਗਠਨ ਖੋਜ, ਟੀਮ ਪ੍ਰਬੰਧਨ, ਅਤੇ ਪਹੁੰਚ ਕੰਟਰੋਲ

**ਅਸਲੀ ਦੁਨੀਆ ਵਿੱਚ ਵਰਤੋਂ**: "ਮੇਰੀ ਫੀਚਰ ਬ੍ਰਾਂਚ ਤੋਂ ਪੁਲ ਰਿਕਵੇਸਟ ਬਣਾਓ", "ਇਸ ਹਫ਼ਤੇ ਸਾਰੇ ਫੇਲ ਹੋਏ CI ਰਨ ਦਿਖਾਓ", "ਮੇਰੇ ਰਿਪੋਜ਼ਟਰੀਜ਼ ਲਈ ਖੁੱਲ੍ਹੇ ਸੁਰੱਖਿਆ ਅਲਰਟਾਂ ਦੀ ਸੂਚੀ ਦਿਖਾਓ", ਜਾਂ "ਮੇਰੇ ਸੰਗਠਨਾਂ ਵਿੱਚ ਮੈਨੂੰ ਸੌਂਪੇ ਗਏ ਸਾਰੇ ਇਸ਼ੂਜ਼ ਲੱਭੋ"

**ਪੂਰਾ ਡੈਮੋ ਸਿਨਾਰੀਓ**: ਇੱਥੇ ਇੱਕ ਸ਼ਕਤੀਸ਼ਾਲੀ ਵਰਕਫਲੋ ਹੈ ਜੋ GitHub MCP Server ਦੀਆਂ ਸਮਰੱਥਾਵਾਂ ਦਿਖਾਉਂਦਾ ਹੈ:

> "ਮੈਨੂੰ ਸਾਡੇ ਸਪ੍ਰਿੰਟ ਰਿਵਿਊ ਦੀ ਤਿਆਰੀ ਕਰਨੀ ਹੈ। ਇਸ ਹਫ਼ਤੇ ਮੈਂ ਜੋ ਸਾਰੇ ਪੁਲ ਰਿਕਵੇਸਟ ਬਣਾਏ ਹਨ ਦਿਖਾਓ, ਸਾਡੇ CI/CD ਪਾਈਪਲਾਈਨਾਂ ਦੀ ਸਥਿਤੀ ਚੈੱਕ ਕਰੋ, ਕਿਸੇ ਵੀ ਸੁਰੱਖਿਆ ਅਲਰਟਾਂ ਦਾ ਸਾਰ ਬਣਾਓ ਜੋ ਸਾਨੂੰ ਹੱਲ ਕਰਨੀਆਂ ਹਨ, ਅਤੇ 'feature' ਲੇਬਲ ਵਾਲੇ ਮਰਜ ਕੀਤੇ PRs ਦੇ ਆਧਾਰ 'ਤੇ ਰਿਲੀਜ਼ ਨੋਟਸ ਤਿਆਰ ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰੋ।"

GitHub MCP Server:
- ਤੁਹਾਡੇ ਹਾਲੀਆ ਪੁਲ ਰਿਕਵੇਸਟਾਂ ਨੂੰ ਵਿਸਥਾਰਪੂਰਕ ਸਥਿਤੀ ਜਾਣਕਾਰੀ ਨਾਲ ਪੁੱਛਗਿੱਛ ਕਰੇਗਾ
- ਵਰਕਫਲੋ ਰਨਜ਼ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੇਗਾ ਅਤੇ ਕਿਸੇ ਵੀ ਫੇਲਿਅਰ ਜਾਂ ਪ੍ਰਦਰਸ਼ਨ ਸਮੱਸਿਆਵਾਂ ਨੂੰ ਹਾਈਲਾਈਟ ਕਰੇਗਾ
- ਸੁਰੱਖਿਆ ਸਕੈਨਿੰਗ ਨਤੀਜੇ ਇਕੱਠੇ ਕਰਕੇ ਅਹਿਮ ਅਲਰਟਾਂ ਨੂੰ ਤਰਜੀਹ ਦੇਵੇਗਾ
- ਮਰਜ ਕੀਤੇ PRs ਤੋਂ ਜਾਣਕਾਰੀ ਕੱਢ ਕੇ ਵਿਸਥਾਰਪੂਰਕ ਰਿਲੀਜ਼ ਨੋਟਸ ਤਿਆਰ ਕਰੇਗਾ
- ਸਪ੍ਰਿੰਟ ਯੋਜਨਾ ਅਤੇ ਰਿਲੀਜ਼ ਤਿਆਰੀ ਲਈ ਕਾਰਗਰ ਅਗਲੇ ਕਦਮ ਦਿੰਦਾ ਹੈ

**ਮਿਸਾਲ**: ਮੈਂ ਕੋਡ ਸਮੀਖਿਆ ਵਰਕਫਲੋਜ਼ ਲਈ ਇਸਨੂੰ ਬਹੁਤ ਪਸੰਦ ਕਰਦਾ ਹਾਂ। VS Code, GitHub ਸੂਚਨਾਵਾਂ ਅਤੇ ਪੁਲ ਰਿਕਵੇਸਟ ਪੰਨਿਆਂ ਵਿਚਕਾਰ ਜੰਪ ਕਰਨ ਦੀ ਥਾਂ, ਮੈਂ ਕਹਿ ਸਕਦਾ ਹਾਂ "ਮੇਰੇ ਸਮੀਖਿਆ ਲਈ ਸਾਰੇ PRs ਦਿਖਾਓ" ਅਤੇ ਫਿਰ "PR #123 ਵਿੱਚ ਪ੍ਰਮਾਣਿਕਤਾ ਵਿਧੀ ਵਿੱਚ ਗਲਤੀ ਸੰਭਾਲਣ ਬਾਰੇ ਟਿੱਪਣੀ ਜੋੜੋ।" ਸਰਵਰ GitHub API ਕਾਲਾਂ ਨੂੰ ਸੰਭਾਲਦਾ ਹੈ, ਗੱਲਬਾਤ ਦਾ ਸੰਦਰਭ ਰੱਖਦਾ ਹੈ, ਅਤੇ ਮੈਨੂੰ ਹੋਰ ਰਚਨਾਤਮਕ ਸਮੀਖਿਆ ਟਿੱਪਣੀਆਂ ਬਣਾਉਣ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹੈ।

**ਪ੍ਰਮਾਣਿਕਤਾ ਵਿਕਲਪ**: ਸਰਵਰ OAuth (VS Code ਵਿੱਚ ਬਿਨਾਂ ਰੁਕਾਵਟ) ਅਤੇ Personal Access Tokens ਦੋਹਾਂ ਨੂੰ ਸਹਿਯੋਗ ਦਿੰਦਾ ਹੈ, ਜਿਸ ਨਾਲ ਤੁਸੀਂ ਸਿਰਫ ਉਹੀ GitHub ਫੰਕਸ਼ਨਲਿਟੀ ਚਾਲੂ ਕਰ ਸਕਦੇ ਹੋ ਜੋ ਤੁਹਾਨੂੰ ਚਾਹੀਦੀ ਹੈ। ਤੁਸੀਂ ਇਸਨੂੰ ਤੁਰੰਤ ਸੈਟਅਪ ਲਈ ਰਿਮੋਟ ਹੋਸਟ ਕੀਤੇ
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: MarkItDown ਇੱਕ ਵਿਸਤ੍ਰਿਤ ਦਸਤਾਵੇਜ਼ ਰੂਪਾਂਤਰਣ ਸਰਵਰ ਹੈ ਜੋ ਵੱਖ-ਵੱਖ ਫਾਇਲ ਫਾਰਮੈਟਾਂ ਨੂੰ ਉੱਚ-ਗੁਣਵੱਤਾ ਵਾਲੇ Markdown ਵਿੱਚ ਬਦਲਦਾ ਹੈ, ਜੋ LLM ਖਪਤ ਅਤੇ ਟੈਕਸਟ ਵਿਸ਼ਲੇਸ਼ਣ ਵਰਕਫਲੋਜ਼ ਲਈ ਅਨੁਕੂਲਿਤ ਹੈ।

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: ਆਧੁਨਿਕ ਦਸਤਾਵੇਜ਼ੀ ਵਰਕਫਲੋਜ਼ ਲਈ ਬਹੁਤ ਜ਼ਰੂਰੀ! MarkItDown ਕਈ ਫਾਇਲ ਫਾਰਮੈਟਾਂ ਨੂੰ ਸੰਭਾਲਦਾ ਹੈ ਅਤੇ ਮਹੱਤਵਪੂਰਨ ਦਸਤਾਵੇਜ਼ੀ ਢਾਂਚਾ ਜਿਵੇਂ ਕਿ ਸਿਰਲੇਖ, ਸੂਚੀਆਂ, ਟੇਬਲਾਂ ਅਤੇ ਲਿੰਕਾਂ ਨੂੰ ਬਰਕਰਾਰ ਰੱਖਦਾ ਹੈ। ਸਧਾਰਣ ਟੈਕਸਟ ਨਿਕਾਸ ਟੂਲਾਂ ਦੇ ਵਿਰੁੱਧ, ਇਹ ਸੈਮਾਂਟਿਕ ਮਾਇਨੇ ਅਤੇ ਫਾਰਮੈਟਿੰਗ ਨੂੰ ਬਰਕਰਾਰ ਰੱਖਣ 'ਤੇ ਧਿਆਨ ਦਿੰਦਾ ਹੈ ਜੋ AI ਪ੍ਰੋਸੈਸਿੰਗ ਅਤੇ ਮਨੁੱਖੀ ਪੜ੍ਹਨਯੋਗਤਾ ਦੋਹਾਂ ਲਈ ਕੀਮਤੀ ਹੈ।

**ਸਮਰਥਿਤ ਫਾਇਲ ਫਾਰਮੈਟ**:
- **ਆਫਿਸ ਦਸਤਾਵੇਜ਼**: PDF, PowerPoint (PPTX), Word (DOCX), Excel (XLSX/XLS)
- **ਮੀਡੀਆ ਫਾਇਲਾਂ**: ਚਿੱਤਰ (EXIF ਮੈਟਾਡੇਟਾ ਅਤੇ OCR ਨਾਲ), ਆਡੀਓ (EXIF ਮੈਟਾਡੇਟਾ ਅਤੇ ਬੋਲਣ ਦੀ ਟ੍ਰਾਂਸਕ੍ਰਿਪਸ਼ਨ ਨਾਲ)
- **ਵੈੱਬ ਸਮੱਗਰੀ**: HTML, RSS ਫੀਡ, YouTube URLs, Wikipedia ਪੰਨੇ
- **ਡਾਟਾ ਫਾਰਮੈਟ**: CSV, JSON, XML, ZIP ਫਾਇਲਾਂ (ਮੁੜ-ਮੁੜ ਸਮੱਗਰੀ ਨੂੰ ਪ੍ਰੋਸੈਸ ਕਰਦਾ ਹੈ)
- **ਪਬਲਿਸ਼ਿੰਗ ਫਾਰਮੈਟ**: EPub, Jupyter ਨੋਟਬੁੱਕ (.ipynb)
- **ਈਮੇਲ**: Outlook ਸੁਨੇਹੇ (.msg)
- **ਉੱਨਤ**: Azure Document Intelligence ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਨਾਲ ਸੁਧਾਰਿਆ PDF ਪ੍ਰੋਸੈਸਿੰਗ

**ਉੱਨਤ ਸਮਰੱਥਾਵਾਂ**: MarkItDown LLM-ਚਲਿਤ ਚਿੱਤਰ ਵਰਣਨਾਂ (ਜਦੋਂ OpenAI ਕਲਾਇੰਟ ਦਿੱਤਾ ਗਿਆ ਹੋਵੇ), Azure Document Intelligence ਨਾਲ ਸੁਧਾਰਿਆ PDF ਪ੍ਰੋਸੈਸਿੰਗ, ਬੋਲਣ ਸਮੱਗਰੀ ਲਈ ਆਡੀਓ ਟ੍ਰਾਂਸਕ੍ਰਿਪਸ਼ਨ, ਅਤੇ ਵਾਧੂ ਫਾਇਲ ਫਾਰਮੈਟਾਂ ਲਈ ਪਲੱਗਇਨ ਸਿਸਟਮ ਨੂੰ ਸਮਰਥਨ ਦਿੰਦਾ ਹੈ।

**ਅਸਲੀ ਦੁਨੀਆ ਵਿੱਚ ਵਰਤੋਂ**: "ਇਸ PowerPoint ਪ੍ਰਜ਼ੈਂਟੇਸ਼ਨ ਨੂੰ ਸਾਡੇ ਦਸਤਾਵੇਜ਼ੀ ਸਾਈਟ ਲਈ Markdown ਵਿੱਚ ਬਦਲੋ", "ਇਸ PDF ਤੋਂ ਸਹੀ ਸਿਰਲੇਖ ਢਾਂਚੇ ਨਾਲ ਟੈਕਸਟ ਨਿਕਾਲੋ", ਜਾਂ "ਇਸ Excel ਸਪ੍ਰੈਡਸ਼ੀਟ ਨੂੰ ਪੜ੍ਹਨਯੋਗ ਟੇਬਲ ਫਾਰਮੈਟ ਵਿੱਚ ਬਦਲੋ"

**ਮੁੱਖ ਉਦਾਹਰਨ**: [MarkItDown docs](https://github.com/microsoft/markitdown#why-markdown) ਤੋਂ ਹਵਾਲਾ:

> Markdown ਸਧਾਰਣ ਟੈਕਸਟ ਦੇ ਬਹੁਤ ਨੇੜੇ ਹੈ, ਜਿਸ ਵਿੱਚ ਘੱਟੋ-ਘੱਟ ਮਾਰਕਅੱਪ ਜਾਂ ਫਾਰਮੈਟਿੰਗ ਹੁੰਦੀ ਹੈ, ਪਰ ਫਿਰ ਵੀ ਇਹ ਮਹੱਤਵਪੂਰਨ ਦਸਤਾਵੇਜ਼ੀ ਢਾਂਚੇ ਨੂੰ ਦਰਸਾਉਂਦਾ ਹੈ। ਮੁੱਖ ਧਾਰਾ LLMs, ਜਿਵੇਂ OpenAI ਦਾ GPT-4o, ਕੁਦਰਤੀ ਤੌਰ 'ਤੇ Markdown "ਬੋਲਦੇ" ਹਨ, ਅਤੇ ਅਕਸਰ ਬਿਨਾਂ ਪੁੱਛੇ ਆਪਣੇ ਜਵਾਬਾਂ ਵਿੱਚ Markdown ਸ਼ਾਮਲ ਕਰਦੇ ਹਨ। ਇਹ ਦਰਸਾਉਂਦਾ ਹੈ ਕਿ ਉਹ ਵੱਡੀ ਮਾਤਰਾ ਵਿੱਚ Markdown-ਫਾਰਮੈਟ ਕੀਤੇ ਟੈਕਸਟ 'ਤੇ ਟ੍ਰੇਨ ਕੀਤੇ ਗਏ ਹਨ ਅਤੇ ਇਸਨੂੰ ਚੰਗੀ ਤਰ੍ਹਾਂ ਸਮਝਦੇ ਹਨ। ਇੱਕ ਸਾਈਡ ਲਾਭ ਵਜੋਂ, Markdown ਰਿਵਾਜ਼ ਵੀ ਬਹੁਤ ਟੋਕਨ-ਕੁਸ਼ਲ ਹਨ।

MarkItDown ਦਸਤਾਵੇਜ਼ੀ ਢਾਂਚੇ ਨੂੰ ਬਰਕਰਾਰ ਰੱਖਣ ਵਿੱਚ ਬਹੁਤ ਵਧੀਆ ਹੈ, ਜੋ AI ਵਰਕਫਲੋਜ਼ ਲਈ ਮਹੱਤਵਪੂਰਨ ਹੈ। ਉਦਾਹਰਨ ਵਜੋਂ, ਜਦੋਂ PowerPoint ਪ੍ਰਜ਼ੈਂਟੇਸ਼ਨ ਨੂੰ ਬਦਲਿਆ ਜਾਂਦਾ ਹੈ, ਇਹ ਸਲਾਈਡਾਂ ਦੀ ਸੰਗਠਨਾ ਨੂੰ ਸਹੀ ਸਿਰਲੇਖਾਂ ਨਾਲ ਰੱਖਦਾ ਹੈ, ਟੇਬਲਾਂ ਨੂੰ Markdown ਟੇਬਲਾਂ ਵਜੋਂ ਨਿਕਾਲਦਾ ਹੈ, ਚਿੱਤਰਾਂ ਲਈ alt ਟੈਕਸਟ ਸ਼ਾਮਲ ਕਰਦਾ ਹੈ, ਅਤੇ ਸਪੀਕਰ ਨੋਟਸ ਨੂੰ ਵੀ ਪ੍ਰੋਸੈਸ ਕਰਦਾ ਹੈ। ਚਾਰਟਾਂ ਨੂੰ ਪੜ੍ਹਨਯੋਗ ਡਾਟਾ ਟੇਬਲਾਂ ਵਿੱਚ ਬਦਲਿਆ ਜਾਂਦਾ ਹੈ, ਅਤੇ ਨਤੀਜੇ ਵਜੋਂ ਬਣਿਆ Markdown ਮੂਲ ਪ੍ਰਜ਼ੈਂਟੇਸ਼ਨ ਦੇ ਤਰਕਸ਼ੀਲ ਪ੍ਰਵਾਹ ਨੂੰ ਬਰਕਰਾਰ ਰੱਖਦਾ ਹੈ। ਇਹ AI ਸਿਸਟਮਾਂ ਵਿੱਚ ਪ੍ਰਜ਼ੈਂਟੇਸ਼ਨ ਸਮੱਗਰੀ ਭਰਨ ਜਾਂ ਮੌਜੂਦਾ ਸਲਾਈਡਾਂ ਤੋਂ ਦਸਤਾਵੇਜ਼ ਬਣਾਉਣ ਲਈ ਬਹੁਤ ਉਚਿਤ ਬਣਾਉਂਦਾ ਹੈ।

### 6. 🗃️ SQL Server MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: SQL Server ਡੇਟਾਬੇਸ (ਆਨ-ਪ੍ਰੇਮਾਈਸ, Azure SQL ਜਾਂ Fabric) ਲਈ ਗੱਲਬਾਤੀ ਪਹੁੰਚ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: PostgreSQL ਸਰਵਰ ਵਾਂਗ ਹੀ ਪਰ Microsoft SQL ਪਰਿਵਾਰ ਲਈ। ਸਧਾਰਣ ਕਨੈਕਸ਼ਨ ਸਟਰਿੰਗ ਨਾਲ ਜੁੜੋ ਅਤੇ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਨਾਲ ਕਵੈਰੀਆਂ ਸ਼ੁਰੂ ਕਰੋ – ਹੁਣ ਹੋਰ ਸੰਦਰਭ ਬਦਲਣ ਦੀ ਲੋੜ ਨਹੀਂ!

**ਅਸਲੀ ਦੁਨੀਆ ਵਿੱਚ ਵਰਤੋਂ**: "ਪਿਛਲੇ 30 ਦਿਨਾਂ ਵਿੱਚ ਜਿਹੜੇ ਆਰਡਰ ਪੂਰੇ ਨਹੀਂ ਹੋਏ ਉਹ ਸਾਰੇ ਲੱਭੋ" ਨੂੰ ਸਹੀ SQL ਕਵੈਰੀਆਂ ਵਿੱਚ ਬਦਲ ਕੇ ਫਾਰਮੈਟ ਕੀਤੇ ਨਤੀਜੇ ਵਾਪਸ ਕਰਦਾ ਹੈ

**ਮੁੱਖ ਉਦਾਹਰਨ**: ਜਦੋਂ ਤੁਸੀਂ ਆਪਣਾ ਡੇਟਾਬੇਸ ਕਨੈਕਸ਼ਨ ਸੈੱਟ ਕਰ ਲੈਂਦੇ ਹੋ, ਤਾਂ ਤੁਸੀਂ ਤੁਰੰਤ ਆਪਣੇ ਡਾਟਾ ਨਾਲ ਗੱਲਬਾਤ ਕਰ ਸਕਦੇ ਹੋ। ਬਲੌਗ ਪੋਸਟ ਇਸਨੂੰ ਇੱਕ ਸਧਾਰਣ ਸਵਾਲ ਨਾਲ ਦਿਖਾਉਂਦੀ ਹੈ: "ਤੁਸੀਂ ਕਿਸ ਡੇਟਾਬੇਸ ਨਾਲ ਜੁੜੇ ਹੋ?" MCP ਸਰਵਰ ਸਹੀ ਡੇਟਾਬੇਸ ਟੂਲ ਨੂੰ ਕਾਲ ਕਰਦਾ ਹੈ, ਤੁਹਾਡੇ SQL Server ਇੰਸਟੈਂਸ ਨਾਲ ਜੁੜਦਾ ਹੈ, ਅਤੇ ਤੁਹਾਡੇ ਮੌਜੂਦਾ ਡੇਟਾਬੇਸ ਕਨੈਕਸ਼ਨ ਬਾਰੇ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰਦਾ ਹੈ – ਬਿਨਾਂ ਕੋਈ SQL ਲਾਈਨ ਲਿਖੇ। ਸਰਵਰ ਸਕੀਮਾ ਪ੍ਰਬੰਧਨ ਤੋਂ ਲੈ ਕੇ ਡਾਟਾ ਮੈਨਿਪੂਲੇਸ਼ਨ ਤੱਕ ਦੇ ਵਿਸਤ੍ਰਿਤ ਡੇਟਾਬੇਸ ਓਪਰੇਸ਼ਨਾਂ ਨੂੰ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਪ੍ਰੰਪਟਾਂ ਰਾਹੀਂ ਸਮਰਥਨ ਦਿੰਦਾ ਹੈ। VS Code ਅਤੇ Claude Desktop ਨਾਲ ਪੂਰੀ ਸੈਟਅਪ ਹਦਾਇਤਾਂ ਅਤੇ ਸੰਰਚਨਾ ਉਦਾਹਰਨਾਂ ਲਈ ਵੇਖੋ: [Introducing MSSQL MCP Server (Preview)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/)।

### 7. 🎭 Playwright MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: AI ਏਜੰਟਾਂ ਨੂੰ ਵੈੱਬ ਪੰਨਿਆਂ ਨਾਲ ਟੈਸਟਿੰਗ ਅਤੇ ਆਟੋਮੇਸ਼ਨ ਲਈ ਇੰਟਰੈਕਟ ਕਰਨ ਦੇ ਯੋਗ ਬਣਾਉਂਦਾ ਹੈ

> **ℹ️ GitHub Copilot ਨੂੰ ਤਾਕਤ ਦਿੰਦਾ ਹੈ**
> 
> Playwright MCP Server GitHub Copilot ਦੇ ਕੋਡਿੰਗ ਏਜੰਟ ਨੂੰ ਤਾਕਤ ਦਿੰਦਾ ਹੈ, ਜਿਸ ਨਾਲ ਇਸਨੂੰ ਵੈੱਬ ਬ੍ਰਾਊਜ਼ਿੰਗ ਸਮਰੱਥਾ ਮਿਲਦੀ ਹੈ! [ਇਸ ਫੀਚਰ ਬਾਰੇ ਹੋਰ ਜਾਣੋ](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/)।

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਵਰਣਨਾਂ ਨਾਲ ਚਲਾਈ ਜਾਣ ਵਾਲੀ ਆਟੋਮੇਟਿਕ ਟੈਸਟਿੰਗ ਲਈ ਬਹੁਤ ਵਧੀਆ। AI ਵੈੱਬਸਾਈਟਾਂ 'ਤੇ ਨੈਵੀਗੇਟ ਕਰ ਸਕਦਾ ਹੈ, ਫਾਰਮ ਭਰ ਸਕਦਾ ਹੈ, ਅਤੇ ਸੰਗਠਿਤ ਐਕਸੈਸੀਬਿਲਿਟੀ ਸਨੈਪਸ਼ਾਟਾਂ ਰਾਹੀਂ ਡਾਟਾ ਨਿਕਾਲ ਸਕਦਾ ਹੈ – ਇਹ ਬਹੁਤ ਹੀ ਸ਼ਕਤੀਸ਼ਾਲੀ ਗੱਲ ਹੈ!

**ਅਸਲੀ ਦੁਨੀਆ ਵਿੱਚ ਵਰਤੋਂ**: "ਲੌਗਿਨ ਪ੍ਰਕਿਰਿਆ ਦੀ ਜਾਂਚ ਕਰੋ ਅਤੇ ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਡੈਸ਼ਬੋਰਡ ਸਹੀ ਤਰ੍ਹਾਂ ਲੋਡ ਹੁੰਦਾ ਹੈ" ਜਾਂ "ਇੱਕ ਟੈਸਟ ਬਣਾਓ ਜੋ ਉਤਪਾਦਾਂ ਦੀ ਖੋਜ ਕਰਦਾ ਹੈ ਅਤੇ ਨਤੀਜਿਆਂ ਵਾਲੇ ਪੰਨੇ ਦੀ ਪੁਸ਼ਟੀ ਕਰਦਾ ਹੈ" – ਇਹ ਸਭ ਬਿਨਾਂ ਐਪਲੀਕੇਸ਼ਨ ਦੇ ਸੋਰਸ ਕੋਡ ਦੀ ਲੋੜ ਦੇ

**ਮੁੱਖ ਉਦਾਹਰਨ**: ਮੇਰੀ ਸਾਥੀ Debbie O'Brien ਨੇ ਹਾਲ ਹੀ ਵਿੱਚ Playwright MCP Server ਨਾਲ ਬਹੁਤ ਵਧੀਆ ਕੰਮ ਕੀਤਾ ਹੈ! ਉਦਾਹਰਨ ਵਜੋਂ, ਉਸਨੇ ਦਿਖਾਇਆ ਕਿ ਤੁਸੀਂ ਐਪਲੀਕੇਸ਼ਨ ਦੇ ਸੋਰਸ ਕੋਡ ਤੱਕ ਪਹੁੰਚ ਨਾ ਹੋਣ ਦੇ ਬਾਵਜੂਦ ਪੂਰੇ Playwright ਟੈਸਟ ਜਨਰੇਟ ਕਰ ਸਕਦੇ ਹੋ। ਉਸਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਉਸਨੇ Copilot ਨੂੰ ਇੱਕ ਮੂਵੀ ਖੋਜ ਐਪ ਲਈ ਟੈਸਟ ਬਣਾਉਣ ਲਈ ਕਿਹਾ: ਸਾਈਟ 'ਤੇ ਜਾਓ, "Garfield" ਖੋਜੋ, ਅਤੇ ਨਤੀਜਿਆਂ ਵਿੱਚ ਮੂਵੀ ਦੀ ਮੌਜੂਦਗੀ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ। MCP ਨੇ ਬ੍ਰਾਊਜ਼ਰ ਸੈਸ਼ਨ ਸ਼ੁਰੂ ਕੀਤਾ, DOM ਸਨੈਪਸ਼ਾਟਾਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਪੰਨੇ ਦੇ ਢਾਂਚੇ ਦੀ ਜਾਂਚ ਕੀਤੀ, ਸਹੀ ਸਿਲੈਕਟਰ ਲੱਭੇ, ਅਤੇ ਪਹਿਲੀ ਕੋਸ਼ਿਸ਼ ਵਿੱਚ ਪਾਸ ਹੋਣ ਵਾਲਾ ਪੂਰਾ TypeScript ਟੈਸਟ ਤਿਆਰ ਕੀਤਾ।

ਇਸਨੂੰ ਬਹੁਤ ਸ਼ਕਤੀਸ਼ਾਲੀ ਬਣਾਉਂਦਾ ਹੈ ਕਿ ਇਹ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਦੇ ਹੁਕਮਾਂ ਅਤੇ ਚਲਾਏ ਜਾ ਸਕਣ ਵਾਲੇ ਟੈਸਟ ਕੋਡ ਵਿਚਕਾਰ ਪੁਲ ਬਣਾਉਂਦਾ ਹੈ। ਰਵਾਇਤੀ ਤਰੀਕੇ ਜਾਂ ਤਾਂ ਮੈਨੂਅਲ ਟੈਸਟ ਲਿਖਣ ਜਾਂ ਸੰਦਰਭ ਲਈ ਕੋਡਬੇਸ ਤੱਕ ਪਹੁੰਚ ਦੀ ਲੋੜ ਰੱਖਦੇ ਹਨ। ਪਰ Playwright MCP ਨਾਲ, ਤੁਸੀਂ ਬਾਹਰੀ ਸਾਈਟਾਂ, ਕਲਾਇੰਟ ਐਪਲੀਕੇਸ਼ਨਾਂ ਜਾਂ ਬਲੈਕ-ਬਾਕਸ ਟੈਸਟਿੰਗ ਸੰਦਰਭਾਂ ਵਿੱਚ ਟੈਸਟ ਕਰ ਸਕਦੇ ਹੋ ਜਿੱਥੇ ਕੋਡ ਪਹੁੰਚ ਉਪਲਬਧ ਨਹੀਂ ਹੁੰਦੀ।

### 8. 💻 Dev Box MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=
IMPORTANT RULES:  
1. ਅਨੁਵਾਦ ਦੇ ਆਲੇ-ਦੁਆਲੇ '''markdown ਜਾਂ ਹੋਰ ਕਿਸੇ ਟੈਗ ਨੂੰ ਨਾ ਜੋੜੋ  
2. ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਅਨੁਵਾਦ ਬਹੁਤ ਜ਼ਿਆਦਾ ਸ਼ਾਬਦਿਕ ਨਾ ਲੱਗੇ  
3. ਟਿੱਪਣੀਆਂ ਦਾ ਵੀ ਅਨੁਵਾਦ ਕਰੋ  
4. ਇਹ ਫਾਇਲ Markdown ਫਾਰਮੈਟ ਵਿੱਚ ਹੈ - ਇਸਨੂੰ XML ਜਾਂ HTML ਵਾਂਗ ਨਾ ਸਮਝੋ  
5. ਅਨੁਵਾਦ ਨਾ ਕਰੋ:  
   - [!NOTE], [!WARNING], [!TIP], [!IMPORTANT], [!CAUTION]  
   - ਵੈਰੀਏਬਲ ਨਾਮ, ਫੰਕਸ਼ਨ ਨਾਮ, ਕਲਾਸ ਨਾਮ  
   - ਜਿਹੜੇ ਪਲੇਸਹੋਲਡਰ ਹਨ ਜਿਵੇਂ @@INLINE_CODE_x@@ ਜਾਂ @@CODE_BLOCK_x@@  
   - URLs ਜਾਂ ਪਾਥ  
6. ਸਾਰੇ ਮੂਲ markdown ਫਾਰਮੈਟਿੰਗ ਨੂੰ ਬਰਕਰਾਰ ਰੱਖੋ  
7. ਸਿਰਫ ਅਨੁਵਾਦਿਤ ਸਮੱਗਰੀ ਵਾਪਸ ਕਰੋ, ਕੋਈ ਵਾਧੂ ਟੈਗ ਜਾਂ ਮਾਰਕਅੱਪ ਨਾ ਜੋੜੋ  
ਕਿਰਪਾ ਕਰਕੇ ਆਉਟਪੁੱਟ ਖੱਬੇ ਤੋਂ ਸੱਜੇ ਲਿਖੋ।  

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: Azure AI Foundry MCP Server ਵਿਕਾਸਕਾਰਾਂ ਨੂੰ Azure ਦੇ AI ਪਰਿਵਾਰ ਨਾਲ ਪੂਰੀ ਪਹੁੰਚ ਦਿੰਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਮਾਡਲ ਕੈਟਾਲੌਗ, ਡਿਪਲੋਇਮੈਂਟ ਪ੍ਰਬੰਧਨ, Azure AI Search ਨਾਲ ਗਿਆਨ ਇੰਡੈਕਸਿੰਗ ਅਤੇ ਮੁਲਾਂਕਣ ਸੰਦ ਸ਼ਾਮਲ ਹਨ। ਇਹ ਪ੍ਰਯੋਗਾਤਮਕ ਸਰਵਰ AI ਵਿਕਾਸ ਅਤੇ Azure ਦੀ ਸ਼ਕਤੀਸ਼ਾਲੀ AI ਢਾਂਚਾ ਵਿਚਕਾਰ ਪੁਲ ਬਣਾਉਂਦਾ ਹੈ, ਜਿਸ ਨਾਲ AI ਐਪਲੀਕੇਸ਼ਨਾਂ ਨੂੰ ਬਣਾਉਣਾ, ਡਿਪਲੋਇ ਕਰਨਾ ਅਤੇ ਮੁਲਾਂਕਣ ਕਰਨਾ ਆਸਾਨ ਹੋ ਜਾਂਦਾ ਹੈ।

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: ਇਹ ਸਰਵਰ ਤੁਹਾਡੇ Azure AI ਸੇਵਾਵਾਂ ਨਾਲ ਕੰਮ ਕਰਨ ਦੇ ਤਰੀਕੇ ਨੂੰ ਬਦਲ ਦਿੰਦਾ ਹੈ, ਜਿੱਥੇ ਉਦਯੋਗ-ਪੱਧਰੀ AI ਸਮਰੱਥਾਵਾਂ ਸਿੱਧਾ ਤੁਹਾਡੇ ਵਿਕਾਸ ਕਾਰਜ ਪ੍ਰਵਾਹ ਵਿੱਚ ਆ ਜਾਂਦੀਆਂ ਹਨ। Azure ਪੋਰਟਲ, ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਅਤੇ IDE ਵਿਚਕਾਰ ਬਦਲਾਅ ਕਰਨ ਦੀ ਬਜਾਏ, ਤੁਸੀਂ ਮਾਡਲ ਖੋਜ ਸਕਦੇ ਹੋ, ਸੇਵਾਵਾਂ ਡਿਪਲੋਇ ਕਰ ਸਕਦੇ ਹੋ, ਗਿਆਨ ਬੇਸ ਪ੍ਰਬੰਧਿਤ ਕਰ ਸਕਦੇ ਹੋ ਅਤੇ ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਕਮਾਂਡਾਂ ਰਾਹੀਂ AI ਪ੍ਰਦਰਸ਼ਨ ਦਾ ਮੁਲਾਂਕਣ ਕਰ ਸਕਦੇ ਹੋ। ਇਹ ਖਾਸ ਕਰਕੇ RAG (Retrieval-Augmented Generation) ਐਪਲੀਕੇਸ਼ਨਾਂ ਨੂੰ ਬਣਾਉਣ ਵਾਲੇ ਵਿਕਾਸਕਾਰਾਂ ਲਈ ਬਹੁਤ ਸ਼ਕਤੀਸ਼ਾਲੀ ਹੈ, ਜਿਹੜੇ ਬਹੁ-ਮਾਡਲ ਡਿਪਲੋਇਮੈਂਟ ਪ੍ਰਬੰਧਨ ਜਾਂ ਵਿਆਪਕ AI ਮੁਲਾਂਕਣ ਪਾਈਪਲਾਈਨਾਂ ਨੂੰ ਲਾਗੂ ਕਰ ਰਹੇ ਹਨ।

**ਮੁੱਖ ਵਿਕਾਸਕਾਰ ਸਮਰੱਥਾਵਾਂ**:  
- **🔍 ਮਾਡਲ ਖੋਜ ਅਤੇ ਡਿਪਲੋਇਮੈਂਟ**: Azure AI Foundry ਦੇ ਮਾਡਲ ਕੈਟਾਲੌਗ ਦੀ ਖੋਜ ਕਰੋ, ਕੋਡ ਨਮੂਨਿਆਂ ਨਾਲ ਵਿਸਥਾਰਿਤ ਮਾਡਲ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ ਅਤੇ ਮਾਡਲ Azure AI ਸੇਵਾਵਾਂ 'ਤੇ ਡਿਪਲੋਇ ਕਰੋ  
- **📚 ਗਿਆਨ ਪ੍ਰਬੰਧਨ**: Azure AI Search ਇੰਡੈਕਸ ਬਣਾਓ ਅਤੇ ਪ੍ਰਬੰਧਿਤ ਕਰੋ, ਦਸਤਾਵੇਜ਼ ਸ਼ਾਮਲ ਕਰੋ, ਇੰਡੈਕਸਰ ਕਨਫਿਗਰ ਕਰੋ ਅਤੇ ਸੁਧਰੇ ਹੋਏ RAG ਸਿਸਟਮ ਬਣਾਓ  
- **⚡ AI ਏਜੰਟ ਇੰਟੀਗ੍ਰੇਸ਼ਨ**: Azure AI ਏਜੰਟਾਂ ਨਾਲ ਜੁੜੋ, ਮੌਜੂਦਾ ਏਜੰਟਾਂ ਨੂੰ ਪੁੱਛੋ ਅਤੇ ਉਤਪਾਦਨ ਸਥਿਤੀਆਂ ਵਿੱਚ ਏਜੰਟ ਪ੍ਰਦਰਸ਼ਨ ਦਾ ਮੁਲਾਂਕਣ ਕਰੋ  
- **📊 ਮੁਲਾਂਕਣ ਫਰੇਮਵਰਕ**: ਵਿਸਥਾਰਿਤ ਟੈਕਸਟ ਅਤੇ ਏਜੰਟ ਮੁਲਾਂਕਣ ਚਲਾਓ, ਮਾਰਕਡਾਊਨ ਰਿਪੋਰਟ ਬਣਾਓ ਅਤੇ AI ਐਪਲੀਕੇਸ਼ਨਾਂ ਲਈ ਗੁਣਵੱਤਾ ਯਕੀਨੀ ਬਣਾਓ  
- **🚀 ਪ੍ਰੋਟੋਟਾਈਪਿੰਗ ਸੰਦ**: GitHub-ਅਧਾਰਿਤ ਪ੍ਰੋਟੋਟਾਈਪਿੰਗ ਲਈ ਸੈਟਅੱਪ ਨਿਰਦੇਸ਼ ਪ੍ਰਾਪਤ ਕਰੋ ਅਤੇ Azure AI Foundry Labs ਵਿੱਚ ਕੱਟਿੰਗ-ਏਜ ਰਿਸਰਚ ਮਾਡਲਾਂ ਤੱਕ ਪਹੁੰਚ ਪ੍ਰਾਪਤ ਕਰੋ  

**ਅਸਲੀ ਦੁਨੀਆ ਵਿੱਚ ਵਿਕਾਸਕਾਰ ਵਰਤੋਂ**: "ਮੇਰੇ ਐਪਲੀਕੇਸ਼ਨ ਲਈ Phi-4 ਮਾਡਲ ਨੂੰ Azure AI ਸੇਵਾਵਾਂ 'ਤੇ ਡਿਪਲੋਇ ਕਰੋ", "ਮੇਰੇ ਦਸਤਾਵੇਜ਼ੀਕਰਨ RAG ਸਿਸਟਮ ਲਈ ਨਵਾਂ ਖੋਜ ਇੰਡੈਕਸ ਬਣਾਓ", "ਮੇਰੇ ਏਜੰਟ ਦੇ ਜਵਾਬਾਂ ਨੂੰ ਗੁਣਵੱਤਾ ਮਾਪਦੰਡਾਂ ਦੇ ਖਿਲਾਫ ਮੁਲਾਂਕਣ ਕਰੋ", ਜਾਂ "ਮੇਰੇ ਜਟਿਲ ਵਿਸ਼ਲੇਸ਼ਣ ਕਾਰਜਾਂ ਲਈ ਸਭ ਤੋਂ ਵਧੀਆ ਤਰਕਸ਼ੀਲ ਮਾਡਲ ਲੱਭੋ"  

**ਪੂਰਾ ਡੈਮੋ ਸਿਨੇਰੀਓ**: ਇੱਥੇ ਇੱਕ ਸ਼ਕਤੀਸ਼ਾਲੀ AI ਵਿਕਾਸ ਕਾਰਜ ਪ੍ਰਵਾਹ ਹੈ:  

> "ਮੈਂ ਇੱਕ ਗਾਹਕ ਸਹਾਇਤਾ ਏਜੰਟ ਬਣਾ ਰਿਹਾ ਹਾਂ। ਮੈਨੂੰ ਕੈਟਾਲੌਗ ਵਿੱਚੋਂ ਇੱਕ ਵਧੀਆ ਤਰਕਸ਼ੀਲ ਮਾਡਲ ਲੱਭਣ ਵਿੱਚ ਮਦਦ ਕਰੋ, ਇਸਨੂੰ Azure AI ਸੇਵਾਵਾਂ 'ਤੇ ਡਿਪਲੋਇ ਕਰੋ, ਸਾਡੇ ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਤੋਂ ਗਿਆਨ ਬੇਸ ਬਣਾਓ, ਜਵਾਬ ਦੀ ਗੁਣਵੱਤਾ ਦੀ ਜਾਂਚ ਲਈ ਮੁਲਾਂਕਣ ਫਰੇਮਵਰਕ ਸੈਟਅੱਪ ਕਰੋ, ਅਤੇ ਫਿਰ GitHub ਟੋਕਨ ਨਾਲ ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਦਾ ਪ੍ਰੋਟੋਟਾਈਪ ਬਣਾਉਣ ਵਿੱਚ ਮਦਦ ਕਰੋ।"  

Azure AI Foundry MCP Server ਇਹ ਕਰੇਗਾ:  
- ਤੁਹਾਡੇ ਲੋੜਾਂ ਦੇ ਅਧਾਰ 'ਤੇ ਸਭ ਤੋਂ ਵਧੀਆ ਤਰਕਸ਼ੀਲ ਮਾਡਲਾਂ ਦੀ ਸਿਫਾਰਸ਼ ਲਈ ਮਾਡਲ ਕੈਟਾਲੌਗ ਨੂੰ ਪੁੱਛਗਿੱਛ ਕਰੇਗਾ  
- ਤੁਹਾਡੇ ਪਸੰਦੀਦਾ Azure ਖੇਤਰ ਲਈ ਡਿਪਲੋਇਮੈਂਟ ਕਮਾਂਡ ਅਤੇ ਕੋਟਾ ਜਾਣਕਾਰੀ ਦੇਵੇਗਾ  
- ਤੁਹਾਡੇ ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਲਈ ਢੰਗ ਨਾਲ ਸਕੀਮਾ ਵਾਲੇ Azure AI Search ਇੰਡੈਕਸ ਸੈਟਅੱਪ ਕਰੇਗਾ  
- ਗੁਣਵੱਤਾ ਮਾਪਦੰਡਾਂ ਅਤੇ ਸੁਰੱਖਿਆ ਜਾਂਚਾਂ ਨਾਲ ਮੁਲਾਂਕਣ ਪਾਈਪਲਾਈਨਾਂ ਕਨਫਿਗਰ ਕਰੇਗਾ  
- ਤੁਰੰਤ ਟੈਸਟਿੰਗ ਲਈ GitHub ਪ੍ਰਮਾਣਿਕਤਾ ਨਾਲ ਪ੍ਰੋਟੋਟਾਈਪਿੰਗ ਕੋਡ ਤਿਆਰ ਕਰੇਗਾ  
- ਤੁਹਾਡੇ ਵਿਸ਼ੇਸ਼ ਤਕਨਾਲੋਜੀ ਸਟੈਕ ਲਈ ਵਿਸਥਾਰਿਤ ਸੈਟਅੱਪ ਗਾਈਡਜ਼ ਪ੍ਰਦਾਨ ਕਰੇਗਾ  

**ਮਿਸਾਲ**: ਇੱਕ ਵਿਕਾਸਕਾਰ ਵਜੋਂ, ਮੈਂ ਵੱਖ-ਵੱਖ LLM ਮਾਡਲਾਂ ਨਾਲ ਕਦਮ ਮਿਲਾਉਣ ਵਿੱਚ ਮੁਸ਼ਕਲ ਮਹਿਸੂਸ ਕਰ ਰਿਹਾ ਹਾਂ। ਮੈਂ ਕੁਝ ਮੁੱਖ ਮਾਡਲਾਂ ਨੂੰ ਜਾਣਦਾ ਹਾਂ, ਪਰ ਮਹਿਸੂਸ ਕਰਦਾ ਹਾਂ ਕਿ ਮੈਂ ਕੁਝ ਉਤਪਾਦਕਤਾ ਅਤੇ ਕੁਸ਼ਲਤਾ ਦੇ ਫਾਇਦੇ ਗੁਆ ਰਿਹਾ ਹਾਂ। ਟੋਕਨ ਅਤੇ ਕੋਟਾ ਸੰਭਾਲਣਾ ਵੀ ਤਣਾਅਪੂਰਨ ਅਤੇ ਮੁਸ਼ਕਲ ਹੈ – ਮੈਨੂੰ ਕਦੇ ਪਤਾ ਨਹੀਂ ਲੱਗਦਾ ਕਿ ਮੈਂ ਸਹੀ ਕੰਮ ਲਈ ਸਹੀ ਮਾਡਲ ਚੁਣ ਰਿਹਾ ਹਾਂ ਜਾਂ ਬਜਟ ਬੇਕਾਰ ਖਰਚ ਕਰ ਰਿਹਾ ਹਾਂ। ਮੈਂ ਇਹ MCP Server James Montemagno ਤੋਂ ਸੁਣਿਆ ਜਦੋਂ ਮੈਂ ਟੀਮ ਮੈਂਬਰਾਂ ਨਾਲ MCP Server ਦੀ ਸਿਫਾਰਸ਼ਾਂ ਬਾਰੇ ਗੱਲ ਕਰ ਰਿਹਾ ਸੀ, ਅਤੇ ਮੈਂ ਇਸਨੂੰ ਵਰਤਣ ਲਈ ਉਤਸ਼ਾਹਿਤ ਹਾਂ! ਮਾਡਲ ਖੋਜ ਸਮਰੱਥਾਵਾਂ ਮੇਰੇ ਵਰਗੇ ਕਿਸੇ ਲਈ ਬਹੁਤ ਪ੍ਰਭਾਵਸ਼ਾਲੀ ਲੱਗਦੀਆਂ ਹਨ ਜੋ ਆਮ ਮਾਡਲਾਂ ਤੋਂ ਅੱਗੇ ਖੋਜ ਕਰਨਾ ਚਾਹੁੰਦਾ ਹੈ ਅਤੇ ਖਾਸ ਕੰਮਾਂ ਲਈ ਅਨੁਕੂਲ ਮਾਡਲ ਲੱਭਣਾ ਚਾਹੁੰਦਾ ਹੈ। ਮੁਲਾਂਕਣ ਫਰੇਮਵਰਕ ਮੈਨੂੰ ਇਹ ਯਕੀਨੀ ਬਣਾਉਣ ਵਿੱਚ ਮਦਦ ਕਰੇਗਾ ਕਿ ਮੈਂ ਵਾਸਤਵ ਵਿੱਚ ਵਧੀਆ ਨਤੀਜੇ ਪ੍ਰਾਪਤ ਕਰ ਰਿਹਾ ਹਾਂ, ਨਾ ਕਿ ਸਿਰਫ ਨਵਾਂ ਕੁਝ ਕਰਨ ਲਈ।  

> **ℹ️ ਪ੍ਰਯੋਗਾਤਮਕ ਸਥਿਤੀ**  
>  
> ਇਹ MCP ਸਰਵਰ ਪ੍ਰਯੋਗਾਤਮਕ ਹੈ ਅਤੇ ਸਰਗਰਮ ਵਿਕਾਸ ਹੇਠ ਹੈ। ਫੀਚਰ ਅਤੇ APIs ਬਦਲ ਸਕਦੇ ਹਨ। Azure AI ਸਮਰੱਥਾਵਾਂ ਦੀ ਖੋਜ ਅਤੇ ਪ੍ਰੋਟੋਟਾਈਪ ਬਣਾਉਣ ਲਈ ਬਹੁਤ ਵਧੀਆ, ਪਰ ਉਤਪਾਦਨ ਲਈ ਸਥਿਰਤਾ ਦੀ ਜਾਂਚ ਕਰੋ।  

### 10. 🏢 Microsoft 365 Agents Toolkit MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**ਇਹ ਕੀ ਕਰਦਾ ਹੈ**: ਵਿਕਾਸਕਾਰਾਂ ਨੂੰ Microsoft 365 ਅਤੇ Microsoft 365 Copilot ਨਾਲ ਇੰਟੀਗ੍ਰੇਟ ਹੋਣ ਵਾਲੇ AI ਏਜੰਟਾਂ ਅਤੇ ਐਪਲੀਕੇਸ਼ਨਾਂ ਬਣਾਉਣ ਲਈ ਜਰੂਰੀ ਸੰਦ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਸਕੀਮਾ ਵੈਰੀਫਿਕੇਸ਼ਨ, ਨਮੂਨਾ ਕੋਡ ਪ੍ਰਾਪਤੀ ਅਤੇ ਸਮੱਸਿਆ ਹੱਲ ਕਰਨ ਵਿੱਚ ਮਦਦ ਸ਼ਾਮਲ ਹੈ।

**ਇਹ ਕਿਉਂ ਲਾਭਦਾਇਕ ਹੈ**: Microsoft 365 ਅਤੇ Copilot ਲਈ ਬਣਾਉਣਾ ਜਟਿਲ ਮੈਨਿਫੈਸਟ ਸਕੀਮਾਂ ਅਤੇ ਖਾਸ ਵਿਕਾਸ ਪੈਟਰਨਾਂ ਨਾਲ ਜੁੜਿਆ ਹੈ। ਇਹ MCP ਸਰਵਰ ਤੁਹਾਡੇ ਕੋਡਿੰਗ ਵਾਤਾਵਰਣ ਵਿੱਚ ਜਰੂਰੀ ਵਿਕਾਸ ਸਰੋਤ ਸਿੱਧਾ ਲਿਆਉਂਦਾ ਹੈ, ਜਿਸ ਨਾਲ ਤੁਸੀਂ ਸਕੀਮਾਂ ਦੀ ਜਾਂਚ ਕਰ ਸਕਦੇ ਹੋ, ਨਮੂਨਾ ਕੋਡ ਲੱਭ ਸਕਦੇ ਹੋ ਅਤੇ ਆਮ ਸਮੱਸਿਆਵਾਂ ਨੂੰ ਬਿਨਾਂ ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਦੇ ਬਾਰ-ਬਾਰ ਹਵਾਲਾ ਦਿੱਤੇ ਹੱਲ ਕਰ ਸਕਦੇ ਹੋ।

**ਅਸਲੀ ਦੁਨੀਆ ਦੀ ਵਰਤੋਂ**: "ਮੇਰੇ ਡਿਕਲੇਰੇਟਿਵ ਏਜੰਟ ਮੈਨਿਫੈਸਟ ਨੂੰ ਵੈਰੀਫਾਈ ਕਰੋ ਅਤੇ ਕਿਸੇ ਵੀ ਸਕੀਮਾ ਗਲਤੀ ਨੂੰ ਠੀਕ ਕਰੋ", "Microsoft Graph API ਪਲੱਗਇਨ ਲਾਗੂ ਕਰਨ ਲਈ ਨਮੂਨਾ ਕੋਡ ਦਿਖਾਓ", ਜਾਂ "ਮੇਰੇ Teams ਐਪ ਪ੍ਰਮਾਣਿਕਤਾ ਸਮੱਸਿਆਵਾਂ ਨੂੰ ਹੱਲ ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰੋ"  

**ਮਿਸਾਲ**: ਮੈਂ ਆਪਣੇ ਦੋਸਤ John Miller ਨਾਲ Build ਸਮਾਰੋਹ ਵਿੱਚ ਗੱਲਬਾਤ ਕਰਦਿਆਂ M365 Agents ਬਾਰੇ ਪੁੱਛਿਆ, ਅਤੇ ਉਸਨੇ ਇਹ MCP ਸਿਫਾਰਸ਼ ਕੀਤੀ। ਇਹ ਨਵੇਂ ਵਿਕਾਸਕਾਰਾਂ ਲਈ ਬਹੁਤ ਵਧੀਆ ਹੋ ਸਕਦਾ ਹੈ ਕਿਉਂਕਿ ਇਹ ਟੈਮਪਲੇਟ, ਨਮੂਨਾ ਕੋਡ ਅਤੇ ਸਕੈਫੋਲਡਿੰਗ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ, ਜਿਸ ਨਾਲ ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਵਿੱਚ ਡੁੱਬਣ ਤੋਂ ਬਚਿਆ ਜਾ ਸਕਦਾ ਹੈ। ਸਕੀਮਾ ਵੈਰੀਫਿਕੇਸ਼ਨ ਫੀਚਰ ਖਾਸ ਕਰਕੇ ਮੈਨਿਫੈਸਟ ਸਟ੍ਰਕਚਰ ਗਲਤੀਆਂ ਤੋਂ ਬਚਾਉਣ ਲਈ ਬਹੁਤ ਲਾਭਦਾਇਕ ਹਨ, ਜੋ ਘੰਟਿਆਂ ਦੀ ਡੀਬੱਗਿੰਗ ਦਾ ਕਾਰਨ ਬਣ ਸਕਦੀਆਂ ਹਨ।  

> **💡 ਪ੍ਰੋ ਟਿਪ**  
>  
> ਇਸ ਸਰਵਰ ਨੂੰ Microsoft Learn Docs MCP Server ਨਾਲ ਇਕੱਠੇ ਵਰਤੋਂ, ਤਾਂ ਜੋ M365 ਵਿਕਾਸ ਲਈ ਪੂਰਾ ਸਹਿਯੋਗ ਮਿਲੇ – ਇੱਕ ਅਧਿਕਾਰਿਕ ਦਸਤਾਵੇਜ਼ੀਕਰਨ ਦਿੰਦਾ ਹੈ, ਦੂਜਾ ਪ੍ਰਯੋਗਾਤਮਕ ਵਿਕਾਸ ਸੰਦ ਅਤੇ ਸਮੱਸਿਆ ਹੱਲ ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹੈ।  

## ਅਗਲਾ ਕੀ ਹੈ? 🔮

## 📋 ਨਤੀਜਾ

Model Context Protocol (MCP) ਵਿਕਾਸਕਾਰਾਂ ਦੇ AI ਸਹਾਇਕਾਂ ਅਤੇ ਬਾਹਰੀ ਸੰਦਾਂ ਨਾਲ ਇੰਟਰੈਕਸ਼ਨ ਦੇ ਤਰੀਕੇ ਨੂੰ ਬਦਲ ਰਿਹਾ ਹੈ। ਇਹ 10 Microsoft MCP ਸਰਵਰ ਮਿਆਰੀਕ੍ਰਿਤ AI ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਦੀ ਤਾਕਤ ਦਿਖਾਉਂਦੇ ਹਨ, ਜੋ ਵਿਕਾਸਕਾਰਾਂ ਨੂੰ ਸ਼ਕਤੀਸ਼ਾਲੀ ਬਾਹਰੀ ਸਮਰੱਥਾਵਾਂ ਤੱਕ ਪਹੁੰਚ ਦਿੰਦਿਆਂ ਉਨ੍ਹਾਂ ਦੇ ਕੰਮ ਦੇ ਪ੍ਰਵਾਹ ਨੂੰ ਬਿਨਾਂ ਰੁਕਾਵਟ ਦੇ ਜਾਰੀ ਰੱਖਦੇ ਹਨ।  

ਵਿਸਤ੍ਰਿਤ Azure ਪਰਿਵਾਰਕ ਇੰਟੀਗ੍ਰੇਸ਼ਨ ਤੋਂ ਲੈ ਕੇ ਖਾਸ ਸੰਦਾਂ ਜਿਵੇਂ Playwright ਬਰਾਊਜ਼ਰ ਆਟੋਮੇਸ਼ਨ ਲਈ ਅਤੇ MarkItDown ਦਸਤਾਵੇਜ਼ ਪ੍ਰੋਸੈਸਿੰਗ ਲਈ, ਇਹ ਸਰਵਰ ਦਿਖਾਉਂਦੇ ਹਨ ਕਿ MCP ਕਿਵੇਂ ਵੱਖ-ਵੱਖ ਵਿਕਾਸ ਸਿਨੇਰੀਓਜ਼ ਵਿੱਚ ਉਤਪਾਦਕਤਾ ਨੂੰ ਵਧਾ ਸਕਦਾ ਹੈ। ਮਿਆਰੀਕ੍ਰਿਤ ਪ੍ਰੋਟੋਕੋਲ ਇਹ ਯਕੀਨੀ ਬਣਾਉਂਦਾ ਹੈ ਕਿ ਇਹ ਸਾਰੇ ਸੰਦ ਮਿਲ ਕੇ ਬਿਨਾਂ ਕਿਸੇ ਰੁਕਾਵਟ ਦੇ ਕੰਮ ਕਰਦੇ ਹਨ, ਜਿਸ ਨਾਲ ਇੱਕ ਸੰਗਠਿਤ ਵਿਕਾਸ ਅਨੁ

**ਅਸਵੀਕਾਰੋਪੱਤਰ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦਿਤ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾ ਲਈ ਕੋਸ਼ਿਸ਼ ਕਰਦੇ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮਰਥਤਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਪ੍ਰਮਾਣਿਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਉਤਪੰਨ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆ ਲਈ ਅਸੀਂ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।