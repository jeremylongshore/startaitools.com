<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T11:13:47+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ja"
}
-->
# MCPセキュリティコントロール - 2025年8月更新

> **現在の標準**: このドキュメントは、[MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) のセキュリティ要件および公式の [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) を反映しています。

Model Context Protocol (MCP) は、従来のソフトウェアセキュリティとAI特有の脅威の両方に対応する強化されたセキュリティコントロールにより、大幅に成熟しました。このドキュメントは、2025年8月時点での安全なMCP実装のための包括的なセキュリティコントロールを提供します。

## **必須セキュリティ要件**

### **MCP仕様における重要な禁止事項:**

> **禁止**: MCPサーバーは、MCPサーバーのために明示的に発行されていないトークンを**受け入れてはなりません**  
>
> **禁止**: MCPサーバーは、認証にセッションを**使用してはなりません**  
>
> **必須**: 認可を実装するMCPサーバーは、**すべての受信リクエストを検証しなければなりません**  
>
> **必須**: 静的クライアントIDを使用するMCPプロキシサーバーは、動的に登録されたクライアントごとにユーザーの同意を**取得しなければなりません**  

---

## 1. **認証と認可のコントロール**

### **外部IDプロバイダーの統合**

**現在のMCP標準 (2025-06-18)** では、MCPサーバーが認証を外部IDプロバイダーに委任することが可能であり、これによりセキュリティが大幅に向上します。

**セキュリティ上の利点:**
1. **カスタム認証リスクの排除**: カスタム認証実装を避けることで脆弱性の表面を削減  
2. **エンタープライズグレードのセキュリティ**: Microsoft Entra IDのような高度なセキュリティ機能を持つ確立されたIDプロバイダーを活用  
3. **集中型ID管理**: ユーザーライフサイクル管理、アクセス制御、コンプライアンス監査を簡素化  
4. **多要素認証 (MFA)**: エンタープライズIDプロバイダーのMFA機能を継承  
5. **条件付きアクセスポリシー**: リスクベースのアクセス制御と適応型認証を活用  

**実装要件:**
- **トークンのオーディエンス検証**: すべてのトークンがMCPサーバーのために明示的に発行されていることを確認  
- **発行者の検証**: トークン発行者が期待されるIDプロバイダーと一致することを確認  
- **署名の検証**: トークンの完全性を暗号的に検証  
- **有効期限の強制**: トークンの有効期間を厳格に管理  
- **スコープの検証**: トークンが要求された操作に適切な権限を含んでいることを確認  

### **認可ロジックのセキュリティ**

**重要なコントロール:**
- **包括的な認可監査**: すべての認可決定ポイントの定期的なセキュリティレビュー  
- **フェイルセーフデフォルト**: 認可ロジックが明確な決定を下せない場合はアクセスを拒否  
- **権限の境界**: 異なる権限レベルとリソースアクセスの明確な分離  
- **監査ログ**: セキュリティ監視のためのすべての認可決定の完全な記録  
- **定期的なアクセスレビュー**: ユーザー権限と権限割り当ての定期的な検証  

## 2. **トークンセキュリティとパススルー防止コントロール**

### **トークンパススルー防止**

**トークンパススルーはMCP認可仕様で明確に禁止されています**。これは重大なセキュリティリスクを軽減するためです。

**対処されるセキュリティリスク:**
- **コントロールの回避**: レート制限、リクエスト検証、トラフィック監視などの重要なセキュリティコントロールを回避  
- **責任の欠如**: クライアント識別が不可能になり、監査記録やインシデント調査が損なわれる  
- **プロキシを利用したデータ流出**: サーバーをプロキシとして悪用し、不正なデータアクセスを実行  
- **信頼境界の侵害**: トークンの出所に関する下流サービスの信頼仮定を破壊  
- **横方向の移動**: 複数のサービス間でトークンが侵害されることで攻撃が拡大  

