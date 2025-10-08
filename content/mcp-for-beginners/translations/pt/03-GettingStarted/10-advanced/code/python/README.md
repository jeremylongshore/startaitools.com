<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:04:32+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "pt"
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

Deverá ver o texto:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Aviso**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autoritária. Para informações críticas, recomenda-se uma tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.