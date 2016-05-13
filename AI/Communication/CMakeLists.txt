#inclui o caminho para os headers (*.h) usando a variável de ambiente (e.g.: ${RoboFEI-HT_SOURCE_DIR})  
include_directories(
  include
  #${RoboFEI-HT_SOURCE_DIR}/Control/Framework/include
  ${RoboFEI-HT_SOURCE_DIR}/Blackboard/include
  ${RoboFEI-HT_SOURCE_DIR}/Blackboard/src
  #${RoboFEI-HT_SOURCE_DIR}/Dynamixel/include
)

#link_directories(
#  ${RoboFEI-HT_BINARY_DIR}/Blackboard}
#)

#MESSAGE(STATUS "CMAKE_SOURCE_DIR:         " ${RoboFEI-HT_SOURCE_DIR})
#MESSAGE(STATUS "CMAKE_BINARY_DIR:         " ${RoboFEI-HT_BINARY_DIR})
#MESSAGE(STATUS "CMAKE_BINARY_DIR:         " ${CMAKE_BINARY_DIR})

#cria executável
add_executable(communication
   src/communication.cpp
   src/INIReader.cpp
   src/ini.c
   src/libUDPclient.cpp
   src/LinuxNetwork.cpp
   include/RoboCupGameControlData.h)

#adiciona as dependências = e.g. communication depende do blackboard
add_dependencies(communication blackboard)

#set(LIB_DARWIN ${RoboFEI-HT_SOURCE_DIR}/Control/Linux/lib/darwin.a)

#adiciona o link para a biblioteca criada blackboard
target_link_libraries(communication
  blackboard pthread
)
#indica caminho para instalação 
#install(TARGETS communication DESTINATION ${RoboFEI-HT_BINARY_DIR}/bin)
#install(TARGETS communication DESTINATION /usr/local/bin)


