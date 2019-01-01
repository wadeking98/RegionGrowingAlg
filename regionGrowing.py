#!usr/bin/env python3

"""
Author
------
    Wade King Dec 30 2018
"""

import numpy as np
import cv2
import queue

#determines if a given pixel is in the bounds of the board
def inBounds(pixel, image):
    """
    Determines if a given pixel is in a specified image
    
    Parameters
    ----------
        arg1 : tuple the pixel in question
        arg2 : list the image containing the pixel
    Returns
    -------
        boolean
            True if pixel is in the image
    """
    dims = image.shape
    if pixel[0]<0 or pixel[0]>=dims[0]:
        return False
    elif pixel[1]<0 or pixel[1]>=dims[1]:
        return False
    else:
        return True

#return adjacent pixels who's value is within the given tolerance and is outside the region
def getRegAdj(pixel, image, regMap, tolerance=1):
    """
    gets all pixels adjacent to the given pixel that satisfy 2 criteria: the difference between the value of the 
    adjacent pixels and the given pixel is within the tolerance provided, and the adjacent pixel is not already 
    within the region
    
    Parameters
    ----------
        arg1 : tuple the pixel in question
        arg2 : list the image containing the pixel
        arg3 : list the region map
        arg4 : int the tolerance for getting adjacent pixels
    Returns
    -------
        list
            all adjacent pixels that satisfy the tolerance and are not alreayd within the region
    """
    adj = []
    row = pixel[0]
    col = pixel[1]
    
    thisVal = image[row][col]
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            pixel = (row-i, col-j)
            try:
                newVal = image[row-i][col-j]

                diff = abs(newVal-thisVal)
                # if pixel is an interior point or is different from the region do nothing
                if(i>-1 and j>-1)and(i<1 and j<1):
                    continue
                else:
                    if inBounds(pixel, image) and diff<=tolerance and not inRegion(pixel, regMap):
                        adj.append(pixel)
            except:
                pass
    return adj


def getAllAdj(pixel, image):
    """
    gets all pixels adjacent to the given pixel regardless of the value of the two pixels or if one pixel is
    already in the region
    
    Parameters
    ----------
        arg1 : tuple the pixel in question
        arg2 : list the image containing the pixel
    Returns
    -------
        list
            all adjacent pixels to the given pixel
    """
    adj = []
    row = pixel[0]
    col = pixel[1]
    
    thisVal = image[row][col]
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            newVal = image[row-i][col-j]
            
            # if pixel is an interior
            if(i>-1 and j>-1)and(i<1 and j<1):
                continue
            else:
                if inBounds((row-i, col-j), image):
                    adj.append((row-i, col-j))
    return adj



#determines if a pixel is already in the region
def inRegion(pixel, regMap):
    """
    determines if a given pixel is already part of the region
    
    Parameters
    ----------
        arg1 : tuple the pixel in question
        arg2 : list the array containing the current region map
    Returns
    -------
        boolean
            True if pixel is already in the region
    """
    return regMap[pixel[0]][pixel[1]] == 0
        


def regionGrow(pixel, image, regMap, tolerance=1, imageCopy=None, newImgVal=0):
    """
    the main logic of the region growing algorithm, from a given pixel it will add adjacent pixels to the region
    if they are similar. The algorithm will keep going until there are no similar adjacent pixels
    
    Parameters
    ----------
        arg1 : tuple the pixel in question
        arg2 : list the image containing the pixel
        arg3 : list the region map
        arg4 : int the tolerance for getting adjacent pixels
        arg5 : list a copy of the image to be written to
        arg6 : int the intensity of the new image value, between 0-255
    
    """
    
    Q = queue.Queue()
    
    #mark starting pixel
    regMap[pixel[0]][pixel[1]]=newImgVal
    if imageCopy is not None:
        imageCopy[pixel[0]][pixel[1]] = newImgVal
    
    #get adjacent pixels, within the tolerance, outside of the already marked region
    regAdj = getRegAdj(pixel, image, regMap, tolerance)
    
    #initialize the queue with the adjacent pixels
    for adjPx in regAdj:
        Q.put(adjPx)
        #mark adjacent pixels
        regMap[adjPx[0]][adjPx[1]] = newImgVal
        if imageCopy is not None:
            imageCopy[adjPx[0]][adjPx[1]] = newImgVal
    
    
    #start BFS
    while(not Q.empty()):
        #dequeue the next pixel
        nextPx = Q.get()
        
        #enque all adjacent pixels
        nextRegAdj = getRegAdj(nextPx, image, regMap, tolerance)
        for nextAdjPx in nextRegAdj:
            Q.put(nextAdjPx)
            #mark adjacent pixels
            regMap[nextAdjPx[0]][nextAdjPx[1]] = newImgVal
            if imageCopy is not None:
                imageCopy[nextAdjPx[0]][nextAdjPx[1]] = newImgVal

                
'''
________________________MAIN_____________________
'''
                
#python does not have do-while loop so we will have to improvise
err = True
while err:
    #get filename from user
    file = input("enter image file name: ")
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    if image is not None:
        err = False
    else:
        print("Err: File not found")
        err = True
        #raise Exception("Err: File not found")

err = True
while err:
    #get starting point from user
    print("enter starting pixel in the form (x,y) or x,y (Note the size of your image is {:d}, {:d}):".format(image.shape[0], image.shape[1]))
    pointStr = input()
    #clean up user input
    pointStr = pointStr.strip("()")
    ptTokens = pointStr.split(",")
    #starting pixel
    stPx = (int(ptTokens[0]), int(ptTokens[1]))
    #exit if incorrectly inputed
    if len(ptTokens) < 2:
        print("Err: please input a pixel in the form (x,y) x,y or x y")
        err = True
    elif not inBounds(stPx, image):
        print("Err: your selected pixel is outside of the image, for pixel (x,y) please use x value between 0-{:d} and y value between 0-{:d}".format(image.shape[0]-1, image.shape[1]-1))
        err = True
    else:
        err = False

err = True
while err:
    #get tolerance from user
    print("enter tolerance for bucket fill, if you dont know what ")
    tolerance = int(input("this is 50 is normally a good value "))
    if tolerance < 0 or tolerance > 255:
        print("Err: incorrect value for tolerance, please choose a value between 0-255")
        err = True
    else:
        err = False







#copy image and init region map
imageCopy = image.copy()
regMap = np.full(image.shape, 255)



regionGrow(stPx, image, regMap, tolerance=tolerance, imageCopy=imageCopy)


cv2.imwrite("output.jpg", imageCopy)
cv2.imwrite("regionMap.jpg", regMap)



