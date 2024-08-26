import Redis from 'ioredis';
import fastify from 'fastify';
import fastifyStatic from '@fastify/static';
import fastifyJwt from '@fastify/jwt';
import fastifyCookie from '@fastify/cookie';
import { join } from 'node:path';
import { randomBytes, randomInt } from 'node:crypto';

const redis = new Redis(6379, "redis");
const app = fastify();

const winning = new Map([
	['🪨', '📃'],
	['📃', '✂️'],
	['✂️', '🪨']
]);

app.register(fastifyStatic, {
	root: join(import.meta.dirname, 'static'),
	prefix: '/'
});

app.register(fastifyJwt, { secret: process.env.SECRET_KEY || randomBytes(32), cookie: { cookieName: 'session' } });

app.register(fastifyCookie);

await redis.zadd('scoreboard', 1336, 'FizzBuzz101');

app.post('/new', async (req, res) => {
	const { username } = req.body;
	const game = randomBytes(8).toString('hex');
	await redis.set(game, 0);
	return res.setCookie('session', await res.jwtSign({ username, game })).send('OK');
});

app.post('/play', async (req, res) => {
	try {
		await req.jwtVerify();
	} catch(e) {
		return res.status(400).send({ error: 'invalid token' });
	}
	const { game, username } = req.user;
	const { position } = req.body;
	const system = ['🪨', '📃', '✂️'][randomInt(3)];
	if (winning.get(system) === position) {
		const score = await redis.incr(game);

		return res.send({ system, score, state: 'win' });
	} else {
		const score = await redis.getdel(game);
		if (score === null) {
			return res.status(404).send({ error: 'game not found' });
		}
		await redis.zadd('scoreboard', score, username);
		return res.send({ system, score, state: 'end' });
	}
});

app.get('/scores', async (req, res) => {
	const result = await redis.zrevrange('scoreboard', 0, 99, 'WITHSCORES');
	const scores = [];
	for (let i = 0; i < result.length; i += 2) {
		scores.push([result[i], parseInt(result[i + 1], 10)]);
	}
	return res.send(scores);
});

app.get('/flag', async (req, res) => {
	try {
		await req.jwtVerify();
	} catch(e) {
		return res.status(400).send({ error: 'invalid token' });
	}
	const score = await redis.zscore('scoreboard', req.user.username);
	if (score && score > 1336) {
		return res.send(process.env.FLAG || 'corctf{test_flag}');
	}
	return res.send('You gotta beat Fizz!');
})

app.listen({ host: '0.0.0.0', port: 8080 }, (err, address) => console.log(err ?? `web/rock-paper-scissors listening on ${address}`));