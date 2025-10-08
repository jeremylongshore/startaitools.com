<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T11:19:45+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "ko"
}
-->
# MCP 보안 모범 사례 - 2025년 8월 업데이트

> **중요**: 이 문서는 최신 [MCP 사양 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) 보안 요구사항과 공식 [MCP 보안 모범 사례](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)를 반영합니다. 가장 최신 지침을 확인하려면 항상 현재 사양을 참조하세요.

## MCP 구현을 위한 필수 보안 모범 사례

모델 컨텍스트 프로토콜은 기존 소프트웨어 보안을 넘어서는 독특한 보안 과제를 제시합니다. 이러한 모범 사례는 기본적인 보안 요구사항과 MCP 고유의 위협(예: 프롬프트 인젝션, 도구 오염, 세션 하이재킹, 혼란스러운 대리 문제, 토큰 패스스루 취약점)을 다룹니다.

### **필수 보안 요구사항**

**MCP 사양의 주요 요구사항:**

> **MUST NOT**: MCP 서버는 MCP 서버를 위해 명시적으로 발급되지 않은 토큰을 **절대** 수락해서는 안 됩니다.
> 
> **MUST**: 인증을 구현하는 MCP 서버는 **모든** 인바운드 요청을 검증해야 합니다.
>  
> **MUST NOT**: MCP 서버는 인증을 위해 세션을 **절대** 사용해서는 안 됩니다.
>
> **MUST**: 정적 클라이언트 ID를 사용하는 MCP 프록시 서버는 동적으로 등록된 클라이언트에 대해 사용자 동의를 얻어야 합니다.

---

## 1. **토큰 보안 및 인증**

**인증 및 권한 부여 제어:**
   - **엄격한 권한 검토**: MCP 서버의 권한 부여 로직을 철저히 감사하여 의도된 사용자와 클라이언트만 리소스에 접근할 수 있도록 보장
   - **외부 ID 공급자 통합**: 맞춤형 인증을 구현하는 대신 Microsoft Entra ID와 같은 신뢰할 수 있는 ID 공급자 사용
   - **토큰 대상 검증**: 토큰이 MCP 서버를 위해 명시적으로 발급되었는지 항상 검증 - 상류 토큰은 절대 수락하지 않음
   - **적절한 토큰 수명 관리**: 안전한 토큰 회전, 만료 정책 구현 및 토큰 재사용 공격 방지

**보호된 토큰 저장:**
   - 모든 비밀을 위해 Azure Key Vault 또는 유사한 안전한 자격 증명 저장소 사용
   - 토큰을 저장 및 전송 시 암호화 구현
   - 정기적인 자격 증명 회전 및 무단 접근 모니터링

## 2. **세션 관리 및 전송 보안**

**안전한 세션 관행:**
   - **암호적으로 안전한 세션 ID**: 안전한 난수 생성기를 사용하여 생성된 비결정론적 세션 ID 사용
   - **사용자별 바인딩**: `<user_id>:<session_id>` 형식과 같은 세션 ID를 사용자 ID에 바인딩하여 사용자 간 세션 남용 방지
   - **세션 수명 관리**: 적절한 만료, 회전 및 무효화를 구현하여 취약성 창을 제한
   - **HTTPS/TLS 강제 적용**: 세션 ID 가로채기를 방지하기 위해 모든 통신에 HTTPS 필수

**전송 계층 보안:**
   - 적절한 인증서 관리를 통해 TLS 1.3 구성
   - 중요한 연결에 대해 인증서 고정 구현
   - 정기적인 인증서 회전 및 유효성 검증

## 3. **AI 고유의 위협 보호** 🤖

**프롬프트 인젝션 방어:**
   - **Microsoft Prompt Shields**: 악성 명령어를 고급 탐지 및 필터링하기 위해 AI Prompt Shields 배포
   - **입력 정화**: 인젝션 공격 및 혼란스러운 대리 문제를 방지하기 위해 모든 입력을 검증 및 정화
   - **콘텐츠 경계**: 신뢰할 수 있는 명령어와 외부 콘텐츠를 구분하기 위해 구분자 및 데이터 마킹 시스템 사용

