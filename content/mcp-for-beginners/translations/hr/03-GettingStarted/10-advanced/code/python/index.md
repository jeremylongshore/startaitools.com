<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:06:26+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "hr"
}
-->
# Pokreni primjer

## Postavljanje virtualnog okruženja

```sh
python -m venv venv
source ./venv/bin/activate
```

## Instaliraj ovisnosti

```sh
pip install "mcp[cli]"
```

## Pokreni kod

```sh
python client.py
```

Trebali biste vidjeti tekst:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Izjava o odricanju odgovornosti**:  
Ovaj dokument je preveden pomoću AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za ključne informacije preporučuje se profesionalni prijevod od strane ljudskog prevoditelja. Ne preuzimamo odgovornost za nesporazume ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.