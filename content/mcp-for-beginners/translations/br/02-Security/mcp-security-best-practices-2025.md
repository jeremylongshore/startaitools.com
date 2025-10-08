<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T17:06:41+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "br"
}
-->
# Melhores Práticas de Segurança MCP - Atualização de Agosto de 2025

> **Importante**: Este documento reflete os últimos requisitos de segurança da [Especificação MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) e as [Melhores Práticas de Segurança MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) oficiais. Sempre consulte a especificação atual para obter as orientações mais recentes.

## Práticas Essenciais de Segurança para Implementações MCP

O Protocolo de Contexto de Modelo (MCP) apresenta desafios únicos de segurança que vão além da segurança tradicional de software. Estas práticas abordam tanto os requisitos fundamentais de segurança quanto as ameaças específicas do MCP, incluindo injeção de prompts, envenenamento de ferramentas, sequestro de sessões, problemas de "confused deputy" e vulnerabilidades de passagem de tokens.

### **Requisitos de Segurança OBRIGATÓRIOS**

**Requisitos Críticos da Especificação MCP:**

> **MUST NOT**: Servidores MCP **NÃO DEVEM** aceitar tokens que não tenham sido explicitamente emitidos para o servidor MCP  
> 
> **MUST**: Servidores MCP que implementam autorização **DEVEM** verificar TODAS as solicitações recebidas  
>  
> **MUST NOT**: Servidores MCP **NÃO DEVEM** usar sessões para autenticação  
>
> **MUST**: Servidores proxy MCP que utilizam IDs de cliente estáticos **DEVEM** obter consentimento do usuário para cada cliente registrado dinamicamente  

---

## 1. **Segurança de Tokens e Autenticação**

**Controles de Autenticação e Autorização:**
   - **Revisão Rigorosa de Autorização**: Realize auditorias abrangentes da lógica de autorização do servidor MCP para garantir que apenas usuários e clientes autorizados possam acessar os recursos  
   - **Integração com Provedores de Identidade Externos**: Utilize provedores de identidade estabelecidos, como o Microsoft Entra ID, em vez de implementar autenticação personalizada  
   - **Validação de Público de Tokens**: Sempre valide se os tokens foram explicitamente emitidos para o seu servidor MCP - nunca aceite tokens de upstream  
   - **Ciclo de Vida Adequado de Tokens**: Implemente rotação segura de tokens, políticas de expiração e previna ataques de repetição de tokens  

**Armazenamento Protegido de Tokens:**
   - Use o Azure Key Vault ou armazenamentos seguros de credenciais semelhantes para todos os segredos  
   - Implemente criptografia para tokens tanto em repouso quanto em trânsito  
   - Realize rotação regular de credenciais e monitore acessos não autorizados  

## 2. **Gerenciamento de Sessões e Segurança de Transporte**

**Práticas Seguras de Sessão:**
   - **IDs de Sessão Criptograficamente Seguros**: Use IDs de sessão seguros e não determinísticos gerados com geradores de números aleatórios seguros  
   - **Vinculação Específica ao Usuário**: Vincule IDs de sessão às identidades dos usuários usando formatos como `<user_id>:<session_id>` para evitar abuso de sessões entre usuários  
   - **Gerenciamento do Ciclo de Vida da Sessão**: Implemente expiração, rotação e invalidação adequadas para limitar janelas de vulnerabilidade  
   - **Enforcement de HTTPS/TLS**: HTTPS obrigatório para todas as comunicações para evitar interceptação de IDs de sessão  

**Segurança da Camada de Transporte:**
   - Configure TLS 1.3 sempre que possível com gerenciamento adequado de certificados  
   - Implemente pinagem de certificados para conexões críticas  
   - Realize rotação regular de certificados e verificação de validade  

## 3. **Proteção Contra Ameaças Específicas de IA** 🤖

**Defesa Contra Injeção de Prompts:**
   - **Microsoft Prompt Shields**: Implante o AI Prompt Shields para detecção avançada e filtragem de instruções maliciosas  
   - **Sanitização de Entradas**: Valide e sanitize todas as entradas para evitar ataques de injeção e problemas de "confused deputy"  
   - **Delimitação de Conteúdo**: Use sistemas de delimitadores e marcação de dados para distinguir entre instruções confiáveis e conteúdo externo  

