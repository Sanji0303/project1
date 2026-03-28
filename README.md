# 🏡 Đồ án: Dự đoán giá nhà & Phát hiện giá bất thường (PySpark)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySpark](https://img.shields.io/badge/PySpark-Data_Processing_%26_ML-orange.svg)

## 📌 Giới thiệu
Đây là đồ án "Dự đoán giá nhà và phát hiện giá bất thường". Mục tiêu của dự án là sử dụng các kiến thức đã học để xử lý tập dữ liệu bất động sản, phát hiện các mức giá nhà bất thường (Anomaly Detection) và xây dựng mô hình học máy cơ bản để dự đoán giá nhà.

Do giới hạn của đồ án nhỏ, nhóm tập trung hoàn toàn vào khâu xử lý dữ liệu lớn và xây dựng mô hình bằng thư viện của *Python* và *Pyspark*.

## 👥 Nhóm thực hiện (3 thành viên)
1. **[Huỳnh Lê Xuân Ánh]** - [Vai trò: Xử lý dữ liệu, xây dựng models ML thường (Python) ]
2. **[Nguyễn Thị Tuyết Vân]**  - [Vai trò: Xây dựng models trong môi trường Pyspark]
3. **[Đặng Đức Duy]** - [Vai trò: Phát hiện giá bất thường, Báo cáo]

---

## 🧭 Hướng dẫn xem đồ án

Để nắm bắt luồng công việc của nhóm một cách dễ dàng nhất, xin vui lòng xem các file theo thứ tự sau:

1. **`Preprocessing.ipynb`**: Tiền xử lý dữ liệu
2. **`PricePrediction_PythonML.ipynb`**: Thực hiện build model trong môi trường Python
3. **`ModelPricePrediction_AnomalyDetection_Pyspark.ipynb`**: Thực hiện build model trong môi trường Pyspark và build function phát hiện giá bất thường

---

## 📁 Cấu trúc thư mục
```text
├── DL07_K311_HuynhLeXuanAnh_DangDucDuy_NguyenThiTuyetVan/
├── 📂 Final Project/
│   
├── 📂 GUI/
│   
├── 📂 Project 1/
│   ├── 📂 data
│        └── quan-binh-thanh.csv
│        └── quan-phu-nhuan.csv
│        └── quan-go-vap.csv
│        └── clean_data.csv
│        └── Mô tả bộ dữ liệu Nhà Tốt.pdf
│   ├── 📂 source_code
│        └── ModelPricePrediction_AnomalyDetection_Pyspark.ipynb
│        └── Preprocessing.ipynb
│        └── PricePrediction_PythonML.ipynb
│   ├── DL07_K311_Team7_Presentation.pptx
|   ├──readme.ipynb
│   
└── 📂 Project 2/
