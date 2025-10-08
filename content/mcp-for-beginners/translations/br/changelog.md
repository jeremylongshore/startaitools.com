<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T22:53:15+00:00",
  "source_file": "changelog.md",
  "language_code": "br"
}
-->
# Registro de Alterações: Currículo MCP para Iniciantes

Este documento serve como registro de todas as mudanças significativas feitas no currículo do Protocolo de Contexto de Modelo (MCP) para Iniciantes. As alterações estão documentadas em ordem cronológica inversa (alterações mais recentes primeiro).

## 6 de outubro de 2025

### Expansão da Seção Introdução – Uso Avançado de Servidores & Autenticação Simples

#### Uso Avançado de Servidores (03-GettingStarted/10-advanced)
- **Novo Capítulo Adicionado**: Introduzido um guia abrangente sobre o uso avançado de servidores MCP, cobrindo arquiteturas de servidores regulares e de baixo nível.
  - **Servidor Regular vs. de Baixo Nível**: Comparação detalhada e exemplos de código em Python e TypeScript para ambas as abordagens.
  - **Design Baseado em Handlers**: Explicação sobre gerenciamento de ferramentas/recursos/prompts baseado em handlers para implementações de servidores escaláveis e flexíveis.
  - **Padrões Práticos**: Cenários do mundo real onde padrões de servidores de baixo nível são benéficos para recursos avançados e arquitetura.

#### Autenticação Simples (03-GettingStarted/11-simple-auth)
- **Novo Capítulo Adicionado**: Guia passo a passo para implementar autenticação simples em servidores MCP.
  - **Conceitos de Autenticação**: Explicação clara sobre autenticação vs. autorização e gerenciamento de credenciais.
  - **Implementação de Autenticação Básica**: Padrões de autenticação baseados em middleware em Python (Starlette) e TypeScript (Express), com exemplos de código.
  - **Progressão para Segurança Avançada**: Orientação sobre como começar com autenticação simples e avançar para OAuth 2.1 e RBAC, com referências a módulos de segurança avançados.

Essas adições fornecem orientações práticas e detalhadas para construir implementações de servidores MCP mais robustas, seguras e flexíveis, conectando conceitos fundamentais a padrões avançados de produção.

## 29 de setembro de 2025

### Laboratórios de Integração de Banco de Dados do Servidor MCP - Caminho de Aprendizado Prático Abrangente

#### 11-MCPServerHandsOnLabs - Novo Currículo Completo de Integração de Banco de Dados
- **Caminho de Aprendizado com 13 Laboratórios**: Adicionado um currículo prático abrangente para construir servidores MCP prontos para produção com integração ao banco de dados PostgreSQL.
  - **Implementação do Mundo Real**: Caso de uso de análise de varejo da Zava demonstrando padrões de nível empresarial.
  - **Progressão Estruturada de Aprendizado**:
    - **Laboratórios 00-03: Fundamentos** - Introdução, Arquitetura Central, Segurança & Multi-Tenancy, Configuração do Ambiente.
    - **Laboratórios 04-06: Construindo o Servidor MCP** - Design & Esquema do Banco de Dados, Implementação do Servidor MCP, Desenvolvimento de Ferramentas.
    - **Laboratórios 07-09: Recursos Avançados** - Integração de Busca Semântica, Testes & Depuração, Integração com VS Code.
    - **Laboratórios 10-12: Produção & Melhores Práticas** - Estratégias de Implantação, Monitoramento & Observabilidade, Melhores Práticas & Otimização.
  - **Tecnologias Empresariais**: Framework FastMCP, PostgreSQL com pgvector, embeddings do Azure OpenAI, Azure Container Apps, Application Insights.
  - **Recursos Avançados**: Segurança em Nível de Linha (RLS), busca semântica, acesso a dados multi-tenant, embeddings vetoriais, monitoramento em tempo real.

