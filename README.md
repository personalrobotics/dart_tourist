# dart_tourist
Lets Python visitors traverse the Dart scenegraph (e.g. to link to custom visualizers)

```python
import dart_tourist

# not-quite-correct json syntax but it suffices for demonstration
class MyVisitor:
    def __init__(self):
        self.indent = 0
        self.inmesh = False

    def say(self, msg):
        print(" " * self.indent + msg)

    def pose4q3t(self, qx, qy, qz, qw, tx, ty, tz):
        self.say('"rot": [{},{},{},{}]'.format(qx, qy, qz, qw))
        self.say('"trans": [{},{},{}]'.format(tx, ty, tz))

    def scale3(self, sx, sy, sz):
        self.say('"scale": [{},{},{}]'.format(sx, sy, sz))

    def enter_mesh(self, meshname):
        self.say('"mesh":"{}"'.format(meshname))
        self.inmesh = True

    def enter_body(self, bodyname):
        self.say('"body.{}":{{'.format(bodyname))
        self.indent += 4

    def enter_skeleton(self, skelname):
        self.say('"skeleton.{}":{{'.format(skelname))
        self.indent += 4

    def leave(self):
        if not self.inmesh:
            self.indent -= 4
            self.say("}")
        else:
            self.inmesh = False

#load in your robot into 'robot'

skelvisitor = dart_tourist.SkeletonVisitor("Skeletor")
skelvisitor.visit_skeleton(robot, MyVisitor())
```

Will produce (for example) this type of not-quite-correct json output:
```
"skeleton.WAM_URDF":{
    "body.wam_base":{
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam_base.STL"
    }
    "body.wam1":{
        "rot": [0.0,0.0,0.0,1.0]
        "trans": [0.22,0.14,0.346]
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam1.STL"
    }
    "body.wam2":{
        "rot": [-0.707108079859,0.0,0.0,0.707105482511]
        "trans": [0.22,0.14,0.346]
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam2.STL"
    }
    "body.wam3":{
        "rot": [0.0,0.0,0.0,1.0]
        "trans": [0.22,0.14,0.346]
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam3.STL"
    }
    "body.wam4":{
        "rot": [-0.707108079859,0.0,0.0,0.707105482511]
        "trans": [0.265,0.14,0.896]
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam4.STL"
    }
    "body.wam5":{
        "rot": [0.0,0.0,0.0,1.0]
        "trans": [0.22,0.14,0.896]
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam5.STL"
    }
    "body.wam6":{
        "rot": [-0.707108079859,0.0,0.0,0.707105482511]
        "trans": [0.22,0.14,1.196]
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam6.STL"
    }
    "body.wam7":{
        "rot": [0.0,0.0,0.0,1.0]
        "trans": [0.22,0.14,1.196]
        "mesh":"/home/pmatikai/Projects/herb_description/meshes/wam7.STL"
    }
}
```
