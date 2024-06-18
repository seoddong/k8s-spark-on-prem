# 목차
- [k8s 구성을 위한 GCP K8S-master VM 세팅](#k8s-구성을-위한-GCP-K8S-master-VM-세팅)
- [K8S Worker Node 세팅](#k8s-worker-node-세팅)
- [외부에서 k8s에 접근하기 위한 GCP 방화벽 설정](#외부에서-k8s에-접근하기-위한-GCP-방화벽-설정)
- [K8S 대시보드 확인](#k8s-대시보드-확인)


<br><br><br><br>

# k8s 구성을 위한 GCP K8S-master VM 세팅
본 과제는 TCP 무료 계정(3개월/40만원 혜택)을 사용하여 진행함.
1. 기본 이미지용 VM 생성
   - 이름: k8s-master
   - 리전: us-west4(라스베이거스)
   - 머신: E2 medium (2vcore, 4GB)
   - 부팅디스크:  Rockylinux
   - 방화벽: HTTP 체크, HTTPS 체크
   - 만들기 클릭

2. VSCode 접속을 위한 root 사용 권한 설정(root 로그인 허용 및 패스워드 인증 허용)
   - SSH 연결(웹 터미널)
   - root 사용 권한 설정
      ```shell
      $sudo su
      $passwd
      Changing password for user root.
      New password:자신의 암호 입력
      Retype new password:방금 입력한 암호 한 번 더 입력 
      passwd: all authentication tokens updated successfully.
      ```
  
    - sshd_config 설정 변경
      (전통적인 방법)
      ```
      $vi /etc/ssh/sshd_config

      vi 편집 화면에서 아래 문구를 찾아 yes로 바꾸고 저장
      PermitRootLogin yes
      PasswordAuthentication yes
      
      $systemctl restart sshd
      ```
  
      (좀 더 편한 방법)
      ```shell
      $sed -i 's/^PermitRootLogin no/PermitRootLogin yes/' /etc/ssh/sshd_config
      $sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
      $systemctl restart sshd
      ```

3. VSCode에서 k8s-master 서버 접속
   - VSCode에서 Ctrl + Shift + P
   - Remote-SSH: SSH 구성 파일 열기… 선택<br>
     - C:\User\[본인계정]\.ssh\config 선택<br>
     - 접속할 호스트 정보 추가 (Host 이름이 실제 이름과 같을 필요는 없음. IP만 같으면 됨)<br>
     - config 파일 저장<br>
     ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/055e3add-e6bb-496c-b765-de1c97b56b37)
   - 호스트에 연결<br>
     ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/0d7607bf-1c12-4d3d-a8ea-30066624351a)

4. k8s-master 서버에 k8s-master용 환경 세팅하기
   - [gcp_k8s_init.sh](https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/gcp_k8s_init.sh) 파일을 열고 안의 스크립트를 모두 복사한다.
   - VSCode에서 파일 > 새 텍스트 파일 메뉴 클릭해서 새 창을 열고 스크립트를 붙여넣는다.
   - 파일 > 저장 (or Ctrl+S)을 누르고 /root/k8s/gcp_k8s_init.sh 이름으로 저장한다.(새 폴더를 만들면서 저장할 것인지 물어보면 순순히 응할 것)
   - 터미널 창에서 저장한 파일을 실행한다.(방금 저장한 파일은 실행 권한이 없으므로 실행 권한을 부여한다)
     ```shell
     $chmod +x ./k8s/gcp_k8s_init.sh
     $./k8s/gcp_k8s_init.sh
     ```

5. 현재까지 작업한 k8s-master 서버를 이용하여 GCP Base Image 생성
   ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/0d5b2252-1728-46cc-b019-8995f3ae4fd4)
   - 이름: img-k8s-base-v1
   - 만들기 클릭
  
6. k8s-master 서버 세팅 마무리
   - 고정IP 적용(수정 > 네트워크 인터페이스 > 외부IPv4 주소 > 고정 외부IP 주소 예약: k8s-master-ip)
   - [gcp_k8s_master.sh](https://github.com/seoddong/k8s-spark-on-prem/blob/main/k8s1.27/gcp_k8s_master.sh) 파일을 열고 안의 스크립트를 모두 복사한다.
   - VSCode에서 파일 > 새 텍스트 파일 메뉴 클릭해서 새 창을 열고 스크립트를 붙여넣는다.
     ### <span style="color: orange;">!!!중요!!!</sapn> 스크립트에서 <span style="color: orange;">GCP내부망주소</sapn>와 <span style="color: orange;">GCP외부망주소</sapn> 부분을 자신의 서버 정보에 맞게 수정한다.
     ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/3c27b29f-d853-4ad0-9da7-855a1c1eaa5a)
   - 파일 > 저장 (or Ctrl+S)을 누르고 /root/k8s/gcp_k8s_master.sh 이름으로 저장한다.(새 폴더를 만들면서 저장할 것인지 물어보면 순순히 응할 것)
   - 터미널 창에서 저장한 파일을 실행한다.
      방금 저장한 파일은 실행 권한이 없으므로 실행 권한을 부여한다.
     ```shell
      $chmod +x ./k8s/gcp_k8s_master.sh
      $./k8s/gcp_k8s_master.sh
     ```


# K8S worker node 세팅
1. k8s worker node 세팅(3대 기준)
   - GCP 머신이미지의 인스턴스 만들기를 이용하여 VM 생성
     ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/c25aa7d2-efbe-45e5-997b-48e7812fb671)
   - 이름: k8s-node1, k8s-node2, k8s-node3
   - 방화벽: HTTP 체크, HTTPS 체크
   - 만들기 클릭

