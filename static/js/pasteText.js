document.getElementById('paste_text').addEventListener('click', function(event) {
    event.preventDefault();
    navigator.clipboard.readText()
        .then(text => {
            document.querySelector('textarea[name="user_input"]').value = text;
        })
        .catch(err => {
            console.error('Failed to read clipboard contents: ', err);
        });
});