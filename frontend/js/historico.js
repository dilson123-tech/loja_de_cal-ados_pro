document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("historico-container");

  try {
    const resposta = await fetch("http://127.0.0.1:8000/api/vendas/resumo");
    const dados = await resposta.json();

    // 🐞 Adiciona esse log para vermos a resposta da API no console do navegador
    console.log(dados); 

    const vendas = dados.vendas;

    if (vendas.length === 0) {
      container.innerHTML = "<p>⚠️ Nenhuma venda registrada ainda.</p>";
      return;
    }

    vendas.forEach((venda) => {
      const div = document.createElement("div");
      div.classList.add("produto");
      div.innerHTML = `
        <h3>Venda #${venda.id}</h3>
        <p><strong>Produto:</strong> ${venda.produto}</p>
        <p><strong>Valor:</strong> R$ ${venda.valor.toFixed(2)}</p>
        <p><strong>Data:</strong> ${venda.data}</p>
        <hr />
      `;
      container.appendChild(div);
    });
  } catch (error) {
    container.innerHTML = "<p>❌ Erro ao carregar o histórico.</p>";
    console.error("Erro:", error);
  }
});
