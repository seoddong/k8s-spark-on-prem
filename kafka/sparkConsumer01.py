from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType, StructField
from pyspark.conf import SparkConf
conf = (
SparkConf()
    .setAppName("MY_kafka") # replace with your desired name
    .set("spark.jars.packages", \
         "org.apache.commons:commons-pool2:2.11.1"\
         ",org.apache.kafka:kafka-clients:3.4.0"\
         ",org.apache.spark:spark-protobuf_2.12:3.4.1"\
         ",org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1"\
         ",org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.4.1"\
        )
    .set("spark.sql.shuffle.partitions", "4") # default is 200 partitions which is too many for local
    .setMaster("local[*]") # replace the * with your desired number of cores. * for use all.
    # .setMaster("spark://34.125.136.103:30077") # replace the * with your desired number of cores. * for use all.
)

def main():
    # Spark 세션 초기화
    spark = SparkSession.builder \
        .config(conf=conf)\
        .getOrCreate()

    # Kafka 서버 정보
    kafka_bootstrap_servers = 'peter-kafka01.foo.bar:9092,peter-kafka02.foo.bar:9092,peter-kafka03.foo.bar:9092'
    topic = 'airportcodes'

    # Kafka 스트림 읽기 설정
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load()

    # 메시지의 value를 JSON으로 파싱
    schema = StructType([
        StructField("ident", StringType(), True),
        StructField("type", StringType(), True),
        StructField("name", StringType(), True),
        StructField("elevation_ft", StringType(), True),
        StructField("continent", StringType(), True),
        StructField("iso_country", StringType(), True),
        StructField("iso_region", StringType(), True),
        StructField("municipality", StringType(), True),
        StructField("gps_code", StringType(), True),
        StructField("iata_code", StringType(), True),
        StructField("local_code", StringType(), True),
        StructField("coordinates", StringType(), True),
    ])
    
    json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # 스트림 출력 설정
    query = json_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
