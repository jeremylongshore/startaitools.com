<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T17:10:32+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "br"
}
-->
# Melhores Práticas de Segurança MCP 2025

Este guia abrangente descreve as melhores práticas essenciais de segurança para a implementação de sistemas Model Context Protocol (MCP) com base na mais recente **Especificação MCP 2025-06-18** e nos padrões atuais da indústria. Essas práticas abordam tanto preocupações tradicionais de segurança quanto ameaças específicas de IA exclusivas para implantações MCP.

## Requisitos Críticos de Segurança

### Controles de Segurança Obrigatórios (Requisitos MUST)

1. **Validação de Token**: Servidores MCP **NÃO DEVEM** aceitar tokens que não foram explicitamente emitidos para o próprio servidor MCP.
2. **Verificação de Autorização**: Servidores MCP que implementam autorização **DEVEM** verificar TODAS as solicitações recebidas e **NÃO DEVEM** usar sessões para autenticação.  
3. **Consentimento do Usuário**: Servidores proxy MCP que utilizam IDs de cliente estáticos **DEVEM** obter consentimento explícito do usuário para cada cliente registrado dinamicamente.
4. **IDs de Sessão Seguros**: Servidores MCP **DEVEM** usar IDs de sessão criptograficamente seguros e não determinísticos, gerados com geradores de números aleatórios seguros.

## Práticas Fundamentais de Segurança

### 1. Validação e Sanitização de Entrada
- **Validação Abrangente de Entrada**: Valide e sanitize todas as entradas para prevenir ataques de injeção, problemas de confusão de autoridade e vulnerabilidades de injeção de prompts.
- **Aplicação de Esquema de Parâmetros**: Implemente validação rigorosa de esquema JSON para todos os parâmetros de ferramentas e entradas de API.
- **Filtragem de Conteúdo**: Utilize Microsoft Prompt Shields e Azure Content Safety para filtrar conteúdo malicioso em prompts e respostas.
- **Sanitização de Saída**: Valide e sanitize todas as saídas do modelo antes de apresentá-las aos usuários ou sistemas subsequentes.

### 2. Excelência em Autenticação e Autorização  
- **Provedores de Identidade Externos**: Delegue a autenticação a provedores de identidade estabelecidos (Microsoft Entra ID, provedores OAuth 2.1) em vez de implementar autenticação personalizada.
- **Permissões Granulares**: Implemente permissões específicas para ferramentas seguindo o princípio do menor privilégio.
- **Gerenciamento de Ciclo de Vida de Tokens**: Utilize tokens de acesso de curta duração com rotação segura e validação adequada de público.
- **Autenticação Multifator**: Exija MFA para todo acesso administrativo e operações sensíveis.

### 3. Protocolos de Comunicação Seguros
- **Segurança da Camada de Transporte**: Utilize HTTPS/TLS 1.3 para todas as comunicações MCP com validação adequada de certificados.
- **Criptografia de Ponta a Ponta**: Implemente camadas adicionais de criptografia para dados altamente sensíveis em trânsito e em repouso.
- **Gerenciamento de Certificados**: Mantenha o ciclo de vida adequado de certificados com processos automatizados de renovação.
- **Aplicação de Versão de Protocolo**: Utilize a versão atual do protocolo MCP (2025-06-18) com negociação adequada de versão.

### 4. Limitação de Taxa Avançada e Proteção de Recursos
- **Limitação de Taxa em Múltiplas Camadas**: Implemente limitação de taxa nos níveis de usuário, sessão, ferramenta e recurso para prevenir abusos.
- **Limitação de Taxa Adaptativa**: Utilize limitação de taxa baseada em aprendizado de máquina que se adapta a padrões de uso e indicadores de ameaça.
- **Gerenciamento de Cotas de Recursos**: Defina limites apropriados para recursos computacionais, uso de memória e tempo de execução.
- **Proteção contra DDoS**: Implante sistemas abrangentes de proteção contra DDoS e análise de tráfego.

