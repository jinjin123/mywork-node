#  override conf is different with noconf

- run override conf compose 
- flushall;cluster reset
- choose redis excute ` redis-cli -a bitnami --cluster create redis-node-0:6379 redis-node-1:6379 redis-node-2:6379 redis-node-3:6379 redis-node-4:6379 redis-node-5:6379    --cluster-replicas 1`
- check `redis-cli -a bitnami cluster nodes`
- must has specify  config  otherwise redis sometime will dead

