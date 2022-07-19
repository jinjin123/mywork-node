@echo off
SETLOCAL
SET CWRSYNCHOME=%PROGRAMFILES%\rsync\
SET HOME=%HOMEDRIVE%%HOMEPATH%
C:\Users\xushaolong\test2\rsync\rsync -avz -e "C:\Users\xushaolong\test2\rsync\ssh.exe -i C:\Users\xushaolong\test2\rsync\id_rsa " -P  /C:\Users\xushaolong\test2\c8d4c45e-9441-46ec-b238-cbad126d52b6-fire.zip   root@47.95.233.176:/root/c8d4c45e-9441-46ec-b238-cbad126d52b6-fire.zip
