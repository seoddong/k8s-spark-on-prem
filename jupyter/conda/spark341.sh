# !!! 주의 !!! #
# 중간에 가상환경 들어가서 실행하는 부분 때문에 한 줄씩 실행해야 함

# Create a conda environment that uses Python 3.11
conda create --name spark341 python=3.11.8 -y

conda activate spark341
conda install -c conda-forge openjdk=11.0.13 -y
# pip install delta-spark==2.3.0 pyspark==3.3.2
pip install pyspark==3.4.1

# 주피터 노트북에서 커널로 선택할 수 있도록 설정
# 주피터 노트북은 base에 설치해도 됨
conda install -n spark341 ipykernel --update-deps --force-reinstall -y
