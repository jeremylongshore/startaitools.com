<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:04:40+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "it"
}
-->
# Esegui esempio

## Configura l'ambiente virtuale

```sh
python -m venv venv
source ./venv/bin/activate
```

## Installa le dipendenze

```sh
pip install "mcp[cli]"
```

## Esegui il codice

```sh
python client.py
```

Dovresti vedere il testo:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa dovrebbe essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un esperto umano. Non siamo responsabili per eventuali incomprensioni o interpretazioni errate derivanti dall'uso di questa traduzione.