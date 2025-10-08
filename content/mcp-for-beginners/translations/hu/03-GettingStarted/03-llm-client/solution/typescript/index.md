<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "6d6315e03f591fb5a39be91da88585dc",
  "translation_date": "2025-07-13T19:20:54+00:00",
  "source_file": "03-GettingStarted/03-llm-client/solution/typescript/README.md",
  "language_code": "hu"
}
-->
# A minta futtatása

Ez a minta azt mutatja be, hogyan használhatunk egy LLM-et a kliens oldalon. Az LLM működéséhez vagy Codespaces-ben kell futtatnod, vagy be kell állítanod egy személyes hozzáférési tokent a GitHubon.

## -1- A függőségek telepítése

```bash
npm install
```

## -3- A szerver indítása

```bash
npm run build
```

## -4- A kliens indítása

```sh
npm run client
```

Egy hasonló eredményt kell látnod:

```text
Asking server for available tools
MCPClient started on stdin/stdout
Querying LLM:  What is the sum of 2 and 3?
Making tool call
Calling tool add with args "{\"a\":2,\"b\":3}"
Tool result:  { content: [ { type: 'text', text: '5' } ] }
```

**Jogi nyilatkozat**:  
Ez a dokumentum az AI fordító szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár a pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén szakmai, emberi fordítást javaslunk. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy téves értelmezésekért.