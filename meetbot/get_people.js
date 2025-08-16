// using aria label instead of classes,
// as the classes looks dynamically generated
// and, can cause breakage later, so avoiding that

// show the people list
let elems = document.querySelectorAll('button[aria-label][aria-expanded="false"]');
let matched = Array.from(elems).filter(el =>
    /People*/.test(el.getAttribute('aria-label'))
);
if (matched && matched.length == 1) {
    matched[0].click();  
}

__participants = []
// wait for few miliseconds to
// let the people div to render
setTimeout(() => {
    let people_div = document.querySelector('div[aria-label="Participants"]');
    people_div.querySelectorAll('div[data-participant-id]').forEach(
        x => {
            __participants.push(x.querySelector("span")?.innerText);
        })
}, 100)
window.__participants = JSON.stringify(__participants)

// hide the list
let elems = document.querySelectorAll('button[aria-label][aria-expanded="true"]');
let matched = Array.from(elems).filter(el =>
    /People*/.test(el.getAttribute('aria-label'))
);
if (matched && matched.length == 1) {
    matched[0].click();  
}
