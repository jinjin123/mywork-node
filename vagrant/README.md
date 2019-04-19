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
