# when u migrate docker volume will happend  permission issue on bitnai image
-- not work
- chown -R 1001:1001
- chown -R 1001:root
- chmod 777  -R 

must mount UID into  docker
