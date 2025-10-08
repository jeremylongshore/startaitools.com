<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-19T18:48:09+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "my"
}
-->
# MCP လုံခြုံရေးထိန်းချုပ်မှုများ - ၂၀၂၅ ခုနှစ် ဩဂုတ်လ အပ်ဒိတ်

> **လက်ရှိစံနှုန်း**: ဒီစာရွက်စာတမ်းသည် [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) လုံခြုံရေးလိုအပ်ချက်များနှင့် [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) တရားဝင်အကြံပေးချက်များကို အဓိကထားပြသထားသည်။

Model Context Protocol (MCP) သည် အဆင့်မြှင့်လုံခြုံရေးထိန်းချုပ်မှုများဖြင့် အရေးပါသော ဆော့ဖ်ဝဲလ်လုံခြုံရေးနှင့် AI အထူးပြုခြိမ်းခြောက်မှုများကို ဖြေရှင်းနိုင်ရန် အလွန်တိုးတက်လာပြီဖြစ်သည်။ ဒီစာရွက်စာတမ်းသည် ၂၀၂၅ ခုနှစ် ဩဂုတ်လအထိ MCP ကို လုံခြုံစွာ အကောင်အထည်ဖော်ရန် လုံခြုံရေးထိန်းချုပ်မှုများကို စုံလင်စွာ ဖော်ပြထားသည်။

## **မဖြစ်မနေလိုအပ်သော လုံခြုံရေးလိုအပ်ချက်များ**

### **MCP Specification မှ အရေးပါသော တားမြစ်ချက်များ**

> **FORBIDDEN**: MCP server များသည် MCP server အတွက် အထူးထုတ်ပေးထားသော token မဟုတ်သော token များကို **လက်ခံလို့မရ**  
>
> **PROHIBITED**: MCP server များသည် authentication အတွက် session များကို **အသုံးမပြုရ**  
>
> **REQUIRED**: Authorization ကို အကောင်အထည်ဖော်ထားသော MCP server များသည် **ဝင်ရောက်လာသော request အားလုံးကို စစ်ဆေးရမည်**  
>
> **MANDATORY**: Static client ID များကို အသုံးပြုသော MCP proxy server များသည် **dynamic client registration တစ်ခုစီအတွက် အသုံးပြုသူ၏ သဘောတူညီမှုကို ရယူရမည်**  

---

## 1. **Authentication & Authorization ထိန်းချုပ်မှုများ**

### **အပြင်ဘက် Identity Provider နှင့် ပေါင်းစည်းမှု**

**လက်ရှိ MCP စံနှုန်း (2025-06-18)** သည် MCP server များကို authentication ကို အပြင်ဘက် identity provider များထံ အပ်နှံခွင့်ပြုထားပြီး လုံခြုံရေးအတွက် အရေးပါသော တိုးတက်မှုတစ်ခုကို ကိုယ်စားပြုသည်။

**လုံခြုံရေးအကျိုးကျေးဇူးများ**:
1. **Custom Authentication အန္တရာယ်များကို ဖယ်ရှားခြင်း**: Custom authentication အကောင်အထည်ဖော်မှုများကို ရှောင်ရှားခြင်းဖြင့် အန္တရာယ်များကို လျှော့ချသည်  
2. **အဖွဲ့အစည်းအဆင့် လုံခြုံရေး**: Microsoft Entra ID ကဲ့သို့သော အတည်ပြု identity provider များ၏ အဆင့်မြင့်လုံခြုံရေး features များကို အသုံးပြုသည်  
3. **Identity ကို ဗဟိုပြုစီမံခန့်ခွဲမှု**: အသုံးပြုသူ၏ အသက်တာစီမံခန့်ခွဲမှု၊ access control နှင့် လိုက်နာမှု auditing ကို လွယ်ကူစေသည်  
4. **Multi-Factor Authentication**: အဖွဲ့အစည်း identity provider များ၏ MFA စွမ်းရည်များကို အလိုအလျောက်ရရှိသည်  
5. **Conditional Access Policies**: အန္တရာယ်အခြေပြု access control နှင့် adaptive authentication ကို အကျိုးခံစားရသည်  

**အကောင်အထည်ဖော်မှုလိုအပ်ချက်များ**:
- **Token Audience Validation**: Token များသည် MCP server အတွက် အထူးထုတ်ပေးထားသည်ကို အတည်ပြုပါ  
- **Issuer Verification**: Token issuer သည် မျှော်မှန်းထားသော identity provider နှင့် ကိုက်ညီမှုရှိသည်ကို စစ်ဆေးပါ  
- **Signature Verification**: Token integrity ကို cryptographic validation ဖြင့် အတည်ပြုပါ  
- **Expiration Enforcement**: Token lifetime အကန့်အသတ်များကို တင်းကြပ်စွာ လိုက်နာပါ  
- **Scope Validation**: Token များတွင် တောင်းဆိုထားသော လုပ်ဆောင်မှုများအတွက် သင့်လျော်သော permissions ပါရှိသည်ကို အတည်ပြုပါ  

