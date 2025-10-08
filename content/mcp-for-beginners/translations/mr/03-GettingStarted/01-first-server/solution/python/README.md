<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d4c162484df410632550a4a357d40341",
  "translation_date": "2025-09-03T16:03:26+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "mr"
}
-->
# हे नमुना चालवणे

`uv` स्थापित करणे शिफारस केले जाते, परंतु ते आवश्यक नाही, [सूचना](https://docs.astral.sh/uv/#highlights) पहा.

## -0- एक आभासी वातावरण तयार करा

```bash
python -m venv venv
```

## -1- आभासी वातावरण सक्रिय करा

```bash
venv\Scripts\activate
```

## -2- आवश्यक गोष्टी स्थापित करा

```bash
pip install "mcp[cli]"
```

## -3- नमुना चालवा

```bash
mcp run server.py
```

## -4- नमुना तपासा

सर्व्हर एका टर्मिनलमध्ये चालू असताना, दुसरे टर्मिनल उघडा आणि खालील आदेश चालवा:

```bash
mcp dev server.py
```

यामुळे एक वेब सर्व्हर सुरू होईल ज्यामध्ये दृश्य इंटरफेस असेल, ज्याद्वारे तुम्ही नमुना तपासू शकता.

सर्व्हर कनेक्ट झाल्यावर:

- टूल्स सूचीबद्ध करण्याचा प्रयत्न करा आणि `add` चालवा, args 2 आणि 4 सह, तुम्हाला निकालात 6 दिसेल.

- संसाधनांमध्ये जा आणि resource template वर जा, get_greeting कॉल करा, नाव टाइप करा आणि तुम्ही दिलेल्या नावासह अभिवादन दिसेल.

### CLI मोडमध्ये चाचणी करणे

तुम्ही चालवलेला inspector प्रत्यक्षात एक Node.js अॅप आहे आणि `mcp dev` त्याभोवती एक wrapper आहे.

तुम्ही खालील आदेश चालवून ते थेट CLI मोडमध्ये सुरू करू शकता:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
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
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
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
> ब्राउझरमध्ये inspector चालवण्यापेक्षा CLI मोडमध्ये चालवणे सहसा खूप जलद असते.
> inspector बद्दल अधिक वाचा [येथे](https://github.com/modelcontextprotocol/inspector).

---

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात ठेवा की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेचा अभाव असू शकतो. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून उद्भवलेल्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.