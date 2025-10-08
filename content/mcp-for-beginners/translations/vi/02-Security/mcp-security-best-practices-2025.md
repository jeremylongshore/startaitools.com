<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T17:13:50+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "vi"
}
-->
# Thực Hành Tốt Nhất Về Bảo Mật MCP - Cập Nhật Tháng 8 Năm 2025

> **Quan trọng**: Tài liệu này phản ánh các yêu cầu bảo mật mới nhất từ [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) và [Thực Hành Tốt Nhất Về Bảo Mật MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). Luôn tham khảo đặc tả hiện tại để có hướng dẫn cập nhật nhất.

## Các Thực Hành Bảo Mật Cần Thiết Cho Triển Khai MCP

Giao thức Model Context Protocol (MCP) mang đến những thách thức bảo mật độc đáo vượt ra ngoài bảo mật phần mềm truyền thống. Các thực hành này giải quyết cả các yêu cầu bảo mật cơ bản và các mối đe dọa đặc thù của MCP, bao gồm tiêm lệnh (prompt injection), làm nhiễm độc công cụ, chiếm đoạt phiên, vấn đề "deputy nhầm lẫn" (confused deputy), và lỗ hổng truyền qua token.

### **Yêu Cầu Bảo Mật BẮT BUỘC**

**Các Yêu Cầu Quan Trọng Từ MCP Specification:**

> **MUST NOT**: Máy chủ MCP **KHÔNG ĐƯỢC** chấp nhận bất kỳ token nào không được phát hành rõ ràng cho máy chủ MCP  
> 
> **MUST**: Máy chủ MCP triển khai ủy quyền **PHẢI** xác minh TẤT CẢ các yêu cầu đến  
>  
> **MUST NOT**: Máy chủ MCP **KHÔNG ĐƯỢC** sử dụng phiên (session) để xác thực  
>
> **MUST**: Máy chủ proxy MCP sử dụng ID khách hàng tĩnh **PHẢI** nhận được sự đồng ý của người dùng cho mỗi khách hàng được đăng ký động  

---

## 1. **Bảo Mật Token & Xác Thực**

**Kiểm Soát Xác Thực & Ủy Quyền:**
   - **Đánh Giá Ủy Quyền Nghiêm Ngặt**: Thực hiện kiểm tra toàn diện logic ủy quyền của máy chủ MCP để đảm bảo chỉ người dùng và khách hàng được phép mới có thể truy cập tài nguyên  
   - **Tích Hợp Nhà Cung Cấp Danh Tính Bên Ngoài**: Sử dụng các nhà cung cấp danh tính uy tín như Microsoft Entra ID thay vì tự triển khai xác thực  
   - **Xác Thực Đối Tượng Token**: Luôn xác minh rằng token được phát hành rõ ràng cho máy chủ MCP của bạn - không bao giờ chấp nhận token từ nguồn khác  
   - **Vòng Đời Token Hợp Lý**: Triển khai chính sách xoay vòng token an toàn, hết hạn token, và ngăn chặn các cuộc tấn công phát lại token  

**Lưu Trữ Token An Toàn:**
   - Sử dụng Azure Key Vault hoặc các kho lưu trữ thông tin xác thực an toàn tương tự cho tất cả các bí mật  
   - Triển khai mã hóa cho token cả khi lưu trữ và khi truyền tải  
   - Xoay vòng thông tin xác thực thường xuyên và giám sát truy cập trái phép  

## 2. **Quản Lý Phiên & Bảo Mật Truyền Tải**

**Thực Hành Phiên An Toàn:**
   - **ID Phiên Mã Hóa An Toàn**: Sử dụng ID phiên an toàn, không thể đoán trước được tạo bằng các trình tạo số ngẫu nhiên an toàn  
   - **Ràng Buộc Cụ Thể Người Dùng**: Ràng buộc ID phiên với danh tính người dùng bằng các định dạng như `<user_id>:<session_id>` để ngăn chặn lạm dụng phiên giữa các người dùng  
   - **Quản Lý Vòng Đời Phiên**: Triển khai hết hạn, xoay vòng, và vô hiệu hóa phiên đúng cách để giảm thiểu cửa sổ lỗ hổng  
   - **Bắt Buộc Sử Dụng HTTPS/TLS**: Bắt buộc sử dụng HTTPS cho tất cả các giao tiếp để ngăn chặn việc đánh cắp ID phiên  

