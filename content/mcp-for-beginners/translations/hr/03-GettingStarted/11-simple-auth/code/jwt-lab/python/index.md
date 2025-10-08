<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "cc12267d65091b22e39026fccfcaa22b",
  "translation_date": "2025-10-07T01:40:05+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/python/README.md",
  "language_code": "hr"
}
-->
# Pokreni primjer

## Postavljanje okruženja

```sh
python -m venv
source ./venv/bin/activate
```

## Instaliraj ovisnosti

```sh
pip install PyJWT
```

## Pokreni kod

```sh
python lab.py
```

Trebali biste vidjeti izlaz sličan:

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

**Izjava o odricanju odgovornosti**:  
Ovaj dokument je preveden pomoću AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za ključne informacije preporučuje se profesionalni prijevod od strane ljudskog prevoditelja. Ne preuzimamo odgovornost za nesporazume ili pogrešna tumačenja koja mogu proizaći iz korištenja ovog prijevoda.