<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:05:25+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "nl"
}
-->
# Voorbeeld uitvoeren

## Virtuele omgeving instellen

```sh
python -m venv venv
source ./venv/bin/activate
```

## Afhankelijkheden installeren

```sh
pip install "mcp[cli]"
```

## Code uitvoeren

```sh
python client.py
```

Je zou de tekst moeten zien:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.