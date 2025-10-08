<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "b2b9e15e78b9d9a2b3ff3e8fd7d1f434",
  "translation_date": "2025-08-18T17:17:13+00:00",
  "source_file": "02-Security/mcp-best-practices.md",
  "language_code": "vi"
}
-->
# MCP Các Thực Tiễn Tốt Nhất Về Bảo Mật 2025

Hướng dẫn toàn diện này trình bày các thực tiễn tốt nhất về bảo mật cần thiết để triển khai hệ thống Model Context Protocol (MCP) dựa trên **MCP Specification 2025-06-18** mới nhất và các tiêu chuẩn ngành hiện tại. Các thực tiễn này giải quyết cả các mối lo ngại bảo mật truyền thống và các mối đe dọa đặc thù liên quan đến AI trong triển khai MCP.

## Các Yêu Cầu Bảo Mật Quan Trọng

### Các Kiểm Soát Bảo Mật Bắt Buộc (Yêu Cầu MUST)

1. **Xác Thực Token**: Máy chủ MCP **KHÔNG ĐƯỢC** chấp nhận bất kỳ token nào không được phát hành rõ ràng cho chính máy chủ MCP đó.
2. **Xác Minh Quyền Hạn**: Máy chủ MCP triển khai quyền hạn **PHẢI** xác minh TẤT CẢ các yêu cầu đến và **KHÔNG ĐƯỢC** sử dụng phiên để xác thực.
3. **Sự Đồng Ý Của Người Dùng**: Máy chủ proxy MCP sử dụng ID khách hàng tĩnh **PHẢI** nhận được sự đồng ý rõ ràng của người dùng cho mỗi khách hàng được đăng ký động.
4. **ID Phiên Bảo Mật**: Máy chủ MCP **PHẢI** sử dụng ID phiên không xác định được, được tạo bằng các trình tạo số ngẫu nhiên an toàn về mặt mật mã.

## Các Thực Tiễn Bảo Mật Cốt Lõi

### 1. Xác Thực & Làm Sạch Dữ Liệu Đầu Vào
- **Xác Thực Dữ Liệu Đầu Vào Toàn Diện**: Xác thực và làm sạch tất cả dữ liệu đầu vào để ngăn chặn các cuộc tấn công chèn mã, vấn đề "deputy confused", và các lỗ hổng tiêm lệnh.
- **Thực Thi Schema Tham Số**: Triển khai xác thực schema JSON nghiêm ngặt cho tất cả các tham số công cụ và dữ liệu đầu vào API.
- **Lọc Nội Dung**: Sử dụng Microsoft Prompt Shields và Azure Content Safety để lọc nội dung độc hại trong các lời nhắc và phản hồi.
- **Làm Sạch Dữ Liệu Đầu Ra**: Xác thực và làm sạch tất cả đầu ra của mô hình trước khi hiển thị cho người dùng hoặc hệ thống hạ nguồn.

### 2. Xuất Sắc Trong Xác Thực & Quyền Hạn  
- **Nhà Cung Cấp Danh Tính Bên Ngoài**: Ủy quyền xác thực cho các nhà cung cấp danh tính uy tín (Microsoft Entra ID, các nhà cung cấp OAuth 2.1) thay vì triển khai xác thực tùy chỉnh.
- **Quyền Hạn Chi Tiết**: Triển khai quyền hạn chi tiết, cụ thể cho từng công cụ theo nguyên tắc quyền hạn tối thiểu.
- **Quản Lý Vòng Đời Token**: Sử dụng token truy cập ngắn hạn với xoay vòng an toàn và xác thực đối tượng phù hợp.
- **Xác Thực Đa Yếu Tố**: Yêu cầu MFA cho tất cả quyền truy cập quản trị và các hoạt động nhạy cảm.

### 3. Giao Thức Truyền Thông Bảo Mật
- **Bảo Mật Lớp Truyền Tải**: Sử dụng HTTPS/TLS 1.3 cho tất cả các giao tiếp MCP với xác thực chứng chỉ phù hợp.
- **Mã Hóa Từ Đầu Đến Cuối**: Triển khai các lớp mã hóa bổ sung cho dữ liệu cực kỳ nhạy cảm khi truyền và lưu trữ.
- **Quản Lý Chứng Chỉ**: Duy trì quản lý vòng đời chứng chỉ phù hợp với quy trình tự động gia hạn.
- **Thực Thi Phiên Bản Giao Thức**: Sử dụng phiên bản giao thức MCP hiện tại (2025-06-18) với đàm phán phiên bản phù hợp.

