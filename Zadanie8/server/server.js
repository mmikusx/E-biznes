const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const session = require('express-session');

const app = express();

app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: false,
}));

app.use(passport.initialize());
app.use(passport.session());
app.use(express.static('../client'));

app.use(express.json());

mongoose.connect('mongodb://localhost:2717/otx_db', { useNewUrlParser: true, useUnifiedTopology: true });

const userSchema = new mongoose.Schema({
    username: String,
    email: String,
    password: String,
    googleId: String,
});

const User = mongoose.model('User', userSchema);

passport.serializeUser((user, done) => {
    done(null, user.id);
});

passport.deserializeUser(async (id, done) => {
    try {
        const user = await User.findById(id);
        done(null, user);
    } catch (err) {
        done(err);
    }
});

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    const user = await User.findOne({ username });

    if (!user) {
        console.log(`User not found for username: ${username}`);
        return res.status(400).send('User not found');
    }

    console.log(`Found user for username: ${username}`);

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
        console.log(`Invalid password for username: ${username}`);
        return res.status(400).send('Invalid password');
    }

    console.log(`Successful login for username: ${username}`);

    const token = jwt.sign({ _id: user._id }, 'SECRET_KEY');

    res.send({ token });
});

app.post('/register', async (req, res) => {
    const { username, email, password } = req.body;

    console.log(`Received register request for username: ${username}`);

    const userExists = await User.findOne({ $or: [{ username }, { email }] });
    if (userExists) {
        console.log(`User already exists for username: ${username}`);
        return res.status(400).send('User already exists');
    }

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const user = new User({ username, email, password: hashedPassword });
    await user.save();

    console.log(`User registered successfully for username: ${username}`);

    res.send('User registered successfully');
});

passport.use(new GoogleStrategy({
        clientID: "",
        clientSecret: "",
        callbackURL: "http://localhost:3000/auth/google/callback"
    },
    async function(accessToken, refreshToken, profile, cb) {
        console.log(profile);
        try {
            let user = await User.findOne({ googleId: profile.id });
            if (!user) {
                user = new User({ googleId: profile.id, username: profile.displayName });
                user = await user.save();
            }
            user.token = jwt.sign({ _id: user._id }, 'SECRET_KEY');
            return cb(null, user);
        } catch (err) {
            return cb(err);
        }
    }
));

app.get('/auth/google',
    passport.authenticate('google', { scope: ['profile'] }));

app.get('/auth/google/callback',
    passport.authenticate('google', { failureRedirect: '/login' }),
    function(req, res) {
        res.redirect(`/welcome.html`);
    });


app.listen(3000, () => console.log('Server started on port 3000'));