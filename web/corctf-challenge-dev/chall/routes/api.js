const express = require("express");
const db = require("../db.js");

const router = express.Router();

const requiresLogin = (req, res, next) =>
    req.user
        ? next()
        : res.json({ success: false, error: "You must be logged in!" });

router.post("/login", (req, res) => {
    let { user, pass } = req.body;
    if (!user || !pass || typeof user !== "string" || typeof pass !== "string") {
        return res.json({
            success: false,
            error: "Missing username or password",
        });
    }

    if (!db.hasUser({user: user})) {
        return res.json({
            success: false,
            error: "No user exists with that username",
        });
    }

    if (!db.checkPass({user: user, pass: pass})) {
        return res.json({ success: false, error: "Invalid password" });
    }

    req.session.user = user;
    res.json({ success: true });
});

router.post("/register", (req, res) => {
    let { user, pass } = req.body;
    if ( !user || !pass || typeof user !== "string" || typeof pass !== "string") {
        return res.json({
            success: false,
            error: "Missing username or password",
        });
    }

    if (db.hasUser({user: user})) {
        return res.json({
            success: false,
            error: "User already exists",
        });
    }

    req.session.user = user;
	db.addUser({user: user, pass: pass});
    res.json({ success: true });
});

router.post("/create", requiresLogin, (req, res) => {
    let { title, description } = req.body;
    if (!title || !description || typeof title !== "string" || typeof description !== "string") {
        return res.json({ success: false, error: "Missing title or description" });
    }

    req.user.challenges.push(db.addChallenge({title: title, description: description}));

    res.json({ success: true });
});

router.post("/challenges", requiresLogin, (req, res) => {
    return res.json({
        success: true,
        data: req.user.challenges.map((id) => db.getChallenge({id: id})),
    });
});

module.exports = router;