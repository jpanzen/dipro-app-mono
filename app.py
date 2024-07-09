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
        values = data.split(',')
        return values
    except (ValueError, IndexError):
        print(f"Error parsing data: {data}")
        return None

# Obsluha přijatých dat přes SocketIO
@socketio.on('set_rgb')
def handle_set_rgb(data):
    r = data.get('r')
    g = data.get('g')
    b = data.get('b')

    print(f'Setting RGB values: R={r}, G={g}, B={b}')  # Debug výpis
    
    if r is not None:
        ser.write(f"r{r}\n".encode('utf-8'))
        print(f"r{r}\n".encode('utf-8'))
    
    if g is not None:
        ser.write(f"g{g}\n".encode('utf-8'))
        print(f"g{g}\n".encode('utf-8'))
    
    if b is not None:
        ser.write(f"b{b}\n".encode('utf-8'))
        print(f"b{b}\n".encode('utf-8'))

if __name__ == '__main__':
    socketio.start_background_task(target=read_serial)
    socketio.run(app, host='0.0.0.0', port=5000)