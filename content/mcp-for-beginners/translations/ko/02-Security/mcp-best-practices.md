<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T11:23:08+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "ko"
}
-->
# MCP 보안 모범 사례 2025

이 포괄적인 가이드는 최신 **MCP 사양 2025-06-18** 및 현재 업계 표준을 기반으로 Model Context Protocol (MCP) 시스템을 구현하기 위한 필수 보안 모범 사례를 설명합니다. 이 모범 사례는 전통적인 보안 문제와 MCP 배포에 고유한 AI 관련 위협을 모두 다룹니다.

## 주요 보안 요구사항

### 필수 보안 통제 (MUST 요구사항)

1. **토큰 검증**: MCP 서버는 **MUST NOT** 자신을 위해 명시적으로 발급되지 않은 토큰을 수락해서는 안 됩니다.
2. **권한 확인**: 권한 부여를 구현하는 MCP 서버는 **MUST** 모든 수신 요청을 확인해야 하며, 인증을 위해 세션을 사용해서는 **MUST NOT** 안 됩니다.  
3. **사용자 동의**: 정적 클라이언트 ID를 사용하는 MCP 프록시 서버는 동적으로 등록된 각 클라이언트에 대해 명시적인 사용자 동의를 **MUST** 받아야 합니다.
4. **보안 세션 ID**: MCP 서버는 암호학적으로 안전하고 비결정적인 세션 ID를 보안 난수 생성기를 사용하여 생성해야 **MUST** 합니다.

## 핵심 보안 관행

### 1. 입력 검증 및 정화
- **포괄적인 입력 검증**: 주입 공격, 혼란된 대리 문제, 프롬프트 주입 취약점을 방지하기 위해 모든 입력을 검증하고 정화합니다.
- **매개변수 스키마 적용**: 모든 도구 매개변수와 API 입력에 대해 엄격한 JSON 스키마 검증을 구현합니다.
- **콘텐츠 필터링**: Microsoft Prompt Shields와 Azure Content Safety를 사용하여 프롬프트와 응답에서 악성 콘텐츠를 필터링합니다.
- **출력 정화**: 사용자나 다운스트림 시스템에 표시하기 전에 모든 모델 출력을 검증하고 정화합니다.

### 2. 인증 및 권한 부여 우수성  
- **외부 ID 제공자**: 맞춤형 인증을 구현하는 대신 Microsoft Entra ID, OAuth 2.1 제공자와 같은 확립된 ID 제공자에게 인증을 위임합니다.
- **세분화된 권한**: 최소 권한 원칙을 따르는 도구별 세분화된 권한을 구현합니다.
- **토큰 수명 주기 관리**: 짧은 수명의 액세스 토큰을 사용하고 안전한 회전 및 적절한 대상 검증을 수행합니다.
- **다중 인증**: 모든 관리 액세스 및 민감한 작업에 대해 MFA를 요구합니다.

### 3. 안전한 통신 프로토콜
- **전송 계층 보안**: 적절한 인증서 검증과 함께 모든 MCP 통신에 HTTPS/TLS 1.3을 사용합니다.
- **종단 간 암호화**: 전송 중 및 저장 중인 고도로 민감한 데이터에 대해 추가 암호화 계층을 구현합니다.
- **인증서 관리**: 자동 갱신 프로세스를 통해 적절한 인증서 수명 주기를 유지합니다.
- **프로토콜 버전 강제 적용**: 적절한 버전 협상을 통해 최신 MCP 프로토콜 버전(2025-06-18)을 사용합니다.

### 4. 고급 속도 제한 및 자원 보호
- **다중 계층 속도 제한**: 남용을 방지하기 위해 사용자, 세션, 도구 및 자원 수준에서 속도 제한을 구현합니다.
- **적응형 속도 제한**: 사용 패턴과 위협 지표에 적응하는 머신러닝 기반 속도 제한을 사용합니다.
- **자원 할당량 관리**: 계산 자원, 메모리 사용량 및 실행 시간에 적절한 제한을 설정합니다.
- **DDoS 보호**: 포괄적인 DDoS 보호 및 트래픽 분석 시스템을 배포합니다.

