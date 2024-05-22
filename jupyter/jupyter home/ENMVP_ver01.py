import logging
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import year, expr, col, max as max_col
from datetime import datetime, timedelta
import boto3
import time
import os

def setup_logging():
    log_filename = datetime.now().strftime('batch_process_%Y%m%d.log')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename)
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()

def get_aws_credentials():
    session = boto3.Session()
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    logger.info("AWS 자경 증명 정보 획득")
    return aws_access_key_id, aws_secret_access_key

aws_access_key_id, aws_secret_access_key = get_aws_credentials()

def create_spark_session(aws_access_key_id, aws_secret_access_key):
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

def get_last_processed_date(spark, mariadb_url, db_properties):
    df_last_date = spark.read.jdbc(mariadb_url, "TB_RE_SALES1", properties=db_properties).select(max_col("Sale_Date").alias("last_date"))
    last_date = df_last_date.collect()[0]["last_date"]
    logger.info(f"마지막 처리된 날짜: {last_date}")
    return last_date

def read_data_from_s3(spark, s3_url, last_date):
    df_sales = spark.read.parquet(s3_url).filter(col("Sale_Date") > last_date)
    logger.info("S3에서 새로운 데이터 읽기 완료")
    return df_sales

def read_reference_data(spark, mariadb_url, db_properties):
    df_product = spark.read.jdbc(mariadb_url, "TB_PRODUCT", properties=db_properties)
    df_employees = spark.read.jdbc(mariadb_url, "TB_EMPLOYEES", properties=db_properties)
    df_code = spark.read.jdbc(mariadb_url, "TB_CODE", properties=db_properties)
    logger.info("MariaDB에서 참조 데이터 읽기 완료")
    return df_product, df_employees, df_code

def process_data(df_sales, df_product, df_employees, df_code):
    df_sales_product = df_sales.join(df_product, df_sales.Product_ID == df_product.Product_ID, "inner")
    df_sales_product_employees = df_sales_product.join(df_employees, df_sales_product.Employee_ID == df_employees.Employee_ID, "inner")
    df_sales_product_employees_pc = df_sales_product_employees.join(df_code.alias("pc"), df_product.Prod_Cat_ID.substr(1, 3) == col("pc.Code"), "left_outer")
    df_sales_product_employees_pc_psc = df_sales_product_employees_pc.join(df_code.alias("psc"), col("psc.Code") == df_product.Prod_Cat_ID, "left_outer")
    df_sales_product_employees_pc_psc_sc = df_sales_product_employees_pc_psc.join(df_code.alias("sc"), df_employees.Branch_CD.substr(1, 3) == col("sc.Code"), "left_outer")
    df_re_sales = df_sales_product_employees_pc_psc_sc.join(df_code.alias("cc"), df_sales_product_employees_pc_psc_sc.Channel_CD == col("cc.Code"), "left_outer").select(
        year(expr("CAST(Sale_Date AS DATE)")).alias("Sale_Year"),
        expr("CAST(Sale_Date AS DATE)").alias("Sale_Date"),
        df_sales.Transaction_ID,
        col("pc.CDNM").alias("Product_Category"),
        col("psc.CDNM").alias("Product_Subcategory"),
        df_sales.Product_ID,
        df_product.Manufacturer_ID.alias("Manufacturer"),
        df_product.Vendor_ID.alias("Vendor"),
        df_sales.Customer_ID,
        df_sales.Sales_Revenue.alias("List_Price"),
        df_sales.Quantity_Sold,
        df_sales.Sales_Revenue,
        df_sales.Cost_Price_per_Unit,
        (df_sales.Cost_Price_per_Unit * df_sales.Quantity_Sold).alias("Total_Cost_Price"),
        df_sales.Selling_Expenses,
        df_sales.Selling_Expenses.alias("Total_Selling_Cost"),
        (df_sales.Sales_Revenue - (df_sales.Cost_Price_per_Unit * df_sales.Quantity_Sold + df_sales.Selling_Expenses)).alias("Profit"),
        df_employees.Employee_NM.alias("Salesperson"),
        df_employees.Branch_CD.alias("Sales_Branch"),
        col("sc.CDNM").alias("Sales_Region"),
        col("cc.CDNM").alias("Sales_Channel")
    )
    logger.info("최종 데이터프레임 생성 완료")
    return df_re_sales

def write_data_to_db(df_re_sales, mariadb_url, db_properties):
    df_re_sales.write.jdbc(url=mariadb_url, table="TB_RE_SALES1", mode="append", properties=db_properties)
    logger.info("결과를 MariaDB에 저장 완료")

def process_batch():
    batch_start_time = datetime.now()
    logger.info(f"배치 시작 시간: {batch_start_time}")

    spark = create_spark_session(aws_access_key_id, aws_secret_access_key)
    mariadb_url = "jdbc:mysql://34.68.13.64:30007/sparkdb?permitMysqlScheme"
    db_properties = {"driver": "org.mariadb.jdbc.Driver", "user": "yourID", "password": "yourPW"}

    last_date = get_last_processed_date(spark, mariadb_url, db_properties)
    s3_url = "s3a://jolajoayo-spark-0001/sales_*.parquet"
    df_sales = read_data_from_s3(spark, s3_url, last_date)
    df_product, df_employees, df_code = read_reference_data(spark, mariadb_url, db_properties)
    
    df_sales.cache()
    df_product.cache()
    df_employees.cache()
    df_code.cache()
    logger.info("데이터 캐싱 완료")

    df_re_sales = process_data(df_sales, df_product, df_employees, df_code)
    write_data_to_db(df_re_sales, mariadb_url, db_properties)

    spark.stop()
    logger.info("스파크 세션 종료")

    batch_end_time = datetime.now()
    logger.info(f"배치 종료 시간: {batch_end_time}")
    logger.info(f"배치 처리 시간: {batch_end_time - batch_start_time}")

def main():
    program_start_time = datetime.now()
    logger.info(f"프로그램 시작 시간: {program_start_time}")

    while True:
        process_batch()
        time.sleep(1800) # 30분(1800초) 대기

    program_end_time = datetime.now()
    logger.info(f"프로그램 종료 시간: {program_end_time}")
    logger.info(f"프로그램 총 실행 시간: {program_end_time - program_start_time}")

if __name__ == "__main__":
    main()
