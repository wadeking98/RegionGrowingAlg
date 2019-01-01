# RegionGrowingAlg
This project uses region growing as an image processing technigue
In this case region growing is akin to "bucket fill" in a image processing/paint
application. Starting from a single specified pixel, the algorithm looks at all
adjacent pixels and decides if they are similar (ie, the pixel values are the same within some tolerance) simalar pixels are added to the region and selected
for the next iteration. The algorithm runs until no similar pixels can be found

# Using the command line interface
-Make sure you have cv2 and numpy installed on python3
-Add an image you would like to use to the project folder
-Specify a starting pixel for the bucket fill
-Specify a tolerance (ie how "similar" pixels have to be to be added 
to the region)

# Notes
This project works best on svg or computer generated images with litle noise
