import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Hệ thống dự đoán & phát hiện bất thường giá nhà", layout="wide")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("model_pipeline.pkl")

model = load_model()

# Load scaler riêng cho phần phát hiện bất thường
@st.cache_resource
def load_scaler():
    # Giả sử đã lưu scaler từ quá trình train
    try:
        return joblib.load("scaler.pkl")
    except:
        # Tạo scaler mới nếu chưa có
        return MinMaxScaler()

scaler = load_scaler()

# Sidebar Menu
with st.sidebar:
    st.title("🏠 MENU")
    menu = st.radio(
        "Chọn chức năng:",
        ["Bài toán kinh doanh", "Đánh giá & Báo cáo", "Dự đoán giá nhà", "Phát hiện bất thường", "Team Info"]
    )

# Business Problem
if menu == "Bài toán kinh doanh":
    st.title("📊 Business Problem")
    st.write("""
    **Bài toán 1: Dự đoán giá nhà**
    - Xây dựng mô hình Machine Learning để dự đoán giá nhà tại TP.HCM
    - Giúp người mua/bán ước lượng giá trị bất động sản
    
    **Bài toán 2: Phát hiện bất thường**
    - Phát hiện các giao dịch bất thường (giá quá cao hoặc quá thấp)
    - Hỗ trợ phát hiện gian lận hoặc sai sót trong định giá
    """)

# Evaluation & Report
elif menu == "Đánh giá & Báo cáo":
    st.title("📈 Đánh giá & Báo cáo")
    
    st.subheader("1. Mô hình dự đoán giá nhà")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("R² Score (Test)", "0.83")
    with col2:
        st.metric("RMSE (log scale)", "0.129")
    with col3:
        st.metric("MAE (log scale)", "0.129")
    
    st.subheader("2. Phát hiện bất thường")
    st.write("""
    **Các phương pháp phát hiện bất thường:**
    - **Z-score:** Phát hiện 40 giao dịch bất thường (ngưỡng |z| > 3)
    - **Min-Max Rule:** Phát hiện 8273 giao dịch (giá/m² < 30 hoặc > 500 triệu)
    - **Percentile:** Phát hiện 1715 giao dịch (giá/m² ngoài P10-P90)
    - **Prediction Error:** Phát hiện 94 giao dịch (sai số dự đoán > 95th percentile)
    
    **Kết hợp các phương pháp (Anomaly Score):**
    - Score = 0.4×RF_Error + 0.2×Z-score + 0.2×MinMax + 0.2×Percentile
    - Ngưỡng bất thường: Score > 0.5
    - Phát hiện ~6.23% giao dịch bất thường
    """)

# Dự đoán giá nhà
elif menu == "Dự đoán giá nhà":
    st.title("🔮 Dự đoán giá nhà")
    st.markdown("### Nhập thông tin bất động sản")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            chieu_ngang = st.number_input("📏 Chiều rộng (m)", min_value=2.0, max_value=30.0, value=5.0, step=0.5)
            chieu_dai = st.number_input("📐 Chiều dài (m)", min_value=3.0, max_value=50.0, value=15.0, step=0.5)
            dien_tich = chieu_ngang * chieu_dai
            st.info(f"🏠 **Diện tích:** {dien_tich:.1f} m² (tự động = rộng × dài)")
            so_phong_ngu = st.slider("🛏️ Số phòng ngủ", min_value=1, max_value=8, value=3)
            
        with col2:
            so_phong_ve_sinh = st.slider("🚽 Số phòng vệ sinh", min_value=1, max_value=6, value=2)
            tong_tang = st.number_input("🏢 Số tầng", min_value=1, max_value=10, value=2)
        
        col3, col4 = st.columns(2)
        
        with col3:
            loai_hinh = st.selectbox("Loại hình", ["Nhà riêng", "Căn hộ", "Đất nền"])
            phap_ly = st.selectbox("Pháp lý", ["Sổ hồng", "Sổ đỏ", "Đang hoàn thiện"])
            noi_that = st.selectbox("Nội thất", ["Đầy đủ", "Cơ bản", "Chưa có"])
            
        with col4:
            dac_diem = st.selectbox("Đặc điểm", ["Mặt tiền", "Hẻm xe hơi", "Hẻm nhỏ"])
            quan = st.selectbox("Quận", ["Quận Gò Vấp", "Quận Phú Nhuận", "Quận Bình Thạnh"])
        
        # Map giá trị
        loai_hinh_map = {"Nhà riêng": 0, "Căn hộ": 1, "Đất nền": 2}
        phap_ly_map = {"Sổ hồng": 5, "Sổ đỏ": 4, "Đang hoàn thiện": 2}
        noi_that_map = {"Đầy đủ": 1, "Cơ bản": 2, "Chưa có": 3}
        dac_diem_map = {"Mặt tiền": 7, "Hẻm xe hơi": 6, "Hẻm nhỏ": 2}
        quan_map = {"Quận Gò Vấp": 1, "Quận Phú Nhuận": 2, "Quận Bình Thạnh": 0}
        
        submitted = st.form_submit_button("🔍 Dự đoán giá", type="primary")
    
    if submitted:
        input_data = pd.DataFrame([{
            "dien_tich": dien_tich,
            "loai_hinh": loai_hinh_map[loai_hinh],
            "giay_to_phap_ly": phap_ly_map[phap_ly],
            "so_phong_ngu": so_phong_ngu,
            "so_phong_ve_sinh": so_phong_ve_sinh,
            "tong_so_tang": tong_tang,
            "tinh_trang_noi_that": noi_that_map[noi_that],
            "dac_diem": dac_diem_map[dac_diem],
            "chieu_ngang": chieu_ngang,
            "chieu_dai": chieu_dai,
            "e_Quận Gò Vấp": 1 if quan_map[quan] == 1 else 0,
            "e_Quận Phú Nhuận": 1 if quan_map[quan] == 2 else 0
        }])
        
        try:
            pred_log = model.predict(input_data)[0]
            pred_price_billion = np.expm1(pred_log)
            
            st.success("### 📊 Kết quả dự đoán")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("💰 Giá dự đoán", f"{pred_price_billion:.2f} tỷ đồng")
            with col_b:
                st.metric("📐 Giá/m²", f"{pred_price_billion/dien_tich:.2f} tỷ/m²")
        
            
            st.info(f"""
            **Thông tin chi tiết:**
            - Diện tích: {dien_tich:.1f}m²
            - Kích thước: {chieu_ngang:.1f}m x {chieu_dai:.1f}m
            - Vị trí: {quan}
            - Loại hình: {loai_hinh}
            - Pháp lý: {phap_ly}
            """)
            
        except Exception as e:
            st.error(f"⚠️ Lỗi dự đoán: {e}")

