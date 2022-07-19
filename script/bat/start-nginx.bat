@ECHO OFF
c:\nginx\nginx.exe
REM c:\php\php-cgi.exe -b 127.0.0.1:9000 -c c:\php\php.ini
ping 127.0.0.1 -n 1>NUL
echo Starting nginx
echo .
echo .
echo .
ping 127.0.0.1 >NUL
EXIT