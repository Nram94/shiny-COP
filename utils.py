import os
from dotenv import load_dotenv
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import pandas as pd
from pathlib import Path
from shiny import session
from data_import import INPUTS

def collect_inputs():
    # Initialize an empty list to store the input data
    data = []

    # Collect the main evaluator's details
    evaluator_data = {
        "field": "name_evaluador",
        "value": INPUTS["name_evaluador"].value,
    }
    data.append(evaluator_data)

    evaluator_role = {
        "field": "rol_evaluador",
        "label": INPUTS["rol_evaluador"].label,
        "value": INPUTS["rol_evaluador"].value,
    }
    data.append(evaluator_role)

    evaluated_name = {
        "field": "name_evaluado",
        "label": INPUTS["name_evaluado"].label,
        "value": INPUTS["name_evaluado"].value,
    }
    data.append(evaluated_name)

    cargo_evaluado = {
        "field": "cargo_evaluado",
        "label": INPUTS["cargo_evaluado"].label,
        "value": INPUTS["cargo_evaluado"].value,
    }
    data.append(cargo_evaluado)

    cargo_evaluado_auto = {
        "field": "cargo_evaluado_auto",
        "label": INPUTS["cargo_evaluado_auto"].label,
        "value": INPUTS["cargo_evaluado_auto"].value,
    }
    data.append(cargo_evaluado_auto)

    # Iterate through each cluster to collect their descriptor values
    for cluster_name, cluster_inputs in INPUTS.items():
        if cluster_name.startswith("cluster"):
            for descriptor_name, descriptor_input in cluster_inputs.items():
                descriptor_data = {
                    "field": descriptor_name,
                    "label": descriptor_input.label,
                    "value": descriptor_input.value,
                }
                data.append(descriptor_data)

    # Convert the collected data into a DataFrame
    df = pd.DataFrame(data)
    return df

# Define the path to the .env file
env_path = Path('.') / '.env'

# Load environment variables from the .env file using Path
load_dotenv(dotenv_path=env_path)

# Scopes required for Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    creds = None
    token_path = Path('token.json')  # Using pathlib Path

    if token_path.exists():
        # Load credentials from token.json
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    else:
        # Load credentials from environment variables
        creds_data = {
            "installed": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI")
            }
        }

        # Use OAuth 2.0 flow with credentials from environment variables
        creds = Credentials.from_authorized_user_info(creds_data["installed"], SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    return creds

def upload_to_drive(file_path, file_name):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='text/csv')
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File uploaded to Google Drive with file ID: {file.get('id')}")

def save_to_google_drive(input_data, file_name='responses.csv'):
    try:
        current_timestamp = datetime.now().isoformat()
        input_data["created_at"] = current_timestamp
        input_data["updated_at"] = current_timestamp

        # Create a DataFrame row with the collected input data
        df_row = pd.DataFrame([input_data])

        # Save the CSV temporarily
        temp_csv_path = file_name
        df_row.to_csv(temp_csv_path, index=False)

        # Upload the file to Google Drive
        upload_to_drive(temp_csv_path, file_name)

        # Remove the temporary file
        os.remove(temp_csv_path)


    except Exception as e:
        print(f"Error saving to Google Drive: {e}")
