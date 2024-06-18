# Helm용 VM 구성
  - 앞서 만든 베이스 머신 이미지 이용해서 새로운 VM을 하나 만든다. K8S worker node 세팅 부분 [참조](https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/GCP_VM_setting.md#k8s-worker-node-%EC%84%B8%ED%8C%85)
  - VSCode 접속 환경도 구성한다.

# Helm 설치
서버에 접속 후 [install.sh](https://github.com/seoddong/k8s-spark-on-prem/blob/main/helm/install.sh) 스크립트 실행 (VSCode로 새 파일 만들고 스크립트 복사해서 넣고 저장하고 권한 주고.. 이런 작업은 앞서 했으니 자세한 설명은 생략)

# kubectl 설치
Helm이 k8s와 통신하기 위해 kubectl을 설치해야 한다. 아래 코드를 한 줄 씩 실행한다.
```shell
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod 700 ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
```
