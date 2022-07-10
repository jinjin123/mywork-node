docker run -d --name jenkins -p 7900:8080 -p 50000:50000 -v /mnt/raid0/data/jenkins:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:lts
