<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T11:23:58+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "ko"
}
-->
# MCP 보안 통제 - 2025년 8월 업데이트

> **현재 표준**: 이 문서는 [MCP 사양 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/)의 보안 요구사항과 공식 [MCP 보안 모범 사례](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)를 반영합니다.

모델 컨텍스트 프로토콜(MCP)은 전통적인 소프트웨어 보안과 AI 관련 위협을 모두 다루는 강화된 보안 통제를 통해 크게 발전했습니다. 이 문서는 2025년 8월 기준으로 안전한 MCP 구현을 위한 포괄적인 보안 통제를 제공합니다.

## **필수 보안 요구사항**

### **MCP 사양에서의 주요 금지 사항:**

> **금지**: MCP 서버는 **명시적으로 MCP 서버를 위해 발급되지 않은 토큰을 수락해서는 안 됩니다.**
>
> **금지**: MCP 서버는 **인증을 위해 세션을 사용해서는 안 됩니다.**  
>
> **필수**: 권한 부여를 구현하는 MCP 서버는 **모든 수신 요청을 검증해야 합니다.**
>
> **의무 사항**: 정적 클라이언트 ID를 사용하는 MCP 프록시 서버는 **동적으로 등록된 클라이언트에 대해 사용자 동의를 얻어야 합니다.**

---

## 1. **인증 및 권한 부여 통제**

### **외부 ID 공급자 통합**

**현재 MCP 표준(2025-06-18)**은 MCP 서버가 인증을 외부 ID 공급자에게 위임할 수 있도록 허용하며, 이는 보안 측면에서 큰 개선을 제공합니다.

**보안 이점:**
1. **맞춤 인증 위험 제거**: 맞춤 인증 구현을 피함으로써 취약점 노출을 줄임
2. **기업 수준 보안**: Microsoft Entra ID와 같은 고급 보안 기능을 갖춘 ID 공급자를 활용
3. **중앙 집중식 ID 관리**: 사용자 수명 주기 관리, 접근 제어, 규정 준수 감사 간소화
4. **다단계 인증(MFA)**: 기업 ID 공급자의 MFA 기능 상속
5. **조건부 접근 정책**: 위험 기반 접근 제어 및 적응형 인증 활용

**구현 요구사항:**
- **토큰 대상 검증**: 모든 토큰이 MCP 서버를 위해 명시적으로 발급되었는지 확인
- **발급자 검증**: 토큰 발급자가 예상된 ID 공급자와 일치하는지 확인
- **서명 검증**: 토큰 무결성에 대한 암호학적 검증
- **만료 강제 적용**: 토큰 수명 제한을 엄격히 준수
- **범위 검증**: 요청된 작업에 적합한 권한이 토큰에 포함되었는지 확인

### **권한 부여 로직 보안**

**주요 통제 사항:**
- **포괄적인 권한 부여 감사**: 모든 권한 부여 결정 지점에 대한 정기적인 보안 검토
- **안전한 기본값**: 권한 부여 로직이 명확한 결정을 내릴 수 없을 때 접근 거부
- **권한 경계 설정**: 서로 다른 권한 수준과 리소스 접근 간 명확한 분리
- **감사 로깅**: 보안 모니터링을 위한 모든 권한 부여 결정의 완전한 로깅
- **정기적인 접근 검토**: 사용자 권한 및 권한 할당의 주기적인 검증

## 2. **토큰 보안 및 패스스루 방지 통제**

### **토큰 패스스루 방지**

**MCP 권한 부여 사양에서는 토큰 패스스루를 명시적으로 금지**하며, 이는 중요한 보안 위험을 해결합니다.

**해결된 보안 위험:**
- **통제 우회**: 속도 제한, 요청 검증, 트래픽 모니터링과 같은 필수 보안 통제를 우회
- **책임성 붕괴**: 클라이언트 식별이 불가능해져 감사 기록 및 사고 조사에 문제 발생
- **프록시 기반 데이터 유출**: 서버를 프록시로 사용하여 비인가 데이터 접근을 가능하게 함
- **신뢰 경계 위반**: 토큰 출처에 대한 다운스트림 서비스의 신뢰 가정을 깨뜨림
- **횡적 이동**: 여러 서비스에서 손상된 토큰을 사용하여 공격 범위를 확장

