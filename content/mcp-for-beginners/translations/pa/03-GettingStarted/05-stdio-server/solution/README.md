<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T20:00:59+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "pa"
}
-->
# MCP stdio ਸਰਵਰ ਹੱਲ

> **⚠️ ਮਹੱਤਵਪੂਰਨ**: ਇਹ ਹੱਲ **stdio ਟ੍ਰਾਂਸਪੋਰਟ** ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਅਪਡੇਟ ਕੀਤੇ ਗਏ ਹਨ, ਜਿਵੇਂ ਕਿ MCP Specification 2025-06-18 ਵਿੱਚ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਗਈ ਹੈ। ਮੂਲ SSE (Server-Sent Events) ਟ੍ਰਾਂਸਪੋਰਟ ਹੁਣ ਡਿਪ੍ਰੀਕੇਟ ਕੀਤਾ ਗਿਆ ਹੈ।

ਹੇਠਾਂ ਹਰ ਰਨਟਾਈਮ ਵਿੱਚ stdio ਟ੍ਰਾਂਸਪੋਰਟ ਦੀ ਵਰਤੋਂ ਕਰਕੇ MCP ਸਰਵਰ ਬਣਾਉਣ ਲਈ ਪੂਰੇ ਹੱਲ ਦਿੱਤੇ ਗਏ ਹਨ:

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - ਪੂਰੀ stdio ਸਰਵਰ ਇੰਪਲੀਮੈਂਟੇਸ਼ਨ
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - asyncio ਨਾਲ Python stdio ਸਰਵਰ
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - dependency injection ਨਾਲ .NET stdio ਸਰਵਰ

ਹਰ ਹੱਲ ਵਿੱਚ ਇਹ ਦਿਖਾਇਆ ਗਿਆ ਹੈ:
- stdio ਟ੍ਰਾਂਸਪੋਰਟ ਸੈਟਅੱਪ ਕਰਨਾ
- ਸਰਵਰ ਟੂਲਜ਼ ਨੂੰ ਪਰਿਭਾਸ਼ਿਤ ਕਰਨਾ
- ਸਹੀ JSON-RPC ਸੁਨੇਹਾ ਸੰਭਾਲ
- MCP ਕਲਾਇੰਟਾਂ ਜਿਵੇਂ Claude ਨਾਲ ਇੰਟੀਗ੍ਰੇਸ਼ਨ

ਸਾਰੇ ਹੱਲ ਮੌਜੂਦਾ MCP ਸਪੈਸਿਫਿਕੇਸ਼ਨ ਦੀ ਪਾਲਣਾ ਕਰਦੇ ਹਨ ਅਤੇ ਵਧੀਆ ਪ੍ਰਦਰਸ਼ਨ ਅਤੇ ਸੁਰੱਖਿਆ ਲਈ ਸਿਫਾਰਸ਼ ਕੀਤੇ stdio ਟ੍ਰਾਂਸਪੋਰਟ ਦੀ ਵਰਤੋਂ ਕਰਦੇ ਹਨ।

---

**ਅਸਵੀਕਤੀ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਅਤ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਦਿਓ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸੁਚੱਜੇਪਣ ਹੋ ਸਕਦੇ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼, ਜੋ ਇਸਦੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਹੈ, ਨੂੰ ਅਧਿਕਾਰਤ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੇ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆ ਲਈ ਅਸੀਂ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।