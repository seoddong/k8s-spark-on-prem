# k8s 환경 설정
GCP 기준으로 테스트 함.
1. k8s-master용 VM을 하나 만든다.
2. 깡통 VM에 아래 배치 파일을 적용한다.
   - https://github.com/seoddong/k8s-on-prem/blob/9db9fdad3097e0856d67809401de53c4a7e66bb7/k8s1.27/gcp_k8s_init.sh
4. k8s-master VM의 머신 이미지를 만든다.
5. k8s-master VM에 아래 배치 파일을 계속 적용한다.
   - https://github.com/seoddong/k8s-on-prem/blob/ae16fac6d18c1f7bc1baf5b1bce48afffb44dea0/k8s1.27/gcp_k8s_master.sh
6. 위에 만들어둔 머신 이미지를 이용하여 VM을 3개 더 만든다.
   - k8s-node1, k8s-node2, k8s-node3 이런식으로 이름을 준다.
7. 각 VM에 접속하여 k8s-master와 연결하고 k8s 클러스터링 여부를 확인한다.
   - 아래 링크에 [k8s-master IP] 부분을 수정하고 접속하여 대시보드를 확인한다.
   - https://[k8s-master IP]:30000/#/workloads?namespace=default

# Spark WEB UI를 위한 Nodeport 설정
1. 기본 Spark Web UI 접속 위한 설정은 helm 설치 과정에서 설정함
2. 각각의 spark executor Web UI 접속을 위해 executor용 Nodeport Service를 만든다.
   - 아래 링크 파일을 기반으로 my-first-spark-worker-1-svc, my-first-spark-worker-2-svc, my-first-spark-worker-3-svc을 만든다.
   - https://github.com/seoddong/k8s-on-prem/blob/4d75c2425c700f106528843477b707704bdf63a7/k8s1.27/my-first-spark-worker-1-svc.yaml
   - <svc이름> my-first-spark-worker-1-svc
   - <port번호> 30079
   - <pod이름> my-first-spark-worker-1
