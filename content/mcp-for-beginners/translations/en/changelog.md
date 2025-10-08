<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T21:49:30+00:00",
  "source_file": "changelog.md",
  "language_code": "en"
}
-->
# Changelog: MCP for Beginners Curriculum

This document serves as a record of all significant changes made to the Model Context Protocol (MCP) for Beginners curriculum. Changes are documented in reverse chronological order (newest changes first).

## October 6, 2025

### Getting Started Section Expansion – Advanced Server Usage & Simple Authentication

#### Advanced Server Usage (03-GettingStarted/10-advanced)
- **New Chapter Added**: Introduced a detailed guide to advanced MCP server usage, covering both standard and low-level server architectures.
  - **Standard vs. Low-Level Server**: In-depth comparison and code examples in Python and TypeScript for both approaches.
  - **Handler-Based Design**: Explanation of handler-based management for tools/resources/prompts to enable scalable and flexible server implementations.
  - **Practical Patterns**: Real-world scenarios where low-level server patterns are advantageous for advanced features and architecture.

#### Simple Authentication (03-GettingStarted/11-simple-auth)
- **New Chapter Added**: Step-by-step instructions for implementing simple authentication in MCP servers.
  - **Auth Concepts**: Clear explanation of authentication vs. authorization and credential management.
  - **Basic Auth Implementation**: Middleware-based authentication patterns in Python (Starlette) and TypeScript (Express), with code examples.
  - **Progression to Advanced Security**: Guidance on transitioning from simple authentication to OAuth 2.1 and RBAC, with references to advanced security modules.

These additions provide practical, hands-on guidance for building more robust, secure, and flexible MCP server implementations, bridging foundational concepts with advanced production patterns.

## September 29, 2025

### MCP Server Database Integration Labs - Comprehensive Hands-On Learning Path

#### 11-MCPServerHandsOnLabs - New Complete Database Integration Curriculum
- **Complete 13-Lab Learning Path**: Added a comprehensive hands-on curriculum for building production-ready MCP servers with PostgreSQL database integration.
  - **Real-World Implementation**: Zava Retail analytics use case demonstrating enterprise-grade patterns.
  - **Structured Learning Progression**:
    - **Labs 00-03: Foundations** - Introduction, Core Architecture, Security & Multi-Tenancy, Environment Setup.
    - **Labs 04-06: Building the MCP Server** - Database Design & Schema, MCP Server Implementation, Tool Development.  
    - **Labs 07-09: Advanced Features** - Semantic Search Integration, Testing & Debugging, VS Code Integration.
    - **Labs 10-12: Production & Best Practices** - Deployment Strategies, Monitoring & Observability, Best Practices & Optimization.
  - **Enterprise Technologies**: FastMCP framework, PostgreSQL with pgvector, Azure OpenAI embeddings, Azure Container Apps, Application Insights.
  - **Advanced Features**: Row Level Security (RLS), semantic search, multi-tenant data access, vector embeddings, real-time monitoring.

#### Terminology Standardization - Module to Lab Conversion
- **Comprehensive Documentation Update**: Systematically updated all README files in 11-MCPServerHandsOnLabs to use "Lab" terminology instead of "Module."
  - **Section Headers**: Updated "What This Module Covers" to "What This Lab Covers" across all 13 labs.
  - **Content Description**: Changed "This module provides..." to "This lab provides..." throughout documentation.
  - **Learning Objectives**: Updated "By the end of this module..." to "By the end of this lab..."
  - **Navigation Links**: Converted all "Module XX:" references to "Lab XX:" in cross-references and navigation.
  - **Completion Tracking**: Updated "After completing this module..." to "After completing this lab..."
  - **Preserved Technical References**: Maintained Python module references in configuration files (e.g., `"module": "mcp_server.main"`).

#### Study Guide Enhancement (study_guide.md)
- **Visual Curriculum Map**: Added new "11. Database Integration Labs" section with a comprehensive lab structure visualization.
- **Repository Structure**: Updated from ten to eleven main sections with detailed 11-MCPServerHandsOnLabs description.
- **Learning Path Guidance**: Enhanced navigation instructions to cover sections 00-11.
- **Technology Coverage**: Added FastMCP, PostgreSQL, Azure services integration details.
- **Learning Outcomes**: Emphasized production-ready server development, database integration patterns, and enterprise security.

