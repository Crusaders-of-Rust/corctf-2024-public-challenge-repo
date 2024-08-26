const options = ['🪨', '📃', '✂️'];
let rotating = true;

const setDisabled = status => {
	for (const btn of document.querySelectorAll('button')) {
		btn.disabled = status;
	}
}

const start = async username => {
	const res = await (await fetch('/new', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ username })
	})).text();

	if (res != 'OK') {
		alert('failed to start game: ' + res);
		return;
	}
}

setInterval(() => {
	if (rotating) {
		const current = document.getElementById('current');
		const next = options[(options.indexOf(current.textContent) + 1) % 3];
		current.textContent = next;
	}
}, 100);

let username = localStorage.getItem('username');
if (!username) {
	username = prompt('What is your username?');
	localStorage.setItem('username', username);
}

await start(username);
setDisabled(false);

const usernameElement = document.getElementById('username');
usernameElement.textContent = username;
usernameElement.parentElement.hidden = false;

window.play = async position => {
	setDisabled(true);
	rotating = false;
	const res = await (await fetch('/play', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ position })
	})).json();
	if (res.error) {
		alert('Error: ' + res.error);
		return;
	}
	document.getElementById('current').textContent = res.system;
	document.getElementById('title').textContent = res.state == 'win' ? '🎉 You Win 🎉' : '🪦 Play Again 🪦';
	document.getElementById('score').textContent = res.score;

	if (res.state !== 'win') {
		await start(username);
		document.getElementById('score').textContent = 0;
	}

	setTimeout(() => {
		setDisabled(false);
		rotating = true;
		document.getElementById('title').textContent = 'Rock, Paper, Scissors!';
	}, 2000);
}