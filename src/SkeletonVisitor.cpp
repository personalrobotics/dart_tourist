#include <dart_tourist/SkeletonVisitor.h>
#include <boost/python.hpp>

using dart::tourist::SkeletonVisitor;

using dart::dynamics::Skeleton;
using dart::dynamics::SkeletonPtr;
using dart::dynamics::BodyNode;
using dart::dynamics::ConstShapePtr;

using dart::dynamics::Shape;
using dart::dynamics::BoxShape;
using dart::dynamics::CylinderShape;
using dart::dynamics::EllipsoidShape;
using dart::dynamics::LineSegmentShape;
using dart::dynamics::MeshShape;
using dart::dynamics::PlaneShape;
using dart::dynamics::SoftMeshShape;

SkeletonVisitor::SkeletonVisitor(const std::string &arg)
{
  // nothing to do
}

// checks if the given rotation+translation pair is
// EXACTLY the identity transformation
bool isIdentity(Eigen::Quaterniond const &q, Eigen::Vector3d const &t)
{
  // floating point comparisons are justified here since these should be
  // exact values if this transformation is truly the identity
  return q.x() == 0.0 && q.y() == 0.0 && q.z() == 0.0 && q.w() == 1.0 &&
          t[0] == 0.0 && t[1] == 0.0 && t[2] == 0.0;
}

// checks if the given scaling is EXACTLY unit scaling
bool isUnitScaling(Eigen::Vector3d const &s) {
  return s[0] == 1.0 && s[1] == 1.0 && s[2] == 1.0;
}

void visitPose(Eigen::Isometry3d const &transform, boost::python::object &visitor) 
{
  Eigen::Quaterniond const q(transform.rotation());
  Eigen::Vector3d const t(transform.translation());

  if(!isIdentity(q, t)) {
    visitor.attr("pose4q3t")(q.x(), q.y(), q.z(), q.w(),
                             t[0], t[1], t[2]);
  }
}

void visitScale(Eigen::Vector3d const &s, boost::python::object &visitor)
{
  if(!isUnitScaling(s)) {
    visitor.attr("scale3")(s[0], s[1], s[2]);
  }
}

void visitMesh(MeshShape const &mesh, boost::python::object &visitor)
{
  std::string const &scenePath = mesh.getMeshPath();
  visitor.attr("enter_mesh")(scenePath);

  visitPose(mesh.getLocalTransform(), visitor);
  visitScale(mesh.getScale(), visitor);

  visitor.attr("leave")(); // leave mesh
}

void visitShape(Shape const &shape, boost::python::object &visitor)
{
  switch (shape.getShapeType()) {
  case Shape::BOX:
  case Shape::ELLIPSOID:
  case Shape::CYLINDER:
  case Shape::PLANE:
    //visitPrimitive(shape, visitor); //TODO
    break;

  case Shape::SOFT_MESH:
  case Shape::LINE_SEGMENT:
    // TODO
    break;

  case Shape::MESH:
    visitMesh(dynamic_cast<MeshShape const &>(shape), visitor);
  }
}

void SkeletonVisitor::visitSkeleton(SkeletonPtr const &skeleton, 
                                  boost::python::object visitor)
{
  // indicate that a skeleton has happened
  visitor.attr("enter_skeleton")(skeleton->getName());

  for (BodyNode *const bodyNode : skeleton->getBodyNodes()) {
    // indicate that a new body has happened
    visitor.attr("enter_body")(bodyNode->getName());

    // body pose
    Eigen::Isometry3d const &Tworld_bodynode = bodyNode->getWorldTransform();
    visitPose(Tworld_bodynode, visitor);

    // all the things that have been attached
    for (size_t i = 0; i < bodyNode->getNumVisualizationShapes(); ++i) {
      ConstShapePtr const shape = bodyNode->getVisualizationShape(i);
      visitShape(*shape, visitor);
    }

    // leave body
    visitor.attr("leave")();
  }

  // leave skeleton
  visitor.attr("leave")();
}
