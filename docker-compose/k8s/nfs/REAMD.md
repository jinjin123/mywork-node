```
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/

helm repo update

tar -zxvf nfs-subdir-external-provisioner-4.0.16.tgz

修改 values.yaml 文件，更改镜像为阿里云镜像

replicaCount: 1
strategyType: Recreate

image:
  repository: registry.cn-hangzhou.aliyuncs.com/lzf-k8s/k8s-nfs-storage #-
  tag: 1.0.0 #-
  pullPolicy: IfNotPresent
imagePullSecrets: []

---
官方例子
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=x.x.x.x \
    --set nfs.path=/exported/path \
    -f values.yaml
使用线上模板，需要指定 values.yaml
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner --set nfs.server=192.168.140.28  --set nfs.path=/home/nfs -f values.yaml

使用本地模板
 helm install  nfs-subdir-external-provisioner nfs-subdir-external-provisioner/  --set nfs.server=192.168.14

 默认的 storageClass 是 nfs-client

```
