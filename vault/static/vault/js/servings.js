(function () {
  const slider = document.getElementById("servings-slider");
  const label = document.getElementById("servings-label");
  const baseServingsEl = document.getElementById("base-servings");
  const rows = document.querySelectorAll("[data-qty]");

  if (!slider || !label || !baseServingsEl) return;

  const baseServings = parseFloat(baseServingsEl.dataset.base);

  function update() {
    const current = parseFloat(slider.value);
    label.textContent = String(current);

    rows.forEach((row) => {
      const baseQty = parseFloat(row.dataset.qty);
      const scaled = (baseQty * current) / baseServings;
      row.textContent = scaled.toFixed(2);
    });
  }

  slider.addEventListener("input", update);
  update();
})();
