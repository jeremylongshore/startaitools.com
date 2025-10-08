<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0f756f0d5b712847bd7d21b5e45c4166",
  "translation_date": "2025-10-07T01:40:37+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/code/jwt-lab/typescript/README.md",
  "language_code": "es"
}
-->
# Ejecutar ejemplo

## Instalar dependencias

```sh
npm install
```

## Ejecutar código

```sh
npm run build
```

```sh
npm start
```

deberías ver un resultado similar a:

```text
JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlVzZXIgdXNlcnNzb24iLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNzU5MTY4NzIyLCJleHAiOjE3NTkxNzIzMjJ9.JAMGCX_sHdqHzsKqqg6jHFUGk6zYZB7N77mWDqcRMcY
Decoded Payload: {
  sub: '1234567890',
  name: 'User usersson',
  admin: true,
  iat: 1759168722,
  exp: 1759172322
```

---

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por garantizar la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.