### 5. 포괄적인 로깅 및 모니터링
- **구조화된 감사 로깅**: 모든 MCP 작업, 도구 실행 및 보안 이벤트에 대해 세부적이고 검색 가능한 로그를 구현합니다.
- **실시간 보안 모니터링**: MCP 워크로드에 대해 AI 기반 이상 탐지 기능이 있는 SIEM 시스템을 배포합니다.
- **프라이버시 준수 로깅**: 데이터 프라이버시 요구사항 및 규정을 준수하면서 보안 이벤트를 기록합니다.
- **사고 대응 통합**: 로깅 시스템을 자동화된 사고 대응 워크플로와 연결합니다.

### 6. 강화된 안전한 저장 관행
- **하드웨어 보안 모듈**: 중요한 암호화 작업에 대해 HSM 지원 키 저장소(Azure Key Vault, AWS CloudHSM)를 사용합니다.
- **암호화 키 관리**: 암호화 키에 대해 적절한 키 회전, 분리 및 액세스 제어를 구현합니다.
- **비밀 관리**: 모든 API 키, 토큰 및 자격 증명을 전용 비밀 관리 시스템에 저장합니다.
- **데이터 분류**: 민감도 수준에 따라 데이터를 분류하고 적절한 보호 조치를 적용합니다.

### 7. 고급 토큰 관리
- **토큰 전달 방지**: 보안 통제를 우회하는 토큰 전달 패턴을 명시적으로 금지합니다.
- **대상 검증**: 토큰 대상 클레임이 의도된 MCP 서버 ID와 일치하는지 항상 확인합니다.
- **클레임 기반 권한 부여**: 토큰 클레임 및 사용자 속성을 기반으로 세분화된 권한 부여를 구현합니다.
- **토큰 바인딩**: 적절한 경우 토큰을 특정 세션, 사용자 또는 장치에 바인딩합니다.

### 8. 안전한 세션 관리
- **암호학적 세션 ID**: 예측 가능한 시퀀스가 아닌 암호학적으로 안전한 난수 생성기를 사용하여 세션 ID를 생성합니다.
- **사용자별 바인딩**: `<user_id>:<session_id>`와 같은 안전한 형식을 사용하여 세션 ID를 사용자별 정보에 바인딩합니다.
- **세션 수명 주기 통제**: 적절한 세션 만료, 회전 및 무효화 메커니즘을 구현합니다.
- **세션 보안 헤더**: 세션 보호를 위해 적절한 HTTP 보안 헤더를 사용합니다.

### 9. AI 전용 보안 통제
- **프롬프트 주입 방어**: Microsoft Prompt Shields를 배포하여 스포트라이트, 구분자 및 데이터마킹 기술을 사용합니다.
- **도구 오염 방지**: 도구 메타데이터를 검증하고 동적 변경 사항을 모니터링하며 도구 무결성을 확인합니다.
- **모델 출력 검증**: 데이터 유출, 유해 콘텐츠 또는 보안 정책 위반 가능성을 모델 출력에서 스캔합니다.
- **컨텍스트 윈도우 보호**: 컨텍스트 윈도우 오염 및 조작 공격을 방지하기 위한 통제를 구현합니다.

### 10. 도구 실행 보안
- **실행 샌드박싱**: 리소스 제한이 있는 컨테이너화된 격리 환경에서 도구 실행을 수행합니다.
- **권한 분리**: 최소한의 필요한 권한으로 도구를 실행하고 별도의 서비스 계정을 사용합니다.
- **네트워크 격리**: 도구 실행 환경에 대해 네트워크 분할을 구현합니다.
- **실행 모니터링**: 비정상적인 동작, 자원 사용량 및 보안 위반에 대해 도구 실행을 모니터링합니다.

