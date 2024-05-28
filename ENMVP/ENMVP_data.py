from pyspark.sql.functions import year, expr, col, count

def process_data(df_sales, df_product, df_employees, df_code, df_iso, logger):
    df_sales_product = df_sales.join(df_product, df_sales.Product_ID == df_product.Product_ID, "inner")
    df_sales_product_employees = df_sales_product.join(df_employees, df_sales_product.Employee_ID == df_employees.Employee_ID, "inner")
    df_sales_product_employees_pc = df_sales_product_employees.join(df_code.alias("pc"), df_product.Prod_Cat_ID.substr(1, 3) == col("pc.Code"), "left_outer")
    df_sales_product_employees_pc_psc = df_sales_product_employees_pc.join(df_code.alias("psc"), col("psc.Code") == df_product.Prod_Cat_ID, "left_outer")
    df_sales_product_employees_pc_psc_sc = df_sales_product_employees_pc_psc.join(df_code.alias("sc"), df_employees.Branch_CD.substr(1, 3) == col("sc.Code"), "left_outer")
    df_sales_product_employees_pc_psc_sc_iso = df_sales_product_employees_pc_psc_sc.join(df_iso.alias("ti"), df_employees.Branch_CD.substr(1, 3) == col("ti.Code"), "left_outer")
    df_re_sales = df_sales_product_employees_pc_psc_sc_iso.join(df_code.alias("cc"), df_sales_product_employees_pc_psc_sc_iso.Channel_CD == col("cc.Code"), "left_outer").select(
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
        col("cc.CDNM").alias("Sales_Channel"),
        col("ti.iso_code").alias("ISO_Code")
    )
    
    # 날짜별 데이터 수를 요약하여 로그에 기록
    df_summary = df_re_sales.groupBy("Sale_Date").agg(count("*").alias("count")).orderBy("Sale_Date")
    summary_data = df_summary.collect()
    for row in summary_data:
        logger.info(f"날짜: {row['Sale_Date']}, 데이터 수: {row['count']}")
    
    logger.info("최종 데이터프레임 생성 완료")
    return df_re_sales

def write_data_to_db(df_re_sales, mariadb_url, db_properties, logger):
    df_re_sales.write.jdbc(url=mariadb_url, table="TB_RE_SALES", mode="append", properties=db_properties)
    logger.info("결과를 MariaDB에 저장 완료")