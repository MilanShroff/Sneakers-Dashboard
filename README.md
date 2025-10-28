# 🏀 Sneakers Dashboard — End-to-End Data & ML Project

## 📌 Overview
The **Sneakers Dashboard** is a full-stack data project that scrapes sneaker listings from **eBay**, stores them in a **MySQL** database, trains **machine learning models** to predict prices, and visualizes insights in an **interactive dashboard** powered by **FastAPI** and **Plotly.js**.

This project combines **web scraping**, **data storage**, **machine learning**, and **web visualization** — making it a complete real-world pipeline from raw data to actionable insights.

---

## ⚙️ Features
✅ **Web Scraping:** Extracts sneaker data from eBay (title, price, brand, location, condition, shipping cost).  
✅ **Data Cleaning:** Automatically identifies brand names, cleans numeric fields, and standardizes missing data.  
✅ **MySQL Integration:** Stores all unique listings with duplicate prevention.  
✅ **Machine Learning Models:**  
   - Linear Regression  
   - Random Forest Regressor  
✅ **Interactive Dashboard:**  
   - Brand & location-based bar and pie charts  
   - Live sneaker data table  
   - Dynamic price prediction tool (select brand, location, and condition)  
✅ **Real-time Updates:** Dashboard charts update dynamically every 5 seconds.  

---

## 🧩 Project Structure
Sneakers-Dashboard/
│
├── Beautiful.py # Scrapes eBay sneaker listings (XPath-based)
├── saving.py # Creates MySQL table & saves scraped data
├── predict.py # Trains and saves ML models (Linear, Random Forest)
├── main.py # FastAPI backend serving API & predictions
├── front.html # Interactive dashboard (frontend)
├── linear_model.joblib # Saved Linear Regression model
├── random_forest_model.joblib # Saved Random Forest model
└── README.md

---

## 🧠 Workflow Diagram

eBay → Beautiful.py → MySQL Database → predict.py → ML Models
↓ ↓
Dashboard (front.html) ← FastAPI (main.py) ← Predictions & Data

---

## 🧱 Technologies Used
| Category | Tools |
|-----------|--------|
| **Scraping** | lxml, requests |
| **Database** | MySQL, mysql-connector-python |
| **Backend** | FastAPI |
| **Frontend** | HTML, CSS, JavaScript, Plotly.js |
| **Machine Learning** | scikit-learn, pandas, joblib |
| **Data Storage** | MySQL tables with duplicate prevention |

---

## 🚀 How to Run the Project

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/MilanShroff/Sneakers-Dashboard.git
cd Sneakers-Dashboard
```
2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Setup MySQL Database

Open MySQL and create a database:
```bash
CREATE DATABASE sneakers_db;
```
Edit your MySQL credentials inside saving.py, predict.py, and main.py if needed.

4️⃣ Scrape Data
python Beautiful.py
This will scrape sneaker listings from eBay (up to 30 pages).

5️⃣ Save Data to Database
python saving.py
6️⃣ Train the Models
python predict.py
This will train and save:

linear_model.joblib

random_forest_model.joblib

7️⃣ Run FastAPI Server
FastAPI will start at http://127.0.0.1:8000

8️⃣ Open Dashboard

Open front.html in your browser.

You’ll see:

Dropdowns for brand, location, condition, model

A Predict Price button

Dynamic charts and sneaker data table

📊 API Endpoints
Endpoint	Method	Description
/	GET	Welcome message
/sneakers	GET	Returns all sneaker data
/dropdown_options	GET	Returns unique dropdown options
/predict_price	POST	Predicts price for selected inputs
/dynamic_brand_data	GET	Returns live brand frequency data
📈 Example Output
Linear Regression — MSE: 62.45, R²: 0.79
Random Forest — MSE: 40.23, R²: 0.87
Both models saved successfully!
Total items scraped: 740
🧑‍💻 Future Improvements

Integrate real-time eBay API updates

Deploy FastAPI backend to Render or AWS EC2

Add more ML algorithms (XGBoost, CatBoost)

Build a login & filtering interface for users

Host the dashboard via Streamlit or React frontend

🏆 Author

Milan Shroff
📧 milanshroff2@gmail.com

📜 License

This project is open-source under the MIT License.

🌟 If you like this project, please ⭐ the repository!
