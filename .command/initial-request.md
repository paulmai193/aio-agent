Tạo dự án Python application điều phối các agent từ repository https://github.com/contains-studio/agents để xử lý các yêu cầu end-to-end, tích hợp với API gốc Ollama (REST).
Yêu cầu chi tiết:
- Kiến trúc source: Dạng module (có thể mở rộng thêm agent khác), phân tách rõ các thành phần.
- Công nghệ: Python, Docker, FastAPI, bổ sung công nghệ nếu cần để đảm bảo tối ưu hóa vận hành.
- Chức năng chính:
- - Điều phối và quản lý các agent từ repository (tích hợp, khởi tạo, routing request).
- - Tích hợp Ollama thông qua API REST (sử dụng Python client hoặc trực tiếp qua HTTP request).
- - Endpoint FastAPI cho phép nhận yêu cầu từ phía người dùng và phân phối đến agent phù hợp, nhận kết quả từ Ollama, trả về client.
- Yêu cầu mở rộng: Dễ dàng thêm mới agent (không cần thêm LLM khác).
- Yêu cầu về nguyên tắc: Tuân thủ theo các nguyên tác được mô tả trong ../.rules/
