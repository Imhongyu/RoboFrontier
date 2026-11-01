'use strict';
(() => {
  const form = document.querySelector('.filters');
  const family = document.querySelector('#family');
  const level = document.querySelector('#level');
  const arms = document.querySelector('#arms');
  const query = document.querySelector('#query');
  const cards = Array.from(document.querySelectorAll('.case'));
  function filter() {
    const needle = query.value.trim().toLowerCase();
    let count = 0;
    for (const card of cards) {
      const visible = (family.value === 'all' || card.dataset.family === family.value)
        && (level.value === 'all' || card.dataset.level === level.value)
        && (arms.value === 'all' || card.dataset.arms === arms.value)
        && card.id.includes(needle);
      card.hidden = !visible;
      count += Number(visible);
    }
    document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'task' : 'tasks'}`;
    document.querySelector('#empty').hidden = count !== 0;
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', filter);
  form.addEventListener('change', filter);
  form.addEventListener('reset', () => setTimeout(filter, 0));
  document.querySelectorAll('[data-family-filter]').forEach(link => {
    link.addEventListener('click', () => {
      form.reset();
      family.value = link.dataset.familyFilter;
      filter();
    });
  });
  cards.forEach(card => {
    card.querySelectorAll('[data-view]').forEach(button => {
      button.addEventListener('click', () => {
        const view = button.dataset.view;
        const image = card.querySelector('.image-link img');
        const path = `images/${card.id}-${view}.jpg`;
        image.src = path;
        image.alt = `Initial ${view === 'top' ? 'top' : 'front'} view of ${card.id}`;
        card.querySelector('.image-link').href = path;
        card.querySelectorAll('[data-view]').forEach(other => {
          other.setAttribute('aria-pressed', String(other === button));
        });
      });
    });
  });
  filter();
})();