#### Padronização de Terminologia - Conversão de Módulo para Laboratório
- **Atualização Abrangente da Documentação**: Atualizados sistematicamente todos os arquivos README em 11-MCPServerHandsOnLabs para usar a terminologia "Laboratório" em vez de "Módulo".
  - **Cabeçalhos de Seção**: Atualizado "O que este módulo cobre" para "O que este laboratório cobre" em todos os 13 laboratórios.
  - **Descrição do Conteúdo**: Alterado "Este módulo fornece..." para "Este laboratório fornece..." em toda a documentação.
  - **Objetivos de Aprendizado**: Atualizado "Ao final deste módulo..." para "Ao final deste laboratório...".
  - **Links de Navegação**: Convertidas todas as referências "Módulo XX:" para "Laboratório XX:" em referências cruzadas e navegação.
  - **Rastreamento de Conclusão**: Atualizado "Após concluir este módulo..." para "Após concluir este laboratório...".
  - **Referências Técnicas Preservadas**: Mantidas referências a módulos Python em arquivos de configuração (por exemplo, `"module": "mcp_server.main"`).

#### Melhoria no Guia de Estudos (study_guide.md)
- **Mapa Visual do Currículo**: Adicionada nova seção "11. Laboratórios de Integração de Banco de Dados" com visualização abrangente da estrutura dos laboratórios.
- **Estrutura do Repositório**: Atualizado de dez para onze seções principais com descrição detalhada de 11-MCPServerHandsOnLabs.
- **Orientação no Caminho de Aprendizado**: Instruções de navegação aprimoradas para cobrir as seções 00-11.
- **Cobertura Tecnológica**: Adicionados detalhes sobre integração com FastMCP, PostgreSQL e serviços do Azure.
- **Resultados de Aprendizado**: Ênfase no desenvolvimento de servidores prontos para produção, padrões de integração de banco de dados e segurança empresarial.

#### Melhoria na Estrutura do README Principal
- **Terminologia Baseada em Laboratórios**: Atualizado o README.md principal em 11-MCPServerHandsOnLabs para usar consistentemente a estrutura de "Laboratório".
- **Organização do Caminho de Aprendizado**: Progressão clara de conceitos fundamentais até a implementação avançada e implantação em produção.
- **Foco no Mundo Real**: Ênfase no aprendizado prático com padrões e tecnologias de nível empresarial.

### Melhorias na Qualidade e Consistência da Documentação
- **Ênfase no Aprendizado Prático**: Reforçada a abordagem prática baseada em laboratórios em toda a documentação.
- **Foco em Padrões Empresariais**: Destaque para implementações prontas para produção e considerações de segurança empresarial.
- **Integração Tecnológica**: Cobertura abrangente de serviços modernos do Azure e padrões de integração com IA.
- **Progressão de Aprendizado**: Caminho claro e estruturado desde conceitos básicos até a implantação em produção.

## 26 de setembro de 2025

### Melhoria nos Estudos de Caso - Integração com o Registro MCP do GitHub

#### Estudos de Caso (09-CaseStudy/) - Foco no Desenvolvimento do Ecossistema
- **README.md**: Expansão significativa com estudo de caso abrangente sobre o Registro MCP do GitHub.
  - **Estudo de Caso do Registro MCP do GitHub**: Novo estudo de caso abrangente examinando o lançamento do Registro MCP do GitHub em setembro de 2025.
    - **Análise do Problema**: Exame detalhado dos desafios de descoberta e implantação fragmentada de servidores MCP.
    - **Arquitetura da Solução**: Abordagem de registro centralizado do GitHub com instalação de um clique no VS Code.
    - **Impacto nos Negócios**: Melhorias mensuráveis no onboarding de desenvolvedores e na produtividade.
    - **Valor Estratégico**: Foco na implantação modular de agentes e na interoperabilidade entre ferramentas.
    - **Desenvolvimento do Ecossistema**: Posicionamento como plataforma fundamental para integração agentic.
  - **Estrutura Aprimorada dos Estudos de Caso**: Atualizados todos os sete estudos de caso com formatação consistente e descrições abrangentes.
    - Agentes de Viagem do Azure AI: Ênfase na orquestração multi-agente.
    - Integração com Azure DevOps: Foco na automação de fluxos de trabalho.
    - Recuperação de Documentação em Tempo Real: Implementação de cliente de console em Python.
    - Gerador de Plano de Estudos Interativo: Aplicativo web conversacional Chainlit.
    - Documentação no Editor: Integração com VS Code e GitHub Copilot.
    - Gerenciamento de API do Azure: Padrões de integração de API empresarial.
    - Registro MCP do GitHub: Desenvolvimento do ecossistema e plataforma comunitária.
  - **Conclusão Abrangente**: Seção de conclusão reescrita destacando sete estudos de caso abrangendo múltiplas dimensões de implementação do MCP.
    - Integração Empresarial, Orquestração Multi-Agente, Produtividade do Desenvolvedor.
    - Desenvolvimento do Ecossistema, Aplicações Educacionais.
    - Insights aprimorados sobre padrões arquiteturais, estratégias de implementação e melhores práticas.
    - Ênfase no MCP como protocolo maduro e pronto para produção.

