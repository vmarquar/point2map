#!/usr/bin/python
# coding: utf-8

"""
point2map_v03 ist fuer die console und Rechner PC-31 bestimmt!

TODO: Hinzufügen von neuen Layern (PDF Seiten)
1. Layername in views liste aufnehmen
2. Zoommaßstab für neuen "View" in views-Liste aufnehmen
3. Neuen Legendeneintrag ab Zeile 255 einfügen
4. neuen Legendeneintrag wieder in den "unsichtbaren" Bereich verschieben (ab Zeile 250)


"""

import arcpy,os,time,point2mapLibrary,codecs
from ConfigParser import SafeConfigParser

""" PATHS """
mxdPath = "C:/GIS/Python_Tools/point2map_v03/mxd/point2mapv03.mxd" # or keyword: "CURRENT" r"E:\\GIS\\GK25_gesamt.mxd"
scriptPath = "C:/GIS/Python_Tools/point2map_v03/Python"
tempSHP = "C:/GIS/Geodatabases/Sonstige_Daten.gdb/temp"
pdfRootPath = "N:/Start_Script/"
geo1footprintPath = "C:/GIS/Geodatabases/footprints.gdb/GK25_footprint"
geo2footprintPath = "C:/GIS/Geodatabases/footprints.gdb/Spezialkarten_footprint"
geo3footprintPath = "C:/GIS/Geodatabases/footprints.gdb/C100_CC200_GK500_footprint"
sk1footprintPath = "C:/GIS/Geodatabases/footprints.gdb/SK25_footprint"
projectPointPath = "N:/Unterlagen/Geologische Karten/Projekte_SCRIPT/Projekte_SCRIPT.shp"

"""Input (default) data"""
x = 4420171
y = 5456084
az = u"Az. 15000"
kopf = u"Kartengrundlagen"

dfName = "Layers"
views = ["geo1", "geo2","geo3","sk1","hydro1","hydro2","hydro3","frost1","topo1"]
#views = []
scales = ["15000","30000","30000","35000","100000","30000","30000","100000","30000"]

if pdfRootPath[-1] != "/":
    pdfRootPath += "/"

pdfRootPath = os.path.normpath(pdfRootPath)


"""Load Document"""
mxd = arcpy.mapping.MapDocument(mxdPath)
df = arcpy.mapping.ListDataFrames(mxd, dfName)[0]
layers = arcpy.mapping.ListLayers(mxd, "*", df)
newExtent = df.extent




""" Data input via config.file """
print "Starte point2map-Skript\t{0}\t{1}".format(time.strftime("%H:%M:%S"),(time.strftime("%d/%m/%Y")))
parser = SafeConfigParser()
with codecs.open('N:/Start_Script/config.txt', 'r', encoding='utf-8-sig') as f:
    """    first = f.read(1)
    if first != '\ufeff':
        # not a BOM, rewind
        f.seek(0)
    """
    parser.readfp(f)

print "Read in following arguments:\n"
print parser.get('mandatory_fields','x')
print parser.get('mandatory_fields','y')
print parser.get('mandatory_fields','az')
print parser.get('mandatory_fields','kopf')
print parser.get('mandatory_fields','pdfRootPath')
print parser.get('mandatory_fields','Untersuchungsgebiet')
print parser.get('optional','addPoint')
print parser.get('optional','Category')

x =  float(parser.get('mandatory_fields','x'))
y =  float(parser.get('mandatory_fields','y'))
az =  parser.get('mandatory_fields','az')
try:
    az = unicode(az)
except:
    print "Fehler beim einlesen von az"
kopf = parser.get('mandatory_fields','kopf')
try:
    kopf = u''+kopf
except:
    print "Fehler beim einlesen von Untersuchungsgebiet"
Untersuchungsgebiet = parser.get('mandatory_fields','Untersuchungsgebiet')
try:
    Untersuchungsgebiet = u''+Untersuchungsgebiet
except:
    print "Fehler beim einlesen von Untersuchungsgebiet"
pdfRootPath =  parser.get('mandatory_fields','pdfRootPath')
if pdfRootPath[-1] != "/":
    pdfRootPath += "/"
