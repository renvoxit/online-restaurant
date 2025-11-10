function showNotification(message) {
  const notif = document.createElement("div");
  notif.className = "bottom-notif";
  notif.textContent = message;
  document.body.appendChild(notif);

  setTimeout(() => {
    notif.classList.add("show");
  }, 50);

  setTimeout(() => {
    notif.classList.remove("show");
    setTimeout(() => notif.remove(), 400);
  }, 3000);
}

// Подключаемся к формам обновления статуса
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".inline-form").forEach(form => {
    form.addEventListener("submit", async e => {
      e.preventDefault();
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form)
      });
      if (res.ok) showNotification("Status updated ✓");
      else showNotification("Something went wrong");
    });
  });
});
