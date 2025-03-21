import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

def get_service(credentials):
    """Google Sheets API 서비스 객체를 생성합니다."""
    return build('sheets', 'v4', credentials=credentials)

def get_sheet_data(credentials, spreadsheet_id, range_name):
    """구글 시트에서 데이터를 가져옵니다."""
    try:
        service = get_service(credentials)
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        if not values:
            return pd.DataFrame()
        
        # 첫 번째 행을 컬럼으로 사용하여 DataFrame 생성
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
    
    except Exception as e:
        print(f"Error fetching sheet data: {e}")
        return pd.DataFrame()

def append_sheet_data(credentials, spreadsheet_id, range_name, values):
    """구글 시트에 데이터를 추가합니다."""
    try:
        service = get_service(credentials)
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        return True
    
    except Exception as e:
        print(f"Error appending sheet data: {e}")
        return False

def update_sheet_data(credentials, spreadsheet_id, range_name, values):
    """구글 시트의 데이터를 업데이트합니다."""
    try:
        service = get_service(credentials)
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        return True
    
    except Exception as e:
        print(f"Error updating sheet data: {e}")
        return False

def get_equipment_status():
    """설비 상태 데이터를 가져옵니다."""
    # 구현 필요
    pass

def get_error_history():
    """오류 이력 데이터를 가져옵니다."""
    # 구현 필요
    pass

def get_maintenance_schedule():
    """유지보수 일정 데이터를 가져옵니다."""
    # 구현 필요
    pass

def add_error_record(data):
    """오류 기록을 추가합니다."""
    # 구현 필요
    pass

def update_equipment_status(equipment_id, status):
    """설비 상태를 업데이트합니다."""
    # 구현 필요
    pass 