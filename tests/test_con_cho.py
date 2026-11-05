import os
import sys
import sqlite3
import pytest
from fastapi.testclient import TestClient

# 1. Thiết lập đường dẫn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Sử dụng một file DB riêng biệt cho mỗi lần chạy test để tránh xung đột dữ liệu
DB_NAME = f"test_con_cho_{os.getpid()}.db"
os.environ["DB_PATH"] = DB_NAME

from ngayhoi_vieclam.main import app, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Khởi tạo lại DB cho mỗi test case
    init_db()
    yield
    # Xóa file db sau khi test xong để sạch máy
    if os.path.exists(DB_NAME):
        try: os.remove(DB_NAME)
        except: pass

def test_con_cho_phien_moi():
    response = client.get("/api/con-cho?ma_phien=P1")
    assert response.status_code == 200
    assert response.json() == {"con_cho": 30}

def test_con_cho_khi_co_nguoi_dang_ky():
    # Đăng ký 5 người cho phiên P2 qua API để đảm bảo dùng chung DB
    for i in range(5):
        client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P2"})

    response = client.get("/api/con-cho?ma_phien=P2")
    assert response.status_code == 200
    assert response.json() == {"con_cho": 25}

def test_con_cho_khi_da_day():
    for i in range(30):
        client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P3"})

    response = client.get("/api/con-cho?ma_phien=P3")
    assert response.status_code == 200
    assert response.json() == {"con_cho": 0}
