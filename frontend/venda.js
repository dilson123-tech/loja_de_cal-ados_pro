document.addEventListener("DOMContentLoaded", () => {
  const carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
  const container = document.getElementById("carrinho-container");
  const totalSpan = document.getElementById("total");
  const finalizarBtn = document.getElementById("finalizar-venda");

  if (carrinho.length === 0) {
    container.innerHTML = "<p>Carrinho vazio.</p>";
    finalizarBtn.disabled = true;
    return;
  }

  let total = 0;
  carrinho.forEach(produto => {
    const item = document.createElement("div");
    item.classList.add("produto-card");
    item.innerHTML = `
      <h3>${produto.nome}</h3>
      <p>Preço: R$ ${produto.preco.toFixed(2)}</p>
    `;
    container.appendChild(item);
    total += produto.preco;
  });

  totalSpan.textContent = `Total: R$ ${total.toFixed(2)}`;

  finalizarBtn.addEventListener("click", async () => {
    try {
      for (let produto of carrinho) {
        await fetch(`http://127.0.0.1:8000/api/produtos/${produto.id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ quantidade: produto.quantidade - 1 })
        });
      }

      alert("✅ Venda finalizada com sucesso!");
      localStorage.removeItem("carrinho");
      location.href = "index.html";
    } catch (error) {
      alert("❌ Erro ao finalizar a venda.");
      console.error(error);
    }
  });
});
