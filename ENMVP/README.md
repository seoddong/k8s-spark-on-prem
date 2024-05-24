다음은 제공된 파일들의 내용을 분석한 결과임.

### ENMVP_setting.py
이 파일은 주로 로깅 설정, AWS 자격 증명 획득, 그리고 Spark 세션을 생성하는 기능을 포함하고 있음.

- **setup_logging**: 로깅 설정을 초기화하고, 파일 핸들러와 스트림 핸들러를 추가함.
- **get_aws_credentials**: AWS 자격 증명을 얻고 이를 반환함.
- **create_spark_session**: Spark 세션을 생성하고 필요한 설정을 적용함.

### ENMVP_util.py
이 파일은 데이터프레임 변환과 관련된 유틸리티 함수를 포함하고 있음.

- **process_sales_data**: 판매 데이터를 다양한 조건에 따라 처리하고 변환함.

### ENMVP_main.py
이 파일은 전체 워크플로우를 실행하는 메인 스크립트로 보임.

- **main**: 설정 및 유틸리티 함수들을 호출하여 데이터 처리를 수행하고, 최종 결과를 데이터베이스에 저장함.

### ENMVP_data.py
이 파일은 데이터베이스에 데이터를 저장하는 기능을 포함하고 있음.

- **write_data_to_db**: 변환된 데이터프레임을 MariaDB에 저장함.

## README.md

```markdown
# ENMVP 프로젝트

## 개요
ENMVP 프로젝트는 데이터 처리 파이프라인을 구축하여 판매 데이터를 처리하고 분석하는 데 중점을 둠. 이 프로젝트는 AWS와 Spark를 사용하여 데이터를 처리하고, 최종 결과를 MariaDB에 저장함.

## 파일 설명

### ENMVP_setting.py
- **setup_logging**: 로깅 설정을 초기화하여 로그를 파일 및 콘솔에 기록함.
- **get_aws_credentials**: AWS 자격 증명을 획득함.
- **create_spark_session**: AWS 자격 증명을 이용하여 Spark 세션을 생성함.

### ENMVP_util.py
- **process_sales_data**: 판매 데이터를 처리하고 필요한 형식으로 변환함.

### ENMVP_main.py
- **main**: 전체 데이터 처리 워크플로우를 실행함. 로깅 설정, AWS 자격 증명 획득, Spark 세션 생성, 데이터 처리 및 최종 결과를 데이터베이스에 저장하는 과정을 포함함.

### ENMVP_data.py
- **write_data_to_db**: 처리된 데이터를 MariaDB에 저장함.

## 실행 방법
1. Python 환경 설정
2. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```
3. 스크립트 실행
   ```bash
   python ENMVP_main.py
   ```

## 필요 조건
- Python 3.x
- AWS 자격 증명
- Spark
- MariaDB

## 로그 파일
로그는 `/root/jupyterHome/logs` 디렉토리에 저장됨.

## 기여 방법
1. 이 프로젝트를 포크함.
2. 새로운 브랜치를 생성함 (`feature/기능_이름`).
3. 변경 사항을 커밋함 (`git commit -am 'Add 새로운 기능'`).
4. 브랜치에 푸시함 (`git push origin feature/기능_이름`).
5. 풀 리퀘스트를 생성함.

## 라이선스
이 프로젝트는 MIT 라이선스를 따름.
```

이 문서는 프로젝트의 개요, 파일 설명, 실행 방법, 필요 조건, 로그 파일 위치, 기여 방법, 및 라이선스를 포함함. 각 파일의 주요 기능을 요약하고, 사용자가 프로젝트를 설정하고 실행하는 방법을 안내함.
