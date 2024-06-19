# MVPSS_main.py

from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from MVPSS_setting import setup_logging, get_aws_credentials, create_spark_session, schema, s3_url, mariadb_url, db_properties
from MVPSS_data import read_and_cache_reference_tables, create_df_sales, write_table_to_mariadb

# 로깅 설정
logger = setup_logging()
logger.info("로그 파일 경로 확인")
aws_access_key_id, aws_secret_access_key = get_aws_credentials(logger)

# Spark 세션 생성
spark = create_spark_session(aws_access_key_id, aws_secret_access_key, logger)

# 참조 테이블 읽기 및 캐싱
df_product, df_employees, df_code, df_iso = read_and_cache_reference_tables(spark, mariadb_url, db_properties, logger)

# 스트리밍 데이터 읽기
streaming_df = spark.readStream \
    .schema(schema) \
    .format("parquet") \
    .load(s3_url) \
    .select("*", "_metadata.file_name")

# 스트리밍 데이터 처리
processed_df = streaming_df.withColumn("Processed_Time", expr("CURRENT_TIMESTAMP"))
 
# df_sales 생성
# 조인을 밖에서 처리하면 나름의 장단점이 있다.
df_sales = create_df_sales(processed_df, df_product, df_employees, df_code, df_iso, logger)

# df_sales를 MariaDB에 저장
def foreach_batch_function(df, epoch_id):
    file_names = df.select("file_name").distinct().collect()
    file_names_str = ", ".join(set([file.file_name for file in file_names]))

    # file_name 컬럼을 제외한 DataFrame 생성
    df_without_file_name = df.drop("file_name")
    
    write_table_to_mariadb(df_without_file_name, "TB_RE_SALES", mariadb_url, db_properties, logger)
    batch_end_time = datetime.now()
    logger.info(f"Epoch {epoch_id} 종료 시간: {batch_end_time}, 파일명: {file_names_str}")

query = df_sales.writeStream \
    .outputMode("append") \
    .foreachBatch(foreach_batch_function) \
    .start()

logger.info("스트리밍 시작")

# 스트리밍 쿼리 대기
query.awaitTermination()