### **Authorization Logic လုံခြုံရေး**

**အရေးပါသော ထိန်းချုပ်မှုများ**:
- **Authorization Audits အပြည့်အစုံ**: Authorization ဆုံးဖြတ်ချက်အချက်အလက်များအားလုံးကို ပုံမှန်လုံခြုံရေးစစ်ဆေးမှုများ ပြုလုပ်ပါ  
- **Fail-Safe Defaults**: Authorization logic သည် အတိအကျဆုံးဖြတ်ချက်မပေးနိုင်သောအခါ access ကို ပိတ်ထားပါ  
- **Permission Boundaries**: Privilege အဆင့်များနှင့် resource access အကြား သေချာသော ခွဲခြားမှုရှိပါ  
- **Audit Logging**: Authorization ဆုံးဖြတ်ချက်အားလုံးကို လုံခြုံရေးစောင့်ကြည့်မှုအတွက် မှတ်တမ်းတင်ပါ  
- **Regular Access Reviews**: အသုံးပြုသူ၏ permission နှင့် privilege ချမှတ်မှုများကို ပုံမှန်စစ်ဆေးပါ  

## 2. **Token လုံခြုံရေးနှင့် Anti-Passthrough ထိန်းချုပ်မှုများ**

### **Token Passthrough တားမြစ်မှု**

**Token passthrough ကို MCP Authorization Specification တွင် အလုံးစုံတားမြစ်ထားသည်** အရေးပါသော လုံခြုံရေးအန္တရာယ်များကြောင့်:

**ဖြေရှင်းထားသော လုံခြုံရေးအန္တရာယ်များ**:
- **Control Circumvention**: Rate limiting, request validation, traffic monitoring ကဲ့သို့သော အရေးပါသော လုံခြုံရေးထိန်းချုပ်မှုများကို ရှောင်လွှဲနိုင်သည်  
- **Accountability Breakdown**: Client identification မဖြစ်နိုင်စေပြီး audit trail နှင့် အရေးပေါ်ဖြေရှင်းမှုကို ပျက်စီးစေသည်  
- **Proxy-Based Exfiltration**: Server များကို proxy အဖြစ် အသုံးပြု၍ မလိုလားအပ်သော data access ကို ခွင့်ပြုနိုင်သည်  
- **Trust Boundary Violations**: Token မူလအရင်းအမြစ်အပေါ် Downstream service များ၏ ယုံကြည်မှုကို ဖျက်ဆီးသည်  
- **Lateral Movement**: Token များကို အတားအဆီးမရှိသော အခြား service များတွင် အသုံးပြု၍ တိုးချဲ့သော တိုက်ခိုက်မှုများကို ဖြစ်စေသည်  

**Implementation Controls**:
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

### **Secure Token Management Patterns**

**အကောင်းဆုံးအလေ့အထများ**:
- **Short-Lived Tokens**: Token rotation ကို မကြာခဏပြုလုပ်ခြင်းဖြင့် အန္တရာယ်အချိန်ကို လျှော့ချပါ  
- **Just-in-Time Issuance**: Token များကို သတ်မှတ်ထားသော လုပ်ဆောင်မှုများအတွက်သာ ထုတ်ပေးပါ  
- **Secure Storage**: Hardware security module (HSM) များ သို့မဟုတ် secure key vault များကို အသုံးပြုပါ  
- **Token Binding**: Token များကို သတ်မှတ် client, session, သို့မဟုတ် လုပ်ဆောင်မှုများနှင့် ချိတ်ဆက်ပါ  
- **Monitoring & Alerting**: Token ကို မလိုလားအပ်သော အသုံးပြုမှု သို့မဟုတ် ခွင့်မပြုသော access pattern များကို အချိန်နှင့်တပြေးညီ ရှာဖွေပါ  

## 3. **Session လုံခြုံရေးထိန်းချုပ်မှုများ**

### **Session Hijacking တားဆီးမှု**

**ဖြေရှင်းထားသော တိုက်ခိုက်မှုလမ်းကြောင်းများ**:
- **Session Hijack Prompt Injection**: Shared session state တွင် မကောင်းသော အဖြစ်အပျက်များ ထည့်သွင်းခြင်း  
- **Session Impersonation**: Session ID များကို ခိုးယူပြီး authentication ကို ရှောင်လွှဲခြင်း  
- **Resumable Stream Attacks**: Server-sent event resumption ကို အသုံးပြု၍ မကောင်းသော content ထည့်သွင်းခြင်း  

