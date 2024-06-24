import serial
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

ser = serial.Serial(port='COM4', baudrate=9600, timeout=1)

@app.route("/")
def index():
    # Your route logic
    return render_template('index.html', title='Home Page')

def read_serial():
    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8', errors='ignore').rstrip()
                if data:
                    voltage = float(data)
                    print(voltage)
                    socketio.emit('data', {'voltage': voltage})
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")

if __name__ == '__main__':
    socketio.start_background_task(target=read_serial)
    socketio.run(app, host='0.0.0.0', port=5000) 