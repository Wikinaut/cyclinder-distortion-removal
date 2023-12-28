#! /usr/bin/env python2

# source: https://drive.google.com/file/d/12VnsZ-5kR_lDkDBFr_k0xz27nHXYIxR5
# distortion_of_cylindrical_projection.py

from gimpfu import *
import math

def (img, layer, cylinderDiameter, steps):
    pdb.gimp_image_undo_group_start(img)

    originalItemVisible = TRUE

    if pdb.gimp_item_get_visible(layer) == FALSE:                                               #checks if the layer is visible
        pdb.gimp_item_set_visible(layer, TRUE)
        originalItemVisible = FALSE

    if cylinderDiameter < layer.width:                                                          #makes sure that: (cylinderdiameter >= layer.width)
        cylinderDiameter = layer.width

    originalWidth = (math.asin(layer.width/cylinderDiameter)*cylinderDiameter* math.pi)/math.pi #original width of the cylinder
    initialAngle = math.acos((layer.width/2)/(cylinderDiameter/2))                              #the blank angle resulting from: (layer.width < cylinderDiameter)
    segmentAngle = (math.pi - (2 * initialAngle))/ steps                                        #angle of each segment
    lastLateralDistance = (cylinderDiameter/2) - ((cylinderDiameter / 2) * math.cos(initialAngle)) 
    #the distance from the left side of the (imaginary) cylinder to the left side of the current/ first segment
    offset = 0                                                                                  #this offset ensures that the area left to the segment is also cut off
    originalSegmentWidth = originalWidth / steps                                                #width of the undistorted segments
    finalLayerOffsetX = ((layer.offsets[0])-((originalWidth - layer.width)/2))                  #x position of the final layer
    finalLayerOffsetY = layer.offsets[1]                                                        #y position of the final layer

    for x in range(1, int(steps) + 1):
        currentAngle = initialAngle + (segmentAngle * x)
        currentLateralDistance = (cylinderDiameter/2) - ((cylinderDiameter / 2) * math.cos(currentAngle))
        width = currentLateralDistance - lastLateralDistance
        lastLateralDistance = currentLateralDistance
        newLayer = pdb.gimp_layer_copy(layer, pdb.gimp_drawable_has_alpha(layer))               #creates a copy of the input layer
        pdb.gimp_image_insert_layer(img, newLayer, None, -1)
        newLayer = pdb.gimp_layer_resize(newLayer, width, layer.height , offset, 0)             #resizes the layer to the calculated width
        offset = offset - width
        newLayer = pdb.gimp_image_get_active_layer(img)
        newLayer = pdb.gimp_layer_scale(newLayer, originalSegmentWidth, layer.height, TRUE)     #scales the layer to the orginal width
        newLayer = pdb.gimp_image_get_active_layer(img)
        newLayer = pdb.gimp_layer_set_offsets(newLayer, (newLayer.width * (x-1)), 0)            #relocates the layer
        newLayer = pdb.gimp_image_get_active_layer(img)
        if x > 1:
            pdb.gimp_image_merge_down(img, newLayer, 0)                                         #merges only the copied layers together (the input layer is needed for refrence)

    newLayer = pdb.gimp_image_get_active_layer(img)
    newLayer = pdb.gimp_layer_translate(newLayer, finalLayerOffsetX, finalLayerOffsetY)         #relocates the final layer
    newLayer = pdb.gimp_image_get_active_layer(img)
    pdb.gimp_image_merge_down(img, newLayer, 0)                                                 #makes the input layer dissapear because it is no longer needed for reference
    
    if originalItemVisible == FALSE:                                                            #restores the layer's original visibility
        pdb.gimp_item_set_visible(pdb.gimp_image_get_active_layer(img), FALSE)
    pdb.gimp_image_undo_group_end(img)

register(
        "distortion_of_cylindrical_projection",
        "Removes the distortions of cylindrical projections.",
        "Removes the distortions that occur when photographing cylinders.",
        "Jakob Guenther",
        "Jakob Guenther",
        "2022",
        "<Image>/Filters/Distorts/Cylindrical Distortion...",
        "*",
        [
            (PF_FLOAT, "cylinderDiameter", "Diameter of the cylinder (px)", 310),   
            (PF_SPINNER, "steps", "Number of steps", 10,(10, 100, 1)),
            
        ],
        [],
         python_distortion_of_cylindrical_projection)
main()
