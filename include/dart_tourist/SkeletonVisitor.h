#ifndef DART_TOURIST_SKELETONVISITOR_H_
#define DART_TOURIST_SKELETONVISITOR_H_

#include <dart/dynamics/dynamics.h>
#include <boost/python.hpp>

namespace dart {
namespace tourist {

using dart::dynamics::SkeletonPtr;

class Visitor {
public:
	virtual void pose4q3t(float qx, float qy, float qz, float qw,
						  float tx, float ty, float tz) = 0;
	virtual void scale3(float sx, float sy, float sz) = 0;
	virtual void filename(const std::string& filename) = 0;
	virtual void enter(const std::string& btype, const std::string& bname) = 0;
	virtual void leave(const std::string& btype) = 0;
};

class PyVisitor : public Visitor {
public:
	boost::python::object& target_;

	PyVisitor(boost::python::object& target) 
		: target_(target) { 
	}

	void pose4q3t(float qx, float qy, float qz, float qw,
						  float tx, float ty, float tz) {
		target_.attr("pose4q3t")(qx, qy, qz, qw, tx, ty, tz);
	}

	void scale3(float sx, float sy, float sz) {
		target_.attr("scale3")(sx, sy, sz);
	}

	void filename(const std::string& filename) {
		target_.attr("filename")(filename);
	}

	void enter(const std::string& btype, const std::string& bname) {
		target_.attr("enter")(btype, bname);
	}

	void leave(const std::string& btype) {
		target_.attr("leave")(btype);
	}
};

class SkeletonVisitor {
public:
  SkeletonVisitor(std::string const &arg);

  void visitSkeleton(SkeletonPtr const &skeleton, 
                      Visitor* visitor);

private:
  // nothing goes in here
};

} // namespace tourist
} // namespace dart

#endif