### 4. Giới Hạn Tốc Độ Nâng Cao & Bảo Vệ Tài Nguyên
- **Giới Hạn Tốc Độ Đa Lớp**: Triển khai giới hạn tốc độ ở cấp độ người dùng, phiên, công cụ, và tài nguyên để ngăn chặn lạm dụng.
- **Giới Hạn Tốc Độ Thích Ứng**: Sử dụng giới hạn tốc độ dựa trên học máy, thích ứng với các mẫu sử dụng và chỉ số đe dọa.
- **Quản Lý Hạn Ngạch Tài Nguyên**: Đặt giới hạn phù hợp cho tài nguyên tính toán, sử dụng bộ nhớ, và thời gian thực thi.
- **Bảo Vệ DDoS**: Triển khai hệ thống bảo vệ DDoS toàn diện và phân tích lưu lượng.

### 5. Ghi Nhật Ký & Giám Sát Toàn Diện
- **Ghi Nhật Ký Kiểm Toán Có Cấu Trúc**: Triển khai nhật ký chi tiết, có thể tìm kiếm cho tất cả các hoạt động MCP, thực thi công cụ, và sự kiện bảo mật.
- **Giám Sát Bảo Mật Thời Gian Thực**: Triển khai hệ thống SIEM với phát hiện bất thường dựa trên AI cho khối lượng công việc MCP.
- **Ghi Nhật Ký Tuân Thủ Quyền Riêng Tư**: Ghi nhật ký sự kiện bảo mật trong khi tôn trọng các yêu cầu và quy định về quyền riêng tư dữ liệu.
- **Tích Hợp Phản Ứng Sự Cố**: Kết nối hệ thống ghi nhật ký với quy trình phản ứng sự cố tự động.

### 6. Các Thực Tiễn Lưu Trữ Bảo Mật Nâng Cao
- **Mô-đun Bảo Mật Phần Cứng**: Sử dụng lưu trữ khóa hỗ trợ HSM (Azure Key Vault, AWS CloudHSM) cho các hoạt động mật mã quan trọng.
- **Quản Lý Khóa Mã Hóa**: Triển khai xoay vòng khóa, phân tách, và kiểm soát truy cập phù hợp cho các khóa mã hóa.
- **Quản Lý Bí Mật**: Lưu trữ tất cả các khóa API, token, và thông tin xác thực trong các hệ thống quản lý bí mật chuyên dụng.
- **Phân Loại Dữ Liệu**: Phân loại dữ liệu dựa trên mức độ nhạy cảm và áp dụng các biện pháp bảo vệ phù hợp.

### 7. Quản Lý Token Nâng Cao
- **Ngăn Chặn Truyền Token**: Cấm rõ ràng các mẫu truyền token vượt qua các kiểm soát bảo mật.
- **Xác Thực Đối Tượng**: Luôn xác minh các tuyên bố đối tượng của token khớp với danh tính máy chủ MCP dự định.
- **Quyền Hạn Dựa Trên Tuyên Bố**: Triển khai quyền hạn chi tiết dựa trên các tuyên bố của token và thuộc tính người dùng.
- **Liên Kết Token**: Liên kết token với các phiên, người dùng, hoặc thiết bị cụ thể khi phù hợp.

### 8. Quản Lý Phiên Bảo Mật
- **ID Phiên Mật Mã**: Tạo ID phiên bằng các trình tạo số ngẫu nhiên an toàn về mặt mật mã (không phải chuỗi có thể dự đoán).
- **Liên Kết Cụ Thể Người Dùng**: Liên kết ID phiên với thông tin cụ thể người dùng bằng các định dạng an toàn như `<user_id>:<session_id>`.
- **Kiểm Soát Vòng Đời Phiên**: Triển khai cơ chế hết hạn, xoay vòng, và vô hiệu hóa phiên phù hợp.
- **Tiêu Đề Bảo Mật Phiên**: Sử dụng các tiêu đề HTTP bảo mật phù hợp để bảo vệ phiên.

### 9. Kiểm Soát Bảo Mật Đặc Thù AI
- **Phòng Chống Tiêm Lệnh Prompt**: Triển khai Microsoft Prompt Shields với các kỹ thuật spotlighting, delimiters, và datamarking.
- **Ngăn Chặn Độc Hại Công Cụ**: Xác thực metadata công cụ, giám sát các thay đổi động, và xác minh tính toàn vẹn của công cụ.
- **Xác Thực Đầu Ra Mô Hình**: Quét đầu ra mô hình để phát hiện rò rỉ dữ liệu, nội dung độc hại, hoặc vi phạm chính sách bảo mật.
- **Bảo Vệ Cửa Sổ Ngữ Cảnh**: Triển khai các kiểm soát để ngăn chặn độc hại và tấn công thao túng cửa sổ ngữ cảnh.

