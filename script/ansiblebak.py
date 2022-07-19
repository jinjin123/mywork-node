`#!/usr/bin/python
#-*- coding:utf-8 -*-
import ansible.runner
import ansible.inventory
import logging
import json
import sys

class rootUser():
    def __init__(self, ipAddress, userName, remoteUser):
        self.ipAddress = [ ipAddress ]
        self.userName = userName
        self.remoteUser = remoteUser

        '''init base info'''
        self.webInventory = ansible.inventory.Inventory(self.ipAddress)
        self.remotePort = 22
        self.timeOut = 10
        self.priKeyFile = '/root/.ssh/id_rsa'

    def printLog(self, output):
        for (hostname, result) in output['contacted'].items():
            if 'failed' in result:
                logging.error('there is a error[%s]' % result['msg'])
                sys.exit(1)
            elif 'stderr' in result:
                if result['stderr']:
                        logging.error('there is a error [%s]' % result['stderr'])
                        sys.exit(1)

    def checkUserExist(self):
        checkrunner = ansible.runner.Runner(
            module_name='shell',
            module_args='id -u %s' % self.userName,
            timeout=self.timeOut,
            remote_port=self.remotePort,
remote_user=self.remoteUser,
#           private_key_file=self.priKeyFile,
            become=True,
            become_user='root',
            inventory = self.webInventory
        )
        self.output = checkrunner.run()
        self.printLog(self.output)

    def addRoot(self):
        self.checkUserExist()
        runner = ansible.runner.Runner(
            module_name='user',
            module_args='name=%s groups=root append=no' % self.userName,
            timeout=self.timeOut,
            remote_port=self.remotePort,
            remote_user=self.remoteUser,
            private_key_file=self.priKeyFile,
            become=True,
            become_user='root',
            inventory = self.webInventory
        )

        self.result = runner.run()
        self.printLog(self.result)
        print ('success')

    def removeRoot(self):
        rmRunner = ansible.runner.Runner(
            module_name='shell',
            module_args='gpasswd -d %s root' % self.userName,
            timeout=self.timeOut,
            remote_port=self.remotePort,
            remote_user=self.remoteUser,
            private_key_file=self.priKeyFile,
            become=True,
            become_user='root',
            inventory = self.webInventory
        )
        self.rmOutput = rmRunner.run()
        self.printLog(self.rmOutput)
        print ('success remove root privilege')


theUser = rootUser('192.168.1.8', 'jin', 'root')
theUser.removeRoot()

"""
输入三个参数，需要操作的ip, 哪个用户需要root权限，执行操作的用户，再执行对应的addRoot函数和removeRoot函数,主要用来自助添加root的权限
"""
