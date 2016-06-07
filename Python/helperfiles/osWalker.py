# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,arcpy
print sys.stdout.encoding
print sys.getdefaultencoding()

encoding = 'utf-8'
path = "C:/Users/Valentin/".decode(encoding='UTF-8')
outpath = "C:/Users/Valentin/Desktop/footprints".decode(encoding='UTF-8')
path = os.path.normpath(path)
outpath = os.path.normpath(outpath)
arcpy.env.workspace = outpath

print path.encode('cp850','')
f = open('test.txt','w')
logs = open('logs.txt','w')

if arcpy.CheckExtension("3D") == "Available":
    arcpy.CheckOutExtension("3D")

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        if name[-6:] == "_c.jpg":
            getID = os.path.normpath(os.path.join(root,name))
            try:
                year = getID.split('\\')[-2][-4:]
            except:
                continue
            try:
                ID = getID.split('\\')[-3]
            except:
                continue
            print getID.encode("utf-8")
            try:
                f.write(os.path.join(root,name).encode("utf-8")+'\t'+year.encode("utf-8")+'\t'+ID.encode("utf-8")+'\n')
                #ArcGIS App here
                print "Calculating raster domain for {0}.shp".format(ID.encode("utf-8"))
                #arcpy.RasterDomain_3d(in_raster=os.path.join(root,name), out_feature_class=ID.encode("utf-8")+".shp", out_geometry_type="LINE")
                arcpy.RasterDomain_3d(in_raster=os.path.join(root,name), out_feature_class=os.path.join(outpath,(ID+".shp")), out_geometry_type="POLYGON")
            except Exception as e:
                print e.message
                print ('Could not execute:\t'+os.path.join(root,name).encode("utf-8")+'\t'+year.encode("utf-8")+'\t'+ID.encode("utf-8")+'\n')
                logs.write('Could not execute:\t'+os.path.join(root,name).encode("utf-8")+'\t'+year.encode("utf-8")+'\t'+ID.encode("utf-8")+'\n')
                continue

            print "Dies ist ein Bild:{0}".format(os.path.join(root,name).encode("utf-8"))
        #print(os.path.join(root, name))
    #for name in dirs:
        #print(os.path.join(root, name))
f.close()
logs.close()