### 5. Registro e Monitoramento Abrangentes
- **Registro Estruturado de Auditoria**: Implemente logs detalhados e pesquisáveis para todas as operações MCP, execuções de ferramentas e eventos de segurança.
- **Monitoramento de Segurança em Tempo Real**: Implante sistemas SIEM com detecção de anomalias baseada em IA para cargas de trabalho MCP.
- **Registro Compatível com Privacidade**: Registre eventos de segurança respeitando os requisitos e regulamentos de privacidade de dados.
- **Integração de Resposta a Incidentes**: Conecte sistemas de registro a fluxos de trabalho automatizados de resposta a incidentes.

### 6. Práticas Avançadas de Armazenamento Seguro
- **Módulos de Segurança de Hardware**: Utilize armazenamento de chaves respaldado por HSM (Azure Key Vault, AWS CloudHSM) para operações criptográficas críticas.
- **Gerenciamento de Chaves de Criptografia**: Implemente rotação adequada de chaves, segregação e controles de acesso para chaves de criptografia.
- **Gerenciamento de Segredos**: Armazene todas as chaves de API, tokens e credenciais em sistemas dedicados de gerenciamento de segredos.
- **Classificação de Dados**: Classifique os dados com base nos níveis de sensibilidade e aplique medidas de proteção apropriadas.

### 7. Gerenciamento Avançado de Tokens
- **Prevenção de Passagem de Tokens**: Proíba explicitamente padrões de passagem de tokens que contornem controles de segurança.
- **Validação de Público**: Sempre verifique se as declarações de público do token correspondem à identidade do servidor MCP pretendido.
- **Autorização Baseada em Declarações**: Implemente autorização granular baseada em declarações de tokens e atributos de usuários.
- **Vinculação de Tokens**: Vincule tokens a sessões, usuários ou dispositivos específicos, quando apropriado.

### 8. Gerenciamento Seguro de Sessões
- **IDs de Sessão Criptográficos**: Gere IDs de sessão usando geradores de números aleatórios criptograficamente seguros (não sequências previsíveis).
- **Vinculação Específica ao Usuário**: Vincule IDs de sessão a informações específicas do usuário usando formatos seguros como `<user_id>:<session_id>`.
- **Controles de Ciclo de Vida de Sessões**: Implemente mecanismos adequados de expiração, rotação e invalidação de sessões.
- **Cabeçalhos de Segurança de Sessão**: Utilize cabeçalhos HTTP apropriados para proteção de sessões.

### 9. Controles de Segurança Específicos de IA
- **Defesa contra Injeção de Prompts**: Implante Microsoft Prompt Shields com técnicas de destaque, delimitadores e marcação de dados.
- **Prevenção de Envenenamento de Ferramentas**: Valide metadados de ferramentas, monitore mudanças dinâmicas e verifique a integridade das ferramentas.
- **Validação de Saída do Modelo**: Analise as saídas do modelo para possíveis vazamentos de dados, conteúdo prejudicial ou violações de políticas de segurança.
- **Proteção da Janela de Contexto**: Implemente controles para prevenir envenenamento da janela de contexto e ataques de manipulação.

### 10. Segurança na Execução de Ferramentas
- **Execução em Ambientes Isolados**: Execute ferramentas em ambientes containerizados e isolados com limites de recursos.
- **Separação de Privilégios**: Execute ferramentas com os privilégios mínimos necessários e contas de serviço separadas.
- **Isolamento de Rede**: Implemente segmentação de rede para ambientes de execução de ferramentas.
- **Monitoramento de Execução**: Monitore a execução de ferramentas para comportamento anômalo, uso de recursos e violações de segurança.

