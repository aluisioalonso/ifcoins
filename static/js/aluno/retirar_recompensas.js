let saldo = parseFloat("{{ aluno.saldo if aluno else 0 }}");

function comprarRecompensa(btn) {
    const card = btn.closest('.recompensa-card');
    const id = card.dataset.id;
    const valor = parseFloat(card.dataset.valor);
    let vagas = parseInt(card.dataset.vagas);

    if (vagas <= 0) {
        alert("Essa recompensa já esgotou!");
        return;
    }

    if (valor > saldo) {
        alert("Você não possui IFCOINS suficientes para comprar essa recompensa!");
        return;
    }

    // Requisição POST para o backend
    fetch("/aluno/comprar_recompensa", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({recompensa_id: id})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Compra realizada com sucesso!");
            saldo -= valor;
            vagas -= 1;
            card.dataset.vagas = vagas;
            card.querySelector('.vagas').innerText = vagas;

            if (vagas <= 0) {
                card.classList.add('esgotada');
            }
        } else {
            alert(data.message);
        }
    })
    .catch(err => console.error(err));
}
