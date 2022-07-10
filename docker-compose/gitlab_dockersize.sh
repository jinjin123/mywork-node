#!/bin/sh
sudo docker run -d  -p 9999:80 -p 10080:22  --name gitlab   --restart always  -v /mnt/raid0/data/gitlab/config:/etc/gitlab  -v /mnt/raid0/data/gitlab/logs:/var/log/gitlab -v /mnt/raid0/data/gitlab/data:/var/opt/gitlab  gitlab/gitlab-ce:latest


#gitlab-rails console -e production   // 耐心等待

#user=User.where(id:1).first // 第一个用户名，自动切换第一个用户

#user.password='CQgitlab@123'// 修改密码  密码必须是八位

#user.password_confirmation='CQgitlab@123'  // 确认密码

#user.save!  // 保存修改

#exit   // 最后依次输入退出容器
