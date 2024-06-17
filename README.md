# k8s-spark에 대하여
k8s 1.27 버전에 spark 3.4.1 버전으로 클러스터링 구성하며 전체적인 아키텍처는 아래 그림 참조
![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/9f49cf1d-5cb4-4aae-9ffb-6f02610ede99)

# k8s 구성을 위한 VM 세팅
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
   - gcp_k8s_init.sh 파일을 열고 안의 스크립트를 모두 복사한다.
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


