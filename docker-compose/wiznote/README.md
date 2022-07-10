``` 
-http
 docker run --name wiz --restart=always -it -d -v  /mnt/raid1/wizdata/Okint:/wiz/storage -v  /etc/localtime:/etc/localtime -p 18000:80 -p 18001:9269/udp  wiznote/wizserver

```
- cannot add user ,so one user one container
