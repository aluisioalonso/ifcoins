const profileBtn = document.getElementById('open-profile');
const profileModal = document.getElementById('profile-modal');
const closeProfile = document.getElementById('close-profile');

if (profileBtn && profileModal) {
  // Alterna o modal ao clicar no botão
  profileBtn.addEventListener('click', (event) => {
    profileModal.classList.toggle('hidden');
    event.stopPropagation();
  });

  // Fecha ao clicar no botão fechar
  if (closeProfile) {
    closeProfile.addEventListener('click', () => {
      profileModal.classList.add('hidden');
    });
  }

  // Fecha ao clicar fora do conteúdo do modal
  window.addEventListener('click', (e) => {
    // se o alvo do clique for o próprio overlay (fundo), fecha
    if (e.target === profileModal) {
      profileModal.classList.add('hidden');
    }
  });

  // evita múltiplos closings caso haja outros listeners
  document.addEventListener('click', (event) => {
    if (!profileModal.contains(event.target) && event.target !== profileBtn) {
      if (!profileModal.classList.contains('hidden')) {
        profileModal.classList.add('hidden');
      }
    }
  });
} else {
  console.error("Erro: Elemento 'profile-modal' ou 'open-profile' não encontrado no DOM.");
}
```

---

Se quiser, posso também fornecer apenas os trechos alterados (por exemplo, só o CSS) para você colar no projeto; diga qual arquivo prefere.
