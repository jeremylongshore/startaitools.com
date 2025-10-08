<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "6d6315e03f591fb5a39be91da88585dc",
  "translation_date": "2025-07-13T19:19:18+00:00",
  "source_file": "03-GettingStarted/03-llm-client/solution/typescript/README.md",
  "language_code": "mr"
}
-->
# हा नमुना चालवणे

हा नमुना क्लायंटवर LLM असण्याचा समावेश करतो. LLM साठी तुम्हाला हा Codespaces मध्ये चालवावा लागेल किंवा GitHub मध्ये वैयक्तिक प्रवेश टोकन सेट करावे लागेल.

## -1- अवलंबित्वे इन्स्टॉल करा

```bash
npm install
```

## -3- सर्व्हर चालवा

```bash
npm run build
```

## -4- क्लायंट चालवा

```sh
npm run client
```

तुम्हाला खालीलप्रमाणे निकाल दिसेल:

```text
Asking server for available tools
MCPClient started on stdin/stdout
Querying LLM:  What is the sum of 2 and 3?
Making tool call
Calling tool add with args "{\"a\":2,\"b\":3}"
Tool result:  { content: [ { type: 'text', text: '5' } ] }
```

**अस्वीकरण**:  
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित केला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये चुका किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी अनुवाद करण्याची शिफारस केली जाते. या अनुवादाच्या वापरामुळे उद्भवलेल्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थलागी आम्ही जबाबदार नाही.