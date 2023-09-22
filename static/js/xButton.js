const textarea = document.querySelector('textarea[name="user_input"]');
const xButton = document.querySelector('.x-button');
const xButtonImg = xButton.querySelector('img');

textarea.addEventListener('input', () => {
    if (textarea.value) {
        xButtonImg.style.display = 'block';
        xButton.setAttribute('tabindex', '0'); // Make the 'x' button focusable
    } else {
        xButtonImg.style.display = 'none';
        xButton.setAttribute('tabindex', '-1'); // Make the 'x' button not focusable
    }
});

function clearTextarea() {
    textarea.value = '';
    textarea.focus();
    // Manually trigger the input event
    var inputEvent = new Event('input', {
        bubbles: true,
        cancelable: true,
    });
    textarea.dispatchEvent(inputEvent);
}

xButton.addEventListener('click', clearTextarea);
xButton.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        clearTextarea();
    }
});