**Prevenção de Envenenamento de Ferramentas:**
   - **Validação de Metadados de Ferramentas**: Implemente verificações de integridade para definições de ferramentas e monitore alterações inesperadas  
   - **Monitoramento Dinâmico de Ferramentas**: Monitore o comportamento em tempo de execução e configure alertas para padrões de execução inesperados  
   - **Fluxos de Aprovação**: Exija aprovação explícita do usuário para modificações de ferramentas e mudanças de capacidade  

## 4. **Controle de Acesso e Permissões**

**Princípio do Menor Privilégio:**
   - Conceda aos servidores MCP apenas as permissões mínimas necessárias para a funcionalidade pretendida  
   - Implemente controle de acesso baseado em funções (RBAC) com permissões granulares  
   - Realize revisões regulares de permissões e monitore continuamente para escalonamento de privilégios  

**Controles de Permissão em Tempo de Execução:**
   - Aplique limites de recursos para evitar ataques de exaustão de recursos  
   - Use isolamento de contêineres para ambientes de execução de ferramentas  
   - Implemente acesso just-in-time para funções administrativas  

## 5. **Segurança de Conteúdo e Monitoramento**

**Implementação de Segurança de Conteúdo:**
   - **Integração com Azure Content Safety**: Use o Azure Content Safety para detectar conteúdo prejudicial, tentativas de jailbreak e violações de políticas  
   - **Análise Comportamental**: Implemente monitoramento comportamental em tempo de execução para detectar anomalias na execução do servidor MCP e ferramentas  
   - **Registro Abrangente**: Registre todas as tentativas de autenticação, invocações de ferramentas e eventos de segurança com armazenamento seguro e à prova de adulteração  

**Monitoramento Contínuo:**
   - Alertas em tempo real para padrões suspeitos e tentativas de acesso não autorizado  
   - Integração com sistemas SIEM para gerenciamento centralizado de eventos de segurança  
   - Auditorias regulares de segurança e testes de penetração das implementações MCP  

## 6. **Segurança da Cadeia de Suprimentos**

**Verificação de Componentes:**
   - **Varredura de Dependências**: Use varredura automatizada de vulnerabilidades para todas as dependências de software e componentes de IA  
   - **Validação de Proveniência**: Verifique a origem, licenciamento e integridade de modelos, fontes de dados e serviços externos  
   - **Pacotes Assinados**: Use pacotes assinados criptograficamente e verifique as assinaturas antes da implantação  

**Pipeline de Desenvolvimento Seguro:**
   - **GitHub Advanced Security**: Implemente varredura de segredos, análise de dependências e análise estática com CodeQL  
   - **Segurança de CI/CD**: Integre validação de segurança em todos os pipelines de implantação automatizados  
   - **Integridade de Artefatos**: Implemente verificação criptográfica para artefatos e configurações implantados  

## 7. **Segurança OAuth e Prevenção de "Confused Deputy"**

**Implementação de OAuth 2.1:**
   - **Implementação de PKCE**: Use Proof Key for Code Exchange (PKCE) para todas as solicitações de autorização  
   - **Consentimento Explícito**: Obtenha consentimento do usuário para cada cliente registrado dinamicamente para evitar ataques de "confused deputy"  
   - **Validação de URI de Redirecionamento**: Implemente validação rigorosa de URIs de redirecionamento e identificadores de cliente  

**Segurança de Proxy:**
   - Prevenir bypass de autorização por meio de exploração de IDs de cliente estáticos  
   - Implemente fluxos de consentimento adequados para acesso a APIs de terceiros  
   - Monitore roubo de códigos de autorização e acessos não autorizados a APIs  

## 8. **Resposta a Incidentes e Recuperação**

**Capacidades de Resposta Rápida:**
   - **Resposta Automatizada**: Implemente sistemas automatizados para rotação de credenciais e contenção de ameaças  
   - **Procedimentos de Reversão**: Capacidade de reverter rapidamente para configurações e componentes conhecidos como seguros  
   - **Capacidades Forenses**: Trilhas de auditoria detalhadas e registros para investigação de incidentes  

