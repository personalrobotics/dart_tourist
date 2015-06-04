import dartpy
import numpy
import time
import dart_ws_server

# Create the environment.
PACKAGE_NAME = 'herb_description'
PACKAGE_PATH = '/home/pmatikai/Projects/herb_description'

ROBOT_PATH \
    = '/home/pmatikai/Projects/herb_description/robots/herb.urdf'

urdf_loader = dartpy.DartLoader()
urdf_loader.add_package_directory(PACKAGE_NAME, PACKAGE_PATH)

# Load the robot.
skel = urdf_loader.parse_skeleton(ROBOT_PATH)
robot = skel.get_root_body_node(0)

world = dartpy.World()
tempo = world.add_skeleton(skel)
robot = world.get_skeleton_by_name(tempo)

skelmessage = dart_ws_server.update_skeleton(robot)
print(skelmessage)

# just block on the server
#dart_ws_server.start_server_this_thread()
