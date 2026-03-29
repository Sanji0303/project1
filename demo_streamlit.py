import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Hệ thống Thẩm định & Đánh giá rủi ro Bất động sản", layout="wide")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("model_pipeline.pkl")

model = load_model()

# Load scaler riêng cho phần phát hiện bất thường
@st.cache_resource
def load_scaler():
    try:
        return joblib.load("scaler.pkl")
    except:
        return MinMaxScaler()

scaler = load_scaler()

# Sidebar Menu
with st.sidebar:
    st.title("🏠 DANH MỤC DỊCH VỤ")
    menu = st.radio(
        "Vui lòng chọn tính năng:",
        ["🌟 Giới thiệu hệ thống", "📊 Độ tin cậy của AI", "🔮 Định giá Bất động sản", "⚠️ Kiểm tra rủi ro giá"]
    )
    
    # Đưa thông tin nhóm xuống cố định ở Sidebar
    st.markdown("---")
    st.subheader("👥 Đội ngũ phát triển")
    st.markdown("""
    **1. Huỳnh Lê Xuân Ánh**  
    *Kỹ sư Dữ liệu & Phát triển AI*
    
    **2. Nguyễn Thị Tuyết Vân**  
    *Chuyên gia Xử lý Dữ liệu lớn*
    
    **3. Đặng Đức Duy**  
    *Chuyên gia Phân tích Rủi ro*
    
    ---
    *Gmail: projectnhom7@gmail.com*
    """)

# Giới thiệu hệ thống
if menu == "🌟 Giới thiệu hệ thống":
    st.title("🌟 Hệ thống Thẩm định & Đánh giá rủi ro Bất động sản")
    st.write("""
    Chào mừng bạn đến với hệ thống ứng dụng Trí tuệ nhân tạo (AI) trong lĩnh vực Bất động sản tại TP.HCM. 
    Hệ thống được thiết kế để mang lại sự minh bạch và an tâm cho các quyết định đầu tư của bạn.
    
    **🎯 Các tính năng chính của chúng tôi:**
    
    **1. Định giá Bất động sản thông minh**
    - Ứng dụng AI để phân tích hàng ngàn giao dịch trên thị trường.
    - Giúp người mua/bán ước lượng chính xác giá trị thực của căn nhà dựa trên diện tích, vị trí, tiện ích...
    - Hỗ trợ thương lượng giá cả hợp lý, tránh mua hớ hoặc bán hớ.
    
    **2. Kiểm tra rủi ro & Cảnh báo giá bất thường**
    - Tự động đối chiếu mức giá bạn đang quan tâm với mặt bằng chung của thị trường.
    - Cảnh báo ngay lập tức nếu phát hiện mức giá "quá rẻ" (nguy cơ lừa đảo, vướng pháp lý) hoặc "quá đắt" (bị thổi giá).
    - Bảo vệ tài sản và quyết định đầu tư của bạn.
    """)

# Độ tin cậy
elif menu == "📊 Độ tin cậy của AI":
    st.title("📊 Độ tin cậy & Năng lực của Hệ thống")
    st.write("Hệ thống của chúng tôi được huấn luyện trên dữ liệu thực tế tại TP.HCM, trải qua quá trình kiểm định nghiêm ngặt để đảm bảo độ chính xác cao nhất cho khách hàng.")
    
    st.subheader("1. Năng lực Định giá")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Độ chính xác tổng thể", "83%")
    with col2:
        st.metric("Khả năng bám sát thị trường", "Rất cao")
    with col3:
        st.metric("Tốc độ xử lý", "< 1 giây")
    
    st.subheader("2. Hệ thống Cảnh báo Rủi ro Đa lớp")
    st.write("""
    Để xác định một mức giá có an toàn hay không, AI của chúng tôi không chỉ nhìn vào một con số, mà thực hiện **kiểm tra chéo qua 4 lớp bảo mật**:
    
    - 🛡️ **Lớp 1 - So sánh mặt bằng chung:** Đối chiếu giá trị căn nhà với mức giá trung bình của toàn khu vực.
    - 🛡️ **Lớp 2 - Kiểm tra khung giá chuẩn:** Đảm bảo đơn giá (triệu/m²) nằm trong giới hạn giao dịch hợp lý của thị trường hiện tại.
    - 🛡️ **Lớp 3 - Phân tích phân khúc:** Đánh giá xem mức giá này có thuộc nhóm "cực hiếm" (những giao dịch có dấu hiệu làm giá) hay không.
    - 🛡️ **Lớp 4 - Thẩm định bằng AI:** Trí tuệ nhân tạo sẽ tự tính toán một mức giá hợp lý dựa trên đặc điểm căn nhà, sau đó so sánh với mức giá đang giao dịch để tìm ra sự chênh lệch bất hợp lý.
    
    *Chỉ khi vượt qua được các bài kiểm tra này, giao dịch mới được hệ thống đánh giá là an toàn.*
    """)

