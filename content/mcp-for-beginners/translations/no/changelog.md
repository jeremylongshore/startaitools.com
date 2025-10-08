<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:19:38+00:00",
  "source_file": "changelog.md",
  "language_code": "no"
}
-->
# Endringslogg: MCP for nybegynnere pensum

Dette dokumentet fungerer som en oversikt over alle betydelige endringer gjort i pensumet for Model Context Protocol (MCP) for nybegynnere. Endringer er dokumentert i omvendt kronologisk rekkefølge (nyeste endringer først).

## 6. oktober 2025

### Utvidelse av "Kom i gang"-seksjonen – Avansert serverbruk og enkel autentisering

#### Avansert serverbruk (03-GettingStarted/10-advanced)
- **Ny kapittel lagt til**: Introduksjon til avansert MCP-serverbruk, som dekker både vanlige og lavnivå serverarkitekturer.
  - **Vanlig vs. lavnivå server**: Detaljert sammenligning og kodeeksempler i Python og TypeScript for begge tilnærminger.
  - **Handler-basert design**: Forklaring av handler-basert verktøy/ressurs/prompt-håndtering for skalerbare og fleksible serverimplementasjoner.
  - **Praktiske mønstre**: Virkelige scenarier der lavnivå servermønstre er fordelaktige for avanserte funksjoner og arkitektur.

#### Enkel autentisering (03-GettingStarted/11-simple-auth)
- **Ny kapittel lagt til**: Trinnvis veiledning for implementering av enkel autentisering i MCP-servere.
  - **Autentiseringskonsepter**: Klar forklaring av autentisering vs. autorisasjon og håndtering av legitimasjon.
  - **Grunnleggende autentisering**: Middleware-basert autentiseringsmønstre i Python (Starlette) og TypeScript (Express), med kodeeksempler.
  - **Overgang til avansert sikkerhet**: Veiledning om hvordan man starter med enkel autentisering og går videre til OAuth 2.1 og RBAC, med referanser til avanserte sikkerhetsmoduler.

Disse tilleggene gir praktisk, praktisk veiledning for å bygge mer robuste, sikre og fleksible MCP-serverimplementasjoner, og brobygger grunnleggende konsepter med avanserte produksjonsmønstre.

## 29. september 2025

### MCP Server Database Integration Labs – Omfattende praktisk læringssti

#### 11-MCPServerHandsOnLabs - Nytt komplett pensum for databaseintegrasjon
- **Komplett 13-lab læringssti**: Lagt til omfattende praktisk pensum for å bygge produksjonsklare MCP-servere med PostgreSQL-databaseintegrasjon.
  - **Virkelig implementering**: Zava Retail-analysebrukstilfelle som demonstrerer mønstre på bedriftsnivå.
  - **Strukturert læringsprogresjon**:
    - **Labs 00-03: Grunnleggende** - Introduksjon, kjernearkitektur, sikkerhet og multi-tenancy, miljøoppsett.
    - **Labs 04-06: Bygging av MCP-serveren** - Databasedesign og skjema, MCP-serverimplementering, verktøyutvikling.
    - **Labs 07-09: Avanserte funksjoner** - Semantisk søkeintegrasjon, testing og feilsøking, VS Code-integrasjon.
    - **Labs 10-12: Produksjon og beste praksis** - Distribusjonsstrategier, overvåking og observasjon, beste praksis og optimalisering.
  - **Bedriftsteknologier**: FastMCP-rammeverk, PostgreSQL med pgvector, Azure OpenAI-embeddings, Azure Container Apps, Application Insights.
  - **Avanserte funksjoner**: Row Level Security (RLS), semantisk søk, multi-tenant dataadgang, vektorembeddings, sanntidsovervåking.

