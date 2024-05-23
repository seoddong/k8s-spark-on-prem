# fakedata_ver01.py 사용법
- fakedata_ver01.py와 requirements.txt 파일 다운로드
- pip install -r requirements.txt 명령으로 필요한 라이브러리 설치
- fakedata_ver01.py 실행시키면 하위에 synthetic_sales_data 폴더를 만들고 그 아래 합성데이터 파일이 sales_data_2024-05-20_1.csv 형태로 만들어 짐 
- 현재 생성하는 합성 데이터 설정하기
   - 파일당 100건의 데이터가 생성되고 10개의 파일을 만듦 = 즉 1,000개의 데이터 생성
      ```python
      # 생성할 데이터의 배수 및 파일당 저장 건수 설정
      multiplier = 10  # 데이터 배수
      records_per_file = 100  # 파일당 저장 건수
      ```
- 합성데이터 생성 날짜 설정하기
   - 범위로 설정할 때: 시작일과 생성할 날짜 수 수정
       - 아래 코드와 같이 오늘 날짜 부분을 주석으로 막고 범위 설정 부분에서 주석을 푼다.
       - "2024-05-15" 부분과 6이라고 적힌 부분을 원하는 대로 수정하고 실행한다.
           ```python
           # 작업 날짜 범위 설정 (start_date부터 n일 순차적으로)
           start_date = datetime.strptime("2024-05-15", '%Y-%m-%d')  # 시작 날짜 설정
           delta_days = 6  # 10일치 생성하려면 9로 입력
           unique_dates = [start_date + timedelta(days=x) for x in range(delta_days + 1)]
           # 오늘 날짜의 데이터만 생성하려면 아래와 같이 설정
           # start_date = datetime.today()
           # delta_days = 0
           # unique_dates = [start_date]
           ```
   - 당일로 설정할 때: 
       - 아래와 같이 범위 설정 부분을 주석으로 막고 실행.
           ```python
           # 작업 날짜 범위 설정 (start_date부터 n일 순차적으로)
           # start_date = datetime.strptime("2024-05-15", '%Y-%m-%d')  # 시작 날짜 설정
           # delta_days = 6  # 10일치 생성하려면 9로 입력
           # unique_dates = [start_date + timedelta(days=x) for x in range(delta_days + 1)]
           # 오늘 날짜의 데이터만 생성하려면 아래와 같이 설정
           start_date = datetime.today()
           delta_days = 0
           unique_dates = [start_date]
           ```
