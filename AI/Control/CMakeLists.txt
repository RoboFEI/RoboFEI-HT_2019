# @author Isaac Jesus da Silva - ROBOFEI-HT - FEI
# @version V0.0.3
# @created 04/07/2014
# @Modified 14/07/2016
# 
# Para Help acesse http://www.cmake.org/cmake/help/v2.8.0/cmake.html#command:link_directories

find_package(Boost REQUIRED COMPONENTS program_options)

include_directories(
  include
  ${RoboFEI-HT_SOURCE_DIR}/Blackboard/include
  ${RoboFEI-HT_SOURCE_DIR}/Control/Linux/include
  ${RoboFEI-HT_SOURCE_DIR}/Control/Framework/include
  ${RoboFEI-HT_SOURCE_DIR}/Control/Linux/project/control
)

include_directories(include)
add_library(libcontrol SHARED ./Linux/project/control/main.cpp ./Linux/project/control/kbhit.cpp ./Linux/project/control/ReadConfig.cpp ./Linux/project/control/ActionMove.cpp ./Linux/project/control/GaitMove.cpp)
install(TARGETS libcontrol DESTINATION ${RoboFEI-HT_BINARY_DIR}/lib)

#link_directories(
#  ${RoboFEI-HT_BINARY_DIR}/Blackboard}
#  ${RoboFEI-HT_BINARY_DIR}/Dynamixel}
#)

#MESSAGE(STATUS "CMAKE_SOURCE_DIR:         " ${RoboFEI-HT_SOURCE_DIR})
#MESSAGE(STATUS "CMAKE_BINARY_DIR:         " ${RoboFEI-HT_BINARY_DIR})
#execute_process(COMMAND pwd)

#cria executável
add_executable(control ./Linux/project/control/main.cpp)

#adiciona as dependências
add_dependencies(control libcontrol blackboard)

set(LIB_DARWIN ${RoboFEI-HT_SOURCE_DIR}/Control/Linux/lib/darwin.a)

target_link_libraries(control libcontrol blackboard ${LIB_DARWIN} -Wno-write-strings -lpthread -lrt ${Boost_LIBRARIES})

#install(TARGETS control DESTINATION ${RoboFEI-HT_BINARY_DIR}/bin)
#install(TARGETS control DESTINATION /usr/local/bin)


