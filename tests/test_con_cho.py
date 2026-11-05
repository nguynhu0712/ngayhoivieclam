import os
import sys
import sqlite3
import pytest
from fastapi.testclient import TestClient

# 1. Thiết lập đường dẫn để import được app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["DB_PATH"] = "test_con_cho.db"

from ngayhoi_vieclam.main import app, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    with sqlite3.connect(os.environ["DB_PATH"]) as conn:
        conn.execute("DELETE FROM dang_ky")
        conn.commit()
    yield
    if os.path.exists(os.environ["DB_PATH"]):
        try: os.remove(os.environ["DB_PATH"])
        except: pass

def test_con_cho_phien_moi():
    # Phiên mới chưa có ai đăng ký -> 30 chỗ
    response = client.get("/api/con-cho?ma_phien=P1")
    assert response.status_code == 200
    assert response.json() == {"con_cho": 30}

def test_con_cho_khi_co_nguoi_dang_ky():
    # Giả lập đăng ký 5 người cho phiên P2
    with sqlite3.connect(os.environ["DB_PATH"]) as conn:
        cursor = conn.cursor()
        for i in range(5):
            cursor.execute("INSERT INTO dang_ky (ma_sv, ma_phien) VALUES (?, ?)", (f"SV{i}", "P2"))
        conn.commit()

    response = client.get("/api/con-cho?ma_phien=P2")
    assert response.status_code == 200
    assert response.json() == {"con_cho": 25}

def test_con_cho_khi_da_day():
    # Giả lập đăng ký đủ 30 người cho phiên P3
    with sqlite3.connect(os.environ["DB_PATH"]) as conn:
        cursor = conn.cursor()
        for i in range(30):
            cursor.execute("INSERT INTO dang_ky (ma_sv, ma_phien) VALUES (?, ?)", (f"SV{i}", "P3"))
        conn.commit()

    response = client.get("/api/con-cho?ma_phien=P3")
    assert response.status_code == 200
    assert response.json() == {"con_cho": 0}
