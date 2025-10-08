<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "ed9cab32cc67c12d8969b407aa47100a",
  "translation_date": "2025-07-13T17:53:32+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/java/README.md",
  "language_code": "ne"
}
-->
# बेसिक क्याल्कुलेटर MCP सेवा

यो सेवा Model Context Protocol (MCP) मार्फत Spring Boot र WebFlux ट्रान्सपोर्ट प्रयोग गरी आधारभूत क्याल्कुलेटर अपरेसनहरू प्रदान गर्छ। यो MCP कार्यान्वयनहरू सिक्न चाहने शुरुवातीहरूका लागि सरल उदाहरणको रूपमा डिजाइन गरिएको हो।

थप जानकारीका लागि, [MCP Server Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html) सन्दर्भ दस्तावेज हेर्नुहोस्।


## सेवाको प्रयोग

सेवाले MCP प्रोटोकल मार्फत तलका API अन्तर्विन्दुहरू उपलब्ध गराउँछ:

- `add(a, b)`: दुई संख्या जोड्नुहोस्
- `subtract(a, b)`: दोस्रो संख्या पहिलोबाट घटाउनुहोस्
- `multiply(a, b)`: दुई संख्या गुणा गर्नुहोस्
- `divide(a, b)`: पहिलो संख्या दोस्रोले भाग गर्नुहोस् (शून्य जाँचसहित)
- `power(base, exponent)`: कुनै संख्याको घात निकाल्नुहोस्
- `squareRoot(number)`: वर्गमूल निकाल्नुहोस् (ऋण संख्या जाँचसहित)
- `modulus(a, b)`: भाग गर्दा बाँकी रहेको भाग निकाल्नुहोस्
- `absolute(number)`: पूर्णांक मान निकाल्नुहोस्

## निर्भरता

प्रोजेक्टले तलका मुख्य निर्भरता आवश्यक पर्छ:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server-webflux</artifactId>
</dependency>
```

## प्रोजेक्ट बनाउने तरिका

Maven प्रयोग गरी प्रोजेक्ट बनाउनुहोस्:
```bash
./mvnw clean install -DskipTests
```

## सर्भर चलाउने तरिका

### Java प्रयोग गरेर

```bash
java -jar target/calculator-server-0.0.1-SNAPSHOT.jar
```

### MCP Inspector प्रयोग गरेर

MCP Inspector MCP सेवाहरूसँग अन्तरक्रिया गर्न सहयोगी उपकरण हो। यस क्याल्कुलेटर सेवासँग प्रयोग गर्न:

1. **MCP Inspector इन्स्टल गरी नयाँ टर्मिनल विन्डोमा चलाउनुहोस्**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **वेब UI पहुँच गर्नुहोस्**: एपले देखाएको URL मा क्लिक गर्नुहोस् (सामान्यतया http://localhost:6274)

3. **कनेक्शन सेटअप गर्नुहोस्**:
   - ट्रान्सपोर्ट प्रकार "SSE" मा सेट गर्नुहोस्
   - URL तपाईंको चलिरहेको सर्भरको SSE अन्तर्विन्दुमा सेट गर्नुहोस्: `http://localhost:8080/sse`
   - "Connect" मा क्लिक गर्नुहोस्

4. **उपकरणहरू प्रयोग गर्नुहोस्**:
   - उपलब्ध क्याल्कुलेटर अपरेसनहरू हेर्न "List Tools" मा क्लिक गर्नुहोस्
   - कुनै उपकरण छान्नुहोस् र अपरेसन चलाउन "Run Tool" मा क्लिक गर्नुहोस्

![MCP Inspector Screenshot](../../../../../../translated_images/tool.40e180a7b0d0fe2067cf96435532b01f63f7f8619d6b0132355a04b426b669ac.ne.png)

**अस्वीकरण**:  
यो दस्तावेज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी शुद्धताका लागि प्रयासरत छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटि वा अशुद्धता हुन सक्छ। मूल दस्तावेज यसको मूल भाषामा नै अधिकारिक स्रोत मानिनु पर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलतफहमी वा गलत व्याख्याका लागि हामी जिम्मेवार छैनौं।