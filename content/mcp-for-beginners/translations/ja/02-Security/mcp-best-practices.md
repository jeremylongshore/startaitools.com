<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T11:12:47+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "ja"
}
-->
# MCPセキュリティベストプラクティス2025

この包括的なガイドは、最新の**MCP仕様2025-06-18**および現在の業界標準に基づいて、Model Context Protocol (MCP)システムを実装する際の重要なセキュリティベストプラクティスを概説しています。これらのプラクティスは、従来のセキュリティ懸念だけでなく、MCP導入に特有のAI関連の脅威にも対応しています。

## 重要なセキュリティ要件

### 必須セキュリティコントロール (MUST要件)

1. **トークン検証**: MCPサーバーは、MCPサーバー自身のために明示的に発行されていないトークンを**受け入れてはならない**
2. **認可の検証**: 認可を実装するMCPサーバーは、すべての受信リクエストを**検証しなければならず**、認証にセッションを使用しては**ならない**  
3. **ユーザーの同意**: 静的なクライアントIDを使用するMCPプロキシサーバーは、動的に登録されたクライアントごとに明示的なユーザーの同意を得なければならない
4. **セッションIDのセキュリティ**: MCPサーバーは、暗号的に安全で非決定論的なセッションIDを、安全な乱数生成器を使用して生成しなければならない

## コアセキュリティプラクティス

### 1. 入力の検証とサニタイズ
- **包括的な入力検証**: インジェクション攻撃、混乱した代理問題、プロンプトインジェクションの脆弱性を防ぐために、すべての入力を検証しサニタイズする
- **パラメータスキーマの強制**: すべてのツールパラメータとAPI入力に対して厳密なJSONスキーマ検証を実施する
- **コンテンツフィルタリング**: Microsoft Prompt ShieldsおよびAzure Content Safetyを使用して、プロンプトや応答内の悪意のあるコンテンツをフィルタリングする
- **出力のサニタイズ**: ユーザーや下流システムに提示する前に、すべてのモデル出力を検証しサニタイズする

### 2. 認証と認可の優秀性
- **外部アイデンティティプロバイダー**: カスタム認証を実装するのではなく、Microsoft Entra IDやOAuth 2.1プロバイダーなどの確立されたアイデンティティプロバイダーに認証を委任する
- **細かい権限管理**: 最小権限の原則に従い、ツール固有の細かい権限を実装する
- **トークンライフサイクル管理**: 短命のアクセストークンを使用し、安全なローテーションと適切なオーディエンス検証を行う
- **多要素認証**: すべての管理アクセスおよび機密操作にMFAを要求する

### 3. 安全な通信プロトコル
- **トランスポート層セキュリティ**: 適切な証明書検証を伴うHTTPS/TLS 1.3をすべてのMCP通信に使用する
- **エンドツーエンド暗号化**: 移動中および保存中の非常に機密性の高いデータに対して追加の暗号化層を実装する
- **証明書管理**: 自動更新プロセスを伴う適切な証明書ライフサイクル管理を維持する
- **プロトコルバージョンの強制**: 適切なバージョン交渉を伴う最新のMCPプロトコルバージョン (2025-06-18) を使用する

### 4. 高度なレート制限とリソース保護
- **多層レート制限**: ユーザー、セッション、ツール、リソースレベルでレート制限を実装し、悪用を防ぐ
- **適応型レート制限**: 使用パターンや脅威指標に適応する機械学習ベースのレート制限を使用する
- **リソースクォータ管理**: 計算リソース、メモリ使用量、実行時間に適切な制限を設定する
- **DDoS保護**: 包括的なDDoS保護とトラフィック分析システムを展開する

### 5. 包括的なログ記録と監視
- **構造化された監査ログ**: すべてのMCP操作、ツール実行、セキュリティイベントに対して詳細で検索可能なログを実装する
- **リアルタイムセキュリティ監視**: AIを活用した異常検知を備えたSIEMシステムをMCPワークロードに展開する
- **プライバシー準拠のログ記録**: データプライバシー要件や規制を尊重しながらセキュリティイベントをログに記録する
- **インシデント対応の統合**: ログ記録システムを自動化されたインシデント対応ワークフローに接続する

### 6. 強化された安全なストレージプラクティス
- **ハードウェアセキュリティモジュール**: 重要な暗号操作に対してHSMバックのキー保管 (Azure Key Vault、AWS CloudHSM) を使用する
- **暗号化キー管理**: 暗号化キーの適切なローテーション、分離、アクセス制御を実施する
- **秘密管理**: すべてのAPIキー、トークン、資格情報を専用の秘密管理システムに保管する
- **データ分類**: 機密性レベルに基づいてデータを分類し、適切な保護措置を適用する

