import pandas as pd
import sys

file_path = r"c:\my_work\life\2024년 서울시 주거실태조사 코드북.xlsx"

try:
    # Read all sheets
    excel_data = pd.read_excel(file_path, sheet_name=None)
    print(f"--- 엑셀 파일 로드 성공: {file_path} ---")
    print(f"시트 목록: {list(excel_data.keys())}\n")
    
    for sheet_name, df in excel_data.items():
        print(f"=== 시트명: {sheet_name} ===")
        print(f"행 개수: {len(df)}, 열 개수: {len(df.columns)}")
        print("컬럼 목록:")
        print(list(df.columns))
        print("첫 5행 데이터:")
        print(df.head())
        print("\n" + "="*40 + "\n")
        
except Exception as e:
    print(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
