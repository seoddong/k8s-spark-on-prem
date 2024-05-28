import logging
from datetime import datetime
import os

def setup_logging():
    log_dir = "/root/jupyterHome/logs"  # 로그 파일을 저장할 디렉토리
    os.makedirs(log_dir, exist_ok=True)  # 디렉토리가 없으면 생성
    log_filename = os.path.join(log_dir, datetime.now().strftime('batch_process_%Y%m%d.log'))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Stream handler (console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

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
        .setAppName("sparkQLwithS3")
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
mariadb_url = "jdbc:mysql://34.68.13.64:30007/sparkdb?permitMysqlScheme"
db_properties = {
    "driver": "org.mariadb.jdbc.Driver",
    "user": "root",
    "password": "tjehdgml"
}
s3_url = "s3a://jolajoayo-spark-0001/sales_"
