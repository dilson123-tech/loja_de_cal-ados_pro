document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("produtos-container");
  const modal = document.getElementById("modal-venda");
  const fecharModal = document.getElementById("fechar-modal");
  const formVenda = document.getElementById("form-venda");

  async function carregarProdutos() {
    try {
      const res = await fetch("/api/produtos");
      const produtos = await res.json();

      produtos.forEach(produto => {
        const card = document.createElement("div");
        card.className = "produto-card";
        card.innerHTML = `
          <h3>${produto.nome}</h3>
          <p>Preço: R$ ${produto.preco.toFixed(2)}</p>
          <p>Estoque: ${produto.quantidade}</p>
          <button onclick="abrirModal(${produto.id})">Vender</button>
        `;
        container.appendChild(card);
      });
    } catch (err) {
      console.error("Erro ao carregar produtos:", err);
    }
  }

  window.abrirModal = (produtoId) => {
    document.getElementById("produto_id").value = produtoId;
    modal.classList.remove("hidden");
  };

  fecharModal.onclick = () => {
    modal.classList.add("hidden");
  };

  formVenda.onsubmit = async (e) => {
    e.preventDefault();

    const dados = {
      produto_id: parseInt(document.getElementById("produto_id").value),
      quantidade_vendida: parseInt(document.getElementById("quantidade").value),
      cliente_nome: document.getElementById("cliente_nome").value,
      cliente_cpf: document.getElementById("cliente_cpf").value,
      cliente_endereco: document.getElementById("cliente_endereco").value,
      forma_pagamento: document.getElementById("forma_pagamento").value
    };

    try {
      const res = await fetch("/api/vendas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
      });

      if (res.ok) {
        alert("✅ Venda realizada com sucesso!");
        location.reload(); // atualiza estoque
      } else {
        const erro = await res.json();
        alert("Erro: " + erro.detail);
      }
    } catch (err) {
      console.error("Erro na venda:", err);
      alert("Erro ao registrar a venda.");
    }
  };

  carregarProdutos();
});
