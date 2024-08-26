import secrets
from flask import Flask, session, request, redirect, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='/', static_folder='./static', template_folder='./templates')
app.config['SECRET_KEY'] = secrets.token_hex(32)

socketio = SocketIO(app, cors_allowed_origins='*')
users = set()

@app.after_request
def csp(response):
	response.headers['Content-Security-Policy'] = '; '.join([
		"default-src 'none'",
		"connect-src 'self' https://fizzbot.crusadersofrust.workers.dev",
		"script-src 'self'",
		"style-src 'self' 'unsafe-inline'",
		"img-src 'self'"
	])
	return response

@app.get('/')
def index():
	return app.send_static_file('index.html')

@app.post('/')
def login():
	username = request.form.get('name', default=secrets.token_hex(8))
	if not username.isalnum() or not (0 < len(username) < 20):
		return 'Invalid username!', 400
	session['username'] = username
	return redirect('/chat')

@app.get('/chat')
def chat():
	if 'username' not in session:
		return redirect('/')
	return render_template('chat.html', username=session['username'])

@app.get('/render/<text>')
def render(text: str):
	if len(text) > 100:
		return 'Invalid text!', 400
	return render_template('render.svg', text=text)

@socketio.on('connect')
def connect():
	if 'username' not in session:
		return False
	
	username = session.get('username')
	if username in users:
		return False
	users.add(username)

	emit('message', {'username': 'System', 'content': f'Connected!'})
	emit('message', {'username': 'System', 'content': f'{username} joined.'}, broadcast=True)

@socketio.on('message')
def message(content):
	if not isinstance(content, str) or not (0 < len(content) < 400):
		return
	emit('message', {'username': session['username'], 'content': content}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
	if session['username'] in users:
		users.remove(session['username'])
		emit('message', {'username': 'System', 'content': f'{session["username"]} disconnected.'}, broadcast=True)

socketio.run(app, host='0.0.0.0', port=8080, use_reloader=False, log_output=True, allow_unsafe_werkzeug=True)