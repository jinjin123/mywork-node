```
after apply 
kubectl -n mongo-db exec -it mongodb0-68fb678849-tb558 -- bash
$ mongo
> db.getSiblingDB("admin").auth("admin", "password")
1
>rs.initiate({ _id: "mongoRS", version: 1,
  members: [
  { _id: 0, host: "mongo-db-0.com:27017" },
  { _id: 1, host: "mongo-db-1.com:27017" },
  { _id: 2, host: "mongo-db-2.com:27017" } ]});
mongoRS:PRIMARY>
Now, you can connect to the Replica set using the database's connection string.

mongosh
"mongodb://admin:password@10.0.0.1:27017,10.0.0.2:27017,10.0.0.3:27017/admin?authSource=admin&replicaSet=mongoRS"

```
Even though using separate deployments for each node of the MongoDB Replica set is a time-consuming task, you can have complete control over the Replica set. Also, in the case of PV expansion, you can increase the PV size of each Secondary Node individually. All this with zero time while performing any operation on MongoDB.

You can efficiently run a highly available MongoDB cluster on Kubernetes using any of the above methods. While each technique has its pros, it is up to the business use case on which cluster type is required. To sum it all up, you can quickly create and deploy the cluster using the Kubernetes Operator to deploy MongoDB. But you will lose many of the customization features. On the other hand, using custom Docker images and individual deployments is more complex than using the Operator. But you will get complete control over the database configurations and customization options for the configurations as per the use case. The choice is yours!