### 11. Validação Contínua de Segurança
- **Testes Automatizados de Segurança**: Integre testes de segurança em pipelines CI/CD com ferramentas como GitHub Advanced Security.
- **Gerenciamento de Vulnerabilidades**: Escaneie regularmente todas as dependências, incluindo modelos de IA e serviços externos.
- **Testes de Penetração**: Realize avaliações regulares de segurança especificamente direcionadas às implementações MCP.
- **Revisões de Código de Segurança**: Implemente revisões obrigatórias de segurança para todas as alterações de código relacionadas ao MCP.

### 12. Segurança da Cadeia de Suprimentos para IA
- **Verificação de Componentes**: Verifique a proveniência, integridade e segurança de todos os componentes de IA (modelos, embeddings, APIs).
- **Gerenciamento de Dependências**: Mantenha inventários atualizados de todas as dependências de software e IA com rastreamento de vulnerabilidades.
- **Repositórios Confiáveis**: Utilize fontes verificadas e confiáveis para todos os modelos de IA, bibliotecas e ferramentas.
- **Monitoramento da Cadeia de Suprimentos**: Monitore continuamente compromissos em provedores de serviços de IA e repositórios de modelos.

## Padrões Avançados de Segurança

### Arquitetura Zero Trust para MCP
- **Nunca Confie, Sempre Verifique**: Implemente verificação contínua para todos os participantes MCP.
- **Micro-segmentação**: Isole componentes MCP com controles granulares de rede e identidade.
- **Acesso Condicional**: Implemente controles de acesso baseados em risco que se adaptem ao contexto e comportamento.
- **Avaliação Contínua de Riscos**: Avalie dinamicamente a postura de segurança com base em indicadores de ameaça atuais.

### Implementação de IA Preservadora de Privacidade
- **Minimização de Dados**: Exponha apenas os dados mínimos necessários para cada operação MCP.
- **Privacidade Diferencial**: Implemente técnicas de preservação de privacidade para processamento de dados sensíveis.
- **Criptografia Homomórfica**: Utilize técnicas avançadas de criptografia para computação segura em dados criptografados.
- **Aprendizado Federado**: Implemente abordagens de aprendizado distribuído que preservem a localidade e privacidade dos dados.

### Resposta a Incidentes para Sistemas de IA
- **Procedimentos Específicos de Incidentes de IA**: Desenvolva procedimentos de resposta a incidentes adaptados a ameaças específicas de IA e MCP.
- **Resposta Automatizada**: Implemente contenção e remediação automatizadas para incidentes comuns de segurança de IA.  
- **Capacidades Forenses**: Mantenha prontidão forense para compromissos de sistemas de IA e violações de dados.
- **Procedimentos de Recuperação**: Estabeleça procedimentos para recuperação de envenenamento de modelos de IA, ataques de injeção de prompts e compromissos de serviços.

## Recursos de Implementação e Padrões

