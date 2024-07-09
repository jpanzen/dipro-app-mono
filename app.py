import serial
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Inicializace Flask aplikace
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Inicializace sériového portu
ser = serial.Serial(port='COM6', baudrate=19200, timeout=1)

# Hlavní cesta - zobrazí index.html
@app.route("/")
def index():
    return render_template('index.html', title='Home Page')

# Funkce pro čtení dat ze sériového portu
def read_serial():
    while True:
        if ser.in_waiting > 0:
            try:
                # Čtení dat ze sériového portu a dekódování do UTF-8
                data = ser.readline().decode('utf-8', errors='ignore').rstrip()
                if data:
                    # Zpracování dat z řetězce na dictionary
                    values = parse_data(data)
                    if values:
                        # Odeslání zpracovaných dat pomocí SocketIO
                        socketio.emit('data', values)
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")

# Funkce pro zpracování dat ze sériového portu do formátu dictionary
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

# SocketIO handler pro příjem dat od klienta a jejich odeslání na sériový port
@socketio.on('send_data')
def handle_send_data(json):
    data = json.get('data')
    if data:
        # Zaslání dat na sériový port ve formátu textu
        ser.write(f"{data}\n".encode('utf-8'))

# Spuštění aplikace a nastavení asynchronního čtení sériového portu
if __name__ == '__main__':
    socketio.start_background_task(target=read_serial)
    socketio.run(app, host='0.0.0.0', port=5000)