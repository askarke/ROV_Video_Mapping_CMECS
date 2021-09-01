

# Map production script.py
# Geospatial analysis of deep-sea environments using ROV video data with the Coastal and Marine Ecological Classification Standard (CMECS).
# Creator: Jacob Freeman 
# Institution: Mississippi State University, Department of Geosciences

from qgis.PyQt import QtGui

# This script generates an output map in .pdf format with the specified shape files. 
# Both the Dive Path and CMECS substrate layers should alwyas be called in order for them to be mapped in the final layout.
layers = QgsProject.instance().mapLayersByName('Dive Path')
layer = layers[0]
layers2 = QgsProject.instance().mapLayersByName('CMECS Substrate Units')
layer2 = layers2[0]

project = QgsProject.instance()
manager = project.layoutManager()
# layoutName allows you to assign a final name to the map layout.
layoutName = 'Dive Map layout'
layouts_list = manager.printLayouts()
# This will remove and duplicate layouts
# These parameters must stay the same in order for the desired map to be properly created.
for layout in layouts_list:
    if layout.name() == layoutName:
        manager.removeLayout(layout)
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layoutName)
manager.addLayout(layout)

# create map item in the layout
# This line of code sets the size of the map image.
# These parameters must stay the same in order for the desired map to be properly created.
map = QgsLayoutItemMap(layout)
map.setRect(20, 20, 20, 20)

# set the map extent
ms = QgsMapSettings()
ms.setLayers([layer,layer2])
# set layers to be mapped
rect = QgsRectangle(ms.fullExtent())
rect.scale(1.1)
ms.setExtent(rect)
map.setExtent(rect)
map.setBackgroundColor(QColor(255, 255, 255, 0))
layout.addLayoutItem(map)

# Creates the frame around the map.
# If a frame is not desired for the final map, the true statement must be changed to false.
map.setFrameEnabled(True)
# Both of these map parameters position the loaded shape files at a desired location within the map layout.
map.attemptMove(QgsLayoutPoint(5, 25, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(200, 169, QgsUnitTypes.LayoutMillimeters))

# Creates the map legend.
# The only line of code that should be modified in this section is the title.
legend = QgsLayoutItemLegend(layout)
# To change the title for the legend manually enter the new title. The title must have quotation marks around it.
legend.setTitle("") # Title of legend can be changed.
layerTree = QgsLayerTree()
layerTree.addLayer(layer)
layerTree.addLayer(layer2)
legend.model().setRootGroup(layerTree)
layout.addLayoutItem(legend)
legend.attemptMove(QgsLayoutPoint(226.954, 114.926, QgsUnitTypes.LayoutMillimeters))

# Creates the map scalebar.
scalebar = QgsLayoutItemScaleBar(layout)
# There are many different types of scalebars that can be used during the production of the map.
# For this particular dive the scalebar is 'Line Ticks Up'.
scalebar.setStyle('Line Ticks Up') # Type of scalebar can be edited.
# Sets the type of units that the scalebar will use to measure distance.
scalebar.setUnits(QgsUnitTypes.DistanceMeters)
# Sets the number of segments in the scalebar.
scalebar.setNumberOfSegments(2)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(200)
# Links the current map with the scalebar.
scalebar.setLinkedMap(map)
# Sets the unit label for the scalebar.
scalebar.setUnitLabel('m')
# Sets the font style and size for the scalebar.
scalebar.setFont(QFont('Arial', 15)) # This is where scalebar font cant be edited.
scalebar.update()
layout.addLayoutItem(scalebar)
# Moves the scalebar to the desired location on the map layout.
# For this particular map, these parameters should not be modified.
scalebar.attemptMove(QgsLayoutPoint(4.7986, 195.063, QgsUnitTypes.LayoutMillimeters))

# Creates the title for the final map.
# For each new dive being mapped this is where the title should be manually entered. 
title = QgsLayoutItemLabel(layout)
title.setText("EX 1903 L2 Dive 19") # This is where a new map title will be entered.
title.setFont(QFont('Arial', 24))
title.adjustSizeToText()
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(70, 5, QgsUnitTypes.LayoutMillimeters))

# Creates the subtitle, showing date that the dive was conducted.
# For each new dive being mapped this is where the subtitle will be manually entered. 
map_label = QgsLayoutItemLabel(layout)
map_label.setText("Date:              July 11, 2019") # This is where a new subtitle will be entered. 
map_label.setFont(QFont("Arial", 12))
map_label.adjustSizeToText()
layout.addLayoutItem(map_label)
map_label.attemptMove(QgsLayoutPoint(208.454, 100.689, QgsUnitTypes.LayoutMillimeters))

# Creates and formats a text box that displays the coordinate system used to create the map.
# For this particular mapping analysis the coordinate system should remain the same. 
map_label = QgsLayoutItemLabel(layout)
map_label.setText("ESPG: 4326 - WGS 84") 
map_label.setFont(QFont("Arial", 15))
map_label.adjustSizeToText()
layout.addLayoutItem(map_label)
map_label.attemptMove(QgsLayoutPoint(239.473, 199.485, QgsUnitTypes.LayoutMillimeters))

# Creates and formats a text box that displays the max depth that the ROV reached during the dive.
# This text box must be edited for the creation of a new map.
map_label = QgsLayoutItemLabel(layout)
map_label.setText("Max Depth:    1623 Meters") # The text can be edited here.
map_label.setFont(QFont("Arial", 12))
map_label.adjustSizeToText()
layout.addLayoutItem(map_label)
map_label.attemptMove(QgsLayoutPoint(208.454, 106.151, QgsUnitTypes.LayoutMillimeters))

# Creates and formats a text box showing the bottom time of the ROV during the dive.
# This box must be edited for the creation of a new map.
map_label = QgsLayoutItemLabel(layout)
map_label.setText("Bottom Time: 5 Hours 58 Minutes 00 Seconds") # Bottom time can be edited here.
map_label.setFont(QFont("Arial", 12)) # Text can be edited here.
map_label.adjustSizeToText()
layout.addLayoutItem(map_label)
map_label.attemptMove(QgsLayoutPoint(208.454, 111.614, QgsUnitTypes.LayoutMillimeters))

# Inserts NOAA logo. 
img = QgsLayoutItemPicture(layout)
img.setPicturePath("C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\NOAA.jpg")

# sets the image size
img.attemptResize(QgsLayoutSize(68.9972, 69.0024,QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(img)
# move to exact position
img.attemptMove(QgsLayoutPoint(213.652, 24.6785, QgsUnitTypes.LayoutMillimeters))

# Inserts north arrow.
img = QgsLayoutItemPicture(layout)
img.setPicturePath("C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\North_Arrow.JPG")

# set the image size
img.attemptResize(QgsLayoutSize(8.93797, 17.1283,QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(img)
# move to exact position
img.attemptMove(QgsLayoutPoint(282.721, 4.89614, QgsUnitTypes.LayoutMillimeters))

layout = manager.layoutByName(layoutName)
exporter = QgsLayoutExporter(layout)
# Export PDF document of the map.
# fn should equal your current working folder, or a desired folder you wish to store the final PDF output of the map. 
fn = "C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\NOAA Final Maps\\EX 1903 L2\\Divetest.pdf"
#exporter.exportToImage(fn, QgsLayoutExporter.ImageExportSettings())
exporter.exportToPdf(fn, QgsLayoutExporter.PdfExportSettings())