### 10. Bảo Mật Thực Thi Công Cụ
- **Sandbox Thực Thi**: Chạy thực thi công cụ trong các môi trường container hóa, cách ly với giới hạn tài nguyên.
- **Phân Tách Quyền Hạn**: Thực thi công cụ với quyền hạn tối thiểu cần thiết và tài khoản dịch vụ riêng biệt.
- **Cách Ly Mạng**: Triển khai phân đoạn mạng cho các môi trường thực thi công cụ.
- **Giám Sát Thực Thi**: Giám sát thực thi công cụ để phát hiện hành vi bất thường, sử dụng tài nguyên, và vi phạm bảo mật.

### 11. Xác Thực Bảo Mật Liên Tục
- **Kiểm Tra Bảo Mật Tự Động**: Tích hợp kiểm tra bảo mật vào các pipeline CI/CD với các công cụ như GitHub Advanced Security.
- **Quản Lý Lỗ Hổng**: Thường xuyên quét tất cả các phụ thuộc, bao gồm mô hình AI và dịch vụ bên ngoài.
- **Kiểm Tra Xâm Nhập**: Thực hiện các đánh giá bảo mật thường xuyên, đặc biệt nhắm vào triển khai MCP.
- **Xem Xét Mã Bảo Mật**: Triển khai các xem xét bảo mật bắt buộc cho tất cả các thay đổi mã liên quan đến MCP.

### 12. Bảo Mật Chuỗi Cung Ứng Cho AI
- **Xác Minh Thành Phần**: Xác minh nguồn gốc, tính toàn vẹn, và bảo mật của tất cả các thành phần AI (mô hình, embeddings, API).
- **Quản Lý Phụ Thuộc**: Duy trì danh sách hiện tại của tất cả các phụ thuộc phần mềm và AI với theo dõi lỗ hổng.
- **Kho Lưu Trữ Đáng Tin Cậy**: Sử dụng các nguồn đã được xác minh, đáng tin cậy cho tất cả các mô hình AI, thư viện, và công cụ.
- **Giám Sát Chuỗi Cung Ứng**: Liên tục giám sát các sự cố trong các nhà cung cấp dịch vụ AI và kho lưu trữ mô hình.

## Các Mẫu Bảo Mật Nâng Cao

### Kiến Trúc Zero Trust Cho MCP
- **Không Bao Giờ Tin, Luôn Xác Minh**: Triển khai xác minh liên tục cho tất cả các thành phần MCP.
- **Phân Đoạn Vi Mô**: Cách ly các thành phần MCP với các kiểm soát mạng và danh tính chi tiết.
- **Truy Cập Có Điều Kiện**: Triển khai các kiểm soát truy cập dựa trên rủi ro, thích ứng với ngữ cảnh và hành vi.
- **Đánh Giá Rủi Ro Liên Tục**: Đánh giá động tư thế bảo mật dựa trên các chỉ số đe dọa hiện tại.

### Triển Khai AI Bảo Vệ Quyền Riêng Tư
- **Giảm Thiểu Dữ Liệu**: Chỉ tiết lộ dữ liệu cần thiết tối thiểu cho mỗi hoạt động MCP.
- **Quyền Riêng Tư Vi Sai**: Triển khai các kỹ thuật bảo vệ quyền riêng tư cho xử lý dữ liệu nhạy cảm.
- **Mã Hóa Đồng Hình**: Sử dụng các kỹ thuật mã hóa tiên tiến để tính toán an toàn trên dữ liệu được mã hóa.
- **Học Liên Kết**: Triển khai các phương pháp học phân tán bảo vệ tính cục bộ và quyền riêng tư của dữ liệu.

### Phản Ứng Sự Cố Cho Hệ Thống AI
- **Quy Trình Sự Cố Đặc Thù AI**: Phát triển quy trình phản ứng sự cố phù hợp với các mối đe dọa đặc thù AI và MCP.
- **Phản Ứng Tự Động**: Triển khai các biện pháp ngăn chặn và khắc phục tự động cho các sự cố bảo mật AI phổ biến.
- **Khả Năng Pháp Lý**: Duy trì khả năng pháp lý để xử lý các sự cố xâm phạm hệ thống AI và rò rỉ dữ liệu.
- **Quy Trình Khôi Phục**: Thiết lập quy trình khôi phục từ các cuộc tấn công độc hại mô hình, tiêm lệnh prompt, và sự cố dịch vụ.

