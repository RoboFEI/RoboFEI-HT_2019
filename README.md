# RoboFEI-HT: Artificial Intelligence and Simulator

## AI: Artificial Intelligence for Humanoid Robots

AI is built upon the Cross Architecture (Perico et. al, 2014; Perico et al., 2015).

### Setup

1. compile the code of the robot running *./setup.sh*

2. run *./start.sh* for running the simulator and the AI

###References

D. H. Perico et al., "Hardware and Software Aspects of the Design and Assembly of a New Humanoid Robot for RoboCup Soccer," Robotics: SBR-LARS Robotics Symposium and Robocontrol (SBR LARS Robocontrol), 2014 Joint Conference on, Sao Carlos, 2014, pp. 73-78.
doi: 10.1109/SBR.LARS.Robocontrol.2014.39

D. H. Perico et al., "Newton: A High Level Control Humanoid Robot for the RoboCup Soccer KidSize League". Robotics: Joint Conference on Robotics, LARS 2014, SBR 2014, Robocontrol 2014, Sao Carlos, Brazil, October 18-23, 2014. Revised Selected Papers. Springer Berlin Heidelberg, 2015.
doi: 10.1007/978-3-662-48134-9_4


## Simulator

RoboFEI-HT simulator used for developing AI (decision, localization, planning etc)

### Changing objects' positions

**Robots:** It is possible to change the position of the robots by pressing the number of the robot + *INSERT*. Example: if I want to change robot 1 position I will press *1* followed by *INSERT*. The robot will be moved following the mouse pointer position. The orientation will be random.

**Ball:** It is possible to change the position of the ball by pressing *b*.The ball will be moved following the mouse pointer position. 

### Simulator Help

**F1:** opens a help with all the possible commands in the simulator. 

## OS and dependencies for AI and Simulator

This program was tested in Ubuntu 14.04 LTS 64 bits

* Main Dependencies:
    * cmake
    * g++
    * python 2.7 
    * python-pygame
    * python-numpy
    * python-opencv
    
## License

GNU GENERAL PUBLIC LICENSE.
Version 3, 29 June 2007
   