#### Atualizações no Guia de Estudos (study_guide.md)
- **Mapa Visual do Currículo**: Mapa mental atualizado para incluir o Registro MCP do GitHub na seção de Estudos de Caso.
- **Descrição dos Estudos de Caso**: Melhorada de descrições genéricas para detalhamento dos sete estudos de caso abrangentes.
- **Estrutura do Repositório**: Atualizada a seção 10 para refletir a cobertura abrangente dos estudos de caso com detalhes específicos de implementação.
- **Integração com o Registro de Alterações**: Adicionada entrada de 26 de setembro de 2025 documentando a adição do Registro MCP do GitHub e melhorias nos estudos de caso.
- **Atualizações de Data**: Atualizado o carimbo de data no rodapé para refletir a revisão mais recente (26 de setembro de 2025).

### Melhorias na Qualidade da Documentação
- **Aprimoramento de Consistência**: Formatação e estrutura padronizadas dos estudos de caso em todos os sete exemplos.
- **Cobertura Abrangente**: Estudos de caso agora abrangem cenários empresariais, de produtividade do desenvolvedor e de desenvolvimento do ecossistema.
- **Posicionamento Estratégico**: Foco aprimorado no MCP como plataforma fundamental para implantação de sistemas agentic.
- **Integração de Recursos**: Recursos adicionais atualizados para incluir link do Registro MCP do GitHub.

## 15 de setembro de 2025

### Expansão de Tópicos Avançados - Transportes Personalizados & Engenharia de Contexto

#### Transportes Personalizados do MCP (05-AdvancedTopics/mcp-transport/) - Novo Guia de Implementação Avançada
- **README.md**: Guia completo de implementação para mecanismos de transporte personalizados do MCP.
  - **Transporte Azure Event Grid**: Implementação abrangente de transporte sem servidor orientado por eventos.
    - Exemplos em C#, TypeScript e Python com integração ao Azure Functions.
    - Padrões de arquitetura orientada por eventos para soluções MCP escaláveis.
    - Receptores de webhook e manipulação de mensagens baseada em push.
  - **Transporte Azure Event Hubs**: Implementação de transporte de streaming de alta taxa de transferência.
    - Capacidades de streaming em tempo real para cenários de baixa latência.
    - Estratégias de particionamento e gerenciamento de checkpoints.
    - Agrupamento de mensagens e otimização de desempenho.
  - **Padrões de Integração Empresarial**: Exemplos arquiteturais prontos para produção.
    - Processamento MCP distribuído em várias Azure Functions.
    - Arquiteturas híbridas de transporte combinando múltiplos tipos de transporte.
    - Estratégias de durabilidade, confiabilidade e tratamento de erros de mensagens.
  - **Segurança & Monitoramento**: Integração com Azure Key Vault e padrões de observabilidade.
    - Autenticação com identidade gerenciada e acesso com privilégios mínimos.
    - Telemetria do Application Insights e monitoramento de desempenho.
    - Padrões de tolerância a falhas e circuit breakers.
  - **Frameworks de Teste**: Estratégias abrangentes de teste para transportes personalizados.
    - Testes unitários com doubles de teste e frameworks de mocking.
    - Testes de integração com Azure Test Containers.
    - Considerações sobre testes de desempenho e carga.

