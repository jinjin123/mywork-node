@ECHO OFF
puppet agent --no-daemonize
:LOOP
netstat -an | find /i ":8139" /c > __null
set /p result=<__null
del __null
echo Result is %result%
if %result%==1 (
  ECHO "puppet agent 掉线"
  ping -n 5 127.0.0.1 >null
  GOTO CONTINUE
) ELSE(
  ECHO "puppet agent 正在运行"
  ping -n 5 127.0.0.1 >null
  GOTO LOOP
)

:CONTINUE
ECHO "正在重启puppet agent程序"
puppet agent --no-daemonize
GOTO LOOP