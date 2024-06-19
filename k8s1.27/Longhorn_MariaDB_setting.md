# 목차
- [Longhorn 설치](#Longhorn-설치)
- [MariaDB 설치](#MariaDB-설치)
- [MariaDB 접속 테스트](#MariaDB-접속-테스트)

<br><br><br><br>

# Longhorn 설치
Longhorn 설치 위한 전제조건으로 k8s가 구동되는 VM에 open iscsi를 설치해야 하는데 이미 베이스이미지 만들 때 설치해놓았다.<br>
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
MariaDB 역시 Helm으로 간단하게 설치할 수 있다. <br>
일반적으로 MariaDB는 3306포트를 사용하지만 여기서는 k8s에서 구동되므로 외부 접속을 위해 30007로 nodeport 설정하여 외부 접속하도록 하였다.<br>

```shell
DB암호설정 문구를 자기가 사용하고자 하는 암호로 바꾸고 실행시킨다.
helm install my-first-mariadb bitnami/mariadb \
    --namespace default \
    --set primary.service.type=NodePort \
    --set primary.service.nodePort=30007 \
    --set auth.rootPassword=DB암호설정 \
    --set auth.database=sparkdb
```
- 방화벽 해제: 설치 후 접속 위해서 GCP 방화벽 해제 작업해야 하는데 여기서는 k8s 구축할 때 미리 다 해 놓았다.

<br>

# MariaDB 접속 테스트
  - Windows: 그냥 DBWeaver 설치해서 접속하면 끝
  - Linux: Helm-client서버 등 k8s 외부 서버에서 아래 스크립트 이용해서 mysql client 설치한 후 접속 테스트
    ```shell
    dnf install mysql –y로 mysql 설치하고 접속 테스트 (패스워드 물어봄)
    mysql -h <<k8s-master외부IP>> -P 30007 -u root -p
    
    mysql 프롬프트 나오면,
    SHOW DATABASES;
    
    USE sparkdb;
    CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255));
    INSERT INTO test (name) VALUES ('example');
    
    SELECT * FROM test;
    exit;
    ```

