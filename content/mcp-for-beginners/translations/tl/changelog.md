<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:40:22+00:00",
  "source_file": "changelog.md",
  "language_code": "tl"
}
-->
# Talaan ng Pagbabago: Kurikulum ng MCP para sa Mga Baguhan

Ang dokumentong ito ay nagsisilbing talaan ng lahat ng mahahalagang pagbabago na ginawa sa kurikulum ng Model Context Protocol (MCP) para sa Mga Baguhan. Ang mga pagbabago ay nakatala sa reverse chronological order (pinakabagong pagbabago muna).

## Oktubre 6, 2025

### Pagpapalawak ng Seksyon ng Pagsisimula – Advanced na Paggamit ng Server at Simpleng Authentication

#### Advanced na Paggamit ng Server (03-GettingStarted/10-advanced)
- **Bagong Kabanata Idinagdag**: Nagpakilala ng komprehensibong gabay sa advanced na paggamit ng MCP server, na sumasaklaw sa parehong regular at low-level na arkitektura ng server.
  - **Regular vs. Low-Level Server**: Detalyadong paghahambing at mga halimbawa ng code sa Python at TypeScript para sa parehong pamamaraan.
  - **Handler-Based Design**: Paliwanag sa handler-based na pamamahala ng tool/resource/prompt para sa scalable at flexible na implementasyon ng server.
  - **Praktikal na Pattern**: Mga senaryo sa totoong mundo kung saan kapaki-pakinabang ang low-level server patterns para sa advanced na mga tampok at arkitektura.

#### Simpleng Authentication (03-GettingStarted/11-simple-auth)
- **Bagong Kabanata Idinagdag**: Step-by-step na gabay sa pag-implement ng simpleng authentication sa MCP servers.
  - **Mga Konsepto ng Auth**: Malinaw na paliwanag sa authentication vs. authorization, at pamamahala ng mga kredensyal.
  - **Pagpapatupad ng Basic Auth**: Middleware-based na authentication patterns sa Python (Starlette) at TypeScript (Express), kasama ang mga halimbawa ng code.
  - **Pag-unlad sa Advanced na Seguridad**: Gabay sa pagsisimula sa simpleng auth at pag-usad sa OAuth 2.1 at RBAC, kasama ang mga reference sa advanced na security modules.

Ang mga karagdagang ito ay nagbibigay ng praktikal, hands-on na gabay para sa pagbuo ng mas matatag, secure, at flexible na implementasyon ng MCP server, na nag-uugnay sa mga pundasyong konsepto sa mga advanced na production patterns.

## Setyembre 29, 2025

### MCP Server Database Integration Labs - Komprehensibong Hands-On Learning Path

#### 11-MCPServerHandsOnLabs - Bagong Kumpletong Kurikulum sa Database Integration
- **Kumpletong 13-Lab Learning Path**: Idinagdag ang komprehensibong hands-on na kurikulum para sa pagbuo ng production-ready MCP servers na may PostgreSQL database integration.
  - **Implementasyon sa Totoong Mundo**: Zava Retail analytics use case na nagpapakita ng enterprise-grade patterns.
  - **Structured Learning Progression**:
    - **Labs 00-03: Mga Pundasyon** - Panimula, Core Architecture, Security & Multi-Tenancy, Environment Setup.
    - **Labs 04-06: Pagbuo ng MCP Server** - Database Design & Schema, MCP Server Implementation, Tool Development.
    - **Labs 07-09: Mga Advanced na Tampok** - Semantic Search Integration, Testing & Debugging, VS Code Integration.
    - **Labs 10-12: Production & Best Practices** - Deployment Strategies, Monitoring & Observability, Best Practices & Optimization.
  - **Enterprise Technologies**: FastMCP framework, PostgreSQL na may pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Mga Advanced na Tampok**: Row Level Security (RLS), semantic search, multi-tenant data access, vector embeddings, real-time monitoring.

