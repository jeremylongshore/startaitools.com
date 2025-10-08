<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "68cd055621b3370948a5a1dff7bedc9a",
  "translation_date": "2025-08-26T20:30:10+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/python/README.md",
  "language_code": "ja"
}
-->
# MCP stdio サーバー - Python ソリューション

> **⚠️ 重要**: このソリューションは、MCP仕様2025-06-18で推奨される**stdioトランスポート**を使用するよう更新されています。従来のSSEトランスポートは廃止されました。

## 概要

このPythonソリューションは、現在のstdioトランスポートを使用してMCPサーバーを構築する方法を示しています。stdioトランスポートは、廃止されたSSEアプローチよりも簡単で、安全性が高く、パフォーマンスが向上しています。

## 前提条件

- Python 3.8以降
- パッケージ管理のために`uv`をインストールすることを推奨します。[インストール手順はこちら](https://docs.astral.sh/uv/#highlights)

## セットアップ手順

### ステップ1: 仮想環境を作成する

```bash
python -m venv venv
```

### ステップ2: 仮想環境を有効化する

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### ステップ3: 依存関係をインストールする

```bash
pip install mcp
```

## サーバーの実行

stdioサーバーは、従来のSSEサーバーとは異なる方法で動作します。ウェブサーバーを起動する代わりに、標準入力/標準出力を通じて通信します:

```bash
python server.py
```

**重要**: サーバーが停止しているように見えるかもしれませんが、これは正常です！標準入力からのJSON-RPCメッセージを待機しています。

## サーバーのテスト

### 方法1: MCPインスペクターを使用する (推奨)

```bash
npx @modelcontextprotocol/inspector python server.py
```

これにより以下が可能になります:
1. サーバーをサブプロセスとして起動
2. テスト用のウェブインターフェースを開く
3. サーバーツールをインタラクティブにテスト

### 方法2: JSON-RPCを直接テストする

JSON-RPCメッセージを直接送信してテストすることもできます:

1. サーバーを起動: `python server.py`
2. JSON-RPCメッセージを送信 (例):

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
```

3. サーバーが利用可能なツールを応答します

### 利用可能なツール

サーバーは以下のツールを提供します:

- **add(a, b)**: 2つの数値を加算
- **multiply(a, b)**: 2つの数値を乗算  
- **get_greeting(name)**: 個別の挨拶を生成
- **get_server_info()**: サーバー情報を取得

### Claude Desktopでのテスト

このサーバーをClaude Desktopで使用するには、以下の設定を`claude_desktop_config.json`に追加してください:

```json
{
  "mcpServers": {
    "example-stdio-server": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

## SSEとの主な違い

**stdioトランスポート (現在):**
- ✅ 簡単なセットアップ - ウェブサーバー不要
- ✅ 高いセキュリティ - HTTPエンドポイント不要
- ✅ サブプロセスベースの通信
- ✅ 標準入力/標準出力を介したJSON-RPC
- ✅ 優れたパフォーマンス

**SSEトランスポート (廃止):**
- ❌ HTTPサーバーのセットアップが必要
- ❌ ウェブフレームワーク (Starlette/FastAPI) が必要
- ❌ 複雑なルーティングとセッション管理
- ❌ 追加のセキュリティ考慮事項
- ❌ MCP 2025-06-18で廃止

## デバッグのヒント

- ログには`stderr`を使用する (決して`stdout`を使用しない)
- インスペクターを使用して視覚的にデバッグ
- すべてのJSONメッセージが改行区切りであることを確認
- サーバーがエラーなしで起動することを確認

このソリューションは現在のMCP仕様に準拠しており、stdioトランスポート実装のベストプラクティスを示しています。

---

**免責事項**:  
この文書はAI翻訳サービス[Co-op Translator](https://github.com/Azure/co-op-translator)を使用して翻訳されています。正確性を追求しておりますが、自動翻訳には誤りや不正確な部分が含まれる可能性があります。元の言語で記載された文書を正式な情報源としてお考えください。重要な情報については、専門の人間による翻訳を推奨します。この翻訳の使用に起因する誤解や誤解釈について、当社は責任を負いません。