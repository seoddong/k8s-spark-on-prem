# MVPSS_setting.py

import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os
from pyspark.sql.types import StructType, StructField, StringType, DateType, LongType

def setup_logging(log_level=logging.INFO):
    log_dir = "/root/jupyterHome/logs"  # 로그 파일을 저장할 디렉토리
    os.makedirs(log_dir, exist_ok=True)  # 디렉토리가 없으면 생성
    log_filename = os.path.join(log_dir, 'batch_process.log')

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # TimedRotatingFileHandler for daily log rotation
    file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7)
    file_handler.suffix = "%Y%m%d"
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    file_handler.setLevel(log_level)

    # Stream handler (console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    stream_handler.setLevel(log_level)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

def get_aws_credentials(logger):
    import boto3
    session = boto3.Session()
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    logger.info("AWS 자격 증명 정보 획득")
    return aws_access_key_id, aws_secret_access_key

def create_spark_session(aws_access_key_id, aws_secret_access_key, logger):
    from pyspark.sql import SparkSession
    from pyspark import SparkConf

    conf = (
        SparkConf()
        .setAppName("sparkStreamS3")
        .set("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0,org.apache.hadoop:hadoop-aws:3.3.2,org.mariadb.jdbc:mariadb-java-client:3.3.3")
        .set("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .set("com.amazonaws.services.s3.enableV4", "true")
        .set("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com")
        .set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
        .set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
        .set("spark.executor.memory", "1536m")
        .set("spark.driver.memory", "2g")
        .set("spark.network.timeout", "300s")
        .set("spark.executor.heartbeatInterval", "60s")
        .setMaster("spark://34.68.13.64:30077")
    )
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    logger.info("Spark 세션 생성 완료")
    return spark

# 추가된 설정 상수
mariadb_url = "jdbc:mysql://k8s-master외부IP:30007/sparkdb?permitMysqlScheme"
db_properties = {
    "driver": "org.mariadb.jdbc.Driver",
    "user": "root",
    "password": "자신의 암호 적으셈"
}
s3_url = "s3a://spark-miniproj-0001/"

# 스키마 정의
schema = StructType([
    StructField("Sale_Date", DateType(), True),
    StructField("Transaction_ID", StringType(), True),
    StructField("Product_ID", StringType(), True),
    StructField("Customer_ID", StringType(), True),
    StructField("Quantity_Sold", LongType(), True),
    StructField("Sales_Revenue", LongType(), True),
    StructField("Cost_Price_per_Unit", LongType(), True),
    StructField("Selling_Expenses", LongType(), True),
    StructField("Employee_ID", LongType(), True),
    StructField("Channel_CD", StringType(), True)
])
