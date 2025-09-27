from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.services.ingest import ingest

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "ingest_arxiv",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_arxiv_papers",
        python_callable=lambda: ingest(category="cs.CL", max_results=2),
    )
