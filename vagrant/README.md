#### Signal kubenets cluster on Vagrant

$ vagrant ssh k8s-master
vagrant@k8s-master:~$ kubectl get nodes
NAME         STATUS   ROLES    AGE     VERSION
k8s-master   Ready    master   18m     v1.14.1
node-1       Ready    <none>   12m     v1.14.1
node-2       Ready    <none>   6m22s   v1.14.1

$ ## Accessing nodes
$ vagrant ssh node-1
$ vagrant ssh node-2


### Note

if you inside the wall and want quickly install, the best way is save the k8s componets images

### through socket5 proxy export ALL_PROXY=socks5://172.18.8.1:1086

$num_instances = 3
$vm_gui = false
$vm_memory = 1024
$vm_cpus = 1
$instance_name_prefix = "ubuntu"
$vb_cpuexecutioncap = 100

def vm_gui
  $vb_gui.nil? ? $vm_gui : $vb_gui
end

def vm_memory
  $vb_memory.nil? ? $vm_memory : $vb_memory
end

def vm_cpus
  $vb_cpus.nil? ? $vm_cpus : $vb_cpus
end

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  (1..$num_instances).each do |i|
    config.vm.define vm_name = "%s-%02d" % [$instance_name_prefix, i] do |config|
      config.vm.hostname = vm_name

      config.vm.provider :virtualbox do |vb|
        vb.gui = vm_gui
        vb.memory = vm_memory
        vb.cpus = vm_cpus
        vb.customize ["modifyvm", :id, "--cpuexecutioncap", "#{$vb_cpuexecutioncap}"]
      end

      ip = "172.18.8.#{i+100}"
      config.vm.network :private_network, ip: ip

      config.vm.synced_folder "./data", "/vagrant_data"
    end
    # config.vm.provision "shell", inline: "echo 'deb http://apt.kubernetes.io/ kubernetes-xenial main'>/etc/apt/sources.list.d/kubernetes.list"
    # config.vm.provision "shell", inline: "cat /etc/apt/sources.list.d/kubernetes.list"
    # config.vm.provision "shell", inline: <<-SHELL
    #   export ALL_PROXY=socks5://172.18.8.1:1086
    #  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    #  apt-get update
    #  apt-get install -y docker.io kubelet kubeadm kubectl kubernetes-cni
    #SHELL
  end
end

