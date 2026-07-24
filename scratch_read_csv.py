import pandas as pd
import os

file_path = r"c:\my_work\life\2024년 서울시 주거실태조사 마이크로데이터.CSV"

try:
    try:
        df = pd.read_csv(file_path, encoding='cp949', nrows=5)
    except:
        df = pd.read_csv(file_path, encoding='utf-8', nrows=5)
        
    out_path = r"C:\Users\user\Downloads\DMDG_LIVE\columns.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        for col in df.columns:
            f.write(col + "\n")
            
    print(f"Columns written to {out_path}")
except Exception as e:
    print(f"Error: {e}")
