from pathlib import Path
import numpy as np
import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================
SEED = 42
N_CUSTOMERS = 50_000
N_PRODUCTS = 1_000
N_ORDERS = 300_000
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

rng = np.random.default_rng(SEED)

# ============================================================
# PATH CONFIGURATION
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# THAI PROVINCES
# ============================================================
PROVINCES = [
    ("Bangkok", "Central"),
    ("Nonthaburi", "Central"),
    ("Pathum Thani", "Central"),
    ("Nakhon Pathom", "Central"),
    ("Ayutthaya", "Central"),
    ("Chiang Mai", "North"),
    ("Chiang Rai", "North"),
    ("Phitsanulok", "North"),
    ("Lampang", "North"),
    ("Khon Kaen", "Northeast"),
    ("Udon Thani", "Northeast"),
    ("Nakhon Ratchasima", "Northeast"),
    ("Ubon Ratchathani", "Northeast"),
    ("Chon Buri", "East"),
    ("Rayong", "East"),
    ("Chanthaburi", "East"),
    ("Phuket", "South"),
    ("Surat Thani", "South"),
    ("Songkhla", "South"),
    ("Nakhon Si Thammarat", "South"),
]

PROVINCE_NAMES = [province[0] for province in PROVINCES]
PROVINCE_REGION_MAP = {province: region for province, region in PROVINCES}

# ============================================================
# PRODUCT CATEGORIES
# ============================================================
CATEGORIES = ["Electronics", "Home & Living", "Beauty", "Fashion", "Grocery", "Pet Supplies", "Health"]
BRANDS = ["ThaiChoice", "SiamStyle", "BangkokPlus", "MangoHome", "ChaoPhraya", "SmartLife", "UrbanThai", "NatureCare", "HappyHome", "DailyBest"]
CHANNELS = ["Website", "Shopee", "Lazada", "TikTok Shop", "Facebook", "LINE"]
PAYMENT_METHODS = ["COD", "Credit Card", "Mobile Banking", "PromptPay", "E-Wallet"]
RETURN_REASONS = ["Damaged Product", "Wrong Product", "Changed Mind", "Product Not as Described", "Size Issue", "Other"]

# ============================================================
# 1. GENERATE CUSTOMERS
# ============================================================
def generate_customers():
    print("Generating customers...")
    customer_ids = [f"C{i:06d}" for i in range(1, N_CUSTOMERS + 1)]

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "gender": rng.choice(["Male", "Female"], size=N_CUSTOMERS, p=[0.45, 0.55]),
        "age": rng.integers(18, 66, size=N_CUSTOMERS),
        "province": rng.choice(
            PROVINCE_NAMES,
            size=N_CUSTOMERS,
            p=[
                0.25,  # [จุดที่แก้ไข 1] เปลี่ยนจาก 0.28 เป็น 0.25 เพื่อให้ผลรวม Probability = 1.0 พอดี
                0.05, 0.05, 0.03, 0.02, 
                0.08, 0.03, 0.02, 0.02, 
                0.07, 0.04, 0.04, 0.03, 
                0.07, 0.03, 0.02, 
                0.05, 0.04, 0.03, 0.03,
            ]
        ),
        "signup_date": rng.choice(pd.date_range(START_DATE, END_DATE), size=N_CUSTOMERS),
        "acquisition_source": rng.choice(
            ["Facebook Ads", "Google Ads", "TikTok", "Organic Search", "Referral", "LINE OA"],
            size=N_CUSTOMERS,
            p=[0.20, 0.18, 0.15, 0.22, 0.10, 0.15]
        )
    })
    customers["region"] = customers["province"].map(PROVINCE_REGION_MAP)
    return customers

# ============================================================
# 2. GENERATE PRODUCTS
# ============================================================
def generate_products():
    print("Generating products...")
    product_ids = [f"P{i:05d}" for i in range(1, N_PRODUCTS + 1)]

    products = pd.DataFrame({
        "product_id": product_ids,
        "product_name": [f"Product_{i:05d}" for i in range(1, N_PRODUCTS + 1)],
        "category": rng.choice(CATEGORIES, size=N_PRODUCTS, p=[0.18, 0.15, 0.15, 0.18, 0.12, 0.10, 0.12]),
        "brand": rng.choice(BRANDS, size=N_PRODUCTS),
        "unit_cost": np.round(rng.uniform(20, 3000, size=N_PRODUCTS), 2)
    })

    products["unit_price"] = (products["unit_cost"] * rng.uniform(1.20, 2.50, size=N_PRODUCTS)).round(2)
    products["popularity_score"] = rng.gamma(shape=2.0, scale=1.0, size=N_PRODUCTS)
    products["initial_stock"] = rng.integers(50, 2000, size=N_PRODUCTS)
    return products

