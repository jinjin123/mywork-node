```
-producer
kubectl exec -it kafka-0 -- kafka-console-producer.sh --broker-list kafka-0.kafka-headless.default.svc.cluster.local:9092 --topic test

-consumer
 kubectl exec -it kafka-0 -- kafka-console-consumer.sh --bootstrap-server kafka.default.svc.cluster.local:9092 --topic test --from-beginning


 helm install kafka bitnami/kafka \
  --set replicaCount=3 \
  --set persistence.enabled=true \
  --set global.storageClass=nfs-ok \
  --set persistence.size=8Gi \
  --set service.type=NodePort
```
