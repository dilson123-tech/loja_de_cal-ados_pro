document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("produtos-container");

  fetch("http://127.0.0.1:8000/api/produtos")
    .then(response => {
      if (!response.ok) throw new Error("Erro ao buscar produtos");
      return response.json();
    })
    .then(produtos => {
      if (produtos.length === 0) {
        container.innerHTML = "<p>Nenhum produto encontrado.</p>";
        return;
      }

      produtos.forEach(produto => {
        const card = document.createElement("div");
        card.classList.add("produto-card");
        card.innerHTML = `
          <h3>${produto.nome}</h3>
          <p><strong>Preço:</strong> R$ ${produto.preco.toFixed(2)}</p>
          <p><strong>Qtd:</strong> ${produto.quantidade}</p>
          <p>${produto.descricao || "Sem descrição"}</p>
          <button class="btn-comprar" data-id="${produto.id}">🛒 Comprar</button>
        `;
        container.appendChild(card);
      });

      // Adiciona ação ao botão
      const botoesComprar = document.querySelectorAll(".btn-comprar");
      botoesComprar.forEach(btn => {
        btn.addEventListener("click", (e) => {
          const id = e.target.dataset.id;
          const produtoSelecionado = produtos.find(p => p.id == id);
          alert(`Produto "${produtoSelecionado.nome}" adicionado ao carrinho!`);
          // Aqui a gente pode salvar no localStorage depois
        });
      });
    })
    .catch(error => {
      container.innerHTML = `<p style="color:red;">Erro: ${error.message}</p>`;
    });
});
