import os
import json
from pyspark.sql.functions import max as max_col, col
from datetime import datetime
import boto3
import re

def get_last_processed_date(spark, mariadb_url, db_properties, logger):
    df_last_date = spark.read.jdbc(mariadb_url, "TB_RE_SALES1", properties=db_properties).select(max_col("Sale_Date").alias("last_date"))
    if df_last_date.head(1):
        logger.info(f"df_last_date.head(1): {df_last_date.head(1)}")
        last_date = df_last_date.collect()[0]["last_date"]
        if last_date is None:
            logger.warning("마지막 처리된 날짜가 None입니다. 기본값을 사용합니다.")
            last_date = "2016-01-02 000000"
    else:
        last_date = "2016-01-02 000000"
    logger.info(f"마지막 처리된 날짜: {last_date}")
    return last_date

def load_last_read_times(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_last_read_times(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

def read_data_from_s3(spark, s3_url, last_date, logger, initial_run=False):
    s3 = boto3.client('s3')
    bucket = s3_url.split('/')[2]
    prefix = '/'.join(s3_url.split('/')[3:])

    last_read_times_file = 'last_read_times.json'
    last_read_times = load_last_read_times(last_read_times_file)

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    new_files = []

    # last_date를 datetime 객체로 변환
    last_date_dt = datetime.strptime(last_date, "%Y-%m-%d %H%M%S")

    logger.info(f"S3 버킷에서 객체 목록 가져오기 완료: {bucket}/{prefix}")
    logger.info(f"last_date_dt: {last_date_dt.strftime('%Y-%m-%d %H%M%S')}")

    if initial_run:
        logger.info("초기 실행이므로 모든 파일을 읽음")
        for obj in response.get('Contents', []):
            file_key = obj['Key']
            logger.info(f"파일 추가 (초기 실행): {file_key}")
            new_files.append(f"s3a://{bucket}/{file_key}")
    else:
        for obj in response.get('Contents', []):
            file_key = obj['Key']
            file_mod_time = obj['LastModified']
            logger.info(f"파일 확인 중: {file_key}, 수정 시간: {file_mod_time}")

            # 파일 이름에서 날짜와 시간 추출
            match = re.search(r'sales_(\d{4}-\d{2}-\d{2})_(\d{6})\.parquet', file_key)
            if match:
                file_date_str = match.group(1) + " " + match.group(2)
                file_date_dt = datetime.strptime(file_date_str, "%Y-%m-%d %H%M%S")
                logger.info(f"파일 날짜 및 시간 추출: {file_date_str}, 변환된 날짜: {file_date_dt.strftime('%Y-%m-%d %H%M%S')}")

                if file_key not in last_read_times or last_read_times[file_key] != file_mod_time.isoformat():
                    if file_date_dt > last_date_dt:
                        new_files.append(f"s3a://{bucket}/{file_key}")
                        last_read_times[file_key] = file_mod_time.isoformat()
                        logger.info(f"새 파일 추가: {file_key}")
                    else:
                        logger.info(f"파일 {file_key}이 최근 처리된 날짜 이후가 아님: {file_date_dt.strftime('%Y-%m-%d %H%M%S')} <= {last_date_dt.strftime('%Y-%m-%d %H%M%S')}")
                else:
                    logger.info(f"파일 {file_key}이 이미 처리되었음: {last_read_times[file_key]}")
            else:
                logger.info(f"파일 {file_key}의 형식을 인식하지 못했습니다. 건너뜀")

    if not new_files and initial_run:
        logger.info("초기 실행 - 모든 파일 읽기 시도")
        df_sales = spark.read.parquet(f"s3a://{bucket}/{prefix}").filter(col("Sale_Date") > last_date)
    elif not new_files:
        logger.info("새로운 파일이 없으므로 빈 DataFrame 반환")
        return spark.createDataFrame([], spark.read.parquet(s3_url).schema)
    else:
        df_sales = spark.read.parquet(*new_files).filter(col("Sale_Date") > last_date)
    
    logger.info("S3에서 새로운 데이터 읽기 완료")
    
    save_last_read_times(last_read_times_file, last_read_times)
    return df_sales

def read_reference_data(spark, mariadb_url, db_properties, logger):
    df_product = spark.read.jdbc(mariadb_url, "TB_PRODUCT", properties=db_properties)
    df_employees = spark.read.jdbc(mariadb_url, "TB_EMPLOYEES", properties=db_properties)
    df_code = spark.read.jdbc(mariadb_url, "TB_CODE", properties=db_properties)
    df_iso = spark.read.jdbc(mariadb_url, "TB_ISO", properties=db_properties)
    logger.info("MariaDB에서 참조 데이터 읽기 완료")
    return df_product, df_employees, df_code, df_iso
