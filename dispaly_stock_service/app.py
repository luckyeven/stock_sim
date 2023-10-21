import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.")

@sio.event
def disconnect():
    print("Disconnected from server.")

@sio.event
def stock_update(data):
    print(f"Stock Update for {data['ticker']}: Current Price is ${data['current_price']}")

def main():
    try:
        sio.connect('http://localhost:5000')
        sio.wait() 
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    main()