### Documentação Oficial MCP
- [Especificação MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Especificação atual do protocolo MCP
- [Melhores Práticas de Segurança MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Orientação oficial de segurança
- [Especificação de Autorização MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Padrões de autenticação e autorização
- [Segurança de Transporte MCP](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Requisitos de segurança da camada de transporte

### Soluções de Segurança Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Proteção avançada contra injeção de prompts
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Filtragem abrangente de conteúdo de IA
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Gerenciamento de identidade e acesso empresarial
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Gerenciamento seguro de segredos e credenciais
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Escaneamento de segurança de código e cadeia de suprimentos

### Padrões e Estruturas de Segurança
- [Melhores Práticas de Segurança OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Orientação atual de segurança OAuth
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Riscos de segurança de aplicativos web
- [OWASP Top 10 para LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Riscos de segurança específicos de IA
- [Estrutura de Gerenciamento de Riscos de IA NIST](https://www.nist.gov/itl/ai-risk-management-framework) - Gerenciamento abrangente de riscos de IA
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Sistemas de gerenciamento de segurança da informação

### Guias e Tutoriais de Implementação
- [Azure API Management como Gateway de Autenticação MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Padrões de autenticação empresarial
- [Microsoft Entra ID com Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Integração de provedores de identidade
- [Implementação de Armazenamento Seguro de Tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Melhores práticas de gerenciamento de tokens
- [Criptografia de Ponta a Ponta para IA](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Padrões avançados de criptografia

### Recursos Avançados de Segurança
- [Ciclo de Vida de Desenvolvimento Seguro Microsoft](https://www.microsoft.com/sdl) - Práticas de desenvolvimento seguro
- [Orientação de Red Team para IA](https://learn.microsoft.com/security/ai-red-team/) - Testes de segurança específicos de IA
- [Modelagem de Ameaças para Sistemas de IA](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Metodologia de modelagem de ameaças de IA
- [Engenharia de Privacidade para IA](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Técnicas de preservação de privacidade em IA

### Conformidade e Governança
- [Conformidade GDPR para IA](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Conformidade de privacidade em sistemas de IA
- [Estrutura de Governança de IA](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Implementação de IA responsável
- [SOC 2 para Serviços de IA](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Controles de segurança para provedores de serviços de IA
- [Conformidade HIPAA para IA](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Requisitos de conformidade de IA para saúde

### DevSecOps e Automação
- [Pipeline DevSecOps para IA](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Pipelines de desenvolvimento seguro para IA
- [Testes Automatizados de Segurança](https://learn.microsoft.com/security/engineering/devsecops) - Validação contínua de segurança
- [Segurança de Infraestrutura como Código](https://learn.microsoft.com/security/engineering/infrastructure-security) - Implantação segura de infraestrutura
- [Segurança de Contêineres para IA](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - Segurança na containerização de cargas de trabalho de IA

### Monitoramento e Resposta a Incidentes  
- [Azure Monitor para Cargas de Trabalho de IA](https://learn.microsoft.com/azure/azure-monitor/overview) - Soluções abrangentes de monitoramento
- [Resposta a Incidentes de Segurança de IA](https://learn.microsoft.com/security/compass/incident-response-playbooks) - Procedimentos específicos de incidentes de IA
- [SIEM para Sistemas de IA](https://learn.microsoft.com/azure/sentinel/overview) - Gerenciamento de informações e eventos de segurança
- [Inteligência de Ameaças para IA](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - Fontes de inteligência de ameaças para IA

## 🔄 Melhoria Contínua

### Mantenha-se Atualizado com Padrões em Evolução
- **Atualizações da Especificação MCP**: Monitore mudanças oficiais na especificação MCP e avisos de segurança.
- **Inteligência de Ameaças**: Assine feeds de ameaças de segurança de IA e bancos de dados de vulnerabilidades.  
- **Engajamento Comunitário**: Participe de discussões e grupos de trabalho da comunidade de segurança MCP.
- **Avaliação Regular**: Realize avaliações trimestrais de postura de segurança e atualize as práticas conforme necessário.

### Contribuindo para a Segurança MCP
- **Pesquisa de Segurança**: Contribua para pesquisas de segurança MCP e programas de divulgação de vulnerabilidades.
- **Compartilhamento de Melhores Práticas**: Compartilhe implementações de segurança e lições aprendidas com a comunidade.
- **Desenvolvimento de Padrões**: Participe do desenvolvimento de especificações MCP e criação de padrões de segurança.
- **Desenvolvimento de Ferramentas**: Desenvolver e compartilhar ferramentas e bibliotecas de segurança para o ecossistema MCP

---

*Este documento reflete as melhores práticas de segurança do MCP em 18 de agosto de 2025, com base na Especificação MCP 2025-06-18. As práticas de segurança devem ser revisadas e atualizadas regularmente conforme o protocolo e o cenário de ameaças evoluem.*

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte oficial. Para informações críticas, recomenda-se a tradução profissional feita por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações equivocadas decorrentes do uso desta tradução.