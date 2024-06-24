from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import os
import RPi.GPIO as GPIO

app = Flask(__name__)



pi_camera = VideoCamera()

GPIO.setmode(GPIO.BCM)

control_pins = [17, 27, 22, 23]
control_pins2 = [24, 25, 6, 5]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
for pin in control_pins2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

seq = [
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]



@app.route('/left')
def left():
    print("Left")
    for i in range(1 * 256):  
        for halfstep in range(8):  
            for pin in range(4): 
                GPIO.output(control_pins[pin], seq[halfstep][pin])
            time.sleep(0.001)  
    return "nothing"

@app.route('/right')
def right():
    print("Right")
    for i in range(1 * 256):  
        for halfstep in range(8): 
            for pin in range(4):
                GPIO.output(control_pins2[pin], seq[halfstep][pin])
            time.sleep(0.001)
    return "nothing"

@app.route('/up')
def up():
    print("Up")
    for i in range(1 * 256): 
        for halfstep in range(8):  
            for pin in range(4):  
                GPIO.output(control_pins[pin], seq[::-1][halfstep][pin])
                GPIO.output(control_pins2[pin], seq[halfstep][pin])
            time.sleep(0.001)  
    return "nothing"

@app.route('/down')
def down():
    print("Down")
    for i in range(1 * 256):  
        for halfstep in range(8):  
            for pin in range(4): 
                GPIO.output(control_pins[pin], seq[::-1][halfstep][pin])
                GPIO.output(control_pins2[pin], seq[halfstep][pin])
            time.sleep(0.001)  
    return "nothing"

@app.route('/', methods=['GET', 'POST'])
def move():
    result = ""
    if request.method == 'POST':
        return render_template('index.html', res_str=result)
    return render_template('index.html')






def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.1)  
        

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
                    
                    
@app.route('/set_credentials', methods=['POST'])
def set_credentials():
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    return 'Credentials set'
    
    
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
    GPIO.cleanup()
