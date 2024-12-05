FROM apache/airflow:2.2.4
copy requirements.txt .

Run pip install -r requirements.txt