#### Standardisasyon ng Terminolohiya - Pag-convert ng Module sa Lab
- **Komprehensibong Update sa Dokumentasyon**: Sistematikong in-update ang lahat ng README files sa 11-MCPServerHandsOnLabs upang gamitin ang terminolohiyang "Lab" sa halip na "Module."
  - **Mga Header ng Seksyon**: In-update ang "What This Module Covers" sa "What This Lab Covers" sa lahat ng 13 labs.
  - **Deskripsyon ng Nilalaman**: Binago ang "This module provides..." sa "This lab provides..." sa buong dokumentasyon.
  - **Mga Layunin sa Pag-aaral**: In-update ang "By the end of this module..." sa "By the end of this lab..."
  - **Mga Link sa Navigation**: Kinonvert ang lahat ng "Module XX:" references sa "Lab XX:" sa mga cross-references at navigation.
  - **Pagsubaybay sa Pagkumpleto**: In-update ang "After completing this module..." sa "After completing this lab..."
  - **Pinanatili ang Mga Teknikal na Reference**: Pinanatili ang mga Python module references sa configuration files (hal., `"module": "mcp_server.main"`).

#### Pagpapahusay ng Study Guide (study_guide.md)
- **Visual Curriculum Map**: Idinagdag ang bagong "11. Database Integration Labs" na seksyon na may komprehensibong visualization ng lab structure.
- **Repository Structure**: In-update mula sa sampu hanggang labing-isang pangunahing seksyon na may detalyadong deskripsyon ng 11-MCPServerHandsOnLabs.
- **Gabay sa Learning Path**: Pinahusay ang mga navigation instructions upang masakop ang mga seksyon 00-11.
- **Coverage ng Teknolohiya**: Idinagdag ang FastMCP, PostgreSQL, Azure services integration details.
- **Mga Layunin sa Pag-aaral**: Binibigyang-diin ang production-ready server development, database integration patterns, at enterprise security.

#### Pagpapahusay ng Main README Structure
- **Terminolohiyang Batay sa Lab**: In-update ang main README.md sa 11-MCPServerHandsOnLabs upang palaging gamitin ang "Lab" structure.
- **Organisasyon ng Learning Path**: Malinaw na progression mula sa mga pundasyong konsepto hanggang sa advanced na implementasyon at production deployment.
- **Totoong Mundo na Pokus**: Binibigyang-diin ang praktikal, hands-on na pag-aaral gamit ang enterprise-grade patterns at technologies.

### Mga Pagpapabuti sa Kalidad at Konsistensya ng Dokumentasyon
- **Hands-On Learning Emphasis**: Pinalakas ang praktikal, lab-based na approach sa buong dokumentasyon.
- **Enterprise Patterns Focus**: Binibigyang-diin ang production-ready implementations at enterprise security considerations.
- **Integration ng Teknolohiya**: Komprehensibong coverage ng modernong Azure services at AI integration patterns.
- **Learning Progression**: Malinaw, structured na path mula sa mga basic concepts hanggang sa production deployment.

## Setyembre 26, 2025

### Pagpapahusay ng Case Studies - GitHub MCP Registry Integration

#### Case Studies (09-CaseStudy/) - Pokus sa Pagpapaunlad ng Ecosystem
- **README.md**: Malaking pagpapalawak na may komprehensibong GitHub MCP Registry case study.
  - **GitHub MCP Registry Case Study**: Bagong komprehensibong case study na sinusuri ang paglulunsad ng GitHub MCP Registry noong Setyembre 2025.
    - **Pagsusuri ng Problema**: Detalyadong pagsusuri sa fragmented MCP server discovery at deployment challenges.
    - **Solution Architecture**: GitHub's centralized registry approach na may one-click VS Code installation.
    - **Epekto sa Negosyo**: Nasusukat na mga pagpapabuti sa developer onboarding at productivity.
    - **Strategic Value**: Pokus sa modular agent deployment at cross-tool interoperability.
    - **Pagpapaunlad ng Ecosystem**: Pagpoposisyon bilang foundational platform para sa agentic integration.
  - **Pinahusay na Case Study Structure**: In-update ang lahat ng pitong case studies na may konsistenteng formatting at komprehensibong deskripsyon.
    - Azure AI Travel Agents: Pokus sa multi-agent orchestration.
    - Azure DevOps Integration: Pokus sa workflow automation.
    - Real-Time Documentation Retrieval: Implementasyon ng Python console client.
    - Interactive Study Plan Generator: Chainlit conversational web app.
    - In-Editor Documentation: VS Code at GitHub Copilot integration.
    - Azure API Management: Enterprise API integration patterns.
    - GitHub MCP Registry: Pagpapaunlad ng ecosystem at community platform.
  - **Komprehensibong Konklusyon**: Muling isinulat ang konklusyon na seksyon na binibigyang-diin ang pitong case studies na sumasaklaw sa iba't ibang dimensyon ng MCP implementation.
    - Enterprise Integration, Multi-Agent Orchestration, Developer Productivity.
    - Ecosystem Development, Educational Applications categorization.
    - Pinahusay na insights sa architectural patterns, implementation strategies, at best practices.
    - Binibigyang-diin ang MCP bilang mature, production-ready protocol.

