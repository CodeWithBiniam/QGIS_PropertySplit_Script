# QGIS_PropertySplit_Script


This script helps in dividing a larger property into smaller ones, with each smaller parcel having at least a specific area (considering the least allowable size is 120 square meters). However, the script assumes that the properties are perfectly square, which may not be the case, so results might vary.


 summarizing the Python script
    1-Import Modules: We import necessary Python libraries: qgis.core, qgis.processing for QGIS-based operations, and math for mathematical functions.

    2-Load Data: We load a shapefile containing land parcel data. If the file path is correct, it gets added to the QGIS project.

    3-Iterate Over Parcels: For each land parcel (referred to as a 'feature'), we retrieve its geometry (the shape) and calculate its area.

    4-Check Parcel Size: If a parcel's area is larger than 500 square meters, we calculate how many smaller parcels of at least 120 square meters we can      create from it.

    5-Split Parcels: We create a grid to split the larger parcel:
        - Calculate width and height for the smaller parcels.
        - Get the bounding box of the larger parcel.
        - Create new layers for horizontal and vertical lines to form a grid.
        - Generate the grid by creating the horizontal and vertical lines.
        - Use the intersection of these lines to create the grid for dividing the larger parcel.
