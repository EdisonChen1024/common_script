@echo off
echo compile protocol...
for %%i in (.\proto\*.proto) do protoc-3.3.0\bin\protoc.exe -I=.\proto --python_out=.\proto %%i
echo all done.
pause