**도구 오염 방지:**
   - **도구 메타데이터 검증**: 도구 정의에 대한 무결성 검사를 구현하고 예상치 못한 변경 사항을 모니터링
   - **동적 도구 모니터링**: 런타임 동작을 모니터링하고 예상치 못한 실행 패턴에 대한 경고 설정
   - **승인 워크플로**: 도구 수정 및 기능 변경에 대해 명시적인 사용자 승인을 요구

## 4. **접근 제어 및 권한**

**최소 권한 원칙:**
   - MCP 서버에 필요한 최소 권한만 부여하여 의도된 기능을 수행
   - 세분화된 권한을 가진 역할 기반 접근 제어(RBAC) 구현
   - 정기적인 권한 검토 및 권한 상승에 대한 지속적인 모니터링

**런타임 권한 제어:**
   - 리소스 고갈 공격을 방지하기 위해 리소스 제한 적용
   - 도구 실행 환경에 대한 컨테이너 격리 사용  
   - 관리 기능에 대해 적시 접근 구현

## 5. **콘텐츠 안전 및 모니터링**

**콘텐츠 안전 구현:**
   - **Azure Content Safety 통합**: 유해 콘텐츠, 탈옥 시도 및 정책 위반을 탐지하기 위해 Azure Content Safety 사용
   - **행동 분석**: MCP 서버 및 도구 실행에서 이상 현상을 탐지하기 위해 런타임 행동 모니터링 구현
   - **포괄적인 로깅**: 안전하고 변조 방지 저장소에 모든 인증 시도, 도구 호출 및 보안 이벤트 기록

**지속적인 모니터링:**
   - 의심스러운 패턴 및 무단 접근 시도에 대한 실시간 경고  
   - 중앙 집중식 보안 이벤트 관리를 위한 SIEM 시스템 통합
   - MCP 구현에 대한 정기적인 보안 감사 및 침투 테스트

## 6. **공급망 보안**

**구성 요소 검증:**
   - **종속성 스캔**: 모든 소프트웨어 종속성과 AI 구성 요소에 대해 자동 취약점 스캔 사용
   - **출처 검증**: 모델, 데이터 소스 및 외부 서비스의 출처, 라이센스 및 무결성 확인
   - **서명된 패키지**: 암호적으로 서명된 패키지를 사용하고 배포 전에 서명 검증

**안전한 개발 파이프라인:**
   - **GitHub Advanced Security**: 비밀 스캔, 종속성 분석 및 CodeQL 정적 분석 구현
   - **CI/CD 보안**: 자동화된 배포 파이프라인 전반에 걸쳐 보안 검증 통합
   - **아티팩트 무결성**: 배포된 아티팩트 및 구성에 대한 암호적 검증 구현

## 7. **OAuth 보안 및 혼란스러운 대리 문제 방지**

**OAuth 2.1 구현:**
   - **PKCE 구현**: 모든 권한 요청에 대해 Proof Key for Code Exchange(PKCE) 사용
   - **명시적 동의**: 혼란스러운 대리 공격을 방지하기 위해 동적으로 등록된 클라이언트에 대해 사용자 동의 획득
   - **리디렉션 URI 검증**: 리디렉션 URI 및 클라이언트 식별자의 엄격한 검증 구현

**프록시 보안:**
   - 정적 클라이언트 ID 악용을 통한 권한 우회 방지
   - 타사 API 접근에 대한 적절한 동의 워크플로 구현
   - 권한 코드 도난 및 무단 API 접근 모니터링

## 8. **사고 대응 및 복구**

**신속한 대응 능력:**
   - **자동화된 대응**: 자격 증명 회전 및 위협 격리를 위한 자동 시스템 구현
   - **롤백 절차**: 알려진 양호한 구성 및 구성 요소로 신속히 복구할 수 있는 능력
   - **포렌식 능력**: 사고 조사에 대한 상세한 감사 추적 및 로깅

**커뮤니케이션 및 협력:**
   - 보안 사고에 대한 명확한 에스컬레이션 절차
   - 조직의 사고 대응 팀과의 통합
   - 정기적인 보안 사고 시뮬레이션 및 테이블탑 연습

## 9. **준수 및 거버넌스**

