@echo off
title svn update
@echo ----------------------------------------
@echo 1    ���²߻�
@echo 2    ����client
@echo 3    ����server
@echo 0    �˳�
@echo ----------------------------------------
set menu=4 
set /P menu=��ѡ����Ҫ�Ĺ���[Ĭ�ϸ���ȫ��]:
if %menu%==1 (
    call :update_cehua
)
if %menu%==2 (
    call :update_client
) 
if %menu%==3 (
    call :update_server
) 
if %menu%==4 (
    call :update_cehua
    call :update_client
    call :update_server
)
if %menu%==0 (
    exit
)

pause
exit
:update_cehua
    echo ���²߻�......
    TortoiseProc.exe /command:update /path:"E:\MobileGame\�߻�" /closeonend:3
goto :EOF

:update_client
    echo ����client......
    TortoiseProc.exe /command:update /path:"E:\MobileGame\client" /closeonend:3
goto :EOF

:update_server
    echo ����server......
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\config" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\def" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\engine" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\script_interface" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\third_party" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\yh_am" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\yh_dbserver" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\yh_platform" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\yh_wserver" /closeonend:3
    TortoiseProc.exe /command:update /path:"E:\MobileGame\server\yh_fepserver" /closeonend:3
goto :EOF
