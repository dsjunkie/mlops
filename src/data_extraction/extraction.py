import os 
from jinja2 import Template
from dotenv import load_dotenv
import pandas as pd
import requests

api_key = os.getenv('WHO_API_KEY')
api_secret = os.getenv('WHO_API_SECRET')


def get_icd_details(diag_code, api_key, api_secret):
    base_url = 'https://id.who.int/icd/release/10/2021'
    headers = {
        'Accept': 'application/json',
        'API-Version': 'v2',
        'Authorization': f'Bearer {api_key}'
    }
    url = f'{base_url}/{diag_code}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        icd_code = data.get('code', diag_code)
        icd_title = data.get('title', {}).get('@value', '')
        return icd_code, icd_title
    else:
        return diag_code, ''

def extract_data_for_service(service_type_code, api_key, api_secret):
    df = pd.read_csv('synthetic_healthcare_claims.csv')
    service_df = df[df['ProviderType'] == service_type_code]

    unique_diag_codes = service_df['DiagnosisCode'].unique()
    icd_details_map = {}
    for code in unique_diag_codes:
        icd_code, icd_title = get_icd_details(code, api_key, api_secret)
        icd_details_map[code] = {'icd_code': icd_code, 'icd_title': icd_title}

    service_df['icd_code'] = service_df['DiagnosisCode'].map(lambda x: icd_details_map[x]['icd_code'])
    service_df['icd_title'] = service_df['DiagnosisCode'].map(lambda x: icd_details_map[x]['icd_title'])

    output_file = f'data/raw/{service_type_code}_claims.csv'
    service_df.to_csv(output_file, index=False)
    print(f"Data extracted for {service_type_code} and saved to {output_file}")



service_types = ['CON', 'MED', 'PROC', 'SUN', 'INV']
for service_type in service_types:
    extract_data_for_service(service_type, api_key, api_secret)

