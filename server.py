# !/usr/bin/python
# -*- coding: utf-8 -*-
import os,time

def checkDir (mypath,filename="config.file"):
    onlyfiles = [f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath, f)) and f == filename)]
    #print "Found match with keyword:{0}<->{1}".format(onlyfiles,filename)
    return onlyfiles


mypath = "/Users/Valentin/Desktop/test/"
filename="config.file"

while True:
    onlyfiles = checkDir(mypath,filename)
    for configfile in onlyfiles:
        try:
            print "starting script..."
            print "successfully created map catalog. Deleting config.file now..."
            os.remove(os.path.join(mypath,configfile))
            pass
        except Exception as e:
            raise



    '''
    if checkDir("/Users/Valentin/Desktop/test/"):
        print "starting script..."
        print "successfully created map catalog. Deleting config.file now..."
        os.remove(os.path.join(mypath,filename))
    '''
    time.sleep(10)
    print "waiting for configfile..."
    pass
