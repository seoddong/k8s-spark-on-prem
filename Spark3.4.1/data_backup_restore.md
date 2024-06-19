## DBeaver를 이용한 테이블 백업 및 복구

### DBeaver를 이용한 테이블 백업

1. **DBeaver 실행 및 MariaDB 연결**
   - DBeaver를 실행하고 MariaDB에 연결함.
   - MariaDB 연결을 설정하지 않은 경우, `Database` -> `New Database Connection`을 선택하고 MariaDB를 선택하여 연결을 설정함.

2. **백업할 테이블 선택**
   - 왼쪽의 데이터베이스 탐색기에서 백업할 테이블이 있는 데이터베이스를 선택하고, 백업할 테이블들을 선택함.

3. **테이블 데이터 내보내기**
   - 선택한 테이블들에 대해 마우스 오른쪽 버튼을 클릭하고, `Export Data`를 선택함.
   - `Database`를 선택한 후, `SQL` 형식을 선택함. (필요한 경우 다른 형식도 선택 가능함)
   - 내보낼 파일의 경로를 설정하고, `Next` 버튼을 클릭한 후, `Finish`를 클릭하여 백업을 완료함.

### DBeaver를 이용한 테이블 복구

1. **DBeaver 실행 및 MariaDB 연결**
   - DBeaver를 실행하고 복구할 MariaDB에 연결함.

2. **백업 파일 가져오기**
   - `Database` -> `Execute SQL Script`를 선택함.
   - 백업 파일(`.sql`)을 선택하고 열기를 클릭함.
   - SQL 스크립트가 DBeaver의 SQL 편집기에 열림.

3. **SQL 스크립트 실행**
   - SQL 편집기에서 열린 스크립트를 실행하여 테이블을 복구함.
   - 상단의 실행 버튼(녹색 화살표)을 클릭하거나 `Ctrl+Enter`를 눌러 스크립트를 실행함.