# ============================================================
# 3. GENERATE PROMOTION / CAMPAIGN CALENDAR
# ============================================================
def generate_promotions():
    print("Generating promotions...")
    records = []
    promotion_counter = 1

    for year in [2024, 2025]:
        for month in range(1, 13):
            campaign_date = pd.Timestamp(year=year, month=month, day=month)
            records.append({
                "promotion_id": f"PROMO{promotion_counter:04d}",
                "promotion_name": f"{month}.{month} Monthly Mega Sale",
                "promotion_date": campaign_date,
                "event_type": "Monthly Campaign",
                "discount_rate": round(rng.uniform(0.10, 0.25), 2),
                "sales_multiplier": round(rng.uniform(1.3, 2.0), 2)
            })
            promotion_counter += 1

        # 11.11
        records.append({
            "promotion_id": f"PROMO{promotion_counter:04d}",
            "promotion_name": "11.11 Mega Sale",
            "promotion_date": pd.Timestamp(year=year, month=11, day=11),
            "event_type": "Mega Campaign",
            "discount_rate": 0.25,
            "sales_multiplier": 3.0
        })
        promotion_counter += 1

        # 12.12
        records.append({
            "promotion_id": f"PROMO{promotion_counter:04d}",
            "promotion_name": "12.12 Year End Sale",
            "promotion_date": pd.Timestamp(year=year, month=12, day=12),
            "event_type": "Mega Campaign",
            "discount_rate": 0.30,
            "sales_multiplier": 3.2
        })
        promotion_counter += 1

        # Songkran
        records.append({
            "promotion_id": f"PROMO{promotion_counter:04d}",
            "promotion_name": "Songkran Shopping Festival",
            "promotion_date": pd.Timestamp(year=year, month=4, day=13),
            "event_type": "Thai Seasonal Campaign",
            "discount_rate": 0.20,
            "sales_multiplier": 2.0
        })
        promotion_counter += 1

        # New Year
        records.append({
            "promotion_id": f"PROMO{promotion_counter:04d}",
            "promotion_name": "New Year Sale",
            "promotion_date": pd.Timestamp(year=year, month=1, day=1),
            "event_type": "Thai Seasonal Campaign",
            "discount_rate": 0.15,
            "sales_multiplier": 1.8
        })
        promotion_counter += 1

    return pd.DataFrame(records)

# ============================================================
# 4. GENERATE THAI E-COMMERCE EVENT CALENDAR
# ============================================================
def generate_thai_events():
    print("Generating Thai event calendar...")
    records = []

    for year in [2024, 2025]:
        records.extend([
            {"event_name": "New Year Shopping", "event_date": pd.Timestamp(year, 1, 1), "event_type": "Seasonal", "sales_multiplier": 1.8},
            {"event_name": "Valentine Campaign", "event_date": pd.Timestamp(year, 2, 14), "event_type": "Seasonal", "sales_multiplier": 1.3},
            {"event_name": "Songkran Festival", "event_date": pd.Timestamp(year, 4, 13), "event_type": "Thai Seasonal", "sales_multiplier": 2.0},
            {"event_name": "Mid-Year Sale", "event_date": pd.Timestamp(year, 6, 6), "event_type": "Campaign", "sales_multiplier": 1.7},
            {"event_name": "9.9 Mega Sale", "event_date": pd.Timestamp(year, 9, 9), "event_type": "Campaign", "sales_multiplier": 2.2},
            {"event_name": "11.11 Mega Sale", "event_date": pd.Timestamp(year, 11, 11), "event_type": "Campaign", "sales_multiplier": 3.0},
            {"event_name": "12.12 Year End Sale", "event_date": pd.Timestamp(year, 12, 12), "event_type": "Campaign", "sales_multiplier": 3.2}
        ])
    return pd.DataFrame(records)

