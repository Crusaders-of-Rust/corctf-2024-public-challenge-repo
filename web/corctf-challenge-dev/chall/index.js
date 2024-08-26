const express = require("express");
const crypto = require("crypto");
const session = require("express-session");
const MemoryStore = require("memorystore")(session)

const app = express();

const PORT = process.env.PORT || 8080;

const db = require("./db.js");
const bot = require("./bot/bot.js");

app.use(
    session({
        cookie: { maxAge: 3600000 },
        store: new MemoryStore({
            checkPeriod: 3600000,
        }),
        resave: false,
        saveUninitialized: false,
        secret: crypto.randomBytes(32).toString("hex"),
    })
);

app.use(express.static("public"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req, res, next) => {
	const nonce = crypto.randomBytes(16).toString('base64');
    res.setHeader(
        "Content-Security-Policy",
        `base-uri 'none'; script-src 'nonce-${nonce}'; img-src *; font-src 'self' fonts.gstatic.com; require-trusted-types-for 'script';`
    );
    res.locals.user = null;
    if (req.session.user && db.hasUser({user: req.session.user})) {
        req.user = db.getUser({user: req.session.user});
        res.locals.user = req.user;
	}
	res.locals.nonce = nonce;
    next();
});

app.set('view engine', 'ejs');

app.use("/api", require("./routes/api.js"));

const requiresLogin = (req, res, next) => 
	req.user
		? next()
		: res.redirect('/login');

app.get("/", (req, res) => res.render("index"));

app.get("/login", (req, res) => res.render("login"));

app.get("/register", (req, res) => res.render("register"));

app.get("/create", requiresLogin, (req, res) => res.render("create"));

app.get("/challenges", requiresLogin, (req, res) => res.render("challenges"));

app.get("/challenge/:id", (req, res) => {
    let { id } = req.params;
    if (!id) {
        return res.json({ success: false, error: "No id provided" });
    }
    if (!db.hasChallenge({id: id})) {
        return res.status(404).send("Challenge not found!");
    }
	challenge = db.getChallenge({id: id});
	res.render('challenge', { challenge });
});

app.get("/submit", requiresLogin, (req, res) => {
    const { url } = req.query;
    
    if (!url || typeof url !== "string") {
        return res.send('missing url');
    }

    const urlObj = new URL(url);
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
        return res.send('url must be http/https')
    }

    bot.visit(url);
    res.send('the admin will visit your url soon');
});

app.listen(PORT, () => console.log(`app listening on port ${PORT}`));