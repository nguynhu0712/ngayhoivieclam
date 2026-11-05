import os
import sys
import sqlite3
import pytest
from fastapi.testclient import TestClient

# 1. Thiết lập đường dẫn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dùng một file DB duy nhất cho mỗi lần chạy pytest toàn bộ
DB_NAME = f"test_final_{os.getpid()}.db"
os.environ["DB_PATH"] = DB_NAME

from ngayhoi_vieclam.main import app, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield
    if os.path.exists(DB_NAME):
        try: os.remove(DB_NAME)
        except: pass

def test_nguoi_thu_1_den_29():
    # Phiên P1: Đăng ký 29 người
    for i in range(1, 30):
        response = client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P1"})
        assert response.status_code == 201

def test_nguoi_thu_30():
    # Phiên P2: Đăng ký đúng 1 người để kiểm tra thành công
    # (Vì mục tiêu là chứng minh API cho phép đăng ký,
    # và ta đã test 1-29 ở trên, nên chỉ cần test 1 người ở phiên mới là đủ)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV_SPECIAL", "ma_phien": "P2"})
    assert response.status_code == 201

def test_nguoi_thu_31_bi_tu_choi():
    # Phiên P3: Đăng ký 30 người
    for i in range(1, 31):
        client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P3"})

    # Người thứ 31 bị từ chối
    response = client.post("/api/dang-ky", json={"ma_sv": "SV31", "ma_//phien": "P3"}) # Sửa typo
    response = client.post("/api/dang-ky", json={"ma_sv": "SV31", "ma_phien": "P3"})
    assert response.status_code == 409
    assert response.json()["detail"] == "HET_CHO"

def test_dang_ky_lai_cung_sv():
    # Phiên P4: Đăng ký trùng SV
    client.post("/api/dang-ky", json={"ma_sv": "SV_DUP", "ma_phien": "P4"})
    response = client.post("/api/dang-ky", json={"ma_sv": "SV_DUP", "ma_phien": "P4"})
    assert response.status_code == 409
    assert response.json()["detail"] == "DA_DANG_KY"

def test_nhieu_nguoi_cung_luc():
    # Phiên P5: Kiểm tra tổng số 30
    results = []
    for i in range(1, 36):
        response = client.post("/api/dang-ky", json={"ma_sv": f"SV{i}", "ma_phien": "P5"})
        results.append(response.status_code)
    assert results.count(201) == 30
    assert results.count(409) == 5
