<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e378b47e0361b7a9b0dab7a0306878c8",
  "translation_date": "2025-08-26T20:01:08+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/README.md",
  "language_code": "pt"
}
-->
# Soluções de Servidor MCP stdio

> **⚠️ Importante**: Estas soluções foram atualizadas para utilizar o **transporte stdio** conforme recomendado pela Especificação MCP 2025-06-18. O transporte original SSE (Server-Sent Events) foi descontinuado.

Aqui estão as soluções completas para construir servidores MCP utilizando o transporte stdio em cada runtime:

- [TypeScript](../../../../../03-GettingStarted/05-stdio-server/solution/typescript) - Implementação completa de servidor stdio
- [Python](../../../../../03-GettingStarted/05-stdio-server/solution/python) - Servidor stdio em Python com asyncio
- [.NET](../../../../../03-GettingStarted/05-stdio-server/solution/dotnet) - Servidor stdio em .NET com injeção de dependências

Cada solução demonstra:
- Configuração do transporte stdio
- Definição de ferramentas do servidor
- Manipulação adequada de mensagens JSON-RPC
- Integração com clientes MCP como Claude

Todas as soluções seguem a especificação atual do MCP e utilizam o transporte stdio recomendado para desempenho e segurança ideais.

---

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, é importante notar que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autoritária. Para informações críticas, recomenda-se a tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes da utilização desta tradução.