include_directories(
  include
  ${PROJECT_SOURCE_DIR}/Blackboard/include
  ${PROJECT_SOURCE_DIR}/Control/Framework/include
)

set(LIB_DARWIN ${RoboFEI-HT_SOURCE_DIR}/Control/Linux/lib/darwin.a)
add_executable(Odometria ${RoboFEI-HT_SOURCE_DIR}/Odometria/Odometria.cpp)

target_link_libraries(Odometria blackboard ${LIB_DARWIN} -Wno-write-strings -lpthread -lrt ${Boost_LIBRARIES})