#### Terminologistandardisering - Modul til lab-konvertering
- **Omfattende dokumentasjonsoppdatering**: Systematisk oppdatert alle README-filer i 11-MCPServerHandsOnLabs for å bruke "Lab"-terminologi i stedet for "Modul".
  - **Seksjonsoverskrifter**: Oppdatert "Hva denne modulen dekker" til "Hva denne laben dekker" på tvers av alle 13 laber.
  - **Innholdsbeskrivelse**: Endret "Denne modulen gir..." til "Denne laben gir..." gjennom hele dokumentasjonen.
  - **Læringsmål**: Oppdatert "Ved slutten av denne modulen..." til "Ved slutten av denne laben..."
  - **Navigasjonslenker**: Konvertert alle "Modul XX:"-referanser til "Lab XX:" i kryssreferanser og navigasjon.
  - **Fullføringssporing**: Oppdatert "Etter å ha fullført denne modulen..." til "Etter å ha fullført denne laben..."
  - **Bevarte tekniske referanser**: Opprettholdt Python-modulreferanser i konfigurasjonsfiler (f.eks., `"module": "mcp_server.main"`).

#### Forbedring av studieveiledning (study_guide.md)
- **Visuell pensumkart**: Lagt til ny "11. Database Integration Labs"-seksjon med omfattende labstrukturvisualisering.
- **Repository-struktur**: Oppdatert fra ti til elleve hovedseksjoner med detaljert beskrivelse av 11-MCPServerHandsOnLabs.
- **Veiledning for læringssti**: Forbedret navigasjonsinstruksjoner for å dekke seksjoner 00-11.
- **Teknologidekning**: Lagt til detaljer om FastMCP, PostgreSQL, Azure-tjenesteintegrasjon.
- **Læringsresultater**: Fremhevet produksjonsklar serverutvikling, databaseintegrasjonsmønstre og sikkerhet på bedriftsnivå.

#### Hoved README-strukturforbedring
- **Lab-basert terminologi**: Oppdatert hoved README.md i 11-MCPServerHandsOnLabs for konsekvent bruk av "Lab"-struktur.
- **Organisering av læringssti**: Klar progresjon fra grunnleggende konsepter gjennom avansert implementering til produksjonsdistribusjon.
- **Virkelighetsfokus**: Vekt på praktisk, praktisk læring med mønstre og teknologier på bedriftsnivå.

### Dokumentasjonskvalitet og konsistensforbedringer
- **Praktisk læringsfokus**: Forsterket praktisk, lab-basert tilnærming gjennom hele dokumentasjonen.
- **Fokus på mønstre på bedriftsnivå**: Fremhevet produksjonsklare implementeringer og sikkerhetsbetraktninger på bedriftsnivå.
- **Teknologiintegrasjon**: Omfattende dekning av moderne Azure-tjenester og AI-integrasjonsmønstre.
- **Læringsprogresjon**: Klar, strukturert sti fra grunnleggende konsepter til produksjonsdistribusjon.

## 26. september 2025

### Forbedring av casestudier – GitHub MCP Registry-integrasjon

#### Casestudier (09-CaseStudy/) - Fokus på økosystemutvikling
- **README.md**: Stor utvidelse med omfattende GitHub MCP Registry casestudie.
  - **GitHub MCP Registry casestudie**: Ny omfattende casestudie som undersøker GitHubs MCP Registry-lansering i september 2025.
    - **Problemanalyse**: Detaljert undersøkelse av fragmenterte MCP-serveroppdagelses- og distribusjonsutfordringer.
    - **Løsningsarkitektur**: GitHubs sentraliserte registertilnærming med ett-klikks VS Code-installasjon.
    - **Forretningspåvirkning**: Målbare forbedringer i utvikleropplæring og produktivitet.
    - **Strategisk verdi**: Fokus på modulær agentdistribusjon og interoperabilitet mellom verktøy.
    - **Økosystemutvikling**: Posisjonering som grunnleggende plattform for agentisk integrasjon.
  - **Forbedret casestudiestruktur**: Oppdatert alle syv casestudier med konsekvent formatering og omfattende beskrivelser.
    - Azure AI Travel Agents: Vekt på multi-agent orkestrering.
    - Azure DevOps-integrasjon: Fokus på arbeidsflytautomatisering.
    - Sanntids dokumenthenting: Python konsollklientimplementering.
    - Interaktiv studieplangenerator: Chainlit samtalewebapp.
    - Dokumentasjon i editor: VS Code og GitHub Copilot-integrasjon.
    - Azure API Management: Integrasjonsmønstre for bedrifts-API.
    - GitHub MCP Registry: Økosystemutvikling og samfunnsplattform.
  - **Omfattende konklusjon**: Omskrevet konklusjonsseksjon som fremhever syv casestudier som dekker flere MCP-implementeringsdimensjoner.
    - Kategorisering av bedriftsintegrasjon, multi-agent orkestrering, utviklerproduktivitet.
    - Økosystemutvikling, utdanningsapplikasjoner.
    - Forbedrede innsikter i arkitekturmønstre, implementeringsstrategier og beste praksis.
    - Vekt på MCP som en moden, produksjonsklar protokoll.

