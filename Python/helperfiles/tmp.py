# Script zur automatisierten Anlagenerstellung

import arcpy
import arcpy.mapping

# funciton declaration
def addData2Point(pathSHP,az,bez,geologie,x,y):
	""" addData2Point fügt Projektbezogene Daten in das Punkt Shapefile auf dem Server."""
	arcpy.AddMessage("\nCatalogPath:"+arcpy.mapping.desc.catalogPath+"\n"+"desc.file:"+arcpy.mapping.desc.file+"\n"+"desc.Type"+arcpy.mapping.desc.dataType)
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


# Enable / Disable Layers
def switchLayers(mxd,df):
	#A list of layer names that you want to be turned off.
	#TODO Erstelle bestimmte Szenarien in welchen festgelegt ist welche Layer angeschaltet sind.
	names = [x,y,z,etc]

	layers = arcpy.mapping.ListLayers(mxd, "*", df)

	for layer in layers:
	  if layer.name in names:
	    layer.visible = False

	arcpy.RefreshTOC()
	arcpy.RefreshActiveView()

def exportView(mxd,exportFile):


	arcpy.mapping.ListDataFrames(mxd)
	arcpy.mapping.ExportToTIFF(mxd,exportFile,640,480,96)




if __name__ == "__main__":
	exportFile = r"C:\Bild1.tif","PAGE_LAYOUT"
	# Lese Daten aus ModelBuilder ein
	#required parameters:
	x = arcpy.GetParameterAsText(0) #mandatory
	x = float(x)
	y = arcpy.GetParameterAsText(1) #mandatory
	y = float(y)
	projectLayer = arcpy.GetParameterAsText(2) #mandatory
	az = arcpy.GetParameterAsText(3) #mandatory
	bez = arcpy.GetParameterAsText(4) #optional
	geologie = arcpy.GetParameterAsText(5) #optional
	arcpy.AddMessage("{0},{1},{2},{3},{4},{5}".format(x,y,projectLayer,az,bez,geologie))
	#TODO
	#resolve pasted string from bayern viewer paste in (rw/hw): 4435307.25 5509620.0 bzw. GK4 (rw/hw): 4423120.0 5434432.0
	altXY = arcpy.GetParameterAsText(6) #optional
	if not arcpy.GetParameterAsText(6) == "":
		altXY = altXY.split(" ",1)
		x = altXY[0]
		arcpy.AddMessage("x={0}".format(x))
		x = float(x)
		y = altXY[1]
		arcpy.AddMessage("y={0}".format(y))
		y = float(y)





	# load map document and data frame
	mxd = arcpy.mapping.MapDocument('CURRENT')
	df = arcpy.mapping.ListDataFrames(mxd)[0]

	# add data to point if a project file is found:
	if not projectLayer == "":
		addData2Point(projectLayer,az,bez,geologie,x,y)


	# Zoom to point (in current map document)

	newExtent = df.extent
	newExtent.XMin, newExtent.YMin = x - 100, y - 100
	newExtent.XMax, newExtent.YMax = x + 100, y + 100
	df.extent = newExtent
	df.scale = 10000

	arcpy.RefreshActiveView()
