# Spark UI 관련 추가 환경 구성
spark UI를 제대로 사용하려면 k8s의 서비스 설정을 바꿔야 한다. 관련 정보는 k8s 폴더에서 확인하자.

# Spark Web UI 확인하기
아래 URL에 접속하여 확인한다. 30078은 helm에서 sparkk 설치할 때 지정한 Nodeport이다.
- http://[k8s-master IP]:30078

# Spark Executor Web UI 확인하기
Spark Application을 만들고 실행시키면 executor가 실행되는데 각 executor도 접속 가능한 링크가 있다.

그러나 해당 링크는 k8s 파드의 내부 IP이기 때문에 외부에서 접속되지 않아 k8s-nodeport 설정이 필요하다.
- 이에 대한 설정은 (https://github.com/seoddong/k8s-on-prem/blob/e9d45bf0ed097dd529280897ce43691e50b3c731/k8s1.27/README.md)을 참고하자.
설정을 완료했다면 http://[k8s-master IP]:30079, http://[k8s-master IP]:30080, http://[k8s-master IP]:30081 에 접속하여 확인 가능하다.

# Spark Application Detail UI 확인하기
Spark Application을 만들어 실행시키고 running 중인 application에 들어가보면 Application Detail UI 링크가 활성화 된 것을 볼 수 있다.
- http://jupyter-notebook.us-central1-a.c.oceanic-hold-423500-q3.internal:4041/
그러나 위와 같이 링크가 spark driver 위치의 호스트 주소 형태로 반환되는데 외부망에서 접속이 안 된다.
이는 GCP에서 방화벽 4041포트를 열고 외부 IP를 이용하여 접속하면 정상적으로 열리는 것을 확인할 수 있다. 
