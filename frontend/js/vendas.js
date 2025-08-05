document.addEventListener("DOMContentLoaded", () => {
  const inputCodigo = document.getElementById("codigo-produto");
  const inputNome = document.getElementById("nome-produto");
  const botaoBuscar = document.getElementById("buscar-produto");
  const resultadoDiv = document.getElementById("resultado-produto");
  const carrinhoTabela = document.querySelector("#lista-carrinho tbody");
  const selectPagamento = document.getElementById("forma-pagamento");
  const camposDiv = document.getElementById("campos-pagamento");
  const botaoFinalizar = document.getElementById("finalizar-venda");


  let carrinho = [];

  // 🔍 Buscar produto
  async function buscarProduto() {
    const codigo = inputCodigo.value.trim();
    const nome = inputNome.value.trim();
    let url = "/api/produtos/buscar";

    if (codigo) {
      url += `?codigo=${codigo}`;
    } else if (nome) {
      url += `?nome=${nome}`;
    } else {
      alert("Informe o código ou nome do produto.");
      return;
    }

    try {
      const resposta = await fetch(url);
      if (!resposta.ok) throw new Error("Produto não encontrado");
      const produto = await resposta.json();
      console.log("🔎 Produto retornado:", produto);


      resultadoDiv.innerHTML = "";

      const nomeEl = document.createElement("p");
      nomeEl.innerHTML = `<strong>Produto:</strong> ${produto.nome}`;

      const precoEl = document.createElement("p");
      precoEl.innerHTML = `<strong>Preço:</strong> R$ ${produto.preco.toFixed(2)}`;

      const botao = document.createElement("button");
      botao.textContent = "Adicionar ao Carrinho";
      botao.classList.add("btn-verde");
      botao.addEventListener("click", () => adicionarAoCarrinho(produto));

      resultadoDiv.appendChild(nomeEl);
      resultadoDiv.appendChild(precoEl);
      resultadoDiv.appendChild(botao);
    } catch (erro) {
      resultadoDiv.innerHTML = "<p style='color:red;'>Produto não encontrado.</p>";
    }
  }

  // ➕ Adicionar produto ao carrinho
  function adicionarAoCarrinho(produto) {
  carrinho.push({ 
    ...produto, 
    quantidade: 1,
    produto_id: produto.id || produto.produto_id  // 👈 garante o ID pro backend
  });
  atualizarCarrinho();
}


  // 🧺 Atualizar carrinho visualmente
  function atualizarCarrinho() {
    carrinhoTabela.innerHTML = "";
    carrinho.forEach((item, index) => {
      const linha = document.createElement("tr");
      linha.innerHTML = `
        <td>${item.nome}</td>
        <td>R$ ${item.preco.toFixed(2)}</td>
        <td><button onclick="removerItem(${index})">Remover</button></td>
      `;
      carrinhoTabela.appendChild(linha);
    });

    // Atualiza total
    const total = carrinho.reduce((soma, item) => soma + item.preco, 0);
    document.getElementById("total").innerText = total.toFixed(2);
  }

  // ❌ Remover item do carrinho
  window.removerItem = function(index) {
    carrinho.splice(index, 1);
    atualizarCarrinho();
  };

  // 💳 Forma de pagamento dinâmica
  selectPagamento.addEventListener("change", () => {
    const forma = selectPagamento.value;
    camposDiv.innerHTML = "";

    const totalSpan = document.getElementById("total");
    let totalCompra = 0;

    if (totalSpan) {
      const totalTexto = totalSpan.innerText.replace(",", ".") || "0.00";
      totalCompra = parseFloat(totalTexto);
    }

    if (forma === "Cartão de Crédito") {
      let opcoes = "";
      for (let i = 1; i <= 12; i++) {
        const valorParcela = (totalCompra / i).toFixed(2).replace(".", ",");
        opcoes += `<option value="${i}">${i}x de R$ ${valorParcela}</option>`;
      }

      camposDiv.innerHTML = `
        <label for="numero-cartao">Número do Cartão:</label>
        <input type="text" id="numero-cartao" required />

        <label for="validade">Validade:</label>
        <input type="text" id="validade" placeholder="MM/AA" required />

        <label for="cvv">CVV:</label>
        <input type="text" id="cvv" required />

        <label for="parcelas">Parcelas:</label>
        <select id="parcelas" required>${opcoes}</select>
      `;
    } else if (forma === "Cartão de Débito") {
      camposDiv.innerHTML = `
        <label for="numero-cartao">Número do Cartão:</label>
        <input type="text" id="numero-cartao" required />

        <label for="validade">Validade:</label>
        <input type="text" id="validade" placeholder="MM/AA" required />

        <label for="cvv">CVV:</label>
        <input type="text" id="cvv" required />
      `;
    } else if (forma === "PIX") {
      camposDiv.innerHTML = `
        <p>Escaneie o QR Code abaixo:</p>
        <img src="/static/img/qr-pix.png" alt="QR Code PIX" />
      `;
    }
  });

  // 🎯 Buscar com Enter
  inputCodigo.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      buscarProduto();
    }
  });
  inputNome.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      buscarProduto();
    }
  });

  botaoBuscar.addEventListener("click", buscarProduto);

  // ✅ Finalizar compra (dentro do DOMContentLoaded)
  botaoFinalizar.addEventListener("click", async () => {
  const nome = document.getElementById("nome").value.trim();
  const cpf = document.getElementById("cpf").value.trim();
  const endereco = document.getElementById("endereco").value.trim();
  const formaPagamento = document.getElementById("forma-pagamento").value;
  const total = parseFloat(document.getElementById("total").innerText.replace("R$", "").replace(",", "."));

  if (!nome || !cpf || !endereco || carrinho.length === 0) {
    alert("Preencha todos os dados do cliente e adicione produtos!");
    return;
  }

 const vendaData = {
  cliente: {
    nome: nome,
    cpf: cpf,
    endereco: endereco,
  },
  pagamento: {
    forma: formaPagamento,
    numero_cartao: document.getElementById("numero-cartao")?.value || "",
    validade: document.getElementById("validade")?.value || "",
    cvv: document.getElementById("cvv")?.value || "",
  },
 produtos: carrinho.map(p => ({
  produto_id: p.id || p.produto_id,
  quantidade: p.quantidade
})),
  total: total
};
 

  try {
   console.log("🧺 Conteúdo do carrinho:", JSON.stringify(carrinho, null, 2));
   console.log("📦 Enviando vendaData:", JSON.stringify(vendaData, null, 2));

  const resposta = await fetch("/api/vendas", {
     method: "POST",
     headers: {
       "Content-Type": "application/json",
  },
  body: JSON.stringify(vendaData),
});


    if (!resposta.ok) {
     const erroDetalhado = await resposta.json();
     throw new Error(JSON.stringify(erroDetalhado));

    }

    alert("✅ Venda registrada com sucesso!");
    location.reload(); // limpa tudo

} catch (erro) {
  console.error("⛔ Erro ao registrar a venda:", erro);

  try {
    // Verifica se é uma resposta do fetch (Response) e tenta extrair JSON
    if (erro instanceof Response && erro.headers.get("content-type")?.includes("application/json")) {
      const erroDetalhado = await erro.json();
      if (Array.isArray(erroDetalhado.detail)) {
        const mensagens = erroDetalhado.detail.map(e => `• ${e.msg}`).join("\n");
        alert("❌ Erro ao registrar venda:\n" + mensagens);
      } else {
        alert("❌ Erro ao registrar venda:\n" + erroDetalhado.detail);
      }
    } else if (erro instanceof Error) {
      alert("❌ Erro inesperado:\n" + erro.message);
    } else {
      alert("❌ Erro inesperado:\n" + JSON.stringify(erro, null, 2));
    }
  } catch (e) {
    alert("❌ Erro ao processar a falha:\n" + (e.message || "Erro desconhecido"));
  }
}





});


});
