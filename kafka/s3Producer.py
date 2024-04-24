import os
import boto3
import json
import logging
import sys
from confluent_kafka import Producer
# from dotenv import load_dotenv

# load_dotenv()  # .env 파일에서 환경 변수 로드

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def acked(err, msg):
    logger = logging.getLogger()
    if err is not None:
        logger.error(f"Failed to deliver message: {err}")
    else:
        logger.info(f"Message produced: {msg.topic()}")

def produce_kafka_messages(bucket, key):
    session = boto3.Session(
        # Boto3가 자동으로 ~/.aws/credentials 파일에서 accessKey, secretKey를 찾기 때문에
        # 명시적으로 알려줄 필요는 없다.
        # aws_access_key_id=os.getenv('aws_access_key_id'),
        # aws_secret_access_key=os.getenv('aws_secret_access_key'),
        region_name='ap-northeast-2'
    )
    s3_client = session.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    records = json.loads(response['Body'].read().decode('utf-8'))

    # Kafka 설정
    kafka_config = {
        'bootstrap.servers': 'peter-kafka01.foo.bar:9092,peter-kafka02.foo.bar:9092,peter-kafka03.foo.bar:9092'
    }
    producer = Producer(kafka_config)

    # 10건씩 Kafka에 보내기
    batch_size = 10
    # for i in range(0, len(records), batch_size):
    for i in range(0, 10, batch_size): # 테스트로 10번만
        batch_records = records[i:i + batch_size]
        for record in batch_records:
            producer.produce('airportcodes', value=json.dumps(record).encode('utf-8'), callback=acked)
        producer.flush()

def main():
    logger = setup_logging()

    # 파일 경로에서 버킷과 키 분리
    bucket = 'jolajoayo-spark-0001'
    key = 'spark2-sql/airports/airport-codes.csv.json'

    try:
        produce_kafka_messages(bucket, key)
        logger.info("Messages successfully sent to Kafka in batches of 10")
    except Exception as e:
        logger.error(f"Error sending messages to Kafka: {e}")

if __name__ == "__main__":
    main()