**구현 통제:**
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

### **안전한 토큰 관리 패턴**

**모범 사례:**
- **단기 토큰 사용**: 빈번한 토큰 회전을 통해 노출 창 최소화
- **필요 시 발급**: 특정 작업에 필요할 때만 토큰 발급
- **안전한 저장소**: 하드웨어 보안 모듈(HSM) 또는 안전한 키 보관소 사용
- **토큰 바인딩**: 가능한 경우 특정 클라이언트, 세션 또는 작업에 토큰 바인딩
- **모니터링 및 경고**: 토큰 오용 또는 비인가 접근 패턴의 실시간 탐지

## 3. **세션 보안 통제**

### **세션 하이재킹 방지**

**대응하는 공격 벡터:**
- **세션 하이재킹 프롬프트 주입**: 공유된 세션 상태에 악성 이벤트 주입
- **세션 가장**: 도난된 세션 ID를 사용한 비인가 접근
- **재개 가능한 스트림 공격**: 서버 전송 이벤트 재개를 악용하여 악성 콘텐츠 주입

**필수 세션 통제:**
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

**전송 보안:**
- **HTTPS 강제 적용**: 모든 세션 통신은 TLS 1.3을 통해 이루어져야 함
- **안전한 쿠키 속성**: HttpOnly, Secure, SameSite=Strict
- **인증서 고정**: MITM 공격 방지를 위한 중요한 연결에 대해 인증서 고정

### **상태 저장 vs 상태 비저장 고려사항**

**상태 저장 구현의 경우:**
- 공유된 세션 상태는 주입 공격에 대한 추가 보호 필요
- 큐 기반 세션 관리는 무결성 검증 필요
- 여러 서버 인스턴스 간 세션 상태 동기화 보안 필요

**상태 비저장 구현의 경우:**
- JWT 또는 유사한 토큰 기반 세션 관리
- 세션 상태 무결성에 대한 암호학적 검증
- 공격 표면 감소, 그러나 강력한 토큰 검증 필요

## 4. **AI 관련 보안 통제**

### **프롬프트 주입 방어**

**Microsoft Prompt Shields 통합:**
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

**구현 통제:**
- **입력 정화**: 모든 사용자 입력에 대한 포괄적인 검증 및 필터링
- **콘텐츠 경계 정의**: 시스템 지침과 사용자 콘텐츠 간 명확한 분리
- **지침 계층 구조**: 충돌하는 지침에 대한 적절한 우선순위 규칙
- **출력 모니터링**: 잠재적으로 유해하거나 조작된 출력 탐지

### **도구 중독 방지**

**도구 보안 프레임워크:**
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

**동적 도구 관리:**
- **승인 워크플로우**: 도구 수정에 대한 명시적인 사용자 동의
- **롤백 기능**: 이전 도구 버전으로 복원 가능
- **변경 감사**: 도구 정의 수정의 전체 이력
- **위험 평가**: 도구 보안 상태의 자동 평가

## 5. **혼동된 대리자 공격 방지**

### **OAuth 프록시 보안**

**공격 방지 통제:**
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

**구현 요구사항:**
- **사용자 동의 검증**: 동적 클라이언트 등록에 대해 동의 화면을 생략하지 않음
- **리디렉션 URI 검증**: 화이트리스트 기반의 엄격한 리디렉션 대상 검증
- **권한 코드 보호**: 단일 사용을 강제하는 단기 코드
- **클라이언트 신원 검증**: 클라이언트 자격 증명 및 메타데이터의 강력한 검증

## 6. **도구 실행 보안**

### **샌드박싱 및 격리**

**컨테이너 기반 격리:**
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