2. VSCode의 SSH 구성 파일에 아래 그림처럼 서버 정보를 추가하고 새로 만든 VM에 접속
   ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/a38c836a-8270-4395-b743-5a8b61e2697b)

3. K8S worker node들을 k8s-master와 연결(클러스터링)
   - k8s-master 서버에 접속하여 연결 명령어 출력
     ```shell
     $cat ./join.sh
     kubeadm join 192.168.56.30:6443 --token 7uruf6.n2w97dphqikk5m8f --discovery-token-ca-cert-hash sha256:b889a7b0767bde6e8d1dca4b326ef31669a7c6a4495ac18c7884d0dc41649e8f
     ```
   - 위 출력된 문자열을 카피하여 worker node 1,2,3에 접속하여 터미널에 붙여넣고 실행시킨다.
   - 간혹 연결이 안 되는 경우가 있는데 이 때는 토큰을 새로 생성하여 출력된 문자열로 작업하면 된다.
     ```shell
     $kubeadm token create --print-join-command
     ```
   - k8s-master에서 worker node들이 잘 연결되어 있는지 확인한다.
     ```shell
     kubectl get nodes
     ```
     추가한 worker node들이 보인다면 잘 연결된 것이다.


# 외부에서 k8s에 접근하기 위한 GCP 방화벽 설정
   ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/28a3279d-fa43-4b67-9e43-9fe36a8ba48a)
   - GCP 메뉴: VPC 네트워크 > 방화벽
   - 방화벽 규칙 만들기 선택
   - 이름: k8s-spark
   - 대상: 네트워크의 모든 인스턴스
   - 소스 IPv4 범위: 0.0.0.0/0
   - TCP 체크, 포트: 6443
   - 만들기 선택
   - 어차피 나중에 아 포트들 추가해야 하므로 여기서 미리 추가해놓는 것도 좋다.<br>
     3306,4040,4041,5001-5003,6443,8080,8888,30000,30007,30077,30078,30079-30081,30705
   - 포트 설명
     - 3306 MariaDB (외부에서는 이 포트로 접속 불가)
     - 4040, 4041 Spark Jobs UI
     - 5001-5003 왜 열었는지 생각 안 남
     - 6443 k8s 통신
     - 8080 python tailon 서비스(서버 로그 파일의 tail 결과를 실시간 웹으로 서비스)
     - 8888 jupyter notebook web
     - 30000 k8s 대시보드
     - 30007 mariaDB의 nodeport (외부에서 접속할 때 사용)
     - 30077 spark간 통신용 nodeport
     - 30078 spark Web UI 접속용 nodeport
     - 30079-30081 spark executor WEb UI 접속용 nodeport

# k8s 대시보드 확인
   1) https://<<k8s-master 외부IP>>:30000
   2) 위 URL에 접속 후 고급 > "안전하지 않음" 클릭
   3) 만약 로그인/토큰 팝업 창이 뜬다면 "생략" 버튼 클릭
   ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/9751d15d-d49d-45af-abfd-95cc9834beaf)

