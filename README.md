# 목차
- [k8s-spark에 대하여](#k8s-spark에-대하여)
- [k8s 구성을 위한 GCP VM 세팅](#k8s-구성을-위한-gcp-vm-세팅)
- [k8s 어플리케이션 설치 위한 Helm-client 환경 세팅](#k8s-어플리케이션-설치-위한-Helm-client-환경-세팅)
- [spark 어플리케이션 개발 위한 Jupyter Notebook 환경 세팅](#spark-어플리케이션-개발-위한-Jupyter-Notebook-환경-세팅)
- [spark 어플리케이션 개발](#spark-어플리케이션-개발)
- [spark Web UI 환경 세팅](#spark-Web-UI-환경-세팅)
- [spark 미니 프로젝트](#spark-미니-프로젝트)

<br><br><br><br>

# k8s-spark에 대하여
k8s 1.27 버전에 spark 3.4.1 버전으로 클러스터링 구성하며 전체적인 아키텍처는 아래 그림 참조
![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/9f49cf1d-5cb4-4aae-9ffb-6f02610ede99)

<br>

# k8s 구성을 위한 GCP VM 세팅
본 과제는 TCP 무료 계정(3개월/40만원 혜택)을 사용하여 진행함.<br>
구축 상세는 아래 링크 참조.
- [https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/GCP_VM_setting.md](https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/GCP_VM_setting.md)

<br>

# k8s 어플리케이션 설치 위한 Helm-client 환경 세팅
별도 서버에 Helm-client를 설치한다. 로컬에 설치해도 되지만 본 과제에서는 하나의 서버에 Helm과 주피터 노트북을 같이 사용할 수 있는 환경을 구성한다.<br>
Helm을 이용하여 Spark 클러스터를 설치하는 방법도 아래 링크에서 설명한다.<br>
구축 상세는 아래 링크 참조.
- [https://github.com/seoddong/k8s-spark-on-prem/blob/main/helm/README.md](https://github.com/seoddong/k8s-spark-on-prem/blob/main/helm/README.md)

<br>

# spark 어플리케이션 개발 위한 Jupyter Notebook 환경 세팅
Helm-client가 설치된 서버에 주피터 노트북 환경도 같이 설정한다.<br>
구축 상세는 아래 링크 참조.
- [https://github.com/seoddong/k8s-spark-on-prem/blob/main/jupyter/README.md](https://github.com/seoddong/k8s-spark-on-prem/blob/main/jupyter/README.md)

<br>

# spark 어플리케이션 개발
[https://github.com/seoddong/k8s-spark-on-prem/tree/main/jupyter/jupyter%20home](https://github.com/seoddong/k8s-spark-on-prem/tree/main/jupyter/jupyter%20home) 폴더의 여러 소스들을 이용해서 spark 프로그램을 테스트해보자.

<br>

# spark Web UI 환경 세팅
스파크 어플리케이션을 돌리다보면 스파크 웹에서 내용을 확인해 볼 필요가 생긴다.<br>
스파크 웹 UI는 크게 3가지 메인 화면, executor 화면, Spark Job 화면이 있는데 메인을 제외하고는 링크를 클릭해도 화면을 볼 수 없다.
이에 대해 아래 링크를 참조하여 각 화면을 볼 수 있다.
- [https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/README.md](https://github.com/seoddong/k8s-spark-on-prem/blob/main/Spark3.4.1/README.md)

<br>

# spark 미니 프로젝트
AWS S3에서 spark stream을 이용하여 파일을 읽고 MariaDB에 저장하는 미니 프로젝트를 진행해본다.<br>
![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/5d296e42-a9c6-4ec8-a4ca-8484a5faa780)

spark client mode로 개발을 진행하게 되며 client mode의 구조는 아래와 같다.<br>
![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/4edc76f2-19de-4df0-a78b-4254fc62ebd1)

미니 프로젝트를 위해 k8s에 MariaDB를 추가해야 하고 MariaDB가 사용할 스토리지로 Longhorn을 미리 설치해야 한다.
MariaDB와 Longhorn의 설치는 아래 링크를 확인하자.
- [https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/Longhorn_MariaDB_setting.md](https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/Longhorn_MariaDB_setting.md)

미니 프로젝트의 데이터 준비, 스파크 소스 등 자세한 설명은 아래 링크를 확인한다.
