import base64
from data_import import COMPS, WEIGHTS
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
import json
import pandas as pd
import os

def authenticate_google_drive():
    # Load the .env file
    load_dotenv()

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    # Retrieve and decode the base64 credentials
    encoded_credentials = os.getenv('GOOGLE_CREDENTIALS_JSON_BASE64')
    if not encoded_credentials:
        raise ValueError("Missing GOOGLE_CREDENTIALS_JSON_BASE64 environment variable")

    credentials_json = base64.b64decode(encoded_credentials).decode('utf-8')
    creds_dict = json.loads(credentials_json)
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)

    return client

    

def get_workbook():
    client = authenticate_google_drive()
    workbook_id = '1INWYtoIlv9rAM47g8AwcUqiTYPWi6dcxYvMAlBLaLeE'
    workbook = client.open_by_key(workbook_id)
    
    return workbook


def save_to_google_drive(data_frame, worksheet_name):
    workbook = get_workbook()

    # Check if worksheet exists
    worksheet_list = map(lambda x: x.title, workbook.worksheets())
    new_worksheet_name = worksheet_name

    if new_worksheet_name in worksheet_list:
        sheet = workbook.worksheet(new_worksheet_name)
    else:
       sheet = workbook.add_worksheet(new_worksheet_name, rows=100, cols=100)

    # sheet.update([data_frame.columns.values.tolist()] + data_frame.values.tolist())
    # Get existing data from the worksheet
    existing_data = sheet.get_all_values()
    
    # If there are no existing data rows (other than header), write the entire dataframe
    if len(existing_data) <= 1:
        sheet.update([data_frame.columns.values.tolist()] + data_frame.values.tolist())
    else:
        # Keep the header and append the new data below existing rows
        next_row = len(existing_data) + 1
        sheet.update(f'A{next_row}', data_frame.values.tolist())


def load_from_google_drive():
    workbook = get_workbook()
    worskheets = workbook.worksheets()
    
    all_dfs = []
    header = None
    for sheet in worskheets:
        data = sheet.get_all_values()
        if header is None:
            header= data[0]
        
        df = pd.DataFrame(data[1:], columns=header)

        all_dfs.append(df)
    combined_df = pd.concat(all_dfs)

    return combined_df

def load_user_sheet_google_drive(user_name):
    workbook = get_workbook()
    worksheet = workbook.worksheet(user_name)
    df = pd.DataFrame(worksheet.get_all_records())

    return df

def get_worksheet_names():
    workbook = get_workbook()
    worksheet_list = []
    worksheets = workbook.worksheets()
    for sheet in worksheets:
        worksheet_list.append(sheet.title)
    
    return worksheet_list

def calculate_competence_averages(user_name, input_date=None):
    try:
        df_ = load_user_sheet_google_drive(user_name)
        df_['created_at'] = pd.to_datetime(df_['created_at'])

        if input_date != None:
            # Extract month and year from user input
            target_month = input_date.month
            target_year = input_date.year

            df = df_[(df_['created_at'].dt.month == target_month) & (df_['created_at'].dt.year == target_year)]
        else:
            df = df_.copy()
        # Extract relevant columns (those that start with 'cl')
        comp_columns = [col for col in df.columns if col.startswith('cl')]
        df[comp_columns] = df[comp_columns].apply(pd.to_numeric, errors='coerce')

        # Initialize a dictionary to hold weighted sums and weights
        weighted_sums = {}
        weight_totals = {}

        # Loop through all competence columns
        for comp in comp_columns:
            # Extract the competence group (e.g., 'cl1_comp1')
            comp_group = '_'.join(comp.split('_')[:2])

            # If the group is not in the dictionaries, initialize it
            if comp_group not in weighted_sums:
                weighted_sums[comp_group] = 0
                weight_totals[comp_group] = 0

       
            # Loop through each row and apply the corresponding weight
            for i, row in df.iterrows():
                rol_evaluador = row['rol_evaluador']
                weight = WEIGHTS.get(rol_evaluador, 1)  # Default to 1 if no weight is specified

                # # Apply special condition for "Auxiliar"
                # if rol_evaluador == "Auxiliar" and df.columns.get_loc(comp) <= start_col_index:
                #     continue  # Skip columns before 'cl1_comp2_descriptor3' for "Auxiliar"
                # Add the weighted value to the weighted sum
                weighted_sums[comp_group] += row[comp] * weight
                # Add the weight to the total weight sum
                weight_totals[comp_group] += weight

        # Create a dictionary to store the final weighted average for each competence group
        final_averages = {}

        # Calculate the weighted average for each competence group
        for comp_group in weighted_sums:
            final_averages[comp_group] = weighted_sums[comp_group] / weight_totals[comp_group]  # Weighted average formula

        # Create a DataFrame with a single row for the weighted averages
        avg_df = pd.DataFrame([final_averages])
    except Exception as e:
        #  print(e)
        
         avg_df = pd.DataFrame()
    
    
    
    return avg_df


