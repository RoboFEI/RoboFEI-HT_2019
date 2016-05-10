RoboFEI-HT
=================


This is an early push and is missing major features such as a REST API to expose higher level functions of the framework library. 

All code within project is GPL GNU v3.

Original source code can be found here:  
https://sourceforge.net/projects/darwinop/  
https://github.com/21stCenturyRobot/HROS5-Framework


Notes
==================
* Operating systems supported & verified: Ubuntu 14.04 LTS
* rme (robot motion editor) is an improved version of action_editor developed by 21stCenturyRobot project (http://www.21stcenturyrobot.com/). Additional features such as individual limb on/off torque control implemented (see wiki). Robot MUST be in sitting position and/or spotted when launching rme, as servos go into low-torque mode upon launching rme followed by the robot sitting down. Currently rme is the only way to create motion pages/files.
* Autonomous blob tracking demos/Vision modules from original Darwin-OP framework have been disabled and deleted.


Ubuntu Build Notes
==================
apt-get should have these

Core library dependencies:
build-essential libncurses5-dev libjpeg-dev mplayer mplayer-skins 

PS3/Bluetooth dependencies:
bluez-utils bluez-compat bluez-hcidump libusb-dev libbluetooth-dev joystick


Make Instructions
=================
'make all' in /Linux/build_Framework to compile core framework libraries.

'make clean && make all' in /Linux/build_Framework any time changes are made to core libraries.

demos & utils are found in /Linux/project 'make clean && make all' for all /project programs



