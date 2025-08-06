document.addEventListener("DOMContentLoaded", async () => {
  const tabelaBody = document.getElementById("historico-container");
  const inputFiltro = document.getElementById("filtro-nome");

  let vendas = [];

  async function carregarHistorico() {
    try {
      const resposta = await fetch("/api/vendas/resumo");
      const dados = await resposta.json();

      vendas = dados.vendas || [];

      if (vendas.length === 0) {
        tabelaBody.innerHTML = "<tr><td colspan='6'>⚠️ Nenhuma venda registrada.</td></tr>";
        return;
      }

      exibirVendas(vendas);
    } catch (error) {
      console.error("Erro ao carregar histórico:", error);
      tabelaBody.innerHTML = "<tr><td colspan='6'>❌ Erro ao carregar histórico.</td></tr>";
    }
  }

  function exibirVendas(lista) {
    tabelaBody.innerHTML = "";

    lista.forEach((venda) => {
      const linha = document.createElement("tr");

      linha.innerHTML = `
        <td>${venda.cliente_nome}</td>
        <td>${venda.cliente_cpf}</td>
        <td>${venda.produto_nome}</td>
        <td>R$ ${venda.valor_total.toFixed(2)}</td>
        <td>${venda.forma_pagamento}</td>
        <td>${new Date(venda.criado_em).toLocaleString("pt-BR")}</td>
      `;

      tabelaBody.appendChild(linha);
    });
  }

  inputFiltro.addEventListener("input", () => {
    const termo = inputFiltro.value.toLowerCase();
    const filtradas = vendas.filter((venda) =>
      venda.cliente_nome.toLowerCase().includes(termo)
    );
    exibirVendas(filtradas);
  });

  carregarHistorico();
});
