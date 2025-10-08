<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "92af35e8c34923031f3d228dffad9ebb",
  "translation_date": "2025-09-03T16:03:44+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/dotnet/README.md",
  "language_code": "mr"
}
-->
# हे नमुना चालवणे

## -1- आवश्यक गोष्टी स्थापित करा

```bash
dotnet restore
```

## -3- नमुना चालवा

```bash
dotnet run
```

## -4- नमुना तपासा

सर्व्हर एका टर्मिनलमध्ये चालू असताना, दुसरे टर्मिनल उघडा आणि खालील कमांड चालवा:

```bash
npx @modelcontextprotocol/inspector dotnet run
```

यामुळे एक वेब सर्व्हर सुरू होईल ज्यामध्ये दृश्य इंटरफेस असेल, ज्याद्वारे तुम्ही नमुना तपासू शकता.

सर्व्हर कनेक्ट झाल्यावर:

- टूल्स सूचीबद्ध करण्याचा प्रयत्न करा आणि `add` चालवा, args 2 आणि 4 सह, तुम्हाला निकालामध्ये 6 दिसेल.
- संसाधने आणि संसाधन टेम्पलेटला जा आणि "greeting" कॉल करा, नाव टाइप करा आणि तुम्ही दिलेल्या नावासह अभिवादन दिसेल.

### CLI मोडमध्ये तपासणी

CLI मोडमध्ये थेट सुरू करण्यासाठी खालील कमांड चालवा:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/list
```

यामुळे सर्व्हरमध्ये उपलब्ध असलेल्या सर्व टूल्सची यादी दिसेल. तुम्हाला खालील आउटपुट दिसेल:

```text
{
  "tools": [
    {
      "name": "Add",
      "description": "Adds two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer"
          },
          "b": {
            "type": "integer"
          }
        },
        "title": "Add",
        "description": "Adds two numbers",
        "required": [
          "a",
          "b"
        ]
      }
    }
  ]
}
```

टूल चालवण्यासाठी टाइप करा:

```bash
npx @modelcontextprotocol/inspector --cli dotnet run --method tools/call --tool-name Add --tool-arg a=1 --tool-arg b=2
```

तुम्हाला खालील आउटपुट दिसेल:

```text
{
  "content": [
    {
      "type": "text",
      "text": "Sum 3"
    }
  ],
  "isError": false
}
```

> [!TIP]
> CLI मोडमध्ये निरीक्षक चालवणे ब्राउझरपेक्षा सहसा खूप जलद असते.
> निरीक्षकाबद्दल अधिक वाचा [येथे](https://github.com/modelcontextprotocol/inspector).

---

**अस्वीकरण**:  
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून भाषांतरित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात ठेवा की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेचा अभाव असू शकतो. मूळ भाषेतील दस्तऐवज हा अधिकृत स्रोत मानावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराचा वापर करून निर्माण होणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थासाठी आम्ही जबाबदार राहणार नाही.