<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T23:31:35+00:00",
  "source_file": "changelog.md",
  "language_code": "vi"
}
-->
# Nhật ký thay đổi: Chương trình học MCP cho người mới bắt đầu

Tài liệu này là bản ghi lại tất cả các thay đổi quan trọng được thực hiện đối với chương trình học Model Context Protocol (MCP) dành cho người mới bắt đầu. Các thay đổi được ghi lại theo thứ tự thời gian ngược (thay đổi mới nhất ở trên cùng).

## Ngày 6 tháng 10, 2025

### Mở rộng phần Bắt đầu – Sử dụng máy chủ nâng cao & Xác thực đơn giản

#### Sử dụng máy chủ nâng cao (03-GettingStarted/10-advanced)
- **Thêm chương mới**: Giới thiệu hướng dẫn toàn diện về cách sử dụng máy chủ MCP nâng cao, bao gồm cả kiến trúc máy chủ thông thường và cấp thấp.
  - **So sánh máy chủ thông thường và cấp thấp**: So sánh chi tiết và ví dụ mã trong Python và TypeScript cho cả hai cách tiếp cận.
  - **Thiết kế dựa trên trình xử lý**: Giải thích cách quản lý công cụ/tài nguyên/lời nhắc dựa trên trình xử lý để triển khai máy chủ linh hoạt và có khả năng mở rộng.
  - **Mẫu thực tế**: Các kịch bản thực tế nơi các mẫu máy chủ cấp thấp mang lại lợi ích cho các tính năng và kiến trúc nâng cao.

#### Xác thực đơn giản (03-GettingStarted/11-simple-auth)
- **Thêm chương mới**: Hướng dẫn từng bước để triển khai xác thực đơn giản trong các máy chủ MCP.
  - **Khái niệm xác thực**: Giải thích rõ ràng về sự khác biệt giữa xác thực và ủy quyền, cũng như cách xử lý thông tin xác thực.
  - **Triển khai xác thực cơ bản**: Các mẫu xác thực dựa trên middleware trong Python (Starlette) và TypeScript (Express), kèm theo ví dụ mã.
  - **Tiến tới bảo mật nâng cao**: Hướng dẫn bắt đầu với xác thực đơn giản và tiến tới OAuth 2.1 và RBAC, kèm theo tham chiếu đến các mô-đun bảo mật nâng cao.

Những bổ sung này cung cấp hướng dẫn thực tế, dễ áp dụng để xây dựng các triển khai máy chủ MCP mạnh mẽ, an toàn và linh hoạt hơn, kết nối các khái niệm cơ bản với các mẫu sản xuất nâng cao.

## Ngày 29 tháng 9, 2025

### Phòng thí nghiệm tích hợp cơ sở dữ liệu máy chủ MCP - Lộ trình học tập thực hành toàn diện

#### 11-MCPServerHandsOnLabs - Chương trình học tích hợp cơ sở dữ liệu hoàn chỉnh mới
- **Lộ trình học tập 13 phòng thí nghiệm hoàn chỉnh**: Thêm chương trình học thực hành toàn diện để xây dựng các máy chủ MCP sẵn sàng cho sản xuất với tích hợp cơ sở dữ liệu PostgreSQL.
  - **Triển khai thực tế**: Trường hợp sử dụng phân tích bán lẻ Zava minh họa các mẫu cấp doanh nghiệp.
  - **Tiến trình học tập có cấu trúc**:
    - **Phòng thí nghiệm 00-03: Nền tảng** - Giới thiệu, Kiến trúc cốt lõi, Bảo mật & Đa người thuê, Thiết lập môi trường.
    - **Phòng thí nghiệm 04-06: Xây dựng máy chủ MCP** - Thiết kế & Lược đồ cơ sở dữ liệu, Triển khai máy chủ MCP, Phát triển công cụ.
    - **Phòng thí nghiệm 07-09: Tính năng nâng cao** - Tích hợp tìm kiếm ngữ nghĩa, Kiểm thử & Gỡ lỗi, Tích hợp VS Code.
    - **Phòng thí nghiệm 10-12: Triển khai & Thực hành tốt nhất** - Chiến lược triển khai, Giám sát & Khả năng quan sát, Thực hành tốt nhất & Tối ưu hóa.
  - **Công nghệ doanh nghiệp**: Khung FastMCP, PostgreSQL với pgvector, nhúng Azure OpenAI, Azure Container Apps, Application Insights.
  - **Tính năng nâng cao**: Bảo mật cấp hàng (RLS), tìm kiếm ngữ nghĩa, truy cập dữ liệu đa người thuê, nhúng vector, giám sát thời gian thực.

