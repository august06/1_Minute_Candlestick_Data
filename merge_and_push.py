import os
import sys
import glob
import subprocess
from datetime import datetime

# Đảm bảo mã hóa UTF-8 cho stdout/stderr trên Windows (tránh lỗi charmap crash khi chạy từ Node.js)
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

MASTER_CONFIGS = [
    {
        "symbol": "XAUUSD",
        "master_file": os.path.join(DIR_PATH, "XAUUSD_M1_RAW_MASTER.csv"),
        "prefixes": ("XAU", "GOLD"),
        "exclude": {
            "XAUUSD_M1_RAW_MASTER.csv",
            "XAUUSD_M1_DUKASCOPY_MASTER.csv",
            "BTCUSD_M1_RAW_MASTER.csv",
            "BTCUSD_M1_DUKASCOPY_MASTER.csv",
        }
    },
    {
        "symbol": "BTCUSD",
        "master_file": os.path.join(DIR_PATH, "BTCUSD_M1_RAW_MASTER.csv"),
        "prefixes": ("BTC",),
        "exclude": {
            "XAUUSD_M1_RAW_MASTER.csv",
            "XAUUSD_M1_DUKASCOPY_MASTER.csv",
            "BTCUSD_M1_RAW_MASTER.csv",
            "BTCUSD_M1_DUKASCOPY_MASTER.csv",
        }
    }
]


def merge_for_symbol(cfg, all_csv_files):
    symbol = cfg["symbol"]
    master_file = cfg["master_file"]
    prefixes = cfg["prefixes"]
    exclude_set = cfg["exclude"]

    if not os.path.exists(master_file):
        print(f"ℹ️ [{symbol}] Chưa có file Master: {master_file}, bỏ qua.")
        return 0, None

    existing_records = {}
    header = "Date,Time,Open,High,Low,Close,Volume"
    with open(master_file, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        if first_line:
            header = first_line
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split(",")
            if len(parts) >= 6:
                key = f"{parts[0].strip()}_{parts[1].strip()}"
                existing_records[key] = line_str

    count_before = len(existing_records)
    print(f"📊 [{symbol}] Số nến M1 hiện có trong Master: {count_before:,} nến")

    new_candles_added = 0
    for file_path in set(all_csv_files):
        base_name = os.path.basename(file_path)
        if base_name in exclude_set:
            continue
        upper_name = base_name.upper()
        if not any(upper_name.startswith(p) for p in prefixes):
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                f.readline()  # Bỏ qua header
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
        except Exception as e:
            print(f"⚠️ [{symbol}] Bỏ qua {base_name} do đang bị khóa: {e}")

    print(f"➕ [{symbol}] Đã phát hiện và ghép thêm: {new_candles_added:,} nến M1 mới!")
    total_candles = len(existing_records)
    print(f"📈 [{symbol}] Tổng số nến sau khi ghép: {total_candles:,} nến")

    sorted_keys = sorted(existing_records.keys())
    if new_candles_added > 0:
        with open(master_file, "w", encoding="utf-8") as f:
            f.write(header + "\n")
            for k in sorted_keys:
                f.write(existing_records[k] + "\n")
        print(f"💾 [{symbol}] Đã lưu thành công file Master: {master_file}")

    latest_candle = sorted_keys[-1] if sorted_keys else "now"
    return new_candles_added, latest_candle


def merge_and_push():
    print("=" * 65)
    print("🚀 BẮT ĐẦU QUY TRÌNH GHÉP NẾN M1 (XAUUSD & BTCUSD) & ĐỒNG BỘ GITHUB")
    print("=" * 65)

    parent_dir = os.path.dirname(DIR_PATH)
    all_csv_files = glob.glob(os.path.join(DIR_PATH, "*.csv")) + glob.glob(os.path.join(parent_dir, "*.csv"))

    total_added = 0
    updated_files = []
    summary_parts = []

    for cfg in MASTER_CONFIGS:
        added, latest = merge_for_symbol(cfg, all_csv_files)
        if added > 0:
            total_added += added
            updated_files.append(os.path.basename(cfg["master_file"]))
            summary_parts.append(f"{cfg['symbol']} +{added} (to {latest})")

    if total_added > 0 and updated_files:
        commit_msg = f"update: append {', '.join(summary_parts)} M1 candles"
        print(f"🌐 Đang đẩy lên GitHub (august06/1_Minute_Candlestick_Data)...")
        try:
            subprocess.run(["git", "-C", DIR_PATH, "add"] + updated_files, check=True)
            subprocess.run(["git", "-C", DIR_PATH, "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "-C", DIR_PATH, "push", "origin", "main"], check=True)
            print("✅ ĐÃ ĐẨY LÊN GITHUB THÀNH CÔNG!")
        except Exception as e:
            print("❌ Lỗi khi push git:", e)
    else:
        print("ℹ️ Dữ liệu XAUUSD & BTCUSD đã là mới nhất, không có nến mới nào cần push.")

    print("=" * 65)


if __name__ == "__main__":
    merge_and_push()