**Bảo Mật Lớp Truyền Tải:**
   - Cấu hình TLS 1.3 nếu có thể với quản lý chứng chỉ đúng cách  
   - Triển khai ghim chứng chỉ (certificate pinning) cho các kết nối quan trọng  
   - Xoay vòng chứng chỉ thường xuyên và xác minh tính hợp lệ  

## 3. **Bảo Vệ Trước Các Mối Đe Dọa Cụ Thể AI** 🤖

**Phòng Chống Tiêm Lệnh:**
   - **Microsoft Prompt Shields**: Triển khai AI Prompt Shields để phát hiện và lọc các lệnh độc hại tiên tiến  
   - **Làm Sạch Dữ Liệu Đầu Vào**: Xác minh và làm sạch tất cả dữ liệu đầu vào để ngăn chặn các cuộc tấn công tiêm lệnh và vấn đề "deputy nhầm lẫn"  
   - **Ranh Giới Nội Dung**: Sử dụng hệ thống phân cách và đánh dấu dữ liệu để phân biệt giữa lệnh đáng tin cậy và nội dung bên ngoài  

**Phòng Chống Làm Nhiễm Độc Công Cụ:**
   - **Xác Minh Metadata Công Cụ**: Triển khai kiểm tra tính toàn vẹn cho định nghĩa công cụ và giám sát các thay đổi bất thường  
   - **Giám Sát Công Cụ Động**: Giám sát hành vi thời gian chạy và thiết lập cảnh báo cho các mẫu thực thi bất thường  
   - **Quy Trình Phê Duyệt**: Yêu cầu sự phê duyệt rõ ràng của người dùng cho các thay đổi công cụ và khả năng  

## 4. **Kiểm Soát Truy Cập & Quyền Hạn**

**Nguyên Tắc Quyền Hạn Tối Thiểu:**
   - Chỉ cấp cho máy chủ MCP các quyền tối thiểu cần thiết để thực hiện chức năng dự định  
   - Triển khai kiểm soát truy cập dựa trên vai trò (RBAC) với quyền hạn chi tiết  
   - Đánh giá quyền hạn thường xuyên và giám sát liên tục để phát hiện leo thang quyền hạn  

**Kiểm Soát Quyền Hạn Thời Gian Chạy:**
   - Áp dụng giới hạn tài nguyên để ngăn chặn các cuộc tấn công làm cạn kiệt tài nguyên  
   - Sử dụng cô lập container cho môi trường thực thi công cụ  
   - Triển khai truy cập "chỉ khi cần thiết" cho các chức năng quản trị  

## 5. **An Toàn Nội Dung & Giám Sát**

**Triển Khai An Toàn Nội Dung:**
   - **Tích Hợp Azure Content Safety**: Sử dụng Azure Content Safety để phát hiện nội dung độc hại, các nỗ lực jailbreak, và vi phạm chính sách  
   - **Phân Tích Hành Vi**: Triển khai giám sát hành vi thời gian chạy để phát hiện các bất thường trong máy chủ MCP và thực thi công cụ  
   - **Ghi Nhật Ký Toàn Diện**: Ghi lại tất cả các nỗ lực xác thực, gọi công cụ, và sự kiện bảo mật với lưu trữ an toàn, chống giả mạo  

**Giám Sát Liên Tục:**
   - Cảnh báo thời gian thực cho các mẫu đáng ngờ và nỗ lực truy cập trái phép  
   - Tích hợp với hệ thống SIEM để quản lý sự kiện bảo mật tập trung  
   - Thực hiện kiểm tra bảo mật và thử nghiệm thâm nhập thường xuyên cho các triển khai MCP  

