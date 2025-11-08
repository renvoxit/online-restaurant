document.addEventListener("mousemove", e => {
  const hero = document.querySelector(".hero");
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;
  hero.style.background = `radial-gradient(circle at ${x * 100}% ${y * 100}%, #0d2019, #0b0f0f 70%)`;
});
