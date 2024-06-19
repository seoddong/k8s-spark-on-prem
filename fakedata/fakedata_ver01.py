import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import random
import os
import re
from datetime import datetime, timedelta
import time

# DB 접속 정보
db_info = {
    'host': '<<k8s-master외부IP>>',
    'port': 30007,
    'user': 'root',
    'password': '자신의 암호 사용하셈셈',
    'database': 'sparkdb'
}

# CSV 파일 경로 설정
employees_csv = 'TB_EMPLOYEES.csv'
product_csv = 'TB_PRODUCT.csv'
sales_csv = 'TB_SALES.csv'
prod_cat_stats_csv = 'Prod_Cat_Stats.csv'

# CSV 파일이 있는 경우 로컬에서 읽기, 없는 경우 DB에서 읽기
if os.path.exists(employees_csv) and os.path.exists(product_csv) and os.path.exists(sales_csv):
    tb_employees = pd.read_csv(employees_csv)
    tb_product = pd.read_csv(product_csv)
    tb_sales = pd.read_csv(sales_csv)
else:
    # SQLAlchemy 엔진 생성
    engine = create_engine(f"mysql+pymysql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}")
    # 테이블 데이터 읽어오기
    tb_employees = pd.read_sql_query("SELECT * FROM TB_EMPLOYEES", engine)
    tb_product = pd.read_sql_query("SELECT * FROM TB_PRODUCT", engine)
    tb_sales = pd.read_sql_query("SELECT * FROM TB_SALES", engine)
    # CSV 파일로 저장
    tb_employees.to_csv(employees_csv, index=False)
    tb_product.to_csv(product_csv, index=False)
    tb_sales.to_csv(sales_csv, index=False)

# Product와 Sales 테이블 조인하여 Prod_Cat_ID별 통계 계산
tb_merged = tb_sales.merge(tb_product, on='Product_ID')
prod_cat_stats = tb_merged.groupby('Prod_Cat_ID').agg({
    'Sales_Revenue': ['min', 'max'],
    'Cost_Price_per_Unit': ['min', 'max'],
    'Selling_Expenses': ['min', 'max']
}).reset_index()

# 컬럼 이름 정리
prod_cat_stats.columns = [
    'Prod_Cat_ID', 
    'Sales_Revenue_Min', 'Sales_Revenue_Max', 
    'Cost_Price_Min', 'Cost_Price_Max', 
    'Selling_Expenses_Min', 'Selling_Expenses_Max'
]
prod_cat_stats.to_csv(prod_cat_stats_csv, index=False)

# faker 라이브러리 설정
fake = Faker()

# py파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))

# 합성 데이터 저장할 폴더 설정
output_dir = os.path.join(current_dir, 'synthetic_sales_data')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 생성할 데이터의 배수 및 파일당 저장 건수 설정
multiplier = 10  # 데이터 배수
records_per_file = 100  # 파일당 저장 건수

# 작업 날짜 범위 설정 (start_date부터 n일 순차적으로)
# start_date = datetime.strptime("2024-05-15", '%Y-%m-%d')  # 시작 날짜 설정
# delta_days = 6  # 10일치 생성하려면 9로 입력
# unique_dates = [start_date + timedelta(days=x) for x in range(delta_days + 1)]
# 오늘 날짜의 데이터만 생성하려면 아래와 같이 설정
start_date = datetime.today()
delta_days = 0
unique_dates = [start_date]

channel_cd_options = ['F01', 'F02', 'F03']

print(f"총 {len(unique_dates)}개의 날짜에 대한 데이터를 처리합니다.")

# Prod_Cat_ID별 통계 데이터 로드
prod_cat_stats = pd.read_csv(prod_cat_stats_csv)

