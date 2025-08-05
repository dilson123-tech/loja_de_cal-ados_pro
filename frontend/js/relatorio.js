document.addEventListener("DOMContentLoaded", () => {
  const resumoEl = document.getElementById("resumo");
  const tabelaEl = document.getElementById("tabela-vendas");

  fetch("http://127.0.0.1:8000/api/vendas/resumo")
    .then(response => response.json())
    .then(dados => {
      resumoEl.innerHTML = `
        <strong>Total de Vendas:</strong> ${dados.total_vendas}<br>
        <strong>Total Arrecadado:</strong> R$ ${dados.total_arrecadado.toFixed(2)}
      `;

      const tabela = document.createElement("table");
      tabela.innerHTML = `
        <tr>
          <th>ID</th>
          <th>Produto</th>
          <th>Valor</th>
          <th>Data</th>
        </tr>
      `;

      dados.vendas.forEach(venda => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
          <td>${venda.id}</td>
          <td>${venda.produto}</td>
          <td>R$ ${venda.valor.toFixed(2)}</td>
          <td>${venda.data}</td>
        `;
        tabela.appendChild(linha);
      });

      tabelaEl.appendChild(tabela);
    })
    .catch(error => {
      resumoEl.textContent = "Erro ao carregar o relatório.";
      console.error(error);
    });
});
