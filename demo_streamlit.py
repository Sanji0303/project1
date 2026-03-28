import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cấu hình trang
st.set_page_config(page_title="Dự đoán giá nhà", layout="wide")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("model_pipeline.pkl")

model = load_model()

# Sidebar Menu
with st.sidebar:
    st.title("🏠 MENU")
    menu = st.radio(
        "Chọn mục:",
        ["Business Problem", "Evaluation & Report", "New Prediction", "Team Info"]
    )

# Business Problem
if menu == "Business Problem":
    st.title("📊 Business Problem")
    st.write("""
    **Bài toán:** Dự đoán giá nhà dựa trên các đặc điểm bất động sản.
    
    **Mục tiêu:** Xây dựng mô hình học máy giúp ước lượng giá nhà chính xác, hỗ trợ người mua và người bán trong việc định giá.
    
    **Phương pháp:** Sử dụng Random Forest Regressor với dữ liệu đã được tiền xử lý.
    """)

# Evaluation & Report
elif menu == "Evaluation & Report":
    st.title("📈 Evaluation & Report")
    st.write("""
    **Kết quả mô hình Random Forest (tối ưu):**
    
    - **R² Score:** 0.83 (Test)
    - **RMSE:** 0.129 (Test - log scale)
    - **MAE:** 0.129 (Test - log scale)
    
    **Nhận xét:**
    - Mô hình giải thích được 83% phương sai của giá nhà.
    - Sai số MAE ~0.129 (log) tương đương khoảng 13.7% sai số trung bình trên giá gốc.
    - Có dấu hiệu overfitting nhẹ (train R²=0.97) nhưng vẫn chấp nhận được.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("R² Score", "0.83")
        st.metric("RMSE (log)", "0.129")
    with col2:
        st.metric("MAE (log)", "0.129")
        st.metric("Sai số trung bình", "~13.7%")

# New Prediction
elif menu == "New Prediction":
    st.title("🔮 Dự đoán giá nhà mới")
    st.write("Nhập thông tin bất động sản để dự đoán giá:")
    
    # Form nhập liệu
    col1, col2 = st.columns(2)
    
    with col1:
        dien_tich = st.number_input("📐 Diện tích (m²)", min_value=10.0, max_value=500.0, value=75.0)
        chieu_dai = st.number_input("📏 Chiều dài (m)", min_value=3.0, max_value=30.0, value=10.0)
        so_phong_ngu = st.number_input("🛏️ Số phòng ngủ", min_value=1, max_value=10, value=3)
        
    with col2:
        chieu_ngang = st.number_input("📐 Chiều rộng (m)", min_value=2.0, max_value=20.0, value=7.5)
        loai_hinh = st.selectbox("🏢 Loại hình", options=[("Nhà riêng", 0), ("Căn hộ", 1), ("Đất", 2)], format_func=lambda x: x[0])
        tinh_trang = st.selectbox("✨ Nội thất", options=[("Đầy đủ", 1), ("Cơ bản", 2), ("Chưa có", 3)], format_func=lambda x: x[0])
    
    giay_to = st.selectbox("📄 Giấy tờ pháp lý", options=[("Sổ hồng", 5), ("Sổ đỏ", 4), ("Đang hoàn thiện", 2)], format_func=lambda x: x[0])
    dac_diem = st.selectbox("📍 Đặc điểm", options=[("Mặt tiền", 7), ("Hẻm xe hơi", 6), ("Hẻm nhỏ", 2)], format_func=lambda x: x[0])
    quan = st.selectbox("📍 Quận", options=[("Quận Gò Vấp", 1), ("Quận Phú Nhuận", 2), ("Quận khác", 0)], format_func=lambda x: x[0])
    
    input_data = pd.DataFrame({
        "dien_tich": [dien_tich],
        "loai_hinh": [loai_hinh[1]],
        "giay_to_phap_ly": [giay_to[1]],
        "so_phong_ngu": [so_phong_ngu],
        "so_phong_ve_sinh": [min(so_phong_ngu, 4)],
        "tong_so_tang": [2],
        "tinh_trang_noi_that": [tinh_trang[1]],
        "dac_diem": [dac_diem[1]],
        "chieu_ngang": [chieu_ngang],
        "chieu_dai": [chieu_dai],
        "e_Quận Gò Vấp": [1 if quan[1] == 1 else 0],
        "e_Quận Phú Nhuận": [1 if quan[1] == 2 else 0]
    })
    
    if st.button("🔍 Dự đoán giá", type="primary"):
        try:
            pred_log = model.predict(input_data)[0]
            pred_price = np.expm1(pred_log)  # kết quả là tỷ đồng
            
            # Hiển thị đúng đơn vị
            st.success(f"""
            💰 **Giá dự đoán: {pred_price:,.2f} tỷ đồng**
            (≈ {pred_price * 1000:,.0f} triệu đồng)
            """)
            
            # Thêm so sánh
            st.info(f"📊 Với diện tích {dien_tich}m², giá trung bình khoảng {pred_price/dien_tich:.2f} tỷ/m²")
            
        except Exception as e:
            st.error(f"Lỗi dự đoán: {e}")
            st.info("⚠️ Lưu ý: Model cần được train với pipeline có scaler")
    # Dự đoán
    if st.button("🔍 Dự đoán giá", type="primary"):
        try:
            # Lưu ý: model đã được train với scaled data nên cần scale
            # Vì pipeline chỉ chứa model (không scaler), cần scale thủ công
            # Cách đơn giản: load scaler riêng hoặc train lại pipeline có scaler
            # Ở đây giả định đã có scaler từ file model_pipeline.pkl là pipeline đầy đủ
            
            # Nếu model_pipeline.pkl là pipeline đã có scaler
            pred_log = model.predict(input_data)[0]
            pred_price = np.expm1(pred_log)
            
            st.success(f"💰 **Giá dự đoán: {pred_price:,.0f} triệu đồng** (≈ {pred_price/1000:.2f} tỷ)")
            
        except Exception as e:
            st.error(f"Lỗi dự đoán: {e}")
            st.info("Lưu ý: Đảm bảo model đã được train với pipeline đầy đủ (scaler + model)")

# Team Info
else:
    st.title("👥 Team Info")
    st.write("""
    **Nhóm thực hiện:** 
    - Nguyễn Thị Tuyết Vân
    - [Thành viên 2]
    - [Thành viên 3]
    
    **Phân công công việc:**
    - **Vân:** Xử lý dữ liệu, xây dựng mô hình, tối ưu tham số
    - **[Tên]:** Phân tích EDA, trực quan hóa dữ liệu
    - **[Tên]:** Xây dựng GUI, viết báo cáo
    
    **Môn học:** Machine Learning
    
    **Ngày:** 27/03/2026
    """)