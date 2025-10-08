<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "904b59de1de9264801242d90a42cdd9d",
  "translation_date": "2025-09-05T11:23:08+00:00",
  "source_file": "01-CoreConcepts/README.md",
  "language_code": "sw"
}
-->
# MCP Dhana Muhimu: Kuelewa Itifaki ya Model Context kwa Muunganisho wa AI

[![MCP Dhana Muhimu](../../../translated_images/02.8203e26c6fb5a797f38a10012061013ec66c95bb3260f6c9cfd2bf74b00860e1.sw.png)](https://youtu.be/earDzWGtE84)

_(Bofya picha hapo juu kutazama video ya somo hili)_

[Model Context Protocol (MCP)](https://github.com/modelcontextprotocol) ni mfumo wenye nguvu na uliosanifishwa unaoboreshwa mawasiliano kati ya Large Language Models (LLMs) na zana za nje, programu, na vyanzo vya data. Mwongozo huu utakufundisha dhana kuu za MCP. Utajifunza kuhusu usanifu wa mteja-server, vipengele muhimu, mitambo ya mawasiliano, na mbinu bora za utekelezaji.

- **Idhini ya Mtumiaji ya Wazi**: Ufikiaji wa data na operesheni zote zinahitaji idhini ya wazi ya mtumiaji kabla ya utekelezaji. Watumiaji wanapaswa kuelewa wazi ni data gani itakayofikiwa na ni hatua gani zitakazochukuliwa, huku wakidhibiti kwa undani ruhusa na idhini.

- **Ulinzi wa Faragha ya Data**: Data ya mtumiaji inapaswa kufikiwa tu kwa idhini ya wazi na lazima ilindwe na udhibiti madhubuti wa ufikiaji katika mzunguko mzima wa mwingiliano. Utekelezaji lazima uzuie usambazaji wa data bila idhini na kudumisha mipaka madhubuti ya faragha.

- **Usalama wa Utekelezaji wa Zana**: Kila mwito wa zana unahitaji idhini ya wazi ya mtumiaji pamoja na ufahamu wa wazi wa utendaji wa zana, vigezo, na athari zinazoweza kutokea. Mipaka madhubuti ya usalama lazima izuie utekelezaji wa zana usio tarajiwa, usio salama, au wenye nia mbaya.

- **Usalama wa Tabaka la Usafirishaji**: Njia zote za mawasiliano zinapaswa kutumia mbinu sahihi za usimbaji na uthibitishaji. Muunganisho wa mbali unapaswa kutekeleza itifaki salama za usafirishaji na usimamizi sahihi wa hati za kuingia.

#### Miongozo ya Utekelezaji:

- **Usimamizi wa Ruhusa**: Tekeleza mifumo ya ruhusa ya kina inayoruhusu watumiaji kudhibiti ni seva, zana, na rasilimali gani zinapatikana
- **Uthibitishaji na Idhini**: Tumia mbinu salama za uthibitishaji (OAuth, funguo za API) na usimamizi sahihi wa tokeni na muda wake wa kuisha  
- **Uthibitishaji wa Ingizo**: Thibitisha vigezo vyote na data za ingizo kulingana na schemas zilizofafanuliwa ili kuzuia mashambulizi ya sindikizo
- **Kumbukumbu za Ukaguzi**: Dumisha kumbukumbu kamili za operesheni zote kwa ufuatiliaji wa usalama na kufuata sheria

## Muhtasari

Somo hili linachunguza usanifu wa msingi na vipengele vinavyounda mfumo wa Model Context Protocol (MCP). Utajifunza kuhusu usanifu wa mteja-server, vipengele muhimu, na mitambo ya mawasiliano inayowezesha mwingiliano wa MCP.

## Malengo Muhimu ya Kujifunza

Mwisho wa somo hili, utakuwa na uwezo wa:

- Kuelewa usanifu wa mteja-server wa MCP.
- Kutambua majukumu na wajibu wa Hosts, Clients, na Servers.
- Kuchambua vipengele vya msingi vinavyofanya MCP kuwa safu rahisi ya muunganisho.
- Kujifunza jinsi taarifa zinavyotiririka ndani ya mfumo wa MCP.
- Kupata maarifa ya vitendo kupitia mifano ya msimbo katika .NET, Java, Python, na JavaScript.

## Usanifu wa MCP: Uchambuzi wa Kina

Mfumo wa MCP umejengwa juu ya modeli ya mteja-server. Muundo huu wa moduli unaruhusu programu za AI kuingiliana na zana, hifadhidata, API, na rasilimali za muktadha kwa ufanisi. Hebu tuchambue usanifu huu katika vipengele vyake vya msingi.

Kwa msingi wake, MCP inafuata usanifu wa mteja-server ambapo programu ya mwenyeji inaweza kuunganishwa na seva nyingi:

```mermaid
flowchart LR
    subgraph "Your Computer"
        Host["Host with MCP (Visual Studio, VS Code, IDEs, Tools)"]
        S1["MCP Server A"]
        S2["MCP Server B"]
        S3["MCP Server C"]
        Host <-->|"MCP Protocol"| S1
        Host <-->|"MCP Protocol"| S2
        Host <-->|"MCP Protocol"| S3
        S1 <--> D1[("Local\Data Source A")]
        S2 <--> D2[("Local\Data Source B")]
    end
    subgraph "Internet"
        S3 <-->|"Web APIs"| D3[("Remote\Services")]
    end
```

- **MCP Hosts**: Programu kama VSCode, Claude Desktop, IDEs, au zana za AI zinazotaka kufikia data kupitia MCP
- **MCP Clients**: Wateja wa itifaki wanaodumisha muunganisho wa 1:1 na seva
- **MCP Servers**: Programu nyepesi zinazofichua uwezo maalum kupitia Model Context Protocol iliyosanifishwa
- **Vyanzo vya Data vya Ndani**: Faili za kompyuta yako, hifadhidata, na huduma ambazo seva za MCP zinaweza kufikia kwa usalama
- **Huduma za Mbali**: Mifumo ya nje inayopatikana kupitia mtandao ambayo seva za MCP zinaweza kuunganishwa nayo kupitia API.

Itifaki ya MCP ni kiwango kinachobadilika kinachotumia toleo la tarehe (muundo wa YYYY-MM-DD). Toleo la sasa la itifaki ni **2025-06-18**. Unaweza kuona masasisho ya hivi karibuni ya [maelezo ya itifaki](https://modelcontextprotocol.io/specification/2025-06-18/)

### 1. Hosts

Katika Model Context Protocol (MCP), **Hosts** ni programu za AI zinazohudumu kama kiolesura cha msingi ambacho watumiaji wanatumia kuingiliana na itifaki. Hosts zinasimamia na kudhibiti muunganisho na seva nyingi za MCP kwa kuunda wateja wa MCP maalum kwa kila muunganisho wa seva. Mifano ya Hosts ni pamoja na:

- **Programu za AI**: Claude Desktop, Visual Studio Code, Claude Code
- **Mazingira ya Maendeleo**: IDEs na wahariri wa msimbo wenye muunganisho wa MCP  
- **Programu Maalum**: Mawakala wa AI na zana zilizojengwa kwa madhumuni maalum

**Hosts** ni programu zinazoratibu mwingiliano wa modeli za AI. Zinafanya kazi zifuatazo:

- **Kuratibu Modeli za AI**: Kutekeleza au kuingiliana na LLMs ili kutoa majibu na kuratibu mtiririko wa kazi za AI
- **Kusimamia Muunganisho wa Wateja**: Kuunda na kudumisha mteja mmoja wa MCP kwa kila muunganisho wa seva ya MCP
- **Kudhibiti Kiolesura cha Mtumiaji**: Kushughulikia mtiririko wa mazungumzo, mwingiliano wa mtumiaji, na uwasilishaji wa majibu  
- **Kutekeleza Usalama**: Kudhibiti ruhusa, vikwazo vya usalama, na uthibitishaji
- **Kushughulikia Idhini ya Mtumiaji**: Kusimamia idhini ya mtumiaji kwa kushiriki data na utekelezaji wa zana

### 2. Clients

**Clients** ni vipengele muhimu vinavyodumisha muunganisho wa moja kwa moja kati ya Hosts na seva za MCP. Kila mteja wa MCP huanzishwa na Host kuunganishwa na seva maalum ya MCP, kuhakikisha njia za mawasiliano zilizoandaliwa na salama. Wateja wengi huruhusu Hosts kuunganishwa na seva nyingi kwa wakati mmoja.

**Clients** ni vipengele vya kiunganishi ndani ya programu ya mwenyeji. Zinafanya kazi zifuatazo:

- **Mawasiliano ya Itifaki**: Kutuma maombi ya JSON-RPC 2.0 kwa seva na maelekezo
- **Majadiliano ya Uwezo**: Kujadiliana vipengele vinavyoungwa mkono na matoleo ya itifaki na seva wakati wa kuanzisha
- **Utekelezaji wa Zana**: Kusimamia maombi ya utekelezaji wa zana kutoka kwa modeli na kuchakata majibu
- **Masasisho ya Wakati Halisi**: Kushughulikia arifa na masasisho ya wakati halisi kutoka kwa seva
- **Usindikaji wa Majibu**: Kuchakata na kuunda majibu ya seva kwa kuonyesha kwa watumiaji

### 3. Servers

**Servers** ni programu zinazotoa muktadha, zana, na uwezo kwa wateja wa MCP. Zinaweza kutekelezwa ndani (kwenye mashine sawa na Host) au mbali (kwenye majukwaa ya nje), na zinawajibika kushughulikia maombi ya wateja na kutoa majibu yaliyoandaliwa. Servers hufichua utendaji maalum kupitia Model Context Protocol iliyosanifishwa.

**Servers** ni huduma zinazotoa muktadha na uwezo. Zinafanya kazi zifuatazo:

- **Usajili wa Vipengele**: Kusajili na kufichua primitives zinazopatikana (rasilimali, maelekezo, zana) kwa wateja
- **Usindikaji wa Maombi**: Kupokea na kutekeleza miito ya zana, maombi ya rasilimali, na maombi ya maelekezo kutoka kwa wateja
- **Utoaji wa Muktadha**: Kutoa taarifa za muktadha na data ili kuboresha majibu ya modeli
- **Usimamizi wa Hali**: Kudumisha hali ya kikao na kushughulikia mwingiliano wa hali wakati inahitajika
- **Arifa za Wakati Halisi**: Kutuma arifa kuhusu mabadiliko ya uwezo na masasisho kwa wateja waliounganishwa

Servers zinaweza kuendelezwa na mtu yeyote ili kupanua uwezo wa modeli kwa utendaji maalum, na zinaunga mkono hali za utekelezaji wa ndani na wa mbali.

### 4. Primitives za Seva

Servers katika Model Context Protocol (MCP) hutoa **primitives** tatu kuu zinazofafanua vipengele vya msingi vya mwingiliano tajiri kati ya wateja, Hosts, na modeli za lugha. Primitives hizi zinaelezea aina za taarifa za muktadha na hatua zinazopatikana kupitia itifaki.

Seva za MCP zinaweza kufichua mchanganyiko wowote wa primitives tatu kuu zifuatazo:

#### Rasilimali

**Rasilimali** ni vyanzo vya data vinavyotoa taarifa za muktadha kwa programu za AI. Zinawakilisha maudhui ya tuli au ya nguvu yanayoweza kuboresha uelewa wa modeli na kufanya maamuzi:

- **Data ya Muktadha**: Taarifa zilizopangwa na muktadha kwa matumizi ya modeli za AI
- **Misingi ya Maarifa**: Hifadhi za nyaraka, makala, miongozo, na karatasi za utafiti
- **Vyanzo vya Data vya Ndani**: Faili, hifadhidata, na taarifa za mfumo wa ndani  
- **Data ya Nje**: Majibu ya API, huduma za wavuti, na data ya mifumo ya mbali
- **Maudhui ya Nguvu**: Data ya wakati halisi inayosasishwa kulingana na hali za nje

Rasilimali zinatambuliwa na URIs na zinaunga mkono ugunduzi kupitia `resources/list` na upatikanaji kupitia `resources/read`:

```text
file://documents/project-spec.md
database://production/users/schema
api://weather/current
```

#### Maelekezo

**Maelekezo** ni templeti zinazoweza kutumika tena zinazosaidia kuunda mwingiliano na modeli za lugha. Zinatoa mifumo sanifishwa ya mwingiliano na mtiririko wa kazi uliotemplatishwa:

- **Mwingiliano wa Kitempleti**: Ujumbe uliopangwa awali na vianzilishi vya mazungumzo
- **Templeti za Mtiririko wa Kazi**: Mfuatano sanifishwa wa kazi za kawaida na mwingiliano
- **Mifano ya Few-shot**: Templeti za msingi wa mifano kwa maelekezo ya modeli
- **Maelekezo ya Mfumo**: Maelekezo ya msingi yanayofafanua tabia ya modeli na muktadha
- **Templeti za Nguvu**: Maelekezo yenye vigezo vinavyobadilika kulingana na muktadha maalum

Maelekezo yanaunga mkono uingizwaji wa vigezo na yanaweza kugunduliwa kupitia `prompts/list` na kupatikana kwa `prompts/get`:

```markdown
Generate a {{task_type}} for {{product}} targeting {{audience}} with the following requirements: {{requirements}}
```

#### Zana

**Zana** ni kazi zinazoweza kutekelezwa ambazo modeli za AI zinaweza kuziita ili kutekeleza hatua maalum. Zinawakilisha "vitenzi" vya mfumo wa MCP, kuwezesha modeli kuingiliana na mifumo ya nje:

- **Kazi Zinazoweza Kutekelezwa**: Operesheni za pekee ambazo modeli zinaweza kuziita na vigezo maalum
- **Muunganisho wa Mfumo wa Nje**: Miito ya API, maswali ya hifadhidata, operesheni za faili, hesabu
- **Utambulisho wa Kipekee**: Kila zana ina jina tofauti, maelezo, na schema ya vigezo
- **I/O Iliyosanifishwa**: Zana zinakubali vigezo vilivyothibitishwa na kurudisha majibu yaliyoandaliwa, yaliyoainishwa
- **Uwezo wa Hatua**: Kuwezesha modeli kutekeleza hatua za ulimwengu halisi na kupata data ya moja kwa moja

Zana zinafafanuliwa na JSON Schema kwa uthibitishaji wa vigezo na kugunduliwa kupitia `tools/list` na kutekelezwa kupitia `tools/call`:

```typescript
server.tool(
  "search_products", 
  {
    query: z.string().describe("Search query for products"),
    category: z.string().optional().describe("Product category filter"),
    max_results: z.number().default(10).describe("Maximum results to return")
  }, 
  async (params) => {
    // Execute search and return structured results
    return await productService.search(params);
  }
);
```

## Primitives za Mteja

Katika Model Context Protocol (MCP), **wateja** wanaweza kufichua primitives zinazowezesha seva kuomba uwezo wa ziada kutoka kwa programu ya mwenyeji. Primitives hizi za upande wa mteja huruhusu utekelezaji wa seva tajiri zaidi, wa mwingiliano zaidi unaoweza kufikia uwezo wa modeli za AI na mwingiliano wa mtumiaji.

### Sampuli

**Sampuli** inaruhusu seva kuomba ukamilishaji wa modeli za lugha kutoka kwa programu ya AI ya mteja. Primitive hii inawawezesha seva kufikia uwezo wa LLM bila kujumuisha utegemezi wa modeli zao wenyewe:

- **Ufikiaji wa Modeli Bila Kujitegemea**: Seva zinaweza kuomba ukamilishaji bila kujumuisha SDK za LLM au kusimamia ufikiaji wa modeli
- **AI Inayoanzishwa na Seva**: Inawawezesha seva kuunda maudhui kwa uhuru kwa kutumia modeli ya AI ya mteja
- **Mwingiliano wa LLM wa Kurejelea**: Inasaidia hali ngumu ambapo seva zinahitaji msaada wa AI kwa usindikaji
- **Uundaji wa Maudhui ya Nguvu**: Inaruhusu seva kuunda majibu ya muktadha kwa kutumia modeli ya mwenyeji

Sampuli huanzishwa kupitia njia ya `sampling/complete`, ambapo seva zinatuma maombi ya ukamilishaji kwa wateja.

### Uchochezi  

**Uchochezi** unaruhusu seva kuomba taarifa za ziada au uthibitisho kutoka kwa watumiaji kupitia kiolesura cha mteja:

- **Maombi ya Ingizo la Mtumiaji**: Seva zinaweza kuuliza taarifa za ziada zinapohitajika kwa utekelezaji wa zana
- **Mazungumzo ya Uthibitisho**: Kuomba idhini ya mtumiaji kwa operesheni nyeti au zenye athari kubwa
- **Mtiririko wa Kazi wa Mwingiliano**: Kuwezesha seva kuunda mwingiliano wa hatua kwa hatua na mtumiaji
- **Ukusanyaji wa Vigezo vya Nguvu**: Kukusanya vigezo vinavyokosekana au vya hiari wakati wa utekelezaji wa zana

Maombi ya uchochezi hufanywa kwa kutumia njia ya `elicitation/request` ili kukusanya ingizo la mtumiaji kupitia kiolesura cha mteja.

### Kumbukumbu

**Kumbukumbu** inaruhusu seva kutuma ujumbe wa kumbukumbu ulioandaliwa kwa wateja kwa ajili ya urekebishaji, ufuatiliaji, na mwonekano wa operesheni:

- **Msaada wa Urekebishaji**: Kuwezesha seva kutoa kumbukumbu za utekelezaji za kina kwa utatuzi wa matatizo
- **Ufuatiliaji wa Operesheni**: Kutuma masasisho ya hali na vipimo vya utendaji kwa wateja
- **Ripoti za Makosa**: Kutoa muktadha wa makosa na taarifa za uchunguzi
- **Njia za Ukaguzi**: Kuunda kumbukumbu kamili za operesheni za seva na maamuzi

Ujumbe wa kumbukumbu hutumwa kwa wateja ili kutoa uwazi katika operesheni za seva na kuwezesha urekebishaji.

## Mtiririko wa Taarifa katika MCP

Model Context Protocol (MCP) inafafanua mtiririko uliopangwa wa taarifa kati ya Hosts, wateja, seva, na modeli. Kuelewa mtiririko huu husaidia kufafanua jinsi maombi ya mtumiaji yanavyosindikwa na jinsi zana za nje na data zinavyounganishwa katika majibu ya modeli.

- **Host Inaanzisha Muunganisho**  
  Programu ya mwenyeji (kama IDE au kiolesura cha mazungumzo) huanzisha muunganisho na seva ya MCP, kawaida kupitia STDIO, WebSocket, au njia nyingine inayoungwa mkono.

- **Majadiliano ya Uwezo**  
  Mteja (uliowekwa ndani ya mwenyeji) na seva hubadilishana taarifa kuhusu vipengele vinavyoungwa mkono, zana, rasilimali, na matoleo ya itifaki. Hii inahakikisha pande zote mbili zinaelewa uwezo gani unapatikana kwa kikao.

- **Ombi la Mtumiaji**  
  Mtumiaji hu
- **JSON-RPC 2.0 Protocol**: Mawasiliano yote hutumia muundo wa ujumbe wa JSON-RPC 2.0 uliosanifishwa kwa miito ya mbinu, majibu, na arifa.
- **Usimamizi wa Mzunguko wa Maisha**: Husimamia uanzishaji wa muunganisho, mazungumzo ya uwezo, na kukomesha kikao kati ya wateja na seva.
- **Vipengele vya Seva**: Huwezesha seva kutoa utendaji wa msingi kupitia zana, rasilimali, na maelekezo.
- **Vipengele vya Mteja**: Huwezesha seva kuomba sampuli kutoka kwa LLMs, kuchochea maoni ya mtumiaji, na kutuma ujumbe wa kumbukumbu.
- **Arifa za Wakati Halisi**: Inasaidia arifa za asinkroni kwa masasisho ya nguvu bila kupiga kura.

#### Vipengele Muhimu:

- **Mazungumzo ya Toleo la Itifaki**: Hutumia toleo la msingi wa tarehe (YYYY-MM-DD) kuhakikisha utangamano.
- **Ugunduzi wa Uwezo**: Wateja na seva hubadilishana taarifa za vipengele vinavyoungwa mkono wakati wa uanzishaji.
- **Vikao vya Hali**: Hudumisha hali ya muunganisho katika mwingiliano mwingi kwa mwendelezo wa muktadha.

### Safu ya Usafirishaji

**Safu ya Usafirishaji** inasimamia njia za mawasiliano, muundo wa ujumbe, na uthibitishaji kati ya washiriki wa MCP:

#### Mbinu za Usafirishaji Zinazoungwa Mkono:

1. **Usafirishaji wa STDIO**:
   - Hutumia mito ya pembejeo/pato la kawaida kwa mawasiliano ya moja kwa moja ya mchakato.
   - Inafaa kwa michakato ya ndani kwenye mashine moja bila mzigo wa mtandao.
   - Inatumika sana kwa utekelezaji wa seva za MCP za ndani.

2. **Usafirishaji wa HTTP Unaoweza Kutiririka**:
   - Hutumia HTTP POST kwa ujumbe wa mteja-kwa-seva.
   - Tukio la Matukio Yanayotumwa na Seva (SSE) la hiari kwa utiririshaji wa seva-kwa-mteja.
   - Huwezesha mawasiliano ya seva ya mbali katika mitandao.
   - Inasaidia uthibitishaji wa kawaida wa HTTP (tokeni za kubeba, funguo za API, vichwa maalum).
   - MCP inapendekeza OAuth kwa uthibitishaji salama wa msingi wa tokeni.

#### Utoaji wa Usafirishaji:

Safu ya usafirishaji inatoa maelezo ya mawasiliano kutoka kwa safu ya data, ikiruhusu muundo wa ujumbe wa JSON-RPC 2.0 sawa katika mbinu zote za usafirishaji. Utoaji huu unaruhusu programu kubadilisha kati ya seva za ndani na za mbali bila shida.

### Masuala ya Usalama

Utekelezaji wa MCP lazima uzingatie kanuni kadhaa muhimu za usalama ili kuhakikisha mwingiliano salama, wa kuaminika, na salama katika operesheni zote za itifaki:

- **Idhini na Udhibiti wa Mtumiaji**: Watumiaji lazima watoe idhini ya wazi kabla ya data yoyote kufikiwa au operesheni kufanywa. Wanapaswa kuwa na udhibiti wazi juu ya data gani inashirikiwa na hatua zipi zimeidhinishwa, zikisaidiwa na miingiliano ya mtumiaji ya angavu kwa ukaguzi na idhini ya shughuli.

- **Faragha ya Data**: Data ya mtumiaji inapaswa kufichuliwa tu kwa idhini ya wazi na lazima ilindwe na udhibiti wa ufikiaji unaofaa. Utekelezaji wa MCP lazima ulinde dhidi ya usambazaji wa data usioidhinishwa na kuhakikisha faragha inahifadhiwa katika mwingiliano wote.

- **Usalama wa Zana**: Kabla ya kutumia zana yoyote, idhini ya wazi ya mtumiaji inahitajika. Watumiaji wanapaswa kuwa na uelewa wazi wa utendaji wa kila zana, na mipaka thabiti ya usalama lazima itekelezwe ili kuzuia utekelezaji wa zana usio wa kawaida au usio salama.

Kwa kufuata kanuni hizi za usalama, MCP inahakikisha uaminifu wa mtumiaji, faragha, na usalama vinahifadhiwa katika mwingiliano wote wa itifaki huku ikiruhusu ujumuishaji wa AI wenye nguvu.

## Mifano ya Nambari: Vipengele Muhimu

Hapa chini kuna mifano ya nambari katika lugha kadhaa maarufu za programu inayoonyesha jinsi ya kutekeleza vipengele muhimu vya seva ya MCP na zana.

### Mfano wa .NET: Kuunda Seva Rahisi ya MCP na Zana

Huu ni mfano wa vitendo wa nambari ya .NET unaoonyesha jinsi ya kutekeleza seva rahisi ya MCP na zana maalum. Mfano huu unaonyesha jinsi ya kufafanua na kusajili zana, kushughulikia maombi, na kuunganisha seva kwa kutumia Itifaki ya Muktadha wa Mfano.

```csharp
using System;
using System.Threading.Tasks;
using ModelContextProtocol.Server;
using ModelContextProtocol.Server.Transport;
using ModelContextProtocol.Server.Tools;

public class WeatherServer
{
    public static async Task Main(string[] args)
    {
        // Create an MCP server
        var server = new McpServer(
            name: "Weather MCP Server",
            version: "1.0.0"
        );
        
        // Register our custom weather tool
        server.AddTool<string, WeatherData>("weatherTool", 
            description: "Gets current weather for a location",
            execute: async (location) => {
                // Call weather API (simplified)
                var weatherData = await GetWeatherDataAsync(location);
                return weatherData;
            });
        
        // Connect the server using stdio transport
        var transport = new StdioServerTransport();
        await server.ConnectAsync(transport);
        
        Console.WriteLine("Weather MCP Server started");
        
        // Keep the server running until process is terminated
        await Task.Delay(-1);
    }
    
    private static async Task<WeatherData> GetWeatherDataAsync(string location)
    {
        // This would normally call a weather API
        // Simplified for demonstration
        await Task.Delay(100); // Simulate API call
        return new WeatherData { 
            Temperature = 72.5,
            Conditions = "Sunny",
            Location = location
        };
    }
}

public class WeatherData
{
    public double Temperature { get; set; }
    public string Conditions { get; set; }
    public string Location { get; set; }
}
```

### Mfano wa Java: Vipengele vya Seva ya MCP

Mfano huu unaonyesha seva ya MCP na usajili wa zana sawa na mfano wa .NET hapo juu, lakini umetekelezwa kwa Java.

```java
import io.modelcontextprotocol.server.McpServer;
import io.modelcontextprotocol.server.McpToolDefinition;
import io.modelcontextprotocol.server.transport.StdioServerTransport;
import io.modelcontextprotocol.server.tool.ToolExecutionContext;
import io.modelcontextprotocol.server.tool.ToolResponse;

public class WeatherMcpServer {
    public static void main(String[] args) throws Exception {
        // Create an MCP server
        McpServer server = McpServer.builder()
            .name("Weather MCP Server")
            .version("1.0.0")
            .build();
            
        // Register a weather tool
        server.registerTool(McpToolDefinition.builder("weatherTool")
            .description("Gets current weather for a location")
            .parameter("location", String.class)
            .execute((ToolExecutionContext ctx) -> {
                String location = ctx.getParameter("location", String.class);
                
                // Get weather data (simplified)
                WeatherData data = getWeatherData(location);
                
                // Return formatted response
                return ToolResponse.content(
                    String.format("Temperature: %.1f°F, Conditions: %s, Location: %s", 
                    data.getTemperature(), 
                    data.getConditions(), 
                    data.getLocation())
                );
            })
            .build());
        
        // Connect the server using stdio transport
        try (StdioServerTransport transport = new StdioServerTransport()) {
            server.connect(transport);
            System.out.println("Weather MCP Server started");
            // Keep server running until process is terminated
            Thread.currentThread().join();
        }
    }
    
    private static WeatherData getWeatherData(String location) {
        // Implementation would call a weather API
        // Simplified for example purposes
        return new WeatherData(72.5, "Sunny", location);
    }
}

class WeatherData {
    private double temperature;
    private String conditions;
    private String location;
    
    public WeatherData(double temperature, String conditions, String location) {
        this.temperature = temperature;
        this.conditions = conditions;
        this.location = location;
    }
    
    public double getTemperature() {
        return temperature;
    }
    
    public String getConditions() {
        return conditions;
    }
    
    public String getLocation() {
        return location;
    }
}
```

### Mfano wa Python: Kujenga Seva ya MCP

Mfano huu unatumia fastmcp, kwa hivyo tafadhali hakikisha umeisakinisha kwanza:

```python
pip install fastmcp
```  
Mfano wa Nambari:

```python
#!/usr/bin/env python3
import asyncio
from fastmcp import FastMCP
from fastmcp.transports.stdio import serve_stdio

# Create a FastMCP server
mcp = FastMCP(
    name="Weather MCP Server",
    version="1.0.0"
)

@mcp.tool()
def get_weather(location: str) -> dict:
    """Gets current weather for a location."""
    return {
        "temperature": 72.5,
        "conditions": "Sunny",
        "location": location
    }

# Alternative approach using a class
class WeatherTools:
    @mcp.tool()
    def forecast(self, location: str, days: int = 1) -> dict:
        """Gets weather forecast for a location for the specified number of days."""
        return {
            "location": location,
            "forecast": [
                {"day": i+1, "temperature": 70 + i, "conditions": "Partly Cloudy"}
                for i in range(days)
            ]
        }

# Register class tools
weather_tools = WeatherTools()

# Start the server
if __name__ == "__main__":
    asyncio.run(serve_stdio(mcp))
```

### Mfano wa JavaScript: Kuunda Seva ya MCP

Mfano huu unaonyesha uundaji wa seva ya MCP kwa JavaScript na jinsi ya kusajili zana mbili zinazohusiana na hali ya hewa.

```javascript
// Using the official Model Context Protocol SDK
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod"; // For parameter validation

// Create an MCP server
const server = new McpServer({
  name: "Weather MCP Server",
  version: "1.0.0"
});

// Define a weather tool
server.tool(
  "weatherTool",
  {
    location: z.string().describe("The location to get weather for")
  },
  async ({ location }) => {
    // This would normally call a weather API
    // Simplified for demonstration
    const weatherData = await getWeatherData(location);
    
    return {
      content: [
        { 
          type: "text", 
          text: `Temperature: ${weatherData.temperature}°F, Conditions: ${weatherData.conditions}, Location: ${weatherData.location}` 
        }
      ]
    };
  }
);

// Define a forecast tool
server.tool(
  "forecastTool",
  {
    location: z.string(),
    days: z.number().default(3).describe("Number of days for forecast")
  },
  async ({ location, days }) => {
    // This would normally call a weather API
    // Simplified for demonstration
    const forecast = await getForecastData(location, days);
    
    return {
      content: [
        { 
          type: "text", 
          text: `${days}-day forecast for ${location}: ${JSON.stringify(forecast)}` 
        }
      ]
    };
  }
);

// Helper functions
async function getWeatherData(location) {
  // Simulate API call
  return {
    temperature: 72.5,
    conditions: "Sunny",
    location: location
  };
}

async function getForecastData(location, days) {
  // Simulate API call
  return Array.from({ length: days }, (_, i) => ({
    day: i + 1,
    temperature: 70 + Math.floor(Math.random() * 10),
    conditions: i % 2 === 0 ? "Sunny" : "Partly Cloudy"
  }));
}

// Connect the server using stdio transport
const transport = new StdioServerTransport();
server.connect(transport).catch(console.error);

console.log("Weather MCP Server started");
```

Mfano huu wa JavaScript unaonyesha jinsi ya kuunda mteja wa MCP anayejumuika na seva, kutuma maelekezo, na kushughulikia majibu ikiwa ni pamoja na miito yoyote ya zana iliyofanywa.

## Usalama na Uidhinishaji

MCP inajumuisha dhana kadhaa zilizojengwa ndani na mifumo ya kusimamia usalama na uidhinishaji katika itifaki:

1. **Udhibiti wa Ruhusa za Zana**:  
   Wateja wanaweza kubainisha zana ambazo modeli inaruhusiwa kutumia wakati wa kikao. Hii inahakikisha kwamba zana zilizoidhinishwa tu zinapatikana, kupunguza hatari ya operesheni zisizotarajiwa au zisizo salama. Ruhusa zinaweza kusanidiwa kwa nguvu kulingana na mapendeleo ya mtumiaji, sera za shirika, au muktadha wa mwingiliano.

2. **Uthibitishaji**:  
   Seva zinaweza kuhitaji uthibitishaji kabla ya kutoa ufikiaji wa zana, rasilimali, au operesheni nyeti. Hii inaweza kuhusisha funguo za API, tokeni za OAuth, au mifumo mingine ya uthibitishaji. Uthibitishaji sahihi unahakikisha kwamba wateja na watumiaji wanaoaminika pekee wanaweza kutumia uwezo wa seva.

3. **Uthibitishaji**:  
   Uthibitishaji wa vigezo unatekelezwa kwa miito yote ya zana. Kila zana hufafanua aina zinazotarajiwa, miundo, na vikwazo vya vigezo vyake, na seva inathibitisha maombi yanayoingia ipasavyo. Hii huzuia pembejeo mbovu au yenye nia mbaya kufikia utekelezaji wa zana na husaidia kudumisha uadilifu wa operesheni.

4. **Upunguzaji wa Kiwango**:  
   Ili kuzuia matumizi mabaya na kuhakikisha matumizi ya haki ya rasilimali za seva, seva za MCP zinaweza kutekeleza upunguzaji wa kiwango kwa miito ya zana na ufikiaji wa rasilimali. Viwango vya upunguzaji vinaweza kutumika kwa kila mtumiaji, kwa kila kikao, au kwa ujumla, na husaidia kulinda dhidi ya mashambulizi ya kukataa huduma au matumizi ya rasilimali kupita kiasi.

Kwa kuunganisha mifumo hii, MCP hutoa msingi salama wa kuunganisha mifano ya lugha na zana za nje na vyanzo vya data, huku ikiwapa watumiaji na watengenezaji udhibiti wa kina juu ya ufikiaji na matumizi.

## Ujumbe wa Itifaki na Mtiririko wa Mawasiliano

Mawasiliano ya MCP hutumia ujumbe uliopangwa wa **JSON-RPC 2.0** kuwezesha mwingiliano wazi na wa kuaminika kati ya majeshi, wateja, na seva. Itifaki hufafanua mifumo maalum ya ujumbe kwa aina tofauti za operesheni:

### Aina za Ujumbe Muhimu:

#### **Ujumbe wa Uanzishaji**
- **Ombi la `initialize`**: Huanzisha muunganisho na kujadili toleo la itifaki na uwezo.
- **Jibu la `initialize`**: Linathibitisha vipengele vinavyoungwa mkono na taarifa za seva.
- **`notifications/initialized`**: Inaashiria kwamba uanzishaji umekamilika na kikao kiko tayari.

#### **Ujumbe wa Ugunduzi**
- **Ombi la `tools/list`**: Hugundua zana zinazopatikana kutoka kwa seva.
- **Ombi la `resources/list`**: Orodhesha rasilimali zinazopatikana (vyanzo vya data).
- **Ombi la `prompts/list`**: Hurejesha templeti za maelekezo zinazopatikana.

#### **Ujumbe wa Utekelezaji**  
- **Ombi la `tools/call`**: Hutekeleza zana maalum na vigezo vilivyotolewa.
- **Ombi la `resources/read`**: Hurejesha maudhui kutoka kwa rasilimali maalum.
- **Ombi la `prompts/get`**: Huchukua templeti ya maelekezo na vigezo vya hiari.

#### **Ujumbe wa Upande wa Mteja**
- **Ombi la `sampling/complete`**: Seva inaomba kukamilisha LLM kutoka kwa mteja.
- **`elicitation/request`**: Seva inaomba maoni ya mtumiaji kupitia kiolesura cha mteja.
- **Ujumbe wa Kumbukumbu**: Seva inatuma ujumbe wa kumbukumbu uliopangwa kwa mteja.

#### **Ujumbe wa Arifa**
- **`notifications/tools/list_changed`**: Seva inamjulisha mteja kuhusu mabadiliko ya zana.
- **`notifications/resources/list_changed`**: Seva inamjulisha mteja kuhusu mabadiliko ya rasilimali.
- **`notifications/prompts/list_changed`**: Seva inamjulisha mteja kuhusu mabadiliko ya maelekezo.

### Muundo wa Ujumbe:

Ujumbe wote wa MCP hufuata muundo wa JSON-RPC 2.0 na:
- **Ujumbe wa Ombi**: Unajumuisha `id`, `method`, na `params` ya hiari.
- **Ujumbe wa Jibu**: Unajumuisha `id` na aidha `result` au `error`.
- **Ujumbe wa Arifa**: Unajumuisha `method` na `params` ya hiari (hakuna `id` au jibu linalotarajiwa).

Mawasiliano haya yaliyopangwa yanahakikisha mwingiliano wa kuaminika, unaoweza kufuatiliwa, na unaoweza kupanuliwa unaounga mkono hali za juu kama masasisho ya wakati halisi, mnyororo wa zana, na utunzaji thabiti wa makosa.

## Mambo Muhimu ya Kuzingatia

- **Usanifu**: MCP hutumia usanifu wa mteja-seva ambapo majeshi husimamia miunganisho mingi ya mteja kwa seva.
- **Washiriki**: Mfumo unajumuisha majeshi (programu za AI), wateja (viunganishi vya itifaki), na seva (watoa uwezo).
- **Mbinu za Usafirishaji**: Mawasiliano yanaunga mkono STDIO (ya ndani) na HTTP inayoweza kutiririka na SSE ya hiari (ya mbali).
- **Vipengele Muhimu**: Seva zinaonyesha zana (kazi zinazoweza kutekelezwa), rasilimali (vyanzo vya data), na maelekezo (templeti).
- **Vipengele vya Mteja**: Seva zinaweza kuomba sampuli (ukamilishaji wa LLM), uchochezi (maoni ya mtumiaji), na kumbukumbu kutoka kwa wateja.
- **Msingi wa Itifaki**: Imejengwa juu ya JSON-RPC 2.0 na toleo la msingi wa tarehe (sasa: 2025-06-18).
- **Uwezo wa Wakati Halisi**: Inasaidia arifa kwa masasisho ya nguvu na usawazishaji wa wakati halisi.
- **Usalama Kwanza**: Idhini ya wazi ya mtumiaji, ulinzi wa faragha ya data, na usafirishaji salama ni mahitaji ya msingi.

## Zoezi

Buni zana rahisi ya MCP ambayo itakuwa muhimu katika uwanja wako. Fafanua:
1. Jina la zana hiyo.
2. Vigezo ambavyo itakubali.
3. Matokeo ambayo itarudisha.
4. Jinsi modeli inaweza kutumia zana hii kutatua matatizo ya mtumiaji.

---

## Kinachofuata

Kinachofuata: [Sura ya 2: Usalama](../02-Security/README.md)

---

**Kanusho**:  
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kwa usahihi, tafadhali fahamu kuwa tafsiri za kiotomatiki zinaweza kuwa na makosa au kutokuwa sahihi. Hati ya asili katika lugha yake ya awali inapaswa kuzingatiwa kama chanzo cha mamlaka. Kwa taarifa muhimu, inashauriwa kutumia huduma ya tafsiri ya kitaalamu ya binadamu. Hatutawajibika kwa maelewano mabaya au tafsiri zisizo sahihi zinazotokana na matumizi ya tafsiri hii.