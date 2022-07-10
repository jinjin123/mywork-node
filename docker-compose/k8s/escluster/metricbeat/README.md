```
下载官方的模板在本地文件系统
wget https://raw.githubusercontent.com/elastic/beats/7.9/deploy/kubernetes/metricbeat-kubernetes.yaml



修改 ConfigMap 中指定的 Elasticsearch 主机相关的配置，并添加 Kibana的主机



    output.elasticsearch:
      hosts: ['http://elasticsearch:9200']
      username: elastic
      password: xxx
    setup.kibana:
      host: "kibana:5601"


应用 YAML 配置创建对应的 Kubernetes 资源
kubectl apply -f metricbeat-kubernetes.yaml



进入 Pod 修改配置
kubectl exec -it metricbeat-xxx /bin/bash



设置 Metricbeat 创建 Kibana上的 Index Pattern 和 Dashboard
metricbeat setup

```
ignore setup error
