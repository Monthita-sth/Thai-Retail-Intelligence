# 🛒 Thai Retail Intelligence: End-to-End E-Commerce Data Analytics

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

## 📌 Project Overview
โปรเจกต์นี้เป็นระบบ **End-to-End Data Analytics** ที่จำลองข้อมูลธุรกิจค้าปลีกและ E-Commerce ขนาดใหญ่ในประเทศไทย โดยดึงข้อมูลดิบจากไฟล์เอกสารมาผ่านกระบวนการทำความสะอาด จัดโครงสร้างฐานข้อมูล วิเคราะห์พฤติกรรมลูกค้า และใช้ Machine Learning (Deep Learning) ในการพยากรณ์ยอดขายล่วงหน้า เพื่อนำเสนอผ่าน Interactive Dashboard ที่ตอบโจทย์การตัดสินใจทางธุรกิจ (Business-Oriented) 

โปรเจกต์นี้ถูกพัฒนาขึ้นเพื่อแสดงทักษะด้าน **Data Analysis** ตั้งแต่การจัดการ Data Pipeline ไปจนถึงการออกแบบ Dashboard เพื่อเตรียมพร้อมสำหรับการประยุกต์ใช้ในสภาพแวดล้อมธุรกิจจริง

## 🎯 Business Questions Answered
- สุขภาพของธุรกิจโดยรวมเป็นอย่างไร? ยอดขาย กำไร และอัตรากำไร (Margin) เติบโตไปในทิศทางใด?
- สินค้าใดคือสินค้าทำเงิน (High Revenue & High Margin) และสินค้าใดที่กำลังเป็นภาระ?
- ลูกค้ากลุ่มหลักคือใคร มาจากช่องทางใด และแคมเปญโปรโมชันใด (เช่น 11.11, 12.12) ที่สร้างผลกำไรได้จริง?
- แนวโน้มความต้องการสินค้าในอีก 30 วันข้างหน้าจะเป็นอย่างไร?
- สินค้าใดอยู่ในสภาวะสต็อกวิกฤต (Critical Stock) ที่ต้องการการสั่งซื้อด่วน?

## ⚙️ Architecture & Workflow
กระบวนการทำงานถูกออกแบบตามมาตรฐานอุตสาหกรรม โดยมีการปรับปรุงเครื่องมือให้เหมาะสมกับ Environment เพื่อความรวดเร็วและมีประสิทธิภาพสูงสุด:

1. **Data Ingestion:** โหลดข้อมูลดิบ (Raw Data) รูปแบบ `.xlsx` จำนวนหลักล้านบรรทัด เข้าสู่ระบบฐานข้อมูล **SQLite** 
2. **Data Transformation (SQL):** ใช้ **CTE (Common Table Expressions)** เขียนคำสั่ง SQL แปลงข้อมูลให้อยู่ในโครงสร้าง **Star Schema** (Fact & Dimension Tables)
3. **Exploratory Data Analysis (EDA):** ใช้ **Jupyter Notebook** และ **Pandas** สำรวจข้อมูลเบื้องต้นและพล็อตกราฟหา Insight 
4. **ETL Pipeline:** ใช้ **Pandas** ดึงข้อมูลยอดขาย ทำความสะอาด และ Aggregate ข้อมูลเป็นรายวัน (Daily Sales) เตรียมพร้อมสำหรับทำโมเดล 
5. **Demand Forecasting (AI):** สร้างโมเดล **LSTM ด้วย TensorFlow** เรียนรู้ข้อมูลอดีตเพื่อทำนายยอดขายในอีก 30 วันข้างหน้า
6. **Data Visualization:** นำข้อมูลทั้งหมดมาผูก Data Model และเขียนสูตร **DAX** สร้าง Dashboard 5 หน้าผ่าน **Power BI**

## 📊 Dashboard Previews

<!--### 1. Executive Overview
หน้าสรุปภาพรวมธุรกิจสำหรับผู้บริหาร ให้เห็น KPI สำคัญ ยอดขายตามภูมิภาค และสัดส่วนรายได้จากแต่ละช่องทาง
![Executive Overview](images/dashboard_page1.png)

### 2. Sales & Product Analysis
วิเคราะห์เจาะลึกสินค้าทำเงินและประเมินประสิทธิภาพของแคมเปญโปรโมชันผ่าน Scatter Plot (Revenue vs Margin)
![Sales and Products](images/dashboard_page2.png)

### 3. Customer Analytics
ทำความเข้าใจพฤติกรรมลูกค้า การกระจายตัวตามช่วงอายุ เพศ และแหล่งที่มาของลูกค้า (Acquisition Source)
![Customer Analytics](images/dashboard_page3.png)

### 4. AI Demand Forecasting
แสดงผลการพยากรณ์ยอดขายล่วงหน้า 30 วัน ด้วยโมเดล LSTM (Deep Learning) เปรียบเทียบกับยอดขายจริง
![Demand Forecasting](images/dashboard_page4.png)

### 5. Inventory & Actionable Recommendation
เปลี่ยน Data ให้เป็น Business Action ด้วยการแจ้งเตือนระดับสต็อก (Critical, Low, Healthy) เพื่อประกอบการตัดสินใจสั่งซื้อ
![Inventory Management](images/dashboard_page5.png)

*(หมายเหตุ: นำภาพหน้าจอ Dashboard จาก Power BI มาบันทึกในชื่อที่ตรงกันและเก็บไว้ในโฟลเดอร์ `images/`)*
-->
## 📂 Project Structure
```text
Thai-Retail-Intelligence/
│
├── config/                 # Configuration files
├── dashboard/              # Power BI (.pbix) files
├── data/
│   ├── raw/                # Raw Excel files (.xlsx)
│   └── processed/          # Transformed CSVs ready for Power BI & AI
├── images/                 # Dashboard screenshots for README
├── models/                 # Saved TensorFlow Keras models (.keras)
├── notebooks/              # Jupyter Notebooks for EDA
├── scripts/                # Python scripts for ETL and Training
│   ├── load_data.py        # Load Excel to SQLite
│   ├── transform_data.py   # SQL Star Schema transformation
│   ├── pandas_etl.py       # Daily sales aggregation
│   └── train_forecast.py   # TensorFlow LSTM training script
└── README.md               # Project documentation