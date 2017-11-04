@echo off
:: echo. newline xopy /r 递归复制 copy复制文件 xcopy复制文件夹
echo "开始安装,请勿关闭窗口，安装完成会自动关闭窗口。"
start /wait /i C:\Users\Administrator\Desktop\600\mysql-5.6.22-win32.msi /quiet
start /wait C:\Users\Administrator\Desktop\600\nginx-1.10.2-win32-setup.exe /Install /VERYSilent
start /wait C:\Users\Administrator\Desktop\600\Git-2.7.2-32.exe /Install /VERYSilent
set gitpath=C:\Program Files\Git\bin
set mqpath=C:\Program Files\RabbitMQ Server\rabbitmq_server-3.6.5\sbin
set mysqlpath=C:\Program Files\MySQL\MySQL Server 5.6\bin
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v "Path" /t reg_sz /d "%Path%;%gitpath%;%mqpath%;%mysqlpath%" /f
set puppetpath="C:\ProgramData\PuppetLabs\puppet\etc\puppet\bin"
start /wait /i C:\Users\Administrator\Desktop\600\puppet-3.8.7.msi /quiet
echo.
net stop "Puppet Agent"
set name=agent3
set fqdn=kisspuppet.com
reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\ComputerName\ActiveComputerName" /v ComputerName /t reg_sz /d %name% /f >nul 2>nul
reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Tcpip\Parameters" /v "NV Hostname" /t reg_sz /d %name% /f >nul 2>nul
reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Tcpip\Parameters" /v Hostname /t reg_sz /d %name% /f >nul 2>nul
reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Tcpip\Parameters" /v "NV Domain" /t reg_sz /d %fqdn% /f >nul 2>nul
@echo 192.168.2.173 puppetmaster.kisspuppet.com puppetmaster >> C:\Windows\System32\drivers\etc\hosts
echo.
rd /s /q "C:\ProgramData\PuppetLabs\puppet\etc"
xcopy /e /s /q /i /r  C:\Users\Administrator\Desktop\600\etc C:\ProgramData\PuppetLabs\puppet\etc 
echo.
xcopy /e /s /q /i /r  C:\Users\Administrator\Desktop\600\600 C:\600
rd /s /q "C:\Program Files\MySQL\MySQL Server 5.6\data"
echo.
xcopy /e /s /q /i /r  C:\Users\Administrator\Desktop\600\data "C:\Program Files\MySQL\MySQL Server 5.6\data"
start /wait C:\Users\Administrator\Desktop\600\otp_win32_19.1.exe /S
start /wait C:\Users\Administrator\Desktop\600\rabbitmq-server-3.6.5.exe /S
start /wait C:\Users\Administrator\Desktop\600\jre-8u112-windows-i586.exe /s
copy  "C:\Users\Administrator\Desktop\600\rabbitmq.config" "C:\Users\Administrator\AppData\Roaming\RabbitMQ"
echo.
copy  "C:\Users\Administrator\Desktop\600\mqplugins.vbs" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
echo.
copy  "C:\Users\Administrator\Desktop\600\start-nginx.vbs" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
echo.
copy  "C:\Users\Administrator\Desktop\600\mysql.vbs" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
echo.
copy  "C:\Users\Administrator\Desktop\600\agent-no-gui.vbs" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
copy  "C:\Users\Administrator\Desktop\600\start-kc.vbs" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
echo.
copy  "C:\Users\Administrator\Desktop\600\nginx.conf" "C:\nginx\conf"
echo.
xcopy /s /e /q /i /r "C:\Users\Administrator\Desktop\600\.ssh" "C:\Users\Administrator\.ssh"
echo.
echo "安装完成"
shutdown -r -t 0
@exit
