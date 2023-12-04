const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const path = require('path');
const { spawn } = require('child_process');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('frontend/public'));

global.processingComplete = false;

// Serve the main search page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/public/index.html'));
});

// Handle the search request and start processing
app.post('/search', (req, res) => {
    const userInput = req.body.userInput;
    global.processingComplete = false;
    startProcessing(userInput); // Start processing based on user input
    res.redirect('/loading'); // Redirect to the loading page
});

// Serve the loading page
app.get('/loading', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/public/loading.html'));
});

// Check if processing is complete
app.get('/checkStatus', (req, res) => {
    res.json({ status: global.processingComplete ? 'complete' : 'processing' });
});

// Serve the results page once processing is complete
app.get('/spotify_tracks', (req, res) => {
    if (global.processingComplete) {
        res.sendFile(path.join(__dirname, 'frontend/public/spotify_tracks.html'));
    } else {
        res.redirect('/loading');
    }
});

function startProcessing(input) {
    // Function to run the Python script
    function runScript(input, callback) {
        const script = spawn('python3', ['backend/main.py', input]);

        let scriptOutput = "";
        script.stdout.on('data', (data) => {
            scriptOutput += data.toString();
        });

        script.on('close', (code) => {
            console.log(`Python script finished with code ${code}`);
            callback(scriptOutput);
        });

        script.on('error', (error) => {
            console.error('Error executing Python script:', error.message);
        });
    }

    // Run the script the first time
    runScript(input, (firstOutput) => {
        console.log(`First Python script output: ${firstOutput}`);

        // Run the script the second time
        runScript(input, (secondOutput) => {
            console.log(`Second Python script output: ${secondOutput}`);
            global.processingComplete = true; // Set processing to complete after the second run
        });
    });
}

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});