<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "cc12267d65091b22e39026fccfcaa22b",
  "translation_date": "2025-10-07T01:38:27+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/python/README.md",
  "language_code": "it"
}
-->
# Esegui esempio

## Configura l'ambiente

```sh
python -m venv
source ./venv/bin/activate
```

## Installa le dipendenze

```sh
pip install PyJWT
```

## Esegui il codice

```sh
python lab.py
```

Dovresti vedere un output simile a:

```text
Encoded JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlVzZXIgVXNlcnNvbiIsImFkbWluIjp0cnVlLCJpYXQiOjE3NTkxNjgzMDEsImV4cCI6MTc1OTE3MTkwMX0.tz0UYNNtGVC61DWjVDF8xlhpNkp5XBtxmQH3m_RNwe8
✅ Token is valid.
Decoded claims:
  sub: 1234567890
  name: User Userson
  admin: True
  iat: 1759168301
  exp: 1759171901
```

---

**Clausola di esclusione della responsabilità**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa dovrebbe essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un traduttore umano. Non siamo responsabili per eventuali incomprensioni o interpretazioni errate derivanti dall'uso di questa traduzione.