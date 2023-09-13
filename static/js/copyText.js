// Copy text from user_output textarea into clipboard when user presses the copy_text button
document.getElementById('copy_text').addEventListener('click', function(event) {
    event.preventDefault();
    var text = document.querySelector('textarea[name="user_output"]').value;
    navigator.clipboard.writeText(text)
        .then(() => {
            console.log('Text copied to clipboard');
        })
        .catch(err => {
            console.error('Failed to copy text: ', err);
        });
});