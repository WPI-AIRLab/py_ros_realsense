- Need to setup:
	- RealSense (pyrealsense2)
	- OpenCV
	- ROS

- To run the node, use `roslaunch py_ros_realsense realsense.launch`
	- The serial number of the RealSense is in the launch file.
	- The color images are published to `/CAM_ALIAS/color/raw` (change the camera name in the launch file if needed).
	- The camera intrinsic is published to `/CAM_ALIAS/color/camera_info`. For a RealSense camera, the intrinsic stays the same all the time.
	- The depth information are published to `/CAM_ALIAS/depth/raw`
    - The color point cloud is published to `/CAM_ALIAS/depth/color/points`

- The color point cloud is transformed by the cameras' extrinsic. To reload the extrinsic, call `rosservice call /CAM_ALIAS/reload_ht`
- The ht is a pickle file, direction is given by the launch file, ht.data[0] is a 4x4 numpy matrix.

- For connect to RealSense, publish image to YOUR_CAMERA_NAME/color/raw and depth to YOUR_CAMERA_NAME/depth/raw.
	- To start recording, use `rosservice call /front_cam/start_recording "PATH_TO_SAVE"`
	- To stop recording, use `rosservice call /front_cam/stop_recording`

- To test, run `subscribe_to_topic.py` or `get_single_image.py`. The image is published to `/py_ros_realsense_test/debug`.