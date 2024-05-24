import logging
import time
import signal
import sys
import os
from datetime import datetime
from ENMVP_setting import setup_logging, get_aws_credentials, create_spark_session
from ENMVP_util import get_last_processed_date, read_data_from_s3, read_reference_data, load_last_read_times
from ENMVP_data import process_data, write_data_to_db

logger = setup_logging()
logger.info("로그 파일 경로 확인")
aws_access_key_id, aws_secret_access_key = get_aws_credentials(logger)

# Global SparkContext variable
spark_context = None

def process_batch(last_batch_time, initial_run=False):
    global spark_context
    batch_start_time = datetime.now()
    logger.info(f"배치 시작 시간: {batch_start_time}")

    spark = create_spark_session(aws_access_key_id, aws_secret_access_key, logger)
    spark_context = spark.sparkContext
    mariadb_url = "jdbc:mysql://34.68.13.64:30007/sparkdb?permitMysqlScheme"
    db_properties = {"driver": "org.mariadb.jdbc.Driver", "user": "root", "password": "tjehdgml"}

    last_date = get_last_processed_date(spark, mariadb_url, db_properties, logger)
    s3_url = "s3a://jolajoayo-spark-0001/sales_*.parquet"
    df_sales = read_data_from_s3(spark, s3_url, last_date, logger, initial_run)
    if df_sales.rdd.isEmpty():
        logger.info("변경된 파일이 없어 데이터를 처리하지 않음")
        return last_batch_time

    df_product, df_employees, df_code, df_iso = read_reference_data(spark, mariadb_url, db_properties, logger)
    
    df_sales.cache()
    df_product.cache()
    df_employees.cache()
    df_code.cache()
    df_iso.cache()
    logger.info("데이터 캐싱 완료")

    df_re_sales = process_data(df_sales, df_product, df_employees, df_code, df_iso, logger)
    write_data_to_db(df_re_sales, mariadb_url, db_properties, logger)

    spark.stop()
    spark_context = None
    logger.info("스파크 세션 종료")

    batch_end_time = datetime.now()
    logger.info(f"배치 종료 시간: {batch_end_time}")
    logger.info(f"배치 처리 시간: {batch_end_time - batch_start_time}")
    return batch_end_time

def signal_handler(signal, frame):
    global spark_context
    program_end_time = datetime.now()
    logger.info(f"프로그램 종료 시간: {program_end_time}")
    logger.info(f"프로그램 총 실행 시간: {program_end_time - program_start_time}")
    if spark_context:
        spark_context.cancelAllJobs()
    sys.exit(0)

def main():
    global program_start_time
    program_start_time = datetime.now()
    logger.info(f"프로그램 시작 시간: {program_start_time}")

    signal.signal(signal.SIGINT, signal_handler)

    last_read_times_file = 'last_read_times.json'
    last_read_times = load_last_read_times(last_read_times_file)
    initial_run = not last_read_times
    last_batch_time = "2016-01-02 000000" # 초기화

    while True:
        try:
            last_batch_time = process_batch(last_batch_time, initial_run)
            initial_run = False
            time.sleep(300) # 5분(300초) 대기
        except KeyboardInterrupt:
            signal_handler(None, None)

if __name__ == "__main__":
    main()
