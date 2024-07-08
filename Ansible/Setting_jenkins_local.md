# ansible local에 jenkins 설치하기
ansible 서버에 jenkins 설치하는 방법

1. ansible hosts에 자기 자신 등록
   
    ```shell
    [ansible]
    ansible-master ansible_host=127.0.0.1 ansible_connection=local
    ```
   
2. jenkins 설치용 playbook 작성
   
    jenkins-playbook.yaml <br>
    참고로 아래 과정 중 Install Jenkins 과정이 매우 오래 걸리니 (10분?) 끈기있게 기다릴 것
  
    ```yaml
    ---
    - name: Install Jenkins
      hosts: ansible-master
      become: yes
      tasks:
    
        - name: Install required dependencies
          yum:
            name: 
              - java-11-openjdk
              - wget
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
    ```

3. Unlock Jenkins
   - server-ip:8080 접속 후 패스워드 경로 보고 파일 열면 패스워드 보임
   - 해당 패스워드를 브라우저에 입력 후 디폴트 옵션으로 젠킨스 설정
   - 
