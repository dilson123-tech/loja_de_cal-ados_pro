document.addEventListener("DOMContentLoaded", async () => {
  try {
    const corpoTabela = document.querySelector("tbody");
    const spanTotal = document.getElementById('total-vendas');
    const spanQtd = document.getElementById('quantidade-total');
    const spanForma = document.getElementById('pagamento-mais-usado');

    const resposta = await fetch('/api/vendas');
    const dados = await resposta.json();

    console.log('📊 É array?', Array.isArray(dados.vendas), dados);

    spanTotal.innerText = `R$ ${dados.total_vendas.toFixed(2)}`;
    spanQtd.innerText = dados.quantidade_total;
    spanForma.innerText = dados.forma_pagamento_mais_usada;

    if (Array.isArray(dados.vendas)) {
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
    } else {
      console.error("❌ 'vendas' não é um array:", dados.vendas);
      corpoTabela.innerHTML = "<tr><td colspan='5'>Nenhuma venda encontrada</td></tr>";
    }

  } catch (erro) {
    alert("Erro ao carregar dashboard: " + erro.message);
    console.error(erro);
  }
});