#### Chuẩn hóa thuật ngữ - Chuyển đổi từ "Module" sang "Lab"
- **Cập nhật tài liệu toàn diện**: Hệ thống hóa việc cập nhật tất cả các tệp README trong 11-MCPServerHandsOnLabs để sử dụng thuật ngữ "Lab" thay vì "Module".
  - **Tiêu đề phần**: Cập nhật "What This Module Covers" thành "What This Lab Covers" trên tất cả 13 phòng thí nghiệm.
  - **Mô tả nội dung**: Thay đổi "This module provides..." thành "This lab provides..." trong toàn bộ tài liệu.
  - **Mục tiêu học tập**: Cập nhật "By the end of this module..." thành "By the end of this lab...".
  - **Liên kết điều hướng**: Chuyển đổi tất cả các tham chiếu "Module XX:" thành "Lab XX:" trong các tham chiếu chéo và điều hướng.
  - **Theo dõi hoàn thành**: Cập nhật "After completing this module..." thành "After completing this lab...".
  - **Bảo toàn tham chiếu kỹ thuật**: Giữ nguyên các tham chiếu mô-đun Python trong các tệp cấu hình (ví dụ: `"module": "mcp_server.main"`).

#### Nâng cấp hướng dẫn học tập (study_guide.md)
- **Bản đồ chương trình học trực quan**: Thêm phần mới "11. Database Integration Labs" với hình ảnh hóa cấu trúc phòng thí nghiệm toàn diện.
- **Cấu trúc kho lưu trữ**: Cập nhật từ mười lên mười một phần chính với mô tả chi tiết về 11-MCPServerHandsOnLabs.
- **Hướng dẫn lộ trình học tập**: Nâng cao hướng dẫn điều hướng để bao quát các phần 00-11.
- **Phạm vi công nghệ**: Thêm chi tiết tích hợp FastMCP, PostgreSQL, và các dịch vụ Azure.
- **Kết quả học tập**: Nhấn mạnh phát triển máy chủ sẵn sàng sản xuất, các mẫu tích hợp cơ sở dữ liệu, và bảo mật cấp doanh nghiệp.

#### Nâng cấp cấu trúc README chính
- **Thuật ngữ dựa trên phòng thí nghiệm**: Cập nhật README.md chính trong 11-MCPServerHandsOnLabs để sử dụng cấu trúc "Lab" một cách nhất quán.
- **Tổ chức lộ trình học tập**: Tiến trình rõ ràng từ các khái niệm cơ bản qua triển khai nâng cao đến triển khai sản xuất.
- **Tập trung thực tế**: Nhấn mạnh học tập thực hành với các mẫu và công nghệ cấp doanh nghiệp.

### Cải thiện chất lượng & tính nhất quán tài liệu
- **Nhấn mạnh học tập thực hành**: Tăng cường cách tiếp cận dựa trên phòng thí nghiệm trong toàn bộ tài liệu.
- **Tập trung vào mẫu doanh nghiệp**: Làm nổi bật các triển khai sẵn sàng sản xuất và các cân nhắc bảo mật cấp doanh nghiệp.
- **Tích hợp công nghệ**: Bao quát toàn diện các dịch vụ Azure hiện đại và các mẫu tích hợp AI.
- **Tiến trình học tập**: Lộ trình rõ ràng, có cấu trúc từ các khái niệm cơ bản đến triển khai sản xuất.

## Ngày 26 tháng 9, 2025

### Nâng cấp nghiên cứu trường hợp - Tích hợp GitHub MCP Registry

