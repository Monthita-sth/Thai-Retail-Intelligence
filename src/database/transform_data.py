import sqlite3
from pathlib import Path

# ==========================================
# PATH CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "retail_db.sqlite"

def create_star_schema():
    print(f"Connecting to Database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # 1. CREATE DIMENSION TABLES (ข้อมูล Master)
    # ---------------------------------------------------------
    print("Creating Dimension Tables...")
    
    # 1.1 Dim_Customers
    cursor.execute("DROP TABLE IF EXISTS dim_customers")
    cursor.execute("""
        CREATE TABLE dim_customers AS
        SELECT customer_id, gender, age, province, region, acquisition_source
        FROM customers
    """)

    # 1.2 Dim_Products
    cursor.execute("DROP TABLE IF EXISTS dim_products")
    cursor.execute("""
        CREATE TABLE dim_products AS
        SELECT product_id, product_name, category, brand, unit_cost, unit_price
        FROM products
    """)

    # 1.3 Dim_Promotions
    cursor.execute("DROP TABLE IF EXISTS dim_promotions")
    cursor.execute("""
        CREATE TABLE dim_promotions AS
        SELECT promotion_id, promotion_name, event_type, discount_rate
        FROM promotions
    """)

    # ---------------------------------------------------------
    # 2. CREATE FACT TABLE (ข้อมูล Transaction)
    # ---------------------------------------------------------
    print("Creating Fact Table (fact_sales) using CTEs...")
    
    # ใช้ CTE (WITH clause) เพื่อกรองเฉพาะออเดอร์ที่จัดส่งสำเร็จ และเตรียมข้อมูลก่อน Join
    cursor.execute("DROP TABLE IF EXISTS fact_sales")
    cursor.execute("""
        CREATE TABLE fact_sales AS
        WITH valid_orders AS (
            SELECT 
                order_id, 
                customer_id, 
                date(order_date) as date_key, 
                channel, 
                promotion_id
            FROM orders
            WHERE order_status = 'Delivered'
        ),
        sales_data AS (
            SELECT 
                oi.order_id,
                oi.product_id,
                oi.quantity,
                oi.gross_sales,
                oi.discount_amount,
                oi.net_sales,
                oi.total_cost,
                oi.profit
            FROM order_items oi
        )
        SELECT 
            vo.date_key,
            vo.order_id,
            vo.customer_id,
            sd.product_id,
            vo.promotion_id,
            vo.channel,
            sd.quantity,
            sd.gross_sales,
            sd.discount_amount,
            sd.net_sales,
            sd.total_cost,
            sd.profit
        FROM valid_orders vo
        JOIN sales_data sd ON vo.order_id = sd.order_id
    """)

    conn.commit()
    conn.close()
    print("Star Schema created successfully!")

if __name__ == "__main__":
    print("=" * 50)
    print("STARTING DATA TRANSFORMATION")
    print("=" * 50)
    create_star_schema()