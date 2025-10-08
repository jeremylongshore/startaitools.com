<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T15:07:26+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "bn"
}
-->
# MCP নিরাপত্তা নিয়ন্ত্রণ - আগস্ট ২০২৫ আপডেট

> **বর্তমান মান**: এই ডকুমেন্টটি [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) এর নিরাপত্তা প্রয়োজনীয়তা এবং অফিসিয়াল [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) প্রতিফলিত করে।

মডেল কনটেক্সট প্রোটোকল (MCP) উল্লেখযোগ্যভাবে উন্নত হয়েছে, যেখানে ঐতিহ্যবাহী সফটওয়্যার নিরাপত্তা এবং AI-নির্দিষ্ট হুমকির জন্য উন্নত নিরাপত্তা নিয়ন্ত্রণ অন্তর্ভুক্ত করা হয়েছে। এই ডকুমেন্টটি আগস্ট ২০২৫ পর্যন্ত নিরাপদ MCP বাস্তবায়নের জন্য বিস্তৃত নিরাপত্তা নিয়ন্ত্রণ প্রদান করে।

## **আবশ্যিক নিরাপত্তা প্রয়োজনীয়তা**

### **MCP স্পেসিফিকেশন থেকে গুরুত্বপূর্ণ নিষেধাজ্ঞা:**

> **নিষিদ্ধ**: MCP সার্ভার **কোনো টোকেন গ্রহণ করতে পারবে না** যা MCP সার্ভারের জন্য স্পষ্টভাবে ইস্যু করা হয়নি  
>
> **নিষিদ্ধ**: MCP সার্ভার **অথেনটিকেশনের জন্য সেশন ব্যবহার করতে পারবে না**  
>
> **আবশ্যিক**: MCP সার্ভার যা অথরাইজেশন বাস্তবায়ন করে **প্রত্যেক ইনবাউন্ড অনুরোধ যাচাই করতে হবে**  
>
> **আবশ্যিক**: MCP প্রক্সি সার্ভার যা স্ট্যাটিক ক্লায়েন্ট আইডি ব্যবহার করে **প্রত্যেক ডায়নামিকভাবে নিবন্ধিত ক্লায়েন্টের জন্য ব্যবহারকারীর সম্মতি পেতে হবে**

---

## ১. **অথেনটিকেশন ও অথরাইজেশন নিয়ন্ত্রণ**

### **বাহ্যিক পরিচয় প্রদানকারী ইন্টিগ্রেশন**

**বর্তমান MCP স্ট্যান্ডার্ড (2025-06-18)** MCP সার্ভারকে বাহ্যিক পরিচয় প্রদানকারীদের কাছে অথেনটিকেশন ডেলিগেট করার অনুমতি দেয়, যা একটি উল্লেখযোগ্য নিরাপত্তা উন্নতি উপস্থাপন করে:

**নিরাপত্তা সুবিধা:**
1. **কাস্টম অথেনটিকেশন ঝুঁকি দূর করে**: কাস্টম অথেনটিকেশন বাস্তবায়ন এড়িয়ে দুর্বলতার পৃষ্ঠতল হ্রাস করে  
2. **এন্টারপ্রাইজ-গ্রেড নিরাপত্তা**: Microsoft Entra ID-এর মতো প্রতিষ্ঠিত পরিচয় প্রদানকারীদের উন্নত নিরাপত্তা বৈশিষ্ট্য ব্যবহার করে  
3. **কেন্দ্রীভূত পরিচয় ব্যবস্থাপনা**: ব্যবহারকারীর জীবনচক্র ব্যবস্থাপনা, অ্যাক্সেস নিয়ন্ত্রণ এবং কমপ্লায়েন্স অডিটিং সহজ করে  
4. **মাল্টি-ফ্যাক্টর অথেনটিকেশন**: এন্টারপ্রাইজ পরিচয় প্রদানকারীদের থেকে MFA ক্ষমতা গ্রহণ করে  
5. **শর্তাধীন অ্যাক্সেস নীতি**: ঝুঁকি-ভিত্তিক অ্যাক্সেস নিয়ন্ত্রণ এবং অভিযোজিত অথেনটিকেশন সুবিধা প্রদান করে  

