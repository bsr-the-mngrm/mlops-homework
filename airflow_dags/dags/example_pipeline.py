from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def print_hello():
    print("✅ Predikciós pipeline futott!")


default_args = {
    "owner": "airbnb",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="airbnb_prediction_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["airbnb"],
) as dag:

    hello_task = PythonOperator(
        task_id="log_hello_message",
        python_callable=print_hello,
    )

    hello_task