#### Engenharia de Contexto (05-AdvancedTopics/mcp-contextengineering/) - Disciplina Emergente de IA
- **README.md**: Exploração abrangente da engenharia de contexto como um campo emergente.
  - **Princípios Centrais**: Compartilhamento completo de contexto, consciência de decisão de ação e gerenciamento de janela de contexto.
  - **Alinhamento ao Protocolo MCP**: Como o design do MCP aborda os desafios da engenharia de contexto.
    - Limitações de janela de contexto e estratégias de carregamento progressivo.
    - Determinação de relevância e recuperação dinâmica de contexto.
    - Manipulação de contexto multimodal e considerações de segurança.
  - **Abordagens de Implementação**: Arquiteturas single-threaded vs. multi-agente.
    - Técnicas de chunking e priorização de contexto.
    - Estratégias de carregamento progressivo e compressão de contexto.
    - Abordagens de contexto em camadas e otimização de recuperação.
  - **Framework de Medição**: Métricas emergentes para avaliação da eficácia do contexto.
    - Eficiência de entrada, desempenho, qualidade e considerações de experiência do usuário.
    - Abordagens experimentais para otimização de contexto.
    - Análise de falhas e metodologias de melhoria.

#### Atualizações de Navegação no Currículo (README.md)
- **Estrutura Aprimorada de Módulos**: Atualizada a tabela do currículo para incluir novos tópicos avançados.
  - Adicionados Engenharia de Contexto (5.14) e Transporte Personalizado (5.15).
  - Formatação consistente e links de navegação em todos os módulos.
  - Descrições atualizadas para refletir o escopo atual do conteúdo.

### Melhorias na Estrutura de Diretórios
- **Padronização de Nomes**: Renomeado "mcp transport" para "mcp-transport" para consistência com outras pastas de tópicos avançados.
- **Organização de Conteúdo**: Todas as pastas de 05-AdvancedTopics agora seguem um padrão de nomenclatura consistente (mcp-[tópico]).

### Melhorias na Qualidade da Documentação
- **Alinhamento à Especificação MCP**: Todo o novo conteúdo faz referência à Especificação MCP 2025-06-18.
- **Exemplos Multi-Linguagem**: Exemplos de código abrangentes em C#, TypeScript e Python.
- **Foco Empresarial**: Padrões prontos para produção e integração com a nuvem Azure em todo o conteúdo.
- **Documentação Visual**: Diagramas Mermaid para visualização de arquitetura e fluxos.

## 18 de agosto de 2025

### Atualização Abrangente da Documentação - Padrões MCP 2025-06-18

#### Melhores Práticas de Segurança do MCP (02-Security/) - Modernização Completa
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Reescrita completa alinhada à Especificação MCP 2025-06-18.
  - **Requisitos Obrigatórios**: Adicionados requisitos explícitos MUST/MUST NOT da especificação oficial com indicadores visuais claros.
  - **12 Práticas Centrais de Segurança**: Reestruturadas de uma lista de 15 itens para domínios abrangentes de segurança.
    - Segurança de Tokens & Autenticação com integração de provedores de identidade externos.
    - Gerenciamento de Sessões & Segurança de Transporte com requisitos criptográficos.
    - Proteção contra Ameaças Específicas de IA com integração do Microsoft Prompt Shields.
    - Controle de Acesso & Permissões com o princípio do menor privilégio.
    - Segurança de Conteúdo & Monitoramento com integração do Azure Content Safety.
    - Segurança da Cadeia de Suprimentos com verificação abrangente de componentes.
    - Segurança OAuth & Prevenção de Ataques Confused Deputy com implementação PKCE.
    - Resposta a Incidentes & Recuperação com capacidades automatizadas.
    - Conformidade & Governança com alinhamento regulatório.
    - Controles Avançados de Segurança com arquitetura de confiança zero.
    - Integração com o Ecossistema de Segurança da Microsoft com soluções abrangentes.
    - Evolução Contínua da Segurança com práticas adaptativas.
  - **Soluções de Segurança da Microsoft**: Orientação aprimorada para integração com Prompt Shields, Azure Content Safety, Entra ID e GitHub Advanced Security.
  - **Recursos de Implementação**: Links de recursos abrangentes categorizados por Documentação Oficial do MCP, Soluções de Segurança da Microsoft, Padrões de Segurança e Guias de Implementação.