**বাস্তবায়ন প্রয়োজনীয়তা:**
- **টোকেন অডিয়েন্স যাচাই**: নিশ্চিত করুন যে সমস্ত টোকেন MCP সার্ভারের জন্য স্পষ্টভাবে ইস্যু করা হয়েছে  
- **ইস্যুয়ার যাচাই**: টোকেন ইস্যুয়ার প্রত্যাশিত পরিচয় প্রদানকারীর সাথে মিলে যাচাই করুন  
- **স্বাক্ষর যাচাই**: টোকেনের অখণ্ডতার ক্রিপ্টোগ্রাফিক যাচাই  
- **মেয়াদ শেষ হওয়ার প্রয়োগ**: টোকেনের জীবনকাল সীমার কঠোর প্রয়োগ  
- **স্কোপ যাচাই**: নিশ্চিত করুন যে টোকেনগুলিতে অনুরোধকৃত অপারেশনের জন্য যথাযথ অনুমতি রয়েছে  

### **অথরাইজেশন লজিক নিরাপত্তা**

**গুরুত্বপূর্ণ নিয়ন্ত্রণ:**
- **বিস্তৃত অথরাইজেশন অডিট**: সমস্ত অথরাইজেশন সিদ্ধান্ত পয়েন্টের নিয়মিত নিরাপত্তা পর্যালোচনা  
- **ফেল-সেফ ডিফল্ট**: অথরাইজেশন লজিক একটি চূড়ান্ত সিদ্ধান্ত নিতে না পারলে অ্যাক্সেস অস্বীকার করুন  
- **অনুমতির সীমানা**: বিভিন্ন বিশেষাধিকার স্তর এবং রিসোর্স অ্যাক্সেসের মধ্যে স্পষ্ট বিভাজন  
- **অডিট লগিং**: নিরাপত্তা পর্যবেক্ষণের জন্য সমস্ত অথরাইজেশন সিদ্ধান্তের সম্পূর্ণ লগিং  
- **নিয়মিত অ্যাক্সেস পর্যালোচনা**: ব্যবহারকারীর অনুমতি এবং বিশেষাধিকার বরাদ্দের পর্যায়ক্রমিক যাচাই  

## ২. **টোকেন নিরাপত্তা ও অ্যান্টি-পাসথ্রু নিয়ন্ত্রণ**

### **টোকেন পাসথ্রু প্রতিরোধ**

**MCP অথরাইজেশন স্পেসিফিকেশনে টোকেন পাসথ্রু স্পষ্টভাবে নিষিদ্ধ** কারণ এটি গুরুতর নিরাপত্তা ঝুঁকি সৃষ্টি করে:

**নিরাপত্তা ঝুঁকি সমাধান:**
- **নিয়ন্ত্রণ এড়ানো**: রেট লিমিটিং, অনুরোধ যাচাই এবং ট্রাফিক পর্যবেক্ষণের মতো গুরুত্বপূর্ণ নিরাপত্তা নিয়ন্ত্রণ বাইপাস করে  
- **দায়িত্বহীনতা**: ক্লায়েন্ট সনাক্তকরণ অসম্ভব করে, অডিট ট্রেইল এবং ঘটনা তদন্তকে দুর্নীতিগ্রস্ত করে  
- **প্রক্সি-ভিত্তিক ডেটা চুরি**: সার্ভারকে অননুমোদিত ডেটা অ্যাক্সেসের জন্য প্রক্সি হিসাবে ব্যবহার করার সুযোগ দেয়  
- **বিশ্বাস সীমা লঙ্ঘন**: টোকেনের উৎস সম্পর্কে ডাউনস্ট্রিম পরিষেবার বিশ্বাসের অনুমান ভেঙে দেয়  
- **ল্যাটারাল মুভমেন্ট**: একাধিক পরিষেবার মধ্যে ক্ষতিগ্রস্ত টোকেনগুলি বিস্তৃত আক্রমণের প্রসার সক্ষম করে  

**বাস্তবায়ন নিয়ন্ত্রণ:**
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

### **নিরাপদ টোকেন ব্যবস্থাপনা প্যাটার্ন**

**সেরা অনুশীলন:**
- **স্বল্প-মেয়াদী টোকেন**: ঘন ঘন টোকেন রোটেশনের মাধ্যমে এক্সপোজার উইন্ডো হ্রাস করুন  
- **জাস্ট-ইন-টাইম ইস্যুয়েন্স**: নির্দিষ্ট অপারেশনের জন্য প্রয়োজন হলে টোকেন ইস্যু করুন  
- **নিরাপদ স্টোরেজ**: হার্ডওয়্যার নিরাপত্তা মডিউল (HSM) বা নিরাপদ কী ভল্ট ব্যবহার করুন  
- **টোকেন বাইন্ডিং**: টোকেনগুলিকে নির্দিষ্ট ক্লায়েন্ট, সেশন বা অপারেশনের সাথে সংযুক্ত করুন যেখানে সম্ভব  
- **পর্যবেক্ষণ ও সতর্কতা**: টোকেনের অপব্যবহার বা অননুমোদিত অ্যাক্সেস প্যাটার্নের রিয়েল-টাইম সনাক্তকরণ  

