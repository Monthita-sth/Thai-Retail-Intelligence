import pandas as pd
from pathlib import Path

# ==========================================
# PATH CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

INPUT_PATH = PROCESSED_DIR / "fact_sales.csv"
OUTPUT_PATH = PROCESSED_DIR / "daily_sales_forecast.csv"

def run_etl():
    print(f"\n[Extract] Reading data from: {INPUT_PATH}")
    
    # อ่านข้อมูล CSV
    df = pd.read_csv(INPUT_PATH)
    
    # แปลงคอลัมน์ date_key ให้เป็นรูปแบบวันที่ที่ถูกต้อง
    df['date_key'] = pd.to_datetime(df['date_key'])
    
    print("\n[Transform] Aggregating daily sales and extracting time features...")
    
    # จับกลุ่มตามวันที่และหายอดรวม
    daily_sales = df.groupby('date_key').agg(
        total_sales=('net_sales', 'sum'),
        total_profit=('profit', 'sum'),
        total_items_sold=('order_id', 'count')
    ).reset_index()
    
    # ปัดเศษทศนิยม 2 ตำแหน่ง
    daily_sales['total_sales'] = daily_sales['total_sales'].round(2)
    daily_sales['total_profit'] = daily_sales['total_profit'].round(2)
    
    # สร้างคอลัมน์ใหม่สำหรับฟีเจอร์เวลา (Year, Month, Day of Week)
    daily_sales['year'] = daily_sales['date_key'].dt.year
    daily_sales['month'] = daily_sales['date_key'].dt.month
    # dt.dayofweek จะได้ 0 (จันทร์) ถึง 6 (อาทิตย์) เราบวก 1 ให้เป็น 1-7
    daily_sales['day_of_week'] = daily_sales['date_key'].dt.dayofweek + 1 
                             
    # เรียงลำดับตามวันที่จากอดีต -> ปัจจุบัน
    daily_sales = daily_sales.sort_values('date_key')
    
    # โชว์ตัวอย่างข้อมูล 5 บรรทัดแรก
    print("\nSample Data (First 5 rows):")
    print(daily_sales.head())
    
    # ==========================================
    # LOAD (SAVE DATA)
    # ==========================================
    print(f"\n[Load] Saving processed data to: {OUTPUT_PATH}")
    daily_sales.to_csv(OUTPUT_PATH, index=False)
    
    print("\nETL Pipeline Completed Successfully! ✅")

if __name__ == "__main__":
    print("=" * 60)
    print("PANDAS ETL PIPELINE (Replaced PySpark)")
    print("=" * 60)
    run_etl()