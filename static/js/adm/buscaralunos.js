document.addEventListener('DOMContentLoaded', () => {
  const campoBusca = document.getElementById('buscaAluno'); // corrigido para alunos

  // ----- Busca ao pressionar Enter -----
  if (campoBusca) {
    campoBusca.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const valor = campoBusca.value.trim();
        const params = new URLSearchParams();
        if (valor) params.set('q', valor);
        window.location.href = `/admin/alunos?${params.toString()}`;
      }
    });
  }

  // ----- Remover aluno (event delegation) -----
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.remove-btn');
    if (!btn) return;

    const email = btn.dataset.email;
    if (!email) return;

    if (!confirm(`Confirma remoção do aluno ${email}?`)) return;

    const url = `/admin/remover_aluno/${encodeURIComponent(email)}`; // rota correta
    fetch(url, { method: 'DELETE' })
      .then(async (resp) => {
        if (!resp.ok) {
          let txt = await resp.text();
          throw new Error(txt || `Erro: ${resp.status}`);
        }
        return resp.json();
      })
      .then(() => {
        const tr = btn.closest('tr');
        if (tr) tr.remove();

        const tbody = document.querySelector('.tabela-avaliadores tbody');
        if (tbody && tbody.children.length === 0) {
          window.location.reload();
        }
      })
      .catch(async (err) => {
        // fallback POST
        try {
          const resp = await fetch(url, { method: 'POST' });
          if (resp.ok) {
            window.location.reload();
            return;
          }
        } catch (_) {}

        alert('Falha ao remover aluno. Tente novamente ou verifique o servidor.');
        console.error('Erro ao remover:', err);
      });
  });
});
