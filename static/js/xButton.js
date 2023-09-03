const textarea = document.querySelector('textarea[name="user_input"]');
const xButton = document.getElementById('clear_text');

textarea.addEventListener('input', () => {
    if (textarea.value) {
        xButton.style.display = 'block';
    } else {
        xButton.style.display = 'none';
    }
});

xButton.addEventListener('click', () => {
    event.preventDefault();
    textarea.value = '';
    textarea.focus();
});