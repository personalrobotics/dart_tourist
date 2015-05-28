cmake_minimum_required(VERSION 2.8)
project(dart_tourist)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "RELWITHDEBINFO")
endif()

add_definitions(-DPROJECT_NAME=${PROJECT_NAME})

find_package(Boost REQUIRED COMPONENTS python thread)
find_package(DART REQUIRED)
find_package(PythonLibs REQUIRED)

include_directories(
  include
  ${Boost_INCLUDE_DIRS}
  ${DART_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/python.cpp
  src/SkeletonVisitor.cpp
)
target_link_libraries(${PROJECT_NAME}
  ${PROJECT_NAME}
  ${Boost_LIBRARIES}
  ${DART_LIBRARIES}
  ${PYTHON_LIBRARIES}
)
set_target_properties(${PROJECT_NAME} PROPERTIES
  PREFIX ""
  SUFFIX ".so"
)