#### Controles Avançados de Segurança (02-Security/) - Implementação Empresarial
- **MCP-SECURITY-CONTROLS-2025.md**: Revisão completa com estrutura de segurança de nível empresarial.
  - **9 Domínios Abrangentes de Segurança**: Expandido de controles básicos para uma estrutura empresarial detalhada.
    - Autenticação & Autorização Avançadas com integração ao Microsoft Entra ID.
    - Segurança de Tokens & Controles Anti-Passthrough com validação abrangente.
    - Controles de Segurança de Sessão com prevenção de sequestro.
    - Controles de Segurança Específicos de IA com prevenção de injeção de prompts e envenenamento de ferramentas.
    - Prevenção de Ataques Confused Deputy com segurança de proxy OAuth.
    - Segurança na Execução de Ferramentas com sandboxing e isolamento.
    - Controles de Segurança da Cadeia de Suprimentos com verificação de dependências.
    - Controles de Monitoramento & Detecção com integração SIEM.
    - Resposta a Incidentes & Recuperação com capacidades automatizadas.
  - **Exemplos de Implementação**: Adicionados blocos de configuração YAML detalhados e exemplos de código.
  - **Integração com Soluções da Microsoft**: Cobertura abrangente de serviços de segurança do Azure, GitHub Advanced Security e gerenciamento de identidade empresarial.
#### Tópicos Avançados de Segurança (05-AdvancedTopics/mcp-security/) - Implementação Pronta para Produção
- **README.md**: Reescrita completa para implementação de segurança empresarial
  - **Alinhamento com Especificação Atual**: Atualizado para a Especificação MCP 2025-06-18 com requisitos obrigatórios de segurança
  - **Autenticação Aprimorada**: Integração com Microsoft Entra ID e exemplos abrangentes em .NET e Java Spring Security
  - **Integração de Segurança com IA**: Implementação do Microsoft Prompt Shields e Azure Content Safety com exemplos detalhados em Python
  - **Mitigação Avançada de Ameaças**: Exemplos abrangentes de implementação para:
    - Prevenção de Ataques de Confusão de Deputado com PKCE e validação de consentimento do usuário
    - Prevenção de Passagem de Token com validação de público e gerenciamento seguro de tokens
    - Prevenção de Sequestro de Sessão com vinculação criptográfica e análise comportamental
  - **Integração de Segurança Empresarial**: Monitoramento com Azure Application Insights, pipelines de detecção de ameaças e segurança da cadeia de suprimentos
  - **Lista de Verificação de Implementação**: Controles de segurança obrigatórios vs. recomendados com benefícios do ecossistema de segurança da Microsoft

### Qualidade da Documentação e Alinhamento com Padrões
- **Referências de Especificação**: Atualizadas todas as referências para a Especificação MCP 2025-06-18
- **Ecossistema de Segurança da Microsoft**: Orientação aprimorada de integração em toda a documentação de segurança
- **Implementação Prática**: Adicionados exemplos detalhados de código em .NET, Java e Python com padrões empresariais
- **Organização de Recursos**: Categorização abrangente de documentação oficial, padrões de segurança e guias de implementação
- **Indicadores Visuais**: Marcação clara de requisitos obrigatórios vs. práticas recomendadas

