import serial
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

ser = serial.Serial(port='COM6', baudrate=19200, timeout=1)

@app.route("/")
def index():
    return render_template('index.html', title='Home Page')

def read_serial():
    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8', errors='ignore').rstrip()
                if data:
                    values = parse_data(data)
                    if values:
                        socketio.emit('data', values)
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")

def parse_data(data):
    try:
        pairs = data.split(',')
        values = {}
        for pair in pairs:
            key, value = pair.split(':')
            values[key.strip()] = float(value.strip())
        return values
    except (ValueError, IndexError):
        print(f"Error parsing data: {data}")
        return None

@socketio.on('send_data')
def handle_send_data(json):
    data = json.get('data')
    if data:
        ser.write(f"{data}\n".encode('utf-8'))

if __name__ == '__main__':
    socketio.start_background_task(target=read_serial)
    socketio.run(app, host='0.0.0.0', port=5000)