# Phát hiện bất thường
elif menu == "Phát hiện bất thường":
    st.title("⚠️ Phát hiện giao dịch bất thường")
    st.markdown("""
    ### Kiểm tra tính bất thường của giao dịch
    Hệ thống sẽ phân tích và đánh giá xem mức giá bạn nhập có bất thường hay không
    dựa trên 4 phương pháp phát hiện khác nhau.
    """)
    
    # Form nhập liệu đơn giản
    with st.form("anomaly_form"):
        st.subheader("📋 Thông tin bất động sản")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dien_tich = st.number_input(
                "🏠 Diện tích (m²)", 
                min_value=10.0, 
                max_value=500.0, 
                value=75.0, 
                step=5.0,
                help="Diện tích đất/sàn xây dựng"
            )
            
            gia_ban = st.number_input(
                "💰 Giá bán (tỷ đồng)", 
                min_value=0.5, 
                max_value=500.0, 
                value=7.0, 
                step=0.5,
                help="Nhập giá bán của bất động sản"
            )
            
        with col2:
            loai_hinh = st.selectbox(
                "🏢 Loại hình",
                ["Nhà riêng", "Căn hộ", "Đất nền"],
                help="Loại hình bất động sản"
            )
            
            quan = st.selectbox(
                "📍 Quận/Huyện",
                ["Quận Gò Vấp", "Quận Phú Nhuận", "Quận Bình Thạnh"],
                help="Vị trí bất động sản"
            )
            
        with col3:
            dac_diem = st.selectbox(
                "📍 Đặc điểm vị trí",
                ["Mặt tiền", "Hẻm xe hơi", "Hẻm nhỏ"],
                help="Đặc điểm về vị trí và đường xá"
            )
            
            so_phong_ngu = st.number_input(
                "🛏️ Số phòng ngủ",
                min_value=1,
                max_value=10,
                value=3,
                step=1
            )
        
        # Map giá trị cho model
        loai_hinh_map = {"Nhà riêng": 0, "Căn hộ": 1, "Đất nền": 2}
        quan_map = {
            "Quận Gò Vấp": 0, 
            "Quận Phú Nhuận": 1, 
            "Quận Bình Thạnh": 2, 
        }
        dac_diem_map = {"Mặt tiền": 7, "Hẻm xe hơi": 6, "Hẻm nhỏ": 2}
        
        # Thêm thông số mặc định cho các trường không nhập
        col4, col5, col6 = st.columns(3)
        with col4:
            st.caption("📐 Kích thước (ước lượng)")
            chieu_ngang = st.number_input("Chiều rộng (m)", min_value=2.0, max_value=30.0, value=5.0, step=0.5, key="anom_width")
            chieu_dai = st.number_input("Chiều dài (m)", min_value=3.0, max_value=50.0, value=15.0, step=0.5, key="anom_length")
        
        with col5:
            st.caption("🏠 Kết cấu (ước lượng)")
            tong_tang = st.number_input("Số tầng", min_value=1, max_value=10, value=2, key="anom_floor")
            so_phong_ve_sinh = st.number_input("Số phòng vệ sinh", min_value=1, max_value=6, value=2, key="anom_bath")
        
        with col6:
            st.caption("📄 Pháp lý")
            phap_ly = st.selectbox(
                "Giấy tờ pháp lý",
                ["Sổ hồng", "Sổ đỏ", "Đang hoàn thiện"],
                key="anom_legal"
            )
        
        submitted = st.form_submit_button("🔍 Kiểm tra tính bất thường", type="primary")
    
    if submitted:
        # Map giá trị
        loai_hinh_map = {"Nhà riêng": 0, "Căn hộ": 1, "Đất nền": 2}
        phap_ly_map = {"Sổ hồng": 5, "Sổ đỏ": 4, "Đang hoàn thiện": 2}
        quan_map = {
            "Quận Gò Vấp": 0, 
            "Quận Phú Nhuận": 1, 
            "Quận Bình Thạnh": 2, 
        }
        
        # Tính giá/m²
        price_m2 = gia_ban / dien_tich
        
        # 1. Z-score (dựa trên phân phối giá từ dữ liệu gốc)
        mean_price = 6.5  # trung bình giá từ dữ liệu (tỷ)
        std_price = 9.95  # độ lệch chuẩn
        z_score = abs(gia_ban - mean_price) / std_price
        anomaly_zscore = z_score > 3
        
        # 2. Min-Max Rule (giá/m² ngoài khoảng 30-500 triệu)
        anomaly_minmax = (price_m2 < 0.03) or (price_m2 > 0.5)
        
        # 3. Percentile (P10=80 triệu, P90=250 triệu)
        p10, p90 = 0.08, 0.25
        anomaly_percentile = (price_m2 < p10) or (price_m2 > p90)
        
        # 4. Dự đoán bằng model
        input_data = pd.DataFrame([{
            "dien_tich": dien_tich,
            "loai_hinh": loai_hinh_map[loai_hinh],
            "giay_to_phap_ly": phap_ly_map[phap_ly],
            "so_phong_ngu": so_phong_ngu,
            "so_phong_ve_sinh": so_phong_ve_sinh,
            "tong_so_tang": tong_tang,
            "tinh_trang_noi_that": 2,  # mặc định
            "dac_diem": dac_diem_map[dac_diem],
            "chieu_ngang": chieu_ngang,
            "chieu_dai": chieu_dai,
            "e_Quận Gò Vấp": 1 if quan_map[quan] == 1 else 0,
            "e_Quận Phú Nhuận": 1 if quan_map[quan] == 2 else 0
        }])
        
        try:
            pred_log = model.predict(input_data)[0]
            pred_price = np.expm1(pred_log)
            error = abs(gia_ban - pred_price)
            
            # Ngưỡng sai số (95th percentile từ dữ liệu)
            error_threshold = 0.387
            anomaly_rf = error > error_threshold
            
            # Tính anomaly score
            anomaly_score = (0.4 * anomaly_rf + 
                           0.2 * anomaly_zscore + 
                           0.2 * anomaly_minmax + 
                           0.2 * anomaly_percentile)
            
            # Hiển thị kết quả
            st.markdown("---")
            st.subheader("📊 Kết quả phân tích")
            
            # Kết luận
            if anomaly_score >= 0.5:
                st.error("🚨 **KẾT LUẬN: GIAO DỊCH BẤT THƯỜNG** 🚨")
                st.warning(f"Điểm bất thường: {anomaly_score:.2f} / 1.00 (ngưỡng: ≥ 0.5)")
            else:
                st.success("✅ **KẾT LUẬN: GIAO DỊCH BÌNH THƯỜNG** ✅")
                st.info(f"Điểm bất thường: {anomaly_score:.2f} / 1.00 (ngưỡng: ≥ 0.5)")
            
            # Chi tiết phân tích
            st.markdown("---")
            st.subheader("🔬 Phân tích chi tiết")
            
            # Tạo 2 cột cho kết quả
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("**📐 Thông số cơ bản**")
                st.metric("Giá/m²", f"{price_m2:.2f} tỷ/m²")
                st.metric("Giá dự đoán", f"{pred_price:.2f} tỷ", 
                         delta=f"{gia_ban - pred_price:+.2f} tỷ so với thực tế")
                
            with col_right:
                st.markdown("**⚠️ Phát hiện bất thường theo từng phương pháp**")
                
                # Hiển thị từng phương pháp với màu sắc
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    if anomaly_zscore:
                        st.error("❌ Z-score: Bất thường")
                    else:
                        st.success("✅ Z-score: Bình thường")
                    
                    if anomaly_minmax:
                        st.error("❌ Min-Max: Bất thường")
                    else:
                        st.success("✅ Min-Max: Bình thường")
                        
                with col_r2:
                    if anomaly_percentile:
                        st.error("❌ Percentile: Bất thường")
                    else:
                        st.success("✅ Percentile: Bình thường")
                    
                    if anomaly_rf:
                        st.error("❌ Sai số dự đoán: Bất thường")
                    else:
                        st.success("✅ Sai số dự đoán: Bình thường")
            
            # Hiển thị biểu đồ so sánh đơn giản
            st.markdown("---")
            st.subheader("📈 So sánh với thị trường")
            
            # Tạo thanh tiến trình cho giá
            price_range = min(gia_ban / 20, 1.0)  # giá tối đa 20 tỷ cho thanh
            st.write(f"**Giá nhập: {gia_ban:.2f} tỷ**")
            st.progress(price_range)
            
            # So sánh với giá dự đoán
            col_comp1, col_comp2, col_comp3 = st.columns(3)
            with col_comp1:
                st.metric("Giá thực tế", f"{gia_ban:.2f} tỷ")
            with col_comp2:
                st.metric("Giá dự đoán", f"{pred_price:.2f} tỷ")
            with col_comp3:
                diff_percent = ((gia_ban - pred_price) / pred_price) * 100
                st.metric("Chênh lệch", f"{diff_percent:+.1f}%")
            
            # Giải thích chi tiết
            st.markdown("---")
            st.subheader("💡 Giải thích kết quả")
            
            reasons = []
            if anomaly_zscore:
                reasons.append(f"• **Z-score = {z_score:.2f}** > 3: Giá bán quá cao hoặc quá thấp so với giá trung bình của thị trường (trung bình {mean_price:.1f} tỷ)")
            if anomaly_minmax:
                reasons.append(f"• **Giá/m² = {price_m2:.2f} tỷ/m²** nằm ngoài khoảng 0.03-0.5 tỷ/m² (30-500 triệu/m²) - đây là khoảng giá phổ biến")
            if anomaly_percentile:
                reasons.append(f"• **Giá/m² = {price_m2:.2f} tỷ/m²** nằm ngoài khoảng phân vị 10-90 của thị trường ({p10:.2f}-{p90:.2f} tỷ/m²)")
            if anomaly_rf:
                reasons.append(f"• **Sai số dự đoán = {error:.2f} tỷ** > {error_threshold:.3f} tỷ (ngưỡng 95%): Mô hình không thể dự đoán chính xác giá này")
            
            if reasons:
                for reason in reasons:
                    st.write(reason)
            else:
                st.write("✅ Tất cả các chỉ số đều nằm trong ngưỡng bình thường. Giao dịch này được đánh giá là hợp lý.")
            
            # Cảnh báo thêm nếu điểm bất thường cao
            if anomaly_score >= 0.7:
                st.warning("⚠️ **Khuyến nghị:** Nên thẩm định kỹ giao dịch này vì có nhiều dấu hiệu bất thường!")
            elif anomaly_score >= 0.5:
                st.info("ℹ️ **Khuyến nghị:** Giao dịch có dấu hiệu bất thường, nên xem xét kỹ các yếu tố.")
            
        except Exception as e:
            st.error(f"⚠️ Lỗi phân tích: {e}")
            st.info("Vui lòng kiểm tra lại thông tin đã nhập")

# Team Info
else:
    st.title("👥 Thông tin nhóm")
    
    st.write("""
    ### Thành viên thực hiện:
    1. **[Huỳnh Lê Xuân Ánh]** - [Vai trò: Xử lý dữ liệu, xây dựng models ML thường (Python) ]
    2. **[Nguyễn Thị Tuyết Vân]** - [Vai trò: Xây dựng models trong môi trường Pyspark]
    3. **[Đặng Đức Duy]** - [Vai trò: Phát hiện giá bất thường, Báo cáo]
    
    ### Phân công công việc:
    - **Giai đoạn 1:** Thu thập và làm sạch dữ liệu 
    - **Giai đoạn 2:** Phân tích và khám phá dữ liệu 
    - **Giai đoạn 3:** Xây dựng và tối ưu mô hình 
    - **Giai đoạn 4:** Triển khai ứng dụng và báo cáo 
    
    ### Công nghệ sử dụng:
    - Python, Scikit-learn, Pandas, NumPy
    - Random Forest Regressor
    - PySpark (xử lý dữ liệu lớn)
    - Streamlit cho giao diện
    
    ### Môn học: Machine Learning

    """)
