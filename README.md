# TMUHyperloop
Code repository for TMU Hyperloop GNC systems

GUI Contributors:
- Alishba Aamir @ 2024-2025/GUI/WorkingGUI.py
- Syed Ka Ab Surkhi @2024-2025/GUI/betterGUI.py

Contributors:
- Andy Lin
- Matthew Trieu
- Alex Meng
- Brian Xu
- Leo Lin

## SETUP
1. Turn on RPI power, RPI should connect to network automatically
2. Connect control station laptop to network
3. Run control station main program
4. Send start command when ready

## Code Explanation
Last updated July 30, 2024

#### Control Laptop Code:
test1.py (TMUHYPERLOOP/2023-2024/GUI/test1.py) is the main control station code. It incorporates the GUI, its update function, and the connection to the RPI in one program. (Very bad I know)
At the very top, there are the import functions. Below that are global variables that need to be initialized. Currently, the exclamation mark ! tells the RPI that the connection is still active, and it prefaces all commands.
The dataReadEvent indicates when data has been received from the RPI. When this is set, the update_values(self) function will run. This function reads from a data storage file and updates the GUI accordingly.

The HyperloopControlGUI class defines the GUI and its functions. the \_\_init\_\_ function defines the layout and appearance of the GUI. As of the last update, the GUI contains mostly redundant displays. Most of it is non-functional.
The other functions below define the functionality of the GUI. Below is an example of how to link a function to a button defined in the \_\_init\_\_ function:

    In the \_\_init\_\_ function:
        button_layout = QHBoxLayout()
        self.launch_button = QPushButton("Launch")
        button_layout.addWidget(self.launch_button)
        self.launch_button.clicked.connect(self.launch_train)

    Where the launch_train function is defined as:
        def launch_train(self):
            # Send Launch Command
            global COMOUT
            COMOUT = COMOUT + " G"
            print("Launch")

Before starting, the HOST variable in the main function at the very bottom (under if \_\_name\_\_ == 'main': header) must be set to the IP address of the control laptop. It will act as the server to which
the RPI will connect. Everything in the while loop underneath is code for the connection to the RPI.

The first line in the 'main' function at the bottom starts a new thread that runs simultaneously alongside the rest of the program (the connection part). This thread is the GUI. This thread calls the function labelled 'main()'.
This is the function that starts up the GUI. Within this function, a global appCloseEvent is declared to signal the original thread, which governs the RPI connection, that the app has been closed.
Below that, the window.show() function displays the GUI. At this point, the thread will not progress with the rest of the code in this function until the window is closed.

###### ***Note: the readData() function is currently unused and has no functionality


#### RPI Connection:
There are 2 nested while loops for the control laptop connection code. 
Inside the outer loop, the laptop attempts to connect to the RPI. Once connected, it enters the inner loop.
The inner loop contains the code that listens for data sent by the RPI and saves it. It also triggers an event that will trigger the GUI update function.
The inner loop also contains the code that sends commands to the RPI. Lastly, the final if statement in the inner loop detects if the app has been closed. If so, end the program

#### Raspberry Pi Code:
The main file for the Raspberry Pi is rpiMain.py. On startup, it establishes connections with each of the 3 Arduinos to gather analog data. Then, it runs a brake check sequence defined in another file. Finally, it enters it's main loop.

The outer loop attempts to establish a connection with the control center. If it is unsuccessful, it will wait one second before retrying. Once the connection is established, the RPI will read data from all three Arduinos, save it in a text file, and then send that data to the laptop. After sending the data, it will listen for incoming commands from the control center. Commands are formatted with letters denoting the command, spaces between each command and exclamation marks at the end. 

At any given point in time, the pod will be in 1 of 4 states. They are:
- Safe (0)
- Running (1)
- Braking (2)
- Fault (3)

The commands are:
- Stop = X
- Go = G

Depending on the current state and the command received from the control station, a number of different functions may be performed. The current state of the pod may also change depending on input from the sensors, or commands received from the control station.
The functions are defined in pinouts.py and podStates.py. Currently, only the brakeCheck and launch functions have been defined in podStates.py. In pinouts.py, the pinouts of the RPI and some base functions are defined. For example, functions to read brake positions, turn on LEDs, apply or release brakes, and directing power to the LIM are all defined here.



## Dependencies

### Libraries
Python:
- PyQt
- PySide6
- serial    
- sys    
- socket    
- time    

Arduino:
- Timer.h    
- AM2302-Sensor.h
