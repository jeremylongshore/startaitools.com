<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "6ebbb78b04c9b1f6c2367c713524fc95",
  "translation_date": "2025-09-03T16:03:35+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/typescript/README.md",
  "language_code": "mr"
}
-->
# हे नमुना चालवणे

`uv` स्थापित करणे शिफारस केले जाते, परंतु ते आवश्यक नाही, [सूचना](https://docs.astral.sh/uv/#highlights) पहा.

## -1- अवलंबित्व स्थापित करा

```bash
npm install
```

## -3- नमुना चालवा

```bash
npm run build
```

## -4- नमुना चाचणी करा

सर्व्हर एका टर्मिनलमध्ये चालू असताना, दुसरे टर्मिनल उघडा आणि खालील कमांड चालवा:

```bash
npm run inspector
```

यामुळे एक वेब सर्व्हर सुरू होईल ज्यामध्ये व्हिज्युअल इंटरफेस असेल, ज्याद्वारे तुम्ही नमुना चाचणी करू शकता.

सर्व्हर कनेक्ट झाल्यावर:

- टूल्स सूचीबद्ध करण्याचा प्रयत्न करा आणि `add` चालवा, args 2 आणि 4 सह, तुम्हाला निकालात 6 दिसेल.
- संसाधनांवर जा आणि संसाधन टेम्पलेटमध्ये "greeting" कॉल करा, नाव टाइप करा आणि तुम्ही दिलेल्या नावासह अभिवादन दिसेल.

### CLI मोडमध्ये चाचणी करणे

तुम्ही चालवलेला निरीक्षक प्रत्यक्षात एक Node.js अॅप आहे आणि `mcp dev` त्याभोवती एक रॅपर आहे.

तुम्ही खालील कमांड चालवून CLI मोडमध्ये थेट लॉन्च करू शकता:

```bash
npx @modelcontextprotocol/inspector --cli node ./build/index.js --method tools/list
```

यामुळे सर्व्हरमध्ये उपलब्ध असलेली सर्व टूल्स सूचीबद्ध होतील. तुम्हाला खालील आउटपुट दिसेल:

```text
{
  "tools": [
    {
      "name": "add",
      "description": "Add two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "title": "A",
            "type": "integer"
          },
          "b": {
            "title": "B",
            "type": "integer"
          }
        },
        "required": [
          "a",
          "b"
        ],
        "title": "addArguments"
      }
    }
  ]
}
```

टूल चालवण्यासाठी टाइप करा:

```bash
nnpx @modelcontextprotocol/inspector --cli node ./build/index.js --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

तुम्हाला खालील आउटपुट दिसेल:

```text
{
  "content": [
    {
      "type": "text",
      "text": "3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> ब्राउझरमध्ये निरीक्षक चालवण्यापेक्षा CLI मोडमध्ये चालवणे सहसा खूप जलद असते.
> निरीक्षकाबद्दल अधिक वाचा [येथे](https://github.com/modelcontextprotocol/inspector).

---

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी कृपया लक्षात ठेवा की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेचा अभाव असू शकतो. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून निर्माण होणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.