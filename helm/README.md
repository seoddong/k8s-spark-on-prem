# Helm용 VM 구성
  - 앞서 만든 베이스 머신 이미지 이용해서 새로운 VM을 하나 만든다. [참조](https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/GCP_VM_setting.md#k8s-worker-node-%EC%84%B8%ED%8C%85)
  - VSCode 접속 환경도 구성한다.

# Helm 설치
install.sh 스크립트 실행

# kubectl 설치
한 줄 씩 실행
```shell
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod 700 ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
```

# Bitnami/spark 설치
Spark 3.4.1로 설치하려면 7.2.2로, spark 3.5로 설치하려면 9.0.0 입력<br>
replicaCount는 kube worker node 숫자 이하로 세팅

```shell
helm install my-first-spark bitnami/spark --version 7.2.2 -n default \
  --set service.type=NodePort \
  --set service.nodePorts.cluster=30077 \
  --set service.nodePorts.http=30078 \
  --set worker.replicaCount=2
```