## Tài Nguyên & Tiêu Chuẩn Triển Khai

### Tài Liệu Chính Thức MCP
- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) - Đặc tả giao thức MCP hiện tại
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) - Hướng dẫn bảo mật chính thức
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Mẫu xác thực và quyền hạn
- [MCP Transport Security](https://modelcontextprotocol.io/specification/2025-06-18/transports/) - Yêu cầu bảo mật lớp truyền tải

### Giải Pháp Bảo Mật Microsoft
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) - Bảo vệ tiêm lệnh prompt tiên tiến
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/) - Lọc nội dung AI toàn diện
- [Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-auth-code-flow) - Quản lý danh tính và truy cập doanh nghiệp
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts) - Quản lý bí mật và thông tin xác thực an toàn
- [GitHub Advanced Security](https://github.com/security/advanced-security) - Quét bảo mật chuỗi cung ứng và mã

### Tiêu Chuẩn & Khung Bảo Mật
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) - Hướng dẫn bảo mật OAuth hiện tại
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Các rủi ro bảo mật ứng dụng web
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559) - Các rủi ro bảo mật đặc thù AI
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Quản lý rủi ro AI toàn diện
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Hệ thống quản lý bảo mật thông tin

### Hướng Dẫn & Tutorial Triển Khai
- [Azure API Management as MCP Auth Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) - Mẫu xác thực doanh nghiệp
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/) - Tích hợp nhà cung cấp danh tính
- [Secure Token Storage Implementation](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2) - Thực tiễn quản lý token tốt nhất
- [End-to-End Encryption for AI](https://learn.microsoft.com/azure/architecture/example-scenario/confidential/end-to-end-encryption) - Mẫu mã hóa tiên tiến

### Tài Nguyên Bảo Mật Nâng Cao
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/sdl) - Thực tiễn phát triển an toàn
- [AI Red Team Guidance](https://learn.microsoft.com/security/ai-red-team/) - Kiểm tra bảo mật đặc thù AI
- [Threat Modeling for AI Systems](https://learn.microsoft.com/security/adoption/approach/threats-ai) - Phương pháp mô hình hóa mối đe dọa AI
- [Privacy Engineering for AI](https://www.microsoft.com/security/blog/2021/07/13/microsofts-pet-project-privacy-enhancing-technologies-in-action/) - Kỹ thuật bảo vệ quyền riêng tư AI

### Tuân Thủ & Quản Trị
- [GDPR Compliance for AI](https://learn.microsoft.com/compliance/regulatory/gdpr-data-protection-impact-assessments) - Tuân thủ quyền riêng tư trong hệ thống AI
- [AI Governance Framework](https://learn.microsoft.com/azure/architecture/guide/responsible-ai/responsible-ai-overview) - Triển khai AI có trách nhiệm
- [SOC 2 for AI Services](https://learn.microsoft.com/compliance/regulatory/offering-soc) - Kiểm soát bảo mật cho nhà cung cấp dịch vụ AI
- [HIPAA Compliance for AI](https://learn.microsoft.com/compliance/regulatory/offering-hipaa-hitech) - Yêu cầu tuân thủ AI trong lĩnh vực y tế

### DevSecOps & Tự Động Hóa
- [DevSecOps Pipeline for AI](https://learn.microsoft.com/azure/devops/migrate/security-validation-cicd-pipeline) - Pipeline phát triển AI an toàn
- [Automated Security Testing](https://learn.microsoft.com/security/engineering/devsecops) - Xác thực bảo mật liên tục
- [Infrastructure as Code Security](https://learn.microsoft.com/security/engineering/infrastructure-security) - Triển khai hạ tầng an toàn
- [Container Security for AI
- **Phát triển công cụ**: Phát triển và chia sẻ các công cụ và thư viện bảo mật cho hệ sinh thái MCP

---

*Tài liệu này phản ánh các thực hành bảo mật tốt nhất của MCP tính đến ngày 18 tháng 8 năm 2025, dựa trên MCP Specification 2025-06-18. Các thực hành bảo mật nên được xem xét và cập nhật thường xuyên khi giao thức và bối cảnh mối đe dọa thay đổi.*

**Tuyên bố miễn trừ trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ bản địa nên được coi là nguồn tham khảo chính thức. Đối với các thông tin quan trọng, chúng tôi khuyến nghị sử dụng dịch vụ dịch thuật chuyên nghiệp từ con người. Chúng tôi không chịu trách nhiệm cho bất kỳ sự hiểu lầm hoặc diễn giải sai nào phát sinh từ việc sử dụng bản dịch này.