### 7. 高度なトークン管理
- **トークンパススルー防止**: セキュリティコントロールを回避するトークンパススルーパターンを明示的に禁止する
- **オーディエンス検証**: トークンのオーディエンスクレームが意図されたMCPサーバーのアイデンティティと一致することを常に検証する
- **クレームベースの認可**: トークンクレームやユーザー属性に基づいた細かい認可を実装する
- **トークンバインディング**: 必要に応じてトークンを特定のセッション、ユーザー、デバイスにバインドする

### 8. 安全なセッション管理
- **暗号的セッションID**: 暗号的に安全な乱数生成器を使用してセッションIDを生成する (予測可能なシーケンスは使用しない)
- **ユーザー固有のバインディング**: `<user_id>:<session_id>`のような安全な形式を使用してセッションIDをユーザー固有の情報にバインドする
- **セッションライフサイクルコントロール**: 適切なセッションの有効期限、ローテーション、無効化メカニズムを実装する
- **セッションセキュリティヘッダー**: セッション保護のために適切なHTTPセキュリティヘッダーを使用する

### 9. AI特有のセキュリティコントロール
- **プロンプトインジェクション防御**: Microsoft Prompt Shieldsを展開し、スポットライティング、デリミタ、データマーキング技術を使用する
- **ツールの毒性防止**: ツールのメタデータを検証し、動的な変更を監視し、ツールの整合性を確認する
- **モデル出力の検証**: データ漏洩、有害なコンテンツ、セキュリティポリシー違反の可能性があるモデル出力をスキャンする
- **コンテキストウィンドウ保護**: コンテキストウィンドウの毒性や操作攻撃を防ぐためのコントロールを実装する

### 10. ツール実行のセキュリティ
- **実行のサンドボックス化**: リソース制限を伴うコンテナ化された隔離環境でツールを実行する
- **権限分離**: 最小限の必要権限でツールを実行し、サービスアカウントを分離する
- **ネットワーク隔離**: ツール実行環境のネットワークセグメンテーションを実装する
- **実行監視**: ツール実行の異常な動作、リソース使用量、セキュリティ違反を監視する

### 11. 継続的なセキュリティ検証
- **自動セキュリティテスト**: GitHub Advanced Securityなどのツールを使用してCI/CDパイプラインにセキュリティテストを統合する
- **脆弱性管理**: AIモデルや外部サービスを含むすべての依存関係を定期的にスキャンする
- **ペネトレーションテスト**: MCP実装を対象とした定期的なセキュリティ評価を実施する
- **セキュリティコードレビュー**: MCP関連のコード変更に対して必須のセキュリティレビューを実施する

### 12. AIのサプライチェーンセキュリティ
- **コンポーネント検証**: すべてのAIコンポーネント (モデル、埋め込み、API) の出所、整合性、セキュリティを検証する
- **依存関係管理**: 脆弱性追跡を伴うすべてのソフトウェアおよびAI依存関係の最新インベントリを維持する
- **信頼できるリポジトリ**: すべてのAIモデル、ライブラリ、ツールに対して検証済みの信頼できるソースを使用する
- **サプライチェーン監視**: AIサービスプロバイダーやモデルリポジトリの妥協を継続的に監視する

## 高度なセキュリティパターン

### MCPのゼロトラストアーキテクチャ
- **信頼せず、常に検証**: すべてのMCP参加者に対して継続的な検証を実施する
- **マイクロセグメンテーション**: MCPコンポーネントを細かいネットワークおよびアイデンティティコントロールで分離する
- **条件付きアクセス**: コンテキストや行動に適応するリスクベースのアクセスコントロールを実装する
- **継続的なリスク評価**: 現在の脅威指標に基づいてセキュリティ態勢を動的に評価する

### プライバシー保護型AI実装
- **データ最小化**: 各MCP操作に必要最小限のデータのみを公開する
- **差分プライバシー**: 機密データ処理にプライバシー保護技術を実装する
- **準同型暗号化**: 暗号化されたデータ上で安全な計算を行うための高度な暗号化技術を使用する
- **フェデレーテッドラーニング**: データの局所性とプライバシーを維持する分散型学習アプローチを実装する

### AIシステムのインシデント対応
- **AI特有のインシデント手順**: AIおよびMCP特有の脅威に対応するインシデント対応手順を開発する
- **自動対応**: 一般的なAIセキュリティインシデントに対する自動化された封じ込めと修復を実装する  
- **フォレンジック能力**: AIシステムの妥協やデータ漏洩に対するフォレンジック準備を維持する
- **復旧手順**: AIモデルの毒性、プロンプトインジェクション攻撃、サービス妥協からの復旧手順を確立する

