const express = require('express');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('frontend/public'));



const { spawn } = require('child_process');

// Inside the '/processData' route handler
app.post('/processData', (req, res) => {
    const userInput = req.body.userInput;

    // Call the Python script with the user input
    const cleanInput = spawn('python3', ['backend/main.py', userInput]);

    // Handle the script's output (stdout)
    cleanInput.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });

    
    // Handle any errors that occur during script execution
    cleanInput.on('error', (error) => {
        console.error('Error executing Python script:', error.message);
        res.status(500).send('Internal Server Error');
    });

    // Respond to the client (you can customize the response as needed)
    res.send(`User input received: ${userInput}`);
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});