## ৩. **সেশন নিরাপত্তা নিয়ন্ত্রণ**

### **সেশন হাইজ্যাকিং প্রতিরোধ**

**আক্রমণের ভেক্টর সমাধান:**
- **সেশন হাইজ্যাক প্রম্পট ইনজেকশন**: শেয়ার করা সেশন স্টেটে ক্ষতিকারক ইভেন্ট ইনজেক্ট করা  
- **সেশন ইমপারসনেশন**: চুরি করা সেশন আইডি ব্যবহার করে অননুমোদিত অথেনটিকেশন বাইপাস  
- **রিজুমেবল স্ট্রিম আক্রমণ**: সার্ভার-সেন্ট ইভেন্ট পুনরায় শুরু করার সুযোগ নিয়ে ক্ষতিকারক বিষয়বস্তু ইনজেকশন  

**আবশ্যিক সেশন নিয়ন্ত্রণ:**
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

**পরিবহন নিরাপত্তা:**
- **HTTPS প্রয়োগ**: TLS 1.3 এর মাধ্যমে সমস্ত সেশন যোগাযোগ  
- **নিরাপদ কুকি অ্যাট্রিবিউট**: HttpOnly, Secure, SameSite=Strict  
- **সার্টিফিকেট পিনিং**: MITM আক্রমণ প্রতিরোধের জন্য গুরুত্বপূর্ণ সংযোগে  

### **স্টেটফুল বনাম স্টেটলেস বিবেচনা**

**স্টেটফুল বাস্তবায়নের জন্য:**
- শেয়ার করা সেশন স্টেট ইনজেকশন আক্রমণের বিরুদ্ধে অতিরিক্ত সুরক্ষা প্রয়োজন  
- কিউ-ভিত্তিক সেশন ব্যবস্থাপনার অখণ্ডতা যাচাই প্রয়োজন  
- একাধিক সার্ভার ইনস্ট্যান্সের জন্য নিরাপদ সেশন স্টেট সিঙ্ক্রোনাইজেশন প্রয়োজন  

**স্টেটলেস বাস্তবায়নের জন্য:**
- JWT বা অনুরূপ টোকেন-ভিত্তিক সেশন ব্যবস্থাপনা  
- সেশন স্টেট অখণ্ডতার ক্রিপ্টোগ্রাফিক যাচাই  
- আক্রমণের পৃষ্ঠতল হ্রাস, তবে শক্তিশালী টোকেন যাচাই প্রয়োজন  

## ৪. **AI-নির্দিষ্ট নিরাপত্তা নিয়ন্ত্রণ**

### **প্রম্পট ইনজেকশন প্রতিরোধ**

**Microsoft Prompt Shields ইন্টিগ্রেশন:**
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

**বাস্তবায়ন নিয়ন্ত্রণ:**
- **ইনপুট স্যানিটাইজেশন**: সমস্ত ব্যবহারকারীর ইনপুটের বিস্তৃত যাচাই এবং ফিল্টারিং  
- **বিষয়বস্তু সীমা সংজ্ঞা**: সিস্টেম নির্দেশনা এবং ব্যবহারকারীর বিষয়বস্তু মধ্যে স্পষ্ট বিভাজন  
- **নির্দেশনার শ্রেণিবিন্যাস**: বিরোধপূর্ণ নির্দেশনার জন্য যথাযথ অগ্রাধিকার নিয়ম  
- **আউটপুট পর্যবেক্ষণ**: সম্ভাব্য ক্ষতিকারক বা ম্যানিপুলেটেড আউটপুট সনাক্তকরণ  

### **টুল পয়জনিং প্রতিরোধ**

**টুল নিরাপত্তা কাঠামো:**
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

