import numpy
import rotation_matrix
import math
import cv2

RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180

full_image_size = 2048

def texutre_convert(image_directory, start_latitude, vertical_fov):
    img = numpy.zeros((full_image_size/2,full_image_size,3),dtype=numpy.uint8)#cv2.imread(image_directory,0)
    h,w,_ = (100,100,0)
    print w,h
    horizontal_fov = float(w)/float(h)*vertical_fov
    rad_per_pix = horizontal_fov / float(w)
    print rad_per_pix * RAD2DEG
    end_latitude = start_latitude+vertical_fov# not used

    lookAt_vector = numpy.array([1,0,0])#x axis
    horizontal_rotation_axis = numpy.array([0,1,0])#y axis
    vertical_rotation_axis = numpy.array([0,0,1])#z axis

    init_vertical_rotation = rotation_matrix.rotation_matrix_numpy(vertical_rotation_axis, math.pi/2 - start_latitude)
    
    horizontal_rotation_axis = init_vertical_rotation.dot(horizontal_rotation_axis)
    init_horizontal_rotation = rotation_matrix.rotation_matrix_numpy(horizontal_rotation_axis, - horizontal_fov/2.0)

    init_horizontal_rotation_for_vertical_rotation_axis = rotation_matrix.rotation_matrix_numpy(numpy.array([0,1,0]), - horizontal_fov/2.0)
    print - horizontal_fov/2.0 * RAD2DEG
    lookAt_vector = init_horizontal_rotation.dot(init_vertical_rotation.dot(lookAt_vector))

    print vertical_rotation_axis
    vertical_rotation_axis_for_lookAt_vector = vertical_rotation_axis

    print "a"
    print vertical_rotation_axis_for_lookAt_vector
    
    vertical_rotation_matrix_for_lookAt_vector = rotation_matrix.rotation_matrix_numpy(vertical_rotation_axis_for_lookAt_vector,-rad_per_pix)

    vertical_rotation_matrix = rotation_matrix.rotation_matrix_numpy(vertical_rotation_axis,-rad_per_pix)

    for i in xrange(h):#vertical_fov
        print horizontal_rotation_axis
        current_yaw = abs(math.pi/2.0 - (i * rad_per_pix + vertical_fov / 2.0))
        #print current_yaw * RAD2DEG 
        horizontal_rotation_rad = math.acos(1-2*math.cos(current_yaw) *math.cos(current_yaw)*math.sin(rad_per_pix/2.0 )*math.sin(rad_per_pix/2.0 ))
        print horizontal_rotation_rad* RAD2DEG  
        horizontal_rotation_matrix = rotation_matrix.rotation_matrix_numpy(horizontal_rotation_axis, horizontal_rotation_rad)
        lookAt_vector_loop = numpy.copy(lookAt_vector)
        for j in xrange(w):
            #do some thing
            if(abs(lookAt_vector_loop[0]*lookAt_vector_loop[0]+lookAt_vector_loop[1]*lookAt_vector_loop[1]+lookAt_vector_loop[2]*lookAt_vector_loop[2]) - 1.0 > 0.0001):
                print "error"
            lon,lat = xyz2lonlat(lookAt_vector_loop[0],lookAt_vector_loop[1],lookAt_vector_loop[2])
            lon += 180
            lat *= full_image_size/float(360)
            lon *= full_image_size/float(360)
            img[int(lat),int(lon),:] = 255
            
            lookAt_vector_loop = horizontal_rotation_matrix.dot(lookAt_vector_loop)
        print "=========="
        lookAt_vector = vertical_rotation_matrix_for_lookAt_vector.dot(lookAt_vector)
        horizontal_rotation_axis = vertical_rotation_matrix.dot(horizontal_rotation_axis)
    cv2.imwrite("test.jpg",img)


def xyz2lonlat(x,y,z):#y goes up, x goes right, z goes toward you
    projection_length = math.sqrt(x*x + z * z)
    latitude = math.atan2(projection_length,y)
    longtitude = math.atan2(z,x)
    return longtitude*RAD2DEG,latitude*RAD2DEG

# for i in xrange(100):
#   print xyz2lonlat(math.sin(0.0628*i),0,math.cos(0.0628*i))

# for i in xrange(100):
#   print xyz2lonlat(math.sin(0.0628*i),math.cos(0.0628*i),0)
print texutre_convert(None, 45 * DEG2RAD, 90 * DEG2RAD)