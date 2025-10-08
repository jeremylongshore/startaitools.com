<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:06:31+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "sl"
}
-->
# Zagon vzorca

## Nastavitev virtualnega okolja

```sh
python -m venv venv
source ./venv/bin/activate
```

## Namestitev odvisnosti

```sh
pip install "mcp[cli]"
```

## Zagon kode

```sh
python client.py
```

Videti bi morali besedilo:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve za prevajanje z umetno inteligenco [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da lahko avtomatski prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem maternem jeziku je treba obravnavati kot avtoritativni vir. Za ključne informacije priporočamo profesionalni človeški prevod. Ne prevzemamo odgovornosti za morebitna nesporazumevanja ali napačne razlage, ki izhajajo iz uporabe tega prevoda.