document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".add-btn");

  buttons.forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const dishId = btn.getAttribute("data-dish-id");
      const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

      const response = await fetch(`/add_to_cart/${dishId}`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrfToken
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) showNotification(data.message);
      } else {
        console.error("Failed to add to cart:", response.status);
      }
    });
  });

  function showNotification(message) {
    const notif = document.createElement("div");
    notif.className = "cart-notification";
    notif.textContent = message;
    document.body.appendChild(notif);
    setTimeout(() => notif.classList.add("visible"), 50);
    setTimeout(() => notif.classList.remove("visible"), 2000);
    setTimeout(() => notif.remove(), 2500);
  }
});
