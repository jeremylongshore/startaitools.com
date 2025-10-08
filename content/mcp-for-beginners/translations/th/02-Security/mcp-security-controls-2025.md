<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T14:28:24+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "th"
}
-->
# การควบคุมความปลอดภัย MCP - อัปเดตเดือนสิงหาคม 2025

> **มาตรฐานปัจจุบัน**: เอกสารนี้สะท้อนถึงข้อกำหนดด้านความปลอดภัยของ [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) และแนวปฏิบัติที่ดีที่สุดด้านความปลอดภัยของ [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) อย่างเป็นทางการ

Model Context Protocol (MCP) ได้พัฒนาไปอย่างมากด้วยการควบคุมความปลอดภัยที่เพิ่มขึ้น ซึ่งครอบคลุมทั้งความปลอดภัยของซอฟต์แวร์แบบดั้งเดิมและภัยคุกคามเฉพาะด้าน AI เอกสารนี้ให้การควบคุมความปลอดภัยที่ครอบคลุมสำหรับการใช้งาน MCP อย่างปลอดภัย ณ เดือนสิงหาคม 2025

## **ข้อกำหนดความปลอดภัยที่จำเป็น**

### **ข้อห้ามสำคัญจาก MCP Specification:**

> **ห้าม**: เซิร์ฟเวอร์ MCP **ต้องไม่** ยอมรับโทเค็นใด ๆ ที่ไม่ได้ออกให้โดยเฉพาะสำหรับเซิร์ฟเวอร์ MCP  
>
> **ห้ามใช้**: เซิร์ฟเวอร์ MCP **ต้องไม่** ใช้เซสชันสำหรับการตรวจสอบสิทธิ์  
>
> **จำเป็น**: เซิร์ฟเวอร์ MCP ที่ใช้การอนุญาต **ต้อง** ตรวจสอบคำขอขาเข้าทั้งหมด  
>
> **ข้อบังคับ**: เซิร์ฟเวอร์พร็อกซี MCP ที่ใช้ Client ID แบบคงที่ **ต้อง** ได้รับความยินยอมจากผู้ใช้สำหรับ Client ที่ลงทะเบียนแบบไดนามิกแต่ละราย  

---

## 1. **การควบคุมการตรวจสอบสิทธิ์และการอนุญาต**

### **การผสานรวมผู้ให้บริการข้อมูลประจำตัวภายนอก**

**มาตรฐาน MCP ปัจจุบัน (2025-06-18)** อนุญาตให้เซิร์ฟเวอร์ MCP มอบหมายการตรวจสอบสิทธิ์ไปยังผู้ให้บริการข้อมูลประจำตัวภายนอก ซึ่งเป็นการปรับปรุงความปลอดภัยที่สำคัญ:

**ประโยชน์ด้านความปลอดภัย:**
1. **ลดความเสี่ยงจากการตรวจสอบสิทธิ์แบบกำหนดเอง**: ลดพื้นผิวของช่องโหว่โดยหลีกเลี่ยงการใช้งานการตรวจสอบสิทธิ์แบบกำหนดเอง  
2. **ความปลอดภัยระดับองค์กร**: ใช้ประโยชน์จากผู้ให้บริการข้อมูลประจำตัวที่มีชื่อเสียง เช่น Microsoft Entra ID พร้อมคุณสมบัติความปลอดภัยขั้นสูง  
3. **การจัดการข้อมูลประจำตัวแบบรวมศูนย์**: ทำให้การจัดการวงจรชีวิตผู้ใช้ การควบคุมการเข้าถึง และการตรวจสอบการปฏิบัติตามข้อกำหนดง่ายขึ้น  
4. **การตรวจสอบสิทธิ์หลายปัจจัย**: สืบทอดความสามารถ MFA จากผู้ให้บริการข้อมูลประจำตัวระดับองค์กร  
5. **นโยบายการเข้าถึงตามเงื่อนไข**: ใช้ประโยชน์จากการควบคุมการเข้าถึงตามความเสี่ยงและการตรวจสอบสิทธิ์แบบปรับเปลี่ยนได้  

