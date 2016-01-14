#!/usr/bin/python
# coding: utf-8
import arcpy,os
manual_encoding = "utf-8" # "latin-1" or "cp850" or sys.getdefaultencoding()
manual_decoding = "mbcs" # "utf-8"

def addData2Point(pathSHP,x,y,az="123456",bez="k/a",geologie="k/a"):
	""" addData2Point fügt Projektbezogene Daten in das Punkt Shapefile auf dem Server."""
	try:
		if not (bez == "" and geologie == ""):
			row = (az,bez,geologie,(x, y))
			arcpy.AddMessage("Add new data entry: with AZ: {0},Bezeichnung: {1} and Geologie: {2}".format(az,bez,geologie))
			# Open an InsertCursor
			#
			c = arcpy.da.InsertCursor(pathSHP, ("Az", "Bez","Geologie","SHAPE@XY"))

		elif not bez == "":
			row = (az,bez,(x, y))
			arcpy.AddMessage("Add new data entry: with AZ: {0} and Bezeichnung: {1}".format(az,bez))
			# Open an InsertCursor
			#
			c = arcpy.da.InsertCursor(pathSHP, ("Az", "Bez","SHAPE@XY"))
		elif not az == "":
			row = (az,(x, y))
			arcpy.AddMessage("Add new data entry: with AZ:{0}".format(az))
			# Open an InsertCursor
			#
			c = arcpy.da.InsertCursor(pathSHP, ("Az","SHAPE@XY"))
		else:
			row = (x, y)
			arcpy.AddMessage("Add new data entry with x,y data")
			# Open an InsertCursor
			#
			c = arcpy.da.InsertCursor(pathSHP, "SHAPE@XY")
		# Insert new rows that include the az name and a x,y coordinate
		#  pair that represents the project center
		#
		c.insertRow(row)

		# Delete cursor object
		#
		del c
	except:
		arcpy.AddMessage("Error executing add_row function. Make sure your provided shape file has at least a field called Az.")
		pass


def rasterCatalogName2textElement(map_document,footprint_layer=r"geo1/GK25_footprint" ,pointGeometry="temp.shp",text_element="Karte",tableField="Name",x=11,y=23.75):
    """ copies point and raster catalog geometry and checks which raster contains the input point(s).
        After that it prints the raster name to the map document.
        Dependency: checkGeometry function
    """
    try:
        raster_name = checkGeometry(footprint_layer,pointGeometry,tableField)
        arcpy.AddMessage(raster_name)
        for elm in arcpy.mapping.ListLayoutElements(map_document, "TEXT_ELEMENT"):
            if elm.name == text_element:
				elm.text = raster_name
				elm.elementPositionX = x
				elm.elementPositionY = y
				break
    except:
        arcpy.AddError("Fehler in Funktion rasterCatalogName2textElement ({0})(rasterCatalogName2textElement -> point2map-library).".format(footprint_layer))
        print("Fehler in Funktion rasterCatalogName2textElement (rasterCatalogName2textElement -> point2map-library).")



def checkGeometry(polygon,point,tableField="Name"):
    """ polygon has to be either a layer object or a shp file / gdb feature file without a Raster-field.
        point has to be a either a layer object or a shp/gdb feature file. NOTE: Only the last row will be taken into consideration.
        Returns: A str-list of polygons which contain the point.
    """
    try:

        #result=[]
        string = ""
        print type(string)
        polygonGeometries= arcpy.CopyFeatures_management(polygon,arcpy.Geometry())
        try:
            pointGeometry= arcpy.CopyFeatures_management(point,arcpy.Geometry())[-1]
        except:
            arcpy.AddWarning("Die Point-Datei ist leer!")
            print("Die Point-Datei ist leer!")
        polygonNames = [row[0] for row in arcpy.da.SearchCursor(polygon, (tableField))]

        for index,polygonGeometry in enumerate(polygonGeometries):
            if polygonGeometry.contains(pointGeometry):
                print "Die Geometrie enthaelt:"+polygonNames[index]
                #result.append(polygonNames[index])
                string += polygonNames[index] +"\n"
        return string
    except:
        arcpy.AddMessage("Fehler in Funktion checkGeometry (checkGeometry -> point2map-library).")
        print("Fehler in Funktion checkGeometry (checkGeometry -> point2map-library).")
        string = "Kartengrundlage: Keine Karte gefunden!"
        return string


def picture2legend(map_document,picture_element="HK500Legend",x=6.8211,y=5.0):
    """ moves a legend item to a specified x,y location on the .pdf map
        Dependencies: Legend item must be added prior executing this function
    """
    try:
        for elm in arcpy.mapping.ListLayoutElements(map_document, "PICTURE_ELEMENT"):
            if elm.name == picture_element:
                elm.elementPositionX = x
                #TODO add elm.elementPositionY = y #genaue Position (um mögliche Bugs zu verhindern)
                break
    except:
        arcpy.AddWarning("Fehler in Funktion picture2legend (picture2legend -> point2map-library).")
        print("Fehler in Funktion picture2legend (picture2legend -> point2map-library).")


def staticText2textElement(map_document,static_text=u"Kartenname",text_element="Karte",x=2.31,y=3.8):
    """ adds a given / known text (UNICODE) to the .pdf map (layout element)
        output is in specified encoding.
    """
    try:
        for elm in arcpy.mapping.ListLayoutElements(map_document, "TEXT_ELEMENT"):
            if elm.name == text_element:
                elm.text = static_text.encode("mbcs")
                elm.elementPositionX = x
                elm.elementPositionY = y
                break
        #time.sleep(2) #wait until text is drawn
    except:
        arcpy.AddWarning("Fehler in Funktion staticText2textElement (staticText2textElement -> point2map-library).")
        print("Fehler in Funktion staticText2textElement (staticText2textElement -> point2map-library).")


def footprint(workspace="C:/workspace",static_value=1,mask="C:/data/maskpoly.jpg",outFootprint="footprint.shp",outIntRaster="IntRaster.jpg"):
    """ calculates the footprint of a raster input.
        Procedure: Creating a mask (of input raster), calculating an integer raster,
        converting integer raster to polygon, deleting integer raster
    """
    try:
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = workspace
        #set mask
        arcpy.env.mask = mask
        #compute integer raster and save it
        outInt = Int(static_value)
        outInt.save(outIntRaster)
        #convert integer raster to polygon
        arcpy.RasterToPolygon_conversion(outInt, outFootprint, "NO_SIMPLIFY")
        #TODO delete processes and int raster

    except:
        print "Footprint (lokale Funktion -> point2map-library) konnte nicht berechnet werden."
        arcpy.AddWarning("Footprint (lokale Funktion -> point2map-library) konnte nicht berechnet werden.")
