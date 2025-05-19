# USAGE
# python detect_apriltag.py --image images/example_01.png


# Source:
# https://www.youtube.com/watch?v=H77ieFq5mQ8
# https://pyimagesearch.com/pyimagesearch-university/#collapse6
#


# import the necessary packages
import apriltag
import cv2

# Open the default camera and read a frame
cap = cv2.VideoCapture(0)
ret, image = cap.read()

while cap.isOpened():
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # define the AprilTags detector options and then detect the AprilTags
    # in the input image
    # print("[INFO] detecting AprilTags...")
    options = apriltag.DetectorOptions(families="tag36h11")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    # print("[INFO] {} total AprilTags detected".format(len(results)))

    # print ("R-Corners - start")
    # print (results)
    # print ("R-Corners - finish")


    # [Detection(
    # tag_family=b'tag36h11', 
    # tag_id=1, 
    # hamming=0, 
    # goodness=0.0, 
    # decision_margin=77.4981460571289, 
    # homography=array([[....
    # center=array
    # corners=array


    # R-Corners - start
    # [Detection(tag_family=b'tag36h11', tag_id=1, hamming=0, goodness=0.0, decision_margin=77.4981460571289, homography=array([[7.36251490e-01, 1.25833013e-02, 3.82244883e+00],
    #        [4.03004178e-02, 7.29073136e-01, 2.20236602e+00],
    #        [5.23751296e-05, 6.10447550e-05, 6.42792651e-03]]), center=array([594.6628087 , 342.62464256]), corners=array([[486.75442505, 226.93656921],
    #        [708.19989014, 235.78948975],
    #        [698.8291626 , 454.30090332],
    #        [481.43157959, 449.17199707]])), Detection(tag_family=b'tag36h11', tag_id=2, hamming=0, goodness=0.0, decision_margin=81.79723358154297, homography=array([[ 7.14202474e-01, -4.04466983e-02,  1.82137701e+00],
    #        [ 5.46583129e-02,  6.96562360e-01,  2.13834269e+00],
    #        [ 8.55505546e-05, -7.88730289e-05,  6.48407655e-03]]), center=array([280.8999855 , 329.78368937]), corners=array([[177.17315674, 214.14799499],
    #        [387.45974731, 225.07913208],
    #        [384.41339111, 445.18145752],
    #        [168.7953186 , 439.93661499]]))]
    # R-Corners - finish

    # Top Left corner  = Pt A
    # Top Right corner = Pt B
    # Bottom Right coner = Pt C
    # Bottom Left corner = Pt D

    # loop over the AprilTag detection results
    for r in results:

        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))

        # print ("ptA: ", ptA)
        # print ("ptB: ", ptB)
        # print ("ptC: ", ptC)
        # print ("ptD: ", ptD)

        print (f"Top size = {ptB[0]-ptA[0]}")
        print (f"Size size = {ptC[1]-ptB[1]}")



        # draw the bounding box of the AprilTag detection   (BGR)
        cv2.line(image, ptA, ptB, (0, 255, 0), 2)      #  Green   Top of April Tag
        cv2.line(image, ptB, ptC, (255, 0, 0), 2)      #  Blue    Right side
        cv2.line(image, ptC, ptD, (0, 0, 255), 2)      #  Red     Bottom
        cv2.line(image, ptD, ptA, (255, 255, 255), 2)  #  white   Left

        # # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        print (f"Shape of image: {gray.shape} ")
        print (f"(cX, cY)  {(cX, cY)}")

        # cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

        print (f"image shape {image.shape}")
        print (f"Center: X pixels off Horizonal center (+left) {image.shape[1]/2-cX}")
        print (f"Center: Y pixels off Vertical center (+Above) {image.shape[0]/2-cY}")


        # draw the tag family on the image
        tagFamily = r.tag_family.decode("utf-8")
        tagId = str(r.tag_id)
        cv2.putText(image, tagId, (ptA[0], ptA[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        

        # Shape of image: (800, 1280)   height, width
        #  Distance:
        #  We know the distance between the top two corners of the physical target
        #  We can measure the viewed number of pixles
        

    # show the output image after AprilTag detection
    cv2.imshow("Image", image)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()




# Printed Apriltag is 6.25  inches wide and tall

# Measured data
# Distance  Top dim in pixels   Side dim in pixels
# 18"   372     290
# 24"   280     290
# 48"   97      97
# 96"   73      73
# 120"  59      59
# 144"  48      48
# 168"  42      42
# 192"  37      37
# 216"  32      32
# 264"  28      28