**မဖြစ်မနေလိုအပ်သော Session ထိန်းချုပ်မှုများ**:
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

**Transport Security**:
- **HTTPS Enforcement**: Session ဆက်သွယ်မှုအားလုံးကို TLS 1.3 ဖြင့် ပြုလုပ်ပါ  
- **Secure Cookie Attributes**: HttpOnly, Secure, SameSite=Strict  
- **Certificate Pinning**: MITM တိုက်ခိုက်မှုများကို တားဆီးရန် အရေးပါသော connection များအတွက်  

### **Stateful vs Stateless အတွေးအခေါ်များ**

**Stateful အကောင်အထည်ဖော်မှုများအတွက်**:
- Shared session state သည် injection တိုက်ခိုက်မှုများကို ထပ်မံကာကွယ်ရန် လိုအပ်သည်  
- Queue-based session management သည် integrity verification လိုအပ်သည်  
- Server instance များစွာအကြား session state synchronization ကို လုံခြုံစွာ ပြုလုပ်ရန် လိုအပ်သည်  

**Stateless အကောင်အထည်ဖော်မှုများအတွက်**:
- JWT သို့မဟုတ် token-based session management  
- Session state integrity ကို cryptographic verification ဖြင့် အတည်ပြုပါ  
- တိုက်ခိုက်မှုအပေါ်လျှော့ချထားသော surface သို့မဟုတ် token validation တင်းကြပ်မှု လိုအပ်သည်  

## 4. **AI အထူးပြု လုံခြုံရေးထိန်းချုပ်မှုများ**

### **Prompt Injection ကာကွယ်မှု**

**Microsoft Prompt Shields Integration**:
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

**Implementation Controls**:
- **Input Sanitization**: အသုံးပြုသူ input အားလုံးကို စုံလင်စွာ စစ်ဆေးပြီး filter ပြုလုပ်ပါ  
- **Content Boundary Definition**: System instruction နှင့် အသုံးပြုသူ content အကြား သေချာသော ခွဲခြားမှုရှိပါ  
- **Instruction Hierarchy**: Instruction များအကြား conflict ဖြစ်သောအခါ precedence rule များကို သေချာစွာ သတ်မှတ်ပါ  
- **Output Monitoring**: မကောင်းသော သို့မဟုတ် manipulated ဖြစ်သော output များကို ရှာဖွေပါ  

### **Tool Poisoning ကာကွယ်မှု**

**Tool Security Framework**:
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

**Dynamic Tool Management**:
- **Approval Workflows**: Tool modification များအတွက် အသုံးပြုသူ၏ သဘောတူညီမှုကို ရယူပါ  
- **Rollback Capabilities**: Tool version များကို ပြန်လည်ပြောင်းနိုင်စွမ်းရှိပါ  
- **Change Auditing**: Tool definition modification များ၏ အပြည့်အစုံသော မှတ်တမ်းတင်မှု  
- **Risk Assessment**: Tool လုံခြုံရေးအခြေအနေကို အလိုအလျောက် အကဲဖြတ်ပါ  

## 5. **Confused Deputy Attack ကာကွယ်မှု**

### **OAuth Proxy လုံခြုံရေး**

**Attack Prevention Controls**:
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

**Implementation Requirements**:
- **User Consent Verification**: Dynamic client registration အတွက် consent screen များကို မဖြစ်မနေပြပါ  
- **Redirect URI Validation**: Redirect destination များကို whitelist-based validation ဖြင့် စစ်ဆေးပါ  
- **Authorization Code Protection**: Single-use enforcement ဖြင့် short-lived code များကို အသုံးပြုပါ  
- **Client Identity Verification**: Client credentials နှင့် metadata ကို တင်းကြပ်စွာ စစ်ဆေးပါ  

## 6. **Tool Execution လုံခြုံရေး**

### **Sandboxing & Isolation**

**Container-Based Isolation**:
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

**Process Isolation**:
- **Separate Process Contexts**: Tool execution တစ်ခုစီကို အထူး process space တွင် ပြုလုပ်ပါ  
- **Inter-Process Communication**: Validation ဖြင့် secure IPC mechanism များကို အသုံးပြုပါ  
- **Process Monitoring**: Runtime behavior analysis နှင့် anomaly detection  
- **Resource Enforcement**: CPU, memory, I/O operation များအပေါ် hard limit များ သတ်မှတ်ပါ  

### **Least Privilege Implementation**

**Permission Management**:
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

## 7. **Supply Chain လုံခြုံရေးထိန်းချုပ်မှုများ**

### **Dependency Verification**

**Comprehensive Component Security**:
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

### **Continuous Monitoring**

