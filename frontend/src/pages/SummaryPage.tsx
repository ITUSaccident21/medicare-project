import React from 'react';

export const SummaryPage: React.FC = () => {
  return (
    <div className="summary-page">
      <h2>M5 - Phiếu Tổng Hợp Tiền Khám & Mã QR Bác Sĩ</h2>
      <p>Một trang tóm tắt ngắn gọn toàn bộ tiền sử, đơn thuốc và cảnh báo tương tác để bác sĩ quét mã QR kiểm tra nhanh.</p>
      <div className="qr-placeholder">
        <div style={{ width: 160, height: 160, border: '2px dashed #0284c7', margin: '20px auto', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          MÃ QR Y TẾ
        </div>
      </div>
    </div>
  );
};

export default SummaryPage;