## 実装リソースと標準

### MCP公式ドキュメント
- [MCP仕様2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - 最新のMCPプロトコル仕様
- [MCPセキュリティベストプラクティス](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - 公式セキュリティガイダンス
- [MCP認可仕様](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - 認証と認可のパターン
- [MCPトランスポートセキュリティ](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - トランスポート層セキュリティ要件

### Microsoftセキュリティソリューション
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - 高度なプロンプトインジェクション保護
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - 包括的なAIコンテンツフィルタリング
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - エンタープライズアイデンティティとアクセス管理
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - 安全な秘密と資格情報管理
- [GitHub Advanced Security](https://github.com/security/advanced-security) - サプライチェーンとコードセキュリティスキャン

### セキュリティ標準とフレームワーク
- [OAuth 2.1セキュリティベストプラクティス](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - 最新のOAuthセキュリティガイダンス
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Webアプリケーションセキュリティリスク
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI特有のセキュリティリスク
- [NIST AIリスク管理フレームワーク](https://www.nist.gov/itl/ai-risk-management-framework) - 包括的なAIリスク管理
- [ISO 27001:2022](https://www.iso.org/standard/27001) - 情報セキュリティ管理システム

### 実装ガイドとチュートリアル
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - エンタープライズ認証パターン
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - アイデンティティプロバイダー統合
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - トークン管理ベストプラクティス
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - 高度な暗号化パターン

### 高度なセキュリティリソース
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - 安全な開発プラクティス
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - AI特有のセキュリティテスト
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - AI脅威モデリング手法
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - プライバシー保護型AI技術

### コンプライアンスとガバナンス
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - AIシステムにおけるプライバシーコンプライアンス
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - 責任あるAI実装
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - AIサービスプロバイダー向けのセキュリティ管理
- [HIPAA Compliance for AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - ヘルスケアAIのコンプライアンス要件

### DevSecOps & Automation
- [DevSecOps Pipeline for AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - 安全なAI開発パイプライン
- [Automated Security Testing](https://learn.microsoft.com/security/engineering/devsecops) - 継続的なセキュリティ検証
- [Infrastructure as Code Security](https://learn.microsoft.com/security/engineering/infrastructure-security) - 安全なインフラストラクチャの展開
- [Container Security for AI](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - AIワークロードコンテナ化セキュリティ

### Monitoring & Incident Response  
- [Azure Monitor for AI Workloads](https://learn.microsoft.com/azure/azure-monitor/overview) - 包括的な監視ソリューション
- [AI Security Incident Response](https://learn.microsoft.com/security/compass/incident-response-playbooks) - AI特有のインシデント手順
- [SIEM for AI Systems](https://learn.microsoft.com/azure/sentinel/overview) - セキュリティ情報およびイベント管理
- [Threat Intelligence for AI](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - AI脅威インテリジェンスソース

## 🔄 継続的な改善

### 進化する標準規格への対応
- **MCP仕様の更新**: 公式MCP仕様の変更とセキュリティアドバイザリを監視
- **脅威インテリジェンス**: AIセキュリティ脅威フィードと脆弱性データベースを購読
- **コミュニティエンゲージメント**: MCPセキュリティコミュニティのディスカッションやワーキンググループに参加
- **定期評価**: 四半期ごとにセキュリティ態勢評価を実施し、それに応じてプラクティスを更新

### MCPセキュリティへの貢献
- **セキュリティリサーチ**: MCPセキュリティリサーチと脆弱性開示プログラムに貢献
- **ベストプラクティスの共有**: セキュリティ実装と得られた教訓をコミュニティと共有
- **標準規格の開発**: MCP仕様の策定とセキュリティ標準規格の作成に参加
- **ツール開発**: MCPエコシステム向けのセキュリティツールとライブラリを開発・共有

---

*このドキュメントは、2025年8月18日時点のMCPセキュリティのベストプラクティスを反映しています（MCP仕様2025-06-18に基づく）。プロトコルや脅威の状況が進化するにつれて、セキュリティの実践は定期的に見直し、更新する必要があります。*

**免責事項**:  
この文書は、AI翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を追求しておりますが、自動翻訳には誤りや不正確さが含まれる可能性があります。元の言語で記載された原文が信頼できる情報源と見なされるべきです。重要な情報については、専門の人間による翻訳を推奨します。この翻訳の使用に起因する誤解や誤認について、当社は一切の責任を負いません。
