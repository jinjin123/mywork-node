- This Ansible Playbook will help you create a `AWS EC2 Infrastructure` and setup `Hadoop Cluster` use [HDP](https://hortonworks.com/products/data-platforms/hdp/)
- The AWS EC2 must be Centos distro 
###Note
aws nat gateway has issue when handle private instance yum install package, you can put them on public group with public IP

# 1. Create a AWS Infrastructure

This role setups the following:

* VPC
* Two networks(private and public)
* Create 1 public instance that will take as Bastion host, create 5 private instances that will take the roles: Ambari server, Namenodes, Datanodes .
* Assign public IP for public instance
* Adds internet gateway and NAT gateway to allow communication between networks and internet
* General new hosts group to the `path_hosts_group`, the path to hosts group file must created
* Allows to cleanup VPC and all created AWS resources

### a. Require

- Create ssh keys pair and paste the content of the public key into `roles/create_ec2_vpc/files/aws.pub`
- Set absolute path of your private key in `group_vars/all.yaml` at row `private_key` 

Example:

```
private_key: /Users/tinhuynh/Work/keys/my_key # Must be absolute path to your private key
```

### b. Prepare
##### Change the parameters match with your requirement!

- Edit `group_vars/all.yaml` file

##### Choose the mode for your system: 

Does EC2 instance need Avaibility Zone or NOT?

- Edit the file `create_hdp_infrastructure.yml`

* Multi AZ: 
```
roles:
    - { role: create_ec2_vpc, mutiAZ: "yes", tags: [ "create" ] }
    - { role: clean-ec2-vpc, mutiAZ: "yes", tags: [ "clean" ] }
```
* Single AZ:
```
roles:
    - { role: create_ec2_vpc, mutiAZ: "no", tags: [ "create" ] }
    - { role: clean-ec2-vpc, mutiAZ: "no", tags: [ "clean" ] }
```


### c. Run
##### Create

```
ansible-playbook create_hdp_infrastructure.yml --tags="create"
```

##### Clean

```
ansible-playbook create_hdp_infrastructure.yml --tags="clean"
```

# 2. Install hadoop cluster with HDP platform

This role will use Ambari Blueprint utility to setups the following:

* Install Ambari
* Install and setup Hadoop cluster use HDP
* Setup Namenode HA
* Setup Resource Manager HA
* Hadoop components: Datanode, Nodemanager, Spark, Hive, ...


### a. Prepare to deploy Hadoop cluster use blue print

- Export `ANSIBLE_HOST_KEY_CHECKING`

Run:

```
export ANSIBLE_HOST_KEY_CHECKING=False
```

- Change the cluster name in `deploy_cluster/files/*.json` and `deploy_cluster/templates/hostmap.json.j2` (`If you want`)

### b. Deploy Hadoop cluster by use blueprint
```
$ ansible-playbook --private-key /path/to/your_private_key -i inventories/staging/hosts install_hdp.yaml
```
- Connect to Ambari in your browser with:

`ssh -i /path/to/private/key -L 8080:ambari_server:8080 bastion_host_address`
```
http://127.0.0.1:8080    #(default login is admin:admin)
```
...and watch the cluster build!

### Note

To stop the agents across the cluster and shut down the ambari server:

```
$ ansible-playbook --private-key .ssh/mykey stopagents.yaml
```

Useful curl commands for manual execution/verification (these steps are completed by the 'cluster' playbook):

List your registered hosts to confirm ambari knows about them:
```
$ curl -H "X-Requested-By: ambari" -X GET -u admin:admin http://[ambari_server]:8080/api/v1/hosts
```
Get a list of registered blueprints:
```
$ curl -H "X-Requested-By: ambari" -X GET -u admin:admin http://[ambari_server]:8080/api/v1/blueprints
```
Post a blueprint to the Ambari server:
```
$ curl -H "X-Requested-By: ambari" -X POST -u admin:admin http://[ambari_server]:8080/api/v1/blueprints/testclus -d @testclus.json
```
Get a list of managed clusters:
```
$ curl -H "X-Requested-By: ambari" -X GET -u admin:admin http://[ambari_server]:8080/api/v1/clusters
```
Post a cluster configuration template:
```
$ curl -H "X-Requested-By: ambari" -X POST -u admin:admin http://[ambari_server]:8080/api/v1/clusters -d @hostmap.json

{
  "href" : "[ambari_server]:8080/api/v1/clusters/testclus/requests/1",
  "Requests" : {
    "id" : 1,
    "status" : "Accepted"
}
```
## Reference
* https://github.com/ersiko/terraform-hadoop
* Authentication with AWS http://docs.ansible.com/ansible/latest/guide_aws.html
