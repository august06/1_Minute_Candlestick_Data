import os
import glob
import subprocess
from datetime import datetime

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
MASTER_FILE = os.path.join(DIR_PATH, "XAUUSD_M1_RAW_MASTER.csv")

def merge_and_push():
    print("=" * 65)
    print("🚀 BẮT ĐẦU QUY TRÌNH GHÉP NẾN M1 & ĐỒNG BỘ LÊN GITHUB")
    print("=" * 65)

    if not os.path.exists(MASTER_FILE):
        print("❌ Không tìm thấy file Master:", MASTER_FILE)
        return

    # 1. Đọc dữ liệu Master hiện có
    existing_records = {}
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        header = f.readline().strip()
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split(",")
            if len(parts) >= 6:
                key = f"{parts[0].strip()}_{parts[1].strip()}" # Date_Time
                existing_records[key] = line_str

    count_before = len(existing_records)
    print(f"📊 Số nến M1 hiện có trong Master: {count_before:,} nến")

    # 2. Quét tất cả các file CSV khác trong thư mục để tìm nến mới ghép vào
    csv_files = glob.glob(os.path.join(DIR_PATH, "*.csv"))
    new_candles_added = 0

    for file_path in csv_files:
        if os.path.basename(file_path) == "XAUUSD_M1_RAW_MASTER.csv":
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            f.readline() # Bỏ qua header
            for line in f:
                line_str = line.strip()
                if not line_str:
                    continue
                parts = line_str.split(",")
                if len(parts) >= 6:
                    key = f"{parts[0].strip()}_{parts[1].strip()}"
                    if key not in existing_records:
                        existing_records[key] = line_str
                        new_candles_added += 1

    print(f"➕ Đã phát hiện và ghép thêm: {new_candles_added:,} nến M1 mới!")
    total_candles = len(existing_records)
    print(f"📈 Tổng số nến sau khi ghép: {total_candles:,} nến")

    # 3. Sắp xếp lại toàn bộ theo trình tự thời gian (Date, Time)
    sorted_keys = sorted(existing_records.keys())

    # 4. Ghi đè lại file Master chuẩn
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for k in sorted_keys:
            f.write(existing_records[k] + "\n")

    print(f"💾 Đã lưu thành công file Master: {MASTER_FILE}")

    # 5. Tự động Git commit & Push lên GitHub
    if new_candles_added > 0:
        latest_candle = sorted_keys[-1] if sorted_keys else "now"
        commit_msg = f"update: append {new_candles_added} new M1 candles up to {latest_candle}"
        print(f"🌐 Đang đẩy lên GitHub (august06/1_Minute_Candlestick_Data)...")
        try:
            subprocess.run(["git", "-C", DIR_PATH, "add", "XAUUSD_M1_RAW_MASTER.csv"], check=True)
            subprocess.run(["git", "-C", DIR_PATH, "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "-C", DIR_PATH, "push", "origin", "main"], check=True)
            print("✅ ĐÃ ĐẨY LÊN GITHUB THÀNH CÔNG!")
        except Exception as e:
            print("❌ Lỗi khi push git:", e)
    else:
        print("ℹ️ Dữ liệu đã là mới nhất, không có nến mới nào cần push.")

    print("=" * 65)

if __name__ == "__main__":
    merge_and_push()