# Định giá Bất động sản
elif menu == "🔮 Định giá Bất động sản":
    st.title("🔮 Định giá Bất động sản")
    st.markdown("### Nhập thông tin căn nhà bạn muốn định giá")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            chieu_ngang = st.number_input("📏 Chiều rộng (m)", min_value=2.0, max_value=30.0, value=5.0, step=0.5)
            chieu_dai = st.number_input("📐 Chiều dài (m)", min_value=3.0, max_value=50.0, value=15.0, step=0.5)
            dien_tich = chieu_ngang * chieu_dai
            st.info(f"🏠 **Diện tích sử dụng:** {dien_tich:.1f} m²")
            so_phong_ngu = st.slider("🛏️ Số phòng ngủ", min_value=1, max_value=8, value=3)
            
        with col2:
            so_phong_ve_sinh = st.slider("🚽 Số phòng vệ sinh", min_value=1, max_value=6, value=2)
            tong_tang = st.number_input("🏢 Số tầng", min_value=1, max_value=10, value=2)
        
        col3, col4 = st.columns(2)
        
        with col3:
            loai_hinh = st.selectbox("Loại hình", ["Nhà riêng", "Căn hộ", "Đất nền"])
            phap_ly = st.selectbox("Tình trạng pháp lý", ["Sổ hồng", "Sổ đỏ", "Đang hoàn thiện"])
            noi_that = st.selectbox("Tình trạng nội thất", ["Đầy đủ", "Cơ bản", "Chưa có"])
            
        with col4:
            dac_diem = st.selectbox("Vị trí đường/hẻm", ["Mặt tiền", "Hẻm xe hơi", "Hẻm nhỏ"])
            quan = st.selectbox("Khu vực (Quận)", ["Quận Gò Vấp", "Quận Phú Nhuận", "Quận Bình Thạnh"])
        
        # Map giá trị
        loai_hinh_map = {"Nhà riêng": 0, "Căn hộ": 1, "Đất nền": 2}
        phap_ly_map = {"Sổ hồng": 5, "Sổ đỏ": 4, "Đang hoàn thiện": 2}
        noi_that_map = {"Đầy đủ": 1, "Cơ bản": 2, "Chưa có": 3}
        dac_diem_map = {"Mặt tiền": 7, "Hẻm xe hơi": 6, "Hẻm nhỏ": 2}
        quan_map = {"Quận Gò Vấp": 1, "Quận Phú Nhuận": 2, "Quận Bình Thạnh": 0}
        
        submitted = st.form_submit_button("🔍 Yêu cầu AI Định giá", type="primary")
    
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
            
            st.success("### 📊 Kết quả Thẩm định từ Hệ thống")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("💰 Giá thị trường ước tính", f"{pred_price_billion:.2f} tỷ đồng")
            with col_b:
                st.metric("📐 Đơn giá trung bình", f"{pred_price_billion/dien_tich:.2f} tỷ/m²")
        
            st.info(f"""
            **Tóm tắt thông tin tài sản:**
            - Kích thước: {chieu_ngang:.1f}m x {chieu_dai:.1f}m (Tổng: {dien_tich:.1f}m²)
            - Vị trí: {dac_diem}, {quan}
            - Phân loại: {loai_hinh} - Pháp lý: {phap_ly}
            """)
            
        except Exception as e:
            st.error("⚠️ Hệ thống đang bận hoặc có lỗi xảy ra, vui lòng thử lại sau.")

