#!/usr/bin/python
# coding: utf-8
import arcpy,os,time

"""Input data"""
x = 4489177
y = 5401462
az = "Az. 12435"
kopf = "KOPF KOPF KOPF KOPF"

mxdPath = "CURRENT" # or keyword: "CURRENT" r"E:\\GIS\\GK25_gesamt.mxd"
dfName = "Layers"
views = ["geo1", "geo2","geo3","hydro1","hydro2","hydro3","frost1"]
scales = ["15000","30000","30000","50000","30000","300000","50000"]
pdfRootPath = r"C:\\GIS-Data-Mirror-3-11-2015\\"
tempSHP = r"temp"

""" Function Definitions """

def checkGeometry(polygon,point):
    """ polygon has to be either a layer object or a shp file / gdb feature file without a Raster-field.
        point has to be a either a layer object or a shp/gdb feature file. NOTE: Only the last row will be taken into consideration.
        Returns: A str-list of polygons which contain the point.
    """
    result=[]
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
            result.append(polygonNames[index])
            string += polygonNames[index] +"\n"
            print type(string)
    return result,string

"""Load Document"""
mxd = arcpy.mapping.MapDocument(mxdPath)
df = arcpy.mapping.ListDataFrames(mxd, dfName)[0]
layers = arcpy.mapping.ListLayers(mxd, "*", df)
newExtent = df.extent

"""Zoom to point"""
newExtent.XMin, newExtent.YMin = float(x), float(y)
newExtent.XMax, newExtent.YMax = float(x), float(y)
df.extent = newExtent
""" Create PDF MapBook Document """
#Set file name and remove if it already exists
pdfPath = pdfRootPath+"GeologyMapBook.pdf"
if os.path.exists(pdfPath):
    os.remove(pdfPath)
pdfDoc = arcpy.mapping.PDFDocumentCreate(pdfPath)

""" Create temporary AOI point and delete it afterwards"""

#create insert cursor
rowInserter = arcpy.InsertCursor(tempSHP)
#create update cursor
#rowUpdater = arcpy.UpdateCursor(tempSHP)
#assign coordinates to point object
pointGeometry = arcpy.Point(x,y)
newPoint = rowInserter.newRow()
newPoint.Shape = pointGeometry
rowInserter.insertRow(newPoint)

""" Update Header and az """
for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if elm.name == 'Az': # whatever your text element is named here
        elm.text = az
    if elm.name == 'Kopf': # whatever your text element is named here
        elm.text = kopf
time.sleep(2)
arcpy.RefreshTOC()
arcpy.RefreshActiveView()

"""Select layers and export PDFs"""
for layer in layers:

    i = 0
    for view in views:
        if layer.name == view:
            layer.visible = True
            df.scale = scales[i]
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
            #quick n dirty: wait 30 sec to draw all wms data
            #TODO Bei gelegenheit schoener schreiben
            if layer.name == "hydro2":
                time.sleep(30)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
            if layer.name == "hydro3":
                time.sleep(20)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()

            if layer.name == "geo1":
                geo1name = checkGeometry(r"geo1\GK25_footprint",tempSHP)

                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = geo1name
                        break
                time.sleep(2)
            """ NUR FUER SPEZIALKARTEN (geo2)"""
            if layer.name == "geo2":
                geo2name = checkGeometry(r"geo2\CC200_footprint",tempSHP)
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = geo2name #"Spezialkarte: genaue Namensimplementierung steht noch aus"
                        break
                time.sleep(2)

            """ NUR FUER SPEZIALKARTEN (geo3)"""
            if layer.name == "geo3":
                geo3name = checkGeometry(r"geo3\Spezialkarte_footprint",tempSHP)
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = geo3name #"Spezialkarte: genaue Namensimplementierung steht noch aus"
                        break
                time.sleep(2)
            """ NUR FUER SPEZIALKARTEN (hydro1)"""
            if layer.name == "hydro1":

                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'HK500Legend': # whatever your text element is named here
                        elm.elementPositionX = 6.8211
                        break

                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = "Grundwassergleichen-Karte"
                        break
                time.sleep(2)
            """ NUR FUER SPEZIALKARTEN (hydro2)"""
            if layer.name == "hydro2":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = "Karte der wassersensiblen / überschwemmungsgefährdeten Bereiche"
                    if elm.name == 'UeberschwemmungText': # whatever your text element is named here
                        elm.elementPositionX = 4.2236

                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Festgesetzte_ueberschwemmungsgebiete': # whatever your text element is named here
                        elm.elementPositionX = 2.3524
                    if elm.name == 'WassersensibelLegend': # whatever your text element is named here
                        elm.elementPositionX = 11.9518
                time.sleep(2)
            """ NUR FUER SPEZIALKARTEN (hydro3)"""
            if layer.name == "hydro3":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = "Karte der Trinkwasser- und Heilquellenschutzgebiete"

                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Trinkwasserschutzgebiete': # whatever your text element is named here
                        elm.elementPositionX = 13.8323
                    if elm.name == 'Heilquellenschutzgebiete': # whatever your text element is named here
                        elm.elementPositionX = 13.8323
                time.sleep(2)
            if layer.name == "frost1":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = "Frostzonenkarte von Bayern"
                time.sleep(2)
            if layer.name == "hydro2":
                arcpy.mapping.ExportToPDF(mxd,pdfRootPath+layer.name+".pdf","PAGE_LAYOUT",resolution=85)
                pdfDoc.appendPages(pdfRootPath+layer.name+".pdf")
            else:
                arcpy.mapping.ExportToPDF(mxd,pdfRootPath+layer.name+".pdf","PAGE_LAYOUT")
                pdfDoc.appendPages(pdfRootPath+layer.name+".pdf")
            try:
                os.remove(pdfRootPath+layer.name+".pdf")
            except:
                #TODO mit arcpy message austauschen!
                print "Datei wurde nicht gefunden."
                arcpy.AddMessage("Die angegebene Datei wurde nicht gefunden!")

            """ VERSCHIEBE Legenden wieder in den unsichtbaren Bereich """
            if layer.name == "hydro1":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'HK500Legend': # whatever your text element is named here
                        elm.elementPositionX = 36.8211
                        break
            if layer.name == "hydro2":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte': # whatever your text element is named here
                        elm.text = u"Karte der wassersensiblen / überschwemmungsgefährdeten Bereiche"
                    if elm.name == 'UeberschwemmungText': # whatever your text element is named here
                        elm.elementPositionX = 44.2236
                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Festgesetzte_ueberschwemmungsgebiete': # whatever your text element is named here
                        elm.elementPositionX = 42.3524
                    if elm.name == 'WassersensibelLegend': # whatever your text element is named here
                        elm.elementPositionX = 41.9518
            if layer.name == "hydro3":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Trinkwasserschutzgebiete': # whatever your text element is named here
                        elm.elementPositionX = 53.8323
                    if elm.name == 'Heilquellenschutzgebiete': # whatever your text element is named here
                        elm.elementPositionX = 53.8323

            layer.visible = False
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
        i+=1


#Commit changes and delete variable reference
pdfDoc.saveAndClose()

#TODO Delete added point
arcpy.DeleteRows_management(r"C:\\GIS-Data-Mirror-3-11-2015\\GIS\\GK25.gdb\\temp")
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
del rowInserter
#del rowUpdater

del pdfDoc
del mxd
