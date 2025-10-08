<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "882aae00f1d3f007e20d03b883f44afa",
  "translation_date": "2025-07-13T22:14:55+00:00",
  "source_file": "03-GettingStarted/samples/csharp/README.md",
  "language_code": "mr"
}
-->
# Basic Calculator MCP सेवा

ही सेवा Model Context Protocol (MCP) द्वारे मूलभूत कॅल्क्युलेटर ऑपरेशन्स प्रदान करते. हे MCP अंमलबजावणी शिकणाऱ्या नवशिक्यांसाठी एक सोपा उदाहरण म्हणून डिझाइन केले आहे.

अधिक माहितीसाठी, पहा [C# SDK](https://github.com/modelcontextprotocol/csharp-sdk)

## वैशिष्ट्ये

हा कॅल्क्युलेटर सेवा खालील क्षमता देते:

1. **मूलभूत अंकगणितीय क्रिया**:
   - दोन संख्यांची बेरीज
   - एका संख्येतून दुसरी संख्या वजा करणे
   - दोन संख्यांची गुणाकार
   - एका संख्येचे दुसऱ्या संख्येने भागाकार (शून्याने भाग देण्याची तपासणी सह)

## `stdio` प्रकार वापरणे

## कॉन्फिगरेशन

1. **MCP सर्व्हर्स कॉन्फिगर करा**:
   - तुमचा वर्कस्पेस VS Code मध्ये उघडा.
   - तुमच्या वर्कस्पेस फोल्डरमध्ये `.vscode/mcp.json` फाइल तयार करा ज्यात MCP सर्व्हर्स कॉन्फिगर करता येतील. उदाहरण कॉन्फिगरेशन:

     ```jsonc
     {
       "inputs": [
         {
           "type": "promptString",
           "id": "repository-root",
           "description": "The absolute path to the repository root"
         }
       ],
       "servers": {
         "calculator-mcp-dotnet": {
           "type": "stdio",
           "command": "dotnet",
           "args": [
             "run",
             "--project",
             "${input:repository-root}/03-GettingStarted/samples/csharp/src/calculator.csproj"
           ]
         }
       }
     }
     ```

   - तुम्हाला GitHub रिपॉझिटरी रूट प्रविष्ट करण्यास सांगितले जाईल, जो `git rev-parse --show-toplevel` या कमांडने मिळवता येतो.

## सेवा वापरणे

ही सेवा MCP प्रोटोकॉलद्वारे खालील API एंडपॉइंट्स उपलब्ध करून देते:

- `add(a, b)`: दोन संख्या एकत्र करा
- `subtract(a, b)`: दुसरी संख्या पहिल्या संख्येतून वजा करा
- `multiply(a, b)`: दोन संख्या गुणा करा
- `divide(a, b)`: पहिली संख्या दुसऱ्या संख्येने भागा (शून्य तपासणीसह)
- isPrime(n): संख्या मूळ आहे का ते तपासा

## VS Code मधील Github Copilot Chat सह चाचणी करा

1. MCP प्रोटोकॉल वापरून सेवेवर विनंती करण्याचा प्रयत्न करा. उदाहरणार्थ, तुम्ही विचारू शकता:
   - "Add 5 and 3"
   - "Subtract 10 from 4"
   - "Multiply 6 and 7"
   - "Divide 8 by 2"
   - "Does 37854 prime?"
   - "What are the 3 prime numbers before after 4242?"
2. हे सुनिश्चित करण्यासाठी की ते टूल्स वापरत आहे, प्रॉम्प्टमध्ये #MyCalculator जोडा. उदाहरणार्थ:
   - "Add 5 and 3 #MyCalculator"
   - "Subtract 10 from 4 #MyCalculator"

## कंटेनराइज्ड आवृत्ती

पूर्वीचे समाधान तेव्हा उत्तम आहे जेव्हा तुमच्याकडे .NET SDK इन्स्टॉल केलेले असेल आणि सर्व अवलंबित्वे उपलब्ध असतील. मात्र, जर तुम्हाला हे समाधान शेअर करायचे असेल किंवा वेगळ्या वातावरणात चालवायचे असेल, तर तुम्ही कंटेनराइज्ड आवृत्ती वापरू शकता.

1. Docker सुरू करा आणि ते चालू आहे याची खात्री करा.
1. टर्मिनलमधून `03-GettingStarted\samples\csharp\src` फोल्डरमध्ये जा
1. कॅल्क्युलेटर सेवेचा Docker इमेज तयार करण्यासाठी खालील कमांड चालवा ( `<YOUR-DOCKER-USERNAME>` च्या जागी तुमचा Docker Hub वापरकर्ता नाव टाका):
   ```bash
   docker build -t <YOUR-DOCKER-USERNAME>/mcp-calculator .
   ```
1. इमेज तयार झाल्यानंतर, Docker Hub वर अपलोड करा. खालील कमांड चालवा:
   ```bash
    docker push <YOUR-DOCKER-USERNAME>/mcp-calculator
  ```

## Dockerized आवृत्ती वापरा

1. `.vscode/mcp.json` फाइलमध्ये सर्व्हर कॉन्फिगरेशन खालीलप्रमाणे बदला:
   ```json
    "mcp-calc": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "<YOUR-DOCKER-USERNAME>/mcp-calc"
      ],
      "envFile": "",
      "env": {}
    }
   ```
   कॉन्फिगरेशन पाहता, कमांड `docker` आहे आणि args आहेत `run --rm -i <YOUR-DOCKER-USERNAME>/mcp-calc`. `--rm` फ्लॅग कंटेनर थांबल्यानंतर तो काढून टाकतो, आणि `-i` फ्लॅग कंटेनरच्या स्टँडर्ड इनपुटशी संवाद साधण्याची परवानगी देतो. शेवटचा आर्ग्युमेंट म्हणजे आपण तयार केलेली आणि Docker Hub वर अपलोड केलेली इमेजचे नाव.

## Dockerized आवृत्तीची चाचणी करा

`"mcp-calc": {` च्या वर असलेल्या लहान Start बटणावर क्लिक करून MCP सर्व्हर सुरू करा, आणि अगदी आधीप्रमाणे तुम्ही कॅल्क्युलेटर सेवेवर गणिती प्रश्न विचारू शकता.

**अस्वीकरण**:  
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित केला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये चुका किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी अनुवाद करण्याची शिफारस केली जाते. या अनुवादाच्या वापरामुळे उद्भवलेल्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थलागी आम्ही जबाबदार नाही.