#### Main README Structure Enhancement
- **Lab-Based Terminology**: Updated main README.md in 11-MCPServerHandsOnLabs to consistently use "Lab" structure.
- **Learning Path Organization**: Clear progression from foundational concepts through advanced implementation to production deployment.
- **Real-World Focus**: Emphasis on practical, hands-on learning with enterprise-grade patterns and technologies.

### Documentation Quality & Consistency Improvements
- **Hands-On Learning Emphasis**: Reinforced practical, lab-based approach throughout documentation.
- **Enterprise Patterns Focus**: Highlighted production-ready implementations and enterprise security considerations.
- **Technology Integration**: Comprehensive coverage of modern Azure services and AI integration patterns.
- **Learning Progression**: Clear, structured path from basic concepts to production deployment.

## September 26, 2025

### Case Studies Enhancement - GitHub MCP Registry Integration

#### Case Studies (09-CaseStudy/) - Ecosystem Development Focus
- **README.md**: Major expansion with a comprehensive GitHub MCP Registry case study.
  - **GitHub MCP Registry Case Study**: New detailed case study examining GitHub's MCP Registry launch in September 2025.
    - **Problem Analysis**: Detailed examination of fragmented MCP server discovery and deployment challenges.
    - **Solution Architecture**: GitHub's centralized registry approach with one-click VS Code installation.
    - **Business Impact**: Measurable improvements in developer onboarding and productivity.
    - **Strategic Value**: Focus on modular agent deployment and cross-tool interoperability.
    - **Ecosystem Development**: Positioning as a foundational platform for agentic integration.
  - **Enhanced Case Study Structure**: Updated all seven case studies with consistent formatting and comprehensive descriptions.
    - Azure AI Travel Agents: Multi-agent orchestration emphasis.
    - Azure DevOps Integration: Workflow automation focus.
    - Real-Time Documentation Retrieval: Python console client implementation.
    - Interactive Study Plan Generator: Chainlit conversational web app.
    - In-Editor Documentation: VS Code and GitHub Copilot integration.
    - Azure API Management: Enterprise API integration patterns.
    - GitHub MCP Registry: Ecosystem development and community platform.
  - **Comprehensive Conclusion**: Rewritten conclusion section highlighting seven case studies spanning multiple MCP implementation dimensions.
    - Enterprise Integration, Multi-Agent Orchestration, Developer Productivity.
    - Ecosystem Development, Educational Applications categorization.
    - Enhanced insights into architectural patterns, implementation strategies, and best practices.
    - Emphasis on MCP as a mature, production-ready protocol.

#### Study Guide Updates (study_guide.md)
- **Visual Curriculum Map**: Updated mindmap to include GitHub MCP Registry in the Case Studies section.
- **Case Studies Description**: Enhanced from generic descriptions to detailed breakdown of seven comprehensive case studies.
- **Repository Structure**: Updated section 10 to reflect comprehensive case study coverage with specific implementation details.
- **Changelog Integration**: Added September 26, 2025 entry documenting GitHub MCP Registry addition and case study enhancements.
- **Date Updates**: Updated footer timestamp to reflect the latest revision (September 26, 2025).

### Documentation Quality Improvements
- **Consistency Enhancement**: Standardized case study formatting and structure across all seven examples.
- **Comprehensive Coverage**: Case studies now span enterprise, developer productivity, and ecosystem development scenarios.
- **Strategic Positioning**: Enhanced focus on MCP as a foundational platform for agentic system deployment.
- **Resource Integration**: Updated additional resources to include GitHub MCP Registry link.

## September 15, 2025

### Advanced Topics Expansion - Custom Transports & Context Engineering

#### MCP Custom Transports (05-AdvancedTopics/mcp-transport/) - New Advanced Implementation Guide
- **README.md**: Complete implementation guide for custom MCP transport mechanisms.
  - **Azure Event Grid Transport**: Comprehensive serverless event-driven transport implementation.
    - C#, TypeScript, and Python examples with Azure Functions integration.
    - Event-driven architecture patterns for scalable MCP solutions.
    - Webhook receivers and push-based message handling.
  - **Azure Event Hubs Transport**: High-throughput streaming transport implementation.
    - Real-time streaming capabilities for low-latency scenarios.
    - Partitioning strategies and checkpoint management.
    - Message batching and performance optimization.
  - **Enterprise Integration Patterns**: Production-ready architectural examples.
    - Distributed MCP processing across multiple Azure Functions.
    - Hybrid transport architectures combining multiple transport types.
    - Message durability, reliability, and error handling strategies.
  - **Security & Monitoring**: Azure Key Vault integration and observability patterns.
    - Managed identity authentication and least privilege access.
    - Application Insights telemetry and performance monitoring.
    - Circuit breakers and fault tolerance patterns.
  - **Testing Frameworks**: Comprehensive testing strategies for custom transports.
    - Unit testing with test doubles and mocking frameworks.
    - Integration testing with Azure Test Containers.
    - Performance and load testing considerations.

