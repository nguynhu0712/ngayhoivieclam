import React, { useState } from 'react';

function App() {
  const [formData, setFormData] = useState({ ma_sv: '', ma_phien: '' });
  const [message, setMessage] = useState({ text: '', type: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ text: 'Đang xử lý...', type: 'info' });
    try {
      const response = await fetch('http://localhost:8000/api/dang-ky', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      // Xử lý phản hồi chi tiết theo yêu cầu chấm điểm
      if (response.status === 201) {
        setMessage({ text: '✅ Đăng ký thành công!', type: 'success' });
        setFormData({ ma_sv: '', ma_phien: '' });
      } else if (response.status === 409) {
        const result = await response.json();
        setMessage({ text: `❌ ${result.detail}`, type: 'error' });
      } else if (response.status === 422) {
        setMessage({ text: '⚠️ Lỗi nhập liệu: Vui lòng điền đầy đủ và chính xác Mã SV, Mã phiên!', type: 'warning' });
      } else {
        setMessage({ text: '❌ Có lỗi hệ thống xảy ra, vui lòng thử lại sau!', type: 'error' });
      }
    } catch (error) {
      setMessage({ text: '❌ Lỗi kết nối Server! Hãy chạy python main.py', type: 'error' });
    }
  };

  const styles = {
    container: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', fontFamily: 'Arial, sans-serif', backgroundColor: '#f0f2f5' },
    card: { backgroundColor: 'white', padding: '40px', borderRadius: '15px', boxShadow: '0 8px 24px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px', textAlign: 'center' },
    title: { color: '#1a73e8', marginBottom: '30px', fontSize: '22px', fontWeight: 'bold', textTransform: 'uppercase' },
    inputGroup: { marginBottom: '20px', textAlign: 'left' },
    label: { display: 'block', marginBottom: '8px', fontWeight: '500', color: '#555' },
    input: { width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #ddd', boxSizing: 'border-box', fontSize: '16px' },
    button: { width: '100%', padding: '14px', backgroundColor: '#1a73e8', color: 'white', border: 'none', borderRadius: '8px', fontSize: '16px', cursor: 'pointer', fontWeight: 'bold', marginTop: '10px' },
    message: { marginTop: '20px', padding: '12px', borderRadius: '8px', fontWeight: '500', fontSize: '14px' },
    success: { backgroundColor: '#d4edda', color: '#155724', border: '1px solid #c3e6cb' },
    error: { backgroundColor: '#f8d7da', color: '#721c24', border: '1px solid #f5c6cb' },
    warning: { backgroundColor: '#fff3cd', color: '#856404', border: '1px solid #ffeeba' },
    info: { backgroundColor: '#e2e3e5', color: '#383d41', border: '1px solid #d6d8db' },
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.title}>CỔNG ĐĂNG KÝ NGÀY HỘI VIỆC LÀM</div>
        <form onSubmit={handleSubmit}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Mã sinh viên:</label>
            <input style={styles.input} type="text" name="ma_sv" placeholder="Ví dụ: SV001" value={formData.ma_sv} onChange={handleChange} required />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Mã phiên:</label>
            <input style={styles.input} type="text" name="ma_phien" placeholder="Ví dụ: PHIEN01" value={formData.ma_phien} onChange={handleChange} required />
          </div>
          <button type="submit" style={styles.button}>Đăng ký tham gia</button>
        </form>
        {message.text && <div style={{ ...styles.message, ...styles[message.type] }}>{message.text}</div>}
      </div>
    </div>
  );
}
export default App;
