const crypto = require("crypto");

const users = new Map();
const challenges = new Map();

const sha256 = (data) => crypto.createHash("sha256").update(data).digest("hex");

const addUser = ({ user, pass }) => {
	users.set(user, {
		pass: sha256(pass),
		challenges: [],
	});
};

const hasUser = ({ user }) => {
	return users.has(user);
}

const getUser = ({ user }) => {
	return users.get(user);
}

const checkPass = ({ user, pass }) => {
	return users.get(user).pass === sha256(pass)
}

const addChallenge = ({title, description}) => {
	let id = crypto.randomBytes(6).toString("hex");
	challenges.set(id, { id, title, description });
	return id;
}

const hasChallenge = ({ id }) => {
	return challenges.has(id);
}

const getChallenge = ({ id }) => {
	return challenges.get(id);
}

module.exports = { users, challenges, addUser, hasUser, getUser, checkPass, addChallenge, hasChallenge, getChallenge };
