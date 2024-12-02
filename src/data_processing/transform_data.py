import pandas as pd
from datetime import date
import os
import glob

def transform_data():
    # Define input and output paths
    data_path = 'data/raw'  # Path to raw data
    output_path = 'data/processed'  # Path for processed files

    # Clean up the output folder
    if os.path.exists(output_path):
        files = glob.glob(os.path.join(output_path, '*'))
        for f in files:
            os.remove(f)
        print(f"Cleaned up folder: {output_path}")
    else:
        os.makedirs(output_path)  # Create the folder if it doesn't exist
    
    # List of relevant columns (excluding identifiers)
    relevant_columns = [
        "ClaimCode", "ProviderCode", "PolicyNumber", "Age", "Gender", 
        "AmountBilled", "ReferenceNumber", "DateOfService", "TotalAmount", 
        "Units", "ServiceDate", "ServiceType", "ProviderID", "ProviderType", 
        "ProviderDescription", "ProcedureCode", "ServiceDescription", 
        "Quantity", "UnitPrice", "DiagnosisCode", "SecondaryDiagnosisCode", 
        "DiagnosisDescription", "Source", "Currency", "ClaimDate", 
        "ClaimType", "PreAuthorization", "Timestamp1", "Timestamp2", 
        "Status", "Timestamp3", "icd_code", "icd_title"
    ]
    
    today_year = date.today().year  # Get the current year
    
    print(f"Processing files from: {data_path}")
    
    # List all CSV files in the data_path directory
    files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    if not files:
        print("No CSV files found in the data directory.")
        return
    
    # Process each file
    for file in files:
        file_path = os.path.join(data_path, file)
        print(f"Processing file: {file_path}")
        
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            print(f"File loaded. Columns: {list(df.columns)}")
            
            # Select only the relevant columns
            available_columns = [col for col in relevant_columns if col in df.columns]
            if not available_columns:
                print(f"No relevant columns found in {file}. Skipping.")
                continue
            
            df = df[available_columns]
            
            # Transform `Age` column if it exists
            if "Age" in df.columns:
                df["Age"] = today_year - pd.to_datetime(df["Age"], errors="coerce").dt.year
                print(f"'Age' column transformed in {file}")
            
            # Save the processed file
            output_file = os.path.join(output_path, f"processed_{file}")
            df.to_csv(output_file, index=False)
            print(f"Processed file saved to {output_file}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# Call the function
transform_data()
