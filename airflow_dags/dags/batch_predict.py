from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import joblib
import os


def run_batch_prediction():
    input_path = "/opt/airflow/data/batch_input.csv"
    output_path = "/opt/airflow/data/predictions.csv"
    model_path = "/opt/airflow/models/final_model.pkl"

    df = pd.read_csv(input_path)
    model = joblib.load(model_path)

    preds = model.predict(df)
    df["predicted_price"] = preds
    df.to_csv(output_path, index=False)
    print(f"✅ Predikció kész, elmentve: {output_path}")


with DAG(
    dag_id="batch_price_prediction",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["airbnb", "batch"],
) as dag:

    predict_task = PythonOperator(
        task_id="run_batch_prediction",
        python_callable=run_batch_prediction,
    )

    predict_task
