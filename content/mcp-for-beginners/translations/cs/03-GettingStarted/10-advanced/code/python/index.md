<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:06:03+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "cs"
}
-->
# Spuštění ukázky

## Nastavení virtuálního prostředí

```sh
python -m venv venv
source ./venv/bin/activate
```

## Instalace závislostí

```sh
pip install "mcp[cli]"
```

## Spuštění kódu

```sh
python client.py
```

Měli byste vidět text:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Prohlášení**:  
Tento dokument byl přeložen pomocí služby AI pro překlad [Co-op Translator](https://github.com/Azure/co-op-translator). I když se snažíme o přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho původním jazyce by měl být považován za autoritativní zdroj. Pro důležité informace se doporučuje profesionální lidský překlad. Neodpovídáme za žádná nedorozumění nebo nesprávné interpretace vyplývající z použití tohoto překladu.