**ডায়নামিক টুল ব্যবস্থাপনা:**
- **অনুমোদন কর্মপ্রবাহ**: টুল পরিবর্তনের জন্য ব্যবহারকারীর স্পষ্ট সম্মতি  
- **রোলব্যাক ক্ষমতা**: পূর্ববর্তী টুল সংস্করণে ফিরে যাওয়ার ক্ষমতা  
- **পরিবর্তন অডিটিং**: টুল সংজ্ঞা পরিবর্তনের সম্পূর্ণ ইতিহাস  
- **ঝুঁকি মূল্যায়ন**: টুল নিরাপত্তা অবস্থানের স্বয়ংক্রিয় মূল্যায়ন  

## ৫. **কনফিউজড ডেপুটি আক্রমণ প্রতিরোধ**

### **OAuth প্রক্সি নিরাপত্তা**

**আক্রমণ প্রতিরোধ নিয়ন্ত্রণ:**
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

**বাস্তবায়ন প্রয়োজনীয়তা:**
- **ব্যবহারকারীর সম্মতি যাচাই**: ডায়নামিক ক্লায়েন্ট নিবন্ধনের জন্য সম্মতি স্ক্রিন কখনো এড়িয়ে যাবেন না  
- **রিডাইরেক্ট URI যাচাই**: রিডাইরেক্ট গন্তব্যের কঠোর হোয়াইটলিস্ট-ভিত্তিক যাচাই  
- **অথরাইজেশন কোড সুরক্ষা**: স্বল্প-মেয়াদী কোডের একক-ব্যবহার প্রয়োগ  
- **ক্লায়েন্ট পরিচয় যাচাই**: ক্লায়েন্টের শংসাপত্র এবং মেটাডেটার শক্তিশালী যাচাই  

## ৬. **টুল এক্সিকিউশন নিরাপত্তা**

### **স্যান্ডবক্সিং ও আইসোলেশন**

**কন্টেইনার-ভিত্তিক আইসোলেশন:**
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

**প্রক্রিয়া আইসোলেশন:**
- **আলাদা প্রক্রিয়া প্রসঙ্গ**: প্রতিটি টুল এক্সিকিউশন পৃথক প্রক্রিয়া স্পেসে  
- **ইন্টার-প্রক্রিয়া যোগাযোগ**: যাচাই সহ নিরাপদ IPC মেকানিজম  
- **প্রক্রিয়া পর্যবেক্ষণ**: রানটাইম আচরণ বিশ্লেষণ এবং অস্বাভাবিকতা সনাক্তকরণ  
- **রিসোর্স প্রয়োগ**: CPU, মেমরি এবং I/O অপারেশনের উপর কঠোর সীমা  

### **ন্যূনতম বিশেষাধিকার বাস্তবায়ন**

**অনুমতি ব্যবস্থাপনা:**
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

## ৭. **সরবরাহ চেইন নিরাপত্তা নিয়ন্ত্রণ**

### **নির্ভরতা যাচাই**

**বিস্তৃত উপাদান নিরাপত্তা:**
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

### **নিরবিচ্ছিন্ন পর্যবেক্ষণ**

**সরবরাহ চেইন হুমকি সনাক্তকরণ:**
- **নির্ভরতা স্বাস্থ্য পর্যবেক্ষণ**: নিরাপত্তা সমস্যার জন্য সমস্ত নির্ভরতার ক্রমাগত মূল্যায়ন  
- **হুমকি বুদ্ধিমত্তা ইন্টিগ্রেশন**: উদীয়মান সরবরাহ চেইন হুমকির উপর রিয়েল-টাইম আপডেট  
- **আচরণগত বিশ্লেষণ**: বাহ্যিক উপাদানগুলির অস্বাভাবিক আচরণ সনাক্তকরণ  
- **স্বয়ংক্রিয় প্রতিক্রিয়া**: আপসকৃত উপাদানগুলির তাৎক্ষণিক নিয়ন্ত্রণ  

## ৮. **পর্যবেক্ষণ ও সনাক্তকরণ নিয়ন্ত্রণ**

### **নিরাপত্তা তথ্য ও ইভেন্ট ব্যবস্থাপনা (SIEM)**

**বিস্তৃত লগিং কৌশল:**
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

### **রিয়েল-টাইম হুমকি সনাক্তকরণ**