**Comunicação e Coordenação:**
   - Procedimentos claros de escalonamento para incidentes de segurança  
   - Integração com equipes organizacionais de resposta a incidentes  
   - Simulações regulares de incidentes de segurança e exercícios de mesa  

## 9. **Conformidade e Governança**

**Conformidade Regulatória:**
   - Garanta que as implementações MCP atendam aos requisitos específicos do setor (GDPR, HIPAA, SOC 2)  
   - Implemente controles de classificação de dados e privacidade para processamento de dados de IA  
   - Mantenha documentação abrangente para auditorias de conformidade  

**Gerenciamento de Mudanças:**
   - Processos formais de revisão de segurança para todas as modificações do sistema MCP  
   - Controle de versão e fluxos de aprovação para alterações de configuração  
   - Avaliações regulares de conformidade e análise de lacunas  

## 10. **Controles Avançados de Segurança**

**Arquitetura Zero Trust:**
   - **Nunca Confie, Sempre Verifique**: Verificação contínua de usuários, dispositivos e conexões  
   - **Microsegmentação**: Controles granulares de rede isolando componentes individuais do MCP  
   - **Acesso Condicional**: Controles de acesso baseados em risco que se adaptam ao contexto e comportamento atuais  

**Proteção de Aplicações em Tempo de Execução:**
   - **Proteção de Aplicações em Tempo de Execução (RASP)**: Implante técnicas de RASP para detecção de ameaças em tempo real  
   - **Monitoramento de Desempenho de Aplicações**: Monitore anomalias de desempenho que possam indicar ataques  
   - **Políticas de Segurança Dinâmicas**: Implemente políticas de segurança que se adaptem com base no cenário atual de ameaças  

## 11. **Integração com o Ecossistema de Segurança da Microsoft**

**Segurança Abrangente da Microsoft:**
   - **Microsoft Defender for Cloud**: Gerenciamento de postura de segurança na nuvem para cargas de trabalho MCP  
   - **Azure Sentinel**: Capacidades nativas de SIEM e SOAR para detecção avançada de ameaças  
   - **Microsoft Purview**: Governança de dados e conformidade para fluxos de trabalho de IA e fontes de dados  

**Gerenciamento de Identidade e Acesso:**
   - **Microsoft Entra ID**: Gerenciamento de identidade empresarial com políticas de acesso condicional  
   - **Privileged Identity Management (PIM)**: Acesso just-in-time e fluxos de aprovação para funções administrativas  
   - **Proteção de Identidade**: Acesso condicional baseado em risco e resposta automatizada a ameaças  

## 12. **Evolução Contínua da Segurança**

**Manter-se Atualizado:**
   - **Monitoramento de Especificações**: Revisão regular de atualizações da especificação MCP e mudanças nas orientações de segurança  
   - **Inteligência de Ameaças**: Integração de feeds de ameaças específicas de IA e indicadores de comprometimento  
   - **Engajamento com a Comunidade de Segurança**: Participação ativa na comunidade de segurança MCP e programas de divulgação de vulnerabilidades  

**Segurança Adaptativa:**
   - **Segurança Baseada em Machine Learning**: Use detecção de anomalias baseada em ML para identificar padrões de ataque novos  
   - **Análise de Segurança Preditiva**: Implemente modelos preditivos para identificação proativa de ameaças  
   - **Automação de Segurança**: Atualizações automatizadas de políticas de segurança com base em inteligência de ameaças e mudanças na especificação  

---

## **Recursos Críticos de Segurança**

### **Documentação Oficial MCP**
- [Especificação MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Melhores Práticas de Segurança MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Especificação de Autorização MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Soluções de Segurança da Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Segurança do Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Padrões de Segurança**
- [Melhores Práticas de Segurança OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 para Modelos de Linguagem Grande](https://genai.owasp.org/)  
- [Framework de Gerenciamento de Riscos de IA do NIST](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Guias de Implementação**
- [Gateway de Autenticação MCP do Azure API Management](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID com Servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Aviso de Segurança**: As práticas de segurança do MCP evoluem rapidamente. Sempre verifique a [especificação MCP](https://spec.modelcontextprotocol.io/) e a [documentação oficial de segurança](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) antes da implementação.

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autoritativa. Para informações críticas, recomenda-se a tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações equivocadas decorrentes do uso desta tradução.