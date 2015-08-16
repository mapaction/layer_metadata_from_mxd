#Import modules...
import arcpy, os, fnmatch, csv

#User input variables...
mxddirectory = os.getcwd()
outputFile = raw_input('Enter Output FileName (include extension xxx.csv):  ')
outputcsvlocation = os.path.join(os.getcwd(),outputFile)

#Create an empty list of ArcMap documents to process...
mxd_list=[]

#Walk through the input directory, adding paths for each .mxd file found to the list...

for dirpath, dirnames, filenames in os.walk(mxddirectory):
    for filename in filenames:
        print filename
        if fnmatch.fnmatch(filename, "*.mxd"):
            mxd_list.append(os.path.join(dirpath, filename))

#Iterate the list of mxd paths and gather property values then write to csv file...

if len(mxd_list) > 0:
    #Create the csv file...
    outputcsv = open(outputcsvlocation,"wb")
    writer = csv.writer(outputcsv, dialect = 'excel')
    writer.writerow(["MXD Path","Layer Name","Layer Description","Layer Source"])
    #Iterate through the list of ArcMap Documents...
    for mxdpath in mxd_list:
        print mxdpath
        mxdname = os.path.split(mxdpath)[1]
        try:
            mxd = arcpy.mapping.MapDocument(mxdpath)
            #Iterate through the ArcMap Document layers...
            for layer in arcpy.mapping.ListLayers(mxd):
                print layer
                layerattributes = [mxdpath, layer.longName, layer.description, layer.dataSource]
                #Write the attributes to the csv file...
                writer.writerow(layerattributes)
            del mxd
        except:
            arcpy.AddMessage("EXCEPTION: {0}".format(mxdpath))
        
    #close the csv file to save it...
    outputcsv.close()
#If no ArcMap Documents are in the list, then notify via an error message...
else:
    arcpy.AddError("No ArcMap Documents found. Please check your input variables.")
