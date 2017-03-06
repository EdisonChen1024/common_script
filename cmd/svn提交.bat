@echo off
SET ws_dir="E:\MobileGame\server\build\bin\lua_script\ws\config\export\"
rem svn update
TortoiseProc.exe /command:update /path:"%cd%" /closeonend:3
TortoiseProc.exe /command:update /path:%ws_dir% /closeonend:3
rem move config to export
XCOPY /Y .\export %ws_dir%
:: 获取当前目录名
:: 当路径中含有空格、感叹号、点号、&和~的时候，也能正确提取
set "cd_=%cd%"
:loop
set "cd_=%cd_:*\=%"
set "cd_tmp=%cd_:\=%"
if not "%cd_tmp%"=="%cd_%" goto loop
rem svn commit
TortoiseProc.exe /command:commit /path:%ws_dir% /logmsg:"同步最新export配置from【%cd_%】" /closeonend:3
echo **************
echo finish...
echo **************
pause
