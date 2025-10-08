<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "e9490aedc71f99bc774af57b207a7adb",
  "translation_date": "2025-07-13T21:45:46+00:00",
  "source_file": "03-GettingStarted/07-aitk/solution/README.md",
  "language_code": "ja"
}
-->
# 📘 課題解答：電卓MCPサーバーに平方根ツールを追加する

## 概要
この課題では、電卓MCPサーバーに数値の平方根を計算する新しいツールを追加しました。この追加により、AIエージェントは「16の平方根は？」や「√49を計算して」といった自然言語の質問に対応できるようになります。

## 🛠️ 平方根ツールの実装
この機能を追加するために、server.pyファイルに新しいツール関数を定義しました。実装は以下の通りです。

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

## 🔍 動作の仕組み

- **`math`モジュールのインポート**：基本的な算術演算を超えた数学的操作を行うために、Pythonには組み込みの`math`モジュールがあります。このモジュールには様々な数学関数や定数が含まれており、`import math`でインポートすることで、平方根を計算する`math.sqrt()`などの関数が使えるようになります。
- **関数定義**：`@server.tool()`デコレーターによって、`sqrt`関数がAIエージェントから利用可能なツールとして登録されます。
- **入力パラメータ**：関数は`float`型の引数`a`を1つ受け取ります。
- **エラーハンドリング**：`a`が負の値の場合、`math.sqrt()`では平方根を計算できないため、`ValueError`を発生させて処理を中断します。
- **戻り値**：非負の入力に対しては、Pythonの組み込み関数`math.sqrt()`を使って平方根を計算し、その結果を返します。

## 🔄 サーバーの再起動
新しい`sqrt`ツールを追加した後は、MCPサーバーを再起動して、エージェントが新機能を認識し利用できるようにしてください。

## 💬 新ツールを試すための例文
平方根機能をテストするための自然言語の例文は以下の通りです。

- 「25の平方根は何ですか？」
- 「81の平方根を計算して。」
- 「0の平方根を教えて。」
- 「2.25の平方根は？」

これらのプロンプトにより、エージェントが`sqrt`ツールを呼び出し、正しい結果を返します。

## ✅ まとめ
この課題を通じて、以下のことができるようになりました。

- 電卓MCPサーバーに新しい`sqrt`ツールを追加した。
- AIエージェントが自然言語の指示で平方根計算を行えるようにした。
- 新しいツールの追加とサーバー再起動による機能統合を実践した。

さらに、べき乗や対数関数など、他の数学ツールを追加してエージェントの機能を拡張することもぜひ試してみてください！

**免責事項**：  
本書類はAI翻訳サービス「[Co-op Translator](https://github.com/Azure/co-op-translator)」を使用して翻訳されました。正確性には努めておりますが、自動翻訳には誤りや不正確な部分が含まれる可能性があります。原文の言語による文書が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じた誤解や誤訳について、当方は一切の責任を負いかねます。