Remove-Item .\build\assets

git pull 
.\ludum\Scripts\python.exe -m nuitka --follow-imports .\app.py

mkdir .\build\assets
mkdir .\build\assets\music

Copy-Item "assets\boat.tmj" .\build\assets
Copy-Item "assets\boat.png" .\build\assets
Copy-Item "assets\boat-port.png" .\build\assets
Copy-Item "assets\carte1.tmj" .\build\assets
Copy-Item "assets\fond.png" .\build\assets
Copy-Item "assets\materiel.json" .\build\assets
Copy-Item "assets\roue2.png" .\build\assets
Copy-Item "assets\roue2-direction.png" .\build\assets
Copy-Item "assets\terrain.tsx" .\build\assets
Copy-Item "assets\tile1.png" .\build\assets
Copy-Item .\assets\music\music-wave.mp3 .\build\assets\music

#Copy-Item -r .\assets .\build
Copy-Item app.exe .\build