#### Nghiên cứu trường hợp (09-CaseStudy/) - Tập trung phát triển hệ sinh thái
- **README.md**: Mở rộng lớn với nghiên cứu trường hợp GitHub MCP Registry toàn diện.
  - **Nghiên cứu trường hợp GitHub MCP Registry**: Nghiên cứu trường hợp mới toàn diện về việc ra mắt GitHub MCP Registry vào tháng 9 năm 2025.
    - **Phân tích vấn đề**: Xem xét chi tiết các thách thức trong việc khám phá và triển khai máy chủ MCP phân mảnh.
    - **Kiến trúc giải pháp**: Cách tiếp cận registry tập trung của GitHub với cài đặt VS Code chỉ bằng một cú nhấp chuột.
    - **Tác động kinh doanh**: Cải thiện đáng kể việc giới thiệu và năng suất của nhà phát triển.
    - **Giá trị chiến lược**: Tập trung vào triển khai tác nhân mô-đun và khả năng tương tác giữa các công cụ.
    - **Phát triển hệ sinh thái**: Định vị như một nền tảng cơ bản cho tích hợp tác nhân.
  - **Cấu trúc nghiên cứu trường hợp nâng cao**: Cập nhật tất cả bảy nghiên cứu trường hợp với định dạng nhất quán và mô tả toàn diện.
    - Azure AI Travel Agents: Nhấn mạnh điều phối đa tác nhân.
    - Tích hợp Azure DevOps: Tập trung vào tự động hóa quy trình làm việc.
    - Truy xuất tài liệu thời gian thực: Triển khai máy khách console Python.
    - Trình tạo kế hoạch học tập tương tác: Ứng dụng web hội thoại Chainlit.
    - Tài liệu trong trình soạn thảo: Tích hợp VS Code và GitHub Copilot.
    - Quản lý API Azure: Các mẫu tích hợp API cấp doanh nghiệp.
    - GitHub MCP Registry: Phát triển hệ sinh thái và nền tảng cộng đồng.
  - **Kết luận toàn diện**: Viết lại phần kết luận làm nổi bật bảy nghiên cứu trường hợp trải dài trên nhiều khía cạnh triển khai MCP.
    - Phân loại Tích hợp Doanh nghiệp, Điều phối Đa Tác nhân, Năng suất Nhà phát triển.
    - Phát triển Hệ sinh thái, Ứng dụng Giáo dục.
    - Cải thiện hiểu biết về các mẫu kiến trúc, chiến lược triển khai, và thực hành tốt nhất.
    - Nhấn mạnh MCP như một giao thức trưởng thành, sẵn sàng sản xuất.

#### Cập nhật hướng dẫn học tập (study_guide.md)
- **Bản đồ chương trình học trực quan**: Cập nhật sơ đồ tư duy để bao gồm GitHub MCP Registry trong phần Nghiên cứu trường hợp.
- **Mô tả nghiên cứu trường hợp**: Nâng cấp từ mô tả chung thành phân tích chi tiết bảy nghiên cứu trường hợp toàn diện.
- **Cấu trúc kho lưu trữ**: Cập nhật phần 10 để phản ánh phạm vi nghiên cứu trường hợp toàn diện với các chi tiết triển khai cụ thể.
- **Tích hợp nhật ký thay đổi**: Thêm mục ngày 26 tháng 9, 2025 ghi lại việc bổ sung GitHub MCP Registry và nâng cấp nghiên cứu trường hợp.
- **Cập nhật ngày tháng**: Cập nhật dấu thời gian ở chân trang để phản ánh lần sửa đổi mới nhất (ngày 26 tháng 9, 2025).

### Cải thiện chất lượng tài liệu
- **Tăng cường tính nhất quán**: Chuẩn hóa định dạng và cấu trúc nghiên cứu trường hợp trên tất cả bảy ví dụ.
- **Phạm vi toàn diện**: Các nghiên cứu trường hợp hiện bao quát các kịch bản doanh nghiệp, năng suất nhà phát triển, và phát triển hệ sinh thái.
- **Định vị chiến lược**: Tăng cường tập trung vào MCP như một nền tảng cơ bản cho triển khai hệ thống tác nhân.
- **Tích hợp tài nguyên**: Cập nhật các tài nguyên bổ sung để bao gồm liên kết GitHub MCP Registry.