**규제 준수:**
   - MCP 구현이 산업별 요구사항(GDPR, HIPAA, SOC 2)을 충족하도록 보장
   - AI 데이터 처리에 대한 데이터 분류 및 개인정보 보호 제어 구현
   - 준수 감사에 대한 포괄적인 문서 유지

**변경 관리:**
   - 모든 MCP 시스템 수정에 대한 공식적인 보안 검토 프로세스
   - 구성 변경에 대한 버전 관리 및 승인 워크플로
   - 정기적인 준수 평가 및 격차 분석

## 10. **고급 보안 제어**

**제로 트러스트 아키텍처:**
   - **절대 신뢰하지 않고 항상 검증**: 사용자, 장치 및 연결의 지속적인 검증
   - **마이크로 세그멘테이션**: 개별 MCP 구성 요소를 격리하는 세분화된 네트워크 제어
   - **조건부 접근**: 현재 상황 및 행동에 적응하는 위험 기반 접근 제어

**런타임 애플리케이션 보호:**
   - **런타임 애플리케이션 자체 보호(RASP)**: 실시간 위협 탐지를 위한 RASP 기술 배포
   - **애플리케이션 성능 모니터링**: 공격을 나타낼 수 있는 성능 이상 현상 모니터링
   - **동적 보안 정책**: 현재 위협 환경에 따라 적응하는 보안 정책 구현

## 11. **Microsoft 보안 생태계 통합**

**포괄적인 Microsoft 보안:**
   - **Microsoft Defender for Cloud**: MCP 워크로드에 대한 클라우드 보안 태세 관리
   - **Azure Sentinel**: 고급 위협 탐지를 위한 클라우드 네이티브 SIEM 및 SOAR 기능
   - **Microsoft Purview**: AI 워크플로 및 데이터 소스에 대한 데이터 거버넌스 및 준수

**ID 및 접근 관리:**
   - **Microsoft Entra ID**: 조건부 접근 정책을 갖춘 엔터프라이즈 ID 관리
   - **Privileged Identity Management(PIM)**: 관리 기능에 대한 적시 접근 및 승인 워크플로
   - **Identity Protection**: 위험 기반 조건부 접근 및 자동화된 위협 대응

## 12. **지속적인 보안 진화**

**최신 상태 유지:**
   - **사양 모니터링**: MCP 사양 업데이트 및 보안 지침 변경 사항에 대한 정기적인 검토
   - **위협 인텔리전스**: AI 고유의 위협 피드 및 침해 지표 통합
   - **보안 커뮤니티 참여**: MCP 보안 커뮤니티 및 취약점 공개 프로그램에 적극 참여

**적응형 보안:**
   - **머신 러닝 보안**: 새로운 공격 패턴을 식별하기 위한 ML 기반 이상 탐지 사용
   - **예측 보안 분석**: 사전 위협 식별을 위한 예측 모델 구현
   - **보안 자동화**: 위협 인텔리전스 및 사양 변경 사항에 기반한 자동화된 보안 정책 업데이트

---

## **중요 보안 리소스**

### **공식 MCP 문서**
- [MCP 사양 (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)
- [MCP 보안 모범 사례](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [MCP 권한 부여 사양](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

### **Microsoft 보안 솔루션**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Entra ID 보안](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **보안 표준**
- [OAuth 2.0 보안 모범 사례 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [OWASP 대형 언어 모델을 위한 Top 10](https://genai.owasp.org/)
- [NIST AI 위험 관리 프레임워크](https://www.nist.gov/itl/ai-risk-management-framework)

### **구현 가이드**
- [Azure API Management MCP 인증 게이트웨이](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Microsoft Entra ID와 MCP 서버](https://den.dev/blog/mcp-server-auth-entra-id-session/)

---

> **보안 공지**: MCP 보안 모범 사례는 빠르게 진화합니다. 구현 전에 항상 현재 [MCP 사양](https://spec.modelcontextprotocol.io/) 및 [공식 보안 문서](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)를 확인하세요.

**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있지만, 자동 번역에는 오류나 부정확성이 포함될 수 있습니다. 원본 문서를 해당 언어로 작성된 상태에서 권위 있는 자료로 간주해야 합니다. 중요한 정보에 대해서는 전문적인 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.