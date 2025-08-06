document.addEventListener("DOMContentLoaded", async () => {
  const spanTotal = document.getElementById("total-vendas");
  const spanQtd = document.getElementById("quantidade-total");
  const spanForma = document.getElementById("pagamento-mais-usado");
  const corpoTabela = document.getElementById("tabela-vendas");

  if (!spanTotal || !spanQtd || !spanForma || !corpoTabela) {
    console.error("❌ Um ou mais elementos não foram encontrados no DOM");
    return;
  }

  try {
    const resposta = await fetch("/api/vendas/resumo");
    const resumo = await resposta.json();  

    spanTotal.innerText = `R$ ${resumo.total_vendas.toFixed(2).replace('.', ',')}`;
    spanQtd.innerText = resumo.quantidade_total;
    spanForma.innerText = resumo.forma_pagamento_mais_usada || '-';

    const vendas = resumo.vendas;

    if (Array.isArray(vendas)) {
      vendas.forEach((venda) => {
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
    } else {
      corpoTabela.innerHTML = "<tr><td colspan='5'>Nenhuma venda encontrada.</td></tr>";
    }

  } catch (erro) {
    alert("Erro ao carregar dashboard: " + erro.message);
    console.error(erro);
  }
}); // ✅ FECHAMENTO QUE FALTAVA AQUI
