<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T11:31:55+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "pt"
}
-->
# Melhores Práticas de Segurança MCP 2025

Este guia abrangente descreve as melhores práticas essenciais de segurança para a implementação de sistemas Model Context Protocol (MCP) com base na mais recente **Especificação MCP 2025-06-18** e nos padrões atuais da indústria. Estas práticas abordam tanto preocupações tradicionais de segurança quanto ameaças específicas de IA exclusivas para implementações MCP.

## Requisitos Críticos de Segurança

### Controles de Segurança Obrigatórios (Requisitos MUST)

1. **Validação de Tokens**: Os servidores MCP **NÃO DEVEM** aceitar tokens que não tenham sido explicitamente emitidos para o próprio servidor MCP.  
2. **Verificação de Autorização**: Os servidores MCP que implementam autorização **DEVEM** verificar TODAS as solicitações recebidas e **NÃO DEVEM** usar sessões para autenticação.  
3. **Consentimento do Utilizador**: Os servidores proxy MCP que utilizam IDs de cliente estáticos **DEVEM** obter consentimento explícito do utilizador para cada cliente registado dinamicamente.  
4. **IDs de Sessão Seguros**: Os servidores MCP **DEVEM** usar IDs de sessão criptograficamente seguros e não determinísticos, gerados com geradores de números aleatórios seguros.

## Práticas Fundamentais de Segurança

### 1. Validação e Saneamento de Entradas
- **Validação Abrangente de Entradas**: Valide e sane todas as entradas para prevenir ataques de injeção, problemas de "confused deputy" e vulnerabilidades de injeção de prompts.  
- **Aplicação de Esquemas de Parâmetros**: Implemente validação rigorosa de esquemas JSON para todos os parâmetros de ferramentas e entradas de APIs.  
- **Filtragem de Conteúdo**: Utilize Microsoft Prompt Shields e Azure Content Safety para filtrar conteúdos maliciosos em prompts e respostas.  
- **Saneamento de Saídas**: Valide e sane todas as saídas do modelo antes de apresentá-las aos utilizadores ou sistemas a jusante.

### 2. Excelência em Autenticação e Autorização  
- **Provedores de Identidade Externos**: Delegue a autenticação a provedores de identidade estabelecidos (Microsoft Entra ID, provedores OAuth 2.1) em vez de implementar autenticação personalizada.  
- **Permissões Granulares**: Implemente permissões específicas para ferramentas, seguindo o princípio do menor privilégio.  
- **Gestão do Ciclo de Vida de Tokens**: Utilize tokens de acesso de curta duração com rotação segura e validação adequada de audiência.  
- **Autenticação Multi-Fator**: Exija MFA para todo acesso administrativo e operações sensíveis.

### 3. Protocolos de Comunicação Seguros
- **Segurança na Camada de Transporte**: Utilize HTTPS/TLS 1.3 para todas as comunicações MCP com validação adequada de certificados.  
- **Criptografia de Ponta a Ponta**: Implemente camadas adicionais de criptografia para dados altamente sensíveis em trânsito e em repouso.  
- **Gestão de Certificados**: Mantenha um ciclo de vida adequado de certificados com processos automatizados de renovação.  
- **Aplicação da Versão do Protocolo**: Utilize a versão atual do protocolo MCP (2025-06-18) com negociação de versão adequada.

### 4. Limitação de Taxa Avançada e Proteção de Recursos
- **Limitação de Taxa em Múltiplas Camadas**: Implemente limitação de taxa nos níveis de utilizador, sessão, ferramenta e recurso para prevenir abusos.  
- **Limitação de Taxa Adaptativa**: Utilize limitação de taxa baseada em machine learning que se adapta a padrões de uso e indicadores de ameaça.  
- **Gestão de Quotas de Recursos**: Defina limites apropriados para recursos computacionais, uso de memória e tempo de execução.  
- **Proteção contra DDoS**: Implante sistemas abrangentes de proteção contra DDoS e análise de tráfego.

### 5. Registo e Monitorização Abrangentes
- **Registo Estruturado de Auditoria**: Implemente registos detalhados e pesquisáveis para todas as operações MCP, execuções de ferramentas e eventos de segurança.  
- **Monitorização de Segurança em Tempo Real**: Implante sistemas SIEM com deteção de anomalias baseada em IA para cargas de trabalho MCP.  
- **Registo em Conformidade com a Privacidade**: Registe eventos de segurança respeitando os requisitos e regulamentos de privacidade de dados.  
- **Integração de Resposta a Incidentes**: Conecte sistemas de registo a fluxos de trabalho automatizados de resposta a incidentes.

### 6. Práticas Avançadas de Armazenamento Seguro
- **Módulos de Segurança de Hardware**: Utilize armazenamento de chaves suportado por HSM (Azure Key Vault, AWS CloudHSM) para operações criptográficas críticas.  
- **Gestão de Chaves de Criptografia**: Implemente rotação adequada de chaves, segregação e controles de acesso para chaves de criptografia.  
- **Gestão de Segredos**: Armazene todas as chaves de API, tokens e credenciais em sistemas dedicados de gestão de segredos.  
- **Classificação de Dados**: Classifique os dados com base nos níveis de sensibilidade e aplique medidas de proteção apropriadas.

