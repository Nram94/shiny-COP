from io import StringIO
import os
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
import pandas as pd
from pathlib import Path
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

# Function to dynamically create credentials.json from environment variables
def create_credentials_json():
    creds_data = {
        "installed": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "https://connect.posit.cloud/Nram94/content/0191dd86-2aff-45f6-9d62-b52d238372e1"],
        }
    }

    # Write credentials to a JSON file dynamically
    app_dir = Path(__file__).parent
    credentials_file = app_dir / 'credentials.json'
    with open(credentials_file, 'w') as f:
        json.dump(creds_data, f)

    return credentials_file

# Authenticate using PyDrive with dynamically created credentials.json
def authenticate_google_drive():
    create_credentials_json()  # Create credentials file from env variables
    gauth = GoogleAuth()

    # Load credentials from the dynamically generated credentials.json
    gauth.LoadCredentialsFile('credentials.json')
    drive = GoogleDrive(gauth)
    return drive


def save_to_google_drive(file_name, data_frame):
    # Authenticate with Google Drive
    drive = authenticate_google_drive()

    # Convert DataFrame to a CSV format in-memory using StringIO
    csv_buffer = StringIO()
    data_frame.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)  # Move the cursor to the start of the buffer

    # Search for the file in Google Drive to check if it already exists
    query = f"title = '{file_name}' and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()

    if file_list:
        # If the file exists, update it
        print(f"File '{file_name}' exists, updating it.")
        gfile = file_list[0]  # Take the first match
    else:
        # If the file does not exist, create a new one
        print(f"File '{file_name}' does not exist, creating a new file.")
        gfile = drive.CreateFile({'title': file_name})  # Create a new file

    # Set the content of the file from the in-memory CSV
    gfile.SetContentString(csv_buffer.getvalue())  # Upload the CSV content from memory
    gfile.Upload()  # Upload the file to Google Drive

    print(f"Uploaded {file_name} to Google Drive successfully!")