<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "8f12fc94cee9ed16a5eddf9f51fba755",
  "translation_date": "2025-07-13T23:28:15+00:00",
  "source_file": "04-PracticalImplementation/samples/javascript/README.md",
  "language_code": "fi"
}
-->
# Esimerkki

Tämä on JavaScript-esimerkki MCP-palvelimelle

Tässä on esimerkki työkalun rekisteröinnistä, jossa rekisteröimme työkalun, joka tekee simuloidun kutsun LLM:lle:

```javascript
this.mcpServer.tool(
    'completion',
    {
    model: z.string(),
    prompt: z.string(),
    options: z.object({
        temperature: z.number().optional(),
        max_tokens: z.number().optional(),
        stream: z.boolean().optional()
    }).optional()
    },
    async ({ model, prompt, options }) => {
    console.log(`Processing completion request for model: ${model}`);
    
    // Validate model
    if (!this.models.includes(model)) {
        throw new Error(`Model ${model} not supported`);
    }
    
    // Emit event for monitoring/metrics
    this.events.emit('request', { 
        type: 'completion', 
        model, 
        timestamp: new Date() 
    });
    
    // In a real implementation, this would call an AI model
    // Here we just echo back parts of the request with a mock response
    const response = {
        id: `mcp-resp-${Date.now()}`,
        model,
        text: `This is a response to: ${prompt.substring(0, 30)}...`,
        usage: {
        promptTokens: prompt.split(' ').length,
        completionTokens: 20,
        totalTokens: prompt.split(' ').length + 20
        }
    };
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Emit completion event
    this.events.emit('completion', {
        model,
        timestamp: new Date()
    });
    
    return {
        content: [
        {
            type: 'text',
            text: JSON.stringify(response)
        }
        ]
    };
    }
);
```

## Asennus

Suorita seuraava komento:

```bash
npm install
```

## Suorita

```bash
npm start
```

**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, huomioithan, että automaattikäännöksissä saattaa esiintyä virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulee pitää virallisena lähteenä. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.