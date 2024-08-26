const scores = await (await fetch('/scores')).json();

for (const [username, score] of scores) {
	const record = document.createElement('tr');
	const usernameElement = document.createElement('td');
	usernameElement.textContent = username;
	record.appendChild(usernameElement)

	const scoreElement = document.createElement('td');
	scoreElement.textContent = score;
	record.appendChild(scoreElement);

	const scoresElement = document.getElementById('scores');
	scoresElement.appendChild(record);
}