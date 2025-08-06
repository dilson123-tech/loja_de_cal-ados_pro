document.addEventListener("DOMContentLoaded", async () => {
  const spanTotal = document.getElementById("total-vendas");
  const spanQtd = document.getElementById("quantidade-total");
  const spanForma = document.getElementById("forma-mais-usada");
  const corpoTabela = document.getElementById("tabela-vendas");

  try {
    const resposta = await fetch("/api/vendas/resumo");
    const dados = await resposta.json();

    console.log("📊 Dados recebidos:", dados);

    // Atualiza os valores no painel
    spanTotal.innerText = `R$ ${dados.total_vendas.toFixed(2).replace(".", ",")}`;
    spanQtd.innerText = dados.quantidade_total;
    spanForma.innerText = dados.forma_pagamento_mais_usada || "-";

    // Preenche a tabela de vendas
    corpoTabela.innerHTML = ""; // limpa o "Carregando..."
    dados.vendas.forEach((venda) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${venda.cliente}</td>
        <td>${venda.produto}</td>
        <td>R$ ${venda.valor.toFixed(2).replace(".", ",")}</td>
        <td>${venda.forma_pagamento}</td>
        <td>${venda.data}</td>
      `;
      corpoTabela.appendChild(tr);
    });
  } catch (erro) {
    console.error("❌ Erro ao carregar dados do dashboard:", erro);
    spanTotal.innerText = "Erro";
    spanQtd.innerText = "Erro";
    spanForma.innerText = "Erro";
    corpoTabela.innerHTML = "<tr><td colspan='5'>Erro ao carregar vendas.</td></tr>";
  }
});
