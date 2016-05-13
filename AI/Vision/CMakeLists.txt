#include_directories(${RobotFEI-HT_SOURCE_DIR}/Blackboard/include)

#inclui o caminho para os headers (*.h) usando a variável de ambiente (e.g.: ${RoboFEI-HT_SOURCE_DIR})  
include_directories(
	include
	./Dynamixel/include
	${RoboFEI-HT_SOURCE_DIR}/Blackboard/include
)

#adiciona as dependências = e.g. vision depende do blackboard
#add_dependencies(libvision blackboard)

add_library(vision SHARED ./src/vision.cpp ./Dynamixel/src/dxl_hal.c ./Dynamixel/src/dynamixel.c)
install(TARGETS vision DESTINATION ${RoboFEI-HT_BINARY_DIR}/lib)
#install(TARGETS blackboard DESTINATION /usr/local/lib)
#add_dependencies(blackboard blackboard)
#target_link_libraries(blackboard blackboard -fPIC)
#install(TARGETS blackboard DESTINATION ${RoboFEI-HT_BINARY_DIR}/lib)

