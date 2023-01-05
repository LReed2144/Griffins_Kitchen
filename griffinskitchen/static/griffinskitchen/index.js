document.addEventListener('DOMContentLoaded', function() {
  
const button = document.querySelector('.button-like')

button.addEventListener('click', () => {
    button.classList.toggle('liked')
})

});