**ข้อกำหนดการใช้งาน:**
- **การตรวจสอบ Audience ของโทเค็น**: ตรวจสอบว่าโทเค็นทั้งหมดออกให้โดยเฉพาะสำหรับเซิร์ฟเวอร์ MCP  
- **การตรวจสอบ Issuer**: ตรวจสอบว่า Issuer ของโทเค็นตรงกับผู้ให้บริการข้อมูลประจำตัวที่คาดหวัง  
- **การตรวจสอบลายเซ็น**: การตรวจสอบความสมบูรณ์ของโทเค็นด้วยวิธีการเข้ารหัส  
- **การบังคับใช้การหมดอายุ**: บังคับใช้อายุการใช้งานของโทเค็นอย่างเข้มงวด  
- **การตรวจสอบ Scope**: ตรวจสอบว่าโทเค็นมีสิทธิ์ที่เหมาะสมสำหรับการดำเนินการที่ร้องขอ  

### **ความปลอดภัยของตรรกะการอนุญาต**

**การควบคุมที่สำคัญ:**
- **การตรวจสอบการอนุญาตอย่างครอบคลุม**: การตรวจสอบความปลอดภัยเป็นประจำสำหรับจุดตัดสินใจการอนุญาตทั้งหมด  
- **ค่าเริ่มต้นที่ปลอดภัย**: ปฏิเสธการเข้าถึงเมื่อตรรกะการอนุญาตไม่สามารถตัดสินใจได้อย่างชัดเจน  
- **ขอบเขตของสิทธิ์**: การแยกที่ชัดเจนระหว่างระดับสิทธิ์และการเข้าถึงทรัพยากร  
- **การบันทึกการตรวจสอบ**: การบันทึกการตัดสินใจการอนุญาตทั้งหมดเพื่อการตรวจสอบความปลอดภัย  
- **การตรวจสอบการเข้าถึงเป็นประจำ**: การตรวจสอบสิทธิ์ของผู้ใช้และการกำหนดสิทธิ์เป็นระยะ  

## 2. **ความปลอดภัยของโทเค็นและการควบคุมการป้องกันการส่งผ่าน**

### **การป้องกันการส่งผ่านโทเค็น**

**การส่งผ่านโทเค็นถูกห้ามอย่างชัดเจน** ใน MCP Authorization Specification เนื่องจากความเสี่ยงด้านความปลอดภัยที่สำคัญ:

**ความเสี่ยงด้านความปลอดภัยที่ได้รับการแก้ไข:**
- **การหลีกเลี่ยงการควบคุม**: ข้ามการควบคุมความปลอดภัยที่สำคัญ เช่น การจำกัดอัตรา การตรวจสอบคำขอ และการตรวจสอบการรับส่งข้อมูล  
- **การล่มสลายของความรับผิดชอบ**: ทำให้การระบุ Client เป็นไปไม่ได้ ทำให้เส้นทางการตรวจสอบและการสอบสวนเหตุการณ์เสียหาย  
- **การขโมยข้อมูลผ่านพร็อกซี**: เปิดโอกาสให้ผู้ไม่หวังดีใช้เซิร์ฟเวอร์เป็นพร็อกซีสำหรับการเข้าถึงข้อมูลโดยไม่ได้รับอนุญาต  
- **การละเมิดขอบเขตความไว้วางใจ**: ทำลายสมมติฐานความไว้วางใจของบริการปลายทางเกี่ยวกับแหล่งที่มาของโทเค็น  
- **การเคลื่อนที่ในแนวราบ**: โทเค็นที่ถูกบุกรุกในหลายบริการช่วยให้การโจมตีขยายตัวได้กว้างขึ้น  

**การควบคุมการใช้งาน:**
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

### **รูปแบบการจัดการโทเค็นอย่างปลอดภัย**

