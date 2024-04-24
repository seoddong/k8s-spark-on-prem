from pyspark.sql import SparkSession
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

if __name__ == '__main__':
    ss: SparkSession = SparkSession.builder\
        .config(conf=conf)\
        .getOrCreate()

    df = ss.readStream.format("kafka")\
        .option("startingOffset", "earliest")\
        .option("subscribe", "book")\
        .option("kafka.bootstrap.servers", "peter-kafka01.foo.bar:9092,peter-kafka02.foo.bar:9092,peter-kafka03.foo.bar:9092")\
        .load()
    
    df.writeStream.format("console")\
        .outputMode("append")\
        .option("truncate", "false")\
        .start()\
        .awaitTermination()