## 6. **Bảo Mật Chuỗi Cung Ứng**

**Xác Minh Thành Phần:**
   - **Quét Phụ Thuộc**: Sử dụng quét lỗ hổng tự động cho tất cả các phụ thuộc phần mềm và thành phần AI  
   - **Xác Minh Nguồn Gốc**: Xác minh nguồn gốc, giấy phép, và tính toàn vẹn của các mô hình, nguồn dữ liệu, và dịch vụ bên ngoài  
   - **Gói Được Ký**: Sử dụng các gói được ký bằng mật mã và xác minh chữ ký trước khi triển khai  

**Quy Trình Phát Triển An Toàn:**
   - **GitHub Advanced Security**: Triển khai quét bí mật, phân tích phụ thuộc, và phân tích tĩnh CodeQL  
   - **Bảo Mật CI/CD**: Tích hợp xác thực bảo mật trong suốt các quy trình triển khai tự động  
   - **Tính Toàn Vẹn Của Tạo Tác**: Triển khai xác minh mật mã cho các tạo tác và cấu hình được triển khai  

## 7. **Bảo Mật OAuth & Phòng Chống "Deputy Nhầm Lẫn"**

**Triển Khai OAuth 2.1:**
   - **Triển Khai PKCE**: Sử dụng Proof Key for Code Exchange (PKCE) cho tất cả các yêu cầu ủy quyền  
   - **Sự Đồng Ý Rõ Ràng**: Nhận được sự đồng ý của người dùng cho mỗi khách hàng được đăng ký động để ngăn chặn các cuộc tấn công "deputy nhầm lẫn"  
   - **Xác Minh URI Chuyển Hướng**: Triển khai xác minh nghiêm ngặt các URI chuyển hướng và định danh khách hàng  

**Bảo Mật Proxy:**
   - Ngăn chặn bỏ qua ủy quyền thông qua khai thác ID khách hàng tĩnh  
   - Triển khai quy trình đồng ý đúng cách cho truy cập API bên thứ ba  
   - Giám sát việc đánh cắp mã ủy quyền và truy cập API trái phép  

## 8. **Phản Ứng Sự Cố & Phục Hồi**

**Khả Năng Phản Ứng Nhanh:**
   - **Phản Ứng Tự Động**: Triển khai hệ thống tự động để xoay vòng thông tin xác thực và ngăn chặn mối đe dọa  
   - **Quy Trình Hoàn Tác**: Khả năng nhanh chóng quay lại cấu hình và thành phần đã biết là an toàn  
   - **Khả Năng Pháp Y**: Nhật ký kiểm tra chi tiết và ghi nhật ký để điều tra sự cố  

**Truyền Thông & Phối Hợp:**
   - Quy trình leo thang rõ ràng cho các sự cố bảo mật  
   - Tích hợp với các đội phản ứng sự cố của tổ chức  
   - Thực hiện các mô phỏng sự cố bảo mật và bài tập thực hành thường xuyên  

## 9. **Tuân Thủ & Quản Trị**

**Tuân Thủ Quy Định:**
   - Đảm bảo các triển khai MCP đáp ứng các yêu cầu ngành cụ thể (GDPR, HIPAA, SOC 2)  
   - Triển khai phân loại dữ liệu và kiểm soát quyền riêng tư cho xử lý dữ liệu AI  
   - Duy trì tài liệu toàn diện để kiểm tra tuân thủ  

**Quản Lý Thay Đổi:**
   - Quy trình xem xét bảo mật chính thức cho tất cả các sửa đổi hệ thống MCP  
   - Kiểm soát phiên bản và quy trình phê duyệt cho các thay đổi cấu hình  
   - Đánh giá tuân thủ thường xuyên và phân tích khoảng cách  

## 10. **Kiểm Soát Bảo Mật Nâng Cao**

