import logging
import time
import signal
import sys
import os
from datetime import datetime
from ENMVP_setting import setup_logging, get_aws_credentials, create_spark_session, mariadb_url, db_properties, s3_url
from ENMVP_util import get_last_processed_date, read_data_from_s3, read_reference_data, load_last_read_times, save_last_read_times
from ENMVP_data import process_data, write_data_to_db

logger = setup_logging()
logger.info("로그 파일 경로 확인")
aws_access_key_id, aws_secret_access_key = get_aws_credentials(logger)

# Global SparkContext variable
spark = None

# 배치 주기 설정 (초 단위)
BATCH_INTERVAL = 30

def process_batch(last_batch_time, initial_run=False):
    global spark
    batch_start_time = datetime.now()
    logger.info(f"배치 시작 시간: {batch_start_time}")

    if spark is None:
        spark = create_spark_session(aws_access_key_id, aws_secret_access_key, logger)

    last_read_times_file = 'last_read_times.json'
    last_read_times = load_last_read_times(last_read_times_file)

    last_date = get_last_processed_date(spark, logger)
    
    # last_date가 문자열인지 확인
    if isinstance(last_date, datetime):
        last_date_str = last_date.strftime("%Y-%m-%d %H%M%S")
    else:
        last_date_str = last_date  # 기본값일 경우 문자열 사용

    df_sales, last_read_times = read_data_from_s3(spark, last_date_str, logger, last_read_times, initial_run)
    if df_sales.rdd.isEmpty():
        logger.info("변경된 파일이 없어 데이터를 처리하지 않음")
        return last_batch_time

    df_product, df_employees, df_code, df_iso = read_reference_data(spark, logger)
    logger.info(f"참조 데이터 읽기 완료: 제품({df_product.count()}), 직원({df_employees.count()}), 코드({df_code.count()}), ISO({df_iso.count()})")
    
    df_sales.cache()
    df_product.cache()
    df_employees.cache()
    df_code.cache()
    df_iso.cache()
    logger.info("데이터 캐싱 완료")

    df_re_sales = process_data(df_sales, df_product, df_employees, df_code, df_iso, logger)
    write_data_to_db(df_re_sales, mariadb_url, db_properties, logger)

    save_last_read_times(last_read_times_file, last_read_times)

    logger.info("스파크 세션 유지")
    
    batch_end_time = datetime.now()
    logger.info(f"배치 종료 시간: {batch_end_time}")
    logger.info(f"배치 처리 시간: {batch_end_time - batch_start_time}")
    return batch_end_time

def signal_handler(signal, frame):
    global spark
    program_end_time = datetime.now()
    logger.info(f"프로그램 종료 시간: {program_end_time}")
    logger.info(f"프로그램 총 실행 시간: {program_end_time - program_start_time}")
    if spark:
        spark.stop()
    sys.exit(0)

def main():
    global program_start_time
    program_start_time = datetime.now()
    logger.info(f"프로그램 시작 시간: {program_start_time}")

    signal.signal(signal.SIGINT, signal_handler)

    last_read_times_file = 'last_read_times.json'
    last_read_times = load_last_read_times(last_read_times_file)
    initial_run = not bool(last_read_times)  # last_read_times가 비어있으면 True, 아니면 False

    last_batch_time = "2016-01-02 000000"  # 초기화

    while True:
        try:
            last_batch_time = process_batch(last_batch_time, initial_run)
            initial_run = False
            remaining_time = BATCH_INTERVAL
            while remaining_time > 0:
                if remaining_time > 5:
                    logger.info(f"배치 대기 중: {remaining_time}초 남음")
                    time.sleep(5)
                    remaining_time -= 5
                else:
                    logger.info(f"배치 대기 중: {remaining_time}초 남음")
                    time.sleep(1)
                    remaining_time -= 1
        except KeyboardInterrupt:
            signal_handler(None, None)

if __name__ == "__main__":
    main()
