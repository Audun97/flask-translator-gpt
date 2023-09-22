const pasteButton = document.getElementById('paste_text');

function pasteTextFromClipboard() {
    navigator.clipboard.readText()
        .then(text => {
            document.querySelector('textarea[name="user_input"]').value = text;
        })
        .catch(err => {
            console.error('Failed to read clipboard contents: ', err);
        });
}

pasteButton.addEventListener('click', function(event) {
    event.preventDefault();
    pasteTextFromClipboard();
});

pasteButton.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        pasteTextFromClipboard();
    }
});