pdfRootPath = os.path.normpath(pdfRootPath)

""" Extract Data for Project point """
try:
    addPoint = parser.get('optional','addPoint')
    try:
        addPoint = u''+addPoint
    except:
        print "Could not resolve addPoint."
    category = parser.get('optional','Category')
    try:
        category = u''+category
    except:
        print "Could not resolve category."
except:
    print "No optional arguments found. Proceeding with pdf creation. A Project point will not be added!"



"""Zoom to point"""
newExtent.XMin, newExtent.YMin = float(x), float(y)
newExtent.XMax, newExtent.YMax = float(x), float(y)
df.extent = newExtent



""" Create PDF MapBook Document """
pdfName = "Kartengrundlagen_"+str(x)+"-"+str(y)+".pdf"
#Set file name and remove if it already exists
pdfPath = os.path.join(pdfRootPath,pdfName)
if os.path.exists(pdfPath):
    os.remove(pdfPath)
pdfDoc = arcpy.mapping.PDFDocumentCreate(pdfPath)



""" Create temporary AOI point and delete it afterwards"""
rowInserter = arcpy.InsertCursor(tempSHP)
pointGeometry = arcpy.Point(x,y)
newPoint = rowInserter.newRow()
newPoint.Shape = pointGeometry
rowInserter.insertRow(newPoint)