**実装コントロール:**
```yaml
Token Validation Requirements:
  audience_validation: MANDATORY
  issuer_verification: MANDATORY  
  signature_check: MANDATORY
  expiration_enforcement: MANDATORY
  scope_validation: MANDATORY
  
Token Lifecycle Management:
  rotation_frequency: "Short-lived tokens preferred"
  secure_storage: "Azure Key Vault or equivalent"
  transmission_security: "TLS 1.3 minimum"
  replay_protection: "Implemented via nonce/timestamp"
```

### **安全なトークン管理パターン**

**ベストプラクティス:**
- **短命トークン**: 頻繁なトークンローテーションで露出期間を最小化  
- **必要時発行**: 特定の操作に必要な場合のみトークンを発行  
- **安全な保管**: ハードウェアセキュリティモジュール (HSM) または安全なキーボルトを使用  
- **トークンバインディング**: トークンを特定のクライアント、セッション、または操作にバインド  
- **監視とアラート**: トークンの不正使用や不正アクセスパターンをリアルタイムで検出  

## 3. **セッションセキュリティコントロール**

### **セッションハイジャック防止**

**対処される攻撃ベクトル:**
- **セッションハイジャックプロンプト注入**: 共有セッション状態に悪意のあるイベントを注入  
- **セッションなりすまし**: 盗まれたセッションIDを使用して認証を回避  
- **再開可能なストリーム攻撃**: サーバー送信イベントの再開を悪用して悪意のあるコンテンツを注入  

**必須セッションコントロール:**
```yaml
Session ID Generation:
  randomness_source: "Cryptographically secure RNG"
  entropy_bits: 128 # Minimum recommended
  format: "Base64url encoded"
  predictability: "MUST be non-deterministic"

Session Binding:
  user_binding: "REQUIRED - <user_id>:<session_id>"
  additional_identifiers: "Device fingerprint, IP validation"
  context_binding: "Request origin, user agent validation"
  
Session Lifecycle:
  expiration: "Configurable timeout policies"
  rotation: "After privilege escalation events"
  invalidation: "Immediate on security events"
  cleanup: "Automated expired session removal"
```

**トランスポートセキュリティ:**
- **HTTPSの強制**: すべてのセッション通信をTLS 1.3で保護  
- **セキュアクッキー属性**: HttpOnly、Secure、SameSite=Strict  
- **証明書ピンニング**: 中間者攻撃 (MITM) を防ぐための重要な接続に適用  

### **ステートフル対ステートレスの考慮事項**

**ステートフル実装の場合:**
- 共有セッション状態は注入攻撃に対する追加の保護が必要  
- キューを使用したセッション管理には整合性検証が必要  
- 複数のサーバーインスタンス間でセッション状態を安全に同期  

**ステートレス実装の場合:**
- JWTや類似のトークンベースのセッション管理  
- セッション状態の整合性を暗号的に検証  
- 攻撃面が減少するが、堅牢なトークン検証が必要  

## 4. **AI特有のセキュリティコントロール**

### **プロンプト注入防御**

**Microsoft Prompt Shieldsの統合:**
```yaml
Detection Mechanisms:
  - "Advanced ML-based instruction detection"
  - "Contextual analysis of external content"
  - "Real-time threat pattern recognition"
  
Protection Techniques:
  - "Spotlighting trusted vs untrusted content"
  - "Delimiter systems for content boundaries"  
  - "Data marking for content source identification"
  
Integration Points:
  - "Azure Content Safety service"
  - "Real-time content filtering"
  - "Threat intelligence updates"
```

**実装コントロール:**
- **入力のサニタイズ**: すべてのユーザー入力の包括的な検証とフィルタリング  
- **コンテンツ境界の定義**: システム指示とユーザーコンテンツの明確な分離  
- **指示の階層構造**: 矛盾する指示に対する適切な優先順位ルール  
- **出力の監視**: 有害または操作された可能性のある出力の検出  

### **ツールポイズニング防止**

