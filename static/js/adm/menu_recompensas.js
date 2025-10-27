document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("modalCadastroRecompensa");
    const btnAbrir = document.getElementById("abrirModalCadastro");
    const btnFechar = document.getElementById("fecharModalCadastro");
    const form = document.getElementById("formRecompensa");
    const modalTitle = document.getElementById("modalTitle");
    const recompensaId = document.getElementById("recompensaId");

    // Abrir modal para cadastro
    if (btnAbrir) {
        btnAbrir.addEventListener('click', function() {
            modal.style.display = "flex";
            modalTitle.textContent = "Cadastrar Nova Recompensa";
            form.action = "/admin/cadastrarrecompensa";
            recompensaId.value = "";
            form.reset();
            this.blur();
        });
    }

    // Fechar modal pelo X
    if (btnFechar) {
        btnFechar.addEventListener('click', function() {
            modal.style.display = "none";
        });
    }

    // Fechar modal clicando fora
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Fechar modal após envio
    if (form) {
        form.addEventListener('submit', function() {
            modal.style.display = "none";
        });
    }
});

// Abrir modal de edição
function abrirModalEdicao(id, tipo, descricao, valor, link, vagas, data_expiracao) {
    const modal = document.getElementById("modalCadastroRecompensa");
    const form = document.getElementById("formRecompensa");
    const modalTitle = document.getElementById("modalTitle");
    const recompensaId = document.getElementById("recompensaId");

    modal.style.display = "flex";
    modalTitle.textContent = "Editar Recompensa";
    form.action = "/admin/editarrecompensa/" + id;

    recompensaId.value = id;
    document.getElementById("tipo").value = tipo || '';
    document.getElementById("descricao").value = descricao || '';
    document.getElementById("valor").value = valor || '';
    document.getElementById("link").value = link || '';
    document.getElementById("vagas").value = vagas || '';
    document.getElementById("data_expiracao").value = data_expiracao ? data_expiracao.split(" ")[0] : '';
}

// Confirmar exclusão
function confirmarExcluir(event) {
    const confirmar = confirm("Tem certeza que deseja excluir esta recompensa?");
    if (!confirmar) {
        event.preventDefault();
    }
}