#### Oppdateringer av studieveiledning (study_guide.md)
- **Visuell pensumkart**: Oppdatert tankekart for å inkludere GitHub MCP Registry i seksjonen for casestudier.
- **Beskrivelse av casestudier**: Forbedret fra generiske beskrivelser til detaljert oppdeling av syv omfattende casestudier.
- **Repository-struktur**: Oppdatert seksjon 10 for å reflektere omfattende dekning av casestudier med spesifikke implementeringsdetaljer.
- **Integrasjon av endringslogg**: Lagt til 26. september 2025-oppføring som dokumenterer GitHub MCP Registry-tillegg og forbedringer av casestudier.
- **Datooppdateringer**: Oppdatert bunnteksttidsstempel for å reflektere siste revisjon (26. september 2025).

### Forbedringer av dokumentasjonskvalitet
- **Konsistensforbedring**: Standardisert formatering og struktur for casestudier på tvers av alle syv eksempler.
- **Omfattende dekning**: Casestudier dekker nå scenarier for bedrifter, utviklerproduktivitet og økosystemutvikling.
- **Strategisk posisjonering**: Forsterket fokus på MCP som grunnleggende plattform for distribusjon av agentiske systemer.
- **Ressursintegrasjon**: Oppdatert tilleggsressurser for å inkludere lenke til GitHub MCP Registry.

## 15. september 2025

### Utvidelse av avanserte emner – Tilpassede transportmekanismer og kontekstingeniørkunst

#### MCP Tilpassede transportmekanismer (05-AdvancedTopics/mcp-transport/) - Ny avansert implementeringsveiledning
- **README.md**: Komplett implementeringsveiledning for tilpassede MCP transportmekanismer.
  - **Azure Event Grid Transport**: Omfattende serverløs hendelsesdrevet transportimplementering.
    - Eksempler i C#, TypeScript og Python med Azure Functions-integrasjon.
    - Hendelsesdrevet arkitekturmønstre for skalerbare MCP-løsninger.
    - Webhook-mottakere og push-basert meldingshåndtering.
  - **Azure Event Hubs Transport**: Høy gjennomstrømming streaming transportimplementering.
    - Sanntids streamingkapasiteter for lav-latens scenarier.
    - Partisjoneringsstrategier og sjekkpunkthåndtering.
    - Meldingsbatching og ytelsesoptimalisering.
  - **Integrasjonsmønstre for bedrifter**: Produksjonsklare arkitektureksempler.
    - Distribuert MCP-prosessering på tvers av flere Azure Functions.
    - Hybrid transportarkitekturer som kombinerer flere transporttyper.
    - Meldingsholdbarhet, pålitelighet og feilhåndteringsstrategier.
  - **Sikkerhet og overvåking**: Azure Key Vault-integrasjon og observasjonsmønstre.
    - Autentisering med administrerte identiteter og minst privilegert tilgang.
    - Application Insights-telemetri og ytelsesovervåking.
    - Kretsbrytere og feiltoleransemønstre.
  - **Testingsrammeverk**: Omfattende teststrategier for tilpassede transportmekanismer.
    - Enhetstesting med testdoubles og mocking-rammeverk.
    - Integrasjonstesting med Azure Test Containers.
    - Ytelses- og belastningstesting.