**แนวปฏิบัติที่ดีที่สุด:**
- **โทเค็นอายุสั้น**: ลดหน้าต่างการเปิดเผยด้วยการหมุนเวียนโทเค็นบ่อยครั้ง  
- **การออกโทเค็นแบบ Just-in-Time**: ออกโทเค็นเฉพาะเมื่อจำเป็นสำหรับการดำเนินการเฉพาะ  
- **การจัดเก็บอย่างปลอดภัย**: ใช้โมดูลความปลอดภัยฮาร์ดแวร์ (HSM) หรือที่เก็บคีย์ที่ปลอดภัย  
- **การผูกโทเค็น**: ผูกโทเค็นกับ Client เซสชัน หรือการดำเนินการเฉพาะเมื่อเป็นไปได้  
- **การตรวจสอบและแจ้งเตือน**: การตรวจจับแบบเรียลไทม์สำหรับการใช้โทเค็นในทางที่ผิดหรือรูปแบบการเข้าถึงโดยไม่ได้รับอนุญาต  

## 3. **การควบคุมความปลอดภัยของเซสชัน**

### **การป้องกันการแย่งชิงเซสชัน**

**ช่องทางการโจมตีที่ได้รับการแก้ไข:**
- **การแย่งชิงเซสชันผ่านการฉีดคำสั่ง**: เหตุการณ์ที่เป็นอันตรายที่ถูกฉีดเข้าไปในสถานะเซสชันที่ใช้ร่วมกัน  
- **การปลอมแปลงเซสชัน**: การใช้ ID เซสชันที่ถูกขโมยโดยไม่ได้รับอนุญาตเพื่อข้ามการตรวจสอบสิทธิ์  
- **การโจมตีการสตรีมที่สามารถกลับมาใช้งานได้**: การใช้ประโยชน์จากการส่งเหตุการณ์ของเซิร์ฟเวอร์ที่กลับมาใช้งานได้เพื่อฉีดเนื้อหาที่เป็นอันตราย  

**การควบคุมเซสชันที่จำเป็น:**
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

**ความปลอดภัยในการรับส่งข้อมูล:**
- **การบังคับใช้ HTTPS**: การสื่อสารเซสชันทั้งหมดผ่าน TLS 1.3  
- **คุณสมบัติคุกกี้ที่ปลอดภัย**: HttpOnly, Secure, SameSite=Strict  
- **การตรึงใบรับรอง**: สำหรับการเชื่อมต่อที่สำคัญเพื่อป้องกันการโจมตี MITM  

### **การพิจารณา Stateful vs Stateless**

**สำหรับการใช้งานแบบ Stateful:**
- สถานะเซสชันที่ใช้ร่วมกันต้องการการป้องกันเพิ่มเติมจากการโจมตีแบบฉีด  
- การจัดการเซสชันแบบคิวต้องการการตรวจสอบความสมบูรณ์  
- อินสแตนซ์เซิร์ฟเวอร์หลายตัวต้องการการซิงโครไนซ์สถานะเซสชันที่ปลอดภัย  

**สำหรับการใช้งานแบบ Stateless:**
- การจัดการเซสชันแบบโทเค็น เช่น JWT  
- การตรวจสอบความสมบูรณ์ของสถานะเซสชันด้วยวิธีการเข้ารหัส  
- ลดพื้นผิวการโจมตี แต่ต้องการการตรวจสอบโทเค็นที่แข็งแกร่ง  

## 4. **การควบคุมความปลอดภัยเฉพาะด้าน AI**

### **การป้องกันการฉีดคำสั่งใน Prompt**

**การผสานรวม Microsoft Prompt Shields:**
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

**การควบคุมการใช้งาน:**
- **การตรวจสอบความถูกต้องของข้อมูลนำเข้า**: การตรวจสอบและกรองข้อมูลนำเข้าของผู้ใช้อย่างครอบคลุม  
- **การกำหนดขอบเขตเนื้อหา**: การแยกที่ชัดเจนระหว่างคำสั่งของระบบและเนื้อหาของผู้ใช้  
- **ลำดับชั้นของคำสั่ง**: กฎการจัดลำดับความสำคัญที่เหมาะสมสำหรับคำสั่งที่ขัดแย้งกัน  
- **การตรวจสอบผลลัพธ์**: การตรวจจับผลลัพธ์ที่อาจเป็นอันตรายหรือถูกจัดการ  

