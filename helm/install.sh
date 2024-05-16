#!/bin/bash

sudo dnf update -y
sudo dnf install -y curl git # git 설치 추가
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc # PATH 업데이트
source ~/.bashrc