### 11. 지속적인 보안 검증
- **자동화된 보안 테스트**: GitHub Advanced Security와 같은 도구를 사용하여 CI/CD 파이프라인에 보안 테스트를 통합합니다.
- **취약점 관리**: AI 모델 및 외부 서비스를 포함한 모든 종속성을 정기적으로 스캔합니다.
- **침투 테스트**: MCP 구현을 대상으로 정기적인 보안 평가를 수행합니다.
- **보안 코드 리뷰**: 모든 MCP 관련 코드 변경에 대해 필수 보안 리뷰를 구현합니다.

### 12. AI 공급망 보안
- **구성 요소 검증**: 모든 AI 구성 요소(모델, 임베딩, API)의 출처, 무결성 및 보안을 검증합니다.
- **종속성 관리**: 취약점 추적과 함께 모든 소프트웨어 및 AI 종속성의 최신 인벤토리를 유지합니다.
- **신뢰할 수 있는 저장소**: 모든 AI 모델, 라이브러리 및 도구에 대해 검증된 신뢰할 수 있는 소스를 사용합니다.
- **공급망 모니터링**: AI 서비스 제공자 및 모델 저장소의 손상 여부를 지속적으로 모니터링합니다.

## 고급 보안 패턴

### MCP를 위한 제로 트러스트 아키텍처
- **절대 신뢰하지 말고 항상 검증**: 모든 MCP 참가자에 대해 지속적인 검증을 구현합니다.
- **마이크로 세분화**: 세분화된 네트워크 및 ID 통제를 통해 MCP 구성 요소를 격리합니다.
- **조건부 액세스**: 컨텍스트와 행동에 적응하는 위험 기반 액세스 통제를 구현합니다.
- **지속적인 위험 평가**: 현재 위협 지표를 기반으로 보안 상태를 동적으로 평가합니다.

### 프라이버시를 보존하는 AI 구현
- **데이터 최소화**: 각 MCP 작업에 필요한 최소 데이터만 노출합니다.
- **차등 프라이버시**: 민감한 데이터 처리를 위한 프라이버시 보존 기술을 구현합니다.
- **동형 암호화**: 암호화된 데이터에 대한 안전한 계산을 위해 고급 암호화 기술을 사용합니다.
- **연합 학습**: 데이터 로컬리티와 프라이버시를 보존하는 분산 학습 접근 방식을 구현합니다.

### AI 시스템을 위한 사고 대응
- **AI 전용 사고 절차**: AI 및 MCP 고유의 위협에 맞춘 사고 대응 절차를 개발합니다.
- **자동화된 대응**: 일반적인 AI 보안 사고에 대해 자동화된 격리 및 복구를 구현합니다.  
- **포렌식 역량**: AI 시스템 손상 및 데이터 유출에 대한 포렌식 준비 태세를 유지합니다.
- **복구 절차**: AI 모델 오염, 프롬프트 주입 공격 및 서비스 손상에서 복구하기 위한 절차를 수립합니다.

## 구현 리소스 및 표준

