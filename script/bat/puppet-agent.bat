@ECHO OFF
puppet agent --no-daemonize
:LOOP
netstat -an | find /i ":8139" /c > __null
set /p result=<__null
del __null
echo Result is %result%
if %result%==1 (
  ECHO "puppet agent ����"
  ping -n 5 127.0.0.1 >null
  GOTO CONTINUE
) ELSE(
  ECHO "puppet agent ��������"
  ping -n 5 127.0.0.1 >null
  GOTO LOOP
)

:CONTINUE
ECHO "��������puppet agent����"
puppet agent --no-daemonize
GOTO LOOP