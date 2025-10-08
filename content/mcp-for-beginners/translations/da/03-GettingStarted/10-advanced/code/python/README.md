<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:05:11+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "da"
}
-->
# Kør eksempel

## Opsæt virtuel miljø

```sh
python -m venv venv
source ./venv/bin/activate
```

## Installer afhængigheder

```sh
pip install "mcp[cli]"
```

## Kør kode

```sh
python client.py
```

Du bør se teksten:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal det bemærkes, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os ikke ansvar for misforståelser eller fejltolkninger, der måtte opstå som følge af brugen af denne oversættelse.