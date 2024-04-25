# Bitnami/spark 설치
Spark 3.4.1로 설치하려면 7.2.2로, spark 3.5로 설치하려면 9.0.0 입력<br>
replicaCount는 kube worker node 숫자 이하로 세팅

```shell
helm install my-first-spark bitnami/spark –version 7.2.2 –n default \
  --set service.type=NodePort \
  --set service.nodePorts.cluster=30077 \
  --set service.nodePorts.http=30078 \
  --set worker.replicaCount=2
```
