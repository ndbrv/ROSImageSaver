#! /usr/bin/python


# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseWithCovariance
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import csv

# Instantiate CvBridge
bridge = CvBridge()

def image_callback(msg):
    print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
	
    except CvBridgeError, e:
        print(e)
    else:
        # Save your OpenCV2 image as a jpeg and write timestamp to a csv
        cv2.imwrite('/home/nikola/catkin_ws/src/images/scamera_image.jpeg', cv2_img)
	with open('timestamp.csv','w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter='', quotechar='|', 				quoting=csv.QUOTE_MINIMAL)
	spamwriter.writerow([rospy.get_rostime()])

def pose_callback(msg):
	# Write pose to a csv
	print("Received pose!")
	with open('pose.csv','w',newline='') as csvfile:
		spamwriter2 = csv.writer(csvfile, delimiter='', quotechar='|', 				quoting=csv.QUOTE_MINIMAL)
	spamwriter2.writerow([msg.pose])



def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/cameras/left_hand_camera/image"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    rospy.Subscriber("amcl_pose", PoseWithCovariance, pose_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
