function abrirModal() {
    document.getElementById('modal').classList.remove('hidden');
}

function fecharModal() {
    document.getElementById('modal').classList.add('hidden');
}

function toggleMenu() {
    const menu = document.getElementById("menu-opcoes");
    menu.classList.toggle("hidden");
}

// Fechar modal clicando fora dela
window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal');
    const modalPessoais = document.getElementById('modal-pessoais');

    if (event.target === modal) {
        fecharModal();
    }
    if (event.target === modalPessoais) {
        fecharModalPessoais();
    }
});

// Modal de Informações Pessoais
function abrirModalPessoais() {
    document.getElementById("modal-pessoais").classList.remove("hidden");
    document.getElementById("menu-opcoes").classList.add("hidden");
}

function fecharModalPessoais() {
    document.getElementById("modal-pessoais").classList.add("hidden");
}
