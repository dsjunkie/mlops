from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from src.training.mlflow_training import train_with_mlflow
from src.training.datarobot_training import train_with_datarobot