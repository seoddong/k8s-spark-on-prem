import boto3
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

# boto3를 통해 자동으로 자격증명 가져오기
# ~/.aws/credentials를 미리 만들어놔야 함
session = boto3.Session()
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

# Create a Spark session with your AWS Credentials
conf = (
    SparkConf()
    .setAppName("sparkQLwithS3") # replace with your desired name
    .set("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0,org.apache.hadoop:hadoop-aws:3.3.2")
    .set("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .set("spark.sql.shuffle.partitions", "4") # default is 200 partitions which is too many for local
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .set("com.amazonaws.services.s3.enableV4", "true")
    .set("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com")
    # .set("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.profile.ProfileCredentialsProvider")
    .set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
    .set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
    .setMaster("spark://34.125.136.103:30077")
)

spark = SparkSession.builder.config(conf=conf).getOrCreate()
# properties = spark.sparkContext.getConf().getAll()
# print(properties)

df = spark.read.format('json').load('s3a://jolajoayo-spark-0001/spark2-sql/airports/airport-codes.csv.json')

df.createOrReplaceTempView("airportcodes")
viewdf = spark.sql(\
                   "SELECT iso_region, name, type "\
                   "FROM airportcodes "\
                   "WHERE iso_country = 'US' "\
                   )

viewdf.show()

spark.stop()

