<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "6d6315e03f591fb5a39be91da88585dc",
  "translation_date": "2025-07-13T19:20:18+00:00",
  "source_file": "03-GettingStarted/03-llm-client/solution/typescript/README.md",
  "language_code": "fi"
}
-->
# Tämän esimerkin suorittaminen

Tässä esimerkissä käytetään LLM:ää asiakkaalla. LLM tarvitsee, että suoritat tämän joko Codespacesissa tai asetat henkilökohtaisen käyttöoikeustunnuksen GitHubiin toimiakseen.

## -1- Asenna riippuvuudet

```bash
npm install
```

## -3- Käynnistä palvelin

```bash
npm run build
```

## -4- Käynnistä asiakas

```sh
npm run client
```

Näet tuloksen, joka näyttää suunnilleen tältä:

```text
Asking server for available tools
MCPClient started on stdin/stdout
Querying LLM:  What is the sum of 2 and 3?
Making tool call
Calling tool add with args "{\"a\":2,\"b\":3}"
Tool result:  { content: [ { type: 'text', text: '5' } ] }
```

**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, huomioithan, että automaattikäännöksissä saattaa esiintyä virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulee pitää virallisena lähteenä. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.