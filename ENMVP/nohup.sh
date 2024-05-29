nohup /root/miniconda3/envs/spark341/bin/python /root/jupyterHome/MVPSS_main.py > output.log 2>&1 &
echo $! > script_pid.txt