#### Context Engineering (05-AdvancedTopics/mcp-contextengineering/) - Emerging AI Discipline
- **README.md**: Comprehensive exploration of context engineering as an emerging field.
  - **Core Principles**: Complete context sharing, action decision awareness, and context window management.
  - **MCP Protocol Alignment**: How MCP design addresses context engineering challenges.
    - Context window limitations and progressive loading strategies.
    - Relevance determination and dynamic context retrieval.
    - Multi-modal context handling and security considerations.
  - **Implementation Approaches**: Single-threaded vs. multi-agent architectures.
    - Context chunking and prioritization techniques.
    - Progressive context loading and compression strategies.
    - Layered context approaches and retrieval optimization.
  - **Measurement Framework**: Emerging metrics for context effectiveness evaluation.
    - Input efficiency, performance, quality, and user experience considerations.
    - Experimental approaches to context optimization.
    - Failure analysis and improvement methodologies.

#### Curriculum Navigation Updates (README.md)
- **Enhanced Module Structure**: Updated curriculum table to include new advanced topics.
  - Added Context Engineering (5.14) and Custom Transport (5.15) entries.
  - Consistent formatting and navigation links across all modules.
  - Updated descriptions to reflect current content scope.

### Directory Structure Improvements
- **Naming Standardization**: Renamed "mcp transport" to "mcp-transport" for consistency with other advanced topic folders.
- **Content Organization**: All 05-AdvancedTopics folders now follow a consistent naming pattern (mcp-[topic]).

### Documentation Quality Enhancements
- **MCP Specification Alignment**: All new content references current MCP Specification 2025-06-18.
- **Multi-Language Examples**: Comprehensive code examples in C#, TypeScript, and Python.
- **Enterprise Focus**: Production-ready patterns and Azure cloud integration throughout.
- **Visual Documentation**: Mermaid diagrams for architecture and flow visualization.

## August 18, 2025

### Documentation Comprehensive Update - MCP 2025-06-18 Standards

#### MCP Security Best Practices (02-Security/) - Complete Modernization
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Complete rewrite aligned with MCP Specification 2025-06-18.
  - **Mandatory Requirements**: Added explicit MUST/MUST NOT requirements from the official specification with clear visual indicators.
  - **12 Core Security Practices**: Restructured from a 15-item list to comprehensive security domains.
    - Token Security & Authentication with external identity provider integration.
    - Session Management & Transport Security with cryptographic requirements.
    - AI-Specific Threat Protection with Microsoft Prompt Shields integration.
    - Access Control & Permissions with the principle of least privilege.
    - Content Safety & Monitoring with Azure Content Safety integration.
    - Supply Chain Security with comprehensive component verification.
    - OAuth Security & Confused Deputy Prevention with PKCE implementation.
    - Incident Response & Recovery with automated capabilities.
    - Compliance & Governance with regulatory alignment.
    - Advanced Security Controls with zero trust architecture.
    - Microsoft Security Ecosystem Integration with comprehensive solutions.
    - Continuous Security Evolution with adaptive practices.
  - **Microsoft Security Solutions**: Enhanced integration guidance for Prompt Shields, Azure Content Safety, Entra ID, and GitHub Advanced Security.
  - **Implementation Resources**: Categorized comprehensive resource links by Official MCP Documentation, Microsoft Security Solutions, Security Standards, and Implementation Guides.

