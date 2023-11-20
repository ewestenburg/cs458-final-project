function submitForm() {
    const userInput = document.getElementById('userInput').value;
    fetch('/processData', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `userInput=${userInput}`,
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
        // You can handle the response as needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}