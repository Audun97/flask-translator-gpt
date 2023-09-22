const copyButton = document.getElementById('copy_text');
const copyButtonImg = copyButton.querySelector('img');

function copyTextToClipboard() {
    var text = document.querySelector('textarea[name="user_output"]').value;
    navigator.clipboard.writeText(text)
        .then(() => {
            console.log('Text copied to clipboard');
        })
        .catch(err => {
            console.error('Failed to copy text: ', err);
        });
}

copyButton.addEventListener('click', function(event) {
    event.preventDefault();
    copyTextToClipboard();
});

copyButton.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        copyTextToClipboard();
    }
});