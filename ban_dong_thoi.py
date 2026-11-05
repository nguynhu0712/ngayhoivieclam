import sys
import httpx
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

def send_request(client, url, ma_phien, sv_id):
    """Hàm gửi một yêu cầu đăng ký đơn lẻ"""
    payload = {
        "ma_sv": f"SV_TEST_{sv_id}", # Tạo mã SV khác nhau để không bị lỗi DA_DANG_KY
        "ma_phien": ma_phien
    }
    try:
        # Gửi request POST đến API
        response = client.post(url, json=payload)
        return response.status_code
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return 500

def main():
    # 1. Kiểm tra tham số dòng lệnh
    if len(sys.argv) < 2:
        print("Sử dụng: python ban_dong_thoi.py <ma_phien>")
        print("Ví dụ: python ban_dong_thoi.py PHIEN01")
        sys.exit(1)

    ma_phien = sys.argv[1]
    url = "http://localhost:8000/api/dang-ky"
    num_requests = 40
    max_workers = 40

    print(f"🚀 Đang gửi {num_requests} request đồng thời cho phiên {ma_phien}...")

    # 2. Sử dụng httpx.Client trong context manager để dùng chung connection pool
    with httpx.Client(timeout=10.0) as client:
        # 3. Sử dụng ThreadPoolExecutor để gửi request song song
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Tạo danh sách các tác vụ gửi request
            futures = [
                executor.submit(send_request, client, url, ma_phien, i)
                for i in range(1, num_requests + 1)
            ]

            # Thu thập kết quả từ các luồng (threads)
            results = [f.result() for f in futures]

    # 4. Thống kê kết quả bằng Counter
    stats = Counter(results)

    print("\n" + "="*30)
    print(" KẾT QUẢ KIỂM THỬ ĐỒNG THỜI")
    print("="*30)

    # Sắp xếp kết quả theo mã status code tăng dần
    for code in sorted(stats.keys()):
        print(f"{code}: {stats[code]}")

    print("="*30)

    # 5. Đánh giá kết quả
    if stats[201] == 30 and stats[409] == 10:
        print("✅ KẾT LUẬN: HỆ THỐNG HOẠT ĐỘNG CHUẨN! (Đúng 30 chỗ)")
    elif stats[201] > 30:
        print(f"❌ KẾT LUẬN: THẤT BẠI! Hệ thống cho phép {stats[201]} người vào (Vượt quá 30)")
    else:
        print("⚠️ KẾT LUẬN: Kết quả không như mong đợi. Vui lòng kiểm tra lại.")

if __name__ == "__main__":
    main()
