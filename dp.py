# Init aplikace
app = Flask(__name__)
socketio = SocketIO(app)
ser = serial.Serial(port='COM4', baudrate=9600, timeout=1)

# Routy
@app.route('/')
def index():
    return render_template('index.html')

# Inicializace websocketu na straně serveru
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Čtení dat ze sériové linky
def read_serial():
    while True:
        if ser.in_waiting > 0:
            # čtení a zpracování dat

if __name__ == '__main__':
    socketio.start_background_task(read_serial)
    socketio.run(app, debug=True)