#### Conceitos Fundamentais (01-CoreConcepts/) - Modernização Completa
- **Atualização de Versão do Protocolo**: Atualizado para referência à Especificação MCP 2025-06-18 com versionamento baseado em data (formato YYYY-MM-DD)
- **Refinamento de Arquitetura**: Descrições aprimoradas de Hosts, Clientes e Servidores para refletir os padrões atuais de arquitetura MCP
  - Hosts agora definidos claramente como aplicativos de IA que coordenam múltiplas conexões de clientes MCP
  - Clientes descritos como conectores de protocolo que mantêm relações um-para-um com servidores
  - Servidores aprimorados com cenários de implantação local vs. remota
- **Reestruturação de Primitivas**: Revisão completa das primitivas de servidor e cliente
  - Primitivas de Servidor: Recursos (fontes de dados), Prompts (modelos), Ferramentas (funções executáveis) com explicações detalhadas e exemplos
  - Primitivas de Cliente: Amostragem (completions de LLM), Elicitação (entrada do usuário), Logging (depuração/monitoramento)
  - Atualizado com padrões atuais de descoberta (`*/list`), recuperação (`*/get`) e execução (`*/call`)
- **Arquitetura do Protocolo**: Introdução de modelo de arquitetura em duas camadas
  - Camada de Dados: Fundação JSON-RPC 2.0 com gerenciamento de ciclo de vida e primitivas
  - Camada de Transporte: STDIO (local) e HTTP com SSE (remoto) como mecanismos de transporte
- **Framework de Segurança**: Princípios abrangentes de segurança, incluindo consentimento explícito do usuário, proteção de privacidade de dados, segurança na execução de ferramentas e segurança na camada de transporte
- **Padrões de Comunicação**: Mensagens do protocolo atualizadas para mostrar fluxos de inicialização, descoberta, execução e notificações
- **Exemplos de Código**: Exemplos multilíngues atualizados (.NET, Java, Python, JavaScript) para refletir os padrões atuais do SDK MCP

#### Segurança (02-Security/) - Revisão Abrangente de Segurança  
- **Alinhamento com Padrões**: Alinhamento completo com os requisitos de segurança da Especificação MCP 2025-06-18
- **Evolução da Autenticação**: Documentada a evolução de servidores OAuth personalizados para delegação de provedores de identidade externos (Microsoft Entra ID)
- **Análise de Ameaças Específicas de IA**: Cobertura aprimorada de vetores modernos de ataque em IA
  - Cenários detalhados de ataques de injeção de prompts com exemplos reais
  - Mecanismos de envenenamento de ferramentas e padrões de ataque "rug pull"
  - Envenenamento de janela de contexto e ataques de confusão de modelo
- **Soluções de Segurança em IA da Microsoft**: Cobertura abrangente do ecossistema de segurança da Microsoft
  - Prompt Shields de IA com técnicas avançadas de detecção, destaque e delimitadores
  - Padrões de integração do Azure Content Safety
  - GitHub Advanced Security para proteção da cadeia de suprimentos
- **Mitigação Avançada de Ameaças**: Controles de segurança detalhados para:
  - Sequestro de sessão com cenários de ataque específicos do MCP e requisitos de ID de sessão criptográfica
  - Problemas de confusão de deputado em cenários de proxy MCP com requisitos explícitos de consentimento
  - Vulnerabilidades de passagem de token com controles obrigatórios de validação
- **Segurança da Cadeia de Suprimentos**: Cobertura expandida da cadeia de suprimentos de IA, incluindo modelos base, serviços de embeddings, provedores de contexto e APIs de terceiros
- **Segurança Fundamental**: Integração aprimorada com padrões de segurança empresarial, incluindo arquitetura de confiança zero e ecossistema de segurança da Microsoft
- **Organização de Recursos**: Links de recursos categorizados de forma abrangente por tipo (Documentação Oficial, Padrões, Pesquisa, Soluções da Microsoft, Guias de Implementação)

### Melhorias na Qualidade da Documentação
- **Objetivos de Aprendizado Estruturados**: Objetivos de aprendizado aprimorados com resultados específicos e acionáveis
- **Referências Cruzadas**: Adicionados links entre tópicos relacionados de segurança e conceitos fundamentais
- **Informações Atualizadas**: Atualizadas todas as referências de datas e links de especificação para padrões atuais
- **Orientação de Implementação**: Adicionadas diretrizes específicas e acionáveis de implementação em ambas as seções

