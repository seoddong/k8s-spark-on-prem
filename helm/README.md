# Helm이란
  ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/f76418b4-7e92-4749-ae6c-ee1896dbc180)

<br>

# Helm 아키텍처
  ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/2e7ed790-aa13-4a1f-a6e2-4ce2248a51c4)

<br>

# Helm용 VM 구성
  - 앞서 만든 베이스 머신 이미지 이용해서 새로운 VM을 하나 만든다.
  - VM의 이름은 Helm-Client 혹은 Jupyter-Notebook 으로 만들자.
  - K8S worker node 세팅 부분 [참조](https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/GCP_VM_setting.md#k8s-worker-node-%EC%84%B8%ED%8C%85)
  - VSCode 접속 환경도 구성한다.

<br>

# Helm 설치
서버에 접속 후 [install.sh](https://github.com/seoddong/k8s-spark-on-prem/blob/main/helm/install.sh) 스크립트 실행 (VSCode로 새 파일 만들고 스크립트 복사해서 넣고 저장하고 권한 주고.. 이런 작업은 앞서 했으니 자세한 설명은 생략)

<br>

# kubectl 설치
Helm이 k8s와 통신하기 위해 kubectl을 설치해야 한다. 아래 코드를 한 줄 씩 실행한다.
```shell
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod 700 ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
```

<br>

# Helm과 kube 클러스터간 연결
  k8s-master의 ~/.kube/config 파일을 helm-client의 동일한 경로에 카피하면 됨
   ```
    [root@helm-client ~]# mkdir .kube
    [root@helm-client ~]# scp root@34.68.13.64:~/.kube/config .kube/config 
    [root@helm-client ~]# ls .kube
    혹시 VM재설치 등으로 호스트 키가 변경되어 로그인이 안 될 경우 아래 명령으로 호스트키 초기화하고 다시 시도한다.
    [root@helm-client ~]# ssh-keygen -R <<호스트명 또는 IP 주소>>
   ```

<br>

# Helm에 repo 추가
  K8s-spark repo를 추가하는 방법<br>
  repo를 추가하더라도 메타정보만 가져오게 되는데 해당 소스까지 몽땅 가져오고 싶다면 pull로 소스 동기화 가능하다.<br>
  여기서는 pull까지 할 필요는 없다.
   ```
    [root@helm-client ~]# helm repo add bitnami https://charts.bitnami.com/bitnami
    [root@helm-client ~]# helm repo update
    pull은 필요한 경우에만 한다.
    [root@helm-client ~]# helm pull bitnami/spark --version 5.1.2
   ```

<br>

# Helm 이용하여 spark 설치
처음엔 최신 버전인 Spark 3.5.0을 설치하여 사용하려 하였으나 다른 라이브러리의 궁합 정보를 찾는 과정에서 가장 정보가 많은 3.4.1버전으로 설치하기로 하였다.<br>
본 과제에서는 Bitnami/Spark를 설치한다. Spark 3.4.1로 설치하려면 Bitnami Spark 버전을 7.2.2로, spark 3.5로 설치하려면 9.0.0 입력한다.<br>
replicaCount는 kube worker node 숫자 이하로 세팅

```shell
helm install my-first-spark bitnami/spark --version 7.2.2 -n default \
  --set service.type=NodePort \
  --set service.nodePorts.cluster=30077 \
  --set service.nodePorts.http=30078 \
  --set worker.replicaCount=3
```

위 스크립트에서 보다시피 외부에서 접속하고자 30077, 30078을 nodeport로 설정하였기 때문에 GCP 방화벽에 추가해주어야 한다.

Spark 설치 결과는 아래 링크 통해 Web UI로 확인 가능하다.
  - http://<<k8s-master 외부IP>>:30078/

<br>

# spark를 삭제하거나 재설치하고자 하는 경우
  - 삭제하기
    ```shell
    [root@helm-client ~]# helm uninstall my-first-spark
    ```
  - 재설치하기
    ```shell
    helm upgrade --install my-first-spark bitnami/spark --version 7.2.2 -n default \
      --set service.type=NodePort \
      --set service.nodePorts.cluster=30077 \
      --set service.nodePorts.http=30078 \
      --set worker.replicaCount=3
    ```

<br>

# 간단한 Helm 명령어 예제
  1) Helm 설치 확인
     ```
      Helm 버전 정보 확인해보기
      [root@helm-client ~]# helm version
     ```
  
  2) Helm repo 관리 명령어
     ```
      [root@helm-client ~]# helm repo list
      [root@helm-client ~]# helm repo remove 리포이름
     ```
  
  3) Helm repo 및 chart 조회
     ```
      [root@helm-client ~]# helm search repo bitnami
      [root@helm-client ~]# helm search repo bitnami/spark --versions
      기본 values.yaml 보기
      [root@helm-client ~]# helm show values bitnami/spark
     ```

<br>

# 다양한 스파크 설치 관련 옵션
더 다양한 옵션들은 아래 사이트에서 확인 가능하다.
- [https://artifacthub.io/packages/helm/bitnami/spark](https://artifacthub.io/packages/helm/bitnami/spark)
