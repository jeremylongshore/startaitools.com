<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:06:08+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "sk"
}
-->
# Spustenie ukážky

## Nastavenie virtuálneho prostredia

```sh
python -m venv venv
source ./venv/bin/activate
```

## Inštalácia závislostí

```sh
pip install "mcp[cli]"
```

## Spustenie kódu

```sh
python client.py
```

Mali by ste vidieť text:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Zrieknutie sa zodpovednosti**:  
Tento dokument bol preložený pomocou služby AI prekladu [Co-op Translator](https://github.com/Azure/co-op-translator). Aj keď sa snažíme o presnosť, prosím, berte na vedomie, že automatizované preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho rodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nenesieme zodpovednosť za akékoľvek nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.