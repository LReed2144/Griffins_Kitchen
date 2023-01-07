document.addEventListener('DOMContentLoaded', function() {
  
const button = document.querySelector('.button-like')

button.addEventListener('click', () => {
    button.classList.toggle('liked')
})

function build_paginator(addon,page,num_pages) {
    page_list = document.getElementById('pagination');
    page_list.innerHTML="";

    const previous = document.createElement('li');
    if(page==1){
        previous.className = "page-item disabled";    
    } else {
        previous.className = "page-item";    
        previous.addEventListener('click', () => load_posts(addon,page-1));
    }   
    
    //add previous page
    const page_a_previous = document.createElement('a');
    page_a_previous.className="page-link";

    page_a_previous.href="#";
    page_a_previous.innerHTML="Previous";
    previous.append(page_a_previous);    
    page_list.append(previous);
    
    
    for (let item=1; item<=num_pages; item++) {
        const page_icon = document.createElement('li');        
        if(item==page) {
            page_icon.className = "page-item active";
        } else {
            page_icon.className = "page-item";    
            page_icon.addEventListener('click', () => load_posts(addon,item));
        }        
        const page_a = document.createElement('a');
        page_a.className="page-link";
        page_a.href="#";
        page_a.innerHTML=item;
        page_icon.append(page_a);

        page_list.append(page_icon);
    }
    
    //add next page
    const next = document.createElement('li');        
    if(page==num_pages){
        next.className = "page-item disabled";    
    } else {
        next.className = "page-item";    
        next.addEventListener('click', () => load_posts(addon,page+1));
    }   
    const page_a_next = document.createElement('a');
    page_a_next.className="page-link"; 
    page_a_next.href="#";
    page_a_next.innerHTML="Next";
    next.append(page_a_next);
    page_list.append(next);
    
}



});

