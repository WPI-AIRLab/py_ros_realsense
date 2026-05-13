# Covert raw RealSense `/camera/depth/image_rect_raw` data to Open3D point cloud data
# Run this first: `roslaunch realsense2_camera rs_camera.launch`

import sys
import rospy, tf2_ros
import numpy as np
import transforms3d as t3d

from geometry_msgs.msg import Pose, TransformStamped

class workspace_tf(): ## TF2 version
    def __init__(self):
        self.static_tfs = []
        self.broadcaster = tf2_ros.StaticTransformBroadcaster()
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
        self.hts_fs2world = None ## fingers to world, homogeneous transformation matrices

    def add_static_tf(self, ref, obj, ht):
        static_transformStamped = TransformStamped()

        static_transformStamped.header.stamp = rospy.Time.now()
        static_transformStamped.header.frame_id = ref
        static_transformStamped.child_frame_id = obj

        quat_t3d = t3d.quaternions.mat2quat(ht[:3,:3]) ## t3d returns (w,x,y,z), we need (x,y,z,w)

        static_transformStamped.transform.translation.x = float(ht[0,3])
        static_transformStamped.transform.translation.y = float(ht[1,3])
        static_transformStamped.transform.translation.z = float(ht[2,3])

        static_transformStamped.transform.rotation.x = quat_t3d[1] # quat[0]
        static_transformStamped.transform.rotation.y = quat_t3d[2] # quat[1]
        static_transformStamped.transform.rotation.z = quat_t3d[3] # quat[2]
        static_transformStamped.transform.rotation.w = quat_t3d[0] # quat[3]

        self.static_tfs.append(static_transformStamped)

        self.update()

    def update(self):
        self.broadcaster.sendTransform(self.static_tfs)

    def get_tf(self, ref_frame, obj):
        updated = False
        while updated==False:
          try:
              msg = self.tfBuffer.lookup_transform(ref_frame, obj, rospy.Time())
              trans = [msg.transform.translation.x, msg.transform.translation.y, msg.transform.translation.z]
              quat = [msg.transform.rotation.x, msg.transform.rotation.y, msg.transform.rotation.z, msg.transform.rotation.w]
              ht = np.identity(4)
              ht[:3,:3] = t3d.quaternions.quat2mat([quat[3], quat[0], quat[1], quat[2]])
              ht[:3,3] = trans
              return ht
          except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
              rospy.sleep(0.1)

if __name__ == '__main__':
  rospy.init_node('tf_converter', anonymous=True)
  ws_tf = workspace_tf()
  # rate = rospy.Rate(10)
  while not rospy.is_shutdown():
    ws_tf.get_tf()
    if ws_tf.tf_updated:
      print(ws_tf.trans)
      print(ws_tf.rot)
      print("====")
      # rate.sleep()
    else:
      print("marker not found")
      print("====")