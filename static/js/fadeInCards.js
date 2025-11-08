window.addEventListener("load", () => {
  const cards = document.querySelectorAll(".menu-card");

  cards.forEach((card, index) => {
    // сначала убираем карточку из видимости
    card.style.opacity = "0";
    card.style.transform = "translateY(40px)";
    card.style.transition = "none";
  });

  // небольшой таймаут, чтобы браузер успел применить стартовые стили
  setTimeout(() => {
    cards.forEach((card, index) => {
      const delay = index * 150; // 0.15s между карточками
      setTimeout(() => {
        card.style.transition = "opacity 0.8s ease, transform 0.8s ease";
        card.style.opacity = "1";
        card.style.transform = "translateY(0)";
      }, delay);
    });
  }, 50); // ← даём браузеру 50 мс, чтобы зафиксировать начальное состояние
});
