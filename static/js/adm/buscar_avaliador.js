document.addEventListener('DOMContentLoaded', () => {
  // Elementos
  const btnAbrirFiltro = document.getElementById('open-filtro-modal');
  const modalFiltro = document.getElementById('filtro-modal');
  const opcoesFiltro = document.querySelectorAll('.mini-btn-filtro');
  const botoesAcesso = document.querySelectorAll('.btn-acesso'); // se existir
  const campoBusca = document.getElementById('buscaAvaliador');

  const btnAbrirPerfil = document.getElementById('open-profile');
  const modalPerfil = document.getElementById('profile-modal');

  // Estado do filtro selecionado ('' = sem filtro / buscar por nome por default no backend)
  let filtroSelecionado = '';

  // ----- Funções utilitárias -----
  function closeFiltroIfOutside(target) {
    if (!modalFiltro.contains(target) && target !== btnAbrirFiltro) {
      modalFiltro.classList.add('hidden-filtro');
    }
  }

  function closePerfilIfOutside(target) {
    if (modalPerfil && !modalPerfil.contains(target) && target !== btnAbrirPerfil) {
      modalPerfil.classList.add('hidden');
    }
  }

  function realizarBusca() {
    const valor = campoBusca.value.trim();
    // monta a url conforme backend espera: /admin/buscaravaliador?filtro=...&q=...
    const params = new URLSearchParams();
    if (filtroSelecionado) params.set('filtro', filtroSelecionado);
    if (valor) params.set('q', valor);
    // mesmo se q estiver vazio, o backend mostra todos
    const url = `/admin/buscaravaliador?${params.toString()}`;
    window.location.href = url;
  }

  // ----- Eventos Filtro -----
  if (btnAbrirFiltro && modalFiltro) {
    btnAbrirFiltro.addEventListener('click', (e) => {
      e.stopPropagation(); // para não disparar document click que fecha
      modalFiltro.classList.toggle('hidden-filtro');
    });

    opcoesFiltro.forEach(opcao => {
      opcao.addEventListener('click', (event) => {
        event.preventDefault();
        filtroSelecionado = opcao.dataset.filtro || '';
        // feedback visual
        campoBusca.placeholder = filtroSelecionado ? `Buscar por ${filtroSelecionado}` : 'Digite o nome ou email...';

        // mostra botoes de acesso se existirem
        botoesAcesso.forEach(btn => btn.classList.remove('hidden-botoes-acesso'));

        // fecha o modal
        modalFiltro.classList.add('hidden-filtro');

        // realiza a busca usando o valor atual do input
        realizarBusca();
      });
    });

    document.addEventListener('click', (event) => {
      closeFiltroIfOutside(event.target);
    });
  }

  // ----- Eventos Perfil -----
  if (btnAbrirPerfil && modalPerfil) {
    btnAbrirPerfil.addEventListener('click', (e) => {
      e.stopPropagation();
      modalPerfil.classList.toggle('hidden');
    });

    document.addEventListener('click', (event) => {
      closePerfilIfOutside(event.target);
    });
  }

  // ----- Busca ao pressionar Enter -----
  if (campoBusca) {
    campoBusca.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        realizarBusca();
      }
    });
  }

  // ----- Remover avaliador (event delegation) -----
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.remove-btn');
    if (!btn) return;

    const email = btn.dataset.email;
    if (!email) return;

    if (!confirm(`Confirma remoção do avaliador ${email}?`)) return;

    // envia DELETE (fallback para POST)
    const url = `/admin/remover_avaliador/${encodeURIComponent(email)}`;
    fetch(url, { method: 'DELETE' })
      .then(async (resp) => {
        if (!resp.ok) {
          // tenta extrair json de erro
          let txt = await resp.text();
          throw new Error(txt || `Erro: ${resp.status}`);
        }
        return resp.json();
      })
      .then((data) => {
        // remove a linha da tabela se possível
        const tr = btn.closest('tr');
        if (tr) tr.remove();

        // se tabela ficou vazia, recarrega (ou mostra mensagem)
        const tbody = document.querySelector('.tabela-avaliadores tbody');
        if (tbody && tbody.children.length === 0) {
          // recarrega para que o template exiba a mensagem "Nenhum avaliador encontrado."
          window.location.reload();
        }
      })
      .catch(async (err) => {
        // fallback: tentar POST (alguns ambientes bloqueiam DELETE)
        try {
          const resp = await fetch(url, { method: 'POST' });
          if (resp.ok) {
            window.location.reload();
            return;
          }
        } catch (_) { /* ignore */ }

        alert('Falha ao remover avaliador. Tente novamente ou verifique o servidor.');
        console.error('Erro ao remover:', err);
      });
  });
});
