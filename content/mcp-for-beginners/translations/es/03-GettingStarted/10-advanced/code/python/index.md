<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:03:08+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "es"
}
-->
# Ejecutar ejemplo

## Configurar entorno virtual

```sh
python -m venv venv
source ./venv/bin/activate
```

## Instalar dependencias

```sh
pip install "mcp[cli]"
```

## Ejecutar código

```sh
python client.py
```

Deberías ver el texto:

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por garantizar la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.