## Ngày 15 tháng 9, 2025

### Mở rộng chủ đề nâng cao - Giao thức tùy chỉnh & Kỹ thuật ngữ cảnh

#### Giao thức tùy chỉnh MCP (05-AdvancedTopics/mcp-transport/) - Hướng dẫn triển khai nâng cao mới
- **README.md**: Hướng dẫn triển khai hoàn chỉnh cho các cơ chế giao thức tùy chỉnh MCP.
  - **Giao thức Azure Event Grid**: Triển khai giao thức không máy chủ dựa trên sự kiện toàn diện.
    - Ví dụ C#, TypeScript, và Python với tích hợp Azure Functions.
    - Các mẫu kiến trúc dựa trên sự kiện cho các giải pháp MCP có khả năng mở rộng.
    - Bộ nhận webhook và xử lý tin nhắn dựa trên đẩy.
  - **Giao thức Azure Event Hubs**: Triển khai giao thức truyền phát hiệu suất cao.
    - Khả năng truyền phát thời gian thực cho các kịch bản độ trễ thấp.
    - Chiến lược phân vùng và quản lý điểm kiểm tra.
    - Gộp tin nhắn và tối ưu hóa hiệu suất.
  - **Mẫu tích hợp doanh nghiệp**: Ví dụ kiến trúc sẵn sàng sản xuất.
    - Xử lý MCP phân tán trên nhiều Azure Functions.
    - Kiến trúc giao thức lai kết hợp nhiều loại giao thức.
    - Chiến lược độ bền tin nhắn, độ tin cậy, và xử lý lỗi.
  - **Bảo mật & Giám sát**: Tích hợp Azure Key Vault và các mẫu quan sát.
    - Xác thực danh tính được quản lý và truy cập tối thiểu.
    - Telemetry Application Insights và giám sát hiệu suất.
    - Bộ ngắt mạch và các mẫu chịu lỗi.
  - **Khung kiểm thử**: Chiến lược kiểm thử toàn diện cho các giao thức tùy chỉnh.
    - Kiểm thử đơn vị với các khung kiểm thử giả lập.
    - Kiểm thử tích hợp với Azure Test Containers.
    - Cân nhắc kiểm thử hiệu suất và tải.

#### Kỹ thuật ngữ cảnh (05-AdvancedTopics/mcp-contextengineering/) - Lĩnh vực AI mới nổi
- **README.md**: Khám phá toàn diện về kỹ thuật ngữ cảnh như một lĩnh vực mới nổi.
  - **Nguyên tắc cốt lõi**: Chia sẻ ngữ cảnh hoàn chỉnh, nhận thức quyết định hành động, và quản lý cửa sổ ngữ cảnh.
  - **Sự phù hợp với giao thức MCP**: Cách thiết kế MCP giải quyết các thách thức kỹ thuật ngữ cảnh.
    - Hạn chế cửa sổ ngữ cảnh và chiến lược tải tiến bộ.
    - Xác định mức độ liên quan và truy xuất ngữ cảnh động.
    - Xử lý ngữ cảnh đa phương tiện và các cân nhắc bảo mật.
  - **Cách tiếp cận triển khai**: Kiến trúc đơn luồng so với đa tác nhân.
    - Kỹ thuật phân đoạn và ưu tiên ngữ cảnh.
    - Tải ngữ cảnh tiến bộ và chiến lược nén.
    - Cách tiếp cận ngữ cảnh phân lớp và tối ưu hóa truy xuất.
  - **Khung đo lường**: Các chỉ số mới nổi để đánh giá hiệu quả ngữ cảnh.
    - Hiệu quả đầu vào, hiệu suất, chất lượng, và cân nhắc trải nghiệm người dùng.
    - Cách tiếp cận thử nghiệm để tối ưu hóa ngữ cảnh.
    - Phân tích lỗi và phương pháp cải tiến.

