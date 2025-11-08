console.log("cart_links.js connected!");

document.addEventListener("DOMContentLoaded", () => {
  console.log("cart_links.js loaded!");

  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  document.querySelectorAll(".btn-qty, .btn-remove").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault(); // блокируем переход по ссылке
      const action = btn.dataset.action;
      const id = btn.dataset.id;

      let url;
      if (action === "increase") url = `/add_to_cart/${id}`;
      else if (action === "decrease") url = `/decrease_quantity/${id}`;
      else if (action === "remove") url = `/remove_from_cart/${id}`;

      try {
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken
          }
        });

        if (res.ok) {
          const data = await res.json();
          updateCartUI(data.cart);
        } else {
          console.error("Request failed:", res.status);
        }
      } catch (err) {
        console.error("Fetch error:", err);
      }
    });
  });

  function updateCartUI(cart) {
    const tbody = document.querySelector(".cart-table tbody");
    tbody.innerHTML = "";

    if (!cart.length) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;">Your cart is empty.</td></tr>`;
    } else {
      cart.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${item.name}</td>
          <td>${item.quantity}</td>
          <td>${(item.price * item.quantity).toFixed(2)} €</td>
          <td class="actions">
            <a href="#" class="btn-qty" data-action="decrease" data-id="${item.id}">−</a>
            <a href="#" class="btn-qty" data-action="increase" data-id="${item.id}">+</a>
            <a href="#" class="btn-remove" data-action="remove" data-id="${item.id}">✖</a>
          </td>`;
        tbody.appendChild(row);
      });
    }

    // обновляем общую сумму
    const total = cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
    document.querySelector(".cart-total-sum").textContent = `${total.toFixed(2)} €`;
  }
});
