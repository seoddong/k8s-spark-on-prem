# ansible local에 jenkins 설치하기
ansible 서버에 jenkins 설치하는 방법

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
      - name: Install Jenkins and ngrok
        hosts: ansible-master
        become: yes
        tasks:
      
          - name: Install required dependencies
            yum:
              name: 
                - java-11-openjdk
                - wget
                - unzip  # 여기에 unzip 추가
              state: present
      
          - name: Add Jenkins repository
            command: >
              wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
            args:
              creates: /etc/yum.repos.d/jenkins.repo
      
          - name: Import Jenkins repository key
            rpm_key:
              key: https://pkg.jenkins.io/redhat-stable/jenkins.io.key
      
          - name: Install Jenkins
            yum:
              name: jenkins
              state: present
      
          - name: Ensure Jenkins is running
            service:
              name: jenkins
              state: started
              enabled: yes
      
          - name: Install EPEL repository for ngrok dependency
            yum:
              name: epel-release
              state: present
      
          - name: Install ngrok
            get_url:
              url: https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
              dest: /tmp/ngrok.zip
      
          - name: Unzip ngrok
            unarchive:
              src: /tmp/ngrok.zip
              dest: /usr/local/bin/
              remote_src: yes
      
          - name: Make ngrok executable
            file:
              path: /usr/local/bin/ngrok
              mode: '0755'
      
          - name: Start ngrok on boot
            copy:
              content: |
                [Unit]
                Description=Ngrok
                After=network.target
      
                [Service]
                ExecStart=/usr/local/bin/ngrok http 8080
                Restart=on-failure
                User=root
      
                [Install]
                WantedBy=multi-user.target
              dest: /etc/systemd/system/ngrok.service
      
          - name: Reload systemd configuration
            systemd:
              daemon_reload: yes
      
          - name: Enable and start ngrok
            systemd:
              name: ngrok
              enabled: yes
              state: started
      
      ```

3. Unlock Jenkins
   - server-ip:8080 접속 후 패스워드 경로 보고 파일 열면 패스워드 보임
   - 해당 패스워드를 브라우저에 입력 후 디폴트 옵션으로 젠킨스 설정
   - admin으로 로그인 과정 스킵

4. Ngrok 설정
   - ngrok을 사용하기 위해서는 https://ngrok.com 접속 후 회원가입 필요
   - 로그인 후 setup & installation 메뉴(https://dashboard.ngrok.com/get-started/setup/linux)에서 authtoken 값 확인 가능
   - 위 메뉴에서 알려주는 ngrok config add-authtoken 2MlUrSbVnI6Q... 명령어는 작동되지 않으므로 아래 명령어 이용해서 토큰 등록
     ```
     ngrok authtoken 2MlUrSbVnI6Q...
     ```
   - 