# ============================================================
# 5. GENERATE ORDERS
# ============================================================
def generate_orders(customers, promotions, events):
    print("Generating orders...")
    dates = pd.date_range(START_DATE, END_DATE, freq="D")
    date_weights = np.ones(len(dates))
    date_series = pd.Series(dates)

    # Weekend effect
    weekend_mask = (date_series.dt.dayofweek >= 5)
    date_weights[weekend_mask.values] *= 1.15

    # Payday effect
    payday_mask = (date_series.dt.day >= 25)
    date_weights[payday_mask.values] *= 1.35

    # Month-end effect
    month_end_mask = (date_series.dt.day >= 28)
    date_weights[month_end_mask.values] *= 1.20

    # Event boost
    event_map = dict(zip(events["event_date"], events["sales_multiplier"]))
    for i, date in enumerate(dates):
        if date in event_map:
            date_weights[i] *= event_map[date]

    # Normalize probabilities
    date_probabilities = date_weights / date_weights.sum()
    order_dates = rng.choice(dates, size=N_ORDERS, p=date_probabilities)
    selected_customers = rng.choice(customers["customer_id"], size=N_ORDERS)

    orders = pd.DataFrame({
        "order_id": [f"O{i:08d}" for i in range(1, N_ORDERS + 1)],
        "customer_id": selected_customers,
        "order_date": order_dates,
        "channel": rng.choice(CHANNELS, size=N_ORDERS, p=[0.20, 0.25, 0.20, 0.15, 0.10, 0.10]),
        "payment_method": rng.choice(PAYMENT_METHODS, size=N_ORDERS, p=[0.25, 0.20, 0.25, 0.20, 0.10]),
        "order_status": rng.choice(["Delivered", "Cancelled"], size=N_ORDERS, p=[0.92, 0.08])
    })

    orders = orders.merge(customers[["customer_id", "province", "region"]], on="customer_id", how="left")

    # Match promotion
    promotion_map = (
        promotions
        .drop_duplicates(subset=["promotion_date"], keep="last") # [จุดที่แก้ไข 2] ลบวันโปรโมชันซ้ำ (เช่น วันที่ 1.1 กับ New Year Sale) ให้เหลือแค่อันใหญ่ล่าสุด
        .set_index("promotion_date")
        .to_dict("index")
    )

    orders["promotion_id"] = orders["order_date"].map(lambda x: promotion_map.get(x, {}).get("promotion_id"))
    orders["promotion_discount"] = orders["order_date"].map(lambda x: promotion_map.get(x, {}).get("discount_rate", 0))

    orders["shipping_fee"] = rng.choice([0, 35, 50, 70], size=N_ORDERS, p=[0.25, 0.35, 0.30, 0.10])
    return orders

# ============================================================
# 6. GENERATE ORDER ITEMS
# ============================================================
def generate_order_items(orders, products):
    print("Generating order items...")
    item_counts = rng.choice([1, 2, 3, 4, 5], size=len(orders), p=[0.08, 0.17, 0.30, 0.25, 0.20])
    
    repeated_order_ids = np.repeat(orders["order_id"].values, item_counts)
    repeated_promotions = np.repeat(orders["promotion_discount"].values, item_counts)
    repeated_dates = np.repeat(orders["order_date"].values, item_counts)

    popularity = products["popularity_score"].values
    popularity = popularity / popularity.sum()
    selected_products = rng.choice(products["product_id"].values, size=len(repeated_order_ids), p=popularity)

    order_items = pd.DataFrame({
        "order_id": repeated_order_ids,
        "product_id": selected_products,
        "order_date": repeated_dates,
        "quantity": rng.integers(1, 5, size=len(repeated_order_ids)),
        "promotion_discount": repeated_promotions
    })

    order_items = order_items.merge(products[["product_id", "unit_cost", "unit_price"]], on="product_id", how="left")
    
    random_discount = rng.uniform(0, 0.08, size=len(order_items))
    order_items["discount_rate"] = np.where(order_items["promotion_discount"] > 0, order_items["promotion_discount"], random_discount)
    
    order_items["gross_sales"] = order_items["quantity"] * order_items["unit_price"]
    order_items["discount_amount"] = (order_items["gross_sales"] * order_items["discount_rate"]).round(2)
    order_items["net_sales"] = (order_items["gross_sales"] - order_items["discount_amount"]).round(2)
    order_items["total_cost"] = (order_items["quantity"] * order_items["unit_cost"]).round(2)
    order_items["profit"] = (order_items["net_sales"] - order_items["total_cost"]).round(2)
    order_items["profit_margin"] = np.where(order_items["net_sales"] > 0, order_items["profit"] / order_items["net_sales"], 0)

    return order_items

