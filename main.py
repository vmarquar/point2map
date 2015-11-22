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
pdfRootPath = os.path.normpath(pdfRootPath)

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

            """ ERSTELLE LEGENDEN / VERÄNDERE TEXT ELEMENTE """
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
                point2mapLibrary.picture2legend(picture_element="HK500Legend",x=6.8211,y=5.0)
                #TODO staticText2textElement durch eine Version von rasterCatalogName2textElement ersetzen
                #TODO Dazu muss zunächst der Footprint für Ansbach, HK500 und Wassergleichen-Nürnberg erstellt werden
                point2mapLibrary.staticText2textElement(static_text="Grundwassergleichenkarte",text_element="Karte")
            if layer.name == "hydro2":
                #wait 20 sec to draw WMS data
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(20)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                point2mapLibrary.staticText2textElement(static_text="Karte der wassersensiblen und\nüberschwemmungsgefährdeten Bereiche",text_element="Karte")
                point2mapLibrary.picture2legend(picture_element="UeberschwemmungText",x=4.2236,y=5.0)
                point2mapLibrary.picture2legend(picture_element="Festgesetzte_ueberschwemmungsgebiete",x=2.3524,y=5.0)
                point2mapLibrary.picture2legend(picture_element="WassersensibelLegend",x=11.9518,y=5.0)
            if layer.name == "hydro3":
                #wait 20 sec to draw WMS data
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(20)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                point2mapLibrary.staticText2textElement(static_text="Karte der Trinkwasser- und Heilquellenschutzgebiete",text_element="Karte")
                point2mapLibrary.picture2legend(picture_element="Trinkwasserschutzgebiete",x=13.8323,y=5.0)
                #TODO x von Heilquellenschutzgebiete genauer definieren
                point2mapLibrary.picture2legend(picture_element="Heilquellenschutzgebiete",x=11.8323,y=5.0)
            if layer.name == "frost1":
                point2mapLibrary.staticText2textElement(static_text="Frostzonenkarte Bayerns",text_element="Karte")

            #TODO Hier könenn weitere Legenden für weitere PDF Seiten hinzu gefügt werden


            """ DRUCKE KARTEN AUS """
            time.sleep(2)
            if layer.name == "hydro2":
                outPDF = (os.path.join(pdfRootPath,layer.name)+".pdf")
                arcpy.mapping.ExportToPDF(mxd,outPDF.encode("utf-8"),"PAGE_LAYOUT",resolution=85)
                pdfDoc.appendPages(outPDF.encode("utf-8"))
            else:
                outPDF = (os.path.join(pdfRootPath,layer.name)+".pdf")
                arcpy.mapping.ExportToPDF(mxd,outPDF.encode("utf-8"),"PAGE_LAYOUT")
                pdfDoc.appendPages(outPDF.encode("utf-8"))
            try:
                os.remove(outPDF.encode("utf-8"))
            except:
                print "Datei wurde nicht gefunden."
                arcpy.AddMessage("Die angegebene Datei wurde nicht gefunden!")



            """ VERSCHIEBE Legenden wieder in den unsichtbaren Bereich """
            try:
                for elm in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
                    if elm.name == 'HK500Legend':
                        elm.elementPositionX = 36.8211
                    if elm.name == 'Trinkwasserschutzgebiete':
                        elm.elementPositionX = 36.8211
                    if elm.name == 'Heilquellenschutzgebiete':
                        elm.elementPositionX = 36.8211
                    if elm.name == 'Festgesetzte_ueberschwemmungsgebiete':
                        elm.elementPositionX = 36.8211
                    if elm.name == 'WassersensibelLegend':
                        elm.elementPositionX = 36.8211
                    if elm.name == 'UeberschwemmungText':
                        elm.elementPositionX = 36.8211
            except:
                print "Fehler in main-function (main.py). Eines oder mehrere Layout-Elemente konnten nicht verschoben werden."
                arcpy.AddMessage("Fehler in main-function (main.py). Eines oder mehrere Layout-Elemente konnten nicht verschoben werden.")

            layer.visible = False
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()



#Commit changes and delete variable reference
pdfDoc.saveAndClose()

#TODO Delete added point
arcpy.DeleteRows_management(tempSHP)
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
del rowInserter
#del rowUpdater

del pdfDoc
del mxd