#### Mga Update sa Study Guide (study_guide.md)
- **Visual Curriculum Map**: In-update ang mindmap upang isama ang GitHub MCP Registry sa Case Studies section.
- **Deskripsyon ng Case Studies**: Pinahusay mula sa generic na deskripsyon patungo sa detalyadong breakdown ng pitong komprehensibong case studies.
- **Repository Structure**: In-update ang seksyon 10 upang ipakita ang komprehensibong case study coverage na may mga partikular na detalye ng implementasyon.
- **Changelog Integration**: Idinagdag ang Setyembre 26, 2025 entry na nagdodokumento ng GitHub MCP Registry addition at case study enhancements.
- **Mga Update sa Petsa**: In-update ang footer timestamp upang ipakita ang pinakabagong rebisyon (Setyembre 26, 2025).

### Mga Pagpapabuti sa Kalidad ng Dokumentasyon
- **Pagpapahusay ng Konsistensya**: Standardisado ang formatting at structure ng case study sa lahat ng pitong halimbawa.
- **Komprehensibong Coverage**: Ang mga case studies ngayon ay sumasaklaw sa enterprise, developer productivity, at ecosystem development scenarios.
- **Strategic Positioning**: Pinahusay na pokus sa MCP bilang foundational platform para sa agentic system deployment.
- **Integration ng Resource**: In-update ang mga karagdagang resources upang isama ang GitHub MCP Registry link.

## Setyembre 15, 2025

### Pagpapalawak ng Advanced Topics - Custom Transports at Context Engineering

#### MCP Custom Transports (05-AdvancedTopics/mcp-transport/) - Bagong Gabay sa Advanced na Implementasyon
- **README.md**: Kumpletong gabay sa implementasyon para sa custom na MCP transport mechanisms.
  - **Azure Event Grid Transport**: Komprehensibong serverless event-driven transport implementation.
    - Mga halimbawa sa C#, TypeScript, at Python na may Azure Functions integration.
    - Event-driven architecture patterns para sa scalable MCP solutions.
    - Webhook receivers at push-based message handling.
  - **Azure Event Hubs Transport**: High-throughput streaming transport implementation.
    - Real-time streaming capabilities para sa low-latency scenarios.
    - Partitioning strategies at checkpoint management.
    - Message batching at performance optimization.
  - **Enterprise Integration Patterns**: Mga production-ready na halimbawa ng arkitektura.
    - Distributed MCP processing sa maraming Azure Functions.
    - Hybrid transport architectures na pinagsasama ang iba't ibang uri ng transport.
    - Mga estratehiya sa message durability, reliability, at error handling.
  - **Seguridad at Monitoring**: Azure Key Vault integration at observability patterns.
    - Managed identity authentication at least privilege access.
    - Application Insights telemetry at performance monitoring.
    - Circuit breakers at fault tolerance patterns.
  - **Testing Frameworks**: Komprehensibong estratehiya sa testing para sa custom transports.
    - Unit testing gamit ang test doubles at mocking frameworks.
    - Integration testing gamit ang Azure Test Containers.
    - Mga konsiderasyon sa performance at load testing.

#### Context Engineering (05-AdvancedTopics/mcp-contextengineering/) - Umuusbong na Disiplina sa AI
- **README.md**: Komprehensibong eksplorasyon ng context engineering bilang umuusbong na larangan.
  - **Mga Pangunahing Prinsipyo**: Kumpletong context sharing, action decision awareness, at context window management.
  - **Pagkakahanay sa MCP Protocol**: Paano tinutugunan ng disenyo ng MCP ang mga hamon sa context engineering.
    - Mga limitasyon ng context window at progressive loading strategies.
    - Relevance determination at dynamic context retrieval.
    - Multi-modal context handling at mga konsiderasyon sa seguridad.
  - **Mga Pamamaraan ng Implementasyon**: Single-threaded vs. multi-agent architectures.
    - Context chunking at prioritization techniques.
    - Progressive context loading at compression strategies.
    - Layered context approaches at retrieval optimization.
  - **Measurement Framework**: Umuusbong na metrics para sa pagsusuri ng context effectiveness.
    - Input efficiency, performance, quality, at user experience considerations.
    - Mga experimental na pamamaraan sa context optimization.
    - Failure analysis at improvement methodologies.

