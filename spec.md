# Đặc tả tính năng: Giới hạn số lượng đăng ký phiên

## 1. Mô tả quy tắc
Mỗi phiên đăng ký sự kiện có giới hạn tối đa là **30 chỗ**. Hệ thống phải kiểm tra số lượng người đã đăng ký trước khi chấp nhận yêu cầu mới và ngăn chặn việc đăng ký trùng lặp.

## 2. Kịch bản kiểm thử (Test Cases)

| STT | Kịch bản | Điều kiện đầu vào | Kết quả mong đợi | Mã phản hồi (HTTP Code) | Ghi chú |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | Đăng ký thành công | Phiên còn trống (< 30 người) | Lưu thông tin đăng ký vào DB | `201 Created` | Thành công |
| 2 | Phiên đã đầy | Phiên đã đủ 30 người | Từ chối đăng ký, thông báo hết chỗ | `409 Conflict` | Lỗi: `HET_CHO` |
| 3 | Đăng ký trùng lặp | Cùng Mã SV và Mã phiên đã tồn tại | Từ chối đăng ký, thông báo đã đăng ký | `409 Conflict` | Lỗi: `DA_DANG_KY` |
| 4 | Ngoài phạm vi | Yêu cầu hủy đăng ký | Không xử lý trong phạm vi tính năng này | N/A | Out of Scope |
