# AI Agent Guidelines - Dự Án Cổng Đăng Ký Sự Kiện

Tệp này quy định các nguyên tắc bắt buộc mà mọi AI Agent phải tuân thủ khi tham gia phát triển dự án này.

## 🛡️ Phạm Vi Hoạt Động (Scope)
- **ĐƯỢC PHÉP**: Chỉ thực hiện chỉnh sửa, thêm mới hoặc tối ưu hóa mã nguồn tại phần **Backend (FastAPI)**.
- **CẤM TUYỆT ĐỐI**:
  - Không sửa đổi bất kỳ nội dung nào trong tệp kiểm thử gốc: `tests/test_gioi_han.py`.
  - Không can thiệp vào cấu hình CI/CD trong thư mục `.github/`.

## 🧪 Quy Định Về Phát Triển Tính Năng
- **Yêu cầu kiểm thử**: Mọi tính năng mới hoặc thay đổi logic phải đi kèm với bài kiểm thử (test case) mới tương ứng, sử dụng framework `pytest`.
- **Kích thước thay đổi**: Giữ cho mỗi lần thay đổi (diff) nhỏ gọn, lý tưởng là dưới **200 dòng** để dễ dàng review.
- **Vị trí test**: Các bài test mới phải được đặt trong thư mục `tests/`.

## 💻 Tiêu Chuẩn Mã Nguồn (Code Quality)
- **Clean Code**: Viết mã nguồn sạch, tuân thủ chuẩn PEP 8 của Python.
- **Chú thích**: Mọi hàm, class hoặc logic phức tạp phải có comment giải thích rõ ràng mục đích và cách hoạt động.
- **Tính nhất quán**: Giữ nguyên phong cách đặt tên và cấu trúc hiện có của dự án.

---
*Vi phạm bất kỳ quy định nào trong tệp này sẽ được coi là lỗi triển khai.*
