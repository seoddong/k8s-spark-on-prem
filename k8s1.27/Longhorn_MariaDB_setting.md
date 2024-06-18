# Longhorn 설치
Longhorn 설치 위한 전제조건으로 open iscsi 설치해야 하는데 이미 베이스이미지 만들 때 설치해놓았다.<br>
Longhorn에 대해 자세히 알고 싶으면 ChatGPT에게 물어보자.

kube기반이므로 역시 helm을 이용하여 쉽게 설치할 수 있다.
1) 우선 Longhorn repo를 추가한다.
    ```shell
    [root@helm-client ~]# helm repo add longhorn https://charts.longhorn.io
    [root@helm-client ~]# helm repo update
    ```

3) Longhorn용 config.yaml 파일 생성
    Longhorn은 분산 스토리지라서 기본적으로 replica=3인데 우리는 이 옵션이 부담스러우므로 1로 바꿔 적용하자.
    그러려면 설정을 적용할 Longhorn용 config.yaml 파일을 만들어야 한다.<br>
    VSCode로 Helm-client 서버에 접속 후 새 파일 만들고 아래 내용을 입력하자.
    ```shell
    csi:
      attacher:
        replicaCount: 1
      provisioner:
        replicaCount: 1
      resizer:
        replicaCount: 1
      snapshotter:
        replicaCount: 1
    
    longhornUI:
      replicaCount: 1
    ```
    저장할 때 Longhorn 폴더를 만들어 config-longhorn.yaml 이름으로 저장하자.

4) Helm으로 Longhorn 설치
   일반적으로 longhorn-system 네임스페이스에 설치한다고 한다.
   ```shell
   [root@helm-client ~]# helm install longhorn longhorn/longhorn --namespace longhorn-system --create-namespace --set service.ui.nodePort=30705,service.ui.type=NodePort --values ./longhorn/config-longhorn.yaml
   ```
    설치가 완료되는데 시간이 꽤 걸린다. (약 10분 정도)<br>
    설치 후 [http://<<k8s-master 외부IP>>:30705/#/dashboard](http://<<k8s-master 외부IP>>:30705/#/dashboard)에서 Web UI 확인 가능하다.

<br>

# MariaDB 설치

