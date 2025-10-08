<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "904b59de1de9264801242d90a42cdd9d",
  "translation_date": "2025-09-05T11:33:17+00:00",
  "source_file": "01-CoreConcepts/README.md",
  "language_code": "ro"
}
-->
# MCP Concepte de Bază: Stăpânirea Protocolului de Context al Modelului pentru Integrarea AI

[![MCP Concepte de Bază](../../../translated_images/02.8203e26c6fb5a797f38a10012061013ec66c95bb3260f6c9cfd2bf74b00860e1.ro.png)](https://youtu.be/earDzWGtE84)

_(Click pe imaginea de mai sus pentru a viziona videoclipul lecției)_

[Model Context Protocol (MCP)](https://github.com/modelcontextprotocol) este un cadru standardizat puternic care optimizează comunicarea între Modelele de Limbaj Extins (LLMs) și instrumentele, aplicațiile și sursele de date externe. 
Acest ghid te va conduce prin conceptele de bază ale MCP. Vei învăța despre arhitectura client-server, componentele esențiale, mecanismele de comunicare și cele mai bune practici de implementare.

- **Consimțământ Explicit al Utilizatorului**: Accesul la date și operațiunile necesită aprobarea explicită a utilizatorului înainte de execuție. Utilizatorii trebuie să înțeleagă clar ce date vor fi accesate și ce acțiuni vor fi efectuate, având control granular asupra permisiunilor și autorizărilor.

- **Protecția Confidențialității Datelor**: Datele utilizatorului sunt expuse doar cu consimțământ explicit și trebuie protejate prin controale de acces robuste pe tot parcursul ciclului de interacțiune. Implementările trebuie să prevină transmiterea neautorizată a datelor și să mențină limite stricte de confidențialitate.

- **Siguranța Execuției Instrumentelor**: Fiecare invocare a unui instrument necesită consimțământ explicit al utilizatorului, cu o înțelegere clară a funcționalității, parametrilor și impactului potențial al instrumentului. Limitele de securitate robuste trebuie să prevină execuțiile neintenționate, nesigure sau malițioase ale instrumentelor.

- **Securitatea Stratului de Transport**: Toate canalele de comunicare ar trebui să utilizeze mecanisme adecvate de criptare și autentificare. Conexiunile la distanță trebuie să implementeze protocoale de transport securizate și gestionarea corespunzătoare a acreditărilor.

#### Ghiduri de Implementare:

- **Gestionarea Permisiunilor**: Implementați sisteme de permisiuni detaliate care permit utilizatorilor să controleze ce servere, instrumente și resurse sunt accesibile.
- **Autentificare și Autorizare**: Utilizați metode de autentificare securizate (OAuth, chei API) cu gestionarea corespunzătoare a tokenurilor și expirarea acestora.  
- **Validarea Inputurilor**: Validați toți parametrii și datele de intrare conform schemelor definite pentru a preveni atacurile de tip injecție.
- **Jurnalizare Audit**: Mențineți jurnale cuprinzătoare ale tuturor operațiunilor pentru monitorizarea securității și conformitate.

## Prezentare Generală

Această lecție explorează arhitectura fundamentală și componentele care alcătuiesc ecosistemul Model Context Protocol (MCP). Vei învăța despre arhitectura client-server, componentele cheie și mecanismele de comunicare care susțin interacțiunile MCP.

## Obiective Cheie de Învățare

Până la sfârșitul acestei lecții, vei:

- Înțelege arhitectura client-server MCP.
- Identifica rolurile și responsabilitățile gazdelor, clienților și serverelor.
- Analiza caracteristicile de bază care fac din MCP un strat de integrare flexibil.
- Înțelege cum circulă informațiile în ecosistemul MCP.
- Obține perspective practice prin exemple de cod în .NET, Java, Python și JavaScript.

## Arhitectura MCP: O Privire Mai Aprofundată

Ecosistemul MCP este construit pe un model client-server. Această structură modulară permite aplicațiilor AI să interacționeze eficient cu instrumente, baze de date, API-uri și resurse contextuale. Să descompunem această arhitectură în componentele sale de bază.

La bază, MCP urmează o arhitectură client-server în care o aplicație gazdă poate conecta mai multe servere:

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

- **Gazde MCP**: Programe precum VSCode, Claude Desktop, IDE-uri sau instrumente AI care doresc să acceseze date prin MCP.
- **Clienți MCP**: Clienți de protocol care mențin conexiuni 1:1 cu serverele.
- **Servere MCP**: Programe ușoare care expun fiecare capabilități specifice prin Protocolul de Context al Modelului standardizat.
- **Surse de Date Locale**: Fișierele, bazele de date și serviciile computerului tău pe care serverele MCP le pot accesa în siguranță.
- **Servicii la Distanță**: Sisteme externe disponibile pe internet la care serverele MCP se pot conecta prin API-uri.

Protocolul MCP este un standard în evoluție care utilizează versiuni bazate pe date (format YYYY-MM-DD). Versiunea actuală a protocolului este **2025-06-18**. Poți vedea cele mai recente actualizări ale [specificației protocolului](https://modelcontextprotocol.io/specification/2025-06-18/).

### 1. Gazde

În Protocolul de Context al Modelului (MCP), **Gazdele** sunt aplicații AI care servesc drept interfața principală prin care utilizatorii interacționează cu protocolul. Gazdele coordonează și gestionează conexiunile la mai multe servere MCP prin crearea de clienți MCP dedicați pentru fiecare conexiune de server. Exemple de gazde includ:

- **Aplicații AI**: Claude Desktop, Visual Studio Code, Claude Code.
- **Mediile de Dezvoltare**: IDE-uri și editori de cod cu integrare MCP.  
- **Aplicații Personalizate**: Agenți AI și instrumente construite pentru scopuri specifice.

**Gazdele** sunt aplicații care coordonează interacțiunile modelelor AI. Ele:

- **Orchestrează Modele AI**: Execută sau interacționează cu LLM-uri pentru a genera răspunsuri și a coordona fluxurile de lucru AI.
- **Gestionează Conexiunile Clienților**: Creează și mențin un client MCP pentru fiecare conexiune de server MCP.
- **Controlează Interfața Utilizatorului**: Gestionează fluxul conversației, interacțiunile utilizatorului și prezentarea răspunsurilor.  
- **Aplică Securitatea**: Controlează permisiunile, constrângerile de securitate și autentificarea.
- **Gestionează Consimțământul Utilizatorului**: Administrează aprobarea utilizatorului pentru partajarea datelor și execuția instrumentelor.

### 2. Clienți

**Clienții** sunt componente esențiale care mențin conexiuni dedicate unu-la-unu între Gazde și serverele MCP. Fiecare client MCP este instanțiat de Gazdă pentru a se conecta la un server MCP specific, asigurând canale de comunicare organizate și sigure. Mai mulți clienți permit Gazdelor să se conecteze simultan la mai multe servere.

**Clienții** sunt componente de conectare în cadrul aplicației gazdă. Ei:

- **Comunicare Protocol**: Trimit cereri JSON-RPC 2.0 către servere cu solicitări și instrucțiuni.
- **Negocierea Capabilităților**: Negociază caracteristicile suportate și versiunile protocolului cu serverele în timpul inițializării.
- **Execuția Instrumentelor**: Gestionează cererile de execuție ale instrumentelor de la modele și procesează răspunsurile.
- **Actualizări în Timp Real**: Gestionează notificările și actualizările în timp real de la servere.
- **Procesarea Răspunsurilor**: Procesează și formatează răspunsurile serverului pentru afișare utilizatorilor.

### 3. Servere

**Serverele** sunt programe care oferă context, instrumente și capabilități clienților MCP. Ele pot fi executate local (pe aceeași mașină ca Gazda) sau la distanță (pe platforme externe) și sunt responsabile de gestionarea cererilor clienților și de furnizarea răspunsurilor structurate. Serverele expun funcționalități specifice prin Protocolul de Context al Modelului standardizat.

**Serverele** sunt servicii care oferă context și capabilități. Ele:

- **Înregistrarea Caracteristicilor**: Înregistrează și expun primitivele disponibile (resurse, solicitări, instrumente) către clienți.
- **Procesarea Cererilor**: Primesc și execută apeluri de instrumente, cereri de resurse și solicitări de prompturi de la clienți.
- **Furnizarea Contextului**: Oferă informații contextuale și date pentru a îmbunătăți răspunsurile modelului.
- **Gestionarea Stării**: Mențin starea sesiunii și gestionează interacțiunile cu stare atunci când este necesar.
- **Notificări în Timp Real**: Trimit notificări despre modificările și actualizările capabilităților către clienții conectați.

Serverele pot fi dezvoltate de oricine pentru a extinde capabilitățile modelului cu funcționalități specializate și suportă atât scenarii de implementare locală, cât și la distanță.

### 4. Primitivele Serverului

Serverele din Protocolul de Context al Modelului (MCP) oferă trei **primitive** de bază care definesc elementele fundamentale pentru interacțiuni bogate între clienți, gazde și modele de limbaj. Aceste primitive specifică tipurile de informații contextuale și acțiuni disponibile prin protocol.

Serverele MCP pot expune orice combinație dintre următoarele trei primitive de bază:

#### Resurse 

**Resursele** sunt surse de date care oferă informații contextuale aplicațiilor AI. Ele reprezintă conținut static sau dinamic care poate îmbunătăți înțelegerea și luarea deciziilor de către model:

- **Date Contextuale**: Informații structurate și context pentru consumul modelului AI.
- **Baze de Cunoștințe**: Repozitorii de documente, articole, manuale și lucrări de cercetare.
- **Surse de Date Locale**: Fișiere, baze de date și informații ale sistemului local.  
- **Date Externe**: Răspunsuri API, servicii web și date ale sistemelor la distanță.
- **Conținut Dinamic**: Date în timp real care se actualizează în funcție de condițiile externe.

Resursele sunt identificate prin URI-uri și suportă descoperirea prin metodele `resources/list` și recuperarea prin `resources/read`:

```text
file://documents/project-spec.md
database://production/users/schema
api://weather/current
```

#### Solicitări

**Solicitările** sunt șabloane reutilizabile care ajută la structurarea interacțiunilor cu modelele de limbaj. Ele oferă modele standardizate de interacțiune și fluxuri de lucru șablonizate:

- **Interacțiuni Bazate pe Șabloane**: Mesaje pre-structurate și inițiatoare de conversații.
- **Șabloane de Flux de Lucru**: Secvențe standardizate pentru sarcini și interacțiuni comune.
- **Exemple Few-shot**: Șabloane bazate pe exemple pentru instrucțiuni ale modelului.
- **Solicitări de Sistem**: Solicitări fundamentale care definesc comportamentul și contextul modelului.
- **Șabloane Dinamice**: Solicitări parametrizate care se adaptează la contexte specifice.

Solicitările suportă substituirea variabilelor și pot fi descoperite prin `prompts/list` și recuperate cu `prompts/get`:

```markdown
Generate a {{task_type}} for {{product}} targeting {{audience}} with the following requirements: {{requirements}}
```

#### Instrumente

**Instrumentele** sunt funcții executabile pe care modelele AI le pot invoca pentru a efectua acțiuni specifice. Ele reprezintă "verbele" ecosistemului MCP, permițând modelelor să interacționeze cu sisteme externe:

- **Funcții Executabile**: Operațiuni discrete pe care modelele le pot invoca cu parametri specifici.
- **Integrarea Sistemelor Externe**: Apeluri API, interogări de baze de date, operațiuni pe fișiere, calcule.
- **Identitate Unică**: Fiecare instrument are un nume distinct, o descriere și o schemă de parametri.
- **I/O Structurat**: Instrumentele acceptă parametri validați și returnează răspunsuri structurate, tipizate.
- **Capabilități de Acțiune**: Permit modelelor să efectueze acțiuni reale și să obțină date live.

Instrumentele sunt definite cu JSON Schema pentru validarea parametrilor și descoperite prin `tools/list` și executate prin `tools/call`:

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

## Primitivele Clientului

În Protocolul de Context al Modelului (MCP), **clienții** pot expune primitive care permit serverelor să solicite capabilități suplimentare de la aplicația gazdă. Aceste primitive de partea clientului permit implementări de server mai bogate și mai interactive, care pot accesa capabilitățile modelului AI și interacțiunile utilizatorului.

### Sampling

**Sampling** permite serverelor să solicite completări ale modelului de limbaj de la aplicația AI a clientului. Această primitivă permite serverelor să acceseze capabilitățile LLM fără a încorpora propriile dependențe de model:

- **Acces Independent de Model**: Serverele pot solicita completări fără a include SDK-uri LLM sau a gestiona accesul la model.
- **AI Inițiat de Server**: Permite serverelor să genereze autonom conținut utilizând modelul AI al clientului.
- **Interacțiuni Recursive LLM**: Suportă scenarii complexe în care serverele au nevoie de asistență AI pentru procesare.
- **Generarea Dinamică de Conținut**: Permite serverelor să creeze răspunsuri contextuale utilizând modelul gazdei.

Sampling este inițiat prin metoda `sampling/complete`, unde serverele trimit cereri de completare către clienți.

### Elicitation  

**Elicitation** permite serverelor să solicite informații suplimentare sau confirmări de la utilizatori prin interfața clientului:

- **Cereri de Input ale Utilizatorului**: Serverele pot solicita informații suplimentare atunci când sunt necesare pentru execuția instrumentelor.
- **Dialoguri de Confirmare**: Solicită aprobarea utilizatorului pentru operațiuni sensibile sau cu impact.
- **Fluxuri de Lucru Interactive**: Permite serverelor să creeze interacțiuni pas cu pas cu utilizatorul.
- **Colectarea Dinamică a Parametrilor**: Adună parametri lipsă sau opționali în timpul execuției instrumentelor.

Cererile de elicitation sunt realizate utilizând metoda `elicitation/request` pentru a colecta inputul utilizatorului prin interfața clientului.

### Logging

**Logging** permite serverelor să trimită mesaje de jurnal structurate către clienți pentru depanare, monitorizare și vizibilitate operațională:

- **Suport pentru Depanare**: Permite serverelor să furnizeze jurnale detaliate de execuție pentru rezolvarea problemelor.
- **Monitorizare Operațională**: Trimite actualizări de stare și metrici de performanță către clienți.
- **Raportarea Erorilor**: Oferă context detaliat al erorilor și informații de diagnostic.
- **Urme de Audit**: Creează jurnale cuprinzătoare ale operațiunilor și deciziilor serverului.

Mesajele de jurnal sunt trimise către clienți pentru a oferi transparență în operațiunile serverului și pentru a facilita depanarea.

## Fluxul de Informații în MCP

Protocolul de Context al Modelului (MCP) definește un flux structurat de informații între gazde, clienți, servere și modele. Înțelegerea acestui flux ajută la clarificarea modului în care cererile utilizatorului sunt procesate și cum instrumentele și datele externe sunt integrate în răspunsurile modelului.

- **Gazda Inițiază Conexiunea**  
  Aplicația gazdă (cum ar fi un IDE sau o interfață de chat) stabilește o conexiune la un server MCP, de obicei prin STDIO, WebSocket sau alt transport suportat.

- **Negocierea Capabilităților**  
  Clientul (încorporat în gazdă) și serverul schimbă informații despre caracteristicile, instrumentele, resursele și versiunile protocolului suportate. Acest lucru asigură că ambele părți înțeleg ce capabilități sunt disponibile pentru sesiune.

- **Cererea Utilizatorului**  
  Utilizatorul interacționează cu gazda (de exemplu, introduce un prompt sau o comandă). Gazda colectează acest input și îl transmite clientului pentru procesare.

- **Utilizarea Resurselor sau Instrumentelor**  
  - Clientul poate solicita context suplimentar sau resurse de la server (cum ar fi fișiere, intrări din baze de date sau articole din baza de cunoștințe) pentru a îmbunătăți înțelegerea modelului.
  - Dacă modelul determină că este necesar un instrument (de exemplu, pentru a obține date, a efectua un calcul sau a apela un API), clientul trimite o cerere de invocare a instrumentului
- **Protocolul JSON-RPC 2.0**: Toată comunicarea utilizează formatul standardizat de mesaje JSON-RPC 2.0 pentru apeluri de metode, răspunsuri și notificări.
- **Gestionarea ciclului de viață**: Se ocupă de inițializarea conexiunii, negocierea capabilităților și terminarea sesiunii între clienți și servere.
- **Primitivele serverului**: Permite serverelor să ofere funcționalități de bază prin instrumente, resurse și șabloane.
- **Primitivele clientului**: Permite serverelor să solicite eșantionare de la LLM-uri, să obțină input de la utilizatori și să trimită mesaje de jurnal.
- **Notificări în timp real**: Suportă notificări asincrone pentru actualizări dinamice fără interogare continuă.

#### Caracteristici cheie:

- **Negocierea versiunii protocolului**: Utilizează versiuni bazate pe dată (YYYY-MM-DD) pentru a asigura compatibilitatea.
- **Descoperirea capabilităților**: Clienții și serverele schimbă informații despre funcționalitățile suportate în timpul inițializării.
- **Sesiuni cu stare**: Menține starea conexiunii pe parcursul mai multor interacțiuni pentru continuitatea contextului.

### Strat de transport

**Stratul de transport** gestionează canalele de comunicare, încadrarea mesajelor și autentificarea între participanții MCP:

#### Mecanisme de transport suportate:

1. **Transport STDIO**:
   - Utilizează fluxurile de intrare/ieșire standard pentru comunicarea directă între procese.
   - Optim pentru procese locale pe aceeași mașină, fără costuri de rețea.
   - Utilizat frecvent pentru implementările locale ale serverelor MCP.

2. **Transport HTTP Streamabil**:
   - Utilizează HTTP POST pentru mesaje de la client la server.
   - Opțional, Server-Sent Events (SSE) pentru streaming de la server la client.
   - Permite comunicarea cu servere la distanță prin rețele.
   - Suportă autentificarea standard HTTP (token-uri bearer, chei API, anteturi personalizate).
   - MCP recomandă OAuth pentru autentificare sigură bazată pe token-uri.

#### Abstracția transportului:

Stratul de transport abstractizează detaliile comunicării față de stratul de date, permițând utilizarea aceluiași format de mesaje JSON-RPC 2.0 pe toate mecanismele de transport. Această abstracție permite aplicațiilor să comute fără probleme între servere locale și servere la distanță.

### Considerații de securitate

Implementările MCP trebuie să respecte mai multe principii critice de securitate pentru a asigura interacțiuni sigure, de încredere și securizate în toate operațiunile protocolului:

- **Consimțământul și controlul utilizatorului**: Utilizatorii trebuie să ofere consimțământ explicit înainte ca orice date să fie accesate sau operațiuni să fie efectuate. Aceștia trebuie să aibă un control clar asupra datelor partajate și acțiunilor autorizate, susținut de interfețe intuitive pentru revizuirea și aprobarea activităților.

- **Confidențialitatea datelor**: Datele utilizatorului trebuie expuse doar cu consimțământ explicit și trebuie protejate prin controale adecvate de acces. Implementările MCP trebuie să prevină transmiterea neautorizată a datelor și să asigure confidențialitatea pe parcursul tuturor interacțiunilor.

- **Siguranța instrumentelor**: Înainte de a invoca orice instrument, este necesar consimțământul explicit al utilizatorului. Utilizatorii trebuie să înțeleagă clar funcționalitatea fiecărui instrument, iar limitele de securitate robuste trebuie să fie impuse pentru a preveni execuția neintenționată sau nesigură a instrumentelor.

Respectând aceste principii de securitate, MCP asigură menținerea încrederii, confidențialității și siguranței utilizatorilor în toate interacțiunile protocolului, oferind în același timp integrații puternice cu AI.

## Exemple de cod: componente cheie

Mai jos sunt exemple de cod în mai multe limbaje de programare populare care ilustrează cum să implementați componentele cheie ale serverului MCP și instrumentele.

### Exemplu .NET: Crearea unui server MCP simplu cu instrumente

Iată un exemplu practic în .NET care demonstrează cum să implementați un server MCP simplu cu instrumente personalizate. Acest exemplu arată cum să definiți și să înregistrați instrumente, să gestionați cererile și să conectați serverul utilizând Protocolul Contextului Modelului.

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

### Exemplu Java: Componentele serverului MCP

Acest exemplu demonstrează același server MCP și înregistrarea instrumentelor ca în exemplul .NET de mai sus, dar implementat în Java.

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

### Exemplu Python: Construirea unui server MCP

Acest exemplu utilizează fastmcp, așa că asigurați-vă că îl instalați mai întâi:

```python
pip install fastmcp
```  
Exemplu de cod:

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

### Exemplu JavaScript: Crearea unui server MCP

Acest exemplu arată crearea unui server MCP în JavaScript și cum să înregistrați două instrumente legate de vreme.

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

Acest exemplu JavaScript demonstrează cum să creați un client MCP care se conectează la un server, trimite un șablon și procesează răspunsul, inclusiv orice apeluri de instrumente efectuate.

## Securitate și autorizare

MCP include mai multe concepte și mecanisme încorporate pentru gestionarea securității și autorizării pe parcursul protocolului:

1. **Controlul permisiunilor instrumentelor**:  
   Clienții pot specifica ce instrumente are voie un model să utilizeze în timpul unei sesiuni. Acest lucru asigură că doar instrumentele autorizate explicit sunt accesibile, reducând riscul operațiunilor neintenționate sau nesigure. Permisiunile pot fi configurate dinamic pe baza preferințelor utilizatorului, politicilor organizaționale sau contextului interacțiunii.

2. **Autentificare**:  
   Serverele pot solicita autentificare înainte de a acorda acces la instrumente, resurse sau operațiuni sensibile. Acest lucru poate implica chei API, token-uri OAuth sau alte scheme de autentificare. Autentificarea corespunzătoare asigură că doar clienții și utilizatorii de încredere pot invoca capabilitățile serverului.

3. **Validare**:  
   Validarea parametrilor este impusă pentru toate invocările de instrumente. Fiecare instrument definește tipurile, formatele și constrângerile așteptate pentru parametrii săi, iar serverul validează cererile primite în consecință. Acest lucru previne intrările defecte sau malițioase să ajungă la implementările instrumentelor și ajută la menținerea integrității operațiunilor.

4. **Limitarea ratei**:  
   Pentru a preveni abuzurile și a asigura utilizarea echitabilă a resurselor serverului, serverele MCP pot implementa limitarea ratei pentru apelurile de instrumente și accesul la resurse. Limitele de rată pot fi aplicate per utilizator, per sesiune sau global și ajută la protejarea împotriva atacurilor de tip denial-of-service sau consumului excesiv de resurse.

Prin combinarea acestor mecanisme, MCP oferă o fundație sigură pentru integrarea modelelor lingvistice cu instrumente și surse de date externe, oferind utilizatorilor și dezvoltatorilor control detaliat asupra accesului și utilizării.

## Mesaje de protocol și fluxul de comunicare

Comunicarea MCP utilizează mesaje structurate **JSON-RPC 2.0** pentru a facilita interacțiuni clare și de încredere între gazde, clienți și servere. Protocolul definește modele specifice de mesaje pentru diferite tipuri de operațiuni:

### Tipuri de mesaje de bază:

#### **Mesaje de inițializare**
- Cerere **`initialize`**: Stabilește conexiunea și negociază versiunea protocolului și capabilitățile.
- Răspuns **`initialize`**: Confirmă funcționalitățile suportate și informațiile serverului.
- **`notifications/initialized`**: Semnalează că inițializarea este completă și sesiunea este gata.

#### **Mesaje de descoperire**
- Cerere **`tools/list`**: Descoperă instrumentele disponibile de la server.
- Cerere **`resources/list`**: Listează resursele disponibile (surse de date).
- Cerere **`prompts/list`**: Recuperează șabloanele de șablon disponibile.

#### **Mesaje de execuție**  
- Cerere **`tools/call`**: Execută un instrument specific cu parametrii furnizați.
- Cerere **`resources/read`**: Recuperează conținutul dintr-o resursă specifică.
- Cerere **`prompts/get`**: Obține un șablon cu parametri opționali.

#### **Mesaje pe partea clientului**
- Cerere **`sampling/complete`**: Serverul solicită completarea LLM de la client.
- **`elicitation/request`**: Serverul solicită input de la utilizator prin interfața clientului.
- Mesaje de jurnalizare: Serverul trimite mesaje structurate de jurnal către client.

#### **Mesaje de notificare**
- **`notifications/tools/list_changed`**: Serverul notifică clientul despre modificările instrumentelor.
- **`notifications/resources/list_changed`**: Serverul notifică clientul despre modificările resurselor.
- **`notifications/prompts/list_changed`**: Serverul notifică clientul despre modificările șabloanelor.

### Structura mesajelor:

Toate mesajele MCP urmează formatul JSON-RPC 2.0 cu:
- **Mesaje de cerere**: Includ `id`, `method` și opțional `params`.
- **Mesaje de răspuns**: Includ `id` și fie `result`, fie `error`.
- **Mesaje de notificare**: Includ `method` și opțional `params` (fără `id` sau răspuns așteptat).

Această comunicare structurată asigură interacțiuni fiabile, trasabile și extensibile, susținând scenarii avansate precum actualizări în timp real, lanțuri de instrumente și gestionarea robustă a erorilor.

## Concluzii cheie

- **Arhitectură**: MCP utilizează o arhitectură client-server în care gazdele gestionează mai multe conexiuni ale clienților la servere.
- **Participanți**: Ecosistemul include gazde (aplicații AI), clienți (conectori de protocol) și servere (furnizori de capabilități).
- **Mecanisme de transport**: Comunicarea suportă STDIO (local) și HTTP Streamabil cu SSE opțional (la distanță).
- **Primitive de bază**: Serverele expun instrumente (funcții executabile), resurse (surse de date) și șabloane (template-uri).
- **Primitivele clientului**: Serverele pot solicita eșantionare (completări LLM), obținerea inputului (de la utilizatori) și jurnalizare de la clienți.
- **Fundamentul protocolului**: Bazat pe JSON-RPC 2.0 cu versiuni bazate pe dată (actual: 2025-06-18).
- **Capabilități în timp real**: Suportă notificări pentru actualizări dinamice și sincronizare în timp real.
- **Securitate prioritară**: Consimțământ explicit al utilizatorului, protecția confidențialității datelor și transport securizat sunt cerințe de bază.

## Exercițiu

Proiectați un instrument MCP simplu care ar fi util în domeniul dvs. Definiți:
1. Cum s-ar numi instrumentul.
2. Ce parametri ar accepta.
3. Ce output ar returna.
4. Cum ar putea un model să utilizeze acest instrument pentru a rezolva problemele utilizatorului.

---

## Ce urmează

Următorul: [Capitolul 2: Securitate](../02-Security/README.md)

---

**Declinarea responsabilității**:  
Acest document a fost tradus utilizând serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși depunem eforturi pentru a asigura acuratețea, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă ar trebui considerat sursa autoritară. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm răspunderea pentru eventualele neînțelegeri sau interpretări greșite care pot apărea din utilizarea acestei traduceri.