### **การป้องกันการปนเปื้อนเครื่องมือ**

**กรอบความปลอดภัยของเครื่องมือ:**
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

**การจัดการเครื่องมือแบบไดนามิก:**
- **กระบวนการอนุมัติ**: ความยินยอมของผู้ใช้ที่ชัดเจนสำหรับการแก้ไขเครื่องมือ  
- **ความสามารถในการย้อนกลับ**: ความสามารถในการย้อนกลับไปยังเวอร์ชันเครื่องมือก่อนหน้า  
- **การตรวจสอบการเปลี่ยนแปลง**: ประวัติการแก้ไขคำจำกัดความของเครื่องมืออย่างสมบูรณ์  
- **การประเมินความเสี่ยง**: การประเมินความปลอดภัยของเครื่องมือโดยอัตโนมัติ  

## 5. **การป้องกันการโจมตี Confused Deputy**

### **ความปลอดภัยของ OAuth Proxy**

**การควบคุมการป้องกันการโจมตี:**
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

**ข้อกำหนดการใช้งาน:**
- **การตรวจสอบความยินยอมของผู้ใช้**: ห้ามข้ามหน้าจอความยินยอมสำหรับการลงทะเบียน Client แบบไดนามิก  
- **การตรวจสอบ Redirect URI**: การตรวจสอบปลายทางการเปลี่ยนเส้นทางตามรายการที่อนุญาตอย่างเข้มงวด  
- **การป้องกัน Authorization Code**: โค้ดที่มีอายุสั้นพร้อมการบังคับใช้การใช้งานครั้งเดียว  
- **การตรวจสอบข้อมูลประจำตัวของ Client**: การตรวจสอบข้อมูลรับรองและเมตาดาตาของ Client อย่างเข้มงวด  

## 6. **ความปลอดภัยในการดำเนินการเครื่องมือ**

### **การแยกและการจำกัดพื้นที่**

**การแยกด้วย Container:**
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

**การแยกกระบวนการ:**
- **บริบทกระบวนการแยกต่างหาก**: การดำเนินการเครื่องมือแต่ละครั้งในพื้นที่กระบวนการที่แยกออกจากกัน  
- **การสื่อสารระหว่างกระบวนการ**: กลไก IPC ที่ปลอดภัยพร้อมการตรวจสอบ  
- **การตรวจสอบกระบวนการ**: การวิเคราะห์พฤติกรรมระหว่างการทำงานและการตรวจจับความผิดปกติ  
- **การบังคับใช้ทรัพยากร**: ขีดจำกัดที่เข้มงวดสำหรับ CPU หน่วยความจำ และการดำเนินการ I/O  

### **การใช้งานสิทธิ์ขั้นต่ำ**

**การจัดการสิทธิ์:**
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

## 7. **การควบคุมความปลอดภัยของห่วงโซ่อุปทาน**

### **การตรวจสอบการพึ่งพา**

**ความปลอดภัยของส่วนประกอบอย่างครอบคลุม:**
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

### **การตรวจสอบอย่างต่อเนื่อง**

**การตรวจจับภัยคุกคามในห่วงโซ่อุปทาน:**
- **การตรวจสอบสุขภาพของการพึ่งพา**: การประเมินความปลอดภัยของการพึ่งพาทั้งหมดอย่างต่อเนื่อง  
- **การผสานรวมข้อมูลภัยคุกคาม**: การอัปเดตแบบเรียลไทม์เกี่ยวกับภัยคุกคามในห่วงโซ่อุปทานที่เกิดขึ้นใหม่  
- **การวิเคราะห์พฤติกรรม**: การตรวจจับพฤติกรรมที่ผิดปกติในส่วนประกอบภายนอก  
- **การตอบสนองอัตโนมัติ**: การควบคุมส่วนประกอบที่ถูกบุกรุกทันที  

## 8. **การควบคุมการตรวจสอบและการตรวจจับ**

### **การจัดการข้อมูลและเหตุการณ์ด้านความปลอดภัย (SIEM)**

**กลยุทธ์การบันทึกอย่างครอบคลุม:**
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

