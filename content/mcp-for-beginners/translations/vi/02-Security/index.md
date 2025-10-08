<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T17:15:50+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "vi"
}
-->
# MCP Bảo Mật: Bảo Vệ Toàn Diện cho Hệ Thống AI

[![Thực hành tốt nhất về MCP Bảo Mật](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.vi.png)](https://youtu.be/88No8pw706o)

_(Nhấp vào hình ảnh trên để xem video của bài học này)_

Bảo mật là yếu tố cốt lõi trong thiết kế hệ thống AI, đó là lý do tại sao chúng tôi ưu tiên nó trong phần thứ hai. Điều này phù hợp với nguyên tắc **Secure by Design** của Microsoft từ [Sáng kiến Tương lai An toàn](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Giao thức Model Context Protocol (MCP) mang lại những khả năng mạnh mẽ mới cho các ứng dụng dựa trên AI, đồng thời giới thiệu các thách thức bảo mật độc đáo vượt xa các rủi ro phần mềm truyền thống. Hệ thống MCP đối mặt với cả các mối lo ngại bảo mật đã được thiết lập (lập trình an toàn, quyền tối thiểu, bảo mật chuỗi cung ứng) và các mối đe dọa đặc thù AI mới bao gồm tiêm lệnh (prompt injection), đầu độc công cụ (tool poisoning), chiếm đoạt phiên (session hijacking), tấn công confused deputy, lỗ hổng truyền token, và sửa đổi khả năng động.

Bài học này khám phá các rủi ro bảo mật quan trọng nhất trong triển khai MCP—bao gồm xác thực, ủy quyền, quyền hạn quá mức, tiêm lệnh gián tiếp, bảo mật phiên, vấn đề confused deputy, quản lý token, và lỗ hổng chuỗi cung ứng. Bạn sẽ học được các biện pháp kiểm soát và thực hành tốt nhất để giảm thiểu các rủi ro này, đồng thời tận dụng các giải pháp của Microsoft như Prompt Shields, Azure Content Safety, và GitHub Advanced Security để củng cố triển khai MCP của bạn.

## Mục tiêu học tập

Sau khi hoàn thành bài học này, bạn sẽ có thể:

- **Nhận diện các mối đe dọa đặc thù MCP**: Nhận biết các rủi ro bảo mật độc đáo trong hệ thống MCP bao gồm tiêm lệnh, đầu độc công cụ, quyền hạn quá mức, chiếm đoạt phiên, vấn đề confused deputy, lỗ hổng truyền token, và rủi ro chuỗi cung ứng
- **Áp dụng các biện pháp kiểm soát bảo mật**: Triển khai các biện pháp giảm thiểu hiệu quả bao gồm xác thực mạnh mẽ, truy cập quyền tối thiểu, quản lý token an toàn, kiểm soát bảo mật phiên, và xác minh chuỗi cung ứng
- **Tận dụng các giải pháp bảo mật của Microsoft**: Hiểu và triển khai Microsoft Prompt Shields, Azure Content Safety, và GitHub Advanced Security để bảo vệ khối lượng công việc MCP
- **Xác thực bảo mật công cụ**: Nhận thức tầm quan trọng của việc xác thực metadata công cụ, giám sát các thay đổi động, và bảo vệ chống lại các cuộc tấn công tiêm lệnh gián tiếp
- **Tích hợp thực hành tốt nhất**: Kết hợp các nguyên tắc bảo mật đã được thiết lập (lập trình an toàn, làm cứng máy chủ, zero trust) với các biện pháp kiểm soát đặc thù MCP để bảo vệ toàn diện

# Kiến trúc & Biện pháp kiểm soát MCP Bảo Mật

Các triển khai MCP hiện đại yêu cầu các phương pháp bảo mật nhiều lớp để giải quyết cả các mối đe dọa bảo mật phần mềm truyền thống và đặc thù AI. Đặc tả MCP đang phát triển nhanh chóng tiếp tục hoàn thiện các biện pháp kiểm soát bảo mật, cho phép tích hợp tốt hơn với các kiến trúc bảo mật doanh nghiệp và thực hành tốt nhất đã được thiết lập.

Nghiên cứu từ [Báo cáo Phòng thủ Kỹ thuật số của Microsoft](https://aka.ms/mddr) cho thấy rằng **98% các vi phạm được báo cáo có thể được ngăn chặn bằng vệ sinh bảo mật mạnh mẽ**. Chiến lược bảo vệ hiệu quả nhất kết hợp các thực hành bảo mật cơ bản với các biện pháp kiểm soát đặc thù MCP—các biện pháp bảo mật cơ bản đã được chứng minh vẫn là tác động lớn nhất trong việc giảm thiểu rủi ro bảo mật tổng thể.

## Bối cảnh bảo mật hiện tại

> **Lưu ý:** Thông tin này phản ánh các tiêu chuẩn bảo mật MCP tính đến **18 tháng 8, 2025**. Giao thức MCP tiếp tục phát triển nhanh chóng, và các triển khai trong tương lai có thể giới thiệu các mẫu xác thực mới và các biện pháp kiểm soát nâng cao. Luôn tham khảo [Đặc tả MCP hiện tại](https://spec.modelcontextprotocol.io/), [Kho GitHub MCP](https://github.com/modelcontextprotocol), và [tài liệu thực hành tốt nhất về bảo mật](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) để có hướng dẫn mới nhất.

### Sự phát triển của xác thực MCP

Đặc tả MCP đã phát triển đáng kể trong cách tiếp cận xác thực và ủy quyền:

- **Cách tiếp cận ban đầu**: Các đặc tả ban đầu yêu cầu nhà phát triển triển khai các máy chủ xác thực tùy chỉnh, với các máy chủ MCP hoạt động như các Máy chủ Ủy quyền OAuth 2.0 quản lý xác thực người dùng trực tiếp
- **Tiêu chuẩn hiện tại (2025-06-18)**: Đặc tả cập nhật cho phép các máy chủ MCP ủy quyền xác thực cho các nhà cung cấp danh tính bên ngoài (như Microsoft Entra ID), cải thiện tư thế bảo mật và giảm độ phức tạp triển khai
- **Bảo mật tầng vận chuyển**: Hỗ trợ nâng cao cho các cơ chế vận chuyển an toàn với các mẫu xác thực phù hợp cho cả kết nối cục bộ (STDIO) và từ xa (Streamable HTTP)

## Bảo mật Xác thực & Ủy quyền

### Thách thức bảo mật hiện tại

Các triển khai MCP hiện đại đối mặt với một số thách thức về xác thực và ủy quyền:

### Rủi ro & Vectơ đe dọa

- **Logic ủy quyền cấu hình sai**: Triển khai ủy quyền sai trong các máy chủ MCP có thể làm lộ dữ liệu nhạy cảm và áp dụng sai các kiểm soát truy cập
- **Thỏa hiệp token OAuth**: Việc đánh cắp token máy chủ MCP cục bộ cho phép kẻ tấn công giả mạo máy chủ và truy cập các dịch vụ hạ nguồn
- **Lỗ hổng truyền token**: Xử lý token không đúng cách tạo ra các lỗ hổng bỏ qua kiểm soát bảo mật và khoảng trống trách nhiệm
- **Quyền hạn quá mức**: Các máy chủ MCP có quyền hạn quá mức vi phạm nguyên tắc quyền tối thiểu và mở rộng bề mặt tấn công

#### Truyền token: Một mẫu chống quan trọng

**Truyền token bị nghiêm cấm rõ ràng** trong đặc tả ủy quyền MCP hiện tại do các tác động bảo mật nghiêm trọng:

##### Vượt qua kiểm soát bảo mật
- Các máy chủ MCP và API hạ nguồn triển khai các kiểm soát bảo mật quan trọng (giới hạn tốc độ, xác thực yêu cầu, giám sát lưu lượng) phụ thuộc vào việc xác thực token đúng cách
- Việc sử dụng token trực tiếp từ client đến API bỏ qua các biện pháp bảo vệ thiết yếu này, làm suy yếu kiến trúc bảo mật

##### Thách thức trách nhiệm & kiểm toán  
- Các máy chủ MCP không thể phân biệt giữa các client sử dụng token được phát hành từ upstream, phá vỡ các dấu vết kiểm toán
- Nhật ký máy chủ tài nguyên hạ nguồn hiển thị nguồn gốc yêu cầu sai lệch thay vì các trung gian máy chủ MCP thực tế
- Điều tra sự cố và kiểm toán tuân thủ trở nên khó khăn đáng kể

##### Rủi ro rò rỉ dữ liệu
- Các tuyên bố token không được xác thực cho phép các tác nhân độc hại với token bị đánh cắp sử dụng các máy chủ MCP làm proxy để rò rỉ dữ liệu
- Vi phạm ranh giới tin cậy cho phép các mẫu truy cập trái phép bỏ qua các kiểm soát bảo mật dự định

##### Vectơ tấn công đa dịch vụ
- Các token bị thỏa hiệp được chấp nhận bởi nhiều dịch vụ cho phép di chuyển ngang qua các hệ thống kết nối
- Các giả định tin cậy giữa các dịch vụ có thể bị vi phạm khi nguồn gốc token không thể được xác minh

### Biện pháp kiểm soát & Giảm thiểu

**Yêu cầu bảo mật quan trọng:**

> **BẮT BUỘC**: Các máy chủ MCP **KHÔNG ĐƯỢC** chấp nhận bất kỳ token nào không được phát hành rõ ràng cho máy chủ MCP

#### Biện pháp kiểm soát Xác thực & Ủy quyền

- **Đánh giá ủy quyền nghiêm ngặt**: Thực hiện các cuộc kiểm toán toàn diện logic ủy quyền của máy chủ MCP để đảm bảo chỉ người dùng và client dự định mới có thể truy cập tài nguyên nhạy cảm
  - **Hướng dẫn triển khai**: [Azure API Management làm Cổng xác thực cho Máy chủ MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Tích hợp danh tính**: [Sử dụng Microsoft Entra ID cho Xác thực Máy chủ MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Quản lý token an toàn**: Triển khai [thực hành tốt nhất về xác thực và vòng đời token của Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Xác thực các tuyên bố đối tượng token khớp với danh tính máy chủ MCP
  - Triển khai chính sách xoay vòng và hết hạn token đúng cách
  - Ngăn chặn các cuộc tấn công phát lại token và sử dụng trái phép

- **Lưu trữ token được bảo vệ**: Lưu trữ token an toàn với mã hóa cả khi lưu trữ và khi truyền
  - **Thực hành tốt nhất**: [Hướng dẫn Lưu trữ và Mã hóa Token An toàn](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Triển khai kiểm soát truy cập

- **Nguyên tắc quyền tối thiểu**: Chỉ cấp cho các máy chủ MCP các quyền tối thiểu cần thiết cho chức năng dự định
  - Đánh giá và cập nhật quyền thường xuyên để ngăn chặn sự gia tăng quyền
  - **Tài liệu Microsoft**: [Truy cập An toàn với Quyền Tối thiểu](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Kiểm soát truy cập dựa trên vai trò (RBAC)**: Triển khai các phân công vai trò chi tiết
  - Phạm vi vai trò chặt chẽ với các tài nguyên và hành động cụ thể
  - Tránh các quyền rộng hoặc không cần thiết mở rộng bề mặt tấn công

- **Giám sát quyền liên tục**: Thực hiện kiểm toán và giám sát truy cập liên tục
  - Giám sát các mẫu sử dụng quyền để phát hiện bất thường
  - Khắc phục ngay lập tức các quyền quá mức hoặc không sử dụng

## Các mối đe dọa bảo mật đặc thù AI

### Tấn công Tiêm Lệnh & Thao Túng Công Cụ

Các triển khai MCP hiện đại đối mặt với các vectơ tấn công đặc thù AI tinh vi mà các biện pháp bảo mật truyền thống không thể giải quyết hoàn toàn:

#### **Tiêm Lệnh Gián Tiếp (Tiêm Lệnh Xuyên Miền)**

**Tiêm lệnh gián tiếp** là một trong những lỗ hổng nghiêm trọng nhất trong các hệ thống AI hỗ trợ MCP. Kẻ tấn công nhúng các hướng dẫn độc hại vào nội dung bên ngoài—tài liệu, trang web, email, hoặc nguồn dữ liệu—mà hệ thống AI sau đó xử lý như các lệnh hợp lệ.

**Kịch bản tấn công:**
- **Tiêm lệnh dựa trên tài liệu**: Hướng dẫn độc hại ẩn trong các tài liệu được xử lý, kích hoạt các hành động AI không mong muốn
- **Khai thác nội dung web**: Các trang web bị xâm phạm chứa các lệnh nhúng thao túng hành vi AI khi được quét
- **Tấn công dựa trên email**: Các lệnh độc hại trong email khiến trợ lý AI rò rỉ thông tin hoặc thực hiện các hành động trái phép
- **Ô nhiễm nguồn dữ liệu**: Các cơ sở dữ liệu hoặc API bị xâm phạm cung cấp nội dung bị nhiễm độc cho hệ thống AI

**Tác động thực tế**: Các cuộc tấn công này có thể dẫn đến rò rỉ dữ liệu, vi phạm quyền riêng tư, tạo nội dung có hại, và thao túng tương tác người dùng. Để phân tích chi tiết, xem [Tiêm Lệnh trong MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Sơ đồ Tấn công Tiêm Lệnh](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.vi.png)

#### **Tấn công Đầu Độc Công Cụ**

**Đầu độc công cụ** nhắm vào metadata định nghĩa các công cụ MCP, khai thác cách LLM diễn giải mô tả công cụ và tham số để đưa ra quyết định thực thi.

**Cơ chế tấn công:**
- **Thao túng metadata**: Kẻ tấn công nhúng các hướng dẫn độc hại vào mô tả công cụ, định nghĩa tham số, hoặc ví dụ sử dụng
- **Hướng dẫn vô hình**: Các lệnh ẩn trong metadata công cụ được AI xử lý nhưng vô hình với người dùng
- **Sửa đổi công cụ động ("Rug Pulls")**: Các công cụ được người dùng phê duyệt sau đó bị sửa đổi để thực hiện các hành động độc hại mà không có sự nhận thức của người dùng
- **Tiêm tham số**: Nội dung độc hại được nhúng trong các schema tham số công cụ ảnh hưởng đến hành vi của mô hình

**Rủi ro máy chủ được lưu trữ**: Các máy chủ MCP từ xa có rủi ro cao hơn vì các định nghĩa công cụ có thể được cập nhật sau khi được người dùng phê duyệt, tạo ra các kịch bản mà các công cụ trước đây an toàn trở nên độc hại. Để phân tích toàn diện, xem [Tấn công Đầu Độc Công Cụ (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Sơ đồ Tấn công Tiêm Công Cụ](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.vi.png)

#### **Các vectơ tấn công AI bổ sung**

- **Tiêm Lệnh Xuyên Miền (XPIA)**: Các cuộc tấn công tinh vi tận dụng nội dung từ nhiều miền để vượt qua các kiểm soát bảo mật
- **Sửa đổi khả năng động**: Thay đổi khả năng công cụ theo thời gian thực thoát khỏi các đánh giá bảo mật ban đầu
- **Ô nhiễm cửa sổ ngữ cảnh**: Các cuộc tấn công thao túng các cửa sổ ngữ cảnh lớn để ẩn các hướng dẫn độc hại
- **Tấn công nhầm lẫn mô hình**: Khai thác các hạn chế của mô hình để tạo ra các hành vi không thể đoán trước hoặc không an toàn

### Tác động rủi ro bảo mật AI

**Hậu quả có tác động cao:**
- **Rò rỉ dữ liệu**: Truy cập trái phép và đánh cắp dữ liệu nhạy cảm của doanh nghiệp hoặc cá nhân
- **Vi phạm quyền riêng tư**: Lộ thông tin nhận dạng cá nhân (PII) và dữ liệu kinh doanh bí mật  
- **Thao túng hệ thống**: Các sửa đổi không mong muốn đối với các hệ thống và quy trình quan trọng
- **Đánh cắp thông tin xác thực**: Thỏa hiệp token xác thực và thông tin xác thực dịch vụ
- **Di chuyển ngang**: Sử dụng các hệ thống AI bị xâm phạm làm điểm tựa cho các cuộc tấn công mạng rộng hơn

### Giải pháp bảo mật AI của Microsoft

#### **AI Prompt Shields: Bảo vệ nâng cao chống lại các cuộc tấn công tiêm lệnh**

Microsoft **AI Prompt Shields** cung cấp sự bảo vệ toàn diện chống lại cả các cuộc tấn công tiêm lệnh trực tiếp và gián tiếp thông qua nhiều lớp bảo mật:

##### **Cơ chế bảo vệ cốt lõi:**

1. **Phát hiện & Lọc nâng cao**
   - Các thuật toán học máy và kỹ thuật NLP phát hiện các hướng dẫn độc hại trong nội dung bên ngoài
   - Phân tích thời gian thực các tài liệu, trang web, email, và nguồn dữ liệu để tìm các mối đe dọa nhúng
   - Hiểu ngữ cảnh giữa các mẫu lệnh hợp lệ và độc hại

2. **Kỹ thuật Spotlighting**  
   - Phân biệt giữa các hướng dẫn hệ thống đáng tin cậy và các đầu vào bên ngoài có thể bị xâm phạm
   - Các phương pháp chuyển đổi văn bản tăng cường sự liên quan của mô hình trong khi cô lập nội dung độc hại
   - Giúp hệ thống AI duy trì thứ bậc hướng dẫn đúng và bỏ qua các lệnh được tiêm

3. **Hệ thống Đánh dấu & Phân định**
   - Định nghĩa ranh giới rõ ràng giữa các thông điệp hệ thống đáng tin cậy và văn bản đầu vào bên ngoài
   - Các dấu đặc biệt làm nổi bật ranh giới giữa các nguồn dữ liệu đáng tin cậy và không đáng tin cậy
   - Sự tách biệt rõ ràng ngăn chặn sự nhầm lẫn hướng dẫn và thực thi lệnh trái phép

4. **Tình báo mối đ
- **Tạo phiên làm việc an toàn**: Sử dụng ID phiên làm việc được tạo ngẫu nhiên bằng các trình tạo số ngẫu nhiên an toàn, không xác định trước.
- **Liên kết theo người dùng**: Liên kết ID phiên làm việc với thông tin cụ thể của người dùng bằng các định dạng như `<user_id>:<session_id>` để ngăn chặn việc lạm dụng phiên giữa các người dùng.
- **Quản lý vòng đời phiên làm việc**: Thực hiện việc hết hạn, xoay vòng và vô hiệu hóa đúng cách để giảm thiểu các lỗ hổng.
- **Bảo mật truyền tải**: Bắt buộc sử dụng HTTPS cho tất cả các giao tiếp để ngăn chặn việc đánh cắp ID phiên làm việc.

### Vấn đề "Confused Deputy"

Vấn đề **confused deputy** xảy ra khi các máy chủ MCP hoạt động như các proxy xác thực giữa khách hàng và dịch vụ bên thứ ba, tạo cơ hội cho việc bỏ qua ủy quyền thông qua việc khai thác ID khách hàng tĩnh.

#### **Cơ chế tấn công & Rủi ro**

- **Bỏ qua sự đồng ý dựa trên cookie**: Xác thực người dùng trước đó tạo ra các cookie đồng ý mà kẻ tấn công khai thác thông qua các yêu cầu ủy quyền độc hại với URI chuyển hướng được tạo ra.
- **Đánh cắp mã ủy quyền**: Cookie đồng ý hiện có có thể khiến máy chủ ủy quyền bỏ qua màn hình đồng ý, chuyển hướng mã đến các điểm cuối do kẻ tấn công kiểm soát.
- **Truy cập API trái phép**: Mã ủy quyền bị đánh cắp cho phép trao đổi token và giả mạo người dùng mà không cần sự chấp thuận rõ ràng.

#### **Chiến lược giảm thiểu**

**Kiểm soát bắt buộc:**
- **Yêu cầu đồng ý rõ ràng**: Các máy chủ proxy MCP sử dụng ID khách hàng tĩnh **PHẢI** nhận được sự đồng ý của người dùng cho mỗi khách hàng được đăng ký động.
- **Triển khai bảo mật OAuth 2.1**: Tuân theo các thực tiễn bảo mật OAuth hiện tại bao gồm PKCE (Proof Key for Code Exchange) cho tất cả các yêu cầu ủy quyền.
- **Xác thực khách hàng nghiêm ngặt**: Thực hiện xác thực nghiêm ngặt các URI chuyển hướng và định danh khách hàng để ngăn chặn khai thác.

### Lỗ hổng "Token Passthrough"

**Token passthrough** là một mô hình chống rõ ràng, trong đó các máy chủ MCP chấp nhận token của khách hàng mà không xác thực đúng cách và chuyển tiếp chúng đến các API hạ nguồn, vi phạm các thông số ủy quyền của MCP.

#### **Hệ quả bảo mật**

- **Bỏ qua kiểm soát**: Việc sử dụng token trực tiếp từ khách hàng đến API bỏ qua các kiểm soát quan trọng như giới hạn tốc độ, xác thực và giám sát.
- **Làm hỏng dấu vết kiểm toán**: Token được phát hành từ phía trên làm cho việc xác định khách hàng trở nên không thể, phá vỡ khả năng điều tra sự cố.
- **Khai thác dữ liệu qua proxy**: Token không được xác thực cho phép kẻ tấn công sử dụng máy chủ làm proxy để truy cập dữ liệu trái phép.
- **Vi phạm ranh giới tin cậy**: Các giả định tin cậy của dịch vụ hạ nguồn có thể bị vi phạm khi nguồn gốc của token không thể được xác minh.
- **Mở rộng tấn công đa dịch vụ**: Token bị xâm phạm được chấp nhận trên nhiều dịch vụ cho phép di chuyển ngang.

#### **Kiểm soát bảo mật bắt buộc**

**Yêu cầu không thể thương lượng:**
- **Xác thực token**: Các máy chủ MCP **KHÔNG ĐƯỢC** chấp nhận token không được phát hành rõ ràng cho máy chủ MCP.
- **Xác minh đối tượng**: Luôn xác thực các tuyên bố đối tượng của token khớp với danh tính của máy chủ MCP.
- **Vòng đời token đúng cách**: Thực hiện token truy cập ngắn hạn với các thực tiễn xoay vòng an toàn.

## Bảo mật chuỗi cung ứng cho hệ thống AI

Bảo mật chuỗi cung ứng đã vượt ra ngoài các phụ thuộc phần mềm truyền thống để bao gồm toàn bộ hệ sinh thái AI. Các triển khai MCP hiện đại phải xác minh và giám sát nghiêm ngặt tất cả các thành phần liên quan đến AI, vì mỗi thành phần đều có thể tạo ra các lỗ hổng tiềm năng làm ảnh hưởng đến tính toàn vẹn của hệ thống.

### Các thành phần chuỗi cung ứng AI mở rộng

**Phụ thuộc phần mềm truyền thống:**
- Thư viện và framework mã nguồn mở
- Hình ảnh container và hệ thống cơ sở
- Công cụ phát triển và quy trình xây dựng
- Các thành phần và dịch vụ hạ tầng

**Các yếu tố chuỗi cung ứng cụ thể của AI:**
- **Mô hình nền tảng**: Các mô hình được huấn luyện trước từ nhiều nhà cung cấp yêu cầu xác minh nguồn gốc.
- **Dịch vụ nhúng**: Dịch vụ vector hóa và tìm kiếm ngữ nghĩa bên ngoài.
- **Nhà cung cấp ngữ cảnh**: Nguồn dữ liệu, cơ sở tri thức và kho tài liệu.
- **API bên thứ ba**: Dịch vụ AI bên ngoài, quy trình ML và điểm cuối xử lý dữ liệu.
- **Tạo tác mô hình**: Trọng số, cấu hình và các biến thể mô hình được tinh chỉnh.
- **Nguồn dữ liệu huấn luyện**: Bộ dữ liệu được sử dụng để huấn luyện và tinh chỉnh mô hình.

### Chiến lược bảo mật chuỗi cung ứng toàn diện

#### **Xác minh & Tin cậy thành phần**
- **Xác minh nguồn gốc**: Xác minh nguồn gốc, giấy phép và tính toàn vẹn của tất cả các thành phần AI trước khi tích hợp.
- **Đánh giá bảo mật**: Thực hiện quét lỗ hổng và đánh giá bảo mật cho các mô hình, nguồn dữ liệu và dịch vụ AI.
- **Phân tích danh tiếng**: Đánh giá hồ sơ bảo mật và thực tiễn của các nhà cung cấp dịch vụ AI.
- **Xác minh tuân thủ**: Đảm bảo tất cả các thành phần đáp ứng yêu cầu bảo mật và quy định của tổ chức.

#### **Quy trình triển khai an toàn**
- **Bảo mật CI/CD tự động**: Tích hợp quét bảo mật trong toàn bộ quy trình triển khai tự động.
- **Tính toàn vẹn của tạo tác**: Thực hiện xác minh mã hóa cho tất cả các tạo tác được triển khai (mã, mô hình, cấu hình).
- **Triển khai theo giai đoạn**: Sử dụng chiến lược triển khai tiến bộ với xác thực bảo mật ở mỗi giai đoạn.
- **Kho tạo tác đáng tin cậy**: Chỉ triển khai từ các kho tạo tác đã được xác minh và bảo mật.

#### **Giám sát & Phản ứng liên tục**
- **Quét phụ thuộc**: Giám sát lỗ hổng liên tục cho tất cả các phụ thuộc phần mềm và thành phần AI.
- **Giám sát mô hình**: Đánh giá liên tục hành vi mô hình, sự lệch hiệu suất và các bất thường về bảo mật.
- **Theo dõi sức khỏe dịch vụ**: Giám sát các dịch vụ AI bên ngoài về tính khả dụng, sự cố bảo mật và thay đổi chính sách.
- **Tích hợp thông tin mối đe dọa**: Kết hợp các nguồn thông tin mối đe dọa cụ thể cho rủi ro bảo mật AI và ML.

#### **Kiểm soát truy cập & Nguyên tắc tối thiểu**
- **Quyền hạn cấp thành phần**: Hạn chế quyền truy cập vào mô hình, dữ liệu và dịch vụ dựa trên nhu cầu kinh doanh.
- **Quản lý tài khoản dịch vụ**: Thực hiện các tài khoản dịch vụ chuyên dụng với quyền hạn tối thiểu cần thiết.
- **Phân đoạn mạng**: Cách ly các thành phần AI và hạn chế truy cập mạng giữa các dịch vụ.
- **Kiểm soát cổng API**: Sử dụng cổng API tập trung để kiểm soát và giám sát quyền truy cập vào các dịch vụ AI bên ngoài.

#### **Phản ứng & Khôi phục sự cố**
- **Quy trình phản ứng nhanh**: Các quy trình được thiết lập để vá hoặc thay thế các thành phần AI bị xâm phạm.
- **Xoay vòng thông tin xác thực**: Hệ thống tự động để xoay vòng các bí mật, khóa API và thông tin xác thực dịch vụ.
- **Khả năng quay lại**: Khả năng nhanh chóng quay lại các phiên bản thành phần AI đã biết là tốt trước đó.
- **Khôi phục vi phạm chuỗi cung ứng**: Các quy trình cụ thể để phản ứng với các sự cố chuỗi cung ứng AI từ phía trên.

### Công cụ & Tích hợp bảo mật của Microsoft

**GitHub Advanced Security** cung cấp bảo vệ chuỗi cung ứng toàn diện bao gồm:
- **Quét bí mật**: Phát hiện tự động các thông tin xác thực, khóa API và token trong kho lưu trữ.
- **Quét phụ thuộc**: Đánh giá lỗ hổng cho các phụ thuộc và thư viện mã nguồn mở.
- **Phân tích CodeQL**: Phân tích mã tĩnh để tìm lỗ hổng bảo mật và vấn đề mã hóa.
- **Thông tin chuỗi cung ứng**: Hiển thị tình trạng sức khỏe và bảo mật của các phụ thuộc.

**Tích hợp Azure DevOps & Azure Repos:**
- Tích hợp quét bảo mật liền mạch trên các nền tảng phát triển của Microsoft.
- Kiểm tra bảo mật tự động trong Azure Pipelines cho khối lượng công việc AI.
- Thực thi chính sách cho triển khai thành phần AI an toàn.

**Thực tiễn nội bộ của Microsoft:**
Microsoft thực hiện các thực tiễn bảo mật chuỗi cung ứng rộng rãi trên tất cả các sản phẩm. Tìm hiểu về các phương pháp đã được chứng minh trong [Hành trình bảo mật chuỗi cung ứng phần mềm tại Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).
### **Giải pháp bảo mật của Microsoft**
- [Tài liệu Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Dịch vụ Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Bảo mật Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Thực hành tốt nhất về quản lý token Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Hướng dẫn triển khai & bài học thực hành**
- [Azure API Management làm cổng xác thực MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Xác thực Microsoft Entra ID với máy chủ MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Lưu trữ và mã hóa token an toàn (Video)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **DevOps & Bảo mật chuỗi cung ứng**
- [Bảo mật Azure DevOps](https://azure.microsoft.com/products/devops)
- [Bảo mật Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [Hành trình bảo mật chuỗi cung ứng của Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Tài liệu bảo mật bổ sung**

Để có hướng dẫn bảo mật toàn diện, hãy tham khảo các tài liệu chuyên biệt trong phần này:

- **[Thực hành tốt nhất về bảo mật MCP 2025](./mcp-security-best-practices-2025.md)** - Các thực hành tốt nhất về bảo mật đầy đủ cho triển khai MCP
- **[Triển khai Azure Content Safety](./azure-content-safety-implementation.md)** - Ví dụ thực tiễn về tích hợp Azure Content Safety  
- **[Kiểm soát bảo mật MCP 2025](./mcp-security-controls-2025.md)** - Các kỹ thuật và kiểm soát bảo mật mới nhất cho triển khai MCP
- **[Tham khảo nhanh thực hành tốt nhất MCP](./mcp-best-practices.md)** - Hướng dẫn tham khảo nhanh về các thực hành bảo mật MCP thiết yếu

---

## Tiếp theo

Tiếp theo: [Chương 3: Bắt đầu](../03-GettingStarted/README.md)

**Tuyên bố miễn trừ trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ bản địa nên được coi là nguồn thông tin chính thức. Đối với các thông tin quan trọng, khuyến nghị sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ sự hiểu lầm hoặc diễn giải sai nào phát sinh từ việc sử dụng bản dịch này.