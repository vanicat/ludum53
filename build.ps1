rm .\app.dist\assets
git pull 
python.exe -m nuitka .\app.py --standalone
cp -r .\assets\ .\app.dist\