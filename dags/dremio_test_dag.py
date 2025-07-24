from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from dremio_simple_query.connect import get_token, DremioConnection


def query_dremio():

    ## URL to Login Endpoint
    login_endpoint = "http://10.90.65.61:9047/api/v2/login"
    ## Payload for Login
    payload = {
        "username": "hohyunkim",
        "password": "8HsVT83AdZNc2h3TkYrd"
    }
    ## Get token from API
    token = get_token(uri = login_endpoint, payload = payload)
    ## URL Dremio Software Flight Endpoint
    arrow_endpoint = "grpc://10.90.65.61:32010"
    ## Establish Client
    dremio = DremioConnection(token, arrow_endpoint)
    
    # Run the query and fetch data
    df = dremio.toPandas("SELECT * FROM minio.datalake.vi.agent.parquet;")
    
    # Process data (For example, save to CSV or further analytics)
    df.to_csv("./agent.csv")

# Define the Airflow DAG
with DAG(
    dag_id="dremio_query_dag",
    start_date=datetime(2025, 7, 24),
    #schedule_interval="@daily",  # Runs the query daily
    catchup=False
) as dag:

    # Define the task using PythonOperator
    run_dremio_query = PythonOperator(
        task_id="run_dremio_query",
        python_callable=query_dremio
    )

    run_dremio_query
