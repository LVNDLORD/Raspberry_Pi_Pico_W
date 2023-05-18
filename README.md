# Content of the README
- Introduction
- Installation
- Code description
- Hardware description



# Introduction
Here are 3 of my Micropython projects using Raspberry Pi Pico W.\
Each project contains a link to a demo GIF, where can be seen what each code does.\
\
The last one is my final project from my first year at the university, which uses a wireless connection to the Kubios Cloud to do the Heart Rate Variability analysis.

The whole setup\
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/whole_setup_1.jpg)


# Installation
1. Download and install the latest standard [Python](https://www.python.org/) and [Thonny IDE](https://thonny.org/)
2. During the installation of Python, select Add Python.exe to the PATH 
3. Create a local directory on your PC and clone this repository from Github to this directory

The shortest and easiest way to proceed would be:
- Open Thonny IDE
- Connect Raspberry Pi Pico W to your PC
- Using Thonny IDE install "Pico W nightly firmware". Instructions can be found [here](https://micropython.org/download/rp2-pico-w/) 
- Make sure your Raspberry Pi Pico W is found and displayed in Thonny IDE Shell.
You should see something like this
```bash
MicroPython v1.19.1-966-g05bb26010 on 2023-03-13; Raspberry Pi Pico W with RP2040`\
`Type "help()" for more information.
```
- Open the cloned folder in Thonny IDE 
- Right-click on **each python file** and `lib` folder from the directory, and select `Upload to /` from the dropdown menu.
- Done!
##

 If that way doesn't work for any reason, try this:

- Open Thonny IDE
- Connect Raspberry Pi Pico W to your PC
- Using Thonny IDE install "Pico W nightly firmware". Instructions can be found [here](https://micropython.org/download/rp2-pico-w/)
- Run `webserver.cmd` (on Windows)  or `webserver.sh` (on Mac)
- When Python is installed, open the first terminal and write `pip3 install mpremote`. Don't close the terminal
- In the new (second) terminal window navigate to the cloned folder (cd <project folder>) and start a web server by writing a command:\
on Windows `python –m http.server`\
on Mac `python3 –m http.server`\
If the server started successfully you should see this in the terminal
```bash
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```
Don't close this terminal!

- Go back to the first terminal, **navigate to the project folder (cd <project folder>)** and check the com-port number of your Pico by writing a command:\
on Windows `mpremote connect list` or if didn't work, try `python -m mpremote connect list`\
on Mac `python3 –m mpremote connect list` 
- Copy the files to Pico W by writing a command:\
on Windows `mpremote connect \<comXX\> mip install --target / http://localhost:8000/`\
if that didn't work, try  `python -m mpremote connect \<comXX\> mip install --target / http://localhost:8000/`\
on Mac `python3 -m mpremote connect \<comXX\> mip install --target / http://localhost:8000/`

 where `comXX` - COM port of your RP Pico W. `XX` should be replaced with a number of the port\
On Windows, com-port looks like this `COM8`\
On Mac com-port is a long string e.g. `/dev/cu.usbmodem12102`. Write the whole string into the previous command instead of `\<comXX\>`.
- Close the second terminal window with the webserver
- Done!


##
If you have done everything correctly, your files in RP Pico should look like this:
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/pico_content.png)\
RP Pico W content


# Code description
1. `led_menu.py` - select and run the file.\
[Link to the demo GIF](https://users.metropolia.fi/~andriid/Micropython_project/led_menu_4.gif)

Control the brightness of LEDs on the add-on board using a rotary knob.\
Selecting LED and going back to the menu is executed by pressing down the knob.\
LED selection and brightness percentage are shown on the OLED display.



##
2. `dataset.py`  - select and run the file.\
[Link to the demo GIF](https://users.metropolia.fi/~andriid/Micropython_project/dataset_5.gif)

Inside the `dataset.py` file are 2 sets of PPI (pulse–pulse intervals) values given in ms.\
Code calculates the basic Heart Rate Variability analysis parameters and shows the following values on the OLED:

▪ Mean PPI\
▪ mean heart rate (HR)\
▪ Standard deviation of PPI (SDNN)\
▪ Root mean square of successive differences (RMSSD)

Pressing SW_2 (upper button) on the Pico add-on board displays the calculation results of "set_1"\
Pressing SW_0 (bottom button) on the Pico add-on board displays the calculation results of "set_2"


##
3. `Project.py`\
   `kubios.py`\
   [Link to the demo GIF](https://users.metropolia.fi/~andriid/Micropython_project/Project.gif)


The heart rate sensor is connected to the ADC pin on the RP Pico add-on board.
To run this code you need to fill the following credentials in the `kubios.py` file.

```
ssid = <your Wifi name>
password = <your Wifi password>
APIKEY = <your Kubios API key>
CLIENT_ID = <your client ID to Kubios Cloud>
CLIENT_SECRET = <your client secret to Kubios Cloud>
LOGIN_URL = <your Kubios Cloud Login URL>
TOKEN_URL = <your Kubios Cloud authentication Token>
REDIRECT_URI = <your Kubios Cloud analysis login link>
```

When filled, save the file.

**Make sure `Project.py` and `kubios.py` are both in the root directory of the RP Pico W.** (as shown on the "RP Pico W content" image)

Execution order:
1. Run the `Project.py` file
2. Put the finger on the heart rate sensor
3. When the display shows **'Press the knob to start measuring'** you can press the knob while keeping the finger on the sensor
4. Wait for the Pico to collect the data from the sensor for the time specified in variable `run_time_in_sec` in `Project.py`\
(by default 20s, but can be set to any desired time for measurement, as long as Pico has enough memory to store data)
5. When the display shows **' Please wait for the data to be processed...'** you can release the finger from the sensor
6. Meanwhile Pico connects to the Wifi and attempts to connect to Kubios Cloud
7. As a connection to the Kubios Cloud is established, collected PPI values are sent to the Kubios Cloud 
8. When calculations in  Kubios Cloud are done, Kubios returns the JSON.
9. The returned JSON is parsed and the needed values (SNS and PNS index, mean BPM, and SDNN values) are extracted.
10. Finally, these 4 values are shown on the OLED display together with the time of measurement.

In the repository, you can see an example of the JSON file `kubios_data.json` returned from Kubios Cloud.



![alt text](https://users.metropolia.fi/~andriid/Micropython_project/project_results.jpg)\
Results of Kubios Cloud PPI analysis

# Hardware description

1. **Raspberry Pico W**
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/picow-pinout.svg)
2. **Add-on board**
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/dev_board.png)
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/dev_board_pinout.png)
3. **Rotary encoder**
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/Rotary%20encoder.webp)
4. **Crowtail pulse sensor v 2.0** - connected to ADC Input on the development board\
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/crowtail_pulse_sensor_v_2_0.webp)
5. **OLED ssd1306**
![alt text](https://users.metropolia.fi/~andriid/Micropython_project/oled-ssd1306-display-i2c-128-x-64-pixel.webp)
