function submitForm() {
    // Show your loading animation here

    // Make a POST request to send the data
    fetch("/translate", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_input: document.querySelector('textarea[name="user_input"]').value,
            input_language: document.querySelector('select[name="input_language"]').value,
            output_language: document.querySelector('select[name="output_language"]').value,
            formal_pronouns: document.querySelector('input[name="formal_pronouns"]').checked ? "1" : "0"
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        // After the POST request is successful, start listening for updates
        var source = new EventSource("/update");

        source.onmessage = function(event) {
            if (event.data != 'END') {
                // Update the user_output textarea with the response
                document.getElementById('user_output').value += event.data;
            } else {
                source.close(); // Close the connection after receiving all data
                // Hide your loading animation here
            }
        };
    }).catch(function() {
        console.log("Fetch error occurred.");
    });
}

// Submit form when user presses control + enter 
function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        submitForm();
    }
}

// Submit form when user presses the submit button 
document.getElementById('submit_button').addEventListener('click', function(event) {
    event.preventDefault();
    submitForm();
});