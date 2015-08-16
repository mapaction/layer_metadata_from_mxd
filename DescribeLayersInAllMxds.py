import os
import arcpy, datetime
from os.path import basename


# ------------ !!!!  Edit these    !!!!  -------------------------------------  

# set the path to the folder where the mxds are 
mxdfolder = r"<enter full path here>"
## e.g. mxdfolder = r"D:\DescribeLayersInMXD"

# set the path to the table to write the output to
theOutput = r"<enter full path here>"
## e.g. theOutput = r"D:\DescribeLayersInMXD\MxdDescribeLayers.gdb\MXDDescribeLayers"

# ------------ !!!!  Stop editing  !!!!  -------------------------------------



arcpy.env.overwriteOutput = 1
starttime = datetime.datetime.now()
print "started job at ", str(starttime)



for root, dirs, files in os.walk(mxdfolder):
    for file in files:
        if file.endswith(".mxd"):
             print(os.path.join(root, file))
             themxd = file
             theMXDname = basename(themxd)
             print theMXDname
             mxd = arcpy.mapping.MapDocument(themxd)
             for df in arcpy.mapping.ListDataFrames(mxd):
                 print df.name
                 AllLayers = arcpy.mapping.ListLayers(mxd, "", df)
                 for layer in AllLayers:
                     print layer.name
                     rows = arcpy.InsertCursor(theOutput)
                     row = rows.newRow()
                     row.MxdName = theMXDname
                     print 'done mxdname'
                     row.Runtime = starttime
                     row.LayerName = layer.name
                     print 'done layer name'
                     row.dataFrameName = df.name
                     print 'done df name'
                     if layer.isGroupLayer == 0:
                         if layer.supports("DATASETNAME"):
                             row.DatasetName = str(layer.datasetName)
                             print 'done datasetName ', layer.datasetName
                         if layer.supports("DATASOURCE"):
                             row.DatasetSource = layer.dataSource
                             print 'done dataSource'
                         if layer.supports("DEFINITIONQUERY"):
                             row.DefinitionQuery = layer.definitionQuery
                             print 'done definitionQuery'
                         if layer.supports("TRANSPARENCY"):
                             row.Transparency = layer.transparency
                             print 'done transparency'
                         if layer.supports("BRIGHTNESS"):
                             row.brightness = layer.brightness
                             print 'done brightness'
                         if layer.supports("CONTRAST"):
                             row.contrast = layer.contrast
                             print 'done contrast'
                         if layer.supports("SHOWLABELS"):
                             row.showLabels = layer.showLabels
                             print 'done show labels'
                         if layer.supports("SYMBOLOGYTYPE"):
                             row.symbologyType = layer.symbologyType
                             print 'done symbology type'
                         row.IsFeatureLayer = layer.isFeatureLayer
                         print 'done isFeatureLayer'
                         row.MaxScale = layer.maxScale
                         print 'done maxScale'
                         row.MinScale = layer.minScale
                         print 'done minScale'
                         row.IsVisible = layer.visible
                         print 'done visible'
                         row.IsDataSourceBroken = layer.isBroken
                         print 'done isBroken'
                         row.LayerLongName = layer.longName
                         print 'done longName'
                     row.IsGroupLayer = layer.isGroupLayer
                     print 'done isGroupLayer'
                     rows.insertRow(row)
                     del rows
             del mxd

