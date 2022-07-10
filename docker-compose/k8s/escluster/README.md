# Note
- prepare  install ingress controller first
- nfs provisioner  install
- change ingressClass name relate controller
```
-gerenate pwd
#kubectl -n elastic exec -it elasticsearch-0 -- bin/elasticsearch-setup-passwords auto -b
Changed password for user apm_system
PASSWORD apm_system = 7IujAS2g2rHLgmNddwqH

Changed password for user kibana_system
PASSWORD kibana_system = qUjxDUNuNGkbqBVyZfs8

Changed password for user kibana
PASSWORD kibana = qUjxDUNuNGkbqBVyZfs8

Changed password for user logstash_system
PASSWORD logstash_system = wToZIb0nafESAlxQJysa

Changed password for user beats_system
PASSWORD beats_system = YUqz4YUojyNxodJFcYb6

Changed password for user remote_monitoring_user
PASSWORD remote_monitoring_user = WQKNWUx2RD0so5WowLL8

Changed password for user elastic
PASSWORD elastic = F31k1cwR8Td1ulNUqnXW

```
