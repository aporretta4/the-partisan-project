(() => {
  let cards = document.querySelectorAll('[data-purpose="example-card"]');
  cards.forEach(card => {
    let card_button = card.querySelector('button[data-purpose="example-card-flipper"]');
    card_button.addEventListener('click', (event) => {
      let hidden_card = card.querySelector('.tweet.hide');
      if (hidden_card != null) {
        hidden_card.classList.add('show');
        hidden_card.classList.remove('hide');
        if (hidden_card.nextElementSibling == null) {
          event.target.classList.add('hide');
        }
      }
    });
  });
})();