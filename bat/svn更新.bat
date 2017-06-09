@echo off
title svn update
@echo ----------------------------------------
@echo 1    更新策划
@echo 2    更新client
@echo 3    更新server
@echo 0    退出
@echo ----------------------------------------
set menu=4 
set /P menu=请选择需要的功能[默认更新全部]:
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
    echo 更新策划......
    TortoiseProc.exe /command:update /path:"E:\MobileGame\策划" /closeonend:3
goto :EOF

:update_client
    echo 更新client......
    TortoiseProc.exe /command:update /path:"E:\MobileGame\client" /closeonend:3
goto :EOF

:update_server
    echo 更新server......
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