**Supply Chain Threat Detection**:
- **Dependency Health Monitoring**: Dependency များအား security issue များအတွက် ဆက်လက်အကဲဖြတ်ပါ  
- **Threat Intelligence Integration**: Supply chain အန္တရာယ်များအပေါ် အချိန်နှင့်တပြေးညီ update များ  
- **Behavioral Analysis**: အပြင်ဘက် component များ၏ ထူးဆန်းသော အပြုအမူများကို ရှာဖွေပါ  
- **Automated Response**: Compromised component များကို ချက်ချင်း containment ပြုလုပ်ပါ  

## 8. **Monitoring & Detection ထိန်းချုပ်မှုများ**

### **Security Information and Event Management (SIEM)**

**Comprehensive Logging Strategy**:
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

### **Real-Time Threat Detection**

**Behavioral Analytics**:
- **User Behavior Analytics (UBA)**: အသုံးပြုသူ၏ ထူးဆန်းသော access pattern များကို ရှာဖွေပါ  
- **Entity Behavior Analytics (EBA)**: MCP server နှင့် tool behavior ကို စောင့်ကြည့်ပါ  
- **Machine Learning Anomaly Detection**: AI-powered security threat များကို ရှာဖွေပါ  
- **Threat Intelligence Correlation**: သိရှိထားသော တိုက်ခိုက်မှု pattern များနှင့် ကိုက်ညီမှုရှိသော လှုပ်ရှားမှုများကို ရှာဖွေပါ  

## 9. **Incident Response & Recovery**

### **Automated Response Capabilities**

**Immediate Response Actions**:
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

### **Forensic Capabilities**

**Investigation Support**:
- **Audit Trail Preservation**: Cryptographic integrity ဖြင့် immutable logging  
- **Evidence Collection**: လိုအပ်သော security artifact များကို အလိုအလျောက် စုဆောင်းပါ  
- **Timeline Reconstruction**: Security incident များအပေါ် အဖြစ်အပျက်များ၏ အစဉ်အလာကို ပြန်လည်တည်ဆောက်ပါ  
- **Impact Assessment**: Compromise scope နှင့် data exposure ကို အကဲဖြတ်ပါ  

## **အရေးပါသော လုံခြုံရေး Architecture အခြေခံသဘောတရားများ**

### **Defense in Depth**
- **လုံခြုံရေးအလွှာများစွာ**: လုံခြုံရေး architecture တွင် failure တစ်ခုတည်းမရှိစေရ  
- **Redundant Controls**: အရေးပါသော လုပ်ဆောင်မှုများအတွက် ထပ်တူလုံခြုံရေးအတိုင်းအတာများ  
- **Fail-Safe Mechanisms**: Error သို့မဟုတ် တိုက်ခိုက်မှုများဖြစ်ပေါ်သောအခါ secure defaults  

### **Zero Trust Implementation**
- **ယုံကြည်မှုမရှိ၊ အမြဲစစ်ဆေးပါ**: Entity နှင့် request အားလုံးကို ဆက်လက်စစ်ဆေးပါ  
- **Principle of Least Privilege**: Component အားလုံးအတွက် access rights ကို အနည်းဆုံးထားပါ  
- **Micro-Segmentation**: Network နှင့် access control များကို အလွန်သေးငယ်စွာ ခွဲခြားပါ  

### **Continuous Security Evolution**
- **Threat Landscape Adaptation**: ပေါ်ပေါက်လာသော အန္တရာယ်များကို ဖြေရှင်းရန် ပုံမှန် update ပြုလုပ်ပါ  
- **Security Control Effectiveness**: ထိန်းချုပ်မှုများ၏ ထိရောက်မှုကို ဆက်လက်အကဲဖြတ်ပြီး တိုးတက်မှုပြုလုပ်ပါ  
- **Specification Compliance**: MCP လုံခြုံရေးစံနှုန်းများနှင့် အဆက်မပြတ် ကိုက်ညီမှုရှိစေရန်  

---

## **Implementation Resources**

### **Official MCP Documentation**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Microsoft Security Solutions**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Security Standards**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST

**ဝက်ဘ်ဆိုက်မှတ်ချက်**:  
ဤစာရွက်စာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) ကို အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးစားနေပါသော်လည်း၊ အလိုအလျောက်ဘာသာပြန်ဆိုမှုများတွင် အမှားများ သို့မဟုတ် မမှန်ကန်မှုများ ပါဝင်နိုင်သည်ကို ကျေးဇူးပြု၍ သတိပြုပါ။ မူရင်းစာရွက်စာတမ်းကို ၎င်း၏ မူလဘာသာစကားဖြင့် အာဏာတည်သောရင်းမြစ်အဖြစ် သတ်မှတ်ပါ။ အရေးကြီးသောအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်ဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုမှားများ သို့မဟုတ် အဓိပ္ပာယ်မှားများအတွက် ကျွန်ုပ်တို့သည် တာဝန်မယူပါ။