from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime

def analyze():
    print("Data analysis complete. Model performance looks good.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 22),
}

with DAG(
    dag_id='process_iris',
    default_args=default_args,
    schedule_interval='0 1 22-24 4 *',
    catchup=True,
    tags=['example'],
    description='A simple Iris model DAG',
) as dag:

    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='echo "Running dbt..."'
    )

    train_model = BashOperator(
        task_id='train_model',
        bash_command='echo "Training model..."'
    )

    analyze_data = PythonOperator(
        task_id='analyze_data',
        python_callable=analyze
    )

    notify = EmailOperator(
        task_id='notify',
        to='airflow@example.com',
        subject='Iris model pipeline finished',
        html_content='<p><strong>The DAG has completed successfully.</strong></p>'
    )

    run_dbt >> train_model >> analyze_data >> notify