#### Advanced Security Controls (02-Security/) - Enterprise Implementation
- **MCP-SECURITY-CONTROLS-2025.md**: Complete overhaul with an enterprise-grade security framework.
  - **9 Comprehensive Security Domains**: Expanded from basic controls to a detailed enterprise framework.
    - Advanced Authentication & Authorization with Microsoft Entra ID integration.
    - Token Security & Anti-Passthrough Controls with comprehensive validation.
    - Session Security Controls with hijacking prevention.
    - AI-Specific Security Controls with prompt injection and tool poisoning prevention.
    - Confused Deputy Attack Prevention with OAuth proxy security.
    - Tool Execution Security with sandboxing and isolation.
    - Supply Chain Security Controls with dependency verification.
    - Monitoring & Detection Controls with SIEM integration.
    - Incident Response & Recovery with automated capabilities.
  - **Implementation Examples**: Added detailed YAML configuration blocks and code examples.
  - **Microsoft Solutions Integration**: Comprehensive coverage of Azure security services, GitHub Advanced Security, and enterprise identity management.
#### Advanced Topics Security (05-AdvancedTopics/mcp-security/) - Production-Ready Implementation
- **README.md**: Complete rewrite for enterprise-level security implementation
  - **Current Specification Alignment**: Updated to MCP Specification 2025-06-18 with mandatory security requirements
  - **Enhanced Authentication**: Integration with Microsoft Entra ID, including detailed examples for .NET and Java Spring Security
  - **AI Security Integration**: Implementation of Microsoft Prompt Shields and Azure Content Safety with detailed Python examples
  - **Advanced Threat Mitigation**: Comprehensive implementation examples for:
    - Preventing Confused Deputy Attacks using PKCE and user consent validation
    - Mitigating Token Passthrough vulnerabilities through audience validation and secure token management
    - Preventing Session Hijacking with cryptographic binding and behavioral analysis
  - **Enterprise Security Integration**: Monitoring with Azure Application Insights, threat detection pipelines, and supply chain security measures
  - **Implementation Checklist**: Clear distinction between mandatory and recommended security controls, highlighting benefits of the Microsoft security ecosystem

### Documentation Quality & Standards Alignment
- **Specification References**: Updated all references to align with MCP Specification 2025-06-18
- **Microsoft Security Ecosystem**: Enhanced guidance for integration across all security documentation
- **Practical Implementation**: Added detailed code examples in .NET, Java, and Python, following enterprise patterns
- **Resource Organization**: Comprehensive categorization of official documentation, security standards, and implementation guides
- **Visual Indicators**: Clear differentiation between mandatory requirements and recommended practices

#### Core Concepts (01-CoreConcepts/) - Complete Modernization
- **Protocol Version Update**: Updated to reference MCP Specification 2025-06-18 with date-based versioning (YYYY-MM-DD format)
- **Architecture Refinement**: Improved descriptions of Hosts, Clients, and Servers to reflect current MCP architecture patterns
  - Hosts: Defined as AI applications managing multiple MCP client connections
  - Clients: Described as protocol connectors maintaining one-to-one server relationships
  - Servers: Enhanced with scenarios for local and remote deployment
- **Primitive Restructuring**: Complete overhaul of server and client primitives
  - Server Primitives: Resources (data sources), Prompts (templates), Tools (executable functions) with detailed explanations and examples
  - Client Primitives: Sampling (LLM completions), Elicitation (user input), Logging (debugging/monitoring)
  - Updated with current discovery (`*/list`), retrieval (`*/get`), and execution (`*/call`) method patterns
- **Protocol Architecture**: Introduced a two-layer architecture model
  - Data Layer: JSON-RPC 2.0 foundation with lifecycle management and primitives
  - Transport Layer: STDIO (local) and Streamable HTTP with SSE (remote) transport mechanisms
- **Security Framework**: Comprehensive security principles, including explicit user consent, data privacy protection, tool execution safety, and transport layer security
- **Communication Patterns**: Updated protocol messages to illustrate initialization, discovery, execution, and notification flows
- **Code Examples**: Refreshed multi-language examples (.NET, Java, Python, JavaScript) to align with current MCP SDK patterns

#### Security (02-Security/) - Comprehensive Security Overhaul  
- **Standards Alignment**: Fully aligned with MCP Specification 2025-06-18 security requirements
- **Authentication Evolution**: Documented transition from custom OAuth servers to external identity provider delegation (Microsoft Entra ID)
- **AI-Specific Threat Analysis**: Expanded coverage of modern AI attack vectors
  - Detailed scenarios for prompt injection attacks with real-world examples
  - Tool poisoning mechanisms and "rug pull" attack patterns
  - Context window poisoning and model confusion attacks
