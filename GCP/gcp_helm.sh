#!/bin/bash

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc # PATH 업데이트
source ~/.bashrc