**ツールセキュリティフレームワーク:**
```yaml
Tool Definition Protection:
  validation:
    - "Schema validation against expected formats"
    - "Content analysis for malicious instructions" 
    - "Parameter injection detection"
    - "Hidden instruction identification"
  
  integrity_verification:
    - "Cryptographic hashing of tool definitions"
    - "Digital signatures for tool packages"
    - "Version control with change auditing"
    - "Tamper detection mechanisms"
  
  monitoring:
    - "Real-time change detection"
    - "Behavioral analysis of tool usage"
    - "Anomaly detection for execution patterns"
    - "Automated alerting for suspicious modifications"
```

**動的ツール管理:**
- **承認ワークフロー**: ツールの変更に対する明示的なユーザー同意  
- **ロールバック機能**: 以前のツールバージョンへの復元能力  
- **変更監査**: ツール定義変更の完全な履歴  
- **リスク評価**: ツールのセキュリティ状況を自動評価  

## 5. **混乱した代理攻撃防止**

### **OAuthプロキシセキュリティ**

**攻撃防止コントロール:**
```yaml
Client Registration:
  static_client_protection:
    - "Explicit user consent for dynamic registration"
    - "Consent bypass prevention mechanisms"  
    - "Cookie-based consent validation"
    - "Redirect URI strict validation"
    
  authorization_flow:
    - "PKCE implementation (OAuth 2.1)"
    - "State parameter validation"
    - "Authorization code binding"
    - "Nonce verification for ID tokens"
```

**実装要件:**
- **ユーザー同意の検証**: 動的クライアント登録の同意画面を省略しない  
- **リダイレクトURIの検証**: 厳格なホワイトリストベースのリダイレクト先検証  
- **認可コードの保護**: 短命コードと一度きりの使用を強制  
- **クライアントIDの検証**: クライアント資格情報とメタデータの堅牢な検証  

## 6. **ツール実行セキュリティ**

### **サンドボックス化と分離**

**コンテナベースの分離:**
```yaml
Execution Environment:
  containerization: "Docker/Podman with security profiles"
  resource_limits:
    cpu: "Configurable CPU quotas"
    memory: "Memory usage restrictions"
    disk: "Storage access limitations"
    network: "Network policy enforcement"
  
  privilege_restrictions:
    user_context: "Non-root execution mandatory"
    capability_dropping: "Remove unnecessary Linux capabilities"
    syscall_filtering: "Seccomp profiles for syscall restriction"
    filesystem: "Read-only root with minimal writable areas"
```

**プロセス分離:**
- **個別のプロセスコンテキスト**: 各ツール実行を分離されたプロセス空間で実行  
- **プロセス間通信**: 検証付きの安全なIPCメカニズム  
- **プロセス監視**: 実行時の動作分析と異常検出  
- **リソース制限**: CPU、メモリ、I/O操作の厳格な制限  

### **最小権限の実装**

**権限管理:**
```yaml
Access Control:
  file_system:
    - "Minimal required directory access"
    - "Read-only access where possible"
    - "Temporary file cleanup automation"
    
  network_access:
    - "Explicit allowlist for external connections"
    - "DNS resolution restrictions" 
    - "Port access limitations"
    - "SSL/TLS certificate validation"
  
  system_resources:
    - "No administrative privilege elevation"
    - "Limited system call access"
    - "No hardware device access"
    - "Restricted environment variable access"
```

## 7. **サプライチェーンセキュリティコントロール**

### **依存関係の検証**

**包括的なコンポーネントセキュリティ:**
```yaml
Software Dependencies:
  scanning: 
    - "Automated vulnerability scanning (GitHub Advanced Security)"
    - "License compliance verification"
    - "Known vulnerability database checks"
    - "Malware detection and analysis"
  
  verification:
    - "Package signature verification"
    - "Checksum validation"
    - "Provenance attestation"
    - "Software Bill of Materials (SBOM)"

AI Components:
  model_verification:
    - "Model provenance validation"
    - "Training data source verification" 
    - "Model behavior testing"
    - "Adversarial robustness assessment"
  
  service_validation:
    - "Third-party API security assessment"
    - "Service level agreement review"
    - "Data handling compliance verification"
    - "Incident response capability evaluation"
```

