# @author Isaac Jesus da Silva - ROBOFEI-HT - FEI
# @version V0.0.1
# @created 24/08/2015
# @Modified 24/08/2015 
#
# 
# Para Help acesse http://www.cmake.org/cmake/help/v2.8.0/cmake.html#command:link_directories

find_package( Boost REQUIRED )

include_directories(
  include
  ${Boost_INCLUDE_DIRS}
  ../Blackboard/include
  ../IMU/include/um7
  ./serial/include

)

include_directories(include)
add_library(comms SHARED src/comms.cpp)
install(TARGETS comms DESTINATION ${RoboFEI-HT_BINARY_DIR}/lib)
add_library(registers SHARED src/registers.cpp)
install(TARGETS registers DESTINATION ${RoboFEI-HT_BINARY_DIR}/lib)


#MESSAGE(STATUS "CMAKE_SOURCE_DIR:         " ${RoboFEI-HT_SOURCE_DIR})
#MESSAGE(STATUS "CMAKE_BINARY_DIR:         " ${RoboFEI-HT_BINARY_DIR})

add_executable(imu src/imu.cpp src/INIReader.cpp src/ini.c)
add_dependencies(imu 
blackboard serial comms registers ${Boost_LIBRARIES})

target_link_libraries(imu 
blackboard serial comms registers rt pthread ${Boost_LIBRARIES})

#install(TARGETS imu DESTINATION ${RoboFEI-HT_BINARY_DIR}/bin)
#install(TARGETS control DESTINATION /usr/local/bin)


