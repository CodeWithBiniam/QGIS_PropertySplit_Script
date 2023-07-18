from qgis.core import *
from qgis import processing
import math

# Load the Data
layer = QgsVectorLayer('path_to_your_shapefile', 'land_parcels', 'ogr')

# Check if the layer is loaded correctly
if not layer.isValid():
    print('Layer failed to load!')
else:
    QgsProject.instance().addMapLayer(layer)

# Iterate over the Features
for feature in layer.getFeatures():
    geom = feature.geometry()  # Geometry of the feature (parcel)
    area = geom.area()  # Area of the feature (parcel)

    # If the area of the parcel is greater than 500 m^2
    if area > 500:
        # Number of parcels to split into, rounded up to ensure each parcel is at least 120 m^2
        num_parcels = math.ceil(area / 120)

        # Calculate the width and height of each parcel based on the square root of the desired area
        parcel_width = math.sqrt(120)
        parcel_height = parcel_width  # Parcels are square

        # Get the bounding box
        bounding_box = geom.boundingBox()

        # Calculate number of horizontal and vertical lines
        num_horizontal_lines = math.ceil(bounding_box.height() / parcel_height)
        num_vertical_lines = math.ceil(bounding_box.width() / parcel_width)

        # Generate horizontal lines
        horizontal_lines = QgsVectorLayer("LineString", "horizontal_lines", "memory")
        hpr = horizontal_lines.dataProvider()
        for i in range(num_horizontal_lines):
            line = QgsFeature()
            line.setGeometry(QgsGeometry.fromPolyline([
                QgsPoint(bounding_box.xMinimum(), bounding_box.yMinimum() + i * parcel_height),
                QgsPoint(bounding_box.xMaximum(), bounding_box.yMinimum() + i * parcel_height)
            ]))
            hpr.addFeature(line)

        # Generate vertical lines
        vertical_lines = QgsVectorLayer("LineString", "vertical_lines", "memory")
        vpr = vertical_lines.dataProvider()
        for i in range(num_vertical_lines):
            line = QgsFeature()
            line.setGeometry(QgsGeometry.fromPolyline([
                QgsPoint(bounding_box.xMinimum() + i * parcel_width, bounding_box.yMinimum()),
                QgsPoint(bounding_box.xMinimum() + i * parcel_width, bounding_box.yMaximum())
            ]))
            vpr.addFeature(line)

        # Intersect the layers
        intersection = processing.run("qgis:intersection", {'INPUT': horizontal_lines, 'OVERLAY': vertical_lines, 'OUTPUT': 'memory:'})['OUTPUT']
        QgsProject.instance().addMapLayer(intersection)
