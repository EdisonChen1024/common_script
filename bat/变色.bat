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
rem call :x c ��һ�������ɫ
rem call :x a �ڶ��������ɫ
rem call :x f �����������ɫ
rem pause
rem goto :EOF
rem :x
rem echo. >%2&findstr /a:%1 . %2*&del %2

rem >"������֮��"set /p=<nul 
rem findstr /a:21 .* "������֮��*" 