from flaskr import create_app, socketio

app = create_app(debug=True)

if __name__ == "__main__":
    socketio.run(app, host="26.182.9.155", port=5000)
