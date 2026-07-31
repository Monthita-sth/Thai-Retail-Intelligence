import pandas as pd
import sqlite3
from pathlib import Path

# ==========================================
# PATH CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "retail_db.sqlite"

# สร้างโฟลเดอร์ processed ถ้ายังไม่มี
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def export_for_powerbi():
    print(f"Connecting to Database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    # รายชื่อตารางใน Star Schema ที่เราต้องการ
    tables = [
        'fact_sales', 
        'dim_customers', 
        'dim_products', 
        'dim_promotions'
    ]
    
    for table in tables:
        print(f"Exporting {table}...")
        # อ่านจาก SQLite และเซฟเป็น CSV (เพื่อให้ Power BI โหลดได้เร็ว)
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        df.to_csv(PROCESSED_DIR / f"{table}.csv", index=False)
        
    conn.close()
    print("\nExport complete! Power BI files are ready in 'data/processed/' folder.")

if __name__ == "__main__":
    print("=" * 50)
    print("EXPORTING STAR SCHEMA TO PROCESSED FOLDER")
    print("=" * 50)
    export_for_powerbi()