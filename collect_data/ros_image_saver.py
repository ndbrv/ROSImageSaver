#! /usr/bin/python


# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseWithCovarianceStamped
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
        cv2.imwrite('/home/turtlebot/catkin_ws/src/collect_data/images/camera_image'+str(msg.header.stamp)+'.jpeg', cv2_img)
	with open('/home/turtlebot/catkin_ws/src/collect_data/timestamp.csv','w') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', 				quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow([msg.header.stamp])
	rospy.sleep(1)
	

def pose_callback(msg):
	# Write pose to a csv
	print("Received pose!")
	with open('/home/turtlebot/catkin_ws/src/collect_data/pose.csv','w') as csvfile2:
		spamwriter2 = csv.writer(csvfile2, delimiter=' ', quotechar='|', 				quoting=csv.QUOTE_MINIMAL)
		spamwriter2.writerow([msg.pose.pose.position.x,msg.pose.pose.position.y,msg.pose.pose.position.z])



def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/camera/rgb/image_raw"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, pose_callback)
    # Spin until ctrl + c
    rospy.spin()
    

if __name__ == '__main__':
    main()