#### Kontekstingeniørkunst (05-AdvancedTopics/mcp-contextengineering/) - Fremvoksende AI-disiplin
- **README.md**: Omfattende utforskning av kontekstingeniørkunst som et fremvoksende felt.
  - **Kjerneprinsipper**: Fullstendig kontekstdeling, bevissthet om handlingsbeslutninger og kontekstvinduadministrasjon.
  - **MCP-protokolltilpasning**: Hvordan MCP-design adresserer utfordringer innen kontekstingeniørkunst.
    - Begrensninger i kontekstvinduer og progressive lastestrategier.
    - Relevansbestemmelse og dynamisk konteksthenting.
    - Multi-modal konteksthåndtering og sikkerhetsbetraktninger.
  - **Implementeringstilnærminger**: Enkelttrådede vs. multi-agent arkitekturer.
    - Kontekstchunking og prioriteringsteknikker.
    - Progressiv kontekstlasting og komprimeringsstrategier.
    - Lagdelte konteksttilnærminger og optimalisering av henting.
  - **Målingsrammeverk**: Fremvoksende metrikker for evaluering av konteksteffektivitet.
    - Inngangseffektivitet, ytelse, kvalitet og brukeropplevelsesbetraktninger.
    - Eksperimentelle tilnærminger til kontekstoptimalisering.
    - Feilanalyse og forbedringsmetodologier.

#### Oppdateringer av pensumnavigasjon (README.md)
- **Forbedret modulstruktur**: Oppdatert pensumtabell for å inkludere nye avanserte emner.
  - Lagt til Kontekstingeniørkunst (5.14) og Tilpasset transport (5.15).
  - Konsistent formatering og navigasjonslenker på tvers av alle moduler.
  - Oppdaterte beskrivelser for å reflektere nåværende innholdsomfang.

### Forbedringer av katalogstruktur
- **Navnestandardisering**: Omdøpt "mcp transport" til "mcp-transport" for konsistens med andre avanserte emne-mapper.
- **Innholdsorganisering**: Alle 05-AdvancedTopics-mapper følger nå konsistent navnemønster (mcp-[emne]).

### Forbedringer av dokumentasjonskvalitet
- **MCP-spesifikasjonsjustering**: Alt nytt innhold refererer til gjeldende MCP-spesifikasjon 2025-06-18.
- **Eksempler på flere språk**: Omfattende kodeeksempler i C#, TypeScript og Python.
- **Fokus på bedrifter**: Produksjonsklare mønstre og Azure-skyintegrasjon gjennom hele.
- **Visuell dokumentasjon**: Mermaid-diagrammer for arkitektur og flytvisualisering.

## 18. august 2025

### Omfattende dokumentasjonsoppdatering – MCP 2025-06-18-standarder

#### MCP Sikkerhetsbeste praksis (02-Security/) - Full modernisering
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Fullstendig omskriving i tråd med MCP-spesifikasjon 2025-06-18.
  - **Obligatoriske krav**: Lagt til eksplisitte MUST/MUST NOT-krav fra offisiell spesifikasjon med klare visuelle indikatorer.
  - **12 kjernepraksiser for sikkerhet**: Restrukturert fra 15-punkts liste til omfattende sikkerhetsdomener.
    - Tokensikkerhet og autentisering med integrasjon av eksterne identitetsleverandører.
    - Sesjonsadministrasjon og transportsikkerhet med kryptografiske krav.
    - AI-spesifikk trusselbeskyttelse med Microsoft Prompt Shields-integrasjon.
    - Tilgangskontroll og tillatelser med prinsippet om minst privilegium.
    - Innholdssikkerhet og overvåking med Azure Content Safety-integrasjon.
    - Forsyningskjedesikkerhet med omfattende komponentverifisering.
    - OAuth-sikkerhet og forvirret stedfortrederforebygging med PKCE-implementering.
    - Hendelsesrespons og gjenoppretting med automatiserte kapabiliteter.
    - Samsvar og styring med regulatorisk tilpasning.
    - Avanserte sikkerhetskontroller med null tillitsarkitektur.
    - Microsoft sikkerhetsøkosystemintegrasjon med omfattende løsninger.
    - Kontinuerlig sikkerhetsevolusjon med adaptive praksiser.
  - **Microsoft sikkerhetsløsninger**: Forbedret integrasjonsveiledning for Prompt Shields, Azure Content Safety, Entra ID og GitHub Advanced Security.
  - **Implementeringsressurser**: Kategoriserte omfattende ressurslenker etter Offisiell MCP-dokumentasjon, Microsoft sikkerhetsløsninger, sikkerhetsstandarder og implementeringsveiledninger.