### 7. Gestão Avançada de Tokens
- **Prevenção de Passagem de Tokens**: Proíba explicitamente padrões de passagem de tokens que contornem controles de segurança.  
- **Validação de Audiência**: Verifique sempre se as declarações de audiência dos tokens correspondem à identidade do servidor MCP pretendido.  
- **Autorização Baseada em Declarações**: Implemente autorização detalhada com base em declarações de tokens e atributos de utilizadores.  
- **Vinculação de Tokens**: Vincule tokens a sessões, utilizadores ou dispositivos específicos, quando apropriado.

### 8. Gestão Segura de Sessões
- **IDs de Sessão Criptográficos**: Gere IDs de sessão usando geradores de números aleatórios criptograficamente seguros (não sequências previsíveis).  
- **Vinculação Específica ao Utilizador**: Vincule IDs de sessão a informações específicas do utilizador usando formatos seguros como `<user_id>:<session_id>`.  
- **Controles do Ciclo de Vida da Sessão**: Implemente mecanismos adequados de expiração, rotação e invalidação de sessões.  
- **Cabeçalhos de Segurança de Sessão**: Utilize cabeçalhos HTTP apropriados para proteção de sessões.

### 9. Controles de Segurança Específicos para IA
- **Defesa contra Injeção de Prompts**: Implante Microsoft Prompt Shields com técnicas de spotlighting, delimitadores e marcação de dados.  
- **Prevenção de Envenenamento de Ferramentas**: Valide metadados de ferramentas, monitorize alterações dinâmicas e verifique a integridade das ferramentas.  
- **Validação de Saídas do Modelo**: Analise as saídas do modelo para identificar possíveis vazamentos de dados, conteúdos prejudiciais ou violações de políticas de segurança.  
- **Proteção da Janela de Contexto**: Implemente controles para prevenir envenenamento e manipulação da janela de contexto.

### 10. Segurança na Execução de Ferramentas
- **Execução em Sandbox**: Execute ferramentas em ambientes isolados e containerizados com limites de recursos.  
- **Separação de Privilégios**: Execute ferramentas com os privilégios mínimos necessários e contas de serviço separadas.  
- **Isolamento de Rede**: Implemente segmentação de rede para ambientes de execução de ferramentas.  
- **Monitorização de Execução**: Monitorize a execução de ferramentas para comportamentos anómalos, uso de recursos e violações de segurança.

### 11. Validação Contínua de Segurança
- **Testes Automatizados de Segurança**: Integre testes de segurança em pipelines CI/CD com ferramentas como GitHub Advanced Security.  
- **Gestão de Vulnerabilidades**: Realize verificações regulares de todas as dependências, incluindo modelos de IA e serviços externos.  
- **Testes de Penetração**: Conduza avaliações regulares de segurança direcionadas especificamente para implementações MCP.  
- **Revisões de Código de Segurança**: Implemente revisões obrigatórias de segurança para todas as alterações de código relacionadas ao MCP.

### 12. Segurança da Cadeia de Suprimentos para IA
- **Verificação de Componentes**: Verifique a proveniência, integridade e segurança de todos os componentes de IA (modelos, embeddings, APIs).  
- **Gestão de Dependências**: Mantenha inventários atualizados de todas as dependências de software e IA com rastreamento de vulnerabilidades.  
- **Repositórios Confiáveis**: Utilize fontes verificadas e confiáveis para todos os modelos, bibliotecas e ferramentas de IA.  
- **Monitorização da Cadeia de Suprimentos**: Monitorize continuamente compromissos em provedores de serviços de IA e repositórios de modelos.

## Padrões Avançados de Segurança

### Arquitetura Zero Trust para MCP
- **Nunca Confie, Sempre Verifique**: Implemente verificação contínua para todos os participantes MCP.  
- **Microsegmentação**: Isole componentes MCP com controles granulares de rede e identidade.  
- **Acesso Condicional**: Implemente controles de acesso baseados em risco que se adaptem ao contexto e comportamento.  
- **Avaliação Contínua de Riscos**: Avalie dinamicamente a postura de segurança com base em indicadores de ameaça atuais.

### Implementação de IA com Preservação de Privacidade
- **Minimização de Dados**: Exponha apenas os dados mínimos necessários para cada operação MCP.  
- **Privacidade Diferencial**: Implemente técnicas de preservação de privacidade para processamento de dados sensíveis.  
- **Criptografia Homomórfica**: Utilize técnicas avançadas de criptografia para computação segura em dados criptografados.  
- **Aprendizagem Federada**: Implemente abordagens de aprendizagem distribuída que preservem a localidade e privacidade dos dados.

### Resposta a Incidentes para Sistemas de IA
- **Procedimentos Específicos para IA**: Desenvolva procedimentos de resposta a incidentes adaptados a ameaças específicas de IA e MCP.  
- **Resposta Automatizada**: Implemente contenção e remediação automatizadas para incidentes comuns de segurança em IA.  
- **Capacidades Forenses**: Mantenha prontidão forense para compromissos de sistemas de IA e violações de dados.  
- **Procedimentos de Recuperação**: Estabeleça procedimentos para recuperação de envenenamento de modelos de IA, ataques de injeção de prompts e compromissos de serviços.

