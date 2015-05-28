import dartpy
import numpy
import time
import dart_tourist

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

# not-quite-correct json syntax but it suffices for demonstration
class MyVisitor:
    def __init__(self):
        self.indent = 0
        self.inmesh = False
        self.curskels = 0
        self.curbodies = 0
        self.curattributes = 0
        self.message = ""

    def newline(self, addcomma = False):
        if addcomma:
            self.message += ",\n"
        else:
            self.message += "\n"

    def append(self, msg):
        self.message += (" " * self.indent + msg)

    def pose4q3t(self, qx, qy, qz, qw, tx, ty, tz):
        self.newline(self.curattributes > 0)
        self.append('"rot": [{},{},{},{}],\n'.format(qx, qy, qz, qw))
        self.append('"trans": [{},{},{}]'.format(tx, ty, tz))
        self.curattributes += 1

    def scale3(self, sx, sy, sz):
        self.newline(self.curattributes > 0)
        self.append('"scale": [{},{},{}]'.format(sx, sy, sz))
        self.curattributes += 1

    def enter_mesh(self, meshname):
        self.newline(self.curattributes > 0)
        self.append('"mesh":"{}"'.format(meshname))
        self.inmesh = True
        self.curattributes += 1

    def enter_body(self, bodyname):
        self.newline(self.curbodies > 0)
        self.append('"body.{}":{{'.format(bodyname))
        self.indent += 4
        self.curattributes = 0
        self.curbodies += 1

    def enter_skeleton(self, skelname):
        self.append('"skeleton.{}":{{'.format(skelname))
        self.indent += 4
        self.curbodies = 0

    def leave(self):
        if not self.inmesh:
            self.newline(False)
            self.indent -= 4
            self.append("}")
        else:
            self.inmesh = False
        if self.indent <= 0:
            print(self.message)

skelvisitor = dart_tourist.SkeletonVisitor("Skeletor")
skelvisitor.visit_skeleton(robot, MyVisitor())