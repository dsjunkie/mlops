import os 
import mlflow
import datarobot as dr
import pandas as pd


print("Tracking URI:", mlflow.get_tracking_uri())


mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("CLAIMS EXPERIMENT")

DATAROBOT_API_TOKEN = os.environ.get("DATAROBOT_API_TOKEN")
DATAROBOT_ENDPOINT = 'https://app.eu.datarobot.com/api/v2'


# def train_and_log_model(service_file, service_name):
#     """ Train and log models for each service type"""
#     with mlflow.start_run(run_name = f"{service_name}_model"):
#         file_path = os.path.join('data/processed', service_file)
#         df = pd.read_csv(file_path)

#         mlflow.log_param("service_name", service_name)
#         mlflow.log_param('num_rows', df.shape[0])
#         mlflow.log_param('num_cols', df.shape[1])

#         dr.Client(endpoint = DATAROBOT_ENDPOINT, token =DATAROBOT_API_TOKEN)

#         project = dr.Project.create(
#             sourcedata = file_path,
#             project_name = f"{service_name.capitalize()} Claims Model"
#         )

#         project.set_target(
#             target = "AmountBilled", 
#             worker_count = -1, 
#             mode = dr.AUTOPILOT_MODE.QUICK
#         )

#         model = project.get_top_model()

#         metrics = model.get_metrics()
#         gamma = metrics['Gamma Deviance']
#         mlflow.log_metrics(gamma)

#         model_filepath = f"models/{service_name}_model.pkl"
#         model.download(model_filepath)

#         mlflow.log_artifact(model_filepath)

#         # os.system(f'dvc add {model_filepath}')
#         # os.system('git add models/.gitignore models/{service_name}_model.pkl.dvc')
#         # os.system(f'git commit -m "Add trained model for {service_name}"')

# def main():

# #iterate over service categories. 
#     processed_path = 'data/processed/'
#     for file_name in os.listdir(processed_path):
#         if file_name.endswith('.csv'):
#             service_name = file_name.split('_')[1]
#             train_and_log_model(file_name, service_name)

# if __name__ == "__main__":
#     main()

dr.Client(endpoint = DATAROBOT_ENDPOINT, token =DATAROBOT_API_TOKEN)
project = dr.Project.get('6750a8c05752f6c76b8418b3')


top_model = project.get_top_model(metric='RMSE')
print(top_model)

# Retrieve model parameters
model_params = top_model.get_parameters()

# Retrieve model metrics
model_metrics = top_model.metrics

with mlflow.start_run(run_name='Top_Model_Run'):
    for metric_name, metric_data in model_metrics.items():
        # Log validation metrics to MLflow if available
        if isinstance(metric_data, dict) and "validation" in metric_data:
            mlflow.log_metric(metric_name, metric_data["validation"])
            print(f"Logged {metric_name}: {metric_data['validation']}")

    # Log model metadata
    mlflow.log_param("model_type", top_model.model_type)
    mlflow.log_param("project_id", project)

    print(f"Logged metrics for model: {top_model}")