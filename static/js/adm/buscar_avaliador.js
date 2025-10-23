document.addEventListener('DOMContentLoaded', () => {
    // Referências dos elementos de Filtro
    const btnAbrirFiltro = document.getElementById('open-filtro-modal');
    const modalFiltro = document.getElementById('filtro-modal');
    const opcoesFiltro = document.querySelectorAll('.mini-btn-filtro');
    const botoesAcesso = document.querySelectorAll('.btn-acesso');
    const campoBusca = document.getElementById('buscaAvaliador');

    // Referências dos elementos de Perfil
    const btnAbrirPerfil = document.getElementById('open-profile');
    const modalPerfil = document.getElementById('profile-modal');

    // ===========================================
    // 1. LÓGICA DE VISIBILIDADE DOS BOTÕES DE AÇÃO
    // ===========================================

    opcoesFiltro.forEach(opcao => {
        opcao.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o link de navegar

            // Remove a classe que esconde os botões Habilitar/Desabilitar
            botoesAcesso.forEach(btn => {
                btn.classList.remove('hidden-botoes-acesso');
            });

            // Fecha o modal de filtro
            modalFiltro.classList.add('hidden-filtro');

            // Atualiza o placeholder do campo de busca (feedback visual)
            const filtroSelecionado = opcao.getAttribute('data-filtro');
            campoBusca.placeholder = `Busca por ${filtroSelecionado}`;

            console.log(`Filtro de busca ativo: ${filtroSelecionado}`);
        });
    });


    // ===========================================
    // 2. FUNCIONALIDADE DO MODAL DE FILTRO
    // ===========================================

    btnAbrirFiltro.addEventListener('click', () => {
        modalFiltro.classList.toggle('hidden-filtro');
    });

    // Fechar o modal ao clicar fora dele
    document.addEventListener('click', (event) => {
        const isClickInsideFiltro = modalFiltro.contains(event.target) || btnAbrirFiltro.contains(event.target);

        if (!isClickInsideFiltro) {
            modalFiltro.classList.add('hidden-filtro');
        }
    });

    // ===========================================
    // 3. FUNCIONALIDADE DO MODAL DE PERFIL
    // ===========================================

    if (btnAbrirPerfil && modalPerfil) {
        btnAbrirPerfil.addEventListener('click', () => {
            modalPerfil.classList.toggle('hidden');
        });

        // Fechar o modal de perfil ao clicar fora
        document.addEventListener('click', (event) => {
            const isClickInsidePerfil = modalPerfil.contains(event.target) || btnAbrirPerfil.contains(event.target);

            if (!isClickInsidePerfil) {
                modalPerfil.classList.add('hidden');
            }
        });
    }
});

const filtroBtn = document.getElementById('open-filtro-modal');
const filtroModal = document.getElementById('filtro-modal');
const campoBusca = document.getElementById('buscaAvaliador');

if (filtroBtn && filtroModal) {
  filtroBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    filtroModal.classList.toggle('hidden-filtro');
  });

  // Clicar nas opções de filtro
  document.querySelectorAll('.mini-btn-filtro').forEach((btn) => {
    btn.addEventListener('click', () => {
      const filtro = btn.dataset.filtro;
      const valor = campoBusca.value;

      // Redireciona com parâmetros de busca
      const url = `/admin/buscaravaliador?filtro=${filtro}&q=${encodeURIComponent(valor)}`;
      window.location.href = url;
    });
  });

  // Fecha o menu ao clicar fora
  document.addEventListener('click', (e) => {
    if (!filtroModal.contains(e.target) && e.target !== filtroBtn) {
      filtroModal.classList.add('hidden-filtro');
    }
  });
}
