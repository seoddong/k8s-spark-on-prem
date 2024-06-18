# Spark WEB UI를 위한 Nodeport 설정
1. 기본 Spark Web UI 접속 위한 설정은 helm 설치 과정에서 설정함
2. 각각의 spark executor Web UI 접속을 위해 executor용 Nodeport Service를 만든다.
   - 아래 링크 파일을 기반으로 my-first-spark-worker-1-svc, my-first-spark-worker-2-svc, my-first-spark-worker-3-svc을 만든다.
   - https://github.com/seoddong/k8s-on-prem/blob/4d75c2425c700f106528843477b707704bdf63a7/k8s1.27/my-first-spark-worker-1-svc.yaml
   - <svc이름> my-first-spark-worker-1-svc, my-first-spark-worker-2-svc, my-first-spark-worker-3-svc
   - <port번호> 30079, 30080, 30081
   - <pod이름> my-first-spark-worker-1, my-first-spark-worker-2, my-first-spark-worker-3
3. http://[k8s-master IP]:30079, http://[k8s-master IP]:30080, http://[k8s-master IP]:30081 접속하여 확인한다.
