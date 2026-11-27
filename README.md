# 1 Minute Candlestick Data (M1 Historical Vault — XAUUSD & BTCUSD)

Kho lưu trữ tập trung dữ liệu nến M1 (1-Minute) cho **Vàng (`XAUUSD`)** và **Bitcoin (`BTCUSD` - Chạy xuyên Thứ 7 & Chủ Nhật 24/7)** phục vụ ứng dụng Backtest và phân tích kỹ thuật.

## Cấu trúc dữ liệu
- **`XAUUSD_M1_RAW_MASTER.csv`**: File nến Master `XAUUSD` trích xuất từ Exness MT5 chứa dữ liệu lịch sử liên tục (tự động cập nhật mỗi khi có nến mới).
  - Cột dữ liệu: `Date,Time,Open,High,Low,Close,Volume`
- **`XAUUSD_M1_DUKASCOPY_MASTER.csv`**: File nến Master độc lập từ Dukascopy Swiss Bank (Giá BID) chứa toàn bộ lịch sử nến M1 `XAUUSD` xuyên suốt 2 năm **2025 - 2026** (~677.300+ nến M1).
  - Cột dữ liệu: `Date,Time,Open,High,Low,Close,Volume`
- **`BTCUSD_M1_RAW_MASTER.csv`**: File nến Master `BTCUSD` đồng bộ song song phục vụ đối chiếu và gộp nến MT5 Exness (`BTCUSD` / `BTCUSDm` / `BTCUSDc`).
  - Cột dữ liệu: `Date,Time,Open,High,Low,Close,Volume`
- **`BTCUSD_M1_DUKASCOPY_MASTER.csv`**: File nến Master độc lập từ Dukascopy Swiss Bank (Giá BID) chứa toàn bộ lịch sử nến M1 `BTCUSD` xuyên suốt 2 năm **2025 - 2026** (chạy 24/7 cả Thứ Bảy & Chủ Nhật, ~985.000+ nến M1).
  - Cột dữ liệu: `Date,Time,Open,High,Low,Close,Volume`
- **`merge_and_push.py`**: Script Python tự động quét file CSV nến mới từ MT5 cho cả `XAUUSD` và `BTCUSD`, gộp nến không trùng lặp vào file Master và đẩy lên GitHub.
- **`update_weekly_and_push.bat`**: Phím tắt 1-click kích hoạt tiến trình gộp và đẩy nến trên Windows.
