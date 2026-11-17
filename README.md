# 1 Minute Candlestick Data (M1 Historical Vault)

Kho lưu trữ tập trung dữ liệu nến M1 (1-Minute) trích xuất từ MetaTrader 5 để phục vụ ứng dụng Backtest và phân tích kỹ thuật.

## Cấu trúc dữ liệu
- **`XAUUSD_M1_RAW_MASTER.csv`**: File nến Master duy nhất chứa toàn bộ dữ liệu lịch sử liên tục từ 2026 đến nay (tự động cập nhật mỗi khi có nến mới).
  - Cột dữ liệu: `Date,Time,Open,High,Low,Close,Volume`
- **`merge_and_push.py`**: Script Python tự động quét file CSV nến mới từ MT5, gộp nến không trùng lặp vào file Master và đẩy lên GitHub.
- **`update_weekly_and_push.bat`**: Phím tắt 1-click kích hoạt tiến trình gộp và đẩy nến trên Windows.
