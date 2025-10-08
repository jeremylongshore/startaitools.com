<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d4c162484df410632550a4a357d40341",
  "translation_date": "2025-09-03T16:04:41+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "pa"
}
-->
# ਇਸ ਨਮੂਨੇ ਨੂੰ ਚਲਾਉਣਾ

ਤੁਹਾਨੂੰ `uv` ਇੰਸਟਾਲ ਕਰਨ ਦੀ ਸਿਫਾਰਿਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ ਪਰ ਇਹ ਲਾਜ਼ਮੀ ਨਹੀਂ ਹੈ, ਵੇਖੋ [ਹਦਾਇਤਾਂ](https://docs.astral.sh/uv/#highlights)

## -0- ਇੱਕ ਵਰਚੁਅਲ ਵਾਤਾਵਰਣ ਬਣਾਓ

```bash
python -m venv venv
```

## -1- ਵਰਚੁਅਲ ਵਾਤਾਵਰਣ ਨੂੰ ਐਕਟੀਵੇਟ ਕਰੋ

```bash
venv\Scripts\activate
```

## -2- ਡਿਪੈਂਡੈਂਸੀਜ਼ ਇੰਸਟਾਲ ਕਰੋ

```bash
pip install "mcp[cli]"
```

## -3- ਨਮੂਨੇ ਨੂੰ ਚਲਾਓ

```bash
mcp run server.py
```

## -4- ਨਮੂਨੇ ਦੀ ਜਾਂਚ ਕਰੋ

ਜਦੋਂ ਸਰਵਰ ਇੱਕ ਟਰਮੀਨਲ ਵਿੱਚ ਚਲ ਰਿਹਾ ਹੋਵੇ, ਦੂਜੇ ਟਰਮੀਨਲ ਨੂੰ ਖੋਲ੍ਹੋ ਅਤੇ ਹੇਠਾਂ ਦਿੱਤਾ ਕਮਾਂਡ ਚਲਾਓ:

```bash
mcp dev server.py
```

ਇਸ ਨਾਲ ਇੱਕ ਵਿਜ਼ੂਅਲ ਇੰਟਰਫੇਸ ਵਾਲਾ ਵੈਬ ਸਰਵਰ ਸ਼ੁਰੂ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ ਜੋ ਤੁਹਾਨੂੰ ਨਮੂਨੇ ਦੀ ਜਾਂਚ ਕਰਨ ਦੀ ਆਗਿਆ ਦਿੰਦਾ ਹੈ।

ਜਦੋਂ ਸਰਵਰ ਕਨੈਕਟ ਹੋ ਜਾਵੇ:

- ਟੂਲਸ ਦੀ ਸੂਚੀ ਬਣਾਉਣ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰੋ ਅਤੇ `add` ਚਲਾਓ, 2 ਅਤੇ 4 ਦੇ ਆਰਗਸ ਨਾਲ, ਤੁਹਾਨੂੰ ਨਤੀਜੇ ਵਿੱਚ 6 ਦੇਖਣਾ ਚਾਹੀਦਾ ਹੈ।

- ਰਿਸੋਰਸ ਅਤੇ ਰਿਸੋਰਸ ਟੈਂਪਲੇਟ ਤੇ ਜਾਓ ਅਤੇ `get_greeting` ਨੂੰ ਕਾਲ ਕਰੋ, ਇੱਕ ਨਾਮ ਟਾਈਪ ਕਰੋ ਅਤੇ ਤੁਹਾਨੂੰ ਉਸ ਨਾਮ ਨਾਲ ਇੱਕ ਗ੍ਰੀਟਿੰਗ ਦੇਖਣੀ ਚਾਹੀਦੀ ਹੈ ਜੋ ਤੁਸੀਂ ਦਿੱਤਾ ਹੈ।

### CLI ਮੋਡ ਵਿੱਚ ਜਾਂਚ ਕਰਨਾ

ਜੋ ਇੰਸਪੈਕਟਰ ਤੁਸੀਂ ਚਲਾਇਆ ਹੈ ਉਹ ਅਸਲ ਵਿੱਚ ਇੱਕ Node.js ਐਪ ਹੈ ਅਤੇ `mcp dev` ਇਸ ਦਾ ਰੈਪਰ ਹੈ।

ਤੁਸੀਂ ਇਸਨੂੰ CLI ਮੋਡ ਵਿੱਚ ਸਿੱਧੇ ਚਲਾਉਣ ਲਈ ਹੇਠਾਂ ਦਿੱਤਾ ਕਮਾਂਡ ਚਲਾ ਸਕਦੇ ਹੋ:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

ਇਹ ਸਰਵਰ ਵਿੱਚ ਉਪਲਬਧ ਸਾਰੇ ਟੂਲਸ ਦੀ ਸੂਚੀ ਦਿਖਾਏਗਾ। ਤੁਹਾਨੂੰ ਹੇਠਾਂ ਦਿੱਤਾ ਆਉਟਪੁੱਟ ਦੇਖਣਾ ਚਾਹੀਦਾ ਹੈ:

```text
{
  "tools": [
    {
      "name": "add",
      "description": "Add two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "title": "A",
            "type": "integer"
          },
          "b": {
            "title": "B",
            "type": "integer"
          }
        },
        "required": [
          "a",
          "b"
        ],
        "title": "addArguments"
      }
    }
  ]
}
```

ਕਿਸੇ ਟੂਲ ਨੂੰ ਚਲਾਉਣ ਲਈ ਟਾਈਪ ਕਰੋ:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

ਤੁਹਾਨੂੰ ਹੇਠਾਂ ਦਿੱਤਾ ਆਉਟਪੁੱਟ ਦੇਖਣਾ ਚਾਹੀਦਾ ਹੈ:

```text
{
  "content": [
    {
      "type": "text",
      "text": "3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> ਇੰਸਪੈਕਟਰ ਨੂੰ CLI ਮੋਡ ਵਿੱਚ ਚਲਾਉਣਾ ਆਮ ਤੌਰ ਤੇ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਚਲਾਉਣ ਨਾਲੋਂ ਕਾਫ਼ੀ ਤੇਜ਼ ਹੁੰਦਾ ਹੈ।
> ਇੰਸਪੈਕਟਰ ਬਾਰੇ ਹੋਰ ਪੜ੍ਹੋ [ਇਥੇ](https://github.com/modelcontextprotocol/inspector)।

---

**ਅਸਵੀਕਾਰਨਾ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਦਿਓ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸੁਚੀਤਤਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਨੂੰ ਇਸਦੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਤ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੇ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆ ਲਈ ਅਸੀਂ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।