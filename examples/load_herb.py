import dartpy
import numpy
import time
import dart_tourist
from collections import deque
import json

# Create the environment.
PACKAGE_NAME = 'WAM_URDF'
PACKAGE_PATH = '/home/pmatikai/Projects/herb_description'

ROBOT_PATH \
    = '/home/pmatikai/Projects/herb_description/robots/WAM_URDF.URDF'

urdf_loader = dartpy.DartLoader()
urdf_loader.add_package_directory(PACKAGE_NAME, PACKAGE_PATH)

# Load the robot.
skel = urdf_loader.parse_skeleton(ROBOT_PATH)
robot = skel.get_root_body_node(0)

world = dartpy.World()
tempo = world.add_skeleton(skel)
robot = world.get_skeleton_by_name(tempo)

# builds up a python data structure
class MyVisitor:
    def __init__(self):
        self.data = {}
        self.stack = deque()
        self.stack.append(self.data)

    def append(self, propname, propval):
        self.stack[-1][propname] = propval

    def pose4q3t(self, qx, qy, qz, qw, tx, ty, tz):
        self.append("rot", (qx, qy, qz, qw))
        self.append("trans", (tx, ty, tz))

    def scale3(self, sx, sy, sz):
        self.append("scale", (sx, sy, sz))

    def enter_mesh(self, meshname):
        curthing = {"filename": meshname}
        self.stack[-1]["nmeshes"] += 1
        self.stack[-1]["mesh.{}".format(self.stack[-1]["nmeshes"])] = curthing
        self.stack.append(curthing)

    def enter_body(self, bodyname):
        curthing = {"nmeshes": 0}
        self.stack[-1]["body." + bodyname] = curthing
        self.stack.append(curthing)

    def enter_skeleton(self, skelname):
        curthing = {}
        self.stack[-1]["skeleton." + skelname] = curthing
        self.stack.append(curthing)

    def leave(self):
        self.stack.pop()

    def toJSON(self, pretty=False):
        if not pretty:
            return json.dumps(self.data)
        else:
            return json.dumps(self.data, indent=1)

visitor = MyVisitor()
skelvisitor = dart_tourist.SkeletonVisitor("Skeletor")
skelvisitor.visit_skeleton(robot, visitor)
print(visitor.toJSON(pretty = True))

import time

temp = []
starttime = time.time()
for i in range(1000):
    visitor = MyVisitor()
    skelvisitor.visit_skeleton(robot, visitor)
    temp.append(visitor.toJSON())
endtime = time.time()

# because we do 1000 runs, the time per run in ms is just the total time in s
# (i.e., dt (s) / 1000 (runs) * 1000 (ms/s) = dt (ms/run))
print("Avg. time for serialization: {} ms".format(endtime - starttime))
nbytes = len(temp[0])
print("Serialized size: {} bytes".format(nbytes))
print("Est. bandwidth @30hz: {} kb/s".format(nbytes * 30 / 1000.0))