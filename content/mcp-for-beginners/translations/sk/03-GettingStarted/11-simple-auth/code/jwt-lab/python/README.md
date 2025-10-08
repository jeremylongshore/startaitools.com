<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "cc12267d65091b22e39026fccfcaa22b",
  "translation_date": "2025-10-07T01:39:47+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/python/README.md",
  "language_code": "sk"
}
-->
# Spustenie ukážky

## Nastavenie prostredia

```sh
python -m venv
source ./venv/bin/activate
```

## Inštalácia závislostí

```sh
pip install PyJWT
```

## Spustenie kódu

```sh
python lab.py
```

Mali by ste vidieť výstup podobný:

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

**Upozornenie**:  
Tento dokument bol preložený pomocou služby AI prekladu [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, prosím, berte na vedomie, že automatizované preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho rodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.