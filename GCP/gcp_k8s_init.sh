#!/bin/bash

# 시스템 업데이트
yum -y update
timedatectl set-timezone Asia/Seoul

# tc 관련 경고 로그 해결
echo '======== [4-4] [WARNING FileExisting-tc]: tc not found in system path 로그 관련 업데이트 ========'
yum install -y yum-utils iproute-tc

# kube에서 사용하는 port에 대한 방화벽 설정
echo '======== [4-5] kube용 방화벽 허용 설정(6443,10250) ========'
sudo firewall-cmd --zone=public --add-port=6443/tcp --permanent
sudo firewall-cmd --zone=public --add-port=10250/tcp --permanent
sudo firewall-cmd --reload

# Swap 비활성화
echo '======== [5] Swap 비활성화 ========'
echo '======== [5] kubelet 컴포넌트가 제대로 동작하기 위해 ========'
swapoff -a && sed -i '/ swap / s/^/#/' /etc/fstab

# 컨테이너 런타임 설치 전 사전작업
echo '======== [6] 컨테이너 런타임 설치 ========'
echo '======== [6-1] 컨테이너 런타임 설치 전 사전작업 ========'
echo '======== [6-1] iptable 세팅 ========'
cat <<EOF |tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter

# 시스템 설정 조정
cat <<EOF |tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sysctl --system

# containerd 설치
echo '======== [6-2] 컨테이너 런타임 (containerd 설치) ========'
echo '======== [6-2-1] containerd 패키지 설치 (option2) ========'
echo '======== [6-2-1-1] docker engine 설치 ========'
echo '======== [6-2-1-1] repo 설정 ========'
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

echo '======== [6-2-1-1] containerd 설치 ========'
yum install -y containerd.io
systemctl daemon-reload
systemctl enable --now containerd

# CRI 활성화
echo '======== [6-3] 컨테이너 런타임 : cri 활성화 ========'
sed -i 's/^disabled_plugins/#disabled_plugins/' /etc/containerd/config.toml
systemctl restart containerd

# kubeadm, kubelet, kubectl 설치
echo '======== [7] kubeadm 설치 ========'
echo '======== [7] repo 설정 ========'
mv /etc/yum.repos.d/kubernetes.repo /etc/yum.repos.d/kubernetes.repo.backup 2>/dev/null || :
cat <<EOF |tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.27/rpm/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.27/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl
EOF

# SELinux 설정 조정
echo '======== [7] SELinux 설정 ========'
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

# Kubernetes 패키지 설치
echo '======== [7] kubelet, kubeadm, kubectl 패키지 설치 ========'
yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
systemctl enable --now kubelet