#### Mga Update sa Curriculum Navigation (README.md)
- **Pinahusay na Module Structure**: In-update ang curriculum table upang isama ang mga bagong advanced topics.
  - Idinagdag ang Context Engineering (5.14) at Custom Transport (5.15) entries.
  - Konsistenteng formatting at navigation links sa lahat ng modules.
  - In-update ang mga deskripsyon upang ipakita ang kasalukuyang saklaw ng nilalaman.

### Mga Pagpapabuti sa Directory Structure
- **Standardisasyon ng Pangalan**: Pinalitan ang "mcp transport" sa "mcp-transport" para sa konsistensya sa iba pang advanced topic folders.
- **Organisasyon ng Nilalaman**: Ang lahat ng 05-AdvancedTopics folders ngayon ay sumusunod sa konsistenteng naming pattern (mcp-[topic]).

### Mga Pagpapahusay sa Kalidad ng Dokumentasyon
- **Pagkakahanay sa MCP Specification**: Ang lahat ng bagong nilalaman ay tumutukoy sa kasalukuyang MCP Specification 2025-06-18.
- **Mga Halimbawa sa Multi-Language**: Komprehensibong mga halimbawa ng code sa C#, TypeScript, at Python.
- **Pokus sa Enterprise**: Mga production-ready patterns at Azure cloud integration sa kabuuan.
- **Visual Documentation**: Mermaid diagrams para sa visualization ng arkitektura at daloy.

## Agosto 18, 2025

### Komprehensibong Update sa Dokumentasyon - MCP 2025-06-18 Standards

#### MCP Security Best Practices (02-Security/) - Kumpletong Modernisasyon
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Kumpletong rewrite na naka-align sa MCP Specification 2025-06-18.
  - **Mandatory Requirements**: Idinagdag ang mga explicit na MUST/MUST NOT requirements mula sa opisyal na specification na may malinaw na visual indicators.
  - **12 Core Security Practices**: Muling inayos mula sa 15-item list patungo sa komprehensibong security domains.
    - Token Security & Authentication na may integration ng external identity provider.
    - Session Management & Transport Security na may cryptographic requirements.
    - AI-Specific Threat Protection na may Microsoft Prompt Shields integration.
    - Access Control & Permissions na may prinsipyo ng least privilege.
    - Content Safety & Monitoring na may Azure Content Safety integration.
    - Supply Chain Security na may komprehensibong component verification.
    - OAuth Security & Confused Deputy Prevention na may PKCE implementation.
    - Incident Response & Recovery na may automated capabilities.
    - Compliance & Governance na may regulatory alignment.
    - Advanced Security Controls na may zero trust architecture.
    - Microsoft Security Ecosystem Integration na may komprehensibong solusyon.
    - Continuous Security Evolution na may adaptive practices.
  - **Microsoft Security Solutions**: Pinahusay na integration guidance para sa Prompt Shields, Azure Content Safety, Entra ID, at GitHub Advanced Security.
  - **Implementation Resources**: Kategoryadong komprehensibong resource links ayon sa Official MCP Documentation, Microsoft Security Solutions, Security Standards, at Implementation Guides.

