## 목차

<br><br><br><br>

# Conda 설치
  Jupyter notebook의 쉬운 설치 뿐만 아니라 편리한 파이썬 가상 환경 관리 위해 Conda를 설치한다.<br>
  여기서는 가볍고 빠른 설치 위해 Miniconda 설치한다.
  ```shell
  [root@jupyter-notebook ~]# dnf install wget -y
  [root@jupyter-notebook ~]# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  [root@jupyter-notebook ~]# chmod +x Miniconda3-latest-Linux-x86_64.sh
  [root@jupyter-notebook ~]# ./Miniconda3-latest-Linux-x86_64.sh
  ```
  - 설치 과정에서 약관 동의 필요(약관 전문 보게 하는데 스페이스 연타로 빨리 넘기고 yes)
  - 이렇게 물어보면 그냥 엔터<br>
   ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/f4d81f94-c82a-4909-adcb-217219b8e519)

  - 마지막 질문은 yes (사실 yes와 no의 차이를 잘 모름)<br>
   ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/005c4fae-cbc1-4da5-a75c-293df9058e09)

  - 설치 완료 후 VSCode의 터미널 재시작 권장함

<br>

# 가상환경(spark341) 생성
  spark 3.4.1과 가장 궁합이 잘 맞는 버전의 라이브러리들을 설치할 가상 환경을 만든다.
  pyspark는 자바기반이므로 openjdk 설치 필수.
  ```shell
  # 중간에 가상환경 들어가서 실행하는 부분 때문에 한 줄씩 실행해야 함
  # spark 3.4.1 wants Python 3.9.19
  conda create --name spark341 python=3.9.19 -y
  conda activate spark341
  # conda-forge에서 opnejdk를 가져와 설치하라
  conda install -c conda-forge openjdk=11.0.13 -y
  pip install pyspark==3.4.1
  ```
  openjdk를 가상환경에 들어가서 설치하면 이 가상환경에만 해당되는 줄 알았는데 사용하다 보니 그건 아닌 것 같다.

<br>

# 주피터 노트북 설치
  ```shell
  (spark341) [root@jupyter-notebook ~]# conda install jupyter -y
  (spark341) [root@jupyter-notebook ~]# jupyter notebook --generate-config # 한 번만 실행하면 되는 듯
  주피터 노트북은 root 권한으로 실행되는 것을 싫어하므로 root로 실행하는 옵션을 준다. 
  (spark341) [root@jupyter-notebook ~]# jupyter notebook --ip='0.0.0.0' --port=8888 --no-browser --allow-root
  ```
  주피터 노트북이 실행되면 아래 그림처럼 결과가 나오는데 둘 중 하나 링크 클릭하여 브라우저에서 확인한다.
  ![image](https://github.com/seoddong/k8s-spark-on-prem/assets/15936649/4f0aa60a-55d7-4d80-bb4e-8a0b29c0b1f5)

  - 링크 클릭해도 화면이 안 나오는 경우는 서버 주소 부분을 Helm-Client 서버 외부IP로 변경해보자.

<br>

# 주피터 노트북 백그라운드 실행
  nohup 명령어로 주피터 노트북을 백그라운드에서 실행하고 종료하기.
  ```shell
  백그라운드에서 실행하기
  (spark341) [root@jupyter-notebook ~]# nohup jupyter notebook --ip='0.0.0.0' --port=8888 --no-browser --allow-root &

  jupyter notebook web 접속 링크 확인하기
  (spark341) [root@jupyter-notebook ~]# cat ./nohup.out

  실행중인 프로세스를 찾아 죽이는 명령
  (spark341) [root@jupyter-notebook ~]# ps aux | grep jupyter
  (spark341) [root@jupyter-notebook ~]# kill -9 프로세스번호
  ```

<br>

# jupyter home
파이썬 소스 파일 관리 상 jupyter home 폴더 만들고 여기에 ipynb나 py파일을 위치시킨다.

