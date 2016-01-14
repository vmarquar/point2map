#!/usr/bin/python
# coding: utf-8

"""
point2map_v03 ist fuer die console und Rechner PC-31 bestimmt!
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


"""Input (default) data"""
x = 4420171
y = 5456084
az = u"Az. 15000"
kopf = u"Kartengrundlagen"

dfName = "Layers"
views = ["geo1", "geo2","geo3","hydro1","hydro2","hydro3","frost1","topo1"]
#views = []
scales = ["15000","30000","30000","100000","30000","300000","100000","30000"]

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
with codecs.open('N:/Start_Script/config.file', 'r', encoding='utf-8') as f:
    parser.readfp(f)

print "Read in following arguments:\n"
print parser.get('mandatory_fields','x')
print parser.get('mandatory_fields','y')
print parser.get('mandatory_fields','az')
print parser.get('mandatory_fields','kopf')
print parser.get('mandatory_fields','pdfRootPath')
print parser.get('mandatory_fields','Untersuchungsgebiet')
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
    print "Fehler beim einlesen von kopf"
Untersuchungsgebiet = parser.get('mandatory_fields','Untersuchungsgebiet')
try:
    Untersuchungsgebiet = u''+Untersuchungsgebiet
except:
    print "Fehler beim einlesen von Untersuchungsgebiet"
pdfRootPath =  parser.get('mandatory_fields','pdfRootPath')
if pdfRootPath[-1] != "/":
    pdfRootPath += "/"
pdfRootPath = os.path.normpath(pdfRootPath)




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
    if elm.name == 'Untersuchungsgebiet':
        elm.text = Untersuchungsgebiet.encode("mbcs")

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
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo1footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Name")
                #add GK25 fullpath:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo1footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Vollpfad_georef_Karte_mit_Legende")
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
                #TODO Ideen: Link zur Geologischen Karte mit Legende (replace string *_c.jpg with *.jpg)
            if layer.name == "geo2":
                #add GK25 Name:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo2footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Name")
                #add GK25 fullpath:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo2footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Vollpfad_georef_Karte_mit_Legende")
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
            if layer.name == "geo3":
                #add GK25 Name:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo3footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Name")
                #add GK25 fullpath:
                point2mapLibrary.rasterCatalogName2textElement(map_document=mxd,footprint_layer=geo3footprintPath ,pointGeometry=tempSHP,text_element="Karte",tableField="Vollpfad_georef_Karte_mit_Legende")
                #TODO Falls weitere Legendeninformationen verfügbar sind, können diese hier festgelegt werden.
                #TODO Ideen: link zu Geologischen Erläuterungen
            if layer.name == "hydro1":
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="HK500Legend",x=6.8211,y=5.0)
                #TODO staticText2textElement durch eine Version von rasterCatalogName2textElement ersetzen
                #TODO Dazu muss zunächst der Footprint für Ansbach, HK500 und Wassergleichen-Nürnberg erstellt werden
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Grundwassergleichenkarte",text_element="Karte",x=2.31,y=3.8)
            if layer.name == "hydro2":
                #wait 20 sec to draw WMS data
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(20)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Karte der wassersensiblen und überschwemmungsgefährdeten Bereiche",text_element="Karte",x=2.31,y=3.8)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="UeberschwemmungText",x=4.2236,y=5.0)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Festgesetzte_ueberschwemmungsgebiete",x=2.3524,y=5.0)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="WassersensibelLegend",x=11.9518,y=5.0)
            if layer.name == "hydro3":
                #wait 20 sec to draw WMS data
                #TODO Bei Gelegenheit schoener schreiben
                time.sleep(20)
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Karte der Trinkwasser- und Heilquellenschutzgebiete",text_element="Karte",x=2.31,y=3.8)
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Trinkwasserschutzgebiete",x=13.8323,y=5.0)
                #TODO x von Heilquellenschutzgebiete genauer definieren
                point2mapLibrary.picture2legend(map_document=mxd,picture_element="Heilquellenschutzgebiete",x=11.8323,y=5.0)
            if layer.name == "frost1":
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Frostzonenkarte Bayerns",text_element="Karte",x=2.31,y=3.8)
            if layer.name == "topo1":
                time.sleep(10)
                point2mapLibrary.staticText2textElement(map_document=mxd,static_text=u"Topographische Karte 1:25.000",text_element="Karte",x=2.31,y=3.8)


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
            except:
                print "Fehler in main-function (main.py). Eines oder mehrere Layout-Elemente konnten nicht verschoben werden."
                arcpy.AddMessage("Fehler in main-function (main.py). Eines oder mehrere Layout-Elemente konnten nicht verschoben werden.")

            layer.visible = False
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()



#Commit changes and delete variable reference
pdfDoc.saveAndClose()
arcpy.DeleteRows_management(tempSHP)
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
mxd.save()
del rowInserter
del pdfDoc
del mxd
