msg_input = document.querySelector('textarea[aria-label="Send a message"]');
button = document.querySelector('button[aria-label="Send a message"]');
button.disabled=false;
msg_input.value = atob("{{message}}");
button.click();