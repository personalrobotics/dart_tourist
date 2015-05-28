#include <boost/python.hpp>
#include <dart_tourist/SkeletonVisitor.h>

BOOST_PYTHON_MODULE(PROJECT_NAME)
{
  using namespace boost::python;

  using boost::noncopyable;
  using dart::tourist::SkeletonVisitor;

  class_<SkeletonVisitor, noncopyable>("SkeletonVisitor",
     init<std::string const &>())
    .def("visit_skeleton", &SkeletonVisitor::visitSkeleton)
    ;
}