#### Cập nhật điều hướng chương trình học (README.md)
- **Cấu trúc mô-đun nâng cao**: Cập nhật bảng chương trình học để bao gồm các chủ đề nâng cao mới.
  - Thêm các mục Kỹ thuật Ngữ cảnh (5.14) và Giao thức Tùy chỉnh (5.15).
  - Định dạng và liên kết điều hướng nhất quán trên tất cả các mô-đun.
  - Cập nhật mô tả để phản ánh phạm vi nội dung hiện tại.

### Cải thiện cấu trúc thư mục
- **Chuẩn hóa tên**: Đổi tên "mcp transport" thành "mcp-transport" để nhất quán với các thư mục chủ đề nâng cao khác.
- **Tổ chức nội dung**: Tất cả các thư mục 05-AdvancedTopics hiện tuân theo mẫu đặt tên nhất quán (mcp-[chủ đề]).

### Cải thiện chất lượng tài liệu
- **Phù hợp với đặc tả MCP**: Tất cả nội dung mới tham chiếu đến Đặc tả MCP hiện tại 2025-06-18.
- **Ví dụ đa ngôn ngữ**: Ví dụ mã toàn diện trong C#, TypeScript, và Python.
- **Tập trung vào doanh nghiệp**: Các mẫu sẵn sàng sản xuất và tích hợp đám mây Azure xuyên suốt.
- **Tài liệu trực quan**: Biểu đồ Mermaid để hình dung kiến trúc và luồng.

## Ngày 18 tháng 8, 2025

### Cập nhật tài liệu toàn diện - Tiêu chuẩn MCP 2025-06-18

#### Thực hành bảo mật MCP tốt nhất (02-Security/) - Hiện đại hóa hoàn chỉnh
- **MCP-SECURITY-BEST-PRACTICES-2025.md**: Viết lại hoàn chỉnh phù hợp với Đặc tả MCP 2025-06-18.
  - **Yêu cầu bắt buộc**: Thêm các yêu cầu MUST/MUST NOT rõ ràng từ đặc tả chính thức với các chỉ báo trực quan rõ ràng.
  - **12 Thực hành bảo mật cốt lõi**: Tái cấu trúc từ danh sách 15 mục thành các miền bảo mật toàn diện.
    - Bảo mật Token & Xác thực với tích hợp nhà cung cấp danh tính bên ngoài.
    - Quản lý phiên & Bảo mật truyền tải với các yêu cầu mã hóa.
    - Bảo vệ mối đe dọa AI cụ thể với tích hợp Microsoft Prompt Shields.
    - Kiểm soát truy cập & Quyền với nguyên tắc đặc quyền tối thiểu.
    - An toàn nội dung & Giám sát với tích hợp Azure Content Safety.
    - Bảo mật chuỗi cung ứng với xác minh thành phần toàn diện.
    - Bảo mật OAuth & Phòng chống tấn công Confused Deputy với triển khai PKCE.
    - Phản ứng & Phục hồi sự cố với các khả năng tự động hóa.
    - Tuân thủ & Quản trị với sự phù hợp quy định.
    - Kiểm soát bảo mật nâng cao với kiến trúc zero trust.
    - Tích hợp hệ sinh thái bảo mật Microsoft với các giải pháp toàn diện.
    - Tiến hóa bảo mật liên tục với các thực hành thích ứng.
  - **Giải pháp bảo mật Microsoft**: Hướng dẫn tích hợp nâng cao cho
