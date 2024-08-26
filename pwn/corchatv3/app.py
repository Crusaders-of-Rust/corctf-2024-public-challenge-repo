from flask import Flask, request, g, render_template, redirect
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
app.config["DATABASE"] = "chat.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return redirect("/chatroom")

@app.route("/chatroom", methods=["GET"])
def chatroom():
    return render_template("chatroom.html")

@app.route("/send_message", methods=["POST"])
def post_new_message():
    message = request.form.get("msg")
    if message == None or len(message) == 0:
        return "Invalid request"

    db = get_db()
    s = f"INSERT INTO messages (message) VALUES ('{message}')"
    db.cursor().execute(s)
    db.commit()

    data = {"msg": message}
    socketio.emit("recv_message", data)
    return "Success"

@socketio.on("connect")
def handle_new_connection():
    cursor = get_db().cursor()
    s = f"SELECT message FROM messages"
    cursor.execute(s)

    messages = cursor.fetchall()
    for message in messages:
        data = {"msg": message[0]}
        socketio.emit("recv_message", data, to=request.sid)

@socketio.on("new_message")
def handle_new_message(data):
    message = data["msg"]
    if message == None or len(message) == 0:
        return

    db = get_db()
    s = f"INSERT INTO messages (message) VALUES ('{message}')"
    db.cursor().execute(s)
    db.commit()

    socketio.emit("recv_message", data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