# ============================================================
# 7. GENERATE RETURNS
# ============================================================
def generate_returns(order_items, orders):
    print("Generating returns...")
    delivered_orders = (orders[orders["order_status"] == "Delivered"])[["order_id", "order_date"]]
    returned_items = order_items.merge(delivered_orders, on="order_id", how="inner", suffixes=("", "_order"))

    return_probability = rng.uniform(0, 1, size=len(returned_items))
    returned_items = returned_items[return_probability < 0.08].copy()

    if len(returned_items) == 0:
        return pd.DataFrame()

    returned_items["return_id"] = [f"RET{i:08d}" for i in range(1, len(returned_items) + 1)]
    returned_items["return_date"] = pd.to_datetime(returned_items["order_date"]) + pd.to_timedelta(rng.integers(1, 21, size=len(returned_items)), unit="D")
    returned_items["return_quantity"] = [rng.integers(1, quantity + 1) for quantity in returned_items["quantity"]]
    returned_items["return_reason"] = rng.choice(RETURN_REASONS, size=len(returned_items))
    returned_items["refund_amount"] = (returned_items["unit_price"] * returned_items["return_quantity"] * (1 - returned_items["discount_rate"])).round(2)

    returns = returned_items[["return_id", "order_id", "product_id", "return_date", "return_quantity", "return_reason", "refund_amount"]]
    return returns

# ============================================================
# 8. GENERATE INVENTORY
# ============================================================
def generate_inventory(products, order_items):
    print("Generating inventory...")
    demand = order_items.groupby("product_id")["quantity"].sum().reset_index()
    demand = demand.rename(columns={"quantity": "total_units_sold"})

    inventory = products[["product_id"]].copy()
    inventory = inventory.merge(demand, on="product_id", how="left")
    inventory["total_units_sold"] = inventory["total_units_sold"].fillna(0)
    inventory["avg_daily_demand"] = inventory["total_units_sold"] / 731
    inventory["safety_stock"] = (inventory["avg_daily_demand"] * rng.uniform(3, 10, size=len(inventory))).round().astype(int)
    inventory["reorder_point"] = (inventory["avg_daily_demand"] * rng.uniform(7, 14, size=len(inventory)) + inventory["safety_stock"]).round().astype(int)
    inventory["stock_level"] = (inventory["avg_daily_demand"] * rng.uniform(2, 45, size=len(inventory))).round().astype(int)
    inventory["lead_time_days"] = rng.integers(2, 15, size=len(inventory))
    inventory["snapshot_date"] = pd.Timestamp(END_DATE)

    inventory["stock_status"] = np.select(
        [
            inventory["stock_level"] <= inventory["reorder_point"],
            inventory["stock_level"] <= inventory["reorder_point"] * 2
        ],
        ["Critical", "Low Stock"],
        default="Healthy"
    )

    return inventory

# ============================================================
# 9. SAVE DATA
# ============================================================
def save_data(customers, products, orders, order_items, returns, inventory, promotions, thai_events):
    print("Saving XLSX files (This may take a few minutes for large tables)...")
    
    #เซฟไฟล์จาก .to_csv เป็น .to_excel เพื่อให้ได้ไฟล์สกุล .xlsx ทั้งหมด
    customers.to_excel(RAW_DIR / "customers.xlsx", index=False)
    products.to_excel(RAW_DIR / "products.xlsx", index=False)
    orders.to_excel(RAW_DIR / "orders.xlsx", index=False)
    order_items.to_excel(RAW_DIR / "order_items.xlsx", index=False)
    returns.to_excel(RAW_DIR / "returns.xlsx", index=False)
    inventory.to_excel(RAW_DIR / "inventory.xlsx", index=False)
    promotions.to_excel(RAW_DIR / "promotions.xlsx", index=False)
    thai_events.to_excel(RAW_DIR / "thai_events.xlsx", index=False)

# ============================================================
# 10. DATA VALIDATION
# ============================================================
def validate_data(customers, products, orders, order_items, returns, inventory, promotions, thai_events):
    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)
    print("Customers:", len(customers))
    print("Products:", len(products))
    print("Orders:", len(orders))
    print("Order Items:", len(order_items))
    print("Returns:", len(returns))
    print("Inventory:", len(inventory))
    print("Promotions:", len(promotions))
    print("Thai Events:", len(thai_events))
    print("\nData validation completed.")

# ============================================================
# MAIN
# ============================================================
def main():
    print("\n" + "=" * 60)
    print("THAI RETAIL INTELLIGENCE")
    print("Synthetic E-Commerce Dataset Generator")
    print("=" * 60 + "\n")

    customers = generate_customers()
    products = generate_products()
    promotions = generate_promotions()
    thai_events = generate_thai_events()
    orders = generate_orders(customers, promotions, thai_events)
    order_items = generate_order_items(orders, products)
    returns = generate_returns(order_items, orders)
    inventory = generate_inventory(products, order_items)

    save_data(customers, products, orders, order_items, returns, inventory, promotions, thai_events)
    validate_data(customers, products, orders, order_items, returns, inventory, promotions, thai_events)

    print("\n" + "=" * 60)
    print("DATA GENERATION COMPLETED!")
    print("=" * 60 + "\n")
    print("Files saved to:")
    print(RAW_DIR)

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    main()