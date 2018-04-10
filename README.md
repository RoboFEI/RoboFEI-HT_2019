[![Build Status](https://travis-ci.com/thiagohomem/RoboFEI-HT_Debug.svg?token=BM6ZpSsKHNz3RkbM8yxT&branch=master)](https://travis-ci.com/thiagohomem/RoboFEI-HT_Debug)
#RoboFEI-HT: Artificial Intelligence and Simulator

## AI: Artificial Intelligence for Humanoid Robots

AI is built upon the Cross Architecture \[[1]] \[[2]]. Some methods used for the Vision System can be found in \[[3]] and \[[4]]. A Control technique applied to improve the robot's stability can be found in \[[5]]. A qualitative localization studied for the robot can be found in \[[6]].

[1]: http://dx.doi.org/10.1109/SBR.LARS.Robocontrol.2014.39
[2]: http://dx.doi.org/10.1007/978-3-662-48134-9_4
[3]: http://dx.doi.org/10.1109/SBR.LARS.Robocontrol.2014.51
[4]: http://dx.doi.org/10.1109/LARS-SBR.2015.43
[5]: http://dx.doi.org/10.1109/LARS-SBR.2015.41
[6]: http://dx.doi.org/10.1109/LARS-SBR.2015.44


### Setup

1. compile the code of the robot running *./setup.sh*

## Simulator

RoboFEI-HT simulator used for developing AI (decision, localization, planning etc).

### Setup

1. Once the AI is compiled, run *./start_simulator.sh* for running the simulator and the AI

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
    * screen
    
## License

GNU GENERAL PUBLIC LICENSE.
Version 3, 29 June 2007
   
