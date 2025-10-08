<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:52:01+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "br"
}
-->
# 📘 Solução da Tarefa: Expandindo Seu Servidor MCP da Calculadora com uma Ferramenta de Raiz Quadrada

## Visão Geral
Nesta tarefa, você aprimorou seu servidor MCP da calculadora adicionando uma nova ferramenta que calcula a raiz quadrada de um número. Essa adição permite que seu agente de IA lide com consultas matemáticas mais avançadas, como "Qual é a raiz quadrada de 16?" ou "Calcule √49", usando comandos em linguagem natural.

## 🛠️ Implementando a Ferramenta de Raiz Quadrada
Para adicionar essa funcionalidade, você definiu uma nova função de ferramenta no seu arquivo server.py. Veja a implementação:

```python
"""
Sample MCP Calculator Server implementation in Python.

This module demonstrates how to create a simple MCP server with calculator tools
that can perform basic arithmetic operations (add, subtract, multiply, divide).
"""

from mcp.server.fastmcp import FastMCP
import math

server = FastMCP("calculator")

@server.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together and return the result."""
    return a + b

@server.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the result."""
    return a - b

@server.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together and return the result."""
    return a * b

@server.tool()
def divide(a: float, b: float) -> float:
    """
    Divide a by b and return the result.
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@server.tool()
def sqrt(a: float) -> float:
    """
    Return the square root of a.

    Raises:
        ValueError: If a is negative.
    """
    if a < 0:
        raise ValueError("Cannot compute the square root of a negative number.")
    return math.sqrt(a)
```

## 🔍 Como Funciona

- **Importar o módulo `math`**: Para realizar operações matemáticas além da aritmética básica, o Python oferece o módulo embutido `math`. Esse módulo inclui diversas funções e constantes matemáticas. Ao importá-lo com `import math`, você tem acesso a funções como `math.sqrt()`, que calcula a raiz quadrada de um número.
- **Definição da Função**: O decorador `@server.tool()` registra a função `sqrt` como uma ferramenta acessível pelo seu agente de IA.
- **Parâmetro de Entrada**: A função recebe um único argumento `a` do tipo `float`.
- **Tratamento de Erros**: Se `a` for negativo, a função lança um `ValueError` para evitar calcular a raiz quadrada de um número negativo, o que não é suportado pela função `math.sqrt()`.
- **Valor de Retorno**: Para entradas não negativas, a função retorna a raiz quadrada de `a` usando o método `math.sqrt()` do Python.

## 🔄 Reiniciando o Servidor
Após adicionar a nova ferramenta `sqrt`, é fundamental reiniciar seu servidor MCP para garantir que o agente reconheça e possa utilizar a funcionalidade recém-adicionada.

## 💬 Exemplos de Comandos para Testar a Nova Ferramenta
Aqui estão alguns comandos em linguagem natural que você pode usar para testar a funcionalidade da raiz quadrada:

- "Qual é a raiz quadrada de 25?"
- "Calcule a raiz quadrada de 81."
- "Encontre a raiz quadrada de 0."
- "Qual é a raiz quadrada de 2,25?"

Esses comandos devem fazer com que o agente invoque a ferramenta `sqrt` e retorne os resultados corretos.

## ✅ Resumo
Ao concluir esta tarefa, você:

- Expandiu seu servidor MCP da calculadora com uma nova ferramenta `sqrt`.
- Permitiu que seu agente de IA realizasse cálculos de raiz quadrada por meio de comandos em linguagem natural.
- Praticou a adição de novas ferramentas e o reinício do servidor para integrar funcionalidades adicionais.

Sinta-se à vontade para experimentar mais, adicionando outras ferramentas matemáticas, como exponenciação ou funções logarítmicas, para continuar aprimorando as capacidades do seu agente!

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.