**আচরণগত বিশ্লেষণ:**
- **ব্যবহারকারীর আচরণ বিশ্লেষণ (UBA)**: অস্বাভাবিক ব্যবহারকারীর অ্যাক্সেস প্যাটার্ন সনাক্তকরণ  
- **সত্তার আচরণ বিশ্লেষণ (EBA)**: MCP সার্ভার এবং টুলের আচরণ পর্যবেক্ষণ  
- **মেশিন লার্নিং অস্বাভাবিকতা সনাক্তকরণ**: AI-চালিত নিরাপত্তা হুমকি সনাক্তকরণ  
- **হুমকি বুদ্ধিমত্তা সম্পর্ক**: পরিচিত আক্রমণের প্যাটার্নের সাথে পর্যবেক্ষিত কার্যকলাপের মিল  

## ৯. **ঘটনা প্রতিক্রিয়া ও পুনরুদ্ধার**

### **স্বয়ংক্রিয় প্রতিক্রিয়া ক্ষমতা**

**তাৎক্ষণিক প্রতিক্রিয়া কর্ম:**
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

### **ফরেনসিক ক্ষমতা**

**তদন্ত সহায়তা:**
- **অডিট ট্রেইল সংরক্ষণ**: ক্রিপ্টোগ্রাফিক অখণ্ডতার সাথে অপরিবর্তনীয় লগিং  
- **প্রমাণ সংগ্রহ**: প্রাসঙ্গিক নিরাপত্তা আর্টিফ্যাক্টের স্বয়ংক্রিয় সংগ্রহ  
- **টাইমলাইন পুনর্গঠন**: নিরাপত্তা ঘটনার দিকে নিয়ে যাওয়া ঘটনাগুলির বিস্তারিত ক্রম  
- **প্রভাব মূল্যায়ন**: আপসের পরিধি এবং ডেটা এক্সপোজার মূল্যায়ন  

## **মূল নিরাপত্তা স্থাপত্য নীতিমালা**

### **ডিফেন্স ইন ডেপথ**
- **একাধিক নিরাপত্তা স্তর**: নিরাপত্তা স্থাপত্যে কোনো একক ব্যর্থতার পয়েন্ট নেই  
- **অতিরিক্ত নিয়ন্ত্রণ**: গুরুত্বপূর্ণ ফাংশনের জন্য ওভারল্যাপিং নিরাপত্তা ব্যবস্থা  
- **ফেল-সেফ মেকানিজম**: সিস্টেম ত্রুটি বা আক্রমণের সম্মুখীন হলে নিরাপদ ডিফল্ট  

### **জিরো ট্রাস্ট বাস্তবায়ন**
- **কখনো বিশ্বাস করবেন না, সবসময় যাচাই করুন**: সমস্ত সত্তা এবং অনুরোধের ক্রমাগত যাচাই  
- **ন্যূনতম বিশেষাধিকার নীতি**: সমস্ত উপাদানের জন্য সর্বনিম্ন অ্যাক্সেস অধিকার  
- **মাইক্রো-সেগমেন্টেশন**: গ্রানুলার নেটওয়ার্ক এবং অ্যাক্সেস নিয়ন্ত্রণ  

### **নিরবিচ্ছিন্ন নিরাপত্তা বিবর্তন**
- **হুমকি ল্যান্ডস্কেপ অভিযোজন**: উদীয়মান হুমকির মোকাবিলায় নিয়মিত আপডেট  
- **নিরাপত্তা নিয়ন্ত্রণ কার্যকারিতা**: নিয়ন্ত্রণের চলমান মূল্যায়ন এবং উন্নতি  
- **স্পেসিফিকেশন সম্মতি**: পরিবর্তিত MCP নিরাপত্তা মানগুলির সাথে সামঞ্জস্য  

---

## **বাস্তবায়ন সম্পদ**

### **অফিসিয়াল MCP ডকুমেন্টেশন**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **মাইক্রোসফট নিরাপত্তা সমাধান**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **নিরাপত্তা মান**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)  

---

> **গুরুত্বপূর্ণ**: এই নিরাপত্তা নিয়ন্ত্রণগুলি বর্তমান MCP স্পেসিফিকেশন (2025-06-18) প্রতিফলিত করে। MCP নিরাপত্তা মান দ্রুত পরিবর্তিত হওয়ার কারণে সর্বদা সর্বশেষ [অফিসিয়াল ডকুমেন্টেশন](https://spec

**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনুবাদ করা হয়েছে। আমরা যথাসাধ্য সঠিকতার জন্য চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। এর মূল ভাষায় থাকা নথিটিকে প্রামাণিক উৎস হিসেবে বিবেচনা করা উচিত। গুরুত্বপূর্ণ তথ্যের জন্য, পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদ ব্যবহারের ফলে কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যা হলে আমরা দায়বদ্ধ থাকব না।