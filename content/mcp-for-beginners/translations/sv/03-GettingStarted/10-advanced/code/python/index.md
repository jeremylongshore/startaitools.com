<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:05:06+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "sv"
}
-->
# Kör exempel

## Ställ in virtuell miljö

```sh
python -m venv venv
source ./venv/bin/activate
```

## Installera beroenden

```sh
pip install "mcp[cli]"
```

## Kör kod

```sh
python client.py
```

Du bör se texten:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, bör det noteras att automatiska översättningar kan innehålla fel eller felaktigheter. Det ursprungliga dokumentet på dess originalspråk bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för eventuella missförstånd eller feltolkningar som uppstår vid användning av denna översättning.