#### Chủ đề Nâng cao về Bảo mật (05-AdvancedTopics/mcp-security/) - Triển khai sẵn sàng cho sản xuất
- **README.md**: Viết lại hoàn toàn để triển khai bảo mật cấp doanh nghiệp
  - **Căn chỉnh với Đặc tả hiện tại**: Cập nhật theo Đặc tả MCP 2025-06-18 với các yêu cầu bảo mật bắt buộc
  - **Xác thực nâng cao**: Tích hợp Microsoft Entra ID với các ví dụ chi tiết về .NET và Java Spring Security
  - **Tích hợp Bảo mật AI**: Triển khai Microsoft Prompt Shields và Azure Content Safety với các ví dụ chi tiết bằng Python
  - **Giảm thiểu mối đe dọa nâng cao**: Các ví dụ triển khai toàn diện cho
    - Ngăn chặn tấn công Confused Deputy với PKCE và xác thực sự đồng ý của người dùng
    - Ngăn chặn truyền qua token với xác thực đối tượng và quản lý token an toàn
    - Ngăn chặn chiếm đoạt phiên với liên kết mã hóa và phân tích hành vi
  - **Tích hợp bảo mật doanh nghiệp**: Giám sát Azure Application Insights, các pipeline phát hiện mối đe dọa và bảo mật chuỗi cung ứng
  - **Danh sách kiểm tra triển khai**: Rõ ràng giữa các kiểm soát bảo mật bắt buộc và khuyến nghị với lợi ích từ hệ sinh thái bảo mật của Microsoft

### Chất lượng Tài liệu & Căn chỉnh Tiêu chuẩn
- **Tham chiếu Đặc tả**: Cập nhật tất cả tham chiếu theo Đặc tả MCP 2025-06-18 hiện tại
- **Hệ sinh thái Bảo mật Microsoft**: Tăng cường hướng dẫn tích hợp trong toàn bộ tài liệu bảo mật
- **Triển khai thực tế**: Thêm các ví dụ mã chi tiết trong .NET, Java và Python với các mẫu doanh nghiệp
- **Tổ chức tài nguyên**: Phân loại toàn diện tài liệu chính thức, tiêu chuẩn bảo mật và hướng dẫn triển khai
- **Chỉ báo trực quan**: Đánh dấu rõ ràng các yêu cầu bắt buộc so với các thực hành khuyến nghị

#### Các khái niệm cốt lõi (01-CoreConcepts/) - Hiện đại hóa hoàn toàn
- **Cập nhật phiên bản giao thức**: Cập nhật để tham chiếu đến Đặc tả MCP 2025-06-18 hiện tại với định dạng phiên bản theo ngày (YYYY-MM-DD)
- **Tinh chỉnh kiến trúc**: Nâng cao mô tả về Máy chủ, Máy khách và Máy chủ để phản ánh các mẫu kiến trúc MCP hiện tại
  - Máy chủ hiện được định nghĩa rõ ràng là các ứng dụng AI phối hợp nhiều kết nối máy khách MCP
  - Máy khách được mô tả là các kết nối giao thức duy trì mối quan hệ một-một với máy chủ
  - Máy chủ được nâng cao với các kịch bản triển khai cục bộ và từ xa
- **Tái cấu trúc nguyên thủy**: Cải tổ hoàn toàn các nguyên thủy máy chủ và máy khách
  - Nguyên thủy Máy chủ: Tài nguyên (nguồn dữ liệu), Gợi ý (mẫu), Công cụ (chức năng thực thi) với các giải thích và ví dụ chi tiết
  - Nguyên thủy Máy khách: Lấy mẫu (hoàn thành LLM), Khai thác (đầu vào người dùng), Ghi nhật ký (gỡ lỗi/giám sát)
  - Cập nhật với các mẫu phương pháp khám phá (`*/list`), truy xuất (`*/get`) và thực thi (`*/call`) hiện tại
- **Kiến trúc giao thức**: Giới thiệu mô hình kiến trúc hai lớp
  - Lớp Dữ liệu: Nền tảng JSON-RPC 2.0 với quản lý vòng đời và các nguyên thủy
  - Lớp Truyền tải: STDIO (cục bộ) và HTTP có thể truyền phát với SSE (từ xa)
- **Khung bảo mật**: Các nguyên tắc bảo mật toàn diện bao gồm sự đồng ý rõ ràng của người dùng, bảo vệ quyền riêng tư dữ liệu, an toàn thực thi công cụ và bảo mật lớp truyền tải
- **Mẫu giao tiếp**: Cập nhật các thông điệp giao thức để hiển thị các luồng khởi tạo, khám phá, thực thi và thông báo
- **Ví dụ mã**: Làm mới các ví dụ đa ngôn ngữ (.NET, Java, Python, JavaScript) để phản ánh các mẫu MCP SDK hiện tại

