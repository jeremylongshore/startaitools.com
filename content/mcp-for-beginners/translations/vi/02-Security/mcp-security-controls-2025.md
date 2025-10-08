<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T17:18:06+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "vi"
}
-->
# Các Biện Pháp Kiểm Soát An Ninh MCP - Cập Nhật Tháng 8 Năm 2025

> **Tiêu Chuẩn Hiện Tại**: Tài liệu này phản ánh các yêu cầu an ninh của [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) và [Thực Hành Tốt Nhất Về An Ninh MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

Giao thức Model Context Protocol (MCP) đã phát triển đáng kể với các biện pháp kiểm soát an ninh được nâng cao, giải quyết cả các mối đe dọa an ninh phần mềm truyền thống và các mối đe dọa đặc thù của AI. Tài liệu này cung cấp các biện pháp kiểm soát an ninh toàn diện để triển khai MCP an toàn tính đến tháng 8 năm 2025.

## **Yêu Cầu An Ninh BẮT BUỘC**

### **Những Điều Cấm Quan Trọng từ MCP Specification:**

> **CẤM**: Máy chủ MCP **KHÔNG ĐƯỢC** chấp nhận bất kỳ token nào không được phát hành rõ ràng cho máy chủ MCP  
>
> **CẤM**: Máy chủ MCP **KHÔNG ĐƯỢC** sử dụng phiên làm việc để xác thực  
>
> **YÊU CẦU**: Máy chủ MCP triển khai ủy quyền **PHẢI** xác minh TẤT CẢ các yêu cầu đến  
>
> **BẮT BUỘC**: Máy chủ proxy MCP sử dụng ID khách hàng tĩnh **PHẢI** nhận được sự đồng ý của người dùng cho mỗi khách hàng được đăng ký động  

---

## 1. **Kiểm Soát Xác Thực & Ủy Quyền**

### **Tích Hợp Nhà Cung Cấp Danh Tính Bên Ngoài**

**Tiêu Chuẩn MCP Hiện Tại (2025-06-18)** cho phép máy chủ MCP ủy quyền xác thực cho các nhà cung cấp danh tính bên ngoài, mang lại sự cải thiện đáng kể về an ninh:

**Lợi Ích An Ninh:**
1. **Loại Bỏ Rủi Ro Xác Thực Tùy Chỉnh**: Giảm bề mặt dễ bị tấn công bằng cách tránh triển khai xác thực tùy chỉnh  
2. **An Ninh Cấp Doanh Nghiệp**: Tận dụng các nhà cung cấp danh tính đã được thiết lập như Microsoft Entra ID với các tính năng an ninh tiên tiến  
3. **Quản Lý Danh Tính Tập Trung**: Đơn giản hóa quản lý vòng đời người dùng, kiểm soát truy cập và kiểm toán tuân thủ  
4. **Xác Thực Đa Yếu Tố (MFA)**: Thừa hưởng khả năng MFA từ các nhà cung cấp danh tính doanh nghiệp  
5. **Chính Sách Truy Cập Có Điều Kiện**: Hưởng lợi từ kiểm soát truy cập dựa trên rủi ro và xác thực thích ứng  

**Yêu Cầu Triển Khai:**
- **Xác Minh Đối Tượng Token**: Xác minh tất cả các token được phát hành rõ ràng cho máy chủ MCP  
- **Xác Minh Nhà Phát Hành**: Đảm bảo nhà phát hành token khớp với nhà cung cấp danh tính mong đợi  
- **Xác Minh Chữ Ký**: Xác minh mật mã tính toàn vẹn của token  
- **Thực Thi Hết Hạn**: Thực thi nghiêm ngặt giới hạn thời gian sống của token  
- **Xác Minh Phạm Vi**: Đảm bảo token chứa các quyền phù hợp cho các hoạt động được yêu cầu  

### **An Ninh Logic Ủy Quyền**

**Kiểm Soát Quan Trọng:**
- **Kiểm Toán Ủy Quyền Toàn Diện**: Xem xét an ninh thường xuyên tại tất cả các điểm quyết định ủy quyền  
- **Mặc Định An Toàn**: Từ chối truy cập khi logic ủy quyền không thể đưa ra quyết định rõ ràng  
- **Ranh Giới Quyền Hạn**: Phân tách rõ ràng giữa các cấp độ quyền hạn và truy cập tài nguyên  
- **Ghi Nhật Ký Kiểm Toán**: Ghi lại đầy đủ tất cả các quyết định ủy quyền để giám sát an ninh  
- **Xem Xét Quyền Truy Cập Định Kỳ**: Xác minh định kỳ quyền hạn và phân quyền của người dùng  

## 2. **An Ninh Token & Kiểm Soát Chống Truyền Qua**

### **Ngăn Chặn Truyền Qua Token**

**Truyền qua token bị nghiêm cấm rõ ràng** trong MCP Authorization Specification do các rủi ro an ninh nghiêm trọng:

**Rủi Ro An Ninh Được Giải Quyết:**
- **Vượt Qua Kiểm Soát**: Bỏ qua các biện pháp kiểm soát an ninh quan trọng như giới hạn tốc độ, xác minh yêu cầu và giám sát lưu lượng  
- **Phá Vỡ Trách Nhiệm**: Làm cho việc nhận diện khách hàng trở nên không thể, làm hỏng nhật ký kiểm toán và điều tra sự cố  
- **Khai Thác Dựa Trên Proxy**: Cho phép kẻ xấu sử dụng máy chủ làm proxy để truy cập dữ liệu trái phép  
- **Vi Phạm Ranh Giới Tin Cậy**: Phá vỡ các giả định tin cậy của dịch vụ hạ nguồn về nguồn gốc token  
- **Di Chuyển Ngang**: Token bị xâm phạm trên nhiều dịch vụ cho phép mở rộng tấn công rộng hơn  

**Kiểm Soát Triển Khai:**
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

### **Mô Hình Quản Lý Token An Toàn**

**Thực Hành Tốt Nhất:**
- **Token Ngắn Hạn**: Giảm thiểu cửa sổ phơi nhiễm bằng cách xoay vòng token thường xuyên  
- **Phát Hành Đúng Lúc**: Chỉ phát hành token khi cần thiết cho các hoạt động cụ thể  
- **Lưu Trữ An Toàn**: Sử dụng các mô-đun an ninh phần cứng (HSM) hoặc kho khóa an toàn  
- **Ràng Buộc Token**: Ràng buộc token với các khách hàng, phiên làm việc hoặc hoạt động cụ thể nếu có thể  
- **Giám Sát & Cảnh Báo**: Phát hiện thời gian thực các hành vi lạm dụng token hoặc mẫu truy cập trái phép  

## 3. **Kiểm Soát An Ninh Phiên Làm Việc**

### **Ngăn Chặn Chiếm Đoạt Phiên Làm Việc**

**Các Phương Thức Tấn Công Được Giải Quyết:**
- **Tiêm Lệnh Chiếm Đoạt Phiên Làm Việc**: Các sự kiện độc hại được tiêm vào trạng thái phiên làm việc chia sẻ  
- **Mạo Danh Phiên Làm Việc**: Sử dụng trái phép ID phiên làm việc bị đánh cắp để vượt qua xác thực  
- **Tấn Công Dòng Dữ Liệu Có Thể Tiếp Tục**: Khai thác việc tiếp tục sự kiện do máy chủ gửi để tiêm nội dung độc hại  

**Kiểm Soát Phiên Làm Việc Bắt Buộc:**
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

**An Ninh Truyền Tải:**
- **Thực Thi HTTPS**: Tất cả giao tiếp phiên làm việc qua TLS 1.3  
- **Thuộc Tính Cookie An Toàn**: HttpOnly, Secure, SameSite=Strict  
- **Ghim Chứng Chỉ**: Đối với các kết nối quan trọng để ngăn chặn tấn công MITM  

### **Cân Nhắc Trạng Thái vs Không Trạng Thái**

**Đối Với Triển Khai Có Trạng Thái:**
- Trạng thái phiên làm việc chia sẻ yêu cầu bảo vệ bổ sung chống lại các cuộc tấn công tiêm lệnh  
- Quản lý phiên làm việc dựa trên hàng đợi cần xác minh tính toàn vẹn  
- Nhiều phiên bản máy chủ yêu cầu đồng bộ hóa trạng thái phiên làm việc an toàn  

**Đối Với Triển Khai Không Trạng Thái:**
- Quản lý phiên làm việc dựa trên JWT hoặc token tương tự  
- Xác minh mật mã tính toàn vẹn của trạng thái phiên làm việc  
- Giảm bề mặt tấn công nhưng yêu cầu xác minh token mạnh mẽ  

## 4. **Kiểm Soát An Ninh Đặc Thù AI**

### **Phòng Chống Tiêm Lệnh Prompt**

**Tích Hợp Microsoft Prompt Shields:**
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

**Kiểm Soát Triển Khai:**
- **Làm Sạch Dữ Liệu Đầu Vào**: Xác minh và lọc toàn diện tất cả các đầu vào của người dùng  
- **Định Nghĩa Ranh Giới Nội Dung**: Phân tách rõ ràng giữa hướng dẫn hệ thống và nội dung người dùng  
- **Thứ Bậc Hướng Dẫn**: Quy tắc ưu tiên phù hợp cho các hướng dẫn xung đột  
- **Giám Sát Đầu Ra**: Phát hiện các đầu ra có khả năng gây hại hoặc bị thao túng  

### **Ngăn Chặn Đầu Độc Công Cụ**

**Khung An Ninh Công Cụ:**
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

**Quản Lý Công Cụ Động:**
- **Luồng Công Việc Phê Duyệt**: Sự đồng ý rõ ràng của người dùng cho các sửa đổi công cụ  
- **Khả Năng Hoàn Tác**: Khả năng quay lại các phiên bản công cụ trước đó  
- **Kiểm Toán Thay Đổi**: Lịch sử đầy đủ của các sửa đổi định nghĩa công cụ  
- **Đánh Giá Rủi Ro**: Đánh giá tự động tư thế an ninh của công cụ  

## 5. **Ngăn Chặn Tấn Công Deputy Nhầm Lẫn**

### **An Ninh Proxy OAuth**

**Kiểm Soát Ngăn Chặn Tấn Công:**
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

**Yêu Cầu Triển Khai:**
- **Xác Minh Đồng Ý Người Dùng**: Không bao giờ bỏ qua màn hình đồng ý cho đăng ký khách hàng động  
- **Xác Minh URI Chuyển Hướng**: Xác minh nghiêm ngặt dựa trên danh sách trắng các điểm đến chuyển hướng  
- **Bảo Vệ Mã Ủy Quyền**: Mã ngắn hạn với thực thi sử dụng một lần  
- **Xác Minh Danh Tính Khách Hàng**: Xác minh mạnh mẽ thông tin xác thực và siêu dữ liệu của khách hàng  

## 6. **An Ninh Thực Thi Công Cụ**

### **Cách Ly & Sandboxing**

**Cách Ly Dựa Trên Container:**
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

**Cách Ly Quy Trình:**
- **Ngữ Cảnh Quy Trình Riêng Biệt**: Mỗi lần thực thi công cụ trong không gian quy trình cách ly  
- **Giao Tiếp Liên Quy Trình**: Cơ chế IPC an toàn với xác minh  
- **Giám Sát Quy Trình**: Phân tích hành vi thời gian chạy và phát hiện bất thường  
- **Thực Thi Tài Nguyên**: Giới hạn cứng về CPU, bộ nhớ và hoạt động I/O  

### **Triển Khai Quyền Hạn Tối Thiểu**

**Quản Lý Quyền Hạn:**
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

## 7. **Kiểm Soát An Ninh Chuỗi Cung Ứng**

### **Xác Minh Phụ Thuộc**

**An Ninh Thành Phần Toàn Diện:**
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

### **Giám Sát Liên Tục**

**Phát Hiện Mối Đe Dọa Chuỗi Cung Ứng:**
- **Giám Sát Sức Khỏe Phụ Thuộc**: Đánh giá liên tục tất cả các phụ thuộc để phát hiện vấn đề an ninh  
- **Tích Hợp Tình Báo Mối Đe Dọa**: Cập nhật thời gian thực về các mối đe dọa chuỗi cung ứng mới nổi  
- **Phân Tích Hành Vi**: Phát hiện hành vi bất thường trong các thành phần bên ngoài  
- **Phản Ứng Tự Động**: Ngăn chặn ngay lập tức các thành phần bị xâm phạm  

## 8. **Kiểm Soát Giám Sát & Phát Hiện**

### **Quản Lý Thông Tin & Sự Kiện An Ninh (SIEM)**

**Chiến Lược Ghi Nhật Ký Toàn Diện:**
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

### **Phát Hiện Mối Đe Dọa Thời Gian Thực**

**Phân Tích Hành Vi:**
- **Phân Tích Hành Vi Người Dùng (UBA)**: Phát hiện các mẫu truy cập bất thường của người dùng  
- **Phân Tích Hành Vi Thực Thể (EBA)**: Giám sát hành vi của máy chủ MCP và công cụ  
- **Phát Hiện Bất Thường Bằng Học Máy**: Xác định các mối đe dọa an ninh bằng AI  
- **Liên Kết Tình Báo Mối Đe Dọa**: So khớp các hoạt động quan sát được với các mẫu tấn công đã biết  

## 9. **Phản Ứng & Phục Hồi Sự Cố**

### **Khả Năng Phản Ứng Tự Động**

**Hành Động Phản Ứng Ngay Lập Tức:**
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

### **Khả Năng Pháp Y**

**Hỗ Trợ Điều Tra:**
- **Bảo Tồn Nhật Ký Kiểm Toán**: Ghi nhật ký không thể thay đổi với tính toàn vẹn mật mã  
- **Thu Thập Bằng Chứng**: Tự động thu thập các hiện vật an ninh liên quan  
- **Tái Tạo Dòng Thời Gian**: Trình tự chi tiết các sự kiện dẫn đến sự cố an ninh  
- **Đánh Giá Tác Động**: Đánh giá phạm vi xâm phạm và mức độ lộ dữ liệu  

## **Nguyên Tắc Kiến Trúc An Ninh Chính**

### **Phòng Thủ Nhiều Lớp**
- **Nhiều Lớp An Ninh**: Không có điểm thất bại duy nhất trong kiến trúc an ninh  
- **Kiểm Soát Dự Phòng**: Các biện pháp an ninh chồng chéo cho các chức năng quan trọng  
- **Cơ Chế An Toàn Khi Lỗi**: Mặc định an toàn khi hệ thống gặp lỗi hoặc bị tấn công  

### **Triển Khai Zero Trust**
- **Không Bao Giờ Tin Tưởng, Luôn Xác Minh**: Xác minh liên tục tất cả các thực thể và yêu cầu  
- **Nguyên Tắc Quyền Hạn Tối Thiểu**: Quyền truy cập tối thiểu cho tất cả các thành phần  
- **Phân Đoạn Vi Mô**: Kiểm soát mạng và truy cập chi tiết  

### **Tiến Hóa An Ninh Liên Tục**
- **Thích Ứng Với Cảnh Quan Mối Đe Dọa**: Cập nhật thường xuyên để giải quyết các mối đe dọa mới nổi  
- **Hiệu Quả Kiểm Soát An Ninh**: Đánh giá và cải thiện liên tục các biện pháp kiểm soát  
- **Tuân Thủ Tiêu Chuẩn**: Phù hợp với các tiêu chuẩn an ninh MCP đang phát triển  

---

## **Tài Nguyên Triển Khai**

### **Tài Liệu Chính Thức MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Thực Hành Tốt Nhất Về An Ninh MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Giải Pháp An Ninh Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Tiêu Chuẩn An Ninh**
- [Thực Hành Tốt Nhất Về An Ninh OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 cho Các Mô Hình Ngôn Ngữ Lớn](https://genai.owasp.org/)  
- [Khung An Ninh Mạng NIST](https://www.nist.gov/cyberframework)  

---

> **Quan Trọng**: Các biện pháp kiểm soát an ninh này phản ánh MCP specification hiện tại (2025-06-18). Luôn xác minh với [tài liệu chính thức](https://spec.modelcontextprotocol.io/) mới nhất vì các tiêu chuẩn tiếp tục phát triển nhanh chóng.  

**Tuyên bố miễn trừ trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ bản địa nên được coi là nguồn tham khảo chính thức. Đối với các thông tin quan trọng, chúng tôi khuyến nghị sử dụng dịch vụ dịch thuật chuyên nghiệp từ con người. Chúng tôi không chịu trách nhiệm cho bất kỳ sự hiểu lầm hoặc diễn giải sai nào phát sinh từ việc sử dụng bản dịch này.