function abrirModal() {
    document.getElementById('modal').classList.remove('hidden');
}

function fecharModal() {
    document.getElementById('modal').classList.add('hidden');
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        fecharModal();
    }
});

function toggleMenu() {
    const menu = document.getElementById('menu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

window.addEventListener('click', function(event) {
    const menu = document.getElementById('menu');
    const toggle = document.querySelector('.menu-toggle');
    if (!menu.contains(event.target) && !toggle.contains(event.target)) {
        menu.style.display = 'none';
    }
});
function abrirAba(aba) {
    const abaAcoes = document.getElementById('aba-acoes');
    const abaPessoais = document.getElementById('aba-pessoais');

    if (aba === 'acoes') {
        abaAcoes.classList.remove('hidden');
        abaPessoais.classList.add('hidden');
    } else if (aba === 'pessoais') {
        abaPessoais.classList.remove('hidden');
        abaAcoes.classList.add('hidden');
    }
}
function toggleMenu() {
    const menu = document.getElementById("menu-opcoes");
    menu.classList.toggle("hidden");
}


function abrirModalPessoais() {
    document.getElementById("modal-pessoais").style.display = "block";
    document.getElementById("menu-opcoes").classList.add("hidden");
}

function fecharModalPessoais() {
    document.getElementById("modal-pessoais").style.display = "none";
}


