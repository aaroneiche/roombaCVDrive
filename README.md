# roombaCVDrive
An app I developed for MakerFaire that let you drive a Roomba by positioning tennis or raquetballs

### Requirements
* Relies on the Python Roomba Library (https://github.com/jflesch/PyRoomba)
* Built with OpenCV 3.1.0, may work with older versions

### Use
Get upper and lower boundaries for the color that you want to track. Place those in ```lower``` and ```upper``` on line 34/35
Then ```python colortrack.py``` should startup, initialize the connection, and you're good to go.

Keeping the balls placed in the "stop zone" will prevent the Roomba from driving around. Moving the balls above the box will
result in the Roomba driving forward. Moving the balls below the box will result in the Roomba driving backwards. 
Differences in height will result in differential driving.