## 16 de julho de 2025

### Melhorias no README e Navegação
- Redesenho completo da navegação do currículo no README.md
- Substituídos os tags `<details>` por formato de tabela mais acessível
- Criadas opções de layout alternativas na nova pasta "alternative_layouts"
- Adicionados exemplos de navegação em estilo de cartões, abas e acordeão
- Atualizada a seção de estrutura do repositório para incluir todos os arquivos mais recentes
- Melhorada a seção "Como Usar Este Currículo" com recomendações claras
- Atualizados os links de especificação MCP para apontar para URLs corretos
- Adicionada seção de Engenharia de Contexto (5.14) à estrutura do currículo

### Atualizações do Guia de Estudos
- Revisão completa do guia de estudos para alinhar com a estrutura atual do repositório
- Adicionadas novas seções para Clientes e Ferramentas MCP, e Servidores MCP Populares
- Atualizado o Mapa Visual do Currículo para refletir com precisão todos os tópicos
- Melhoradas as descrições de Tópicos Avançados para cobrir todas as áreas especializadas
- Atualizada a seção de Estudos de Caso para refletir exemplos reais
- Adicionado este changelog abrangente

### Contribuições da Comunidade (06-CommunityContributions/)
- Adicionadas informações detalhadas sobre servidores MCP para geração de imagens
- Adicionada seção abrangente sobre o uso do Claude no VSCode
- Adicionadas instruções de configuração e uso do cliente terminal Cline
- Atualizada a seção de clientes MCP para incluir todas as opções populares de clientes
- Melhorados os exemplos de contribuição com amostras de código mais precisas

### Tópicos Avançados (05-AdvancedTopics/)
- Organizadas todas as pastas de tópicos especializados com nomenclatura consistente
- Adicionados materiais e exemplos de engenharia de contexto
- Adicionada documentação de integração do agente Foundry
- Melhorada a documentação de integração de segurança do Entra ID

## 11 de junho de 2025

### Criação Inicial
- Lançada a primeira versão do currículo MCP para Iniciantes
- Criada estrutura básica para todas as 10 seções principais
- Implementado Mapa Visual do Currículo para navegação
- Adicionados projetos de exemplo iniciais em várias linguagens de programação

### Primeiros Passos (03-GettingStarted/)
- Criados os primeiros exemplos de implementação de servidor
- Adicionada orientação para desenvolvimento de clientes
- Incluídas instruções de integração de clientes LLM
- Adicionada documentação de integração com VS Code
- Implementados exemplos de servidor com Server-Sent Events (SSE)

### Conceitos Fundamentais (01-CoreConcepts/)
- Adicionada explicação detalhada da arquitetura cliente-servidor
- Criada documentação sobre componentes-chave do protocolo
- Documentados padrões de mensagens no MCP

## 23 de maio de 2025

### Estrutura do Repositório
- Inicializado o repositório com estrutura básica de pastas
- Criados arquivos README para cada seção principal
- Configurada infraestrutura de tradução
- Adicionados ativos de imagem e diagramas

### Documentação
- Criado README.md inicial com visão geral do currículo
- Adicionados CODE_OF_CONDUCT.md e SECURITY.md
- Configurado SUPPORT.md com orientações para obter ajuda
- Criada estrutura preliminar do guia de estudos

## 15 de abril de 2025

### Planejamento e Estrutura
- Planejamento inicial para o currículo MCP para Iniciantes
- Definidos objetivos de aprendizado e público-alvo
- Estruturadas as 10 seções do currículo
- Desenvolvido framework conceitual para exemplos e estudos de caso
- Criados protótipos iniciais de exemplos para conceitos-chave

---

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte oficial. Para informações críticas, recomenda-se a tradução profissional feita por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações equivocadas decorrentes do uso desta tradução.