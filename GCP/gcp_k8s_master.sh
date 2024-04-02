#!/bin/bash

# 클러스터 생성
echo '======== [8] kubeadm으로 클러스터 생성  ========'
echo '======== [8-1] 클러스터 초기화 (Pod Network 세팅) ========'
kubeadm init --pod-network-cidr=20.96.0.0/12 --apiserver-advertise-address 10.182.0.2 <-- !!!!!!!! master 서버 IP로 입력하세요 !!!!!!!!
kubeadm token create --print-join-command > ~/join.sh

# kubectl 사용 설정
echo '======== [8-2] kubectl 사용 설정 ========'
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config

# Pod Network 설치 (calico)
echo '======== [8-3] Pod Network 설치 (calico) ========'
kubectl create -f https://raw.githubusercontent.com/k8s-1pro/install/main/ground/k8s-1.27/calico-3.25.1/calico.yaml
kubectl create -f https://raw.githubusercontent.com/k8s-1pro/install/main/ground/k8s-1.27/calico-3.25.1/calico-custom.yaml

# 쿠버네티스 편의기능 설치
echo '======== [9] 쿠버네티스 편의기능 설치 ========'
echo '======== [9-1] kubectl 자동완성 기능 ========'
echo "source <(kubectl completion bash)" >> ~/.bashrc
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc

# Dashboard 설치
echo '======== [9-2] Dashboard 설치 ========'
kubectl create -f https://raw.githubusercontent.com/k8s-1pro/install/main/ground/k8s-1.27/dashboard-2.7.0/dashboard.yaml

echo '======== 모든 설치 과정이 완료되었습니다. ========'
