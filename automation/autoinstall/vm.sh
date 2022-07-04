#!/usr/bin/env bash
 
## Define variables
MEM_SIZE=2048       # Memory setting in MiB
VCPUS=2             # CPU Cores count
OS_VARIANT="rhl8.0" # List with osinfo-query  os
ISO_FILE="/raid/CentOS-7-x86_64-Minimal-2009.iso"

echo -en "Enter vm name: "
read VM_NAME
OS_TYPE="linux"
echo -en "Enter virtual disk size : "
read DISK_SIZE
 
sudo virt-install \
     --name ${VM_NAME} \
     --memory=${MEM_SIZE} \
     --vcpus=${VCPUS} \
     --os-type ${OS_TYPE} \
     --location ${ISO_FILE} \
     --disk path=/mnt/raid0/centos.qcow2,device=disk,cache=none,bus=virtio,size=${DISK_SIZE}  \
     --network bridge=virbr0 \
     --graphics=none \
     --os-variant=${OS_VARIANT} \
     --console pty,target_type=serial \
     --initrd-inject ks.cfg --extra-args "inst.ks=file:./ks.cfg  console=tty0 console=ttyS0,115200n8"
     #--extra-args="ks=http://192.168.122.1/ks.cfg console=tty0 console=ttyS0,115200n8"
