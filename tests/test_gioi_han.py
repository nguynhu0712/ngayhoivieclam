import os
import sys
import sqlite3
import pytest
from fastapi.testclient import TestClient

# 1. Thiết lập đường dẫn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Sử dụng một file DB tạm duy nhất cho mỗi test case để tránh Lock và mất bảng
os.environ["DB_PATH"] = "test_env.db"

from ngayhoi_vieclam.main import app, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Tạo lại bảng cho mỗi test case
    init_db()
    # Xóa dữ liệu cũ
    with sqlite3.connect(os.environ["DB_PATH"]) as conn:
        conn.execute("DELETE FROM dang_ky")
        conn.commit()
    yield
    # Xóa file db sau khi test xong
    if os.path.exists(os.environ["DB_PATH"]):
        try: os.remove(os.environ["DB_PATH"])
        except: pass

def test_nguoi_thu_1_den_29():
    for i in range(1, 30):
        response = client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P1"})
        assert response.status_code == 201

def test_nguoi_thu_30():
    for i in range(1, 30):
        client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P1"})
    response = client.post("/api/dang-ky", json={"ma_sv": "SV30", "ma_phien": "P1"})
    assert response.status_code == 201

def test_nguoi_thu_31_bi_tu_choi():
    for i in range(1, 31):
        client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P1"})
    response = client.post("/api/dang-ky", json={"ma_sv": "SV31", "ma_phien": "P1"})
    assert response.status_code == 409
    assert response.json()["detail"] == "HET_CHO"

def test_dang_ky_lai_cung_sv():
    client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P1"})
    response = client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P1"})
    assert response.status_code == 409
    assert response.json()["detail"] == "DA_DANG_KY"

def test_nhieu_nguoi_cung_luc():
    results = []
    for i in range(1, 36):
        response = client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P2"})
        results.append(response.status_code)
    assert results.count(201) == 30
    assert results.count(409) == 5