#### Advanced Security Controls (02-Security/) - Implementasyon sa Enterprise
- **MCP-SECURITY-CONTROLS-2025.md**: Kumpletong overhaul na may enterprise-grade security framework.
  - **9 Comprehensive Security Domains**: Pinalawak mula sa basic controls patungo sa detalyadong enterprise framework.
    - Advanced Authentication & Authorization na may Microsoft Entra ID integration.
    - Token Security & Anti-Passthrough Controls na may komprehensibong validation.
    - Session Security Controls na may hijacking prevention.
    - AI-Specific Security Controls na may prompt injection at tool poisoning prevention.
    - Confused Deputy Attack Prevention na may OAuth proxy security.
    - Tool Execution Security na may sandboxing at isolation.
    - Supply Chain Security Controls na may dependency verification.
    - Monitoring & Detection Controls na may SIEM integration.
    - Incident Response & Recovery na may automated capabilities.
  - **Mga Halimbawa ng Implementasyon**: Idinagdag ang detalyadong YAML configuration blocks at mga halimbawa ng code.
  - **Microsoft Solutions Integration**: Komprehensibong coverage ng Azure security services, GitHub Advanced Security, at enterprise identity management.
#### Mga Advanced na Paksa sa Seguridad (05-AdvancedTopics/mcp-security/) - Handa na para sa Produksyon
- **README.md**: Ganap na muling isinulat para sa enterprise security implementation
  - **Pagkakahanay sa Kasalukuyang Espesipikasyon**: Na-update sa MCP Specification 2025-06-18 na may mga mandatoryong kinakailangan sa seguridad
  - **Pinahusay na Pagpapatunay**: Microsoft Entra ID integration na may detalyadong mga halimbawa sa .NET at Java Spring Security
  - **AI Security Integration**: Microsoft Prompt Shields at Azure Content Safety implementation na may detalyadong mga halimbawa sa Python
  - **Advanced Threat Mitigation**: Komprehensibong mga halimbawa ng implementasyon para sa
    - Pag-iwas sa Confused Deputy Attack gamit ang PKCE at user consent validation
    - Pag-iwas sa Token Passthrough gamit ang audience validation at secure token management
    - Pag-iwas sa Session Hijacking gamit ang cryptographic binding at behavioral analysis
  - **Enterprise Security Integration**: Azure Application Insights monitoring, threat detection pipelines, at seguridad sa supply chain
  - **Implementation Checklist**: Malinaw na pagkakaiba ng mandatoryo vs. rekomendadong mga kontrol sa seguridad na may mga benepisyo ng Microsoft security ecosystem

### Kalidad ng Dokumentasyon at Pagkakahanay sa Pamantayan
- **Mga Sanggunian sa Espesipikasyon**: Na-update ang lahat ng sanggunian sa kasalukuyang MCP Specification 2025-06-18
- **Microsoft Security Ecosystem**: Pinahusay na gabay sa integrasyon sa buong dokumentasyon ng seguridad
- **Praktikal na Implementasyon**: Idinagdag ang detalyadong mga halimbawa ng code sa .NET, Java, at Python na may mga enterprise pattern
- **Organisasyon ng mga Resource**: Komprehensibong pagkakategorya ng opisyal na dokumentasyon, mga pamantayan sa seguridad, at mga gabay sa implementasyon
- **Visual Indicators**: Malinaw na pagmamarka ng mga mandatoryong kinakailangan vs. mga rekomendadong kasanayan

#### Mga Pangunahing Konsepto (01-CoreConcepts/) - Ganap na Modernisasyon
- **Pag-update ng Bersyon ng Protocol**: Na-update upang sumangguni sa kasalukuyang MCP Specification 2025-06-18 na may format na batay sa petsa (YYYY-MM-DD)
- **Pagpapabuti ng Arkitektura**: Pinahusay na mga paglalarawan ng Hosts, Clients, at Servers upang ipakita ang kasalukuyang mga pattern ng arkitektura ng MCP
  - Ang mga Hosts ay malinaw na tinukoy bilang mga AI application na nagkokonekta sa maraming MCP client
  - Ang mga Clients ay inilarawan bilang mga protocol connector na nagpapanatili ng one-to-one na relasyon sa server
  - Ang mga Servers ay pinahusay na may mga lokal vs. remote na deployment scenario
- **Pag-aayos ng Primitibo**: Ganap na pagbabago ng mga server at client primitives
  - Server Primitives: Resources (mga pinagmulan ng data), Prompts (mga template), Tools (mga executable function) na may detalyadong paliwanag at mga halimbawa
  - Client Primitives: Sampling (LLM completions), Elicitation (user input), Logging (debugging/monitoring)
  - Na-update gamit ang kasalukuyang mga pattern ng discovery (`*/list`), retrieval (`*/get`), at execution (`*/call`) na mga pamamaraan
