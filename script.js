// Importing required modules
const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const dotenv = require('dotenv');
const path = require('path');
const bcrypt = require('bcrypt');
const User = require('./models/user'); // Ensure you have a User model defined

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
}));

app.use(passport.initialize());
app.use(passport.session());

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error(err));

// Passport Config
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/google/callback',
},
    (accessToken, refreshToken, profile, done) => {
        return done(null, profile);
    }
));

passport.serializeUser((user, done) => {
    done(null, user);
});

passport.deserializeUser((user, done) => {
    done(null, user);
});

// Routes
app.post('/signup', async (req, res) => {
    try {
        const { username, email, password } = req.body;
        const hashedPassword = await bcrypt.hash(password, 10);
        const user = new User({ username, email, password: hashedPassword });
        await user.save();
        res.json({ success: true, message: 'User registered successfully!' });
    } catch (error) {
        res.json({ success: false, message: 'Registration failed. Please try again.' });
    }
});

app.post('/signin', async (req, res) => {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (user && await bcrypt.compare(password, user.password)) {
        req.session.user = user; // Store user session
        res.json({ success: true, message: 'Signed in successfully!' });
    } else {
        res.json({ success: false, message: 'Invalid email or password.' });
    }
});

app.get('/auth/google',
    passport.authenticate('google', { scope: ['profile', 'email'] })
);

app.get('/auth/google/callback',
    passport.authenticate('google', { failureRedirect: '/' }),
    (req, res) => {
        // Successful authentication, redirect to index.html
        res.redirect('/index.html');
    }
);

app.get('/logout', (req, res) => {
    req.logout(err => {
        if (err) { return next(err); }
        res.redirect('/');
    });
});

// Serve sign-up page by default
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'signup.html'));
});

// Protect main route
app.get('/index.html', (req, res) => {
    if (!req.isAuthenticated()) {
        return res.redirect('/signin.html'); // Redirect to sign-in if not authenticated
    }
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Predict route (placeholder for actual prediction logic)
app.post('/predict', (req, res) => {
    // Handle prediction logic here
    res.json({ prediction: 'Example Prediction' });
});

// Client-side logic
app.get('/script.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'script.js'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Frontend logic for file upload and prediction
document.getElementById('uploadForm').onsubmit = async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput').files[0];
    if (!fileInput) return;

    const formData = new FormData();
    formData.append('file', fileInput);

    const response = await fetch('/predict', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    document.getElementById('predictionResult').innerText = result.prediction ? `Prediction: ${result.prediction}` : `Error: ${result.error}`;
};
