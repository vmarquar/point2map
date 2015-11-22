

import arcpy

def footprint(inRaster,msk,outraster,outPoly):
    inRaster=1

    # Set environment
    arcpy.env.workspace = "C:/workspace"

    # Set Mask environment
    arcpy.env.mask = "C:/data/maskpoly.jpg"

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute Int
    outInt = Int(inRaster)

    # Save the output
    outInt.save("C:/sapyexamples/output/outint")

    #convert
    arcpy.RasterToPolygon_conversion(outInt, outPolygons, "NO_SIMPLIFY")
