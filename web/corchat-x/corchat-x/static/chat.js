import { io } from "/socket.io.esm.min.js";

document.getElementById('connect').onclick = async () => {
	document.getElementById('chat').hidden = false;
	document.getElementById('connect').hidden = true;

	const me = document.body.getAttribute('data-username');
	const conversation = [];

	const socket = io();

	window.socket = socket; // so the admin bot can reply to messages!

	const messages = document.getElementById('messages');
	const message = document.getElementById('message');

	const createMessage = (username, content, html = false) => {
		const span = document.createElement('span');

		const name = document.createElement('b');
		name.textContent = username;
		span.appendChild(name);
		
		const message = document.createElement('blockquote');
		if (html) {
			message.innerHTML = content;
		} else {
			message.textContent = content;
		}
		span.appendChild(message);

		return span;
	}

	socket.on('connect_error', err => {
		messages.appendChild(createMessage('System', err.message));
	});

	socket.on('message', async ({ username, content }) => {
		messages.appendChild(createMessage(username, content, username === 'FizzBuzz101'));
		if (username !== 'System') {
			conversation.push({ username, message: content });
		}

		if (me === 'FizzBuzz101' && !['System', me].includes(username)) {
			const res = await fetch('https://fizzbot.crusadersofrust.workers.dev', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(conversation.slice(-10))
			})

			const response = (await res.text()).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');;

			if (res.status != 200) {
				socket.emit('message', 'FizzBot is currently experiencing: ' + sanitize.textContent);
			} else {
				socket.emit('message', response);
			}
		}
		messages.scrollTo(0, messages.scrollHeight);
	});

	socket.on('disconnect', () => {
		messages.appendChild(createMessage('System', 'Disconnected!'));
	});

	document.getElementById('messageForm').onsubmit = e => {
		e.preventDefault();
		socket.emit('message', message.value);
		message.value = '';
	}
}