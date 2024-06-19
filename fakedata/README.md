# fakedata에 대하여
- spark 미니 프로젝트에 사용할 원본 데이터가 6만여건으로 데이터 수가 너무 적음
- 합성 데이터를 만들되 원본 데이터의 제품, 직원, 판매 실적 등의 비율이 비슷하게 유지되도록 만들어야 함

<br>

# 실행 전 준비 사항
- MariaDB가 설치 되어 있어야 함
- MariaDB에 아래 테이블들이 만들어져있고 데이터가 들어있어야 함
   - TB_EMPLOYEES, TB_PRODUCT - [MariaDB 덤프 파일](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/dump-sparkdb-202406191320.sql) 이용하여 생성
   - TB_SALES
      1) [DDL문](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/DDL_TB_SALES.sql) 이용하여 테이블 생성
      2) DBWeaver로 [원본 샘플 데이터](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/data/TB_SALES.csv)를 TB_SALES에 import

<br>

# fakedata_ver01.py 사용법
- fakedata_ver01.py와 requirements.txt 파일 다운로드
- pip install -r requirements.txt 명령으로 필요한 라이브러리 설치
- fakedata_ver01.py 실행시키면 하위에 synthetic_sales_data 폴더를 만들고 그 아래 합성데이터 파일이 sales_data_2024-05-20_1.csv 형태로 만들어 짐
- 각 csv파일은 현재 1초 간격으로 저장되도록 설정되어 있으므로 시연 시 이 시간과 multiplier를 조절하여 실시간으로 파일이 생성되는 것처럼 할 수 있음
- 현재 생성하는 합성 데이터 설정하기
   - 파일당 100건의 데이터가 생성되고 10개의 파일을 만듦 = 즉 1,000개의 데이터 생성
      ```python
      # 생성할 데이터의 배수 및 파일당 저장 건수 설정
      multiplier = 10  # 데이터 배수
      records_per_file = 100  # 파일당 저장 건수
      ```
- 합성데이터 생성 날짜 설정하기
   - 범위로 설정할 때: 시작일과 종료일 입력
         ```python
         # 작업 날짜 범위 설정
         start_date = datetime.strptime("2024-06-01", '%Y-%m-%d')  # 시작 날짜 설정
         end_date = datetime.strptime("2024-06-30", '%Y-%m-%d')  # 종료 날짜 설정
         ```
   - 하루로 설정할 때: 시작일과 종료일을 같게 입력
         ```python
         # 작업 날짜 범위 설정
         start_date = datetime.strptime("2024-06-30", '%Y-%m-%d')  # 시작 날짜 설정
         end_date = datetime.strptime("2024-06-30", '%Y-%m-%d')  # 종료 날짜 설정
         ```
