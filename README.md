# InSight_RPI_scripts
 
InSight is an integrated system designed to enhance security and user interaction through the combination of a mobile application and a Raspberry Pi-based facial recognition system. The project encompasses two primary components: a mobile application developed in Android studio with Java and a web-based control system utilizing Python and HTML, hosted on a Raspberry Pi. The mobile application facilitates user management tasks such as registration, login, profile updates, and image handling, leveraging Firebase for backend services. Concurrently, the Raspberry Pi system captures real-time video, processes facial recognition, and provides motor control for viewing different angles of the video stream.

This project aims to create a seamless user experience by enabling users to register, authenticate, and manage their profiles through the mobile app while utilizing the Raspberry Pi system for real-time surveillance and control.







Within this repository, the scripts for the live stream,face recognition and camera movements are defined. 
In order to be able to run this code, multiple steps need to be followed:

I will start with the premise that you begin with a RaspberryPi 4B+, which has the latest version of Raspberry Pi OS available as of 01.01.2024 (this version is available for free on the official site https://www.raspberrypi.com/software/), and the Python version is >= Python 3.
Additionally, you will need a RaspberryPi camera v1.3, two 28BYJ-48 Stepper Motors, two ULN2003 motor drivers, and cables to connect them to the board.

After starting the board, the output port for the video camera must be activated. This can be done through the operating system interface (Settings - Interfaces - Legacy Camera), or by running the following command in the terminal: sudo raspi-config nonint do_legacy 0
After this, a reboot is necessary.

The physical connections between the board and the accessories mentioned above are described in the documentation, Chapter 2.3.5.

Necessary imports for the correct and efficient functioning of the script (below is a list of commands that need to be sent in the terminal before running the actual application):
(Depending on the internet connection, these imports can take between 2 and 10 hours)

"sudo apt-get update

sudo apt-get upgrade

sudo apt-get install gfortran

sudo apt-get install git

sudo apt-get install build-essential

sudo apt-get install cmake

sudo apt-get install wget

sudo apt-get install graphicsmagick

sudo apt-get install curl

sudo apt-get install libgraphicsmagick1-dev

sudo apt-get install libatlas-base-dev

sudo apt-get install libavcodec-dev

sudo apt-get install libboost-all-dev

sudo apt-get install libgtk2.0-dev

sudo apt-get install libavformat-dev

sudo apt-get install libjpeg-dev

sudo apt-get install liblapack-dev

sudo apt-get install libswscale-dev

sudo apt-get install pkg-config

sudo apt-get install python3-dev

sudo apt-get install python3-numpy

sudo apt-get install python3-pip

sudo apt-get install zip

sudo apt-get clean

sudo apt-get install python3-picamera

sudo pip3 install --upgrade picamera[array]

sudo nano /etc/dphys-swapfile -- a configuration file will now be opened, and the following variable will need to be altered from CONF_SWAPSIZE=100 to CONF_SWAPSIZE=1024 and then save / exit nano

sudo /etc/init.d/dphys-swapfile 

mkdir -p dlib

git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git dlib/

cd ./dlib

sudo apt-get install cmake

mkdir build; cd build; cmake .. ; cmake --build

pip3 install dlib

sudo nano /etc/dphys-swapfile -- same configuration file as before, now the variable will need to be changed to the original value, from: CONF_SWAPSIZE=1024 to CONF_SWAPSIZE=100 and then save / exit nano

pip3 install numpy

sudo apt-get install python3-scipy

pip3 install scikit-image

sudo apt-get install libjasper-dev

sudo apt-get install libqtgui4

sudo apt-get install python3-pyqt5

sudo apt install libqt4-test

pip3 install opencv-python==3.4.6.27

pip3 install face_recognition 

git clone --single-branch https://github.com/ageitgey/face_recognition.git

cd ./face_recognition/examples && python3 facerec_on_raspberry_pi.py

python3 facerec_on_raspberry_pi.py"

After these imports are completed, a reboot is necessary.


Steps to run the application (Ensure that the list of imports described above is satisfied before running the application):


- Open the terminal window
- Navigate to the location where the main.py script is saved using the "cd ..", "ls .." commands
- Inside the main.py script, replace the IP address from "host:0.0.0.0" with the IP address of the internet network where the script is running (e.g., "host:192.168.62.48"):
"    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
    GPIO.cleanup()
"
- Run the main.py script: python3 main.py
- To view the live stream, the user will need to either use the mobile application or enter a browser and access: [Previously provided IP address]:5000. To view the video stream, the device from which the stream is being viewed must be on the internet network with the provided IP.
- To stop the stream, type the command "CTRL+C" in the terminal window
