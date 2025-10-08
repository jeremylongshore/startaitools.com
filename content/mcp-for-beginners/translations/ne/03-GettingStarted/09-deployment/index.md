<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1d9dc83260576b76f272d330ed93c51f",
  "translation_date": "2025-07-13T22:07:47+00:00",
  "source_file": "03-GettingStarted/09-deployment/README.md",
  "language_code": "ne"
}
-->
# MCP सर्भरहरू तैनाथ गर्ने

तपाईंको MCP सर्भर तैनाथ गर्दा अरूले यसको उपकरण र स्रोतहरू तपाईंको स्थानीय वातावरणभन्दा बाहिर पहुँच गर्न सक्छन्। तपाईंको आवश्यकताहरू अनुसार स्केलेबिलिटी, विश्वसनीयता, र व्यवस्थापन सजिलो बनाउन विभिन्न तैनाथ गर्ने रणनीतिहरू छन्। तल तपाईंले स्थानीय, कन्टेनरहरूमा, र क्लाउडमा MCP सर्भरहरू कसरी तैनाथ गर्ने बारे मार्गदर्शन पाउनुहुनेछ।

## अवलोकन

यस पाठले तपाईंको MCP Server एप कसरी तैनाथ गर्ने सिकाउँछ।

## सिकाइका उद्देश्यहरू

यस पाठको अन्त्यसम्म, तपाईं सक्षम हुनुहुनेछ:

- विभिन्न तैनाथ गर्ने तरिकाहरूको मूल्याङ्कन गर्न।
- तपाईंको एप तैनाथ गर्न।

## स्थानीय विकास र तैनाथीकरण

यदि तपाईंको सर्भर प्रयोगकर्ताको मेसिनमा चलाएर प्रयोग गरिनु पर्ने हो भने, तपाईंले तलका चरणहरू पालना गर्न सक्नुहुन्छ:

1. **सर्भर डाउनलोड गर्नुहोस्**। यदि तपाईंले सर्भर लेख्नुभएको छैन भने, पहिले यसलाई आफ्नो मेसिनमा डाउनलोड गर्नुहोस्।  
1. **सर्भर प्रक्रिया सुरु गर्नुहोस्**: तपाईंको MCP सर्भर एप्लिकेसन चलाउनुहोस्।

SSE का लागि (stdio प्रकारको सर्भरमा आवश्यक छैन)

1. **नेटवर्किङ कन्फिगर गर्नुहोस्**: सुनिश्चित गर्नुहोस् सर्भर अपेक्षित पोर्टमा पहुँचयोग्य छ।  
1. **क्लाइन्टहरू जडान गर्नुहोस्**: स्थानीय जडान URL हरू जस्तै `http://localhost:3000` प्रयोग गर्नुहोस्।

## क्लाउड तैनाथीकरण

MCP सर्भरहरू विभिन्न क्लाउड प्लेटफर्महरूमा तैनाथ गर्न सकिन्छ:

- **सर्भरलेस फंक्शनहरू**: हल्का MCP सर्भरहरू सर्भरलेस फंक्शनको रूपमा तैनाथ गर्नुहोस्।  
- **कन्टेनर सेवा**: Azure Container Apps, AWS ECS, वा Google Cloud Run जस्ता सेवाहरू प्रयोग गर्नुहोस्।  
- **कुबेरनेट्स**: उच्च उपलब्धताका लागि MCP सर्भरहरू कुबेरनेट्स क्लस्टरहरूमा तैनाथ र व्यवस्थापन गर्नुहोस्।

### उदाहरण: Azure Container Apps

Azure Container Apps ले MCP सर्भरहरूको तैनाथीकरण समर्थन गर्दछ। यो अझै विकासको क्रममा छ र हाल SSE सर्भरहरूलाई समर्थन गर्दछ।

यसरी गर्न सकिन्छ:

1. एउटा रिपोजिटरी क्लोन गर्नुहोस्:

  ```sh
  git clone https://github.com/anthonychu/azure-container-apps-mcp-sample.git
  ```

1. स्थानीय रूपमा परीक्षण गर्न यसलाई चलाउनुहोस्:

  ```sh
  uv venv
  uv sync

  # linux/macOS
  export API_KEYS=<AN_API_KEY>
  # windows
  set API_KEYS=<AN_API_KEY>

  uv run fastapi dev main.py
  ```

1. स्थानीय रूपमा प्रयास गर्न, *.vscode* डाइरेक्टरीमा *mcp.json* फाइल बनाउनुहोस् र तलको सामग्री थप्नुहोस्:

  ```json
  {
      "inputs": [
          {
              "type": "promptString",
              "id": "weather-api-key",
              "description": "Weather API Key",
              "password": true
          }
      ],
      "servers": {
          "weather-sse": {
              "type": "sse",
              "url": "http://localhost:8000/sse",
              "headers": {
                  "x-api-key": "${input:weather-api-key}"
              }
          }
      }
  }
  ```

  SSE सर्भर सुरु भएपछि, JSON फाइलमा प्ले आइकनमा क्लिक गर्न सक्नुहुन्छ, अब तपाईंले GitHub Copilot द्वारा सर्भरका उपकरणहरू पत्ता लगाइरहेको देख्नुहुनेछ, उपकरण आइकन हेर्नुहोस्।

1. तैनाथ गर्न, तलको कमाण्ड चलाउनुहोस्:

  ```sh
  az containerapp up -g <RESOURCE_GROUP_NAME> -n weather-mcp --environment mcp -l westus --env-vars API_KEYS=<AN_API_KEY> --source .
  ```

यति भयो, यसरी स्थानीय रूपमा वा Azure मा यी चरणहरू मार्फत तैनाथ गर्नुहोस्।

## थप स्रोतहरू

- [Azure Functions + MCP](https://learn.microsoft.com/en-us/samples/azure-samples/remote-mcp-functions-dotnet/remote-mcp-functions-dotnet/)
- [Azure Container Apps लेख](https://techcommunity.microsoft.com/blog/appsonazureblog/host-remote-mcp-servers-in-azure-container-apps/4403550)
- [Azure Container Apps MCP रिपो](https://github.com/anthonychu/azure-container-apps-mcp-sample)

## के आउनेछ

- अर्को: [व्यावहारिक कार्यान्वयन](../../04-PracticalImplementation/README.md)

**अस्वीकरण**:  
यो दस्तावेज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी शुद्धताका लागि प्रयासरत छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटि वा अशुद्धता हुन सक्छ। मूल दस्तावेज यसको मूल भाषामा नै अधिकारिक स्रोत मानिनु पर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलतफहमी वा गलत व्याख्याका लागि हामी जिम्मेवार छैनौं।