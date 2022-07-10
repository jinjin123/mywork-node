```
helm install mydbs \
--set global.storageClass=rook-ceph-block \
--set mongodbRootPassword=DU2K123m1SxT9F  \
--set shards=2,replicas=2,shardsvr.dataNode.replicas=2 \
--set shardsvr.persistence.size=1Gi  \
--set shardsvr.persistence.storageClass=rook-ceph-block \
--set configsvr.replicas=2 \
--set configsvr.persistence.storageClass=rook-ceph-block \
--set configsvr.persistence.size=1Gi \
 bitnami/mongodb-sharded
 ```
