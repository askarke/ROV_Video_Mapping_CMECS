# Mapping script.py
# Geospatial analysis of deep-sea environments using ROV video data with the Coastal and Marine Ecological Classification Standard (CMECS).
# Creator: Jacob Freeman 
# Institution: Mississippi State University, Department of Geosciences

# This script was designed to run in PyQGIS.

# The first create points layer from table algorithm allows 1 Hz rov data to be mapped in the form of a point shapefile.


# Use the QGIS “Create points layer from table” tool to create a point shape file from ROV navigational data stored in a 1Hz .csv file.
# INPUT is a 1 Hz data file from the ROV in csv format.
# XFIELD is'LON_DD' as long as the user does not make manual corrections to the 1 Hz .csv file header.
# YFIELD is "LAT_DD' as long as the user does not make manual corrections to the 1 Hz .csv file header. 
# ZFIELD is None.
# TARGET_CRS is QgsCoordinateReferenceSystem('EPSG:4326').
# OUTPUT is a path for the desired folder in which the output shapefile will be stored.
# onehzpath will always remain ['OUTPUT'].
result = processing.run("qgis:createpointslayerfromtable",
{'INPUT':"C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\1 hz dive files\\EX 1903L2 Dives\\EX1903L2_DIVE11_20190703\\EX1903L2_DIVE11_RovTrack1Hz.csv", 
'XFIELD': 'LON_DD', 
'YFIELD': 'LAT_DD',
'ZFIELD': None,
'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
'OUTPUT':"C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\NOAA Shapefiles\\path_dive_EX1903#11.shp"})
onehzpath = result['OUTPUT']


# Use the QGIS “Points to path” tool to create a 1 Hz dive path shapefile
# INPUT is the output parameter that is set in the previous section of the script (Example: onehzpath).
# ORDER_FIELD is date. 
# GROUP_FIELD is None.
# DATE_FORMAT is ''. 
# OUTPUT is a path for the desired folder in which the output shapefile will be stored.
# divepath will always remain ['OUTPUT'].
result = processing.run("qgis:pointstopath",
{'INPUT': onehzpath,
'ORDER_FIELD': 'DATE',
'GROUP_FIELD': None,  
'DATE_FORMAT':'', 
'OUTPUT':"C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\NOAA Shapefiles\\Dive Path.shp"})
divepath = result['OUTPUT']


# Use the QGIS “Create points layer from table” tool to creates a shapefile with points at each location where seafloor annotation was recorded in the SeaTube annotation data file.
# INPUT of this algorith will always remain a Dive annotation data file from the ROV in .csv format, that is acquired from SeaTube.
# XFIELD is 'Enviroment - Longitude' as long as the user does not make manual corrections to the annotation .csv file.
# YFIELD is 'Enviroment - Latitude' as long as the user does not make manual corrections to the 1 annotation .csv file. 
# ZFIELD is None.
# TARGET_CRS is QgsCoordinateReferenceSystem('EPSG:4326').
# OUTPUT is a path for the desired folder in which the output shapefile will be stored.
# annotation will always remain ['OUTPUT'].
result = processing.run("qgis:createpointslayerfromtable",
{'INPUT':"C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\Dive_annotation_files\\EX 1903 L2\\Dive11.csv", 
'XFIELD': 'Environment - Longitude', 
'YFIELD': 'Environment - Latitude',
'ZFIELD': None,
'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
'OUTPUT':"C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\Graduate Research\\NOAA Shapefiles\\annotation_points_EX1903_Dive#11.shp"})
annotation = result['OUTPUT']

# Use the QGIS “Wedge Buffer” tool to creates wedge polygons that represent the seafloor extent of the ROV camera viewshed at the point in time when each annotation was made as well as substrate type.
# INPUT is "annotation", this allows the wedges to be placed where observations were made along the seafloor. 
# AZIMUTH is QgsProperty.fromExpression("attribute('Environm_1')").
# WIDTH is set to “44”. To represent an estimated camera view angle of 44°(This may be modified to represent different camera view geometries).
# OUTER_RADIUS is set to 0.0005. This represents an estimated viewshed depth in map units. (This may be modified to represent different camera view geometries and environmental conditions)
# INNER_RADIUS is 0.
# OUTPUT is a path for the desired folder in which the output shapefile will be stored.
# wedgebuffer will always remain ['OUTPUT'].
result = processing.run("native:wedgebuffers",
{'INPUT': annotation,
'AZIMUTH': QgsProperty.fromExpression("attribute('Environm_1')"),
'WIDTH': 44, 
'OUTER_RADIUS': 0.0005, 
'INNER_RADIUS': 0,
'OUTPUT':"C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\Graduate Research\\NOAA Shapefiles\\wedge_buffers_EX1903_dive#11.shp"})
wedgebuffer = result['OUTPUT']

# Use the QGIS “Dissolve” tool to dissolves the boundary between overlapping wedge polygons with common substrate classifications. 
# INPUT is wedgebuffer.
# DISSOLVE_ALL is None.
# FIELD is 'Substrate' 
# OUTPUT is a path for the desired folder in which the output shapefile will be stored.
# wedgebuffer will always remain ['OUTPUT'].
result = processing.run('qgis:dissolve',
{'INPUT': wedgebuffer ,
'DISSOLVE_ALL': None,
'FIELD': 'Substrate',
'OUTPUT':"C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\NOAA Shapefiles\\CMECS Substrate Units.shp"})
dissolvebuffer = result ['OUTPUT']

# Load the generated shapefiles into QGIS. 
# qmlfile ssets the exact color and symbology for the polygon shapefiles. The substrate qml file should be stored in the same working folder as all other shapefiles and scripts used to generate the maps.
# fileInfo is QFileInfo(dissolvebuffer).
# basename is fileInfo.baseName().
# rlayer is QgsVectorLayer(dissolvebuffer, baseName).
# The if statement and the parameters found within it should not be modified.
qmlfile = "C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\NOAA qml files\\Substrate type by colorv2.qml"
fileInfo = QFileInfo(dissolvebuffer)
baseName = fileInfo.baseName()
rlayer = QgsVectorLayer(dissolvebuffer, baseName)
if rlayer.isValid():
   print ('Layer loaded!') 
QgsProject.instance().addMapLayer(rlayer)
processing.run("native:setlayerstyle", {'INPUT': dissolvebuffer, 'STYLE': qmlfile})   ##returns nothing........
extent = rlayer.extent()
rlayer.triggerRepaint()

# his portion of the mapping script loads the previously generated and dive path shapefile into QGIS and applies a uniform prescribed color symbology. 
# qmlfile sets the exact color and symbology for the line shapefile. The substrate qml file should be stored in the same working folder as all other shapefiles and scripts used to generate the maps.
# fileInfo is QFileInfo(divepath).
# basename is fileInfo.baseName().
# rlayer is QgsVectorLayer(divepath, baseName).
# The if statement and the parameters found within it should not be modified.
qmlfile= "C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\NOAA qml files\\divepath.qml"
fileInfo = QFileInfo(divepath)
basename = fileInfo.baseName()
rlayer = QgsVectorLayer(divepath, basename)
if rlayer.isValid():
    print('Layer loaded!')
QgsProject.instance().addMapLayer(rlayer)
processing.run("native:setlayerstyle", {'INPUT': divepath, 'STYLE': qmlfile})
extent = rlayer.extent()
rlayer.triggerRepaint()
