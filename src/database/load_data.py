import pandas as pd
import sqlite3
from pathlib import Path

# ==========================================
# PATH CONFIGURATION
# ==========================================
# ตั้งค่าให้ชี้กลับไปที่โฟลเดอร์นอกสุด
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

# กำหนดที่เก็บไฟล์ Database ไว้ในโฟลเดอร์ data
DB_PATH = BASE_DIR / "data" / "retail_db.sqlite"

# ==========================================
# LOAD DATA FUNCTION
# ==========================================
def load_excel_to_sqlite():
    print(f"Connecting to local SQLite Database at: \n{DB_PATH}\n")
    
    # เชื่อมต่อ (หรือสร้างไฟล์ฐานข้อมูลใหม่ถ้ายังไม่มี)
    conn = sqlite3.connect(DB_PATH)
    
    # กวาดไฟล์ .xlsx ทั้งหมด
    excel_files = list(RAW_DIR.glob("*.xlsx"))
    
    if not excel_files:
        print("No .xlsx files found in data/raw/")
        return

    for file_path in excel_files:
        table_name = file_path.stem # ใช้ชื่อไฟล์เป็นชื่อ Table
        print(f"Reading {file_path.name} ...")
        
        # อ่านไฟล์ Excel
        df = pd.read_excel(file_path)
        
        print(f"Loading data into table: {table_name} ({len(df):,} rows)")
        
        # โหลดเข้า SQLite
        df.to_sql(
            table_name, 
            conn, 
            if_exists='replace', 
            index=False,
            chunksize=10000 # แบ่งส่งทีละหมื่นบรรทัดเพื่อไม่ให้กิน Memory เครื่องมากไป
        )
        print(f"Success: {table_name}\n")

    # ปิดการเชื่อมต่อ
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("STARTING DATA INGESTION (SQLITE)")
    print("=" * 60)
    load_excel_to_sqlite()
    print("ALL DATA LOADED SUCCESSFULLY!")