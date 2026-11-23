# 1 Minute Candlestick Data (M1 Historical Vault)

Kho lưu trữ tập trung dữ liệu nến M1 (1-Minute) trích xuất từ MetaTrader 5 để phục vụ ứng dụng Backtest và phân tích kỹ thuật.

## Cấu trúc dữ liệu
- **`XAUUSD_M1_RAW_MASTER.csv`**: File nến Master trích xuất từ Exness MT5 chứa dữ liệu lịch sử liên tục (tự động cập nhật mỗi khi có nến mới).
  - Cột dữ liệu: `Date,Time,Open,High,Low,Close,Volume`
- **`XAUUSD_M1_DUKASCOPY_MASTER.csv`**: File nến Master độc lập từ Dukascopy Swiss Bank (Giá BID) chứa toàn bộ lịch sử nến M1 XAUUSD xuyên suốt 2 năm **2025 - 2026** (~670.910 nến M1).
  - Cột dữ liệu: `Date,Time,Open,High,Low,Close,Volume`
- **`merge_and_push.py`**: Script Python tự động quét file CSV nến mới từ MT5, gộp nến không trùng lặp vào file Master Exness và đẩy lên GitHub.
- **`update_weekly_and_push.bat`**: Phím tắt 1-click kích hoạt tiến trình gộp và đẩy nến trên Windows.