""" Update Header and az """
for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if elm.name == 'Az':
        elm.text = az.encode("mbcs")
    if elm.name == 'Kopf':
        elm.text = kopf.encode("mbcs")
        elm.elementPositionX = 11.0
        elm.elementPositionY = 27.5
    """
    if elm.name == 'Untersuchungsgebiet':
        elm.text = Untersuchungsgebiet.encode("mbcs")
    """
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
                #add GK25 Name:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo1footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="GK_25_Name",x=11,y=23.75)
                #add GK25 fullpath:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo1footprintPath ,pointGeometry=tempSHP,text_element="vollpfad",tableField="fullpath",x=2.35,y=1.75)
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
                #TODO Ideen: Link zur Geologischen Karte mit Legende (replace string *_c.jpg with *.jpg)
            if layer.name == "geo2":
                #add GK25 Name:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo2footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Name",x=11,y=23.75)
                #add GK25 fullpath:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo2footprintPath ,pointGeometry=tempSHP,text_element="vollpfad",tableField="fullpath",x=2.35,y=1.75)
                static_link = u"http://geoportal.bayern.de/bayernatlas-klassik?lon="+str(x)+"&lat="+str(y)+"&zoom=10&addwms=http://www.bis.bayern.de/wms/lfu/gk25_wms?"
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=static_link,text_element="vollpfad",x=2.35,y=1.75)
            if layer.name == "geo3":
                #add GK25 Name:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo3footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Name",x=11,y=23.75)
                #add GK25 fullpath:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo3footprintPath ,pointGeometry=tempSHP,text_element="vollpfad",tableField="fullpath",x=2.35,y=1.75)
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
            if layer.name == "hydro1":
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="HK500Legend",x=13.84,y=2.9)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="HKLegende",x=8,y=4)

                #TODO staticText2textElement durch eine Version von rasterCatalogName2textElement ersetzen
                #TODO Dazu muss zunächst der Footprint für Ansbach, HK500 und Wassergleichen-Nürnberg erstellt werden
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"file:///C:/PfadzuHK500",text_element="vollpfad",x=2.35,y=1.75)
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Grundwassergleichenkarte",text_element="Karte",x=11,y=23.75)
            if layer.name == "hydro2":
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(5)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Karte der wassersensiblen und überschwemmungsgefährdeten Bereiche",text_element="Karte",x=11,y=23.75)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="UeberschwemmungText",x=11.35,y=3.8)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Festgesetzte_ueberschwemmungsgebiete",x=9.68,y=3.35)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="WassersensibelLegend",x=9.65,y=2.9)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Trinkwasserschutzgebiete",x=2.29,y=2.84)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Heilquellenschutzgebiete",x=2.29,y=2.125)
                static_link = u"http://geoportal.bayern.de/bayernatlas-klassik?lon="+str(x)+"&lat="+str(y)+"&zoom=12&addwms=http://www.lfu.bayern.de/gdi/wms/hwrk/wassersensible_bereiche?"
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=static_link,text_element="vollpfad",x=2.35,y=1.75)

            if layer.name == "hydro3":
                #wait 20 sec to draw WMS data
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(5)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="UeberschwemmungText",x=11.35,y=3.8)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Festgesetzte_ueberschwemmungsgebiete",x=9.68,y=3.35)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="WassersensibelLegend",x=9.65,y=2.9)
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Karte der Trinkwasser- und Heilquellenschutzgebiete",text_element="Karte",x=11,y=23.75)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Trinkwasserschutzgebiete",x=2.29,y=2.84)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Heilquellenschutzgebiete",x=2.29,y=2.125)
                static_link = u"http://geoportal.bayern.de/bayernatlas-klassik?lon="+str(x)+"&lat="+str(y)+"&zoom=12&addwms=http://www.lfu.bayern.de/gdi/wms/hwrk/ueberschwemmungsgebiete?"
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=static_link,text_element="vollpfad",x=2.35,y=1.75)
            if layer.name == "frost1":
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Frostzonenkarte Bayerns",text_element="Karte",x=11,y=23.75)
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"file:///C:/PfadzuFrostZonenKArte",text_element="vollpfad",x=2.35,y=1.75)

            if layer.name == "topo1":
                time.sleep(5)
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Topographische Karte",text_element="Karte",x=11,y=23.75)
                static_link = u"http://geoportal.bayern.de/bayernatlas-klassik?lon="+str(x)+"&lat="+str(y)+"&zoom=12"
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=static_link,text_element="vollpfad",x=2.35,y=1.75)

            if layer.name == "sk1":
                #add GK25 Name:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=sk1footprintPath ,pointGeometry=tempSHP,text_element="Bezugshorizont",tableField="Bezugshorizont_local",x=3.161,y=3.2652)
                #add GK25 fullpath:
                #point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo1footprintPath ,pointGeometry=tempSHP,text_element="vollpfad",tableField="fullpath",x=2.35,y=1.75)
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=sk1footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Name",x=11,y=23.75)

            #TODO Hier könenn weitere Legenden für weitere PDF Seiten hinzu gefügt werden



            """ DRUCKE KARTEN AUS """
            time.sleep(2)
            #if statements for unusual print settings, e.g. lower resolution to stay below maximum pixel boundaries.
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
                    if elm.name == 'HKLegende':
                        elm.elementPositionX = 36.8211
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == 'UeberschwemmungText':
                        elm.elementPositionX = 36.82
                    if elm.name == 'HKLegende':
                        elm.elementPositionX = 36.82
                    if elm.name == 'Bezugshorizont':
                        elm.elementPositionX = 36.82

            except:
                print "Fehler in main-function (main.py). Eines oder mehrere Layout-Elemente konnten nicht verschoben werden."
                arcpy.AddMessage("Fehler in main-function (main.py). Eines oder mehrere Layout-Elemente konnten nicht verschoben werden.")

            layer.visible = False
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()

#TODO Punkt zu Projekt Shapefile hinzufügen

#Commit changes and delete variable reference
pdfDoc.saveAndClose()
arcpy.DeleteRows_management(tempSHP)
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
mxd.save()
del rowInserter
del pdfDoc
del mxd
''' END CREATION OF PDF DOCUMENT -> RPOCEEDING WITH ADDING DATA TO PROJECT POINT '''
if addPoint == "TRUE":
    try:
        rowInserter = arcpy.InsertCursor(projectPointPath)
        rowUpdater = arcpy.UpdateCursor(projectPointPath)
        pointGeometry = arcpy.Point(x,y)
        newPoint = rowInserter.newRow()

        newPoint.Shape = pointGeometry
        # add az to point
        if not az == None:
            newPoint.az = az
        # add kopf data to bez (Bezeichnung)
        if not kopf == None:
            newPoint.Bemerkung = kopf
        if not category == None:
            newPoint.Kategorie = category

        rowInserter.insertRow(newPoint)

        del rowInserter
    except:
        print("Could not add project point. Exiting now...")