#### Bảo mật (02-Security/) - Cải tổ bảo mật toàn diện  
- **Căn chỉnh tiêu chuẩn**: Hoàn toàn phù hợp với các yêu cầu bảo mật của Đặc tả MCP 2025-06-18
- **Tiến hóa xác thực**: Tài liệu hóa sự phát triển từ các máy chủ OAuth tùy chỉnh sang ủy quyền nhà cung cấp danh tính bên ngoài (Microsoft Entra ID)
- **Phân tích mối đe dọa AI cụ thể**: Tăng cường phạm vi các vector tấn công AI hiện đại
  - Các kịch bản tấn công tiêm gợi ý chi tiết với các ví dụ thực tế
  - Cơ chế đầu độc công cụ và các mẫu tấn công "giật thảm"
  - Đầu độc cửa sổ ngữ cảnh và các cuộc tấn công nhầm lẫn mô hình
- **Giải pháp Bảo mật AI của Microsoft**: Phạm vi toàn diện về hệ sinh thái bảo mật của Microsoft
  - AI Prompt Shields với các kỹ thuật phát hiện, làm nổi bật và phân tách tiên tiến
  - Các mẫu tích hợp Azure Content Safety
  - GitHub Advanced Security để bảo vệ chuỗi cung ứng
- **Giảm thiểu mối đe dọa nâng cao**: Các kiểm soát bảo mật chi tiết cho
  - Chiếm đoạt phiên với các kịch bản tấn công cụ thể của MCP và các yêu cầu ID phiên mã hóa
  - Các vấn đề Confused Deputy trong các kịch bản proxy MCP với các yêu cầu đồng ý rõ ràng
  - Lỗ hổng truyền qua token với các kiểm soát xác thực bắt buộc
- **Bảo mật chuỗi cung ứng**: Mở rộng phạm vi chuỗi cung ứng AI bao gồm các mô hình nền tảng, dịch vụ nhúng, nhà cung cấp ngữ cảnh và API bên thứ ba
- **Bảo mật nền tảng**: Tăng cường tích hợp với các mẫu bảo mật doanh nghiệp bao gồm kiến trúc zero trust và hệ sinh thái bảo mật của Microsoft
- **Tổ chức tài nguyên**: Phân loại các liên kết tài nguyên toàn diện theo loại (Tài liệu chính thức, Tiêu chuẩn, Nghiên cứu, Giải pháp Microsoft, Hướng dẫn triển khai)

### Cải tiến Chất lượng Tài liệu
- **Mục tiêu học tập có cấu trúc**: Tăng cường mục tiêu học tập với các kết quả cụ thể, có thể hành động
- **Tham chiếu chéo**: Thêm liên kết giữa các chủ đề bảo mật và khái niệm cốt lõi liên quan
- **Thông tin hiện tại**: Cập nhật tất cả các tham chiếu ngày và liên kết đặc tả theo tiêu chuẩn hiện tại
- **Hướng dẫn triển khai**: Thêm các hướng dẫn triển khai cụ thể, có thể hành động trong suốt cả hai phần

## Ngày 16 tháng 7, 2025

### Cải tiến README và Điều hướng
- Thiết kế lại hoàn toàn điều hướng chương trình học trong README.md
- Thay thế các thẻ `<details>` bằng định dạng bảng dễ tiếp cận hơn
- Tạo các tùy chọn bố cục thay thế trong thư mục "alternative_layouts" mới
- Thêm các ví dụ điều hướng kiểu thẻ, tab và accordion
- Cập nhật phần cấu trúc kho lưu trữ để bao gồm tất cả các tệp mới nhất
- Tăng cường phần "Cách sử dụng chương trình học này" với các khuyến nghị rõ ràng
- Cập nhật các liên kết đặc tả MCP để trỏ đến các URL chính xác
- Thêm phần Kỹ thuật Ngữ cảnh (5.14) vào cấu trúc chương trình học

