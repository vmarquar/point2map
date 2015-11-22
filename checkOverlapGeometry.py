#!/usr/bin/python
# coding: utf-8
def checkGeometry(polygon,point):
    """ polygon has to be either a layer object or a shp file / gdb feature file without a Raster-field.
        point has to be a either a layer object or a shp/gdb feature file. NOTE: Only the last row will be taken into consideration.
        Returns: A str-list of polygons which contain the point.
    """
    #result=[]
    string = r"Kartengrundlage:\n"
    print type(string)
    polygonGeometries= arcpy.CopyFeatures_management(polygon,arcpy.Geometry())
    try:
        pointGeometry= arcpy.CopyFeatures_management(point,arcpy.Geometry())[-1]
    except:
        arcpy.AddMessage("Die Point-Datei ist leer!")
        print("Die Point-Datei ist leer!")
    polygonNames = [row[0] for row in arcpy.da.SearchCursor(polygon, ("Name"))]

    for index,polygonGeometry in enumerate(polygonGeometries):
        if polygonGeometry.contains(pointGeometry):
            print "Die Geometrie enthaelt:"+polygonNames[index]
            print type(polygonNames[index])
            #result.append(polygonNames[index])
            string += polygonNames[index] +"\n"
            print type(string)
    return string