#### Avanserte sikkerhetskontroller (02-Security/) - Implementering på bedriftsnivå
- **MCP-SECURITY-CONTROLS-2025.md**: Fullstendig overhaling med sikkerhetsrammeverk på bedriftsnivå.
  - **9 omfattende sikkerhetsdomener**: Utvidet fra grunnleggende kontroller til detaljert rammeverk på bedriftsnivå.
    - Avansert autentisering og autorisasjon med Microsoft Entra ID-integrasjon.
    - Tokensikkerhet og anti-passthrough-kontroller med omfattende validering.
    - Sesjonssikkerhetskontroller med kapringforebygging.
    - AI-spesifikke sikkerhetskontroller med promptinj
#### Avanserte emner sikkerhet (05-AdvancedTopics/mcp-security/) - Produksjonsklar implementering
- **README.md**: Fullstendig omskriving for implementering av sikkerhet på bedriftsnivå
  - **Nåværende spesifikasjonsjustering**: Oppdatert til MCP-spesifikasjon 2025-06-18 med obligatoriske sikkerhetskrav
  - **Forbedret autentisering**: Microsoft Entra ID-integrasjon med omfattende eksempler i .NET og Java Spring Security
  - **AI-sikkerhetsintegrasjon**: Implementering av Microsoft Prompt Shields og Azure Content Safety med detaljerte eksempler i Python
  - **Avansert trusselredusering**: Omfattende implementeringseksempler for
    - Forebygging av "Confused Deputy"-angrep med PKCE og validering av brukersamtykke
    - Forebygging av token-passthrough med validering av målgruppe og sikker tokenhåndtering
    - Forebygging av sesjonskapring med kryptografisk binding og atferdsanalyse
  - **Integrasjon av bedriftsikkerhet**: Overvåking med Azure Application Insights, trusseldeteksjonspipelines og forsyningskjedesikkerhet
  - **Implementeringssjekkliste**: Klare obligatoriske vs. anbefalte sikkerhetskontroller med fordeler fra Microsofts sikkerhetsøkosystem

### Dokumentasjonskvalitet og standardjustering
- **Spesifikasjonsreferanser**: Oppdatert alle referanser til gjeldende MCP-spesifikasjon 2025-06-18
- **Microsofts sikkerhetsøkosystem**: Forbedret integrasjonsveiledning gjennom all sikkerhetsdokumentasjon
- **Praktisk implementering**: Lagt til detaljerte kodeeksempler i .NET, Java og Python med mønstre for bedriftsbruk
- **Ressursorganisering**: Omfattende kategorisering av offisiell dokumentasjon, sikkerhetsstandarder og implementeringsveiledninger
- **Visuelle indikatorer**: Klar markering av obligatoriske krav vs. anbefalte praksiser

#### Grunnleggende konsepter (01-CoreConcepts/) - Full modernisering
- **Protokollversjonsoppdatering**: Oppdatert til å referere til gjeldende MCP-spesifikasjon 2025-06-18 med datobasert versjonering (YYYY-MM-DD-format)
- **Arkitekturbeskrivelse**: Forbedrede beskrivelser av verter, klienter og servere for å reflektere gjeldende MCP-arkitekturmønstre
  - Verter nå tydelig definert som AI-applikasjoner som koordinerer flere MCP-klienttilkoblinger
  - Klienter beskrevet som protokollkoblinger som opprettholder én-til-én serverforhold
  - Servere forbedret med lokale vs. eksterne distribusjonsscenarier
