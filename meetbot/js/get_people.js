// using aria label instead of classes,
// as the classes looks dynamically generated
// and, can cause breakage later, so avoiding that

// show the people list
elems = document.querySelectorAll('button[aria-label][aria-expanded="false"]');
matched = Array.from(elems).filter(el =>
    /People*/.test(el.getAttribute('aria-label'))
);
if (matched && matched.length == 1) {
    matched[0].click();
}

// wait for few miliseconds to
// let the people div to render
setTimeout(() => {
    people_div = document.querySelector('div[aria-label="Participants"]');
    __participants = []
    people_div.querySelectorAll('div[data-participant-id]').forEach(
        (x) => {
            __participants.push(x.querySelector("span")?.innerText);
        })
    window.__participants = JSON.stringify(__participants)
}, 100)

// hide the list
elems = document.querySelectorAll('button[aria-label][aria-expanded="true"]');
matched = Array.from(elems).filter(el =>
    /People*/.test(el.getAttribute('aria-label'))
);
if (matched && matched.length == 1) {
    matched[0].click();
}