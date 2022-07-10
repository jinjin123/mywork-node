for port in `seq 7001 7006`; do \
  mkdir -p ./redis-cluster/${port}/conf \
  && PORT=${port} envsubst < ./redis-cluster.tmpl > ./redis-cluster/${port}/conf/redis.conf \
  && mkdir -p ./redis-cluster/${port}/data; \
done
https://www.cnblogs.com/idea360/p/12391416.html
docker exec -it redis7001 redis-cli -p 7001 -a 123456 --cluster create 192.168.1.107:7001 192.168.1.107:7002 192.168.1.107:7003 192.168.1.107:7004 192.168.1.107:7005 192.168.1.107:7006 --cluster-replicas 1
