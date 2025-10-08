<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T17:08:45+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "br"
}
-->
# Segurança do MCP: Proteção Abrangente para Sistemas de IA

[![Melhores Práticas de Segurança do MCP](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.br.png)](https://youtu.be/88No8pw706o)

_(Clique na imagem acima para assistir ao vídeo desta lição)_

A segurança é fundamental no design de sistemas de IA, e é por isso que a priorizamos como nossa segunda seção. Isso está alinhado com o princípio **Secure by Design** da Microsoft, parte da [Iniciativa Futuro Seguro](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

O Protocolo de Contexto de Modelo (MCP) traz novas e poderosas capacidades para aplicações baseadas em IA, mas também introduz desafios únicos de segurança que vão além dos riscos tradicionais de software. Sistemas MCP enfrentam preocupações de segurança já conhecidas (codificação segura, princípio do menor privilégio, segurança da cadeia de suprimentos) e novas ameaças específicas de IA, como injeção de prompts, envenenamento de ferramentas, sequestro de sessões, ataques de confusão de autoridade, vulnerabilidades de passagem de tokens e modificação dinâmica de capacidades.

Esta lição explora os riscos de segurança mais críticos em implementações do MCP—cobrindo autenticação, autorização, permissões excessivas, injeção indireta de prompts, segurança de sessões, problemas de confusão de autoridade, gerenciamento de tokens e vulnerabilidades na cadeia de suprimentos. Você aprenderá controles práticos e melhores práticas para mitigar esses riscos, enquanto utiliza soluções da Microsoft como Prompt Shields, Azure Content Safety e GitHub Advanced Security para fortalecer sua implantação do MCP.

## Objetivos de Aprendizado

Ao final desta lição, você será capaz de:

- **Identificar Ameaças Específicas do MCP**: Reconhecer riscos únicos de segurança em sistemas MCP, incluindo injeção de prompts, envenenamento de ferramentas, permissões excessivas, sequestro de sessões, problemas de confusão de autoridade, vulnerabilidades de passagem de tokens e riscos na cadeia de suprimentos
- **Aplicar Controles de Segurança**: Implementar mitigações eficazes, incluindo autenticação robusta, acesso com menor privilégio, gerenciamento seguro de tokens, controles de segurança de sessões e verificação da cadeia de suprimentos
- **Aproveitar Soluções de Segurança da Microsoft**: Entender e implementar Microsoft Prompt Shields, Azure Content Safety e GitHub Advanced Security para proteger cargas de trabalho do MCP
- **Validar Segurança de Ferramentas**: Reconhecer a importância da validação de metadados de ferramentas, monitoramento de mudanças dinâmicas e defesa contra ataques de injeção indireta de prompts
- **Integrar Melhores Práticas**: Combinar fundamentos de segurança estabelecidos (codificação segura, fortalecimento de servidores, confiança zero) com controles específicos do MCP para uma proteção abrangente

# Arquitetura e Controles de Segurança do MCP

Implementações modernas do MCP exigem abordagens de segurança em camadas que abordem tanto ameaças tradicionais de segurança de software quanto ameaças específicas de IA. A especificação do MCP está evoluindo rapidamente, amadurecendo seus controles de segurança e permitindo melhor integração com arquiteturas de segurança corporativa e melhores práticas estabelecidas.

Pesquisas do [Relatório de Defesa Digital da Microsoft](https://aka.ms/mddr) demonstram que **98% das violações relatadas poderiam ser evitadas com práticas robustas de higiene de segurança**. A estratégia de proteção mais eficaz combina práticas de segurança fundamentais com controles específicos do MCP—medidas de segurança básicas comprovadas continuam sendo as mais impactantes na redução do risco geral.

## Cenário Atual de Segurança

> **Nota:** Estas informações refletem os padrões de segurança do MCP em **18 de agosto de 2025**. O protocolo MCP continua evoluindo rapidamente, e implementações futuras podem introduzir novos padrões de autenticação e controles aprimorados. Consulte sempre a [Especificação Atual do MCP](https://spec.modelcontextprotocol.io/), o [repositório GitHub do MCP](https://github.com/modelcontextprotocol) e a [documentação de melhores práticas de segurança](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) para obter as orientações mais recentes.

### Evolução da Autenticação no MCP

A especificação do MCP evoluiu significativamente em sua abordagem à autenticação e autorização:

- **Abordagem Original**: As primeiras especificações exigiam que os desenvolvedores implementassem servidores de autenticação personalizados, com servidores MCP atuando como Servidores de Autorização OAuth 2.0 gerenciando a autenticação de usuários diretamente
- **Padrão Atual (2025-06-18)**: A especificação atualizada permite que servidores MCP deleguem a autenticação a provedores de identidade externos (como Microsoft Entra ID), melhorando a postura de segurança e reduzindo a complexidade da implementação
- **Segurança na Camada de Transporte**: Suporte aprimorado para mecanismos de transporte seguro com padrões adequados de autenticação para conexões locais (STDIO) e remotas (HTTP Streamable)

## Segurança de Autenticação e Autorização

### Desafios de Segurança Atuais

Implementações modernas do MCP enfrentam vários desafios relacionados à autenticação e autorização:

### Riscos e Vetores de Ameaça

- **Lógica de Autorização Mal Configurada**: Implementações defeituosas de autorização em servidores MCP podem expor dados sensíveis e aplicar controles de acesso incorretamente
- **Comprometimento de Tokens OAuth**: O roubo de tokens de servidores MCP locais permite que atacantes se façam passar por servidores e acessem serviços a jusante
- **Vulnerabilidades de Passagem de Tokens**: O manuseio inadequado de tokens cria brechas nos controles de segurança e lacunas de responsabilidade
- **Permissões Excessivas**: Servidores MCP com privilégios excessivos violam os princípios de menor privilégio e ampliam as superfícies de ataque

#### Passagem de Tokens: Um Padrão Crítico a Ser Evitado

**A passagem de tokens é explicitamente proibida** na especificação atual de autorização do MCP devido às graves implicações de segurança:

##### Circunvenção de Controles de Segurança
- Servidores MCP e APIs a jusante implementam controles de segurança críticos (limitação de taxa, validação de solicitações, monitoramento de tráfego) que dependem da validação adequada de tokens
- O uso direto de tokens cliente-para-API contorna essas proteções essenciais, comprometendo a arquitetura de segurança

##### Desafios de Responsabilidade e Auditoria  
- Servidores MCP não conseguem distinguir entre clientes usando tokens emitidos a montante, quebrando trilhas de auditoria
- Logs de servidores de recursos a jusante mostram origens de solicitações enganosas em vez de intermediários reais (servidores MCP)
- Investigações de incidentes e auditorias de conformidade tornam-se significativamente mais difíceis

##### Riscos de Exfiltração de Dados
- Declarações de tokens não validadas permitem que atores mal-intencionados com tokens roubados usem servidores MCP como proxies para exfiltração de dados
- Violações de limites de confiança permitem padrões de acesso não autorizados que contornam os controles de segurança pretendidos

##### Vetores de Ataque Multi-Serviço
- Tokens comprometidos aceitos por vários serviços permitem movimentos laterais em sistemas conectados
- Suposições de confiança entre serviços podem ser violadas quando as origens dos tokens não podem ser verificadas

### Controles de Segurança e Mitigações

**Requisitos Críticos de Segurança:**

> **OBRIGATÓRIO**: Servidores MCP **NÃO DEVEM** aceitar tokens que não tenham sido explicitamente emitidos para o servidor MCP

#### Controles de Autenticação e Autorização

- **Revisão Rigorosa de Autorização**: Realizar auditorias abrangentes da lógica de autorização dos servidores MCP para garantir que apenas usuários e clientes pretendidos possam acessar recursos sensíveis
  - **Guia de Implementação**: [Azure API Management como Gateway de Autenticação para Servidores MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Integração de Identidade**: [Usando Microsoft Entra ID para Autenticação de Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Gerenciamento Seguro de Tokens**: Implementar [práticas recomendadas de validação e ciclo de vida de tokens da Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Validar que as declarações de audiência dos tokens correspondem à identidade do servidor MCP
  - Implementar políticas adequadas de rotação e expiração de tokens
  - Prevenir ataques de repetição de tokens e uso não autorizado

- **Armazenamento Protegido de Tokens**: Armazenar tokens de forma segura com criptografia tanto em repouso quanto em trânsito
  - **Melhores Práticas**: [Diretrizes de Armazenamento Seguro e Criptografia de Tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implementação de Controle de Acesso

- **Princípio do Menor Privilégio**: Conceder aos servidores MCP apenas as permissões mínimas necessárias para a funcionalidade pretendida
  - Revisões regulares de permissões e atualizações para evitar o aumento de privilégios
  - **Documentação da Microsoft**: [Acesso Seguro com Menor Privilégio](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Controle de Acesso Baseado em Funções (RBAC)**: Implementar atribuições de funções granulares
  - Restringir funções a recursos e ações específicas
  - Evitar permissões amplas ou desnecessárias que ampliem as superfícies de ataque

- **Monitoramento Contínuo de Permissões**: Implementar auditorias e monitoramento contínuos de acesso
  - Monitorar padrões de uso de permissões para identificar anomalias
  - Remediar prontamente privilégios excessivos ou não utilizados

## Ameaças Específicas de Segurança em IA

### Ataques de Injeção de Prompts e Manipulação de Ferramentas

Implementações modernas do MCP enfrentam vetores de ataque sofisticados específicos de IA que medidas tradicionais de segurança não conseguem abordar completamente:

#### **Injeção Indireta de Prompts (Injeção de Prompts entre Domínios)**

A **injeção indireta de prompts** representa uma das vulnerabilidades mais críticas em sistemas de IA habilitados pelo MCP. Atacantes inserem instruções maliciosas em conteúdos externos—documentos, páginas da web, e-mails ou fontes de dados—que os sistemas de IA processam como comandos legítimos.

**Cenários de Ataque:**
- **Injeção Baseada em Documentos**: Instruções maliciosas ocultas em documentos processados que acionam ações não intencionais da IA
- **Exploração de Conteúdo da Web**: Páginas da web comprometidas contendo prompts embutidos que manipulam o comportamento da IA quando extraídas
- **Ataques Baseados em E-mail**: Prompts maliciosos em e-mails que fazem assistentes de IA vazarem informações ou executarem ações não autorizadas
- **Contaminação de Fontes de Dados**: Bancos de dados ou APIs comprometidos servindo conteúdos adulterados para sistemas de IA

**Impacto no Mundo Real**: Esses ataques podem resultar em exfiltração de dados, violações de privacidade, geração de conteúdos prejudiciais e manipulação de interações com usuários. Para uma análise detalhada, veja [Injeção de Prompts no MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Diagrama de Ataque de Injeção de Prompts](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.br.png)

#### **Ataques de Envenenamento de Ferramentas**

O **envenenamento de ferramentas** tem como alvo os metadados que definem as ferramentas do MCP, explorando como os LLMs interpretam descrições de ferramentas e parâmetros para tomar decisões de execução.

**Mecanismos de Ataque:**
- **Manipulação de Metadados**: Atacantes inserem instruções maliciosas em descrições de ferramentas, definições de parâmetros ou exemplos de uso
- **Instruções Invisíveis**: Prompts ocultos nos metadados das ferramentas que são processados por modelos de IA, mas invisíveis para usuários humanos
- **Modificação Dinâmica de Ferramentas ("Rug Pulls")**: Ferramentas aprovadas pelos usuários são posteriormente modificadas para realizar ações maliciosas sem o conhecimento do usuário
- **Injeção de Parâmetros**: Conteúdo malicioso embutido em esquemas de parâmetros de ferramentas que influenciam o comportamento do modelo

**Riscos em Servidores Hospedados**: Servidores MCP remotos apresentam riscos elevados, pois as definições de ferramentas podem ser atualizadas após a aprovação inicial do usuário, criando cenários em que ferramentas anteriormente seguras se tornam maliciosas. Para uma análise abrangente, veja [Ataques de Envenenamento de Ferramentas (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Diagrama de Ataque de Injeção de Ferramentas](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.br.png)

#### **Vetores Adicionais de Ataque em IA**

- **Injeção de Prompts entre Domínios (XPIA)**: Ataques sofisticados que utilizam conteúdos de múltiplos domínios para contornar controles de segurança
- **Modificação Dinâmica de Capacidades**: Alterações em tempo real nas capacidades das ferramentas que escapam de avaliações de segurança iniciais
- **Envenenamento de Janelas de Contexto**: Ataques que manipulam grandes janelas de contexto para ocultar instruções maliciosas
- **Ataques de Confusão de Modelos**: Exploração de limitações do modelo para criar comportamentos imprevisíveis ou inseguros

### Impacto dos Riscos de Segurança em IA

**Consequências de Alto Impacto:**
- **Exfiltração de Dados**: Acesso não autorizado e roubo de dados sensíveis empresariais ou pessoais
- **Violações de Privacidade**: Exposição de informações pessoalmente identificáveis (PII) e dados confidenciais de negócios  
- **Manipulação de Sistemas**: Modificações não intencionais em sistemas e fluxos de trabalho críticos
- **Roubo de Credenciais**: Comprometimento de tokens de autenticação e credenciais de serviço
- **Movimento Lateral**: Uso de sistemas de IA comprometidos como pivôs para ataques mais amplos na rede

### Soluções de Segurança da Microsoft para IA

#### **AI Prompt Shields: Proteção Avançada Contra Ataques de Injeção**

Os **AI Prompt Shields** da Microsoft oferecem defesa abrangente contra ataques de injeção direta e indireta por meio de múltiplas camadas de segurança:

##### **Mecanismos Centrais de Proteção:**

1. **Detecção e Filtragem Avançadas**
   - Algoritmos de aprendizado de máquina e técnicas de PLN detectam instruções maliciosas em conteúdos externos
   - Análise em tempo real de documentos, páginas da web, e-mails e fontes de dados para ameaças embutidas
   - Compreensão contextual de padrões legítimos vs. maliciosos de prompts

2. **Técnicas de Destaque**
   - Distingue entre instruções confiáveis do sistema e entradas externas potencialmente comprometidas
   - Métodos de transformação de texto que isolam conteúdos maliciosos enquanto mantêm a relevância do modelo
   - Ajuda sistemas de IA a manter hierarquias de instruções adequadas e ignorar comandos injetados

3. **Sistemas de Delimitação e Marcação de Dados**
   - Definição explícita de limites entre mensagens confiáveis do sistema e texto de entrada externo
   - Marcadores especiais destacam limites entre fontes de dados confiáveis e não confiáveis
   - Separação clara evita confusão de instruções e execução de comandos não autorizados

4. **Inteligência Contínua de Ameaças**
   - A Microsoft monitora continuamente padrões emergentes de ataque e atualiza as defesas
   - Busca proativa por novas técnicas de injeção e vetores de ataque
   - Atualizações regulares de modelos de segurança para manter a eficácia contra ameaças em evolução

5. **Integração com Azure Content Safety**
   - Parte do conjunto abrangente de segurança de conteúdo do Azure AI
   - Detecção adicional de tentativas de jailbreak, conteúdos prejudiciais e violações de políticas de segurança
   - Controles de segurança unificados em componentes de aplicações de IA

**Recursos de Implementação**: [Documentação do Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)

![Proteção do Microsoft Prompt Shields](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.br.png)


## Ameaças Avançadas de Segurança do MCP

### Vulnerabilidades de Sequestro de Sessões

O **sequestro de sessões** representa um vetor de ataque crítico em implementações MCP com estado, onde partes não autorizadas obtêm e abusam de identificadores de sessão legítimos para se passar por clientes e realizar ações não autorizadas.

#### **Cenários de Ataque e Riscos**

- **Injeção de Prompts em Sessões Sequestradas**: Atacantes com IDs de sessão roubados injetam eventos maliciosos em servidores que compartilham estado de sessão, potencialmente acionando ações prejudiciais ou acessando dados sensíveis
- **Impersonação Direta**: IDs de sessão roubados permitem chamadas diretas a servidores MCP que contornam a autenticação, tratando atacantes como usuários legítimos
- **Streams Reutilizáveis Comprometidos**: Atacantes podem encerrar solicitações prematuramente, fazendo com que clientes legítimos retomem com conteúdos potencialmente maliciosos

#### **Controles de Segurança para Gerenciamento de Sessões**

**Requisitos Críticos:**
- **Verificação de Autorização**: Servidores MCP que implementam autorização **DEVEM** verificar TODAS as solicitações recebidas e **NÃO DEVEM** depender de sessões para autenticação
- **Geração Segura de Sessões**: Use IDs de sessão criptograficamente seguros e não determinísticos, gerados com geradores de números aleatórios seguros  
- **Vinculação Específica ao Usuário**: Vincule os IDs de sessão a informações específicas do usuário usando formatos como `<user_id>:<session_id>` para evitar abuso de sessões entre usuários  
- **Gerenciamento do Ciclo de Vida da Sessão**: Implemente expiração, rotação e invalidação adequadas para limitar janelas de vulnerabilidade  
- **Segurança no Transporte**: HTTPS obrigatório para todas as comunicações, evitando a interceptação de IDs de sessão  

### Problema do Deputado Confuso  

O **problema do deputado confuso** ocorre quando servidores MCP atuam como proxies de autenticação entre clientes e serviços de terceiros, criando oportunidades para bypass de autorização por meio da exploração de IDs de cliente estáticos.  

#### **Mecânica do Ataque e Riscos**  

- **Bypass de Consentimento Baseado em Cookies**: A autenticação prévia do usuário cria cookies de consentimento que atacantes exploram por meio de solicitações de autorização maliciosas com URIs de redirecionamento manipulados  
- **Roubo de Código de Autorização**: Cookies de consentimento existentes podem fazer com que servidores de autorização ignorem telas de consentimento, redirecionando códigos para endpoints controlados por atacantes  
- **Acesso Não Autorizado a APIs**: Códigos de autorização roubados permitem a troca de tokens e a personificação do usuário sem aprovação explícita  

#### **Estratégias de Mitigação**  

**Controles Obrigatórios:**  
- **Requisitos de Consentimento Explícito**: Servidores proxy MCP que usam IDs de cliente estáticos **DEVEM** obter consentimento do usuário para cada cliente registrado dinamicamente  
- **Implementação de Segurança OAuth 2.1**: Siga as melhores práticas de segurança OAuth atuais, incluindo PKCE (Prova de Chave para Troca de Código) para todas as solicitações de autorização  
- **Validação Estrita de Clientes**: Implemente validação rigorosa de URIs de redirecionamento e identificadores de cliente para evitar exploração  

### Vulnerabilidades de Passagem de Tokens  

A **passagem de tokens** representa um antipadrão explícito onde servidores MCP aceitam tokens de clientes sem validação adequada e os encaminham para APIs downstream, violando especificações de autorização MCP.  

#### **Implicações de Segurança**  

- **Circunvenção de Controles**: O uso direto de tokens de cliente para API ignora controles críticos de limitação de taxa, validação e monitoramento  
- **Corrupção de Trilhas de Auditoria**: Tokens emitidos upstream tornam impossível a identificação do cliente, prejudicando investigações de incidentes  
- **Exfiltração de Dados Baseada em Proxy**: Tokens não validados permitem que atores maliciosos usem servidores como proxies para acesso não autorizado a dados  
- **Violações de Limites de Confiança**: Suposições de confiança de serviços downstream podem ser violadas quando as origens dos tokens não podem ser verificadas  
- **Expansão de Ataques Multi-serviço**: Tokens comprometidos aceitos em vários serviços permitem movimentos laterais  

#### **Controles de Segurança Necessários**  

**Requisitos Inegociáveis:**  
- **Validação de Tokens**: Servidores MCP **NÃO DEVEM** aceitar tokens que não tenham sido explicitamente emitidos para o servidor MCP  
- **Verificação de Público**: Sempre valide as declarações de público dos tokens para garantir que correspondam à identidade do servidor MCP  
- **Ciclo de Vida Adequado de Tokens**: Implemente tokens de acesso de curta duração com práticas seguras de rotação  

## Segurança da Cadeia de Suprimentos para Sistemas de IA  

A segurança da cadeia de suprimentos evoluiu além das dependências tradicionais de software para abranger todo o ecossistema de IA. Implementações modernas de MCP devem verificar e monitorar rigorosamente todos os componentes relacionados à IA, já que cada um deles introduz potenciais vulnerabilidades que podem comprometer a integridade do sistema.  

### Componentes Ampliados da Cadeia de Suprimentos de IA  

**Dependências Tradicionais de Software:**  
- Bibliotecas e frameworks de código aberto  
- Imagens de contêiner e sistemas base  
- Ferramentas de desenvolvimento e pipelines de build  
- Componentes e serviços de infraestrutura  

**Elementos Específicos de IA na Cadeia de Suprimentos:**  
- **Modelos Fundamentais**: Modelos pré-treinados de diversos provedores que exigem verificação de procedência  
- **Serviços de Embedding**: Serviços externos de vetorização e busca semântica  
- **Provedores de Contexto**: Fontes de dados, bases de conhecimento e repositórios de documentos  
- **APIs de Terceiros**: Serviços externos de IA, pipelines de ML e endpoints de processamento de dados  
- **Artefatos de Modelos**: Pesos, configurações e variantes de modelos ajustados  
- **Fontes de Dados de Treinamento**: Conjuntos de dados usados para treinamento e ajuste fino de modelos  

### Estratégia Abrangente de Segurança da Cadeia de Suprimentos  

#### **Verificação de Componentes e Confiança**  
- **Validação de Procedência**: Verifique a origem, licenciamento e integridade de todos os componentes de IA antes da integração  
- **Avaliação de Segurança**: Realize varreduras de vulnerabilidades e revisões de segurança para modelos, fontes de dados e serviços de IA  
- **Análise de Reputação**: Avalie o histórico de segurança e as práticas dos provedores de serviços de IA  
- **Verificação de Conformidade**: Certifique-se de que todos os componentes atendam aos requisitos de segurança e regulamentação da organização  

#### **Pipelines de Implantação Seguros**  
- **Segurança Automatizada em CI/CD**: Integre varreduras de segurança em pipelines de implantação automatizados  
- **Integridade de Artefatos**: Implemente verificações criptográficas para todos os artefatos implantados (código, modelos, configurações)  
- **Implantação em Estágios**: Use estratégias de implantação progressiva com validação de segurança em cada estágio  
- **Repositórios de Artefatos Confiáveis**: Implante apenas a partir de registros e repositórios de artefatos verificados e seguros  

#### **Monitoramento Contínuo e Resposta**  
- **Varredura de Dependências**: Monitoramento contínuo de vulnerabilidades para todas as dependências de software e componentes de IA  
- **Monitoramento de Modelos**: Avaliação contínua do comportamento do modelo, desvios de desempenho e anomalias de segurança  
- **Rastreamento de Saúde de Serviços**: Monitore serviços externos de IA quanto à disponibilidade, incidentes de segurança e mudanças de políticas  
- **Integração de Inteligência contra Ameaças**: Incorpore feeds de ameaças específicos para riscos de segurança em IA e ML  

#### **Controle de Acesso e Privilégio Mínimo**  
- **Permissões em Nível de Componente**: Restrinja o acesso a modelos, dados e serviços com base na necessidade de negócios  
- **Gerenciamento de Contas de Serviço**: Implemente contas de serviço dedicadas com permissões mínimas necessárias  
- **Segmentação de Rede**: Isole componentes de IA e limite o acesso entre serviços na rede  
- **Controles de Gateway de API**: Use gateways de API centralizados para controlar e monitorar o acesso a serviços externos de IA  

#### **Resposta a Incidentes e Recuperação**  
- **Procedimentos de Resposta Rápida**: Processos estabelecidos para corrigir ou substituir componentes de IA comprometidos  
- **Rotação de Credenciais**: Sistemas automatizados para rotação de segredos, chaves de API e credenciais de serviço  
- **Capacidades de Rollback**: Capacidade de reverter rapidamente para versões anteriores conhecidas e confiáveis de componentes de IA  
- **Recuperação de Brechas na Cadeia de Suprimentos**: Procedimentos específicos para responder a comprometimentos de serviços de IA upstream  

### Ferramentas de Segurança da Microsoft e Integração  

**GitHub Advanced Security** oferece proteção abrangente para a cadeia de suprimentos, incluindo:  
- **Varredura de Segredos**: Detecção automatizada de credenciais, chaves de API e tokens em repositórios  
- **Varredura de Dependências**: Avaliação de vulnerabilidades para dependências e bibliotecas de código aberto  
- **Análise CodeQL**: Análise estática de código para vulnerabilidades de segurança e problemas de codificação  
- **Insights da Cadeia de Suprimentos**: Visibilidade sobre a saúde e o status de segurança das dependências  

**Integração com Azure DevOps e Azure Repos:**  
- Integração perfeita de varreduras de segurança nas plataformas de desenvolvimento da Microsoft  
- Verificações de segurança automatizadas em Azure Pipelines para cargas de trabalho de IA  
- Aplicação de políticas para implantação segura de componentes de IA  

**Práticas Internas da Microsoft:**  
A Microsoft implementa práticas extensivas de segurança da cadeia de suprimentos em todos os produtos. Saiba mais sobre abordagens comprovadas em [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Soluções de Segurança da Microsoft**
- [Documentação do Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Serviço de Segurança de Conteúdo do Azure](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Segurança do Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Práticas Recomendadas para Gerenciamento de Tokens no Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Segurança Avançada do GitHub](https://github.com/security/advanced-security)

### **Guias de Implementação e Tutoriais**
- [Gerenciamento de API do Azure como Gateway de Autenticação MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Autenticação do Microsoft Entra ID com Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Armazenamento Seguro de Tokens e Criptografia (Vídeo)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps e Segurança da Cadeia de Suprimentos**
- [Segurança do Azure DevOps](https://azure.microsoft.com/products/devops)
- [Segurança do Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [A Jornada de Segurança da Cadeia de Suprimentos da Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Documentação Adicional de Segurança**

Para orientações completas sobre segurança, consulte os documentos especializados nesta seção:

- **[Práticas Recomendadas de Segurança MCP 2025](./mcp-security-best-practices-2025.md)** - Práticas recomendadas completas de segurança para implementações MCP  
- **[Implementação de Segurança de Conteúdo do Azure](./azure-content-safety-implementation.md)** - Exemplos práticos de integração com o Azure Content Safety  
- **[Controles de Segurança MCP 2025](./mcp-security-controls-2025.md)** - Controles e técnicas de segurança mais recentes para implantações MCP  
- **[Guia Rápido de Práticas Recomendadas MCP](./mcp-best-practices.md)** - Guia de referência rápida para práticas essenciais de segurança MCP  

---

## O Que Vem a Seguir

Próximo: [Capítulo 3: Primeiros Passos](../03-GettingStarted/README.md)

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte oficial. Para informações críticas, recomenda-se a tradução profissional feita por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações equivocadas decorrentes do uso desta tradução.