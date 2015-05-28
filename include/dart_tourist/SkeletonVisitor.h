#ifndef DART_TOURIST_SKELETONVISITOR_H_
#define DART_TOURIST_SKELETONVISITOR_H_

#include <dart/dynamics/dynamics.h>
#include <boost/python.hpp>

namespace dart {
namespace tourist {

using dart::dynamics::SkeletonPtr;

class SkeletonVisitor {
public:
  SkeletonVisitor(std::string const &arg);

  void visitSkeleton(SkeletonPtr const &skeleton, 
                      boost::python::object visitor);

private:
  // nothing goes in here
};

} // namespace tourist
} // namespace dart

#endif
