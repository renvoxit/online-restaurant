window.addEventListener("load", () => {
  const cards = document.querySelectorAll(".menu-card");

  cards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(40px)";
    card.style.transition = "none";
  });

  setTimeout(() => {
    cards.forEach((card, index) => {
      const delay = index * 150; // 0.15s
      setTimeout(() => {
        card.style.transition = "opacity 0.8s ease, transform 0.8s ease";
        card.style.opacity = "1";
        card.style.transform = "translateY(0)";
      }, delay);
    });
  }, 50); 
});