- **Omstrukturering av primitiver**: Fullstendig overhaling av server- og klientprimitiver
  - Serverprimitiver: Ressurser (datakilder), Prompter (maler), Verktøy (eksekverbare funksjoner) med detaljerte forklaringer og eksempler
  - Klientprimitiver: Sampling (LLM-fullføringer), Elicitering (brukerinndata), Logging (feilsøking/overvåking)
  - Oppdatert med gjeldende oppdagelses- (`*/list`), hentings- (`*/get`) og eksekverings- (`*/call`) metode-mønstre
- **Protokollarkitektur**: Introdusert tolags arkitekturmodell
  - Datalag: JSON-RPC 2.0-grunnlag med livssyklusadministrasjon og primitiver
  - Transportlag: STDIO (lokalt) og Streamable HTTP med SSE (eksterne) transportmekanismer
- **Sikkerhetsrammeverk**: Omfattende sikkerhetsprinsipper inkludert eksplisitt brukersamtykke, databeskyttelse, verktøysikkerhet og transportlagsikkerhet
- **Kommunikasjonsmønstre**: Oppdaterte protokollmeldinger for å vise initialisering, oppdagelse, eksekvering og varslingsflyter
- **Kodeeksempler**: Oppfrisket flerspråklige eksempler (.NET, Java, Python, JavaScript) for å reflektere gjeldende MCP SDK-mønstre

#### Sikkerhet (02-Security/) - Omfattende sikkerhetsrevisjon  
- **Standardjustering**: Full justering med MCP-spesifikasjon 2025-06-18 sikkerhetskrav
- **Autentiseringsevolusjon**: Dokumentert utvikling fra tilpassede OAuth-servere til delegasjon til eksterne identitetsleverandører (Microsoft Entra ID)
- **AI-spesifikk trusselanalyse**: Forbedret dekning av moderne AI-angrepsvektorer
  - Detaljerte scenarier for prompt-injeksjonsangrep med eksempler fra virkeligheten
  - Mekanismer for verktøyforgiftning og "rug pull"-angrepsmønstre
  - Angrep på kontekstvindu og modellforvirring
- **Microsoft AI-sikkerhetsløsninger**: Omfattende dekning av Microsofts sikkerhetsøkosystem
  - AI Prompt Shields med avansert deteksjon, spotlighting og skilleteknikker
  - Azure Content Safety-integrasjonsmønstre
  - GitHub Advanced Security for forsyningskjedevern
- **Avansert trusselredusering**: Detaljerte sikkerhetskontroller for
  - Sesjonskapring med MCP-spesifikke angrepsscenarier og krav til kryptografisk sesjons-ID
  - "Confused Deputy"-problemer i MCP-proxy-scenarier med eksplisitte samtykkekrav
  - Token-passthrough-sårbarheter med obligatoriske valideringskontroller
- **Forsyningskjedesikkerhet**: Utvidet dekning av AI-forsyningskjeden inkludert grunnmodeller, embeddings-tjenester, kontekstleverandører og tredjeparts-APIer
- **Grunnsikkerhet**: Forbedret integrasjon med sikkerhetsmønstre for bedrifter, inkludert nulltillitsarkitektur og Microsofts sikkerhetsøkosystem
- **Ressursorganisering**: Kategorisert omfattende ressurslenker etter type (Offisielle dokumenter, standarder, forskning, Microsoft-løsninger, implementeringsveiledninger)

### Forbedringer i dokumentasjonskvalitet
- **Strukturerte læringsmål**: Forbedrede læringsmål med spesifikke, handlingsrettede utfall 
- **Kryssreferanser**: Lagt til lenker mellom relaterte sikkerhets- og grunnkonseptemner
- **Oppdatert informasjon**: Oppdatert alle datoreferanser og spesifikasjonslenker til gjeldende standarder
- **Implementeringsveiledning**: Lagt til spesifikke, handlingsrettede implementeringsretningslinjer gjennom begge seksjoner

