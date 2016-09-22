[OPTIONAL]
[[Preconfig if your start from a blank windows python]]

http://docs.python-guide.org/en/latest/starting/install/win/#install-windows

Powershell command:
[Environment]::SetEnvironmentVariable("Path", "$env:Path; C:\Python27\ArcGIS10.3\;C:\Python27\ArcGIS10.3\Scripts\", "User")

http://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows

python get-pip.py

python -m pip install --upgrade pip


[ARCSCRIPT CONFIG]
[[Configuration if you already have pip installed and upgraded correctly]]

pip install -r /path/to/requirements.txt

[CONFIGURE AUTOMATIC STARTUP WHEN USER IS LOGGED IN]

Add this key/value pairs to following registry string:
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

--> new: string (Zeichenfolge):
1a. Name: You can choose whatever you want (e.g. ArcGIS Script Starter)
2a. Path to your starting batch file (C:\GIS\start_server.bat)

1b. Name: point2db Valentin
2b. Path: C:\GIS\start_point2db.bat
