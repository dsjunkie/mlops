import os
import mlflow
import datarobot as dr
import pandas as pd

# MLflow setup
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("KE HEALTH CONSULTATION PRICING")  # Explicitly set the desired experiment

# DataRobot API setup
DATAROBOT_API_TOKEN = os.environ.get("DATAROBOT_API_TOKEN", "Njc0NzY3Y2UzMjhhOWJiZTA4MzViYzc5Okw4YWFLeTIyVVI0Mm0veWN4elkrSDlkTjRlaXRlcTNoOHUrSnZ4anhRL289")
DATAROBOT_ENDPOINT = 'https://app.eu.datarobot.com/api/v2'

if not DATAROBOT_API_TOKEN:
    raise ValueError("DataRobot API token is not set. Please set it in the environment.")

# Connect to DataRobot
dr.Client(endpoint=DATAROBOT_ENDPOINT, token=DATAROBOT_API_TOKEN)

# Fetch the project
project_id = '6614d0f2a239817eb2fd1f89'
project = dr.Project.get(project_id)

# Get the top model
top_model = project.get_top_model(metric='Gamma Deviance')
print(f"Top model: {top_model}")

# Retrieve model metrics
model_metrics = top_model.metrics

with mlflow.start_run(run_name='Top_Model_Run'):
    # 1. Log relevant regression metrics
    regression_metrics = ["Gamma Deviance","RMSE", "MAE", "R Squared"]
    for metric_name in regression_metrics:
        metric_data = model_metrics.get(metric_name)
        if metric_data and "validation" in metric_data:
            value = metric_data["validation"]
            mlflow.log_metric(metric_name, value)
            print(f"Logged metric: {metric_name} -> {value}")

    # 2. Log model metadata
    mlflow.log_param("model_type", top_model.model_type)
    mlflow.log_param("project_id", project_id)
    mlflow.log_param("blueprint_id", top_model.blueprint_id)

    # 3. Log feature importance
    feature_importance = top_model.get_or_request_feature_impact()
    importance_df = pd.DataFrame(feature_importance)
    importance_csv = "feature_importance.csv"
    importance_df.to_csv(importance_csv, index=False)
    mlflow.log_artifact(importance_csv)
    print("Logged feature importance.")

    # 4. Log blueprint using project API
    # blueprints = project.get_blueprints()  # Get all blueprints
    # blueprint_info = [bp for bp in blueprints if bp['id'] == top_model.blueprint_id]
    # if blueprint_info:
    #     blueprint_filepath = "blueprint.json"
    #     with open(blueprint_filepath, "w") as f:
    #         json.dump(blueprint_info[0], f, indent=4)
    #     mlflow.log_artifact(blueprint_filepath)
    #     print("Logged blueprint information.")
    # else:
    #     print("Blueprint not found for the top model.")

    # 5. Log leaderboard
    leaderboard = project.get_models()
    leaderboard_df = pd.DataFrame([
        {"model_id": model.id, "model_type": model.model_type, "Gamma Deviance": model.metrics["Gamma Deviance"]["validation"]}
        for model in leaderboard
    ])
    leaderboard_csv = "leaderboard.csv"
    leaderboard_df.to_csv(leaderboard_csv, index=False)
    mlflow.log_artifact(leaderboard_csv)
    print("Logged leaderboard.")

    scoring_code_filepath = f"{top_model.id}_scoring_code.zip"
    try:
        top_model.download_scoring_code(scoring_code_filepath)
        mlflow.log_artifact(scoring_code_filepath)
        print("Logged model scoring code.")
    except Exception as e:
        print(f"Error downloading scoring code: {e}")

    # 7. Log serialized model (if available)
    try:
        model_filepath = f"{top_model.id}_model.pkl"
        top_model.download_model(model_filepath)
        mlflow.log_artifact(model_filepath)
        print("Logged serialized model.")
    except Exception as e:
        print(f"Error downloading serialized model: {e}")

    print("Metrics, artifacts, and metadata logged to MLflow.")