## Recursos de Implementação e Padrões

### Documentação Oficial MCP
- [Especificação MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Especificação atual do protocolo MCP  
- [Melhores Práticas de Segurança MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Orientação oficial de segurança  
- [Especificação de Autorização MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Padrões de autenticação e autorização  
- [Segurança de Transporte MCP](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Requisitos de segurança na camada de transporte  

### Soluções de Segurança Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Proteção avançada contra injeção de prompts  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Filtragem abrangente de conteúdo de IA  
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Gestão empresarial de identidade e acesso  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Gestão segura de segredos e credenciais  
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Verificação de segurança de código e cadeia de suprimentos  

### Padrões e Estruturas de Segurança
- [Melhores Práticas de Segurança OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Orientação atual de segurança OAuth  
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Riscos de segurança em aplicações web  
- [OWASP Top 10 para LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Riscos de segurança específicos para IA  
- [Estrutura de Gestão de Riscos de IA NIST](https://www.nist.gov/itl/ai-risk-management-framework) - Gestão abrangente de riscos de IA  
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sistemas de gestão de segurança da informação  

### Guias e Tutoriais de Implementação
- [Azure API Management como Gateway de Autenticação MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Padrões empresariais de autenticação  
- [Microsoft Entra ID com Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integração com provedores de identidade  
- [Implementação de Armazenamento Seguro de Tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Melhores práticas de gestão de tokens  
- [Criptografia de Ponta a Ponta para IA](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Padrões avançados de criptografia  

### Recursos Avançados de Segurança
- [Ciclo de Vida de Desenvolvimento Seguro Microsoft](https://www.microsoft.com/sdl) - Práticas de desenvolvimento seguro  
- [Orientação de Red Team para IA](https://learn.microsoft.com/security/ai-red-team/) - Testes de segurança específicos para IA  
- [Modelagem de Ameaças para Sistemas de IA](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologia de modelagem de ameaças para IA  
- [Engenharia de Privacidade para IA](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Técnicas de preservação de privacidade em IA  

### Conformidade e Governança
- [Conformidade GDPR para IA](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Conformidade de privacidade em sistemas de IA  
- [Estrutura de Governança de IA](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementação de IA responsável  
- [SOC 2 para Serviços de IA](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Controles de segurança para provedores de serviços de IA  
- [Conformidade HIPAA para IA](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Requisitos de conformidade para IA na área da saúde  

### DevSecOps e Automação
- [Pipeline DevSecOps para IA](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Pipelines seguros de desenvolvimento de IA  
- [Testes Automatizados de Segurança](https://learn.microsoft.com/security/engineering/devsecops) - Validação contínua de segurança  
- [Segurança de Infraestrutura como Código](https://learn.microsoft.com/security/engineering/infrastructure-security) - Implantação segura de infraestrutura  
- [Segurança de Contêineres para IA](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Segurança na containerização de cargas de trabalho de IA  

### Monitorização e Resposta a Incidentes  
- [Azure Monitor para Cargas de Trabalho de IA](https://learn.microsoft.com/azure/azure-monitor/overview) - Soluções abrangentes de monitorização  
- [Resposta a Incidentes de Segurança em IA](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Procedimentos específicos para incidentes de IA  
- [SIEM para Sistemas de IA](https://learn.microsoft.com/azure/sentinel/overview) - Gestão de informações e eventos de segurança  
- [Inteligência de Ameaças para IA](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Fontes de inteligência de ameaças para IA  

## 🔄 Melhoria Contínua

### Mantenha-se Atualizado com os Padrões em Evolução
- **Atualizações da Especificação MCP**: Monitore alterações oficiais na especificação MCP e avisos de segurança.  
- **Inteligência de Ameaças**: Subscreva feeds de ameaças de segurança em IA e bases de dados de vulnerabilidades.  
- **Engajamento Comunitário**: Participe de discussões comunitárias e grupos de trabalho sobre segurança MCP.  
- **Avaliação Regular**: Realize avaliações trimestrais da postura de segurança e atualize as práticas conforme necessário.  

### Contribuindo para a Segurança MCP
- **Pesquisa em Segurança**: Contribua para pesquisas de segurança MCP e programas de divulgação de vulnerabilidades.  
- **Partilha de Melhores Práticas**: Partilhe implementações de segurança e lições aprendidas com a comunidade.  
- **Desenvolvimento de Padrões**: Participe no desenvolvimento da especificação MCP e na criação de padrões de segurança.  
- **Desenvolvimento de Ferramentas**: Desenvolver e partilhar ferramentas e bibliotecas de segurança para o ecossistema MCP

---

*Este documento reflete as melhores práticas de segurança do MCP a partir de 18 de agosto de 2025, com base na Especificação MCP 2025-06-18. As práticas de segurança devem ser regularmente revistas e atualizadas à medida que o protocolo e o panorama de ameaças evoluem.*

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte oficial. Para informações críticas, recomenda-se uma tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes do uso desta tradução.