**Kiến Trúc Zero Trust:**
   - **Không Bao Giờ Tin, Luôn Xác Minh**: Xác minh liên tục người dùng, thiết bị, và kết nối  
   - **Phân Đoạn Vi Mô**: Kiểm soát mạng chi tiết cô lập các thành phần MCP riêng lẻ  
   - **Truy Cập Có Điều Kiện**: Kiểm soát truy cập dựa trên rủi ro thích ứng với ngữ cảnh và hành vi hiện tại  

**Bảo Vệ Ứng Dụng Thời Gian Chạy:**
   - **Bảo Vệ Ứng Dụng Tự Thân (RASP)**: Triển khai kỹ thuật RASP để phát hiện mối đe dọa thời gian thực  
   - **Giám Sát Hiệu Suất Ứng Dụng**: Giám sát các bất thường về hiệu suất có thể chỉ ra các cuộc tấn công  
   - **Chính Sách Bảo Mật Động**: Triển khai các chính sách bảo mật thích ứng dựa trên bối cảnh mối đe dọa hiện tại  

## 11. **Tích Hợp Hệ Sinh Thái Bảo Mật Microsoft**

**Bảo Mật Toàn Diện Microsoft:**
   - **Microsoft Defender for Cloud**: Quản lý tư thế bảo mật đám mây cho khối lượng công việc MCP  
   - **Azure Sentinel**: Khả năng SIEM và SOAR gốc đám mây để phát hiện mối đe dọa nâng cao  
   - **Microsoft Purview**: Quản trị dữ liệu và tuân thủ cho quy trình làm việc AI và nguồn dữ liệu  

**Quản Lý Danh Tính & Truy Cập:**
   - **Microsoft Entra ID**: Quản lý danh tính doanh nghiệp với chính sách truy cập có điều kiện  
   - **Quản Lý Danh Tính Đặc Quyền (PIM)**: Truy cập "chỉ khi cần thiết" và quy trình phê duyệt cho các chức năng quản trị  
   - **Bảo Vệ Danh Tính**: Truy cập có điều kiện dựa trên rủi ro và phản ứng mối đe dọa tự động  

## 12. **Tiến Hóa Bảo Mật Liên Tục**

**Luôn Cập Nhật:**
   - **Giám Sát Đặc Tả**: Xem xét thường xuyên các cập nhật đặc tả MCP và thay đổi hướng dẫn bảo mật  
   - **Tình Báo Mối Đe Dọa**: Tích hợp các nguồn tình báo mối đe dọa cụ thể AI và chỉ số xâm phạm  
   - **Tham Gia Cộng Đồng Bảo Mật**: Tham gia tích cực vào cộng đồng bảo mật MCP và các chương trình tiết lộ lỗ hổng  

**Bảo Mật Thích Ứng:**
   - **Bảo Mật Học Máy**: Sử dụng phát hiện bất thường dựa trên học máy để nhận diện các mẫu tấn công mới  
   - **Phân Tích Bảo Mật Dự Đoán**: Triển khai các mô hình dự đoán để nhận diện mối đe dọa chủ động  
   - **Tự Động Hóa Bảo Mật**: Cập nhật chính sách bảo mật tự động dựa trên tình báo mối đe dọa và thay đổi đặc tả  

---

## **Tài Nguyên Bảo Mật Quan Trọng**

### **Tài Liệu Chính Thức MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Giải Pháp Bảo Mật Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Security](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **Tiêu Chuẩn Bảo Mật**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **Hướng Dẫn Triển Khai**
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **Thông Báo Bảo Mật**: Các thực hành bảo mật MCP thay đổi nhanh chóng. Luôn xác minh với [đặc tả MCP hiện tại](https://spec.modelcontextprotocol.io/) và [tài liệu bảo mật chính thức](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) trước khi triển khai.

**Tuyên bố miễn trừ trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ bản địa nên được coi là nguồn tham khảo chính thức. Đối với các thông tin quan trọng, chúng tôi khuyến nghị sử dụng dịch vụ dịch thuật chuyên nghiệp từ con người. Chúng tôi không chịu trách nhiệm cho bất kỳ sự hiểu lầm hoặc diễn giải sai nào phát sinh từ việc sử dụng bản dịch này.