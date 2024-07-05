1. Vagrant로 로컬 VM에 Ansible 서버 설치
    ```shell
    dnf install epel-release -y
    dnf install ansible -y
    ```

2. Ansible 서버 접속하여 잘 설치되었는지 확인
    ```shell
    ansible --version
    ```

3. 원격서버와 통신하기 위한 SSH key 생성
   ```shell
   ssh-keygen
   ssh-copy-id [원격서버계정ID]@[원격서버IP]
   ```
   
   copy에 성공했다면 아래 명령으로 접속 시도
   ```shell
   ssh [원격서버계정ID]@[원격서버IP]
   ```

4. 인벤토리 파일 작성
   ```shell
   vi /etc/ansible/hosts

   ##seoddong-web
   34.121.212.104
   ```

   방금 등록한 서버들 접속이 잘 되는지 확인
   ```shell
   ansible all -m ping
   ```
