# dart_tourist
Lets Python visitors traverse the Dart scenegraph (e.g. to link to custom visualizers)

```python
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
```

The above visitor will serialize the skeleton into a plain python structure, which can
then be converted to JSON:
```
{
 "skeleton.WAM_URDF": {
  "body.wam_base": {
   "mesh.1": {
    "filename": "/home/pmatikai/Projects/herb_description/meshes/wam_base.STL"
   }, 
   "nmeshes": 1
  }, 
  "body.wam1": {
   "trans": [
    0.22, 
    0.14, 
    0.346
   ], 
   "rot": [
    0.0, 
    0.0, 
    0.0, 
    1.0
   ], 
   "mesh.1": {
    "filename": "/home/pmatikai/Projects/herb_description/meshes/wam1.STL"
   }, 
   "nmeshes": 1
  }, [...]
```

Performance is reasonably good, for the seven-link WAM urdf (in a virtual machine):
```
Avg. time for serialization: 0.0999028682709 ms
Serialized size: 1597 bytes
Est. bandwidth @30hz: 47.91 kb/s
```