# 합성 데이터 생성 함수
def generate_synthetic_data(date, sales_data_by_date, multiplier):
    synthetic_data = []
    for _ in range(multiplier):  # 입력된 배수만큼 합성 데이터 생성
        for _, row in sales_data_by_date.iterrows():
            new_row = row.copy()

            # Sale_Date 변경
            new_row['Sale_Date'] = date.strftime('%Y-%m-%d')

            # Transaction_ID 생성
            year = new_row['Sale_Date'][:4]
            product_id = tb_product.sample(1)['Product_ID'].values[0]
            if product_id.startswith('B-MAX-CAN'):
                product_code = 'CAN'
            elif product_id.startswith('J-TECH-AirCL'):
                product_code = 'AirCL'
            elif product_id.startswith('T-B-COF'):
                product_code = 'COF'
            else:
                product_code_match = re.search(r'-(\D+)', product_id)
                product_code = product_code_match.group(1) if product_code_match else 'UNK'
            transaction_id_suffix = str(fake.random_int(min=0, max=99999)).zfill(5)
            new_row['Transaction_ID'] = f"{year}{product_code}{transaction_id_suffix}"

            # Employee_ID, Channel_CD, Product_ID 업데이트
            new_row['Employee_ID'] = tb_employees.sample(1)['Employee_ID'].values[0]
            new_row['Channel_CD'] = random.choice(channel_cd_options)
            new_row['Product_ID'] = product_id

            # Prod_Cat_ID에 따른 Sales_Revenue, Cost_Price_per_Unit, Selling_Expenses 값 설정
            prod_cat_id = tb_product[tb_product['Product_ID'] == product_id]['Prod_Cat_ID'].values[0]
            stats = prod_cat_stats[prod_cat_stats['Prod_Cat_ID'] == prod_cat_id].iloc[0]
            new_row['Sales_Revenue'] = random.randint(stats['Sales_Revenue_Min'], stats['Sales_Revenue_Max'])
            new_row['Cost_Price_per_Unit'] = random.randint(stats['Cost_Price_Min'], stats['Cost_Price_Max'])
            new_row['Selling_Expenses'] = random.randint(stats['Selling_Expenses_Min'], stats['Selling_Expenses_Max'])

            synthetic_data.append(new_row)
    return synthetic_data

# 각 날짜별로 합성 데이터 생성 및 저장
for date in unique_dates:
    sales_data_by_date = tb_sales.sample(n=records_per_file, replace=True)
    print(f"{date.strftime('%Y-%m-%d')}에 대한 데이터를 처리합니다.")
    print(f"샘플링된 원본 데이터 수: {len(sales_data_by_date)}")

    synthetic_data = generate_synthetic_data(date, sales_data_by_date, multiplier)

    if len(synthetic_data) == 0:
        print(f"{date.strftime('%Y-%m-%d')}에 대한 합성 데이터가 생성되지 않았습니다.")
        continue

    # 데이터프레임으로 변환
    df_synthetic = pd.DataFrame(synthetic_data)
    print(f"{date.strftime('%Y-%m-%d')}에 대한 생성된 합성 데이터 수: {len(df_synthetic)}")

    # 날짜별로 저장
    num_files = len(df_synthetic) // records_per_file + (1 if len(df_synthetic) % records_per_file > 0 else 0)
    print(f"{date.strftime('%Y-%m-%d')}에 저장될 파일 수: {num_files}")
    for i in range(num_files):
        start_idx = i * records_per_file
        end_idx = start_idx + records_per_file
        output_path = os.path.join(output_dir, f'sales_data_{date.strftime("%Y-%m-%d")}_{i+1}.csv')
        
        # 파일이 이미 존재하면 삭제
        if os.path.exists(output_path):
            os.remove(output_path)
        
        df_synthetic[start_idx:end_idx].to_csv(output_path, index=False)

        if os.path.exists(output_path):
            print(f"{date.strftime('%Y-%m-%d')} 데이터 저장 완료: {output_path}")
        else:
            print(f"{date.strftime('%Y-%m-%d')} 데이터 저장 실패: {output_path}")
        
        time.sleep(1)  # 각 파일 저장 후 1초 대기

print("모든 합성 데이터가 날짜별로 저장됨")