### **継続的な監視**

**サプライチェーン脅威検出:**
- **依存関係の健全性監視**: すべての依存関係のセキュリティ問題を継続的に評価  
- **脅威インテリジェンスの統合**: 新たなサプライチェーン脅威に関するリアルタイム更新  
- **行動分析**: 外部コンポーネントの異常な行動を検出  
- **自動対応**: 侵害されたコンポーネントの即時封じ込め  

## 8. **監視と検出コントロール**

### **セキュリティ情報およびイベント管理 (SIEM)**

**包括的なログ戦略:**
```yaml
Authentication Events:
  - "All authentication attempts (success/failure)"
  - "Token issuance and validation events"
  - "Session creation, modification, termination"
  - "Authorization decisions and policy evaluations"

Tool Execution:
  - "Tool invocation details and parameters"
  - "Execution duration and resource usage"
  - "Output generation and content analysis"
  - "Error conditions and exception handling"

Security Events:
  - "Potential prompt injection attempts"
  - "Tool poisoning detection events"
  - "Session hijacking indicators"
  - "Unusual access patterns and anomalies"
```

### **リアルタイム脅威検出**

**行動分析:**
- **ユーザー行動分析 (UBA)**: 異常なユーザーアクセスパターンの検出  
- **エンティティ行動分析 (EBA)**: MCPサーバーおよびツールの動作を監視  
- **機械学習異常検出**: AIを活用したセキュリティ脅威の特定  
- **脅威インテリジェンスの相関**: 観測された活動を既知の攻撃パターンと照合  

## 9. **インシデント対応と復旧**

### **自動対応機能**

**即時対応アクション:**
```yaml
Threat Containment:
  session_management:
    - "Immediate session termination"
    - "Account lockout procedures"
    - "Access privilege revocation"
  
  system_isolation:
    - "Network segmentation activation"
    - "Service isolation protocols"
    - "Communication channel restriction"

Recovery Procedures:
  credential_rotation:
    - "Automated token refresh"
    - "API key regeneration"
    - "Certificate renewal"
  
  system_restoration:
    - "Clean state restoration"
    - "Configuration rollback"
    - "Service restart procedures"
```

### **フォレンジック機能**

**調査支援:**
- **監査記録の保存**: 暗号的整合性を持つ不変のログ  
- **証拠収集**: 関連するセキュリティアーティファクトの自動収集  
- **タイムライン再構築**: セキュリティインシデントに至る詳細なイベントの順序  
- **影響評価**: 侵害範囲とデータ露出の評価  

## **主要なセキュリティアーキテクチャ原則**

### **多層防御**
- **複数のセキュリティ層**: セキュリティアーキテクチャにおける単一障害点を排除  
- **冗長コントロール**: 重要な機能に対する重複するセキュリティ対策  
- **フェイルセーフメカニズム**: システムがエラーや攻撃に直面した際の安全なデフォルト  

### **ゼロトラストの実装**
- **信頼せず、常に検証**: すべてのエンティティとリクエストを継続的に検証  
- **最小権限の原則**: すべてのコンポーネントに最小限のアクセス権を付与  
- **マイクロセグメンテーション**: 詳細なネットワークおよびアクセス制御  

### **継続的なセキュリティ進化**
- **脅威の状況への適応**: 新たな脅威に対応するための定期的な更新  
- **セキュリティコントロールの有効性**: コントロールの継続的な評価と改善  
- **仕様準拠**: 進化するMCPセキュリティ標準との整合性  

---

## **実装リソース**

### **公式MCPドキュメント**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoftセキュリティソリューション**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **セキュリティ標準**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **重要**: これらのセキュリティコントロールは、現在のMCP仕様 (2025-06-18) を反映しています。標準は急速に進化し続けているため、常に最新の [公式ドキュメント](https://spec.modelcontextprotocol.io/) を確認してください。

**免責事項**:  
この文書は、AI翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を追求しておりますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知ください。元の言語で記載された文書が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。この翻訳の使用に起因する誤解や誤解釈について、当方は一切の責任を負いません。