@ECHO OFF
CALL "C:\Users\ecm\Python Files\flask-getting-started\Scripts\activate.bat"
START /B python -m flask run
ping 127.0.0.1 -n 3 > nul
explorer "http://127.0.0.1:5000/"