**프로세스 격리:**
- **별도 프로세스 컨텍스트**: 각 도구 실행을 격리된 프로세스 공간에서 수행
- **프로세스 간 통신**: 검증된 안전한 IPC 메커니즘
- **프로세스 모니터링**: 런타임 동작 분석 및 이상 탐지
- **자원 강제 적용**: CPU, 메모리, I/O 작업에 대한 엄격한 제한

### **최소 권한 구현**

**권한 관리:**
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

## 7. **공급망 보안 통제**

### **종속성 검증**

**포괄적인 구성 요소 보안:**
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

### **지속적인 모니터링**

**공급망 위협 탐지:**
- **종속성 상태 모니터링**: 보안 문제에 대한 모든 종속성의 지속적인 평가
- **위협 인텔리전스 통합**: 신속한 공급망 위협 업데이트
- **행동 분석**: 외부 구성 요소의 비정상적인 행동 탐지
- **자동 대응**: 손상된 구성 요소의 즉각적인 격리

## 8. **모니터링 및 탐지 통제**

### **보안 정보 및 이벤트 관리(SIEM)**

**포괄적인 로깅 전략:**
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

### **실시간 위협 탐지**

**행동 분석:**
- **사용자 행동 분석(UBA)**: 비정상적인 사용자 접근 패턴 탐지
- **엔터티 행동 분석(EBA)**: MCP 서버 및 도구 동작 모니터링
- **머신러닝 이상 탐지**: AI 기반 보안 위협 식별
- **위협 인텔리전스 상관관계**: 관찰된 활동과 알려진 공격 패턴 매칭

## 9. **사고 대응 및 복구**

### **자동화된 대응 기능**

**즉각적인 대응 조치:**
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

### **포렌식 기능**

**조사 지원:**
- **감사 기록 보존**: 암호학적 무결성을 갖춘 불변 로깅
- **증거 수집**: 관련 보안 아티팩트의 자동 수집
- **타임라인 재구성**: 보안 사고로 이어진 사건의 상세한 순서
- **영향 평가**: 손상 범위 및 데이터 노출 평가

## **주요 보안 아키텍처 원칙**

### **심층 방어**
- **다중 보안 계층**: 보안 아키텍처에서 단일 실패 지점 제거
- **중복 통제**: 중요한 기능에 대한 중첩된 보안 조치
- **안전한 기본 메커니즘**: 시스템이 오류나 공격에 직면했을 때 안전한 기본값 유지

### **제로 트러스트 구현**
- **절대 신뢰하지 말고 항상 검증**: 모든 엔터티와 요청의 지속적인 검증
- **최소 권한 원칙**: 모든 구성 요소에 최소한의 접근 권한 부여
- **마이크로 세분화**: 세밀한 네트워크 및 접근 통제

### **지속적인 보안 진화**
- **위협 환경 적응**: 새로운 위협에 대응하기 위한 정기적인 업데이트
- **보안 통제 효과성**: 통제의 지속적인 평가 및 개선
- **사양 준수**: 변화하는 MCP 보안 표준과의 정렬

---

## **구현 리소스**

### **공식 MCP 문서**
- [MCP 사양 (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)
- [MCP 보안 모범 사례](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [MCP 권한 부여 사양](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

### **Microsoft 보안 솔루션**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [GitHub Advanced Security](https://github.com/security/advanced-security)
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)

### **보안 표준**
- [OAuth 2.0 보안 모범 사례 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [OWASP 대형 언어 모델 상위 10](https://genai.owasp.org/)
- [NIST 사이버 보안 프레임워크](https://www.nist.gov/cyberframework)

---

> **중요**: 이 보안 통제는 현재 MCP 사양(2025-06-18)을 반영합니다. 표준이 빠르게 진화하므로 항상 최신 [공식 문서](https://spec.modelcontextprotocol.io/)를 확인하십시오.

**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있지만, 자동 번역에는 오류나 부정확성이 포함될 수 있습니다. 원본 문서를 해당 언어로 작성된 권위 있는 자료로 간주해야 합니다. 중요한 정보의 경우, 전문적인 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.