### Cập nhật Hướng dẫn Học tập
- Sửa đổi hoàn toàn hướng dẫn học tập để phù hợp với cấu trúc kho lưu trữ hiện tại
- Thêm các phần mới về Máy khách và Công cụ MCP, và Các Máy chủ MCP phổ biến
- Cập nhật Bản đồ Chương trình Học tập Trực quan để phản ánh chính xác tất cả các chủ đề
- Tăng cường mô tả về Các Chủ đề Nâng cao để bao quát tất cả các lĩnh vực chuyên biệt
- Cập nhật phần Nghiên cứu Tình huống để phản ánh các ví dụ thực tế
- Thêm nhật ký thay đổi toàn diện này

### Đóng góp Cộng đồng (06-CommunityContributions/)
- Thêm thông tin chi tiết về các máy chủ MCP cho tạo hình ảnh
- Thêm phần toàn diện về sử dụng Claude trong VSCode
- Thêm hướng dẫn thiết lập và sử dụng máy khách terminal Cline
- Cập nhật phần máy khách MCP để bao gồm tất cả các tùy chọn máy khách phổ biến
- Tăng cường các ví dụ đóng góp với các mẫu mã chính xác hơn

### Chủ đề Nâng cao (05-AdvancedTopics/)
- Tổ chức tất cả các thư mục chủ đề chuyên biệt với cách đặt tên nhất quán
- Thêm tài liệu và ví dụ về kỹ thuật ngữ cảnh
- Thêm tài liệu tích hợp tác nhân Foundry
- Tăng cường tài liệu tích hợp bảo mật Entra ID

## Ngày 11 tháng 6, 2025

### Tạo ban đầu
- Phát hành phiên bản đầu tiên của chương trình học MCP cho người mới bắt đầu
- Tạo cấu trúc cơ bản cho tất cả 10 phần chính
- Triển khai Bản đồ Chương trình Học tập Trực quan để điều hướng
- Thêm các dự án mẫu ban đầu bằng nhiều ngôn ngữ lập trình

### Bắt đầu (03-GettingStarted/)
- Tạo các ví dụ triển khai máy chủ đầu tiên
- Thêm hướng dẫn phát triển máy khách
- Bao gồm hướng dẫn tích hợp máy khách LLM
- Thêm tài liệu tích hợp VS Code
- Triển khai các ví dụ máy chủ Server-Sent Events (SSE)

### Các khái niệm cốt lõi (01-CoreConcepts/)
- Thêm giải thích chi tiết về kiến trúc máy khách-máy chủ
- Tạo tài liệu về các thành phần giao thức chính
- Tài liệu hóa các mẫu thông điệp trong MCP

## Ngày 23 tháng 5, 2025

### Cấu trúc Kho lưu trữ
- Khởi tạo kho lưu trữ với cấu trúc thư mục cơ bản
- Tạo các tệp README cho mỗi phần chính
- Thiết lập cơ sở hạ tầng dịch thuật
- Thêm tài sản hình ảnh và sơ đồ

### Tài liệu
- Tạo README.md ban đầu với tổng quan chương trình học
- Thêm CODE_OF_CONDUCT.md và SECURITY.md
- Thiết lập SUPPORT.md với hướng dẫn nhận trợ giúp
- Tạo cấu trúc hướng dẫn học tập sơ bộ

## Ngày 15 tháng 4, 2025

### Lập kế hoạch và Khung
- Lập kế hoạch ban đầu cho chương trình học MCP cho người mới bắt đầu
- Xác định mục tiêu học tập và đối tượng mục tiêu
- Phác thảo cấu trúc 10 phần của chương trình học
- Phát triển khung khái niệm cho các ví dụ và nghiên cứu tình huống
- Tạo các ví dụ nguyên mẫu ban đầu cho các khái niệm chính

---

**Tuyên bố miễn trừ trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ bản địa nên được coi là nguồn thông tin chính thức. Đối với các thông tin quan trọng, khuyến nghị sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm cho bất kỳ sự hiểu lầm hoặc diễn giải sai nào phát sinh từ việc sử dụng bản dịch này.