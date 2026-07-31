import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

# ==========================================
# 1. PATH CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True) # สร้างโฟลเดอร์ models ถ้ายังไม่มี

INPUT_PATH = PROCESSED_DIR / "daily_sales_forecast.csv"
OUTPUT_PATH = PROCESSED_DIR / "forecasted_sales.csv"
MODEL_PATH = MODEL_DIR / "sales_lstm.keras"

# ฟังก์ชันสร้างข้อมูลแบบ Sequence (ดูย้อนหลังทีละ 30 วัน เพื่อทายวันที่ 31)
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def main():
    print("\n[1/5] Loading and Preprocessing Data...")
    df = pd.read_csv(INPUT_PATH)
    df['date_key'] = pd.to_datetime(df['date_key'])

    # ดึงมาเฉพาะคอลัมน์ยอดขายรวม
    sales_data = df['total_sales'].values.reshape(-1, 1)

    # ปรับสเกลข้อมูลให้อยู่ระหว่าง 0 ถึง 1 เพื่อให้ AI เรียนรู้ได้เร็วขึ้น
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_sales = scaler.fit_transform(sales_data)

    # กำหนดให้ดูข้อมูลย้อนหลัง 30 วัน
    SEQ_LENGTH = 30
    X, y = create_sequences(scaled_sales, SEQ_LENGTH)

    # แบ่งข้อมูล Train (80%) และ Test (20%)
    split_index = int(len(X) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    print(f"[2/5] Building LSTM Model (Input shape: {X_train.shape})...")
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(SEQ_LENGTH, 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    print("\n[3/5] Training Model (This will take a minute or two)...")
    # สั่งให้ AI เริ่มเรียนรู้ (รัน 20 รอบ/Epochs)
    model.fit(
        X_train, y_train, 
        batch_size=32, 
        epochs=20, 
        validation_data=(X_test, y_test), 
        verbose=1
    )

    print(f"\n[4/5] Saving Trained Model to: {MODEL_PATH}")
    model.save(MODEL_PATH)

    print("\n[5/5] Generating 30-Day Future Forecast...")
    # ดึงข้อมูล 30 วันสุดท้ายของปี 2025 มาเป็นจุดเริ่มต้นการทำนาย
    last_30_days = scaled_sales[-SEQ_LENGTH:]
    current_sequence = last_30_days.reshape(1, SEQ_LENGTH, 1)

    forecast_scaled = []
    # ทำนายล่วงหน้า 30 วัน
    for _ in range(30):
        next_pred = model.predict(current_sequence, verbose=0)
        forecast_scaled.append(next_pred[0, 0])
        
        # อัปเดต Sequence โดยเอาค่าที่เพิ่งทายได้ ต่อท้ายเข้าไป และตัดค่าเก่าสุดออก
        next_pred_reshaped = np.reshape(next_pred, (1, 1, 1))
        current_sequence = np.append(current_sequence[:, 1:, :], next_pred_reshaped, axis=1)

    # แปลงสเกลกลับเป็นตัวเลขยอดขาย (หลักล้านบาท) แบบปกติ
    forecast_actual = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1))

    # สร้างวันที่สำหรับอนาคตอีก 30 วัน (มกราคม 2026)
    last_date = df['date_key'].max()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30)

    # สร้าง DataFrame เซฟเป็นไฟล์ CSV
    forecast_df = pd.DataFrame({
        'date_key': forecast_dates,
        'forecasted_sales': forecast_actual.flatten().round(2)
    })

    forecast_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nForecast data saved to: {OUTPUT_PATH}")
    print("=" * 60)
    print("TENSORFLOW FORECASTING COMPLETED SUCCESSFULLY! ✅")
    print("=" * 60)

if __name__ == "__main__":
    main()