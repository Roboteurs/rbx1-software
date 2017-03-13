# RXB1 Software

[![N|Roboteurs](https://cdn.shopify.com/s/files/1/0742/2899/files/logosmall.png?575371702457707276
)](https://www.roboteurs.com)

The RXB1 is a 6 axis remix of the famous Thor robot. This robot can be driven by a number of diffrent method. Using the SlushEngine this robot can be driven with a purley Python implementation. This makes it simple to understand how the robot is working and makes it easy for enginnergs and students to make changes to.
*It should be noted that at the moment this software is still under a lot of development. It is working but the software will undergo a lot of changes. 
# Installation
To install this software all you need to do is clone the directory somewhere. This software does require the Slush library and Inputs
```sh
$ sudo pip3 install Inputs
```
# Usage
To use this code to drive your robot just go into the working directory and run robot.py. Make sure you have a joystick connected or you can do nothing
```sh
$ cd rbx1-software
$ python3 robot.py
```
Now you are up and running. If you move the connected joystick you will see movment in the robot. For more info on using the software check out the wiki.
# How does it work?
Good question. Its actually pretty straight forward really. The Python program reads the commands comming from the joystick and translates them into motions in the robot. If you want to save a point then robot.py saves your point to the points file located in examples. If you want to run a program the robot will execute the instructions that it finds in the run.rbt file. 







