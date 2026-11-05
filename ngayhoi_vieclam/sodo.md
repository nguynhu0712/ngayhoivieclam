sequenceDiagram
    autonumber
    participant User as Người dùng (Frontend)
    participant API as FastAPI Backend
    participant DB as SQLite Database

    Note over User, DB: Trường hợp 1: Đăng ký lần đầu (Thành công)
    User->>API: POST /api/dang-ky {ma_sv, ma_phien}
    API->>DB: INSERT INTO dang_ky (ma_sv, ma_phien)
    DB-->>API: Xác nhận ghi dữ liệu thành công
    API-->>User: HTTP 201 Created {"ok": true}
    User->>User: Hiển thị thông báo màu xanh

    Note over User, DB: Trường hợp 2: Đăng ký trùng (Lỗi 409)
    User->>API: POST /api/dang-ky {ma_sv, ma_phien}
    API->>DB: INSERT INTO dang_ky (ma_sv, ma_phien)
    DB-->>API: Lỗi IntegrityError (UNIQUE constraint failed)
    API-->>User: HTTP 409 Conflict {"detail": "DA_DANG_KY"}
    User->>User: Hiển thị thông báo màu đỏ "Sinh viên đã đăng ký phiên này!"
