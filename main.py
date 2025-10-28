from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


linear_model = joblib.load('linear_model.joblib')
rf_model = joblib.load('random_forest_model.joblib')


class PredictionRequest(BaseModel):
    brand: str
    location: str
    condition: str
    model_type: str

def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Milan@76",
        database="sneakers_db"
    )

def fetch_data():
    try:
        conn = connect_to_mysql()
        cursor = conn.cursor()
        query = "SELECT brand, location, `condition`, price FROM sneakers"
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sneakers API!"}

@app.get("/sneakers")
def get_sneakers_data():
    df = fetch_data()
    return df.to_dict(orient="records")

@app.get("/dropdown_options")
def get_dropdown_options():
    df = fetch_data()
    return {
        "locations": sorted(df["location"].dropna().unique().tolist()),
        "brands": sorted(df["brand"].dropna().unique().tolist()),
        "conditions": sorted(df["condition"].dropna().unique().tolist())
    }

@app.post("/predict_price")
def predict_price(request: PredictionRequest):
    try:
        input_df = pd.DataFrame([[request.brand, request.location, request.condition]],
                                columns=["brand", "location", "`condition`"])

        if request.model_type == "linear":
            prediction = linear_model.predict(input_df)[0]
        elif request.model_type == "rf":
            prediction = rf_model.predict(input_df)[0]
        else:
            return {"error": "Invalid model_type. Choose 'linear' or 'rf'."}

        return {"predicted_price": round(float(prediction), 2)}
    
    except Exception as e:
        return {"error": f"Prediction failed. Error: {str(e)}"}


@app.get("/dynamic_brand_data")
def get_dynamic_brand_data():
    try:
        conn = connect_to_mysql()
        cursor = conn.cursor()
        query = "SELECT brand, COUNT(*) as count FROM sneakers GROUP BY brand"
        cursor.execute(query)
        data = cursor.fetchall()
        return [{"brand": row[0], "count": row[1]} for row in data]
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()