- **Microsoft AI Security Solutions**: Comprehensive coverage of Microsoft security ecosystem
  - AI Prompt Shields with advanced detection, spotlighting, and delimiter techniques
  - Azure Content Safety integration patterns
  - GitHub Advanced Security for supply chain protection
- **Advanced Threat Mitigation**: Detailed security controls for:
  - Session hijacking with MCP-specific attack scenarios and cryptographic session ID requirements
  - Confused deputy problems in MCP proxy scenarios with explicit consent requirements
  - Token passthrough vulnerabilities with mandatory validation controls
- **Supply Chain Security**: Expanded AI supply chain coverage, including foundation models, embedding services, context providers, and third-party APIs
- **Foundation Security**: Enhanced integration with enterprise security patterns, including zero trust architecture and Microsoft security ecosystem
- **Resource Organization**: Categorized comprehensive resource links by type (Official Docs, Standards, Research, Microsoft Solutions, Implementation Guides)

### Documentation Quality Improvements
- **Structured Learning Objectives**: Improved learning objectives with specific, actionable outcomes
- **Cross-References**: Added links between related security and core concept topics
- **Current Information**: Updated all date references and specification links to reflect current standards
- **Implementation Guidance**: Included specific, actionable implementation guidelines throughout both sections

## July 16, 2025

### README and Navigation Improvements
- Completely redesigned the curriculum navigation in README.md
- Replaced `<details>` tags with a more accessible table-based format
- Created alternative layout options in the new "alternative_layouts" folder
- Added examples for card-based, tabbed-style, and accordion-style navigation
- Updated the repository structure section to include all latest files
- Enhanced the "How to Use This Curriculum" section with clear recommendations
- Updated MCP specification links to point to correct URLs
- Added a Context Engineering section (5.14) to the curriculum structure

### Study Guide Updates
- Completely revised the study guide to align with the current repository structure
- Added new sections for MCP Clients and Tools, and Popular MCP Servers
- Updated the Visual Curriculum Map to accurately reflect all topics
- Enhanced descriptions of Advanced Topics to cover all specialized areas
- Updated the Case Studies section to include real-world examples
- Added this comprehensive changelog

### Community Contributions (06-CommunityContributions/)
- Added detailed information about MCP servers for image generation
- Included a comprehensive section on using Claude in VSCode
- Added setup and usage instructions for the Cline terminal client
- Updated the MCP client section to include all popular client options
- Enhanced contribution examples with more accurate code samples

### Advanced Topics (05-AdvancedTopics/)
- Organized all specialized topic folders with consistent naming conventions
- Added context engineering materials and examples
- Included documentation for Foundry agent integration
- Enhanced Entra ID security integration documentation

## June 11, 2025

### Initial Creation
- Released the first version of the MCP for Beginners curriculum
- Created the basic structure for all 10 main sections
- Implemented a Visual Curriculum Map for navigation
- Added initial sample projects in multiple programming languages

### Getting Started (03-GettingStarted/)
- Created initial server implementation examples
- Added guidance for client development
- Included instructions for LLM client integration
- Added documentation for VS Code integration
- Implemented Server-Sent Events (SSE) server examples

### Core Concepts (01-CoreConcepts/)
- Added detailed explanations of client-server architecture
- Created documentation on key protocol components
- Documented messaging patterns in MCP

## May 23, 2025

### Repository Structure
- Initialized the repository with a basic folder structure
- Created README files for each major section
- Set up translation infrastructure
- Added image assets and diagrams

### Documentation
- Created the initial README.md with a curriculum overview
- Added CODE_OF_CONDUCT.md and SECURITY.md
- Set up SUPPORT.md with guidance for getting help
- Created a preliminary study guide structure

## April 15, 2025

### Planning and Framework
- Initial planning for the MCP for Beginners curriculum
- Defined learning objectives and target audience
- Outlined the 10-section structure of the curriculum
- Developed a conceptual framework for examples and case studies
- Created initial prototype examples for key concepts

---

**Disclaimer**:  
This document has been translated using the AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we aim for accuracy, please note that automated translations may contain errors or inaccuracies. The original document in its native language should be regarded as the authoritative source. For critical information, professional human translation is recommended. We are not responsible for any misunderstandings or misinterpretations resulting from the use of this translation.