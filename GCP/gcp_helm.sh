#!/bin/bash

echo '========== [1] helm 설치 =========='
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc # PATH 업데이트
source ~/.bashrc

echo '========== [2] kube 연결 설정 =========='
mkdir ~/.kube
scp root@쿠베마스터외부IP:~/.kube/config .kube/config
echo '=========='
echo '========== config 파일 열고 내부IP를 외부IP로 수정하세요'
echo '=========='
