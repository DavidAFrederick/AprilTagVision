# USAGE
# python detect_apriltag.py --image images/example_01.png


# Source:
# https://www.youtube.com/watch?v=H77ieFq5mQ8
# https://pyimagesearch.com/pyimagesearch-university/#collapse6
# https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/


# import the necessary packages
import apriltag
import cv2
import math
from gpiozero import AngularServo, LED
from datetime import datetime
from time import sleep

# Constants for pin assignments
SERVO_PIN = 2
LED_PIN   = 3

class AprilTagTracker():

    def __init__(self, display_image : bool):
        # Configure
        self.servo = AngularServo(SERVO_PIN, min_pulse_width=0.0006, max_pulse_width=0.0023)
        self.green_led = LED(LED_PIN, active_high=False)

        self.cap = cv2.VideoCapture(0)
        ret, self.image = self.cap.read()
        self.display_image = display_image


    def scan_for_apriltag(self) -> float:

        while self.cap.isOpened():
            ret, image = self.cap.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # define the AprilTags detector options and then detect the AprilTags in the input image
            options = apriltag.DetectorOptions(families="tag36h11")
            detector = apriltag.Detector(options)
            results = detector.detect(gray)

            self.green_led.off()  # The LED indicates if an Apriltag is being tracked
            offset_angle_in_degrees = 0

            for result in results:

                if result:
                    self.green_led.on()
                    # print("AprilTag(s) detected!")

                (ptA, ptB, ptC, ptD) = result.corners
                ptB = (int(ptB[0]), int(ptB[1]))
                ptC = (int(ptC[0]), int(ptC[1]))
                ptD = (int(ptD[0]), int(ptD[1]))
                ptA = (int(ptA[0]), int(ptA[1]))

                top_size_in_pixels = ptB[0]-ptA[0]
                # side_size_in_pixels = ptC[1]-ptB[1]

                # print (f"Top size  = {top_size_in_pixels}")
                # print (f"Size size = {side_size_in_pixels}")

                # draw the bounding box of the AprilTag detection   (BGR)
                cv2.line(image, ptA, ptB, (0, 255, 0), 2)      #  Green   Top of April Tag
                cv2.line(image, ptB, ptC, (255, 0, 0), 2)      #  Blue    Right side
                cv2.line(image, ptC, ptD, (0, 0, 255), 2)      #  Red     Bottom
                cv2.line(image, ptD, ptA, (255, 255, 255), 2)  #  white   Left

                # # draw the center (x, y)-coordinates of the AprilTag
                (cX, cY) = (int(result.center[0]), int(result.center[1]))
                cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)    # Draw a dot in the center

                # center_of_apriltag = cX
                # print (f" Center of April Tag: (cX, cY)  {(cX, cY)}")

                center_of_image_x_pixels = image.shape[1]/2
                # center_of_image_y_pixels = image.shape[0]/2
                
                # print (f"Center: X pixels off Horizonal center (+left) {center_of_image_x_pixels - cX}")
                # print (f"Center: Y pixels off Vertical center (+Above) {center_of_image_y_pixels - cY}")

                # "Distance to target in inches" = ("size in inches of known side" x "Focal Length")/ "Number of pixels on known size" 
                # D' = 7006 / Pixels
                size_of_top_edge_in_pixels = ptB[0]-ptA[0]
                distance_to_target_in_inches = (7006/size_of_top_edge_in_pixels)  
                distance_to_target_in_feet = distance_to_target_in_inches/12   # Divide by  12 to get feet

                #  Angle off center
                #  Tangent(offset_angle) = Opposite side / Adjancent side
                #  offset_angle_in_radians = arc-tangent (0.5 * AprilTag Width)/ distance_to_target_in_inches

                # Use the fixed width of the apriltag as a reference (6.25 inches top_size_in_pixels)
                horizonal_inches_per_pixel = 6.25 / top_size_in_pixels
                center_of_apriltag_offset_in_pixels = center_of_image_x_pixels - cX
                center_of_apriltag_offset_in_inches = center_of_apriltag_offset_in_pixels * horizonal_inches_per_pixel
                
                offset_angle_in_radians = math.atan(center_of_apriltag_offset_in_inches/distance_to_target_in_inches)
                offset_angle_in_degrees = math.degrees(offset_angle_in_radians)

                # Draw lines on the  screen  Shape of image: (800, 1280)  height, width
                IMAGE_WIDTH = 1280
                IMAGE_HEIGHT = 800
                half_width = int(IMAGE_WIDTH/2)
                half_height = int(IMAGE_HEIGHT/2)

                cv2.line(image, (0, half_height), (IMAGE_WIDTH, half_height), (255, 255, 255), 2)    #BGR      Horizonal line across center
                cv2.line(image, (half_width,0), (half_width,IMAGE_HEIGHT), (255, 255, 255), 2)    #BGR      Vertical line across center

                # draw the tag family on the image
                tagFamily = result.tag_family.decode("utf-8")
                tagId = "TagId: " + str(result.tag_id)  
                distanceText = "Distance: " + str(f"{distance_to_target_in_feet:.2f}") 
                offsetAngleText = "Angle: " + str(f"{offset_angle_in_degrees:.3f}")

                # Write to the image
                cv2.putText(image, tagId, (ptA[0], ptA[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, distanceText, (ptA[0], ptA[1] - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  #BGR colors
                cv2.putText(image, offsetAngleText, (ptA[0], ptA[1] - 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  #BGR colors
                
                # Adjust for direction and physical mis-alignment
                offset_angle_in_degrees = 0 - offset_angle_in_degrees + 8

                # print (f"offset_angle_in_degrees: {int(offset_angle_in_degrees)}")

                # Set the servo to the angle
                self.servo.angle = int(offset_angle_in_degrees)

            # current_time = datetime.now()
            # print(f"current_time: {current_time}")
            # print(current_time.strftime("%M:%S"))

            if (self.display_image):

                # show the output image after AprilTag detection
                cv2.imshow("Image", image)

            return offset_angle_in_degrees

    def cleanup(self):
        cv2.destroyAllWindows()
        self.cap.release()


#===(Main program)=====================================================

apriltagtracker = AprilTagTracker(True)

while (True):

    apriltagtracker.scan_for_apriltag()

    if cv2.waitKey(1) == 27:
        break

#======================================================================


#####################################################

# Printed Apriltag is 6.25  inches wide and tall

# Measured data
# Distance  Top dim in pixels   Side dim in pixels
# 18"   372     290
# 24"   280     290
# 48"   144     150
# 96"   73      73
# 120"  59      59
# 144"  48      48
# 168"  42      42
# 192"  37      37
# 216"  32      32
# 264"  28      28


# F = (P x D) / W

# Focal length = (Pixel x distance / width)
# [24"]     285 x 24 / 6.25  = 1094
# [48"]     148  x 48 / 6.25 = 1136
# [96"]     73  x 96 / 6.25  = 1121
# [120"]    59  x 120 /6.25  = 1132  

# "Distance to target in inches" = ("size in inches of known side" x "Focal Length")/ "Number of pixels on known size" 
# D’ = (W x F) / P   =  6.25 x 1121 / P
# D' = 7006 / Pixels


