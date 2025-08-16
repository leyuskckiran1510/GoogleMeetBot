// https://dom.spec.whatwg.org/#mutationrecord
container = document.querySelector('aside[aria-label="Side panel"]');
config = { attributes: false, childList: true, subtree: true };
window.__new_message = JSON.stringify({
    user:null,
    content:null,
    id:null,
})


CLASSES_ = { user: "poVWob", "content": "dTKtvb"}

if (container) {
    const observer = new MutationObserver((mutations)=>{
    user = null;
    content = null;
    msg_id = null;
    content_node = null;
    mutations= mutations.filter(x=>x.type=="childList");
    for(mutation of mutations){
        target = mutation.target;
        // CLASSES_.user
        if(target.className.match("poVWob")!=null){
            user = target.innerText;
        }
        if(target.getAttribute("data-message-id")!=null){
            msg_id = target.getAttribute("data-message-id")
            // CLASSES_.content
            msg_container = target.querySelector('[jsname="dTKtvb"]');
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
});
    observer.observe(container, { childList: true, subtree: true });
}
