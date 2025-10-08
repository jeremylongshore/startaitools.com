<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "904b59de1de9264801242d90a42cdd9d",
  "translation_date": "2025-09-05T11:09:58+00:00",
  "source_file": "01-CoreConcepts/README.md",
  "language_code": "no"
}
-->
# MCP Kjernekonsepter: Mestre Model Context Protocol for AI-integrasjon

[![MCP Kjernekonsepter](../../../translated_images/02.8203e26c6fb5a797f38a10012061013ec66c95bb3260f6c9cfd2bf74b00860e1.no.png)](https://youtu.be/earDzWGtE84)

_(Klikk på bildet over for å se videoen til denne leksjonen)_

[Model Context Protocol (MCP)](https://github.com/modelcontextprotocol) er et kraftig, standardisert rammeverk som optimaliserer kommunikasjonen mellom store språkmodeller (LLMs) og eksterne verktøy, applikasjoner og datakilder. 
Denne guiden vil lede deg gjennom MCPs kjernekonsepter. Du vil lære om dens klient-server-arkitektur, essensielle komponenter, kommunikasjonsmekanismer og beste praksis for implementering.

- **Eksplisitt brukerens samtykke**: All tilgang til data og operasjoner krever eksplisitt godkjenning fra brukeren før utførelse. Brukeren må ha en klar forståelse av hvilke data som vil bli brukt og hvilke handlinger som vil bli utført, med detaljert kontroll over tillatelser og autorisasjoner.

- **Beskyttelse av personvern**: Brukerdata skal kun eksponeres med eksplisitt samtykke og må beskyttes av robuste tilgangskontroller gjennom hele interaksjonslivssyklusen. Implementeringer må forhindre uautorisert dataoverføring og opprettholde strenge personverngrenser.

- **Sikkerhet ved verktøyutførelse**: Hver verktøyaktivering krever eksplisitt brukerens samtykke med en klar forståelse av verktøyets funksjonalitet, parametere og potensielle konsekvenser. Robuste sikkerhetsgrenser må forhindre utilsiktet, usikker eller ondsinnet verktøyutførelse.

- **Transportlagssikkerhet**: Alle kommunikasjonskanaler bør bruke passende kryptering og autentiseringsmekanismer. Fjernforbindelser bør implementere sikre transportprotokoller og korrekt håndtering av legitimasjon.

#### Retningslinjer for implementering:

- **Tillatelseshåndtering**: Implementer detaljerte tillatelsessystemer som lar brukere kontrollere hvilke servere, verktøy og ressurser som er tilgjengelige
- **Autentisering og autorisasjon**: Bruk sikre autentiseringsmetoder (OAuth, API-nøkler) med korrekt tokenhåndtering og utløp  
- **Validering av input**: Valider alle parametere og data-input i henhold til definerte skjemaer for å forhindre injeksjonsangrep
- **Revisjonslogging**: Oppretthold omfattende logger over alle operasjoner for sikkerhetsovervåking og samsvar

## Oversikt

Denne leksjonen utforsker den grunnleggende arkitekturen og komponentene som utgjør Model Context Protocol (MCP)-økosystemet. Du vil lære om klient-server-arkitekturen, nøkkelkomponentene og kommunikasjonsmekanismene som driver MCP-interaksjoner.

## Viktige læringsmål

Ved slutten av denne leksjonen vil du:

- Forstå MCPs klient-server-arkitektur.
- Identifisere roller og ansvar for verter, klienter og servere.
- Analysere kjernefunksjonene som gjør MCP til et fleksibelt integrasjonslag.
- Lære hvordan informasjon flyter innen MCP-økosystemet.
- Få praktisk innsikt gjennom kodeeksempler i .NET, Java, Python og JavaScript.

## MCP Arkitektur: En dypere titt

MCP-økosystemet er bygget på en klient-server-modell. Denne modulære strukturen lar AI-applikasjoner samhandle med verktøy, databaser, API-er og kontekstuelle ressurser effektivt. La oss bryte ned denne arkitekturen i dens kjernekomponenter.

I sin kjerne følger MCP en klient-server-arkitektur der en vertsapplikasjon kan koble til flere servere:

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

- **MCP Verter**: Programmer som VSCode, Claude Desktop, IDE-er eller AI-verktøy som ønsker å få tilgang til data via MCP
- **MCP Klienter**: Protokollklienter som opprettholder 1:1-forbindelser med servere
- **MCP Servere**: Lettvektsprogrammer som hver eksponerer spesifikke funksjoner gjennom den standardiserte Model Context Protocol
- **Lokale datakilder**: Filene, databasene og tjenestene på datamaskinen din som MCP-servere kan få sikker tilgang til
- **Eksterne tjenester**: Systemer tilgjengelige over internett som MCP-servere kan koble til via API-er.

MCP-protokollen er en utviklende standard som bruker datobasert versjonering (YYYY-MM-DD-format). Den nåværende protokollversjonen er **2025-06-18**. Du kan se de siste oppdateringene til [protokollspesifikasjonen](https://modelcontextprotocol.io/specification/2025-06-18/)

### 1. Verter

I Model Context Protocol (MCP) er **Verter** AI-applikasjoner som fungerer som det primære grensesnittet der brukere interagerer med protokollen. Verter koordinerer og administrerer forbindelser til flere MCP-servere ved å opprette dedikerte MCP-klienter for hver serverforbindelse. Eksempler på verter inkluderer:

- **AI-applikasjoner**: Claude Desktop, Visual Studio Code, Claude Code
- **Utviklingsmiljøer**: IDE-er og kodeeditorer med MCP-integrasjon  
- **Egendefinerte applikasjoner**: Spesialbygde AI-agenter og verktøy

**Verter** er applikasjoner som koordinerer AI-modellinteraksjoner. De:

- **Orkestrerer AI-modeller**: Utfører eller interagerer med LLMs for å generere svar og koordinere AI-arbeidsflyter
- **Administrerer klientforbindelser**: Oppretter og opprettholder én MCP-klient per MCP-serverforbindelse
- **Kontrollerer brukergrensesnitt**: Håndterer samtaleflyt, brukerinteraksjoner og presentasjon av svar  
- **Håndhever sikkerhet**: Kontrollerer tillatelser, sikkerhetsbegrensninger og autentisering
- **Håndterer brukerens samtykke**: Administrerer brukerens godkjenning for datadeling og verktøyutførelse

### 2. Klienter

**Klienter** er essensielle komponenter som opprettholder dedikerte én-til-én-forbindelser mellom verter og MCP-servere. Hver MCP-klient opprettes av verten for å koble til en spesifikk MCP-server, og sikrer organiserte og sikre kommunikasjonskanaler. Flere klienter gjør det mulig for verter å koble til flere servere samtidig.

**Klienter** er koblingskomponenter innen vertsapplikasjonen. De:

- **Protokollkommunikasjon**: Sender JSON-RPC 2.0-forespørsler til servere med instruksjoner og oppgaver
- **Funksjonsforhandling**: Forhandler støttede funksjoner og protokollversjoner med servere under initialisering
- **Verktøyutførelse**: Administrerer forespørsler om verktøyutførelse fra modeller og behandler svar
- **Sanntidsoppdateringer**: Håndterer varsler og sanntidsoppdateringer fra servere
- **Svarbehandling**: Behandler og formaterer serverens svar for visning til brukere

### 3. Servere

**Servere** er programmer som gir kontekst, verktøy og funksjoner til MCP-klienter. De kan kjøre lokalt (på samme maskin som verten) eller eksternt (på eksterne plattformer), og er ansvarlige for å håndtere klientforespørsler og gi strukturerte svar. Servere eksponerer spesifikke funksjoner gjennom den standardiserte Model Context Protocol.

**Servere** er tjenester som gir kontekst og funksjonalitet. De:

- **Funksjonsregistrering**: Registrerer og eksponerer tilgjengelige primitivene (ressurser, instruksjoner, verktøy) til klienter
- **Forespørselsbehandling**: Mottar og utfører verktøyanrop, ressursforespørsler og instruksjonsforespørsler fra klienter
- **Kontekstlevering**: Gir kontekstuell informasjon og data for å forbedre modellens svar
- **Tilstandshåndtering**: Opprettholder sesjonstilstand og håndterer tilstandsbaserte interaksjoner når det er nødvendig
- **Sanntidsvarsler**: Sender varsler om endringer i funksjonalitet og oppdateringer til tilkoblede klienter

Servere kan utvikles av hvem som helst for å utvide modellens funksjonalitet med spesialisert funksjonalitet, og de støtter både lokale og eksterne distribusjonsscenarier.

### 4. Serverprimitiver

Servere i Model Context Protocol (MCP) gir tre kjerne**primitiver** som definerer de grunnleggende byggesteinene for rike interaksjoner mellom klienter, verter og språkmodeller. Disse primitivene spesifiserer typene kontekstuell informasjon og handlinger som er tilgjengelige gjennom protokollen.

MCP-servere kan eksponere en hvilken som helst kombinasjon av følgende tre kjerneprimitiver:

#### Ressurser 

**Ressurser** er datakilder som gir kontekstuell informasjon til AI-applikasjoner. De representerer statisk eller dynamisk innhold som kan forbedre modellens forståelse og beslutningstaking:

- **Kontekstuelle data**: Strukturert informasjon og kontekst for AI-modellens forbruk
- **Kunnskapsbaser**: Dokumentarkiver, artikler, manualer og forskningsartikler
- **Lokale datakilder**: Filer, databaser og lokal systeminformasjon  
- **Eksterne data**: API-svar, webtjenester og eksterne systemdata
- **Dynamisk innhold**: Sanntidsdata som oppdateres basert på eksterne forhold

Ressurser identifiseres av URI-er og støtter oppdagelse gjennom `resources/list` og henting gjennom `resources/read`-metoder:

```text
file://documents/project-spec.md
database://production/users/schema
api://weather/current
```

#### Instruksjoner

**Instruksjoner** er gjenbrukbare maler som hjelper med å strukturere interaksjoner med språkmodeller. De gir standardiserte interaksjonsmønstre og malbaserte arbeidsflyter:

- **Malbaserte interaksjoner**: Forhåndsstrukturerte meldinger og samtalestartere
- **Arbeidsflytmaler**: Standardiserte sekvenser for vanlige oppgaver og interaksjoner
- **Few-shot eksempler**: Eksempelbaserte maler for modellinstruksjon
- **Systeminstruksjoner**: Grunnleggende instruksjoner som definerer modellens oppførsel og kontekst
- **Dynamiske maler**: Parameteriserte instruksjoner som tilpasser seg spesifikke kontekster

Instruksjoner støtter variabel substitusjon og kan oppdages via `prompts/list` og hentes med `prompts/get`:

```markdown
Generate a {{task_type}} for {{product}} targeting {{audience}} with the following requirements: {{requirements}}
```

#### Verktøy

**Verktøy** er utførbare funksjoner som AI-modeller kan påkalle for å utføre spesifikke handlinger. De representerer "verbene" i MCP-økosystemet, og gjør det mulig for modeller å samhandle med eksterne systemer:

- **Utførbare funksjoner**: Diskrete operasjoner som modeller kan påkalle med spesifikke parametere
- **Integrasjon med eksterne systemer**: API-anrop, databaseforespørsler, filoperasjoner, beregninger
- **Unik identitet**: Hvert verktøy har et distinkt navn, beskrivelse og parameter-skjema
- **Strukturert I/O**: Verktøy aksepterer validerte parametere og returnerer strukturerte, typede svar
- **Handlingskapabiliteter**: Gjør det mulig for modeller å utføre virkelige handlinger og hente live data

Verktøy defineres med JSON Schema for parametervalidering og oppdages gjennom `tools/list` og utføres via `tools/call`:

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

## Klientprimitiver

I Model Context Protocol (MCP) kan **klienter** eksponere primitivene som gjør det mulig for servere å be om ytterligere funksjoner fra vertsapplikasjonen. Disse klientbaserte primitivene tillater rikere, mer interaktive serverimplementeringer som kan få tilgang til AI-modellens kapabiliteter og brukerinteraksjoner.

### Sampling

**Sampling** gjør det mulig for servere å be om språkmodellens fullføringer fra klientens AI-applikasjon. Denne primitivene gjør det mulig for servere å få tilgang til LLM-funksjoner uten å inkludere egne modellavhengigheter:

- **Modelluavhengig tilgang**: Servere kan be om fullføringer uten å inkludere LLM SDK-er eller administrere modelltilgang
- **Server-initiert AI**: Gjør det mulig for servere å autonomt generere innhold ved hjelp av klientens AI-modell
- **Rekursiv LLM-interaksjon**: Støtter komplekse scenarier der servere trenger AI-assistanse for behandling
- **Dynamisk innholdsgenerering**: Gjør det mulig for servere å lage kontekstuelle svar ved hjelp av vertens modell

Sampling initieres gjennom `sampling/complete`-metoden, der servere sender fullføringsforespørsler til klienter.

### Elicitation  

**Elicitation** gjør det mulig for servere å be om ytterligere informasjon eller bekreftelse fra brukere gjennom klientgrensesnittet:

- **Brukerinputforespørsler**: Servere kan be om ytterligere informasjon når det er nødvendig for verktøyutførelse
- **Bekreftelsesdialoger**: Be om brukerens godkjenning for sensitive eller betydningsfulle operasjoner
- **Interaktive arbeidsflyter**: Gjør det mulig for servere å lage steg-for-steg brukerinteraksjoner
- **Dynamisk parameterinnsamling**: Samle manglende eller valgfrie parametere under verktøyutførelse

Elicitation-forespørsler gjøres ved hjelp av `elicitation/request`-metoden for å samle brukerinput gjennom klientens grensesnitt.

### Logging

**Logging** gjør det mulig for servere å sende strukturerte loggmeldinger til klienter for feilsøking, overvåking og operasjonell synlighet:

- **Feilsøkingsstøtte**: Gjør det mulig for servere å gi detaljerte utførelseslogger for feilsøking
- **Operasjonell overvåking**: Send statusoppdateringer og ytelsesmetrikker til klienter
- **Feilrapportering**: Gi detaljert feilkontekst og diagnostisk informasjon
- **Revisjonsspor**: Opprett omfattende logger over serveroperasjoner og beslutninger

Loggmeldinger sendes til klienter for å gi innsyn i serveroperasjoner og lette feilsøking.

## Informasjonsflyt i MCP

Model Context Protocol (MCP) definerer en strukturert flyt av informasjon mellom verter, klienter, servere og modeller. Å forstå denne flyten hjelper med å klargjøre hvordan brukerforespørsler behandles og hvordan eksterne verktøy og data integreres i modellens svar.

- **Vert initierer tilkobling**  
  Vertsapplikasjonen (som en IDE eller chatgrensesnitt) etablerer en tilkobling til en MCP-server, vanligvis via STDIO, WebSocket eller en annen støttet transport.

- **Funksjonsforhandling**  
  Klienten (innebygd i verten) og serveren utveksler informasjon om deres støttede funksjoner, verktøy, ressurser og protokollversjoner. Dette sikrer at begge sider forstår hvilke kapabiliteter som er tilgjengelige for økten.

- **Brukerforespørsel**  
  Brukeren interagerer med verten (f.eks. skriver inn en prompt eller kommando). Verten samler denne inputen og sender den til klienten for behandling.

- **Bruk av ressurser eller verktøy**  
  - Klienten kan be om ytterligere kontekst eller ressurser fra serveren (som filer, databaseoppføringer eller kunnskapsbaseartikler) for å berike modellens forståelse.
  - Hvis modellen bestemmer at et verktøy er nødvendig (f.eks. for å hente data, utføre en beregning eller ringe en API), sender klienten en verktøyaktiveringsforespørsel til serveren, med spesifikasjon av verktøyets navn og parametere.

- **Serverutførelse**  
  Serveren mottar ressurs- eller verktøyforespørselen, utfører de nødvendige operasjonene (som å kjøre en funksjon, spørre en database eller hente en fil), og returnerer resultatene til klienten i et strukturert format.

- **Svargenerering**  
  Klienten integrerer serverens svar (ressursdata, verktøyutganger, etc.) i den pågående modellinteraksjonen. Modellen bruker denne informasjonen til å generere et omfattende og kontekstuelt relevant svar.

- **Resultatpresentasjon**  
  Verten mottar det endelige outputet fra klienten og presenterer det for brukeren, ofte inkludert både modellens genererte tekst og eventuelle resultater fra verktøyutførelser eller ressursoppslag.

Denne flyten gjør det mulig for MCP å støtte avanserte, interaktive og kontekstbevisste AI-applikasjoner ved sømløst å koble modeller med eksterne verktøy og datakilder.

## Protokollarkitektur og lag

MCP består av to
- **JSON-RPC 2.0-protokoll**: All kommunikasjon bruker standardisert JSON-RPC 2.0-meldingsformat for metodekall, svar og varsler  
- **Livssyklusadministrasjon**: Håndterer tilkoblingsinitialisering, kapabilitetsforhandling og sesjonsavslutning mellom klienter og servere  
- **Serverprimitiver**: Gjør det mulig for servere å tilby kjernefunksjonalitet gjennom verktøy, ressurser og maler  
- **Klientprimitiver**: Gjør det mulig for servere å be om prøvetaking fra LLM-er, hente brukerinput og sende loggmeldinger  
- **Varsler i sanntid**: Støtter asynkrone varsler for dynamiske oppdateringer uten polling  

#### Nøkkelfunksjoner:

- **Protokollversjonsforhandling**: Bruker dato-basert versjonering (ÅÅÅÅ-MM-DD) for å sikre kompatibilitet  
- **Kapabilitetsoppdagelse**: Klienter og servere utveksler informasjon om støttede funksjoner under initialisering  
- **Tilstandfulle sesjoner**: Opprettholder tilkoblingstilstand på tvers av flere interaksjoner for kontekstkonsistens  

### Transportlag

**Transportlaget** administrerer kommunikasjonskanaler, meldingsrammer og autentisering mellom MCP-deltakere:

#### Støttede transportmekanismer:

1. **STDIO-transport**:
   - Bruker standard inn-/utstrømmer for direkte prosesskommunikasjon  
   - Optimalt for lokale prosesser på samme maskin uten nettverksbelastning  
   - Vanlig brukt for lokale MCP-serverimplementasjoner  

2. **Streamable HTTP-transport**:
   - Bruker HTTP POST for meldinger fra klient til server  
   - Valgfri Server-Sent Events (SSE) for strømming fra server til klient  
   - Muliggjør fjernserverkommunikasjon over nettverk  
   - Støtter standard HTTP-autentisering (bearertokens, API-nøkler, egendefinerte overskrifter)  
   - MCP anbefaler OAuth for sikker token-basert autentisering  

#### Transportabstraksjon:

Transportlaget abstraherer kommunikasjonsdetaljer fra datalaget, slik at samme JSON-RPC 2.0-meldingsformat kan brukes på tvers av alle transportmekanismer. Denne abstraksjonen gjør det mulig for applikasjoner å bytte mellom lokale og eksterne servere sømløst.

### Sikkerhetsbetraktninger

MCP-implementasjoner må følge flere kritiske sikkerhetsprinsipper for å sikre trygge, pålitelige og sikre interaksjoner på tvers av alle protokolloperasjoner:

- **Brukersamtykke og kontroll**: Brukere må gi eksplisitt samtykke før data blir aksessert eller operasjoner utført. De bør ha klar kontroll over hvilke data som deles og hvilke handlinger som er autorisert, støttet av intuitive brukergrensesnitt for å gjennomgå og godkjenne aktiviteter.

- **Datapersonvern**: Brukerdata skal kun eksponeres med eksplisitt samtykke og må beskyttes av passende tilgangskontroller. MCP-implementasjoner må forhindre uautorisert datatransmisjon og sikre at personvernet opprettholdes gjennom alle interaksjoner.

- **Verktøysikkerhet**: Før et verktøy brukes, kreves eksplisitt brukersamtykke. Brukere bør ha en klar forståelse av hvert verktøys funksjonalitet, og robuste sikkerhetsgrenser må håndheves for å forhindre utilsiktet eller usikker verktøyutførelse.

Ved å følge disse sikkerhetsprinsippene sikrer MCP at brukertillit, personvern og sikkerhet opprettholdes på tvers av alle protokollinteraksjoner, samtidig som kraftige AI-integrasjoner muliggjøres.

## Kodeeksempler: Nøkkelkomponenter

Nedenfor er kodeeksempler i flere populære programmeringsspråk som illustrerer hvordan man implementerer nøkkelkomponenter og verktøy for MCP-servere.

### .NET-eksempel: Opprette en enkel MCP-server med verktøy

Her er et praktisk .NET-kodeeksempel som demonstrerer hvordan man implementerer en enkel MCP-server med egendefinerte verktøy. Eksemplet viser hvordan man definerer og registrerer verktøy, håndterer forespørsler og kobler serveren ved hjelp av Model Context Protocol.

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

### Java-eksempel: MCP-serverkomponenter

Dette eksemplet demonstrerer den samme MCP-serveren og verktøyregistreringen som .NET-eksemplet ovenfor, men implementert i Java.

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

### Python-eksempel: Bygge en MCP-server

Dette eksemplet bruker fastmcp, så sørg for å installere det først:

```python
pip install fastmcp
```  
Kodeeksempel:

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

### JavaScript-eksempel: Opprette en MCP-server

Dette eksemplet viser opprettelse av MCP-server i JavaScript og hvordan man registrerer to værrelaterte verktøy.

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

Dette JavaScript-eksemplet demonstrerer hvordan man oppretter en MCP-klient som kobler til en server, sender en prompt og behandler svaret, inkludert eventuelle verktøykall som ble utført.

## Sikkerhet og autorisasjon

MCP inkluderer flere innebygde konsepter og mekanismer for å administrere sikkerhet og autorisasjon gjennom hele protokollen:

1. **Verktøytillatelseskontroll**:  
   Klienter kan spesifisere hvilke verktøy en modell har lov til å bruke under en sesjon. Dette sikrer at kun eksplisitt autoriserte verktøy er tilgjengelige, og reduserer risikoen for utilsiktede eller usikre operasjoner. Tillatelser kan konfigureres dynamisk basert på brukerpreferanser, organisasjonspolicyer eller interaksjonskontekst.

2. **Autentisering**:  
   Servere kan kreve autentisering før tilgang til verktøy, ressurser eller sensitive operasjoner gis. Dette kan innebære API-nøkler, OAuth-tokens eller andre autentiseringsordninger. Riktig autentisering sikrer at kun betrodde klienter og brukere kan påkalle server-side kapabiliteter.

3. **Validering**:  
   Parametervalidering håndheves for alle verktøykall. Hvert verktøy definerer forventede typer, formater og begrensninger for sine parametere, og serveren validerer innkommende forespørsler deretter. Dette forhindrer feilformet eller ondsinnet input fra å nå verktøyimplementasjoner og bidrar til å opprettholde integriteten til operasjoner.

4. **Ratebegrensning**:  
   For å forhindre misbruk og sikre rettferdig bruk av serverressurser, kan MCP-servere implementere ratebegrensning for verktøykall og ressursaksess. Ratebegrensninger kan brukes per bruker, per sesjon eller globalt, og bidrar til å beskytte mot tjenestenektangrep eller overdreven ressursbruk.

Ved å kombinere disse mekanismene gir MCP et sikkert grunnlag for å integrere språkmodeller med eksterne verktøy og datakilder, samtidig som brukere og utviklere får finjustert kontroll over tilgang og bruk.

## Protokollmeldinger og kommunikasjonsflyt

MCP-kommunikasjon bruker strukturerte **JSON-RPC 2.0**-meldinger for å legge til rette for klare og pålitelige interaksjoner mellom verter, klienter og servere. Protokollen definerer spesifikke meldingsmønstre for ulike typer operasjoner:

### Kjerne-meldingstyper:

#### **Initialiseringsmeldinger**
- **`initialize` Forespørsel**: Etablerer tilkobling og forhandler protokollversjon og kapabiliteter  
- **`initialize` Svar**: Bekrefter støttede funksjoner og serverinformasjon  
- **`notifications/initialized`**: Signalerer at initialisering er fullført og sesjonen er klar  

#### **Oppdagelsesmeldinger**
- **`tools/list` Forespørsel**: Oppdager tilgjengelige verktøy fra serveren  
- **`resources/list` Forespørsel**: Lister tilgjengelige ressurser (datakilder)  
- **`prompts/list` Forespørsel**: Henter tilgjengelige maler  

#### **Utførelsesmeldinger**  
- **`tools/call` Forespørsel**: Utfører et spesifikt verktøy med angitte parametere  
- **`resources/read` Forespørsel**: Henter innhold fra en spesifikk ressurs  
- **`prompts/get` Forespørsel**: Henter en mal med valgfrie parametere  

#### **Klient-side meldinger**
- **`sampling/complete` Forespørsel**: Serveren ber om LLM-fullføring fra klienten  
- **`elicitation/request`**: Serveren ber om brukerinput via klientgrensesnittet  
- **Loggmeldinger**: Serveren sender strukturerte loggmeldinger til klienten  

#### **Varslingsmeldinger**
- **`notifications/tools/list_changed`**: Serveren varsler klienten om endringer i verktøy  
- **`notifications/resources/list_changed`**: Serveren varsler klienten om endringer i ressurser  
- **`notifications/prompts/list_changed`**: Serveren varsler klienten om endringer i maler  

### Meldingsstruktur:

Alle MCP-meldinger følger JSON-RPC 2.0-format med:  
- **Forespørselsmeldinger**: Inkluderer `id`, `method` og valgfrie `params`  
- **Svarmeldinger**: Inkluderer `id` og enten `result` eller `error`  
- **Varslingsmeldinger**: Inkluderer `method` og valgfrie `params` (ingen `id` eller svar forventet)  

Denne strukturerte kommunikasjonen sikrer pålitelige, sporbare og utvidbare interaksjoner som støtter avanserte scenarier som sanntidsoppdateringer, verktøykjeding og robust feilbehandling.

## Viktige punkter

- **Arkitektur**: MCP bruker en klient-server-arkitektur der verter administrerer flere klienttilkoblinger til servere  
- **Deltakere**: Økosystemet inkluderer verter (AI-applikasjoner), klienter (protokollkoblinger) og servere (kapabilitetsleverandører)  
- **Transportmekanismer**: Kommunikasjon støtter STDIO (lokal) og Streamable HTTP med valgfri SSE (fjern)  
- **Kjerneprimitiver**: Servere eksponerer verktøy (utførbare funksjoner), ressurser (datakilder) og maler (templates)  
- **Klientprimitiver**: Servere kan be om prøvetaking (LLM-fullføringer), innhenting (brukerinput) og logging fra klienter  
- **Protokollgrunnlag**: Bygget på JSON-RPC 2.0 med dato-basert versjonering (nåværende: 2025-06-18)  
- **Sanntidskapabiliteter**: Støtter varsler for dynamiske oppdateringer og sanntidssynkronisering  
- **Sikkerhet først**: Eksplisitt brukersamtykke, beskyttelse av personvern og sikker transport er kjernekrav  

## Øvelse

Design et enkelt MCP-verktøy som ville være nyttig i ditt domene. Definer:  
1. Hva verktøyet skal hete  
2. Hvilke parametere det skal akseptere  
3. Hvilken output det skal returnere  
4. Hvordan en modell kan bruke dette verktøyet for å løse brukerproblemer  

---

## Hva skjer videre

Neste: [Kapittel 2: Sikkerhet](../02-Security/README.md)  

---

**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi tilstreber nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på sitt opprinnelige språk bør anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.