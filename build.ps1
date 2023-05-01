Remove-Item .\app.dist\assets
git pull 
python.exe -m nuitka --mingw64 .\app.py
Copy-Item -r .\assets\ .\app.dist\