### 공식 MCP 문서
- [MCP 사양 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - 최신 MCP 프로토콜 사양
- [MCP 보안 모범 사례](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - 공식 보안 지침
- [MCP 권한 부여 사양](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - 인증 및 권한 부여 패턴
- [MCP 전송 보안](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - 전송 계층 보안 요구사항

### Microsoft 보안 솔루션
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - 고급 프롬프트 주입 보호
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - 포괄적인 AI 콘텐츠 필터링
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - 엔터프라이즈 ID 및 액세스 관리
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - 안전한 비밀 및 자격 증명 관리
- [GitHub Advanced Security](https://github.com/security/advanced-security) - 공급망 및 코드 보안 스캔

### 보안 표준 및 프레임워크
- [OAuth 2.1 보안 모범 사례](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - 최신 OAuth 보안 지침
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - 웹 애플리케이션 보안 위험
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - AI 전용 보안 위험
- [NIST AI 위험 관리 프레임워크](https://www.nist.gov/itl/ai-risk-management-framework) - 포괄적인 AI 위험 관리
- [ISO 27001:2022](https://www.iso.org/standard/27001) - 정보 보안 관리 시스템

### 구현 가이드 및 튜토리얼
- [Azure API Management를 MCP 인증 게이트웨이로 사용하기](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - 엔터프라이즈 인증 패턴
- [Microsoft Entra ID와 MCP 서버 통합](https://den.dev/blog/mcp-server-auth-entra-id-session/) - ID 제공자 통합
- [안전한 토큰 저장 구현](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - 토큰 관리 모범 사례
- [AI를 위한 종단 간 암호화](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - 고급 암호화 패턴

### 고급 보안 리소스
- [Microsoft 보안 개발 수명 주기](https://www.microsoft.com/sdl) - 안전한 개발 관행
- [AI 레드 팀 가이드라인](https://learn.microsoft.com/security/ai-red-team/) - AI 전용 보안 테스트
- [AI 시스템을 위한 위협 모델링](https://learn.microsoft.com/security/adoption/approach/threats-ai) - AI 위협 모델링 방법론
- [AI를 위한 프라이버시 엔지니어링](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - 프라이버시 보존 AI 기술

### 규정 준수 및 거버넌스
- [AI를 위한 GDPR 준수](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - AI 시스템의 프라이버시 준수
- [AI 거버넌스 프레임워크](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - 책임 있는 AI 구현
- [AI 서비스용 SOC 2](https://learn.microsoft.com/compliance/regulatory/offering-soc) - AI 서비스 제공자를 위한 보안 통제
- [AI를 위한 HIPAA 준수](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - 헬스케어 AI 준수 요구사항

### DevSecOps 및 자동화
- [AI를 위한 DevSecOps 파이프라인](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - 안전한 AI 개발 파이프라인
- [자동화된 보안 테스트](https://learn.microsoft.com/security/engineering/devsecops) - 지속적인 보안 검증
- [코드형 인프라 보안](https://learn.microsoft.com/security/engineering/infrastructure-security) - 안전한 인프라 배포
- [AI를 위한 컨테이너 보안](https://learn.microsoft.com/azure/container-instances/container-instances-image-security) - AI 워크로드 컨테이너화 보안

### 모니터링 및 사고 대응  
- [AI 워크로드를 위한 Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/overview) - 포괄적인 모니터링 솔루션
- [AI 보안 사고 대응](https://learn.microsoft.com/security/compass/incident-response-playbooks) - AI 전용 사고 절차
- [AI 시스템용 SIEM](https://learn.microsoft.com/azure/sentinel/overview) - 보안 정보 및 이벤트 관리
- [AI를 위한 위협 인텔리전스](https://learn.microsoft.com/security/compass/security-operations-videos-and-decks#threat-intelligence) - AI 위협 인텔리전스 소스

## 🔄 지속적인 개선

### 진화하는 표준에 발맞추기
- **MCP 사양 업데이트**: 공식 MCP 사양 변경 및 보안 권고 사항을 모니터링합니다.
- **위협 인텔리전스**: AI 보안 위협 피드 및 취약점 데이터베이스를 구독합니다.  
- **커뮤니티 참여**: MCP 보안 커뮤니티 토론 및 작업 그룹에 참여합니다.
- **정기 평가**: 분기별 보안 상태 평가를 수행하고 관행을 업데이트합니다.

### MCP 보안에 기여하기
- **보안 연구**: MCP 보안 연구 및 취약점 공개 프로그램에 기여합니다.
- **모범 사례 공유**: 보안 구현 및 학습 내용을 커뮤니티와 공유합니다.
- **표준 개발**: MCP 사양 개발 및 보안 표준 생성에 참여합니다.
- **도구 개발**: MCP 생태계를 위한 보안 도구와 라이브러리를 개발하고 공유합니다

---

*이 문서는 2025년 8월 18일 기준 MCP 사양 2025-06-18에 기반한 MCP 보안 모범 사례를 반영합니다. 프로토콜과 위협 환경이 변화함에 따라 보안 관행은 정기적으로 검토되고 업데이트되어야 합니다.*

**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있으나, 자동 번역에는 오류나 부정확성이 포함될 수 있습니다. 원본 문서를 해당 언어로 작성된 상태에서 권위 있는 자료로 간주해야 합니다. 중요한 정보의 경우, 전문적인 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생할 수 있는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.