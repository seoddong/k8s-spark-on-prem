## 목차
- [Data](#Data)

<br><br><br><br>

# Data
1) 데이터 구조
   - S3로부터 읽어들이는 판매실적(data/sales_data_xxx.csv)와
   - MariaDB에 존재하는 참조 테이블들(제품, 직원, 지역, 코드) 등으로 구성된다.
   - 위 데이터를 spark에서 가공하여 MariaDB의 TB_RE_SALES 테이블에 넣게 된다.
   ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/376a9e2c-a746-4d34-aaba-7a80f923bf1b)

2) 사용할 데이터 파일 (모두 data 폴더에 있음)
   - 샘플 데이터 원본 : [TB_SALES.csv](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/TB_SALES.csv)
      - 이 파일 이용하여 fakedata 생성 로직으로 아래 데이터 생성하였음
   - S3용 데이터 - [sales_data_202405까지.zip](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/sales_data_202405%EA%B9%8C%EC%A7%80.zip) : 2024.01 ~ 05월 판매 실적 데이터
   - S3용 데이터 - [sales_data_2024-06.zip](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/sales_data_2024-06.zip) : 2024.06월 판매실적 데이터
   - MariaDB용 데이터 - [dump-sparkdb-202406191320.sql](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/dump-sparkdb-202406191320.sql) : MariaDB의 제품, 직원, 지역, 코드 덤프 파일
      - 덤프파일은 DBWeaver에서 데이터베이스를 선택하고 `도구` > `Restore database`를 선택하여 자기 DB에 복원 가능
      - 자세한 내용은 여기 [참조](https://velog.io/@suuuinkim/DBeaver-%EB%8D%B0%EC%9D%B4%ED%84%B0-dumpexportrestoreimport-%EB%B0%A9%EB%B2%95)

3) TB_RE_SALES 테이블
   - 스파크 데이터 처리 결과가 저장되는 테이블로써 미리 테이블을 만들어놓아야 함 ([DDL문 참조](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/DDL_TB_RE_SALES.sql))

<br>

# 준실시간 버전 소스
스파크 미니 프로젝트 초기에 만든 버전 <br>
정해진 배치 간격에 따라 실행되는 데이터 처리 구조로 ENMVP_로 시작하는 4개의 파일로 이루어짐 <br>
S3 데이터가 parquet 형식이 아니고 csv 파일을 가정하고 처리하는 방식
- ENMVP_main.py
- ENMVP_data.py
- ENMVP_setting.py
- ENMVP_util.py
  - S3파일을 어디까지 읽었는지 체크하는 등 여러 기능 담당

<br>

# 실시간 Sparkstream 버전 소스
스파크 미니 프로젝트 후반에 만든 개선 버전 <br>
Sparkstream을 이용한 실시간 데이터 처리 구조로 MVPSS_로 시작하는 3개의 파일로 이루어짐 <br>
개선사항
 - 판매실적 데이터를 parquet 형식으로 S3에 저장하므로 이를 처리하도록 변경
 - SparkStream 사용으로 신규 S3파일을 찾고 처리하는 util 로직 불필요 (코드 단순화)

### 소스 설명
- MVPSS_main.py
   - `_metadata.file_name`은 S3에 새로운 파일이 생겨서 readStream 할 때 생기는 메타 정보에 접근하기 위해 추가함
- MVPSS_data.py
   - 판매실적 데이터와 제품, 직원, 지역, 코드 테이블을 dataframe으로 처리
   - 사실 SQL문을 직접 사용해도 되는데 괜히 dataframe으로 데이터 조인을 처리해보고 싶었
- MVPSS_setting.py
   - S3 접속은 boto3를 이용하여 aws credential로 자격증명 관리함
      - aws credential은 서버의 root/.aws/credentials 파일에 저장해 놓아야 함
      - aws에서 accessKeys.csv 파일을 다운받을 수 있고 그 파일 참고하여 작성하면 됨 (자세한 건 ChatGPT에게 물어보자)
      - credentails 파일 내용 (예시)
        ```shell
        [default]
        aws_access_key_id = AKIABZI2CLB26L37BL4
        aws_secret_access_key = crBhJRiBeTxxQd+dlPOFzO8sop68j4JHJPFux2PP
        ```
   - MariaDB 접속 정보 설정
     - ChatGPT가 알려주는 url은 작동되지 않음
     - `jdbc:mysql`을 써야 함 <br>
        ```shell
        mariadb_url = "jdbc:mysql://k8s-master외부IP:30007/sparkdb?permitMysqlScheme"
        db_properties = {
            "driver": "org.mariadb.jdbc.Driver",
            "user": "root",
            "password": "자신의 암호 적으셈"
        }
        ```
   - SparkSession config 설정 : 설정에 필요한 라이브러리나 파일들은 spark가 자동으로 체크하고 없으면 다운로드함
   - S3 parquet 파일 스키마 설정
      - parquet 파일은 스키마를 미리 정의해 놓아야 함

<br>

<br>

<br>

<br>
