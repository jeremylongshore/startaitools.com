<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:04:36+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "br"
}
-->
# Executar exemplo

## Configurar ambiente virtual

```sh
python -m venv venv
source ./venv/bin/activate
```

## Instalar dependências

```sh
pip install "mcp[cli]"
```

## Executar código

```sh
python client.py
```

Você deverá ver o texto:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, é importante estar ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte oficial. Para informações críticas, recomenda-se a tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações equivocadas decorrentes do uso desta tradução.