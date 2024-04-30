
# jupyter home
jupyter home 폴더는 jupyter notebook 서버가 실행되는 경로

ex) root경로에서 jupyter notebook을 실행하였다면 jupyter home은 root가 됨 
```shell
rm nohup.out
nohup jupyter notebook --ip='0.0.0.0' --port=8888 --no-browser --allow-root &
cat nohup.out
```
