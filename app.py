import serial
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Vytvoření Flask aplikace a nastavení Socket.IO
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Nastavení sériového portu pro komunikaci s hardwarem
ser = serial.Serial(port='COM4', baudrate=9600, timeout=1)

# Definice základní cesty a renderování hlavní stránky
@app.route("/")
def index():
    return render_template('index.html', title='Home Page')

# Funkce pro čtení dat ze sériového portu
def read_serial():
    while True:
        if ser.in_waiting > 0:
            try:
                # Čtení dat ze sériového portu
                data = ser.readline().decode('utf-8', errors='ignore').rstrip()
                if data:
                    # Parsování dat a odeslání pomocí Socket.IO
                    values = parse_data(data)
                    if values:
                        socketio.emit('data', values)
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")

# Funkce pro parsování přijatých dat
def parse_data(data):
    try:
        # Rozdělení řetězce dat podle čárky
        values = data.split(',')
        return values
    except (ValueError, IndexError):
        print(f"Error parsing data: {data}")
        return None

# Obsluha přijatých dat přes Socket.IO pro nastavení RGB hodnot
@socketio.on('set_rgb')
def handle_set_rgb(data):
    r = data.get('r')
    g = data.get('g')
    b = data.get('b')

    print(f'Setting RGB values: R={r}, G={g}, B={b}')  # Debug výpis
    
    # Odeslání hodnot pro červenou složku
    if r is not None:
        ser.write(f"r{r}\n".encode('utf-8'))
        print(f"r{r}\n".encode('utf-8'))
    
    # Odeslání hodnot pro zelenou složku
    if g is not None:
        ser.write(f"g{g}\n".encode('utf-8'))
        print(f"g{g}\n".encode('utf-8'))
    
    # Odeslání hodnot pro modrou složku
    if b is not None:
        ser.write(f"b{b}\n".encode('utf-8'))
        print(f"b{b}\n".encode('utf-8'))

# Spuštění aplikace
if __name__ == '__main__':
    # Spuštění funkce read_serial jako pozadí úlohy
    socketio.start_background_task(target=read_serial)
    # Spuštění Flask aplikace
    socketio.run(app, host='0.0.0.0', port=5000)