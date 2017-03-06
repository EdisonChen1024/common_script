@echo off

call :cecho "Hello World"
call :cecho "A"
call :cecho "B"
call :cecho "C"
echo Done

goto :EOF
:cecho
>%1 set /p=<nul 
findstr /a:0C . %1*
echo.
del %1

rem @echo off
rem call :x c 第一行输出红色
rem call :x a 第二行输出绿色
rem call :x f 第三行输出白色
rem pause
rem goto :EOF
rem :x
rem echo. >%2&findstr /a:%1 . %2*&del %2

rem >"批处理之家"set /p=<nul 
rem findstr /a:21 .* "批处理之家*" 