- **Arkitektura ng Protocol**: Ipinakilala ang two-layer architecture model
  - Data Layer: JSON-RPC 2.0 foundation na may lifecycle management at primitives
  - Transport Layer: STDIO (lokal) at Streamable HTTP na may SSE (remote) na mga mekanismo ng transportasyon
- **Seguridad na Framework**: Komprehensibong mga prinsipyo ng seguridad kabilang ang tahasang pahintulot ng user, proteksyon sa privacy ng data, kaligtasan sa pag-execute ng tool, at seguridad sa transport layer
- **Mga Pattern ng Komunikasyon**: Na-update ang mga protocol message upang ipakita ang initialization, discovery, execution, at notification flows
- **Mga Halimbawa ng Code**: Na-refresh ang mga halimbawa sa iba't ibang wika (.NET, Java, Python, JavaScript) upang ipakita ang kasalukuyang mga pattern ng MCP SDK

#### Seguridad (02-Security/) - Komprehensibong Pagbabago sa Seguridad  
- **Pagkakahanay sa Pamantayan**: Ganap na pagkakahanay sa mga kinakailangan sa seguridad ng MCP Specification 2025-06-18
- **Ebolusyon ng Pagpapatunay**: Na-dokumento ang ebolusyon mula sa custom OAuth servers patungo sa external identity provider delegation (Microsoft Entra ID)
- **AI-Specific Threat Analysis**: Pinahusay na saklaw ng mga modernong AI attack vectors
  - Detalyadong mga senaryo ng prompt injection attack na may mga halimbawa sa totoong mundo
  - Mga mekanismo ng tool poisoning at mga pattern ng "rug pull" attack
  - Context window poisoning at model confusion attacks
- **Microsoft AI Security Solutions**: Komprehensibong saklaw ng Microsoft security ecosystem
  - AI Prompt Shields na may advanced detection, spotlighting, at delimiter techniques
  - Azure Content Safety integration patterns
  - GitHub Advanced Security para sa proteksyon ng supply chain
- **Advanced Threat Mitigation**: Detalyadong mga kontrol sa seguridad para sa
  - Session hijacking na may mga MCP-specific attack scenario at mga kinakailangan sa cryptographic session ID
  - Mga problema sa Confused Deputy sa mga MCP proxy scenario na may mga kinakailangan sa tahasang pahintulot
  - Mga kahinaan sa Token Passthrough na may mga mandatoryong kontrol sa validation
- **Seguridad ng Supply Chain**: Pinalawak na saklaw ng AI supply chain kabilang ang mga foundation model, embedding services, context providers, at third-party APIs
- **Seguridad ng Pundasyon**: Pinahusay na integrasyon sa mga enterprise security pattern kabilang ang zero trust architecture at Microsoft security ecosystem
- **Organisasyon ng Resource**: Kinategorya ang komprehensibong mga link ng resource ayon sa uri (Opisyal na Dokumento, Pamantayan, Pananaliksik, Solusyon ng Microsoft, Mga Gabay sa Implementasyon)

### Mga Pagpapabuti sa Kalidad ng Dokumentasyon
- **Mga Nakabalangkas na Layunin ng Pag-aaral**: Pinahusay na mga layunin ng pag-aaral na may tiyak at maaksiyong mga resulta
- **Mga Cross-References**: Idinagdag ang mga link sa pagitan ng mga kaugnay na paksa ng seguridad at pangunahing konsepto
- **Kasalukuyang Impormasyon**: Na-update ang lahat ng mga sanggunian sa petsa at mga link sa espesipikasyon sa kasalukuyang mga pamantayan
- **Gabay sa Implementasyon**: Idinagdag ang tiyak at maaksiyong mga gabay sa implementasyon sa buong seksyon

## Hulyo 16, 2025

### README at Mga Pagpapabuti sa Navigation
- Ganap na muling idinisenyo ang navigation ng kurikulum sa README.md
- Pinalitan ang mga `<details>` na tag ng mas accessible na format na batay sa talahanayan
- Lumikha ng mga alternatibong opsyon sa layout sa bagong folder na "alternative_layouts"
- Idinagdag ang mga halimbawa ng navigation na batay sa card, tabbed-style, at accordion-style
- Na-update ang seksyon ng repository structure upang isama ang lahat ng pinakabagong mga file
- Pinahusay ang seksyong "Paano Gamitin ang Kurikulum na Ito" na may malinaw na mga rekomendasyon
- Na-update ang mga link ng MCP specification upang ituro sa tamang mga URL
- Idinagdag ang seksyon ng Context Engineering (5.14) sa istruktura ng kurikulum

