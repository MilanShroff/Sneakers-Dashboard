import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Milan@76",
        database="sneakers_db"
    )

def fetch_data():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = "SELECT brand, location, `condition`, price FROM sneakers"
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["brand", "location", "`condition`", "price"])
    cursor.close()
    connection.close()
    return df


df = fetch_data()

X = df[["brand", "location", "`condition`"]]
y = df["price"]

categorical_features = ["brand", "location", "`condition`"]


preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


linear_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

linear_pipeline.fit(X_train, y_train)
y_pred_lr = linear_pipeline.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f"Linear Regression — MSE: {mse_lr:.2f}, R²: {r2_lr:.2f}")


joblib.dump(linear_pipeline, "linear_model.joblib")


rf_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

rf_pipeline.fit(X_train, y_train)
y_pred_rf = rf_pipeline.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest — MSE: {mse_rf:.2f}, R²: {r2_rf:.2f}")


joblib.dump(rf_pipeline, "random_forest_model.joblib")

print("Both models saved successfully!")
