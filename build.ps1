rm .\app.dist\assets
git pull 
python.exe -m nuitka --mingw64 .\app.py
cp -r .\assets\ .\app.dist\