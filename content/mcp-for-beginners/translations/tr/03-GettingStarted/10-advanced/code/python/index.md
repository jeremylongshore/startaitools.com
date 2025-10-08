<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:04:50+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "tr"
}
-->
# Örnek Çalıştırma

## Sanal ortamı kurun

```sh
python -m venv venv
source ./venv/bin/activate
```

## Bağımlılıkları yükleyin

```sh
pip install "mcp[cli]"
```

## Kodu çalıştırın

```sh
python client.py
```

Şu metni görmelisiniz:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Feragatname**:  
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayın. Belgenin orijinal dili, yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımından kaynaklanan yanlış anlamalar veya yanlış yorumlamalar için sorumluluk kabul edilmez.