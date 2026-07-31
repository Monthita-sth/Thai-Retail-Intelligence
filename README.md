# 🛒 Thai Retail Intelligence: End-to-End E-Commerce Data Analytics

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

## 📌 Project Overview
โปรเจกต์นี้เป็นระบบ **End-to-End Data Analytics** ที่จำลองข้อมูลธุรกิจค้าปลีกและ E-Commerce ขนาดใหญ่ในประเทศไทย โดยดึงข้อมูลจากไฟล์ข้อมูลดิบ (Raw Data) มาผ่านกระบวนการทำความสะอาด จัดโครงสร้างฐานข้อมูล วิเคราะห์พฤติกรรมลูกค้า และใช้ Machine Learning (Deep Learning) ในการพยากรณ์ยอดขายล่วงหน้า เพื่อนำเสนอผ่าน Interactive Dashboard ที่ตอบโจทย์การตัดสินใจทางธุรกิจ (Business-Oriented) 

โปรเจกต์นี้ถูกพัฒนาขึ้นเพื่อแสดงทักษะด้าน **Data Analysis** ตั้งแต่การจัดการ Data Pipeline ไปจนถึงการออกแบบ Dashboard เพื่อเตรียมพร้อมสำหรับการประยุกต์ใช้ในสภาพแวดล้อมธุรกิจจริง

***🛠️ Core Tech Stack:** Python, Pandas, SQLite, SQL, TensorFlow, Power BI, Git*

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

### 1. Executive Overview
หน้าสรุปภาพรวมธุรกิจสำหรับผู้บริหาร ให้เห็น KPI สำคัญ ยอดขายตามภูมิภาค และสัดส่วนรายได้จากแต่ละช่องทาง
<!-- ![Executive Overview](images/dashboard_page1.png) -->

### 2. Sales, Product & Campaign
วิเคราะห์เจาะลึกสินค้าทำเงินและประเมินประสิทธิภาพของแคมเปญโปรโมชันผ่าน Scatter Plot (Revenue vs Margin)
<!-- ![Sales and Products](images/dashboard_page2.png) -->

### 3. Customer Analytics
ทำความเข้าใจพฤติกรรมลูกค้า การกระจายตัวตามช่วงอายุ เพศ และแหล่งที่มาของลูกค้า (Acquisition Source)
<!-- ![Customer Analytics](images/dashboard_page3.png) -->

### 4. AI Demand Forecasting
แสดงผลการพยากรณ์ยอดขายล่วงหน้า 30 วัน ด้วยโมเดล LSTM (Deep Learning) เปรียบเทียบกับยอดขายจริง
<!-- ![Demand Forecasting](images/dashboard_page4.png) -->

### 5. Inventory & Actionable Recommendation
เปลี่ยน Data ให้เป็น Business Action ด้วยการแจ้งเตือนระดับสต็อก (Critical, Low, Healthy) เพื่อประกอบการตัดสินใจสั่งซื้อ
<!-- ![Inventory Management](images/dashboard_page5.png) -->

*(หมายเหตุ: รูปภาพ Dashboard จะถูกอัปเดตในภายหลังเมื่อการออกแบบเสร็จสมบูรณ์)*

## 📂 Project Structure
```text
Thai-Retail-Intelligence/
│
├── config/                 # Configuration files
├── dashboard/              # Power BI (.pbix) files (Will be added)
├── data/
│   ├── external/           # External data sources
│   ├── processed/          # Transformed CSVs ready for Power BI & AI
│   ├── raw/                # Raw Excel files (.xlsx)
│   └── retail_db.sqlite    # SQLite Database
├── images/                 # Dashboard screenshots for README
├── models/                 
│   └── sales_lstm.keras    # Saved TensorFlow LSTM model
├── notebooks/              # Jupyter Notebooks for EDA
├── scripts/                # Python scripts for ETL and Training
│   ├── pyspark_etl.py      # Daily sales aggregation (Pandas implementation)
│   └── train_forecast.py   # TensorFlow LSTM training script
├── src/                    # Source code for data pipelines
│   ├── data_generation/    
│   │   └── generate_data.py   # Script to pull and format raw retail data (.xlsx)
│   └── database/           
│       ├── export_to_powerbi.py # Export processed tables to CSV
│       ├── load_data.py       # Load Excel to SQLite
│       └── transform_data.py  # SQL Star Schema transformation
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
## 🚀 How to Run the Project
### 1.Clone the repository:
`git clone [https://github.com/Monthita-sth/Thai-Retail-Intelligence.git](https://github.com/Monthita-sth/Thai-Retail-Intelligence.git)`

### 2.Install dependencies:
`pip install pandas sqlite3 matplotlib seaborn tensorflow scikit-learn`

### 3.Execute the Data Pipeline in order:
`python src/data_generation/generate_data.py 
python src/database/load_data.py
python src/database/transform_data.py
python src/database/export_to_powerbi.py
python scripts/pyspark_etl.py
python scripts/train_forecast.py`

### 4.View Dashboard:
Open dashboard/Thai_Retail_Dashboard.pbix in Power BI Desktop.

### 👨‍💻 Author: Monthita Songthong
* #### 🎓 Education: 4rd Year Computer Science Student, Faculty of Science, Prince of Songkla University
#### 📫 Connect: 
* #### Email: monthita.sth@gmail.com
* #### LinkedIn: linkedin.com/in/your-profile (ยังไม่มี)
* #### GitHub: [github.com/Monthita-sth](https://github.com/Monthita-sth)