<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c3c28b090a54f59374677200e23a809e",
  "translation_date": "2025-10-06T16:03:04+00:00",
  "source_file": "03-GettingStarted/10-advanced/code/python/README.md",
  "language_code": "fr"
}
-->
# Exécuter l'exemple

## Configurer l'environnement virtuel

```sh
python -m venv venv
source ./venv/bin/activate
```

## Installer les dépendances

```sh
pip install "mcp[cli]"
```

## Exécuter le code

```sh
python client.py
```

Vous devriez voir le texte :

```text
Available tools: ['add']
Result of add tool: meta=None content=[TextContent(type='text', text='8.0', annotations=None, meta=None)] structuredContent=None isError=False
```

---

**Avertissement** :  
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue d'origine doit être considéré comme la source faisant autorité. Pour des informations critiques, il est recommandé de recourir à une traduction humaine professionnelle. Nous déclinons toute responsabilité en cas de malentendus ou d'interprétations erronées résultant de l'utilisation de cette traduction.