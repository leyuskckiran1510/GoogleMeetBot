// https://dom.spec.whatwg.org/#mutationrecord
let container = document.querySelector('aside[aria-label="Side panel"]');
let config = { attributes: false, childList: true, subtree: true };
window.__new_message = JSON.stringify({
    user:null,
    content:null,
    id:null,
})


let CLASSES_ = { user: "poVWob", "content": "dTKtvb"}

let mutation_callback = (mutations)=>{
    let user = null;
    let content = null;
    let msg_id = null;
    let content_node = null;
    mutations= mutations.filter(x=>x.type=="childList");
    for(mutation of mutations){
        let target = mutation.target;
        // CLASSES_.user
        if(target.className.match("poVWob")!=null){
            user = target.innerText;
        }
        if(target.getAttribute("data-message-id")!=null){
            msg_id = target.getAttribute("data-message-id")
            // CLASSES_.content
            let msg_container = target.querySelector('[jsname="dTKtvb"]');
            if(msg_container){
                content = msg_container.innerText;
                content_node  = target;
            }
        }
        if(user && content)break;
    }
    // if message appear frequently
    // then they are nested under same user,
    // so, find the parent for it's name
    if(user==null && content){
        user = content_node.parentNode?.parentNode?.querySelector(".poVWob").innerText;
    }
    if(content){
        window.__new_message = JSON.stringify({
            user:user,
            content:content,
            id:msg_id,
        })
    }
}
if (container) {
    const observer = new MutationObserver(mutation_callback);
    observer.observe(container, { childList: true, subtree: true });
}
