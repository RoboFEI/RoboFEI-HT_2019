include_directories(
  include
  ${PROJECT_SOURCE_DIR}/Blackboard/include
  ${PROJECT_SOURCE_DIR}/Control/Framework/include
)

set(LIB_DARWIN ${RoboFEI-HT_SOURCE_DIR}/Control/Linux/lib/darwin.a)
add_executable(Odometry ${RoboFEI-HT_SOURCE_DIR}/Odometry/Odometry.cpp)

target_link_libraries(Odometry blackboard ${LIB_DARWIN} -Wno-write-strings -lpthread -lrt ${Boost_LIBRARIES})




