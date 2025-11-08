document.addEventListener("DOMContentLoaded", () => {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  const tbody = document.querySelector(".cart-body");
  const totalEl = document.querySelector(".cart-total-sum");

  tbody.addEventListener("click", async (e) => {
    const btn = e.target.closest(".btn-qty, .btn-remove");
    if (!btn) return;
    e.preventDefault();

    const action = btn.dataset.action;
    const id = btn.dataset.id;
    let url = "";
    if (action === "increase") url = `/add_to_cart/${id}`;
    else if (action === "decrease") url = `/decrease_quantity/${id}`;
    else if (action === "remove")   url = `/remove_from_cart/${id}`;
    else return;

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrfToken
        }
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      tbody.innerHTML = data.html;
      if (totalEl) totalEl.textContent = `${data.total} €`;
    } catch (err) {
      console.error("Cart update failed:", err);
    }
  });
});