# Kiểm tra rủi ro
elif menu == "⚠️ Kiểm tra rủi ro giá":
    st.title("⚠️ Kiểm tra rủi ro giao dịch")
    st.markdown("""
    ### Đánh giá mức độ an toàn của giá bán
    Bạn đang định mua hoặc bán một căn nhà? Hãy nhập mức giá đó vào đây. 
    Hệ thống AI sẽ đối chiếu với hàng ngàn giao dịch khác để cảnh báo nếu mức giá này có dấu hiệu "bất thường" (thổi giá hoặc quá rẻ do vướng pháp lý).
    """)
    
    with st.form("anomaly_form"):
        st.subheader("📋 Thông tin giao dịch cần kiểm tra")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dien_tich = st.number_input("🏠 Diện tích (m²)", min_value=10.0, max_value=500.0, value=75.0, step=5.0)
            gia_ban = st.number_input("💰 Giá đang rao bán (tỷ đồng)", min_value=0.5, max_value=500.0, value=7.0, step=0.5)
            
        with col2:
            loai_hinh = st.selectbox("🏢 Loại hình", ["Nhà riêng", "Căn hộ", "Đất nền"])
            quan = st.selectbox("📍 Khu vực", ["Quận Gò Vấp", "Quận Phú Nhuận", "Quận Bình Thạnh"])
            
        with col3:
            dac_diem = st.selectbox("📍 Vị trí đường/hẻm", ["Mặt tiền", "Hẻm xe hơi", "Hẻm nhỏ"])
            so_phong_ngu = st.number_input("🛏️ Số phòng ngủ", min_value=1, max_value=10, value=3, step=1)
        
        # Map giá trị cho model
        loai_hinh_map = {"Nhà riêng": 0, "Căn hộ": 1, "Đất nền": 2}
        quan_map = {"Quận Gò Vấp": 0, "Quận Phú Nhuận": 1, "Quận Bình Thạnh": 2}
        dac_diem_map = {"Mặt tiền": 7, "Hẻm xe hơi": 6, "Hẻm nhỏ": 2}
        
        # Thông số phụ (ẩn bớt sự phức tạp)
        with st.expander("Nhấn vào đây nếu bạn muốn nhập thêm chi tiết (Không bắt buộc)"):
            col4, col5, col6 = st.columns(3)
            with col4:
                chieu_ngang = st.number_input("Chiều rộng (m)", min_value=2.0, max_value=30.0, value=5.0, step=0.5, key="anom_width")
                chieu_dai = st.number_input("Chiều dài (m)", min_value=3.0, max_value=50.0, value=15.0, step=0.5, key="anom_length")
            with col5:
                tong_tang = st.number_input("Số tầng", min_value=1, max_value=10, value=2, key="anom_floor")
                so_phong_ve_sinh = st.number_input("Số phòng vệ sinh", min_value=1, max_value=6, value=2, key="anom_bath")
            with col6:
                phap_ly = st.selectbox("Giấy tờ pháp lý", ["Sổ hồng", "Sổ đỏ", "Đang hoàn thiện"], key="anom_legal")
        
        submitted = st.form_submit_button("🔍 Phân tích rủi ro", type="primary")
    
    if submitted:
        phap_ly_map = {"Sổ hồng": 5, "Sổ đỏ": 4, "Đang hoàn thiện": 2}
        price_m2 = gia_ban / dien_tich
        
        # Logic tính toán
        mean_price = 6.5
        std_price = 9.95
        z_score = abs(gia_ban - mean_price) / std_price
        anomaly_zscore = z_score > 3
        
        anomaly_minmax = (price_m2 < 0.03) or (price_m2 > 0.5)
        
        p10, p90 = 0.08, 0.25
        anomaly_percentile = (price_m2 < p10) or (price_m2 > p90)
        
        input_data = pd.DataFrame([{
            "dien_tich": dien_tich,
            "loai_hinh": loai_hinh_map[loai_hinh],
            "giay_to_phap_ly": phap_ly_map[phap_ly],
            "so_phong_ngu": so_phong_ngu,
            "so_phong_ve_sinh": so_phong_ve_sinh,
            "tong_so_tang": tong_tang,
            "tinh_trang_noi_that": 2,
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
            
            error_threshold = 0.387
            anomaly_rf = error > error_threshold
            
            anomaly_score = (0.4 * anomaly_rf + 0.2 * anomaly_zscore + 0.2 * anomaly_minmax + 0.2 * anomaly_percentile)
            
            st.markdown("---")
            st.subheader("📊 Kết luận từ Hệ thống")
            
            if anomaly_score >= 0.5:
                st.error("🚨 **CẢNH BÁO: MỨC GIÁ CÓ DẤU HIỆU BẤT THƯỜNG!** 🚨")
                st.write("Giao dịch này tiềm ẩn rủi ro. Mức giá bạn nhập vào đang chênh lệch quá lớn so với giá trị thực tế của thị trường.")
            else:
                st.success("✅ **AN TOÀN: MỨC GIÁ HỢP LÝ** ✅")
                st.write("Mức giá này phù hợp với mặt bằng chung của thị trường và các đặc điểm của căn nhà.")
            
            st.markdown("---")
            st.subheader("🔬 Chi tiết các bài kiểm tra của AI")
            
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("**So sánh giá trị**")
                st.metric("Giá bạn nhập", f"{gia_ban:.2f} tỷ")
                st.metric("Giá AI thẩm định", f"{pred_price:.2f} tỷ", delta=f"{gia_ban - pred_price:+.2f} tỷ (Chênh lệch)")
                
            with col_right:
                st.markdown("**Kết quả 4 lớp kiểm tra**")
                
                if anomaly_zscore:
                    st.error("❌ Lớp 1 (Mặt bằng chung): Giá chênh lệch quá lớn so với khu vực.")
                else:
                    st.success("✅ Lớp 1 (Mặt bằng chung): An toàn.")
                
                if anomaly_minmax:
                    st.error("❌ Lớp 2 (Khung giá chuẩn): Đơn giá nằm ngoài khung giao dịch phổ biến.")
                else:
                    st.success("✅ Lớp 2 (Khung giá chuẩn): An toàn.")
                    
                if anomaly_percentile:
                    st.error("❌ Lớp 3 (Phân khúc): Mức giá thuộc nhóm cực hiếm, cần cẩn trọng.")
                else:
                    st.success("✅ Lớp 3 (Phân khúc): An toàn.")
                
                if anomaly_rf:
                    st.error("❌ Lớp 4 (AI Thẩm định): Giá không tương xứng với tiện ích/vị trí nhà.")
                else:
                    st.success("✅ Lớp 4 (AI Thẩm định): Giá tương xứng với tiện ích nhà.")
            
            st.markdown("---")
            st.subheader("💡 Lời khuyên cho bạn")
            
            reasons = []
            if anomaly_zscore:
                reasons.append("• **Về mặt bằng chung:** Mức giá này đang chênh lệch rất bất thường so với mức giá trung bình của toàn khu vực.")
            if anomaly_minmax:
                reasons.append(f"• **Về đơn giá:** Mức giá {price_m2:.2f} tỷ/m² là mức giá phi thực tế hoặc rất hiếm gặp trên thị trường hiện nay.")
            if anomaly_percentile:
                reasons.append("• **Về phân khúc:** Giao dịch này có dấu hiệu bị 'thổi giá' (nếu quá cao) hoặc có vấn đề nghiêm trọng về pháp lý/quy hoạch (nếu quá thấp).")
            if anomaly_rf:
                reasons.append("• **Về giá trị thực:** Trí tuệ nhân tạo đánh giá rằng với diện tích, vị trí và tiện ích như trên, căn nhà không thể có mức giá này.")
            
            if reasons:
                for reason in reasons:
                    st.write(reason)
                st.warning("⚠️ **Khuyến nghị:** Bạn nên đến xem xét trực tiếp tài sản, kiểm tra kỹ giấy tờ pháp lý, quy hoạch và tham khảo thêm ý kiến chuyên gia trước khi xuống tiền.")
            else:
                st.write("✅ Mọi chỉ số đều nằm trong vùng an toàn. Bạn có thể tự tin tiến hành các bước tiếp theo của giao dịch.")
            
        except Exception as e:
            st.error("⚠️ Vui lòng kiểm tra lại các thông tin đã nhập.")
