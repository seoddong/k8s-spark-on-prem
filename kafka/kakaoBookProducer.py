import requests
import json

from confluent_kafka import Producer
import book_data_pb2 as pb2
import keywords

class KakaoException(Exception):
    pass

def get_original_data(query: str) -> dict:
    rest_api_key = "0cc8b42b7db806e9fe2349968a35de0e"
    url = "https://dapi.kakao.com/v3/search/book"

    res = requests.get(
        url=url,
        headers={
            "Authorization": f"KakaoAK {rest_api_key}"
        },
        params={
            "query": query,
            "size": 50,
            "start": 1,
        }
    )

    if res.status_code >= 400:
        raise KakaoException(res.content)
    
    return json.loads(res.text)
    
    


if __name__ == "__main__":

    #kafka configs
    conf = {
        'bootstrap.servers': 'peter-kafka01.foo.bar:9092',
        # 'bootstrap.servers': 'localhost:29092',
    }

    producer = Producer(conf)
    topic = "book"

    cnt = 0
    for keyword in keywords.book_keywords:
        original_Data = get_original_data(query=keyword)
        for item in original_Data['documents']:
            book = pb2.Book()
            # dictionamry --> protobuf
            
            book.title = item['title']
            book.author = ','.join(item['authors'])
            book.publisher = item['publisher']
            book.isbn = item['isbn']
            book.price = item['price']
            book.publication_Date = item['datetime']
            book.source = 'kakao'
            print('--------------')
            print(book)
            producer.produce(topic=topic, value=book.SerializeToString())
            producer.flush()
            cnt += 1
            print(f"전송 완료 - {cnt}")


    
    # print(original_Data)
