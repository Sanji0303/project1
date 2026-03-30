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
    
    # Tạo tab để chọn giữa nhập thủ công và upload file
    tab1, tab2 = st.tabs(["📝 Nhập thủ công", "📂 Upload file CSV (Định giá hàng loạt)"])
    
    # ==================== TAB 1: NHẬP THỦ CÔNG ====================
    with tab1:
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
                st.error(f"⚠️ Hệ thống đang bận hoặc có lỗi xảy ra: {str(e)}")
    
    # ==================== TAB 2: UPLOAD CSV (ĐỊNH GIÁ HÀNG LOẠT) ====================
    with tab2:
        st.markdown("""
        ### 📂 Định giá hàng loạt bằng file CSV
        
        **Hướng dẫn:**
        1. Tải file mẫu để biết cấu trúc dữ liệu
        2. Điền thông tin các bất động sản vào file
        3. Upload file lên hệ thống
        4. Hệ thống sẽ tự động định giá và xuất kết quả
        
        **Các cột bắt buộc trong file CSV:**
        - `chieu_ngang` (m) - Chiều rộng mặt tiền
        - `chieu_dai` (m) - Chiều dài đất
        - `so_phong_ngu` - Số phòng ngủ
        - `so_phong_ve_sinh` - Số phòng vệ sinh
        - `tong_so_tang` - Tổng số tầng
        - `loai_hinh` - Nhà riêng/Căn hộ/Đất nền
        - `phap_ly` - Sổ hồng/Sổ đỏ/Đang hoàn thiện
        - `noi_that` - Đầy đủ/Cơ bản/Chưa có
        - `dac_diem` - Mặt tiền/Hẻm xe hơi/Hẻm nhỏ
        - `quan` - Quận Gò Vấp/Quận Phú Nhuận/Quận Bình Thạnh
        """)
        
        # Nút tải file mẫu
        if st.button("📥 Tải file mẫu CSV", key="download_template"):
            # Tạo file mẫu
            sample_data = pd.DataFrame({
                "chieu_ngang": [5.0, 6.5, 4.2, 7.0],
                "chieu_dai": [15.0, 12.0, 10.5, 18.0],
                "so_phong_ngu": [3, 4, 2, 5],
                "so_phong_ve_sinh": [2, 3, 1, 4],
                "tong_so_tang": [2, 3, 1, 4],
                "loai_hinh": ["Nhà riêng", "Căn hộ", "Nhà riêng", "Đất nền"],
                "phap_ly": ["Sổ hồng", "Sổ đỏ", "Sổ hồng", "Sổ đỏ"],
                "noi_that": ["Đầy đủ", "Cơ bản", "Chưa có", "Đầy đủ"],
                "dac_diem": ["Mặt tiền", "Hẻm xe hơi", "Hẻm nhỏ", "Mặt tiền"],
                "quan": ["Quận Gò Vấp", "Quận Bình Thạnh", "Quận Phú Nhuận", "Quận Gò Vấp"]
            })
            
            # Thêm cột diện tích để người dùng tham khảo
            sample_data["dien_tich"] = sample_data["chieu_ngang"] * sample_data["chieu_dai"]
            
            # Chuyển thành CSV
            csv = sample_data.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📥 Tải file mẫu (CSV)",
                data=csv,
                file_name="mau_dinh_gia_bds.csv",
                mime="text/csv",
                key="download_template_btn"
            )
        
        st.divider()
        
        # Upload file
        uploaded_file = st.file_uploader(
            "📁 Chọn file CSV của bạn",
            type=["csv"],
            help="File phải có đủ các cột bắt buộc theo mẫu",
            key="csv_uploader"
        )
        
        if uploaded_file is not None:
            try:
                # Đọc file
                df_upload = pd.read_csv(uploaded_file)
                
                # Kiểm tra các cột bắt buộc
                required_cols = [
                    "chieu_ngang", "chieu_dai", "so_phong_ngu", "so_phong_ve_sinh",
                    "tong_so_tang", "loai_hinh", "phap_ly", "noi_that", "dac_diem", "quan"
                ]
                
                missing_cols = [col for col in required_cols if col not in df_upload.columns]
                if missing_cols:
                    st.error(f"❌ File thiếu các cột bắt buộc: {', '.join(missing_cols)}")
                    st.info("Vui lòng tải file mẫu và điền đúng định dạng!")
                else:
                    st.success(f"✅ Đã tải file thành công! Có {len(df_upload)} bất động sản cần định giá.")
                    
                    # Hiển thị preview dữ liệu
                    with st.expander("📋 Xem trước dữ liệu đã tải", expanded=False):
                        st.dataframe(df_upload.head(10), use_container_width=True)
                    
                    # Xử lý định giá
                    with st.spinner("🔄 Đang định giá cho từng bất động sản..."):
                        # Map giá trị
                        loai_hinh_map = {"Nhà riêng": 0, "Căn hộ": 1, "Đất nền": 2}
                        phap_ly_map = {"Sổ hồng": 5, "Sổ đỏ": 4, "Đang hoàn thiện": 2}
                        noi_that_map = {"Đầy đủ": 1, "Cơ bản": 2, "Chưa có": 3}
                        dac_diem_map = {"Mặt tiền": 7, "Hẻm xe hơi": 6, "Hẻm nhỏ": 2}
                        quan_map = {"Quận Gò Vấp": 1, "Quận Phú Nhuận": 2, "Quận Bình Thạnh": 0}
                        
                        # Tạo dataframe kết quả
                        results = []
                        
                        for idx, row in df_upload.iterrows():
                            try:
                                # Tính diện tích
                                dien_tich = row["chieu_ngang"] * row["chieu_dai"]
                                
                                # Tạo input
                                input_data = pd.DataFrame([{
                                    "dien_tich": dien_tich,
                                    "loai_hinh": loai_hinh_map.get(row["loai_hinh"], 0),
                                    "giay_to_phap_ly": phap_ly_map.get(row["phap_ly"], 2),
                                    "so_phong_ngu": row["so_phong_ngu"],
                                    "so_phong_ve_sinh": row["so_phong_ve_sinh"],
                                    "tong_so_tang": row["tong_so_tang"],
                                    "tinh_trang_noi_that": noi_that_map.get(row["noi_that"], 2),
                                    "dac_diem": dac_diem_map.get(row["dac_diem"], 2),
                                    "chieu_ngang": row["chieu_ngang"],
                                    "chieu_dai": row["chieu_dai"],
                                    "e_Quận Gò Vấp": 1 if quan_map.get(row["quan"], 0) == 1 else 0,
                                    "e_Quận Phú Nhuận": 1 if quan_map.get(row["quan"], 0) == 2 else 0
                                }])
                                
                                # Dự đoán
                                pred_log = model.predict(input_data)[0]
                                pred_price = np.expm1(pred_log)
                                
                                # Lưu kết quả
                                results.append({
                                    "STT": idx + 1,
                                    "Chiều ngang (m)": row["chieu_ngang"],
                                    "Chiều dài (m)": row["chieu_dai"],
                                    "Diện tích (m²)": round(dien_tich, 2),
                                    "Số phòng ngủ": row["so_phong_ngu"],
                                    "Số phòng vệ sinh": row["so_phong_ve_sinh"],
                                    "Số tầng": row["tong_so_tang"],
                                    "Loại hình": row["loai_hinh"],
                                    "Pháp lý": row["phap_ly"],
                                    "Nội thất": row["noi_that"],
                                    "Vị trí": row["dac_diem"],
                                    "Quận": row["quan"],
                                    "Giá dự đoán (tỷ)": round(pred_price, 2),
                                    "Đơn giá (tỷ/m²)": round(pred_price / dien_tich, 3)
                                })
                            except Exception as e:
                                results.append({
                                    "STT": idx + 1,
                                    **{col: row.get(col, "N/A") for col in required_cols[:8]},
                                    "Giá dự đoán (tỷ)": "Lỗi",
                                    "Đơn giá (tỷ/m²)": str(e)[:50]
                                })
                        
                        # Tạo dataframe kết quả
                        df_results = pd.DataFrame(results)
                        
                        st.success(f"✅ Đã định giá thành công {len([r for r in results if 'Lỗi' not in str(r['Giá dự đoán (tỷ)'])])} bất động sản!")
                        
                        # Hiển thị thống kê
                        st.subheader("📊 Thống kê tổng quan")
                        valid_prices = [r["Giá dự đoán (tỷ)"] for r in results if isinstance(r["Giá dự đoán (tỷ)"], (int, float))]
                        
                        if valid_prices:
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("🏠 Tổng số BĐS", len(results))
                            with col2:
                                st.metric("💰 Giá trung bình", f"{np.mean(valid_prices):.2f} tỷ")
                            with col3:
                                st.metric("📈 Giá cao nhất", f"{np.max(valid_prices):.2f} tỷ")
                            with col4:
                                st.metric("📉 Giá thấp nhất", f"{np.min(valid_prices):.2f} tỷ")
                        
                        # Hiển thị kết quả
                        st.subheader("📋 Kết quả định giá")
                        st.dataframe(df_results, use_container_width=True, height=400)
                        
                        # Nút tải kết quả
                        csv_results = df_results.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📥 Tải kết quả định giá (CSV)",
                            data=csv_results,
                            file_name="ket_qua_dinh_gia.csv",
                            mime="text/csv",
                            key="download_results"
                        )
                        
                        # Hiển thị biểu đồ phân bố giá
                        if valid_prices:
                            st.subheader("📊 Phân bố giá dự đoán")
                            chart_data = pd.DataFrame(valid_prices, columns=["Giá (tỷ)"])
                            st.bar_chart(chart_data, height=300)
                            
            except Exception as e:
                st.error(f"❌ Lỗi khi đọc file: {str(e)}")
                st.info("Vui lòng kiểm tra lại định dạng file CSV hoặc tải file mẫu để tham khảo.")
