[OPTIONAL]
[Preconfig if your start from a blank windows python]

http://docs.python-guide.org/en/latest/starting/install/win/#install-windows

Powershell command:
[Environment]::SetEnvironmentVariable("Path", "$env:Path; C:\Python27\ArcGIS10.3\;C:\Python27\ArcGIS10.3\Scripts\", "User")

http://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows

python get-pip.py

python -m pip install --upgrade pip


[ARCSCRIPT CONFIG]
[Configuration if you already have pip installed and upgraded correctly]

pip install -r /path/to/requirements.txt
