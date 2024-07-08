# ansible local에 jenkins & ngrok 설치하기
ansible 서버에 도커를 설치하고 jenkins와 ngrok을 모두 도커 컨테이너를 땡겨와서 설치하는 방법

1. ansible hosts에 자기 자신 등록
   
    ```shell
    [ansible]
    ansible-master ansible_host=127.0.0.1 ansible_connection=local
    ```
   
2. jenkins 설치용 playbook 작성
   
    jenkins-playbook.yaml <br>
    - 참고로 아래 과정 중 Install Jenkins 과정이 매우 오래 걸리니 (10분?) 끈기있게 기다릴 것
    - github 등 외부에서 jenkins 접근이 용이하도록 ngrok도 같이 설치
  
      ```yaml
      ---
      - name: Install Jenkins and ngrok with Docker
        hosts: ansible-master
        become: yes
        tasks:
      
          - name: Install required dependencies
            yum:
              name: 
                - python3-pip
                - yum-utils
                - device-mapper-persistent-data
                - lvm2
              state: present
          
          - name: Install requests library
            pip:
              name: requests
              state: present
      
          - name: Install and update Docker repository
            shell: |
              yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
              yum makecache
      
          - name: Install Docker
            yum:
              name:
                - docker-ce
                - docker-ce-cli
                - containerd.io
              state: present
      
          - name: Start and enable Docker
            service:
              name: docker
              state: started
              enabled: yes
      
          - name: Add user to docker group
            user:
              name: "root"
              groups: docker
              append: yes
      
          - name: Pull Jenkins Docker image
            docker_image:
              name: jenkins/jenkins
              tag: lts
              source: pull
      
          - name: Run Jenkins Docker container
            docker_container:
              name: jenkins
              image: jenkins/jenkins:lts
              ports:
                - "8080:8080"
                - "50000:50000"
              restart_policy: always
              state: started
      
          - name: Pull ngrok Docker image
            docker_image:
              name: ngrok/ngrok
              tag: latest
              source: pull
      
      ```

3. Unlock Jenkins
   - server-ip:8080 접속 후 패스워드 경로 보고 파일 열면 패스워드 보임<br>경로를 열기 위해 도커 컨테이너로 들어가야 함
     ```shell
     docker ps
     docker exec -it [컨테이너 이름 또는 ID] /bin/bash
     cat /var/jenkins_home/secrets/initialAdminPassword
     ```
   - 해당 패스워드를 브라우저에 입력 후 디폴트 옵션으로 젠킨스 설정
   - admin으로 로그인 과정 스킵

4. Ngrok 설정
   - ngrok을 사용하기 위해서는 https://ngrok.com 접속 후 회원가입 필요
   - 로그인 후 setup & installation 메뉴(https://dashboard.ngrok.com/get-started/setup/linux)에서 authtoken 값 확인 가능
   - 도커 실행 명령어
      ```shell
      docker run --net=host -it -e NGROK_AUTHTOKEN=MlUrSbVnI6...(authtoken값 입력) ngrok/ngrok:latest http 8080
      ```

5. Jenkins - github 연동 설정
    - https://www.youtube.com/watch?v=GE-jl7Cwiuk
    - jenkins git credential 생성: https://medium.com/@sneakstarberry/jenkins-git-credential-%EB%93%B1%EB%A1%9D-aff572de329e
    - 