## 16. juli 2025

### README og navigasjonsforbedringer
- Fullstendig redesignet navigasjonen i README.md
- Erstattet `<details>`-tagger med mer tilgjengelig tabellbasert format
- Opprettet alternative layoutalternativer i ny "alternative_layouts"-mappe
- Lagt til eksempler på kortbasert, fanebasert og trekkspillbasert navigasjon
- Oppdatert seksjonen for mappestruktur til å inkludere alle nyeste filer
- Forbedret "Hvordan bruke dette pensumet"-seksjonen med klare anbefalinger
- Oppdatert MCP-spesifikasjonslenker til å peke til riktige URL-er
- Lagt til seksjonen for kontekstingeniørkunst (5.14) i pensumstrukturen

### Oppdateringer i studieveiledning
- Fullstendig revidert studieveiledningen for å tilpasse seg gjeldende mappestruktur
- Lagt til nye seksjoner for MCP-klienter og verktøy, samt populære MCP-servere
- Oppdatert det visuelle pensumkartet for å nøyaktig reflektere alle emner
- Forbedret beskrivelser av avanserte emner for å dekke alle spesialiserte områder
- Oppdatert seksjonen for casestudier til å reflektere faktiske eksempler
- Lagt til denne omfattende endringsloggen

### Felles bidrag (06-CommunityContributions/)
- Lagt til detaljert informasjon om MCP-servere for bildegenerering
- Lagt til omfattende seksjon om bruk av Claude i VSCode
- Lagt til oppsett og bruksanvisning for Cline terminalklient
- Oppdatert MCP-klientseksjonen til å inkludere alle populære klientalternativer
- Forbedret bidragseksempler med mer nøyaktige kodeprøver

### Avanserte emner (05-AdvancedTopics/)
- Organisert alle spesialiserte emnemapper med konsistent navngivning
- Lagt til materialer og eksempler for kontekstingeniørkunst
- Lagt til dokumentasjon for Foundry-agentintegrasjon
- Forbedret dokumentasjon for sikkerhetsintegrasjon med Entra ID

## 11. juni 2025

### Første opprettelse
- Utgitt første versjon av MCP for nybegynnere-pensumet
- Opprettet grunnleggende struktur for alle 10 hovedseksjoner
- Implementert visuelt pensumkart for navigasjon
- Lagt til innledende prøveprosjekter i flere programmeringsspråk

### Komme i gang (03-GettingStarted/)
- Opprettet første serverimplementeringseksempler
- Lagt til veiledning for klientutvikling
- Inkludert integrasjonsinstruksjoner for LLM-klienter
- Lagt til dokumentasjon for integrasjon med VS Code
- Implementert eksempler på Server-Sent Events (SSE)-servere

### Grunnleggende konsepter (01-CoreConcepts/)
- Lagt til detaljert forklaring av klient-server-arkitektur
- Opprettet dokumentasjon om nøkkelkomponenter i protokollen
- Dokumentert meldingsmønstre i MCP

## 23. mai 2025

### Mappestruktur
- Initialisert depotet med grunnleggende mappestruktur
- Opprettet README-filer for hver hovedseksjon
- Satt opp oversettelsesinfrastruktur
- Lagt til bildeaktiva og diagrammer

### Dokumentasjon
- Opprettet innledende README.md med oversikt over pensumet
- Lagt til CODE_OF_CONDUCT.md og SECURITY.md
- Satt opp SUPPORT.md med veiledning for å få hjelp
- Opprettet foreløpig struktur for studieveiledning

## 15. april 2025

### Planlegging og rammeverk
- Innledende planlegging for MCP for nybegynnere-pensumet
- Definerte læringsmål og målgruppe
- Skisserte 10-seksjonsstrukturen for pensumet
- Utviklet konseptuelt rammeverk for eksempler og casestudier
- Opprettet innledende prototypeeksempler for nøkkelkonsepter

---

**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på dets opprinnelige språk bør anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.