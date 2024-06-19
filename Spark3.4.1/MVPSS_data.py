# MVPSS_data.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import year, expr, col

def read_table_from_mariadb(spark: SparkSession, table_name: str, mariadb_url: str, db_properties: dict, logger):
    df = spark.read.jdbc(url=mariadb_url, table=table_name, properties=db_properties)
    row_count = df.count()
    logger.info(f"{table_name} 테이블 읽기 완료, 총 {row_count}건의 데이터")
    return df

def write_table_to_mariadb(df, table_name: str, mariadb_url: str, db_properties: dict, logger):
    row_count = df.count()
    df.write.jdbc(url=mariadb_url, table=table_name, mode="append", properties=db_properties)
    logger.info(f"{table_name} 테이블에 {row_count}건의 데이터 저장 완료")

def read_and_cache_reference_tables(spark: SparkSession, mariadb_url: str, db_properties: dict, logger):
    df_product = read_table_from_mariadb(spark, "TB_PRODUCT", mariadb_url, db_properties, logger)
    df_employees = read_table_from_mariadb(spark, "TB_EMPLOYEES", mariadb_url, db_properties, logger)
    df_code = read_table_from_mariadb(spark, "TB_CODE", mariadb_url, db_properties, logger)
    df_iso = read_table_from_mariadb(spark, "TB_ISO", mariadb_url, db_properties, logger)

    df_product.cache()
    df_employees.cache()
    df_code.cache()
    df_iso.cache()

    logger.info("참조 테이블 캐싱 완료")
    return df_product, df_employees, df_code, df_iso

def create_df_sales(processed_df, df_product, df_employees, df_code, df_iso, logger):
    df_sales_product = processed_df.join(df_product, processed_df.Product_ID == df_product.Product_ID, "inner")
    df_sales_product_employees = df_sales_product.join(df_employees, df_sales_product.Employee_ID == df_employees.Employee_ID, "inner")
    df_sales_product_employees_pc = df_sales_product_employees.join(df_code.alias("pc"), df_product.Prod_Cat_ID.substr(1, 3) == col("pc.Code"), "left_outer")
    df_sales_product_employees_pc_psc = df_sales_product_employees_pc.join(df_code.alias("psc"), col("psc.Code") == df_product.Prod_Cat_ID, "left_outer")
    df_sales_product_employees_pc_psc_pcm = df_sales_product_employees_pc_psc.join(df_code.alias("pcm"), df_product.Manufacturer_ID == col("pcm.Code"), "left_outer")
    df_sales_product_employees_pc_psc_pcm_pcv = df_sales_product_employees_pc_psc_pcm.join(df_code.alias("pcv"), df_product.Vendor_ID == col("pcv.Code"), "left_outer")
    df_sales_product_employees_pc_psc_pcm_pcv_pcb = df_sales_product_employees_pc_psc_pcm_pcv.join(df_code.alias("pcb"), df_employees.Branch_CD == col("pcb.Code"), "left_outer")
    df_sales_product_employees_pc_psc_pcm_pcv_pcb_sc = df_sales_product_employees_pc_psc_pcm_pcv_pcb.join(df_code.alias("sc"), df_employees.Branch_CD.substr(1, 3) == col("sc.Code"), "left_outer")
    df_sales_product_employees_pc_psc_pcm_pcv_pcb_sc_cc = df_sales_product_employees_pc_psc_pcm_pcv_pcb_sc.join(df_code.alias("cc"), processed_df.Channel_CD == col("cc.Code"), "left_outer")
    df_sales_product_employees_pc_psc_pcm_pcv_pcb_sc_cc_iso = df_sales_product_employees_pc_psc_pcm_pcv_pcb_sc_cc.join(df_iso.alias("ti"), df_employees.Branch_CD.substr(1, 3) == col("ti.Code"), "left_outer")

    df_sales = df_sales_product_employees_pc_psc_pcm_pcv_pcb_sc_cc_iso.select(
        year(expr("CAST(Sale_Date AS DATE)")).alias("Sale_Year"),
        expr("CAST(Sale_Date AS DATE)").alias("Sale_Date"),
        processed_df.Transaction_ID,
        col("pc.CDNM").alias("Product_Category"),
        col("psc.CDNM").alias("Product_Subcategory"),
        processed_df.Product_ID,
        col("pcm.CDNM").alias("Manufacturer"),
        col("pcv.CDNM").alias("Vendor"),
        processed_df.Customer_ID,
        processed_df.Sales_Revenue.alias("List_Price"),
        processed_df.Quantity_Sold,
        processed_df.Sales_Revenue,
        processed_df.Cost_Price_per_Unit,
        (processed_df.Cost_Price_per_Unit * processed_df.Quantity_Sold).alias("Total_Cost_Price"),
        processed_df.Selling_Expenses,
        (processed_df.Cost_Price_per_Unit * processed_df.Quantity_Sold + processed_df.Selling_Expenses).alias("Total_Selling_Cost"),
        (processed_df.Sales_Revenue - (processed_df.Cost_Price_per_Unit * processed_df.Quantity_Sold + processed_df.Selling_Expenses)).alias("Profit"),
        df_employees.Employee_NM.alias("Salesperson"),
        col("pcb.CDNM").alias("Sales_Branch"),
        col("sc.CDNM").alias("Sales_Region"),
        col("cc.CDNM").alias("Sales_Channel"),
        col("ti.iso_code").alias("ISO_Code"),
        processed_df.Processed_Time,
        processed_df.file_name
    )

    return df_sales
