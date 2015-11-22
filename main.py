#!/usr/bin/python
# coding: utf-8

import arcpy,os,time,point2mapLibrary.py

"""Input data"""
x = 4489177
y = 5401462
az = "Az. 12435"
kopf = "KOPF KOPF KOPF KOPF"

mxdPath = "CURRENT" # or keyword: "CURRENT" r"E:\\GIS\\GK25_gesamt.mxd"
dfName = "Layers"
views = ["geo1", "geo2","geo3","hydro1","hydro2","hydro3","frost1"]
scales = ["15000","30000","30000","50000","30000","300000","50000"]
pdfRootPath = "C:/GIS-Data-Mirror-3-11-2015/"
tempSHP = r"temp"


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
    if elm.name == 'Az':
        elm.text = az
    if elm.name == 'Kopf':
        elm.text = kopf
time.sleep(2)
arcpy.RefreshTOC()
arcpy.RefreshActiveView()

"""Select layers and export PDFs"""
for layer in layers:


    for indexView,view in enumerate(views):
        if layer.name == view:
            layer.visible = True
            df.scale = scales[indexView]
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()

            if layer.name == "geo1":
                point2mapLibrary.rasterCatalogName2textElement(footprint_layer=r"geo1/GK25_footprint" ,pointGeometry=tempSHP,text_element="Karte")
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
                #TODO Ideen: Link zur Geologischen Karte mit Legende (replace string *_c.jpg with *.jpg)
            if layer.name == "geo2":
                point2mapLibrary.rasterCatalogName2textElement(footprint_layer=r"geo2/CC200_C100_footprint" ,pointGeometry=tempSHP,text_element="Karte")
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
            if layer.name == "geo3":
                point2mapLibrary.rasterCatalogName2textElement(footprint_layer=r"geo3/Spezialkarten_footprint" ,pointGeometry=tempSHP,text_element="Karte")
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
            if layer.name == "hydro1":

                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'HK500Legend':
                        elm.elementPositionX = 6.8211
                        break

                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte':
                        elm.text = "Grundwassergleichen-Karte"
                        break
                time.sleep(2)
            """ NUR FUER SPEZIALKARTEN (hydro2)"""
            if layer.name == "hydro2":
                #wait 20 sec to draw WMS data
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(20)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte':
                        elm.text = "Karte der wassersensiblen / überschwemmungsgefährdeten Bereiche"
                    if elm.name == 'UeberschwemmungText':
                        elm.elementPositionX = 4.2236

                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Festgesetzte_ueberschwemmungsgebiete':
                        elm.elementPositionX = 2.3524
                    if elm.name == 'WassersensibelLegend':
                        elm.elementPositionX = 11.9518
                time.sleep(2)
            """ NUR FUER SPEZIALKARTEN (hydro3)"""
            if layer.name == "hydro3":
                #wait 20 sec to draw WMS data
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(20)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte':
                        elm.text = "Karte der Trinkwasser- und Heilquellenschutzgebiete"

                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Trinkwasserschutzgebiete':
                        elm.elementPositionX = 13.8323
                    if elm.name == 'Heilquellenschutzgebiete':
                        elm.elementPositionX = 13.8323
                time.sleep(2)
            if layer.name == "frost1":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte':
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
                    if elm.name == 'HK500Legend':
                        elm.elementPositionX = 36.8211
                        break
            if layer.name == "hydro2":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'Karte':
                        elm.text = u"Karte der wassersensiblen / überschwemmungsgefährdeten Bereiche"
                    if elm.name == 'UeberschwemmungText':
                        elm.elementPositionX = 44.2236
                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Festgesetzte_ueberschwemmungsgebiete':
                        elm.elementPositionX = 42.3524
                    if elm.name == 'WassersensibelLegend':
                        elm.elementPositionX = 41.9518
            if layer.name == "hydro3":
                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'Trinkwasserschutzgebiete':
                        elm.elementPositionX = 53.8323
                    if elm.name == 'Heilquellenschutzgebiete':
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