### Mga Update sa Study Guide
- Ganap na binago ang study guide upang maiparehas sa kasalukuyang istruktura ng repository
- Idinagdag ang mga bagong seksyon para sa MCP Clients at Tools, at Popular MCP Servers
- Na-update ang Visual Curriculum Map upang tumpak na ipakita ang lahat ng mga paksa
- Pinahusay ang mga paglalarawan ng Advanced Topics upang masaklaw ang lahat ng mga espesyal na lugar
- Na-update ang seksyon ng Case Studies upang ipakita ang mga aktwal na halimbawa
- Idinagdag ang komprehensibong changelog na ito

### Mga Ambag ng Komunidad (06-CommunityContributions/)
- Idinagdag ang detalyadong impormasyon tungkol sa mga MCP server para sa image generation
- Idinagdag ang komprehensibong seksyon sa paggamit ng Claude sa VSCode
- Idinagdag ang mga tagubilin sa pag-set up at paggamit ng Cline terminal client
- Na-update ang seksyon ng MCP client upang isama ang lahat ng mga popular na opsyon sa client
- Pinahusay ang mga halimbawa ng kontribusyon na may mas tumpak na mga sample ng code

### Mga Advanced na Paksa (05-AdvancedTopics/)
- Inorganisa ang lahat ng mga folder ng espesyal na paksa na may pare-parehong pangalan
- Idinagdag ang mga materyales at halimbawa ng context engineering
- Idinagdag ang dokumentasyon ng Foundry agent integration
- Pinahusay ang dokumentasyon ng Entra ID security integration

## Hunyo 11, 2025

### Unang Paglikha
- Inilabas ang unang bersyon ng kurikulum ng MCP para sa mga Baguhan
- Lumikha ng pangunahing istruktura para sa lahat ng 10 pangunahing seksyon
- Nagpatupad ng Visual Curriculum Map para sa navigation
- Idinagdag ang mga paunang sample na proyekto sa iba't ibang programming language

### Pagsisimula (03-GettingStarted/)
- Lumikha ng mga unang halimbawa ng implementasyon ng server
- Idinagdag ang gabay sa pag-develop ng client
- Isinama ang mga tagubilin sa integrasyon ng LLM client
- Idinagdag ang dokumentasyon ng integrasyon sa VS Code
- Nagpatupad ng mga halimbawa ng Server-Sent Events (SSE) server

### Mga Pangunahing Konsepto (01-CoreConcepts/)
- Idinagdag ang detalyadong paliwanag ng client-server architecture
- Lumikha ng dokumentasyon sa mga pangunahing bahagi ng protocol
- Na-dokumento ang mga pattern ng messaging sa MCP

## Mayo 23, 2025

### Istruktura ng Repository
- Inisyalisa ang repository na may pangunahing istruktura ng folder
- Lumikha ng mga README file para sa bawat pangunahing seksyon
- Nag-set up ng translation infrastructure
- Idinagdag ang mga asset ng imahe at diagram

### Dokumentasyon
- Lumikha ng paunang README.md na may overview ng kurikulum
- Idinagdag ang CODE_OF_CONDUCT.md at SECURITY.md
- Nag-set up ng SUPPORT.md na may gabay para sa pagkuha ng tulong
- Lumikha ng paunang istruktura ng study guide

## Abril 15, 2025

### Pagpaplano at Framework
- Paunang pagpaplano para sa kurikulum ng MCP para sa mga Baguhan
- Tinukoy ang mga layunin ng pag-aaral at target na audience
- In-outline ang 10-seksyon na istruktura ng kurikulum
- Nag-develop ng conceptual framework para sa mga halimbawa at case studies
- Lumikha ng paunang prototype na mga halimbawa para sa mga pangunahing konsepto

---

**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Bagamat sinisikap naming maging tumpak, pakatandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa kanyang katutubong wika ang dapat ituring na opisyal na sanggunian. Para sa mahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na dulot ng paggamit ng pagsasaling ito.