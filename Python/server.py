# !/usr/bin/python
# -*- coding: utf-8 -*-
import os,time

def checkDir (mypath,filename="config.file"):
    onlyfiles = [f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath, f)) and f == filename)]
    #print "Found match with keyword:{0}<->{1}".format(onlyfiles,filename)
    return onlyfiles


mypath = "N:/Start_Script"
filename="config.file"

while True:
    onlyfiles = checkDir(mypath,filename)
    for configfile in onlyfiles:
        try:
            print "starting script..."
            try:
                os.system("C:\GIS\Python_Tools\point2map_v03\Python\main.py")
                print "successfully created map catalog. Deleting config.file now..."
                os.remove(os.path.join(mypath,configfile))
            except:
                raise
        except:
            pass





    print "waiting for configfile..."
    time.sleep(30)
    pass
