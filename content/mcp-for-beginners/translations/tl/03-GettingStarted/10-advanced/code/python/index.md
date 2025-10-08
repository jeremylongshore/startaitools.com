<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:05:48+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "tl"
}
-->
# Patakbuhin ang halimbawa

## Mag-set up ng virtual na kapaligiran

```sh
python -m venv venv
source ./venv/bin/activate
```

## I-install ang mga kinakailangan

```sh
pip install "mcp[cli]"
```

## Patakbuhin ang code

```sh
python client.py
```

Makikita mo ang teksto:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't sinisikap naming maging tumpak, mangyaring tandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa kanyang katutubong wika ang dapat ituring na opisyal na sanggunian. Para sa mahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na dulot ng paggamit ng pagsasaling ito.