### **การตรวจจับภัยคุกคามแบบเรียลไทม์**

**การวิเคราะห์พฤติกรรม:**
- **การวิเคราะห์พฤติกรรมผู้ใช้ (UBA)**: การตรวจจับรูปแบบการเข้าถึงผู้ใช้ที่ผิดปกติ  
- **การวิเคราะห์พฤติกรรมของเอนทิตี (EBA)**: การตรวจสอบพฤติกรรมของเซิร์ฟเวอร์ MCP และเครื่องมือ  
- **การตรวจจับความผิดปกติด้วย Machine Learning**: การระบุภัยคุกคามด้านความปลอดภัยด้วย AI  
- **การเชื่อมโยงข้อมูลภัยคุกคาม**: การจับคู่กิจกรรมที่สังเกตได้กับรูปแบบการโจมตีที่ทราบ  

## 9. **การตอบสนองและการกู้คืนเหตุการณ์**

### **ความสามารถในการตอบสนองอัตโนมัติ**

**การดำเนินการตอบสนองทันที:**
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

### **ความสามารถด้านนิติวิทยาศาสตร์**

**การสนับสนุนการสอบสวน:**
- **การรักษาเส้นทางการตรวจสอบ**: การบันทึกที่ไม่เปลี่ยนแปลงพร้อมความสมบูรณ์ของการเข้ารหัส  
- **การรวบรวมหลักฐาน**: การรวบรวมสิ่งประดิษฐ์ด้านความปลอดภัยที่เกี่ยวข้องโดยอัตโนมัติ  
- **การสร้างลำดับเหตุการณ์**: ลำดับเหตุการณ์โดยละเอียดที่นำไปสู่เหตุการณ์ด้านความปลอดภัย  
- **การประเมินผลกระทบ**: การประเมินขอบเขตของการบุกรุกและการเปิดเผยข้อมูล  

## **หลักการสถาปัตยกรรมความปลอดภัยที่สำคัญ**

### **การป้องกันในเชิงลึก**
- **หลายชั้นของความปลอดภัย**: ไม่มีจุดล้มเหลวเพียงจุดเดียวในสถาปัตยกรรมความปลอดภัย  
- **การควบคุมที่ซ้ำซ้อน**: มาตรการความปลอดภัยที่ทับซ้อนกันสำหรับฟังก์ชันที่สำคัญ  
- **กลไก Fail-Safe**: ค่าเริ่มต้นที่ปลอดภัยเมื่อระบบพบข้อผิดพลาดหรือการโจมตี  

### **การใช้งาน Zero Trust**
- **ไม่เชื่อถือใคร ตรวจสอบเสมอ**: การตรวจสอบอย่างต่อเนื่องของเอนทิตีและคำขอทั้งหมด  
- **หลักการสิทธิ์ขั้นต่ำ**: สิทธิ์การเข้าถึงขั้นต่ำสำหรับส่วนประกอบทั้งหมด  
- **การแบ่งส่วนย่อย**: การควบคุมเครือข่ายและการเข้าถึงในระดับละเอียด  

### **การพัฒนาความปลอดภัยอย่างต่อเนื่อง**
- **การปรับตัวต่อภูมิทัศน์ภัยคุกคาม**: การอัปเดตเป็นประจำเพื่อจัดการกับภัยคุกคามที่เกิดขึ้นใหม่  
- **ประสิทธิภาพของการควบคุมความปลอดภัย**: การประเมินและปรับปรุงการควบคุมอย่างต่อเนื่อง  
- **การปฏิบัติตามข้อกำหนดของข้อกำหนด**: การปรับให้สอดคล้องกับมาตรฐานความปลอดภัย MCP ที่พัฒนาอย่างต่อ

**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) แม้ว่าเราจะพยายามให้การแปลมีความถูกต้อง แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่แม่นยำ เอกสารต้นฉบับในภาษาดั้งเดิมควรถือเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ขอแนะนำให้ใช้บริการแปลภาษาจากผู้เชี่ยวชาญที่เป็นมนุษย์ เราจะไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดซึ่งเกิดจากการใช้การแปลนี้