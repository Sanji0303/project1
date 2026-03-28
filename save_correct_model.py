# save_correct_model.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

# Load data
df = pd.read_csv('clean_data.csv')

# Chuẩn bị dữ liệu
X = df.drop('gia_ban', axis=1)
y = np.log1p(df["gia_ban"])

# Tạo pipeline hoàn chỉnh
pipeline = Pipeline([
    ('scaler', MinMaxScaler()),
    ('model', RandomForestRegressor(
        n_estimators=300,
        max_depth=20,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features='sqrt',
        random_state=42
    ))
])

# Train
pipeline.fit(X, y)

# Lưu model
joblib.dump(pipeline, "model_pipeline.pkl")
print("✅ Đã lưu model pipeline hoàn chỉnh")