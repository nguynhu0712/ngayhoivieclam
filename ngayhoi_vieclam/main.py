from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

# Lấy đường dẫn DB từ biến môi trường, mặc định là ngayhoi.db
DB_PATH = os.environ.get("DB_PATH", "ngayhoi.db")

app = FastAPI(title="Ngày Hội Việc Làm API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DangKy(BaseModel):
    ma_sv: str
    ma_phien: str

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS dang_ky (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_sv TEXT NOT NULL,
                ma_phien TEXT NOT NULL,
                UNIQUE(ma_sv, ma_phien)
            )
        ''')
        conn.commit()

# Khởi tạo DB khi app start
init_db()

@app.get("/api/con-cho")
async def con_cho(ma_phien: str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (ma_phien,))
            count = cursor.fetchone()[0]
            return {"con_cho": 30 - count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/dang-ky", status_code=status.HTTP_201_CREATED)
async def dang_ky_tham_gia(registration: DangKy):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # 1. Kiểm tra giới hạn 30 chỗ
            cursor.execute("SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (registration.ma_phien,))
            count = cursor.fetchone()[0]
            if count >= 30:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="HET_CHO")

            # 2. Chèn dữ liệu
            cursor.execute("INSERT INTO dang_ky (ma_sv, ma_phien) VALUES (?, ?)",
                           (registration.ma_sv, registration.ma_phien))
            conn.commit()
            return {"ok": True}

    except HTTPException as he:
        raise he
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="DA_DANG_KY")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
